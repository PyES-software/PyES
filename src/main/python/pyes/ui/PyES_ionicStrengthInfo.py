# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_ionicStrengthInfo.ui'
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

class Ui_IonicStrengthInfoDialog(object):
    def setupUi(self, IonicStrengthInfoDialog):
        if not IonicStrengthInfoDialog.objectName():
            IonicStrengthInfoDialog.setObjectName(u"IonicStrengthInfoDialog")
        IonicStrengthInfoDialog.resize(930, 515)
        IonicStrengthInfoDialog.setMinimumSize(QSize(930, 515))
        self.gridLayout = QGridLayout(IonicStrengthInfoDialog)
        self.gridLayout.setObjectName(u"gridLayout")
        self.buttonBox = QDialogButtonBox(IonicStrengthInfoDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.gridLayout.addWidget(self.buttonBox, 5, 0, 1, 2)

        self.label = QLabel(IonicStrengthInfoDialog)
        self.label.setObjectName(u"label")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label.setWordWrap(True)

        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)

        self.widget = QSvgWidget(IonicStrengthInfoDialog)
        self.widget.setObjectName(u"widget")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.widget.sizePolicy().hasHeightForWidth())
        self.widget.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.widget, 1, 0, 1, 2)

        self.label_2 = QLabel(IonicStrengthInfoDialog)
        self.label_2.setObjectName(u"label_2")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy2)
        self.label_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.label_2.setWordWrap(True)

        self.gridLayout.addWidget(self.label_2, 2, 0, 3, 1)

        self.widget_2 = QSvgWidget(IonicStrengthInfoDialog)
        self.widget_2.setObjectName(u"widget_2")
        sizePolicy1.setHeightForWidth(self.widget_2.sizePolicy().hasHeightForWidth())
        self.widget_2.setSizePolicy(sizePolicy1)

        self.gridLayout.addWidget(self.widget_2, 2, 1, 3, 1)

        self.gridLayout.setRowStretch(0, 1)
        self.gridLayout.setRowStretch(3, 1)
        self.gridLayout.setRowStretch(4, 1)

        self.retranslateUi(IonicStrengthInfoDialog)
        self.buttonBox.accepted.connect(IonicStrengthInfoDialog.accept)
        self.buttonBox.rejected.connect(IonicStrengthInfoDialog.reject)

        QMetaObject.connectSlotsByName(IonicStrengthInfoDialog)
    # setupUi

    def retranslateUi(self, IonicStrengthInfoDialog):
        IonicStrengthInfoDialog.setWindowTitle(QCoreApplication.translate("IonicStrengthInfoDialog", u"Dialog", None))
        self.label.setText(QCoreApplication.translate("IonicStrengthInfoDialog", u"<html><head/><body><p>The effect of ionic strength on the formation constants of soluble and precipitable species can be expressed applying a correction factor originated from the <span style=\" background-color:transparent;\">Debye-H\u00fcckel that can be used to estimate the value of the activity coefficient of the components in the system:</span></p></body></html>", None))
        self.label_2.setText(QCoreApplication.translate("IonicStrengthInfoDialog", u"<html><head/><body><p>A and B are the so-called Debye-H\u00fcckel parameters (A = 0.51 and B = 1.5 at T=298.15 K) and C , D and E are empirical parameters (the E term can generally be neglected for I\u22641.0 mol dm<span style=\" vertical-align:super;\">-3</span>).</p><p>I<span style=\" vertical-align:sub;\">1</span> and I<span style=\" vertical-align:sub;\">2 </span>are the ionic strength values of the current point and the one for which the thermodynamic constant is given respectively. </p><p>The empirical terms (also know as &quot;expansion terms&quot;) are defined through the equations presented on the right:</p></body></html>", None))
    # retranslateUi

