# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_multipleRangeSelector.ui'
##
## Created by: Qt User Interface Compiler version 6.4.3
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
    QGridLayout,
    QLabel,
    QLayout,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)

from ui.widgets.spinbox import CustomSpinBox


class Ui_multipleRangeSelector(object):
    def setupUi(self, multipleRangeSelector):
        if not multipleRangeSelector.objectName():
            multipleRangeSelector.setObjectName("multipleRangeSelector")
        multipleRangeSelector.resize(626, 478)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(
            multipleRangeSelector.sizePolicy().hasHeightForWidth()
        )
        multipleRangeSelector.setSizePolicy(sizePolicy)
        self.verticalLayout_2 = QVBoxLayout(multipleRangeSelector)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout.setSizeConstraint(QLayout.SetDefaultConstraint)
        self.rangeLabel1 = QLabel(multipleRangeSelector)
        self.rangeLabel1.setObjectName("rangeLabel1")
        self.rangeLabel1.setAlignment(Qt.AlignCenter)

        self.gridLayout.addWidget(self.rangeLabel1, 0, 0, 1, 1)

        self.lowerBound1 = CustomSpinBox(multipleRangeSelector)
        self.lowerBound1.setObjectName("lowerBound1")

        self.gridLayout.addWidget(self.lowerBound1, 0, 1, 1, 1)

        self.upperBound1 = CustomSpinBox(multipleRangeSelector)
        self.upperBound1.setObjectName("upperBound1")

        self.gridLayout.addWidget(self.upperBound1, 0, 2, 1, 1)

        self.gridLayout.setColumnStretch(0, 1)
        self.gridLayout.setColumnStretch(1, 2)
        self.gridLayout.setColumnStretch(2, 2)

        self.verticalLayout_2.addLayout(self.gridLayout)

        self.verticalLayout_2.setStretch(0, 1)

        self.retranslateUi(multipleRangeSelector)

        QMetaObject.connectSlotsByName(multipleRangeSelector)

    # setupUi

    def retranslateUi(self, multipleRangeSelector):
        multipleRangeSelector.setWindowTitle(
            QCoreApplication.translate("multipleRangeSelector", "Form", None)
        )
        self.rangeLabel1.setText(
            QCoreApplication.translate("multipleRangeSelector", "1", None)
        )

    # retranslateUi
