# Decisions

## Phase 1 - Minimal API + CI

### API framework
- Decision: Use FastAPI for the initial `GET /` endpoint.
- Why: Lightweight setup for a small API and natural path for later async and validation features in future phases.
- Alternative considered: Flask. It is also valid, but FastAPI gives stronger typing and request/response ergonomics for upcoming phases.
- Deferred: No extra endpoints, parameter handling, or external integrations in this phase.

### Test framework
- Decision: Use `pytest`.
- Why: Simple tests with clear assertions and easy scaling to fixtures/mocks in later phases.
- Alternative considered: `unittest`. It is standard library, but more verbose for this learning roadmap.
- Deferred: Broader edge-case suites and integration tests until features are added in Phase 2+.

### Lint and format
- Decision: Use `ruff` for linting and formatting checks.
- Why: Single fast tool for quality gates with low configuration overhead.
- Alternative considered: `pylint` plus separate formatter tooling.
- Deferred: Custom rule tuning; defaults are enough for Phase 1.

### Dependencies added and rationale
- `fastapi`: API framework for the service.
- `uvicorn`: ASGI server for local runtime.
- `pytest`: test runner.
- `httpx`: HTTP client dependency used by FastAPI testing stack.
- `ruff`: lint and format checks in CI.

### Collaboration scenario (Phase 1)
- Question: If three teammates were setting up CI simultaneously, how do we avoid conflicting configs?
- Answer:
  - Assign one owner for `.github/workflows/ci.yml` changes per task.
  - Keep job names stable (`lint`, `format`, `test`) and treat them as API contracts for branch protection.
  - Require PR review for workflow changes and avoid parallel edits to the same workflow in separate PRs.

## Phase 2 - API Parameters + Quality Gates

### API endpoints and parameter handling
- Decision: Add `GET /greet` with required query parameter `name` and add `GET /health` returning `{"status": "ok"}`.
- Why: Introduces parameterized request handling and a basic health endpoint while keeping the API simple for incremental learning.
- Alternative considered: Make `name` optional with a default response (for example, `"Hello, World!"`), but this would skip explicit validation behavior needed in this phase.
- Deferred: Additional endpoints, request body models, and custom response schemas.

### Validation strategy
- Decision: Use FastAPI's built-in query validation for missing required parameters and accept the default `422` validation response.
- Why: Keeps validation logic concise and consistent with framework defaults.
- Alternative considered: Manual validation in endpoint logic with custom `400` responses.
- Deferred: Custom exception handlers and standardized error payloads.

### Request logging approach
- Decision: Add minimal HTTP middleware logging (`method`, `path`, `status_code`) using Python's built-in `logging` module.
- Why: Provides immediate request visibility with minimal complexity and no added dependencies.
- Alternative considered: Add a structured logging dependency or rely only on server-level access logs.
- Deferred: Correlation IDs, JSON logs, and environment-driven log configuration.

### Test coverage for new behavior
- Decision: Add tests for `/greet` happy path, `/greet` missing `name` (expect `422`), and `/health`.
- Why: Keeps tests behavior-focused and aligns with the rule that each new behavior should be covered.
- Alternative considered: Only testing happy paths, which would miss validation behavior.
- Deferred: Dedicated contract tests and warning cleanup work outside core Phase 2 scope.

### Dependencies added in Phase 2
- Decision: Add no new dependencies.
- Why: Existing stack (`fastapi`, `pytest`, `ruff`) already supports this phase's goals.
- Alternative considered: Introduce additional logging or validation helper libraries.
- Deferred: Re-evaluate dependencies only when Phase 3 introduces external API integration.
