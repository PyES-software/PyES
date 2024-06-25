import logging
import os
import time
import traceback
from datetime import datetime
from pathlib import Path
from libeq import EqSolver, PotentiometryOptimizer, SolverData, species_concentration, uncertanties
from libeq.solver.solids_solver import _compute_saturation_index
import numpy as np

from workers_utils import _species_info, _comp_info


import pandas as pd

# from optimizers.distribution import Distribution
from PySide6.QtCore import QObject, QRunnable, Signal, Slot


# Main optimization routine worker and signals
class optimizeSignal(QObject):
    log = Signal(str)
    aborted = Signal(str)
    finished = Signal()
    result = Signal(object, str)


class optimizeWorker(QRunnable):
    def __init__(self, data_list, debug):
        super().__init__()
        self.signals = optimizeSignal()
        self.data = data_list
        self.debug = debug

    @Slot()
    def run(self):
        import debugpy

        # debugpy.debug_this_thread()
        # If run with debug enabled create the logging istance
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

        # # Start timer to time entire process
        start_time = time.time()

        self.signals.log.emit(r"### Beginning Calculation ###")
        self.signals.log.emit(r"Loading data...")

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

        self.signals.log.emit(r"DATA LOADED!")
        if self.data["dmode"] == 0:
            mode = "titration"
            self.result_index = np.arange(solver_data.titration_opts.n_add) * (
                solver_data.titration_opts.v_increment
            )
            self.index_name = ""
            self.conc_sigma = np.tile(
                solver_data.titration_opts.c0_sigma, [self.result_index.size, 1]
            ) + (
                np.tile(self.result_index, [solver_data.nc, 1]).T
                * solver_data.titration_opts.ct_sigma
            )
            self.signals.log.emit(
                r"Calculating species concentration for the simulated titration..."
            )
            start_time = time.time()
            self.signals.log.emit("--" * 40)
        elif self.data["dmode"] == 1:
            mode = "distribution"
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

            self.signals.log.emit(r"Calculating distribution of the species...")
            start_time = time.time()
            self.signals.log.emit("--" * 40)
        elif self.data["dmode"] == 2:
            mode = "potentiometry"

        # predict species distribution
        try:
            result, log_beta, log_ks, saturation_index, total_concentration = EqSolver(
                solver_data, mode=mode
            )
            # Calculate elapsed time between start to finish
            elapsed_time = round((time.time() - start_time), 5)
        except Exception as e:
            self.signals.aborted.emit(str(e))
            return None

        # Store input info
        species_info, solids_info = _species_info(solver_data)
        comp_info = _comp_info(solver_data, mode)

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
        if self.ionic_strength_dependence:
            self.ionic_strength = 0.5 * (
                soluble_concentration.to_numpy()
                * (
                    np.concatenate([solver_data.charges, solver_data.species_charges])
                    ** 2
                )
            ).sum(axis=1, keepdims=True)

        soluble_concentration = self._create_df_result(
            soluble_concentration,
            columns=solver_data.species_names,
        ).rename_axis(columns="Species Conc. [mol/L]")

        solids_concentration = pd.DataFrame(
            concentrations[:, solver_data.nc : (solver_data.nc + solver_data.nf)],
            index=self.result_index,
        )

        saturation_index = pd.DataFrame(
            _compute_saturation_index(
                result[:, : solver_data.nc], log_ks, solver_data.solid_stoichiometry
            ),
            index=self.result_index,
        )
        precipitate_check = pd.DataFrame(
            (solids_concentration > 0).replace({True: "*", False: ""}),
            index=self.result_index,
            dtype=str,
        )

        solids_concentration = self._create_df_result(
            pd.concat(
                (solids_concentration, precipitate_check, saturation_index),
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
                        solids_concentration.columns,
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
        )

        solubility_products = (
            pd.DataFrame()
            if not solver_data.ionic_strength_dependence
            else self._create_df_result(
                log_ks,
                columns=solver_data.species_names[solver_data.nc :],
            )
        ).rename_axis(columns="Solubility Products")

        self._storeResult(species_info, "species_info", log=True)
        self._storeResult(solids_info, "solids_info", log=True)
        self._storeResult(comp_info, "comp_info", log=True)

        self._storeResult(soluble_concentration, "species_concentrations", log=True)
        self._storeResult(solids_concentration, "solids_concentrations", log=True)

        # If working at variable ionic strength print and store formation constants/solubility products aswell
        self._storeResult(formation_constants, "formation_constants", log=True)
        self._storeResult(solubility_products, "solubility_products", log=True)

        if self.data["emode"] is True:
            soluble_sigma, solids_sigma = uncertanties(
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
                soluble_sigma,
                columns=solver_data.species_names,
            )

            solids_sigma = self._create_df_result(
                solids_sigma,
                columns=solver_data.solids_names,
            )

            self._storeResult(soluble_sigma, "species_sigma", log=True)
            self._storeResult(solids_sigma, "solid_sigma", log=True)

        self.signals.log.emit("Elapsed Time: %s s" % elapsed_time)

        self.signals.log.emit("### FINISHED ###")
        self.signals.finished.emit()
        return None

        # Print and store species percentages
        self._storeResult(
            optimizer.speciesPercentages(), "species_percentages", log=True
        )
        # Print and store solid species percentages
        self._storeResult(optimizer.solidPercentages(), "solid_percentages", log=True)
        return None

    def _storeResult(self, data: pd.DataFrame, name: str, log=False):
        self.signals.result.emit(data, name)
        if log and not data.empty:
            self.signals.log.emit("\t\t" + name.replace("_", " ").upper() + "\n")
            self.signals.log.emit(data.to_string())
            self.signals.log.emit("--" * 40)

    def _create_df_result(self, data, columns: list | None = None):
        if data is None:
            return pd.DataFrame()
        else:
            result = pd.DataFrame(
                data, index=self.result_index, columns=columns
            ).rename_axis(index=self.index_name)
            if self.ionic_strength_dependence:
                result.insert(0, "I", self.ionic_strength)
                result.set_index("I", append=True, inplace=True)

            return result

    def _simple_calculation(self, solver_data: SolverData):
        if mode == "titration":
            result, log_beta, log_ks, saturation_index, total_concentration = EqSolver(
                solver_data, mode=mode
            )
        elif mode == "distribution":
            result, log_beta, log_ks, saturation_index, total_concentration = EqSolver(
                solver_data, mode=mode
            )

    def _optimization(self, solver):
        pass
