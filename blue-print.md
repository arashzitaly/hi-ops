here is the AGENTS.md I created my own


# AGENTS.md — hello_ops

## 1) Project overview (what + why)

**hello_ops** is a learning-first repository to build a small Python API and progressively add DevOps practices **in controlled phases**. Each phase introduces one new concept (testing, CI quality gates, external calls, containers, Terraform, Kubernetes, observability) without jumping to production-complete complexity.

**Core principle:** incremental change + understanding "why" behind each choice.  
**Non-goal:** a production-ready platform. Anything "production-grade" must be explicitly requested later.

---

## 2) Current phase and scope boundaries

**CURRENT PHASE:** Phase 1 — Minimal API + CI

**What you can build right now:**
- FastAPI app with one "Hello World" endpoint
- One pytest test for the endpoint
- GitHub Actions CI with lint/format/test jobs
- Basic README documentation

**What you CANNOT build yet (even if I ask):**
- Multiple endpoints (wait for Phase 2)
- Query parameters or request validation (wait for Phase 2)
- External API calls (wait for Phase 3)
- Docker containers (wait for Phase 4)
- Any infrastructure (wait for Phase 5+)

**If I ask for something out of scope:** Politely remind me which phase it belongs to and suggest I explicitly request moving to that phase first.

---

## 3) Execution rules (MUST follow)

### Rule 1: One concept per PR
- Each PR adds ONE new capability
- Example: "Add health endpoint" is one PR, not "Add health + logging + metrics"
- If I ask for multiple things, break them into separate PRs

### Rule 2: Tests are mandatory
- Every new endpoint needs at least one test
- Every new function needs at least one test
- Tests must validate behavior, not just happy paths
  - Example: test missing required params, invalid inputs, timeout scenarios

### Rule 3: Document decisions
- For each phase, create or update a **DECISIONS.md** file
- Document:
  - Why you chose each tool/approach
  - What alternatives you considered
  - What you're explicitly deferring and why
- Example: "Chose pytest over unittest because of simpler fixture management and better parametrization support"

### Rule 4: Stable naming for CI
- CI job names must be stable across changes: `lint`, `format`, `test`
- These names will be used in branch protection rules
- Don't rename jobs unless explicitly asked

### Rule 5: No secrets in code
- Use environment variables for configuration
- Use `.env.example` to document required vars
- Never commit real API keys, tokens, or credentials

### Rule 6: Minimize dependencies
- Only add dependencies actually needed for current phase
- Document why each new dependency is required
- Prefer standard library when reasonable

---

## 4) Repository structure (tree) + phase additions

Target structure over time:

```text
hello_ops/
├── AGENTS.md                    # This file
├── README.md                    # Project roadmap
├── DECISIONS.md                 # Per-phase decision log
├── requirements.txt             # Python dependencies
├── .gitignore
├── .env.example                 # Phase 3+
├── app/
│   ├── __init__.py
│   ├── main.py                  # Phase 1: minimal FastAPI app
│   ├── config.py                # Phase 3: env var handling
│   ├── services/
│   │   ├── __init__.py
│   │   └── weather.py           # Phase 3: external API client
│   └── metrics.py               # Phase 7: Prometheus metrics
├── tests/
│   ├── __init__.py
│   ├── test_main.py             # Phase 1: root endpoint test
│   └── test_weather.py          # Phase 3: weather service tests
├── .github/
│   └── workflows/
│       └── ci.yml               # Phase 1: lint/format/test jobs
├── Dockerfile                   # Phase 4: container build
├── .dockerignore                # Phase 4: build exclusions
├── infra/
│   └── terraform/               # Phase 5: learning-grade IaC
│       ├── README.md
│       ├── versions.tf
│       ├── providers.tf
│       ├── variables.tf
│       ├── outputs.tf
│       └── main.tf
└── deploy/
    └── k8s/                     # Phase 6: dev-grade K8s
        ├── README.md
        ├── deployment.yaml
        ├── service.yaml
        ├── hpa.yaml             # Phase 6: horizontal pod autoscaler
        ├── configmap.yaml
        ├── secret.yaml          # placeholder refs only
        ├── prometheus/          # Phase 7: metrics collection
        │   └── prometheus.yaml
        └── grafana/             # Phase 7: dashboards
            └── dashboard.json
```

---

## 5) Phase-by-phase build instructions

### Phase 1 — Minimal API + CI

**Files to create:**
- `app/main.py` — FastAPI app with one `GET /` endpoint returning `{"message": "Hello, World!"}`
- `tests/test_main.py` — One pytest test validating the endpoint response
- `requirements.txt` — fastapi, uvicorn, pytest, httpx
- `.github/workflows/ci.yml` — Three jobs: `lint`, `format`, `test`
- `DECISIONS.md` — Document tool choices (FastAPI vs Flask, pytest vs unittest, ruff vs pylint)

**What to test:**
- Root endpoint returns 200 status
- Response body matches expected JSON

**CI jobs:**
- `lint` — Run ruff check
- `format` — Run ruff format --check
- `test` — Run pytest -v

**Success criteria:**
- CI passes on all jobs
- Test coverage includes the endpoint
- DECISIONS.md explains why FastAPI and pytest

### Phase 2 — API parameters + quality gates

**Files to create/modify:**
- `app/main.py` — Add `GET /greet?name=...` endpoint with required query param
- `app/main.py` — Add `GET /health` endpoint returning `{"status": "ok"}`
- Add basic request logging (Python logging module)
- `tests/test_main.py` — Tests for valid name, missing name (422 error), health endpoint
- Update `DECISIONS.md` — Document branch protection approach

**What to test:**
- Valid name parameter returns greeting
- Missing name parameter returns 422
- Health endpoint returns 200

**CI requirement:**
- All three jobs (`lint`, `format`, `test`) must pass before merge
- Document how to configure branch protection in README

**Success criteria:**
- CI job names are stable
- Tests cover both happy and error paths
- DECISIONS.md explains branch protection strategy

### Phase 3 — Optional params + external API

**Files to create/modify:**
- `app/config.py` — Load env vars (WEATHER_API_KEY, etc.)
- `app/services/weather.py` — Weather API client with timeout and error handling
- `app/main.py` — Modify endpoint to accept name (required), surname (required), phone (optional), city (optional)
- If city provided, call weather service
- `tests/test_weather.py` — Mock weather API calls
- `.env.example` — Document required env vars
- Update `DECISIONS.md` — Document API choice, timeout values, mock strategy

**What to test:**
- Required params validation
- Optional params work when provided/omitted
- Weather service timeout handling
- Weather service error responses
- Mocked external calls (don't hit real API in tests)

**Success criteria:**
- No secrets in code
- External calls have timeouts
- Tests use mocks/fixtures
- DECISIONS.md explains timeout choice and mock approach

### Phase 4 — Containerization

**Files to create:**
- `Dockerfile` — Multi-stage build with Python 3.11
- `.dockerignore` — Exclude tests, .git, __pycache__, etc.
- Update README with docker build and run instructions
- (Optional) Add CI job to build image
- Update `DECISIONS.md` — Document base image choice, multi-stage rationale

**What to document:**
```bash
# Build
docker build -t hello-ops:latest .

# Run
docker run -p 8000:8000 hello-ops:latest
```

**Success criteria:**
- Image builds successfully
- Container runs and serves traffic
- .dockerignore excludes dev files
- DECISIONS.md explains image choices

### Phase 5 — Terraform IaC (learning scope)

**Files to create:**
- `infra/terraform/README.md` — How to init/plan/apply/destroy
- `infra/terraform/versions.tf` — Terraform and provider versions
- `infra/terraform/providers.tf` — AWS provider config
- `infra/terraform/variables.tf` — Input variables with descriptions
- `infra/terraform/outputs.tf` — Resource outputs
- `infra/terraform/main.tf` — VPC, subnets, ECR (learning-grade only)
- Update `DECISIONS.md` — Document resource choices, cost notes, what's deferred

**What to build (learning-grade):**
- VPC with 2 public subnets
- ECR repository for container images
- Basic networking (no NAT gateway, no production security)

**What NOT to build:**
- Production-grade networking (NAT, private subnets)
- IAM roles/policies (unless explicitly requested)
- RDS, ECS, EKS (wrong phase)

**Success criteria:**
- Can run `terraform plan` and `terraform apply`
- Resources are namespaced (e.g., prefix with project name)
- DECISIONS.md documents cost trade-offs

### Phase 6 — Kubernetes deployment (dev-grade)

**Files to create:**
- `deploy/k8s/README.md` — How to apply manifests
- `deploy/k8s/deployment.yaml` — Pod spec with resource limits
- `deploy/k8s/service.yaml` — ClusterIP or LoadBalancer
- `deploy/k8s/configmap.yaml` — Non-sensitive config
- `deploy/k8s/secret.yaml` — Placeholder for sensitive config (no real secrets)
- `deploy/k8s/hpa.yaml` — Horizontal Pod Autoscaler (if appropriate)
- Update `DECISIONS.md` — Document K8s choices, break/fix drill results

**What to test:**
- Deploy to local K8s (minikube, kind, Docker Desktop)
- Run one controlled break/fix drill:
  - Example: Delete pod, observe recreation
  - Example: Scale to zero, observe behavior
  - Document recovery steps

**Success criteria:**
- Manifests apply without errors
- Service is reachable
- Break/fix drill documented in DECISIONS.md

### Phase 7 — Observability (metrics + dashboards)

**Files to create/modify:**
- `app/metrics.py` — Prometheus metrics endpoint
- `app/main.py` — Integrate metrics middleware
- `deploy/k8s/prometheus/prometheus.yaml` — Scrape config (dev-only)
- `deploy/k8s/grafana/dashboard.json` — Dashboard export
- Update `DECISIONS.md` — Document metrics choices, production gaps

**What to build:**
- `/metrics` endpoint exposing Prometheus format
- Basic metrics: request count, latency, error rate
- Grafana dashboard with 2-3 panels
- Simple alert examples (documentation only)

**Production-readiness gap checklist:**
- ✅ Done: metrics exposed, dashboard exists
- ⏸ Deferred: alerting integration, on-call runbooks
- ❌ Out of scope: multi-region observability, long-term storage

**Success criteria:**
- Metrics endpoint returns data
- Dashboard can be imported to Grafana
- DECISIONS.md includes gap analysis

---

## 6) How to respond to requests

### If I ask for something in the current phase:
✅ Build it following the execution rules above

### If I ask for something in a future phase:
❌ **Don't build it yet.** Instead, say:

> "That feature is part of Phase X. We're currently in Phase Y. Would you like to:
> 1. Finish Phase Y first, or
> 2. Explicitly move to Phase X now?"

### If I ask for production-grade complexity:
❌ **Don't build it unless I explicitly request it.** Instead, say:

> "That's a production-grade feature. The current scope is learning-grade. Would you like me to:
> 1. Build a simplified learning version, or
> 2. Build the full production version (and document why)?"

### If I ask for multiple things at once:
🔀 **Break them into separate PRs.** Say:

> "I can build that in X separate PRs:
> 1. PR 1: [feature A]
> 2. PR 2: [feature B]
> 3. PR 3: [feature C]
> 
> Should I start with PR 1?"

---

## 7) Agent collaboration scenarios (for learning)

For each phase, consider these collaboration questions:

**Phase 1:** "If three teammates were setting up CI simultaneously, how would we prevent duplicated effort or conflicting configurations?"

**Phase 2:** "If two engineers add different endpoints with validation, how do we ensure consistent error handling?"

**Phase 3:** "If the weather API key needs to rotate, how would we coordinate secret updates across environments?"

**Phase 4:** "If two teams build containers from the same base image, how do we handle base image updates?"

**Phase 5:** "If multiple engineers run `terraform apply` concurrently, what breaks and how do we prevent it?"

**Phase 6:** "If two deployments happen simultaneously, how does K8s handle rollout conflicts?"

**Phase 7:** "If alerts fire for three different services, how do we correlate them to a single root cause?"

These questions help build operational thinking even in solo learning environments.

---

## 8) Tool choices and rationale (default stack)

| Layer | Tool | Why |
|-------|------|-----|
| **API** | FastAPI | Async support, automatic OpenAPI docs, modern Python |
| **Testing** | pytest | Better fixtures, parametrization, plugin ecosystem |
| **Linting** | ruff | Fast, replaces multiple tools (flake8, isort, etc.) |
| **CI** | GitHub Actions | Native GitHub integration, free for public repos |
| **Containers** | Docker | Industry standard, wide support |
| **IaC** | Terraform | Cloud-agnostic, large community, mature |
| **Orchestration** | Kubernetes | Industry standard for container orchestration |
| **Metrics** | Prometheus | De facto standard for metrics, K8s native |
| **Dashboards** | Grafana | Widely used, integrates with Prometheus |

**Can I change these?** Yes, but document why in DECISIONS.md.

---

## 9) Red flags (what not to do)

🚫 **Don't add features from future phases** without explicit approval  
🚫 **Don't skip tests** ("I'll add them later" is not allowed)  
🚫 **Don't commit secrets** (use env vars and .env.example)  
🚫 **Don't write "TODO" comments** without GitHub issues to track them  
🚫 **Don't add dependencies** without documenting why in DECISIONS.md  
🚫 **Don't build "production-grade" features** unless explicitly requested  
🚫 **Don't rename CI jobs** (they're referenced in branch protection)  
🚫 **Don't make decisions without documenting rationale**  

---

## 10) Success metrics

After each phase, validate:

- ✅ **CI passes** — All jobs green
- ✅ **Tests exist** — Coverage includes new code
- ✅ **Decisions documented** — DECISIONS.md updated
- ✅ **Scope respected** — No future-phase features leaked in
- ✅ **Collaboration question answered** — Operational thinking captured
- ✅ **README updated** — Instructions for running new features

If all six checkboxes pass, the phase is complete.

---

## 11) Quick reference card

```text
┌─────────────────────────────────────────────────────────────┐
│ PHASE GATE CHECKLIST                                        │
├─────────────────────────────────────────────────────────────┤
│ Before moving to next phase:                                │
│                                                              │
│ □ All CI jobs pass (lint, format, test)                     │
│ □ Tests cover new functionality (happy + error paths)       │
│ □ DECISIONS.md updated with tool choices and rationale      │
│ □ No future-phase features included                         │
│ □ Collaboration scenario answered                           │
│ □ README updated with usage instructions                    │
│ □ No secrets committed                                      │
│ □ Dependencies documented                                   │
│                                                              │
│ Phase incomplete until ALL boxes checked.                   │
└─────────────────────────────────────────────────────────────┘
```
