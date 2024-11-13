from PySide6.QtGui import QUndoCommand, QUndoStack
from PySide6.QtWidgets import (
    QHBoxLayout,
    QTabBar,
    QTabWidget,
    QWidget,
    QTableWidget,
    QTableView,
)
from ui.widgets.combobox import CustomComboBox
from ui.widgets import inputTitrationOpt
from utils_func import apply_table_map, get_table_map, get_widgets_from_tab


class AddTab(QUndoCommand):
    def __init__(
        self,
        tab_widget: QTabWidget,
        undo_stack: QUndoStack,
        components: list[str],
        conc_to_refine: QTableWidget,
        electrode_to_refine: QTableWidget,
    ):
        QUndoCommand.__init__(self)
        self.tab_widget = tab_widget
        self.undo_stack = undo_stack
        self.components = components
        self.conc_to_refine = conc_to_refine
        self.electrode_to_refine = electrode_to_refine

        self.previous_conc_state = get_table_map(self.conc_to_refine)
        self.previous_electrode_state = get_table_map(self.electrode_to_refine)

        self.new_conc_state = [r + [False] for r in self.previous_conc_state]
        self.new_electrode_state = [r + [False] for r in self.previous_electrode_state]

    def undo(self) -> None:
        idx_to_remove = self.tab_widget.count() - 1
        removed_widget = self.tab_widget.widget(idx_to_remove)
        self.tab_widget.removeTab(idx_to_remove)
        removed_widget.setParent(None)

        self.conc_to_refine.setColumnCount(self.tab_widget.count())
        self.electrode_to_refine.setColumnCount(self.tab_widget.count())

        apply_table_map(self.conc_to_refine, self.previous_conc_state)
        apply_table_map(self.electrode_to_refine, self.previous_electrode_state)

    def redo(self) -> None:
        new_widget = QWidget()
        layout = QHBoxLayout()
        layout.addWidget(
            inputTitrationOpt(
                None, undo_stack=self.undo_stack, components=self.components
            )
        )
        new_widget.setLayout(layout)

        self.tab_widget.addTab(
            new_widget, str(self.tab_widget.findChild(QTabBar).count() + 1)
        )

        self.conc_to_refine.setColumnCount(self.tab_widget.count())
        self.electrode_to_refine.setColumnCount(self.tab_widget.count())

        apply_table_map(self.conc_to_refine, self.new_conc_state)
        apply_table_map(self.electrode_to_refine, self.new_electrode_state)


class RemoveTab(QUndoCommand):
    def __init__(
        self,
        tab_widget: QTabWidget,
        conc_to_refine: QTableWidget,
        electrode_to_refine: QTableWidget,
    ):
        QUndoCommand.__init__(self)
        self.tab_widget = tab_widget
        self.idx_to_remove = self.tab_widget.currentIndex()
        self.removed_widget = self.tab_widget.currentWidget()
        self.old_parent = self.removed_widget.parent()
        self.conc_to_refine = conc_to_refine
        self.electrode_to_refine = electrode_to_refine

        self.previous_conc_state = get_table_map(self.conc_to_refine)
        self.previous_electrode_state = get_table_map(self.electrode_to_refine)

        self.new_conc_state = [r[:-1] for r in self.previous_conc_state]
        self.new_electrode_state = [r[:-1] for r in self.previous_electrode_state]

    def undo(self) -> None:
        self.tab_widget.insertTab(
            self.idx_to_remove,
            self.removed_widget,
            str(self.idx_to_remove + 1),
        )
        self.removed_widget.setParent(self.old_parent)
        for i in range(self.tab_widget.count()):
            self.tab_widget.setTabText(i, f"{i + 1}")
        self.tab_widget.setCurrentIndex(self.idx_to_remove)

        self.conc_to_refine.setColumnCount(self.tab_widget.count())
        self.electrode_to_refine.setColumnCount(self.tab_widget.count())

        apply_table_map(self.conc_to_refine, self.previous_conc_state)
        apply_table_map(self.electrode_to_refine, self.previous_electrode_state)

    def redo(self) -> None:
        self.tab_widget.removeTab(self.idx_to_remove)
        self.removed_widget.setParent(None)
        for i in range(self.tab_widget.count()):
            self.tab_widget.setTabText(i, f"{i + 1}")

        self.conc_to_refine.setColumnCount(self.tab_widget.count())
        self.electrode_to_refine.setColumnCount(self.tab_widget.count())

        apply_table_map(self.conc_to_refine, self.new_conc_state)
        apply_table_map(self.electrode_to_refine, self.new_electrode_state)


class ChangeWeightsModeCommand(QUndoCommand):
    def __init__(
        self,
        field: CustomComboBox,
        index: int,
        titration_tabs: QTabWidget,
    ):
        QUndoCommand.__init__(self)
        self.titrations_tables = get_widgets_from_tab(
            titration_tabs, QTableView, "titrationView"
        )

        self.field = field
        self.index = index
        self.previous_index = field.previous_index

    def undo(self) -> None:
        self.field.blockSignals(True)
        self.field.setCurrentIndex(self.previous_index)
        self.field.blockSignals(False)

        self._update_row_editable(index=self.previous_index)

    def redo(self) -> None:
        self.field.blockSignals(True)
        self.field.setCurrentIndex(self.index)
        self.field.blockSignals(False)

        self._update_row_editable(index=self.index)

    def _update_row_editable(self, index) -> None:
        # find model in each titration input widget
        for titration_input in self.titrations_tables:
            model = titration_input.model()
            if index == 2:
                model.setColumnReadOnly([3], False)
            else:
                model.setColumnReadOnly([3], True)
