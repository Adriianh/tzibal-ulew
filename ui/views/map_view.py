"""
Map view — shows the interactive Folium map.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.api_client import ApiClient
from ui.widgets.map_widget import MapWidget


class MapView(QWidget):
    """View that wraps the MapWidget with a title."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__()
        self.api_client = api_client
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        title = QLabel("Mapa de Expediciones")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)
        self.map_widget = MapWidget(self.api_client)
        layout.addWidget(self.map_widget)
