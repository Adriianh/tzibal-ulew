"""
FastAPI application entry point.
Registers all routers and configures middleware.
"""

from fastapi import FastAPI

from api.routers import records, species, trips

app = FastAPI(
    title="Tz'ib'al Ulew API",
    description="API local para la app de escritorio de salidas de campo",
    version="0.1.0",
)

app.include_router(trips.router)
app.include_router(species.router)
app.include_router(records.router)


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint to verify that the API is running."""
    return {"status": "ok"}
