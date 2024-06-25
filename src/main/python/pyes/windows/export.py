import os
from datetime import datetime
from pathlib import Path

from pandas import ExcelWriter
from PySide6.QtWidgets import QFileDialog, QWidget
from ui.PyES_dataExport import Ui_ExportWindow
from utils_func import adjustColumnWidths


class ExportWindow(QWidget, Ui_ExportWindow):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)

        self.result = parent.result
        self.path = parent.project_path

        if self.path is None:
            self.project_name = "unknown"
        else:
            self.project_name = os.path.splitext(os.path.basename(self.path))[0]

        if self.result["species_sigma"].empty:
            self.errors_check_excel.setChecked(False)
            self.errors_check_excel.setEnabled(False)
            self.errors_check_csv.setChecked(False)
            self.errors_check_csv.setEnabled(False)

        if self.result["formation_constants"].empty:
            self.adjlogb_check_excel.setChecked(False)
            self.adjlogb_check_excel.setEnabled(False)
            self.adjlogb_check_csv.setChecked(False)
            self.adjlogb_check_csv.setEnabled(False)

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

                    self.result["species_info"].to_excel(
                        writer, sheet_name="Model Info", startrow=3
                    )
                    skip_cols += self.result["species_info"].shape[1]

                    if not self.result["solid_info"].empty:
                        self.result["solid_info"].to_excel(
                            writer,
                            sheet_name="Model Info",
                            startrow=3,
                            startcol=skip_cols + 2,
                        )
                        skip_cols += self.result["solid_info"].shape[1] + 2

                    self.result["comp_info"].to_excel(
                        writer,
                        sheet_name="Model Info",
                        na_rep="---",
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

                if self.distribution_check_excel.isChecked():
                    self.result["species_distribution"].to_excel(
                        writer, sheet_name="Species Distribution"
                    )
                    adjustColumnWidths(
                        wb, "Species Distribution", self.result["species_distribution"]
                    )

                    if self.errors_check_excel.isChecked():
                        self.result["species_sigma"].to_excel(
                            writer, sheet_name="Species SD"
                        )

                        adjustColumnWidths(
                            wb, "Species SD", self.result["species_sigma"]
                        )

                    if not self.result["solid_distribution"].empty:
                        self.result["solid_distribution"].to_excel(
                            writer, sheet_name="Solid Distribution"
                        )
                        adjustColumnWidths(
                            wb,
                            "Solid Distribution",
                            self.result["solid_distribution"],
                        )

                        if self.errors_check_excel.isChecked():
                            self.result["solid_sigma"].to_excel(
                                writer, sheet_name="Solid SD"
                            )

                            adjustColumnWidths(
                                wb, "Solid SD", self.result["solid_sigma"]
                            )

                if self.perc_check_excel.isChecked():
                    self.result["species_percentages"].to_excel(
                        writer, sheet_name="Species Percentages"
                    )

                    adjustColumnWidths(
                        wb, "Species Percentages", self.result["species_percentages"]
                    )

                    if not self.result["solid_percentages"].empty:
                        self.result["solid_percentages"].to_excel(
                            writer, sheet_name="Solid Percentages"
                        )

                        adjustColumnWidths(
                            wb, "Solid Percentages", self.result["solid_percentages"]
                        )

                if self.adjlogb_check_excel.isChecked():
                    self.result["formation_constants"].to_excel(
                        writer,
                        sheet_name="Adjusted Formation Constants",
                        float_format="%.3f",
                    )

                    adjustColumnWidths(
                        wb,
                        "Adjusted Formation Constants",
                        self.result["formation_constants"],
                    )

                    if not self.result["solubility_products"].empty:
                        self.result["solubility_products"].to_excel(
                            writer,
                            sheet_name="Adjusted Solubility Products",
                            float_format="%.3f",
                        )

                        adjustColumnWidths(
                            wb,
                            "Adjusted Solubility Products",
                            self.result["solubility_products"],
                        )

    def CsvExport(self):
        """
        Export results as csv files.
        """
        folder_path = QFileDialog.getExistingDirectory(self, "Select a Folder")

        if folder_path:
            base_name = folder_path + "/" + self.project_name
            if self.input_check_csv.isChecked():
                self.result["species_info"].to_csv(base_name + "_species.csv")
                self.result["comp_info"].to_csv(base_name + "_comp.csv")

                if "solid_info" in self.result:
                    self.result["solid_info"].to_csv(base_name + "_solid.csv")

            if self.distribution_check_csv.isChecked():
                self.result["species_distribution"].to_csv(
                    base_name + "_species_distribution.csv"
                )

                if not self.result["solid_distribution"].empty:
                    self.result["solid_distribution"].to_csv(
                        base_name + "_solid_distribution.csv"
                    )

            if self.perc_check_csv.isChecked():
                self.result["species_percentages"].to_csv(
                    base_name + "_species_percentages.csv"
                )

                if not self.result["solid_percentages"].empty:
                    self.result["solid_percentages"].to_csv(
                        base_name + "_solid_percentages.csv"
                    )

            if self.adjlogb_check_csv.isChecked():
                self.result["formation_constants"].to_csv(base_name + "_logb.csv")

                if not self.result["solubility_products"].empty:
                    self.result["solubility_products"].to_csv(base_name + "_logks.csv")

            if self.errors_check_csv.isChecked():
                self.result["species_sigma"].to_csv(base_name + "_species_SD.csv")

                if not self.result["solid_sigma"].empty:
                    self.result["solid_sigma"].to_csv(base_name + "_solid_SD.csv")
