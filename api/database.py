"""
SQLAlchemy database connection and session management.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from config import DB_URL

engine = create_engine(DB_URL, connect_args={"check_same_thread": False}, echo=False)

SessionLocal = sessionmaker(bind=engine, autoflush=False)


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models."""

    pass
