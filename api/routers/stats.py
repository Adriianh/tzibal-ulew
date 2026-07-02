"""
Endpoints for statistics and aggregations.
"""

from fastapi import APIRouter, Depends
from sqlalchemy import func
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.models.record import Record
from api.models.species import Species
from api.models.trip import Trip
from api.schemas.stats import (
    MonthSummary,
    StatsSummaryResponse,
    TopSpeciesItem,
)

router = APIRouter(prefix="/stats", tags=["Stats"])


@router.get("/summary", response_model=StatsSummaryResponse)
def get_stats_summary(db: Session = Depends(get_db)) -> StatsSummaryResponse:
    """Returns total counts of trips, species, and records."""
    total_trips = db.query(func.count(Trip.id)).scalar() or 0
    total_species = db.query(func.count(Species.id)).scalar() or 0
    total_records = db.query(func.count(Record.id)).scalar() or 0

    return StatsSummaryResponse(
        total_trips=total_trips,
        total_species=total_species,
        total_records=total_records,
    )


@router.get("/top-species", response_model=list[TopSpeciesItem])
def get_top_species(db: Session = Depends(get_db)) -> list[TopSpeciesItem]:
    """Returns top 10 most recorded species."""
    results = (
        db.query(
            Species.id,
            Species.common_name,
            Species.scientific_name,
            func.count(Record.id).label("record_count"),
        )
        .outerjoin(Record, Species.id == Record.species_id)
        .group_by(Species.id)
        .order_by(func.count(Record.id).desc())
        .limit(10)
        .all()
    )

    return [
        TopSpeciesItem(
            species_id=row.id,
            common_name=row.common_name,
            scientific_name=row.scientific_name,
            record_count=row.record_count,
        )
        for row in results
    ]


@router.get("/by-month", response_model=list[MonthSummary])
def get_trips_by_month(db: Session = Depends(get_db)) -> list[MonthSummary]:
    """Returns trip counts grouped by year and month."""
    results = (
        db.query(
            func.strftime("%Y", Trip.trip_date).label("year"),
            func.strftime("%m", Trip.trip_date).label("month"),
            func.count(Trip.id).label("trip_count"),
        )
        .group_by("year", "month")
        .order_by(
            func.strftime("%Y", Trip.trip_date).desc(), func.strftime("%m", Trip.trip_date).desc()
        )
        .all()
    )

    return [
        MonthSummary(
            year=int(row.year),
            month=int(row.month),
            trip_count=row.trip_count,
        )
        for row in results
    ]
