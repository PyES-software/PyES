# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_uncertaintyInfo.ui'
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
from PySide6.QtSvgWidgets import QSvgWidget
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QGridLayout, QLabel, QSizePolicy, QWidget)

class Ui_UncertaintyInfoDialog(object):
    def setupUi(self, UncertaintyInfoDialog):
        if not UncertaintyInfoDialog.objectName():
            UncertaintyInfoDialog.setObjectName(u"UncertaintyInfoDialog")
        UncertaintyInfoDialog.resize(930, 515)
        UncertaintyInfoDialog.setMinimumSize(QSize(930, 515))
        self.gridLayout = QGridLayout(UncertaintyInfoDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(UncertaintyInfoDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 4, 0, 1, 2)

        self.widget = QSvgWidget(UncertaintyInfoDialog)
        self.widget.setObjectName(u"widget")

        self.gridLayout.addWidget(self.widget, 1, 0, 1, 2)

        self.label = QLabel(UncertaintyInfoDialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.widget_2 = QSvgWidget(UncertaintyInfoDialog)
        self.widget_2.setObjectName(u"widget_2")

        self.gridLayout.addWidget(self.widget_2, 2, 0, 1, 2)

        self.widget_3 = QSvgWidget(UncertaintyInfoDialog)
        self.widget_3.setObjectName(u"widget_3")

        self.gridLayout.addWidget(self.widget_3, 3, 0, 1, 2)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(4, 1)

        self.retranslateUi(UncertaintyInfoDialog)
        self.buttonBox.accepted.connect(UncertaintyInfoDialog.accept)
        self.buttonBox.rejected.connect(UncertaintyInfoDialog.reject)

        QMetaObject.connectSlotsByName(UncertaintyInfoDialog)
    # setupUi

    def retranslateUi(self, UncertaintyInfoDialog):
        UncertaintyInfoDialog.setWindowTitle(QCoreApplication.translate("UncertaintyInfoDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("UncertaintyInfoDialog", u"<html><head/><body><p>The uncertainty on the concentration obtained as results can be calculated given the uncertainty on the input data (analytical concentration and thermodynamic constants) using the following equations:</p></body></html>", None))
    # retranslateUi

