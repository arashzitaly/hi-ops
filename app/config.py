import os
from dataclasses import dataclass
from typing import Optional

DEFAULT_WEATHER_API_BASE_URL = "https://api.openweathermap.org/data/2.5/weather"
DEFAULT_WEATHER_TIMEOUT_SECONDS = 3.0


@dataclass(frozen=True)
class Settings:
    weather_api_base_url: str
    weather_api_key: Optional[str]
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
        weather_api_base_url=os.getenv(
            "WEATHER_API_BASE_URL",
            DEFAULT_WEATHER_API_BASE_URL,
        ),
        weather_api_key=os.getenv("WEATHER_API_KEY"),
        weather_timeout_seconds=_parse_timeout(
            os.getenv("WEATHER_TIMEOUT_SECONDS"),
        ),
    )
