"""
Tests for SpeciesView.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QComboBox, QTableWidget
from pytestqt.qtbot import QtBot

from ui.api_client import ApiClient
from ui.views.species_view import SpeciesView


def test_species_has_table_and_filter(qtbot: QtBot) -> None:
    client = ApiClient("http://localhost:9999")
    view = SpeciesView(client)
    qtbot.add_widget(view)

    assert view.table is not None
    assert isinstance(view.table, QTableWidget)
    assert view.table.columnCount() == 3

    assert view.filter_combo is not None
    assert isinstance(view.filter_combo, QComboBox)
    assert view.filter_combo.count() > 1
