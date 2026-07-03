"""
Tests for the main application window.
"""

from __future__ import annotations

from PyQt6.QtWidgets import QLabel
from pytestqt.qtbot import QtBot

from ui.app import MainWindow


def test_window_title(qtbot: QtBot) -> None:
    """Window title should describe the application."""
    window = MainWindow()
    qtbot.add_widget(window)

    assert "Tz'ib'al Ulew" in window.windowTitle()
    assert "Expediciones" in window.windowTitle()


def test_sidebar_has_three_items(qtbot: QtBot) -> None:
    """Navigation sidebar should contain Dashboard, Salidas, Especies."""
    window = MainWindow()
    qtbot.add_widget(window)

    assert window.nav.count() == 3
    assert window.nav.item(0).text() == "Dashboard"
    assert window.nav.item(1).text() == "Salidas"
    assert window.nav.item(2).text() == "Especies"


def test_navigation_switches_pages(qtbot: QtBot) -> None:
    """Clicking each nav item should show the corresponding page."""
    window = MainWindow()
    qtbot.add_widget(window)

    # Start at Dashboard (index 0)
    assert window.pages.currentIndex() == 0

    # Click Salidas (index 1)
    window.nav.setCurrentRow(1)
    assert window.pages.currentIndex() == 1

    # Click Especies (index 2)
    window.nav.setCurrentRow(2)
    assert window.pages.currentIndex() == 2

    # Click back to Dashboard (index 0)
    window.nav.setCurrentRow(0)
    assert window.pages.currentIndex() == 0


def test_initial_selection_is_dashboard(qtbot: QtBot) -> None:
    """First page visible on launch should be Dashboard."""
    window = MainWindow()
    qtbot.add_widget(window)

    assert window.pages.currentIndex() == 0
    page = window.pages.currentWidget()
    assert page is not None
    label = page.findChild(QLabel)
    assert label is not None
    assert "Dashboard" in label.text()
