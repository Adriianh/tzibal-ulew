"""
Pydantic schemas for map-related endpoints.
"""

from datetime import date

from pydantic import BaseModel


class MapSpeciesInfo(BaseModel):
    """Lightweight species info for map points."""

    id: int
    common_name: str
    scientific_name: str


class MapPointResponse(BaseModel):
    """A trip point on the map with summary of species found."""

    id: int
    name: str
    trip_date: date
    latitude: float
    longitude: float
    species: list[MapSpeciesInfo]
    species_count: int
