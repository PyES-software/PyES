# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_dataExport.ui'
##
## Created by: Qt User Interface Compiler version 6.7.3
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QPushButton,
    QSizePolicy, QTabWidget, QVBoxLayout, QWidget)
import resources_rc

class Ui_ExportWindow(object):
    def setupUi(self, ExportWindow):
        if not ExportWindow.objectName():
            ExportWindow.setObjectName(u"ExportWindow")
        ExportWindow.resize(498, 237)
        ExportWindow.setMinimumSize(QSize(498, 237))
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        ExportWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icons/application-export.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ExportWindow.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(ExportWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.export_type = QTabWidget(ExportWindow)
        self.export_type.setObjectName(u"export_type")
        self.excel_tab = QWidget()
        self.excel_tab.setObjectName(u"excel_tab")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.excel_tab.sizePolicy().hasHeightForWidth())
        self.excel_tab.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(self.excel_tab)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(5, 0, 5, 10)
        self.widget_2 = QWidget(self.excel_tab)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.verticalLayout_5 = QVBoxLayout(self.widget_2)
        self.verticalLayout_5.setSpacing(5)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(5, 0, 0, 0)
        self.options_label_excel = QLabel(self.widget_2)
        self.options_label_excel.setObjectName(u"options_label_excel")

        self.verticalLayout_5.addWidget(self.options_label_excel)

        self.input_check_excel = QCheckBox(self.widget_2)
        self.input_check_excel.setObjectName(u"input_check_excel")
        self.input_check_excel.setChecked(True)

        self.verticalLayout_5.addWidget(self.input_check_excel)

        self.distribution_check_excel = QCheckBox(self.widget_2)
        self.distribution_check_excel.setObjectName(u"distribution_check_excel")

        self.verticalLayout_5.addWidget(self.distribution_check_excel)

        self.perc_check_excel = QCheckBox(self.widget_2)
        self.perc_check_excel.setObjectName(u"perc_check_excel")

        self.verticalLayout_5.addWidget(self.perc_check_excel)

        self.errors_check_excel = QCheckBox(self.widget_2)
        self.errors_check_excel.setObjectName(u"errors_check_excel")

        self.verticalLayout_5.addWidget(self.errors_check_excel)

        self.adjlogb_check_excel = QCheckBox(self.widget_2)
        self.adjlogb_check_excel.setObjectName(u"adjlogb_check_excel")

        self.verticalLayout_5.addWidget(self.adjlogb_check_excel)

        self.optimized_check_excel = QCheckBox(self.widget_2)
        self.optimized_check_excel.setObjectName(u"optimized_check_excel")

        self.verticalLayout_5.addWidget(self.optimized_check_excel)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.export_button_excel = QPushButton(self.excel_tab)
        self.export_button_excel.setObjectName(u"export_button_excel")
        self.export_button_excel.setEnabled(True)
        self.export_button_excel.setAutoDefault(False)
        self.export_button_excel.setFlat(False)

        self.verticalLayout_2.addWidget(self.export_button_excel)

        icon1 = QIcon()
        icon1.addFile(u":/icons/document-excel.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.export_type.addTab(self.excel_tab, icon1, "")
        self.csv_tab = QWidget()
        self.csv_tab.setObjectName(u"csv_tab")
        self.verticalLayout_3 = QVBoxLayout(self.csv_tab)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(5, 0, 5, 10)
        self.widget_5 = QWidget(self.csv_tab)
        self.widget_5.setObjectName(u"widget_5")
        sizePolicy1.setHeightForWidth(self.widget_5.sizePolicy().hasHeightForWidth())
        self.widget_5.setSizePolicy(sizePolicy1)
        self.verticalLayout_4 = QVBoxLayout(self.widget_5)
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(5, 0, 0, 0)
        self.options_label_csv = QLabel(self.widget_5)
        self.options_label_csv.setObjectName(u"options_label_csv")

        self.verticalLayout_4.addWidget(self.options_label_csv)

        self.input_check_csv = QCheckBox(self.widget_5)
        self.input_check_csv.setObjectName(u"input_check_csv")
        self.input_check_csv.setChecked(True)

        self.verticalLayout_4.addWidget(self.input_check_csv)

        self.distribution_check_csv = QCheckBox(self.widget_5)
        self.distribution_check_csv.setObjectName(u"distribution_check_csv")

        self.verticalLayout_4.addWidget(self.distribution_check_csv)

        self.perc_check_csv = QCheckBox(self.widget_5)
        self.perc_check_csv.setObjectName(u"perc_check_csv")

        self.verticalLayout_4.addWidget(self.perc_check_csv)

        self.errors_check_csv = QCheckBox(self.widget_5)
        self.errors_check_csv.setObjectName(u"errors_check_csv")

        self.verticalLayout_4.addWidget(self.errors_check_csv)

        self.adjlogb_check_csv = QCheckBox(self.widget_5)
        self.adjlogb_check_csv.setObjectName(u"adjlogb_check_csv")

        self.verticalLayout_4.addWidget(self.adjlogb_check_csv)

        self.optimized_check_csv = QCheckBox(self.widget_5)
        self.optimized_check_csv.setObjectName(u"optimized_check_csv")

        self.verticalLayout_4.addWidget(self.optimized_check_csv)


        self.verticalLayout_3.addWidget(self.widget_5)

        self.export_button_csv = QPushButton(self.csv_tab)
        self.export_button_csv.setObjectName(u"export_button_csv")
        self.export_button_csv.setEnabled(True)
        self.export_button_csv.setAutoDefault(False)
        self.export_button_csv.setFlat(False)

        self.verticalLayout_3.addWidget(self.export_button_csv)

        icon2 = QIcon()
        icon2.addFile(u":/icons/table.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.export_type.addTab(self.csv_tab, icon2, "")

        self.verticalLayout.addWidget(self.export_type)


        self.retranslateUi(ExportWindow)
        self.export_button_excel.clicked.connect(ExportWindow.ExcelExport)
        self.export_button_csv.clicked.connect(ExportWindow.CsvExport)

        self.export_type.setCurrentIndex(0)
        self.export_button_excel.setDefault(False)
        self.export_button_csv.setDefault(False)


        QMetaObject.connectSlotsByName(ExportWindow)
    # setupUi

    def retranslateUi(self, ExportWindow):
        ExportWindow.setWindowTitle(QCoreApplication.translate("ExportWindow", u"Export Results", None))
        self.options_label_excel.setText(QCoreApplication.translate("ExportWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Options:</span></p></body></html>", None))
        self.input_check_excel.setText(QCoreApplication.translate("ExportWindow", u"Input info", None))
        self.distribution_check_excel.setText(QCoreApplication.translate("ExportWindow", u"Distribution", None))
        self.perc_check_excel.setText(QCoreApplication.translate("ExportWindow", u"% with respect to component", None))
        self.errors_check_excel.setText(QCoreApplication.translate("ExportWindow", u"Std. Deviation of concentration", None))
        self.adjlogb_check_excel.setText(QCoreApplication.translate("ExportWindow", u"Adjusted formation constants", None))
        self.optimized_check_excel.setText(QCoreApplication.translate("ExportWindow", u"Optimized parameters", None))
        self.export_button_excel.setText(QCoreApplication.translate("ExportWindow", u"Export", None))
        self.export_type.setTabText(self.export_type.indexOf(self.excel_tab), QCoreApplication.translate("ExportWindow", u"Excel", None))
        self.options_label_csv.setText(QCoreApplication.translate("ExportWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Options:</span></p></body></html>", None))
        self.input_check_csv.setText(QCoreApplication.translate("ExportWindow", u"Input info", None))
        self.distribution_check_csv.setText(QCoreApplication.translate("ExportWindow", u"Distribution", None))
        self.perc_check_csv.setText(QCoreApplication.translate("ExportWindow", u"% with respect to component", None))
        self.errors_check_csv.setText(QCoreApplication.translate("ExportWindow", u"Std. Deviation of concentration", None))
        self.adjlogb_check_csv.setText(QCoreApplication.translate("ExportWindow", u"Adjusted formation constants", None))
        self.optimized_check_csv.setText(QCoreApplication.translate("ExportWindow", u"Optimized parameters", None))
        self.export_button_csv.setText(QCoreApplication.translate("ExportWindow", u"Export", None))
        self.export_type.setTabText(self.export_type.indexOf(self.csv_tab), QCoreApplication.translate("ExportWindow", u"CSV", None))
    # retranslateUi

