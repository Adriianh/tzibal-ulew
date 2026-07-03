"""
HTTP client for the local FastAPI server.
"""

from __future__ import annotations

from typing import Any

import httpx

from ui.exceptions import (
    ApiConnectionError,
    ApiNotFoundError,
    ApiResponseError,
    ApiServerError,
    ApiValidationError,
)


class BaseClient:
    """Shared HTTP logic for all sub-clients."""

    def __init__(self, client: httpx.Client) -> None:
        self.client = client

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
    ) -> Any:
        """Send an HTTP request and handle errors."""
        try:
            response = self.client.request(method, endpoint, params=params, json=json_data)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            status_code = exc.response.status_code
            if status_code == 404:
                raise ApiNotFoundError() from exc
            elif status_code == 422:
                raise ApiValidationError() from exc
            elif status_code >= 500:
                raise ApiServerError() from exc
            else:
                raise ApiResponseError(status_code, exc.response.text) from exc
        except httpx.RequestError as exc:
            url = exc.request.url if exc.request is not None else "unknown URL"
            raise ApiConnectionError(f"An error occurred while requesting {url!r}.") from exc

        if response.status_code == 204:
            return None

        return response.json()

    def _get(self, endpoint: str, params: dict[str, Any] | None = None) -> Any:
        """Send a GET request to the specified endpoint."""
        return self._request("GET", endpoint, params=params)

    def _post(self, endpoint: str, json_data: dict[str, Any]) -> Any:
        """Send a POST request to the specified endpoint."""
        return self._request("POST", endpoint, json_data=json_data)

    def _put(self, endpoint: str, json_data: dict[str, Any]) -> Any:
        """Send a PUT request to the specified endpoint."""
        return self._request("PUT", endpoint, json_data=json_data)

    def _delete(self, endpoint: str) -> Any:
        """Send a DELETE request to the specified endpoint."""
        return self._request("DELETE", endpoint)


class StatsClient(BaseClient):
    """Client for the /stats endpoint."""

    def get_summary(self) -> Any:
        """Get summary statistics from the /stats endpoint."""
        return self._get("/stats/summary")

    def get_top_species(self, limit: int = 10) -> Any:
        """Get top species from the /stats/top-species endpoint."""
        return self._get("/stats/top-species", params={"limit": limit})

    def get_by_month(self) -> Any:
        """Get statistics by month from the /stats/by-month endpoint."""
        return self._get("/stats/by-month")


class TripsClient(BaseClient):
    """Client for the /trips endpoint."""

    def list_trips(self) -> Any:
        """Get all trips from the /trips endpoint."""
        return self._get("/trips")

    def get_trip(self, trip_id: int) -> Any:
        """Get a specific trip by ID from the /trips/{trip_id} endpoint."""
        return self._get(f"/trips/{trip_id}")

    def create_trip(self, trip_data: dict[str, Any]) -> Any:
        """Create a new trip using the /trips endpoint."""
        return self._post("/trips", json_data=trip_data)

    def update_trip(self, trip_id: int, trip_data: dict[str, Any]) -> Any:
        """Update an existing trip by ID using the /trips/{trip_id} endpoint."""
        return self._put(f"/trips/{trip_id}", json_data=trip_data)

    def delete_trip(self, trip_id: int) -> Any:
        """Delete a specific trip by ID using the /trips/{trip_id} endpoint."""
        return self._delete(f"/trips/{trip_id}")

    def get_trip_records(self, trip_id: int) -> Any:
        """Get all records for a specific trip by ID from the /trips/{trip_id}/records endpoint."""
        return self._get(f"/trips/{trip_id}/records")


class SpeciesClient(BaseClient):
    """Client for the /species endpoint."""

    def list_species(self, type: str | None = None) -> Any:
        """List all species, optionally filtered by type from the /species endpoint."""
        params = {"type": type} if type else None
        return self._get("/species", params=params)

    def get_species(self, species_id: int) -> Any:
        """Get a specific species by ID from the /species/{species_id} endpoint."""
        return self._get(f"/species/{species_id}")

    def create_species(self, species_data: dict[str, Any]) -> Any:
        """Create a new species using the /species endpoint."""
        return self._post("/species", json_data=species_data)

    def update_species(self, species_id: int, species_data: dict[str, Any]) -> Any:
        """Update an existing species by ID using the /species/{species_id} endpoint."""
        return self._put(f"/species/{species_id}", json_data=species_data)


class RecordsClient(BaseClient):
    """Client for the /records endpoint."""

    def create_record(self, record_data: dict[str, Any]) -> Any:
        """Create a new record using the /records endpoint."""
        return self._post("/records", json_data=record_data)

    def update_record(self, record_id: int, record_data: dict[str, Any]) -> Any:
        """Update an existing record by ID using the /records/{record_id} endpoint."""
        return self._put(f"/records/{record_id}", json_data=record_data)

    def delete_record(self, record_id: int) -> Any:
        """Delete a specific record by ID using the /records/{record_id} endpoint."""
        return self._delete(f"/records/{record_id}")


class MapClient(BaseClient):
    """Client for the /map endpoint."""

    def get_map_points(self) -> Any:
        """Get map points for all trips with their species from the /map/points endpoint."""
        return self._get("/map/points")


class ApiClient:
    """Facade that exposes all sub-clients for the API."""

    def __init__(self, base_url: str) -> None:
        self.client = httpx.Client(base_url=base_url)
        self.stats = StatsClient(self.client)
        self.trips = TripsClient(self.client)
        self.species = SpeciesClient(self.client)
        self.records = RecordsClient(self.client)
        self.map = MapClient(self.client)

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self.client.close()
