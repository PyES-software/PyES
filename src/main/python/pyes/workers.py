import time
import traceback
from typing import Any, Callable

import numpy as np
import pandas as pd
from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from libeq import (
    EqSolver,
    PotentiometryOptimizer,
    SolverData,
    uncertanties,
    Flags
)

from libeq.optimizers.potentiometry import refine_indices
from libeq.solver.solids_solver import _compute_saturation_index
from libeq.solver.solver_utils import _titration_background_ions_c
from libeq.utils import species_concentration

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
    result = Signal(dict)


class optimizeWorker(QRunnable):
    def __init__(self, data_list: dict, debug: bool):
        super().__init__()
        self.signals = optimizeSignal()
        self.data = data_list
        self.debug = debug
        # self.solver_data = None
        self.index_name: str | list[str]

    def _run_potentiometry(self, solver_data: SolverData):
        # If run with debug enabled create the logging istance
        def log_reporter(**kwargs):
            """
            Log out the result of each iteration.
            """
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
                txt = "   # " + "".join(f"{comp:>5}" for comp in labels) + \
                      "     logβ       change  previous"
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
                                                         solver_data.potentiometry_opts.titrations)):
                    out(f"titr {n:<4}: ")
                    for c0v, c0f, comp in zip(c0, refine_indices(titr.c0_flags), labels):
                        if c0f:
                            out(f"\tc0[{comp}] {c0v:10.4f} {next(increment):10.4f}")
            out(80*'-')

        self.__print_dataset_stats(solver_data)

        self.signals.log.emit("Optimizing stability constants from potentiometric data...\n")

        self.index_name = "V Add. [mL]"

        self.optimized_species = np.array(solver_data.potentiometry_opts.beta_flags) == Flags.REFINE

        self.signals.log.emit("--" * 40)
        initial_logbeta = solver_data.log_beta.copy()

        try:
            fit_result = PotentiometryOptimizer(solver_data, reporter=log_reporter)
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

        ## never used
        # x = fit_result['final variables']
        concentrations = fit_result['free concentration']
        log_beta = fit_result['final log beta']
        b_error = fit_result['error log beta']

        ## print correlation matrix
        # cor_matrix = fit_result['correlation']
        # self.signals.log.emit(repr(cor_matrix))
        # cov_matrix = fit_result['covariance']

        slices = fit_result['slices']
        total_concentration = fit_result["total concentration"]

        solver_data.log_beta_sigma = solver_data.log_beta_sigma.copy()
        solver_data.log_beta_sigma[:] = b_error[:]

        log_ks = np.tile(solver_data.log_ks, (total_concentration.shape[0], 1))

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
        for t in solver_data.potentiometry_opts.titrations:
            v_aux = t.v_add[~t.ignored]
            conc_sigma.append(
                np.tile(t.c0_sigma, [v_aux.size, 1])
                + (
                    np.tile(v_aux, [solver_data.nc, 1]).T
                    * 1e-3
                    * t.ct_sigma
                )
            )
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

        formation_constants = pd.DataFrame()
        formation_constants['species'] = solver_data.species_names[solver_data.nc:]
        components_idx = pd.Index(solver_data.components)
        formation_constants[components_idx] = solver_data.stoichiometry.T
        formation_constants['log beta'] = log_beta
        formation_constants['stdev'] = solver_data.log_beta_sigma
        mask = formation_constants['stdev'].isna()
        formation_constants['initial'] = initial_logbeta
        formation_constants['change'] = formation_constants['log beta'] - formation_constants['initial'] 
        formation_constants['initial'] = formation_constants['initial'].mask(mask, np.nan)
        formation_constants['change'] = formation_constants['change'].mask(mask, np.nan)
        formation_constants = formation_constants.fillna('')

        solubility_products = pd.DataFrame()
        if len(solver_data.log_ks):
            solubility_products['logKs'] = solver_data.log_ks
            solubility_products[components_idx] = solver_data.stoichiometry
            solubility_products['stdev'] = solver_data.log_ks_sigma

        _print_titration(slices, soluble_concentration, self.signals.log.emit, "soluble species")
        _print_titration(slices, solids_concentration, self.signals.log.emit, "solid species")

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

        # _print_titration(slices, soluble_percentages, self.signals.log.emit, "percent soluble species")
        # _print_titration(slices, solids_percentages, self.signals.log.emit, "percent solids species")

        _emit_df(self.signals.log.emit, formation_constants, "Formation constants")
        _emit_df(self.signals.log.emit, solubility_products, "Solubility products")

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
                None
            )
            fit_result['soluble_sigma'] = soluble_sigma_np
            fit_result['solids_sigma'] = solids_sigma_np

        return fit_result

    def _run_titration(self, solver_data: SolverData):
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
        self.signals.log.emit(r"Calculating titration of the species...")
        return self._simulation_common(solver_data, mode='titration')

    def _run_distribution(self, solver_data: SolverData):
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
        return self._simulation_common(solver_data, mode='distribution')

    def _simulation_common(self, solver_data: SolverData, mode: str):
        (
            result,
            log_beta,
            log_ks,
            saturation_index,
            total_concentration,
        ) = EqSolver(solver_data, mode=mode)
        # slices = [slice(0, result.shape[0])]
        # Calculate elapsed time between start to finish
        concentrations = species_concentration(
            result, log_beta, solver_data.stoichiometry, full=True
        )

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

        _emit_df(self.signals.log.emit, soluble_concentration, "soluble species concentration")
        _emit_df(self.signals.log.emit, solids_concentration, "solid species")
        _emit_df(self.signals.log.emit, formation_constants, "formation constants")
        _emit_df(self.signals.log.emit, solubility_products, "solubility products")

        retval = {
            'species_concentrations': soluble_concentration,
            'solids_concentrations': solids_concentration,
            'soluble_percentages': soluble_percentages,
            'solids_percentages': solids_percentages
        }

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
                solver_data.distribution_opts.independent_component,
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

            retval.update({'soluble_percentages': soluble_percentages_sigma,
                           'solids_percentages': solids_percentages_sigma,
                           'species_sigma': soluble_sigma,
                           'solid_sigma': solids_sigma})

            self.signals.log.emit(repr(soluble_sigma))
            self.signals.log.emit(repr(solids_sigma))

        return retval

    @Slot()
    def run(self):
        # Start timer to time entire process
        start_time = time.time()

        self.signals.log.emit("### Beginning Calculation ###\n")
        self.signals.log.emit("Loading data...\n")

        self.data, ignored_soluble, ignored_solids = self._simplify_problem(self.data)
        if ignored_soluble:
            self.signals.log.emit(r"Found ignored soluble species:")
            self.signals.log.emit(f"{ignored_soluble}\n")

        if ignored_solids:
            self.signals.log.emit(r"Found ignored precipitable species:")
            self.signals.log.emit(f"{ignored_solids}\n")

        # load the data into the optimizer, catch errors that might invalidate the output
        try:
            solver_data: SolverData = SolverData.load_from_pyes(self.data)
            # self.solver_data = solver_data
        except Exception as e:
            if self.debug:
                self.signals.aborted.emit(
                    "".join(traceback.TracebackException.from_exception(e).format())
                )
            else:
                self.signals.aborted.emit(str(e))
            return

        ok, errors = solver_data.model_ready
        if not ok:
            error_messages = "\n".join([
                f"  {field}: {msg}" for field, msg in errors.items()
            ])
            self.signals.aborted.emit(
                "Model not ready, please check the errors and try again:\n"
                + error_messages
            )
            return

        ready = self._check_ready(solver_data)
        if not ready:
            return

        # store mode of operation as selected in the software
        available_modes = ('titration', 'distribution', 'potentiometry')
        mode = available_modes[self.data['dmode']]

        # Store input info
        species_info, solids_info = _species_info(solver_data, mode, self.data["emode"])
        comp_info = _comp_info(solver_data, mode, self.data["emode"])

        retinfo = {'species_info': species_info, 'solids_info': solids_info, 'comp_info': comp_info}
        stoichiometry = pd.DataFrame(
            np.clip(
                np.hstack((np.eye(solver_data.nc), solver_data.stoichiometry)),
                1,
                np.inf,
            ),
            columns=solver_data.species_names,
        )
        solid_stoichiometry = pd.DataFrame(
            np.clip(solver_data.solid_stoichiometry, 1, np.inf),
            columns=[name + "_(s)" for name in solver_data.solids_names],
        )

        self.signals.log.emit("DATA LOADED!\n")

        if mode == "titration":
            retval = self._run_titration(solver_data)
        elif mode == "distribution":
            retval = self._run_distribution(solver_data)
        elif mode == "potentiometry":
            retval = self._run_potentiometry(solver_data)
        else:
            raise ValueError(f"mode unknown. {mode=}")

        retval.update(retinfo)
        retval.update({'stoichiometry': stoichiometry,
                       'solid_stoichiometry': solid_stoichiometry})

        elapsed_time = round((time.time() - start_time), 5)
        self.signals.log.emit(f"\nElapsed Time: {elapsed_time} s")

        self.signals.log.emit("\n### FINISHED ###")
        self.signals.result.emit(retval)
        self.signals.finished.emit()

        return

    def _reportData(self, data: pd.DataFrame, extra: list[str]):
        extra_df = pd.DataFrame(
            [data.index.get_level_values(e).to_numpy().mean() for e in extra],
            columns=[""],
            index=[f"Mean {e.replace('_', ' ').upper()}" for e in extra],
        )
        self.signals.log.emit(extra_df.to_string())

    def _check_ready(self, solver_data):
        """
        Check whether data is ready or gaps are present.
        """
        match self.data["dmode"]:
            case 0:
                ok, errors = solver_data.titration_ready
                what = "Titration"
            case 1:
                ok, errors = solver_data.distribution_ready
                what = "Distribution"
            case 2:
                ok, errors = solver_data.potentiometry_ready
                what = "Potentiometry optimization"

        if not ok:
            error_messages = "\n".join([
                f"  {field}: {msg}" for field, msg in errors.items()
            ])
            self.signals.aborted.emit(
                f"{what} data not complete, please check the errors and try again:\n"
                + error_messages
            )
        return ok

    def _create_df_result(self, data, columns: list | None = None):
        if data is None:
            return pd.DataFrame()

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

    def __print_dataset_stats(self, solver_data):
        out = self.signals.log.emit
        for n, tit in enumerate(solver_data.potentiometry_opts.titrations):
            igno_points = np.count_nonzero(tit.ignored)
            used_points = np.count_nonzero(np.logical_not(tit.ignored))
            out(f"Titration #{n}: used {used_points} points ({igno_points} ignored)")
            if tit.px_range:
                ranges = "; ".join(f"{pxmin}-{pxmax}" for pxmin, pxmax in tit.px_range)
                out(f"\tpX ranges: {ranges}")
        out("")
            


def component_encoder(components: list[str], reference_component: list[str]):
    # Given the list of species names as strings and a list of the same names for each species
    #  return a list of their indexes instead.
    # This is used to calculate percentages of species concentrations
    return np.array([components.index(c) for c in reference_component], dtype=int)


def _emit_df(emitter: Callable[[str], None], df: pd.DataFrame, title: str | None = None) -> None:
    """Emit a dataframe through emitter as a formatted string (title optional)."""
    if title:
        emitter(f"\n{title}")
    if df.empty:
        emitter(f"No {title} to print")
    else:
        emitter(df.to_string())


def _print_titration(slices, dataset, emitter, title: str = "data"):
    if dataset.empty:
        emitter(f"No {title} data to print")
        return

    for n, s in enumerate(slices):
        emitter(f"titration #{n}")
        emitter((13+len(str(n)))*"-")
        emitter(repr(dataset[s]))
        emitter("\n")


def _print_correlation_matrix(corr: np.ndarray, labels: list[str], emitter) -> None:
    """
    Pretty-print a correlation matrix.
    
    If matrix size <= SIZE_THRESHOLD, print full labeled matrix.
    Otherwise, print the TOP_N largest correlations with labels.
    """
    SIZE_THRESHOLD = 10
    TOP_N = 20

    n = corr.shape[0]

    if corr.shape[0] != corr.shape[1]:
        raise ValueError("Correlation matrix must be square")

    if len(labels) != n:
        raise ValueError("Number of labels must match matrix size")

    df = pd.DataFrame(corr, index=labels, columns=labels)

    # ---- Small matrix: print everything ----
    if n <= SIZE_THRESHOLD:
        with pd.option_context("display.precision", 4):
            emitter(df)
        return

    # ---- Large matrix: print strongest correlations ----

    # Mask diagonal and lower triangle to avoid duplicates
    mask = np.triu(np.ones_like(df, dtype=bool), k=1)
    upper = df.where(mask)

    # Convert to long format and drop NaNs
    corr_pairs = (
        upper.stack()
             .rename("correlation")
             .reset_index()
             .rename(columns={"level_0": "Var 1", "level_1": "Var 2"})
    )

    # Sort by absolute correlation strength
    corr_pairs["abs_corr"] = corr_pairs["correlation"].abs()
    top_corrs = corr_pairs.sort_values("abs_corr", ascending=False).head(TOP_N)

    # Pretty print
    for _, row in top_corrs.iterrows():
        emitter(
            f"{row['Var 1']}  <->  {row['Var 2']}:  "
            f"{row['correlation']:+.3f}"
        )
