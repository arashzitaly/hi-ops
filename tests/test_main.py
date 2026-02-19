from fastapi.testclient import TestClient

from app.main import app, weather_client
from app.services.weather import WeatherClientError

client = TestClient(app)


def test_root_returns_hello_world() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World!"}


def test_greet_happy_path() -> None:
    response = client.get("/greet", params={"name": "Arash", "surname": "Karimi"})

    assert response.status_code == 200

    assert response.json() == {"message": "Hello, Arash Karimi!"}


def test_greet_missing_name_returns_422() -> None:
    response = client.get("/greet", params={"surname": "Karimi"})

    assert response.status_code == 422

    body = response.json()
    assert body["detail"][0]["loc"] == ["query", "name"]
    assert body["detail"][0]["msg"] == "Field required"


def test_greet_missing_surname_returns_422() -> None:
    response = client.get("/greet", params={"name": "Arash"})

    assert response.status_code == 422

    body = response.json()
    assert body["detail"][0]["loc"] == ["query", "surname"]
    assert body["detail"][0]["msg"] == "Field required"


def test_greet_with_phone_returns_phone() -> None:
    response = client.get(
        "/greet",
        params={
            "name": "Arash",
            "surname": "Karimi",
            "phone": "555-0101",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, Arash Karimi!",
        "phone": "555-0101",
    }


def test_greet_with_city_returns_weather(monkeypatch) -> None:
    def fake_get_weather(city: str) -> dict[str, object]:
        assert city == "Tehran"
        return {"description": "clear sky", "temperature_c": 18.4}

    monkeypatch.setattr(weather_client, "get_weather", fake_get_weather)

    response = client.get(
        "/greet",
        params={
            "name": "Arash",
            "surname": "Karimi",
            "city": "Tehran",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, Arash Karimi!",
        "city": "Tehran",
        "weather": {"description": "clear sky", "temperature_c": 18.4},
    }


def test_greet_with_city_handles_weather_failure(monkeypatch) -> None:
    def fake_get_weather(_city: str) -> dict[str, object]:
        raise WeatherClientError("Weather lookup timed out.")

    monkeypatch.setattr(weather_client, "get_weather", fake_get_weather)

    response = client.get(
        "/greet",
        params={
            "name": "Arash",
            "surname": "Karimi",
            "city": "Tehran",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": "Hello, Arash Karimi!",
        "city": "Tehran",
        "weather_error": "Weather lookup timed out.",
    }


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
