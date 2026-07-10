"""
Tests for the main application window.
"""

from __future__ import annotations

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

    item0 = window.nav.item(0)
    item1 = window.nav.item(1)
    item2 = window.nav.item(2)
    item3 = window.nav.item(3)
    item4 = window.nav.item(4)

    assert window.nav.count() == 5

    assert item0 is not None
    assert item0.text() == "Dashboard"

    assert item1 is not None
    assert item1.text() == "Salidas"

    assert item2 is not None
    assert item2.text() == "Especies"

    assert item3 is not None
    assert item3.text() == "Mapa"

    assert item4 is not None
    assert item4.text() == "Estadísticas"


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
