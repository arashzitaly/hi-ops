from typing import Any

import httpx

from app.config import Settings


class WeatherClientError(RuntimeError):
    pass


class WeatherClient:
    def __init__(self, settings: Settings) -> None:
        self._base_url = settings.weather_api_base_url
        self._api_key = settings.weather_api_key
        self._timeout_seconds = settings.weather_timeout_seconds

    def get_weather(self, city: str) -> dict[str, Any]:
        if not self._api_key:
            raise WeatherClientError("WEATHER_API_KEY is not configured.")

        try:
            response = httpx.get(
                self._base_url,
                params={
                    "q": city,
                    "appid": self._api_key,
                    "units": "metric",
                },
                timeout=self._timeout_seconds,
            )
            response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise WeatherClientError("Weather lookup timed out.") from exc
        except httpx.HTTPStatusError as exc:
            raise WeatherClientError(
                f"Weather lookup failed with status {exc.response.status_code}.",
            ) from exc
        except httpx.RequestError as exc:
            raise WeatherClientError("Weather lookup request failed.") from exc

        payload = response.json()
        weather_entries = payload.get("weather")
        main = payload.get("main")

        if (
            not isinstance(weather_entries, list)
            or not weather_entries
            or "description" not in weather_entries[0]
            or not isinstance(main, dict)
            or "temp" not in main
        ):
            raise WeatherClientError(
                "Weather lookup returned unexpected response format.",
            )

        return {
            "description": str(weather_entries[0]["description"]),
            "temperature_c": main["temp"],
        }
