import logging
from collections import deque

import numpy as np
import pandas as pd
from numpy.typing import NDArray


class BaseSolver:
    def __init__(
        self,
        *,
        epsl: int = 200,
        max_nr_iters: int = 200,
        jacobian_mode: str = "Normal mode",
    ):
        self.epsl = epsl
        self.jacobian_mode = jacobian_mode
        self.max_nr_iters = max_nr_iters
        self.done_flag = False

    def load(self, data):
        logging.info("--- START DATA LOADING ---")
        match self.jacobian_mode:
            case "Normal mode":
                self.jacobian_function = self._computeNormalJacobian
                self.residual_function = self._computeNormalDelta
                self.apply_shift_function = self._applyNormalShift
            case "Mixed mode":
                self.jacobian_function = self._computeMixedJacobian
                self.residual_function = self._computeMixedDelta
                self.apply_shift_function = self._applyMixedShift
            case "Log mode":
                self.jacobian_function = self._computeLogJacobian
                self.residual_function = self._computeLogDelta
                self.apply_shift_function = self._applyLogShift

            case _:
                raise Exception("Jacobian method not available")

        if data["dmode"] == 0:
            self.distribution = False
        else:
            self.distribution = True

        if data["emode"] == 1:
            self.errors = True
        else:
            self.errors = False

        self.imode = data["imode"]

        self.comp_charge = pd.DataFrame(data["compModel"])["Charge"]
        species_data: pd.DataFrame = pd.DataFrame(data["speciesModel"])
        solid_data: pd.DataFrame = pd.DataFrame(data["solidSpeciesModel"])
        conc_data = pd.DataFrame(data["concModel"])

        self._load_mode_params(data)

        # Check if the number of points in the range of pH is greater then 0
        if self.nop == 0:
            raise Exception("Number of points in the -log[A] range shouldn't be 0.")

        # Analytical concentration of each component (including the ones that will be ignored)
        self.c_tot = conc_data.iloc[:, 0].copy().to_numpy(dtype="float")

        # Check if they are all zero
        if (self.c_tot == 0).all():
            raise Exception(
                "Analytical concentration shouldn't be zero for all components."
            )

        # Charges of components
        self.comp_charge = self.comp_charge.copy().to_numpy(dtype="int")

        ignored_comps = self._get_ignored_comps()

        # get number of effective components
        self.nc = int(len(conc_data)) - ignored_comps.sum()

        self._adjust_for_ignored_comps(ignored_comps)

        # Store the stoichiometric coefficients for the components
        # IMPORTANT: each component is considered as a species with logB = 0
        comp_model = np.identity(self.nc, dtype="int")

        # Ignore the rows relative to the flagged as ignored species and ignored solid species
        species_not_ignored = species_data.loc[species_data["Ignored"] == False]
        solid_not_ignored = solid_data.loc[solid_data["Ignored"] == False]

        species_duplicates = species_not_ignored.loc[
            species_not_ignored.duplicated(subset="Name", keep="first").to_list(),
            "Name",
        ]
        if not species_duplicates.empty:
            raise Exception(
                f"Species {', '.join(species_duplicates.to_list())} with indices"
                f" {', '.join(species_duplicates.index.astype(str).to_list())} appear"
                " to be duplicates, you can and should remove them to avoid"
                " ambiguities in the results."
            )

        solids_duplicates = solid_not_ignored.loc[
            solid_not_ignored.duplicated(subset="Name", keep="first").to_list(),
            "Name",
        ]
        if not solids_duplicates.empty:
            raise Exception(
                f"Solids {', '.join(solids_duplicates.to_list())} with indices"
                f" {', '.join(solids_duplicates.index.astype(str).to_list())} appear to"
                " be duplicates, you can and should remove them to avoid ambiguities"
                " in the results."
            )

        # Store the stoichiometric coefficients for the species and solid species
        base_model = species_not_ignored.iloc[:, 8:-1].to_numpy(dtype="int").T
        solid_model = solid_not_ignored.iloc[:, 8:-1].to_numpy(dtype="int").T

        # Stores log_betas and log_ks of not ignored species
        base_log_beta = species_not_ignored.iloc[:, 2].to_numpy(dtype="float")
        base_log_ks = solid_not_ignored.iloc[:, 2].to_numpy(dtype="float")

        # Store comp_names
        self.comp_names = conc_data.index
        ignored_comp_names = self.comp_names[ignored_comps]
        self.comp_names = np.delete(self.comp_names, ignored_comps, 0)

        # Store for each species which component is used to calculate relative percentage.
        self.species_perc_str = species_not_ignored.iloc[:, -1].to_numpy(dtype="str")
        self.solid_perc_str = solid_not_ignored.iloc[:, -1].to_numpy(dtype="str")

        # Remove all the species and solid species that have one or more ignored comp with not null coeff.
        # with their relative betas and component for percentage computation
        species_to_remove = (base_model[ignored_comps, :] != 0).sum(axis=0) != 0
        solid_to_remove = (solid_model[ignored_comps, :] != 0).sum(axis=0) != 0
        base_model = np.delete(base_model, species_to_remove, axis=1)
        solid_model = np.delete(solid_model, solid_to_remove, axis=1)
        base_log_beta = np.delete(base_log_beta, species_to_remove, axis=0)
        base_log_ks = np.delete(base_log_ks, solid_to_remove, axis=0)
        self.species_perc_str = np.delete(
            self.species_perc_str, species_to_remove, axis=0
        )
        self.solid_perc_str = np.delete(self.solid_perc_str, solid_to_remove, axis=0)

        # Delete the columns for the coeff relative to the ignored components
        base_model = np.delete(base_model, ignored_comps, axis=0)
        solid_model = np.delete(solid_model, ignored_comps, axis=0)

        # Transforms the component used to calculate percentages from string to the corresponding index
        # If any of the species or solid species would use one of the ignored comps
        # assign the index for computation as if the independent comp
        # would be used instead (its percent value will be zero)
        self.species_perc_int, self.solid_perc_int = self._perc_encoder(
            ignored_comp_names
        )

        # Assemble the models and betas matrix
        self.model = np.concatenate((comp_model, base_model), axis=1)
        self.log_beta_ris = np.concatenate(
            (np.array([0 for _ in range(self.nc)]), base_log_beta), axis=0
        )
        self.solid_model = solid_model
        self.log_ks_ris = base_log_ks

        # Get the number of not-ignored species/solid species
        self.ns = base_model.shape[1]
        self.nf = solid_model.shape[1]

        # Number of components and number of species/solids has to be > 0
        if self.nc <= 0 | (self.ns <= 0 & self.nf <= 0):
            raise Exception(
                "Number of components and number of not ignored species should be more"
                " then zero."
            )

        if self.errors:
            self._set_errors_params(
                conc_data,
                species_not_ignored,
                solid_not_ignored,
                ignored_comps,
                species_to_remove,
                solid_to_remove,
            )

        if self.imode == 1:
            self._set_ionic_strength_params()

        # Compose species names from the model
        self.species_names = (
            list(self.comp_names)
            + species_not_ignored.iloc[~species_to_remove, 1].to_list()
        )
        self.solid_names = solid_not_ignored.iloc[~solid_to_remove, 1].to_list()

        logging.info("--- DATA LOADED ---")

    def calculate(self):
        logging.info("--- BEGINNING CALCULATION --- ")
        (
            species,
            solid,
            si,
            species_sigma,
            solid_sigma,
            log_b,
            log_ks,
            ionic_strength,
        ) = self._compute()

        # Set the flag to signal a completed run
        self.done_flag = True

        # Create the table containing the species/comp. concentration
        self.species_distribution = pd.DataFrame(
            species,
            columns=self.species_names,
        ).rename_axis(columns="Species Conc. [mol/L]")
        self.species_distribution = self._set_dataframe_index(self.species_distribution)

        # Compute and create table with percentages of species with respect to component
        # As defined with the input
        species_perc_table = self._computer_perc_table(
            self.perc_cans, species, self.model, self.species_perc_int
        )

        # Percentages are rounded two the second decimal and stored in a dataframe
        self.species_percentages = (
            pd.DataFrame(
                species_perc_table,
                columns=[self.species_names, self.species_perc_str],
            )
            .rename_axis(columns=["Species", r"% relative to comp."])
            .round(2)
        )
        self.species_percentages = self._set_dataframe_index(self.species_percentages)

        if self.nf > 0:
            # Create the table containing the solid species "concentration"
            self.solid_distribution = pd.DataFrame(
                solid, columns=self.solid_names
            ).rename_axis(columns="Solid Conc. [mol/L]")
            check = pd.DataFrame(
                [
                    ["*" if i > 0 else "" for i in row]
                    for row in self.solid_distribution.values
                ],
                columns=["Prec." + name for name in self.solid_distribution.columns],
                index=self.solid_distribution.index,
                dtype=str,
            )
            saturation_index = pd.DataFrame(
                si, columns=["SI" + name for name in self.solid_names]
            )

            self.solid_distribution = pd.concat(
                [self.solid_distribution, check, saturation_index],
                axis=1,
                sort=True,
            )
            self.solid_distribution = self.solid_distribution[
                sum(
                    [
                        [check_col, si_col, solid_col]
                        for check_col, si_col, solid_col in zip(
                            check.columns,
                            saturation_index.columns,
                            self.solid_distribution.columns,
                        )
                    ],
                    [],
                )
            ]
            self.solid_distribution = self._set_dataframe_index(self.solid_distribution)

            # Compute solid percentages as for species percentages
            solid_perc_table = self._computer_perc_table(
                self.perc_cans,
                solid,
                self.solid_model,
                self.solid_perc_int,
                solids=True,
            )

            self.solid_percentages = (
                pd.DataFrame(
                    solid_perc_table,
                    columns=[self.solid_names, self.solid_perc_str],
                )
                .rename_axis(columns=["Solids", r"% relative to comp."])
                .round(2)
            )
            self.solid_percentages = self._set_dataframe_index(self.solid_percentages)

        if self.errors:
            # For error propagation create the corresponding tables
            self.species_sigma = pd.DataFrame(
                species_sigma, columns=self.species_names
            ).rename_axis(columns="Species Std. Dev. [mol/L]")
            self.species_sigma = self._set_dataframe_index(self.species_sigma)

            if self.nf > 0:
                self.solid_sigma = pd.DataFrame(
                    solid_sigma, columns=self.solid_names
                ).rename_axis(columns="Solid Std. Dev. [mol]")
                self.solid_sigma = self._set_dataframe_index(self.solid_sigma)

        # If working at variable ionic strength
        if self.imode == 1:
            # Add multi index to the species distribution containing the ionic strength
            self.species_distribution.insert(0, "I", ionic_strength)
            self.species_distribution.set_index("I", append=True, inplace=True)

            # Create table containing adjusted LogB for each point
            self.log_beta = pd.DataFrame(
                log_b[:, self.nc :],
                columns=self.species_names[self.nc :],
            ).rename_axis(columns="Formation Constants")
            self.log_beta = self._set_dataframe_index(self.log_beta)

            self.log_beta.insert(0, "I", ionic_strength)
            self.log_beta.set_index("I", append=True, inplace=True)

            if self.nf > 0:
                self.solid_distribution.insert(0, "I", ionic_strength)
                self.solid_distribution.set_index("I", append=True, inplace=True)
                # Create table containing adjusted LogKs for each point
                self.log_ks = pd.DataFrame(
                    log_ks,
                    columns=self.solid_names,
                ).rename_axis(columns="Solubility Products")
                self.log_ks = self._set_dataframe_index(self.log_ks)

                self.log_ks.insert(0, "I", ionic_strength)
                self.log_ks.set_index("I", append=True, inplace=True)

        logging.info("--- CALCULATION TERMINATED ---")

        return True

    def _compute(self):
        # Initialize array to contain the species concentration
        # obtained from the calculations
        for_estimation_c = deque(maxlen=3)
        results_species_conc = np.zeros(
            dtype=float, shape=(self.nop, self.ns + self.nc)
        )
        results_solid_conc = np.zeros(dtype=float, shape=(self.nop, self.nf))
        results_solid_si = np.zeros(dtype=float, shape=(self.nop, self.nf))
        results_species_sigma = np.zeros(
            dtype=float, shape=(self.nop, self.ns + self.nc)
        )
        results_solid_sigma = np.zeros(dtype=float, shape=(self.nop, self.nf))
        results_log_b = np.zeros(dtype=float, shape=(self.nop, self.ns + self.nc))
        results_log_ks = np.zeros(dtype=float, shape=(self.nop, self.nf))
        results_ionic_strength = np.zeros(dtype=float, shape=(self.nop, 1))

        # Cycle over each point of titration
        for point in range(self.nop):
            logging.debug("--> OPTIMIZATION POINT: %s", point)

            if self.distribution:
                c, fixed_c = self._distributionGuess(point, for_estimation_c)
            else:
                fixed_c = None
                c = self._titrationGuess(point, for_estimation_c)

            # Initial guess for solids concentrations should always be zero
            cp = np.zeros(self.nf)

            logging.debug("INITIAL ESTIMATED FREE C: %s", c)
            logging.debug("TOTAL C: %s", self.c_tot[point])

            shifts_to_calculate = np.array(
                [True for _ in range(self.nc)] + [False for _ in range(self.nf)]
            )

            shifts_to_calculate, shifts_to_skip = self._getComputableShifts(
                shifts_to_calculate
            )
            # Calculate species concentration for aqueous species only
            (
                species_conc_calc,
                solid_conc_calc,
                log_b,
                log_ks,
                ionic_strength,
            ) = self._solve_point(
                point,
                c,
                cp,
                self.c_tot[point],
                fixed_c,
                shifts_to_calculate,
                shifts_to_skip,
                with_solids=False,
            )

            # Store concentrations before solid precipitation to estimate next points c
            for_estimation_c.append(species_conc_calc)

            saturation_index_calc = np.zeros(self.nf)
            adjust_solids = True and (self.nf > 0)
            while adjust_solids:
                saturation_index = self._getSaturationIndex(
                    species_conc_calc[: self.nc], log_ks
                )

                # Check which solids are to be considered
                shifts_to_calculate, shifts_to_skip = self._getComputableShifts(
                    shifts_to_calculate, saturation_index, solid_conc_calc
                )

                if shifts_to_calculate[-self.nf :].any():
                    (
                        species_conc_calc,
                        solid_conc_calc,
                        log_b,
                        log_ks,
                        ionic_strength,
                    ) = self._solve_point(
                        point,
                        species_conc_calc[: self.nc],
                        solid_conc_calc,
                        self.c_tot[point],
                        fixed_c,
                        shifts_to_calculate,
                        shifts_to_skip,
                        with_solids=True,
                    )
                else:
                    saturation_index_calc = saturation_index
                    adjust_solids = False

            if self.errors:
                species_sigma, solid_sigma = self._computeErrors(
                    species_conc_calc,
                    solid_conc_calc,
                    saturation_index_calc,
                    log_b,
                    log_ks,
                    point,
                )
            else:
                species_sigma = np.array([None for _ in range(self.nc + self.ns)])
                solid_sigma = np.array([None for _ in range(self.nf)])

            # Store calculated species/solid concentration into a vector
            results_species_conc[point, :] = species_conc_calc
            results_solid_conc[point, :] = solid_conc_calc

            results_solid_si[point, :] = saturation_index_calc
            # Store uncertainty for calculated values
            results_species_sigma[point, :] = species_sigma
            results_solid_sigma[point, :] = solid_sigma
            # Store calculated ionic strength
            results_ionic_strength[point] = ionic_strength
            # Store calculated LogB/LogKs
            results_log_b[point, :] = log_b
            results_log_ks[point, :] = log_ks

        # Return distribution/logb/ionic strength
        return (
            results_species_conc,
            results_solid_conc,
            results_solid_si,
            results_species_sigma,
            results_solid_sigma,
            results_log_b,
            results_log_ks,
            results_ionic_strength,
        )

    def _solve_point(
        self,
        point,
        c,
        cp,
        c_tot,
        fixed_c,
        shifts_to_calculate,
        shifts_to_skip,
        with_solids=False,
    ):
        pass

    def _after_jacobian_func(self):
        pass

    def _pre_jacobian_func(self):
        pass

    def _pre_residual_func(self):
        pass

    def _after_residual_func(self):
        pass

    def _perc_encoder(self, ignored_comp_names):
        comp_encoder = dict(zip(self.comp_names, range(self.comp_names.shape[0])))
        invalid_comp_encoder = dict(
            zip(ignored_comp_names, range(len(ignored_comp_names)))
        )
        default_value = self.ind_comp if self.distribution else 0
        species_perc_int = self.species_perc_str
        solid_perc_int = self.solid_perc_str
        self.species_perc_str = np.concatenate(
            (self.comp_names, self.species_perc_str), axis=0
        )
        for key, value in comp_encoder.items():
            species_perc_int = np.where(
                species_perc_int == key, value, species_perc_int
            )
            solid_perc_int = np.where(solid_perc_int == key, value, solid_perc_int)
        for key, value in invalid_comp_encoder.items():
            species_perc_int = np.where(
                species_perc_int == key, default_value, species_perc_int
            )
            solid_perc_int = np.where(
                solid_perc_int == key, default_value, solid_perc_int
            )
        return species_perc_int.astype(int), solid_perc_int.astype(int)

    def _set_errors_params(
        self,
        conc_data,
        species_not_ignored,
        solid_not_ignored,
        ignored_comps,
        species_to_remove,
        solid_to_remove,
    ):
        self.c0_sigma = conc_data.iloc[:, 2].copy().to_numpy(dtype="float")
        self.c0_sigma = np.delete(self.c0_sigma, ignored_comps)

        self.log_beta_sigma = species_not_ignored.iloc[:, 3].to_numpy(dtype="float")
        self.log_ks_sigma = solid_not_ignored.iloc[:, 3].to_numpy(dtype="float")

        self.log_beta_sigma = np.delete(self.log_beta_sigma, species_to_remove, axis=0)
        self.log_ks_sigma = np.delete(self.log_ks_sigma, solid_to_remove, axis=0)

        self.beta_sigma = (
            self.log_beta_sigma * np.log(10) * (10 ** self.log_beta_ris[self.nc :])
        )

        self.ks_sigma = self.log_ks_sigma * np.log(10) * (10**self.log_ks_ris)

    def _set_ionic_strength_params(
        self,
        data,
        species_not_ignored,
        solid_not_ignored,
        species_to_remove,
        solid_to_remove,
    ):
        # Load reference ionic strength
        self.species_ris = species_not_ignored.iloc[:, 4].to_numpy(dtype="float")
        self.solid_ris = solid_not_ignored.iloc[:, 4].to_numpy(dtype="float")

        # Remove ionic strength for species/solids that are ignored
        self.species_ris = np.delete(self.species_ris, species_to_remove, axis=0)
        self.solid_ris = np.delete(self.solid_ris, solid_to_remove, axis=0)

        # If ref. ionic strength is not given for one of the species use the reference one
        self.species_ris = np.where(
            self.species_ris == 0, data["ris"], self.species_ris
        )
        self.solid_ris = np.where(self.solid_ris == 0, data["ris"], self.solid_ris)

        # Add ref. ionic strength for components
        self.species_ris = np.insert(
            self.species_ris, 0, [data["ris"] for _ in range(self.nc)]
        )
        # Calculate square root of reference ionic strength for species
        self.species_radqris = np.sqrt(self.species_ris)
        self.solid_radqris = np.sqrt(self.solid_ris)

        a = data["a"]
        self.b = data["b"]
        c = [data["c0"], data["c1"]]
        d = [data["d0"], data["d1"]]
        e = [data["e0"], data["e1"]]

        # Check if default have to be used
        if (a == 0) & (self.b == 0):
            a = 0.5
            self.b = 1.5

        # Compute p* for alla the species
        species_past = self.model.sum(axis=0) - 1
        solid_past = self.solid_model.sum(axis=0)

        # Reshape charges into a column vector
        comp_charge_column = np.reshape(self.comp_charge, (self.nc, 1))

        # Compute species charges
        self.species_charges = (self.model * comp_charge_column).sum(axis=0)
        self.solid_charges = (self.solid_model * comp_charge_column).sum(axis=0)

        # Compute z* for all the species
        species_zast = (self.model * (comp_charge_column**2)).sum(axis=0) - (
            self.species_charges
        ) ** 2
        solid_zast = (self.solid_model * (comp_charge_column**2)).sum(axis=0)

        # Compute A/B term of D-H equation
        self.species_az = a * species_zast
        self.solid_az = a * solid_zast

        self.species_fib = self.species_radqris / (1 + (self.b * self.species_radqris))
        self.solid_fib = self.solid_radqris / (1 + (self.b * self.solid_radqris))

        # For both species and solids sets the Debye-Huckle parameters used to update their defining constants
        (self.species_cg, self.species_dg, self.species_eg) = self._set_dbh_params(
            species_not_ignored,
            species_to_remove,
            species_past,
            species_zast,
            c,
            d,
            e,
        )

        (self.solid_cg, self.solid_dg, self.solid_eg) = self._set_dbh_params(
            solid_not_ignored,
            solid_to_remove,
            solid_past,
            solid_zast,
            c,
            d,
            e,
            solids=True,
        )

    def _load_mode_params(self, data):
        raise NotImplementedError

    def _get_ignored_comps(self):
        raise NotImplementedError

    def _adjust_for_ignored_comps(self, ignored_comps):
        self.c_tot = np.delete(self.c_tot, ignored_comps, 0)
        self.comp_charge = np.delete(self.comp_charge, ignored_comps)

    def _get_species_concentration(self, c, cp, log_beta):
        """Calculate species concentration it returns c_spec and c_tot_calc:
        - c_spec[0->nc] = free conc for each component.
        - c_spec[nc+1->nc+ns] = species concentrations.
        - c_tot_calc = estimated anaytical concentration.
        """
        log_c_spec = self._check_over_under_flow(
            np.sum(np.log10(c)[:, np.newaxis] * self.model, axis=0) + log_beta
        )

        c_spec = 10**log_c_spec
        logging.debug("Species Concentrations: %s", c_spec)

        # Estimate total concentration given the species concentration
        c_tot_calc = np.dot(self.model, c_spec)

        if self.nf > 0:
            c_tot_calc += np.dot(self.solid_model, cp)

        logging.debug("Calculated Total Concentration: %s", c_tot_calc)

        return c_spec, c_tot_calc

    def _check_over_under_flow(self, c, d=1):
        """
        Given c check if any of the given log of concentrations would give overflow or underflow errors, adjust accordingly
        """
        c = np.clip(c, -self.epsl / d, self.epsl / d)
        return c

    def _set_dbh_params(self, species, to_remove, past, zast, c, d, e, solids=False):
        # Retrive CG/DG/EG for each of the species
        # Remove values that refers to ignored comps
        cg = species.iloc[:, 5].to_numpy(dtype="float")
        dg = species.iloc[:, 6].to_numpy(dtype="float")
        eg = species.iloc[:, 7].to_numpy(dtype="float")
        cg = np.delete(cg, to_remove, axis=0)
        dg = np.delete(dg, to_remove, axis=0)
        eg = np.delete(eg, to_remove, axis=0)

        if not solids:
            # If computing solution species adds values for components
            cg = np.insert(cg, 0, [0 for _ in range(self.nc)])
            dg = np.insert(dg, 0, [0 for _ in range(self.nc)])
            eg = np.insert(eg, 0, [0 for _ in range(self.nc)])

        use_reference = (cg == 0) + (dg == 0) + (eg == 0)

        # Compute CG/DG/EG terms of D-H
        reference_cg = c[0] * past + c[1] * zast
        reference_dg = d[0] * past + d[1] * zast
        reference_eg = e[0] * past + e[1] * zast

        cg = np.where(use_reference, reference_cg, cg)
        dg = np.where(use_reference, reference_dg, dg)
        eg = np.where(use_reference, reference_eg, eg)

        return cg, dg, eg

    def get_species_distribution(self):
        """
        Returns the species concentration table.
        """
        if not self.done_flag:
            return False
        return self.species_distribution

    def get_solid_distribution(self):
        """
        Returns the solid species concentration table.
        """
        if not self.done_flag:
            return False
        try:
            return self.solid_distribution
        except AttributeError:
            return pd.DataFrame()

    def get_formation_constants(self):
        """
        Returns the table containing formation constants and the ionic strength.
        """
        if not self.done_flag:
            return False
        try:
            return self.log_beta
        except AttributeError:
            return pd.DataFrame()

    def get_solubility_products(self):
        """
        Returns the table containing the LogKps for the solid species present in the model.
        """
        if not self.done_flag:
            return False
        try:
            return self.log_ks
        except AttributeError:
            return pd.DataFrame()

    def get_species_percentages(self):
        """
        Return percentages of species with respect to the desired component.
        """
        if not self.done_flag:
            return False
        return self.species_percentages

    def get_solid_percentages(self):
        """
        Return percentages of solids with respect to the desired component.
        """
        if not self.done_flag:
            return False
        try:
            return self.solid_percentages
        except AttributeError:
            return pd.DataFrame()

    def get_species_sigmas(self):
        """
        Return percentages of species with respect to the desired component.
        """
        if not self.done_flag:
            return False
        try:
            return self.species_sigma
        except AttributeError:
            return pd.DataFrame()

    def get_solid_sigmas(self):
        """
        Return percentages of solids with respect to the desired component.
        """
        if not self.done_flag:
            return False
        try:
            return self.solid_sigma
        except AttributeError:
            return pd.DataFrame()

    def get_parameters(self):
        """
        Returns relevant data that was used for the computation
        """
        if not self.done_flag:
            return False
        species_info = pd.DataFrame(
            {
                "logB": self.log_beta_ris[self.nc :],
            },
            index=self.species_names[self.nc :],
        ).rename_axis(index="Species Names")

        if self.nf > 0:
            solid_info = pd.DataFrame(
                {
                    "logKs": self.log_ks_ris,
                },
                index=self.solid_names,
            ).rename_axis(index="Solid Names")
        else:
            solid_info = pd.DataFrame()

        if self.imode == 1:
            species_info.insert(1, "Ref. I", self.species_ris[self.nc :])
            species_info.insert(2, "Charge", self.species_charges[self.nc :])
            species_info.insert(3, "C", self.species_cg[self.nc :])
            species_info.insert(4, "D", self.species_dg[self.nc :])
            species_info.insert(5, "E", self.species_eg[self.nc :])

            if self.nf > 0:
                solid_info.insert(1, "Ref. I", self.solid_ris)
                solid_info.insert(2, "Charge", self.solid_charges)
                solid_info.insert(3, "C", self.solid_cg)
                solid_info.insert(4, "D", self.solid_dg)
                solid_info.insert(5, "E", self.solid_eg)

        if self.errors:
            species_info.insert(1, "Sigma logB", self.log_beta_sigma)

            if self.nf > 0:
                solid_info.insert(1, "Sigma logKs", self.log_ks_sigma)

        comp_info = pd.DataFrame(
            {
                "Charge": self.comp_charge,
            },
            index=self.species_names[: self.nc],
        ).rename_axis(index="Components Names")

        return species_info, solid_info, comp_info

    def _applyNormalShift(self, c, cp, shifts):
        one_over_del = -shifts[: self.nc] / (0.5 * c)

        rev_del = 1 / np.where(one_over_del > 1, one_over_del, 1)
        c = c + rev_del[: self.nc] * shifts[: self.nc]

        # if with_solids:
        cp = cp + shifts[self.nc :]

        return c, cp

    def _applyMixedShift(self, c, cp, shifts):
        one_over_del = (-shifts[: self.nc] * c) / (0.5 * c)

        rev_del = 1 / np.where(one_over_del > 1, one_over_del, 1)
        c = c + shifts[: self.nc] * c * rev_del[: self.nc]

        # if with_solids:
        cp = cp + shifts[self.nc :]

        return c, cp

    def _applyLogShift(self, c, cp, shifts):
        # one_over_del = -shifts[: self.nc] / (0.5 * np.log10(c))

        # rev_del = 1 / np.where(one_over_del > 1, one_over_del, 1)
        # c = c + rev_del[: self.nc] * shifts[: self.nc]
        c = 10 ** (np.log10(c) + shifts[: self.nc])

        # if with_solids:
        # cp = cp + shifts[self.nc :]
        cp = 10 ** (np.log10(cp) + shifts[self.nc :])

        return c, cp

    def _computeNormalDelta(
        self,
        c,
        c_tot,
        c_tot_calc,
        log_ks,
        with_solids,
        cp_to_calculate,
    ):
        can_delta = c_tot_calc - c_tot

        if with_solids:
            solid_delta = np.ones(self.nf) - self._getSaturationIndex(c, log_ks)
            solid_delta = solid_delta[cp_to_calculate]
        else:
            solid_delta = []

        delta = np.concatenate((can_delta, solid_delta))

        return delta, can_delta, solid_delta

    def _computeMixedDelta(
        self,
        c,
        c_tot,
        c_tot_calc,
        log_ks,
        with_solids,
        cp_to_calculate,
    ):
        can_delta = c_tot_calc - c_tot

        if with_solids:
            solid_delta = (
                np.sum(np.tile(np.log10(c), [self.nf, 1]).T * self.solid_model, axis=0)
                - log_ks
            )
            solid_delta = solid_delta[cp_to_calculate]
        else:
            solid_delta = []

        delta = np.concatenate((can_delta, solid_delta))

        return delta, can_delta, solid_delta

    def _computeLogDelta(
        self,
        c,
        c_tot,
        c_tot_calc,
        log_ks,
        with_solids,
        cp_to_calculate,
    ):
        can_delta = c_tot_calc - c_tot

        if with_solids:
            solid_delta = (
                np.sum(np.tile(np.log10(c), [self.nf, 1]).T * self.solid_model, axis=0)
                - log_ks
            )
            solid_delta = solid_delta[cp_to_calculate]
        else:
            solid_delta = []

        delta = np.concatenate((can_delta, solid_delta))

        return delta, can_delta, solid_delta

    def _computeNormalJacobian(self, c_spec, saturation_index, with_solids, to_skip):
        if with_solids:
            nt = self.nc + self.nf
            to_skip_with_species = np.concatenate((
                [False for _ in range(self.nc)],
                to_skip,
            ))
        else:
            nt = self.nc
            to_skip_with_species = np.array([False for _ in range(self.nc)])

        J = np.zeros(shape=(nt, nt))

        # Compute Jacobian
        # Jacobian for aqueous species
        J[: self.nc, : self.nc] = (
            (
                np.tile(c_spec, (self.nc, self.nc, 1))
                / np.tile(
                    c_spec[: self.nc].reshape((self.nc, 1)),
                    (self.nc, 1, self.ns + self.nc),
                )
            )
            * np.tile(self.model, (self.nc, 1, 1))
            * np.rot90(np.tile(self.model, (self.nc, 1, 1)), -1, axes=(0, 1))
        ).sum(axis=-1)

        if with_solids:
            # Jacobian for solid species
            J[: self.nc, self.nc : nt] = self.solid_model

            J[self.nc : nt, : self.nc] = -self.solid_model.T * (
                np.tile(saturation_index, (self.nc, 1)).T
                / np.tile(c_spec[: self.nc], (nt - self.nc, 1))
            )
            # Remove rows and columns referring to under-saturated solids

        return J[np.ix_(~to_skip_with_species, ~to_skip_with_species)]

    def _computeLogJacobian(
        self, c_spec: NDArray, saturation_index, with_solids: bool, to_skip: list[bool]
    ):
        if with_solids:
            nt = self.nc + self.nf
            to_skip = np.concatenate(([False for _ in range(self.nc)], to_skip))
        else:
            nt = self.nc

        J = np.zeros(shape=(nt, nt) if with_solids else (self.nc, self.nc))

        # Compute Jacobian for binary components only
        J[np.tril_indices(self.nc)] = (
            c_spec[: self.nc].T @ self.model[: self.nc] @ c_spec[: self.nc]
        )

        # Add solid contribution to diagonal if necessary
        if with_solids:
            for i in range(self.nc, self.nc + self.nt):
                for j in range(self.nc):
                    J[i, j] = (
                        self.solid_model[i, saturation_index - 1]
                        * c_spec[saturation_index + self.nc]
                    )
        # Remove rows and columns referring to under-saturated solids if necessary
        return J[: nt - sum(to_skip), : nt - sum(to_skip)][~np.array(to_skip)]

    def _computeMixedJacobian(self, c_spec, saturation_index, with_solids, to_skip):
        if with_solids:
            nt = self.nc + self.nf
            to_skip_with_species = np.concatenate((
                [False for _ in range(self.nc)],
                to_skip,
            ))
        else:
            nt = self.nc
            to_skip_with_species = np.array([False for _ in range(self.nc)])

        J = np.zeros(shape=(nt, nt))

        # Compute Jacobian for binary components only
        J[: self.nc, : self.nc] = self.model @ np.diag(c_spec) @ self.model.T
        J[np.diag_indices(self.nc)] += c_spec[: self.nc]
        # Add solid contribution to diagonal if necessary
        if with_solids:
            J[self.nc : self.nc + self.nf, : self.nc] = self.solid_model.T
            J[: self.nc, self.nc : self.nc + self.nf] = self.solid_model
            # for i in range(self.nc, self.nc+self.nf):
            #     for j in range(self.nc):
            #         J[i, j] = self.solid_model[i - self.nc, j]
        # Remove rows and columns referring to under-saturated solids if necessary
        return J[np.ix_(~to_skip_with_species, ~to_skip_with_species)]

    def _damping(self, point, c, cp, log_beta, c_tot, fixed_c):
        logging.debug("ENTERING DAMP ROUTINE")

        epsilon = 2.5e-1 if point > 0 else 1e-9

        coeff = np.zeros(self.nc)
        a0 = np.max(np.abs(self.model[self.model != 0]), axis=1)

        iteration = 0
        while True:
            _, c_spec = self._get_species_concentration(c, cp, log_beta)

            c_times_model = c_spec[:, np.newaxis] * self.model

            sum_reac = np.clip(
                np.where(self.model > 0, c_times_model, 0).sum(axis=1)
                + np.abs(np.where(c_tot < 0, c_tot, 0)),
                0,
                None,
            )
            sum_prod = np.clip(
                np.where(c_tot >= 0, c_tot, 0)
                - np.where(self.model < 0, c_times_model, 0).sum(axis=1),
                0,
                None,
            )

            conv_criteria = (sum_reac - sum_prod) / (sum_reac + sum_prod)

            if np.all(conv_criteria < epsilon) or iteration >= 10000:
                logging.debug("EXITING DAMP ROUTINE")
                return c, c_spec

            new_coeff = (
                0.9
                - np.where(
                    sum_reac > sum_prod, sum_prod / sum_reac, sum_reac / sum_prod
                )
                * 0.8
            )

            if iteration == 0:
                coeff = new_coeff
            coeff = np.where(new_coeff > coeff, new_coeff, coeff)

            c *= coeff * (sum_prod / sum_reac) ** (1 / a0) + (1 - coeff)

            iteration += 1

    def _computer_perc_table(self, cans, calculated_c, model, percent_to, solids=False):
        can_to_perc = np.take(cans, percent_to, axis=1)

        if not solids:
            can_to_perc = np.concatenate((cans, can_to_perc), axis=1)

        adjust_factor = np.take(model, percent_to + (self.nc if not solids else 0))

        adjust_factor = np.where(adjust_factor <= 0, 1, adjust_factor)

        if not solids:
            adjust_factor = np.concatenate(([1] * self.nc, adjust_factor), axis=0)

        perc_table = np.where(
            can_to_perc == 0, 0, (calculated_c * adjust_factor) / can_to_perc
        )
        perc_table *= 100

        return perc_table

    def _set_dataframe_index(self, dataframe) -> pd.DataFrame:
        raise NotImplementedError

    

class Distribution(BaseSolver):
    def __init__(
        self,
        *,
        epsl: int = 200,
        max_nr_iters: int = 200,
        jacobian_mode: str = "Normal mode",
    ):
        super().__init__(
            epsl=epsl, max_nr_iters=max_nr_iters, jacobian_mode=jacobian_mode
        )

    def load(self, data):
        super().load(data)
        self.model = np.delete(self.model, self.ind_comp, axis=1)
        self.model = np.delete(self.model, self.ind_comp, axis=0)
        self.solid_model = np.delete(self.solid_model, self.ind_comp, axis=0)

        self.nc -= 1
        self.ns = self.model.shape[1] - self.nc
        self.nf = self.solid_model.shape[1]

    def _set_ionic_strength_params(
        self,
        data,
        species_not_ignored,
        solid_not_ignored,
        species_to_remove,
        solid_to_remove,
    ):
        super()._set_ionic_strength_params(
            data,
            species_not_ignored,
            solid_not_ignored,
            species_to_remove,
            solid_to_remove,
        )
        self.background_c = np.tile(data["cback"], self.nop)

    def _set_errors_params(
        self,
        conc_data,
        species_not_ignored,
        solid_not_ignored,
        ignored_comps,
        species_to_remove,
        solid_to_remove,
    ):
        super()._set_errors_params(
            conc_data,
            species_not_ignored,
            solid_not_ignored,
            ignored_comps,
            species_to_remove,
            solid_to_remove,
        )
        self.c0_sigma[self.ind_comp] = 0
        self.conc_sigma = np.tile(self.c0_sigma, [self.nop, 1])

    def _load_mode_params(self, data):
        self.ind_comp = data["ind_comp"]
        # Initial log value
        initial_log = data["initialLog"]
        # Final log value
        final_log = data["finalLog"]
        # log increments at each point
        log_increments = data["logInc"]

        # Final log value should be higher than the initial one
        if initial_log >= final_log:
            raise Exception("Initial -log[A] should be lower then final -log[A].")

        if log_increments == 0:
            raise Exception("Increment of -log[A] should be more then zero.")
        # Create two arrays (log and conc. of independent component)
        self.ind_comp_logs = np.arange(
            initial_log, (final_log + log_increments), log_increments
        )
        self.ind_comp_c = 10 ** (-self.ind_comp_logs)

        # Calculate the number of points in the interval
        self.nop = len(self.ind_comp_c)

    def _get_ignored_comps(self):
        return (self.c_tot == 0) & (np.arange(len(self.c_tot)) != self.ind_comp)

    def _adjust_for_ignored_comps(self, ignored_comps):
        super()._adjust_for_ignored_comps(ignored_comps)
        # for every ignored comp which index is lower
        # of the designated independent comp
        # reduce its index by one (they "slide over")
        self.ind_comp = self.ind_comp - ignored_comps[: self.ind_comp].sum()
        # Assign total concentrations for each point
        self.c_tot = np.delete(self.c_tot, self.ind_comp, 0)
        self.c_tot = np.tile(self.c_tot, [self.nop, 1])
        self.perc_cans = np.insert(self.c_tot, self.ind_comp, 0, axis=1)

    def _get_species_concentration(self, c, cp, log_beta):
        c_tot_calc, c_spec = super()._get_species_concentration(c, cp, log_beta)
        c_tot_calc = np.delete(c_tot_calc, self.ind_comp, 0)
        return c_spec, c_tot_calc

    def parameters(self):
        speces_info, solid_info, comp_info = super().parameters()
        comp_info["Tot. C."] = np.insert(self.c_tot[0], self.ind_comp, None)
        if self.errors:
            comp_info.insert(2, "Sigma Tot C", self.c0_sigma)
        return speces_info, solid_info, comp_info

    def _set_dataframe_index(self, dataframe) -> pd.DataFrame:
        return dataframe.set_index(self.ind_comp_logs).rename_axis(
            index="p[" + self.comp_names[self.ind_comp] + "]",
        )
