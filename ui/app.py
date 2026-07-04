"""
Main application window with sidebar navigation.
"""

from __future__ import annotations

from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QStackedWidget,
    QVBoxLayout,
    QWidget,
)

from ui.api_client import ApiClient
from ui.views.dashboard_view import DashboardView
from ui.views.species_view import SpeciesView
from ui.views.trips_view import TripsView


class MainWindow(QMainWindow):
    """Main application window with sidebar navigation and content area."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Tz'ib'al Ulew — Registro de Expediciones")
        self.resize(1100, 700)

        self.api_client = ApiClient("http://127.0.0.1:8000")

        self._setup_ui()
        self._load_styles()

    def _setup_ui(self) -> None:
        central = QWidget()
        self.setCentralWidget(central)
        layout = QHBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # ── Sidebar ────────────────────────────────────────────
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(200)

        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)

        logo = QLabel("Tz'ib'al Ulew")
        logo.setObjectName("logo")
        logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        logo.setFixedHeight(60)

        self.nav = QListWidget()
        self.nav.setObjectName("nav")
        self.nav.addItems(["Dashboard", "Salidas", "Especies"])
        self.nav.setCurrentRow(0)

        sidebar_layout.addWidget(logo)
        sidebar_layout.addWidget(self.nav)
        sidebar_layout.addStretch()

        # ── Content area ───────────────────────────────────────
        self.pages = QStackedWidget()
        self.pages.setObjectName("pages")

        dashboard = DashboardView(self.api_client)
        self.pages.addWidget(dashboard)

        trips_page = TripsView(self.api_client)
        self.pages.addWidget(trips_page)

        species_page = SpeciesView(self.api_client)
        self.pages.addWidget(species_page)

        # ── Navigation connection ──────────────────────────────
        self.nav.currentRowChanged.connect(self.pages.setCurrentIndex)

        # ── Assembling ─────────────────────────────────────────
        layout.addWidget(sidebar)
        layout.addWidget(self.pages, 1)

    def _load_styles(self) -> None:
        """Load the stylesheet from a file."""

        qss_path = Path(__file__).resolve().parent.parent / "assets" / "styles.qss"
        if qss_path.exists():
            with open(qss_path) as f:
                self.setStyleSheet(f.read())
