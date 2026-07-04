from PyQt6.QtWidgets import QLabel
from pytestqt.qtbot import QtBot

from ui.api_client import ApiClient
from ui.views.dashboard_view import DashboardView


def test_dashboard_has_three_cards(qtbot: QtBot) -> None:
    client = ApiClient("http://localhost:9999")
    view = DashboardView(client)
    qtbot.add_widget(view)

    assert view.trips_value is not None
    assert isinstance(view.trips_value, QLabel)

    assert view.species_value is not None
    assert isinstance(view.species_value, QLabel)

    assert view.records_value is not None
    assert isinstance(view.records_value, QLabel)
