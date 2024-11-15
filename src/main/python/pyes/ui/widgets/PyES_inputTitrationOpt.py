# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_inputTitrationOpt.ui'
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
    QApplication,
    QFormLayout,
    QFrame,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QSpacerItem,
    QTableView,
    QToolButton,
    QVBoxLayout,
    QWidget,
)

from ui.widgets import CustomComboBox
from ui.widgets.spinbox import CustomSpinBox


class Ui_inputTitrationOpt(object):
    def setupUi(self, inputTitrationOpt):
        if not inputTitrationOpt.objectName():
            inputTitrationOpt.setObjectName("inputTitrationOpt")
        inputTitrationOpt.resize(1068, 628)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(inputTitrationOpt.sizePolicy().hasHeightForWidth())
        inputTitrationOpt.setSizePolicy(sizePolicy)
        inputTitrationOpt.setFocusPolicy(Qt.FocusPolicy.ClickFocus)
        self.horizontalLayout = QHBoxLayout(inputTitrationOpt)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.formLayout.setLabelAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignVCenter
        )
        self.formLayout.setFormAlignment(
            Qt.AlignmentFlag.AlignLeading
            | Qt.AlignmentFlag.AlignLeft
            | Qt.AlignmentFlag.AlignTop
        )
        self.formLayout.setContentsMargins(10, -1, 0, -1)
        self.titrationNameLabel = QLabel(inputTitrationOpt)
        self.titrationNameLabel.setObjectName("titrationNameLabel")

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.titrationNameLabel)

        self.titrationName = QLineEdit(inputTitrationOpt)
        self.titrationName.setObjectName("titrationName")

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.titrationName)

        self.importDataLabel = QLabel(inputTitrationOpt)
        self.importDataLabel.setObjectName("importDataLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.importDataLabel)

        self.importDataButton = QPushButton(inputTitrationOpt)
        self.importDataButton.setObjectName("importDataButton")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.importDataButton.sizePolicy().hasHeightForWidth()
        )
        self.importDataButton.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.importDataButton)

        self.px_ranges = QScrollArea(inputTitrationOpt)
        self.px_ranges.setObjectName("px_ranges")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Maximum
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.px_ranges.sizePolicy().hasHeightForWidth())
        self.px_ranges.setSizePolicy(sizePolicy2)
        self.px_ranges.setWidgetResizable(True)
        self.rangesScrollAreaWidgetContents = QWidget()
        self.rangesScrollAreaWidgetContents.setObjectName(
            "rangesScrollAreaWidgetContents"
        )
        self.rangesScrollAreaWidgetContents.setGeometry(QRect(0, 0, 282, 69))
        self.verticalLayout = QVBoxLayout(self.rangesScrollAreaWidgetContents)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.px_ranges.setWidget(self.rangesScrollAreaWidgetContents)

        self.formLayout.setWidget(4, QFormLayout.SpanningRole, self.px_ranges)

        self.line_6 = QFrame(inputTitrationOpt)
        self.line_6.setObjectName("line_6")
        self.line_6.setFrameShape(QFrame.Shape.HLine)
        self.line_6.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout.setWidget(5, QFormLayout.SpanningRole, self.line_6)

        self.label_7 = QLabel(inputTitrationOpt)
        self.label_7.setObjectName("label_7")

        self.formLayout.setWidget(6, QFormLayout.SpanningRole, self.label_7)

        self.e0Label = QLabel(inputTitrationOpt)
        self.e0Label.setObjectName("e0Label")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.e0Label)

        self.e0 = CustomSpinBox(inputTitrationOpt)
        self.e0.setObjectName("e0")
        self.e0.setMinimum(-10000.000000000000000)
        self.e0.setMaximum(10000.000000000000000)

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.e0)

        self.slopeLabel = QLabel(inputTitrationOpt)
        self.slopeLabel.setObjectName("slopeLabel")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.slopeLabel)

        self.slope = CustomSpinBox(inputTitrationOpt)
        self.slope.setObjectName("slope")
        self.slope.setMinimum(-10000.000000000000000)
        self.slope.setMaximum(10000.000000000000000)

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.slope)

        self.jaLabel = QLabel(inputTitrationOpt)
        self.jaLabel.setObjectName("jaLabel")
        self.jaLabel.setEnabled(False)

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.jaLabel)

        self.ja = CustomSpinBox(inputTitrationOpt)
        self.ja.setObjectName("ja")
        self.ja.setEnabled(False)
        self.ja.setMinimum(-10000.000000000000000)
        self.ja.setMaximum(10000.000000000000000)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.ja)

        self.jbLabel = QLabel(inputTitrationOpt)
        self.jbLabel.setObjectName("jbLabel")
        self.jbLabel.setEnabled(False)

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.jbLabel)

        self.jb = CustomSpinBox(inputTitrationOpt)
        self.jb.setObjectName("jb")
        self.jb.setEnabled(False)
        self.jb.setMinimum(-10000.000000000000000)
        self.jb.setMaximum(10000.000000000000000)

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.jb)

        self.eSigmaLabel = QLabel(inputTitrationOpt)
        self.eSigmaLabel.setObjectName("eSigmaLabel")

        self.formLayout.setWidget(11, QFormLayout.LabelRole, self.eSigmaLabel)

        self.eSigma = CustomSpinBox(inputTitrationOpt)
        self.eSigma.setObjectName("eSigma")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.eSigma.sizePolicy().hasHeightForWidth())
        self.eSigma.setSizePolicy(sizePolicy3)
        self.eSigma.setMinimum(0.000000000000000)
        self.eSigma.setMaximum(10000.000000000000000)

        self.formLayout.setWidget(11, QFormLayout.FieldRole, self.eSigma)

        self.electroActiveComponentLabel = QLabel(inputTitrationOpt)
        self.electroActiveComponentLabel.setObjectName("electroActiveComponentLabel")

        self.formLayout.setWidget(
            12, QFormLayout.LabelRole, self.electroActiveComponentLabel
        )

        self.electroActiveComponent = CustomComboBox(inputTitrationOpt)
        self.electroActiveComponent.setObjectName("electroActiveComponent")

        self.formLayout.setWidget(
            12, QFormLayout.FieldRole, self.electroActiveComponent
        )

        self.line = QFrame(inputTitrationOpt)
        self.line.setObjectName("line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout.setWidget(13, QFormLayout.SpanningRole, self.line)

        self.label_8 = QLabel(inputTitrationOpt)
        self.label_8.setObjectName("label_8")

        self.formLayout.setWidget(14, QFormLayout.SpanningRole, self.label_8)

        self.vSigmaLabel = QLabel(inputTitrationOpt)
        self.vSigmaLabel.setObjectName("vSigmaLabel")

        self.formLayout.setWidget(15, QFormLayout.LabelRole, self.vSigmaLabel)

        self.vSigma = CustomSpinBox(inputTitrationOpt)
        self.vSigma.setObjectName("vSigma")
        sizePolicy3.setHeightForWidth(self.vSigma.sizePolicy().hasHeightForWidth())
        self.vSigma.setSizePolicy(sizePolicy3)
        self.vSigma.setMaximum(10000.000000000000000)
        self.vSigma.setSingleStep(0.100000000000000)

        self.formLayout.setWidget(15, QFormLayout.FieldRole, self.vSigma)

        self.initialVolumeLabel = QLabel(inputTitrationOpt)
        self.initialVolumeLabel.setObjectName("initialVolumeLabel")

        self.formLayout.setWidget(16, QFormLayout.LabelRole, self.initialVolumeLabel)

        self.initialVolume = CustomSpinBox(inputTitrationOpt)
        self.initialVolume.setObjectName("initialVolume")
        self.initialVolume.setMaximum(10000.000000000000000)

        self.formLayout.setWidget(16, QFormLayout.FieldRole, self.initialVolume)

        self.line_3 = QFrame(inputTitrationOpt)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShape(QFrame.Shape.HLine)
        self.line_3.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout.setWidget(17, QFormLayout.SpanningRole, self.line_3)

        self.label_6 = QLabel(inputTitrationOpt)
        self.label_6.setObjectName("label_6")

        self.formLayout.setWidget(18, QFormLayout.SpanningRole, self.label_6)

        self.c0back_label = QLabel(inputTitrationOpt)
        self.c0back_label.setObjectName("c0back_label")

        self.formLayout.setWidget(19, QFormLayout.LabelRole, self.c0back_label)

        self.c0back = CustomSpinBox(inputTitrationOpt)
        self.c0back.setObjectName("c0back")
        self.c0back.setDecimals(5)
        self.c0back.setMaximum(900.000000000000000)
        self.c0back.setSingleStep(0.050000000000000)

        self.formLayout.setWidget(19, QFormLayout.FieldRole, self.c0back)

        self.ctback_label = QLabel(inputTitrationOpt)
        self.ctback_label.setObjectName("ctback_label")

        self.formLayout.setWidget(20, QFormLayout.LabelRole, self.ctback_label)

        self.ctback = CustomSpinBox(inputTitrationOpt)
        self.ctback.setObjectName("ctback")
        self.ctback.setDecimals(5)
        self.ctback.setMaximum(900.000000000000000)
        self.ctback.setSingleStep(0.050000000000000)

        self.formLayout.setWidget(20, QFormLayout.FieldRole, self.ctback)

        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(-1, 0, 0, -1)
        self.ranges_label = QLabel(inputTitrationOpt)
        self.ranges_label.setObjectName("ranges_label")

        self.horizontalLayout_2.addWidget(self.ranges_label)

        self.horizontalSpacer = QSpacerItem(
            40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum
        )

        self.horizontalLayout_2.addItem(self.horizontalSpacer)

        self.addRangeButton = QToolButton(inputTitrationOpt)
        self.addRangeButton.setObjectName("addRangeButton")
        icon = QIcon()
        icon.addFile(":/icons/plus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.addRangeButton.setIcon(icon)

        self.horizontalLayout_2.addWidget(self.addRangeButton)

        self.removeRangeButton = QToolButton(inputTitrationOpt)
        self.removeRangeButton.setObjectName("removeRangeButton")
        icon1 = QIcon()
        icon1.addFile(":/icons/minus.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.removeRangeButton.setIcon(icon1)

        self.horizontalLayout_2.addWidget(self.removeRangeButton)

        self.formLayout.setLayout(3, QFormLayout.SpanningRole, self.horizontalLayout_2)

        self.horizontalLayout.addLayout(self.formLayout)

        self.titrationLayout = QVBoxLayout()
        self.titrationLayout.setObjectName("titrationLayout")
        self.titration_label = QLabel(inputTitrationOpt)
        self.titration_label.setObjectName("titration_label")

        self.titrationLayout.addWidget(self.titration_label)

        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setSpacing(2)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.useAllButton = QPushButton(inputTitrationOpt)
        self.useAllButton.setObjectName("useAllButton")

        self.horizontalLayout_3.addWidget(self.useAllButton)

        self.useEvenButton = QPushButton(inputTitrationOpt)
        self.useEvenButton.setObjectName("useEvenButton")

        self.horizontalLayout_3.addWidget(self.useEvenButton)

        self.useOddButton = QPushButton(inputTitrationOpt)
        self.useOddButton.setObjectName("useOddButton")

        self.horizontalLayout_3.addWidget(self.useOddButton)

        self.titrationLayout.addLayout(self.horizontalLayout_3)

        self.titrationView = QTableView(inputTitrationOpt)
        self.titrationView.setObjectName("titrationView")

        self.titrationLayout.addWidget(self.titrationView)

        self.horizontalLayout.addLayout(self.titrationLayout)

        self.concLayout = QVBoxLayout()
        self.concLayout.setObjectName("concLayout")
        self.conc_label = QLabel(inputTitrationOpt)
        self.conc_label.setObjectName("conc_label")

        self.concLayout.addWidget(self.conc_label)

        self.concView = QTableView(inputTitrationOpt)
        self.concView.setObjectName("concView")

        self.concLayout.addWidget(self.concView)

        self.horizontalLayout.addLayout(self.concLayout)

        self.horizontalLayout.setStretch(1, 1)
        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(inputTitrationOpt)

        QMetaObject.connectSlotsByName(inputTitrationOpt)

    # setupUi

    def retranslateUi(self, inputTitrationOpt):
        inputTitrationOpt.setWindowTitle(
            QCoreApplication.translate("inputTitrationOpt", "Form", None)
        )
        self.titrationNameLabel.setText(
            QCoreApplication.translate(
                "inputTitrationOpt",
                '<html><head/><body><p><span style=" font-weight:600;">Titration Name:</span></p></body></html>',
                None,
            )
        )
        self.importDataLabel.setText(
            QCoreApplication.translate("inputTitrationOpt", "Import Data", None)
        )
        self.importDataButton.setText(
            QCoreApplication.translate("inputTitrationOpt", "Import", None)
        )
        self.label_7.setText(
            QCoreApplication.translate(
                "inputTitrationOpt",
                '<html><head/><body><p><span style=" font-weight:600;">Electrode Options:</span></p></body></html>',
                None,
            )
        )
        self.e0Label.setText(
            QCoreApplication.translate("inputTitrationOpt", "E0", None)
        )
        self.e0.setSuffix(QCoreApplication.translate("inputTitrationOpt", " mV", None))
        self.slopeLabel.setText(
            QCoreApplication.translate("inputTitrationOpt", "Slope", None)
        )
        self.jaLabel.setText(
            QCoreApplication.translate("inputTitrationOpt", "Ja", None)
        )
        self.jbLabel.setText(
            QCoreApplication.translate("inputTitrationOpt", "Jb", None)
        )
        self.eSigmaLabel.setText(
            QCoreApplication.translate("inputTitrationOpt", "E Sigma", None)
        )
        self.eSigma.setSuffix("")
        self.electroActiveComponentLabel.setText(
            QCoreApplication.translate(
                "inputTitrationOpt", "Electro Active Component", None
            )
        )
        self.label_8.setText(
            QCoreApplication.translate(
                "inputTitrationOpt",
                '<html><head/><body><p><span style=" font-weight:600;">Vessel Options:</span></p></body></html>',
                None,
            )
        )
        self.vSigmaLabel.setText(
            QCoreApplication.translate("inputTitrationOpt", "V Sigma", None)
        )
        self.vSigma.setSuffix("")
        self.initialVolumeLabel.setText(
            QCoreApplication.translate("inputTitrationOpt", "Initial Volume", None)
        )
        self.initialVolume.setSuffix(
            QCoreApplication.translate("inputTitrationOpt", " ml", None)
        )
        self.label_6.setText(
            QCoreApplication.translate(
                "inputTitrationOpt",
                '<html><head/><body><p><span style=" font-weight:600;">Background Ions Settings:</span></p></body></html>',
                None,
            )
        )
        self.c0back_label.setText(
            QCoreApplication.translate("inputTitrationOpt", "Initial C:", None)
        )
        # if QT_CONFIG(statustip)
        self.c0back.setStatusTip(
            QCoreApplication.translate(
                "inputTitrationOpt",
                "Initial concentration of background ions in titration vessel.",
                None,
            )
        )
        # endif // QT_CONFIG(statustip)
        self.c0back.setSuffix(
            QCoreApplication.translate("inputTitrationOpt", " mol/l", None)
        )
        self.ctback_label.setText(
            QCoreApplication.translate("inputTitrationOpt", "Titrant C:", None)
        )
        # if QT_CONFIG(statustip)
        self.ctback.setStatusTip(
            QCoreApplication.translate(
                "inputTitrationOpt",
                "Concentration of background ions in the titrant.",
                None,
            )
        )
        # endif // QT_CONFIG(statustip)
        self.ctback.setSuffix(
            QCoreApplication.translate("inputTitrationOpt", " mol/l", None)
        )
        self.ranges_label.setText(
            QCoreApplication.translate(
                "inputTitrationOpt",
                '<html><head/><body><p><span style=" font-weight:700;">pX Ranges:</span></p></body></html>',
                None,
            )
        )
        self.addRangeButton.setText("")
        self.removeRangeButton.setText(
            QCoreApplication.translate("inputTitrationOpt", "...", None)
        )
        self.titration_label.setText(
            QCoreApplication.translate(
                "inputTitrationOpt",
                '<html><head/><body><p><span style=" font-weight:700;">Titration:</span></p></body></html>',
                None,
            )
        )
        self.useAllButton.setText(
            QCoreApplication.translate("inputTitrationOpt", "Use All", None)
        )
        self.useEvenButton.setText(
            QCoreApplication.translate("inputTitrationOpt", "Use Half (even)", None)
        )
        self.useOddButton.setText(
            QCoreApplication.translate("inputTitrationOpt", "Use Half (odd)", None)
        )
        self.conc_label.setText(
            QCoreApplication.translate(
                "inputTitrationOpt",
                '<html><head/><body><p><span style=" font-weight:700;">Concentrations:</span></p></body></html>',
                None,
            )
        )

    # retranslateUi
