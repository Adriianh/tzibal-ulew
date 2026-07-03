"""
Tests for trip CRUD endpoints.
"""

from fastapi.testclient import TestClient


def test_list_trips_empty(client: TestClient) -> None:
    """GET /trips returns empty list when no trips exist."""
    response = client.get("/trips")
    assert response.status_code == 200
    assert response.json() == []


def test_create_trip(client: TestClient) -> None:
    """POST /trips creates a trip and returns 201."""
    payload = {
        "name": "Volcán Tajumulco",
        "trip_date": "2026-06-15",
        "place": "San Marcos",
        "latitude": 15.0,
        "longitude": -91.5,
        "altitude_m": 4220,
        "weather": "Sunny",
        "temperature_c": 18,
        "notes": "Excelente día",
    }
    response = client.post("/trips/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["name"] == "Volcán Tajumulco"
    assert data["latitude"] == 15.0
    assert "id" in data
    assert "created_at" in data


def test_list_trips_not_empty(client: TestClient) -> None:
    """GET /trips returns created trips."""
    # Arrange
    client.post(
        "/trips/",
        json={
            "name": "Lago Atitlán",
            "trip_date": "2026-07-01",
            "place": "Sololá",
            "latitude": 14.7,
            "longitude": -91.2,
        },
    )

    # Act
    response = client.get("/trips/")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Lago Atitlán"


def test_get_trip_by_id(client: TestClient) -> None:
    """GET /trips/{id} returns a trip by ID."""
    create_resp = client.post(
        "/trips/",
        json={
            "name": "Biotopo Monterrico",
            "trip_date": "2026-05-10",
            "place": "Monterrico",
            "latitude": 13.9,
            "longitude": -90.5,
        },
    )
    trip_id = create_resp.json()["id"]

    response = client.get(f"/trips/{trip_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Biotopo Monterrico"


def test_get_trip_not_found(client: TestClient) -> None:
    """GET /trips/{id} returns 404 for non-existent trip."""
    response = client.get("/trips/999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Trip not found"


def test_update_trip(client: TestClient) -> None:
    """PUT /trips/{id} updates a trip."""
    create_resp = client.post(
        "/trips/",
        json={
            "name": "Old Name",
            "trip_date": "2026-01-01",
            "place": "Guatemala",
            "latitude": 14.5,
            "longitude": -90.5,
        },
    )
    trip_id = create_resp.json()["id"]

    update_resp = client.put(
        f"/trips/{trip_id}",
        json={
            "name": "New Name",
            "trip_date": "2026-06-15",
            "place": "Guatemala",
            "latitude": 14.5,
            "longitude": -90.5,
        },
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["name"] == "New Name"


def test_delete_trip(client: TestClient) -> None:
    """DELETE /trips/{id} deletes a trip."""
    create_resp = client.post(
        "/trips/",
        json={
            "name": "Trip to Delete",
            "trip_date": "2026-03-15",
            "place": "Quetzaltenango",
            "latitude": 14.8,
            "longitude": -91.5,
        },
    )
    trip_id = create_resp.json()["id"]

    del_resp = client.delete(f"/trips/{trip_id}")
    assert del_resp.status_code == 204

    get_resp = client.get(f"/trips/{trip_id}")
    assert get_resp.status_code == 404


def test_delete_trip_not_found(client: TestClient) -> None:
    """DELETE /trips/{id} returns 404 for non-existent trip."""
    response = client.delete("/trips/999")
    assert response.status_code == 404
