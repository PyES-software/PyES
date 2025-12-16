import sys
import typing
from itertools import cycle
from pathlib import Path

import numpy as np
import pyqtgraph as pg
import pyqtgraph.exporters
from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItem, QStandardItemModel
from PySide6.QtWidgets import QDialog, QFileDialog, QInputDialog, QMainWindow
from ui.PyES_graphExport import Ui_ExportGraphDialog
from ui.PyES_pyqtgraphPlotExport import Ui_PlotWindow
from viewmodels.delegate import ColorPickerDelegate

if typing.TYPE_CHECKING:
    from windows.window import MainWindow

# Setup white background and black axis for the plot
# THIS NEEDS TO BE DONE BOFORE LOADING THE UI FILE
pg.setConfigOption("background", "w")
pg.setConfigOption("foreground", "k")

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
        super().__init__()
        self.setupUi(self)
        self.componentComboBox.currentTextChanged.connect(self._updateTitrationCurve)
        self.componentComboBox_perc.currentTextChanged.connect(
            self._updatePercentageReference
        )
        self.exportButton.clicked.connect(self._exportGraph)
        self.monochrome_check.clicked.connect(self.changeMonochrome)
        self.monochrome_color.colorChanged.connect(self.redraw)

        self.c_unit.currentTextChanged.connect(self.changeCUnit)
        self.v_unit.currentTextChanged.connect(self.changeVUnit)

        # Colour cycle to use for plotting species.
        self.color_palette = cycle(PALETTE)

        self.color_palette_solids = cycle(PALETTE)

        # Inherit the required informations from the primary window
        self.distribution = parent.dmode.currentIndex() == 1

        self.with_solids = not parent.result["solid_distribution"].empty
        self.with_errors = parent.uncertaintyMode.isChecked()

        self.conc_result = parent.result["species_distribution"]
        self.perc_result = parent.result["species_percentages"]
        self.perc_result.columns = self.conc_result.columns

        if not self.with_errors:
            self.errors_check.setEnabled(False)

        self.conc_sd = parent.result["species_sigma"]
        self.solid_sd = parent.result["solid_sigma"]
        self.solid_sd.columns = [column + "_(s)" for column in self.solid_sd.columns]

        self.solid_conc_result = parent.result["solid_distribution"][
            [
                column
                for column in parent.result["solid_distribution"]
                if not (column.startswith("Prec.") or column.startswith("SI"))
            ]
        ]
        self.solid_conc_result.columns = [
            column + "_(s)" for column in self.solid_conc_result.columns
        ]

        self.solid_perc_result = parent.result["solid_percentages"]
        self.solid_perc_result.columns = self.solid_conc_result.columns

        self.comps = parent.result["comp_info"]
        self.comp_names = list(self.comps.index)

        # Get values for the x from the index
        self.original_x_values = self.conc_result.index.get_level_values(0)
        self.x_values = self.conc_result.index.get_level_values(0).to_numpy()

        self.perc_comp = 0
        if self.distribution:
            self.tot_conc = parent.result["comp_info"]["Tot. C."].to_numpy()
            self.point_conc = None
            self.perc_reference = self.tot_conc
        else:
            self.tot_conc = parent.result["comp_info"]["Vessel Conc."].to_numpy()
            self.point_conc = parent.result["comp_info"]["Titrant Conc."].to_numpy()

            self.perc_reference = self.tot_conc[:, None] + (
                self.point_conc[:, None] * self.x_values
            )

        self.original_species_values = {
            name: [
                self.conc_result[name].to_numpy(dtype=float),
                self.perc_result[name].to_numpy(dtype=float),
            ]
            for name in self.conc_result.columns
        }
        self.species_values = self.original_species_values.copy()

        self.original_solids_values = {
            name: [
                self.solid_conc_result[name].to_numpy(dtype=float),
                self.solid_perc_result[name].to_numpy(dtype=float),
            ]
            for name in self.solid_conc_result.columns
        }
        self.solids_values = self.original_solids_values.copy()

        if self.with_errors:
            self.original_species_errors = {
                name: [
                    self.conc_sd[name].to_numpy(dtype=float)
                    + self.species_values[name][0],
                    -self.conc_sd[name].to_numpy(dtype=float)
                    + self.species_values[name][0],
                ]
                for name in self.conc_result.columns
            }
            self.species_errors = self.original_species_errors.copy()

            self.original_solids_errors = {
                name: [
                    self.solid_sd[name].to_numpy(dtype=float)
                    + self.solids_values[name][0],
                    -self.solid_sd[name].to_numpy(dtype=float)
                    + self.solids_values[name][0],
                ]
                for name in self.solid_conc_result.columns
            }
            self.solids_errors = self.original_solids_errors.copy()

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
        self.speciesModel.itemChanged.connect(self.check_checked_state)
        self.solidsModel.itemChanged.connect(self.check_checked_state)

        self.speciesView.setModel(self.speciesModel)
        self.solidsView.setModel(self.solidsModel)

        self.speciesView.setItemDelegateForColumn(1, ColorPickerDelegate(self))
        self.solidsView.setItemDelegateForColumn(1, ColorPickerDelegate(self))

        # Each colum holds a checkbox and the species name
        for column in self.conc_result.columns:
            item = QStandardItem()
            item.setText(column)
            item.setColumnCount(2)
            item.setCheckable(True)
            item.setEditable(False)

            item2 = QStandardItem()
            item2.setText(self.get_species_color(column, new=True))
            self.speciesModel.appendRow([item, item2])

        if self.with_solids:
            for column in self.solid_conc_result.columns:
                item = QStandardItem()
                item.setText(column)
                item.setColumnCount(2)
                item.setCheckable(True)
                item.setEditable(False)

                item2 = QStandardItem()
                item2.setText(self.get_solids_color(column, new=True))
                self.solidsModel.appendRow([item, item2])
        else:
            self.regions_check.setEnabled(False)

        self.componentComboBox_perc.blockSignals(True)
        self.componentComboBox_perc.addItems(self.comp_names)
        self.componentComboBox_perc.blockSignals(False)

        if self.distribution:
            self.independent_comp_name = parent.indComp.currentText()
            self.tabWidget.setTabEnabled(2, False)
            self.v_unit.setEnabled(False)
            self.v_unit_label.setEnabled(False)
            ind_comp_idx = np.argwhere(np.isnan(self.tot_conc))[0, 0]
            self.componentComboBox_perc.setItemData(
                ind_comp_idx,
                self.comp_names[ind_comp_idx],
                Qt.ItemDataRole.UserRole - 1,
            )

        else:
            self.componentComboBox.addItems(self.comp_names)

        # Resize column to newly added species
        self.speciesView.resizeColumnToContents(0)
        self.speciesView.setColumnWidth(1, self.speciesView.rowHeight(0))
        self.solidsView.resizeColumnToContents(0)
        self.solidsView.setColumnWidth(1, self.solidsView.rowHeight(0))

        self._initGraphs()

    def check_checked_state(self, i):
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

    def get_species_color(self, species, new=False):
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

    def get_solids_color(self, solids, new=False):
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

    def redraw(self):
        conc_y_min, conc_y_max = 0, sys.maxsize
        perc_y_min, perc_y_max = 0, sys.maxsize
        x_min, x_max = min(self.x_values), max(self.x_values)

        for name in self.conc_result.columns:
            v = self.species_values[name]
            if self.with_errors:
                e = self.species_errors[name]
            if name in self._data_visible:
                line_style = Qt.PenStyle.SolidLine
                errorline_style = Qt.PenStyle.DashDotDotLine
                color = (
                    self.monochrome_color.color()
                    if self.monochrome_check.isChecked()
                    else self.get_species_color(name)
                )
                if name not in self._data_lines:
                    self._addPlotLines(v, name, color, line_style)
                    if self.with_errors and self.errors_check.isChecked():
                        self._addErrorLines(e, name, color, errorline_style)
                else:
                    for i, plot in enumerate(self._data_lines[name]):
                        if i == 0:
                            plot.setPen(pg.mkPen(color, width=2, style=line_style))
                            plot.setData(self.x_values, v[i])
                        elif i == 1:
                            plot.setPen(pg.mkPen(color, width=2, style=line_style))
                            plot.setData(
                                self.x_values,
                                v[0] / self.perc_reference[self.perc_comp] * 100,
                            )
                        else:
                            plot.setPen(pg.mkPen(color, width=2, style=errorline_style))
                            plot.setData(self.x_values, e[i - 2])

                conc_y_min, conc_y_max = min(conc_y_min, *v[0]), max(conc_y_max, *v[0])
                perc_y_min, perc_y_max = min(perc_y_min, *v[1]), max(perc_y_max, *v[1])
            else:
                if name in self._data_lines:
                    self._removePlotLines(name)
        if self.with_solids:
            for name in self.solid_conc_result.columns:
                if self.regions_check.isChecked():
                    solid_regions = np.reshape(
                        np.diff(
                            np.r_[0, (self.solid_conc_result[name] > 0).astype(int), 0]
                        ).nonzero()[0],
                        (-1, 2),
                    )

                    if name in self._data_visible:
                        color = self.get_solids_color(name) + "66"
                        if name not in self._data_lines:
                            self._addRegionLines(solid_regions, name, color)
                        else:
                            for plot in self._data_lines[name]:
                                for region in plot:
                                    region.setBrush(pg.mkBrush(color))
                    else:
                        if name in self._data_lines:
                            self._removeRegionLines(name)
                else:
                    v = self.solids_values[name]
                    if self.with_errors and self.errors_check.isChecked():
                        e = self.solids_errors[name]
                    if name in self._data_visible:
                        line_style = Qt.PenStyle.DashLine
                        errorline_style = Qt.PenStyle.DashDotDotLine
                        color = (
                            self.monochrome_color.color()
                            if self.monochrome_check.isChecked()
                            else self.get_solids_color(name)
                        )
                        if name not in self._data_lines:
                            self._addPlotLines(v, name, color, line_style)
                            if self.with_errors and self.errors_check.isChecked():
                                self._addErrorLines(e, name, color, errorline_style)
                        else:
                            for i, plot in enumerate(self._data_lines[name]):
                                if i == 0:
                                    plot.setPen(
                                        pg.mkPen(color, width=2, style=line_style)
                                    )
                                    plot.setData(self.x_values, v[i])
                                elif i == 1:
                                    plot.setPen(
                                        pg.mkPen(color, width=2, style=line_style)
                                    )
                                    plot.setData(
                                        self.x_values,
                                        v[i]
                                        / self.perc_reference[self.perc_comp]
                                        * 100,
                                    )
                                else:
                                    plot.setPen(
                                        pg.mkPen(color, width=2, style=errorline_style)
                                    )
                                    plot.setData(self.x_values, e[i - 2])

                        conc_y_min, conc_y_max = (
                            min(conc_y_min, *v[0]),
                            max(conc_y_max, *v[0]),
                        )
                        perc_y_min, perc_y_max = (
                            min(perc_y_min, *v[1]),
                            max(perc_y_max, *v[1]),
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
            yMin=perc_y_min * 0.5,
            yMax=perc_y_max * 1.1,
            xMin=x_min * 0.5,
            xMax=x_max * 1.1,
        )
        self.conc_graph.enableAutoRange()
        self.perc_graph.enableAutoRange()

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

        if self.distribution:
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
                text="Volume of Titrant [l]",
            )
            self.perc_graph.setLabel(
                "bottom",
                text="Volume of Titrant [l]",
            )

            self.titration_graph.setTitle("Titration Curve")
            self.titration_graph.setLabel(
                "bottom",
                text="Volume of Titrant [l]",
            )

        self.conc_graph.enableAutoRange()
        self.perc_graph.enableAutoRange()
        self.titration_graph.enableAutoRange()

        self._createLegend()

    def _removePlotLines(self, name):
        self._removeLegendItem(name)
        for plot in self._data_lines[name]:
            plot.clear()
        self._data_lines.pop(name)

    def _removeErrorLines(self, name):
        for plot in self._data_lines[name][2:]:
            plot.clear()
        self._data_lines[name] = self._data_lines[name][:2]

    def _addPlotLines(self, values, name, color, line_style):
        self._data_lines[name] = [
            self.conc_graph.plot(
                self.x_values,
                values[0],
                pen=pg.mkPen(color, width=2, style=line_style),
                name=name,
            ),
            self.perc_graph.plot(
                self.x_values,
                values[0] / self.perc_reference[self.perc_comp] * 100,
                pen=pg.mkPen(color, width=2, style=line_style),
                name=name,
            ),
        ]
        self._addLegendItem(name)

    def _addErrorLines(self, values, name, color, line_style):
        self._data_lines[name] += [
            self.conc_graph.plot(
                self.x_values,
                values[0],
                pen=pg.mkPen(color, width=2, style=line_style),
                name=name + "_ub_error",
            ),
            self.conc_graph.plot(
                self.x_values,
                values[1],
                pen=pg.mkPen(color, width=2, style=line_style),
                name=name + "_lb_error",
            ),
        ]

    def _removeRegionLines(self, name):
        for region in self._data_lines[name]:
            self.conc_graph.removeItem(region[0])
            self.perc_graph.removeItem(region[1])
        self._data_lines.pop(name)

    def _addRegionLines(self, solid_regions, name, color):
        regions_list = []
        for region in solid_regions:
            line_region_conc = pg.LinearRegionItem(
                values=[self.x_values[region[0]], self.x_values[region[1] - 1]],
                movable=False,
                pen=pg.mkPen(None),
                brush=pg.mkBrush(color),
            )
            line_region_perc = pg.LinearRegionItem(
                values=[self.x_values[region[0]], self.x_values[region[1] - 1]],
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

    def _addLegendItem(self, name):
        self.conc_legend.addItem(self._data_lines[name][0], name)
        self.perc_legend.addItem(self._data_lines[name][1], name)

    def _removeLegendItem(self, name):
        self.conc_legend.removeItem(name)
        self.perc_legend.removeItem(name)

    def changeSolidsGraphics(self):
        if self.regions_check.isChecked():
            for name in self.solid_conc_result.columns:
                if name in self._data_visible:
                    self._removePlotLines(name)
        else:
            for name in self.solid_conc_result.columns:
                if name in self._data_visible:
                    self._removeRegionLines(name)

        self.redraw()

    def changeMonochrome(self, checked):
        if checked:
            self.perc_legend.hide()
            self.conc_legend.hide()
        else:
            self.conc_legend.show()
            self.perc_legend.show()
        self.redraw()

    def changeErrorsGraphics(self):
        if self.errors_check.isChecked():
            for name in self.conc_result.columns:
                if name in self._data_visible:
                    e = self.species_errors[name]
                    color = self.get_species_color(name)

                    self._addErrorLines(
                        e, name, color, line_style=Qt.PenStyle.DashDotDotLine
                    )
            for name in self.solid_conc_result.columns:
                if name in self._data_visible:
                    e = self.solids_errors[name]
                    color = self.get_solids_color(name)

                    self._addErrorLines(
                        e, name, color, line_style=Qt.PenStyle.DashDotDotLine
                    )
        else:
            for name in list(self.solid_conc_result.columns) + list(
                self.conc_result.columns
            ):
                if name in self._data_visible:
                    self._removeErrorLines(name)
        self.redraw()

    def changeCUnit(self, current_text):
        match current_text:
            case "mol/l":
                self.conc_graph.setLabel(
                    "left",
                    text=f"Concentration [{current_text}]",
                )
                factor = 1
            case "mmol/l":
                self.conc_graph.setLabel(
                    "left",
                    text=f"Concentration [{current_text}]",
                )
                factor = 1e3
            case "\u03BCmol/l":  # micro
                self.conc_graph.setLabel(
                    "left",
                    text=f"Concentration [{current_text}]",
                )
                factor = 1e6
            case _:
                return

        for k, v in self.original_species_values.items():
            self.species_values[k] = list(map(lambda x: x * factor, v))
        for k, v in self.original_solids_values.items():
            self.solids_values[k] = list(map(lambda x: x * factor, v))

        if self.with_errors:
            for k, v in self.original_species_errors.items():
                self.species_errors[k] = list(map(lambda x: x * factor, v))
            for k, v in self.original_solids_errors.items():
                self.solids_errors[k] = list(map(lambda x: x * factor, v))
        self.redraw()

    def changeVUnit(self, current_text):
        match current_text:
            case "l":
                self.conc_graph.setLabel(
                    "bottom",
                    text=f"Volume of Titrant [{current_text}]",
                )
                factor = 1
            case "ml":
                self.conc_graph.setLabel(
                    "bottom", text=f"Volume of Titrant [{current_text}]"
                )
                self.perc_graph.setLabel(
                    "bottom", text=f"Volume of Titrant [{current_text}]"
                )
                factor = 1e3
            case _:
                return
        self.x_values = self.original_x_values * factor
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

    def _createLegend(self):
        self.conc_legend = pg.LegendItem()
        self.perc_legend = pg.LegendItem()
        self.conc_legend.setParentItem((self.conc_graph.graphicsItem()))
        self.perc_legend.setParentItem((self.perc_graph.graphicsItem()))

    def _resetGraphs(self):
        self.conc_graph.clear()
        self.perc_graph.clear()
        self.conc_legend = pg.LegendItem()
        self.perc_legend = pg.LegendItem()
        self.conc_legend.setParentItem((self.conc_graph.graphicsItem()))
        self.perc_legend.setParentItem((self.perc_graph.graphicsItem()))

    def _updateTitrationCurve(self, comp_name: str):
        self.titration_graph.setLabel(
            "left",
            text=f"p{self.componentComboBox.currentText()}",
        )
        self.titration_graph.clear()
        self.titration_graph.plot(
            self.original_x_values,
            -np.log10(self.conc_result[comp_name].to_numpy()),
            pen=pg.mkPen("b", width=2, style=Qt.PenStyle.SolidLine),
        )

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

    # self.titration_graph.clear()
    # self.titration_graph.plot(
    #     self.original_x_values,
    #     -np.log10(self.conc_result[comp_name].to_numpy()),
    #     pen=pg.mkPen("b", width=2, style=Qt.PenStyle.SolidLine),
    # )

    def _exportGraph(self):
        selected_plot = self.tabWidget.currentWidget().findChild(pg.PlotWidget)
        ExportGraphDialog(self, selected_plot).exec()


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
