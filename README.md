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

## Phase 1 quickstart
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run locally:
```bash
uvicorn app.main:app --reload
```

Quality checks:
```bash
ruff check .
ruff format --check .
pytest -v
```

Endpoint response:
```bash
curl http://127.0.0.1:8000/
# {"message":"Hello, World!"}
```
