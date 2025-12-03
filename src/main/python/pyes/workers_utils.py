from typing import Literal

import numpy as np
import pandas as pd
from libeq import SolverData, Flags


def _comp_info(
    data: SolverData,
    mode: Literal["titration", "distribution", "potentiometry"],
    errors: bool,
):
    comp_info = pd.DataFrame()

    if mode == "distribution":
        comp_info["Tot. C. [mol/l]"] = data.distribution_opts.c0
        comp_info["Tot. C. [mol/l]"][
            data.distribution_opts.independent_component
        ] = None

        comp_info = comp_info.set_index([data.components, data.charges]).rename_axis(
            index=["Component", "Charge"]
        )

        if errors:
            comp_info["Sigma Tot C"] = data.distribution_opts.c0_sigma
    elif mode == "titration":
        comp_info["Vessel Conc. [mol/l]"] = data.titration_opts.c0
        comp_info["Titrant Conc. [mol/l]"] = data.titration_opts.ct
        comp_info = comp_info.set_index(
            [
                data.components,
                data.charges,
                [data.titration_opts.v0 for _ in data.components],
            ]
        ).rename_axis(index=["Component", "Charge", "V0 [ml]"])

        if errors:
            comp_info["Sigma C0"] = data.titration_opts.c0_sigma
            comp_info["Sigma CT"] = data.titration_opts.ct_sigma

    elif mode == "potentiometry":
        vessel_conc = []
        titrant_conc = []
        if errors:
            vessel_conc_sigma = []
            titrant_conc_sigma = []
        for t in data.potentiometry_opts.titrations:
            vessel_conc.append(t.c0)
            titrant_conc.append(t.ct)
            if errors:
                vessel_conc_sigma.append(t.c0_sigma)
                titrant_conc_sigma.append(t.ct_sigma)

        titration_index = [
            index + 1
            for index, _ in enumerate(data.potentiometry_opts.titrations)
            for _ in data.components
        ]

        e0_index = [
            t.e0 for t in data.potentiometry_opts.titrations for _ in data.components
        ]
        es_index = [
            t.e0_sigma
            for t in data.potentiometry_opts.titrations
            for _ in data.components
        ]

        v0_index = [
            t.v0 for t in data.potentiometry_opts.titrations for _ in data.components
        ]

        vs_index = [
            t.v0_sigma
            for t in data.potentiometry_opts.titrations
            for _ in data.components
        ]

        components_index = [
            data.components for _ in range(len(data.potentiometry_opts.titrations))
        ]

        components_index = [item for sublist in components_index for item in sublist]

        charges_index = [
            data.charges for _ in range(len(data.potentiometry_opts.titrations))
        ]
        charges_index = [item for sublist in charges_index for item in sublist]

        comp_info["Vessel Conc. [mol/l]"] = np.concatenate(vessel_conc, axis=0)
        comp_info["Titrant Conc. [mol/l]"] = np.concatenate(titrant_conc, axis=0)
        if errors:
            comp_info["Sigma C0"] = np.concatenate(vessel_conc_sigma, axis=0)
            comp_info["Sigma CT"] = np.concatenate(titrant_conc_sigma, axis=0)
        comp_info = comp_info.set_index(
            [
                titration_index,
                e0_index,
                es_index,
                v0_index,
                vs_index,
                components_index,
                charges_index,
            ]
        ).rename_axis(
            index=[
                "Titration",
                "E0 [mV]",
                "E Sigma",
                "V0 [ml]",
                "V Sigma",
                "Component",
                "Charge",
            ]
        )

    return comp_info


def _species_info(
    data: SolverData,
    mode: Literal["titration", "distribution", "potentiometry"],
    errors: bool,
):
    species_info = pd.DataFrame(
        {
            "logB": data.log_beta,
        },
        index=data.species_names[data.nc :],
    ).rename_axis(index="Species Names")

    if errors:
        species_info["Sigma logB"] = data.log_beta_sigma

    if mode == "potentiometry":
        species_info["Optimize"] = [
            "*" if flag == Flags.REFINE else "" for flag in data.potentiometry_opts.beta_flags
        ]

    if data.nf > 0:
        solids_info = pd.DataFrame(
            {
                "logKs": data.log_ks,
            },
            index=data.solids_names,
        ).rename_axis(index="Solid Names")

        if errors:
            solids_info["Sigma logKs"] = data.log_ks_sigma
    else:
        solids_info = pd.DataFrame()

    if data.ionic_strength_dependence:
        species_info.insert(1, "Ref. I", data.reference_ionic_str_species)
        species_info.insert(2, "Charge", data.species_charges)
        species_info.insert(3, "C", data.dbh_values["species"]["cdh"])
        species_info.insert(4, "D", data.dbh_values["species"]["ddh"])
        species_info.insert(5, "E", data.dbh_values["species"]["edh"])
        species_info.insert(6, "z*", data.z_star_species)
        species_info.insert(7, "p*", data.p_star_species)

        if data.nf > 0:
            solids_info.insert(1, "Ref. I", data.reference_ionic_str_solids)
            solids_info.insert(2, "Charge", data.solid_charges)
            solids_info.insert(3, "C", data.dbh_values["solids"]["cdh"])
            solids_info.insert(4, "D", data.dbh_values["solids"]["ddh"])
            solids_info.insert(5, "E", data.dbh_values["solids"]["edh"])
            solids_info.insert(6, "z*", data.z_star_solids)
            solids_info.insert(7, "p*", data.p_star_solids)

    return species_info, solids_info
