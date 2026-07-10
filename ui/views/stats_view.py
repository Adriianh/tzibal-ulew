"""
Statistics view with matplotlib charts.
"""

from __future__ import annotations

from typing import Any

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PyQt6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.api_client import ApiClient


class StatsView(QWidget):
    """Dashboard with matplotlib charts (trips by month, top species, etc.)."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__()
        self.api_client = api_client
        self._setup_ui()
        self._load_charts()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        title = QLabel("Estadísticas")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        self.figure = Figure(figsize=(8, 8))
        self.canvas = FigureCanvasQTAgg(self.figure)  # type: ignore[no-untyped-call]
        layout.addWidget(self.canvas)

    def _load_charts(self) -> None:
        try:
            by_month = self.api_client.stats.get_by_month()
            top_species = self.api_client.stats.get_top_species()
            self._plot_by_month(by_month)
            self._plot_top_species(top_species)
        except Exception as e:
            print(f"Error loading stats: {e}")

    def _plot_by_month(self, data: list[dict[str, Any]]) -> None:
        ax = self.figure.add_subplot(211)
        # data: [{"year": 2026, "month": 1, "count": 3}, ...]
        labels = [f"{d['year']}-{d['month']:02d}" for d in data]
        counts = [d["count"] for d in data]
        ax.bar(labels, counts, color="#27ae60")
        ax.set_title("Salidas por Mes")
        ax.tick_params(axis="x", rotation=45)

    def _plot_top_species(self, data: list[dict[str, Any]]) -> None:
        ax = self.figure.add_subplot(212)
        names = [d["common_name"] for d in data]
        counts = [d["count"] for d in data]
        ax.barh(names[::-1], counts[::-1], color="#2c3e50")
        ax.set_title("Top 10 Especies")
