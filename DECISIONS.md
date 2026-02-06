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
