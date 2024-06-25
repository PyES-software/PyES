from typing import Optional

from PySide6.QtWidgets import (
    QLineEdit,
    QDoubleSpinBox,
    QWidget,
    QSpinBox,
    QComboBox,
    QTableView,
)
from PySide6.QtGui import QUndoStack

from .PyES_inputTitrationOpt import Ui_inputTitrationOpt
from commands.fields import DoubleSpinBoxEdit
from dialogs import loadCSVDialog
import pandas as pd


class inputTitrationOpt(QWidget, Ui_inputTitrationOpt):
    def __init__(
        self,
        parent: QWidget | None = None,
        undo_stack: QUndoStack = None,
        components: list[str] = ["A"],
    ) -> None:
        from viewmodels.models import TitrationModel, ConcentrationsModel

        super().__init__(parent)
        self.setupUi(self)

        self.qspinbox_fields: list[QDoubleSpinBox] = [
            self.e0,
            self.slope,
            self.ja,
            self.jb,
            self.eSigma,
            self.initialVolume,
            self.vSigma,
        ]

        for field in self.qspinbox_fields:
            field.valueChanged.connect(
                lambda value, field=field: undo_stack.push(
                    DoubleSpinBoxEdit(field, value)
                )
            )

        self.importDataButton.clicked.connect(self.import_data)

        self.titrationView.setModel(TitrationModel())
        self.concView.setModel(
            ConcentrationsModel(
                pd.DataFrame(
                    [[0.0 for x in range(4)] for _ in range(len(components))],
                    columns=["C0", "CT", "Sigma C0", "Sigma CT"],
                    index=components,
                ),
                undo_stack=undo_stack,
            )
        )
        self.electroActiveComponent.addItems(components)

    def retrive_data(self):
        data = dict()
        children = self.children()
        for c in children:
            if isinstance(c, QLineEdit):
                data[c.objectName()] = c.text()
            elif isinstance(c, (QDoubleSpinBox, QSpinBox)):
                data[c.objectName()] = c.value()
            elif isinstance(c, QComboBox):
                data[c.objectName()] = c.currentIndex()
            elif isinstance(c, QTableView):
                data[c.objectName()] = c.model()._data.to_dict()
            else:
                continue
        return data

    def set_data(self, data: dict):
        children = self.children()
        for c in children:
            if c.objectName() in data:
                if isinstance(c, QLineEdit):
                    c.setText(data[c.objectName()])
                elif isinstance(c, (QDoubleSpinBox, QSpinBox)):
                    c.setValue(data[c.objectName()])
                elif isinstance(c, QComboBox):
                    c.setCurrentIndex(data[c.objectName()])
                elif isinstance(c, QTableView):
                    c.model()._data = pd.DataFrame(data[c.objectName()])
                else:
                    continue

    def import_data(self):
        dlg = loadCSVDialog(self)
        if dlg.exec():
            self.titrationView.setModel(dlg.previewModel)
