import pandas as pd
from commands.fields import DoubleSpinBoxEdit
from dialogs import loadCSVDialog
from PySide6.QtGui import QUndoCommand, QUndoStack
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QLineEdit,
    QScrollArea,
    QSpinBox,
    QTableView,
    QWidget,
)
from viewmodels.delegate import CheckBoxDelegate

from .combobox import CustomComboBox
from .PyES_inputTitrationOpt import Ui_inputTitrationOpt
from .range_selector import MultipleRangeSelector


class inputTitrationOpt(QWidget, Ui_inputTitrationOpt):
    def __init__(
        self,
        parent: QWidget | None = None,
        undo_stack: QUndoStack = None,
        components: list[str] = ["A"],
    ) -> None:
        from viewmodels.models import ConcentrationsModel, TitrationModel

        super().__init__(parent)
        self.setupUi(self)

        self.undo_stack = undo_stack
        self.titrationView.setModel(TitrationModel())
        self.titrationView.model().setColumnReadOnly([3], True)
        self.titrationView.setItemDelegateForColumn(
            0, CheckBoxDelegate(self.titrationView)
        )

        self.concView.setModel(
            ConcentrationsModel(
                pd.DataFrame(
                    [[0.0 for _ in range(4)] for _ in range(len(components))],
                    columns=["C0", "CT", "Sigma C0", "Sigma CT"],
                    index=components,
                ),
                undo_stack=undo_stack,
            )
        )
        self.electroActiveComponent.addItems(components)

        pxRange = MultipleRangeSelector(undo_stack=undo_stack)
        pxRange.setObjectName("pxRange")
        self.px_ranges.setWidget(pxRange)

        self.qspinbox_fields: list[QDoubleSpinBox] = [
            self.e0,
            self.slope,
            self.ja,
            self.jb,
            self.eSigma,
            self.initialVolume,
            self.vSigma,
            self.c0back,
            self.ctback,
        ]

        self.qspinbox_px_fields: list[QDoubleSpinBox] = [
            self.e0,
            self.slope,
        ]

        self.qcombobox_fields: list[QComboBox] = [
            self.electroActiveComponent,
        ]

        self.electroActiveComponent.currentIndexChanged.connect(
            lambda index, field=self.electroActiveComponent: self.undo_stack.push(
                ChangeElectroActiveCommand(field, index)
            )
        )

        self.addRangeButton.clicked.connect(self.add_range)

        self.removeRangeButton.clicked.connect(self.remove_range)

        for field in self.qspinbox_fields:
            field.valueChanged.connect(
                lambda value, field=field: undo_stack.push(
                    DoubleSpinBoxEdit(field, value)
                )
            )

        for field in self.qspinbox_px_fields:
            field.valueChanged.connect(
                lambda value, field=field: self.titrationView.model().update_pX(
                    e0=self.e0.value(), slope=self.slope.value()
                )
            )

        self.importDataButton.clicked.connect(self.import_data)

        self.useAllButton.clicked.connect(self.use_all)
        self.useEvenButton.clicked.connect(self.use_even)
        self.useOddButton.clicked.connect(self.use_odd)

    def retrive_data(self):
        data = dict()
        children = self.children()
        for c in children:
            #if c.objectName() == 'titrationView':
            #    breakpoint()
            if isinstance(c, QLineEdit):
                data[c.objectName()] = c.text()
            elif isinstance(c, (QDoubleSpinBox, QSpinBox)):
                data[c.objectName()] = c.value()
            elif isinstance(c, QComboBox):
                data[c.objectName()] = c.currentIndex()
            elif isinstance(c, QTableView):
                data[c.objectName()] = c.model()._data.fillna(0).to_dict()
            elif isinstance(c, QScrollArea):
                data[c.widget().objectName()] = c.widget().getRanges()
            else:
                continue
        return data

    def set_data(self, data: dict):
        children = self.children()
        for c in children:
            try:
                if isinstance(c, QLineEdit):
                    c.setText(data[c.objectName()])
                elif isinstance(c, (QDoubleSpinBox, QSpinBox)):
                    c.setValue(data[c.objectName()])
                elif isinstance(c, QComboBox):
                    c.setCurrentIndex(data[c.objectName()])
                elif isinstance(c, QTableView):
                    c.model()._data = pd.DataFrame(data[c.objectName()])
                    if c.objectName() == "titrationView":
                        c.model().setColumnReadOnly([3], True)
                        #c.model()._data.iloc[:, 4] = 0.0
                        #c.model()._data["pX"] = 0.0
                        c.model().update_pX(
                            e0=self.e0.value(), slope=self.slope.value()
                        )
                elif isinstance(c, QScrollArea):
                    c.widget().setRanges(data[c.widget().objectName()])
                else:
                    continue
            except KeyError:
                continue

    def import_data(self):
        dlg = loadCSVDialog(self)
        if dlg.exec():
            self.titrationView.model()._data = dlg.get_final_model()
            self.titrationView.model().update_pX(
                e0=self.e0.value(), slope=self.slope.value()
            )

    def add_range(self):
        self.undo_stack.push(AddRangeCommand(self.px_ranges.widget()))

    def remove_range(self):
        self.undo_stack.push(RemoveRangeCommand(self.px_ranges.widget()))

    def use_all(self):
        self.titrationView.model().use_all()

    def use_even(self):
        self.titrationView.model().use_even()

    def use_odd(self):
        self.titrationView.model().use_odd()


class ChangeElectroActiveCommand(QUndoCommand):
    def __init__(self, field: CustomComboBox, index: int):
        QUndoCommand.__init__(self)
        self.field = field
        self.index = index
        self.previous_index = field.previous_index

    def undo(self) -> None:
        self.field.blockSignals(True)
        self.field.setCurrentIndex(self.previous_index)
        self.field.blockSignals(False)

    def redo(self) -> None:
        self.field.blockSignals(True)
        self.field.setCurrentIndex(self.index)
        self.field.blockSignals(False)


class AddRangeCommand(QUndoCommand):
    def __init__(self, field: MultipleRangeSelector):
        QUndoCommand.__init__(self)
        self.field = field

    def undo(self) -> None:
        self.field.removeRange()
        print(self.field.numRanges)

    def redo(self) -> None:
        self.field.addRange()


class RemoveRangeCommand(QUndoCommand):
    def __init__(self, field: MultipleRangeSelector):
        QUndoCommand.__init__(self)
        self.field = field

    def undo(self) -> None:
        self.field.addRange()

    def redo(self) -> None:
        self.field.removeRange()
