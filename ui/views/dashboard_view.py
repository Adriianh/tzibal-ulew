"""
Dashboard view — shows summary statistics.
"""

from __future__ import annotations

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout, QWidget

from ui.api_client import ApiClient


class DashboardView(QWidget):
    """Initial summary with statistics from the API."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__()
        self.api_client = api_client
        self._setup_ui()
        self._load_data()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        title = QLabel("Dashboard")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        cards_layout = QHBoxLayout()
        trips_card, self.trips_value = self._create_card("Total Trips", "0")
        species_card, self.species_value = self._create_card("Total Species", "0")
        records_card, self.records_value = self._create_card("Total Records", "0")

        cards_layout.addWidget(trips_card)
        cards_layout.addWidget(species_card)
        cards_layout.addWidget(records_card)

        layout.addLayout(cards_layout)

    def _create_card(self, title: str, value: str) -> tuple[QFrame, QLabel]:
        """Create a card widget with a title and value."""
        card = QFrame()
        card.setObjectName("card")
        card.setFrameShape(QFrame.Shape.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                border: 1px solid #ccc;
                border-radius: 8px;
                padding: 16px;
                background-color: #f9f9f9;
                min-width: 120px;
            }
        """)

        card_layout = QVBoxLayout(card)

        value_label = QLabel(value)
        value_label.setStyleSheet("font-size: 32px; font-weight: bold;")
        value_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel(title)
        title_label.setStyleSheet("font-size: 14px; color: #555;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout.addWidget(value_label)
        card_layout.addWidget(title_label)

        return card, value_label

    def _load_data(self) -> None:
        """Fetch stats from the API and update the UI."""
        try:
            summary = self.api_client.stats.get_summary()

            self.trips_value.setText(str(summary["total_trips"]))
            self.species_value.setText(str(summary["total_species"]))
            self.records_value.setText(str(summary["total_records"]))
        except Exception as e:
            print(f"Error fetching summary data: {e}")
            return
