# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_main.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

import resources_rc
from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    Qt,
    QTime,
    QUrl,
)
from PySide6.QtGui import (
    QAction,
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QAbstractItemView,
    QAbstractScrollArea,
    QApplication,
    QCheckBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLayout,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMenu,
    QMenuBar,
    QPushButton,
    QSizePolicy,
    QSpacerItem,
    QSpinBox,
    QStackedWidget,
    QStatusBar,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
    QTextEdit,
    QToolBar,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ui.widgets import CustomComboBox
from ui.widgets.spinbox import CustomSpinBox


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1289, 809)
        MainWindow.setMinimumSize(QSize(1289, 809))
        MainWindow.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        MainWindow.setUnifiedTitleAndToolBarOnMac(True)
        self.actionNew = QAction(MainWindow)
        self.actionNew.setObjectName("actionNew")
        self.actionNew.setEnabled(True)
        icon = QIcon()
        icon.addFile(
            ":/icons/document.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.actionNew.setIcon(icon)
        self.actionOpen = QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        icon1 = QIcon()
        icon1.addFile(
            ":/icons/folder-open-document.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.actionOpen.setIcon(icon1)
        self.actionSave = QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        icon2 = QIcon()
        icon2.addFile(":/icons/disk.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionSave.setIcon(icon2)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName("actionAbout")
        icon3 = QIcon()
        icon3.addFile(
            ":/icons/question-frame.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.actionAbout.setIcon(icon3)
        self.actionExit = QAction(MainWindow)
        self.actionExit.setObjectName("actionExit")
        self.actionExit.setMenuRole(QAction.MenuRole.QuitRole)
        self.actionWebsite = QAction(MainWindow)
        self.actionWebsite.setObjectName("actionWebsite")
        self.actionCalculate = QAction(MainWindow)
        self.actionCalculate.setObjectName("actionCalculate")
        icon4 = QIcon()
        icon4.addFile(
            ":/icons/control.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.actionCalculate.setIcon(icon4)
        self.actionExport_Results = QAction(MainWindow)
        self.actionExport_Results.setObjectName("actionExport_Results")
        icon5 = QIcon()
        icon5.addFile(
            ":/icons/application-export.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.actionExport_Results.setIcon(icon5)
        self.actionPlot_Results = QAction(MainWindow)
        self.actionPlot_Results.setObjectName("actionPlot_Results")
        icon6 = QIcon()
        icon6.addFile(
            ":/icons/pencil-ruler.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.actionPlot_Results.setIcon(icon6)
        self.actionAbout_Qt = QAction(MainWindow)
        self.actionAbout_Qt.setObjectName("actionAbout_Qt")
        self.actionUndo = QAction(MainWindow)
        self.actionUndo.setObjectName("actionUndo")
        icon7 = QIcon()
        iconThemeName = "edit-undo"
        if QIcon.hasThemeIcon(iconThemeName):
            icon7 = QIcon.fromTheme(iconThemeName)
        else:
            icon7.addFile(
                "../../../../../../../.designer/backup",
                QSize(),
                QIcon.Mode.Normal,
                QIcon.State.Off,
            )

        self.actionUndo.setIcon(icon7)
        self.actionRedo = QAction(MainWindow)
        self.actionRedo.setObjectName("actionRedo")
        icon8 = QIcon()
        iconThemeName = "edit-redo"
        if QIcon.hasThemeIcon(iconThemeName):
            icon8 = QIcon.fromTheme(iconThemeName)
        else:
            icon8.addFile(
                "../../../../../../../.designer/backup",
                QSize(),
                QIcon.Mode.Normal,
                QIcon.State.Off,
            )

        self.actionRedo.setIcon(icon8)
        self.actionSaveAs = QAction(MainWindow)
        self.actionSaveAs.setObjectName("actionSaveAs")
        icon9 = QIcon()
        icon9.addFile(
            ":/icons/disk--plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.actionSaveAs.setIcon(icon9)
        self.actionBSTAC = QAction(MainWindow)
        self.actionBSTAC.setObjectName("actionBSTAC")
        self.actionMonitor_Results = QAction(MainWindow)
        self.actionMonitor_Results.setObjectName("actionMonitor_Results")
        icon10 = QIcon()
        icon10.addFile(":/icons/eye.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.actionMonitor_Results.setIcon(icon10)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_5 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(2, 2, 2, 2)
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tabWidget.setTabShape(QTabWidget.TabShape.Rounded)
        self.tabWidget.setUsesScrollButtons(False)
        self.tabWidget.setDocumentMode(False)
        self.Species = QWidget()
        self.Species.setObjectName("Species")
        self.Species.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.horizontalLayout = QHBoxLayout(self.Species)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setSizeConstraint(
            QLayout.SizeConstraint.SetDefaultConstraint
        )
        self.horizontalLayout.setContentsMargins(5, 5, 5, 5)
        self.widget_7 = QWidget(self.Species)
        self.widget_7.setObjectName("widget_7")
        self.widget_7.setEnabled(True)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget_7.sizePolicy().hasHeightForWidth())
        self.widget_7.setSizePolicy(sizePolicy)
        self.verticalLayout_6 = QVBoxLayout(self.widget_7)
        self.verticalLayout_6.setSpacing(8)
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(1, 0, 1, 1)
        self.sys_opt_label = QLabel(self.widget_7)
        self.sys_opt_label.setObjectName("sys_opt_label")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.sys_opt_label.sizePolicy().hasHeightForWidth()
        )
        self.sys_opt_label.setSizePolicy(sizePolicy1)

        self.verticalLayout_6.addWidget(self.sys_opt_label)

        self.frame_5 = QFrame(self.widget_7)
        self.frame_5.setObjectName("frame_5")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Maximum
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.frame_5.sizePolicy().hasHeightForWidth())
        self.frame_5.setSizePolicy(sizePolicy2)
        self.frame_5.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_5.setFrameShadow(QFrame.Shadow.Sunken)
        self.horizontalLayout_6 = QHBoxLayout(self.frame_5)
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.horizontalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.widget_8 = QWidget(self.frame_5)
        self.widget_8.setObjectName("widget_8")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.widget_8.sizePolicy().hasHeightForWidth())
        self.widget_8.setSizePolicy(sizePolicy3)
        self.formLayout_3 = QFormLayout(self.widget_8)
        self.formLayout_3.setObjectName("formLayout_3")
        self.formLayout_3.setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)
        self.formLayout_3.setFieldGrowthPolicy(
            QFormLayout.FieldGrowthPolicy.AllNonFixedFieldsGrow
        )
        self.formLayout_3.setContentsMargins(-1, 5, -1, 5)
        self.comp_label = QLabel(self.widget_8)
        self.comp_label.setObjectName("comp_label")
        sizePolicy4 = QSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
        )
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.comp_label.sizePolicy().hasHeightForWidth())
        self.comp_label.setSizePolicy(sizePolicy4)

        self.formLayout_3.setWidget(0, QFormLayout.LabelRole, self.comp_label)

        self.numComp = QSpinBox(self.widget_8)
        self.numComp.setObjectName("numComp")
        sizePolicy5 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Fixed
        )
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.numComp.sizePolicy().hasHeightForWidth())
        self.numComp.setSizePolicy(sizePolicy5)
        self.numComp.setMinimum(1)
        self.numComp.setMaximum(999)

        self.formLayout_3.setWidget(0, QFormLayout.FieldRole, self.numComp)

        self.species_label = QLabel(self.widget_8)
        self.species_label.setObjectName("species_label")
        sizePolicy4.setHeightForWidth(
            self.species_label.sizePolicy().hasHeightForWidth()
        )
        self.species_label.setSizePolicy(sizePolicy4)

        self.formLayout_3.setWidget(1, QFormLayout.LabelRole, self.species_label)

        self.numSpecies = QSpinBox(self.widget_8)
        self.numSpecies.setObjectName("numSpecies")
        sizePolicy5.setHeightForWidth(self.numSpecies.sizePolicy().hasHeightForWidth())
        self.numSpecies.setSizePolicy(sizePolicy5)
        self.numSpecies.setMinimum(1)
        self.numSpecies.setMaximum(999)

        self.formLayout_3.setWidget(1, QFormLayout.FieldRole, self.numSpecies)

        self.phases_label = QLabel(self.widget_8)
        self.phases_label.setObjectName("phases_label")
        sizePolicy4.setHeightForWidth(
            self.phases_label.sizePolicy().hasHeightForWidth()
        )
        self.phases_label.setSizePolicy(sizePolicy4)

        self.formLayout_3.setWidget(2, QFormLayout.LabelRole, self.phases_label)

        self.numPhases = QSpinBox(self.widget_8)
        self.numPhases.setObjectName("numPhases")
        sizePolicy5.setHeightForWidth(self.numPhases.sizePolicy().hasHeightForWidth())
        self.numPhases.setSizePolicy(sizePolicy5)
        self.numPhases.setMinimum(0)
        self.numPhases.setMaximum(999)
        self.numPhases.setValue(0)

        self.formLayout_3.setWidget(2, QFormLayout.FieldRole, self.numPhases)

        self.line_7 = QFrame(self.widget_8)
        self.line_7.setObjectName("line_7")
        self.line_7.setFrameShape(QFrame.Shape.HLine)
        self.line_7.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_3.setWidget(3, QFormLayout.SpanningRole, self.line_7)

        self.line = QFrame(self.widget_8)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_3.setWidget(8, QFormLayout.SpanningRole, self.line)

        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.ionic_strength_info = QToolButton(self.widget_8)
        self.ionic_strength_info.setObjectName("ionic_strength_info")
        sizePolicy6 = QSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum
        )
        sizePolicy6.setHorizontalStretch(0)
        sizePolicy6.setVerticalStretch(0)
        sizePolicy6.setHeightForWidth(
            self.ionic_strength_info.sizePolicy().hasHeightForWidth()
        )
        self.ionic_strength_info.setSizePolicy(sizePolicy6)
        icon11 = QIcon()
        icon11.addFile(
            ":/icons/information-frame.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.ionic_strength_info.setIcon(icon11)

        self.gridLayout.addWidget(self.ionic_strength_info, 0, 2, 1, 1)

        self.formLayout_6 = QFormLayout()
        self.formLayout_6.setObjectName("formLayout_6")
        self.imode_label = QLabel(self.widget_8)
        self.imode_label.setObjectName("imode_label")

        self.formLayout_6.setWidget(0, QFormLayout.LabelRole, self.imode_label)

        self.imode = CustomComboBox(self.widget_8)
        self.imode.addItem("")
        self.imode.addItem("")
        self.imode.setObjectName("imode")
        sizePolicy3.setHeightForWidth(self.imode.sizePolicy().hasHeightForWidth())
        self.imode.setSizePolicy(sizePolicy3)

        self.formLayout_6.setWidget(0, QFormLayout.FieldRole, self.imode)

        self.gridLayout.addLayout(self.formLayout_6, 0, 0, 1, 2)

        self.formLayout_7 = QFormLayout()
        self.formLayout_7.setObjectName("formLayout_7")
        self.refIonicStr_label = QLabel(self.widget_8)
        self.refIonicStr_label.setObjectName("refIonicStr_label")
        self.refIonicStr_label.setEnabled(False)

        self.formLayout_7.setWidget(0, QFormLayout.LabelRole, self.refIonicStr_label)

        self.refIonicStr = CustomSpinBox(self.widget_8)
        self.refIonicStr.setObjectName("refIonicStr")
        self.refIonicStr.setEnabled(False)
        self.refIonicStr.setDecimals(5)
        self.refIonicStr.setMaximum(999.000000000000000)
        self.refIonicStr.setSingleStep(0.050000000000000)

        self.formLayout_7.setWidget(0, QFormLayout.FieldRole, self.refIonicStr)

        self.A_label = QLabel(self.widget_8)
        self.A_label.setObjectName("A_label")
        self.A_label.setEnabled(False)

        self.formLayout_7.setWidget(1, QFormLayout.LabelRole, self.A_label)

        self.A = CustomSpinBox(self.widget_8)
        self.A.setObjectName("A")
        self.A.setEnabled(False)
        self.A.setDecimals(4)
        self.A.setMinimum(-999.000000000000000)
        self.A.setMaximum(999.000000000000000)
        self.A.setSingleStep(0.050000000000000)

        self.formLayout_7.setWidget(1, QFormLayout.FieldRole, self.A)

        self.B_label = QLabel(self.widget_8)
        self.B_label.setObjectName("B_label")
        self.B_label.setEnabled(False)

        self.formLayout_7.setWidget(2, QFormLayout.LabelRole, self.B_label)

        self.B = CustomSpinBox(self.widget_8)
        self.B.setObjectName("B")
        self.B.setEnabled(False)
        self.B.setDecimals(4)
        self.B.setMinimum(-999.000000000000000)
        self.B.setMaximum(999.000000000000000)
        self.B.setSingleStep(0.050000000000000)

        self.formLayout_7.setWidget(2, QFormLayout.FieldRole, self.B)

        self.c0_label = QLabel(self.widget_8)
        self.c0_label.setObjectName("c0_label")
        self.c0_label.setEnabled(False)

        self.formLayout_7.setWidget(3, QFormLayout.LabelRole, self.c0_label)

        self.c0 = CustomSpinBox(self.widget_8)
        self.c0.setObjectName("c0")
        self.c0.setEnabled(False)
        self.c0.setDecimals(4)
        self.c0.setMinimum(-999.000000000000000)
        self.c0.setMaximum(999.000000000000000)
        self.c0.setSingleStep(0.050000000000000)

        self.formLayout_7.setWidget(3, QFormLayout.FieldRole, self.c0)

        self.c1_label = QLabel(self.widget_8)
        self.c1_label.setObjectName("c1_label")
        self.c1_label.setEnabled(False)

        self.formLayout_7.setWidget(4, QFormLayout.LabelRole, self.c1_label)

        self.c1 = CustomSpinBox(self.widget_8)
        self.c1.setObjectName("c1")
        self.c1.setEnabled(False)
        self.c1.setDecimals(4)
        self.c1.setMinimum(-999.000000000000000)
        self.c1.setMaximum(999.000000000000000)
        self.c1.setSingleStep(0.050000000000000)

        self.formLayout_7.setWidget(4, QFormLayout.FieldRole, self.c1)

        self.d0_label = QLabel(self.widget_8)
        self.d0_label.setObjectName("d0_label")
        self.d0_label.setEnabled(False)

        self.formLayout_7.setWidget(5, QFormLayout.LabelRole, self.d0_label)

        self.d0 = CustomSpinBox(self.widget_8)
        self.d0.setObjectName("d0")
        self.d0.setEnabled(False)
        self.d0.setDecimals(4)
        self.d0.setMinimum(-999.000000000000000)
        self.d0.setMaximum(999.000000000000000)
        self.d0.setSingleStep(0.050000000000000)

        self.formLayout_7.setWidget(5, QFormLayout.FieldRole, self.d0)

        self.d1_label = QLabel(self.widget_8)
        self.d1_label.setObjectName("d1_label")
        self.d1_label.setEnabled(False)

        self.formLayout_7.setWidget(6, QFormLayout.LabelRole, self.d1_label)

        self.d1 = CustomSpinBox(self.widget_8)
        self.d1.setObjectName("d1")
        self.d1.setEnabled(False)
        self.d1.setDecimals(4)
        self.d1.setMinimum(-999.000000000000000)
        self.d1.setMaximum(999.000000000000000)
        self.d1.setSingleStep(0.050000000000000)

        self.formLayout_7.setWidget(6, QFormLayout.FieldRole, self.d1)

        self.e0_label = QLabel(self.widget_8)
        self.e0_label.setObjectName("e0_label")
        self.e0_label.setEnabled(False)

        self.formLayout_7.setWidget(7, QFormLayout.LabelRole, self.e0_label)

        self.e0 = CustomSpinBox(self.widget_8)
        self.e0.setObjectName("e0")
        self.e0.setEnabled(False)
        self.e0.setDecimals(4)
        self.e0.setMinimum(-999.000000000000000)
        self.e0.setMaximum(999.000000000000000)
        self.e0.setSingleStep(0.050000000000000)

        self.formLayout_7.setWidget(7, QFormLayout.FieldRole, self.e0)

        self.e1_label = QLabel(self.widget_8)
        self.e1_label.setObjectName("e1_label")
        self.e1_label.setEnabled(False)

        self.formLayout_7.setWidget(8, QFormLayout.LabelRole, self.e1_label)

        self.e1 = CustomSpinBox(self.widget_8)
        self.e1.setObjectName("e1")
        self.e1.setEnabled(False)
        self.e1.setDecimals(4)
        self.e1.setMinimum(-999.000000000000000)
        self.e1.setMaximum(999.000000000000000)
        self.e1.setSingleStep(0.050000000000000)

        self.formLayout_7.setWidget(8, QFormLayout.FieldRole, self.e1)

        self.gridLayout.addLayout(self.formLayout_7, 1, 0, 1, 3)

        self.gridLayout.setRowStretch(0, 1)

        self.formLayout_3.setLayout(10, QFormLayout.SpanningRole, self.gridLayout)

        self.gridLayout_2 = QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.uncertainty_info = QToolButton(self.widget_8)
        self.uncertainty_info.setObjectName("uncertainty_info")
        self.uncertainty_info.setIcon(icon11)

        self.gridLayout_2.addWidget(self.uncertainty_info, 0, 1, 1, 1)

        self.formLayout_4 = QFormLayout()
        self.formLayout_4.setObjectName("formLayout_4")
        self.uncertaintyMode = QCheckBox(self.widget_8)
        self.uncertaintyMode.setObjectName("uncertaintyMode")
        self.uncertaintyMode.setChecked(True)

        self.formLayout_4.setWidget(0, QFormLayout.SpanningRole, self.uncertaintyMode)

        self.gridLayout_2.addLayout(self.formLayout_4, 0, 0, 1, 1)

        self.formLayout_3.setLayout(7, QFormLayout.SpanningRole, self.gridLayout_2)

        self.horizontalLayout_6.addWidget(self.widget_8)

        self.verticalLayout_6.addWidget(self.frame_5)

        self.verticalSpacer_2 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_6.addItem(self.verticalSpacer_2)

        self.horizontalLayout.addWidget(self.widget_7)

        self.widget_6 = QWidget(self.Species)
        self.widget_6.setObjectName("widget_6")
        sizePolicy4.setHeightForWidth(self.widget_6.sizePolicy().hasHeightForWidth())
        self.widget_6.setSizePolicy(sizePolicy4)
        self.verticalLayout_8 = QVBoxLayout(self.widget_6)
        self.verticalLayout_8.setSpacing(8)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.tab_comp_label = QLabel(self.widget_6)
        self.tab_comp_label.setObjectName("tab_comp_label")
        sizePolicy4.setHeightForWidth(
            self.tab_comp_label.sizePolicy().hasHeightForWidth()
        )
        self.tab_comp_label.setSizePolicy(sizePolicy4)

        self.verticalLayout_8.addWidget(self.tab_comp_label)

        self.horizontalFrame_2 = QFrame(self.widget_6)
        self.horizontalFrame_2.setObjectName("horizontalFrame_2")
        sizePolicy4.setHeightForWidth(
            self.horizontalFrame_2.sizePolicy().hasHeightForWidth()
        )
        self.horizontalFrame_2.setSizePolicy(sizePolicy4)
        self.horizontalFrame_2.setFrameShape(QFrame.Shape.Box)
        self.horizontalFrame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_8 = QHBoxLayout(self.horizontalFrame_2)
        self.horizontalLayout_8.setObjectName("horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 2, 0, 2)
        self.insert_above_comp_button = QToolButton(self.horizontalFrame_2)
        self.insert_above_comp_button.setObjectName("insert_above_comp_button")
        icon12 = QIcon()
        icon12.addFile(
            ":/icons/table-insert-row-before.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.insert_above_comp_button.setIcon(icon12)
        self.insert_above_comp_button.setIconSize(QSize(18, 18))
        self.insert_above_comp_button.setAutoRaise(True)

        self.horizontalLayout_8.addWidget(self.insert_above_comp_button)

        self.insert_below_comp_button = QToolButton(self.horizontalFrame_2)
        self.insert_below_comp_button.setObjectName("insert_below_comp_button")
        sizePolicy7 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy7.setHorizontalStretch(0)
        sizePolicy7.setVerticalStretch(0)
        sizePolicy7.setHeightForWidth(
            self.insert_below_comp_button.sizePolicy().hasHeightForWidth()
        )
        self.insert_below_comp_button.setSizePolicy(sizePolicy7)
        icon13 = QIcon()
        icon13.addFile(
            ":/icons/table-insert-row-after.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.insert_below_comp_button.setIcon(icon13)
        self.insert_below_comp_button.setIconSize(QSize(18, 18))
        self.insert_below_comp_button.setAutoRaise(True)

        self.horizontalLayout_8.addWidget(self.insert_below_comp_button)

        self.remove_comp_button = QToolButton(self.horizontalFrame_2)
        self.remove_comp_button.setObjectName("remove_comp_button")
        icon14 = QIcon()
        icon14.addFile(
            ":/icons/table-delete-row.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.remove_comp_button.setIcon(icon14)
        self.remove_comp_button.setIconSize(QSize(18, 18))
        self.remove_comp_button.setAutoRaise(True)

        self.horizontalLayout_8.addWidget(self.remove_comp_button)

        self.line_5 = QFrame(self.horizontalFrame_2)
        self.line_5.setObjectName("line_5")
        self.line_5.setFrameShape(QFrame.Shape.VLine)
        self.line_5.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_8.addWidget(self.line_5)

        self.move_up_comp_button = QToolButton(self.horizontalFrame_2)
        self.move_up_comp_button.setObjectName("move_up_comp_button")
        icon15 = QIcon()
        icon15.addFile(
            ":/icons/row_up.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.move_up_comp_button.setIcon(icon15)
        self.move_up_comp_button.setIconSize(QSize(18, 18))
        self.move_up_comp_button.setAutoRaise(True)

        self.horizontalLayout_8.addWidget(self.move_up_comp_button)

        self.move_down_comp_button = QToolButton(self.horizontalFrame_2)
        self.move_down_comp_button.setObjectName("move_down_comp_button")
        icon16 = QIcon()
        icon16.addFile(
            ":/icons/row_down.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.move_down_comp_button.setIcon(icon16)
        self.move_down_comp_button.setIconSize(QSize(18, 18))
        self.move_down_comp_button.setAutoRaise(True)

        self.horizontalLayout_8.addWidget(self.move_down_comp_button)

        self.horizontalSpacer_2 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_8.addItem(self.horizontalSpacer_2)

        self.verticalLayout_8.addWidget(self.horizontalFrame_2)

        self.compView = QTableView(self.widget_6)
        self.compView.setObjectName("compView")
        sizePolicy8 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        sizePolicy8.setHorizontalStretch(0)
        sizePolicy8.setVerticalStretch(0)
        sizePolicy8.setHeightForWidth(self.compView.sizePolicy().hasHeightForWidth())
        self.compView.setSizePolicy(sizePolicy8)
        self.compView.setMaximumSize(QSize(180, 16777215))
        self.compView.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored
        )
        self.compView.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.compView.setProperty("showDropIndicator", False)
        self.compView.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.compView.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.compView.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.compView.verticalHeader().setVisible(False)

        self.verticalLayout_8.addWidget(self.compView)

        self.horizontalLayout.addWidget(self.widget_6)

        self.widget_2 = QWidget(self.Species)
        self.widget_2.setObjectName("widget_2")
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(1, 1, 1, 1)
        self.tab_comp_label_2 = QLabel(self.widget_2)
        self.tab_comp_label_2.setObjectName("tab_comp_label_2")
        sizePolicy4.setHeightForWidth(
            self.tab_comp_label_2.sizePolicy().hasHeightForWidth()
        )
        self.tab_comp_label_2.setSizePolicy(sizePolicy4)

        self.verticalLayout.addWidget(self.tab_comp_label_2)

        self.horizontalFrame = QFrame(self.widget_2)
        self.horizontalFrame.setObjectName("horizontalFrame")
        sizePolicy9 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred
        )
        sizePolicy9.setHorizontalStretch(0)
        sizePolicy9.setVerticalStretch(0)
        sizePolicy9.setHeightForWidth(
            self.horizontalFrame.sizePolicy().hasHeightForWidth()
        )
        self.horizontalFrame.setSizePolicy(sizePolicy9)
        self.horizontalFrame.setFrameShape(QFrame.Shape.Box)
        self.horizontalFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.horizontalFrame)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 2, 0, 2)
        self.checkAllSpeciesButton = QToolButton(self.horizontalFrame)
        self.checkAllSpeciesButton.setObjectName("checkAllSpeciesButton")
        icon17 = QIcon()
        icon17.addFile(
            ":/icons/ui-check-box.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.checkAllSpeciesButton.setIcon(icon17)
        self.checkAllSpeciesButton.setIconSize(QSize(18, 18))
        self.checkAllSpeciesButton.setAutoRaise(True)

        self.horizontalLayout_4.addWidget(self.checkAllSpeciesButton)

        self.uncheckAllSpeciesButton = QToolButton(self.horizontalFrame)
        self.uncheckAllSpeciesButton.setObjectName("uncheckAllSpeciesButton")
        icon18 = QIcon()
        icon18.addFile(
            ":/icons/ui-check-box-uncheck.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        self.uncheckAllSpeciesButton.setIcon(icon18)
        self.uncheckAllSpeciesButton.setIconSize(QSize(18, 18))
        self.uncheckAllSpeciesButton.setAutoRaise(True)

        self.horizontalLayout_4.addWidget(self.uncheckAllSpeciesButton)

        self.line_6 = QFrame(self.horizontalFrame)
        self.line_6.setObjectName("line_6")
        self.line_6.setFrameShape(QFrame.Shape.VLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line_6)

        self.insert_above_species_button = QToolButton(self.horizontalFrame)
        self.insert_above_species_button.setObjectName("insert_above_species_button")
        self.insert_above_species_button.setIcon(icon12)
        self.insert_above_species_button.setIconSize(QSize(18, 18))
        self.insert_above_species_button.setAutoRaise(True)

        self.horizontalLayout_4.addWidget(self.insert_above_species_button)

        self.insert_below_species_button = QToolButton(self.horizontalFrame)
        self.insert_below_species_button.setObjectName("insert_below_species_button")
        sizePolicy7.setHeightForWidth(
            self.insert_below_species_button.sizePolicy().hasHeightForWidth()
        )
        self.insert_below_species_button.setSizePolicy(sizePolicy7)
        self.insert_below_species_button.setIcon(icon13)
        self.insert_below_species_button.setIconSize(QSize(18, 18))
        self.insert_below_species_button.setAutoRaise(True)

        self.horizontalLayout_4.addWidget(self.insert_below_species_button)

        self.remove_species_button = QToolButton(self.horizontalFrame)
        self.remove_species_button.setObjectName("remove_species_button")
        self.remove_species_button.setIcon(icon14)
        self.remove_species_button.setIconSize(QSize(18, 18))
        self.remove_species_button.setAutoRaise(True)

        self.horizontalLayout_4.addWidget(self.remove_species_button)

        self.line_4 = QFrame(self.horizontalFrame)
        self.line_4.setObjectName("line_4")
        self.line_4.setFrameShape(QFrame.Shape.VLine)
        self.line_4.setFrameShadow(QFrame.Shadow.Sunken)

        self.horizontalLayout_4.addWidget(self.line_4)

        self.move_up_species_button = QToolButton(self.horizontalFrame)
        self.move_up_species_button.setObjectName("move_up_species_button")
        self.move_up_species_button.setIcon(icon15)
        self.move_up_species_button.setIconSize(QSize(18, 18))
        self.move_up_species_button.setAutoRaise(True)

        self.horizontalLayout_4.addWidget(self.move_up_species_button)

        self.move_down_species_button = QToolButton(self.horizontalFrame)
        self.move_down_species_button.setObjectName("move_down_species_button")
        self.move_down_species_button.setIcon(icon16)
        self.move_down_species_button.setIconSize(QSize(18, 18))
        self.move_down_species_button.setAutoRaise(True)

        self.horizontalLayout_4.addWidget(self.move_down_species_button)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_4.addItem(self.horizontalSpacer)

        self.edit_column_button = QToolButton(self.horizontalFrame)
        self.edit_column_button.setObjectName("edit_column_button")
        icon19 = QIcon()
        icon19.addFile(
            ":/icons/table--pencil.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.edit_column_button.setIcon(icon19)
        self.edit_column_button.setIconSize(QSize(18, 18))
        self.edit_column_button.setAutoRaise(True)

        self.horizontalLayout_4.addWidget(self.edit_column_button)

        self.verticalLayout.addWidget(self.horizontalFrame)

        self.tablesTab = QTabWidget(self.widget_2)
        self.tablesTab.setObjectName("tablesTab")
        self.tablesTab.setUsesScrollButtons(False)
        self.species = QWidget()
        self.species.setObjectName("species")
        self.verticalLayout_3 = QVBoxLayout(self.species)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 5, 5, 5)
        self.speciesView = QTableView(self.species)
        self.speciesView.setObjectName("speciesView")
        self.speciesView.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored
        )
        self.speciesView.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.speciesView.setProperty("showDropIndicator", False)
        self.speciesView.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.speciesView.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.speciesView.setTextElideMode(Qt.TextElideMode.ElideNone)
        self.speciesView.horizontalHeader().setCascadingSectionResizes(True)

        self.verticalLayout_3.addWidget(self.speciesView)

        icon20 = QIcon()
        icon20.addFile(":/icons/flask.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.tablesTab.addTab(self.species, icon20, "")
        self.solidspecies = QWidget()
        self.solidspecies.setObjectName("solidspecies")
        self.verticalLayout_12 = QVBoxLayout(self.solidspecies)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName("verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(5, 5, 5, 5)
        self.solidSpeciesView = QTableView(self.solidspecies)
        self.solidSpeciesView.setObjectName("solidSpeciesView")
        self.solidSpeciesView.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustIgnored
        )
        self.solidSpeciesView.setEditTriggers(
            QAbstractItemView.EditTrigger.AllEditTriggers
        )
        self.solidSpeciesView.setProperty("showDropIndicator", False)
        self.solidSpeciesView.setSelectionMode(
            QAbstractItemView.SelectionMode.SingleSelection
        )
        self.solidSpeciesView.setSelectionBehavior(
            QAbstractItemView.SelectionBehavior.SelectRows
        )
        self.solidSpeciesView.horizontalHeader().setCascadingSectionResizes(True)

        self.verticalLayout_12.addWidget(self.solidSpeciesView)

        icon21 = QIcon()
        icon21.addFile(
            ":/icons/beaker-empty.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off
        )
        self.tablesTab.addTab(self.solidspecies, icon21, "")

        self.verticalLayout.addWidget(self.tablesTab)

        self.horizontalLayout.addWidget(self.widget_2)

        self.horizontalLayout.setStretch(1, 2)
        self.horizontalLayout.setStretch(2, 5)
        self.tabWidget.addTab(self.Species, "")
        self.Settings = QWidget()
        self.Settings.setObjectName("Settings")
        self.Settings.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.Settings.sizePolicy().hasHeightForWidth())
        self.Settings.setSizePolicy(sizePolicy1)
        self.verticalLayout_7 = QVBoxLayout(self.Settings)
        self.verticalLayout_7.setObjectName("verticalLayout_7")
        self.verticalLayout_7.setSizeConstraint(QLayout.SizeConstraint.SetMaximumSize)
        self.verticalLayout_7.setContentsMargins(5, 5, 5, 5)
        self.dmodeSelector = QWidget(self.Settings)
        self.dmodeSelector.setObjectName("dmodeSelector")
        sizePolicy6.setHeightForWidth(
            self.dmodeSelector.sizePolicy().hasHeightForWidth()
        )
        self.dmodeSelector.setSizePolicy(sizePolicy6)
        self.horizontalLayout_2 = QHBoxLayout(self.dmodeSelector)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.dmode_label = QLabel(self.dmodeSelector)
        self.dmode_label.setObjectName("dmode_label")
        sizePolicy6.setHeightForWidth(self.dmode_label.sizePolicy().hasHeightForWidth())
        self.dmode_label.setSizePolicy(sizePolicy6)

        self.horizontalLayout_2.addWidget(self.dmode_label)

        self.dmode = CustomComboBox(self.dmodeSelector)
        self.dmode.addItem("")
        self.dmode.addItem("")
        self.dmode.addItem("")
        self.dmode.setObjectName("dmode")
        sizePolicy7.setHeightForWidth(self.dmode.sizePolicy().hasHeightForWidth())
        self.dmode.setSizePolicy(sizePolicy7)

        self.horizontalLayout_2.addWidget(self.dmode)

        self.verticalLayout_7.addWidget(self.dmodeSelector)

        self.mode_views = QStackedWidget(self.Settings)
        self.mode_views.setObjectName("mode_views")
        self.pyes_modes = QWidget()
        self.pyes_modes.setObjectName("pyes_modes")
        self.horizontalLayout_7 = QHBoxLayout(self.pyes_modes)
        self.horizontalLayout_7.setSpacing(0)
        self.horizontalLayout_7.setObjectName("horizontalLayout_7")
        self.horizontalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.dmode0Input = QWidget(self.pyes_modes)
        self.dmode0Input.setObjectName("dmode0Input")
        sizePolicy9.setHeightForWidth(self.dmode0Input.sizePolicy().hasHeightForWidth())
        self.dmode0Input.setSizePolicy(sizePolicy9)
        self.horizontalLayout_3 = QHBoxLayout(self.dmode0Input)
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 500, 0)
        self.dmode_inputs = QStackedWidget(self.dmode0Input)
        self.dmode_inputs.setObjectName("dmode_inputs")
        sizePolicy4.setHeightForWidth(
            self.dmode_inputs.sizePolicy().hasHeightForWidth()
        )
        self.dmode_inputs.setSizePolicy(sizePolicy4)
        self.page = QWidget()
        self.page.setObjectName("page")
        sizePolicy4.setHeightForWidth(self.page.sizePolicy().hasHeightForWidth())
        self.page.setSizePolicy(sizePolicy4)
        self.horizontalLayout_9 = QHBoxLayout(self.page)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.horizontalLayout_9.setContentsMargins(0, 0, 0, 0)
        self.widget_3 = QWidget(self.page)
        self.widget_3.setObjectName("widget_3")
        sizePolicy10 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred
        )
        sizePolicy10.setHorizontalStretch(0)
        sizePolicy10.setVerticalStretch(0)
        sizePolicy10.setHeightForWidth(self.widget_3.sizePolicy().hasHeightForWidth())
        self.widget_3.setSizePolicy(sizePolicy10)
        self.widget_3.setMinimumSize(QSize(263, 287))
        self.verticalLayout_9 = QVBoxLayout(self.widget_3)
        self.verticalLayout_9.setObjectName("verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 25, 0, 0)
        self.frame = QFrame(self.widget_3)
        self.frame.setObjectName("frame")
        sizePolicy2.setHeightForWidth(self.frame.sizePolicy().hasHeightForWidth())
        self.frame.setSizePolicy(sizePolicy2)
        self.frame.setMinimumSize(QSize(280, 0))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout = QFormLayout(self.frame)
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.formLayout.setContentsMargins(-1, 0, -1, 6)
        self.label_3 = QLabel(self.frame)
        self.label_3.setObjectName("label_3")

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.label_3)

        self.v0_label = QLabel(self.frame)
        self.v0_label.setObjectName("v0_label")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.v0_label)

        self.v0 = CustomSpinBox(self.frame)
        self.v0.setObjectName("v0")
        self.v0.setDecimals(3)
        self.v0.setMaximum(900.000000000000000)
        self.v0.setSingleStep(0.050000000000000)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.v0)

        self.initv_label = QLabel(self.frame)
        self.initv_label.setObjectName("initv_label")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.initv_label)

        self.initv = CustomSpinBox(self.frame)
        self.initv.setObjectName("initv")
        self.initv.setDecimals(3)
        self.initv.setMaximum(900.000000000000000)
        self.initv.setSingleStep(0.050000000000000)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.initv)

        self.vinc_label = QLabel(self.frame)
        self.vinc_label.setObjectName("vinc_label")

        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.vinc_label)

        self.vinc = CustomSpinBox(self.frame)
        self.vinc.setObjectName("vinc")
        self.vinc.setDecimals(3)
        self.vinc.setMaximum(900.000000000000000)
        self.vinc.setSingleStep(0.050000000000000)

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.vinc)

        self.nop_label = QLabel(self.frame)
        self.nop_label.setObjectName("nop_label")

        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.nop_label)

        self.nop = CustomSpinBox(self.frame)
        self.nop.setObjectName("nop")
        self.nop.setDecimals(0)
        self.nop.setMinimum(1.000000000000000)
        self.nop.setMaximum(9000.000000000000000)
        self.nop.setSingleStep(1.000000000000000)

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.nop)

        self.line_2 = QFrame(self.frame)
        self.line_2.setObjectName("line_2")
        self.line_2.setFrameShape(QFrame.Shape.HLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout.setWidget(5, QFormLayout.SpanningRole, self.line_2)

        self.label_4 = QLabel(self.frame)
        self.label_4.setObjectName("label_4")

        self.formLayout.setWidget(6, QFormLayout.SpanningRole, self.label_4)

        self.c0back_label = QLabel(self.frame)
        self.c0back_label.setObjectName("c0back_label")
        self.c0back_label.setEnabled(False)

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.c0back_label)

        self.ctback_label = QLabel(self.frame)
        self.ctback_label.setObjectName("ctback_label")
        self.ctback_label.setEnabled(False)

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.ctback_label)

        self.c0back = CustomSpinBox(self.frame)
        self.c0back.setObjectName("c0back")
        self.c0back.setEnabled(False)
        self.c0back.setDecimals(5)
        self.c0back.setMaximum(900.000000000000000)
        self.c0back.setSingleStep(0.050000000000000)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.c0back)

        self.ctback = CustomSpinBox(self.frame)
        self.ctback.setObjectName("ctback")
        self.ctback.setEnabled(False)
        self.ctback.setDecimals(5)
        self.ctback.setMaximum(900.000000000000000)
        self.ctback.setSingleStep(0.050000000000000)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.ctback)

        self.verticalLayout_9.addWidget(self.frame)

        self.verticalSpacer_3 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_9.addItem(self.verticalSpacer_3)

        self.horizontalLayout_9.addWidget(self.widget_3)

        self.dmode_inputs.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName("page_2")
        sizePolicy4.setHeightForWidth(self.page_2.sizePolicy().hasHeightForWidth())
        self.page_2.setSizePolicy(sizePolicy4)
        self.horizontalLayout_10 = QHBoxLayout(self.page_2)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.widget_11 = QWidget(self.page_2)
        self.widget_11.setObjectName("widget_11")
        sizePolicy10.setHeightForWidth(self.widget_11.sizePolicy().hasHeightForWidth())
        self.widget_11.setSizePolicy(sizePolicy10)
        self.widget_11.setMinimumSize(QSize(263, 287))
        self.verticalLayout_11 = QVBoxLayout(self.widget_11)
        self.verticalLayout_11.setObjectName("verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 25, 0, 0)
        self.frame_2 = QFrame(self.widget_11)
        self.frame_2.setObjectName("frame_2")
        sizePolicy2.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy2)
        self.frame_2.setMinimumSize(QSize(284, 0))
        self.frame_2.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Shadow.Raised)
        self.formLayout_2 = QFormLayout(self.frame_2)
        self.formLayout_2.setObjectName("formLayout_2")
        self.formLayout_2.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.formLayout_2.setContentsMargins(-1, 0, -1, 6)
        self.label_9 = QLabel(self.frame_2)
        self.label_9.setObjectName("label_9")

        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.label_9)

        self.indComp_label = QLabel(self.frame_2)
        self.indComp_label.setObjectName("indComp_label")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.indComp_label)

        self.indComp = CustomComboBox(self.frame_2)
        self.indComp.setObjectName("indComp")

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.indComp)

        self.initialLog_label = QLabel(self.frame_2)
        self.initialLog_label.setObjectName("initialLog_label")
        sizePolicy10.setHeightForWidth(
            self.initialLog_label.sizePolicy().hasHeightForWidth()
        )
        self.initialLog_label.setSizePolicy(sizePolicy10)

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.initialLog_label)

        self.initialLog = CustomSpinBox(self.frame_2)
        self.initialLog.setObjectName("initialLog")
        self.initialLog.setDecimals(3)
        self.initialLog.setMaximum(900.000000000000000)
        self.initialLog.setSingleStep(0.050000000000000)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.initialLog)

        self.finalLog_label = QLabel(self.frame_2)
        self.finalLog_label.setObjectName("finalLog_label")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.finalLog_label)

        self.finalLog = CustomSpinBox(self.frame_2)
        self.finalLog.setObjectName("finalLog")
        self.finalLog.setDecimals(3)
        self.finalLog.setMaximum(900.000000000000000)
        self.finalLog.setSingleStep(0.050000000000000)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.finalLog)

        self.logInc_label = QLabel(self.frame_2)
        self.logInc_label.setObjectName("logInc_label")

        self.formLayout_2.setWidget(5, QFormLayout.LabelRole, self.logInc_label)

        self.logInc = CustomSpinBox(self.frame_2)
        self.logInc.setObjectName("logInc")
        self.logInc.setDecimals(3)
        self.logInc.setMaximum(900.000000000000000)
        self.logInc.setSingleStep(0.050000000000000)

        self.formLayout_2.setWidget(5, QFormLayout.FieldRole, self.logInc)

        self.line_3 = QFrame(self.frame_2)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(6, QFormLayout.SpanningRole, self.line_3)

        self.label_16 = QLabel(self.frame_2)
        self.label_16.setObjectName("label_16")

        self.formLayout_2.setWidget(7, QFormLayout.SpanningRole, self.label_16)

        self.cback_label = QLabel(self.frame_2)
        self.cback_label.setObjectName("cback_label")
        self.cback_label.setEnabled(False)

        self.formLayout_2.setWidget(8, QFormLayout.LabelRole, self.cback_label)

        self.cback = CustomSpinBox(self.frame_2)
        self.cback.setObjectName("cback")
        self.cback.setEnabled(False)
        self.cback.setDecimals(5)
        self.cback.setMaximum(900.000000000000000)
        self.cback.setSingleStep(0.050000000000000)

        self.formLayout_2.setWidget(8, QFormLayout.FieldRole, self.cback)

        self.checkBox = QCheckBox(self.frame_2)
        self.checkBox.setObjectName("checkBox")

        self.formLayout_2.setWidget(2, QFormLayout.SpanningRole, self.checkBox)

        self.verticalLayout_11.addWidget(self.frame_2)

        self.verticalSpacer_6 = QSpacerItem(
            20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )

        self.verticalLayout_11.addItem(self.verticalSpacer_6)

        self.horizontalLayout_10.addWidget(self.widget_11)

        self.dmode_inputs.addWidget(self.page_2)

        self.horizontalLayout_3.addWidget(self.dmode_inputs)

        self.widget = QWidget(self.dmode0Input)
        self.widget.setObjectName("widget")
        sizePolicy9.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy9)
        self.verticalLayout_4 = QVBoxLayout(self.widget)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.widget)
        self.label_2.setObjectName("label_2")

        self.verticalLayout_4.addWidget(self.label_2)

        self.concView = QTableView(self.widget)
        self.concView.setObjectName("concView")
        self.concView.setSizeAdjustPolicy(
            QAbstractScrollArea.SizeAdjustPolicy.AdjustToContents
        )

        self.verticalLayout_4.addWidget(self.concView)

        self.horizontalLayout_3.addWidget(self.widget)

        self.horizontalLayout_7.addWidget(self.dmode0Input)

        self.mode_views.addWidget(self.pyes_modes)
        self.bstac_modes = QWidget()
        self.bstac_modes.setObjectName("bstac_modes")
        self.verticalLayout_10 = QVBoxLayout(self.bstac_modes)
        self.verticalLayout_10.setSpacing(0)
        self.verticalLayout_10.setObjectName("verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.frame_3 = QFrame(self.bstac_modes)
        self.frame_3.setObjectName("frame_3")
        sizePolicy1.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy1)
        self.frame_3.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame_3.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_11 = QHBoxLayout(self.frame_3)
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.add_titration = QToolButton(self.frame_3)
        self.add_titration.setObjectName("add_titration")
        icon22 = QIcon()
        icon22.addFile(":/icons/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.add_titration.setIcon(icon22)
        self.add_titration.setIconSize(QSize(18, 18))
        self.add_titration.setAutoRaise(True)

        self.horizontalLayout_11.addWidget(self.add_titration)

        self.remove_titration = QToolButton(self.frame_3)
        self.remove_titration.setObjectName("remove_titration")
        icon23 = QIcon()
        icon23.addFile(":/icons/minus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.remove_titration.setIcon(icon23)
        self.remove_titration.setIconSize(QSize(18, 18))
        self.remove_titration.setAutoRaise(True)

        self.horizontalLayout_11.addWidget(self.remove_titration)

        self.horizontalSpacer_4 = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_11.addItem(self.horizontalSpacer_4)

        self.verticalLayout_10.addWidget(self.frame_3)

        self.horizontalLayout_13 = QHBoxLayout()
        self.horizontalLayout_13.setSpacing(10)
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.verticalLayout_13 = QVBoxLayout()
        self.verticalLayout_13.setSpacing(2)
        self.verticalLayout_13.setObjectName("verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(-1, 0, -1, -1)
        self.gridLayout_6 = QGridLayout()
        self.gridLayout_6.setObjectName("gridLayout_6")
        self.gridLayout_6.setContentsMargins(-1, 0, -1, -1)
        self.weightsModeLabel = QLabel(self.bstac_modes)
        self.weightsModeLabel.setObjectName("weightsModeLabel")

        self.gridLayout_6.addWidget(self.weightsModeLabel, 1, 0, 1, 1)

        self.optimizationOptionsLabel = QLabel(self.bstac_modes)
        self.optimizationOptionsLabel.setObjectName("optimizationOptionsLabel")

        self.gridLayout_6.addWidget(self.optimizationOptionsLabel, 0, 0, 1, 1)

        self.weightsMode = CustomComboBox(self.bstac_modes)
        self.weightsMode.addItem("")
        self.weightsMode.addItem("")
        self.weightsMode.addItem("")
        self.weightsMode.setObjectName("weightsMode")

        self.gridLayout_6.addWidget(self.weightsMode, 1, 1, 1, 1)

        self.verticalLayout_13.addLayout(self.gridLayout_6)

        self.paramstoRefineLabel = QLabel(self.bstac_modes)
        self.paramstoRefineLabel.setObjectName("paramstoRefineLabel")

        self.verticalLayout_13.addWidget(self.paramstoRefineLabel)

        self.gridLayout_3 = QGridLayout()
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.gridLayout_3.setContentsMargins(-1, -1, -1, 0)
        self.betaCheckAll = QToolButton(self.bstac_modes)
        self.betaCheckAll.setObjectName("betaCheckAll")
        self.betaCheckAll.setIcon(icon17)

        self.gridLayout_3.addWidget(self.betaCheckAll, 0, 1, 1, 1)

        self.betaToRefineLabel = QLabel(self.bstac_modes)
        self.betaToRefineLabel.setObjectName("betaToRefineLabel")

        self.gridLayout_3.addWidget(self.betaToRefineLabel, 0, 0, 1, 1)

        self.betaUncheckAll = QToolButton(self.bstac_modes)
        self.betaUncheckAll.setObjectName("betaUncheckAll")
        self.betaUncheckAll.setIcon(icon18)

        self.gridLayout_3.addWidget(self.betaUncheckAll, 0, 2, 1, 1)

        self.gridLayout_3.setColumnStretch(0, 1)

        self.verticalLayout_13.addLayout(self.gridLayout_3)

        self.betaToRefine = QListWidget(self.bstac_modes)
        __qlistwidgetitem = QListWidgetItem(self.betaToRefine)
        __qlistwidgetitem.setCheckState(Qt.Unchecked)
        __qlistwidgetitem.setFlags(
            Qt.ItemIsDragEnabled | Qt.ItemIsUserCheckable | Qt.ItemIsEnabled
        )
        self.betaToRefine.setObjectName("betaToRefine")

        self.verticalLayout_13.addWidget(self.betaToRefine)

        self.gridLayout_4 = QGridLayout()
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.gridLayout_4.setContentsMargins(-1, -1, -1, 0)
        self.concUncheckAll = QToolButton(self.bstac_modes)
        self.concUncheckAll.setObjectName("concUncheckAll")
        self.concUncheckAll.setIcon(icon18)

        self.gridLayout_4.addWidget(self.concUncheckAll, 0, 2, 1, 1)

        self.concCheckAll = QToolButton(self.bstac_modes)
        self.concCheckAll.setObjectName("concCheckAll")
        self.concCheckAll.setIcon(icon17)

        self.gridLayout_4.addWidget(self.concCheckAll, 0, 1, 1, 1)

        self.conToRefineLabel = QLabel(self.bstac_modes)
        self.conToRefineLabel.setObjectName("conToRefineLabel")

        self.gridLayout_4.addWidget(self.conToRefineLabel, 0, 0, 1, 1)

        self.gridLayout_4.setColumnStretch(0, 1)

        self.verticalLayout_13.addLayout(self.gridLayout_4)

        self.concToRefine = QTableWidget(self.bstac_modes)
        if self.concToRefine.columnCount() < 1:
            self.concToRefine.setColumnCount(1)
        if self.concToRefine.rowCount() < 1:
            self.concToRefine.setRowCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.concToRefine.setVerticalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setCheckState(Qt.Unchecked)
        self.concToRefine.setItem(0, 0, __qtablewidgetitem1)
        self.concToRefine.setObjectName("concToRefine")
        self.concToRefine.horizontalHeader().setCascadingSectionResizes(False)
        self.concToRefine.horizontalHeader().setDefaultSectionSize(25)

        self.verticalLayout_13.addWidget(self.concToRefine)

        self.gridLayout_5 = QGridLayout()
        self.gridLayout_5.setObjectName("gridLayout_5")
        self.gridLayout_5.setContentsMargins(-1, -1, -1, 0)
        self.electrodeUncheckAll = QToolButton(self.bstac_modes)
        self.electrodeUncheckAll.setObjectName("electrodeUncheckAll")
        self.electrodeUncheckAll.setIcon(icon18)

        self.gridLayout_5.addWidget(self.electrodeUncheckAll, 0, 2, 1, 1)

        self.electrodeCheckAll = QToolButton(self.bstac_modes)
        self.electrodeCheckAll.setObjectName("electrodeCheckAll")
        self.electrodeCheckAll.setIcon(icon17)

        self.gridLayout_5.addWidget(self.electrodeCheckAll, 0, 1, 1, 1)

        self.electrodeToRefineLabel = QLabel(self.bstac_modes)
        self.electrodeToRefineLabel.setObjectName("electrodeToRefineLabel")

        self.gridLayout_5.addWidget(self.electrodeToRefineLabel, 0, 0, 1, 1)

        self.gridLayout_5.setColumnStretch(0, 1)

        self.verticalLayout_13.addLayout(self.gridLayout_5)

        self.electrodeToRefine = QTableWidget(self.bstac_modes)
        if self.electrodeToRefine.columnCount() < 1:
            self.electrodeToRefine.setColumnCount(1)
        if self.electrodeToRefine.rowCount() < 5:
            self.electrodeToRefine.setRowCount(5)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.electrodeToRefine.setVerticalHeaderItem(0, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.electrodeToRefine.setVerticalHeaderItem(1, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.electrodeToRefine.setVerticalHeaderItem(2, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.electrodeToRefine.setVerticalHeaderItem(3, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        __qtablewidgetitem6.setCheckState(Qt.Unchecked)
        self.electrodeToRefine.setItem(0, 0, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        __qtablewidgetitem7.setCheckState(Qt.Unchecked)
        self.electrodeToRefine.setItem(1, 0, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        __qtablewidgetitem8.setCheckState(Qt.Unchecked)
        self.electrodeToRefine.setItem(2, 0, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        __qtablewidgetitem9.setCheckState(Qt.Unchecked)
        self.electrodeToRefine.setItem(3, 0, __qtablewidgetitem9)
        self.electrodeToRefine.setObjectName("electrodeToRefine")
        self.electrodeToRefine.setRowCount(5)
        self.electrodeToRefine.horizontalHeader().setDefaultSectionSize(25)

        self.verticalLayout_13.addWidget(self.electrodeToRefine)

        self.verticalLayout_13.setStretch(3, 2)
        self.verticalLayout_13.setStretch(5, 1)
        self.verticalLayout_13.setStretch(7, 1)

        self.horizontalLayout_13.addLayout(self.verticalLayout_13)

        self.titration_tabs = QTabWidget(self.bstac_modes)
        self.titration_tabs.setObjectName("titration_tabs")
        self.tab = QWidget()
        self.tab.setObjectName("tab")
        sizePolicy11 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy11.setHorizontalStretch(0)
        sizePolicy11.setVerticalStretch(0)
        sizePolicy11.setHeightForWidth(self.tab.sizePolicy().hasHeightForWidth())
        self.tab.setSizePolicy(sizePolicy11)
        self.horizontalLayout_12 = QHBoxLayout(self.tab)
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.titration_tabs.addTab(self.tab, "")

        self.horizontalLayout_13.addWidget(self.titration_tabs)

        self.horizontalLayout_13.setStretch(1, 1)

        self.verticalLayout_10.addLayout(self.horizontalLayout_13)

        self.mode_views.addWidget(self.bstac_modes)

        self.verticalLayout_7.addWidget(self.mode_views)

        self.tabWidget.addTab(self.Settings, "")
        self.Calc = QWidget()
        self.Calc.setObjectName("Calc")
        self.verticalLayout_2 = QVBoxLayout(self.Calc)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 5, 5, 5)
        self.debug = QCheckBox(self.Calc)
        self.debug.setObjectName("debug")

        self.verticalLayout_2.addWidget(self.debug)

        self.consoleOutput = QTextEdit(self.Calc)
        self.consoleOutput.setObjectName("consoleOutput")
        font = QFont()
        font.setFamilies(["Courier New"])
        font.setPointSize(11)
        self.consoleOutput.setFont(font)
        self.consoleOutput.setUndoRedoEnabled(False)
        self.consoleOutput.setLineWrapMode(QTextEdit.LineWrapMode.NoWrap)
        self.consoleOutput.setReadOnly(True)

        self.verticalLayout_2.addWidget(self.consoleOutput)

        self.calcButton = QPushButton(self.Calc)
        self.calcButton.setObjectName("calcButton")
        sizePolicy3.setHeightForWidth(self.calcButton.sizePolicy().hasHeightForWidth())
        self.calcButton.setSizePolicy(sizePolicy3)
        self.calcButton.setIcon(icon4)

        self.verticalLayout_2.addWidget(self.calcButton)

        self.widget_4 = QWidget(self.Calc)
        self.widget_4.setObjectName("widget_4")
        self.horizontalLayout_5 = QHBoxLayout(self.widget_4)
        self.horizontalLayout_5.setSpacing(5)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.exportButton = QPushButton(self.widget_4)
        self.exportButton.setObjectName("exportButton")
        self.exportButton.setEnabled(False)
        self.exportButton.setIcon(icon5)

        self.horizontalLayout_5.addWidget(self.exportButton)

        self.plotDistButton = QPushButton(self.widget_4)
        self.plotDistButton.setObjectName("plotDistButton")
        self.plotDistButton.setEnabled(False)
        self.plotDistButton.setIcon(icon6)

        self.horizontalLayout_5.addWidget(self.plotDistButton)

        self.verticalLayout_2.addWidget(self.widget_4)

        self.tabWidget.addTab(self.Calc, "")

        self.verticalLayout_5.addWidget(self.tabWidget)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName("menubar")
        self.menubar.setGeometry(QRect(0, 0, 1289, 43))
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuImport_Legacy = QMenu(self.menuFile)
        self.menuImport_Legacy.setObjectName("menuImport_Legacy")
        self.menuHelp = QMenu(self.menubar)
        self.menuHelp.setObjectName("menuHelp")
        self.menuEdit = QMenu(self.menubar)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.toolBar = QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        self.toolBar.setMovable(False)
        self.toolBar.setIconSize(QSize(18, 18))
        self.toolBar.setFloatable(False)
        MainWindow.addToolBar(Qt.ToolBarArea.TopToolBarArea, self.toolBar)

        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuHelp.menuAction())
        self.menuFile.addAction(self.actionNew)
        self.menuFile.addAction(self.actionOpen)
        self.menuFile.addAction(self.menuImport_Legacy.menuAction())
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSaveAs)
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionExit)
        self.menuImport_Legacy.addAction(self.actionBSTAC)
        self.menuHelp.addAction(self.actionWebsite)
        self.menuHelp.addSeparator()
        self.menuHelp.addAction(self.actionAbout)
        self.menuHelp.addAction(self.actionAbout_Qt)
        self.menuEdit.addAction(self.actionUndo)
        self.menuEdit.addAction(self.actionRedo)
        self.menuView.addAction(self.actionExport_Results)
        self.menuView.addAction(self.actionPlot_Results)
        self.menuView.addAction(self.actionMonitor_Results)
        self.toolBar.addAction(self.actionNew)
        self.toolBar.addAction(self.actionOpen)
        self.toolBar.addAction(self.actionSave)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionCalculate)
        self.toolBar.addAction(self.actionExport_Results)
        self.toolBar.addAction(self.actionPlot_Results)
        self.toolBar.addAction(self.actionMonitor_Results)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionAbout)

        self.retranslateUi(MainWindow)
        self.calcButton.clicked.connect(MainWindow.calculate)
        self.exportButton.clicked.connect(MainWindow.exportDist)
        self.plotDistButton.clicked.connect(MainWindow.plotDist)
        self.v0.valueChanged.connect(MainWindow.v0Updater)
        self.numComp.valueChanged.connect(MainWindow.updateComp)
        self.numSpecies.valueChanged.connect(MainWindow.updateSpecies)
        self.speciesView.clicked.connect(self.speciesView.edit)
        self.numPhases.valueChanged.connect(MainWindow.updateSolid)
        self.insert_above_species_button.clicked.connect(MainWindow.insertSpeciesAbove)
        self.insert_below_species_button.clicked.connect(MainWindow.insertSpeciesBelow)
        self.remove_species_button.clicked.connect(MainWindow.removeSpecies)
        self.move_up_species_button.clicked.connect(MainWindow.moveSpeciesUp)
        self.move_down_species_button.clicked.connect(MainWindow.moveSpeciesDown)
        self.insert_above_comp_button.clicked.connect(MainWindow.insertCompAbove)
        self.insert_below_comp_button.clicked.connect(MainWindow.insertCompBelow)
        self.remove_comp_button.clicked.connect(MainWindow.removeComp)
        self.move_up_comp_button.clicked.connect(MainWindow.moveCompUp)
        self.move_down_comp_button.clicked.connect(MainWindow.moveCompDown)
        self.uncertainty_info.clicked.connect(MainWindow.displayUncertaintyInfo)
        self.ionic_strength_info.clicked.connect(MainWindow.displayIonicStrengthInfo)
        self.edit_column_button.clicked.connect(MainWindow.massEditColumn)
        self.add_titration.clicked.connect(MainWindow.addTitration)
        self.remove_titration.clicked.connect(MainWindow.removeTitration)
        self.checkAllSpeciesButton.clicked.connect(MainWindow.checkAllSpecies)
        self.uncheckAllSpeciesButton.clicked.connect(MainWindow.uncheckAllSpecies)

        self.tabWidget.setCurrentIndex(1)
        self.tablesTab.setCurrentIndex(0)
        self.dmode.setCurrentIndex(0)
        self.mode_views.setCurrentIndex(1)
        self.dmode_inputs.setCurrentIndex(0)
        self.titration_tabs.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "PyES", None)
        )
        self.actionNew.setText(
            QCoreApplication.translate("MainWindow", "New Project", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionNew.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+N", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionOpen.setText(
            QCoreApplication.translate("MainWindow", "Open Project", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionOpen.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+O", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionSave.setText(
            QCoreApplication.translate("MainWindow", "Save Project", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionSave.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+S", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionAbout.setText(
            QCoreApplication.translate("MainWindow", "About PyES", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionAbout.setToolTip(
            QCoreApplication.translate("MainWindow", "About PyES", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionAbout.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+H", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionExit.setText(QCoreApplication.translate("MainWindow", "Exit", None))
        # if QT_CONFIG(shortcut)
        self.actionExit.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+Q", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionWebsite.setText(
            QCoreApplication.translate("MainWindow", "Website", None)
        )
        self.actionCalculate.setText(
            QCoreApplication.translate("MainWindow", "Calculate", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionCalculate.setToolTip(
            QCoreApplication.translate("MainWindow", "Launch the calculation", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionCalculate.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+R", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionExport_Results.setText(
            QCoreApplication.translate("MainWindow", "Export Results", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionExport_Results.setToolTip(
            QCoreApplication.translate("MainWindow", "Export Results", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionExport_Results.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+E", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionPlot_Results.setText(
            QCoreApplication.translate("MainWindow", "Plot Results", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionPlot_Results.setToolTip(
            QCoreApplication.translate("MainWindow", "Plot Results", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionPlot_Results.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+P", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionAbout_Qt.setText(
            QCoreApplication.translate("MainWindow", "About Qt", None)
        )
        self.actionUndo.setText(QCoreApplication.translate("MainWindow", "Undo", None))
        self.actionRedo.setText(QCoreApplication.translate("MainWindow", "Redo", None))
        self.actionSaveAs.setText(
            QCoreApplication.translate("MainWindow", "Save Project As...", None)
        )
        # if QT_CONFIG(tooltip)
        self.actionSaveAs.setToolTip(
            QCoreApplication.translate("MainWindow", "Save Project As...", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(shortcut)
        self.actionSaveAs.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+Shift+S", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.actionBSTAC.setText(
            QCoreApplication.translate("MainWindow", "BSTAC", None)
        )
        self.actionMonitor_Results.setText(
            QCoreApplication.translate("MainWindow", "Monitor Results", None)
        )
        # if QT_CONFIG(shortcut)
        self.actionMonitor_Results.setShortcut(
            QCoreApplication.translate("MainWindow", "Ctrl+M", None)
        )
        # endif // QT_CONFIG(shortcut)
        self.sys_opt_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-weight:600;">Options</span></p></body></html>',
                None,
            )
        )
        self.comp_label.setText(
            QCoreApplication.translate("MainWindow", "N\u00b0 Components", None)
        )
        # if QT_CONFIG(statustip)
        self.numComp.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Number of components present.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.species_label.setText(
            QCoreApplication.translate("MainWindow", "N\u00b0 Species", None)
        )
        # if QT_CONFIG(statustip)
        self.numSpecies.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Number of species to be considered.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.phases_label.setText(
            QCoreApplication.translate("MainWindow", "N\u00b0 Solid Species", None)
        )
        # if QT_CONFIG(statustip)
        self.numPhases.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Number of solid phases to be considered.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.ionic_strength_info.setText("")
        self.imode_label.setText(
            QCoreApplication.translate("MainWindow", "Ionic Strength", None)
        )
        self.imode.setItemText(
            0, QCoreApplication.translate("MainWindow", "Const.", None)
        )
        self.imode.setItemText(
            1, QCoreApplication.translate("MainWindow", "Var.", None)
        )

        # if QT_CONFIG(statustip)
        self.imode.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Constant/variable ionic strength.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.refIonicStr_label.setText(
            QCoreApplication.translate("MainWindow", "Ref. Ionic Strength", None)
        )
        # if QT_CONFIG(statustip)
        self.refIonicStr.setStatusTip(
            QCoreApplication.translate(
                "MainWindow",
                "Reference Ionic Strength to be used (if no other ionic strengths are being explicited).",
                None,
            )
        )
        # endif // QT_CONFIG(statustip)
        self.A_label.setText(QCoreApplication.translate("MainWindow", "A", None))
        # if QT_CONFIG(statustip)
        self.A.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", '"A" term of the Debye-H\u00fcckel equation.', None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.B_label.setText(QCoreApplication.translate("MainWindow", "B", None))
        # if QT_CONFIG(statustip)
        self.B.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", '"B" term of the Debye-H\u00fcckel equation.', None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.c0_label.setText(QCoreApplication.translate("MainWindow", "c0", None))
        # if QT_CONFIG(statustip)
        self.c0.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", '"c0" term of the Debye-H\u00fcckel equation.', None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.c1_label.setText(QCoreApplication.translate("MainWindow", "c1", None))
        # if QT_CONFIG(statustip)
        self.c1.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", '"c1" term of the Debye-H\u00fcckel equation.', None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.d0_label.setText(QCoreApplication.translate("MainWindow", "d0", None))
        # if QT_CONFIG(statustip)
        self.d0.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", '"d0" term of the Debye-H\u00fcckel equation.', None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.d1_label.setText(QCoreApplication.translate("MainWindow", "d1", None))
        # if QT_CONFIG(statustip)
        self.d1.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", '"d1" term of the Debye-H\u00fcckel equation.', None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.e0_label.setText(QCoreApplication.translate("MainWindow", "e0", None))
        # if QT_CONFIG(statustip)
        self.e0.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", '"e0" term of the Debye-H\u00fcckel equation.', None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.e1_label.setText(QCoreApplication.translate("MainWindow", "e1", None))
        # if QT_CONFIG(statustip)
        self.e1.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", '"e1" term of the Debye-H\u00fcckel equation.', None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.uncertainty_info.setText("")
        self.uncertaintyMode.setText(
            QCoreApplication.translate("MainWindow", "Uncertainty Estimation", None)
        )
        self.tab_comp_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-weight:600;">Components</span></p></body></html>',
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.insert_above_comp_button.setToolTip(
            QCoreApplication.translate("MainWindow", "Add Component Above", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.insert_above_comp_button.setStatusTip(
            QCoreApplication.translate("MainWindow", "Add Component Above", None)
        )
        # endif // QT_CONFIG(statustip)
        self.insert_above_comp_button.setText("")
        # if QT_CONFIG(tooltip)
        self.insert_below_comp_button.setToolTip(
            QCoreApplication.translate("MainWindow", "Add Component Below", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.insert_below_comp_button.setStatusTip(
            QCoreApplication.translate("MainWindow", "Add Component Below", None)
        )
        # endif // QT_CONFIG(statustip)
        self.insert_below_comp_button.setText("")
        # if QT_CONFIG(tooltip)
        self.remove_comp_button.setToolTip(
            QCoreApplication.translate("MainWindow", "Remove Component", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.remove_comp_button.setStatusTip(
            QCoreApplication.translate("MainWindow", "Remove Component", None)
        )
        # endif // QT_CONFIG(statustip)
        self.remove_comp_button.setText("")
        # if QT_CONFIG(tooltip)
        self.move_up_comp_button.setToolTip(
            QCoreApplication.translate("MainWindow", "Move Component Up", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.move_up_comp_button.setStatusTip(
            QCoreApplication.translate("MainWindow", "Move Component Up", None)
        )
        # endif // QT_CONFIG(statustip)
        self.move_up_comp_button.setText("")
        # if QT_CONFIG(tooltip)
        self.move_down_comp_button.setToolTip(
            QCoreApplication.translate("MainWindow", "Move Component Down", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.move_down_comp_button.setStatusTip(
            QCoreApplication.translate("MainWindow", "Move Component Down", None)
        )
        # endif // QT_CONFIG(statustip)
        self.move_down_comp_button.setText("")
        self.tab_comp_label_2.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-weight:600;">Species</span></p></body></html>',
                None,
            )
        )
        # if QT_CONFIG(tooltip)
        self.checkAllSpeciesButton.setToolTip(
            QCoreApplication.translate("MainWindow", "Ignore all species", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.checkAllSpeciesButton.setStatusTip(
            QCoreApplication.translate("MainWindow", "Ignore all species", None)
        )
        # endif // QT_CONFIG(statustip)
        # if QT_CONFIG(tooltip)
        self.uncheckAllSpeciesButton.setToolTip(
            QCoreApplication.translate("MainWindow", "Consider all species", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.uncheckAllSpeciesButton.setStatusTip(
            QCoreApplication.translate("MainWindow", "Consider all species", None)
        )
        # endif // QT_CONFIG(statustip)
        self.uncheckAllSpeciesButton.setText("")
        # if QT_CONFIG(tooltip)
        self.insert_above_species_button.setToolTip(
            QCoreApplication.translate("MainWindow", "Add Species Above", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.insert_above_species_button.setStatusTip(
            QCoreApplication.translate("MainWindow", "Add Species Above", None)
        )
        # endif // QT_CONFIG(statustip)
        self.insert_above_species_button.setText("")
        # if QT_CONFIG(tooltip)
        self.insert_below_species_button.setToolTip(
            QCoreApplication.translate("MainWindow", "Add Species Below", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.insert_below_species_button.setStatusTip(
            QCoreApplication.translate("MainWindow", "Add Species Below", None)
        )
        # endif // QT_CONFIG(statustip)
        self.insert_below_species_button.setText("")
        # if QT_CONFIG(tooltip)
        self.remove_species_button.setToolTip(
            QCoreApplication.translate("MainWindow", "Remove Species", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.remove_species_button.setStatusTip(
            QCoreApplication.translate("MainWindow", "Remove Species", None)
        )
        # endif // QT_CONFIG(statustip)
        self.remove_species_button.setText("")
        # if QT_CONFIG(tooltip)
        self.move_up_species_button.setToolTip(
            QCoreApplication.translate("MainWindow", "Move Species Up", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.move_up_species_button.setStatusTip(
            QCoreApplication.translate("MainWindow", "Move Species Up", None)
        )
        # endif // QT_CONFIG(statustip)
        self.move_up_species_button.setText("")
        # if QT_CONFIG(tooltip)
        self.move_down_species_button.setToolTip(
            QCoreApplication.translate("MainWindow", "Move Species Down", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.move_down_species_button.setStatusTip(
            QCoreApplication.translate("MainWindow", "Move Species Down", None)
        )
        # endif // QT_CONFIG(statustip)
        self.move_down_species_button.setText("")
        # if QT_CONFIG(tooltip)
        self.edit_column_button.setToolTip(
            QCoreApplication.translate("MainWindow", "Edit whole column", None)
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.edit_column_button.setStatusTip(
            QCoreApplication.translate("MainWindow", "Edit whole column", None)
        )
        # endif // QT_CONFIG(statustip)
        self.edit_column_button.setText("")
        self.tablesTab.setTabText(
            self.tablesTab.indexOf(self.species),
            QCoreApplication.translate("MainWindow", "Solution Species", None),
        )
        self.tablesTab.setTabText(
            self.tablesTab.indexOf(self.solidspecies),
            QCoreApplication.translate("MainWindow", "Solid Species", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.Species),
            QCoreApplication.translate("MainWindow", "Species", None),
        )
        self.dmode_label.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-weight:600;">Work Mode:</span></p></body></html>',
                None,
            )
        )
        self.dmode.setItemText(
            0, QCoreApplication.translate("MainWindow", "Titration", None)
        )
        self.dmode.setItemText(
            1, QCoreApplication.translate("MainWindow", "Distribution", None)
        )
        self.dmode.setItemText(
            2, QCoreApplication.translate("MainWindow", "Refine Potentiometric", None)
        )

        # if QT_CONFIG(statustip)
        self.dmode.setStatusTip(
            QCoreApplication.translate("MainWindow", "Select operation mode.", None)
        )
        # endif // QT_CONFIG(statustip)
        self.label_3.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-weight:600;">Volume Settings:</span></p></body></html>',
                None,
            )
        )
        self.v0_label.setText(
            QCoreApplication.translate("MainWindow", "Initial Volume:", None)
        )
        # if QT_CONFIG(statustip)
        self.v0.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Initial volume in the titration vessel.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.v0.setSuffix(QCoreApplication.translate("MainWindow", " ml", None))
        self.initv_label.setText(
            QCoreApplication.translate("MainWindow", "First Point Volume:", None)
        )
        # if QT_CONFIG(statustip)
        self.initv.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Volume in the vessel at the first titration point.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.initv.setSuffix(QCoreApplication.translate("MainWindow", " ml", None))
        self.vinc_label.setText(
            QCoreApplication.translate("MainWindow", "Volume Increments:", None)
        )
        # if QT_CONFIG(statustip)
        self.vinc.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Increment in volume for each titration point.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.vinc.setSuffix(QCoreApplication.translate("MainWindow", " ml", None))
        self.nop_label.setText(
            QCoreApplication.translate("MainWindow", "Number of points:", None)
        )
        # if QT_CONFIG(statustip)
        self.nop.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Number of titration points.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.nop.setSuffix("")
        self.label_4.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-weight:600;">Background Ions Settings:</span></p></body></html>',
                None,
            )
        )
        self.c0back_label.setText(
            QCoreApplication.translate("MainWindow", "Initial C:", None)
        )
        self.ctback_label.setText(
            QCoreApplication.translate("MainWindow", "Titrant C:", None)
        )
        # if QT_CONFIG(statustip)
        self.c0back.setStatusTip(
            QCoreApplication.translate(
                "MainWindow",
                "Initial concentration of background ions in titration vessel.",
                None,
            )
        )
        # endif // QT_CONFIG(statustip)
        self.c0back.setSuffix(QCoreApplication.translate("MainWindow", " mol/l", None))
        # if QT_CONFIG(statustip)
        self.ctback.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Concentration of background ions in the titrant.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.ctback.setSuffix(QCoreApplication.translate("MainWindow", " mol/l", None))
        self.label_9.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-weight:600;">Indipendent Component Settings:</span></p></body></html>',
                None,
            )
        )
        self.indComp_label.setText(
            QCoreApplication.translate("MainWindow", "Indipendent Comp:", None)
        )
        # if QT_CONFIG(statustip)
        self.indComp.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Component to be considered indipendent.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.initialLog_label.setText(
            QCoreApplication.translate("MainWindow", "Initial -log[A]:", None)
        )
        # if QT_CONFIG(statustip)
        self.initialLog.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Initial Log value of the indipendent component.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.finalLog_label.setText(
            QCoreApplication.translate("MainWindow", "Final -log[A]", None)
        )
        # if QT_CONFIG(statustip)
        self.finalLog.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Final Log value of the indipendent component.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.logInc_label.setText(
            QCoreApplication.translate("MainWindow", "-log[A] Increment:", None)
        )
        # if QT_CONFIG(statustip)
        self.logInc.setStatusTip(
            QCoreApplication.translate(
                "MainWindow",
                "Log increment of the indipendent component at each point.",
                None,
            )
        )
        # endif // QT_CONFIG(statustip)
        self.label_16.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-weight:600;">Background Ions Settings:</span></p></body></html>',
                None,
            )
        )
        self.cback_label.setText(
            QCoreApplication.translate("MainWindow", "Concentration:", None)
        )
        # if QT_CONFIG(tooltip)
        self.cback.setToolTip(
            QCoreApplication.translate(
                "MainWindow",
                "Sum of the concentrations of ionic species that do not take part in the reactions.",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.cback.setStatusTip(
            QCoreApplication.translate(
                "MainWindow",
                "Sum of the concentrations of ionic species that do not take part in the reactions.",
                None,
            )
        )
        # endif // QT_CONFIG(statustip)
        self.cback.setSuffix(QCoreApplication.translate("MainWindow", " mol/l", None))
        self.checkBox.setText(
            QCoreApplication.translate("MainWindow", "Total Concentration Mode", None)
        )
        self.label_2.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-weight:600;">Analytical Concentrations:</span></p></body></html>',
                None,
            )
        )
        self.add_titration.setText("")
        self.remove_titration.setText("")
        self.weightsModeLabel.setText(
            QCoreApplication.translate("MainWindow", "Weights", None)
        )
        self.optimizationOptionsLabel.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-weight:700;">Optimization Options:</span></p></body></html>',
                None,
            )
        )
        self.weightsMode.setItemText(
            0, QCoreApplication.translate("MainWindow", "Constants", None)
        )
        self.weightsMode.setItemText(
            1, QCoreApplication.translate("MainWindow", "Calculated", None)
        )
        self.weightsMode.setItemText(
            2, QCoreApplication.translate("MainWindow", "Given", None)
        )

        self.paramstoRefineLabel.setText(
            QCoreApplication.translate(
                "MainWindow",
                '<html><head/><body><p><span style=" font-weight:700;">Parameters to refine</span></p></body></html>',
                None,
            )
        )
        self.betaCheckAll.setText("")
        self.betaToRefineLabel.setText(
            QCoreApplication.translate("MainWindow", "Constants", None)
        )

        __sortingEnabled = self.betaToRefine.isSortingEnabled()
        self.betaToRefine.setSortingEnabled(False)
        self.betaToRefine.setSortingEnabled(__sortingEnabled)

        self.concCheckAll.setText("")
        self.conToRefineLabel.setText(
            QCoreApplication.translate("MainWindow", "Concentrations", None)
        )
        ___qtablewidgetitem = self.concToRefine.verticalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", "A", None))
        __sortingEnabled1 = self.concToRefine.isSortingEnabled()
        self.concToRefine.setSortingEnabled(False)
        self.concToRefine.setSortingEnabled(__sortingEnabled1)

        self.electrodeCheckAll.setText("")
        self.electrodeToRefineLabel.setText(
            QCoreApplication.translate("MainWindow", "Electrode", None)
        )
        ___qtablewidgetitem1 = self.electrodeToRefine.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(
            QCoreApplication.translate("MainWindow", "E0", None)
        )
        ___qtablewidgetitem2 = self.electrodeToRefine.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(
            QCoreApplication.translate("MainWindow", "Ja", None)
        )
        ___qtablewidgetitem3 = self.electrodeToRefine.verticalHeaderItem(2)
        ___qtablewidgetitem3.setText(
            QCoreApplication.translate("MainWindow", "Jb", None)
        )
        ___qtablewidgetitem4 = self.electrodeToRefine.verticalHeaderItem(3)
        ___qtablewidgetitem4.setText(
            QCoreApplication.translate("MainWindow", "Slope", None)
        )
        __sortingEnabled2 = self.electrodeToRefine.isSortingEnabled()
        self.electrodeToRefine.setSortingEnabled(False)
        self.electrodeToRefine.setSortingEnabled(__sortingEnabled2)

        self.titration_tabs.setTabText(
            self.titration_tabs.indexOf(self.tab),
            QCoreApplication.translate("MainWindow", "1", None),
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.Settings),
            QCoreApplication.translate("MainWindow", "Settings", None),
        )
        # if QT_CONFIG(statustip)
        self.debug.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Create a Debug Log to file.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.debug.setText(
            QCoreApplication.translate("MainWindow", "Debug to file", None)
        )
        # if QT_CONFIG(statustip)
        self.calcButton.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Launch the calculation routine.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.calcButton.setText(
            QCoreApplication.translate("MainWindow", "Calculate", None)
        )
        # if QT_CONFIG(statustip)
        self.exportButton.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Export the results in various formats.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.exportButton.setText(
            QCoreApplication.translate("MainWindow", "Export Results", None)
        )
        # if QT_CONFIG(statustip)
        self.plotDistButton.setStatusTip(
            QCoreApplication.translate(
                "MainWindow", "Plot the results and export the graphs.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.plotDistButton.setText(
            QCoreApplication.translate("MainWindow", "Plot Results", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.Calc),
            QCoreApplication.translate("MainWindow", "Calculate", None),
        )
        self.menuFile.setTitle(QCoreApplication.translate("MainWindow", "File", None))
        self.menuImport_Legacy.setTitle(
            QCoreApplication.translate("MainWindow", "Import Legacy", None)
        )
        self.menuHelp.setTitle(QCoreApplication.translate("MainWindow", "?", None))
        self.menuEdit.setTitle(QCoreApplication.translate("MainWindow", "Edit", None))
        self.menuView.setTitle(QCoreApplication.translate("MainWindow", "View", None))
        self.toolBar.setWindowTitle(
            QCoreApplication.translate("MainWindow", "toolBar", None)
        )

    # retranslateUi
