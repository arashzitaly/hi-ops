from typing import Any

import httpx

from app.config import Settings

WMO_WEATHER_CODES = {
    0: "clear sky",
    1: "mainly clear",
    2: "partly cloudy",
    3: "overcast",
    45: "fog",
    48: "depositing rime fog",
    51: "light drizzle",
    53: "moderate drizzle",
    55: "dense drizzle",
    56: "light freezing drizzle",
    57: "dense freezing drizzle",
    61: "slight rain",
    63: "moderate rain",
    65: "heavy rain",
    66: "light freezing rain",
    67: "heavy freezing rain",
    71: "slight snow fall",
    73: "moderate snow fall",
    75: "heavy snow fall",
    77: "snow grains",
    80: "slight rain showers",
    81: "moderate rain showers",
    82: "violent rain showers",
    85: "slight snow showers",
    86: "heavy snow showers",
    95: "thunderstorm",
    96: "thunderstorm with slight hail",
    99: "thunderstorm with heavy hail",
}


class WeatherClientError(RuntimeError):
    pass


class WeatherClient:
    def __init__(self, settings: Settings) -> None:
        self._geocoding_base_url = settings.weather_geocoding_base_url
        self._forecast_base_url = settings.weather_forecast_base_url
        self._timeout_seconds = settings.weather_timeout_seconds

    def get_weather(self, city: str) -> dict[str, Any]:
        try:
            geocoding_response = httpx.get(
                self._geocoding_base_url,
                params={
                    "name": city,
                    "count": 1,
                    "language": "en",
                    "format": "json",
                },
                timeout=self._timeout_seconds,
            )
            geocoding_response.raise_for_status()

            geocoding_payload = geocoding_response.json()
            results = geocoding_payload.get("results")
            if not isinstance(results, list) or not results:
                raise WeatherClientError(
                    f"No weather location match found for '{city}'."
                )

            location = results[0]
            latitude = location.get("latitude")
            longitude = location.get("longitude")

            if not isinstance(latitude, (int, float)) or not isinstance(
                longitude,
                (int, float),
            ):
                raise WeatherClientError(
                    "Weather lookup returned unexpected geocoding format.",
                )

            forecast_response = httpx.get(
                self._forecast_base_url,
                params={
                    "latitude": latitude,
                    "longitude": longitude,
                    "current": "temperature_2m,weather_code",
                },
                timeout=self._timeout_seconds,
            )
            forecast_response.raise_for_status()
        except httpx.TimeoutException as exc:
            raise WeatherClientError("Weather lookup timed out.") from exc
        except httpx.HTTPStatusError as exc:
            raise WeatherClientError(
                f"Weather lookup failed with status {exc.response.status_code}.",
            ) from exc
        except httpx.RequestError as exc:
            raise WeatherClientError("Weather lookup request failed.") from exc

        payload = forecast_response.json()
        current = payload.get("current")

        if (
            not isinstance(current, dict)
            or "temperature_2m" not in current
            or "weather_code" not in current
        ):
            raise WeatherClientError(
                "Weather lookup returned unexpected response format.",
            )

        weather_code = current["weather_code"]
        if not isinstance(weather_code, (int, float)):
            raise WeatherClientError(
                "Weather lookup returned unexpected weather code format.",
            )

        description = WMO_WEATHER_CODES.get(
            int(weather_code),
            f"WMO weather code {weather_code}",
        )

        return {
            "description": description,
            "temperature_c": current["temperature_2m"],
        }
