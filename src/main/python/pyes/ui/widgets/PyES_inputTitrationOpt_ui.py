# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_inputTitrationOpt.ui'
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
from PySide6.QtWidgets import (QApplication, QFormLayout, QFrame, QHBoxLayout,
    QHeaderView, QLabel, QLineEdit, QPushButton,
    QSizePolicy, QTableView, QVBoxLayout, QWidget)

from ui.widgets import CustomComboBox
from ui.widgets.spinbox import CustomSpinBox

class Ui_inputTitrationOpt(object):
    def setupUi(self, inputTitrationOpt):
        if not inputTitrationOpt.objectName():
            inputTitrationOpt.setObjectName(u"inputTitrationOpt")
        inputTitrationOpt.resize(1068, 572)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(inputTitrationOpt.sizePolicy().hasHeightForWidth())
        inputTitrationOpt.setSizePolicy(sizePolicy)
        inputTitrationOpt.setFocusPolicy(Qt.ClickFocus)
        self.horizontalLayout = QHBoxLayout(inputTitrationOpt)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setLabelAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignVCenter)
        self.formLayout.setFormAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.formLayout.setContentsMargins(-1, -1, 0, -1)
        self.importDataLabel = QLabel(inputTitrationOpt)
        self.importDataLabel.setObjectName(u"importDataLabel")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.importDataLabel)

        self.importDataButton = QPushButton(inputTitrationOpt)
        self.importDataButton.setObjectName(u"importDataButton")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.importDataButton.sizePolicy().hasHeightForWidth())
        self.importDataButton.setSizePolicy(sizePolicy1)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.importDataButton)

        self.line_6 = QFrame(inputTitrationOpt)
        self.line_6.setObjectName(u"line_6")
        self.line_6.setFrameShape(QFrame.HLine)
        self.line_6.setFrameShadow(QFrame.Sunken)

        self.formLayout.setWidget(3, QFormLayout.SpanningRole, self.line_6)

        self.label_7 = QLabel(inputTitrationOpt)
        self.label_7.setObjectName(u"label_7")

        self.formLayout.setWidget(4, QFormLayout.SpanningRole, self.label_7)

        self.e0Label = QLabel(inputTitrationOpt)
        self.e0Label.setObjectName(u"e0Label")

        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.e0Label)

        self.e0 = CustomSpinBox(inputTitrationOpt)
        self.e0.setObjectName(u"e0")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.e0)

        self.eSigmaLabel = QLabel(inputTitrationOpt)
        self.eSigmaLabel.setObjectName(u"eSigmaLabel")

        self.formLayout.setWidget(9, QFormLayout.LabelRole, self.eSigmaLabel)

        self.eSigma = CustomSpinBox(inputTitrationOpt)
        self.eSigma.setObjectName(u"eSigma")
        sizePolicy2 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.eSigma.sizePolicy().hasHeightForWidth())
        self.eSigma.setSizePolicy(sizePolicy2)

        self.formLayout.setWidget(9, QFormLayout.FieldRole, self.eSigma)

        self.electroActiveComponent = CustomComboBox(inputTitrationOpt)
        self.electroActiveComponent.setObjectName(u"electroActiveComponent")

        self.formLayout.setWidget(10, QFormLayout.FieldRole, self.electroActiveComponent)

        self.line = QFrame(inputTitrationOpt)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)

        self.formLayout.setWidget(11, QFormLayout.SpanningRole, self.line)

        self.label_8 = QLabel(inputTitrationOpt)
        self.label_8.setObjectName(u"label_8")

        self.formLayout.setWidget(12, QFormLayout.SpanningRole, self.label_8)

        self.vSigmaLabel = QLabel(inputTitrationOpt)
        self.vSigmaLabel.setObjectName(u"vSigmaLabel")

        self.formLayout.setWidget(13, QFormLayout.LabelRole, self.vSigmaLabel)

        self.vSigma = CustomSpinBox(inputTitrationOpt)
        self.vSigma.setObjectName(u"vSigma")
        sizePolicy2.setHeightForWidth(self.vSigma.sizePolicy().hasHeightForWidth())
        self.vSigma.setSizePolicy(sizePolicy2)

        self.formLayout.setWidget(13, QFormLayout.FieldRole, self.vSigma)

        self.initialVolumeLabel = QLabel(inputTitrationOpt)
        self.initialVolumeLabel.setObjectName(u"initialVolumeLabel")

        self.formLayout.setWidget(14, QFormLayout.LabelRole, self.initialVolumeLabel)

        self.initialVolume = CustomSpinBox(inputTitrationOpt)
        self.initialVolume.setObjectName(u"initialVolume")

        self.formLayout.setWidget(14, QFormLayout.FieldRole, self.initialVolume)

        self.line_3 = QFrame(inputTitrationOpt)
        self.line_3.setObjectName(u"line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.formLayout.setWidget(15, QFormLayout.SpanningRole, self.line_3)

        self.label_6 = QLabel(inputTitrationOpt)
        self.label_6.setObjectName(u"label_6")

        self.formLayout.setWidget(16, QFormLayout.SpanningRole, self.label_6)

        self.c0back_label = QLabel(inputTitrationOpt)
        self.c0back_label.setObjectName(u"c0back_label")
        self.c0back_label.setEnabled(False)

        self.formLayout.setWidget(17, QFormLayout.LabelRole, self.c0back_label)

        self.c0back = CustomSpinBox(inputTitrationOpt)
        self.c0back.setObjectName(u"c0back")
        self.c0back.setEnabled(False)
        self.c0back.setDecimals(5)
        self.c0back.setMaximum(900.000000000000000)
        self.c0back.setSingleStep(0.050000000000000)

        self.formLayout.setWidget(17, QFormLayout.FieldRole, self.c0back)

        self.ctback_label = QLabel(inputTitrationOpt)
        self.ctback_label.setObjectName(u"ctback_label")
        self.ctback_label.setEnabled(False)

        self.formLayout.setWidget(18, QFormLayout.LabelRole, self.ctback_label)

        self.ctback = CustomSpinBox(inputTitrationOpt)
        self.ctback.setObjectName(u"ctback")
        self.ctback.setEnabled(False)
        self.ctback.setDecimals(5)
        self.ctback.setMaximum(900.000000000000000)
        self.ctback.setSingleStep(0.050000000000000)

        self.formLayout.setWidget(18, QFormLayout.FieldRole, self.ctback)

        self.electroActiveComponentLabel = QLabel(inputTitrationOpt)
        self.electroActiveComponentLabel.setObjectName(u"electroActiveComponentLabel")

        self.formLayout.setWidget(10, QFormLayout.LabelRole, self.electroActiveComponentLabel)

        self.slopeLabel = QLabel(inputTitrationOpt)
        self.slopeLabel.setObjectName(u"slopeLabel")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.slopeLabel)

        self.slope = CustomSpinBox(inputTitrationOpt)
        self.slope.setObjectName(u"slope")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.slope)

        self.jaLabel = QLabel(inputTitrationOpt)
        self.jaLabel.setObjectName(u"jaLabel")

        self.formLayout.setWidget(7, QFormLayout.LabelRole, self.jaLabel)

        self.ja = CustomSpinBox(inputTitrationOpt)
        self.ja.setObjectName(u"ja")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.ja)

        self.jbLabel = QLabel(inputTitrationOpt)
        self.jbLabel.setObjectName(u"jbLabel")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.jbLabel)

        self.jb = CustomSpinBox(inputTitrationOpt)
        self.jb.setObjectName(u"jb")

        self.formLayout.setWidget(8, QFormLayout.FieldRole, self.jb)

        self.titrationName = QLineEdit(inputTitrationOpt)
        self.titrationName.setObjectName(u"titrationName")

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.titrationName)

        self.titrationNameLabel = QLabel(inputTitrationOpt)
        self.titrationNameLabel.setObjectName(u"titrationNameLabel")

        self.formLayout.setWidget(0, QFormLayout.SpanningRole, self.titrationNameLabel)


        self.horizontalLayout.addLayout(self.formLayout)

        self.titrationLayout = QVBoxLayout()
        self.titrationLayout.setObjectName(u"titrationLayout")
        self.titration_label = QLabel(inputTitrationOpt)
        self.titration_label.setObjectName(u"titration_label")

        self.titrationLayout.addWidget(self.titration_label)

        self.titrationView = QTableView(inputTitrationOpt)
        self.titrationView.setObjectName(u"titrationView")

        self.titrationLayout.addWidget(self.titrationView)


        self.horizontalLayout.addLayout(self.titrationLayout)

        self.concLayout = QVBoxLayout()
        self.concLayout.setObjectName(u"concLayout")
        self.conc_label = QLabel(inputTitrationOpt)
        self.conc_label.setObjectName(u"conc_label")

        self.concLayout.addWidget(self.conc_label)

        self.concView = QTableView(inputTitrationOpt)
        self.concView.setObjectName(u"concView")

        self.concLayout.addWidget(self.concView)


        self.horizontalLayout.addLayout(self.concLayout)

        self.horizontalLayout.setStretch(2, 1)

        self.retranslateUi(inputTitrationOpt)

        QMetaObject.connectSlotsByName(inputTitrationOpt)
    # setupUi

    def retranslateUi(self, inputTitrationOpt):
        inputTitrationOpt.setWindowTitle(QCoreApplication.translate("inputTitrationOpt", u"Form", None))
        self.importDataLabel.setText(QCoreApplication.translate("inputTitrationOpt", u"Import Data", None))
        self.importDataButton.setText(QCoreApplication.translate("inputTitrationOpt", u"Import", None))
        self.label_7.setText(QCoreApplication.translate("inputTitrationOpt", u"<html><head/><body><p><span style=\" font-weight:600;\">Electrode Options:</span></p></body></html>", None))
        self.e0Label.setText(QCoreApplication.translate("inputTitrationOpt", u"E0", None))
        self.eSigmaLabel.setText(QCoreApplication.translate("inputTitrationOpt", u"E Sigma", None))
        self.label_8.setText(QCoreApplication.translate("inputTitrationOpt", u"<html><head/><body><p><span style=\" font-weight:600;\">Vessel Options:</span></p></body></html>", None))
        self.vSigmaLabel.setText(QCoreApplication.translate("inputTitrationOpt", u"V Sigma", None))
        self.initialVolumeLabel.setText(QCoreApplication.translate("inputTitrationOpt", u"Initial Volume", None))
        self.label_6.setText(QCoreApplication.translate("inputTitrationOpt", u"<html><head/><body><p><span style=\" font-weight:600;\">Background Ions Settings:</span></p></body></html>", None))
        self.c0back_label.setText(QCoreApplication.translate("inputTitrationOpt", u"Initial C:", None))
#if QT_CONFIG(statustip)
        self.c0back.setStatusTip(QCoreApplication.translate("inputTitrationOpt", u"Initial concentration of background ions in titration vessel.", None))
#endif // QT_CONFIG(statustip)
        self.c0back.setSuffix(QCoreApplication.translate("inputTitrationOpt", u" mol/l", None))
        self.ctback_label.setText(QCoreApplication.translate("inputTitrationOpt", u"Titrant C:", None))
#if QT_CONFIG(statustip)
        self.ctback.setStatusTip(QCoreApplication.translate("inputTitrationOpt", u"Concentration of background ions in the titrant.", None))
#endif // QT_CONFIG(statustip)
        self.ctback.setSuffix(QCoreApplication.translate("inputTitrationOpt", u" mol/l", None))
        self.electroActiveComponentLabel.setText(QCoreApplication.translate("inputTitrationOpt", u"Electro Active Component", None))
        self.slopeLabel.setText(QCoreApplication.translate("inputTitrationOpt", u"Slope", None))
        self.jaLabel.setText(QCoreApplication.translate("inputTitrationOpt", u"Ja", None))
        self.jbLabel.setText(QCoreApplication.translate("inputTitrationOpt", u"Jb", None))
        self.titrationNameLabel.setText(QCoreApplication.translate("inputTitrationOpt", u"<html><head/><body><p><span style=\" font-weight:600;\">Titration Name:</span></p></body></html>", None))
        self.titration_label.setText(QCoreApplication.translate("inputTitrationOpt", u"<html><head/><body><p><span style=\" font-weight:700;\">Titration:</span></p></body></html>", None))
        self.conc_label.setText(QCoreApplication.translate("inputTitrationOpt", u"<html><head/><body><p><span style=\" font-weight:700;\">Concentrations:</span></p></body></html>", None))
    # retranslateUi

