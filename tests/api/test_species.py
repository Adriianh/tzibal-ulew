"""
Tests for species catalog CRUD endpoints.
"""

from fastapi.testclient import TestClient


def test_list_species_empty(client: TestClient) -> None:
    """GET /species returns empty list when no species exist."""
    response = client.get("/species/")
    assert response.status_code == 200
    assert response.json() == []


def test_create_species(client: TestClient) -> None:
    """POST /species creates a species and returns 201."""
    payload = {
        "common_name": "Quetzal",
        "scientific_name": "Pharomachrus mocinno",
        "type": "Bird",
    }
    response = client.post("/species/", json=payload)
    assert response.status_code == 201

    data = response.json()
    assert data["common_name"] == "Quetzal"
    assert data["scientific_name"] == "Pharomachrus mocinno"
    assert data["type"] == "Bird"
    assert "id" in data


def test_list_species_with_data(client: TestClient) -> None:
    """GET /species returns created species."""
    client.post(
        "/species/",
        json={
            "common_name": "Tapir",
            "scientific_name": "Tapirus bairdii",
            "type": "Mammal",
        },
    )

    response = client.get("/species/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["common_name"] == "Tapir"


def test_get_species_by_id(client: TestClient) -> None:
    """GET /species/{id} returns a species by ID."""
    create_resp = client.post(
        "/species/",
        json={
            "common_name": "Colibrí",
            "scientific_name": "Selasphorus",
            "type": "Bird",
        },
    )
    species_id = create_resp.json()["id"]

    response = client.get(f"/species/{species_id}")
    assert response.status_code == 200
    assert response.json()["common_name"] == "Colibrí"


def test_get_species_not_found(client: TestClient) -> None:
    """GET /species/{id} returns 404 for non-existent species."""
    response = client.get("/species/999")
    assert response.status_code == 404


def test_update_species(client: TestClient) -> None:
    """PUT /species/{id} updates a species."""
    create_resp = client.post(
        "/species/",
        json={
            "common_name": "Old",
            "scientific_name": "Oldus nameus",
            "type": "Insect",
        },
    )
    species_id = create_resp.json()["id"]

    update_resp = client.put(
        f"/species/{species_id}",
        json={
            "common_name": "New",
            "scientific_name": "Newus nameus",
            "type": "Amphibian",
        },
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["common_name"] == "New"


def test_filter_species_by_type(client: TestClient) -> None:
    """GET /species?type=Bird filters by type."""
    client.post(
        "/species/",
        json={
            "common_name": "Quetzal",
            "scientific_name": "Pharomachrus mocinno",
            "type": "Bird",
        },
    )
    client.post(
        "/species/",
        json={
            "common_name": "Tapir",
            "scientific_name": "Tapirus bairdii",
            "type": "Mammal",
        },
    )

    response = client.get("/species/?type=Bird")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["common_name"] == "Quetzal"
