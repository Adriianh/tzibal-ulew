"""
Endpoints CRUD for species catalog.
"""

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from api.dependencies import get_db
from api.models.species import Species
from api.schemas.species import SpeciesCreate, SpeciesResponse

router = APIRouter(prefix="/species", tags=["Species"])


@router.get("/", response_model=list[SpeciesResponse])
def list_species(
    type: str | None = Query(None, description="Filter by type (Bird, Mammal, Plant, ...)"),
    db: Session = Depends(get_db),
) -> list[Species]:
    """Lists all species, optionally filtered by type."""
    query = db.query(Species)
    if type:
        query = query.filter(Species.type == type)
    return query.order_by(Species.common_name).all()


@router.get("/{species_id}", response_model=SpeciesResponse)
def get_species(species_id: int, db: Session = Depends(get_db)) -> Species | None:
    """Retrieves a species by its ID."""
    species = db.get(Species, species_id)
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")
    return species


@router.post("/", response_model=SpeciesResponse, status_code=status.HTTP_201_CREATED)
def create_species(species_data: SpeciesCreate, db: Session = Depends(get_db)) -> Species:
    """Creates a new species in the catalog."""
    species = Species(**species_data.model_dump())
    db.add(species)
    db.commit()
    db.refresh(species)
    return species


@router.put("/{species_id}", response_model=SpeciesResponse)
def update_species(
    species_id: int, species_data: SpeciesCreate, db: Session = Depends(get_db)
) -> Species:
    """Updates an existing species."""
    species = db.get(Species, species_id)
    if not species:
        raise HTTPException(status_code=404, detail="Species not found")

    for field, value in species_data.model_dump().items():
        setattr(species, field, value)

    db.commit()
    db.refresh(species)
    return species
