import logging
import os
import time
import traceback
import warnings
from datetime import datetime
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from libeq import (
    EqSolver,
    PotentiometryOptimizer,
    SolverData,
    # species_concentration,
    uncertanties,
    Flags
)
from libeq.excepts import DivergedIonicStrengthWarning
# from libeq.optimizers.potentiometry import ravel
from libeq.solver.solids_solver import _compute_saturation_index
from libeq.solver.solver_utils import _titration_background_ions_c

from workers_utils import _comp_info, _species_info


pd.set_option('display.max_rows', None)     # to display all rows.
pd.set_option('display.max_columns', None)  # to display all columns.
pd.set_option('display.width', None)        # to prevent line wrapping and allow full width display.
pd.set_option('display.max_colwidth', None)


# Main optimization routine worker and signals
class optimizeSignal(QObject):
    log = Signal(str)
    aborted = Signal(str)
    finished = Signal()
    result = Signal(object, str)


class optimizeWorker(QRunnable):
    def __init__(self, data_list: dict, debug: bool):
        super().__init__()
        self.signals = optimizeSignal()
        self.data = data_list
        self.debug = debug

    @Slot()
    def run(self):
        # If run with debug enabled create the logging istance
        def log_reporter(**kwargs):
            """
            Log out the result of each iteration.
            """
            iteration = kwargs['iteration']
            damping = kwargs['damping']
            chisq = kwargs['chisq']
            sigma = kwargs['sigma']
            gradient_norm = kwargs['gradient_norm']
            log_beta = kwargs['log_beta']
            stoich = kwargs['stoichiometry']
            labels = self.data['compModel']['Name'].values()

            out = self.signals.log.emit
            out(f"iteration = {kwargs['iteration']}")
            out(f"damping = {kwargs['damping']:.4e}, chisq = {kwargs['chisq']:.4f}, "
                f"gradient_norm = {kwargs['gradient_norm']:.4e}, rho = {kwargs['rho']:.4e}")
            out(f"sigma: {kwargs['sigma']:.4e} ({kwargs['exit_sigma']})")
            out(f"grad : {kwargs['exit_gradient_value']:.4e} ({kwargs['exit_gradient']})")
            out(f"step : {kwargs['exit_step_value']:.4e} ({kwargs['exit_step']})")

            if kwargs['any beta refined']:
                txt = "   # " + "".join(f"{comp:>5}" for comp in labels) + "     logβ       change  previous"
                out(txt)
                lgbeta = kwargs['log_beta']
                oldbeta = iter(kwargs['previous log beta'].tolist())
                stoich = kwargs['stoichiometry']
                increment = iter(kwargs['increment'].tolist())
                refined = [f'{next(increment):10.4f}{next(oldbeta):10.4f}' \
                           if _ else '' \
                           for _ in self.data['potentiometry_data']['beta_refine_flags']]
                for n, (lgb, st, rflag) in enumerate(zip(lgbeta, stoich, refined)):
                    out(f"{n:>4} { ''.join(f'{_:>5}' for _ in st)} {lgb:10.4f} {rflag}")

            if kwargs['any conc refined']:
                for n, ((c0, ct), titr) in enumerate(zip(kwargs['titration params'],
                                                         self.data['potentiometry_data']['titrations'])):
                    out(f"titr {n:<4}: ")
                    for c0v, c0f, comp in zip(c0, refine_indices(titr.c0_flags), labels):
                        if c0f:
                            out(f"c0[{comp}] {c0v:10.4f} {next(increment):10.4f}")
                    out('\n')
            out(80*'-')
            out('\n')

            # self.signals.log.emit(f"iteration #{iteration}")
            # self.signals.log.emit(f"sigma: {sigma}; chi-squared: {chisq}")
            # for a, lgb in zip(stoich, log_beta):
            #     stoich_txt = "".join(f"{n:>4}" for n in a)
            #     self.signals.log.emit(f"{stoich_txt}  {lgb:>10.4f}")
            # self.signals.log.emit("--" * 40 + "\n")

        if self.debug:
            log_path = Path.home().joinpath("pyes_logs")
            os.makedirs(log_path, exist_ok=True)
            date_time = datetime.now()
            log_file = log_path.joinpath(
                "pyes_" + date_time.strftime("%d_%m_%Y-%H:%M:%S") + ".log"
            )
            filehandler = logging.FileHandler(log_file)
            formatter = logging.Formatter("%(levelname)s:%(message)s")
            filehandler.setFormatter(formatter)
            log = logging.getLogger()  # root logger - Good to get it only once.
            for hdlr in log.handlers[:]:  # remove the existing file handlers
                if isinstance(hdlr, logging.FileHandler):
                    log.removeHandler(hdlr)
            log.addHandler(filehandler)
            log.setLevel(logging.DEBUG)

        # Start timer to time entire process
        start_time = time.time()

        self.signals.log.emit(r"### Beginning Calculation ###")
        self.signals.log.emit(r"Loading data...")

        self.data, ignored_soluble, ignored_solids = self._simplify_problem(self.data)
        if ignored_soluble:
            self.signals.log.emit(r"Found ignored soluble species:")
            self.signals.log.emit(f"{ignored_soluble}\n")

        if ignored_solids:
            self.signals.log.emit(r"Found ignored precipitable species:")
            self.signals.log.emit(f"{ignored_solids}\n")

        # load the data into the optimizer, catch errors that might invalidate the output
        try:
            # optimizer.fit(self.data)
            solver_data = SolverData.load_from_pyes(self.data)
        except Exception as e:
            if self.debug:
                self.signals.aborted.emit(
                    "".join(traceback.TracebackException.from_exception(e).format())
                )
            else:
                self.signals.aborted.emit(str(e))
            return None

        ok, errors = solver_data.model_ready
        if not ok:
            error_messages = "\n".join([
                f"  {field}: {msg}" for field, msg in errors.items()
            ])
            self.signals.aborted.emit(
                "Model not ready, please check the errors and try again:\n"
                + error_messages
            )
            return None

        # store mode of operation as selected in the software
        match self.data["dmode"]:
            case 0:
                ok, errors = solver_data.titration_ready
                if not ok:
                    error_messages = "\n".join([
                        f"  {field}: {msg}" for field, msg in errors.items()
                    ])
                    self.signals.aborted.emit(
                        "Titration data not complete, please check the errors and try again:\n"
                        + error_messages
                    )
                    return None
                mode = "titration"
            case 1:
                ok, errors = solver_data.distribution_ready
                if not ok:
                    error_messages = "\n".join([
                        f"  {field}: {msg}" for field, msg in errors.items()
                    ])
                    self.signals.aborted.emit(
                        "Distribution data not complete, please check the errors and try again:\n"
                        + error_messages
                    )
                    return None
                mode = "distribution"
            case 2:
                ok, errors = solver_data.potentiometry_ready
                if not ok:
                    error_messages = "\n".join([
                        f"  {field}: {msg}" for field, msg in errors.items()
                    ])
                    self.signals.aborted.emit(
                        "Potentiometry optimization data not complete, please check the errors and try again:\n"
                        + error_messages
                    )
                    return None
                mode = "potentiometry"

        # Store input info
        species_info, solids_info = _species_info(solver_data, mode, self.data["emode"])
        comp_info = _comp_info(solver_data, mode, self.data["emode"])

        self._storeResult(species_info, "species_info")
        self._storeResult(solids_info, "solids_info")
        self._storeResult(comp_info, "comp_info")

        self._storeResult(
            pd.DataFrame(
                np.clip(
                    np.hstack((np.eye(solver_data.nc), solver_data.stoichiometry)),
                    1,
                    np.inf,
                ),
                columns=solver_data.species_names,
            ),
            "stoichiometry",
            print_out=False,
        )
        self._storeResult(
            pd.DataFrame(
                np.clip(solver_data.solid_stoichiometry, 1, np.inf),
                columns=[name + "_(s)" for name in solver_data.solids_names],
            ),
            "solid_stoichiometry",
            print_out=False,
        )

        self.signals.log.emit(r"DATA LOADED!")

        if mode == "titration":
            means_to_report = ["I"]
            self.result_index = np.arange(solver_data.titration_opts.n_add) * (
                solver_data.titration_opts.v_increment
            )
            self.index_name = "V Add. [mL]"
            self.conc_sigma = np.tile(
                solver_data.titration_opts.c0_sigma, [self.result_index.size, 1]
            ) + (
                np.tile(self.result_index, [solver_data.nc, 1]).T
                * 1e-3
                * solver_data.titration_opts.ct_sigma
            )
            self.background_ions_concentration = _titration_background_ions_c(
                solver_data.titration_opts
            )
            self.signals.log.emit(
                r"Calculating species concentration for the simulated titration..."
            )
        elif mode == "distribution":
            means_to_report = ["I"]
            self.result_index = np.arange(
                solver_data.distribution_opts.initial_log,
                (
                    solver_data.distribution_opts.final_log
                    + solver_data.distribution_opts.log_increments
                ),
                solver_data.distribution_opts.log_increments,
            )
            self.index_name = (
                "p["
                + solver_data.components[
                    solver_data.distribution_opts.independent_component
                ]
                + "]"
            )
            self.conc_sigma = np.tile(
                solver_data.distribution_opts.c0_sigma, [self.result_index.size, 1]
            )
            self.background_ions_concentration = solver_data.distribution_opts.cback

            self.signals.log.emit(r"Calculating distribution of the species...")

        elif mode == "potentiometry":
            means_to_report = ["I", "Residual [V]"]
            self.signals.log.emit(
                r"Optimizing stability constants from potentiometric data..."
            )

            self.index_name = "V Add. [mL]"

            self.optimized_species = (
                np.array(solver_data.potentiometry_opts.beta_flags) == Flags.REFINE
            )

        start_time = time.time()
        self.signals.log.emit("--" * 40)

        with warnings.catch_warnings(record=True) as recorded_warnings:
            try:
                if mode == "potentiometry":
                    # (
                    #     x,
                    #     result,
                    #     log_beta,
                    #     b_error,
                    #     cor_matrix,
                    #     cov_matrix,
                    #     return_extra,
                    # ) = PotentiometryOptimizer(solver_data, reporter=log_reporter)
                    fit_result = PotentiometryOptimizer(solver_data, reporter=log_reporter)
                    x = fit_result['final variables']
                    concentrations = fit_result['free concentration']
                    log_beta = fit_result['final log beta']
                    b_error = fit_result['error log beta']
                    cor_matrix = fit_result['correlation']
                    cov_matrix = fit_result['covariance']

                    # Calculate elapsed time between start to finish
                    elapsed_time = round((time.time() - start_time), 5)

                    slices = fit_result['slices']
                    #idx_to_keep = return_extra["idx_to_keep"]

                    idx_to_keep = [tuple(n for n, f in enumerate(t.ignored) if not f) for t in solver_data.potentiometry_opts.titrations]

                    total_concentration = fit_result["total concentration"]

                    solver_data.log_beta_sigma = solver_data.log_beta_sigma.copy()
                    refined = [ f == Flags.REFINE for f in solver_data.potentiometry_opts.beta_flags ]
                    solver_data.log_beta_sigma[refined] = b_error[:]
                    # solver_data.log_beta_sigma = np.array(
                    #     list(
                    #         ravel(
                    #             solver_data.log_beta_sigma,
                    #             b_error,
                    #             solver_data.potentiometry_opts.beta_flags,
                    #         )
                    #     )
                    # )

                    log_ks = np.tile(
                        solver_data.log_ks, (total_concentration.shape[0], 1)
                    )

                    read_potential = fit_result["read emf"]
                    residuals = fit_result["residuals"]
                    calculated_potential = read_potential - residuals

                    px = -np.log10(fit_result['eactive'])
                    # px = np.concatenate([
                    #     (return_extra["calculated_potential"][i] - t.e0) / -t.slope
                    #     for i, t in enumerate(solver_data.potentiometry_opts.titrations)
                    # ])

                    self.result_index = np.concatenate([
                         t.v_add[~t.ignored]
                         for t in solver_data.potentiometry_opts.titrations
                    ])
                    # self.result_index = np.concatenate([
                    #     t.v_add[idx_to_keep[i]]
                    #     for i, t in enumerate(solver_data.potentiometry_opts.titrations)
                    # ])

                    self.result_index = [
                        self.result_index,
                        read_potential,
                        calculated_potential,
                        residuals,
                        px,
                        fit_result["weights"]
                        #np.diag(return_extra["weights"]),
                    ]

                    conc_sigma = []
                    # background_ions_conc = []
                    for i, t in enumerate(solver_data.potentiometry_opts.titrations):
                        v_aux = t.v_add[~t.ignored]
                        conc_sigma.append(
                            np.tile(t.c0_sigma, [v_aux.size, 1])
                            + (
                                np.tile(v_aux, [solver_data.nc, 1]).T
                                * 1e-3
                                * t.ct_sigma
                            )
                        )
                        # background_ions_conc.append(
                        #     _titration_background_ions_c(t, idx_to_keep[i])
                        # )
                    self.conc_sigma = np.concatenate(conc_sigma)
                    # self.background_ions_concentration = np.vstack(background_ions_conc)
                    self.background_ions_concentration = fit_result['background ion concentration']

                    self.index_name = [
                        "V Add. [mL]",
                        "Read Potential [V]",
                        "Calculated Potential [V]",
                        "Residual [V]",
                        "pX",
                        "Weight",
                    ]

                    optimized_constants = pd.DataFrame(
                        {
                            "Old logB": solver_data.log_beta[self.optimized_species],
                            "New logB": x,
                            "Std. Err.": b_error,
                        },
                        index=[
                            name
                            for name, flag in zip(
                                solver_data.species_names[solver_data.nc :],
                                solver_data.potentiometry_opts.beta_flags,
                            )
                            if flag == Flags.REFINE
                        ],
                    )

                    self._storeResult(optimized_constants, "optimized_constants")
                else:
                    (
                        result,
                        log_beta,
                        log_ks,
                        saturation_index,
                        total_concentration,
                    ) = EqSolver(solver_data, mode=mode)
                    slices = [0, result.shape[0]]
                    # Calculate elapsed time between start to finish
                    elapsed_time = round((time.time() - start_time), 5)
            except Exception as e:
                if self.debug:
                    msg = "".join(
                        traceback.TracebackException.from_exception(e).format()
                    )
                    if hasattr(e, "last_value"):
                        msg += f"\nLast value: {e.last_value}"
                    self.signals.aborted.emit(msg)

                else:
                    msg = str(e)

                    if hasattr(e, "last_value"):
                        msg += f"\nLast value: {e.last_value}"

                    self.signals.aborted.emit(msg)

                return None
            finally:
                if recorded_warnings:
                    self.signals.log.emit("Warnings occured during calculations:\n")
                    for w in recorded_warnings:
                        if isinstance(w.message, DivergedIonicStrengthWarning):
                            self.signals.log.emit(str(w.message))
                    self.signals.log.emit("\n")

        # concentrations = species_concentration(
        #     result, log_beta, solver_data.stoichiometry, full=True
        # )

        soluble_concentration = concentrations[
            :,
            np.r_[
                0 : solver_data.nc,
                (solver_data.nc + solver_data.nf) : (
                    solver_data.nc + solver_data.nf + solver_data.ns
                ),
            ],
        ]

        self.ionic_strength_dependence = solver_data.ionic_strength_dependence
        self.ionic_strength = 0.5 * (
            (
                soluble_concentration
                * (
                    np.concatenate([solver_data.charges, solver_data.species_charges])
                    ** 2
                )
            ).sum(axis=1, keepdims=True)
            + self.background_ions_concentration
        )

        soluble_concentration = self._create_df_result(
            soluble_concentration,
            columns=solver_data.species_names,
        ).rename_axis(columns="Species Conc. [mol/L]")

        solids_concentration_only = pd.DataFrame(
            concentrations[:, solver_data.nc : (solver_data.nc + solver_data.nf)],
            index=self.result_index,
            columns=solver_data.solids_names,
        ).rename_axis(columns="Solid Conc. [mol/L]")

        saturation_index = pd.DataFrame(
            _compute_saturation_index(
                concentrations[:, : solver_data.nc], log_ks, solver_data.solid_stoichiometry
            ),
            index=self.result_index,
            columns=["SI" + name for name in solver_data.solids_names],
        )

        precipitate_check = (
            (solids_concentration_only > 0)
            .replace({True: "*", False: ""})
            .set_axis(
                ["Prec." + name for name in solids_concentration_only.columns], axis=1
            )
        )

        solids_concentration = self._create_df_result(
            pd.concat(
                (solids_concentration_only, precipitate_check, saturation_index),
                axis=1,
                sort=True,
            )
        )

        solids_concentration = solids_concentration[
            sum(
                [
                    [check_col, si_col, solid_col]
                    for check_col, si_col, solid_col in zip(
                        precipitate_check.columns,
                        saturation_index.columns,
                        solids_concentration_only.columns,
                    )
                ],
                [],
            )
        ]

        formation_constants = (
            pd.DataFrame()
            if not solver_data.ionic_strength_dependence
            else self._create_df_result(
                log_beta,
                columns=solver_data.species_names[solver_data.nc :],
            )
        ).rename_axis(columns="Formation Constant")

        solubility_products = (
            pd.DataFrame()
            if not solver_data.ionic_strength_dependence
            else self._create_df_result(
                log_ks,
                columns=solver_data.solids_names,
            )
        ).rename_axis(columns="Solubility Product")

        self.signals.log.emit(repr(soluble_concentration))
        self.signals.log.emit(repr(solids_concentration))

        # self._storeResult(
        #     soluble_concentration,
        #     "species_concentrations",
        #     slices=slices,
        #     extra=means_to_report,
        # )
        # self._storeResult(
        #     solids_concentration,
        #     "solids_concentrations",
        #     slices=slices,
        #     extra=means_to_report,
        # )

        ref_percentage_soluble = solver_data.components + list(
            self.data["speciesModel"]["Ref. Comp."].values()
        )
        ref_percentage_soluble_ix = component_encoder(
            solver_data.components, ref_percentage_soluble
        )

        ref_tot_conc_soluble = total_concentration[:, ref_percentage_soluble_ix]

        adjust_factor_soluble = np.clip(
            np.concatenate(
                (
                    np.eye(solver_data.nc, dtype=int),
                    solver_data.stoichiometry,
                ),
                axis=1,
            )[ref_percentage_soluble_ix, range(ref_percentage_soluble_ix.size)],
            1,
            np.inf,
        )

        ref_poercentage_solids = list(
            self.data["solidSpeciesModel"]["Ref. Comp."].values()
        )

        ref_percentage_solids_ix = component_encoder(
            solver_data.components,
            ref_poercentage_solids,
        )

        ref_tot_conc_solids = total_concentration[:, ref_percentage_solids_ix]

        adjust_factor_solids = np.clip(
            solver_data.solid_stoichiometry[
                ref_percentage_solids_ix, range(ref_percentage_solids_ix.size)
            ],
            1,
            np.inf,
        )

        soluble_percentages_np = (
            (soluble_concentration.to_numpy() * adjust_factor_soluble)
            / ref_tot_conc_soluble
        ) * 100

        soluble_percentages = self._create_df_result(
            (soluble_percentages_np).round(2),
            columns=[solver_data.species_names, ref_percentage_soluble],
        ).rename_axis(columns=["Species", r"% relative to comp."])

        solids_percentage_np = (
            (solids_concentration_only.to_numpy() * adjust_factor_solids)
            / ref_tot_conc_solids
        ) * 100

        solids_percentages = self._create_df_result(
            (solids_percentage_np).round(2),
            columns=[solver_data.solids_names, ref_poercentage_solids],
        ).rename_axis(columns=["Solids", r"% relative to comp."])

        self.signals.log.emit(repr(soluble_percentages))
        self.signals.log.emit(repr(solids_percentages))
        self.signals.log.emit(repr(formation_constants))
        self.signals.log.emit(repr(solubility_products))

        # Print and store species percentages
        # self._storeResult(
        #     soluble_percentages,
        #     "soluble_percentages",
        #     slices=slices,
        #     extra=means_to_report,
        # )
        # Print and store solid species percentages
        # self._storeResult(
        #     solids_percentages,
        #     "solids_percentages",
        #     slices=slices,
        #     extra=means_to_report,
        # )

        # If working at variable ionic strength print and store formation constants/solubility products aswell
        # self._storeResult(formation_constants, "formation_constants", slices=slices)
        # self._storeResult(solubility_products, "solubility_products", slices=slices)

        if self.data["emode"] is True:
            soluble_sigma_np, solids_sigma_np = uncertanties(
                concentrations,
                solver_data.stoichiometry,
                solver_data.solid_stoichiometry,
                log_beta,
                log_ks,
                solver_data.log_beta_sigma,
                solver_data.log_ks_sigma,
                self.conc_sigma,
                (
                    solver_data.distribution_opts.independent_component
                    if mode == "distribution"
                    else None
                ),
            )

            soluble_sigma = self._create_df_result(
                soluble_sigma_np,
                columns=solver_data.species_names,
            )

            solids_sigma = self._create_df_result(
                solids_sigma_np,
                columns=solver_data.solids_names,
            )

            sigma_ref_tot_conc_soluble = np.array([
                self.conc_sigma[:, ix] for ix in ref_percentage_soluble_ix
            ]).T

            sigma_ref_tot_conc_solids = np.array([
                self.conc_sigma[:, ix] for ix in ref_percentage_solids_ix
            ]).T

            soluble_percentages_sigma = self._create_df_result(
                soluble_percentages_np
                * np.sqrt(
                    (
                        soluble_sigma_np
                        / (soluble_concentration.to_numpy() * adjust_factor_soluble)
                    )
                    ** 2
                    + (sigma_ref_tot_conc_soluble / ref_tot_conc_soluble) ** 2
                ),
                columns=solver_data.species_names,
            )

            solids_percentages_sigma = self._create_df_result(
                solids_percentage_np
                * np.sqrt(
                    (
                        solids_sigma_np
                        / (solids_concentration_only.to_numpy() * adjust_factor_solids)
                    )
                    ** 2
                    + (sigma_ref_tot_conc_solids / ref_tot_conc_solids) ** 2
                ),
                columns=solver_data.solids_names,
            )

            self._storeResult(soluble_sigma, "species_sigma", slices=slices)
            self._storeResult(solids_sigma, "solid_sigma", slices=slices)

            self._storeResult(
                soluble_percentages_sigma, "soluble_percentages_sigma", slices=slices
            )
            self._storeResult(
                solids_percentages_sigma, "solids_percentages_sigma", slices=slices
            )

        self.signals.log.emit("Elapsed Time: %s s" % elapsed_time)

        self.signals.log.emit("### FINISHED ###")
        self.signals.finished.emit()

        return None

    def _reportData(self, data: pd.DataFrame, extra: list[str]):
        extra_df = pd.DataFrame(
            [data.index.get_level_values(e).to_numpy().mean() for e in extra],
            columns=[""],
            index=[f"Mean {e.replace('_', ' ').upper()}" for e in extra],
        )
        self.signals.log.emit(extra_df.to_string())

    def _storeResult(
        self,
        data: pd.DataFrame,
        name: str,
        slices: list[int] = [],
        extra: list[str] = [],
        print_out: bool = True,
    ):
        multiple_items = len(slices) > 2
        if multiple_items:
            # Ensure slices does not include data.shape[0] as its last element
            if slices[-1] == data.shape[0]:
                slices = slices[:-1]

            # Create the list of tuples representing the intervals
            ix_ranges = [(slices[i], slices[i + 1]) for i in range(len(slices) - 1)] + [
                (slices[-1], data.shape[0])
            ]
            result = []
            for counter, (i1, i2) in enumerate(ix_ranges):
                df = data.iloc[i1:i2, :]
                result.append(df)
                self.signals.result.emit(df, name)
                if not df.empty and print_out:
                    if i1 == 0:
                        self.signals.log.emit(
                            "\t\t" + name.replace("_", " ").upper() + "\n"
                        )
                    self.signals.log.emit(f"\t\t\t Titration {counter + 1}")
                    self.signals.log.emit(df.to_string())
                    if extra:
                        self._reportData(df, extra)
                    self.signals.log.emit("\n\n")
                    self.signals.log.emit("--" * 40)
        else:
            self.signals.result.emit(data, name)
            if not data.empty and print_out:
                self.signals.log.emit("\t\t" + name.replace("_", " ").upper() + "\n")
                self.signals.log.emit(data.to_string())
                if extra:
                    self._reportData(data, extra)
                self.signals.log.emit("--" * 40)

    def _create_df_result(self, data, columns: list | None = None):
        if data is None:
            return pd.DataFrame()
        else:
            result = pd.DataFrame(
                data, index=self.result_index, columns=columns
            ).rename_axis(index=self.index_name)
            result.insert(0, "I", self.ionic_strength)
            result.set_index("I", append=True, inplace=True)

            return result

    def _simplify_problem(self, data: dict[str, Any]):
        def remove_ignored(model: dict[str, Any]):
            ignored_ix = set()

            names = model["Name"]
            ignored = model["Ignored"]

            keys = list(model.keys())

            for s, (name, flag) in enumerate(zip(names.values(), ignored.values())):
                if name == "" or flag:
                    ignored_ix.add(s)

            for key in keys:
                model[key] = {
                    k: v for k, v in list(model[key].items()) if k not in ignored_ix
                }

            return model, list(ignored_ix)

        data["speciesModel"], ignored_soluble = remove_ignored(data["speciesModel"])
        data["solidSpeciesModel"], ignored_solids = remove_ignored(
            data["solidSpeciesModel"]
        )
        data["potentiometry_data"]["beta_refine_flags"] = [
            flag
            for i, flag in enumerate(data["potentiometry_data"]["beta_refine_flags"])
            if i not in ignored_soluble
        ]

        return data, ignored_soluble, ignored_solids


def component_encoder(components: list[str], reference_component: list[str]):
    # Given the list of species names as strings and a list of the same names for each species return a list of their indexes instead.
    # This is used to calculate percentages of species concentrations
    return np.array([components.index(c) for c in reference_component], dtype=int)


# def compute_index_mean(data: pd.DataFrame, index_name: str):
#     # Compute the mean of the index of the dataframe
#     return data.index.get_level_values(index_name).to_numpy().mean()
