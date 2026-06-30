"""
ORM model for sighting records.
"""

from __future__ import annotations

from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from api.database import Base

if TYPE_CHECKING:
    from api.models.species import Species
    from api.models.trip import Trip


class Record(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    trip_id: Mapped[int] = mapped_column(ForeignKey("trips.id"), nullable=False)
    species_id: Mapped[int] = mapped_column(ForeignKey("species.id"), nullable=False)
    count: Mapped[int | None] = mapped_column(Integer, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    image_url: Mapped[str | None] = mapped_column(String(255), nullable=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.now)

    trip: Mapped[Trip] = relationship("Trip", back_populates="records")
    species: Mapped[Species] = relationship("Species", back_populates="records")

    def __repr__(self) -> str:
        return f"<Record {self.id}: sp={self.species_id} trip={self.trip_id}>"
