"""
Tests for statistics endpoints.
"""

from fastapi.testclient import TestClient


def test_stats_summary_empty(client: TestClient) -> None:
    """GET /stats/summary returns zeros when no data."""
    response = client.get("/stats/summary")
    assert response.status_code == 200
    data = response.json()
    assert data == {"total_trips": 0, "total_species": 0, "total_records": 0}


def test_stats_summary_with_data(client: TestClient) -> None:
    """GET /stats/summary returns correct counts."""
    # Create a trip and species
    trip_resp = client.post(
        "/trips/",
        json={
            "name": "Test",
            "trip_date": "2026-06-15",
            "place": "GT",
            "latitude": 14.5,
            "longitude": -90.5,
        },
    )
    trip_id = trip_resp.json()["id"]
    assert isinstance(trip_id, int)

    sp_resp = client.post(
        "/species/",
        json={
            "common_name": "Quetzal",
            "scientific_name": "P. mocinno",
            "type": "Bird",
        },
    )
    species_id = sp_resp.json()["id"]
    assert isinstance(species_id, int)

    client.post(
        "/records/",
        json={
            "trip_id": trip_id,
            "species_id": species_id,
            "count": 1,
        },
    )

    response = client.get("/stats/summary")
    assert response.status_code == 200
    assert response.json() == {"total_trips": 1, "total_species": 1, "total_records": 1}


def test_top_species_empty(client: TestClient) -> None:
    """GET /stats/top-species returns empty list when no records."""
    response = client.get("/stats/top-species")
    assert response.status_code == 200
    assert response.json() == []


def test_top_species_with_data(client: TestClient) -> None:
    """GET /stats/top-species returns ranked species list."""
    trip_resp = client.post(
        "/trips/",
        json={
            "name": "Test",
            "trip_date": "2026-06-15",
            "place": "GT",
            "latitude": 14.5,
            "longitude": -90.5,
        },
    )
    trip_id = trip_resp.json()["id"]
    assert isinstance(trip_id, int)

    sp1_resp = client.post(
        "/species/",
        json={
            "common_name": "Quetzal",
            "scientific_name": "P. mocinno",
            "type": "Bird",
        },
    )
    sp2_resp = client.post(
        "/species/",
        json={
            "common_name": "Tapir",
            "scientific_name": "T. bairdii",
            "type": "Mammal",
        },
    )
    sp1 = sp1_resp.json()["id"]
    sp2 = sp2_resp.json()["id"]
    assert isinstance(sp1, int)
    assert isinstance(sp2, int)

    # Record Quetzal twice, Tapir once
    client.post("/records/", json={"trip_id": trip_id, "species_id": sp1, "count": 1})
    client.post("/records/", json={"trip_id": trip_id, "species_id": sp1, "count": 1})
    client.post("/records/", json={"trip_id": trip_id, "species_id": sp2, "count": 1})

    response = client.get("/stats/top-species")
    data = response.json()
    assert len(data) == 2
    assert data[0]["common_name"] == "Quetzal"
    assert data[0]["record_count"] == 2
    assert data[1]["common_name"] == "Tapir"
    assert data[1]["record_count"] == 1


def test_trips_by_month_empty(client: TestClient) -> None:
    """GET /stats/by-month returns empty list when no trips."""
    response = client.get("/stats/by-month")
    assert response.status_code == 200
    assert response.json() == []


def test_trips_by_month_with_data(client: TestClient) -> None:
    """GET /stats/by-month returns trips grouped by month."""
    client.post(
        "/trips/",
        json={
            "name": "Trip 1",
            "trip_date": "2026-06-15",
            "place": "GT",
            "latitude": 14.5,
            "longitude": -90.5,
        },
    )
    client.post(
        "/trips/",
        json={
            "name": "Trip 2",
            "trip_date": "2026-06-20",
            "place": "GT",
            "latitude": 14.5,
            "longitude": -90.5,
        },
    )
    client.post(
        "/trips/",
        json={
            "name": "Trip 3",
            "trip_date": "2026-07-01",
            "place": "GT",
            "latitude": 14.5,
            "longitude": -90.5,
        },
    )

    response = client.get("/stats/by-month")
    data = response.json()
    assert len(data) == 2

    june = next(m for m in data if m["month"] == 6)
    july = next(m for m in data if m["month"] == 7)
    assert june["trip_count"] == 2
    assert july["trip_count"] == 1
