"""
Shared fixtures for pytest.
"""

from collections.abc import Generator
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import NullPool

from api.database import Base
from api.dependencies import get_db


@pytest.fixture
def engine(tmp_path: Path) -> Generator[Engine, None, None]:
    """Creates a fresh SQLite database file per test with tables created."""
    db_path = tmp_path / "test.db"
    _engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
        poolclass=NullPool,
        echo=False,
    )
    # Import models so they register on Base.metadata before create_all
    import api.models  # noqa: F401

    Base.metadata.create_all(bind=_engine)
    yield _engine


@pytest.fixture
def client(engine: Engine) -> Generator[TestClient, None, None]:
    """HTTP client with test database isolation."""
    from api.main import app

    testing_session_local = sessionmaker(bind=engine, autoflush=False)

    def override_get_db() -> Generator[Session, None, None]:
        db = testing_session_local()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    with TestClient(app) as _client:
        yield _client

    app.dependency_overrides.clear()
