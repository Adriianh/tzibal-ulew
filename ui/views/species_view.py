"""
Species catalog view.
"""

from __future__ import annotations

from typing import Any

from PyQt6.QtWidgets import (
    QComboBox,
    QHBoxLayout,
    QLabel,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)

from ui.api_client import ApiClient


class SpeciesView(QWidget):
    """Catalog of all species with filtering."""

    def __init__(self, api_client: ApiClient) -> None:
        super().__init__()
        self.api_client = api_client
        self._setup_ui()
        self._load_species()

    def _setup_ui(self) -> None:
        layout = QVBoxLayout(self)

        # Title
        title = QLabel("Catálogo de Especies")
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(title)

        # Filter row
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filtrar por tipo:"))
        self.filter_combo = QComboBox()
        self.filter_combo.addItems(
            ["Todos", "Bird", "Mammal", "Reptile", "Amphibian", "Insect", "Plant", "Fungi", "Other"]
        )
        filter_layout.addWidget(self.filter_combo)
        filter_layout.addStretch()
        layout.addLayout(filter_layout)

        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Nombre común", "Nombre científico", "Tipo"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        header = self.table.horizontalHeader()
        assert header is not None
        header.setStretchLastSection(True)

        self.filter_combo.currentTextChanged.connect(self._load_species)

        layout.addWidget(self.table)

    def _load_species(self) -> None:
        """Fetch species from API and populate the table."""
        try:
            species_filter = self.filter_combo.currentText()

            species_list = self.api_client.species.list_species(
                species_filter if species_filter != "Todos" else None
            )
            self._populate_table(species_list)
        except Exception as e:
            print(f"Error loading species: {e}")

    def _populate_table(self, species_list: list[dict[str, Any]]) -> None:
        """Fill the table with species data."""
        self.table.setRowCount(0)
        self.table.setRowCount(len(species_list))

        for row, species in enumerate(species_list):
            self.table.setItem(row, 0, QTableWidgetItem(species["common_name"]))
            self.table.setItem(row, 1, QTableWidgetItem(species["scientific_name"]))
            self.table.setItem(row, 2, QTableWidgetItem(species["type"]))
