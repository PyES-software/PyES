import logging
from collections import deque

import numpy as np
import pandas as pd
from numba import jit, njit, prange
from numpy.typing import NDArray


class Distribution:
    """
    Newton-Raphson method to solve iteratively mass balance equations.
    """

    def __init__(self):
        # Set limit for underflow/overflow exp
        self.epsl = 200
        # Set flag to report that computation is done
        self.done_flag = False

    def fit(self, data):
        """
        Loads the data used to optimize the system.

        :param data: data as given from the GUI.
        """
        logging.info("--- START DATA LOADING ---")
        # Titration or Distribution mode
        if data["dmode"] == 0:
            self.distribution = False
        else:
            self.distribution = True

        if data["emode"] == 1:
            self.errors = True
        else:
            self.errors = False

        # Charge values of comps
        self.comp_charge = pd.DataFrame(data["compModel"])["Charge"]
        # Data relative to the species and solid species
        species_data: pd.DataFrame = pd.DataFrame(data["speciesModel"])
        solid_data: pd.DataFrame = pd.DataFrame(data["solidSpeciesModel"])
        # Data relative to comp concentrations
        conc_data = pd.DataFrame(data["concModel"])

        if self.distribution:
            # Independent comp
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
        else:
            self.c_added = conc_data.iloc[:, 1].copy().to_numpy(dtype="float")
            # Initial volume
            v0 = data["v0"] * 1e-3
            # First titration point volume
            initial_volume = data["initv"] * 1e-3
            # Volume increment at each point
            volume_increments = data["vinc"] * 1e-3
            # number of points
            self.nop = int(data["nop"])

            if v0 <= 0:
                raise Exception("Initial volume can't be zero")

            if volume_increments <= 0:
                raise Exception("Volume increments should be higher then 0.")

            if v0 > initial_volume:
                raise Exception(
                    "Initial titration volume should be higer or equal to initial"
                    " volume."
                )

            self.v_added = np.array([volume_increments * x for x in range(self.nop)])
            v1_diff = initial_volume - v0
            self.v_added += v1_diff
            v_tot = v0 + self.v_added

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

        # Find which components have to be ignored (c0 = 0)
        ignored_comps = (
            (self.c_tot == 0) & (np.arange(len(self.c_tot)) != self.ind_comp)
            if self.distribution
            else (self.c_tot == 0)
        )

        # Remove the concentration and charge data relative to those
        if not self.distribution:
            self.c_added = np.delete(self.c_added, ignored_comps, 0)
        self.c_tot = np.delete(self.c_tot, ignored_comps, 0)
        self.comp_charge = np.delete(self.comp_charge, ignored_comps)

        # get number of effective components
        self.nc = int(len(conc_data)) - ignored_comps.sum()

        if self.distribution:
            # for every ignored comp which index is lower
            # of the designated independent comp
            # reduce its index by one (they "slide over")
            self.ind_comp = self.ind_comp - ignored_comps[: self.ind_comp].sum()
            # Assign total concentrations for each point
            self.c_tot = np.delete(self.c_tot, self.ind_comp, 0)
            self.c_tot = np.tile(self.c_tot, [self.nop, 1])
        else:
            self.initial_c = self.c_tot
            self.c_tot = (
                (np.tile(self.c_tot, [self.nop, 1]) * v0)
                + (np.tile(self.v_added, [self.nc, 1]).T * self.c_added)
            ) / np.tile(v_tot, [self.nc, 1]).T
            self.c_tot[self.c_tot == 0] = -1e-9

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
        self.species_perc_int, self.solid_perc_int = self._percEncoder(
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
            self.c0_sigma = conc_data.iloc[:, 2].copy().to_numpy(dtype="float")
            self.c0_sigma = np.delete(self.c0_sigma, ignored_comps)
            if self.distribution:
                self.c0_sigma[self.ind_comp] = 0
                self.conc_sigma = np.tile(self.c0_sigma, [self.nop, 1])
            else:
                self.ct_sigma = conc_data.iloc[:, 3].copy().to_numpy(dtype="float")
                self.ct_sigma = np.delete(self.ct_sigma, ignored_comps)
                self.conc_sigma = np.tile(self.c0_sigma, [self.nop, 1]) + (
                    np.tile(self.v_added, [self.nc, 1]).T * self.ct_sigma
                )

            self.log_beta_sigma = species_not_ignored.iloc[:, 3].to_numpy(dtype="float")
            self.log_ks_sigma = solid_not_ignored.iloc[:, 3].to_numpy(dtype="float")

            self.log_beta_sigma = np.delete(
                self.log_beta_sigma, species_to_remove, axis=0
            )
            self.log_ks_sigma = np.delete(self.log_ks_sigma, solid_to_remove, axis=0)

            self.beta_sigma = (
                self.log_beta_sigma * np.log(10) * (10 ** self.log_beta_ris[self.nc :])
            )

            self.ks_sigma = self.log_ks_sigma * np.log(10) * (10**self.log_ks_ris)

        # Check the ionic strength mode
        # Load the required data if so
        self.imode = data["imode"]
        if self.imode == 1:
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

            # Load background ions concentration
            if self.distribution:
                self.background_c = np.tile(data["cback"], self.nop)
            else:
                background_c0 = data["c0back"]
                background_ct = data["ctback"]
                self.background_c = np.array(
                    ((background_c0 * v0) + (background_ct * self.v_added)) / v_tot
                )

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

            if self.distribution:
                # Same vector except missing the charge of the indipendent component, used later in the computation
                self.comp_charge_no_indipendent = np.delete(
                    self.comp_charge, self.ind_comp
                )

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

            self.species_fib = self.species_radqris / (
                1 + (self.b * self.species_radqris)
            )
            self.solid_fib = self.solid_radqris / (1 + (self.b * self.solid_radqris))

            # For both species and solids sets the Debye-Huckle parameters used to update their defining constants
            (self.species_cg, self.species_dg, self.species_eg) = self._setDBHParams(
                species_not_ignored,
                species_to_remove,
                species_past,
                species_zast,
                c,
                d,
                e,
            )

            (self.solid_cg, self.solid_dg, self.solid_eg) = self._setDBHParams(
                solid_not_ignored,
                solid_to_remove,
                solid_past,
                solid_zast,
                c,
                d,
                e,
                solids=True,
            )

        # Compose species names from the model
        self.species_names = (
            list(self.comp_names)
            + species_not_ignored.iloc[~species_to_remove, 1].to_list()
        )
        self.solid_names = solid_not_ignored.iloc[~solid_to_remove, 1].to_list()

        logging.info("--- DATA LOADED ---")

    def predict(self):
        """
        Given the loaded data returns species distribution.
        """
        # Calculate species distribution
        # Return formatted species distribution as a nice table
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
        self.species_distribution = self._setDataframeIndex(self.species_distribution)

        if self.distribution:
            cans = np.insert(self.c_tot, self.ind_comp, 0, axis=1)
        else:
            cans = self.c_tot

        # Compute and create table with percentages of species with respect to component
        # As defined with the input
        species_perc_table = self._computePercTable(
            cans, species, self.model, self.species_perc_int
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
        self.species_percentages = self._setDataframeIndex(self.species_percentages)

        if self.nf > 0:
            # Create the table containing the solid species "concentration"
            self.solid_distribution = pd.DataFrame(
                solid, columns=self.solid_names
            ).rename_axis(columns="Solid Conc. [mol/L]")
            check = self.solid_distribution.apply(
                lambda x: pd.Series(
                    ["*" if i > 0 else "" for i in x],
                    index=["Prec." + name for name in self.solid_distribution.columns],
                    dtype=str,
                ),
                axis=1,
            )
            saturation_index = pd.DataFrame(
                si, columns=["SI" + name for name in self.solid_names]
            )

            self.solid_distribution = pd.merge(
                self.solid_distribution,
                check,
                left_index=True,
                right_index=True,
                sort=True,
            )

            self.solid_distribution = pd.merge(
                self.solid_distribution,
                saturation_index,
                left_index=True,
                right_index=True,
                sort=True,
            )

            self.solid_distribution = self.solid_distribution[
                list(
                    sum(
                        zip(
                            check.columns,
                            saturation_index,
                            self.solid_distribution.columns,
                        ),
                        (),
                    )
                )
            ]
            self.solid_distribution = self._setDataframeIndex(self.solid_distribution)

            # Compute solid percentages as for species percentages
            solid_perc_table = self._computePercTable(
                cans, solid, self.solid_model, self.solid_perc_int, solids=True
            )

            self.solid_percentages = (
                pd.DataFrame(
                    solid_perc_table,
                    columns=[self.solid_names, self.solid_perc_str],
                )
                .rename_axis(columns=["Solids", r"% relative to comp."])
                .round(2)
            )
            self.solid_percentages = self._setDataframeIndex(self.solid_percentages)

        if self.errors:
            # For error propagation create the corresponding tables
            self.species_sigma = pd.DataFrame(
                species_sigma, columns=self.species_names
            ).rename_axis(columns="Species Std. Dev. [mol/L]")
            self.species_sigma = self._setDataframeIndex(self.species_sigma)

            if self.nf > 0:
                self.solid_sigma = pd.DataFrame(
                    solid_sigma, columns=self.solid_names
                ).rename_axis(columns="Solid Std. Dev. [mol]")
                self.solid_sigma = self._setDataframeIndex(self.solid_sigma)

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
            self.log_beta = self._setDataframeIndex(self.log_beta)

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
                self.log_ks = self._setDataframeIndex(self.log_ks)

                self.log_ks.insert(0, "I", ionic_strength)
                self.log_ks.set_index("I", append=True, inplace=True)

        logging.info("--- CALCULATION TERMINATED ---")

        return True

    def speciesDistribution(self):
        """
        Returns the species concentration table.
        """
        if self.done_flag:
            return self.species_distribution
        else:
            return False

    def solidDistribution(self):
        """
        Returns the solid species concentration table.
        """
        if self.done_flag:
            try:
                return self.solid_distribution
            except AttributeError:
                return pd.DataFrame()
        else:
            return False

    def formationConstants(self):
        """
        Returns the table containing formation constants and the ionic strength.
        """
        if self.done_flag:
            try:
                return self.log_beta
            except AttributeError:
                return pd.DataFrame()
        else:
            return False

    def solubilityProducts(self):
        """
        Returns the table containing the LogKps for the solid species present in the model.
        """
        if self.done_flag:
            try:
                return self.log_ks
            except AttributeError:
                return pd.DataFrame()
        else:
            return False

    def speciesPercentages(self):
        """
        Return percentages of species with respect to the desired component.
        """
        if self.done_flag:
            return self.species_percentages
        else:
            return False

    def solidPercentages(self):
        """
        Return percentages of solids with respect to the desired component.
        """
        if self.done_flag:
            try:
                return self.solid_percentages
            except AttributeError:
                return pd.DataFrame()

        else:
            return False

    def speciesSigmas(self):
        """
        Return percentages of species with respect to the desired component.
        """
        if self.done_flag:
            try:
                return self.species_sigma
            except AttributeError:
                return pd.DataFrame()
        else:
            return False

    def solidSigmas(self):
        """
        Return percentages of solids with respect to the desired component.
        """
        if self.done_flag:
            try:
                return self.solid_sigma
            except AttributeError:
                return pd.DataFrame()
        else:
            return False

    def parameters(self):
        """
        Returns relevant data that was used for the computation
        """
        if self.done_flag:
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

            if self.distribution:
                comp_info["Tot. C."] = np.insert(self.c_tot[0], self.ind_comp, None)
                if self.errors:
                    comp_info.insert(2, "Sigma Tot C", self.c0_sigma)
            else:
                comp_info["Vessel Conc."] = self.initial_c
                comp_info["Titrant Conc."] = self.c_added
                if self.errors:
                    comp_info.insert(2, "Sigma C0", self.c0_sigma)
                    comp_info.insert(4, "Sigma cT", self.ct_sigma)

            return species_info, solid_info, comp_info
        else:
            return False

    def _compute(self):
        """
        Calculate species distribution.
        """
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
            ) = self._newtonRaphson(
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
                    ) = self._newtonRaphson(
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

        # Stack calculated species concentration/logB/ionic strength in tabular fashion
        # results_species_conc = np.stack(results_species_conc)
        # results_solid_conc = np.stack(results_solid_conc)
        # results_solid_si = np.stack(results_solid_si)
        # results_species_sigma = np.stack(results_species_sigma)
        # results_solid_sigma = np.stack(results_solid_sigma)
        # results_log_b = np.stack(results_log_b)
        # results_log_ks = np.stack(results_log_ks)
        # results_ionic_strength = np.stack(results_ionic_strength)

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

    def _newtonRaphson(
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
        np.seterr(all="ignore")
        iteration = 0

        if not with_solids:
            # If working with variable ionic strength compute initial guess for species concentration
            if self.imode == 1:
                if point == 0:
                    log_beta, log_ks, _ = self._updateConstants(
                        c_tot,
                        self.log_beta_ris,
                        self.log_ks_ris,
                        self.comp_charge,
                        point,
                        first_guess=True,
                    )
                else:
                    log_beta = self.previous_log_beta
                    log_ks = self.previous_log_ks

                logging.debug("Estimate of LogB for point %s: %s", point, log_beta)

                c, c_spec = self._damping(point, c, cp, log_beta, c_tot, fixed_c)

                log_beta, log_ks, cis = self._updateConstants(
                    c_spec,
                    self.log_beta_ris,
                    self.log_ks_ris,
                    self.species_charges,
                    point,
                )

                self.previous_log_beta = log_beta
                self.previous_log_ks = log_ks
                logging.debug("Updated LogB: %s", log_beta)
            else:
                log_beta = self.log_beta_ris
                log_ks = self.log_ks_ris
                c, c_spec = self._damping(point, c, cp, log_beta, c_tot, fixed_c)
                cis = [None]
        else:
            if self.imode == 1:
                c_tot_calc, c_spec = self._speciesConcentration(
                    c, cp, self.previous_log_beta
                )
                log_beta, log_ks, cis = self._updateConstants(
                    c_spec,
                    self.log_beta_ris,
                    self.log_ks_ris,
                    self.species_charges,
                    point,
                )

                self.previous_log_beta = log_beta
                self.previous_log_ks = log_ks
            else:
                log_beta = self.log_beta_ris
                log_ks = self.log_ks_ris
                cis = [None]
            c, c_spec = self._damping(point, c, cp, log_beta, c_tot, fixed_c)

        # Calculate total concentration given the species concentration
        c_tot_calc, c_spec = self._speciesConcentration(c, cp, log_beta)

        # Calculate saturation index for solid species if any
        saturation_index = self._getSaturationIndex(c, log_ks)

        # Compute difference between total concentrations and calculated one
        delta, can_delta, solid_delta = self._computeDelta(
            c_tot,
            c_tot_calc,
            with_solids,
            saturation_index,
            shifts_to_calculate[-self.nf :],
        )

        while iteration < 2000:
            logging.debug(
                "-> BEGINNING NEWTON-RAPHSON ITERATION %s ON POINT %s", iteration, point
            )

            # Compute Jacobian
            J = self._computeJacobian(
                c_spec,
                saturation_index,
                with_solids,
                shifts_to_skip[-self.nf :],
            )

            if self.distribution:
                # Ignore row and column relative to the independent component
                J = np.delete(J, self.ind_comp, axis=0)
                J = np.delete(J, self.ind_comp, axis=1)

            # J, delta = self._scaleMatrix(J, delta)

            # Solve the equations to obtain newton step
            shifts = np.linalg.solve(J, -delta)

            actual_shifts = np.zeros(self.nc + self.nf)
            actual_shifts[shifts_to_calculate] = shifts
            shifts = actual_shifts

            # if self.distribution:
            #     shifts = np.insert(shifts, self.ind_comp, 0, axis=0)

            logging.debug(
                "Shifts to be applied to concentrations and precipitates: %s", shifts
            )

            # if with_solids:
            #     one_over_del = -shifts / (0.5 * np.append(c, cp))
            # else:
            one_over_del = -shifts[: self.nc] / (0.5 * c)

            rev_del = 1 / np.where(one_over_del > 1, one_over_del, 1)

            c = c + rev_del[: self.nc] * shifts[: self.nc]

            # if with_solids:
            cp = cp + shifts[self.nc :]

            logging.debug("Newton-Raphson updated free concentrations: %s", c)
            logging.debug("Newton-Raphson updated precipitate concentrations: %s", cp)

            # Calculate total concentration given the updated free/precipitate concentration
            c_tot_calc, c_spec = self._speciesConcentration(c, cp, log_beta)

            # Compute difference between total concentrations and convergence
            saturation_index = self._getSaturationIndex(c, log_ks)

            # Compute difference between total concentrations
            delta, can_delta, solid_delta = self._computeDelta(
                c_tot,
                c_tot_calc,
                with_solids,
                saturation_index,
                shifts_to_calculate[-self.nf :],
            )

            comp_conv_criteria = np.sum(can_delta / c_tot) ** 2

            logging.debug(
                (
                    "Convergence for analytical concentrations at Point %s iteration"
                    " %s: %s"
                ),
                point,
                iteration,
                comp_conv_criteria,
            )

            iteration += 1
            # If convergence criteria is met return check if any solid has to be considered
            if with_solids:
                if comp_conv_criteria < 1e-12 and all(
                    abs(i) <= 1e-9 for i in solid_delta
                ):
                    return c_spec, cp, log_beta, log_ks, cis
            else:
                if comp_conv_criteria < 1e-12:
                    return c_spec, cp, log_beta, log_ks, cis

        # If during the first or second run you exceed the iteration limit report it
        logging.error(
            "Calculation terminated early, no convergence found at point {} in {}"
            " iterations".format(point, iteration)
            + (
                (
                    " after solids were considered."
                    if with_solids
                    else " before solids were considered."
                )
                if self.nf > 0
                else ""
            )
        )
        raise Exception(
            "Calculation of species concentration aborted, no convergence found with"
            " conc {} at point {} in {} iterations".format(
                str(c_spec), point, iteration
            )
            + (
                (
                    " after solids were considered."
                    if with_solids
                    else " before solids were considered."
                )
                if self.nf > 0
                else ""
            )
        )

    def _getComputableShifts(
        self,
        shifts_to_calculate: NDArray,
        saturation_index: NDArray = np.array([]),
        solid_concentrations: NDArray = np.array([]),
    ):
        negative_cp = solid_concentrations < 0
        supersaturated_solid = saturation_index > 1 + 1e-9

        if negative_cp.any():
            shifts_to_calculate[-self.nf :] = ~negative_cp
        elif supersaturated_solid.any():
            shifts_to_calculate[-self.nf :][np.argmax(saturation_index)] = True
        else:
            shifts_to_calculate = np.array(
                [True for _ in range(self.nc)] + [False for _ in range(self.nf)]
            )

        if self.distribution:
            # If calculating distribution of species exclude the indipendent component from the species to consider
            # shifts_to_calculate = np.delete(shifts_to_calculate, self.ind_comp, axis=0)
            # shifts_to_skip = np.delete(shifts_to_skip, self.ind_comp, axis=0)
            shifts_to_calculate[self.ind_comp] = False

        shifts_to_skip = ~shifts_to_calculate

        return shifts_to_calculate, shifts_to_skip

    def _computeDelta(
        self, c_tot, c_tot_calc, with_solids, saturation_index, cp_to_calculate
    ):
        can_delta = c_tot_calc - c_tot

        if with_solids:
            solid_delta = np.ones(self.nf) - saturation_index
            solid_delta = solid_delta[cp_to_calculate]
        else:
            solid_delta = []

        delta = np.concatenate((can_delta, solid_delta))

        return delta, can_delta, solid_delta

    def _computeJacobian(self, c_spec, saturation_index, with_solids, to_skip):
        if with_solids:
            nt = self.nc + self.nf
            to_skip = np.concatenate(([False for _ in range(self.nc)], to_skip))
        else:
            nt = self.nc

        J = numba_jacobian(
            self.nc,
            nt,
            c_spec,
            saturation_index,
            self.model,
            self.solid_model,
            with_solids,
        )
        # print(numba_jacobian.parallel_diagnostics(level=4))

        if with_solids:
            # Remove rows and columns referring to under-saturated solids
            J = np.delete(J, to_skip, axis=0)
            J = np.delete(J, to_skip, axis=1)

        return J

    def _speciesConcentration(self, c, cp, log_beta):
        """
        Calculate species concentration it returns c_spec and c_tot_calc:
        - c_spec[0->nc] = free conc for each component.
        - c_spec[nc+1->nc+ns] = species concentrations.
        - c_tot_calc = estimated anaytical concentration.
        """
        log_c_spec = self._checkOverUnderFlow(
            np.sum(np.tile(np.log10(c), (self.ns + self.nc, 1)).T * self.model, axis=0)
            + log_beta
        )

        c_spec = 10**log_c_spec
        logging.debug("Species Concentrations: %s", c_spec)

        # Estimate total concentration given the species concentration
        c_tot_calc = np.sum(self.model * np.tile(c_spec, (self.nc, 1)), axis=1)

        if self.nf > 0:
            c_tot_calc += np.sum(self.solid_model * np.tile(cp, (self.nc, 1)), axis=1)

        if self.distribution:
            # Take out the analytical concentration relative to the independent component
            c_tot_calc = np.delete(c_tot_calc, self.ind_comp, 0)

        logging.debug("Calculated Total Concentration: %s", c_tot_calc)

        return c_tot_calc, c_spec

    def _distributionGuess(self, point, for_estimation_c):
        """
        Return an initial guess for the first newton raphson iteration when dealing with distributions of species
        """
        fixed_c = self.ind_comp_c[point]
        # Initial guess of free concentration (c) is considered as follows:
        #   - First point as a fraction of the total concentration
        #   - Second and third points as estimate from previous point
        #   - Subsequent points are extrapolated as follows
        if point > 2:
            lp1 = -np.log10(for_estimation_c[-1][: self.nc])
            lp2 = -np.log10(for_estimation_c[-2][: self.nc])
            lp3 = -np.log10(for_estimation_c[-3][: self.nc])

            # If two subsequent points present the same concentration
            # avoid the issue by using simply the previous point concentration
            c = np.where(lp2 == lp3, lp1, (lp1 + ((lp1 - lp2) ** 2) / (lp2 - lp3)))
            # If the extrapolation returns values that would cause under/overflow adjust them accordingly
            c = self._checkOverUnderFlow(c, d=2)

            if (c < 0).any():
                c = lp1

            # Convert logs back to concentrations
            c = 10 ** (-c)
            # Free C of independent component is set as defined in the settings tab
            c[self.ind_comp] = fixed_c
            logging.debug("ESTIMATED C WITH INTERPOLATION")
        elif point > 0:
            c = for_estimation_c[-1][: self.nc].copy()
            c[self.ind_comp] = fixed_c
            logging.debug("ESTIMATED C FROM PREVIOUS POINT")
        elif point == 0:
            c = np.multiply(self.c_tot[0], 0.001)
            c = np.insert(c, self.ind_comp, fixed_c)
            logging.debug("ESTIMATED C AS FRACTION TOTAL C")
        return c, fixed_c

    def _titrationGuess(self, point, for_estimation_c):
        """
        Return an initial guess for the first newton raphson iteration when dealing with simulated titrations
        """
        # Initial guess of free concentration (c) is considered as follows:
        #   - First point as a fraction of the total concentration
        #   - Second and third points as estimate from previous point
        #   - Subsequent points are extrapolated as follows
        if point > 2:
            v = self.v_added[point]
            v1 = self.v_added[(point - 1)]
            v2 = self.v_added[(point - 2)]
            v3 = self.v_added[(point - 3)]
            lp1 = -np.log10(for_estimation_c[-1][: self.nc])
            lp2 = -np.log10(for_estimation_c[-2][: self.nc])
            lp3 = -np.log10(for_estimation_c[-3][: self.nc])

            # If two subsequent points present the same concentration
            # avoid the issue by using simply the previous point concentration
            c = np.where(
                lp2 == lp3,
                lp1,
                (
                    lp1
                    + (((lp1 - lp2) / (v1 - v2)) ** 2)
                    * ((v2 - v3) / (lp2 - lp3))
                    * (v - v1)
                ),
            )
            # If the extrapolation returns values that would cause under/overflow adjust them accordingly
            c = self._checkOverUnderFlow(c, d=2)

            if (c < 0).any():
                c = lp1

            # Convert logs back to concentrations
            c = 10 ** (-c)
            logging.debug("ESTIMATED C WITH INTERPOLATION")
        elif point > 0:
            c = for_estimation_c[(point - 1)][: self.nc]
            logging.debug("ESTIMATED C FROM PREVIOUS POINT")
        elif point == 0:
            c = np.multiply(self.c_tot[0], 0.001)
            logging.debug("ESTIMATED C AS FRACTION TOTAL C")

        return c

    def _checkOverUnderFlow(self, c, d=1):
        """
        Given c check if any of the given log of concentrations would give overflow or underflow errors, adjust accordingly
        """
        c = np.where(c > (self.epsl / d), (self.epsl / d), c)
        c = np.where(c < (-self.epsl / d), (-self.epsl / d), c)
        return c

    def _setDBHParams(self, species, to_remove, past, zast, c, d, e, solids=False):
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

    def _damping(self, point, c, cp, log_beta, c_tot, fixed_c):
        logging.debug("ENTERING DAMP ROUTINE")

        epsilon = 2.5e-1 if point > 0 else 1e-9
        model = self.model
        nc = self.nc
        if self.distribution:
            nc -= 1
            model = np.delete(model, self.ind_comp, axis=0)
            model = np.delete(model, self.ind_comp, axis=1)

        coeff = np.array([0 for _ in range(nc)])
        a0 = np.max(np.where(model == 0, 1, np.abs(model)), axis=1)

        iteration = 0
        while True:
            _, c_spec = self._speciesConcentration(c, cp, log_beta)

            if self.distribution:
                c_spec = np.delete(c_spec, self.ind_comp)

            c_times_model = np.tile(c_spec, [nc, 1]) * model

            sum_reac = np.where(model > 0, c_times_model, 0).sum(axis=1) + np.where(
                c_tot < 0, np.abs(c_tot), 0
            )
            sum_prod = np.where(c_tot >= 0, c_tot, 0) - np.where(
                model < 0, c_times_model, 0
            ).sum(axis=1)

            conv_criteria = (sum_reac - sum_prod) / (sum_reac + sum_prod)

            if all(i < epsilon for i in conv_criteria) or iteration >= 10000:
                logging.debug("EXITING DAMP ROUTINE")
                if self.distribution:
                    c_spec = np.insert(c_spec, self.ind_comp, fixed_c)
                return c, c_spec

            new_coeff = (
                0.9
                - np.where(
                    (sum_reac > sum_prod), (sum_prod / sum_reac), (sum_reac / sum_prod)
                )
                * 0.8
            )

            if iteration == 0:
                coeff = new_coeff
            coeff = np.where(new_coeff > coeff, new_coeff, coeff)

            if self.distribution:
                c = np.delete(c, self.ind_comp)
            c = coeff * c * (sum_prod / sum_reac) ** (1 / a0) + (1 - coeff) * c
            if self.distribution:
                c = np.insert(c, self.ind_comp, fixed_c)

            iteration += 1

        # # if self.distribution:
        # #     c_spec = np.insert(c_spec, self.ind_comp, fixed_c)
        # logging.debug("EXITING DAMP ROUTINE, MAX N ITERATIONS REACHED")
        # if self.distribution:
        #     c_spec = np.insert(c_spec, self.ind_comp, fixed_c)
        # return c, c_spec
        # raise Exception(
        #     "Dampening routine couldn't find a solution at point {}".format(point)
        # )

        # raise Exception(
        #     "Dampening routine couldn't find a solution at point %s", point
        # )

    def _getSaturationIndex(self, c, log_ks):
        if self.nf > 0:
            saturation_index = np.prod(
                np.tile(c, [self.nf, 1]).T ** self.solid_model, axis=0
            ) / (10**log_ks)
            return saturation_index
        else:
            return np.array([])

    def _ionicStr(self, c, charges, point, first_guess):
        """
        Calculate ionic strength given concentrations of species and their charges.
        """
        if first_guess:
            ionic_strength = ((c * (charges**2)).sum() / 2) + self.background_c[point]
        else:
            ionic_strength = ((c * (charges**2)).sum() + self.background_c[point]) / 2

        return ionic_strength

    def _updateConstants(self, c, log_beta, log_ks, charges, point, first_guess=False):
        if first_guess and self.distribution:
            c = np.insert(c, self.ind_comp, 0, axis=0)

        cis = self._ionicStr(c, charges, point, first_guess)
        logging.debug("Current I: %s %s", cis, ("\tFIRST GUESS" if first_guess else ""))
        updated_log_b = self._updateLogB(cis, log_beta)
        updated_log_ks = self._updateLogKs(cis, log_ks)
        return updated_log_b, updated_log_ks, cis

    def _updateLogKs(self, cis, log_ks):
        cis = np.tile(cis, self.nf)
        radqcis = np.sqrt(cis)
        fib2 = radqcis / (1 + (self.b * radqcis))
        updated_log_ks = (
            log_ks
            + self.solid_az * (fib2 - self.solid_fib)
            - self.solid_cg * (cis - self.solid_ris)
            - self.solid_dg * ((cis * radqcis) - (self.solid_ris * self.solid_radqris))
            - self.solid_eg * ((cis**2) - (self.solid_ris**2))
        )

        return updated_log_ks

    def _updateLogB(self, cis, log_beta):
        """
        Update formation constants of species given the current
        """
        cis = np.tile(cis, self.nc + self.ns)
        radqcis = np.sqrt(cis)
        fib2 = radqcis / (1 + (self.b * radqcis))
        updated_log_beta = (
            log_beta
            - self.species_az * (fib2 - self.species_fib)
            + self.species_cg * (cis - self.species_ris)
            + self.species_dg
            * ((cis * radqcis) - (self.species_ris * self.species_radqris))
            + self.species_eg * ((cis**2) - (self.species_ris**2))
        )

        return updated_log_beta

    def _computePercTable(self, cans, calculated_c, model, percent_to, solids=False):
        can_to_perc = np.array(
            [
                [cans[point, index] for index in percent_to]
                for point in range(cans.shape[0])
            ]
        )

        if not solids:
            can_to_perc = np.concatenate((cans, can_to_perc), axis=1)
        adjust_factor = np.array(
            [
                model[component, index + (self.nc if not solids else 0)]
                for index, component in enumerate(percent_to)
            ]
        )
        adjust_factor = np.where(adjust_factor <= 0, 1, adjust_factor)
        if not solids:
            adjust_factor = np.concatenate(
                ([1 for _ in range(self.nc)], adjust_factor), axis=0
            )

        perc_table = np.where(
            can_to_perc == 0, 0, (calculated_c * adjust_factor) / can_to_perc
        )
        perc_table = perc_table * 100

        return perc_table

    def _percEncoder(self, ignored_comp_names):
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

    def _computeErrors(
        self, c_all_spec, c_solid, saturation_index, log_b, log_ks, point
    ):
        # Get betas from log betas
        beta = 10 ** log_b[self.nc :]
        ks = 10**log_ks
        model = self.model[:, self.nc :]
        free_c = c_all_spec[: self.nc]
        c_spec = c_all_spec[self.nc :]

        with_solids = any(c_solid > 0)

        to_skip = np.concatenate(([False for _ in range(self.nc)], c_solid == 0))
        if with_solids:
            nt = self.nc + self.nf
        else:
            nt = self.nc

        # Define dimension of arrays required
        M = np.zeros(shape=(nt, nt))

        der_free_beta = np.zeros(shape=(self.nc, self.ns))
        der_free_tot = np.zeros(shape=(self.nc, self.nc))
        der_free_ks = np.zeros(shape=(self.nc, self.nf))

        der_solid_beta = np.zeros(shape=(self.nf, self.ns))
        der_solid_tot = np.zeros(shape=(self.nf, self.nc))
        der_solid_ks = np.zeros(shape=(self.nf, self.nf))

        b = -model * (c_spec / beta)
        d = np.identity(self.nc)
        f = np.zeros(shape=(self.nc, self.nf))

        # Compute common matrix term
        M[: self.nc, : self.nc] = (
            (
                np.tile(c_spec, (self.nc, self.nc, 1))
                / np.tile(free_c.reshape((self.nc, 1)), (self.nc, 1, self.ns))
            )
            * np.tile(model, (self.nc, 1, 1))
            * np.rot90(np.tile(model, (self.nc, 1, 1)), -1, axes=(0, 1))
        ).sum(axis=-1)
        M[: self.nc, : self.nc] += d

        if with_solids:
            M[: self.nc, self.nc : nt] = self.solid_model
            M[self.nc : nt, : self.nc] = self.solid_model.T * (
                np.tile(saturation_index, (self.nc, 1)).T
                / np.tile(free_c, (nt - self.nc, 1))
            )

            f = np.concatenate((f, np.diag(saturation_index / ks)), axis=0)
            b = np.concatenate(
                (
                    b,
                    [[0 for _ in range(self.ns)] for _ in range(self.nf)],
                )
            )
            d = np.concatenate(
                (
                    d,
                    [[0 for _ in range(self.nc)] for _ in range(self.nf)],
                )
            )

            der_solid_beta = np.delete(der_solid_beta, c_solid == 0, axis=0)
            der_solid_tot = np.delete(der_solid_tot, c_solid == 0, axis=0)
            der_solid_ks = np.delete(der_solid_ks, c_solid == 0, axis=0)

            M = np.delete(M, to_skip, axis=0)
            M = np.delete(M, to_skip, axis=1)

            b = np.delete(b, to_skip, axis=0)

            d = np.delete(d, to_skip, axis=0)

            f = np.delete(f, to_skip, axis=0)

        if self.distribution:
            M = np.delete(M, self.ind_comp, axis=0)
            M = np.delete(M, self.ind_comp, axis=1)

            b = np.delete(b, self.ind_comp, axis=0)
            d = np.delete(d, self.ind_comp, axis=0)
            f = np.delete(f, self.ind_comp, axis=0)

            der_free_beta = np.delete(der_free_beta, self.ind_comp, 0)
            der_free_tot = np.delete(der_free_tot, self.ind_comp, 0)
            der_free_ks = np.delete(der_free_ks, self.ind_comp, 0)

        # Solve the systems of equations
        for i in range(self.ns):
            solution = np.linalg.solve(M, b[:, i])
            der_free_beta[:, i] = solution[
                : (self.nc - 1 if self.distribution else self.nc)
            ]
            if with_solids:
                der_solid_beta[:, i] = solution[
                    (self.nc - 1 if self.distribution else self.nc) :
                ]

        for r in range(self.nc):
            solution = np.linalg.solve(M, d[:, r])
            der_free_tot[:, r] = solution[
                : (self.nc - 1 if self.distribution else self.nc)
            ]
            if with_solids:
                der_solid_tot[:, r] = solution[
                    (self.nc - 1 if self.distribution else self.nc) :
                ]

        if with_solids:
            for k, skip in enumerate(to_skip[-self.nf :]):
                if skip:
                    continue
                solution = np.linalg.solve(M, f[:, k])
                der_free_ks[:, k] = solution[
                    : (self.nc - 1 if self.distribution else self.nc)
                ]
                der_solid_ks[:, k] = solution[
                    (self.nc - 1 if self.distribution else self.nc) :
                ]

        if with_solids:
            null_solids_index = np.nonzero(c_solid == 0)[0]
            if null_solids_index.size:
                der_solid_beta = np.insert(der_solid_beta, null_solids_index, 0, axis=0)
                der_solid_tot = np.insert(der_solid_tot, null_solids_index, 0, axis=0)
                der_solid_ks = np.insert(der_solid_ks, null_solids_index, 0, axis=0)

        if self.distribution:
            der_free_beta = np.insert(der_free_beta, self.ind_comp, 0, axis=0)
            der_free_tot = np.insert(der_free_tot, self.ind_comp, 0, axis=0)
            der_free_ks = np.insert(der_free_ks, self.ind_comp, 0, axis=0)

        # Compute derivatives for the species
        der_spec_beta = (
            np.rot90(np.tile(model.T, (self.ns, 1, 1)), -1)
            * (
                np.stack(
                    [np.tile(c_spec, (self.ns, 1)).T for _ in range(self.nc)], axis=-1
                )
                / free_c
            )
            * np.tile(der_free_beta.T, (self.ns, 1, 1))
        ).sum(axis=-1) + np.diag(c_spec / beta)

        der_spec_tot = (
            np.rot90(np.tile(model.T, (self.nc, 1, 1)), -1)
            * (
                np.stack(
                    [np.tile(c_spec, (self.nc, 1)).T for _ in range(self.nc)], axis=-1
                )
                / free_c
            )
            * np.tile(der_free_tot.T, (self.ns, 1, 1))
        ).sum(axis=-1)

        der_spec_ks = (
            np.rot90(np.tile(model.T, (self.nf, 1, 1)), -1)
            * (
                np.stack(
                    [np.tile(c_spec, (self.nf, 1)).T for _ in range(self.nc)], axis=-1
                )
                / free_c
            )
            * np.tile(der_free_ks.T, (self.ns, 1, 1))
        ).sum(axis=-1)

        # Calculate uncertanity for components and species given the input
        comp_sigma = np.sqrt(
            ((der_free_beta**2) * (self.beta_sigma**2)).sum(axis=1)
            + ((der_free_tot**2) * (self.conc_sigma[point] ** 2)).sum(axis=1)
            + ((der_free_ks**2) * (self.ks_sigma**2)).sum(axis=1)
        )

        species_sigma = np.sqrt(
            ((der_spec_beta**2) * (self.beta_sigma**2)).sum(axis=1)
            + ((der_spec_tot**2) * (self.conc_sigma[point] ** 2)).sum(axis=1)
            + ((der_spec_ks**2) * (self.ks_sigma**2)).sum(axis=1)
        )
        species_sigma = np.concatenate((comp_sigma, species_sigma))

        if with_solids:
            solid_sigma = np.sqrt(
                ((der_solid_beta**2) * (self.beta_sigma**2)).sum(axis=1)
                + ((der_solid_tot**2) * (self.conc_sigma[point] ** 2)).sum(axis=1)
                + ((der_solid_ks**2) * (self.ks_sigma**2)).sum(axis=1)
            )
        else:
            solid_sigma = np.zeros(shape=self.nf)

        return species_sigma, solid_sigma

    def _setDataframeIndex(self, dataframe):
        if self.distribution:
            dataframe = dataframe.set_index(self.ind_comp_logs).rename_axis(
                index="p[" + self.comp_names[self.ind_comp] + "]",
            )
        else:
            dataframe = dataframe.set_index(self.v_added).rename_axis(
                index="Added Volume [l]",
            )

        return dataframe

    def _scaleMatrix(self, J: NDArray, delta: NDArray):
        d1 = np.diag(np.sqrt(J.max(axis=1)))
        d2 = np.diag(np.sqrt(J.max(axis=0)))
        # d1 = np.diag(np.sqrt(np.diag(J)))
        # d2 = np.diag(np.sqrt(np.diag(J)))
        J = d1 @ J @ d2
        delta = d1 @ delta
        return J, delta


@njit(parallel=True, cache=True)
def numba_jacobian(nc, nt, c_spec, saturation_index, model, solid_model, with_solids):
    J = np.empty(shape=(nt, nt))
    ns = len(c_spec)
    # Compute Jacobian
    # Jacobian for aqueous species
    for j in prange(nc):
        for k in prange(nc):
            val = 0
            for z in prange(ns):
                val += model[j, z] * model[k, z] * (c_spec[z] / c_spec[k])
            J[j, k] = val

    if with_solids:
        # Jacobian for solid species
        for j in range(nc):
            for k in range(nc, nt):
                J[j, k] = solid_model[j, (k - nc)]

        for j in range(nc, nt):
            for k in range(nc):
                J[j, k] = -(solid_model[k, (j - nc)]) * (
                    saturation_index[(j - nc)] / c_spec[k]
                )
    return J
