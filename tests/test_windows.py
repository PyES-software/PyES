
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QMessageBox, QTableView
from pytest import MonkeyPatch, fixture
from pytestqt.qtbot import QtBot

from pyes.windows.window import MainWindow


@fixture
def window(qtbot: QtBot, monkeypatch: MonkeyPatch):
    window = MainWindow()
    monkeypatch.setattr(window, "closeEvent", lambda *args: True)
    qtbot.addWidget(window)
    return window


@fixture
def window_solid(qtbot: QtBot, monkeypatch: MonkeyPatch):
    window = MainWindow()
    monkeypatch.setattr(window, "closeEvent", lambda *args: True)

    qtbot.addWidget(window)

    window.numPhases.setValue(1)
    window.tablesTab.setTabVisible(1, True)
    window.tablesTab.setTabVisible(0, False)
    return window


def select_cell(widget: QTableView, qtbot: QtBot, position: tuple[int, int]):
    row, col = position
    rect = widget.visualRect(widget.model().index(row, col))
    qtbot.mouseClick(widget.viewport(), Qt.MouseButton.LeftButton, pos=rect.center())


def assert_comp_names_headers(window: MainWindow, pos: int, value: str):
    assert (
        window.speciesView.model().headerData(pos + 8, Qt.Orientation.Horizontal)
        == value
    )
    assert (
        window.solidSpeciesView.model().headerData(pos + 8, Qt.Orientation.Horizontal)
        == value
    )
    assert window.concView.model().headerData(pos, Qt.Orientation.Vertical) == value
    assert (
        window.dmode1_concView.model().headerData(pos, Qt.Orientation.Vertical) == value
    )


class TestMainWindow:
    def test_default_values(self, window: MainWindow):
        assert window.uncertaintyMode.isChecked() == False
        assert window.imode.currentIndex() == 0

        assert window.dmode.currentIndex() == 0

        assert window.numComp.value() == 1
        assert window.numSpecies.value() == 1
        assert window.numPhases.value() == 0

    def test_comp_model(self, window: MainWindow):
        assert window.compView.model() is window.compModel

        assert window.compView.model().rowCount() == 1
        assert window.compView.model().columnCount() == 2

    def test_species_model(self, window: MainWindow):
        assert window.speciesView.model() is window.speciesModel

        assert window.speciesView.model().rowCount() == 1
        assert window.speciesView.model().columnCount() == 10

    def test_solid_model(self, window: MainWindow):
        assert window.solidSpeciesView.model() is window.solidSpeciesModel

        assert window.solidSpeciesView.model().rowCount() == 0
        assert window.solidSpeciesView.model().columnCount() == 10


class TestCompChanges:
    def test_add_comp_above_unselected(self, window: MainWindow, qtbot: QtBot):
        qtbot.mouseClick(window.insert_above_comp_button, Qt.MouseButton.LeftButton)

        assert window.numComp.value() == 2
        assert window.compView.model().rowCount() == 2

        assert window.speciesView.model().columnCount() == 11
        assert window.solidSpeciesView.model().columnCount() == 11

        assert (
            window.compView.model().data(
                window.compView.model().index(0, 0), Qt.ItemDataRole.DisplayRole
            )
            == "COMP1"
        )

        assert_comp_names_headers(window, 0, "COMP1")

    def test_add_comp_below_unselected(self, window: MainWindow, qtbot: QtBot):
        qtbot.mouseClick(window.insert_below_comp_button, Qt.MouseButton.LeftButton)

        assert window.numComp.value() == 2
        assert window.compView.model().rowCount() == 2

        assert window.speciesView.model().columnCount() == 11
        assert window.solidSpeciesView.model().columnCount() == 11

        assert (
            window.compView.model().data(
                window.compView.model().index(1, 0), Qt.ItemDataRole.DisplayRole
            )
            == "COMP2"
        )

        assert_comp_names_headers(window, 1, "COMP2")

    def test_add_comp_above_selected(self, window: MainWindow, qtbot: QtBot):
        window.numComp.setValue(2)

        select_cell(window.compView, qtbot, (0, 1))
        qtbot.mouseClick(window.insert_above_comp_button, Qt.MouseButton.LeftButton)

        assert window.numComp.value() == 3
        assert window.compView.model().rowCount() == 3

        assert window.speciesView.model().columnCount() == 12
        assert window.solidSpeciesView.model().columnCount() == 12

        assert (
            window.compView.model().data(
                window.compView.model().index(1, 0), Qt.ItemDataRole.DisplayRole
            )
            == "COMP1"
        )

        assert_comp_names_headers(window, 1, "COMP1")

    def test_add_comp_below_selected(self, window: MainWindow, qtbot: QtBot):
        window.numComp.setValue(3)
        window.compView.selectRow(1)

        select_cell(window.compView, qtbot, (1, 1))
        qtbot.mouseClick(window.insert_below_comp_button, Qt.MouseButton.LeftButton)

        assert window.numComp.value() == 4
        assert window.compView.model().rowCount() == 4

        assert window.speciesView.model().columnCount() == 13
        assert window.solidSpeciesView.model().columnCount() == 13

        assert (
            window.compView.model().data(
                window.compView.model().index(2, 0), Qt.ItemDataRole.DisplayRole
            )
            == "COMP3"
        )

        assert_comp_names_headers(window, 2, "COMP3")

    def test_increase_comp_key(self, window: MainWindow, qtbot: QtBot):
        qtbot.keyClick(window.numComp, Qt.Key.Key_Up)

        assert window.numComp.value() == 2

        assert window.speciesView.model().columnCount() == 11
        assert window.solidSpeciesView.model().columnCount() == 11

        assert (
            window.compView.model().data(
                window.compView.model().index(
                    window.compView.model().rowCount() - 1, 0
                ),
                Qt.ItemDataRole.DisplayRole,
            )
            == "COMP2"
        )

        assert_comp_names_headers(window, 1, "COMP2")

    def test_decrease_comp_key(self, window: MainWindow, qtbot: QtBot):
        qtbot.keyClick(window.numComp, Qt.Key.Key_Down)
        assert window.numComp.value() == 1
        assert_comp_names_headers(window, 0, "COMP1")

        window.numComp.setValue(2)

        qtbot.keyClick(window.numComp, Qt.Key.Key_Down)
        assert window.numComp.value() == 1
        assert window.speciesView.model().columnCount() == 10
        assert window.solidSpeciesView.model().columnCount() == 10

        assert_comp_names_headers(window, 0, "COMP1")

    def test_remove_comp(
        self, window: MainWindow, qtbot: QtBot, monkeypatch: MonkeyPatch
    ):
        window.numComp.setValue(3)
        select_cell(window.compView, qtbot, (1, 1))

        monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)
        qtbot.mouseClick(window.remove_comp_button, Qt.MouseButton.LeftButton)

        assert window.numComp.value() == 2

        assert window.speciesView.model().columnCount() == 11
        assert window.solidSpeciesView.model().columnCount() == 11

        assert (
            window.compView.model().data(
                window.compView.model().index(window.compView.model().rowCount() - 1, 0)
            )
            == "COMP3"
        )

        assert_comp_names_headers(window, 1, "COMP3")

    def test_abort_remove_comp(
        self, window: MainWindow, qtbot: QtBot, monkeypatch: MonkeyPatch
    ):
        window.numComp.setValue(3)

        select_cell(window.compView, qtbot, (1, 1))
        monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.No)
        qtbot.mouseClick(window.remove_comp_button, Qt.MouseButton.LeftButton)

        assert window.numComp.value() == 3

        assert window.speciesView.model().columnCount() == 12
        assert window.solidSpeciesView.model().columnCount() == 12

        assert (
            window.compView.model().data(
                window.compView.model().index(window.compView.model().rowCount() - 1, 0)
            )
            == "COMP3"
        )

        assert_comp_names_headers(window, 2, "COMP3")

    def test_move_comp_up(self, window: MainWindow, qtbot: QtBot):
        window.numComp.setValue(3)

        select_cell(window.compView, qtbot, (1, 1))
        qtbot.mouseClick(window.move_up_comp_button, Qt.MouseButton.LeftButton)

        comp_names = []
        for i in range(window.compView.model().rowCount()):
            comp_names.append(
                window.compView.model().data(window.compView.model().index(i, 0))
            )

        assert_comp_names_headers(window, 1, "COMP1")

    def test_move_comp_up_first(self, window: MainWindow, qtbot: QtBot):
        window.numComp.setValue(3)

        select_cell(window.compView, qtbot, (0, 1))
        qtbot.mouseClick(window.move_up_comp_button, Qt.MouseButton.LeftButton)

        comp_names = []
        for i in range(window.compView.model().rowCount()):
            comp_names.append(
                window.compView.model().data(window.compView.model().index(i, 0))
            )

        assert comp_names == ["COMP1", "COMP2", "COMP3"]

        assert_comp_names_headers(window, 0, "COMP1")
        assert_comp_names_headers(window, 1, "COMP2")
        assert_comp_names_headers(window, 2, "COMP3")

    def test_move_comp_down(self, window: MainWindow, qtbot: QtBot):
        window.numComp.setValue(3)

        select_cell(window.compView, qtbot, (1, 1))
        qtbot.mouseClick(window.move_down_comp_button, Qt.MouseButton.LeftButton)

        comp_names = []
        for i in range(window.compView.model().rowCount()):
            comp_names.append(
                window.compView.model().data(window.compView.model().index(i, 0))
            )

        assert comp_names == ["COMP1", "COMP3", "COMP2"]

        assert_comp_names_headers(window, 0, "COMP1")
        assert_comp_names_headers(window, 1, "COMP3")
        assert_comp_names_headers(window, 2, "COMP2")

    def test_move_comp_down_last(self, window: MainWindow, qtbot: QtBot):
        window.numComp.setValue(3)

        select_cell(window.compView, qtbot, (window.compView.model().rowCount() - 1, 1))
        qtbot.mouseClick(window.move_down_comp_button, Qt.MouseButton.LeftButton)

        comp_names = []
        for i in range(window.compView.model().rowCount()):
            comp_names.append(
                window.compView.model().data(window.compView.model().index(i, 0))
            )

        assert comp_names == ["COMP1", "COMP2", "COMP3"]

        assert_comp_names_headers(window, 0, "COMP1")
        assert_comp_names_headers(window, 1, "COMP2")
        assert_comp_names_headers(window, 2, "COMP3")

    def test_rename_comp(self, window: MainWindow, qtbot: QtBot):
        window.compView.model().setData(
            window.compView.model().index(0, 0), "Test", Qt.ItemDataRole.EditRole
        )

        assert (
            window.compView.model().data(window.compView.model().index(0, 0)) == "Test"
        )
        assert_comp_names_headers(window, 0, "Test")


class TestSpeciesChanges:
    def test_add_species_above_unselected(self, window: MainWindow, qtbot):
        window.speciesView.model().setData(
            window.speciesView.model().index(
                0, window.speciesView.model().columnCount() - 2
            ),
            1,
            Qt.ItemDataRole.EditRole,
        )

        qtbot.mouseClick(window.insert_above_species_button, Qt.MouseButton.LeftButton)

        assert window.numSpecies.value() == 2
        assert window.speciesView.model().rowCount() == 2

        assert window.speciesView.model().data(
            window.speciesView.model().index(
                1, window.speciesView.model().columnCount() - 2
            )
        ) == str(1)

    def test_add_species_below_unselected(self, window: MainWindow, qtbot: QtBot):
        window.speciesView.model().setData(
            window.speciesView.model().index(
                0, window.speciesView.model().columnCount() - 2
            ),
            1,
            Qt.ItemDataRole.EditRole,
        )
        qtbot.mouseClick(window.insert_below_species_button, Qt.MouseButton.LeftButton)

        assert window.numSpecies.value() == 2
        assert window.speciesView.model().rowCount() == 2

        assert window.speciesView.model().data(
            window.speciesView.model().index(
                1, window.speciesView.model().columnCount() - 2
            )
        ) == str(0)

    def test_add_species_above_selected(self, window: MainWindow, qtbot: QtBot):
        window.numSpecies.setValue(3)

        for i in range(window.speciesView.model().rowCount()):
            window.speciesView.model().setData(
                window.speciesView.model().index(
                    i, window.speciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window.speciesView, qtbot, (1, 1))
        qtbot.mouseClick(window.insert_above_species_button, Qt.MouseButton.LeftButton)

        assert window.numSpecies.value() == 4
        assert window.speciesView.model().rowCount() == 4

        column_data = []

        for i in range(window.speciesView.model().rowCount()):
            column_data.append(
                window.speciesView.model().data(
                    window.speciesView.model().index(
                        i, window.speciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "0", "2", "3"]

    def test_add_species_below_selected(self, window: MainWindow, qtbot: QtBot):
        window.numSpecies.setValue(3)

        for i in range(window.speciesView.model().rowCount()):
            window.speciesView.model().setData(
                window.speciesView.model().index(
                    i, window.speciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window.speciesView, qtbot, (1, 1))
        qtbot.mouseClick(window.insert_below_species_button, Qt.MouseButton.LeftButton)

        assert window.numSpecies.value() == 4
        assert window.speciesView.model().rowCount() == 4

        column_data = []

        for i in range(window.speciesView.model().rowCount()):
            column_data.append(
                window.speciesView.model().data(
                    window.speciesView.model().index(
                        i, window.speciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "2", "0", "3"]

    def test_increase_species_key(self, window: MainWindow, qtbot: QtBot):
        window.speciesView.model().setData(
            window.speciesView.model().index(
                0, window.speciesView.model().columnCount() - 2
            ),
            1,
            Qt.ItemDataRole.EditRole,
        )
        qtbot.keyClick(window.numSpecies, Qt.Key.Key_Up)

        assert window.numSpecies.value() == 2

        assert window.speciesView.model().rowCount() == 2

        assert window.speciesView.model().data(
            window.speciesView.model().index(
                0,
                window.speciesView.model().columnCount() - 2,
            )
        ) == str(1)

    def test_decrease_species_key(self, window: MainWindow, qtbot: QtBot):
        qtbot.keyClick(window.numSpecies, Qt.Key.Key_Down)
        assert window.numSpecies.value() == 1

        window.numSpecies.setValue(2)

        qtbot.keyClick(window.numSpecies, Qt.Key.Key_Down)
        assert window.numSpecies.value() == 1
        assert window.speciesView.model().rowCount() == 1

    def test_remove_species(
        self, window: MainWindow, qtbot: QtBot, monkeypatch: MonkeyPatch
    ):
        window.numSpecies.setValue(3)

        for i in range(window.speciesView.model().rowCount()):
            window.speciesView.model().setData(
                window.speciesView.model().index(
                    i, window.speciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window.speciesView, qtbot, (1, 1))
        monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)
        qtbot.mouseClick(window.remove_species_button, Qt.MouseButton.LeftButton)

        assert window.numSpecies.value() == 2
        assert window.speciesView.model().rowCount() == 2

        column_data = []

        for i in range(window.speciesView.model().rowCount()):
            column_data.append(
                window.speciesView.model().data(
                    window.speciesView.model().index(
                        i, window.speciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "3"]

    def test_abort_remove_species(
        self, window: MainWindow, qtbot: QtBot, monkeypatch: MonkeyPatch
    ):
        window.numSpecies.setValue(3)

        for i in range(window.speciesView.model().rowCount()):
            window.speciesView.model().setData(
                window.speciesView.model().index(
                    i, window.speciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window.speciesView, qtbot, (1, 1))
        monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.No)
        qtbot.mouseClick(window.remove_species_button, Qt.MouseButton.LeftButton)

        assert window.numSpecies.value() == 3
        assert window.speciesView.model().rowCount() == 3

        column_data = []

        for i in range(window.speciesView.model().rowCount()):
            column_data.append(
                window.speciesView.model().data(
                    window.speciesView.model().index(
                        i, window.speciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "2", "3"]

    def test_move_species_up(self, window: MainWindow, qtbot: QtBot):
        window.numSpecies.setValue(3)

        for i in range(window.speciesView.model().rowCount()):
            window.speciesView.model().setData(
                window.speciesView.model().index(
                    i, window.speciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window.speciesView, qtbot, (1, 1))
        qtbot.mouseClick(window.move_up_species_button, Qt.MouseButton.LeftButton)

        column_data = []
        for i in range(window.speciesView.model().rowCount()):
            column_data.append(
                window.speciesView.model().data(
                    window.speciesView.model().index(
                        i, window.speciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["2", "1", "3"]

    def test_move_species_up_first(self, window: MainWindow, qtbot: QtBot):
        window.numSpecies.setValue(3)

        for i in range(window.speciesView.model().rowCount()):
            window.speciesView.model().setData(
                window.speciesView.model().index(
                    i, window.speciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window.speciesView, qtbot, (0, 1))
        qtbot.mouseClick(window.move_up_species_button, Qt.MouseButton.LeftButton)

        column_data = []
        for i in range(window.speciesView.model().rowCount()):
            column_data.append(
                window.speciesView.model().data(
                    window.speciesView.model().index(
                        i, window.speciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "2", "3"]

    def test_move_species_down(self, window: MainWindow, qtbot: QtBot):
        window.numSpecies.setValue(3)

        for i in range(window.speciesView.model().rowCount()):
            window.speciesView.model().setData(
                window.speciesView.model().index(
                    i, window.speciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window.speciesView, qtbot, (1, 1))
        qtbot.mouseClick(window.move_down_species_button, Qt.MouseButton.LeftButton)

        column_data = []
        for i in range(window.speciesView.model().rowCount()):
            column_data.append(
                window.speciesView.model().data(
                    window.speciesView.model().index(
                        i, window.speciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "3", "2"]

    def test_move_species_down_last(self, window: MainWindow, qtbot: QtBot):
        window.numSpecies.setValue(3)

        for i in range(window.speciesView.model().rowCount()):
            window.speciesView.model().setData(
                window.speciesView.model().index(
                    i, window.speciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(
            window.speciesView, qtbot, (window.speciesView.model().rowCount() - 1, 1)
        )
        qtbot.mouseClick(window.move_down_species_button, Qt.MouseButton.LeftButton)

        column_data = []
        for i in range(window.speciesView.model().rowCount()):
            column_data.append(
                window.speciesView.model().data(
                    window.speciesView.model().index(
                        i, window.speciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "2", "3"]


class TestSolidChanges:
    def test_add_solid_above_unselected(self, window_solid: MainWindow, qtbot: QtBot):
        window_solid.solidSpeciesView.model().setData(
            window_solid.solidSpeciesView.model().index(
                0, window_solid.solidSpeciesView.model().columnCount() - 2
            ),
            1,
            Qt.ItemDataRole.EditRole,
        )

        qtbot.mouseClick(
            window_solid.insert_above_species_button, Qt.MouseButton.LeftButton
        )

        assert window_solid.numPhases.value() == 2
        assert window_solid.solidSpeciesView.model().rowCount() == 2

        assert window_solid.solidSpeciesView.model().data(
            window_solid.solidSpeciesView.model().index(
                1, window_solid.solidSpeciesView.model().columnCount() - 2
            )
        ) == str(1)

    def test_add_solid_below_unselected(self, window_solid: MainWindow, qtbot: QtBot):
        window_solid.solidSpeciesView.model().setData(
            window_solid.solidSpeciesView.model().index(
                0, window_solid.solidSpeciesView.model().columnCount() - 2
            ),
            1,
            Qt.ItemDataRole.EditRole,
        )
        qtbot.mouseClick(
            window_solid.insert_below_species_button, Qt.MouseButton.LeftButton
        )

        assert window_solid.numPhases.value() == 2
        assert window_solid.solidSpeciesView.model().rowCount() == 2

        assert window_solid.solidSpeciesView.model().data(
            window_solid.solidSpeciesView.model().index(
                1, window_solid.solidSpeciesView.model().columnCount() - 2
            )
        ) == str(0)

    def test_add_solid_above_selected(self, window_solid: MainWindow, qtbot: QtBot):
        window_solid.numPhases.setValue(3)

        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            window_solid.solidSpeciesView.model().setData(
                window_solid.solidSpeciesView.model().index(
                    i, window_solid.solidSpeciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window_solid.solidSpeciesView, qtbot, (1, 1))
        qtbot.mouseClick(
            window_solid.insert_above_species_button, Qt.MouseButton.LeftButton
        )

        assert window_solid.numPhases.value() == 4
        assert window_solid.solidSpeciesView.model().rowCount() == 4

        column_data = []

        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            column_data.append(
                window_solid.solidSpeciesView.model().data(
                    window_solid.solidSpeciesView.model().index(
                        i, window_solid.solidSpeciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "0", "2", "3"]

    def test_add_solid_below_selected(self, window_solid: MainWindow, qtbot: QtBot):
        window_solid.numPhases.setValue(3)

        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            window_solid.solidSpeciesView.model().setData(
                window_solid.solidSpeciesView.model().index(
                    i, window_solid.solidSpeciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window_solid.solidSpeciesView, qtbot, (1, 1))
        qtbot.mouseClick(
            window_solid.insert_below_species_button, Qt.MouseButton.LeftButton
        )

        assert window_solid.numPhases.value() == 4
        assert window_solid.solidSpeciesView.model().rowCount() == 4

        column_data = []

        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            column_data.append(
                window_solid.solidSpeciesView.model().data(
                    window_solid.solidSpeciesView.model().index(
                        i, window_solid.solidSpeciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "2", "0", "3"]

    def test_increase_solid_key(self, window_solid: MainWindow, qtbot: QtBot):
        window_solid.solidSpeciesView.model().setData(
            window_solid.solidSpeciesView.model().index(
                0, window_solid.solidSpeciesView.model().columnCount() - 2
            ),
            1,
            Qt.ItemDataRole.EditRole,
        )
        qtbot.keyClick(window_solid.numPhases, Qt.Key.Key_Up)

        assert window_solid.numPhases.value() == 2

        assert window_solid.solidSpeciesView.model().rowCount() == 2

        assert window_solid.solidSpeciesView.model().data(
            window_solid.solidSpeciesView.model().index(
                0,
                window_solid.solidSpeciesView.model().columnCount() - 2,
            )
        ) == str(1)

    def test_decrease_solid_key(self, window_solid: MainWindow, qtbot: QtBot):
        qtbot.keyClick(window_solid.numPhases, Qt.Key.Key_Down)
        assert window_solid.numPhases.value() == 0

        window_solid.numPhases.setValue(2)

        qtbot.keyClick(window_solid.numPhases, Qt.Key.Key_Down)
        assert window_solid.numPhases.value() == 1
        assert window_solid.solidSpeciesView.model().rowCount() == 1

    def test_remove_species(
        self, window_solid: MainWindow, qtbot: QtBot, monkeypatch: MonkeyPatch
    ):
        window_solid.numPhases.setValue(3)

        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            window_solid.solidSpeciesView.model().setData(
                window_solid.solidSpeciesView.model().index(
                    i, window_solid.solidSpeciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window_solid.solidSpeciesView, qtbot, (1, 1))
        monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.Yes)
        qtbot.mouseClick(window_solid.remove_species_button, Qt.MouseButton.LeftButton)

        assert window_solid.numPhases.value() == 2
        assert window_solid.solidSpeciesView.model().rowCount() == 2

        column_data = []

        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            column_data.append(
                window_solid.solidSpeciesView.model().data(
                    window_solid.solidSpeciesView.model().index(
                        i, window_solid.solidSpeciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "3"]

    def test_abort_remove_species(
        self, window_solid: MainWindow, qtbot: QtBot, monkeypatch: MonkeyPatch
    ):
        window_solid.numPhases.setValue(3)

        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            window_solid.solidSpeciesView.model().setData(
                window_solid.solidSpeciesView.model().index(
                    i, window_solid.solidSpeciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window_solid.solidSpeciesView, qtbot, (1, 1))
        monkeypatch.setattr(QMessageBox, "question", lambda *args: QMessageBox.No)
        qtbot.mouseClick(window_solid.remove_species_button, Qt.MouseButton.LeftButton)

        assert window_solid.numPhases.value() == 3
        assert window_solid.solidSpeciesView.model().rowCount() == 3

        column_data = []

        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            column_data.append(
                window_solid.solidSpeciesView.model().data(
                    window_solid.solidSpeciesView.model().index(
                        i, window_solid.solidSpeciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "2", "3"]

    def test_move_solid_up(self, window_solid: MainWindow, qtbot: QtBot):
        window_solid.numPhases.setValue(3)

        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            window_solid.solidSpeciesView.model().setData(
                window_solid.solidSpeciesView.model().index(
                    i, window_solid.solidSpeciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window_solid.solidSpeciesView, qtbot, (1, 1))
        qtbot.mouseClick(window_solid.move_up_species_button, Qt.MouseButton.LeftButton)

        column_data = []
        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            column_data.append(
                window_solid.solidSpeciesView.model().data(
                    window_solid.solidSpeciesView.model().index(
                        i, window_solid.solidSpeciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["2", "1", "3"]

    def test_move_solid_up_first(self, window_solid: MainWindow, qtbot: QtBot):
        window_solid.numPhases.setValue(3)

        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            window_solid.solidSpeciesView.model().setData(
                window_solid.solidSpeciesView.model().index(
                    i, window_solid.solidSpeciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window_solid.solidSpeciesView, qtbot, (0, 1))
        qtbot.mouseClick(window_solid.move_up_species_button, Qt.MouseButton.LeftButton)

        column_data = []
        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            column_data.append(
                window_solid.solidSpeciesView.model().data(
                    window_solid.solidSpeciesView.model().index(
                        i, window_solid.solidSpeciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "2", "3"]

    def test_move_solid_down(self, window_solid: MainWindow, qtbot: QtBot):
        window_solid.numPhases.setValue(3)

        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            window_solid.solidSpeciesView.model().setData(
                window_solid.solidSpeciesView.model().index(
                    i, window_solid.solidSpeciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(window_solid.solidSpeciesView, qtbot, (1, 1))
        qtbot.mouseClick(
            window_solid.move_down_species_button, Qt.MouseButton.LeftButton
        )

        column_data = []
        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            column_data.append(
                window_solid.solidSpeciesView.model().data(
                    window_solid.solidSpeciesView.model().index(
                        i, window_solid.solidSpeciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "3", "2"]

    def test_move_solid_down_last(self, window_solid: MainWindow, qtbot: QtBot):
        window_solid.numPhases.setValue(3)

        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            window_solid.solidSpeciesView.model().setData(
                window_solid.solidSpeciesView.model().index(
                    i, window_solid.solidSpeciesView.model().columnCount() - 2
                ),
                i + 1,
                Qt.ItemDataRole.EditRole,
            )

        select_cell(
            window_solid.solidSpeciesView,
            qtbot,
            (window_solid.solidSpeciesView.model().rowCount() - 1, 1),
        )
        qtbot.mouseClick(
            window_solid.move_down_species_button, Qt.MouseButton.LeftButton
        )

        column_data = []
        for i in range(window_solid.solidSpeciesView.model().rowCount()):
            column_data.append(
                window_solid.solidSpeciesView.model().data(
                    window_solid.solidSpeciesView.model().index(
                        i, window_solid.solidSpeciesView.model().columnCount() - 2
                    )
                )
            )

        assert column_data == ["1", "2", "3"]

