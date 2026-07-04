"""
Tests for TripsView.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QPushButton, QTableWidget
from pytestqt.qtbot import QtBot

from ui.api_client import ApiClient
from ui.views.trips_view import TripsView


def test_trips_has_table_and_button(qtbot: QtBot) -> None:
    client = ApiClient("http://localhost:9999")
    view = TripsView(client)
    qtbot.add_widget(view)

    assert view.table is not None
    assert isinstance(view.table, QTableWidget)
    assert view.table.columnCount() == 5

    assert view.new_trip_btn is not None
    assert isinstance(view.new_trip_btn, QPushButton)
    assert "Nueva" in view.new_trip_btn.text()
