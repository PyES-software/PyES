# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_about.ui'
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
    QDialog,
    QDialogButtonBox,
    QLabel,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class Ui_dialogAbout(object):
    def setupUi(self, dialogAbout):
        if not dialogAbout.objectName():
            dialogAbout.setObjectName("dialogAbout")
        dialogAbout.resize(471, 298)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Maximum, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(dialogAbout.sizePolicy().hasHeightForWidth())
        dialogAbout.setSizePolicy(sizePolicy)
        dialogAbout.setMinimumSize(QSize(471, 298))
        dialogAbout.setMaximumSize(QSize(471, 298))
        self.verticalLayout = QVBoxLayout(dialogAbout)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QLabel(dialogAbout)
        self.label.setObjectName("label")

        self.verticalLayout.addWidget(self.label)

        self.label_3 = QLabel(dialogAbout)
        self.label_3.setObjectName("label_3")
        sizePolicy1 = QSizePolicy(
            QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum
        )
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy1)
        self.label_3.setWordWrap(True)
        self.label_3.setOpenExternalLinks(True)
        self.label_3.setTextInteractionFlags(
            Qt.LinksAccessibleByMouse | Qt.TextSelectableByMouse
        )

        self.verticalLayout.addWidget(self.label_3)

        self.dialogButtonBox = QDialogButtonBox(dialogAbout)
        self.dialogButtonBox.setObjectName("dialogButtonBox")
        self.dialogButtonBox.setOrientation(Qt.Horizontal)
        self.dialogButtonBox.setStandardButtons(QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.dialogButtonBox)

        self.retranslateUi(dialogAbout)
        self.dialogButtonBox.accepted.connect(dialogAbout.accept)
        self.dialogButtonBox.rejected.connect(dialogAbout.reject)

        QMetaObject.connectSlotsByName(dialogAbout)

    # setupUi

    def retranslateUi(self, dialogAbout):
        dialogAbout.setWindowTitle(
            QCoreApplication.translate("dialogAbout", "About", None)
        )
        self.label.setText(
            QCoreApplication.translate("dialogAbout", "PyES Version 2.0.7beta", None)
        )
        self.label_3.setText(
            QCoreApplication.translate(
                "dialogAbout",
                '<html><head/><body><p>PyES is a sotware created by the chemistry department of the University of Turin in collabration with the University of Messina and the University of Bialystok.</p><p>Based on the previous work of Professor Sammartano of the University of Messina, PyES aims to empower researchers with the ability to easly compute species distribution and simulate titration curves even for complex systems.</p><p>PyES is licensed under GPL3 and its source code is aviable on its entirety on <a href="https://github.com/Kastakin/PyES"><span style=" text-decoration: underline; color:#0000ff;">GitHub</span></a>.</p></body></html>',
                None,
            )
        )

    # retranslateUi
