# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_load.ui'
##
## Created by: Qt User Interface Compiler version 6.8.0
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
    QAbstractButton,
    QApplication,
    QCheckBox,
    QComboBox,
    QDialog,
    QDialogButtonBox,
    QGridLayout,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLayout,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QTableView,
    QVBoxLayout,
    QWidget,
)


class Ui_loadCSVDialog(object):
    def setupUi(self, loadCSVDialog):
        if not loadCSVDialog.objectName():
            loadCSVDialog.setObjectName("loadCSVDialog")
        loadCSVDialog.resize(545, 597)
        loadCSVDialog.setMinimumSize(QSize(545, 597))
        icon = QIcon()
        icon.addFile(
            ":/icons/application-import.png",
            QSize(),
            QIcon.Mode.Normal,
            QIcon.State.Off,
        )
        loadCSVDialog.setWindowIcon(icon)
        self.verticalLayout = QVBoxLayout(loadCSVDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.filePath_label = QLabel(loadCSVDialog)
        self.filePath_label.setObjectName("filePath_label")
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            self.filePath_label.sizePolicy().hasHeightForWidth()
        )
        self.filePath_label.setSizePolicy(sizePolicy)

        self.horizontalLayout.addWidget(self.filePath_label)

        self.filePath = QLineEdit(loadCSVDialog)
        self.filePath.setObjectName("filePath")
        self.filePath.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.filePath.setAcceptDrops(False)
        self.filePath.setReadOnly(True)

        self.horizontalLayout.addWidget(self.filePath)

        self.open = QPushButton(loadCSVDialog)
        self.open.setObjectName("open")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.open.sizePolicy().hasHeightForWidth())
        self.open.setSizePolicy(sizePolicy1)

        self.horizontalLayout.addWidget(self.open)

        self.verticalLayout.addLayout(self.horizontalLayout)

        self.excelOptions = QGridLayout()
        self.excelOptions.setObjectName("excelOptions")
        self.excelOptions.setSizeConstraint(QLayout.SetMinimumSize)
        self.excelOptions.setContentsMargins(-1, -1, -1, 0)
        self.head_label = QLabel(loadCSVDialog)
        self.head_label.setObjectName("head_label")
        sizePolicy.setHeightForWidth(self.head_label.sizePolicy().hasHeightForWidth())
        self.head_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.head_label, 2, 0, 1, 1)

        self.decimal_auto = QCheckBox(loadCSVDialog)
        self.decimal_auto.setObjectName("decimal_auto")
        sizePolicy1.setHeightForWidth(
            self.decimal_auto.sizePolicy().hasHeightForWidth()
        )
        self.decimal_auto.setSizePolicy(sizePolicy1)
        self.decimal_auto.setChecked(False)

        self.excelOptions.addWidget(self.decimal_auto, 1, 2, 1, 1)

        self.vCol = QSpinBox(loadCSVDialog)
        self.vCol.setObjectName("vCol")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.MinimumExpanding, QSizePolicy.Policy.Fixed
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.vCol.sizePolicy().hasHeightForWidth())
        self.vCol.setSizePolicy(sizePolicy2)
        self.vCol.setMinimum(0)
        self.vCol.setMaximum(999)

        self.excelOptions.addWidget(self.vCol, 4, 1, 1, 1)

        self.head = QSpinBox(loadCSVDialog)
        self.head.setObjectName("head")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.head.sizePolicy().hasHeightForWidth())
        self.head.setSizePolicy(sizePolicy3)
        self.head.setMaximum(9999)

        self.excelOptions.addWidget(self.head, 2, 1, 1, 1)

        self.vCol_label = QLabel(loadCSVDialog)
        self.vCol_label.setObjectName("vCol_label")
        sizePolicy.setHeightForWidth(self.vCol_label.sizePolicy().hasHeightForWidth())
        self.vCol_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.vCol_label, 4, 0, 1, 1)

        self.decimal = QComboBox(loadCSVDialog)
        self.decimal.addItem("")
        self.decimal.addItem("")
        self.decimal.setObjectName("decimal")
        sizePolicy3.setHeightForWidth(self.decimal.sizePolicy().hasHeightForWidth())
        self.decimal.setSizePolicy(sizePolicy3)

        self.excelOptions.addWidget(self.decimal, 1, 1, 1, 1)

        self.eCol_label = QLabel(loadCSVDialog)
        self.eCol_label.setObjectName("eCol_label")
        sizePolicy.setHeightForWidth(self.eCol_label.sizePolicy().hasHeightForWidth())
        self.eCol_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.eCol_label, 5, 0, 1, 1)

        self.footer = QSpinBox(loadCSVDialog)
        self.footer.setObjectName("footer")
        sizePolicy3.setHeightForWidth(self.footer.sizePolicy().hasHeightForWidth())
        self.footer.setSizePolicy(sizePolicy3)
        self.footer.setMaximum(9999)

        self.excelOptions.addWidget(self.footer, 3, 1, 1, 1)

        self.separator = QComboBox(loadCSVDialog)
        self.separator.addItem("")
        self.separator.addItem("")
        self.separator.addItem("")
        self.separator.addItem("")
        self.separator.addItem("")
        self.separator.setObjectName("separator")
        sizePolicy3.setHeightForWidth(self.separator.sizePolicy().hasHeightForWidth())
        self.separator.setSizePolicy(sizePolicy3)

        self.excelOptions.addWidget(self.separator, 0, 1, 1, 1)

        self.decimal_label = QLabel(loadCSVDialog)
        self.decimal_label.setObjectName("decimal_label")
        sizePolicy.setHeightForWidth(
            self.decimal_label.sizePolicy().hasHeightForWidth()
        )
        self.decimal_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.decimal_label, 1, 0, 1, 1)

        self.separator_auto = QCheckBox(loadCSVDialog)
        self.separator_auto.setObjectName("separator_auto")
        sizePolicy1.setHeightForWidth(
            self.separator_auto.sizePolicy().hasHeightForWidth()
        )
        self.separator_auto.setSizePolicy(sizePolicy1)
        self.separator_auto.setChecked(False)

        self.excelOptions.addWidget(self.separator_auto, 0, 2, 1, 1)

        self.eCol = QSpinBox(loadCSVDialog)
        self.eCol.setObjectName("eCol")
        sizePolicy2.setHeightForWidth(self.eCol.sizePolicy().hasHeightForWidth())
        self.eCol.setSizePolicy(sizePolicy2)
        self.eCol.setMinimum(0)
        self.eCol.setMaximum(999)
        self.eCol.setValue(0)

        self.excelOptions.addWidget(self.eCol, 5, 1, 1, 1)

        self.footer_label = QLabel(loadCSVDialog)
        self.footer_label.setObjectName("footer_label")
        sizePolicy.setHeightForWidth(self.footer_label.sizePolicy().hasHeightForWidth())
        self.footer_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.footer_label, 3, 0, 1, 1)

        self.separator_label = QLabel(loadCSVDialog)
        self.separator_label.setObjectName("separator_label")
        sizePolicy.setHeightForWidth(
            self.separator_label.sizePolicy().hasHeightForWidth()
        )
        self.separator_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.separator_label, 0, 0, 1, 1)

        self.wCol = QSpinBox(loadCSVDialog)
        self.wCol.setObjectName("wCol")
        sizePolicy2.setHeightForWidth(self.wCol.sizePolicy().hasHeightForWidth())
        self.wCol.setSizePolicy(sizePolicy2)
        self.wCol.setMinimum(0)
        self.wCol.setMaximum(999)
        self.wCol.setValue(0)

        self.excelOptions.addWidget(self.wCol, 6, 1, 1, 1)

        self.wCol_label = QLabel(loadCSVDialog)
        self.wCol_label.setObjectName("wCol_label")
        sizePolicy.setHeightForWidth(self.wCol_label.sizePolicy().hasHeightForWidth())
        self.wCol_label.setSizePolicy(sizePolicy)

        self.excelOptions.addWidget(self.wCol_label, 6, 0, 1, 1)

        self.no_weights = QCheckBox(loadCSVDialog)
        self.no_weights.setObjectName("no_weights")
        sizePolicy1.setHeightForWidth(self.no_weights.sizePolicy().hasHeightForWidth())
        self.no_weights.setSizePolicy(sizePolicy1)
        self.no_weights.setChecked(False)

        self.excelOptions.addWidget(self.no_weights, 6, 2, 1, 1)

        self.verticalLayout.addLayout(self.excelOptions)

        self.preview_label = QLabel(loadCSVDialog)
        self.preview_label.setObjectName("preview_label")

        self.verticalLayout.addWidget(self.preview_label)

        self.preview = QTableView(loadCSVDialog)
        self.preview.setObjectName("preview")

        self.verticalLayout.addWidget(self.preview)

        self.buttonBox = QDialogButtonBox(loadCSVDialog)
        self.buttonBox.setObjectName("buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)

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
        loadCSVDialog.setWindowTitle(
            QCoreApplication.translate("loadCSVDialog", "Load Curve", None)
        )
        self.filePath_label.setText(
            QCoreApplication.translate("loadCSVDialog", "File Path:", None)
        )
        self.open.setText(QCoreApplication.translate("loadCSVDialog", "Open", None))
        self.head_label.setText(
            QCoreApplication.translate("loadCSVDialog", "Skip Head:", None)
        )
        self.decimal_auto.setText(
            QCoreApplication.translate("loadCSVDialog", "Autodetect", None)
        )
        self.head.setSuffix(QCoreApplication.translate("loadCSVDialog", " lines", None))
        self.vCol_label.setText(
            QCoreApplication.translate("loadCSVDialog", "V Column:", None)
        )
        self.decimal.setItemText(
            0, QCoreApplication.translate("loadCSVDialog", ",", None)
        )
        self.decimal.setItemText(
            1, QCoreApplication.translate("loadCSVDialog", ".", None)
        )

        self.eCol_label.setText(
            QCoreApplication.translate("loadCSVDialog", "E Column:", None)
        )
        self.footer.setSuffix(
            QCoreApplication.translate("loadCSVDialog", " lines", None)
        )
        self.separator.setItemText(
            0, QCoreApplication.translate("loadCSVDialog", ",", None)
        )
        self.separator.setItemText(
            1, QCoreApplication.translate("loadCSVDialog", ".", None)
        )
        self.separator.setItemText(
            2, QCoreApplication.translate("loadCSVDialog", ";", None)
        )
        self.separator.setItemText(
            3, QCoreApplication.translate("loadCSVDialog", "Tab", None)
        )
        self.separator.setItemText(
            4, QCoreApplication.translate("loadCSVDialog", "Space", None)
        )

        self.decimal_label.setText(
            QCoreApplication.translate("loadCSVDialog", "Decimal Point:", None)
        )
        self.separator_auto.setText(
            QCoreApplication.translate("loadCSVDialog", "Autodetect", None)
        )
        self.footer_label.setText(
            QCoreApplication.translate("loadCSVDialog", "Skip Footer:", None)
        )
        self.separator_label.setText(
            QCoreApplication.translate("loadCSVDialog", "Separator:", None)
        )
        self.wCol_label.setText(
            QCoreApplication.translate("loadCSVDialog", "W Column:", None)
        )
        self.no_weights.setText(
            QCoreApplication.translate("loadCSVDialog", "No Weights", None)
        )
        self.preview_label.setText(
            QCoreApplication.translate(
                "loadCSVDialog",
                '<html><head/><body><p><span style=" font-weight:600;">Preview</span></p></body></html>',
                None,
            )
        )

    # retranslateUi
