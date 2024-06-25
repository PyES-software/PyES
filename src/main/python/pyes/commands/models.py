from typing import Union

from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide6.QtGui import QUndoCommand
from PySide6.QtWidgets import (
    QComboBox,
    QListWidget,
    QListWidgetItem,
    QSpinBox,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
)
from utils_func import (
    addSpeciesComp,
    apply_table_map,
    get_table_map,
    getName,
    removeSpeciesComp,
    updateCompNames,
)


class ListWidgetEditAll(QUndoCommand):
    def __init__(
        self,
        list_widget: QListWidget,
        *,
        checked: bool | None = None,
        enabled: bool | None = None,
    ):
        QUndoCommand.__init__(self)
        self.list_widget = list_widget
        self.checked = checked
        self.enabled = enabled

    def undo(self) -> None:
        self._apply(undo=True)

    def redo(self) -> None:
        self._apply()

    def _apply(self, undo: bool = False):
        if undo:
            if self.checked is not None:
                check = not self.checked
            if self.enabled is not None:
                enable = not self.enabled
        else:
            check = self.checked
            enable = self.enabled

        for index in range(self.list_widget.count()):
            if check is not None:
                if check:
                    self.list_widget.item(index).setCheckState(Qt.CheckState.Checked)
                else:
                    self.list_widget.item(index).setCheckState(Qt.CheckState.Unchecked)
            if enable is not None:
                if enable:
                    self.list_widget.item(index).setFlags(
                        self.list_widget.item(index).flags() | Qt.ItemFlag.ItemIsEnabled
                    )
                else:
                    self.list_widget.item(index).setFlags(
                        self.list_widget.item(index).flags()
                        & ~Qt.ItemFlag.ItemIsEnabled
                    )


class SpeciesEditColumn(QUndoCommand):
    def __init__(self, table: QTableView, column: int, value):
        QUndoCommand.__init__(self)
        self.table = table
        self.model = table.model()
        self.column = column
        self.new_value = value
        self.old_values = self.model._data.iloc[:, column].copy()

    def undo(self) -> None:
        print(self.old_values)
        self.model._data.iloc[:, self.column] = self.old_values
        self.cleanup()

    def redo(self) -> None:
        self.model._data.iloc[:, self.column] = self.new_value
        self.cleanup()

    def cleanup(self) -> None:
        self.model.layoutChanged.emit()


class SpeciesSwapRows(QUndoCommand):
    def __init__(
        self,
        table: QTableView,
        first_row: int,
        second_row: int,
        swap_soluble: bool,
        betas_list: QListWidget | None = None,
    ):
        QUndoCommand.__init__(self)
        self.table = table
        self.model = table.model()
        self.first_row = first_row
        self.second_row = second_row
        self.swap_soluble = swap_soluble
        self.betas_list = betas_list

    def undo(self) -> None:
        self.model.swapRows(self.second_row, self.first_row)
        second_row_item = self.betas_list.takeItem(self.second_row)
        first_row_item = self.betas_list.takeItem(self.first_row)
        self.betas_list.insertItem(self.first_row, second_row_item)
        self.betas_list.insertItem(self.second_row, first_row_item)
        self.table.updateEditorData()
        self.table.selectRow(self.first_row)

    def redo(self) -> None:
        self.model.swapRows(self.first_row, self.second_row)
        # second_row_item = self.betas_list.takeItem(max(self.first_row, self.second_row))
        # first_row_item = self.betas_list.takeItem(min(self.first_row, self.second_row))
        second_row_item = self.betas_list.takeItem(self.second_row)
        first_row_item = self.betas_list.takeItem(self.first_row)
        self.betas_list.insertItem(self.first_row, second_row_item)
        self.betas_list.insertItem(self.second_row, first_row_item)

        # second_row = first_row.clone()

        self.table.updateEditorData()
        self.table.selectRow(self.second_row)


class ComponentsCellEdit(QUndoCommand):
    def __init__(self, model: QAbstractItemModel, index: QModelIndex, value):
        QUndoCommand.__init__(self)
        self.index = index
        self.value = value
        self.prev = model.data(index, Qt.ItemDataRole.UserRole)
        self.model = model

    def undo(self):
        self.model._data.iloc[self.index.row(), self.index.column()] = self.prev

        self.cleanup()

    def redo(self):
        self.model._data.iloc[self.index.row(), self.index.column()] = self.value

        self.cleanup()

    def cleanup(self):
        # Updating coeff. should update the corresponding species name
        self.model.dataChanged.emit(self.index, self.index)
        self.model.layoutChanged.emit()


class SpeciesCellEdit(QUndoCommand):
    def __init__(self, model: QAbstractItemModel, index: QModelIndex, value):
        QUndoCommand.__init__(self)
        self.index = index
        self.value = value
        self.prev = model.data(index, Qt.ItemDataRole.UserRole)
        self.model = model

    def undo(self):
        self.model._data.iloc[self.index.row(), self.index.column()] = self.prev

        self.cleanup()

    def redo(self):
        self.model._data.iloc[self.index.row(), self.index.column()] = self.value

        self.cleanup()

    def cleanup(self):
        # Updating coeff. should update the corresponding species name
        self.model._data.iloc[self.index.row(), 1] = str(
            getName(self.model._data.iloc[self.index.row(), 8:-1])
        )
        self.model.dataChanged.emit(self.index, self.index)
        self.model.layoutChanged.emit()


class SpeciesAddRows(QUndoCommand):
    def __init__(
        self,
        table: QTableView,
        counter: Union[QSpinBox, None],
        position: int,
        number: int,
        add_soluble: bool,
        betas_list: QListWidget | None = None,
    ):
        QUndoCommand.__init__(self)
        self.table = table
        self.model = table.model()
        self.counter = counter
        self.position = position
        self.number = number
        self.add_soluble = add_soluble
        self.betas_list = betas_list

    def undo(self) -> None:
        self.model.removeRows(position=self.position + self.number, rows=self.number)
        if self.add_soluble:
            for item in self.list_items:
                self.betas_list.removeItemWidget(item)
        self.cleanup()

    def redo(self) -> None:
        self.model.insertRows(position=self.position, rows=self.number)
        if self.add_soluble:
            new_item = QListWidgetItem("")
            new_item.setFlags(new_item.flags() | Qt.ItemFlag.ItemIsUserCheckable)
            new_item.setFlags(new_item.flags() & ~Qt.ItemFlag.ItemIsSelectable)
            new_item.setCheckState(Qt.CheckState.Unchecked)
            self.list_items = [new_item.clone() for _ in range(self.number)]
            for index, item in enumerate(self.list_items):
                self.betas_list.insertItem(self.position + index, item)
        self.cleanup()

    def cleanup(self):
        self.counter.blockSignals(True)
        self.counter.setValue(self.model.rowCount())
        self.counter.blockSignals(False)


class SpeciesRemoveRows(QUndoCommand):
    def __init__(
        self,
        table: QTableView,
        counter: Union[QSpinBox, None],
        position: int,
        number: int,
        remove_soluble: bool,
        betas_list: QListWidget | None = None,
    ):
        QUndoCommand.__init__(self)
        self.table = table
        self.model = table.model()
        self.counter = counter
        self.position = position
        self.number = number
        self.removed_row = None
        self.remove_soluble = remove_soluble
        self.betas_list = betas_list

    def undo(self) -> None:
        self.model.insertRows(position=self.position - self.number, rows=self.number)
        self.model._data.iloc[(self.position - self.number) : (self.position), :] = (
            self.removed_rows
        )
        for item, row in zip(self.list_items, self.indexes):
            self.betas_list.insertItem(row, item)

        self.cleanup()

    def redo(self) -> None:
        self.removed_rows = self.model._data.iloc[
            (self.position - self.number) : (self.position), :
        ]
        self.model.removeRows(position=self.position, rows=self.number)

        self.list_items = []
        self.indexes = list(range((self.position - self.number), (self.position)))
        self.indexes.reverse()
        for i in self.indexes:
            self.list_items.append(self.betas_list.takeItem(i))

        self.cleanup()

    def cleanup(self):
        self.counter.blockSignals(True)
        self.counter.setValue(self.model.rowCount())
        self.counter.blockSignals(False)


class ComponentsSwapRows(QUndoCommand):
    def __init__(
        self,
        comp_table: QTableView,
        species_table: QTableView,
        solids_table: QTableView,
        conc_model: QAbstractItemModel,
        params_list: QListWidget,
        titrations_views: list[QTableView],
        electro_active_comp: list[QComboBox],
        conc_to_refine: QTableWidget,
        ind_comp: QComboBox,
        prev_ind_comp: str,
        first_row: int,
        second_row: int,
    ):
        QUndoCommand.__init__(self)
        self.comp_table = comp_table
        self.comp_model = comp_table.model()
        self.conc_model = conc_model
        self.species_tables = [species_table, solids_table]
        self.species_models = [table.model() for table in self.species_tables]
        self.params_list = params_list
        self.titrations_models = [table.model() for table in titrations_views]
        self.electro_active_comp = electro_active_comp
        self.conc_to_refine = conc_to_refine
        self.ind_comp = ind_comp
        self.prev_ind_comp = prev_ind_comp
        self.first_row = first_row
        self.second_row = second_row

    def undo(self) -> None:
        for table, model in zip(self.species_tables, self.species_models):
            model.swapColumns(self.second_row + 8, self.first_row + 8)

        self.conc_model.swapRows(self.second_row, self.first_row)
        for m in self.titrations_models:
            m.swapRows(self.second_row, self.first_row)
        self.comp_model.swapRows(self.second_row, self.first_row)

        apply_table_map(self.conc_to_refine, self.previous_state)

        self.cleanup()
        self.comp_table.selectRow(self.first_row)

    def redo(self) -> None:
        for table, model in zip(self.species_tables, self.species_models):
            model.swapColumns(self.first_row + 8, self.second_row + 8)

        self.conc_model.swapRows(self.first_row, self.second_row)
        for m in self.titrations_models:
            m.swapRows(self.first_row, self.second_row)
        self.comp_model.swapRows(self.first_row, self.second_row)

        self.previous_state = get_table_map(self.conc_to_refine)
        self.new_state = self.previous_state.copy()
        self.new_state[self.first_row], self.new_state[self.second_row] = (
            self.new_state[self.second_row],
            self.new_state[self.first_row],
        )
        apply_table_map(self.conc_to_refine, self.new_state)

        self.cleanup()
        self.comp_table.selectRow(self.second_row)

    def cleanup(self):
        updateCompNames(
            self.comp_model,
            *self.species_tables,
            self.conc_model,
            self.params_list,
            self.titrations_models,
            self.ind_comp,
            self.electro_active_comp,
            self.conc_to_refine,
        )
        self.comp_table.updateEditorData()
        self.ind_comp.setCurrentIndex(self.ind_comp.findData(self.prev_ind_comp, 0))
        for c in self.electro_active_comp:
            c.setCurrentIndex(c.findData(self.prev_ind_comp, 0))


class ComponentsAddRows(QUndoCommand):
    def __init__(
        self,
        comp_table: QTableView,
        species_table: QTableView,
        solids_table: QTableView,
        conc_model: QAbstractItemModel,
        params_list: QListWidget,
        titrations_views: list[QTableView],
        electro_active_comp: list[QComboBox],
        conc_to_refine: QTableWidget,
        ind_comp: QComboBox,
        counter: Union[QSpinBox, None],
        position: int,
        number: int,
    ):
        QUndoCommand.__init__(self)
        self.comp_model = comp_table.model()
        self.conc_model = conc_model
        self.species_tables = [species_table, solids_table]
        self.species_models = [table.model() for table in self.species_tables]
        self.params_list = params_list
        self.titrations_models = [table.model() for table in titrations_views]
        self.electro_active_comp = electro_active_comp
        self.conc_to_refine = conc_to_refine
        self.ind_comp = ind_comp
        self.counter = counter
        self.position = position
        self.number = number

    def undo(self) -> None:
        self.comp_model.removeRows(
            position=self.position + self.number, rows=self.number
        )

        for table, model in zip(self.species_tables, self.species_models):
            removeSpeciesComp(
                self.position + self.number + 8,
                self.number,
                table,
                self.comp_model._data["Name"].tolist(),
            )
        self.conc_model.removeRows(self.position + self.number, self.number)
        for m in self.titrations_models:
            m.removeRows(self.position + self.number, self.number)

        self.conc_to_refine.setRowCount(self.conc_to_refine.rowCount() - self.number)
        apply_table_map(self.conc_to_refine, values=self.previous_state)
        self.cleanup()

    def redo(self) -> None:
        self.comp_model.insertRows(position=self.position, rows=self.number)

        for table, model in zip(self.species_tables, self.species_models):
            addSpeciesComp(
                self.position + 8,
                self.number,
                table,
                self.comp_model._data["Name"].tolist(),
            )

        self.conc_model.insertRows(self.position, self.number)
        for m in self.titrations_models:
            m.insertRows(self.position, self.number)

        self.previous_state = get_table_map(self.conc_to_refine)
        self.conc_to_refine.setRowCount(self.conc_model.rowCount())
        self.new_state = (
            self.previous_state[0 : self.position]
            + [
                [False for _ in range(len(self.titrations_models))]
                for _ in range(self.number)
            ]
            + self.previous_state[self.position :]
        )
        apply_table_map(self.conc_to_refine, values=self.new_state)

        self.cleanup()

    def cleanup(self):
        self.counter.blockSignals(True)
        self.counter.setValue(self.comp_model.rowCount())
        self.counter.blockSignals(False)

        updateCompNames(
            self.comp_model,
            *self.species_tables,
            self.conc_model,
            self.params_list,
            self.titrations_models,
            self.ind_comp,
            self.electro_active_comp,
            self.conc_to_refine,
        )


class ComponentsRemoveRows(QUndoCommand):
    def __init__(
        self,
        comp_table: QTableView,
        species_table: QTableView,
        solids_table: QTableView,
        conc_model: QAbstractItemModel,
        params_list: QListWidget,
        titrations_views: list[QTableView],
        electro_active_comp: list[QComboBox],
        conc_to_refine: QTableWidget,
        ind_comp: QComboBox,
        counter: Union[QSpinBox, None],
        position: int,
        number: int,
    ):
        QUndoCommand.__init__(self)
        self.comp_model = comp_table.model()
        self.conc_model = conc_model
        self.species_tables = [species_table, solids_table]
        self.species_models = [table.model() for table in self.species_tables]
        self.params_list = params_list
        self.titrations_models = [table.model() for table in titrations_views]
        self.electro_active_comp = electro_active_comp
        self.conc_to_refine = conc_to_refine
        self.ind_comp = ind_comp
        self.counter = counter
        self.position = position
        self.number = number
        self.comp_removed_row = None
        self.conc_removed_row = None
        self.titrations_removed_rows = [None for _ in titrations_views]
        self.removed_columns = [None, None]

    def undo(self) -> None:
        self.comp_model.insertRows(
            position=self.position - self.number, rows=self.number
        )
        self.comp_model._data.iloc[
            (self.position - self.number) : (self.position), :
        ] = self.comp_removed_rows

        for i, (table, model) in enumerate(
            zip(self.species_tables, self.species_models)
        ):
            addSpeciesComp(
                self.position - self.number + 8,
                self.number,
                table,
                self.comp_model._data["Name"].tolist(),
            )

            model._data.iloc[
                :, (self.position - self.number) + 8 : (self.position) + 8
            ] = self.removed_columns[i]

        self.conc_model.insertRows(
            position=self.position - self.number, rows=self.number
        )
        self.conc_model._data.iloc[
            (self.position - self.number) : (self.position), :
        ] = self.conc_removed_rows

        for i, m in enumerate(self.titrations_models):
            m.insertRows(position=self.position - self.number, rows=self.number)
            m._data.iloc[(self.position - self.number) : (self.position), :] = (
                self.titrations_removed_rows[i]
            )

        self.conc_to_refine.setRowCount(len(self.previous_state))
        apply_table_map(self.conc_to_refine, self.previous_state)

        self.cleanup()

    def redo(self) -> None:
        self.comp_removed_rows = self.comp_model._data.iloc[
            (self.position - self.number) : (self.position), :
        ]
        self.conc_removed_rows = self.conc_model._data.iloc[
            (self.position - self.number) : (self.position), :
        ]
        for i, m in enumerate(self.titrations_models):
            self.titrations_removed_rows[i] = m._data.iloc[
                (self.position - self.number) : (self.position), :
            ]
            self.titrations_models[i].removeRows(self.position, self.number)

        self.comp_model.removeRows(position=self.position, rows=self.number)

        for i, (table, model) in enumerate(
            zip(self.species_tables, self.species_models)
        ):
            self.removed_columns[i] = model._data.iloc[
                :, (self.position - self.number) + 8 : (self.position) + 8
            ]

            removeSpeciesComp(
                self.position + 8,
                self.number,
                table,
                self.comp_model._data["Name"].tolist(),
            )

        self.conc_model.removeRows(self.position, self.number)

        self.previous_state = get_table_map(self.conc_to_refine)
        self.conc_to_refine.setRowCount(self.conc_model.rowCount())
        self.new_state = (
            self.previous_state[0 : self.position]
            + self.previous_state[self.position :]
        )
        apply_table_map(self.conc_to_refine, values=self.new_state)

        self.cleanup()

    def cleanup(self):
        self.counter.blockSignals(True)
        self.counter.setValue(self.comp_model.rowCount())
        self.counter.blockSignals(False)

        updateCompNames(
            self.comp_model,
            *self.species_tables,
            self.conc_model,
            self.params_list,
            self.titrations_models,
            self.ind_comp,
            self.electro_active_comp,
            self.conc_to_refine,
        )


class TitrationRefineEdit(QUndoCommand):
    def __init__(self, item: QTableWidgetItem):
        QUndoCommand.__init__(self)
        self.table_widget = item.tableWidget()
        self.row = item.row()
        self.column = item.column()
        self.new_state = item.checkState()
        if self.new_state == Qt.CheckState.Checked:
            self.previous_state = Qt.CheckState.Unchecked
        else:
            self.previous_state = Qt.CheckState.Checked

    def undo(self):
        self.table_widget.blockSignals(True)
        self.table_widget.item(self.row, self.column).setCheckState(self.previous_state)
        self.table_widget.blockSignals(False)

    def redo(self):
        self.table_widget.blockSignals(True)
        self.table_widget.item(self.row, self.column).setCheckState(self.new_state)
        self.table_widget.blockSignals(False)


class BetaRefineEdit(QUndoCommand):
    def __init__(self, item: QListWidgetItem):
        QUndoCommand.__init__(self)
        self.beta_to_refine = item.listWidget()
        self.row = self.beta_to_refine.row(item)
        self.new_state = item.checkState()
        if self.new_state == Qt.CheckState.Checked:
            self.previous_state = Qt.CheckState.Unchecked
        else:
            self.previous_state = Qt.CheckState.Checked

    def undo(self):
        self.beta_to_refine.blockSignals(True)
        self.beta_to_refine.item(self.row).setCheckState(self.previous_state)
        self.beta_to_refine.blockSignals(False)

    def redo(self):
        self.beta_to_refine.blockSignals(True)
        self.beta_to_refine.item(self.row).setCheckState(self.new_state)
        self.beta_to_refine.blockSignals(False)


class BetaRefineCheckAll(QUndoCommand):
    def __init__(self, beta_to_refine: QListWidget):
        QUndoCommand.__init__(self)
        self.beta_to_refine = beta_to_refine

    def undo(self) -> None:
        for ix, prev_data in enumerate(self.previous_state):
            if prev_data:
                self.beta_to_refine.item(ix).setCheckState(Qt.CheckState.Checked)
            else:
                self.beta_to_refine.item(ix).setCheckState(Qt.CheckState.Unchecked)

    def redo(self) -> None:
        self.previous_state = [
            self.beta_to_refine.item(i).checkState() == Qt.CheckState.Checked
            for i in range(self.beta_to_refine.count())
        ]

        for ix in range(self.beta_to_refine.count()):
            self.beta_to_refine.item(ix).setCheckState(Qt.CheckState.Checked)


class BetaRefineUncheckAll(QUndoCommand):
    def __init__(self, beta_to_refine: QListWidget):
        QUndoCommand.__init__(self)
        self.beta_to_refine = beta_to_refine

    def undo(self) -> None:
        for ix, prev_data in enumerate(self.previous_state):
            if prev_data:
                self.beta_to_refine.item(ix).setCheckState(Qt.CheckState.Checked)
            else:
                self.beta_to_refine.item(ix).setCheckState(Qt.CheckState.Unchecked)

    def redo(self) -> None:
        self.previous_state = [
            self.beta_to_refine.item(i).checkState() == Qt.CheckState.Checked
            for i in range(self.beta_to_refine.count())
        ]

        for ix in range(self.beta_to_refine.count()):
            self.beta_to_refine.item(ix).setCheckState(Qt.CheckState.Unchecked)


class TableCheckAll(QUndoCommand):
    def __init__(self, table_widget: QTableWidget):
        QUndoCommand.__init__(self)
        self.table_widget = table_widget
        self.previous_state = get_table_map(self.table_widget)
        self.new_state = [[True for _ in row] for row in self.previous_state]

    def undo(self) -> None:
        apply_table_map(self.table_widget, self.previous_state)

    def redo(self) -> None:
        apply_table_map(self.table_widget, self.new_state)


class TableUncheckAll(QUndoCommand):
    def __init__(self, table_widget: QTableWidget):
        QUndoCommand.__init__(self)
        self.table_widget = table_widget
        self.previous_state = get_table_map(self.table_widget)
        self.new_state = [[False for _ in row] for row in self.previous_state]

    def undo(self) -> None:
        apply_table_map(self.table_widget, self.previous_state)

    def redo(self) -> None:
        apply_table_map(self.table_widget, self.new_state)
