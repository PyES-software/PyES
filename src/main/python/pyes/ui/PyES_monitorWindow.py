# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_monitorWindow.ui'
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QGridLayout, QHeaderView,
    QLabel, QSizePolicy, QTableWidget, QTableWidgetItem,
    QVBoxLayout, QWidget)

class Ui_MonitorWindow(object):
    def setupUi(self, MonitorWindow):
        if not MonitorWindow.objectName():
            MonitorWindow.setObjectName(u"MonitorWindow")
        MonitorWindow.resize(470, 617)
        MonitorWindow.setMinimumSize(QSize(470, 617))
        self.verticalLayout = QVBoxLayout(MonitorWindow)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(-1, 0, -1, -1)
        self.status = QLabel(MonitorWindow)
        self.status.setObjectName(u"status")
        self.status.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.gridLayout.addWidget(self.status, 0, 1, 1, 1)

        self.status_label = QLabel(MonitorWindow)
        self.status_label.setObjectName(u"status_label")

        self.gridLayout.addWidget(self.status_label, 0, 0, 1, 1)

        self.tableWidget = QTableWidget(MonitorWindow)
        self.tableWidget.setObjectName(u"tableWidget")
        self.tableWidget.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)

        self.gridLayout.addWidget(self.tableWidget, 2, 0, 1, 2)

        self.label = QLabel(MonitorWindow)
        self.label.setObjectName(u"label")

        self.gridLayout.addWidget(self.label, 1, 0, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout)


        self.retranslateUi(MonitorWindow)

        QMetaObject.connectSlotsByName(MonitorWindow)
    # setupUi

    def retranslateUi(self, MonitorWindow):
        MonitorWindow.setWindowTitle(QCoreApplication.translate("MonitorWindow", u"Result Monitor", None))
        self.status.setText(QCoreApplication.translate("MonitorWindow", u"Waiting", None))
        self.status_label.setText(QCoreApplication.translate("MonitorWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Status:</span></p></body></html>", None))
        self.label.setText(QCoreApplication.translate("MonitorWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Results:</span></p></body></html>", None))
    # retranslateUi

