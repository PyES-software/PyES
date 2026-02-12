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
        ExportWindow.resize(291, 176)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ExportWindow.sizePolicy().hasHeightForWidth())
        ExportWindow.setSizePolicy(sizePolicy)
        ExportWindow.setMinimumSize(QSize(0, 0))
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
        self.options_label = QLabel(self.widget_2)
        self.options_label.setObjectName(u"options_label")
        sizePolicy1.setHeightForWidth(self.options_label.sizePolicy().hasHeightForWidth())
        self.options_label.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.options_label)

        self.parameters_check = QCheckBox(self.widget_2)
        self.parameters_check.setObjectName(u"parameters_check")
        sizePolicy1.setHeightForWidth(self.parameters_check.sizePolicy().hasHeightForWidth())
        self.parameters_check.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.parameters_check)

        self.concentration_check = QCheckBox(self.widget_2)
        self.concentration_check.setObjectName(u"concentration_check")
        sizePolicy1.setHeightForWidth(self.concentration_check.sizePolicy().hasHeightForWidth())
        self.concentration_check.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.concentration_check)

        self.percent_check = QCheckBox(self.widget_2)
        self.percent_check.setObjectName(u"percent_check")
        sizePolicy1.setHeightForWidth(self.percent_check.sizePolicy().hasHeightForWidth())
        self.percent_check.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.percent_check)


        self.verticalLayout_2.addWidget(self.widget_2)

        self.export_button = QPushButton(ExportWindow)
        self.export_button.setObjectName(u"export_button")
        self.export_button.setEnabled(True)
        sizePolicy1.setHeightForWidth(self.export_button.sizePolicy().hasHeightForWidth())
        self.export_button.setSizePolicy(sizePolicy1)
        self.export_button.setAutoDefault(False)
        self.export_button.setFlat(False)

        self.verticalLayout_2.addWidget(self.export_button)


        self.retranslateUi(ExportWindow)

        self.export_button.setDefault(False)


        QMetaObject.connectSlotsByName(ExportWindow)
    # setupUi

    def retranslateUi(self, ExportWindow):
        ExportWindow.setWindowTitle(QCoreApplication.translate("ExportWindow", u"Export Results", None))
        self.options_label.setText(QCoreApplication.translate("ExportWindow", u"<html><head/><body><p><span style=\" font-weight:600;\">Select data you want to export:</span></p></body></html>", None))
        self.parameters_check.setText(QCoreApplication.translate("ExportWindow", u"Optimized parameters", None))
        self.concentration_check.setText(QCoreApplication.translate("ExportWindow", u"Concentrations in equilibrium", None))
        self.percent_check.setText(QCoreApplication.translate("ExportWindow", u"Percent concentrations in equilibrium", None))
        self.export_button.setText(QCoreApplication.translate("ExportWindow", u"Export", None))
    # retranslateUi

