# Operations Notes

## Runtime Behavior
- The service logs request `method`, `path`, and `status_code`.
- `/health` is the primary liveness check endpoint.

## Config Changes
- Weather behavior is controlled through env vars: `WEATHER_GEOCODING_BASE_URL`, `WEATHER_FORECAST_BASE_URL`, `WEATHER_TIMEOUT_SECONDS`.

## Failure Modes
- Weather provider timeout.
- Weather provider non-200 HTTP response.
- Weather provider payload format mismatch.

Current behavior on weather failure:
- `/greet` still returns `200` with base greeting fields.
- Adds `weather_error` instead of failing full request.

## Safe Change Checklist
1. Update config and docs together.
2. Keep tests deterministic; mock external calls.
3. Run `ruff` + `pytest` before merge.
4. Verify `weather_smoke` for integration confidence.

## Known Deferrals
- Retry/backoff policy.
- Caching for repeated city lookups.
- Full observability stack (metrics dashboards/alerts).
