from PySide6.QtCore import QEvent, QObject, QPoint, QRect, Qt, QTimer
from PySide6.QtWidgets import (
    QAbstractItemDelegate,
    QApplication,
    QColorDialog,
    QComboBox,
    QLineEdit,
    QStyle,
    QStyledItemDelegate,
    QStyleOptionButton,
    QStyleOptionComboBox,
    QStyleOptionViewItem,
)


class NumberFormatDelegate(QStyledItemDelegate):
    def __init__(
        self,
        parent=None,
        bottom: float = -float("inf"),
        top: float = float("inf"),
        decimals: int = -1,
    ) -> None:
        super().__init__(parent)
        self.bottom = bottom
        self.top = top
        self.decimals = decimals

    def createEditor(self, parent, option, index):
        from ui.widgets.spinbox import LineSpinBox

        editor = LineSpinBox(
            parent,
            bottom=self.bottom,
            top=self.top,
            decimals=self.decimals,
        )
        return editor

    def setEditorData(self, editor, index):
        value = index.model().data(index, Qt.EditRole)
        if value is not None:
            editor.setText(str(value))
        else:
            editor.setText("")

    def setModelData(self, editor, model, index):
        text = editor.text()
        if text:  # or add validation if needed
            model.setData(index, text, Qt.EditRole)


class LineEditDelegate(QStyledItemDelegate):
    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)

    def createEditor(self, parent, option, index):
        editor = QLineEdit(parent=parent)
        return editor

    def setEditorData(self, editor, index):
        data = index.model().data(index, Qt.EditRole)
        editor.setText(data)

    def setModelData(self, editor, model, index):
        model.setData(index, editor.text(), Qt.EditRole)


class CheckBoxDelegate(QStyledItemDelegate):
    """
    A delegate that places a fully functioning QCheckBox in every
    cell of the column to which it's applied
    """

    def __init__(self, parent):
        QStyledItemDelegate.__init__(self, parent)
        self.parent = parent

    def createEditor(self, parent, option, index):
        """
        Important, otherwise an editor is created if the user clicks in this cell.
        ** Need to hook up a signal to the model
        """
        return None

    def paint(self, painter, option, index):
        """
        Paint a checkbox without the label.
        """

        checked = index.data()  # .toBool()
        check_box_style_option = QStyleOptionButton()

        if (index.flags() & Qt.ItemFlag.ItemIsEditable):  # != False:
            check_box_style_option.state |= QStyle.State_Enabled
        else:
            check_box_style_option.state |= QStyle.State_ReadOnly

        if checked:
            check_box_style_option.state |= QStyle.State_On
        else:
            check_box_style_option.state |= QStyle.State_Off

        check_box_style_option.rect = self.getCheckBoxRect(option)

        # if not index.model().hasFlag(index, Qt.ItemIsEditable):
        # check_box_style_option.state |= QtGui.#QStyle.State_ReadOnly

        check_box_style_option.state |= QStyle.State_Enabled

        QApplication.style().drawControl(
            QStyle.CE_CheckBox, check_box_style_option, painter
        )

    def editorEvent(self, event, model, option, index):
        """
        Change the data in the model and the state of the checkbox
        if the user presses the left mousebutton or presses
        Key_Space or Key_Select and this cell is editable. Otherwise do nothing.
        """
        if not (index.flags() & Qt.ItemIsEditable) != 0:
            return False

        # Do not change the checkbox-state
        if event.type() == QEvent.MouseButtonPress:
            return False
        if (
            event.type() == QEvent.MouseButtonRelease
            or event.type() == QEvent.MouseButtonDblClick
        ):
            if event.button() != Qt.LeftButton or not self.getCheckBoxRect(
                option
            ).contains(event.pos()):
                return False
            if event.type() == QEvent.MouseButtonDblClick:
                return True
        elif event.type() == QEvent.KeyPress:
            if event.key() != Qt.Key_Space and event.key() != Qt.Key_Select:
                return False
            else:
                return False

        # Change the checkbox-state
        self.setModelData(None, model, index)
        return True

    def setModelData(self, editor, model, index):
        """
        The user wanted to change the old state in the opposite.
        """
        newValue = True if not index.data() else False
        model.setData(index, newValue, Qt.EditRole)

    def getCheckBoxRect(self, option):
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(
            QStyle.SE_CheckBoxIndicator, check_box_style_option, None
        )
        check_box_point = QPoint(
            option.rect.x() + option.rect.width() / 2 - check_box_rect.width() / 2,
            option.rect.y() + option.rect.height() / 2 - check_box_rect.height() / 2,
        )
        return QRect(check_box_point, check_box_rect.size())


class ComboBoxDelegate(QStyledItemDelegate):
    def __init__(self, view, choices, parent=None):
        QStyledItemDelegate.__init__(self, parent)
        self.items = choices
        self._view = view

    def createEditor(self, parent, option, index):
        self.editor = QComboBox(parent)
        self.editor.addItems(self.items)

        self.editor.activated.connect(
            lambda index, editor=self.editor: self._view.commitData(editor)
        )
        self.editor.activated.connect(
            lambda index, editor=self.editor: self._view.closeEditor(
                editor, QAbstractItemDelegate.NoHint
            )
        )
        QTimer.singleShot(10, self.editor.showPopup)
        return self.editor

    def paint(self, painter, option, index):
        value = index.data(Qt.DisplayRole)
        style = QApplication.style()
        opt = QStyleOptionComboBox()
        opt.text = str(value)
        opt.rect = option.rect
        style.drawComplexControl(QStyle.CC_ComboBox, opt, painter)
        QStyledItemDelegate.paint(self, painter, option, index)

    def setEditorData(self, editor, index):
        value = index.data(Qt.DisplayRole)
        num = self.items.index(value)
        editor.setCurrentIndex(num)

    def setModelData(self, editor, model, index):
        try:
            value = self.items[editor.currentIndex()]
            model.setData(index, value, Qt.EditRole)
        except Exception:
            pass

    def updateEditorGeometry(self, editor, option, index):
        editor.setGeometry(option.rect)


class ColorPickerDelegate(QStyledItemDelegate):
    def __init__(self, parent=None):
        QStyledItemDelegate.__init__(self, parent)

    def paint(self, painter, option, index):
        color = index.data(Qt.DisplayRole)

        style = QApplication.style()
        opt = QStyleOptionViewItem()
        opt.rect = option.rect

        painter.save()
        painter.fillRect(option.rect, color)
        painter.restore()

        style.drawControl(QStyle.CE_PushButton, opt, painter)

    def createEditor(self, parent, option, index):
        dialog = QColorDialog(parent)
        dialog.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, False)
        dialog.setOption(QColorDialog.ColorDialogOption.DontUseNativeDialog, True)
        dialog.setModal(True)
        return dialog

    def setEditorData(self, editor, index):
        color = index.data(Qt.EditRole)
        editor.setCurrentColor(color)

    def setModelData(self, editor, model, index):
        color = editor.currentColor().name()
        model.setData(index, color, Qt.EditRole)
