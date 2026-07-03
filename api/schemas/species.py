"""
Pydantic schemas for Species catalog
"""

from pydantic import BaseModel, ConfigDict, Field


class SpeciesBase(BaseModel):
    common_name: str = Field(
        ..., max_length=255, examples=["Quetzal"], description="Common name of the species"
    )
    scientific_name: str = Field(
        ...,
        max_length=255,
        examples=["Pharomachrus mocinno"],
        description="Scientific name of the species",
    )
    type: str = Field(
        ...,
        max_length=20,
        examples=["Bird"],
        description="Type of the species (e.g., Bird, Mammal, Plant, etc.)",
        pattern="^(Bird|Mammal|Reptile|Fish|Amphibian|Insect|Plant)$",
    )
    description: str | None = None


class SpeciesCreate(SpeciesBase):
    pass


class SpeciesResponse(SpeciesBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
