import time
import traceback
from typing import Any, Callable

import numpy as np
import pandas as pd
from PySide6.QtCore import QObject, QRunnable, Signal, Slot

from libeq import (
    EqSolver,
    Flags,
    PotentiometryOptimizer,
    SolverData,
    uncertanties,
)
from libeq.optimizers.potentiometry import refine_indices
from libeq.solver.solids_solver import _compute_saturation_index
from libeq.solver.solver_utils import _titration_background_ions_c
from libeq.utils import species_concentration

from workers_utils import _comp_info, _species_info

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", None)


# ---------------------------------------------------------------------------
# Signals and worker classes
# ---------------------------------------------------------------------------


class OptimizeSignals(QObject):
    """Qt signals emitted by :class:`OptimizeWorker` during a calculation run."""

    log = Signal(str)
    aborted = Signal(str)
    finished = Signal()
    result = Signal(dict)


class OptimizeWorker(QRunnable):
    """Background worker that runs equilibrium simulations and optimisations.

    Depending on the value of ``data_list['dmode']``, the worker runs one of
    three calculation modes:

    * ``0`` – titration simulation
    * ``1`` – distribution simulation
    * ``2`` – potentiometry optimisation

    Parameters
    ----------
    data_list:
        Dictionary produced by the GUI containing model and experimental data.
    debug:
        When ``True``, full tracebacks are forwarded to the ``aborted`` signal
        instead of just the exception message.
    """

    def __init__(self, data_list: dict[str, Any], debug: bool) -> None:
        super().__init__()
        self.signals = OptimizeSignals()
        self.data = data_list
        self.debug = debug
        self.index_name: str | list[str]

    # ------------------------------------------------------------------
    # Public entry point
    # ------------------------------------------------------------------

    @Slot()
    def run(self) -> None:
        """Execute the calculation selected in ``self.data['dmode']``.

        Emits :attr:`OptimizeSignals.result` with the result dictionary on
        success, or :attr:`OptimizeSignals.aborted` with an error message on
        failure.
        """
        start_time = time.time()

        self.signals.log.emit("### Beginning Calculation ###\n")
        self.signals.log.emit("Loading data...\n")

        self.data, ignored_soluble, ignored_solids = self._simplify_problem(self.data)
        self._emit_ignored_species(ignored_soluble, ignored_solids)

        solver_data = self._load_solver_data()
        if solver_data is None:
            return

        if not self._validate_model(solver_data):
            return

        if not self._check_ready(solver_data):
            return

        available_modes = ("titration", "distribution", "potentiometry")
        mode = available_modes[self.data["dmode"]]

        species_info, solids_info = _species_info(solver_data, mode, self.data["emode"])
        comp_info = _comp_info(solver_data, mode, self.data["emode"])
        input_info = {
            "species_info": species_info,
            "solids_info": solids_info,
            "comp_info": comp_info,
        }

        stoichiometry_df, solid_stoichiometry_df = self._build_stoichiometry_dataframes(
            solver_data
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

        retval.update(input_info)
        retval["stoichiometry"] = stoichiometry_df
        retval["solid_stoichiometry"] = solid_stoichiometry_df

        elapsed_time = round((time.time() - start_time), 5)
        self.signals.log.emit(f"\nElapsed Time: {elapsed_time} s")
        self.signals.log.emit("\n### FINISHED ###")
        self.signals.result.emit(retval)
        self.signals.finished.emit()

    # ------------------------------------------------------------------
    # Calculation mode runners
    # ------------------------------------------------------------------

    def _run_titration(self, solver_data: SolverData) -> dict[str, Any]:
        """Set up titration-specific state and delegate to the common simulator.

        Parameters
        ----------
        solver_data:
            Validated solver data object.

        Returns
        -------
        dict
            Result dictionary from :meth:`_simulation_common`.
        """
        self.result_index = (
            np.arange(solver_data.titration_opts.n_add)
            * solver_data.titration_opts.v_increment
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
        return self._simulation_common(solver_data, mode="titration")

    def _run_distribution(self, solver_data: SolverData) -> dict[str, Any]:
        """Set up distribution-specific state and delegate to the common simulator.

        Parameters
        ----------
        solver_data:
            Validated solver data object.

        Returns
        -------
        dict
            Result dictionary from :meth:`_simulation_common`.
        """
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
            + solver_data.components[solver_data.distribution_opts.independent_component]
            + "]"
        )
        self.conc_sigma = np.tile(
            solver_data.distribution_opts.c0_sigma, [self.result_index.size, 1]
        )
        self.background_ions_concentration = solver_data.distribution_opts.cback

        self.signals.log.emit(r"Calculating distribution of the species...")
        return self._simulation_common(solver_data, mode="distribution")

    def _run_potentiometry(self, solver_data: SolverData) -> dict[str, Any] | None:
        """Run the potentiometry optimisation and return a results dictionary.

        Parameters
        ----------
        solver_data:
            Validated solver data object.

        Returns
        -------
        dict or None
            Result dictionary on success, ``None`` if the optimiser raised an
            exception.
        """
        self._emit_dataset_stats(solver_data)
        self.signals.log.emit(
            "Optimizing stability constants from potentiometric data...\n"
        )

        self.optimized_species = (
            np.array(solver_data.potentiometry_opts.beta_flags) == Flags.REFINE
        )
        self.signals.log.emit("--" * 40)
        initial_logbeta = solver_data.log_beta.copy()

        log_reporter = self._build_potentiometry_log_reporter(solver_data)

        try:
            fit_result = PotentiometryOptimizer(solver_data, reporter=log_reporter)
        except Exception as e:
            self._emit_exception(e)
            return None

        concentrations = fit_result["free concentration"]
        log_beta = fit_result["final log beta"]
        b_error = fit_result["error log beta"]

        _print_correlation_matrix(
            fit_result["correlation"],
            fit_result["variable names"],
            self.signals.log.emit,
        )

        slices = fit_result["slices"]
        total_concentration = fit_result["total concentration"]

        solver_data.log_beta_sigma = solver_data.log_beta_sigma.copy()
        solver_data.log_beta_sigma[:] = b_error[:]

        log_ks = np.tile(solver_data.log_ks, (total_concentration.shape[0], 1))

        read_potential, calculated_potential, residuals, px = (
            self._compute_potentiometry_emf(fit_result)
        )

        self.background_ions_concentration = fit_result["background ion concentration"]
        self.index_name = [
            "V Add. [mL]",
            "Read Potential [V]",
            "Calculated Potential [V]",
            "Residual [V]",
            "pX",
            "Weight",
        ]
        self.result_index = [
            np.concatenate(
                [t.get_titre for t in solver_data.potentiometry_opts.titrations]
            ),
            read_potential,
            calculated_potential,
            residuals,
            px,
            fit_result["weights"],
        ]

        soluble_concentration_np = _extract_soluble_concentration(
            concentrations, solver_data.nc, solver_data.nf, solver_data.ns
        )
        self.ionic_strength_dependence = solver_data.ionic_strength_dependence
        self.ionic_strength = _compute_ionic_strength(
            soluble_concentration_np,
            solver_data.charges,
            solver_data.species_charges,
            self.background_ions_concentration,
        )

        soluble_concentration = self._create_df_result(
            soluble_concentration_np,
            columns=solver_data.species_names,
        ).rename_axis(columns="Species Conc. [mol/L]")

        soluble = self._build_potentiometry_soluble_df(
            solver_data,
            concentrations,
            read_potential,
            calculated_potential,
            residuals,
            px,
            fit_result,
        )

        (
            solids_concentration_only,
            solids_concentration,
        ) = self._build_solids_dataframes(
            concentrations,
            solver_data.nc,
            solver_data.nf,
            solver_data.solids_names,
            log_ks,
            solver_data.solid_stoichiometry,
        )

        _print_titration(slices, soluble, self.signals.log.emit, "soluble species")
        _print_titration(
            slices, solids_concentration, self.signals.log.emit, "solid species"
        )

        fit_result["optimized_parms"] = self._build_optimized_parameters_df(fit_result)
        formation_constants = self._build_formation_constants_df(
            solver_data, log_beta, initial_logbeta
        )
        solubility_products = self._build_solubility_products_df(solver_data)

        (
            ref_tot_conc_soluble,
            adjust_factor_soluble,
            ref_tot_conc_solids,
            adjust_factor_solids,
            ref_percentage_solids,
        ) = self._compute_reference_percentage_data(
            solver_data, total_concentration
        )

        soluble_percentages_np = (
            (soluble_concentration.to_numpy() * adjust_factor_soluble)
            / ref_tot_conc_soluble
        ) * 100

        solids_percentage_np = (
            (solids_concentration_only.to_numpy() * adjust_factor_solids)
            / ref_tot_conc_solids
        ) * 100

        solids_percentages = self._create_df_result(
            solids_percentage_np.round(2),
            columns=[solver_data.solids_names, ref_percentage_solids],
        ).rename_axis(columns=["Solids", r"% relative to comp."])

        fit_result["soluble_percentages"] = [
            pd.DataFrame(soluble_percentages_np[s], columns=solver_data.species_names)
            for s in slices
        ]
        fit_result["soluble_percentages_np"] = soluble_percentages_np
        fit_result["solids_concentrations"] = [
            pd.DataFrame(solids_concentration.iloc[s], columns=solver_data.species_names)
            for s in slices
        ]
        fit_result["solids_percentages"] = [
            pd.DataFrame(solids_percentages.iloc[s], columns=solver_data.species_names)
            for s in slices
        ]

        _emit_df(self.signals.log.emit, formation_constants, "Formation constants")
        self._emit_titration_params(
            fit_result["final titration parameters"],
            fit_result["error titration parameters"],
            fit_result["initial titration parameters"],
            solver_data.components,
            self.signals.log.emit,
        )
        _emit_df(self.signals.log.emit, solubility_products, "Solubility products")

        if self.data["emode"] is True:
            conc_sigma = self._compute_potentiometry_conc_sigma(solver_data)
            soluble_sigma_np, solids_sigma_np = uncertanties(
                concentrations,
                solver_data.stoichiometry,
                solver_data.solid_stoichiometry,
                log_beta,
                log_ks,
                solver_data.log_beta_sigma,
                solver_data.log_ks_sigma,
                conc_sigma,
                None,
            )
            fit_result["soluble_sigma"] = soluble_sigma_np
            fit_result["solids_sigma"] = solids_sigma_np

        fit_result["species_concentrations"] = self._split_titration(
            fit_result["species_concentrations"],
            slices,
            solver_data.species_names,
        )

        return fit_result

    def _simulation_common(
        self, solver_data: SolverData, mode: str
    ) -> dict[str, Any]:
        """Run the equilibrium solver and build the result dictionary.

        This method is shared by both titration and distribution modes.

        Parameters
        ----------
        solver_data:
            Validated solver data object.
        mode:
            Either ``'titration'`` or ``'distribution'``.

        Returns
        -------
        dict
            Keys include ``'species_concentrations'``, ``'solids_concentrations'``,
            ``'soluble_percentages'``, ``'solids_percentages'``, ``'concentrations'``,
            and ``'percent'``.
        """
        (
            result,
            log_beta,
            log_ks,
            _saturation_index,
            total_concentration,
        ) = EqSolver(solver_data, mode=mode)

        concentrations = species_concentration(
            result, log_beta, solver_data.stoichiometry, full=True
        )

        soluble_concentration_np = _extract_soluble_concentration(
            concentrations, solver_data.nc, solver_data.nf, solver_data.ns
        )

        self.ionic_strength_dependence = solver_data.ionic_strength_dependence
        self.ionic_strength = _compute_ionic_strength(
            soluble_concentration_np,
            solver_data.charges,
            solver_data.species_charges,
            self.background_ions_concentration,
        )

        soluble_concentration = self._create_df_result(
            soluble_concentration_np,
            columns=solver_data.species_names,
        ).rename_axis(columns="Species Conc. [mol/L]")

        (
            solids_concentration_only,
            solids_concentration,
        ) = self._build_solids_dataframes(
            concentrations,
            solver_data.nc,
            solver_data.nf,
            solver_data.solids_names,
            log_ks,
            solver_data.solid_stoichiometry,
        )

        formation_constants = self._build_ionic_strength_df(
            solver_data, log_beta
        )
        solubility_products = self._build_ionic_strength_ks_df(
            solver_data, log_ks
        )

        (
            ref_tot_conc_soluble,
            adjust_factor_soluble,
            ref_tot_conc_solids,
            adjust_factor_solids,
            ref_percentage_solids,
        ) = self._compute_reference_percentage_data(solver_data, total_concentration)

        soluble_percentages_np = (
            (soluble_concentration.to_numpy() * adjust_factor_soluble)
            / ref_tot_conc_soluble
        ) * 100

        soluble_percentages = self._create_df_result(
            soluble_percentages_np.round(2),
            columns=[
                solver_data.species_names,
                solver_data.components
                + list(self.data["speciesModel"]["Ref. Comp."].values()),
            ],
        ).rename_axis(columns=["Species", r"% relative to comp."])

        solids_percentage_np = (
            (solids_concentration_only.to_numpy() * adjust_factor_solids)
            / ref_tot_conc_solids
        ) * 100

        solids_percentages = self._create_df_result(
            solids_percentage_np.round(2),
            columns=[solver_data.solids_names, ref_percentage_solids],
        ).rename_axis(columns=["Solids", r"% relative to comp."])

        _emit_df(
            self.signals.log.emit,
            soluble_concentration,
            "soluble species concentration",
        )
        _emit_df(self.signals.log.emit, solids_concentration, "solid species")
        _emit_df(self.signals.log.emit, formation_constants, "formation constants")
        _emit_df(self.signals.log.emit, solubility_products, "solubility products")

        retval: dict[str, Any] = {
            "species_concentrations": soluble_concentration,
            "solids_concentrations": solids_concentration,
            "soluble_percentages": soluble_percentages,
            "solids_percentages": solids_percentages,
            "concentrations": pd.concat(
                [soluble_concentration, solids_concentration], axis=1
            ),
            "percent": pd.concat([soluble_percentages, solids_percentages], axis=1),
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

            ref_percentage_soluble = solver_data.components + list(
                self.data["speciesModel"]["Ref. Comp."].values()
            )
            ref_percentage_soluble_ix = component_encoder(
                solver_data.components, ref_percentage_soluble
            )
            ref_percentage_solids_ix = component_encoder(
                solver_data.components, ref_percentage_solids
            )

            sigma_ref_tot_conc_soluble = np.array(
                [self.conc_sigma[:, ix] for ix in ref_percentage_soluble_ix]
            ).T
            sigma_ref_tot_conc_solids = np.array(
                [self.conc_sigma[:, ix] for ix in ref_percentage_solids_ix]
            ).T

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
                        / (
                            solids_concentration_only.to_numpy() * adjust_factor_solids
                        )
                    )
                    ** 2
                    + (sigma_ref_tot_conc_solids / ref_tot_conc_solids) ** 2
                ),
                columns=solver_data.solids_names,
            )

            retval.update(
                {
                    "soluble_percentages": soluble_percentages_sigma,
                    "solids_percentages": solids_percentages_sigma,
                    "species_sigma": soluble_sigma,
                    "solid_sigma": solids_sigma,
                }
            )

            self.signals.log.emit(repr(soluble_sigma))
            self.signals.log.emit(repr(solids_sigma))

        return retval

    # ------------------------------------------------------------------
    # Potentiometry helpers
    # ------------------------------------------------------------------

    def _build_potentiometry_log_reporter(
        self, solver_data: SolverData
    ) -> Callable[..., None]:
        """Create and return the iteration-logging callback for the optimiser.

        Parameters
        ----------
        solver_data:
            Validated solver data object used to access titration metadata.

        Returns
        -------
        Callable
            A keyword-argument function suitable for passing as ``reporter`` to
            :func:`PotentiometryOptimizer`.
        """
        labels = list(self.data["compModel"]["Name"].values())
        beta_refine_flags = self.data["potentiometry_data"]["beta_refine_flags"]
        out = self.signals.log.emit

        def log_reporter(**kwargs: Any) -> None:
            """Log the result of each optimisation iteration."""
            out(f"iteration = {kwargs['iteration']}")
            out(
                f"damping = {kwargs['damping']:.4e}, chisq = {kwargs['chisq']:.4f}, "
                f"gradient_norm = {kwargs['gradient_norm']:.4e}, rho = {kwargs['rho']:.4e}"
            )
            out(f"-sigma: {kwargs['sigma']:.4e} ({kwargs['exit_sigma']})")
            out(f"-grad : {kwargs['exit_gradient_value']:.4e} ({kwargs['exit_gradient']})")
            out(f"-step : {kwargs['exit_step_value']:.4e} ({kwargs['exit_step']})")

            increment = iter(kwargs["increment"].tolist())

            if kwargs["any beta refined"]:
                out(
                    "   # "
                    + "".join(f"{comp:>5}" for comp in labels)
                    + "     logβ       change  previous"
                )
                lgbeta = kwargs["log_beta"]
                oldbeta = iter(kwargs["previous log beta"].tolist())
                stoich = kwargs["stoichiometry"]
                refined = [
                    f"{next(increment):10.4f}{next(oldbeta):10.4f}"
                    if flag
                    else ""
                    for flag in beta_refine_flags
                ]
                for n, (lgb, st, rflag) in enumerate(zip(lgbeta, stoich, refined)):
                    out(
                        f"{n:>4} {''.join(f'{v:>5}' for v in st)} {lgb:10.4f} {rflag}"
                    )

            if kwargs["any conc refined"]:
                for n, ((c0, ct), titr) in enumerate(
                    zip(
                        kwargs["titration params"],
                        solver_data.potentiometry_opts.titrations,
                    )
                ):
                    out(f"titr {n:<4}: ")
                    for c0v, c0f, comp in zip(
                        c0, refine_indices(titr.c0_flags), labels
                    ):
                        if c0f:
                            out(f"\tc0[{comp}] {c0v:10.4f} {next(increment):10.4f}")
                    for ctv, ctf, comp in zip(
                        ct, refine_indices(titr.ct_flags), labels
                    ):
                        if ctf:
                            out(f"\tcT[{comp}] {ctv:10.4f} {next(increment):10.4f}")
            out(80 * "-" + "\n")

        return log_reporter

    def _compute_potentiometry_emf(
        self, fit_result: dict[str, Any]
    ) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
        """Extract and derive EMF-related arrays from the optimiser result.

        Parameters
        ----------
        fit_result:
            Dictionary returned by :func:`PotentiometryOptimizer`.

        Returns
        -------
        tuple
            ``(read_potential, calculated_potential, residuals, px)``
        """
        read_potential: np.ndarray = fit_result["read emf"]
        residuals: np.ndarray = fit_result["residuals"]
        calculated_potential = read_potential - residuals
        px = -np.log10(fit_result["eactive"])
        return read_potential, calculated_potential, residuals, px

    def _compute_potentiometry_conc_sigma(
        self, solver_data: SolverData
    ) -> np.ndarray:
        """Compute the concentration uncertainty matrix for potentiometry runs.

        For each titration, the uncertainty on the total concentration is
        propagated from the vessel (``c0_sigma``) and titrant (``ct_sigma``)
        uncertainties.

        Parameters
        ----------
        solver_data:
            Validated solver data object.

        Returns
        -------
        np.ndarray
            2-D array of shape ``(n_points, nc)``.
        """
        conc_sigma = []
        for t in solver_data.potentiometry_opts.titrations:
            v_aux = t.v_add[~t.ignored]
            conc_sigma.append(
                np.tile(t.c0_sigma, [v_aux.size, 1])
                + np.tile(v_aux, [solver_data.nc, 1]).T * 1e-3 * t.ct_sigma
            )
        return np.concatenate(conc_sigma)

    def _build_potentiometry_soluble_df(
        self,
        solver_data: SolverData,
        concentrations: np.ndarray,
        read_potential: np.ndarray,
        calculated_potential: np.ndarray,
        residuals: np.ndarray,
        px: np.ndarray,
        fit_result: dict[str, Any],
    ) -> pd.DataFrame:
        """Build the per-point DataFrame for soluble species in potentiometry.

        Parameters
        ----------
        solver_data:
            Validated solver data object.
        concentrations:
            Full species concentration array from the optimiser.
        read_potential, calculated_potential, residuals, px:
            EMF-related arrays (see :meth:`_compute_potentiometry_emf`).
        fit_result:
            Dictionary returned by :func:`PotentiometryOptimizer`.

        Returns
        -------
        pd.DataFrame
            DataFrame with one row per experimental point, indexed by the
            multi-index stored in ``self.result_index``.
        """
        soluble_concentration_np = _extract_soluble_concentration(
            concentrations, solver_data.nc, solver_data.nf, solver_data.ns
        )
        ionic_strength = _compute_ionic_strength(
            soluble_concentration_np,
            solver_data.charges,
            solver_data.species_charges,
            fit_result["background ion concentration"],
        )

        species_index = pd.Index(
            solver_data.species_names, name="Soluble species conc. [mol/L]"
        )

        soluble = pd.DataFrame()
        soluble["V Add. [mL]"] = np.concatenate(
            [t.get_titre for t in solver_data.potentiometry_opts.titrations]
        )
        soluble["Read Potential [V]"] = read_potential
        soluble["Calculated Potential [V]"] = calculated_potential
        soluble["Residual [V]"] = residuals
        soluble["pX"] = px
        soluble["Weight"] = fit_result["weights"]
        soluble["I"] = ionic_strength

        df_soluble_conc = pd.DataFrame(
            data=soluble_concentration_np, columns=species_index
        ).rename_axis("Soluble species conc. [mol/L]")
        soluble = soluble.join(df_soluble_conc)

        if solver_data.nf:
            solids_np = concentrations[
                :, solver_data.nc : (solver_data.nc + solver_data.nf)
            ]
            df_solids = pd.DataFrame(
                data=solids_np,
                columns=[f"{name}(sld.)" for name in species_index],
            )
            soluble = soluble.join(df_solids)

        return soluble

    def _build_formation_constants_df(
        self,
        solver_data: SolverData,
        log_beta: np.ndarray,
        initial_logbeta: np.ndarray,
    ) -> pd.DataFrame:
        """Build a DataFrame summarising optimised formation constants.

        Parameters
        ----------
        solver_data:
            Validated solver data object.
        log_beta:
            Optimised log β values.
        initial_logbeta:
            Log β values before optimisation (used to compute the change).

        Returns
        -------
        pd.DataFrame
            One row per species with columns for the log β, its standard
            deviation, the initial value, and the change.
        """
        components_idx = pd.Index(solver_data.components)
        df = pd.DataFrame()
        df["species"] = solver_data.species_names[solver_data.nc :]
        df[components_idx] = solver_data.stoichiometry.T
        df["log beta"] = log_beta
        df["stdev"] = solver_data.log_beta_sigma
        mask = df["stdev"].isna()
        df["initial"] = initial_logbeta
        df["change"] = df["log beta"] - df["initial"]
        df["initial"] = df["initial"].mask(mask, np.nan)
        df["change"] = df["change"].mask(mask, np.nan)
        return df.fillna("")

    def _build_solubility_products_df(self, solver_data: SolverData) -> pd.DataFrame:
        """Build a DataFrame summarising solubility products.

        Parameters
        ----------
        solver_data:
            Validated solver data object.

        Returns
        -------
        pd.DataFrame
            One row per solid species, or an empty DataFrame if there are none.
        """
        df = pd.DataFrame()
        if len(solver_data.log_ks):
            components_idx = pd.Index(solver_data.components)
            df["logKs"] = solver_data.log_ks
            df[components_idx] = solver_data.stoichiometry
            df["stdev"] = solver_data.log_ks_sigma
        return df

    @staticmethod
    def _build_optimized_parameters_df(fit_result: dict[str, Any]) -> pd.DataFrame:
        """Build a DataFrame summarising the optimiser's refined variables.

        Parameters
        ----------
        fit_result:
            Dictionary returned by :func:`PotentiometryOptimizer`.

        Returns
        -------
        pd.DataFrame
            Columns: ``variable``, ``value``, ``stdev``.
        """
        df = pd.DataFrame()
        df["variable"] = fit_result["variable names"]
        df["value"] = fit_result["final variables"]
        df["stdev"] = fit_result["standard deviation"]
        return df

    # ------------------------------------------------------------------
    # Shared helpers used by multiple calculation modes
    # ------------------------------------------------------------------

    def _build_solids_dataframes(
        self,
        concentrations: np.ndarray,
        nc: int,
        nf: int,
        solids_names: list[str],
        log_ks: np.ndarray,
        solid_stoichiometry: np.ndarray,
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Build the solids-concentration and combined-solids DataFrames.

        Constructs the raw solids concentration DataFrame, the precipitation
        indicator, the saturation index, and then combines them into the
        interleaved result used for reporting.

        Parameters
        ----------
        concentrations:
            Full species concentration array.
        nc, nf:
            Number of components and solid phases.
        solids_names:
            Names of the solid species.
        log_ks:
            Log solubility products (may be 2-D for potentiometry).
        solid_stoichiometry:
            Solid stoichiometry matrix.

        Returns
        -------
        tuple[pd.DataFrame, pd.DataFrame]
            ``(solids_concentration_only, solids_concentration_combined)``
        """
        solids_concentration_only = pd.DataFrame(
            concentrations[:, nc : (nc + nf)],
            index=self.result_index,
            columns=solids_names,
        ).rename_axis(columns="Solid Conc. [mol/L]")

        saturation_index = pd.DataFrame(
            _compute_saturation_index(
                concentrations[:, :nc], log_ks, solid_stoichiometry
            ),
            index=self.result_index,
            columns=["SI" + name for name in solids_names],
        )

        precipitate_check = (
            (solids_concentration_only > 0)
            .replace({True: "*", False: ""})
            .set_axis(
                ["Prec." + name for name in solids_concentration_only.columns], axis=1
            )
        )

        combined = self._create_df_result(
            pd.concat(
                (solids_concentration_only, precipitate_check, saturation_index),
                axis=1,
                sort=True,
            )
        )

        # Re-order columns to group each solid's check, SI, and concentration
        ordered_columns = sum(
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
        combined = combined[ordered_columns]

        return solids_concentration_only, combined

    def _compute_reference_percentage_data(
        self,
        solver_data: SolverData,
        total_concentration: np.ndarray,
    ) -> tuple[
        np.ndarray,
        np.ndarray,
        np.ndarray,
        np.ndarray,
        list[str],
    ]:
        """Compute reference concentrations and adjustment factors for percentages.

        Gathers the reference component lists from the GUI model data and
        computes the total concentration columns and stoichiometry adjustment
        factors needed to convert absolute concentrations to percentages.

        Parameters
        ----------
        solver_data:
            Validated solver data object.
        total_concentration:
            Total analytical concentrations at each simulation point.

        Returns
        -------
        tuple
            ``(ref_tot_conc_soluble, adjust_factor_soluble,
               ref_tot_conc_solids, adjust_factor_solids,
               ref_percentage_solids)``
        """
        ref_percentage_soluble = solver_data.components + list(
            self.data["speciesModel"]["Ref. Comp."].values()
        )
        ref_percentage_soluble_ix = component_encoder(
            solver_data.components, ref_percentage_soluble
        )
        ref_tot_conc_soluble = total_concentration[:, ref_percentage_soluble_ix]
        adjust_factor_soluble = np.clip(
            np.concatenate(
                (np.eye(solver_data.nc, dtype=int), solver_data.stoichiometry),
                axis=1,
            )[ref_percentage_soluble_ix, range(ref_percentage_soluble_ix.size)],
            1,
            np.inf,
        )

        ref_percentage_solids = list(
            self.data["solidSpeciesModel"]["Ref. Comp."].values()
        )
        ref_percentage_solids_ix = component_encoder(
            solver_data.components, ref_percentage_solids
        )
        ref_tot_conc_solids = total_concentration[:, ref_percentage_solids_ix]
        adjust_factor_solids = np.clip(
            solver_data.solid_stoichiometry[
                ref_percentage_solids_ix, range(ref_percentage_solids_ix.size)
            ],
            1,
            np.inf,
        )

        return (
            ref_tot_conc_soluble,
            adjust_factor_soluble,
            ref_tot_conc_solids,
            adjust_factor_solids,
            ref_percentage_solids,
        )

    def _build_ionic_strength_df(
        self,
        solver_data: SolverData,
        log_beta: np.ndarray,
    ) -> pd.DataFrame:
        """Build a per-point formation-constants DataFrame (ionic strength mode only).

        Parameters
        ----------
        solver_data:
            Validated solver data object.
        log_beta:
            Log β values at each simulation point.

        Returns
        -------
        pd.DataFrame
            Empty DataFrame when ionic strength dependence is disabled, otherwise
            a result DataFrame of log β values indexed by the run index.
        """
        if not solver_data.ionic_strength_dependence:
            return pd.DataFrame().rename_axis(columns="Formation Constant")
        return self._create_df_result(
            log_beta,
            columns=solver_data.species_names[solver_data.nc :],
        ).rename_axis(columns="Formation Constant")

    def _build_ionic_strength_ks_df(
        self,
        solver_data: SolverData,
        log_ks: np.ndarray,
    ) -> pd.DataFrame:
        """Build a per-point solubility-products DataFrame (ionic strength mode only).

        Parameters
        ----------
        solver_data:
            Validated solver data object.
        log_ks:
            Log Ks values at each simulation point.

        Returns
        -------
        pd.DataFrame
            Empty DataFrame when ionic strength dependence is disabled, otherwise
            a result DataFrame of log Ks values indexed by the run index.
        """
        if not solver_data.ionic_strength_dependence:
            return pd.DataFrame().rename_axis(columns="Solubility Product")
        return self._create_df_result(
            log_ks,
            columns=solver_data.solids_names,
        ).rename_axis(columns="Solubility Product")

    # ------------------------------------------------------------------
    # Validation and setup helpers
    # ------------------------------------------------------------------

    def _load_solver_data(self) -> SolverData | None:
        """Load and return the :class:`SolverData` from ``self.data``.

        Returns
        -------
        SolverData or None
            ``None`` if loading raises an exception (error is emitted via
            :attr:`OptimizeSignals.aborted`).
        """
        try:
            return SolverData.load_from_pyes(self.data)
        except Exception as e:
            if self.debug:
                self.signals.aborted.emit(
                    "".join(
                        traceback.TracebackException.from_exception(e).format()
                    )
                )
            else:
                self.signals.aborted.emit(str(e))
            return None

    def _validate_model(self, solver_data: SolverData) -> bool:
        """Check that the model is fully configured before running a calculation.

        Parameters
        ----------
        solver_data:
            Validated solver data object.

        Returns
        -------
        bool
            ``True`` if the model is ready, ``False`` otherwise (the
            :attr:`OptimizeSignals.aborted` signal is emitted with details).
        """
        ok, errors = solver_data.model_ready
        if not ok:
            error_messages = "\n".join(
                f"  {field}: {msg}" for field, msg in errors.items()
            )
            self.signals.aborted.emit(
                "Model not ready, please check the errors and try again:\n"
                + error_messages
            )
        return ok

    def _check_ready(self, solver_data: SolverData) -> bool:
        """Check whether mode-specific data is complete.

        Parameters
        ----------
        solver_data:
            Validated solver data object.

        Returns
        -------
        bool
            ``True`` if the mode-specific data is ready, ``False`` otherwise.
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
            error_messages = "\n".join(
                f"  {field}: {msg}" for field, msg in errors.items()
            )
            self.signals.aborted.emit(
                f"{what} data not complete, please check the errors and try again:\n"
                + error_messages
            )
        return ok

    def _emit_ignored_species(
        self, ignored_soluble: list[int], ignored_solids: list[int]
    ) -> None:
        """Emit log messages for any ignored species.

        Parameters
        ----------
        ignored_soluble:
            Indices of soluble species that were removed from the model.
        ignored_solids:
            Indices of solid species that were removed from the model.
        """
        if ignored_soluble:
            self.signals.log.emit(r"Found ignored soluble species:")
            self.signals.log.emit(f"{ignored_soluble}\n")
        if ignored_solids:
            self.signals.log.emit(r"Found ignored precipitable species:")
            self.signals.log.emit(f"{ignored_solids}\n")

    def _emit_exception(self, exc: Exception) -> None:
        """Emit an exception through :attr:`OptimizeSignals.aborted`.

        When ``self.debug`` is ``True``, the full traceback is included.

        Parameters
        ----------
        exc:
            The exception to report.
        """
        if self.debug:
            msg = "".join(
                traceback.TracebackException.from_exception(exc).format()
            )
        else:
            msg = str(exc)

        if hasattr(exc, "last_value"):
            msg += f"\nLast value: {exc.last_value}"

        self.signals.aborted.emit(msg)

    # ------------------------------------------------------------------
    # DataFrame building helpers
    # ------------------------------------------------------------------

    def _create_df_result(
        self,
        data: Any,
        columns: list | None = None,
    ) -> pd.DataFrame:
        """Wrap *data* in a result DataFrame with the run index and ionic strength.

        Parameters
        ----------
        data:
            Array-like data (rows correspond to simulation points).
        columns:
            Column labels for the resulting DataFrame.

        Returns
        -------
        pd.DataFrame
            DataFrame indexed by ``self.result_index`` / ``self.index_name``
            with an appended ``"I"`` (ionic strength) level.
        """
        if data is None:
            return pd.DataFrame()

        result = pd.DataFrame(
            data, index=self.result_index, columns=columns
        ).rename_axis(index=self.index_name)
        result.insert(0, "I", self.ionic_strength)
        result.set_index("I", append=True, inplace=True)
        return result

    def _split_titration(
        self,
        data: pd.DataFrame,
        slices: list[slice],
        columns: list[str],
    ) -> list[pd.DataFrame]:
        """Split a concentration DataFrame into per-titration slices.

        Parameters
        ----------
        data:
            Full concentration DataFrame to split.
        slices:
            List of slices, one per titration experiment.
        columns:
            Column names for the result DataFrame.

        Returns
        -------
        list[pd.DataFrame]
            One DataFrame per titration.
        """
        tmp = self._create_df_result(
            data,
            columns=pd.Index(columns),
        ).rename_axis(columns="Species Conc. [mol/L]")
        return [tmp[s] for s in slices]

    def _build_stoichiometry_dataframes(
        self, solver_data: SolverData
    ) -> tuple[pd.DataFrame, pd.DataFrame]:
        """Build clipped stoichiometry DataFrames for output.

        Parameters
        ----------
        solver_data:
            Validated solver data object.

        Returns
        -------
        tuple[pd.DataFrame, pd.DataFrame]
            ``(stoichiometry_df, solid_stoichiometry_df)``
        """
        stoichiometry_df = pd.DataFrame(
            np.clip(
                np.hstack((np.eye(solver_data.nc), solver_data.stoichiometry)),
                1,
                np.inf,
            ),
            columns=solver_data.species_names,
        )
        solid_stoichiometry_df = pd.DataFrame(
            np.clip(solver_data.solid_stoichiometry, 1, np.inf),
            columns=[name + "_(s)" for name in solver_data.solids_names],
        )
        return stoichiometry_df, solid_stoichiometry_df

    # ------------------------------------------------------------------
    # Problem simplification
    # ------------------------------------------------------------------

    def _simplify_problem(
        self, data: dict[str, Any]
    ) -> tuple[dict[str, Any], list[int], list[int]]:
        """Remove ignored species from the model data in-place.

        Species are considered ignored when their name is empty or their
        *Ignored* flag is set.

        Parameters
        ----------
        data:
            Full GUI data dictionary (modified in-place).

        Returns
        -------
        tuple
            ``(data, ignored_soluble_indices, ignored_solid_indices)``
        """

        def remove_ignored(
            model: dict[str, Any],
        ) -> tuple[dict[str, Any], list[int]]:
            """Remove entries flagged as ignored from a species sub-model.

            Parameters
            ----------
            model:
                Sub-dictionary keyed by field name, with values being dicts
                keyed by species index.

            Returns
            -------
            tuple
                ``(filtered_model, ignored_indices)``
            """
            ignored_ix: set[int] = set()
            for s, (name, flag) in enumerate(
                zip(model["Name"].values(), model["Ignored"].values())
            ):
                if name == "" or flag:
                    ignored_ix.add(s)

            for key in list(model.keys()):
                model[key] = {
                    k: v for k, v in model[key].items() if k not in ignored_ix
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

    # ------------------------------------------------------------------
    # Logging / reporting helpers
    # ------------------------------------------------------------------

    def _report_data(self, data: pd.DataFrame, extra: list[str]) -> None:
        """Emit mean values for selected index levels of a result DataFrame.

        Parameters
        ----------
        data:
            Result DataFrame with a multi-level index.
        extra:
            Names of index levels whose mean values should be reported.
        """
        extra_df = pd.DataFrame(
            [data.index.get_level_values(e).to_numpy().mean() for e in extra],
            columns=[""],
            index=[f"Mean {e.replace('_', ' ').upper()}" for e in extra],
        )
        self.signals.log.emit(extra_df.to_string())

    def _emit_dataset_stats(self, solver_data: SolverData) -> None:
        """Emit per-titration and total point counts to the log.

        Parameters
        ----------
        solver_data:
            Validated solver data object containing potentiometry data.
        """
        out = self.signals.log.emit
        total_points = 0
        for n, tit in enumerate(solver_data.potentiometry_opts.titrations):
            used_points = len(tit.get_emf)
            total_points += used_points
            ignored_points = len(tit.emf) - used_points
            out(
                f"Titration #{n}: used {used_points} points "
                f"({ignored_points} ignored)"
            )
            if tit.px_range:
                ranges = "; ".join(
                    f"{pxmin}-{pxmax}" for pxmin, pxmax in tit.px_range
                )
                out(f"\tpX ranges: {ranges}")
        out(f"Total experimental points: {total_points}\n")

    @staticmethod
    def _emit_titration_params(
        params: list,
        perror: list,
        iparams: list,
        components: list[str],
        emitter: Callable[[str], None],
    ) -> None:
        """Emit a table of refined titration parameters (c0 and cT).

        Parameters
        ----------
        params:
            Final optimised values, structured as a list of titration tuples
            each containing ``(c0_values, cT_values)``.
        perror:
            Corresponding standard deviations (same structure as *params*).
        iparams:
            Initial values before optimisation (same structure as *params*).
        components:
            Component names.
        emitter:
            Callable used to emit each line of text.
        """
        emitter("\nRefined titrations parameters")
        emitter("              Final values         Initial values")
        for ntit, (ptit, etit, itit) in enumerate(zip(params, perror, iparams)):
            for values, errors, init, tag in zip(ptit, etit, itit, ["c0", "cT"]):
                if not errors:
                    continue
                for name, value, error, ivalue in zip(
                    components, values, errors, init
                ):
                    if not error:
                        continue
                    emitter(
                        f"{tag}[tit#{ntit},{name}] = {value:.5f} +/- {error:.5f}"
                        f"  {ivalue:.5f}"
                    )


# ---------------------------------------------------------------------------
# Backward-compatible aliases
# ---------------------------------------------------------------------------

#: Alias for :class:`OptimizeSignals` kept for backwards compatibility.
optimizeSignal = OptimizeSignals
#: Alias for :class:`OptimizeWorker` kept for backwards compatibility.
optimizeWorker = OptimizeWorker


# ---------------------------------------------------------------------------
# Module-level helper functions
# ---------------------------------------------------------------------------


def component_encoder(
    components: list[str], reference_component: list[str]
) -> np.ndarray:
    """Return the index of each *reference_component* within *components*.

    Used to convert component-name references in the GUI model into integer
    indices suitable for array indexing.

    Parameters
    ----------
    components:
        Ordered list of all component names.
    reference_component:
        List of component names whose indices are required.

    Returns
    -------
    np.ndarray
        1-D integer array of the same length as *reference_component*.
    """
    return np.array([components.index(c) for c in reference_component], dtype=int)


def _extract_soluble_concentration(
    concentrations: np.ndarray,
    nc: int,
    nf: int,
    ns: int,
) -> np.ndarray:
    """Slice the soluble (non-solid) species columns from a concentration array.

    Parameters
    ----------
    concentrations:
        Full species concentration array of shape ``(n_points, nc + nf + ns)``.
    nc:
        Number of components.
    nf:
        Number of solid phases.
    ns:
        Number of soluble complex species.

    Returns
    -------
    np.ndarray
        Array of shape ``(n_points, nc + ns)`` containing only the soluble
        species concentrations.
    """
    return concentrations[
        :,
        np.r_[0:nc, (nc + nf) : (nc + nf + ns)],
    ]


def _compute_ionic_strength(
    soluble_concentration: np.ndarray,
    charges: list[int] | np.ndarray,
    species_charges: list[int] | np.ndarray,
    background_ions: np.ndarray,
) -> np.ndarray:
    """Compute the ionic strength at each simulation point.

    Uses the standard formula:

    .. math::

        I = \\frac{1}{2} \\left( \\sum_i c_i z_i^2 + I_{\\text{background}} \\right)

    Parameters
    ----------
    soluble_concentration:
        Array of shape ``(n_points, nc + ns)`` with soluble species concentrations.
    charges:
        Charges of the components (length ``nc``).
    species_charges:
        Charges of the soluble complex species (length ``ns``).
    background_ions:
        Background ionic contribution at each point, shape ``(n_points, 1)``
        or broadcastable.

    Returns
    -------
    np.ndarray
        Ionic strength column vector of shape ``(n_points, 1)``.
    """
    all_charges = np.concatenate([charges, species_charges])
    return 0.5 * (
        (soluble_concentration * all_charges**2).sum(axis=1, keepdims=True)
        + background_ions
    )


def _emit_df(
    emitter: Callable[[str], None],
    df: pd.DataFrame,
    title: str | None = None,
) -> None:
    """Emit a DataFrame through *emitter* as a formatted string.

    Parameters
    ----------
    emitter:
        Callable that accepts a single string argument (e.g. a Qt signal's
        ``emit`` method).
    df:
        DataFrame to print.  When empty, a ``"No <title> to print"`` message
        is emitted instead.
    title:
        Optional section title printed before the DataFrame.
    """
    if title:
        emitter(f"\n{title}")
    if df.empty:
        emitter(f"No {title} to print")
    else:
        emitter(df.to_string())


def _print_titration(
    slices: list[slice],
    dataset: pd.DataFrame,
    emitter: Callable[[str], None],
    title: str = "data",
) -> None:
    """Emit a DataFrame split into per-titration sections.

    Parameters
    ----------
    slices:
        One slice per titration experiment.
    dataset:
        Full combined DataFrame to slice and print.
    emitter:
        Callable used to emit each line.
    title:
        Label used in the header and in the empty-dataset message.
    """
    if dataset.empty:
        emitter(f"No {title} data to print")
        return

    for n, s in enumerate(slices):
        emitter(f"titration #{n}")
        emitter((13 + len(str(n))) * "-")
        emitter(dataset[s].to_string())
        emitter("\n")


def _print_correlation_matrix(
    corr: np.ndarray,
    labels: list[str],
    emitter: Callable[[str], None],
) -> None:
    """Emit the upper triangle of a correlation matrix in a readable format.

    Parameters
    ----------
    corr:
        Square correlation matrix of shape ``(n, n)``.
    labels:
        Variable names corresponding to the rows/columns of *corr*.
    emitter:
        Callable used to emit each line.

    Raises
    ------
    ValueError
        If *corr* is not square or its size does not match *labels*.
    """
    nrow, ncol = corr.shape
    if nrow != ncol:
        raise ValueError("matrix is not squared")
    if nrow != len(labels):
        raise ValueError("matrix and label list are not of the same size")

    df = pd.DataFrame(corr[:-1, 1:], index=labels[:-1], columns=labels[1:])
    tfilter = np.triu(np.ones(nrow - 1, dtype=bool))
    emitter("Correlation matrix")
    emitter(20 * "-" + "\n")
    emitter(str(df.where(tfilter).fillna("")))
    emitter("\n")
