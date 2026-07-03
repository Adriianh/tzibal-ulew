"""
Main application window with sidebar navigation.
"""

from __future__ import annotations

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


class MainWindow(QMainWindow):
    """Main application window with sidebar navigation and content area."""

    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Tz'ib'al Ulew — Registro de Expediciones")
        self.resize(1100, 700)

        self._setup_ui()

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

        for title in ["Dashboard", "Salidas", "Especies"]:
            page = QWidget()
            page_layout = QVBoxLayout(page)
            label = QLabel(f"{title} — en construcción")
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            page_layout.addWidget(label)
            self.pages.addWidget(page)

        # ── Navigation connection ──────────────────────────────
        self.nav.currentRowChanged.connect(self.pages.setCurrentIndex)

        # ── Assembling ─────────────────────────────────────────
        layout.addWidget(sidebar)
        layout.addWidget(self.pages, 1)
