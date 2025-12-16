# This file handles the creation of all the custom dialogs
# used by the software

from typing import Literal

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QLineEdit,
    QMessageBox,
    QSpinBox,
)
from ui.PyES_about import Ui_dialogAbout
from ui.PyES_editDialog import Ui_EditColumnDialog
from ui.PyES_ionicStrengthInfo import Ui_IonicStrengthInfoDialog
from ui.PyES_newDialog import Ui_dialogNew
from ui.PyES_uncertaintyInfo import Ui_UncertaintyInfoDialog


class NewDialog(QDialog):
    def __init__(self, parent=None):
        """
        Dialog asking if you want to save before initializing new project.
        """
        super().__init__(parent)
        self.ui = Ui_dialogNew()
        self.ui.setupUi(self)


class EditColumnDialog(QDialog, Ui_EditColumnDialog):
    def __init__(
        self,
        items: dict[str, Literal["float", "integer", "string", "choice"]],
        parent=None,
    ):
        super().__init__(parent)
        self.setupUi(self)
        self.items = items
        self.columnComboBox.currentTextChanged.connect(self.update_filed_type)
        self.columnComboBox.addItems(self.items.keys())
        self.columnComboBox.insertSeparator(6)
        self.columnComboBox.insertSeparator(len(items))

        self.comboBox.addItems(list(self.items.keys())[6:-1])

    def update_filed_type(self, field_name: str):
        self.selected_field_name = field_name
        match self.items[field_name]:
            case "float":
                self.stackedWidget.setCurrentWidget(self.float_input)
            case "integer":
                self.stackedWidget.setCurrentWidget(self.integer_input)
            case "string":
                self.stackedWidget.setCurrentWidget(self.string_input)
            case "choice":
                self.stackedWidget.setCurrentWidget(self.choice_input)

    def accept(self) -> None:
        input_field = self.stackedWidget.currentWidget().children()[1]
        if isinstance(input_field, QComboBox):
            self.choice = input_field.currentText()
        elif isinstance(input_field, (QDoubleSpinBox, QSpinBox)):
            self.choice = input_field.value()
        elif isinstance(input_field, QLineEdit):
            self.choice = input_field.text()
        return super().accept()


class AboutDialog(QDialog):
    def __init__(self, parent=None):
        """
        Dialog reporting info about the program and liceses involved in its creation.
        """
        super().__init__(parent)
        self.ui = Ui_dialogAbout()
        self.ui.setupUi(self)


class NotSavedDialog(QMessageBox):
    def __init__(self, parent=None):
        """
        Dialog for asking confirmation of intention of closing the file when unsaved modification are present
        """
        super().__init__(parent)
        self.setIcon(QMessageBox.Icon.Question)
        self.setWindowTitle("Unsaved changes detected")
        self.setText("The document has been modified.")
        self.setInformativeText("Do you want to save your changes?")
        self.setStandardButtons(
            QMessageBox.StandardButton.Save
            | QMessageBox.StandardButton.Discard
            | QMessageBox.StandardButton.Cancel
        )
        self.setDefaultButton(QMessageBox.StandardButton.Save)


class WrongFileDialog(QMessageBox):
    def __init__(self, parent=None):
        """
        Dialog signaling that the selected file is not a valid project file.
        """
        super().__init__(parent)
        self.setWindowTitle("Wrong File")
        self.setText("The file you tried to open is not a valid PyES project file")
        self.setIcon(QMessageBox.Icon.Critical)


class IssuesLoadingDialog(QMessageBox):
    def __init__(self, parent=None):
        """
        Dialog signaling that the selected file is not a valid project file.
        """
        super().__init__(parent)
        self.setWindowTitle("Issues in Project File")
        self.setIcon(QMessageBox.Warning)


class CompletedCalculation(QMessageBox):
    def __init__(self, succesful: bool, parent=None):
        """
        Dialog signaling that the selected file is not a valid project file.
        """
        super().__init__(parent)
        if succesful:
            self.setWindowTitle("Completed")
            self.setText("Calculation was completed succesfully.")
            self.setIcon(QMessageBox.Information)
        else:
            self.setWindowTitle("Failure")
            self.setText(
                'Calculation was aborted, see the "Calculate" Tab for more info.'
            )
            self.setIcon(QMessageBox.Critical)


class IonicStrengthInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_IonicStrengthInfoDialog()
        self.ui.setupUi(self)

        self.ui.widget.load(":/equations/dh_equation.svg")
        self.ui.widget.renderer().setAspectRatioMode(Qt.KeepAspectRatio)

        self.ui.widget_2.load(":/equations/dh_expansion.svg")
        self.ui.widget_2.renderer().setAspectRatioMode(Qt.KeepAspectRatio)


class UncertaintyInfoDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_UncertaintyInfoDialog()
        self.ui.setupUi(self)

        self.ui.widget.load(":/equations/error_components.svg")
        self.ui.widget.renderer().setAspectRatioMode(Qt.KeepAspectRatio)

        self.ui.widget_2.load(":/equations/error_soluble.svg")
        self.ui.widget_2.renderer().setAspectRatioMode(Qt.KeepAspectRatio)

        self.ui.widget_3.load(":/equations/error_precipitate.svg")
        self.ui.widget_3.renderer().setAspectRatioMode(Qt.KeepAspectRatio)
