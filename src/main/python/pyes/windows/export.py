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


def check_table_presence(result: dict[str, Any], field: str) -> bool:
    value = result.get(field, pd.DataFrame())
    if isinstance(value, list) or not value.empty:
        return True
    else:
        return False


class ExportWindow(QWidget, Ui_ExportWindow):
    def __init__(self, parent):
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

        if not self.errors_present:
            self.errors_check_excel.setChecked(False)
            self.errors_check_excel.setEnabled(False)
            self.errors_check_csv.setChecked(False)
            self.errors_check_csv.setEnabled(False)

        if not self.formation_constants_present:
            self.adjlogb_check_excel.setChecked(False)
            self.adjlogb_check_excel.setEnabled(False)
            self.adjlogb_check_csv.setChecked(False)
            self.adjlogb_check_csv.setEnabled(False)

        if not self.optimized_present:
            self.optimized_check_excel.setChecked(False)
            self.optimized_check_excel.setEnabled(False)
            self.optimized_check_csv.setChecked(False)
            self.optimized_check_csv.setEnabled(False)

    def ExcelExport(self):
        """
        Export results to an excel file.
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
                        "Optimized Constants",
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
        Export results as csv files.
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
