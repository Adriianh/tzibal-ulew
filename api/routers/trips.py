"""
Endpoints CRUD for trips (field expeditions).
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session, joinedload

from api.dependencies import get_db
from api.models.record import Record
from api.models.trip import Trip
from api.schemas.record import RecordWithSpeciesResponse
from api.schemas.trip import TripCreate, TripResponse

router = APIRouter(prefix="/trips", tags=["Trips"])


@router.get("", response_model=list[TripResponse])
def list_trips(db: Session = Depends(get_db)) -> list[Trip]:
    """Lists all field trips ordered by date descending."""
    trips = db.query(Trip).order_by(Trip.trip_date.desc()).all()
    return trips


@router.get("/{trip_id}", response_model=TripResponse)
def get_trip(trip_id: int, db: Session = Depends(get_db)) -> Trip | None:
    """Gets a trip by its ID."""
    trip = db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return trip


@router.post("", response_model=TripResponse, status_code=status.HTTP_201_CREATED)
def create_trip(trip_data: TripCreate, db: Session = Depends(get_db)) -> Trip:
    """Create a new field trip."""
    trip = Trip(**trip_data.model_dump())
    db.add(trip)
    db.commit()
    db.refresh(trip)
    return trip


@router.put("/{trip_id}", response_model=TripResponse)
def update_trip(trip_id: int, trip_data: TripCreate, db: Session = Depends(get_db)) -> Trip:
    """Updates an existing trip."""
    trip = db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    for field, value in trip_data.model_dump().items():
        setattr(trip, field, value)

    db.commit()
    db.refresh(trip)
    return trip


@router.delete("/{trip_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_trip(trip_id: int, db: Session = Depends(get_db)) -> None:
    """Deletes a trip and its associated records (cascade)."""
    trip = db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    db.delete(trip)
    db.commit()


@router.get("/{trip_id}/records", response_model=list[RecordWithSpeciesResponse])
def get_trip_records(
    trip_id: int, db: Session = Depends(get_db)
) -> list[RecordWithSpeciesResponse]:
    """Gets all records for a specific trip, including species info."""
    trip = db.get(Trip, trip_id)
    if not trip:
        raise HTTPException(status_code=404, detail="Trip not found")

    records = (
        db.query(Record).options(joinedload(Record.species)).filter(Record.trip_id == trip_id).all()
    )

    return [
        RecordWithSpeciesResponse(
            id=r.id,
            trip_id=r.trip_id,
            species_id=r.species_id,
            count=r.count,
            notes=r.notes,
            created_at=r.created_at,
            common_name=r.species.common_name,
            scientific_name=r.species.scientific_name,
        )
        for r in records
    ]
