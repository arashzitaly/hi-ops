# Architecture

## High-Level Flow
1. Client sends request to FastAPI app.
2. Middleware logs method, path, and status code.
3. Endpoint handler builds response payload.
4. If `city` is provided, weather client runs geocoding lookup (`city -> lat/lon`).
5. Weather client runs forecast lookup (`lat/lon -> current weather`).
6. Handler returns final JSON response.

## Code Layout
- `app/main.py`: app creation, middleware, endpoints.
- `app/config.py`: environment-driven settings and defaults.
- `app/services/weather.py`: external weather integration and error handling.
- `tests/test_main.py`: API behavior tests.
- `tests/test_weather.py`: weather client unit tests with mocked HTTP calls.

## Config Model
- `WEATHER_GEOCODING_BASE_URL`
- `WEATHER_FORECAST_BASE_URL`
- `WEATHER_TIMEOUT_SECONDS`

Fallback behavior:
- Missing or invalid timeout values fall back to default `3.0` seconds.
- Missing URLs fall back to Open-Meteo defaults.

## Error Handling Model
- External request timeout -> weather client raises `WeatherClientError`.
- Upstream HTTP errors -> weather client raises `WeatherClientError`.
- Malformed upstream payload -> weather client raises `WeatherClientError`.
- `/greet` catches weather errors and returns `weather_error` while keeping request `200`.
