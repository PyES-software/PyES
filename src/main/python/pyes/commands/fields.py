import re

from PySide6.QtCore import QAbstractItemModel
from PySide6.QtGui import QUndoCommand
from PySide6.QtWidgets import (
    QCheckBox,
    QComboBox,
    QDoubleSpinBox,
    QLabel,
    QStackedWidget,
    QTableView,
    QTabWidget,
    QWidget,
)

from utils_func import get_widgets_from_tab


class DoubleSpinBoxEdit(QUndoCommand):
    def __init__(self, field: QDoubleSpinBox, value: float):
        QUndoCommand.__init__(self)
        self.field = field
        self.previous_value = field.previous_value
        self.new_value = value

    def undo(self) -> None:
        self.field.blockSignals(True)
        self.field.setValue(self.previous_value)
        self.field.blockSignals(False)

    def redo(self) -> None:
        self.field.blockSignals(True)
        self.field.setValue(self.new_value)
        self.field.blockSignals(False)


class uncertaintyEdit(QUndoCommand):
    def __init__(
        self, field: QCheckBox, state: bool, affected_models: list[QAbstractItemModel]
    ):
        QUndoCommand.__init__(self)
        self.field = field
        self.state = state
        self.previous_state = not state
        self.affected_models = affected_models

    def undo(self) -> None:
        for model in self.affected_models[:2]:
            model.setColumnReadOnly([3], not self.previous_state)
            model.setColumnReadOnly([3], not self.previous_state)
        self.affected_models[-1].setColumnReadOnly([2, 3], not self.previous_state)

        self.field.blockSignals(True)
        self.field.setChecked(self.previous_state)
        self.field.blockSignals(False)

    def redo(self) -> None:
        for model in self.affected_models[:2]:
            model.setColumnReadOnly([3], not self.state)
            model.setColumnReadOnly([3], not self.state)
        self.affected_models[-1].setColumnReadOnly([2, 3], not self.state)

        self.field.blockSignals(True)
        self.field.setChecked(self.state)
        self.field.blockSignals(False)


class indCompEdit(QUndoCommand):
    def __init__(
        self,
        field: QComboBox,
        index: int,
        affected_labels: list[QLabel],
        conc_model: QAbstractItemModel,
        dmode: QComboBox,
    ):
        QUndoCommand.__init__(self)
        self.field = field
        self.affected_labels = affected_labels
        self.index = index
        self.previous_index = field.previous_index
        self.value = field.itemText(self.index)
        self.previous_value = field.itemText(self.previous_index)
        self.conc_model = conc_model
        self.dmode = dmode.currentIndex()

    def undo(self) -> None:
        self.conc_model.showAllRows()
        if self.dmode == 1:
            self.conc_model.setRowReadOnly([self.previous_index], True)
        self.conc_model.setPreviousIndependentComponent(self.previous_index)

        for label in self.affected_labels:
            label.setText(
                re.sub(
                    "\[\w+\]",
                    f"[{self.field.itemText(self.previous_index)}]",
                    label.text(),
                )
            )

        self.field.blockSignals(True)
        self.field.setCurrentIndex(self.previous_index)
        self.field.blockSignals(False)

    def redo(self) -> None:
        self.conc_model.showAllRows()
        if self.dmode == 1:
            self.conc_model.setRowReadOnly([self.index], True)
        self.conc_model.setPreviousIndependentComponent(self.index)

        for label in self.affected_labels:
            label.setText(
                re.sub(
                    "\[\w+\]",
                    f"[{self.field.itemText(self.index)}]",
                    label.text(),
                )
            )

        self.field.blockSignals(True)
        self.field.setCurrentIndex(self.index)
        self.field.blockSignals(False)


class dmodeEdit(QUndoCommand):
    def __init__(
        self,
        field: QComboBox,
        index: int,
        affected_fields: list[QStackedWidget],
        affected_table: QTableView,
    ):
        QUndoCommand.__init__(self)
        self.field = field
        self.index = index
        self.previous_index = field.previous_index
        self.affected_fields = affected_fields
        self.affected_table = affected_table

        if index == 0:
            self.to_hide = False
        else:
            self.to_hide = True

    def undo(self) -> None:
        self.show_stacked_widgets(self.previous_index)
        self.affected_table.setColumnHidden(1, not self.to_hide)
        self.affected_table.setColumnHidden(3, not self.to_hide)

        self.affected_table.model().setRowReadOnly(
            [self.affected_table.model().previous_ind_comp],
            (False if self.previous_index == 0 else True),
        )

        self.field.blockSignals(True)
        self.field.setCurrentIndex(self.previous_index)
        self.field.blockSignals(False)

    def redo(self) -> None:
        self.show_stacked_widgets(self.index)
        self.affected_table.setColumnHidden(1, self.to_hide)
        self.affected_table.setColumnHidden(3, self.to_hide)

        self.affected_table.model().setRowReadOnly(
            [self.affected_table.model().previous_ind_comp],
            (False if self.index == 0 else True),
        )

        self.field.blockSignals(True)
        self.field.setCurrentIndex(self.index)
        self.field.blockSignals(False)

    def show_stacked_widgets(self, index):
        if index > 1:
            self.affected_fields[1].setCurrentIndex(1)
        else:
            self.affected_fields[1].setCurrentIndex(0)
            if index == 0:
                self.affected_fields[0].setCurrentIndex(0)
            else:
                self.affected_fields[0].setCurrentIndex(1)


class imodeEdit(QUndoCommand):
    def __init__(
        self,
        field: QComboBox,
        affected_fields: list[QWidget],
        affected_models: list[QAbstractItemModel],
        titration_tabs: QTabWidget,
        index: int,
    ):

        QUndoCommand.__init__(self)
        self.field = field
        self.affected_fields = affected_fields
        self.affected_models = affected_models
        self.titration_tabs = titration_tabs
        self.index = index
        self.previous_index = field.previous_index
        self.state = bool(self.index)
        self.previous_state = bool(self.previous_index)

    def undo(self) -> None:
        from ui.widgets import CustomSpinBox
        for field in self.affected_fields:
            field.setEnabled(self.previous_state)

        for model in self.affected_models:
            model.setColumnReadOnly(range(4, 8), not self.previous_state)

        for c0back in get_widgets_from_tab(
            self.titration_tabs, CustomSpinBox, "c0back"
        ):
            c0back.setEnabled(self.state)

        for ctback in get_widgets_from_tab(
            self.titration_tabs, CustomSpinBox, "ctback"
        ):
            ctback.setEnabled(self.state)

        for c0back_label in get_widgets_from_tab(
            self.titration_tabs, QLabel, "c0back_label"
        ):
            c0back_label.setEnabled(self.state)

        for ctback_label in get_widgets_from_tab(
            self.titration_tabs, QLabel, "ctback_label"
        ):
            ctback_label.setEnabled(self.state)

        self.field.blockSignals(True)
        self.field.setCurrentIndex(self.previous_index)
        self.field.blockSignals(False)

    def redo(self) -> None:
        from ui.widgets import CustomSpinBox
        for field in self.affected_fields:
            field.setEnabled(self.state)

        for model in self.affected_models:
            model.setColumnReadOnly(range(4, 8), not self.state)

        for c0back in get_widgets_from_tab(
            self.titration_tabs, CustomSpinBox, "c0back"
        ):
            c0back.setEnabled(self.state)

        for ctback in get_widgets_from_tab(
            self.titration_tabs, CustomSpinBox, "ctback"
        ):
            ctback.setEnabled(self.state)

        for c0back_label in get_widgets_from_tab(
            self.titration_tabs, QLabel, "c0back_label"
        ):
            c0back_label.setEnabled(self.state)

        for ctback_label in get_widgets_from_tab(
            self.titration_tabs, QLabel, "ctback_label"
        ):
            ctback_label.setEnabled(self.state)

        self.field.blockSignals(True)
        self.field.setCurrentIndex(self.index)
        self.field.blockSignals(False)
