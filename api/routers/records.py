"""
Endpoints for sighting records.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.models.record import Record
from api.schemas.record import RecordCreate, RecordResponse, RecordUpdate

router = APIRouter(prefix="/records", tags=["Records"])


@router.post("/", response_model=RecordResponse, status_code=status.HTTP_201_CREATED)
def create_record(record_data: RecordCreate, db: Session = Depends(get_db)) -> Record:
    """Adds a sighting record to a trip."""

    # Verifies that the trip exists
    from api.models.trip import Trip

    if not db.get(Trip, record_data.trip_id):
        raise HTTPException(status_code=404, detail="Trip not found")

    # Verifies that the species exists
    from api.models.species import Species

    if not db.get(Species, record_data.species_id):
        raise HTTPException(status_code=404, detail="Species not found")

    record = Record(**record_data.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.put("/{record_id}", response_model=RecordResponse)
def update_record(
    record_id: int, record_data: RecordUpdate, db: Session = Depends(get_db)
) -> Record:
    """Updates a sighting record (only count and notes)."""
    record = db.get(Record, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    for field, value in record_data.model_dump(exclude_unset=True).items():
        setattr(record, field, value)

    db.commit()
    db.refresh(record)
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(record_id: int, db: Session = Depends(get_db)) -> None:
    """Deletes a sighting record."""
    record = db.get(Record, record_id)
    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    db.delete(record)
    db.commit()
