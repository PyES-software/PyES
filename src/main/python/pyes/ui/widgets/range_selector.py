from PySide6.QtWidgets import QWidget, QDoubleSpinBox, QLabel
from PySide6.QtCore import Qt
from PySide6.QtGui import QUndoStack

from commands.fields import DoubleSpinBoxEdit

from .PyES_multipleRangeSelector import Ui_multipleRangeSelector
from .spinbox import CustomSpinBox


class MultipleRangeSelector(QWidget, Ui_multipleRangeSelector):
    def __init__(
        self, parent: QWidget | None = None, undo_stack: QUndoStack | None = None
    ) -> None:
        super().__init__(parent)
        self.setupUi(self)
        self.undo_stack = undo_stack
        self.qspinbox_fields = set(self.findChildren(CustomSpinBox))
        self.setUndoStack()
        self.numRanges = 1
        self.getRanges()

    def addRange(self) -> None:
        new_row = self.numRanges
        label_row = QLabel(f"{new_row + 1}")
        label_row.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.gridLayout.addWidget(label_row, new_row, 0)
        self.gridLayout.addWidget(CustomSpinBox(), new_row, 1)
        self.gridLayout.addWidget(CustomSpinBox(), new_row, 2)
        self.numRanges += 1

    def removeRange(self) -> None:
        if self.numRanges > 1:
            for col in range(3):
                item = self.gridLayout.itemAtPosition(self.numRanges - 1, col)
                if item is not None:
                    item.widget().deleteLater()
                    self.gridLayout.removeItem(item)
            self.numRanges -= 1

    def getRanges(self) -> list[list[float]]:
        ranges = []
        for row in range(self.numRanges):
            lb = self.gridLayout.itemAtPosition(row, 1).widget().value()
            ub = self.gridLayout.itemAtPosition(row, 2).widget().value()
            if lb != 0.0 or ub != 0.0:
                ranges.append([lb, ub])
        return ranges

    def setRanges(self, ranges: list[list[float]]) -> None:
        for row in range(self.numRanges):
            for col in range(1, 3):
                item = self.gridLayout.itemAtPosition(row, col)
                if item is not None:
                    item.widget().deleteLater()
                    self.gridLayout.removeItem(item)
        self.numRanges = 0
        for lb, ub in ranges:
            self.addRange()
            self.gridLayout.itemAtPosition(self.numRanges - 1, 1).widget().setValue(lb)
            self.gridLayout.itemAtPosition(self.numRanges - 1, 2).widget().setValue(ub)

        if self.numRanges == 0:
            self.addRange()
            self.gridLayout.itemAtPosition(self.numRanges - 1, 1).widget().setValue(0.0)
            self.gridLayout.itemAtPosition(self.numRanges - 1, 2).widget().setValue(0.0)

    def setUndoStack(self) -> None:
        for field in self.qspinbox_fields:
            field.valueChanged.connect(
                lambda value, field=field: self.undo_stack.push(
                    DoubleSpinBoxEdit(field, value)
                )
            )
