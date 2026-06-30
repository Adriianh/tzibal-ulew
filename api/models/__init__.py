"""
All models are imported here to make them available for
use in other parts of the application.

It also works for Alembic migrations, as it needs to know about all models
"""

from api.models.record import Record
from api.models.species import Species
from api.models.trip import Trip

__all__ = ["Record", "Species", "Trip"]
