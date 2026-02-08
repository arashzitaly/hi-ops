import httpx
import pytest

from app.config import Settings
from app.services.weather import WeatherClient, WeatherClientError


def test_get_weather_returns_description_and_temperature(monkeypatch) -> None:
    client = WeatherClient(
        Settings(
            weather_api_base_url="https://weather.example/api",
            weather_api_key="test-api-key",
            weather_timeout_seconds=1.5,
        ),
    )

    def fake_get(url: str, params: dict[str, str], timeout: float) -> httpx.Response:
        assert url == "https://weather.example/api"
        assert params == {
            "q": "Tehran",
            "appid": "test-api-key",
            "units": "metric",
        }
        assert timeout == 1.5

        request = httpx.Request("GET", url, params=params)
        return httpx.Response(
            200,
            request=request,
            json={
                "weather": [{"description": "sunny"}],
                "main": {"temp": 26.2},
            },
        )

    monkeypatch.setattr("app.services.weather.httpx.get", fake_get)

    assert client.get_weather("Tehran") == {
        "description": "sunny",
        "temperature_c": 26.2,
    }


def test_get_weather_requires_api_key() -> None:
    client = WeatherClient(
        Settings(
            weather_api_base_url="https://weather.example/api",
            weather_api_key=None,
            weather_timeout_seconds=1.5,
        ),
    )

    with pytest.raises(WeatherClientError, match="WEATHER_API_KEY"):
        client.get_weather("Tehran")


def test_get_weather_timeout_raises_client_error(monkeypatch) -> None:
    client = WeatherClient(
        Settings(
            weather_api_base_url="https://weather.example/api",
            weather_api_key="test-api-key",
            weather_timeout_seconds=1.5,
        ),
    )

    def fake_get(*_args, **_kwargs) -> httpx.Response:
        raise httpx.TimeoutException("timed out")

    monkeypatch.setattr("app.services.weather.httpx.get", fake_get)

    with pytest.raises(WeatherClientError, match="timed out"):
        client.get_weather("Tehran")
