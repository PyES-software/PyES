from typing import Union

from PySide6.QtCore import QAbstractItemModel, QModelIndex, Qt
from PySide6.QtGui import QUndoCommand
from PySide6.QtWidgets import QComboBox, QSpinBox, QTableView
from utils_func import addSpeciesComp, getName, removeSpeciesComp, updateCompNames


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
    def __init__(self, table: QTableView, first_row: int, second_row: int):
        QUndoCommand.__init__(self)
        self.table = table
        self.model = table.model()
        self.first_row = first_row
        self.second_row = second_row

    def undo(self) -> None:
        self.model.swapRows(self.second_row, self.first_row)
        self.table.updateEditorData()
        self.table.selectRow(self.first_row)

    def redo(self) -> None:
        self.model.swapRows(self.first_row, self.second_row)
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
    ):
        QUndoCommand.__init__(self)
        self.table = table
        self.model = table.model()
        self.counter = counter
        self.position = position
        self.number = number

    def undo(self) -> None:
        self.model.removeRows(position=self.position + self.number, rows=self.number)
        self.cleanup()

    def redo(self) -> None:
        self.model.insertRows(position=self.position, rows=self.number)
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
    ):
        QUndoCommand.__init__(self)
        self.table = table
        self.model = table.model()
        self.counter = counter
        self.position = position
        self.number = number
        self.removed_row = None

    def undo(self) -> None:
        self.model.insertRows(position=self.position - self.number, rows=self.number)
        self.model._data.iloc[
            (self.position - self.number) : (self.position), :
        ] = self.removed_rows

        self.cleanup()

    def redo(self) -> None:
        self.removed_rows = self.model._data.iloc[
            (self.position - self.number) : (self.position), :
        ]
        self.model.removeRows(position=self.position, rows=self.number)

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
        self.ind_comp = ind_comp
        self.prev_ind_comp = prev_ind_comp
        self.first_row = first_row
        self.second_row = second_row

    def undo(self) -> None:
        for table, model in zip(self.species_tables, self.species_models):
            model.swapColumns(self.second_row + 8, self.first_row + 8)

        self.conc_model.swapRows(self.second_row, self.first_row)
        self.comp_model.swapRows(self.second_row, self.first_row)

        self.cleanup()
        self.comp_table.selectRow(self.first_row)

    def redo(self) -> None:
        for table, model in zip(self.species_tables, self.species_models):
            model.swapColumns(self.first_row + 8, self.second_row + 8)

        self.conc_model.swapRows(self.first_row, self.second_row)
        self.comp_model.swapRows(self.first_row, self.second_row)

        self.cleanup()
        self.comp_table.selectRow(self.second_row)

    def cleanup(self):
        updateCompNames(
            self.comp_model, *self.species_tables, self.conc_model, self.ind_comp
        )
        self.comp_table.updateEditorData()
        self.ind_comp.setCurrentIndex(self.ind_comp.findData(self.prev_ind_comp, 0))


class ComponentsAddRows(QUndoCommand):
    def __init__(
        self,
        comp_table: QTableView,
        species_table: QTableView,
        solids_table: QTableView,
        conc_model: QAbstractItemModel,
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
        self.cleanup()

    def cleanup(self):
        self.counter.blockSignals(True)
        self.counter.setValue(self.comp_model.rowCount())
        self.counter.blockSignals(False)

        updateCompNames(
            self.comp_model, *self.species_tables, self.conc_model, self.ind_comp
        )


class ComponentsRemoveRows(QUndoCommand):
    def __init__(
        self,
        comp_table: QTableView,
        species_table: QTableView,
        solids_table: QTableView,
        conc_model: QAbstractItemModel,
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
        self.ind_comp = ind_comp
        self.counter = counter
        self.position = position
        self.number = number
        self.comp_removed_row = None
        self.conc_removed_row = None
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
        self.cleanup()

    def redo(self) -> None:
        self.comp_removed_rows = self.comp_model._data.iloc[
            (self.position - self.number) : (self.position), :
        ]
        self.conc_removed_rows = self.conc_model._data.iloc[
            (self.position - self.number) : (self.position), :
        ]
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

        self.cleanup()

    def cleanup(self):
        self.counter.blockSignals(True)
        self.counter.setValue(self.comp_model.rowCount())
        self.counter.blockSignals(False)

        updateCompNames(
            self.comp_model, *self.species_tables, self.conc_model, self.ind_comp
        )
