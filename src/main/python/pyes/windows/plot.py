# import sys
import sys
import typing
from copy import deepcopy
from itertools import cycle
from pathlib import Path

import numpy as np
import pandas as pd
import pyqtgraph as pg
import pyqtgraph.exporters
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont, QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QDialog, QFileDialog, QInputDialog, QMainWindow, QToolTip
from ui.PyES_graphExport import Ui_ExportGraphDialog
from ui.PyES_pyqtgraphPlotExport import Ui_PlotWindow
from utils_func import resultToDataList
from viewmodels.delegate import ColorPickerDelegate

if typing.TYPE_CHECKING:
    from windows.window import MainWindow

# Setup white background and black axis for the plot
# THIS NEEDS TO BE DONE BOFORE LOADING THE UI FILE
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")
pg.setConfigOption("antialias", True)

PALETTE = [
    "#ebac23",
    "#b80058",
    "#008cf9",
    "#006e00",
    "#00bbad",
    "#d163e6",
    "#b24502",
    "#ff9287",
    "#5954d6",
    "#00c6f8",
    "#878500",
    "#00a76c",
]


class PlotWindow(QMainWindow, Ui_PlotWindow):
    def __init__(self, parent: "MainWindow"):
        # import debugpy

        # debugpy.debug_this_thread()

        super().__init__()
        self.setupUi(self)

        # Colour cycle to use for plotting species.
        self.color_palette = cycle(PALETTE)

        self.color_palette_solids = cycle(PALETTE)

        self.plot_widgets = [self.conc_graph, self.perc_graph, self.titration_graph]
        self.legends = []

        self.font_size = 10
        self.line_width = 2

        self.componentComboBox.currentTextChanged.connect(self._updateTitrationCurve)
        self.componentComboBox_perc.currentTextChanged.connect(
            self._updatePercentageReference
        )
        self.exportButton.clicked.connect(self.exportGraph)
        self.errors_check.clicked.connect(self.redraw)
        self.monochrome_check.clicked.connect(self.changeMonochrome)
        self.monochrome_color.colorChanged.connect(self.redraw)
        self.textSize.valueChanged.connect(self._set_plot_fontsize)
        self.lineWidth.valueChanged.connect(self._set_line_width)
        self.hide_legend_check.clicked.connect(self._toggle_legend_visibility)

        self.c_unit.currentTextChanged.connect(self.changeCUnit)
        self.v_unit.currentTextChanged.connect(self.changeVUnit)

        # TODO: make checking more robust
        self.is_distribution_result = parent.dmode.currentIndex() == 1
        self.is_optimization_result = parent.dmode.currentIndex() == 2

        self.soluble_result = resultToDataList(parent.result["species_concentrations"])
        self.perc_result = resultToDataList(parent.result["soluble_percentages"])

        self.solids_result = [
            d[
                [
                    column
                    for column in d.columns
                    if not (column.startswith("Prec.") or column.startswith("SI"))
                ]
            ]
            for d in resultToDataList(parent.result["solids_concentrations"])
        ]
        self.solid_perc_result = resultToDataList(parent.result["solids_percentages"])

        self.with_solids = not self.solids_result[0].empty
        self.with_errors = parent.uncertaintyMode.isChecked()

        if self.with_errors:
            self.soluble_sd = resultToDataList(parent.result["species_sigma"])
            self.soluble_sd_perc = resultToDataList(
                parent.result["soluble_percentages_sigma"]
            )

            self.solids_sd = resultToDataList(parent.result["solid_sigma"])
            self.solids_sd_perc = resultToDataList(
                parent.result["solids_percentages_sigma"]
            )
        else:
            self.soluble_sd = [pd.DataFrame() for _ in self.soluble_result]
            self.soluble_sd_perc = [pd.DataFrame() for _ in self.soluble_result]
            self.solids_sd = [pd.DataFrame() for _ in self.solids_result]
            self.solids_sd_perc = [pd.DataFrame() for _ in self.solids_result]

        for result, perc, sd, sd_perc in zip(
            self.solids_result,
            self.solid_perc_result,
            self.solids_sd,
            self.solids_sd_perc,
        ):
            result.columns = [column + "_(s)" for column in result.columns]
            perc.columns = result.columns
            if self.with_errors:
                sd.columns = result.columns
                sd_perc.columns = result.columns

        self.comps = parent.result["comp_info"]
        self.comp_names = list(self.comps.index.get_level_values("Component").unique())

        self.number_of_results = len(self.soluble_result)
        self.nc = len(self.comp_names)

        # Get values for the x from the index
        self.original_x_values = [
            self.soluble_result[i].index.get_level_values(0).to_numpy()
            for i in range(self.number_of_results)
        ]
        self.x_values = [
            self.soluble_result[i].index.get_level_values(0).to_numpy()
            for i in range(self.number_of_results)
        ]

        if not self.is_optimization_result:
            self.titrationSelector.setEnabled(False)
        else:
            for i in range(self.number_of_results):
                self.titrationSelector.addItem(f"Titration {i + 1}")
            self.titrationSelector.setCurrentIndex(0)
            self.titrationSelector.setEnabled(True)
            self.titrationSelector.currentIndexChanged.connect(self.redraw)
            self.titrationSelector.currentIndexChanged.connect(
                self._updateTitrationCurve
            )
            self.calculated_potential = [
                self.soluble_result[i].index.get_level_values(2).to_numpy()
                for i in range(self.number_of_results)
            ]
            self.potential = [
                self.soluble_result[i].index.get_level_values(1).to_numpy()
                for i in range(self.number_of_results)
            ]

        self.perc_comp = 0
        self.adjust_factor_soluble = parent.result["stoichiometry"]
        self.adjust_factor_solids = parent.result["solid_stoichiometry"]

        if self.is_distribution_result:
            self.tot_conc = [parent.result["comp_info"]["Tot. C. [mol/l]"].to_numpy()]
            self.point_conc = [None]
            self.perc_reference = self.tot_conc
            if self.with_errors:
                self.sigma_perc_reference = [parent.result["comp_info"]["Sigma Tot C"]]
        else:
            self.tot_conc = []
            self.point_conc = []
            self.perc_reference = []
            if self.with_errors:
                self.sigma_perc_reference = []

            for i in range(self.number_of_results):
                tot_conc = parent.result["comp_info"][
                    "Vessel Conc. [mol/l]"
                ].to_numpy()[i * self.nc : i * self.nc + self.nc]
                point_conc = parent.result["comp_info"][
                    "Titrant Conc. [mol/l]"
                ].to_numpy()[i * self.nc : i * self.nc + self.nc]
                v0 = (
                    parent.result["comp_info"]
                    .index.get_level_values("V0 [ml]")
                    .to_numpy()[i * self.nc]
                    * 1e-3
                )

                perc_reference = (
                    tot_conc[:, None] * v0
                    + (point_conc[:, None] * self.x_values[i] * 1e-3)
                ) / (v0 + self.x_values[i] * 1e-3)

                self.tot_conc.append(tot_conc)
                self.point_conc.append(point_conc)
                self.perc_reference.append(perc_reference)

                if self.with_errors:
                    sigma_c0 = parent.result["comp_info"]["Sigma C0"].to_numpy()[
                        i * self.nc : i * self.nc + self.nc
                    ]
                    sigma_ct = parent.result["comp_info"]["Sigma CT"].to_numpy()[
                        i * self.nc : i * self.nc + self.nc
                    ]
                    sigma_reference = (
                        sigma_c0[:, None] + sigma_ct[:, None] * self.x_values[i] * 1e-3
                    )
                    self.sigma_perc_reference.append(sigma_reference)

        self.original_soluble_values = [
            {
                name: [
                    self.soluble_result[i][name].to_numpy(dtype=float),
                    self.perc_result[i][name].to_numpy(dtype=float),
                ]
                for name in self.soluble_result[i].columns
            }
            for i in range(self.number_of_results)
        ]
        self.soluble_values = deepcopy(self.original_soluble_values)

        self.original_solids_values = [
            {
                name: [
                    self.solids_result[i][name].to_numpy(dtype=float),
                    self.solid_perc_result[i][name].to_numpy(dtype=float),
                ]
                for name in self.solids_result[i].columns
            }
            for i in range(self.number_of_results)
        ]
        self.solids_values = deepcopy(self.original_solids_values)

        if self.with_errors:
            self.original_soluble_errors = [
                {
                    name: [
                        self.soluble_sd[i][name].to_numpy(dtype=float),
                    ]
                    for name in self.soluble_sd[i].columns
                }
                for i in range(self.number_of_results)
            ]
            self.soluble_errors = deepcopy(self.original_soluble_errors)

            self.original_solids_errors = [
                {
                    name: [
                        self.solids_sd[i][name].to_numpy(dtype=float),
                    ]
                    for name in self.solids_sd[i].columns
                }
                for i in range(self.number_of_results)
            ]
            self.solids_errors = deepcopy(self.original_solids_errors)
        else:
            self.errors_check.setEnabled(False)

        # Store a reference to lines on the plot, and items in our
        # data viewer we can update rather than redraw.
        self._data_lines = dict()
        self._data_colors = dict()
        self._data_visible = []

        # Initialize a Model for species_conc
        self.speciesModel = QStandardItemModel()
        self.solidsModel = QStandardItemModel()
        self.speciesModel.setHorizontalHeaderLabels(["Species", "Color"])
        self.solidsModel.setHorizontalHeaderLabels(["Species", "Color"])
        self.speciesModel.itemChanged.connect(self._check_checked_state)
        self.solidsModel.itemChanged.connect(self._check_checked_state)

        self.speciesView.setModel(self.speciesModel)
        self.solidsView.setModel(self.solidsModel)

        self.speciesView.setItemDelegateForColumn(1, ColorPickerDelegate(self))
        self.solidsView.setItemDelegateForColumn(1, ColorPickerDelegate(self))
        self.speciesView.setColumnWidth(1, 150)
        # Each colum holds a checkbox and the species name
        for column in self.soluble_result[0].columns:
            item = QStandardItem()
            item.setText(column)
            item.setColumnCount(2)
            item.setCheckable(True)
            item.setEditable(False)

            item2 = QStandardItem()
            item2.setText(self._get_species_color(column, new=True))
            self.speciesModel.appendRow([item, item2])

        if self.with_solids:
            for column in self.solids_result[0].columns:
                item = QStandardItem()
                item.setText(column)
                item.setColumnCount(2)
                item.setCheckable(True)
                item.setEditable(False)

                item2 = QStandardItem()
                item2.setText(self._get_solids_color(column, new=True))
                self.solidsModel.appendRow([item, item2])
        else:
            self.regions_check.setEnabled(False)

        self.componentComboBox_perc.blockSignals(True)
        self.componentComboBox_perc.addItems(self.comp_names)
        self.componentComboBox_perc.blockSignals(False)

        if self.is_distribution_result:
            self.independent_comp_name = parent.indComp.currentText()
            self.tabWidget.setTabEnabled(2, False)
            self.v_unit.setEnabled(False)
            self.v_unit_label.setEnabled(False)
            ind_comp_idx = np.argwhere(np.isnan(self.tot_conc[0]))[0, 0]
            self.componentComboBox_perc.setItemData(
                ind_comp_idx,
                self.comp_names[ind_comp_idx],
                Qt.ItemDataRole.UserRole - 1,
            )

        self._initGraphs()

        if not self.is_distribution_result:
            self.componentComboBox.addItems(self.comp_names)
            if self.is_optimization_result:
                self.componentComboBox.addItem("Pot.")

        # Resize column to newly added species
        self.speciesView.resizeColumnToContents(0)
        self.speciesView.setColumnWidth(1, self.speciesView.rowHeight(0))
        self.solidsView.resizeColumnToContents(0)
        self.solidsView.setColumnWidth(1, self.solidsView.rowHeight(0))

    def changeSolidsGraphics(self):
        result_index = self.titrationSelector.currentIndex()
        for name in self.solids_result[result_index].columns:
            if name in self._data_visible:
                if self.regions_check.isChecked():
                    self._removePlotLines(name)
                else:
                    self._removeRegionLines(name)

        self.redraw()

    def filterSpecies(self):
        """
        Select only species that contain some components.
        """
        choice, ok = QInputDialog.getItem(
            self, "Pick Component", "Component:", self.comp_names
        )
        if ok:
            self.deselectAll()
            for row in range(self.speciesModel.rowCount()):
                item = self.speciesModel.item(row)
                if choice in item.text():
                    item.setCheckState(Qt.CheckState.Checked)

            for row in range(self.solidsModel.rowCount()):
                item = self.solidsModel.item(row)
                if choice in item.text():
                    item.setCheckState(Qt.CheckState.Checked)
        self.redraw()

    def changeErrorsGraphics(self):
        if self.errors_check.isChecked():
            result_index = self.titrationSelector.currentIndex()
            for name in self.soluble_result[0].columns:
                if name in self._data_visible:
                    v = self.soluble_values[result_index][name]
                    p = (
                        v[0]
                        * self.adjust_factor_soluble[name][self.perc_comp]
                        / self.perc_reference[result_index][self.perc_comp]
                        * 100
                    )
                    e = self.soluble_errors[result_index][name][0]
                    ep = self._calculate_error_percentages(
                        result_index,
                        e,
                        p,
                        self.adjust_factor_soluble[name][self.perc_comp],
                        v[0],
                    )
                    color = self._get_species_color(name)

                    self._addErrorLines(
                        result_index,
                        v,
                        p,
                        e,
                        ep,
                        name,
                        color,
                        line_style=Qt.PenStyle.DashDotDotLine,
                    )
            for name in self.solids_result[0].columns:
                if name in self._data_visible:
                    v = self.solids_values[result_index][name]
                    p = (
                        v[0]
                        * self.adjust_factor_solids[name][self.perc_comp]
                        / self.perc_reference[result_index][self.perc_comp]
                        * 100
                    )
                    e = self.solids_errors[result_index][name][0]
                    ep = self._calculate_error_percentages(
                        result_index,
                        e,
                        p,
                        self.adjust_factor_solids[name][self.perc_comp],
                        v[0],
                    )
                    color = self._get_solids_color(name)

                    self._addErrorLines(
                        result_index,
                        v,
                        p,
                        e,
                        ep,
                        name,
                        color,
                        line_style=Qt.PenStyle.DashDotDotLine,
                    )
        else:
            for name in list(self.solids_result[0].columns) + list(
                self.soluble_result[0].columns
            ):
                if name in self._data_visible:
                    self._removeErrorLines(name)
        self.redraw()

    def selectAll(self):
        """
        Select all species.
        """
        for row in range(self.speciesModel.rowCount()):
            item = self.speciesModel.item(row)
            if item.checkState() != Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Checked)

        for row in range(self.solidsModel.rowCount()):
            item = self.solidsModel.item(row)
            if item.checkState() != Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Checked)

    def deselectAll(self):
        """
        Deselect all species.
        """
        for row in range(self.speciesModel.rowCount()):
            item = self.speciesModel.item(row)
            if item.checkState() == Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Unchecked)

        for row in range(self.solidsModel.rowCount()):
            item = self.solidsModel.item(row)
            if item.checkState() == Qt.CheckState.Checked:
                item.setCheckState(Qt.CheckState.Unchecked)

    def redraw(self):
        result_index = self.titrationSelector.currentIndex()

        conc_y_min, conc_y_max = 0, sys.maxsize
        perc_y_min, perc_y_max = 0, 100
        x_min, x_max = (
            min(self.x_values[result_index]),
            max(self.x_values[result_index]),
        )

        # Loop over all species and add/update/remove lines on the plot.
        for name in self.soluble_result[result_index].columns:
            if name in self._data_visible:
                v = self.soluble_values[result_index][name]
                p = (
                    v[0]
                    * self.adjust_factor_soluble[name][self.perc_comp]
                    / self.perc_reference[result_index][self.perc_comp]
                    * 100
                )
                if self.with_errors:
                    e = self.soluble_errors[result_index][name][0]
                    ep = self._calculate_error_percentages(
                        result_index,
                        e,
                        p,
                        self.adjust_factor_soluble[name][self.perc_comp],
                        v[0],
                    )

                line_style = Qt.PenStyle.SolidLine
                errorline_style = Qt.PenStyle.DashDotDotLine
                color = (
                    self.monochrome_color.color()
                    if self.monochrome_check.isChecked()
                    else self._get_species_color(name)
                )

                if name not in self._data_lines:
                    self._addPlotLines(result_index, v, name, color, line_style)
                    if self.with_errors and self.errors_check.isChecked():
                        self._addErrorLines(
                            result_index, v, p, e, ep, name, color, errorline_style
                        )
                else:
                    for i, plot in enumerate(self._data_lines[name]):
                        if i == 0:
                            plot.setPen(
                                pg.mkPen(color, width=self.line_width, style=line_style)
                            )
                            plot.setData(self.x_values[result_index], v[i])
                        elif i == 1:
                            plot.setPen(
                                pg.mkPen(color, width=self.line_width, style=line_style)
                            )
                            plot.setData(
                                self.x_values[result_index],
                                p,
                            )
                        elif i == 2:
                            plot.setPen(
                                pg.mkPen(
                                    color, width=self.line_width, style=errorline_style
                                )
                            )
                            plot.setData(self.x_values[result_index], v[0] + e)
                        elif i == 3:
                            plot.setPen(
                                pg.mkPen(
                                    color, width=self.line_width, style=errorline_style
                                )
                            )
                            plot.setData(self.x_values[result_index], v[0] - e)
                        elif i == 4:
                            plot.setPen(
                                pg.mkPen(
                                    color, width=self.line_width, style=errorline_style
                                )
                            )
                            plot.setData(self.x_values[result_index], p + ep)
                        elif i == 5:
                            plot.setPen(
                                pg.mkPen(
                                    color, width=self.line_width, style=errorline_style
                                )
                            )
                            plot.setData(self.x_values[result_index], p - ep)

                conc_y_min, conc_y_max = min(conc_y_min, *v[0]), max(conc_y_max, *v[0])
                perc_y_min, perc_y_max = min(perc_y_min, *p), max(perc_y_max, *p)
            else:
                if name in self._data_lines:
                    self._removePlotLines(name)

        if self.with_solids:
            for name in self.solids_result[result_index].columns:
                if self.regions_check.isChecked():
                    # Identify regions where the solid concentration is greater than zero
                    positive_conc = self.solids_result[result_index][name] > 0
                    positive_conc_edges = np.diff(
                        np.r_[0, positive_conc.astype(int), 0]
                    )
                    solid_regions_indices = positive_conc_edges.nonzero()[0]
                    solids_regions = np.reshape(solid_regions_indices, (-1, 2))

                    if name in self._data_visible:
                        color = self._get_solids_color(name) + "66"
                        if name not in self._data_lines:
                            self._addRegionLines(
                                result_index, solids_regions, name, color
                            )
                        else:
                            for plot in self._data_lines[name]:
                                for region in plot:
                                    region.setBrush(pg.mkBrush(color))
                    else:
                        if name in self._data_lines:
                            self._removeRegionLines(name)

                else:
                    if name in self._data_visible:
                        v = self.solids_values[result_index][name]
                        p = (
                            v[0]
                            * self.adjust_factor_solids[name][self.perc_comp]
                            / self.perc_reference[result_index][self.perc_comp]
                            * 100
                        )
                        if self.with_errors:
                            e = self.solids_errors[result_index][name][0]
                            ep = self._calculate_error_percentages(
                                result_index,
                                e,
                                p,
                                self.adjust_factor_solids[name][self.perc_comp],
                                v[0],
                            )

                        line_style = Qt.PenStyle.DashLine
                        errorline_style = Qt.PenStyle.DashDotDotLine
                        color = (
                            self.monochrome_color.color()
                            if self.monochrome_check.isChecked()
                            else self._get_solids_color(name)
                        )
                        if name not in self._data_lines:
                            self._addPlotLines(result_index, v, name, color, line_style)
                            if self.with_errors and self.errors_check.isChecked():
                                self._addErrorLines(
                                    result_index,
                                    v,
                                    p,
                                    e,
                                    ep,
                                    name,
                                    color,
                                    errorline_style,
                                )
                        else:
                            for i, plot in enumerate(self._data_lines[name]):
                                if i == 0:
                                    plot.setPen(
                                        pg.mkPen(
                                            color,
                                            width=self.line_width,
                                            style=line_style,
                                        )
                                    )
                                    plot.setData(self.x_values[result_index], v[i])
                                elif i == 1:
                                    plot.setPen(
                                        pg.mkPen(
                                            color,
                                            width=self.line_width,
                                            style=line_style,
                                        )
                                    )
                                    plot.setData(
                                        self.x_values[result_index],
                                        p,
                                    )
                                elif i == 2:
                                    plot.setPen(
                                        pg.mkPen(
                                            color,
                                            width=self.line_width,
                                            style=errorline_style,
                                        )
                                    )
                                    plot.setData(self.x_values[result_index], v[0] + e)
                                elif i == 3:
                                    plot.setPen(
                                        pg.mkPen(
                                            color,
                                            width=self.line_width,
                                            style=errorline_style,
                                        )
                                    )
                                    plot.setData(self.x_values[result_index], v[0] - e)
                                elif i == 4:
                                    plot.setPen(
                                        pg.mkPen(
                                            color,
                                            width=self.line_width,
                                            style=errorline_style,
                                        )
                                    )
                                    plot.setData(self.x_values[result_index], p + ep)
                                elif i == 5:
                                    plot.setPen(
                                        pg.mkPen(
                                            color,
                                            width=self.line_width,
                                            style=errorline_style,
                                        )
                                    )
                                    plot.setData(self.x_values[result_index], p - ep)

                        conc_y_min, conc_y_max = (
                            min(conc_y_min, *v[0]),
                            max(conc_y_max, *v[0]),
                        )
                    else:
                        if name in self._data_lines:
                            self._removePlotLines(name)

        self.conc_graph.setLimits(
            yMin=conc_y_min * 0.5,
            yMax=conc_y_max * 1.1,
            xMin=x_min * 0.5,
            xMax=x_max * 1.1,
        )
        self.perc_graph.setLimits(
            yMin=perc_y_min,
            yMax=perc_y_max,
            xMin=x_min * 0.5,
            xMax=x_max * 1.1,
        )
        self.conc_graph.enableAutoRange()
        self.perc_graph.enableAutoRange()

    def _addPlotLines(self, ix, v, name, color, line_style):
        self._data_lines[name] = [
            self.conc_graph.plot(
                self.x_values[ix],
                v[0],
                pen=pg.mkPen(color, width=self.line_width, style=line_style),
                name=name,
            ),
            self.perc_graph.plot(
                self.x_values[ix],
                v[0] / self.perc_reference[ix][self.perc_comp] * 100,
                pen=pg.mkPen(color, width=self.line_width, style=line_style),
                name=name,
            ),
        ]

        self._addLegendItem(name)

    def _addErrorLines(self, result_index, v, p, e, ep, name, color, line_style):
        self._data_lines[name] += [
            self.conc_graph.plot(
                self.x_values[result_index],
                v[0] + e,
                pen=pg.mkPen(color, width=self.line_width, style=line_style),
                name=name + "_ub_error",
            ),
            self.conc_graph.plot(
                self.x_values[result_index],
                v[0] - e,
                pen=pg.mkPen(color, width=self.line_width, style=line_style),
                name=name + "_lb_error",
            ),
            self.perc_graph.plot(
                self.x_values[result_index],
                p + ep,
                pen=pg.mkPen(color, width=self.line_width, style=line_style),
                name=name + "_ub_error_perc",
            ),
            self.perc_graph.plot(
                self.x_values[result_index],
                p - ep,
                pen=pg.mkPen(color, width=self.line_width, style=line_style),
                name=name + "_lb_error_perc",
            ),
        ]

    def _addRegionLines(self, result_index, solid_regions, name, color):
        regions_list = []
        for region in solid_regions:
            line_region_conc = pg.LinearRegionItem(
                values=[
                    self.x_values[result_index][region[0]],
                    self.x_values[result_index][region[1] - 1],
                ],
                movable=False,
                pen=pg.mkPen(None),
                brush=pg.mkBrush(color),
            )
            line_region_perc = pg.LinearRegionItem(
                values=[
                    self.x_values[result_index][region[0]],
                    self.x_values[result_index][region[1] - 1],
                ],
                movable=False,
                pen=pg.mkPen(None),
                brush=pg.mkBrush(color),
            )

            self.conc_graph.addItem(line_region_conc)
            self.perc_graph.addItem(line_region_perc)

            pg.InfLineLabel(
                line_region_conc.lines[1],
                name,
                position=0.75,
                rotateAxis=(1, 0),
                anchor=(1, 1),
                color="k",
            )
            pg.InfLineLabel(
                line_region_perc.lines[1],
                name,
                position=0.75,
                rotateAxis=(1, 0),
                anchor=(1, 1),
                color="k",
            )

            regions_list.append([line_region_conc, line_region_perc])

        self._data_lines[name] = regions_list

    def _removeErrorLines(self, name):
        for plot in self._data_lines[name][2:]:
            plot.clear()
        self._data_lines[name] = self._data_lines[name][:2]

    def _removePlotLines(self, name):
        self._removeLegendItem(name)
        for plot in self._data_lines[name]:
            plot.clear()
        self._data_lines.pop(name)

    def _removeRegionLines(self, name):
        for region in self._data_lines[name]:
            self.conc_graph.removeItem(region[0])
            self.perc_graph.removeItem(region[1])
        self._data_lines.pop(name)

    def _initGraphs(self):
        self.conc_graph.setTitle("Distribution of Species")
        self.conc_graph.setLabel(
            "left",
            text="Concentration [mol/l]",
        )

        self.perc_graph.setTitle("Relative Percentage")
        self.perc_graph.setLabel(
            "left",
            text=f"Percentage of {self.comp_names[0]} %",
        )

        if self.is_distribution_result:
            self.conc_graph.setLabel(
                "bottom",
                text=f"Independent Component -log[{self.independent_comp_name}]",
            )
            self.perc_graph.setLabel(
                "bottom",
                text=f"Independent Component -log[{self.independent_comp_name}]",
            )
        else:
            self.conc_graph.setLabel(
                "bottom",
                text="Volume of Titrant [ml]",
            )
            self.perc_graph.setLabel(
                "bottom",
                text="Volume of Titrant [ml]",
            )

            self.titration_graph.setTitle("Titration Curve")
            self.titration_graph.setLabel(
                "bottom",
                text="Volume of Titrant [ml]",
            )
        for plot in self.plot_widgets:
            plot.enableAutoRange()
            plot.setMenuEnabled(False)

        self._createLegend()
        self._set_plot_fontsize(self.font_size)

    def _resetGraphs(self):
        self.conc_graph.clear()
        self.perc_graph.clear()
        self.titration_graph.clear()
        for legend in self.legends:
            legend.deleteLater()
        self._createLegend()

    def _createLegend(self):
        self.conc_legend = pg.LegendItem(
            brush=pg.mkBrush(None),
            labelTextSize=f"{self.font_size}pt",
            verAlignment=Qt.AlignmentFlag.AlignBaseline,
            offset=(-10, 100),
        )
        self.perc_legend = pg.LegendItem(
            brush=pg.mkBrush(None),
            labelTextSize=f"{self.font_size}pt",
            verAlignment=Qt.AlignmentFlag.AlignVCenter,
            offset=(-10, 100),
        )
        self.titr_legend = pg.LegendItem(
            brush=pg.mkBrush(None),
            labelTextSize=f"{self.font_size}pt",
            verAlignment=Qt.AlignmentFlag.AlignVCenter,
            offset=(-10, 100),
        )
        self.conc_legend.setParentItem(self.conc_graph.getPlotItem())
        self.perc_legend.setParentItem(self.perc_graph.getPlotItem())
        self.titr_legend.setParentItem(self.titration_graph.getPlotItem())
        self.legends = [self.conc_legend, self.perc_legend, self.titr_legend]

    def _addLegendItem(self, name):
        self.conc_legend.addItem(self._data_lines[name][0], name)
        self.perc_legend.addItem(self._data_lines[name][1], name)

    def _removeLegendItem(self, name):
        self.conc_legend.removeItem(name)
        self.perc_legend.removeItem(name)

    def changeMonochrome(self, checked):
        if checked:
            self.perc_legend.hide()
            self.conc_legend.hide()
        else:
            self.conc_legend.show()
            self.perc_legend.show()
        self.redraw()

    def changeCUnit(self, unit):
        match unit:
            case "mol/l":
                self.conc_graph.setLabel(
                    "left",
                    text=f"Concentration [{unit}]",
                )
                factor = 1
            case "mmol/l":
                self.conc_graph.setLabel(
                    "left",
                    text=f"Concentration [{unit}]",
                )
                factor = 1e3
            case "\u03bcmol/l":  # micro
                self.conc_graph.setLabel(
                    "left",
                    text=f"Concentration [{unit}]",
                )
                factor = 1e6
            case _:
                return

        for i in range(self.number_of_results):
            for k, v in self.original_soluble_values[i].items():
                self.soluble_values[i][k] = list(map(lambda x: x * factor, v))
            for k, v in self.original_solids_values[i].items():
                self.solids_values[i][k] = list(map(lambda x: x * factor, v))

        if self.with_errors:
            for i in range(self.number_of_results):
                for k, v in self.original_soluble_errors[i].items():
                    self.soluble_errors[i][k] = list(map(lambda x: x * factor, v))
                for k, v in self.original_solids_errors[i].items():
                    self.solids_errors[i][k] = list(map(lambda x: x * factor, v))
        self.redraw()

    def changeVUnit(self, unit):
        match unit:
            case "l":
                self.conc_graph.setLabel("bottom", text=f"Volume of Titrant [{unit}]")
                self.perc_graph.setLabel("bottom", text=f"Volume of Titrant [{unit}]")
                self.titration_graph.setLabel(
                    "bottom", text=f"Volume of Titrant [{unit}]"
                )
                factor = 1e-3
            case "ml":
                self.conc_graph.setLabel("bottom", text=f"Volume of Titrant [{unit}]")
                self.perc_graph.setLabel("bottom", text=f"Volume of Titrant [{unit}]")
                self.titration_graph.setLabel(
                    "bottom", text=f"Volume of Titrant [{unit}]"
                )
                factor = 1
            case _:
                return
        for i in range(self.number_of_results):
            self.x_values[i] = self.original_x_values[i] * factor

        self.redraw()
        self._updateTitrationCurve()

    def _updateTitrationCurve(self, *args):
        comp_name = self.componentComboBox.currentText()
        result_index = self.titrationSelector.currentIndex()

        self.titration_graph.clear()
        self.titr_legend.clear()

        if comp_name != "Pot.":
            y = -np.log10(self.soluble_values[result_index][comp_name][0])

            pl_line = pg.PlotDataItem(
                self.x_values[result_index],
                y,
                pen=pg.mkPen("b", width=self.line_width, style=Qt.PenStyle.SolidLine),
            )
            self.titration_graph.addItem(pl_line)
            self.titr_legend.addItem(pl_line, f"p{comp_name}")
            self.titration_graph.setLabel(
                "left",
                text=f"p{comp_name}",
            )
        else:
            y = self.potential[result_index]

            potential_line = pg.PlotDataItem(
                self.x_values[result_index],
                y,
                pen=pg.mkPen("r", width=self.line_width, style=Qt.PenStyle.SolidLine),
                symbol="o",
                symbolSize=5,
                symbolBrush="r",
            )
            calculated_line = pg.PlotDataItem(
                self.x_values[result_index],
                self.calculated_potential[result_index],
                pen=pg.mkPen("b", width=self.line_width, style=Qt.PenStyle.SolidLine),
            )

            self.titration_graph.addItem(potential_line)
            self.titration_graph.addItem(calculated_line)

            self.titr_legend.addItem(potential_line, "Experimental")
            self.titr_legend.addItem(calculated_line, "Calculated")

            self.titration_graph.setLabel(
                "left",
                text="Potential [mV]",
            )

        self.titration_graph.setLimits(
            yMin=min(y),
            yMax=max(y),
            xMin=min(self.x_values[result_index]) * 0.5,
            xMax=max(self.x_values[result_index]) * 1.1,
        )
        self.titration_graph.autoRange()

    def _updatePercentageReference(self, comp_name: str):
        self.perc_graph.setLabel(
            "left",
            text=f"Percentage of {self.componentComboBox_perc.currentText()} %",
        )

        choice = self.componentComboBox_perc.currentText()
        self.perc_comp = self.componentComboBox_perc.currentIndex()

        for row in range(self.speciesModel.rowCount()):
            item = self.speciesModel.item(row)
            if choice not in item.text():
                item.setCheckState(Qt.CheckState.Unchecked)
        for row in range(self.solidsModel.rowCount()):
            item = self.solidsModel.item(row)
            if choice not in item.text():
                item.setCheckState(Qt.CheckState.Unchecked)
        self.redraw()

    def _check_checked_state(self, i):
        if i.isCheckable():  # Skip data columns.
            name = i.text()
            checked = i.checkState() == Qt.CheckState.Checked

            if name in self._data_visible:
                if not checked:
                    self._data_visible.remove(name)
                    self.redraw()
                    if self._data_visible == []:
                        self._resetGraphs()
            else:
                if checked:
                    self._data_visible.append(name)
                    self.redraw()
        else:
            self.redraw()

    def _get_species_color(self, species, new=False):
        if new:
            color = next(self.color_palette)
        else:
            color = self.speciesModel.item(
                self.speciesModel.findItems(species, Qt.MatchFlag.MatchExactly, 0)[0]
                .index()
                .row(),
                1,
            ).text()

        return color

    def _get_solids_color(self, solids, new=False):
        if new:
            color = next(self.color_palette_solids)
        else:
            color = self.solidsModel.item(
                self.solidsModel.findItems(solids, Qt.MatchFlag.MatchExactly, 0)[0]
                .index()
                .row(),
                1,
            ).text()

        return color

    def _set_plot_fontsize(self, font_size):
        self.font_size = font_size
        font = QFont("Arial", font_size)
        for plot_widget, legend in zip(self.plot_widgets, self.legends):
            plot_item = plot_widget.getPlotItem()
            # Set the font size for the plot title
            plot_item.setTitle(plot_item.titleLabel.text, size=f"{font_size}pt")

            # Set the font size for the tick labels
            plot_item.getAxis("left").setStyle(tickFont=font)
            plot_item.getAxis("bottom").setStyle(tickFont=font)

            # Set the font size for the tick labels
            plot_item.getAxis("left").label.setFont(font)
            plot_item.getAxis("bottom").label.setFont(font)

            legend.setLabelTextSize(f"{font_size}pt")
            for _, item in legend.items:
                item.setText(item.text, size=f"{font_size}pt")

    def _set_line_width(self, line_width):
        self.line_width = line_width
        self.redraw()
        self._updateTitrationCurve()

    def _calculate_error_percentages(self, result_index, e, p, adjust_factor, conc):
        error_percentage = p * np.sqrt(
            (e / conc * adjust_factor) ** 2
            + (
                self.sigma_perc_reference[result_index][self.perc_comp]
                / self.perc_reference[result_index][self.perc_comp]
            )
            ** 2
        )

        return error_percentage

    def exportGraph(self):
        selected_plot = self.tabWidget.currentWidget().findChild(pg.PlotWidget)
        ExportGraphDialog(self, selected_plot).exec()

    def _toggle_legend_visibility(self, checked):
        for legend in self.legends:
            if checked:
                legend.hide()
            else:
                legend.show()


class ExportGraphDialog(QDialog, Ui_ExportGraphDialog):
    def __init__(self, parent: PlotWindow, graph: pg.PlotWidget):
        super().__init__(parent)
        self.setupUi(self)
        self.graph = graph

        self.export_button.clicked.connect(self.save_file)
        self.transparent_check.clicked.connect(self.toggle_transparent)

    def toggle_transparent(self, checked):
        self.background.setEnabled(not checked)
        self.backgroundLabel.setEnabled(not checked)

    def save_file(self):
        exporter = pg.exporters.ImageExporter(self.graph.plotItem)

        exporter.parameters()["width"] = int(
            exporter.parameters()["width"] * self.scaleDoubleSpinBox.value()
        )

        exporter.parameters()["background"] = (
            "#00000000"
            if self.transparent_check.isChecked()
            else self.background.color()
        )
        exporter.parameters()["antialias"] = False

        path, _ = QFileDialog.getSaveFileName(
            self, "Export Plot", "", "PNG File (*.png)"
        )

        if path:
            file_name = Path(path).parents[0]
            file_name = file_name.joinpath(Path(path).stem)
            file_name = file_name.with_suffix(".png")

            exporter.export(str(file_name))

        self.accept()
