"""
Shared fixtures for pytest.
"""

from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient


@pytest.fixture
def client() -> Generator[TestClient, None, None]:
    """
    HTTP client for testing FastAPI endpoints.
    """
    try:
        from api.main import app  # type: ignore[import-not-found]
    except ImportError:
        pytest.skip("api.main not available yet — build the API first")

    with TestClient(app) as _client:
        yield _client
