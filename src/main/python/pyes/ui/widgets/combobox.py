from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QComboBox, QWidget


class CustomComboBox(QComboBox):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.previous_index = self.currentIndex()

    def mousePressEvent(self, e: QMouseEvent) -> None:
        self.previous_index = self.currentIndex()
        return super().mousePressEvent(e)