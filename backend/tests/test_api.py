from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root():

    response = client.get("/")

    assert response.status_code == 200

    assert response.json()["status"] == "running"


def test_iss_latest():

    response = client.get(
        "/iss/latest"
    )

    assert response.status_code == 200


def test_apod_latest():

    response = client.get(
        "/apod/latest"
    )

    assert response.status_code == 200


def test_asteroids():

    response = client.get(
        "/asteroids"
    )

    assert response.status_code == 200
    