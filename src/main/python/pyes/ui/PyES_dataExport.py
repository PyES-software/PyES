# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_dataExport.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QLabel, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget)
import resources_rc

class Ui_ExportWindow(object):
    def setupUi(self, ExportWindow):
        if not ExportWindow.objectName():
            ExportWindow.setObjectName(u"ExportWindow")
        ExportWindow.resize(300, 200)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ExportWindow.sizePolicy().hasHeightForWidth())
        ExportWindow.setSizePolicy(sizePolicy)
        ExportWindow.setMinimumSize(QSize(300, 200))
        font = QFont()
        font.setFamilies([u".AppleSystemUIFont"])
        ExportWindow.setFont(font)
        icon = QIcon()
        icon.addFile(u":/icons/application-export.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        ExportWindow.setWindowIcon(icon)
        self.verticalLayout_2 = QVBoxLayout(ExportWindow)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.widget_2 = QWidget(ExportWindow)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Preferred)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)
        self.verticalLayout = QVBoxLayout(self.widget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.options_label_excel = QLabel(self.widget_2)
        self.options_label_excel.setObjectName(u"options_label_excel")
        sizePolicy1.setHeightForWidth(self.options_label_excel.sizePolicy().hasHeightForWidth())
        self.options_label_excel.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.options_label_excel)

        self.input_check_excel = QCheckBox(self.widget_2)
        self.input_check_excel.setObjectName(u"input_check_excel")
        sizePolicy1.setHeightForWidth(self.input_check_excel.sizePolicy().hasHeightForWidth())
        self.input_check_excel.setSizePolicy(sizePolicy1)
        self.input_check_excel.setChecked(True)

        self.verticalLayout.addWidget(self.input_check_excel)

        self.optimized_check_excel = QCheckBox(self.widget_2)
        self.optimized_check_excel.setObjectName(u"optimized_check_excel")
        sizePolicy1.setHeightForWidth(self.optimized_check_excel.sizePolicy().hasHeightForWidth())
        self.optimized_check_excel.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.optimized_check_excel)

        self.distribution_check_excel = QCheckBox(self.widget_2)
        self.distribution_check_excel.setObjectName(u"distribution_check_excel")
        sizePolicy1.setHeightForWidth(self.distribution_check_excel.sizePolicy().hasHeightForWidth())
        self.distribution_check_excel.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.distribution_check_excel)

        self.errors_check_excel = QCheckBox(self.widget_2)
        self.errors_check_excel.setObjectName(u"errors_check_excel")
        sizePolicy1.setHeightForWidth(self.errors_check_excel.sizePolicy().hasHeightForWidth())
        self.errors_check_excel.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.errors_check_excel)

        self.perc_check_excel = QCheckBox(self.widget_2)
        self.perc_check_excel.setObjectName(u"perc_check_excel")
        sizePolicy1.setHeightForWidth(self.perc_check_excel.sizePolicy().hasHeightForWidth())
        self.perc_check_excel.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.perc_check_excel)

        self.adjlogb_check_excel = QCheckBox(self.widget_2)
        self.adjlogb_check_excel.setObjectName(u"adjlogb_check_excel")
        sizePolicy1.setHeightForWidth(self.adjlogb_check_excel.sizePolicy().hasHeightForWidth())
        self.adjlogb_check_excel.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.adjlogb_check_excel)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.export_button_excel = QPushButton(ExportWindow)
        self.export_button_excel.setObjectName(u"export_button_excel")
        self.export_button_excel.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.export_button_excel.sizePolicy().hasHeightForWidth())
        self.export_button_excel.setSizePolicy(sizePolicy1)
        self.export_button_excel.setAutoDefault(False)
        self.export_button_excel.setFlat(False)

        self.verticalLayout_2.addWidget(self.export_button_excel)


        self.retranslateUi(ExportWindow)

        self.export_button_excel.setDefault(False)


        QMetaObject.connectSlotsByName(ExportWindow)
    # setupUi

    def retranslateUi(self, ExportWindow):
        ExportWindow.setWindowTitle(QCoreApplication.translate("ExportWindow", u"Export Results", None))
        self.options_label_excel.setText(QCoreApplication.translate("ExportWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Options:</span></p></body></html>", None))
        self.input_check_excel.setText(QCoreApplication.translate("ExportWindow", u"Input info", None))
        self.optimized_check_excel.setText(QCoreApplication.translate("ExportWindow", u"Optimized parameters", None))
        self.distribution_check_excel.setText(QCoreApplication.translate("ExportWindow", u"Species distribution", None))
        self.errors_check_excel.setText(QCoreApplication.translate("ExportWindow", u"Std. Deviation of concentration", None))
        self.perc_check_excel.setText(QCoreApplication.translate("ExportWindow", u"Percentages with respect to component", None))
        self.adjlogb_check_excel.setText(QCoreApplication.translate("ExportWindow", u"Adjusted formation constants", None))
        self.export_button_excel.setText(QCoreApplication.translate("ExportWindow", u"Export", None))
    # retranslateUi

