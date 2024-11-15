import os
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
from pandas import ExcelWriter
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFileDialog, QTableWidgetItem, QWidget
from ui.PyES_monitorWindow import Ui_MonitorWindow
from utils_func import resultToCSV, resultToExcel


class MonitorWindow(QWidget, Ui_MonitorWindow):
    def __init__(self, parent):
        super().__init__()
        self.setupUi(self)
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint)

        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.setColumnCount(4)
        self.tableWidget.setHorizontalHeaderLabels(
            [
                "Type",
                "Name",
                "Value",
                "Difference",
            ]
        )
        # Add 3 rows to the tableWidget

        # Populate the rows with test strings

        self.reset_data()

    def reset_data(self):
        self.tableWidget.clearContents()
        self.tableWidget.setRowCount(0)
        self.set_waiting()

    def recieve_data(self, data: pd.DataFrame | None):
        self.reset_data()
        self.status.setText("Done")
        if data is not None:
            data, original_value = self.prepare_data(data)
            self.tableWidget.setRowCount(len(data))

            for row, rowData in enumerate(data):
                for col, value in enumerate(rowData):
                    if col == 3:  # Difference column
                        if value != 0:
                            ratio = abs(value / original_value[row])
                            foreground = Qt.green if value > 0 else Qt.red
                        else:
                            ratio = 0
                            foreground = Qt.GlobalColor.color0

                        if ratio > 0.75:
                            arrows = "↑↑↑↑" if value > 0 else "↓↓↓↓"
                        elif ratio > 0.50:
                            arrows = "↑↑↑" if value > 0 else "↓↓↓"
                        elif ratio > 0.25:
                            arrows = "↑↑" if value > 0 else "↓↓"
                        elif ratio > 0:
                            arrows = "↑" if value > 0 else "↓"
                        else:
                            arrows = "="

                        item = QTableWidgetItem(f"{value:<10} {arrows:>4}")
                        item.setForeground(foreground)
                    else:
                        item = QTableWidgetItem(str(value))
                    self.tableWidget.setItem(row, col, item)

    def error(self):
        self.reset_data()
        self.status.setText("Error")

    def prepare_data(self, data: pd.DataFrame):
        names = data.index.to_list()
        types = ["Constant" for _ in range(len(names))]
        difference = (data["New logB"] - data["Old logB"]).round(4).to_list()
        value = data["New logB"].round(4).to_list()
        original_value = data["Old logB"].round(4).to_list()

        list_data = [
            [t, n, v, d] for t, n, v, d in zip(types, names, value, difference)
        ]

        return list_data, original_value

    def set_waiting(self):
        self.status.setText("Waiting")
