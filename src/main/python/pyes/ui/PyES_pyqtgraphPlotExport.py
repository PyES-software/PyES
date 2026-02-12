# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_pyqtgraphPlotExport.ui'
##
## Created by: Qt User Interface Compiler version 6.8.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QCheckBox, QComboBox,
    QFormLayout, QFrame, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QMainWindow,
    QPushButton, QSizePolicy, QSpinBox, QTabWidget,
    QTableView, QVBoxLayout, QWidget)

from pyqtgraph import PlotWidget
from ui.widgets import ColorButton

class Ui_PlotWindow(object):
    def setupUi(self, PlotWindow):
        if not PlotWindow.objectName():
            PlotWindow.setObjectName(u"PlotWindow")
        PlotWindow.resize(919, 619)
        PlotWindow.setMinimumSize(QSize(800, 600))
        self.centralwidget = QWidget(PlotWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(2, 5, 2, 2)
        self.widget = QWidget(self.centralwidget)
        self.widget.setObjectName(u"widget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy)
        self.verticalLayout = QVBoxLayout(self.widget)
        self.verticalLayout.setSpacing(2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(2, 0, 2, 2)
        self.widget_2 = QWidget(self.widget)
        self.widget_2.setObjectName(u"widget_2")
        self.gridLayout = QGridLayout(self.widget_2)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setHorizontalSpacing(2)
        self.gridLayout.setVerticalSpacing(5)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.filter = QPushButton(self.widget_2)
        self.filter.setObjectName(u"filter")

        self.gridLayout.addWidget(self.filter, 3, 0, 1, 2)

        self.errors_check = QCheckBox(self.widget_2)
        self.errors_check.setObjectName(u"errors_check")

        self.gridLayout.addWidget(self.errors_check, 8, 0, 1, 2)

        self.textSize = QSpinBox(self.widget_2)
        self.textSize.setObjectName(u"textSize")
        self.textSize.setMinimum(1)
        self.textSize.setValue(10)

        self.gridLayout.addWidget(self.textSize, 10, 1, 1, 1)

        self.select_all = QPushButton(self.widget_2)
        self.select_all.setObjectName(u"select_all")

        self.gridLayout.addWidget(self.select_all, 1, 1, 1, 1)

        self.lineWidth = QSpinBox(self.widget_2)
        self.lineWidth.setObjectName(u"lineWidth")
        self.lineWidth.setMinimum(1)
        self.lineWidth.setValue(2)

        self.gridLayout.addWidget(self.lineWidth, 11, 1, 1, 1)

        self.tabWidget_2 = QTabWidget(self.widget_2)
        self.tabWidget_2.setObjectName(u"tabWidget_2")
        self.tabWidget_2.setEnabled(True)
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.tabWidget_2.sizePolicy().hasHeightForWidth())
        self.tabWidget_2.setSizePolicy(sizePolicy1)
        self.tabWidget_2.setMouseTracking(False)
        self.species = QWidget()
        self.species.setObjectName(u"species")
        self.horizontalLayout_4 = QHBoxLayout(self.species)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(2, 2, 2, 2)
        self.speciesView = QTableView(self.species)
        self.speciesView.setObjectName(u"speciesView")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.speciesView.sizePolicy().hasHeightForWidth())
        self.speciesView.setSizePolicy(sizePolicy2)
        self.speciesView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.speciesView.setAlternatingRowColors(True)
        self.speciesView.horizontalHeader().setVisible(False)

        self.horizontalLayout_4.addWidget(self.speciesView)

        self.tabWidget_2.addTab(self.species, "")
        self.solids = QWidget()
        self.solids.setObjectName(u"solids")
        self.horizontalLayout_3 = QHBoxLayout(self.solids)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(2, 2, 2, 2)
        self.solidsView = QTableView(self.solids)
        self.solidsView.setObjectName(u"solidsView")
        sizePolicy2.setHeightForWidth(self.solidsView.sizePolicy().hasHeightForWidth())
        self.solidsView.setSizePolicy(sizePolicy2)
        self.solidsView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.solidsView.setAlternatingRowColors(True)
        self.solidsView.horizontalHeader().setVisible(False)

        self.horizontalLayout_3.addWidget(self.solidsView)

        self.tabWidget_2.addTab(self.solids, "")

        self.gridLayout.addWidget(self.tabWidget_2, 0, 0, 1, 2)

        self.deselect_all = QPushButton(self.widget_2)
        self.deselect_all.setObjectName(u"deselect_all")

        self.gridLayout.addWidget(self.deselect_all, 1, 0, 1, 1)

        self.lineWidth_label = QLabel(self.widget_2)
        self.lineWidth_label.setObjectName(u"lineWidth_label")

        self.gridLayout.addWidget(self.lineWidth_label, 11, 0, 1, 1)

        self.plot_options_label = QLabel(self.widget_2)
        self.plot_options_label.setObjectName(u"plot_options_label")

        self.gridLayout.addWidget(self.plot_options_label, 5, 0, 1, 2)

        self.regions_check = QCheckBox(self.widget_2)
        self.regions_check.setObjectName(u"regions_check")

        self.gridLayout.addWidget(self.regions_check, 7, 0, 1, 2)

        self.monochrome_color = ColorButton(self.widget_2)
        self.monochrome_color.setObjectName(u"monochrome_color")

        self.gridLayout.addWidget(self.monochrome_color, 6, 1, 1, 1)

        self.v_unit = QComboBox(self.widget_2)
        self.v_unit.addItem("")
        self.v_unit.addItem("")
        self.v_unit.setObjectName(u"v_unit")

        self.gridLayout.addWidget(self.v_unit, 13, 1, 1, 1)

        self.c_unit_label = QLabel(self.widget_2)
        self.c_unit_label.setObjectName(u"c_unit_label")

        self.gridLayout.addWidget(self.c_unit_label, 12, 0, 1, 1)

        self.line = QFrame(self.widget_2)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.VLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.gridLayout.addWidget(self.line, 4, 0, 1, 2)

        self.c_unit = QComboBox(self.widget_2)
        self.c_unit.addItem("")
        self.c_unit.addItem("")
        self.c_unit.addItem("")
        self.c_unit.setObjectName(u"c_unit")

        self.gridLayout.addWidget(self.c_unit, 12, 1, 1, 1)

        self.v_unit_label = QLabel(self.widget_2)
        self.v_unit_label.setObjectName(u"v_unit_label")

        self.gridLayout.addWidget(self.v_unit_label, 13, 0, 1, 1)

        self.textSize_label = QLabel(self.widget_2)
        self.textSize_label.setObjectName(u"textSize_label")

        self.gridLayout.addWidget(self.textSize_label, 10, 0, 1, 1)

        self.monochrome_check = QCheckBox(self.widget_2)
        self.monochrome_check.setObjectName(u"monochrome_check")

        self.gridLayout.addWidget(self.monochrome_check, 6, 0, 1, 1)

        self.hide_legend_check = QCheckBox(self.widget_2)
        self.hide_legend_check.setObjectName(u"hide_legend_check")

        self.gridLayout.addWidget(self.hide_legend_check, 9, 0, 1, 2)

        self.gridLayout.setColumnStretch(1, 1)

        self.verticalLayout.addWidget(self.widget_2)


        self.horizontalLayout.addWidget(self.widget)

        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setSpacing(7)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, -1, -1, -1)
        self.titrationSelector = QComboBox(self.centralwidget)
        self.titrationSelector.setObjectName(u"titrationSelector")
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        self.titrationSelector.setFont(font)

        self.verticalLayout_4.addWidget(self.titrationSelector)

        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.conc_tab = QWidget()
        self.conc_tab.setObjectName(u"conc_tab")
        self.horizontalLayout_2 = QHBoxLayout(self.conc_tab)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.conc_graph = PlotWidget(self.conc_tab)
        self.conc_graph.setObjectName(u"conc_graph")

        self.horizontalLayout_2.addWidget(self.conc_graph)

        self.tabWidget.addTab(self.conc_tab, "")
        self.perc_tab = QWidget()
        self.perc_tab.setObjectName(u"perc_tab")
        self.verticalLayout_2 = QVBoxLayout(self.perc_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(1, 1, 1, 1)
        self.perc_graph = PlotWidget(self.perc_tab)
        self.perc_graph.setObjectName(u"perc_graph")

        self.verticalLayout_2.addWidget(self.perc_graph)

        self.formLayout_2 = QFormLayout()
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.componentComboBox_perc = QComboBox(self.perc_tab)
        self.componentComboBox_perc.setObjectName(u"componentComboBox_perc")

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.componentComboBox_perc)

        self.componentLabel_2 = QLabel(self.perc_tab)
        self.componentLabel_2.setObjectName(u"componentLabel_2")

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.componentLabel_2)


        self.verticalLayout_2.addLayout(self.formLayout_2)

        self.verticalLayout_2.setStretch(0, 1)
        self.tabWidget.addTab(self.perc_tab, "")
        self.titration_tab = QWidget()
        self.titration_tab.setObjectName(u"titration_tab")
        self.verticalLayout_3 = QVBoxLayout(self.titration_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(1, 1, 1, 1)
        self.titration_graph = PlotWidget(self.titration_tab)
        self.titration_graph.setObjectName(u"titration_graph")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.titration_graph.sizePolicy().hasHeightForWidth())
        self.titration_graph.setSizePolicy(sizePolicy3)

        self.verticalLayout_3.addWidget(self.titration_graph)

        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.componentLabel = QLabel(self.titration_tab)
        self.componentLabel.setObjectName(u"componentLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.componentLabel)

        self.componentComboBox = QComboBox(self.titration_tab)
        self.componentComboBox.setObjectName(u"componentComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.componentComboBox)


        self.verticalLayout_3.addLayout(self.formLayout)

        self.verticalLayout_3.setStretch(0, 1)
        self.tabWidget.addTab(self.titration_tab, "")
        self.data_tab = QWidget()
        self.data_tab.setObjectName(u"data_tab")
        self.tabWidget.addTab(self.data_tab, "")

        self.verticalLayout_4.addWidget(self.tabWidget)

        self.exportButton = QPushButton(self.centralwidget)
        self.exportButton.setObjectName(u"exportButton")

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
        PlotWindow.setWindowTitle(QCoreApplication.translate("PlotWindow", u"Export Plot", None))
        self.filter.setText(QCoreApplication.translate("PlotWindow", u"Filter", None))
        self.errors_check.setText(QCoreApplication.translate("PlotWindow", u"Plot error bars", None))
        self.select_all.setText(QCoreApplication.translate("PlotWindow", u"Select All", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.species), QCoreApplication.translate("PlotWindow", u"Species", None))
        self.tabWidget_2.setTabText(self.tabWidget_2.indexOf(self.solids), QCoreApplication.translate("PlotWindow", u"Solids", None))
        self.deselect_all.setText(QCoreApplication.translate("PlotWindow", u"Deselect All", None))
        self.lineWidth_label.setText(QCoreApplication.translate("PlotWindow", u"Line width", None))
        self.plot_options_label.setText(QCoreApplication.translate("PlotWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Plot Options</span></p></body></html>", None))
        self.regions_check.setText(QCoreApplication.translate("PlotWindow", u"Solids as regions", None))
        self.monochrome_color.setText("")
        self.v_unit.setItemText(0, QCoreApplication.translate("PlotWindow", u"ml", None))
        self.v_unit.setItemText(1, QCoreApplication.translate("PlotWindow", u"l", None))

        self.c_unit_label.setText(QCoreApplication.translate("PlotWindow", u"Concentration Units", None))
        self.c_unit.setItemText(0, QCoreApplication.translate("PlotWindow", u"mol/l", None))
        self.c_unit.setItemText(1, QCoreApplication.translate("PlotWindow", u"mmol/l", None))
        self.c_unit.setItemText(2, QCoreApplication.translate("PlotWindow", u"\u03bcmol/l", None))

        self.v_unit_label.setText(QCoreApplication.translate("PlotWindow", u"Volume Units", None))
        self.textSize_label.setText(QCoreApplication.translate("PlotWindow", u"Text size", None))
        self.monochrome_check.setText(QCoreApplication.translate("PlotWindow", u"Monochrome", None))
        self.hide_legend_check.setText(QCoreApplication.translate("PlotWindow", u"Hide legend", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.conc_tab), QCoreApplication.translate("PlotWindow", u"Concentrations", None))
        self.componentLabel_2.setText(QCoreApplication.translate("PlotWindow", u"Component:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.perc_tab), QCoreApplication.translate("PlotWindow", u"Percentages", None))
        self.componentLabel.setText(QCoreApplication.translate("PlotWindow", u"Component:", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.titration_tab), QCoreApplication.translate("PlotWindow", u"Titration Curve", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.data_tab), QCoreApplication.translate("PlotWindow", u"Experimental Data", None))
        self.exportButton.setText(QCoreApplication.translate("PlotWindow", u"Export Graph", None))
    # retranslateUi

