from typing import Literal

import numpy as np
import pandas as pd
from libeq import SolverData


def _comp_info(
    data: SolverData, mode: Literal["titration", "distribution", "potentiometry"]
):
    comp_info = pd.DataFrame(
        {
            "Charge": data.charges,
        },
        index=data.components,
    ).rename_axis(index="Components Names")

    if mode == "distribution":
        comp_info["Tot. C."] = data.distribution_opts.c0
        comp_info["Tot. C."][data.distribution_opts.independent_component] = None
        # if self.errors:
        #     comp_info.insert(2, "Sigma Tot C", self.c0_sigma)
    elif mode == "titration":
        comp_info["Vessel Conc."] = data.titration_opts.c0
        comp_info["Titrant Conc."] = data.titration_opts.ct
        # TODO add errors data
        # if self.errors:
        #     comp_info.insert(2, "Sigma C0", self.c0_sigma)
        #     comp_info.insert(4, "Sigma cT", self.ct_sigma)

    elif mode == "potentiometry":
        for i, t in enumerate(data.potentiometry_options.titrations):
            comp_info[f"Vessel Conc. {i}"] = t.c0
            comp_info[f"Titrant Conc. {i}"] = t.ct

    return comp_info


def _species_info(data: SolverData):
    species_info = pd.DataFrame(
        {
            "logB": data.log_beta,
        },
        index=data.species_names[data.nc :],
    ).rename_axis(index="Species Names")

    if data.nf > 0:
        solids_info = pd.DataFrame(
            {
                "logKs": data.log_ks,
            },
            # index=data.name,
        ).rename_axis(index="Solid Names")
    else:
        solids_info = pd.DataFrame()

    if data.ionic_strength_dependence:
        species_info.insert(1, "Ref. I", data.reference_ionic_str_species)
        species_info.insert(2, "Charge", data.species_charges)
        species_info.insert(3, "C", data.dbh_values["species"]["cdh"])
        species_info.insert(4, "D", data.dbh_values["species"]["ddh"])
        species_info.insert(5, "E", data.dbh_values["species"]["edh"])

        if data.nf > 0:
            solids_info.insert(1, "Ref. I", data.reference_ionic_str_solids)
            solids_info.insert(2, "Charge", data.solid_charges)
            solids_info.insert(3, "C", data.dbh_values["solids"]["cdh"])
            solids_info.insert(4, "D", data.dbh_values["solids"]["ddh"])
            solids_info.insert(5, "E", data.dbh_values["solids"]["edh"])

    return species_info, solids_info
