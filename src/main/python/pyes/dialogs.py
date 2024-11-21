# This file handles the creation of all the custom dialogs
# used by the software

from typing import Literal

import pandas as pd
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QDoubleSpinBox,
    QFileDialog,
    QLineEdit,
    QMessageBox,
    QSpinBox,
    QWidget,
)
from ui.PyES_about import Ui_dialogAbout
from ui.PyES_editDialog import Ui_EditColumnDialog
from ui.PyES_ionicStrengthInfo import Ui_IonicStrengthInfoDialog
from ui.PyES_load import Ui_loadCSVDialog
from ui.PyES_uncertaintyInfo import Ui_UncertaintyInfoDialog


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


class loadCSVDialog(QDialog, Ui_loadCSVDialog):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        from viewmodels.models import PreviewModel

        self.setupUi(self)
        self.setModal(True)

        # Generate a preview view/model
        self.previewModel = PreviewModel()
        self.preview.setModel(self.previewModel)

        # No file is being opened yet
        self.fileName = None

        # Get initial settings
        self.updateSettings()

        self.no_weights.stateChanged.connect(self.importWeights)
        self.no_weights.setChecked(True)

        self.eCol.valueChanged.connect(self.updateEColumnColor)
        self.vCol.valueChanged.connect(self.updateVColumnColor)
        self.wCol.valueChanged.connect(self.updateWColumnColor)
        self.vCol.setValue(0)
        self.eCol.setValue(1)
        self.wCol.setValue(2)

    def updateEColumnColor(self, v):
        self.previewModel.red_colored = v
        self.previewModel.layoutChanged.emit()
        self.updateSettings()

    def updateVColumnColor(self, v):
        self.previewModel.blue_colored = v
        self.previewModel.layoutChanged.emit()
        self.updateSettings()

    def updateWColumnColor(self, v):
        self.previewModel.green_colored = v
        self.previewModel.layoutChanged.emit()
        self.updateSettings()

    def updateSettings(self):
        self.settings = {
            "sep": self.separator.currentText(),
            "dec": self.decimal.currentText(),
            "head": self.head.value(),
            "footer": self.footer.value(),
            "vcol": self.vCol.value(),
            "ecol": self.eCol.value(),
            "wcol": self.wCol.value(),
        }

        if not self.separator.isEnabled():
            self.settings["sep"] = None

        if not self.decimal.isEnabled():
            self.settings["dec"] = None

        self._updateModel()

    def autodetectSep(self, s):
        # TODO: find why Qt.CheckState.Checked does not work
        if s == 2:
            self.separator.setEnabled(False)
        else:
            self.separator.setEnabled(True)
        self.updateSettings()

    def autodetectDec(self, s):
        # TODO: find why Qt.CheckState.Checked does not work
        if s == 2:
            self.decimal.setEnabled(False)
        else:
            self.decimal.setEnabled(True)
        self.updateSettings()

    def importWeights(self, s):
        if s == 2:
            self.wCol.setEnabled(False)
            self.previewModel.green_colored = None
        else:
            self.wCol.setEnabled(True)
            self.previewModel.green_colored = None
        self.updateSettings()

    def loadFile(self):
        self.fileName, _ = QFileDialog.getOpenFileName(
            self, "Open CSV", "~", "CSV (*.csv)"
        )
        self._updateModel()

    def _updateModel(self):
        if self.fileName:
            self.filePath.setText(self.fileName)
            self.previewModel._data = pd.read_csv(
                self.fileName,
                sep=self.settings["sep"],
                decimal=self.settings["dec"],
                skiprows=self.settings["head"],
                skipfooter=self.settings["footer"],
                header=None,
            )
            self.previewModel.layoutChanged.emit()

    def get_final_model(self):
        columns = [self.settings["vcol"], self.settings["ecol"]]
        if not self.no_weights.isChecked():
            wcol = self.settings["wcol"]
            if self.previewModel._data.columns.size <= wcol:
                columns.append(0)
            else:
                columns.append(self.settings["wcol"])
        else:
            columns.append(0)
        data = self.previewModel._data.iloc[:, columns]
        if self.no_weights.isChecked():
            data.iloc[:, 2] = 0

        data.insert(0, "ignored", False)
        data.columns = [str(i) for i in range(data.shape[1])]
        data.insert(4, "pX", 0)
        # data = data.astype(float)
        return data
