# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_load.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QComboBox,
    QDialog, QDialogButtonBox, QGridLayout, QHBoxLayout,
    QHeaderView, QLabel, QLayout, QLineEdit,
    QPushButton, QSizePolicy, QSpinBox, QTableView,
    QVBoxLayout, QWidget)
import resources_rc

class Ui_loadCSVDialog(object):
    def setupUi(self, loadCSVDialog):
        if not loadCSVDialog.objectName():
            loadCSVDialog.setObjectName(u"loadCSVDialog")
        loadCSVDialog.resize(545, 597)
        loadCSVDialog.setMinimumSize(QSize(545, 597))
        icon = QIcon()
        icon.addFile(u":/icons/application-import.png", QSize(), QIcon.Normal, QIcon.Off)
        loadCSVDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(loadCSVDialog)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.filePath_label = QLabel(loadCSVDialog)
        self.filePath_label.setObjectName(u"filePath_label")
        sizePolicy = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.filePath_label.sizePolicy().hasHeightForWidth())
        self.filePath_label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.filePath_label)

        self.filePath = QLineEdit(loadCSVDialog)
        self.filePath.setObjectName(u"filePath")
        self.filePath.setCursor(QCursor(Qt.ArrowCursor))
        self.filePath.setAcceptDrops(False)
        self.filePath.setReadOnly(True)

        self.horizontalLayout.addWidget(self.filePath)

        self.open = QPushButton(loadCSVDialog)
        self.open.setObjectName(u"open")
        sizePolicy1 = QSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.open.sizePolicy().hasHeightForWidth())
        self.open.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.open)


        self.verticalLayout.addLayout(self.horizontalLayout)

        self.excelOptions = QGridLayout()
        self.excelOptions.setObjectName(u"excelOptions")
        self.excelOptions.setSizeConstraint(QLayout.SetMinimumSize)
        self.excelOptions.setContentsMargins(-1, -1, -1, 0)
        self.vCol_label = QLabel(loadCSVDialog)
        self.vCol_label.setObjectName(u"vCol_label")
        sizePolicy.setHeightForWidth(self.vCol_label.sizePolicy().hasHeightForWidth())
        self.vCol_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.vCol_label, 4, 0, 1, 1)

        self.eCol = QSpinBox(loadCSVDialog)
        self.eCol.setObjectName(u"eCol")
        sizePolicy2 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.eCol.sizePolicy().hasHeightForWidth())
        self.eCol.setSizePolicy(sizePolicy2)
        self.eCol.setMinimum(0)
        self.eCol.setMaximum(999)
        self.eCol.setValue(0)

        self.excelOptions.addWidget(self.eCol, 5, 1, 1, 1)

        self.head_label = QLabel(loadCSVDialog)
        self.head_label.setObjectName(u"head_label")
        sizePolicy.setHeightForWidth(self.head_label.sizePolicy().hasHeightForWidth())
        self.head_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.head_label, 2, 0, 1, 1)

        self.decimal = QComboBox(loadCSVDialog)
        self.decimal.addItem("")
        self.decimal.addItem("")
        self.decimal.setObjectName(u"decimal")
        sizePolicy3 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.decimal.sizePolicy().hasHeightForWidth())
        self.decimal.setSizePolicy(sizePolicy3)

        self.excelOptions.addWidget(self.decimal, 1, 1, 1, 1)

        self.separator_auto = QCheckBox(loadCSVDialog)
        self.separator_auto.setObjectName(u"separator_auto")
        sizePolicy1.setHeightForWidth(self.separator_auto.sizePolicy().hasHeightForWidth())
        self.separator_auto.setSizePolicy(sizePolicy1)
        self.separator_auto.setChecked(False)

        self.excelOptions.addWidget(self.separator_auto, 0, 2, 1, 1)

        self.vCol = QSpinBox(loadCSVDialog)
        self.vCol.setObjectName(u"vCol")
        sizePolicy2.setHeightForWidth(self.vCol.sizePolicy().hasHeightForWidth())
        self.vCol.setSizePolicy(sizePolicy2)
        self.vCol.setMinimum(0)
        self.vCol.setMaximum(999)

        self.excelOptions.addWidget(self.vCol, 4, 1, 1, 1)

        self.footer = QSpinBox(loadCSVDialog)
        self.footer.setObjectName(u"footer")
        sizePolicy3.setHeightForWidth(self.footer.sizePolicy().hasHeightForWidth())
        self.footer.setSizePolicy(sizePolicy3)
        self.footer.setMaximum(9999)

        self.excelOptions.addWidget(self.footer, 3, 1, 1, 1)

        self.separator_label = QLabel(loadCSVDialog)
        self.separator_label.setObjectName(u"separator_label")
        sizePolicy.setHeightForWidth(self.separator_label.sizePolicy().hasHeightForWidth())
        self.separator_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.separator_label, 0, 0, 1, 1)

        self.head = QSpinBox(loadCSVDialog)
        self.head.setObjectName(u"head")
        sizePolicy3.setHeightForWidth(self.head.sizePolicy().hasHeightForWidth())
        self.head.setSizePolicy(sizePolicy3)
        self.head.setMaximum(9999)

        self.excelOptions.addWidget(self.head, 2, 1, 1, 1)

        self.decimal_label = QLabel(loadCSVDialog)
        self.decimal_label.setObjectName(u"decimal_label")
        sizePolicy.setHeightForWidth(self.decimal_label.sizePolicy().hasHeightForWidth())
        self.decimal_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.decimal_label, 1, 0, 1, 1)

        self.decimal_auto = QCheckBox(loadCSVDialog)
        self.decimal_auto.setObjectName(u"decimal_auto")
        sizePolicy1.setHeightForWidth(self.decimal_auto.sizePolicy().hasHeightForWidth())
        self.decimal_auto.setSizePolicy(sizePolicy1)
        self.decimal_auto.setChecked(False)

        self.excelOptions.addWidget(self.decimal_auto, 1, 2, 1, 1)

        self.footer_label = QLabel(loadCSVDialog)
        self.footer_label.setObjectName(u"footer_label")
        sizePolicy.setHeightForWidth(self.footer_label.sizePolicy().hasHeightForWidth())
        self.footer_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.footer_label, 3, 0, 1, 1)

        self.separator = QComboBox(loadCSVDialog)
        self.separator.addItem("")
        self.separator.addItem("")
        self.separator.addItem("")
        self.separator.addItem("")
        self.separator.addItem("")
        self.separator.setObjectName(u"separator")
        sizePolicy3.setHeightForWidth(self.separator.sizePolicy().hasHeightForWidth())
        self.separator.setSizePolicy(sizePolicy3)

        self.excelOptions.addWidget(self.separator, 0, 1, 1, 1)

        self.eCol_label = QLabel(loadCSVDialog)
        self.eCol_label.setObjectName(u"eCol_label")
        sizePolicy.setHeightForWidth(self.eCol_label.sizePolicy().hasHeightForWidth())
        self.eCol_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.eCol_label, 5, 0, 1, 1)


        self.verticalLayout.addLayout(self.excelOptions)

        self.preview_label = QLabel(loadCSVDialog)
        self.preview_label.setObjectName(u"preview_label")

        self.verticalLayout.addWidget(self.preview_label)

        self.preview = QTableView(loadCSVDialog)
        self.preview.setObjectName(u"preview")

        self.verticalLayout.addWidget(self.preview)

        self.buttonBox = QDialogButtonBox(loadCSVDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(loadCSVDialog)
        self.buttonBox.accepted.connect(loadCSVDialog.accept)
        self.buttonBox.rejected.connect(loadCSVDialog.reject)
        self.separator_auto.stateChanged.connect(loadCSVDialog.autodetectSep)
        self.decimal_auto.stateChanged.connect(loadCSVDialog.autodetectDec)
        self.open.clicked.connect(loadCSVDialog.loadFile)
        self.separator.currentIndexChanged.connect(loadCSVDialog.updateSettings)
        self.decimal.currentIndexChanged.connect(loadCSVDialog.updateSettings)
        self.head.valueChanged.connect(loadCSVDialog.updateSettings)
        self.footer.valueChanged.connect(loadCSVDialog.updateSettings)

        self.decimal.setCurrentIndex(0)
        self.separator.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(loadCSVDialog)
    # setupUi

    def retranslateUi(self, loadCSVDialog):
        loadCSVDialog.setWindowTitle(QCoreApplication.translate("loadCSVDialog", u"Load Curve", None))
        self.filePath_label.setText(QCoreApplication.translate("loadCSVDialog", u"File Path:", None))
        self.open.setText(QCoreApplication.translate("loadCSVDialog", u"Open", None))
        self.vCol_label.setText(QCoreApplication.translate("loadCSVDialog", u"V Column:", None))
        self.head_label.setText(QCoreApplication.translate("loadCSVDialog", u"Skip Head:", None))
        self.decimal.setItemText(0, QCoreApplication.translate("loadCSVDialog", u",", None))
        self.decimal.setItemText(1, QCoreApplication.translate("loadCSVDialog", u".", None))

        self.separator_auto.setText(QCoreApplication.translate("loadCSVDialog", u"Autodetect", None))
        self.footer.setSuffix(QCoreApplication.translate("loadCSVDialog", u" lines", None))
        self.separator_label.setText(QCoreApplication.translate("loadCSVDialog", u"Separator:", None))
        self.head.setSuffix(QCoreApplication.translate("loadCSVDialog", u" lines", None))
        self.decimal_label.setText(QCoreApplication.translate("loadCSVDialog", u"Decimal Point:", None))
        self.decimal_auto.setText(QCoreApplication.translate("loadCSVDialog", u"Autodetect", None))
        self.footer_label.setText(QCoreApplication.translate("loadCSVDialog", u"Skip Footer:", None))
        self.separator.setItemText(0, QCoreApplication.translate("loadCSVDialog", u",", None))
        self.separator.setItemText(1, QCoreApplication.translate("loadCSVDialog", u".", None))
        self.separator.setItemText(2, QCoreApplication.translate("loadCSVDialog", u";", None))
        self.separator.setItemText(3, QCoreApplication.translate("loadCSVDialog", u"Tab", None))
        self.separator.setItemText(4, QCoreApplication.translate("loadCSVDialog", u"Space", None))

        self.eCol_label.setText(QCoreApplication.translate("loadCSVDialog", u"E Column:", None))
        self.preview_label.setText(QCoreApplication.translate("loadCSVDialog", u"<html><head/><body><p><span style=\" font-weight:600;\">Preview</span></p></body></html>", None))
    # retranslateUi

