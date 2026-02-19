import os
from dataclasses import dataclass
from typing import Optional

DEFAULT_WEATHER_GEOCODING_BASE_URL = "https://geocoding-api.open-meteo.com/v1/search"
DEFAULT_WEATHER_FORECAST_BASE_URL = "https://api.open-meteo.com/v1/forecast"
DEFAULT_WEATHER_TIMEOUT_SECONDS = 3.0


@dataclass(frozen=True)
class Settings:
    weather_geocoding_base_url: str
    weather_forecast_base_url: str
    weather_timeout_seconds: float


def _parse_timeout(raw_timeout: Optional[str]) -> float:
    if raw_timeout is None:
        return DEFAULT_WEATHER_TIMEOUT_SECONDS

    try:
        timeout = float(raw_timeout)
    except ValueError:
        return DEFAULT_WEATHER_TIMEOUT_SECONDS

    if timeout <= 0:
        return DEFAULT_WEATHER_TIMEOUT_SECONDS

    return timeout


def get_settings() -> Settings:
    return Settings(
        weather_geocoding_base_url=os.getenv(
            "WEATHER_GEOCODING_BASE_URL",
            DEFAULT_WEATHER_GEOCODING_BASE_URL,
        ),
        weather_forecast_base_url=os.getenv(
            "WEATHER_FORECAST_BASE_URL",
            os.getenv(
                "WEATHER_API_BASE_URL",
                DEFAULT_WEATHER_FORECAST_BASE_URL,
            ),
        ),
        weather_timeout_seconds=_parse_timeout(
            os.getenv("WEATHER_TIMEOUT_SECONDS"),
        ),
    )
