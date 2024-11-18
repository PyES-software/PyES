# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'PyES_editDialog.ui'
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
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QDoubleSpinBox, QFormLayout, QHBoxLayout,
    QLabel, QLayout, QLineEdit, QSizePolicy,
    QSpinBox, QStackedWidget, QVBoxLayout, QWidget)

class Ui_EditColumnDialog(object):
    def setupUi(self, EditColumnDialog):
        if not EditColumnDialog.objectName():
            EditColumnDialog.setObjectName(u"EditColumnDialog")
        EditColumnDialog.setMinimumSize(QSize(353, 159))
        EditColumnDialog.setMaximumSize(QSize(353, 183))
        self.verticalLayout = QVBoxLayout(EditColumnDialog)
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(5, 5, 5, -1)
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setSizeConstraint(QLayout.SetMaximumSize)
        self.columnLabel = QLabel(EditColumnDialog)
        self.columnLabel.setObjectName(u"columnLabel")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.columnLabel)

        self.columnComboBox = QComboBox(EditColumnDialog)
        self.columnComboBox.setObjectName(u"columnComboBox")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.columnComboBox)

        self.label = QLabel(EditColumnDialog)
        self.label.setObjectName(u"label")

        self.formLayout.setWidget(1, QFormLayout.SpanningRole, self.label)

        self.stackedWidget = QStackedWidget(EditColumnDialog)
        self.stackedWidget.setObjectName(u"stackedWidget")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.stackedWidget.sizePolicy().hasHeightForWidth())
        self.stackedWidget.setSizePolicy(sizePolicy)
        self.stackedWidget.setLineWidth(0)
        self.choice_input = QWidget()
        self.choice_input.setObjectName(u"choice_input")
        sizePolicy.setHeightForWidth(self.choice_input.sizePolicy().hasHeightForWidth())
        self.choice_input.setSizePolicy(sizePolicy)
        self.horizontalLayout_2 = QHBoxLayout(self.choice_input)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.comboBox = QComboBox(self.choice_input)
        self.comboBox.setObjectName(u"comboBox")

        self.horizontalLayout_2.addWidget(self.comboBox)

        self.stackedWidget.addWidget(self.choice_input)
        self.string_input = QWidget()
        self.string_input.setObjectName(u"string_input")
        sizePolicy.setHeightForWidth(self.string_input.sizePolicy().hasHeightForWidth())
        self.string_input.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.string_input)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.lineEdit = QLineEdit(self.string_input)
        self.lineEdit.setObjectName(u"lineEdit")

        self.horizontalLayout.addWidget(self.lineEdit)

        self.stackedWidget.addWidget(self.string_input)
        self.integer_input = QWidget()
        self.integer_input.setObjectName(u"integer_input")
        sizePolicy.setHeightForWidth(self.integer_input.sizePolicy().hasHeightForWidth())
        self.integer_input.setSizePolicy(sizePolicy)
        self.horizontalLayout_3 = QHBoxLayout(self.integer_input)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.spinBox = QSpinBox(self.integer_input)
        self.spinBox.setObjectName(u"spinBox")
        self.spinBox.setMinimum(-99)

        self.horizontalLayout_3.addWidget(self.spinBox)

        self.stackedWidget.addWidget(self.integer_input)
        self.float_input = QWidget()
        self.float_input.setObjectName(u"float_input")
        sizePolicy.setHeightForWidth(self.float_input.sizePolicy().hasHeightForWidth())
        self.float_input.setSizePolicy(sizePolicy)
        self.horizontalLayout_4 = QHBoxLayout(self.float_input)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.doubleSpinBox = QDoubleSpinBox(self.float_input)
        self.doubleSpinBox.setObjectName(u"doubleSpinBox")
        self.doubleSpinBox.setLocale(QLocale(QLocale.English, QLocale.UnitedStates))
        self.doubleSpinBox.setDecimals(3)
        self.doubleSpinBox.setMinimum(-10000.000000000000000)
        self.doubleSpinBox.setMaximum(9999999999.000000000000000)

        self.horizontalLayout_4.addWidget(self.doubleSpinBox)

        self.stackedWidget.addWidget(self.float_input)

        self.formLayout.setWidget(2, QFormLayout.SpanningRole, self.stackedWidget)


        self.verticalLayout.addLayout(self.formLayout)

        self.buttonBox = QDialogButtonBox(EditColumnDialog)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)

        self.verticalLayout.addWidget(self.buttonBox)


        self.retranslateUi(EditColumnDialog)
        self.buttonBox.accepted.connect(EditColumnDialog.accept)
        self.buttonBox.rejected.connect(EditColumnDialog.reject)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(EditColumnDialog)
    # setupUi

    def retranslateUi(self, EditColumnDialog):
        EditColumnDialog.setWindowTitle(QCoreApplication.translate("EditColumnDialog", u"Edit column", None))
        self.columnLabel.setText(QCoreApplication.translate("EditColumnDialog", u"Column", None))
#if QT_CONFIG(tooltip)
        self.columnComboBox.setToolTip(QCoreApplication.translate("EditColumnDialog", u"Column to edit", None))
#endif // QT_CONFIG(tooltip)
        self.label.setText(QCoreApplication.translate("EditColumnDialog", u"New Value:", None))
    # retranslateUi

