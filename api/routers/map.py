"""
Endpoint for map visualization points.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session, selectinload

from api.dependencies import get_db
from api.models.record import Record
from api.models.trip import Trip
from api.schemas.map import MapPointResponse, MapSpeciesInfo

router = APIRouter(prefix="/map", tags=["Map"])


@router.get("/points", response_model=list[MapPointResponse])
def get_map_points(db: Session = Depends(get_db)) -> list[MapPointResponse]:
    """Returns all trips with their species for map visualization."""
    trips = (
        db.query(Trip)
        .options(selectinload(Trip.records).joinedload(Record.species))
        .order_by(Trip.trip_date.desc())
        .all()
    )

    return [
        MapPointResponse(
            id=t.id,
            name=t.name,
            trip_date=t.trip_date,
            latitude=t.latitude,
            longitude=t.longitude,
            species=[
                MapSpeciesInfo(
                    id=r.species.id,
                    common_name=r.species.common_name,
                    scientific_name=r.species.scientific_name,
                )
                for r in t.records
            ],
            species_count=len(t.records),
        )
        for t in trips
    ]
