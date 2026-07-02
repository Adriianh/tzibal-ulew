"""
Shared dependencies for FastAPI routes.
"""

from collections.abc import Generator

from sqlalchemy.orm import Session

from api.database import SessionLocal


def get_db() -> Generator[Session, None, None]:
    """
    Provides a DB session for request.
    It closes the session after the request is done.

    Usage:
        dep=Depends(get_db) in route function parameters.
    """

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
