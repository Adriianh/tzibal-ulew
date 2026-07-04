"""
Tests for TripFormDialog.
"""
from __future__ import annotations

from PyQt6.QtWidgets import QDateEdit, QDoubleSpinBox, QLineEdit, QTextEdit
from pytestqt.qtbot import QtBot

from ui.api_client import ApiClient
from ui.views.trip_form import TripFormDialog


def test_dialog_title(qtbot: QtBot) -> None:
    """Dialog window title should be 'Nueva Salida'."""
    client = ApiClient("http://localhost:9999")  # API inexistente
    dialog = TripFormDialog(client)
    qtbot.add_widget(dialog)

    assert dialog.windowTitle() == "Nueva Salida"


def test_form_has_all_fields(qtbot: QtBot) -> None:
    """All expected form fields should be present."""
    client = ApiClient("http://localhost:9999")
    dialog = TripFormDialog(client)
    qtbot.add_widget(dialog)

    assert dialog.name_edit is not None
    assert isinstance(dialog.name_edit, QLineEdit)

    assert dialog.date_edit is not None
    assert isinstance(dialog.date_edit, QDateEdit)

    assert dialog.place_edit is not None
    assert isinstance(dialog.place_edit, QLineEdit)

    assert dialog.latitude_edit is not None
    assert isinstance(dialog.latitude_edit, QDoubleSpinBox)

    assert dialog.longitude_edit is not None
    assert isinstance(dialog.longitude_edit, QDoubleSpinBox)

    assert dialog.notes_edit is not None
    assert isinstance(dialog.notes_edit, QTextEdit)
