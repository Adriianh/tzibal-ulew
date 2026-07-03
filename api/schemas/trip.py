"""
Pydantic schemas for Trip (field expeditions)
"""

from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class TripBase(BaseModel):
    """Common fields for creating and listing trips."""

    name: str = Field(
        ..., max_length=200, examples=["Volcán Tajumulco"], description="Name of the trip"
    )
    trip_date: date
    place: str = Field(
        ..., max_length=200, examples=["San Marcos, Guatemala"], description="Place of the trip"
    )
    latitude: float = Field(
        ..., ge=-90, le=90, examples=[15.0], description="Latitude of the trip location"
    )
    longitude: float = Field(
        ..., ge=-180, le=180, examples=[-91.0], description="Longitude of the trip location"
    )
    altitude_m: float | None = None
    weather: str | None = Field(
        None, max_length=50, examples=["Sunny"], description="Weather during the trip"
    )
    temperature_c: float | None = Field(
        None, examples=[25.0], description="Temperature in Celsius during the trip"
    )
    notes: str | None = None


class TripCreate(TripBase):
    """Request body for /trips POST endpoint."""

    pass


class TripResponse(TripBase):
    """Response model for /trips GET endpoint."""

    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
