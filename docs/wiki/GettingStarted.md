# Getting Started

## Prerequisites
- Python 3.11+ recommended
- `pip`

## Setup
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

## Optional Weather Environment Variables
```bash
export WEATHER_GEOCODING_BASE_URL="https://geocoding-api.open-meteo.com/v1/search"
export WEATHER_FORECAST_BASE_URL="https://api.open-meteo.com/v1/forecast"
export WEATHER_TIMEOUT_SECONDS="3.0"
```

Notes:
- If not set, the app uses built-in defaults.
- Open-Meteo public endpoints used here do not require an API key.

## Run the API
```bash
python3 -m uvicorn app.main:app --reload
```

## Quick Smoke Check
```bash
curl http://127.0.0.1:8000/
curl http://127.0.0.1:8000/health
curl "http://127.0.0.1:8000/greet?name=Arash&surname=Karimi"
```

## Troubleshooting
- Import errors for `httpx`/`fastapi`: run `python -m pip install -r requirements.txt` in the active environment.
- Port in use on `8000`: run with `--port 8001` and call that port instead.
