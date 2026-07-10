"""
Map widget — embeds a Folium-generated Leaflet map.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWidgets import QVBoxLayout, QWidget

from ui.api_client import ApiClient


class MapWidget(QWidget):
    """Widget that displays an interactive Folium map."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__()
        self.api_client = api_client
        self._setup_ui()
        self.refresh()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)

    def refresh(self) -> None:
        """Fetch map data and regenerate the Folium HTML."""
        points = self.api_client.map.get_map_points()
        html = self._generate_map(points)
        self.web_view.setHtml(html)

    def _generate_map(self, points: list[dict[str, Any]]) -> str:
        """Build a Folium map HTML from API data."""
        import folium

        m = folium.Map(location=[15.5, -90.5], zoom_start=7)

        for trip in points:
            popup_text = f"""
                <b>{trip["name"]}</b><br>
                {trip["trip_date"]}<br>
                Especies: {trip["species_count"]}
            """
            folium.Marker(
                location=[trip["latitude"], trip["longitude"]],
                popup=folium.Popup(popup_text, max_width=300),
                icon=folium.Icon(color="green", icon="tree", prefix="fa"),
            ).add_to(m)

        return m._repr_html_()
