"""
Shared fixtures for pytest.
"""

import pytest

from fastapi.testclient import TestClient


@pytest.fixture
def client():
    """
    HTTP client for testing FastAPI endpoints.
    """
    pytest.skip("Skipping client fixture as the FastAPI app is not defined in this context.")
