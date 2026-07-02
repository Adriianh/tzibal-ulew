"""
Pydantic schemas for sighting records.
"""

from datetime import datetime

from pydantic import BaseModel, Field


class RecordBase(BaseModel):
    species_id: int
    count: int | None = Field(None, ge=1)
    notes: str | None = None


class RecordCreate(RecordBase):
    trip_id: int


class RecordResponse(RecordBase):
    id: int
    trip_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class RecordUpdate(BaseModel):
    count: int | None = Field(None, ge=1)
    notes: str | None = None
