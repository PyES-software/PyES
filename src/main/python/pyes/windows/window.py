import json
import os
import sys
import traceback
from typing import Callable
from pathlib import Path

import pandas as pd
from commands import (
    AddTab,
    BetaRefineCheckAll,
    BetaRefineEdit,
    BetaRefineUncheckAll,
    ChangeWeightsModeCommand,
    ComponentsAddRows,
    ComponentsRemoveRows,
    ComponentsSwapRows,
    DoubleSpinBoxEdit,
    RemoveTab,
    SpeciesAddRows,
    SpeciesEditColumn,
    SpeciesRemoveRows,
    SpeciesSwapRows,
    TableCheckAll,
    TableUncheckAll,
    TitrationRefineEdit,
    dmodeEdit,
    imodeEdit,
    indCompEdit,
    uncertaintyEdit,
)
from dialogs import (
    AboutDialog,
    CompletedCalculation,
    EditColumnDialog,
    IonicStrengthInfoDialog,
    IssuesLoadingDialog,
    NotSavedDialog,
    UncertaintyInfoDialog,
    WrongFileDialog,
)
from libeq import SolverData
from PySide6.QtCore import (
    QByteArray,
    QModelIndex,
    QSettings,
    Qt,
    QThreadPool,
    QUrl,
    QSize,
)
from PySide6.QtGui import QDesktopServices, QKeySequence, QTextCursor, QUndoStack, QIcon
from PySide6.QtWidgets import (
    QComboBox,
    QDoubleSpinBox,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QMainWindow,
    QMessageBox,
    QTabBar,
    QTableView,
    QTableWidgetItem,
    QWidget,
    QToolButton,
)
from ui.PyES_main import Ui_MainWindow
from ui.widgets import CustomComboBox, inputTitrationOpt
from utils_func import (
    apply_list_map,
    apply_table_map,
    cleanData,
    get_list_map,
    get_table_map,
    get_widgets_from_tab,
    updateCompNames,
    updateIndComponent,
    value_or_problem,
)
from viewmodels.delegate import (
    CheckBoxDelegate,
    ComboBoxDelegate,
    LineEditDelegate,
    NumberFormatDelegate,
)
from viewmodels.models import (
    ComponentsModel,
    ConcentrationsModel,
    SolidSpeciesModel,
    SolubleSpeciesModel,
)
from workers import optimizeWorker

from windows.export import ExportWindow
from windows.monitor import MonitorWindow
from windows.plot import PlotWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Initiate threadpool
        self.threadpool = QThreadPool()

        if sys.platform.startswith("darwin"):
            self.threadpool.setStackSize(16 * 2**20)

        self.undostack = QUndoStack()
        # Setup for secondary windows
        self.PlotWindow = None
        self.ExportWindow = None
        self.MonitorWindow = MonitorWindow(self)

        self.undostack.cleanChanged.connect(self.check_clean_state)
        self.undostack.indexChanged.connect(self.MonitorWindow.set_waiting)

        self.actionUndo.triggered.connect(self.undostack.undo)
        self.actionUndo.setShortcut(QKeySequence.StandardKey.Undo)
        self.actionRedo.triggered.connect(self.undostack.redo)
        self.actionRedo.setShortcut(QKeySequence.StandardKey.Redo)

        # Initiate settings context
        self.settings = QSettings()
        self.settings.setValue("path/default", str(Path.home()))

        self.restoreGeometry(self.settings.value("mainwindow/geometry", QByteArray()))

        # Set window title and project path as defaults
        self.setWindowTitle("PyES - New Project")
        self.project_path = None

        self.qspinbox_fields: list[QDoubleSpinBox] = [
            self.refIonicStr,
            self.A,
            self.B,
            self.c0,
            self.c1,
            self.d0,
            self.d1,
            self.e0,
            self.e1,
            self.v0,
            self.initv,
            self.vinc,
            self.nop,
            self.c0back,
            self.ctback,
            self.initialLog,
            self.finalLog,
            self.logInc,
            self.cback,
        ]

        self.qcombobox_fields: list[QComboBox] = [
            self.imode,
            self.dmode,
            self.indComp,
            self.weightsMode,
        ]

        self.imode_fields: list[QWidget] = [
            self.refIonicStr,
            self.refIonicStr_label,
            self.A,
            self.A_label,
            self.B,
            self.B_label,
            self.c0,
            self.c0_label,
            self.c1,
            self.c1_label,
            self.d0,
            self.d0_label,
            self.d1,
            self.d1_label,
            self.e0,
            self.e0_label,
            self.e1,
            self.e1_label,
            self.c0back,
            self.c0back_label,
            self.ctback,
            self.ctback_label,
            self.cback,
            self.cback_label,
        ]

        for field in self.qspinbox_fields:
            field.valueChanged.connect(
                lambda value, field=field: self.undostack.push(
                    DoubleSpinBoxEdit(field, value)
                )
            )

        self.imode.currentIndexChanged.connect(
            lambda index: self.undostack.push(
                imodeEdit(
                    self.imode,
                    self.imode_fields,
                    [self.speciesView.model(), self.solidSpeciesView.model()],
                    self.titration_tabs,
                    index,
                )
            )
        )

        self.dmode.currentIndexChanged.connect(
            lambda index: self.undostack.push(
                dmodeEdit(
                    self.dmode,
                    index,
                    [self.dmode_inputs, self.mode_views],
                    self.concView,
                )
            )
        )

        self.indComp.currentIndexChanged.connect(
            lambda index: self.undostack.push(
                indCompEdit(
                    self.indComp,
                    index,
                    [self.initialLog_label, self.finalLog_label, self.logInc_label],
                    self.concModel,
                    self.dmode,
                )
            )
        )

        self.weightsMode.currentIndexChanged.connect(
            lambda index,
            field=self.weightsMode,
            titration_tabs=self.titration_tabs: self.undostack.push(
                ChangeWeightsModeCommand(field, index, titration_tabs)
            )
        )

        self.uncertaintyMode.toggled.connect(
            lambda state: self.undostack.push(
                uncertaintyEdit(
                    self.uncertaintyMode,
                    state,
                    [
                        self.speciesView.model(),
                        self.solidSpeciesView.model(),
                        self.concView.model(),
                    ],
                )
            )
        )

        # Generate clean data for tableviews
        (
            self.conc_data,
            self.comp_data,
            self.species_data,
            self.solid_species_data,
        ) = cleanData()

        # Connect slots for actions
        self.actionNew.triggered.connect(self.file_new)
        self.actionSave.triggered.connect(self.file_save)
        self.actionSaveAs.triggered.connect(self.file_save_as)
        self.actionOpen.triggered.connect(self.file_open)
        self.actionBSTAC.triggered.connect(self.import_bstac)
        self.actionSuperquad.triggered.connect(self.import_superquad)
        self.actionExit.triggered.connect(self.close)

        self.actionCalculate.triggered.connect(self.calculate)

        self.actionExport_Results.triggered.connect(self.exportDist)
        self.actionPlot_Results.triggered.connect(self.plotDist)
        self.actionMonitor_Results.triggered.connect(self.monitorWindow)

        self.actionAbout.triggered.connect(self.help_about)
        self.actionAbout_Qt.triggered.connect(self.help_about_qt)
        self.actionWebsite.triggered.connect(self.help_website)

        # Create a QWidget to hold the corner widgets
        titration_corner_widget = QWidget()
        titration_corner_layout = QHBoxLayout()

        # Create two QToolButtons
        add_titration_button = QToolButton()
        add_icon = QIcon()
        add_icon.addFile(
            ":/icons/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        add_titration_button.setIcon(add_icon)
        add_titration_button.clicked.connect(self.addTitration)
        add_titration_button.setFixedSize(20, 20)

        remove_titration_button = QToolButton()
        add_icon = QIcon()
        add_icon.addFile(
            ":/icons/minus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        remove_titration_button.setIcon(add_icon)
        remove_titration_button.clicked.connect(self.removeTitration)
        remove_titration_button.setFixedSize(20, 20)

        # Add the QToolButtons to the layout
        titration_corner_layout.addWidget(add_titration_button)
        titration_corner_layout.addWidget(remove_titration_button)

        # Set layout margins to zero for a tighter layout
        titration_corner_layout.setContentsMargins(0, 0, 0, 0)

        # Set the layout to the corner widget
        titration_corner_widget.setLayout(titration_corner_layout)

        # Set the corner widget to the top-left corner
        self.titration_tabs.setCornerWidget(titration_corner_widget, Qt.TopLeftCorner)

        self.concModel = ConcentrationsModel(self.conc_data, self.undostack)

        self.concView.setModel(self.concModel)
        self.concView.setItemDelegate(NumberFormatDelegate(self.concView))
        d0header = self.concView.horizontalHeader()
        d0header.setSectionResizeMode(QHeaderView.ResizeToContents)

        # Sets the tableview for the components
        self.compModel = ComponentsModel(self.comp_data, self.undostack)
        self.compView.setModel(self.compModel)
        self.compView.setItemDelegateForColumn(0, LineEditDelegate(self.compView))
        self.compView.setItemDelegateForColumn(1, NumberFormatDelegate(self.compView))
        compHeader = self.compView.horizontalHeader()
        compHeader.setSectionResizeMode(QHeaderView.ResizeToContents)
        # Connect the dataChanged signal to the corresponding slot
        # used to update header of species with components names
        self.compModel.dataChanged.connect(
            lambda _: updateCompNames(
                self.compModel,
                self.speciesView,
                self.solidSpeciesView,
                self.concModel,
                self.betaToRefine,
                [
                    table.model()
                    for table in get_widgets_from_tab(
                        self.titration_tabs, QTableView, "concView"
                    )
                ],
                self.indComp,
                get_widgets_from_tab(
                    self.titration_tabs, CustomComboBox, "electroActiveComponent"
                ),
                self.concToRefine,
            )
        )

        # Sets the tableview for the species
        self.speciesModel = SolubleSpeciesModel(self.species_data, self.undostack)
        self.speciesView.setModel(self.speciesModel)
        self.speciesView.setItemDelegateForColumn(0, CheckBoxDelegate(self.speciesView))
        self.speciesView.setItemDelegate(NumberFormatDelegate(self.speciesView))
        # assign combobox delegate to last column
        self.speciesView.setItemDelegateForColumn(
            self.speciesModel.columnCount() - 1,
            ComboBoxDelegate(self.speciesView, self.compModel._data["Name"].tolist()),
        )
        speciesHeader = self.speciesView.horizontalHeader()
        speciesHeader.setSectionResizeMode(QHeaderView.ResizeToContents)

        # Sets the tableview for the solid species
        self.solidSpeciesModel = SolidSpeciesModel(
            self.solid_species_data, self.undostack
        )
        self.solidSpeciesView.setModel(self.solidSpeciesModel)
        self.solidSpeciesView.setItemDelegateForColumn(
            0, CheckBoxDelegate(self.solidSpeciesView)
        )
        self.solidSpeciesView.setItemDelegate(
            NumberFormatDelegate(self.solidSpeciesView)
        )
        # assign combobox delegate to last column
        self.solidSpeciesView.setItemDelegateForColumn(
            self.solidSpeciesModel.columnCount() - 1,
            ComboBoxDelegate(
                self.solidSpeciesView, self.compModel._data["Name"].tolist()
            ),
        )
        solidSpeciesHeader = self.solidSpeciesView.horizontalHeader()
        solidSpeciesHeader.setSectionResizeMode(QHeaderView.ResizeToContents)

        self.speciesModel.dataChanged.connect(self.rename_beta_to_refine)

        # Interface is populated with empty basic data
        self.resetFields()

        self.solidSpeciesModel.layoutChanged.connect(self.check_solid_presence)

        self.betaCheckAll.clicked.connect(self.checkAllBeta)
        self.betaUncheckAll.clicked.connect(self.uncheckAllBeta)

        self.concCheckAll.clicked.connect(self.checkAllConc)
        self.concUncheckAll.clicked.connect(self.uncheckAllConc)

        self.electrodeCheckAll.clicked.connect(self.checkAllElectrode)
        self.electrodeUncheckAll.clicked.connect(self.uncheckAllElectrode)

        self.betaToRefine.itemClicked.connect(
            lambda item: self.undostack.push(BetaRefineEdit(item))
        )
        self.concToRefine.itemClicked.connect(
            lambda item: self.undostack.push(TitrationRefineEdit(item))
        )
        self.electrodeToRefine.itemClicked.connect(
            lambda item: self.undostack.push(TitrationRefineEdit(item))
        )

        # declare the checkline used to validate project files
        self.check_line = {"check": "PyES project file --- DO NOT MODIFY THIS LINE!"}

    def save_or_discard(self):
        """
        Display a prompt asking if you want to save or discard the current project
        """
        if not self.undostack.isClean():
            choice = NotSavedDialog().exec()

            if choice == QMessageBox.StandardButton.Cancel:
                return False
            elif choice == QMessageBox.StandardButton.Discard:
                pass
            elif choice == QMessageBox.StandardButton.Save:
                if not self.file_save():
                    return False
        return True

    def file_new(self):
        """
        Display a prompt asking if you want to create a new project
        """
        if not self.save_or_discard():
            return False

        self.resetFields()
        self.project_path = None
        self.setWindowTitle("PyES - New Project")
        # Resets results
        self.result = {}

        # Disable results windows
        if self.PlotWindow:
            self.PlotWindow.close()
        if self.ExportWindow:
            self.ExportWindow.close()
        self.MonitorWindow.reset_data()

        # Disable buttons to show results
        self.exportButton.setEnabled(False)
        self.plotDistButton.setEnabled(False)
        self.actionExport_Results.setEnabled(False)
        self.actionPlot_Results.setEnabled(False)

    def help_about(self):
        """
        Display about dialog
        """
        dialog = AboutDialog(self)
        dialog.exec()

    def help_about_qt(self):
        """
        Display about dialog
        """
        QMessageBox.aboutQt(self)

    def file_save(self):
        save_path = self.save_helper()
        self.update_file_title(save_path)

    def file_save_as(self):
        save_path = self.save_helper(save_as=True)
        self.update_file_title(save_path)

    def update_file_title(self, save_path):
        if save_path:
            # Store the file path
            self.project_path = save_path
            # Set window title accordingly
            self.setWindowTitle("PyES - " + self.project_path)

    def save_helper(self, save_as=False):
        """
        Saves current project as json file that can be later reopened
        """
        if save_as or self.project_path is None:
            output_path, filter = QFileDialog.getSaveFileName(
                self,
                "Save Project",
                (
                    self.project_path
                    if self.project_path is not None
                    else self.settings.value("path/default")
                ),
                "JSON (*.json)",
            )
        else:
            output_path = self.project_path

        if output_path:
            file_name = Path(output_path).parents[0]
            file_name = file_name.joinpath(Path(output_path).stem)
            file_name = file_name.with_suffix(".json")

            # dictionary that holds all the relevant data locations
            data_list = self.returnDataToDict()
            data = {**self.check_line, **data_list}

            with open(
                file_name,
                "w",
            ) as out_file:
                json.dump(data, out_file, indent=4)

            self.undostack.setClean()
            return output_path
        else:
            return None

    def file_open(self):
        """
        Load a previously saved project
        """
        if not self.save_or_discard():
            return False

        default_path = (
            self.settings.value("path/default")
            if self.project_path is None
            else os.path.dirname(self.project_path)
        )
        input_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Project",
            default_path,
            "JSON (*.json)",
        )

        if input_path:
            with open(
                input_path,
                "r",
            ) as input_file:
                try:
                    jsdata: dict = json.load(input_file)

                    # TODO: better and more robust validation of project files
                    # The loaded file has to be a valid project file, discard it if not
                    checksum = jsdata["check"]
                    assert checksum == self.check_line["check"]
                except (
                    json.JSONDecodeError,
                    UnicodeDecodeError,
                    KeyError,
                    AssertionError,
                ):
                    if not self.isVisible():
                        self.show()
                    dialog = WrongFileDialog(self)
                    dialog.exec()
                    return False

            return self.load_project_file(jsdata, input_path)

    def import_bstac(self):
        """
        Import a BSTAC file
        """
        self._import_common("BSTAC", SolverData.load_from_bstac)
        # if not self.save_or_discard():
        #     return False

        # default_path = (
        #     self.settings.value("path/default")
        #     if self.project_path is None
        #     else os.path.dirname(self.project_path)
        # )
        # input_path, _ = QFileDialog.getOpenFileName(
        #     self,
        #     "Import BSTAC file",
        #     default_path,
        # )

        # if input_path:
        #     try:
        #         parsed_data = SolverData.load_from_bstac(input_path)
        #         parsed_data = parsed_data.to_pyes()
        #     except Exception as e:
        #         dialog = WrongFileDialog(self)
        #         dialog.setText(
        #             "Error in parsing provided file as a valid BSTAC file:\n"
        #             + "".join(traceback.TracebackException.from_exception(e).format())
        #         )
        #         dialog.exec()
        #         return False

        #     self.load_project_file(parsed_data)

        #     self.dmode.setCurrentIndex(2)

    def import_superquad(self):
        """
        Import Superquad file.
        """
        self._import_common("SUPERQUAD", SolverData.load_from_superquad)
        # if not self.save_or_discard():
        #     return False

        # default_path = (
        #     self.settings.value("path/default")
        #     if self.project_path is None
        #     else os.path.dirname(self.project_path)
        # )
        # input_path, _ = QFileDialog.getOpenFileName(
        #     self,
        #     "Import SUPERQUAD file",
        #     default_path,
        # )
        # if not input_path:
        #     return

        # try:
        #     parsed_data = SolverData.load_from_superquad(input_path)
        #     parsed_data = parsed_data.to_pyes()
        # except Exception as e:
        #     dialog = WrongFileDialog(self)
        #     dialog.setText(
        #         "Error in parsing provided file as a valid SUPERQUAD file:\n"
        #         + "".join(traceback.TracebackException.from_exception(e).format())
        #     )
        #     dialog.exec()
        #     return False

        # self.load_project_file(parsed_data)

        # self.dmode.setCurrentIndex(2)

    def _import_common(self, legacy_name: str, legacy_parser: Callable):
        """
        Common tasks for importing legacy file
        """
        if not self.save_or_discard():
            return False

        default_path = (
            self.settings.value("path/default")
            if self.project_path is None
            else os.path.dirname(self.project_path)
        )
        input_path, _ = QFileDialog.getOpenFileName(
            self,
            f"Import {legacy_name} file",
            default_path,
        )

        if input_path:
            try:
                parsed_data = legacy_parser(input_path)
                parsed_data = parsed_data.to_pyes()
            except Exception as e:
                dialog = WrongFileDialog(self)
                dialog.setText(
                    f"Error in parsing provided file as a valid {legacy_name} file:\n"
                    + "".join(traceback.TracebackException.from_exception(e).format())
                )
                dialog.exec()
                return False

            self.load_project_file(parsed_data)

            self.dmode.setCurrentIndex(2)


    def load_project_file(self, jsdata, input_path=None):
        self.resetFields()
        # Resets results
        self.result = {}
        # Get file path from the open project file
        self.project_path = input_path

        # Set window title accordingly
        self.setWindowTitle(
            "PyES - " + (self.project_path if input_path else "New Project")
        )

        # Disable results windows
        if self.PlotWindow:
            self.PlotWindow.close()
        if self.ExportWindow:
            self.ExportWindow.close()

            # Disable buttons to show results
        self.exportButton.setEnabled(False)
        self.plotDistButton.setEnabled(False)
        self.actionExport_Results.setEnabled(False)
        self.actionPlot_Results.setEnabled(False)

        problems = []

        # Species Tab
        self.numComp.setValue(
            value_or_problem(jsdata, "nc", 1, "Number of components", problems)
        )
        self.numSpecies.setValue(
            value_or_problem(jsdata, "ns", 1, "Number of species", problems)
        )
        self.numPhases.setValue(
            value_or_problem(jsdata, "np", 0, "Number of phases", problems)
        )
        self.uncertaintyMode.setChecked(
            value_or_problem(jsdata, "emode", 0, "Uncertainty estimation", problems)
        )
        self.imode.setCurrentIndex(
            value_or_problem(jsdata, "imode", 0, "Ionic strength effect", problems)
        )
        self.refIonicStr.setValue(
            value_or_problem(jsdata, "ris", 0, "Reference ionic strength", problems)
        )
        self.A.setValue(
            value_or_problem(jsdata, "a", 0, "A parameter D-H equation", problems)
        )
        self.B.setValue(
            value_or_problem(jsdata, "b", 0, "B parameter D-H equation", problems),
        )
        self.c0.setValue(
            value_or_problem(jsdata, "c0", 0, "c0 parameter D-H equation", problems)
        )
        self.c1.setValue(
            value_or_problem(jsdata, "c1", 0, "c1 parameter D-H equation", problems)
        )
        self.d0.setValue(
            value_or_problem(jsdata, "d0", 0, "d0 parameter D-H equation", problems)
        )
        self.d1.setValue(
            value_or_problem(jsdata, "d1", 0, "d1 parameter D-H equation", problems)
        )
        self.e0.setValue(
            value_or_problem(jsdata, "e0", 0, "e0 parameter D-H equation", problems)
        )

        self.e1.setValue(
            value_or_problem(jsdata, "e1", 0, "e1 parameter D-H equation", problems)
        )

        # Settings tabs
        self.dmode.setCurrentIndex(
            value_or_problem(jsdata, "dmode", 0, "Work mode", problems)
        )

        self.v0.setValue(
            value_or_problem(jsdata, "v0", 0, "Initial titration volume", problems)
        )
        self.initv.setValue(
            value_or_problem(jsdata, "initv", 0, "First point of titration", problems),
        )
        self.vinc.setValue(
            value_or_problem(
                jsdata,
                "vinc",
                0,
                "Volume increments for each titration point",
                problems,
            )
        )
        self.nop.setValue(
            value_or_problem(jsdata, "nop", 1, "Number of titration points", problems)
        )
        self.c0back.setValue(
            value_or_problem(
                jsdata,
                "c0back",
                0,
                "Concentration of background ions in titration vessel",
                problems,
            )
        )
        self.ctback.setValue(
            value_or_problem(
                jsdata,
                "ctback",
                0,
                "Concentration of background ions in titrant",
                problems,
            )
        )

        ind_comp = value_or_problem(
            jsdata, "ind_comp", 0, "Independent component", problems
        )

        self.initialLog.setValue(
            value_or_problem(
                jsdata,
                "initialLog",
                0,
                "Initial Log of concentration of independent component",
                problems,
            )
        )
        self.finalLog.setValue(
            value_or_problem(
                jsdata,
                "finalLog",
                0,
                "Final Log of concentration of independent component",
                problems,
            )
        )
        self.logInc.setValue(
            value_or_problem(
                jsdata,
                "logInc",
                0,
                "Increments in Log of concentration of independent component",
                problems,
            )
        )
        self.cback.setValue(
            value_or_problem(
                jsdata, "cback", 0, "Concentration of background ions", problems
            )
        )
        poentiometric_data = value_or_problem(
            jsdata, "potentiometry_data", {}, "Potentiometric titration data", problems
        )

        titrations = value_or_problem(
            poentiometric_data, "titrations", [], "Titrations parameters", problems
        )

        for ix, titration_data in enumerate(titrations):
            if ix == 0:
                tab = self.titration_tabs.widget(ix)
                tab.findChild(inputTitrationOpt).set_data(titration_data)
            else:
                new_widget = QWidget()
                layout = QHBoxLayout()
                input_widget = inputTitrationOpt(
                    None,
                    undo_stack=self.undostack,
                    components=self.compModel._data["Name"].tolist(),
                )
                input_widget.set_data(titration_data)
                layout.addWidget(input_widget)
                new_widget.setLayout(layout)

                self.titration_tabs.addTab(
                    new_widget, str(self.titration_tabs.findChild(QTabBar).count() + 1)
                )

        self.concToRefine.setColumnCount(len(titrations))
        self.concToRefine.setRowCount(self.numComp.value())
        self.electrodeToRefine.setColumnCount(len(titrations))

        self.weightsMode.setCurrentIndex(
            value_or_problem(
                poentiometric_data,
                "weightsMode",
                0,
                "Weights used for calulation",
                problems,
            ),
        )

        apply_list_map(
            self.betaToRefine,
            value_or_problem(
                poentiometric_data,
                "beta_refine_flags",
                [False for _ in range(self.numSpecies.value())],
                "Constants to refine flags",
                problems,
            ),
        )

        apply_table_map(
            self.concToRefine,
            value_or_problem(
                poentiometric_data,
                "conc_refine_flags",
                [[False for _ in titrations] for _ in range(self.numComp.value())],
                "Concentrations to refine flags",
                problems,
            ),
        )
        apply_table_map(
            self.electrodeToRefine,
            value_or_problem(
                poentiometric_data,
                "electrode_refine_flags",
                [[False for _ in titrations] for _ in range(4)],
                "Electrode parameters to refine flags",
                problems,
            ),
        )

        # Calculate tab

        # Models
        self.compModel._data = pd.DataFrame.from_dict(
            value_or_problem(
                jsdata,
                "compModel",
                pd.concat(
                    [self.comp_data] * self.numComp.value(), ignore_index=True
                ).assign(
                    Name=sorted(
                        self.compModel.default_names,
                        key=lambda item: (len(item), item),
                    )[: self.numComp.value()]
                ),
                "Components model",
                problems,
            )
        )
        self.compModel._data.index = range(self.numComp.value())

        self.speciesModel._data = pd.DataFrame.from_dict(
            value_or_problem(
                jsdata,
                "speciesModel",
                pd.concat(
                    [self.species_data] * self.numSpecies.value(), ignore_index=True
                ),
                "Species model",
                problems,
            )
        )
        self.speciesModel._data.index = range(self.numSpecies.value())

        for row in range(self.numSpecies.value()):
            self.betaToRefine.item(row).setText(self.speciesModel._data.iloc[row, 1])
            if self.speciesModel._data.iloc[row, 0]:
                self.betaToRefine.item(row).setFlags(
                    self.betaToRefine.item(row).flags() & ~Qt.ItemFlag.ItemIsEnabled
                )
            else:
                self.betaToRefine.item(row).setFlags(
                    self.betaToRefine.item(row).flags() | Qt.ItemFlag.ItemIsEnabled
                )

        self.solidSpeciesModel._data = pd.DataFrame.from_dict(
            value_or_problem(
                jsdata,
                "solidSpeciesModel",
                self.solid_species_data,
                "Solid species model",
                problems,
            )
        )

        if self.solidSpeciesModel._data.empty:
            self.solidSpeciesModel._data = self.speciesModel._data.iloc[0:0, :].copy()
            self.solidSpeciesModel._data.rename(columns={"LogB": "LogKs"}, inplace=True)

        self.solidSpeciesModel._data.index = range(self.numPhases.value())

        self.concModel._data = pd.DataFrame.from_dict(
            value_or_problem(
                jsdata,
                "concModel",
                pd.concat(
                    [self.conc_data] * self.numComp.value(), ignore_index=True
                ).set_index(pd.Index(self.compModel._data["Name"])),
                "Concentrations model",
                problems,
            )
        )

        updateIndComponent(
            self.compModel,
            self.indComp,
            get_widgets_from_tab(
                self.titration_tabs, CustomComboBox, "electroActiveComponent"
            ),
        )
        updated_comps = self.compModel._data["Name"].tolist()
        self.speciesModel.updateHeader(updated_comps)
        self.speciesModel.updateCompName(updated_comps)
        self.solidSpeciesModel.updateHeader(updated_comps)
        self.solidSpeciesModel.updateCompName(updated_comps)
        self.indComp.currentIndexChanged.emit(ind_comp)
        self.speciesView.setItemDelegateForColumn(
            self.speciesModel.columnCount() - 1,
            ComboBoxDelegate(self.speciesView, self.compModel._data["Name"].tolist()),
        )
        self.solidSpeciesView.setItemDelegateForColumn(
            self.solidSpeciesModel.columnCount() - 1,
            ComboBoxDelegate(
                self.solidSpeciesView, self.compModel._data["Name"].tolist()
            ),
        )

        # The model layout changed so it has to be updated
        self.compModel.layoutChanged.emit()
        self.speciesModel.layoutChanged.emit()
        self.solidSpeciesModel.layoutChanged.emit()
        self.concModel.layoutChanged.emit()
        # Clear logger output
        self.consoleOutput.clear()

        # Clear undo stack after loading
        self.undostack.clear()

        if problems:
            problems_dialog = IssuesLoadingDialog(self)
            problems_dialog.setText(
                "The following fields had problems being imported:\n"
                + "\n".join([f"- {p}" for p in problems])
                + "\n" * 2
                + "Default values have been used in their place."
            )
            problems_dialog.exec()

    def help_website(self):
        """
        Opens the project website in the web
        """
        url = QUrl("https://github.com/Kastakin/PyES")
        QDesktopServices.openUrl(url)

    def resetFields(self):
        """
        Initializes the input fields as new "empty" values
        """
        (
            self.conc_data,
            self.comp_data,
            self.species_data,
            self.solid_species_data,
        ) = cleanData()

        # Reset number of comp/species/phases
        self.numComp.setValue(1)
        self.numSpecies.setValue(1)
        self.numPhases.setValue(0)

        # at init phases are 0 so disable the modelview
        self.solidSpeciesView.setEnabled(False)

        # Reset rel. error settings
        self.uncertaintyMode.setChecked(False)

        # Reset Ionic strenght params
        self.imode.currentIndexChanged.emit(0)
        self.refIonicStr.setValue(0)
        self.A.setValue(0.5)
        self.B.setValue(1.5)
        self.c0.setValue(0.1)
        self.c1.setValue(0.230)
        self.d0.setValue(0)
        self.d1.setValue(-0.1)
        self.e0.setValue(0)
        self.e1.setValue(0)

        # Set dmode as 0 (titration)
        # and display the correct associated widget
        self.dmode.currentIndexChanged.emit(0)

        # Resets fields for all dmodes
        # Titration
        self.v0.setValue(0)
        self.initv.setValue(0)
        self.vinc.setValue(0)
        self.nop.setValue(1)
        self.c0back.setValue(0)
        self.ctback.setValue(0)
        # Distribution
        self.initialLog.setValue(0)
        self.finalLog.setValue(0)
        self.logInc.setValue(0)
        self.cback.setValue(0)
        # Potentiometry
        self.weightsMode.setCurrentIndex(0)

        self.betaToRefine.item(0).setText("")

        self.concToRefine.setColumnCount(1)
        self.concToRefine.setRowCount(1)
        self.concToRefine.setVerticalHeaderLabels(["A"])
        item = QTableWidgetItem()
        item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
        item.setCheckState(Qt.CheckState.Unchecked)
        self.concToRefine.setItem(0, 0, item)

        self.electrodeToRefine.setColumnCount(1)
        self.electrodeToRefine.setRowCount(4)
        for row in range(4):
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(Qt.CheckState.Unchecked)
            self.electrodeToRefine.setItem(row, 0, item)

        for i in sorted(range(self.titration_tabs.count()), reverse=True):
            removed_widget = self.titration_tabs.widget(i)
            self.titration_tabs.removeTab(i)
            if removed_widget is not None:
                removed_widget.setParent(None)

        new_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(inputTitrationOpt(None, undo_stack=self.undostack))
        new_widget.setLayout(layout)

        self.titration_tabs.addTab(
            new_widget, str(self.titration_tabs.findChild(QTabBar).count() + 1)
        )

        # No results should be aviable so
        # grayout export and plot buttons
        self.plotDistButton.setEnabled(False)
        self.exportButton.setEnabled(False)
        self.actionExport_Results.setEnabled(False)
        self.actionPlot_Results.setEnabled(False)
        # Clear logger output
        self.consoleOutput.clear()

        # Clear previous stored results
        self.result = {}

        # if the function is called after
        # first initialization when models are already
        # declared update them to the empty values
        try:
            self.concModel._data = self.conc_data
            self.compModel._data = self.comp_data
            self.speciesModel._data = self.species_data
            self.solidSpeciesModel._data = self.solid_species_data
            self.concModel.layoutChanged.emit()
            self.compModel.layoutChanged.emit()
            self.speciesModel.layoutChanged.emit()
            self.solidSpeciesModel.layoutChanged.emit()
            updateIndComponent(
                self.compModel,
                self.indComp,
                get_widgets_from_tab(
                    self.titration_tabs, CustomComboBox, "electroActiveComponent"
                ),
            )
        except Exception:
            pass
        finally:
            self.tabWidget.setCurrentIndex(0)
            self.undostack.clear()

    def updateComp(self, rows):
        """
        Handles the updating to species and components models
        due to changes in the components present
        """
        if self.compModel.rowCount() < rows:
            added_rows = rows - self.compModel.rowCount()

            self.undostack.push(
                ComponentsAddRows(
                    self.compView,
                    self.speciesView,
                    self.solidSpeciesView,
                    self.concModel,
                    self.betaToRefine,
                    get_widgets_from_tab(self.titration_tabs, QTableView, "concView"),
                    get_widgets_from_tab(
                        self.titration_tabs, CustomComboBox, "electroActiveComponent"
                    ),
                    self.concToRefine,
                    self.indComp,
                    self.numComp,
                    self.compModel.rowCount(),
                    added_rows,
                )
            )

        elif self.compModel.rowCount() > rows:
            removed_rows = self.compModel.rowCount() - rows

            self.undostack.push(
                ComponentsRemoveRows(
                    self.compView,
                    self.speciesView,
                    self.solidSpeciesView,
                    self.concModel,
                    self.betaToRefine,
                    get_widgets_from_tab(self.titration_tabs, QTableView, "concView"),
                    get_widgets_from_tab(
                        self.titration_tabs, CustomComboBox, "electroActiveComponent"
                    ),
                    self.concToRefine,
                    self.indComp,
                    self.numComp,
                    self.compModel.rowCount(),
                    removed_rows,
                )
            )

    def updateSpecies(self):
        """
        Handles the updating species model due to changes in the number of species present.
        """
        new_value = self.numSpecies.value()
        if self.speciesModel.rowCount() < new_value:
            added_rows = new_value - self.speciesModel.rowCount()
            self.undostack.push(
                SpeciesAddRows(
                    self.speciesView,
                    self.numSpecies,
                    self.speciesModel.rowCount(),
                    added_rows,
                    True,
                    self.betaToRefine,
                )
            )
        elif self.speciesModel.rowCount() > new_value:
            removed_rows = self.speciesModel.rowCount() - new_value
            self.undostack.push(
                SpeciesRemoveRows(
                    self.speciesView,
                    self.numSpecies,
                    self.speciesModel.rowCount(),
                    removed_rows,
                    True,
                    self.betaToRefine,
                )
            )
        else:
            pass

    def updateSolid(self, s):
        """
        Handles the updating solid species model due to changes in the number of solid phases present.
        """
        if self.solidSpeciesModel.rowCount() < s:
            added_rows = s - self.solidSpeciesModel.rowCount()
            self.undostack.push(
                SpeciesAddRows(
                    self.solidSpeciesView,
                    self.numPhases,
                    self.solidSpeciesModel.rowCount(),
                    added_rows,
                    False,
                )
            )
        elif self.solidSpeciesModel.rowCount() > s:
            removed_rows = self.solidSpeciesModel.rowCount() - s
            self.undostack.push(
                SpeciesRemoveRows(
                    self.solidSpeciesView,
                    self.numPhases,
                    self.solidSpeciesModel.rowCount(),
                    removed_rows,
                    False,
                )
            )
        else:
            pass

    def insertCompAbove(self):
        if self.compView.selectedIndexes():
            row = self.compView.selectedIndexes()[0].row()
        else:
            row = 0
        self.undostack.push(
            ComponentsAddRows(
                self.compView,
                self.speciesView,
                self.solidSpeciesView,
                self.concModel,
                self.betaToRefine,
                get_widgets_from_tab(self.titration_tabs, QTableView, "concView"),
                get_widgets_from_tab(
                    self.titration_tabs, CustomComboBox, "electroActiveComponent"
                ),
                self.concToRefine,
                self.indComp,
                self.numComp,
                row,
                1,
            )
        )

    def insertCompBelow(self):
        if self.compView.selectedIndexes():
            row = self.compView.selectedIndexes()[0].row() + 1
        else:
            row = self.compModel.rowCount()
        self.undostack.push(
            ComponentsAddRows(
                self.compView,
                self.speciesView,
                self.solidSpeciesView,
                self.concModel,
                self.betaToRefine,
                get_widgets_from_tab(self.titration_tabs, QTableView, "concView"),
                get_widgets_from_tab(
                    self.titration_tabs, CustomComboBox, "electroActiveComponent"
                ),
                self.concToRefine,
                self.indComp,
                self.numComp,
                row,
                1,
            )
        )

    def removeComp(self):
        if self.compView.selectedIndexes() and self.compModel.rowCount() > 1:
            if (
                QMessageBox.question(
                    self,
                    "Deleting Component",
                    "Are you sure you want to delete the selected component?",
                )
                == QMessageBox.Yes
            ):
                row = self.compView.selectedIndexes()[0].row() + 1
                self.undostack.push(
                    ComponentsRemoveRows(
                        self.compView,
                        self.speciesView,
                        self.solidSpeciesView,
                        self.concModel,
                        self.betaToRefine,
                        get_widgets_from_tab(
                            self.titration_tabs, QTableView, "concView"
                        ),
                        get_widgets_from_tab(
                            self.titration_tabs,
                            CustomComboBox,
                            "electroActiveComponent",
                        ),
                        self.concToRefine,
                        self.indComp,
                        self.numComp,
                        row,
                        1,
                    )
                )

    def moveCompUp(self):
        if self.compView.selectedIndexes():
            selected_ind_comp = self.indComp.currentData(0)
            row = self.compView.selectedIndexes()[0].row()
            if row != 0:
                self.undostack.push(
                    ComponentsSwapRows(
                        self.compView,
                        self.speciesView,
                        self.solidSpeciesView,
                        self.concModel,
                        self.betaToRefine,
                        get_widgets_from_tab(
                            self.titration_tabs, QTableView, "concView"
                        ),
                        get_widgets_from_tab(
                            self.titration_tabs,
                            CustomComboBox,
                            "electroActiveComponent",
                        ),
                        self.concToRefine,
                        self.indComp,
                        selected_ind_comp,
                        row,
                        row - 1,
                    )
                )

    def moveCompDown(self):
        if self.compView.selectedIndexes():
            selected_ind_comp = self.indComp.currentData(0)
            row = self.compView.selectedIndexes()[0].row()
            if row != self.compModel.rowCount() - 1:
                self.undostack.push(
                    ComponentsSwapRows(
                        self.compView,
                        self.speciesView,
                        self.solidSpeciesView,
                        self.concModel,
                        self.betaToRefine,
                        get_widgets_from_tab(
                            self.titration_tabs, QTableView, "concView"
                        ),
                        get_widgets_from_tab(
                            self.titration_tabs,
                            CustomComboBox,
                            "electroActiveComponent",
                        ),
                        self.concToRefine,
                        self.indComp,
                        selected_ind_comp,
                        row,
                        row + 1,
                    )
                )

    def insertSpeciesAbove(self):
        table = self.get_shown_tab()
        if not table:
            return
        add_soluble = True if table == self.speciesView else False

        counter = self.get_shown_tab_counter()
        selected_indexes = table.selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
        else:
            row = 0

        self.undostack.push(
            SpeciesAddRows(table, counter, row, 1, add_soluble, self.betaToRefine)
        )

    def insertSpeciesBelow(self):
        table = self.get_shown_tab()
        if not table:
            return
        add_soluble = True if table == self.speciesView else False

        counter = self.get_shown_tab_counter()
        selected_indexes = table.selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row() + 1
        else:
            row = table.model().rowCount()

        self.undostack.push(
            SpeciesAddRows(table, counter, row, 1, add_soluble, self.betaToRefine)
        )

    def removeSpecies(self):
        table = self.get_shown_tab()
        if not table or (table == self.speciesView and self.numSpecies.value() == 1):
            return
        add_soluble = True if table == self.speciesView else False

        counter = self.get_shown_tab_counter()
        selected_indexes = table.selectedIndexes()
        if selected_indexes:
            if (
                QMessageBox.question(
                    self,
                    "Deleting Species",
                    "Are you sure you want to delete the selected species?",
                )
                == QMessageBox.Yes
            ):
                self.undostack.push(
                    SpeciesRemoveRows(
                        table,
                        counter,
                        selected_indexes[0].row() + 1,
                        1,
                        add_soluble,
                        self.betaToRefine,
                    )
                )

    def moveSpeciesUp(self):
        table = self.get_shown_tab()
        if not table:
            return
        swap_soluble = True if table == self.speciesView else False

        selected_indexes = table.selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            if row != 0:
                self.undostack.push(
                    SpeciesSwapRows(
                        table, row, row - 1, swap_soluble, self.betaToRefine
                    )
                )

    def moveSpeciesDown(self):
        table = self.get_shown_tab()
        if not table:
            return
        swap_soluble = True if table == self.speciesView else False

        selected_indexes = table.selectedIndexes()
        if selected_indexes:
            row = selected_indexes[0].row()
            if row != (table.model().rowCount() - 1):
                self.undostack.push(
                    SpeciesSwapRows(
                        table, row, row + 1, swap_soluble, self.betaToRefine
                    )
                )

    def checkAllSpecies(self):
        table = self.get_shown_tab()
        if not table:
            return
        self.undostack.push(SpeciesEditColumn(table, 0, True))

    def uncheckAllSpecies(self):
        table = self.get_shown_tab()
        if not table:
            return
        self.undostack.push(SpeciesEditColumn(table, 0, False))

    def massEditColumn(self):
        table = self.get_shown_tab()
        if not table:
            return

        items = dict(zip(table.model()._data.columns[2:8], ["float" for _ in range(6)]))
        items.update(
            dict(zip(table.model()._data.columns[8:-1], ["integer" for _ in range(6)]))
        )
        items[table.model()._data.columns[-1]] = "choice"

        dlg = EditColumnDialog(items=items)
        if dlg.exec():
            self.undostack.push(
                SpeciesEditColumn(
                    table,
                    list(items.keys()).index(dlg.selected_field_name) + 2,
                    dlg.choice,
                )
            )

    def get_shown_tab(self):
        if self.tablesTab.currentIndex() == 0:
            table = self.speciesView
        elif self.tablesTab.currentIndex() == 1:
            table = self.solidSpeciesView
        else:
            table = None
        return table

    def get_shown_tab_counter(self):
        if self.tablesTab.currentIndex() == 0:
            counter = self.numSpecies
        elif self.tablesTab.currentIndex() == 1:
            counter = self.numPhases
        else:
            counter = None
        return counter

    def calculate(self):
        "Initiate calculations."
        # Disable the button, one omptimization calculation at the time
        self.calcButton.setEnabled(False)
        self.plotDistButton.setEnabled(False)
        self.exportButton.setEnabled(False)
        self.actionExport_Results.setEnabled(False)
        self.actionPlot_Results.setEnabled(False)

        # Clear old results and secondary windows
        self.result = {}
        self.PlotWindow = None
        self.ExportWindow = None

        # Clear Logger
        self.consoleOutput.setText("")
        data_list = self.returnDataToDict()
        debug = self.debug.isChecked()
        worker = optimizeWorker(data_list, debug)

        # Conncect worker signals to slots
        worker.signals.finished.connect(self.workerComplete)
        worker.signals.result.connect(self.storeResults)
        worker.signals.log.connect(self.logger)
        worker.signals.aborted.connect(self.aborted)

        # Execute
        self.threadpool.start(worker)

    def workerComplete(self):
        self.consoleOutput.moveCursor(QTextCursor.Start)
        self.calcButton.setEnabled(True)
        self.plotDistButton.setEnabled(True)
        self.exportButton.setEnabled(True)
        self.actionExport_Results.setEnabled(True)
        self.actionPlot_Results.setEnabled(True)
        self.MonitorWindow.recieve_data(self.result.get("optimized_constants", None))
        info_dialog = CompletedCalculation(succesful=True)
        info_dialog.exec()

    def aborted(self, error):
        self.consoleOutput.append("### ERROR ###")
        self.consoleOutput.append(error)
        self.consoleOutput.append("### ABORTED ###")

        self.calcButton.setEnabled(True)
        info_dialog = CompletedCalculation(succesful=False)
        info_dialog.exec()

    def logger(self, log):
        self.consoleOutput.append(log)

    def exportDist(self):
        """
        Export calculated distribution in csv/excel format
        """
        if self.ExportWindow is None:
            self.ExportWindow = ExportWindow(self)
        else:
            self.ExportWindow.result = self.result
        self.ExportWindow.show()

    def monitorWindow(self):
        """
        Open the monitor window
        """
        if self.MonitorWindow.isHidden():
            self.MonitorWindow.show()
        else:
            self.MonitorWindow.hide()

    def storeResults(self, data, name):
        """
        Store result for exporting.
        """
        if name in self.result:
            if isinstance(self.result[name], list):
                self.result[name].append(data)
            else:
                self.result[name] = [self.result[name], data]
        else:
            self.result[name] = data

    def plotDist(self, data):
        """
        Plot the distribution of species obtained from the optimization
        """
        if self.PlotWindow is None:
            self.PlotWindow = PlotWindow(self)
        self.PlotWindow.show()

    def v0Updater(self, value):
        self.initv.setMinimum(value)

    def closeEvent(self, event):
        """
        Cleanup before closing.
        """
        if not self.save_or_discard():
            event.ignore()

        self.settings.setValue("mainwindow/geometry", self.saveGeometry())

        # Close any secondary window still open
        if self.ExportWindow:
            self.ExportWindow.close()
        if self.PlotWindow:
            self.PlotWindow.close()
        self.MonitorWindow.close()

    def check_clean_state(self, clean: bool) -> None:
        title = self.windowTitle()
        if not clean:
            self.setWindowTitle(f"* {title}")
        else:
            self.setWindowTitle(title.lstrip("* "))

    def check_solid_presence(self):
        if self.solidSpeciesModel.rowCount() == 0:
            self.solidSpeciesView.setEnabled(False)
        else:
            self.solidSpeciesView.setEnabled(True)

    def displayUncertaintyInfo(self):
        UncertaintyInfoDialog(parent=self).exec()

    def displayIonicStrengthInfo(self):
        IonicStrengthInfoDialog(parent=self).exec()

    def addTitration(self):
        self.undostack.push(
            AddTab(
                self.titration_tabs,
                self.undostack,
                self.compModel._data["Name"].tolist(),
                self.concToRefine,
                self.electrodeToRefine,
            )
        )

    def removeTitration(self):
        if (
            QMessageBox.question(
                self,
                "Deleting Titration",
                "Are you sure you want to delete the currently selected titration?",
            )
            == QMessageBox.Yes
        ):
            self.undostack.push(
                RemoveTab(
                    self.titration_tabs, self.concToRefine, self.electrodeToRefine
                )
            )

    def returnDataToDict(self):
        """
        Returns a dict containing the relevant data extracted from the form.

        If saving is True dataframes/tables are returned as dictionaries for ease of storage reasons.
        Otherwise dictionay will simply hold the dataframes as they are.
        """
        data_list = {
            "nc": self.numComp.value(),
            "ns": self.numSpecies.value(),
            "np": self.numPhases.value(),
            "emode": self.uncertaintyMode.isChecked(),
            "imode": self.imode.currentIndex(),
            "ris": self.refIonicStr.value(),
            "a": self.A.value(),
            "b": self.B.value(),
            "c0": self.c0.value(),
            "c1": self.c1.value(),
            "d0": self.d0.value(),
            "d1": self.d1.value(),
            "e0": self.e0.value(),
            "e1": self.e1.value(),
            "dmode": self.dmode.currentIndex(),
            "v0": self.v0.value(),
            "initv": self.initv.value(),
            "vinc": self.vinc.value(),
            "nop": self.nop.value(),
            "c0back": self.c0back.value(),
            "ctback": self.ctback.value(),
            "ind_comp": self.indComp.currentIndex(),
            "initialLog": self.initialLog.value(),
            "finalLog": self.finalLog.value(),
            "logInc": self.logInc.value(),
            "cback": self.cback.value(),
        }

        titrations = []

        for i in range(self.titration_tabs.count()):
            tab = self.titration_tabs.widget(i)
            titrations.append(tab.findChild(inputTitrationOpt).retrive_data())

        beta_refine = get_list_map(self.betaToRefine)
        conc_refine = get_table_map(self.concToRefine)
        electrode_refine = get_table_map(self.electrodeToRefine)

        data_list["potentiometry_data"] = {
            "weightsMode": self.weightsMode.currentIndex(),
            "beta_refine_flags": beta_refine,
            "conc_refine_flags": conc_refine,
            "electrode_refine_flags": electrode_refine,
            "titrations": titrations,
        }

        data_models = {
            "compModel": self.compModel._data.to_dict(),
            "concModel": self.concModel._data.to_dict(),
        }
        data_models["speciesModel"] = self.speciesModel._data.to_dict()
        data_models["solidSpeciesModel"] = self.solidSpeciesModel._data.to_dict()

        data_list = {**data_list, **data_models}
        return data_list

    def rename_beta_to_refine(self, index: QModelIndex):
        row = index.row()
        column = index.column()
        if column >= 8 and column < self.speciesModel.columnCount() - 1:
            self.betaToRefine.item(row).setText(self.speciesModel.getColumn(1)[row])
        elif column == 0:
            if self.speciesModel._data.iloc[row, 0]:
                self.betaToRefine.item(row).setFlags(
                    self.betaToRefine.item(row).flags() & ~Qt.ItemFlag.ItemIsEnabled
                )
            else:
                self.betaToRefine.item(row).setFlags(
                    self.betaToRefine.item(row).flags() | Qt.ItemFlag.ItemIsEnabled
                )

    def checkAllBeta(self):
        self.undostack.push(BetaRefineCheckAll(self.betaToRefine))

    def uncheckAllBeta(self):
        self.undostack.push(BetaRefineUncheckAll(self.betaToRefine))

    def checkAllConc(self):
        self.undostack.push(TableCheckAll(self.concToRefine))

    def uncheckAllConc(self):
        self.undostack.push(TableUncheckAll(self.concToRefine))

    def checkAllElectrode(self):
        self.undostack.push(TableCheckAll(self.electrodeToRefine))

    def uncheckAllElectrode(self):
        self.undostack.push(TableUncheckAll(self.electrodeToRefine))

    def editBeta(self, item):
        print(not item.checkState())
