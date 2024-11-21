# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_pyqtgraphPlotExport.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from pyqtgraph import PlotWidget
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
    QApplication,
    QCheckBox,
    QComboBox,
    QFormLayout,
    QFrame,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLayout,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QTableView,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from ui.widgets import ColorButton


class Ui_PlotWindow(object):
    def setupUi(self, PlotWindow):
        if not PlotWindow.objectName():
            PlotWindow.setObjectName("PlotWindow")
        PlotWindow.resize(919, 619)
        PlotWindow.setMinimumSize(QSize(800, 600))
        self.centralwidget = QWidget(PlotWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 5, 2, 2)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName("widget")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(2, 0, 2, 2)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName("widget_2")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(5)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.filter = QPushButton(self.widget_2)
        self.filter.setObjectName("filter")

        self.gridLayout.addWidget(self.filter, 3, 0, 1, 2)

        self.errors_check = QCheckBox(self.widget_2)
        self.errors_check.setObjectName("errors_check")

        self.gridLayout.addWidget(self.errors_check, 8, 0, 1, 2)

        self.textSize = QSpinBox(self.widget_2)
        self.textSize.setObjectName("textSize")
        self.textSize.setMinimum(1)
        self.textSize.setValue(10)

        self.gridLayout.addWidget(self.textSize, 10, 1, 1, 1)

        self.select_all = QPushButton(self.widget_2)
        self.select_all.setObjectName("select_all")

        self.gridLayout.addWidget(self.select_all, 1, 1, 1, 1)

        self.lineWidth = QSpinBox(self.widget_2)
        self.lineWidth.setObjectName("lineWidth")
        self.lineWidth.setMinimum(1)
        self.lineWidth.setValue(2)

        self.gridLayout.addWidget(self.lineWidth, 11, 1, 1, 1)

        self.tabWidget_2 = QTabWidget(self.widget_2)
        self.tabWidget_2.setObjectName("tabWidget_2")
        self.tabWidget_2.setEnabled(True)
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy1)
        self.tabWidget_2.setMouseTracking(False)
        self.species = QWidget()
        self.species.setObjectName("species")
        self.horizontalLayout_4 = QHBoxLayout(self.species)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.speciesView = QTableView(self.species)
        self.speciesView.setObjectName("speciesView")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.speciesView.sizePolicy().hasHeightForWidth())
        self.speciesView.setSizePolicy(sizePolicy2)
        self.speciesView.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.speciesView.setAlternatingRowColors(True)
        self.speciesView.horizontalHeader().setVisible(False)

        self.horizontalLayout_4.addWidget(self.speciesView)

        self.tabWidget_2.addTab(self.species, "")
        self.solids = QWidget()
        self.solids.setObjectName("solids")
        self.horizontalLayout_3 = QHBoxLayout(self.solids)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.solidsView = QTableView(self.solids)
        self.solidsView.setObjectName("solidsView")
        sizePolicy2.setHeightForWidth(self.solidsView.sizePolicy().hasHeightForWidth())
        self.solidsView.setSizePolicy(sizePolicy2)
        self.solidsView.setEditTriggers(QAbstractItemView.EditTrigger.AllEditTriggers)
        self.solidsView.setAlternatingRowColors(True)
        self.solidsView.horizontalHeader().setVisible(False)

        self.horizontalLayout_3.addWidget(self.solidsView)

        self.tabWidget_2.addTab(self.solids, "")

        self.gridLayout.addWidget(self.tabWidget_2, 0, 0, 1, 2)

        self.deselect_all = QPushButton(self.widget_2)
        self.deselect_all.setObjectName("deselect_all")

        self.gridLayout.addWidget(self.deselect_all, 1, 0, 1, 1)

        self.lineWidth_label = QLabel(self.widget_2)
        self.lineWidth_label.setObjectName("lineWidth_label")

        self.gridLayout.addWidget(self.lineWidth_label, 11, 0, 1, 1)

        self.plot_options_label = QLabel(self.widget_2)
        self.plot_options_label.setObjectName("plot_options_label")

        self.gridLayout.addWidget(self.plot_options_label, 5, 0, 1, 2)

        self.regions_check = QCheckBox(self.widget_2)
        self.regions_check.setObjectName("regions_check")

        self.gridLayout.addWidget(self.regions_check, 7, 0, 1, 2)

        self.monochrome_color = ColorButton(self.widget_2)
        self.monochrome_color.setObjectName("monochrome_color")

        self.gridLayout.addWidget(self.monochrome_color, 6, 1, 1, 1)

        self.v_unit = QComboBox(self.widget_2)
        self.v_unit.addItem("")
        self.v_unit.addItem("")
        self.v_unit.setObjectName("v_unit")

        self.gridLayout.addWidget(self.v_unit, 13, 1, 1, 1)

        self.c_unit_label = QLabel(self.widget_2)
        self.c_unit_label.setObjectName("c_unit_label")

        self.gridLayout.addWidget(self.c_unit_label, 12, 0, 1, 1)

        self.line = QFrame(self.widget_2)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 4, 0, 1, 2)

        self.c_unit = QComboBox(self.widget_2)
        self.c_unit.addItem("")
        self.c_unit.addItem("")
        self.c_unit.addItem("")
        self.c_unit.setObjectName("c_unit")

        self.gridLayout.addWidget(self.c_unit, 12, 1, 1, 1)

        self.v_unit_label = QLabel(self.widget_2)
        self.v_unit_label.setObjectName("v_unit_label")

        self.gridLayout.addWidget(self.v_unit_label, 13, 0, 1, 1)

        self.textSize_label = QLabel(self.widget_2)
        self.textSize_label.setObjectName("textSize_label")

        self.gridLayout.addWidget(self.textSize_label, 10, 0, 1, 1)

        self.monochrome_check = QCheckBox(self.widget_2)
        self.monochrome_check.setObjectName("monochrome_check")

        self.gridLayout.addWidget(self.monochrome_check, 6, 0, 1, 1)

        self.hide_legend_check = QCheckBox(self.widget_2)
        self.hide_legend_check.setObjectName("hide_legend_check")

        self.gridLayout.addWidget(self.hide_legend_check, 9, 0, 1, 2)

        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout.addWidget(self.widget_2)

        self.horizontalLayout.addWidget(self.widget)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(7)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.titrationSelector = QComboBox(self.centralwidget)
        self.titrationSelector.setObjectName("titrationSelector")
        font = QFont()
        font.setFamilies([".AppleSystemUIFont"])
        self.titrationSelector.setFont(font)

        self.verticalLayout_4.addWidget(self.titrationSelector)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.conc_tab = QWidget()
        self.conc_tab.setObjectName("conc_tab")
        self.horizontalLayout_2 = QHBoxLayout(self.conc_tab)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.conc_graph = PlotWidget(self.conc_tab)
        self.conc_graph.setObjectName("conc_graph")

        self.horizontalLayout_2.addWidget(self.conc_graph)

        self.tabWidget.addTab(self.conc_tab, "")
        self.perc_tab = QWidget()
        self.perc_tab.setObjectName("perc_tab")
        self.verticalLayout_2 = QVBoxLayout(self.perc_tab)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.perc_graph = PlotWidget(self.perc_tab)
        self.perc_graph.setObjectName("perc_graph")

        self.verticalLayout_2.addWidget(self.perc_graph)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName("formLayout_2")
        self.formLayout_2.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.componentComboBox_perc = QComboBox(self.perc_tab)
        self.componentComboBox_perc.setObjectName("componentComboBox_perc")

        self.formLayout_2.setWidget(
            0, QFormLayout.FieldRole, self.componentComboBox_perc
        )

        self.componentLabel_2 = QLabel(self.perc_tab)
        self.componentLabel_2.setObjectName("componentLabel_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.componentLabel_2)

        self.verticalLayout_2.addLayout(self.formLayout_2)

        self.verticalLayout_2.setStretch(0, 1)
        self.tabWidget.addTab(self.perc_tab, "")
        self.titration_tab = QWidget()
        self.titration_tab.setObjectName("titration_tab")
        self.verticalLayout_3 = QVBoxLayout(self.titration_tab)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.titration_graph = PlotWidget(self.titration_tab)
        self.titration_graph.setObjectName("titration_graph")
        sizePolicy3 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred
        )
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(
            self.titration_graph.sizePolicy().hasHeightForWidth()
        )
        self.titration_graph.setSizePolicy(sizePolicy3)

        self.verticalLayout_3.addWidget(self.titration_graph)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setSizeConstraint(QLayout.SizeConstraint.SetDefaultConstraint)
        self.componentLabel = QLabel(self.titration_tab)
        self.componentLabel.setObjectName("componentLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.componentLabel)

        self.componentComboBox = QComboBox(self.titration_tab)
        self.componentComboBox.setObjectName("componentComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.componentComboBox)

        self.verticalLayout_3.addLayout(self.formLayout)

        self.verticalLayout_3.setStretch(0, 1)
        self.tabWidget.addTab(self.titration_tab, "")

        self.verticalLayout_4.addWidget(self.tabWidget)

        self.exportButton = QPushButton(self.centralwidget)
        self.exportButton.setObjectName("exportButton")

        self.verticalLayout_4.addWidget(self.exportButton)

        self.horizontalLayout.addLayout(self.verticalLayout_4)

        self.horizontalLayout.setStretch(1, 1)
        PlotWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(PlotWindow)
        self.deselect_all.clicked.connect(PlotWindow.deselectAll)
        self.select_all.clicked.connect(PlotWindow.selectAll)
        self.filter.clicked.connect(PlotWindow.filterSpecies)
        self.regions_check.clicked.connect(PlotWindow.changeSolidsGraphics)
        self.errors_check.clicked.connect(PlotWindow.changeErrorsGraphics)

        self.tabWidget_2.setCurrentIndex(0)
        self.tabWidget.setCurrentIndex(0)

        QMetaObject.connectSlotsByName(PlotWindow)

    # setupUi

    def retranslateUi(self, PlotWindow):
        PlotWindow.setWindowTitle(
            QCoreApplication.translate("PlotWindow", "Export Plot", None)
        )
        self.filter.setText(QCoreApplication.translate("PlotWindow", "Filter", None))
        self.errors_check.setText(
            QCoreApplication.translate("PlotWindow", "Plot error bars", None)
        )
        self.select_all.setText(
            QCoreApplication.translate("PlotWindow", "Select All", None)
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.species),
            QCoreApplication.translate("PlotWindow", "Species", None),
        )
        self.tabWidget_2.setTabText(
            self.tabWidget_2.indexOf(self.solids),
            QCoreApplication.translate("PlotWindow", "Solids", None),
        )
        self.deselect_all.setText(
            QCoreApplication.translate("PlotWindow", "Deselect All", None)
        )
        self.lineWidth_label.setText(
            QCoreApplication.translate("PlotWindow", "Line width", None)
        )
        self.plot_options_label.setText(
            QCoreApplication.translate(
                "PlotWindow",
                '<html><head/><body><p><span style=" font-weight:700;">Plot Options</span></p></body></html>',
                None,
            )
        )
        self.regions_check.setText(
            QCoreApplication.translate("PlotWindow", "Solids as regions", None)
        )
        self.monochrome_color.setText("")
        self.v_unit.setItemText(0, QCoreApplication.translate("PlotWindow", "ml", None))
        self.v_unit.setItemText(1, QCoreApplication.translate("PlotWindow", "l", None))

        self.c_unit_label.setText(
            QCoreApplication.translate("PlotWindow", "Concentration Units", None)
        )
        self.c_unit.setItemText(
            0, QCoreApplication.translate("PlotWindow", "mol/l", None)
        )
        self.c_unit.setItemText(
            1, QCoreApplication.translate("PlotWindow", "mmol/l", None)
        )
        self.c_unit.setItemText(
            2, QCoreApplication.translate("PlotWindow", "\u03bcmol/l", None)
        )

        self.v_unit_label.setText(
            QCoreApplication.translate("PlotWindow", "Volume Units", None)
        )
        self.textSize_label.setText(
            QCoreApplication.translate("PlotWindow", "Text size", None)
        )
        self.monochrome_check.setText(
            QCoreApplication.translate("PlotWindow", "Monochrome", None)
        )
        self.hide_legend_check.setText(
            QCoreApplication.translate("PlotWindow", "Hide legend", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.conc_tab),
            QCoreApplication.translate("PlotWindow", "Concentrations", None),
        )
        self.componentLabel_2.setText(
            QCoreApplication.translate("PlotWindow", "Component:", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.perc_tab),
            QCoreApplication.translate("PlotWindow", "Percentages", None),
        )
        self.componentLabel.setText(
            QCoreApplication.translate("PlotWindow", "Component:", None)
        )
        self.tabWidget.setTabText(
            self.tabWidget.indexOf(self.titration_tab),
            QCoreApplication.translate("PlotWindow", "Titration Curve", None),
        )
        self.exportButton.setText(
            QCoreApplication.translate("PlotWindow", "Export Graph", None)
        )

    # retranslateUi
