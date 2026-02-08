# hello_ops
## Project goal
Build a small Python API and **learn DevOps step-by-step**: testing, CI/CD,
containers, Terraform IaC, Kubernetes, autoscaling, and observability. The focus
is **manual learning** (no production-complete stacks unless explicitly asked).
Each phase is small so a junior engineer can understand the “why” behind every
tool and decision.
## Core principles
- Learn incrementally: add one major concept at a time with small, reviewable PRs.
- Why before how: document decision rationale, not only implementation steps.
- Build and operate: include basic checks/tests and operational visibility as you go.
- Keep scope intentional: stay learning-grade by default and explicitly note deferred production items.
## Learning phases (extended)
Below is a simple phase map from entry-level to mid-junior/early-senior topics.
Each phase includes **what you build** and **what you learn**. Keep PRs small and
reviewable.
### Phase 1 — Minimal API + CI
**Build**
- A tiny FastAPI app with one “Hello World” endpoint.
- One pytest test.
- GitHub Actions CI for lint/format + tests.
**Learn**
- Basic Python project structure.
- FastAPI basics.
- CI fundamentals and quality gates.
### Phase 2 — API parameters + quality gates
**Build**
- Add a required query parameter (e.g., name).
- Tests for valid and missing inputs.
- Stable CI job names to use in branch protection.
- Add a basic health endpoint and simple request logging.
**Learn**
- Validation and request handling.
- CI checks as a merge gate.
- Branch protection basics.
- Early observability habits for debugging and service checks.
### Phase 3 — Optional params + external API
**Build**
- Required params: name, surname.
- Optional params: phone, city.
- Weather lookup if city is provided (mocked in tests).
- Secure config via environment variables.
**Learn**
- Optional vs. required inputs.
- External API calls with timeouts and error handling.
- Secrets management and mocking.
### Phase 4 — Containerization
**Build**
- Dockerfile and .dockerignore.
- Local docker build + docker run instructions in README.
- (Optional) CI job to build the image.
**Learn**
- Packaging an app into a container.
- Image build basics and reproducibility.
- How CI validates a container build.
### Phase 5 — Terraform IaC (learning scope)
**Build**
- infra/terraform/ with small, **non-production** examples.
- Minimal network primitives (VPC/subnets) and a container registry (ECR).
- Documentation on variables and how to plan/apply/destroy locally.
- Add short notes on cost and complexity trade-offs for chosen resources.
**Learn**
- Terraform structure, modules, and state.
- Safe resource provisioning.
- Infrastructure change review workflow (plan/apply/destroy).
- Practical cost-awareness for infrastructure choices.
### Phase 6 — Kubernetes deployment (dev-grade)
**Build**
- deploy/k8s/ manifests: Deployment + Service (no production ingress yet).
- Config/Secret references (no real secrets in repo).
- Basic autoscaling (HPA) if appropriate.
- Run one controlled break/fix drill and document recovery steps.
**Learn**
- Core Kubernetes objects and service exposure.
- Config and secret management.
- Basic scaling principles.
- Troubleshooting and recovery basics.
### Phase 7 — Observability (metrics + dashboards)
**Build**
- Add a metrics endpoint to the app (e.g., Prometheus format).
- Prometheus scrape config (dev-only).
- Grafana dashboard JSON export.
- Simple alert examples (latency/error rate).
- Add a short production-readiness gap checklist: done / deferred / out-of-scope.
**Learn**
- Metrics-driven visibility.
- Dashboards for quick health checks.
- Foundations of alerting and SLO thinking.
- Clear separation between learning-grade and production-grade scope.
## How to use this roadmap
- Keep each phase small and reviewable (tiny PRs).
- Write at least one meaningful test per phase.
- Use CI as a guardrail (lint + tests).
- Document the “why” behind each change in README.
- Add a brief **Decisions & Trade-offs** note for each phase.

## Implemented status (through Phase 3)
- Phase 1 completed:
  - FastAPI app with `GET /`
  - CI workflow with stable job names: `lint`, `format`, `test`
  - Initial pytest coverage
- Phase 2 completed:
  - `GET /greet` with required query parameter `name`
  - `GET /health` returning `{"status": "ok"}`
  - Minimal request logging middleware (`method`, `path`, `status_code`)
  - Tests for happy path and validation behavior (`422` on missing `name`)
- Phase 3 completed:
  - `GET /greet` now requires `name` and `surname`
  - Optional query parameters: `phone`, `city`
  - Weather lookup for `city` using an external API client with timeout/error handling
  - Environment-variable-based weather client configuration
  - Mocked tests for weather success and failure behavior

## Quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```

Weather environment variables (optional for local testing; required for live weather calls):
```bash
cp .env.example .env
export WEATHER_API_BASE_URL="https://api.openweathermap.org/data/2.5/weather"
export WEATHER_API_KEY="replace-with-your-api-key"
export WEATHER_TIMEOUT_SECONDS="3.0"
```

Run locally:
```bash
python3 -m uvicorn app.main:app --reload
```

Quality checks:
```bash
python3 -m ruff check .
python3 -m ruff format --check .
python3 -m pytest -v
```

## API behavior (current)
`GET /`:
```bash
curl http://127.0.0.1:8000/
# {"message":"Hello, World!"}
```

`GET /greet?name=Arash&surname=Karimi`:
```bash
curl "http://127.0.0.1:8000/greet?name=Arash&surname=Karimi"
# {"message":"Hello, Arash Karimi!"}
```

`GET /greet?name=Arash&surname=Karimi&phone=555-0101`:
```bash
curl "http://127.0.0.1:8000/greet?name=Arash&surname=Karimi&phone=555-0101"
# {"message":"Hello, Arash Karimi!","phone":"555-0101"}
```

`GET /greet?name=Arash&surname=Karimi&city=Tehran`:
```bash
curl "http://127.0.0.1:8000/greet?name=Arash&surname=Karimi&city=Tehran"
# {"message":"Hello, Arash Karimi!","city":"Tehran","weather":{"description":"...","temperature_c":...}}
```

`GET /greet` (missing required query parameters):
```bash
curl "http://127.0.0.1:8000/greet?name=Arash"
# HTTP 422 Unprocessable Entity (missing `surname`)
```

`GET /health`:
```bash
curl http://127.0.0.1:8000/health
# {"status":"ok"}
```

## Tests currently in repo
- `test_root_returns_hello_world`
- `test_greet_happy_path`
- `test_greet_missing_name_returns_422`
- `test_greet_missing_surname_returns_422`
- `test_greet_with_phone_returns_phone`
- `test_greet_with_city_returns_weather`
- `test_greet_with_city_handles_weather_failure`
- `test_health_returns_ok`
- `test_get_weather_returns_description_and_temperature`
- `test_get_weather_requires_api_key`
- `test_get_weather_timeout_raises_client_error`
