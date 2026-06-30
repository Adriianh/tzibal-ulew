"""
ORM model for species catalog.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Text

if TYPE_CHECKING:
    from api.models.record import Record
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base


class Species(Base):
    __tablename__ = "species"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    common_name: Mapped[str] = mapped_column(String(255), nullable=False)
    scientific_name: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(20), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    records: Mapped[list[Record]] = relationship("Record", back_populates="species")

    def __repr__(self) -> str:
        return f"<Species {self.id}: {self.common_name} ({self.scientific_name})>"
