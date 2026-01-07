import os
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from pandas import ExcelWriter
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QWidget
from ui.PyES_dataExport import Ui_ExportWindow
from utils_func import resultToCSV, resultToExcel

"""
pyes.windows.export

GUI window that allows the user to export computed project results to Excel
(.xlsx) or to multiple CSV files.

This module contains:
- check_table_presence: a small helper for detecting whether a result table
  (often a pandas.DataFrame) is present and non-empty.
- ExportWindow: a QWidget subclass that renders the export dialog and performs
  the actual writing of Excel and CSV files based on which checkboxes the user
  has selected.

Note: The module intentionally keeps logic minimal and delegates file writing
to the utility functions `resultToExcel` and `resultToCSV`.
"""

def check_table_presence(result: dict[str, Any], field: str) -> bool:
    """
    Determine whether a given field is present in the result dict and contains
    data that should be exported.

    The function treats a value as present if:
    - The field exists in `result` and the value is a non-empty pandas.DataFrame.
    - The field exists and the value is a non-empty list.

    Parameters
    ----------
    result : dict[str, Any]
        The results dictionary produced by the model. Commonly contains
        pandas.DataFrame objects keyed by field name.
    field : str
        The key to test in `result`.

    Returns
    -------
    bool
        True if the field exists and appears to contain data worth exporting,
        False otherwise.

    Notes
    -----
    - The implementation intentionally uses a conservative default for
      missing keys (pd.DataFrame()) so that code using `.get()` will not raise.
    - If other types (e.g., numpy arrays, tuples) must be supported, consider
      extending the type checks to use pandas.api.types.is_list_like or checking
      for length via `len(value)` where appropriate.
    """
    value = result.get(field, pd.DataFrame())
    # if isinstance(value, list) or not value.empty:
    #     return True
    # else:
    #     return False
    return isinstance(value, list) or not value.empty


class ExportWindow(QWidget, Ui_ExportWindow):
    """
    Window for exporting PyES results to Excel and CSV.

    This class is a QWidget that is constructed with a `parent` window which is
    expected to have two attributes:
    - result: dict[str, Any] containing the computed result tables
    - project_path: Optional[str] path to the project file (used to derive the
      project name for exported files)

    The UI contains checkboxes mapped to the kinds of results that can be
    exported (input/model info, optimized constants, distributions, percentages,
    adjusted log-beta / formation constants, and errors). The class exposes
    two methods that perform the exports when the user requests them:
    - ExcelExport(): export selected tables to a single .xlsx workbook.
    - CsvExport(): export selected tables to separate .csv files.

    Attributes
    ----------
    result : dict[str, Any]
        The results dictionary taken from the parent.
    path : str | None
        The project path (may be None).
    project_name : str
        A safe basename used to name exported files.
    errors_present : bool
        Whether species error/sd information is present.
    formation_constants_present : bool
        Whether formation constants data is present.
    solids_present : bool
        Whether solid-phase related data is present.
    optimized_present : bool
        Whether optimized constants are present.
    """
    def __init__(self, parent):
        """
        Initialize the export dialog.

        The constructor wires the UI (Ui_ExportWindow), sets the dialog to stay
        on top, reads the `result` and `project_path` from `parent`, computes a
        human-friendly project name, and disables checkboxes corresponding to
        data that is not present in `result`.

        Parameters
        ----------
        parent : QWidget-like
            Parent widget which must provide `result` and `project_path`.
        """
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        self.result = parent.result
        self.path = parent.project_path

        if self.path is None:
            self.project_name = "unknown"
        else:
            self.project_name = os.path.splitext(os.path.basename(self.path))[0]

        self.errors_present = check_table_presence(
            result=self.result, field="species_sigma"
        )
        self.formation_constants_present = check_table_presence(
            result=self.result, field="formation_constants"
        )
        self.solids_present = check_table_presence(
            result=self.result, field="solids_info"
        )
        self.optimized_present = check_table_presence(
            result=self.result, field="optimized_constants"
        )

        if not any((self.errors_present,
                    self.formation_constants_present,
                    self.optimized_present)):
            self.errors_check_excel.setChecked(False)
            self.errors_check_excel.setEnabled(False)
            self.errors_check_csv.setChecked(False)
            self.errors_check_csv.setEnabled(False)

        # if not self.errors_present:
        #     self.errors_check_excel.setChecked(False)
        #     self.errors_check_excel.setEnabled(False)
        #     self.errors_check_csv.setChecked(False)
        #     self.errors_check_csv.setEnabled(False)

        # if not self.formation_constants_present:
        #     self.adjlogb_check_excel.setChecked(False)
        #     self.adjlogb_check_excel.setEnabled(False)
        #     self.adjlogb_check_csv.setChecked(False)
        #     self.adjlogb_check_csv.setEnabled(False)

        # if not self.optimized_present:
        #     self.optimized_check_excel.setChecked(False)
        #     self.optimized_check_excel.setEnabled(False)
        #     self.optimized_check_csv.setChecked(False)
        #     self.optimized_check_csv.setEnabled(False)

    def ExcelExport(self):
        """
        Export selected results to a single Excel workbook (.xlsx).

        Behavior
        --------
        - Prompts the user to pick a save path with a QFileDialog.
        - Builds an .xlsx workbook and writes selected pandas.DataFrame tables
          to named sheets via the helper `resultToExcel(writer, dataframe, sheet)`.
        - Adds a "Model Info" top-left block with the project name and current
          date.
        - Uses simple heuristics to arrange tables horizontally on the
          "Model Info" sheet by incrementing `startcol` (skip_cols).

        Notes
        -----
        - This method assumes that `resultToExcel` knows how to accept the
          arguments used here (writer, DataFrame, sheet name, optional
          `startrow`, `startcol`, and `float_format`).
        - No explicit error dialogs are shown on exceptions; consider adding
          user-visible error handling (QMessageBox) if write operations can
          fail due to permissions or other IO issues.
        """
        output_path, _ = QFileDialog.getSaveFileName(
            self, "Pick a Path", "", "Excel 2007-365 (*.xlsx)"
        )

        if output_path:
            file_name = Path(output_path).parents[0]
            file_name = file_name.joinpath(Path(output_path).stem)
            file_name = file_name.with_suffix(".xlsx")

            with ExcelWriter(file_name, engine="openpyxl") as writer:
                wb = writer.book

                if self.input_check_excel.isChecked():
                    skip_cols = 0

                    resultToExcel(
                        writer,
                        self.result["species_info"],
                        "Model Info",
                        startrow=3,
                        startcol=skip_cols,
                    )

                    skip_cols += self.result["species_info"].shape[1]

                    if self.solids_present:
                        resultToExcel(
                            writer,
                            self.result["solids_info"],
                            "Model Info",
                            startrow=3,
                            startcol=skip_cols + 2,
                        )
                        skip_cols += self.result["solids_info"].shape[1] + 2

                    resultToExcel(
                        writer,
                        self.result["comp_info"],
                        "Model Info",
                        startrow=3,
                        startcol=skip_cols + 2,
                    )

                    ws = wb["Model Info"]
                    ws["A1"] = "File:"
                    ws["A2"] = "Date:"
                    ws.merge_cells("B1:D1")
                    ws.merge_cells("B2:D2")
                    ws["B1"] = self.project_name
                    ws["B2"] = datetime.now()

                if self.optimized_check_excel.isChecked():
                    resultToExcel(
                        writer,
                        self.result["optimized_constants"],
                        "Optimized Parameters",
                    )

                if self.distribution_check_excel.isChecked():
                    resultToExcel(
                        writer,
                        self.result["species_concentrations"],
                        "Species Distribution",
                    )

                    if self.errors_check_excel.isChecked():
                        resultToExcel(
                            writer, self.result["species_sigma"], "Species SD"
                        )

                    if self.solids_present:
                        resultToExcel(
                            writer,
                            self.result["solids_percentages"],
                            "Solid Distribution",
                        )

                        if self.errors_check_excel.isChecked():
                            resultToExcel(
                                writer, self.result["solid_sigma"], "Solid SD"
                            )

                if self.perc_check_excel.isChecked():
                    resultToExcel(
                        writer,
                        self.result["soluble_percentages"],
                        "Soluble Percentages",
                    )

                    if self.solids_present:
                        resultToExcel(
                            writer,
                            self.result["solids_percentages"],
                            "Solid Percentages",
                        )

                if self.adjlogb_check_excel.isChecked():
                    resultToExcel(
                        writer,
                        self.result["formation_constants"],
                        "Log Beta",
                    )

                    if self.solids_present:
                        resultToExcel(
                            writer,
                            self.result["solubility_products"],
                            "Log Ks",
                            float_format="%.3f",
                        )

    def CsvExport(self):
        """
        Export selected results as separate CSV files.

        Behavior
        --------
        - Prompts the user to choose an output directory with QFileDialog.
        - Writes one or more CSV files, prefixed with the project name, using
          the helper `resultToCSV(dataframe, filename_base)`.
        - The function appends different suffixes to the base name to
          distinguish exports (e.g., 'species', 'components', 'solids', etc.).

        Notes
        -----
        - This function currently constructs file paths using string
          concatenation; using pathlib.Path is recommended for cross-platform
          safety and readability.
        - Several `base_name + ""` uses are present; ensure `resultToCSV`
          appends/handles extensions correctly, otherwise supply explicit
          suffixes.
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Select a Folder")

        if folder_path:
            base_name = folder_path + "/" + self.project_name + "_"
            if self.input_check_csv.isChecked():
                resultToCSV(self.result["species_info"], base_name + "species")
                resultToCSV(self.result["comp_info"], base_name + "components")

                if "solids_info" in self.result:
                    resultToCSV(self.result["solids_info"], base_name + "solids")

            if self.optimized_check_csv.isChecked():
                resultToCSV(self.result["optimized_constants"], base_name + "optimized")

            if self.distribution_check_csv.isChecked():
                resultToCSV(
                    self.result["species_concentrations"], base_name + "species"
                )

                if self.solids_present:
                    resultToCSV(self.result["solids_percentages"], base_name + "solids")

            if self.perc_check_csv.isChecked():
                resultToCSV(
                    self.result["soluble_percentages"],
                    base_name + "soluble_percentages",
                )

                if self.solids_present:
                    resultToCSV(
                        self.result["solids_percentages"],
                        base_name + "solid_percentages",
                    )

            if self.adjlogb_check_csv.isChecked():
                resultToCSV(self.result["formation_constants"], base_name + "")

                if self.solids_present:
                    resultToCSV(self.result["solubility_products"], base_name + "")

            if self.errors_check_csv.isChecked():
                resultToCSV(self.result["species_sigma"], base_name + "")

                if self.solids_present:
                    resultToCSV(self.result["solid_sigma"], base_name + "")
