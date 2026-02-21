# DECISIONS

## Phase 1 - Minimal API + CI

### Decision: FastAPI for the starter API
- Why: simple route definitions, built-in validation, and a path to async features.
- Alternative considered: Flask.
- Trade-off: FastAPI adds type-driven conventions earlier, but this is useful for learning.

### Decision: pytest for tests
- Why: compact test syntax, fixtures, and strong ecosystem support.
- Alternative considered: unittest.
- Trade-off: one extra dependency, but better readability and faster iteration.

### Decision: ruff for lint + format
- Why: one fast tool for linting and formatting in CI.
- Alternative considered: separate flake8 + black + isort.
- Trade-off: fewer knobs than combining many tools, but lower complexity for this repo.

## Phase 2 - Parameters + quality gates

### Decision: add `/greet` and `/health` first
- Why: introduces validation and operational checks without large scope increase.
- Alternative considered: adding multiple feature endpoints at once.
- Trade-off: slower feature breadth, better reviewability.

### Decision: keep CI job names stable (`lint`, `format`, `test`)
- Why: predictable branch protection and less CI churn.
- Alternative considered: phase-specific job renames.
- Trade-off: less naming flexibility, better long-term consistency.

### Decision: minimal request logging middleware
- Why: capture method/path/status for basic debugging.
- Alternative considered: postpone logging until observability phase.
- Trade-off: very basic logs now, richer telemetry later in Phase 7.

## Phase 3 - Optional params + external weather API

### Decision: use Open-Meteo public endpoints without API key
- Why: no secret handling needed for learning-grade weather integration.
- Alternative considered: providers requiring API keys.
- Trade-off: fewer auth/secret lessons now, simpler onboarding and safer defaults.

### Decision: two-step weather lookup (geocoding then forecast)
- Why: city name must be resolved to latitude/longitude before forecast query.
- Alternative considered: direct city-to-forecast provider.
- Trade-off: two network calls instead of one, but clearer error boundaries.

### Decision: timeout from env with safe default (`WEATHER_TIMEOUT_SECONDS=3.0`)
- Why: adjustable behavior per environment with sensible fallback.
- Alternative considered: hard-coded timeout.
- Trade-off: slight config complexity, better operational control.

### Decision: degrade gracefully on weather failure
- Why: `/greet` still succeeds and returns `weather_error` when weather lookup fails.
- Alternative considered: fail the whole request with 5xx.
- Trade-off: partial response instead of hard failure, better user-facing resilience.

### Decision: mock external calls in tests
- Why: deterministic tests that do not depend on network/provider uptime.
- Alternative considered: only live integration tests.
- Trade-off: mocks require maintenance, but CI remains reliable and fast.

### Deferred (explicitly out of current scope)
- Retries with backoff and circuit breaker behavior.
- Response caching for repeated city lookups.
- Stronger typed response models for weather payload.
- Separate integration test environment with scheduled live checks.
