# Testing and CI

## Local Quality Commands
```bash
python3 -m ruff check .
python3 -m ruff format --check .
python3 -m pytest -v
```

## Test Coverage Focus
- Endpoint behavior for `/`, `/health`, `/greet`.
- Validation behavior for missing required query params.
- Weather integration behavior using mocked external calls.
- Error paths: timeout, upstream HTTP status errors, malformed forecast payload.

## CI Workflow
File: `.github/workflows/ci.yml`

Stable required jobs:
- `lint`
- `format`
- `test`

Additional workflow-dispatch smoke job:
- `weather_smoke`
- Starts API, hits `/health`, then hits `/greet` with `city`.
- Verifies response contains either `weather` or `weather_error`.

## Branch Protection Guidance
- Require `lint`, `format`, and `test` before merge.
- Keep job names stable to avoid protection rule drift.
