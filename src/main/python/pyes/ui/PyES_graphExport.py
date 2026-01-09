# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_graphExport.ui'
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDialog, QDoubleSpinBox,
    QFormLayout, QFrame, QLabel, QPushButton,
    QSizePolicy, QWidget)

from ui.widgets import ColorButton

class Ui_ExportGraphDialog(object):
    def setupUi(self, ExportGraphDialog):
        if not ExportGraphDialog.objectName():
            ExportGraphDialog.setObjectName(u"ExportGraphDialog")
        ExportGraphDialog.setMinimumSize(QSize(264, 158))
        ExportGraphDialog.setMaximumSize(QSize(264, 158))
        self.formLayout_2 = QFormLayout(ExportGraphDialog)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.formLayout_2.setFieldGrowthPolicy(QFormLayout.FieldGrowthPolicy.ExpandingFieldsGrow)
        self.formLayout_2.setLabelAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.backgroundLabel = QLabel(ExportGraphDialog)
        self.backgroundLabel.setObjectName(u"backgroundLabel")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.backgroundLabel)

        self.background = ColorButton(ExportGraphDialog)
        self.background.setObjectName(u"background")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.background.sizePolicy().hasHeightForWidth())
        self.background.setSizePolicy(sizePolicy)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.background)

        self.scaleLabel = QLabel(ExportGraphDialog)
        self.scaleLabel.setObjectName(u"scaleLabel")

        self.formLayout_2.setWidget(3, QFormLayout.LabelRole, self.scaleLabel)

        self.export_button = QPushButton(ExportGraphDialog)
        self.export_button.setObjectName(u"export_button")
        self.export_button.setEnabled(True)
        self.export_button.setAutoDefault(False)
        self.export_button.setFlat(False)

        self.formLayout_2.setWidget(4, QFormLayout.SpanningRole, self.export_button)

        self.scaleDoubleSpinBox = QDoubleSpinBox(ExportGraphDialog)
        self.scaleDoubleSpinBox.setObjectName(u"scaleDoubleSpinBox")
        sizePolicy.setHeightForWidth(self.scaleDoubleSpinBox.sizePolicy().hasHeightForWidth())
        self.scaleDoubleSpinBox.setSizePolicy(sizePolicy)
        self.scaleDoubleSpinBox.setMaximum(100.000000000000000)
        self.scaleDoubleSpinBox.setSingleStep(0.050000000000000)
        self.scaleDoubleSpinBox.setValue(1.000000000000000)

        self.formLayout_2.setWidget(3, QFormLayout.FieldRole, self.scaleDoubleSpinBox)

        self.line = QFrame(ExportGraphDialog)
        self.line.setObjectName(u"line")
        self.line.setFrameShape(QFrame.Shape.HLine)
        self.line.setFrameShadow(QFrame.Shadow.Sunken)

        self.formLayout_2.setWidget(2, QFormLayout.SpanningRole, self.line)

        self.transparent_check = QCheckBox(ExportGraphDialog)
        self.transparent_check.setObjectName(u"transparent_check")

        self.formLayout_2.setWidget(0, QFormLayout.SpanningRole, self.transparent_check)


        self.retranslateUi(ExportGraphDialog)

        self.export_button.setDefault(False)


        QMetaObject.connectSlotsByName(ExportGraphDialog)
    # setupUi

    def retranslateUi(self, ExportGraphDialog):
        ExportGraphDialog.setWindowTitle(QCoreApplication.translate("ExportGraphDialog", u"Export Options", None))
        self.backgroundLabel.setText(QCoreApplication.translate("ExportGraphDialog", u"Background", None))
        self.background.setText("")
        self.scaleLabel.setText(QCoreApplication.translate("ExportGraphDialog", u"Scale", None))
        self.export_button.setText(QCoreApplication.translate("ExportGraphDialog", u"Export", None))
        self.transparent_check.setText(QCoreApplication.translate("ExportGraphDialog", u"Transparent Background?", None))
    # retranslateUi

