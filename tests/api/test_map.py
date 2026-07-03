"""
Tests for map visualization endpoints.
"""

from fastapi.testclient import TestClient


def test_map_points_empty(client: TestClient) -> None:
    """GET /map/points returns empty list when no trips exist."""
    response = client.get("/map/points")
    assert response.status_code == 200
    assert response.json() == []


def test_map_points_with_data(client: TestClient) -> None:
    """GET /map/points returns trips with species info."""
    # Create a trip
    trip_resp = client.post(
        "/trips/",
        json={
            "name": "Volcán",
            "trip_date": "2026-06-15",
            "place": "Guatemala",
            "latitude": 15.0,
            "longitude": -91.5,
        },
    )
    trip_id = trip_resp.json()["id"]
    assert isinstance(trip_id, int)

    # Create a species
    sp_resp = client.post(
        "/species/",
        json={
            "common_name": "Quetzal",
            "scientific_name": "Pharomachrus mocinno",
            "type": "Bird",
        },
    )
    species_id = sp_resp.json()["id"]
    assert isinstance(species_id, int)

    # Add a record
    client.post(
        "/records/",
        json={
            "trip_id": trip_id,
            "species_id": species_id,
            "count": 2,
        },
    )

    response = client.get("/map/points")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1

    point = data[0]
    assert point["name"] == "Volcán"
    assert point["latitude"] == 15.0
    assert point["longitude"] == -91.5
    assert point["species_count"] == 1
    assert len(point["species"]) == 1
    assert point["species"][0]["common_name"] == "Quetzal"


def test_map_point_no_records(client: TestClient) -> None:
    """GET /map/points returns trip with empty species list."""
    trip_resp = client.post(
        "/trips/",
        json={
            "name": "Empty Trip",
            "trip_date": "2026-07-01",
            "place": "Sololá",
            "latitude": 14.7,
            "longitude": -91.2,
        },
    )
    trip_id = trip_resp.json()["id"]
    assert isinstance(trip_id, int)

    response = client.get("/map/points")
    data = response.json()
    trip = next(t for t in data if t["id"] == trip_id)
    assert trip["species_count"] == 0
    assert trip["species"] == []
