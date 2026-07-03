"""
Tests for sighting record endpoints.
"""

from fastapi.testclient import TestClient


def _create_trip(client: TestClient) -> int:
    """Helper to create a trip and return its ID."""
    resp = client.post(
        "/trips/",
        json={
            "name": "Test Trip",
            "trip_date": "2026-06-15",
            "place": "Guatemala",
            "latitude": 14.5,
            "longitude": -90.5,
        },
    )

    trip_id = resp.json()["id"]
    assert isinstance(trip_id, int), "Trip ID should be an integer"
    return trip_id


def _create_species(client: TestClient, name: str = "Test Species") -> int:
    """Helper to create a species and return its ID."""
    resp = client.post(
        "/species/",
        json={
            "common_name": name,
            "scientific_name": f"{name}us fieldus",
            "type": "Bird",
        },
    )

    trip_id = resp.json()["id"]
    assert isinstance(trip_id, int), "Species ID should be an integer"
    return trip_id


def test_create_record(client: TestClient) -> None:
    """POST /records creates a record and returns 201."""
    trip_id = _create_trip(client)
    species_id = _create_species(client)

    response = client.post(
        "/records/",
        json={
            "trip_id": trip_id,
            "species_id": species_id,
            "count": 2,
            "notes": "Avistado en la cima",
        },
    )
    assert response.status_code == 201

    data = response.json()
    assert data["trip_id"] == trip_id
    assert data["species_id"] == species_id
    assert data["count"] == 2
    assert "id" in data
    assert "created_at" in data


def test_create_record_no_trip(client: TestClient) -> None:
    """POST /records with non-existent trip returns 404."""
    species_id = _create_species(client)

    response = client.post(
        "/records/",
        json={
            "trip_id": 999,
            "species_id": species_id,
            "count": 1,
        },
    )
    assert response.status_code == 404


def test_create_record_no_species(client: TestClient) -> None:
    """POST /records with non-existent species returns 404."""
    trip_id = _create_trip(client)

    response = client.post(
        "/records/",
        json={
            "trip_id": trip_id,
            "species_id": 999,
            "count": 1,
        },
    )
    assert response.status_code == 404


def test_update_record(client: TestClient) -> None:
    """PUT /records/{id} updates count and notes."""
    trip_id = _create_trip(client)
    species_id = _create_species(client)

    create_resp = client.post(
        "/records/",
        json={
            "trip_id": trip_id,
            "species_id": species_id,
            "count": 1,
            "notes": "Original",
        },
    )
    record_id = create_resp.json()["id"]

    update_resp = client.put(
        f"/records/{record_id}",
        json={
            "count": 5,
            "notes": "Actualizado",
        },
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["count"] == 5
    assert update_resp.json()["notes"] == "Actualizado"


def test_update_record_partial(client: TestClient) -> None:
    """PUT /records/{id} with only count leaves notes unchanged."""
    trip_id = _create_trip(client)
    species_id = _create_species(client)

    create_resp = client.post(
        "/records/",
        json={
            "trip_id": trip_id,
            "species_id": species_id,
            "count": 1,
            "notes": "Nota original",
        },
    )
    record_id = create_resp.json()["id"]

    update_resp = client.put(f"/records/{record_id}", json={"count": 10})
    assert update_resp.status_code == 200
    assert update_resp.json()["count"] == 10
    assert update_resp.json()["notes"] == "Nota original"


def test_delete_record(client: TestClient) -> None:
    """DELETE /records/{id} deletes a record."""
    trip_id = _create_trip(client)
    species_id = _create_species(client)

    create_resp = client.post(
        "/records/",
        json={
            "trip_id": trip_id,
            "species_id": species_id,
            "count": 1,
        },
    )
    record_id = create_resp.json()["id"]

    del_resp = client.delete(f"/records/{record_id}")
    assert del_resp.status_code == 204


def test_delete_record_not_found(client: TestClient) -> None:
    """DELETE /records/{id} returns 404 for non-existent record."""
    response = client.delete("/records/999")
    assert response.status_code == 404


def test_get_trip_records(client: TestClient) -> None:
    """GET /trips/{id}/records returns records with species info."""
    trip_id = _create_trip(client)
    sp1 = _create_species(client, "Quetzal")
    sp2 = _create_species(client, "Tapir")

    client.post(
        "/records/",
        json={
            "trip_id": trip_id,
            "species_id": sp1,
            "count": 2,
        },
    )
    client.post(
        "/records/",
        json={
            "trip_id": trip_id,
            "species_id": sp2,
            "count": 1,
        },
    )

    response = client.get(f"/trips/{trip_id}/records")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["common_name"] in ("Quetzal", "Tapir")
    assert "scientific_name" in data[0]


def test_get_trip_records_empty(client: TestClient) -> None:
    """GET /trips/{id}/records returns empty list when no records."""
    trip_id = _create_trip(client)

    response = client.get(f"/trips/{trip_id}/records")
    assert response.status_code == 200
    assert response.json() == []


def test_get_trip_records_not_found(client: TestClient) -> None:
    """GET /trips/{id}/records returns 404 for non-existent trip."""
    response = client.get("/trips/999/records")
    assert response.status_code == 404
