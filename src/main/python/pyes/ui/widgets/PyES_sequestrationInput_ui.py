# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_sequestrationInput.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

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
    QSizePolicy,
    QSpacerItem,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from ui.widgets import CustomComboBox
from ui.widgets.spinbox import CustomSpinBox


class Ui_Form(object):
    def setupUi(self, Form):
        if not Form.objectName():
            Form.setObjectName("Form")
        Form.resize(943, 601)
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(Form)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QFrame(Form)
        self.frame_2.setObjectName("frame_2")
        sizePolicy1 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Maximum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.frame_2.sizePolicy().hasHeightForWidth())
        self.frame_2.setSizePolicy(sizePolicy1)
        self.frame_2.setMinimumSize(QSize(284, 0))
        self.frame_2.setFrameShape(QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QFrame.Raised)
        self.formLayout_2 = QFormLayout(self.frame_2)
        self.formLayout_2.setObjectName("formLayout_2")
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

        self.formLayout_2.setWidget(2, QFormLayout.LabelRole, self.initialLog_label)

        self.initialLog = CustomSpinBox(self.frame_2)
        self.initialLog.setObjectName("initialLog")
        self.initialLog.setDecimals(3)
        self.initialLog.setMaximum(900.000000000000000)
        self.initialLog.setSingleStep(0.050000000000000)

        self.formLayout_2.setWidget(2, QFormLayout.FieldRole, self.initialLog)

        self.finalLog_label = QLabel(self.frame_2)
        self.finalLog_label.setObjectName("finalLog_label")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.finalLog_label)

        self.finalLog = CustomSpinBox(self.frame_2)
        self.finalLog.setObjectName("finalLog")
        self.finalLog.setDecimals(3)
        self.finalLog.setMaximum(900.000000000000000)
        self.finalLog.setSingleStep(0.050000000000000)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.finalLog)

        self.logInc_label = QLabel(self.frame_2)
        self.logInc_label.setObjectName("logInc_label")

        self.formLayout_2.setWidget(4, QFormLayout.LabelRole, self.logInc_label)

        self.logInc = CustomSpinBox(self.frame_2)
        self.logInc.setObjectName("logInc")
        self.logInc.setDecimals(3)
        self.logInc.setMaximum(900.000000000000000)
        self.logInc.setSingleStep(0.050000000000000)

        self.formLayout_2.setWidget(4, QFormLayout.FieldRole, self.logInc)

        self.line_3 = QFrame(self.frame_2)
        self.line_3.setObjectName("line_3")
        self.line_3.setFrameShape(QFrame.HLine)
        self.line_3.setFrameShadow(QFrame.Sunken)

        self.formLayout_2.setWidget(5, QFormLayout.SpanningRole, self.line_3)

        self.label_16 = QLabel(self.frame_2)
        self.label_16.setObjectName("label_16")

        self.formLayout_2.setWidget(6, QFormLayout.SpanningRole, self.label_16)

        self.cback_label = QLabel(self.frame_2)
        self.cback_label.setObjectName("cback_label")
        self.cback_label.setEnabled(False)

        self.formLayout_2.setWidget(7, QFormLayout.LabelRole, self.cback_label)

        self.cback = CustomSpinBox(self.frame_2)
        self.cback.setObjectName("cback")
        self.cback.setEnabled(False)
        self.cback.setDecimals(5)
        self.cback.setMaximum(900.000000000000000)
        self.cback.setSingleStep(0.050000000000000)

        self.formLayout_2.setWidget(7, QFormLayout.FieldRole, self.cback)

        self.verticalLayout_2.addWidget(self.frame_2)

        self.verticalSpacer = QSpacerItem(
            20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding
        )

        self.verticalLayout_2.addItem(self.verticalSpacer)

        self.horizontalLayout_2.addLayout(self.verticalLayout_2)

        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.concView = QTableView(Form)
        self.concView.setObjectName("concView")

        self.verticalLayout.addWidget(self.concView)

        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.horizontalLayout_2.setStretch(1, 1)

        self.retranslateUi(Form)

        QMetaObject.connectSlotsByName(Form)

    # setupUi

    def retranslateUi(self, Form):
        Form.setWindowTitle(QCoreApplication.translate("Form", "Form", None))
        self.label_9.setText(
            QCoreApplication.translate(
                "Form",
                '<html><head/><body><p><span style=" font-weight:600;">Ligand of Interest Settings:</span></p></body></html>',
                None,
            )
        )
        self.indComp_label.setText(QCoreApplication.translate("Form", "Ligand:", None))
        # if QT_CONFIG(statustip)
        self.indComp.setStatusTip(
            QCoreApplication.translate(
                "Form", "Component to be considered indipendent.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.initialLog_label.setText(
            QCoreApplication.translate("Form", "Initial -log[A]:", None)
        )
        # if QT_CONFIG(statustip)
        self.initialLog.setStatusTip(
            QCoreApplication.translate(
                "Form", "Initial Log value of the indipendent component.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.finalLog_label.setText(
            QCoreApplication.translate("Form", "Final -log[A]", None)
        )
        # if QT_CONFIG(statustip)
        self.finalLog.setStatusTip(
            QCoreApplication.translate(
                "Form", "Final Log value of the indipendent component.", None
            )
        )
        # endif // QT_CONFIG(statustip)
        self.logInc_label.setText(
            QCoreApplication.translate("Form", "-log[A] Increment:", None)
        )
        # if QT_CONFIG(statustip)
        self.logInc.setStatusTip(
            QCoreApplication.translate(
                "Form",
                "Log increment of the indipendent component at each point.",
                None,
            )
        )
        # endif // QT_CONFIG(statustip)
        self.label_16.setText(
            QCoreApplication.translate(
                "Form",
                '<html><head/><body><p><span style=" font-weight:600;">Background Ions Settings:</span></p></body></html>',
                None,
            )
        )
        self.cback_label.setText(
            QCoreApplication.translate("Form", "Concentration:", None)
        )
        # if QT_CONFIG(tooltip)
        self.cback.setToolTip(
            QCoreApplication.translate(
                "Form",
                "Sum of the concentrations of ionic species that do not take part in the reactions.",
                None,
            )
        )
        # endif // QT_CONFIG(tooltip)
        # if QT_CONFIG(statustip)
        self.cback.setStatusTip(
            QCoreApplication.translate(
                "Form",
                "Sum of the concentrations of ionic species that do not take part in the reactions.",
                None,
            )
        )
        # endif // QT_CONFIG(statustip)
        self.cback.setSuffix(QCoreApplication.translate("Form", " mol/l", None))

    # retranslateUi
