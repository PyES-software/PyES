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
from PySide6 import QtWidgets


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

        self.parameters_check.setEnabled('optimized_parms' in self.result.keys())
        self.concentration_check.setEnabled('concentrations' in self.result.keys())
        self.percent_check.setEnabled('percent' in self.result.keys())

        self.export_button.clicked.connect(self.open_export)

        self._what_to_export = []
        self._section_labels = []

    def open_export(self):
        filters = ("Excel files (*.xlsx *.xls)", "CSV files (*.csv)", "Text files (*.txt)")
        filename, ftype = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', self.path, ";;".join(filters))
        if not filename:
            return

        if self.parameters_check.isChecked():
            self._what_to_export.append(self.result['optimized_parms'])
            self._section_labels.append('Refined')
        if self.concentration_check.isChecked():
            self._what_to_export.append(self.result['concentrations'])
            self._section_labels.append('Concentrations')
        if self.percent_check.isChecked():
            self._what_to_export.append(self.result['percent'])
            self._section_labels.append('Percent')

        exported_methods = (
            self._export_excel,
            self._export_csv,
            self._export_txt)

        ntype: int = filters.index(ftype)
        exported_methods[ntype](filename)

    def _export_excel(self, filename: str):
        with pd.ExcelWriter(filename, mode='w') as xlw:
            for label, df in zip(self._section_labels, self._what_to_export):
                df.to_excel(xlw, sheet_name=label)

    def _export_csv(self, filename: str):
        with open(filename, 'a') as fh:
            for label, df in zip(self._section_labels, self._what_to_export):
                _write_header(fh, label)
                df.to_csv(fh, mode='a')
                fh.write('\n')

    def _export_txt(self, filename: str):
        with open(filename, 'a') as fh:
            for label, df in zip(self._section_labels, self._what_to_export):
                _write_header(fh, label)
                df.to_string(fh)
                fh.write('\n')


def _write_header(file, label: str) -> None:
    file.write(20*'=' + '\n')
    file.write(f'  {label}\n')
    file.write(20*'=' + '\n\n')
