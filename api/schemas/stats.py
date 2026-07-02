"""
Pydantic schemas for statistics endpoints.
"""

from pydantic import BaseModel


class StatsSummaryResponse(BaseModel):
    """General statistics summary."""

    total_trips: int
    total_species: int
    total_records: int


class TopSpeciesItem(BaseModel):
    """A species ranked by record count."""

    species_id: int
    common_name: str
    scientific_name: str
    record_count: int


class MonthSummary(BaseModel):
    """Trip count grouped by year and month."""

    year: int
    month: int
    trip_count: int
