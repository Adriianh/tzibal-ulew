"""
Trip creation/editing dialog.
"""

from __future__ import annotations

from PyQt6.QtCore import QDate
from PyQt6.QtWidgets import (
    QDateEdit,
    QDialog,
    QDialogButtonBox,
    QDoubleSpinBox,
    QFormLayout,
    QLineEdit,
    QTextEdit,
    QVBoxLayout,
)

from ui.api_client import ApiClient


class TripFormDialog(QDialog):
    """Dialog for creating a new trip."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__()
        self.api_client = api_client
        self.setWindowTitle("Nueva Salida")
        self.setMinimumWidth(400)
        self._setup_ui()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        form = QFormLayout()

        self.name_edit = QLineEdit()
        form.addRow("Nombre:", self.name_edit)

        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)

        self.date_edit.setDate(QDate.currentDate())
        form.addRow("Fecha:", self.date_edit)

        self.place_edit = QLineEdit()
        form.addRow("Lugar:", self.place_edit)

        self.latitude_edit = QDoubleSpinBox()
        self.latitude_edit.setRange(-90.0, 90.0)
        self.latitude_edit.setDecimals(6)
        form.addRow("Latitud:", self.latitude_edit)

        self.longitude_edit = QDoubleSpinBox()
        self.longitude_edit.setRange(-180.0, 180.0)
        self.longitude_edit.setDecimals(6)
        form.addRow("Longitud:", self.longitude_edit)

        self.notes_edit = QTextEdit()
        form.addRow("Notas:", self.notes_edit)

        layout.addLayout(form)

        buttons = QDialogButtonBox(
            QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        )
        buttons.accepted.connect(self._save)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def _save(self) -> None:
        """Build the trip data dict and call the API."""

        trip_data = {
            "name": self.name_edit.text(),
            "trip_date": self.date_edit.date().toString("yyyy-MM-dd"),
            "place": self.place_edit.text(),
            "latitude": self.latitude_edit.value(),
            "longitude": self.longitude_edit.value(),
            "notes": self.notes_edit.toPlainText(),
        }

        try:
            self.api_client.trips.create_trip(trip_data)
            self.accept()
        except Exception as e:
            print(f"Error creating trip: {e}")
