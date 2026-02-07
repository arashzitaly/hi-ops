from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_hello_world() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_greet_happy_path() -> None:
    response = client.get("/greet", params={"name": "Arash"})

    assert response.status_code == 200

    assert response.json() == {"message": "Hello, Arash!"}


def test_greet_missing_name_returns_422() -> None:
    response = client.get("/greet")

    assert response.status_code == 422

    body = response.json()
    assert body["detail"][0]["loc"] == ["query", "name"]
    assert body["detail"][0]["msg"] == "Field required"


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
