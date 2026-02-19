import httpx
import pytest

from app.config import Settings
from app.services.weather import WeatherClient, WeatherClientError


def test_get_weather_returns_description_and_temperature(monkeypatch) -> None:
    client = WeatherClient(
        Settings(
            weather_geocoding_base_url="https://geo.example/api",
            weather_forecast_base_url="https://forecast.example/api",
            weather_timeout_seconds=1.5,
        ),
    )

    def fake_get(url: str, params: dict[str, object], timeout: float) -> httpx.Response:
        assert timeout == 1.5

        if url == "https://geo.example/api":
            assert params == {
                "name": "Tehran",
                "count": 1,
                "language": "en",
                "format": "json",
            }
            request = httpx.Request("GET", url, params=params)
            return httpx.Response(
                200,
                request=request,
                json={
                    "results": [
                        {
                            "name": "Tehran",
                            "latitude": 35.6892,
                            "longitude": 51.389,
                        },
                    ],
                },
            )

        assert url == "https://forecast.example/api"
        assert params == {
            "latitude": 35.6892,
            "longitude": 51.389,
            "current": "temperature_2m,weather_code",
        }
        request = httpx.Request("GET", url, params=params)
        return httpx.Response(
            200,
            request=request,
            json={
                "current": {
                    "temperature_2m": 26.2,
                    "weather_code": 0,
                },
            },
        )

    monkeypatch.setattr("app.services.weather.httpx.get", fake_get)

    assert client.get_weather("Tehran") == {
        "description": "clear sky",
        "temperature_c": 26.2,
    }


def test_get_weather_city_not_found_raises_client_error(monkeypatch) -> None:
    client = WeatherClient(
        Settings(
            weather_geocoding_base_url="https://geo.example/api",
            weather_forecast_base_url="https://forecast.example/api",
            weather_timeout_seconds=1.5,
        ),
    )

    def fake_get(url: str, params: dict[str, object], timeout: float) -> httpx.Response:
        assert url == "https://geo.example/api"
        assert timeout == 1.5
        request = httpx.Request("GET", url, params=params)
        return httpx.Response(200, request=request, json={"results": []})

    monkeypatch.setattr("app.services.weather.httpx.get", fake_get)

    with pytest.raises(WeatherClientError, match="No weather location match found"):
        client.get_weather("Tehran")


def test_get_weather_timeout_raises_client_error(monkeypatch) -> None:
    client = WeatherClient(
        Settings(
            weather_geocoding_base_url="https://geo.example/api",
            weather_forecast_base_url="https://forecast.example/api",
            weather_timeout_seconds=1.5,
        ),
    )

    def fake_get(*_args, **_kwargs) -> httpx.Response:
        raise httpx.TimeoutException("timed out")

    monkeypatch.setattr("app.services.weather.httpx.get", fake_get)

    with pytest.raises(WeatherClientError, match="timed out"):
        client.get_weather("Tehran")
