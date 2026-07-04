"""
Trips view - shows a list of trips
"""

from __future__ import annotations

from PyQt6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ui.api_client import ApiClient
from ui.views.trip_form import TripFormDialog


class TripsView(QWidget):
    """View for displaying a list of trips."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__()
        self.api_client = api_client
        self._setup_ui()
        self._load_trips()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        title = QLabel("Salidas")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")

        header_layout = QHBoxLayout()
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.new_trip_btn = QPushButton("Nueva Salida")
        self.new_trip_btn.clicked.connect(self._open_form)
        header_layout.addWidget(self.new_trip_btn)

        layout.addLayout(header_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["Nombre", "Fecha", "Lugar", "Latitud", "Longitud"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        table_header = self.table.horizontalHeader()
        assert table_header is not None
        table_header.setStretchLastSection(True)

        layout.addWidget(self.table)

    def _load_trips(self) -> None:
        """Load trips from the API and populate the table."""
        try:
            trips = self.api_client.trips.list_trips()
            self.table.setRowCount(len(trips))

            for row, trip in enumerate(trips):
                self.table.setItem(row, 0, QTableWidgetItem(trip["name"]))
                self.table.setItem(row, 1, QTableWidgetItem(trip["trip_date"]))
                self.table.setItem(row, 2, QTableWidgetItem(trip["place"]))
                self.table.setItem(row, 3, QTableWidgetItem(str(trip["latitude"])))
                self.table.setItem(row, 4, QTableWidgetItem(str(trip["longitude"])))
        except Exception as e:
            print(f"Error loading trips: {e}")

    def _open_form(self) -> None:
        """Open the trip form dialog to create a new trip."""

        form_dialog = TripFormDialog(self.api_client)
        if form_dialog.exec():
            self._load_trips()
