import logging
from typing import Any, Optional

from fastapi import FastAPI, Request

from app.config import get_settings
from app.services.weather import WeatherClient, WeatherClientError

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("hello_ops")

app = FastAPI(title="hello_ops")
weather_client = WeatherClient(get_settings())


@app.middleware("http")
async def log_requests(request: Request, call_next):
    response = await call_next(request)
    logger.info(
        "%s %s -> %s",
        request.method,
        request.url.path,
        response.status_code,
    )
    return response


@app.get("/")
def read_root() -> dict[str, str]:
    return {"message": "Hello, World!"}


@app.get("/greet")
def greet(
    name: str,
    surname: str,
    phone: Optional[str] = None,
    city: Optional[str] = None,
) -> dict[str, Any]:
    payload: dict[str, Any] = {"message": f"Hello, {name} {surname}!"}

    if phone:
        payload["phone"] = phone

    if city:
        payload["city"] = city
        try:
            payload["weather"] = weather_client.get_weather(city)
        except WeatherClientError as exc:
            logger.warning("Weather lookup failed for city '%s': %s", city, exc)
            payload["weather_error"] = str(exc)

    return payload


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
