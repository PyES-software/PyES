from PySide6.QtCore import QLocale
from PySide6.QtGui import QDoubleValidator
from PySide6.QtWidgets import QDoubleSpinBox, QLineEdit, QWidget


class CustomSpinBox(QDoubleSpinBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.previous_value = self.value()

    def focusInEvent(self, event):
        self.previous_value = self.value()
        QDoubleSpinBox.focusInEvent(self, event)


class LineSpinBox(QLineEdit):
    def __init__(
        self,
        parent=None,
        bottom: float = -float("inf"),
        top: float = float("inf"),
        decimals: int = -1,
    ):
        QLineEdit.__init__(self, parent)
        float_validator = DotDoubleValidator(bottom, top, decimals)
        float_validator.setLocale(QLocale("UnitedStates"))
        float_validator.setNotation(DotDoubleValidator.ScientificNotation)

        self.setValidator(float_validator)


class DotDoubleValidator(QDoubleValidator):
    def __init__(
        self,
        bottom: float = -float("inf"),
        top: float = float("inf"),
        decimals: int = -1,
        parent=None,
    ) -> None:
        return super().__init__(bottom, top, decimals, parent)

    def validate(self, input: str, pos: int) -> object:
        if "," in input:
            return QDoubleValidator.Intermediate
        return super().validate(input, pos)

    def fixup(self, input: str) -> str:
        return input.replace(",", ".")
