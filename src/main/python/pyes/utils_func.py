import numpy as np
import pandas as pd
from openpyxl.utils import get_column_letter
from PySide6.QtCore import QAbstractItemModel, Qt
from PySide6.QtWidgets import (
    QWidget,
    QComboBox,
    QListWidget,
    QTableView,
    QTableWidget,
    QTableWidgetItem,
    QTabWidget,
)
from viewmodels.delegate import ComboBoxDelegate


def value_or_problem(d: dict, field: str, default, message: str, problems: list[str]):
    value = d.get(field)
    if value is None:
        value = default
        problems.append(message + f" ({field})")
    return value


def addSpeciesComp(position: int, added_rows: int, view: QTableView, comp_names):
    view.setItemDelegateForColumn(view.model().columnCount() - 1, None)
    view.model().insertColumns(position, added_rows)
    view.setItemDelegateForColumn(
        view.model().columnCount() - 1,
        ComboBoxDelegate(view, comp_names),
    )


def removeSpeciesComp(position: int, removed_rows: int, view: QTableView, comp_names):
    view.setItemDelegateForColumn(view.model().columnCount() - 1, None)
    view.model().removeColumns(position, removed_rows)
    view.setItemDelegateForColumn(
        view.model().columnCount() - 1,
        ComboBoxDelegate(view, comp_names),
    )


def updateCompNames(
    comp_model: QAbstractItemModel,
    species_table: QTableView,
    solids_table: QTableView,
    conc_model: QAbstractItemModel,
    params_list: QListWidget,
    titrations_models: list[QAbstractItemModel],
    ind_comp: QComboBox,
    electro_active_comp: list[QComboBox],
    conc_to_refine: QTableWidget,
):
    """
    Handles the displayed names in the species table when edited in the components one
    """
    species_tables = [species_table, solids_table]
    species_models = [table.model() for table in species_tables]

    updated_comps = comp_model._data["Name"].tolist()

    for table, model in zip(species_tables, species_models):
        table.setItemDelegateForColumn(
            model.columnCount() - 1,
            ComboBoxDelegate(table, updated_comps),
        )
        model.updateHeader(updated_comps)
        model.updateCompName(updated_comps)

    updated_species_names = species_models[0].getColumn(1)
    for row, name in enumerate(updated_species_names):
        params_list.item(row).setText(name)

    conc_model.updateIndex(updated_comps)
    for m in titrations_models:
        m.updateIndex(updated_comps)

    conc_to_refine.setVerticalHeaderLabels(updated_comps)

    updateIndComponent(comp_model, ind_comp, electro_active_comp)


def updateIndComponent(
    comp_model: QAbstractItemModel,
    components_combobox: QComboBox,
    electro_active_combobox: list[QComboBox],
):
    """
    Update the selected indipendent component, tries to preserve the last one picked.
    """
    old_selected = components_combobox.currentIndex()
    if old_selected < 0:
        old_selected = 0

    components_combobox.blockSignals(True)
    components_combobox.clear()
    components_combobox.addItems(comp_model._data["Name"])
    components_combobox.blockSignals(False)

    num_elements = components_combobox.count()
    if num_elements > old_selected:
        components_combobox.setCurrentIndex(old_selected)
    else:
        components_combobox.setCurrentIndex(num_elements - 1)

    for c in electro_active_combobox:
        old_selected = c.currentIndex()
        if old_selected < 0:
            old_selected = 0
        c.blockSignals(True)
        c.clear()
        c.addItems(comp_model._data["Name"])
        c.blockSignals(False)

        if num_elements > old_selected:
            c.setCurrentIndex(old_selected)
        else:
            c.setCurrentIndex(num_elements - 1)


def cleanData():
    """
    Returns clean data to be used in the initialization
    of the software
    """

    conc_data = pd.DataFrame(
        [[0.0 for x in range(4)]],
        columns=["C0", "CT", "Sigma C0", "Sigma CT"],
        index=["A"],
    )
    comp_data = pd.DataFrame(
        [["A", 0]],
        columns=[
            "Name",
            "Charge",
        ],
    )
    species_data = pd.DataFrame(
        [[False] + [""] + [0.0 for x in range(6)] + [int(0)] + ["A"]],
        columns=[
            "Ignored",
            "Name",
            "LogB",
            "Sigma",
            "Ref. Ionic Str.",
            "CGF",
            "DGF",
            "EGF",
            "A",
            "Ref. Comp.",
        ],
    )
    solid_species_data = pd.DataFrame(
        [[False] + [""] + [0.0 for x in range(6)] + [int(0)] + ["A"]],
        columns=[
            "Ignored",
            "Name",
            "LogKs",
            "Sigma",
            "Ref. Ionic Str.",
            "CGF",
            "DGF",
            "EGF",
            "A",
            "Ref. Comp.",
        ],
    ).drop(0)

    return conc_data, comp_data, species_data, solid_species_data


def getName(vector):
    """
    Get name of species given their coefficients.
    """
    # TODO: rewrite, this is garbage and difficult to understand, maybe refactor
    comps = vector.index.to_numpy(copy=True)
    coeff = vector.to_numpy(copy=True)
    comps = comps[coeff != 0]
    coeff = coeff[coeff != 0]
    comps = np.where(coeff < 0, "OH", comps)
    coeff = np.abs(coeff)
    comps = np.where(
        coeff > 1, "(" + comps + ")" + coeff.astype(str), "(" + comps + ")"
    )
    return "".join(comps)


def resultToExcel(
    writer, data: pd.DataFrame | list[pd.DataFrame], sheet_name, **kwargs
):
    if isinstance(data, list):
        for i, d in enumerate(data):
            name = sheet_name + " Titr. " + str(i)
            d.to_excel(writer, sheet_name=name, **kwargs)
            adjustColumnWidths(writer.book, name, d)
    else:
        data.to_excel(writer, sheet_name=sheet_name, **kwargs)
        adjustColumnWidths(writer.book, sheet_name, data)


def resultToCSV(data: pd.DataFrame | list[pd.DataFrame], path: str):
    if isinstance(data, list):
        for i, d in enumerate(data):
            name = path + " Titration " + str(i) + ".csv"
            d.to_csv(name)
    else:
        data.to_csv(path + ".csv")


def resultToDataList(data: pd.DataFrame | list[pd.DataFrame]):
    if isinstance(data, list):
        return data
    else:
        return [data]


def getColWidths(dataframe):
    """
    Function to be used in conjuction with openpyxl to adjust width to tontent of a dataframe.
    """
    # Find the maximum length for the index
    idx_max = [len(str(dataframe.index.name)) + 5]

    cols_max = [(len(col) + 5) for col in dataframe.columns]
    # Concatenate the two
    return idx_max + cols_max


def adjustColumnWidths(wb, ws_name, data):
    """
    Given a worksheet apply the desired widths to all the columns
    """
    ws = wb[ws_name]
    widths = getColWidths(data)

    for i, column_width in enumerate(widths):
        ws.column_dimensions[get_column_letter(i + 1)].width = column_width


def get_list_map(table: QListWidget):
    values = []
    for i in range(table.count()):
        values.append(table.item(i).checkState() == Qt.CheckState.Checked)

    return values


def apply_list_map(table: QListWidget, values: list[bool]):
    for i, value in enumerate(values):
        table.item(i).setCheckState(
            Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
        )


def get_table_map(table: QTableWidget):
    values = []
    for r in range(table.rowCount()):
        row_values = []
        for c in range(table.columnCount()):
            row_values.append(table.item(r, c).checkState() == Qt.CheckState.Checked)
        values.append(row_values)

    return values


def apply_table_map(table: QTableWidget, values: list[list[bool]]):
    for r, row_value in enumerate(values):
        for c, value in enumerate(row_value):
            item = QTableWidgetItem()
            item.setFlags(Qt.ItemFlag.ItemIsUserCheckable | Qt.ItemFlag.ItemIsEnabled)
            item.setCheckState(
                Qt.CheckState.Checked if value else Qt.CheckState.Unchecked
            )
            table.setItem(r, c, item)


def get_widgets_from_tab(
    tab_widget: QTabWidget, widget_type, widget_name=None
) -> list[QWidget]:
    """
    Get all the widgets of a certain type from a tab widget
    """
    widgets = []
    for i in range(tab_widget.count()):
        tab = tab_widget.widget(i)
        if tab is not None:
            if widget_name is not None:
                widget = tab.findChildren(widget_type, widget_name)
            else:
                widget = tab.findChildren(widget_type)
            if widget is not None:
                widgets.extend(widget)
    return widgets


def encode_weights_mode(index):
    if index == 0:
        return "constant"
    elif index == 1:
        return "calculated"
    elif index == 2:
        return "given"
