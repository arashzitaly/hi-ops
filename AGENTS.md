# AGENTS.md — hello_ops

## 1) Project overview (what + why)

**hello_ops** is a learning-first repository to build a small Python API and progressively add DevOps practices **in controlled phases**. Each phase introduces one new concept (testing, CI quality gates, external calls, containers, Terraform, Kubernetes, observability) without jumping to production-complete complexity.

**Core principle:** incremental change + understanding "why" behind each choice.  
**Non-goal:** a production-ready platform. Anything "production-grade" must be explicitly requested later.

---

## 2) Code vs Coach: How Codex must behave

### 🤖 CODEX SHOULD CODE (Pair Programmer Mode)
Application logic that is not the core DevOps learning goal:
- FastAPI endpoint implementation (request/response handling)
- Business logic functions (formatting, small transformations)
- Python utility helpers
- Pydantic models (schemas, constraints)
- Error handling patterns inside application code
- External API client implementation (Phase 3)
- Small refactors for clarity (no architecture rewrite)

**Default output style:** file list + diffs; minimal changes; include “how to test”.

### 👨‍🏫 CODEX SHOULD COACH (Teaching Mode)
DevOps and operational topics you must do hands-on:
- **CI/CD config** (GitHub Actions workflow content + job design)
- **Dockerfile** (you write it; Codex provides skeleton + rationale)
- **Terraform** (you write HCL; Codex explains blocks + provides skeleton)
- **Kubernetes manifests** (you write YAML; Codex explains objects + provides skeleton)
- **Branch protection** (Codex explains; you configure in GitHub UI)
- **Observability wiring** (Prometheus/Grafana configs: you write; Codex guides)

**Coaching protocol (mandatory for DevOps work):**
1) Explain concept + trade-offs (short)
2) Provide a skeleton with TODO markers
3) Ask you to fill the TODOs
4) Review your result and propose improvements
5) Stop and request outputs (logs/CI run/plan output) before continuing

**Exception:** If you explicitly say: “I’m stuck, show me the full solution,” Codex can provide a complete example plus explanation.

---

## 3) Current phase and scope boundaries

**CURRENT PHASE:** Phase 1 — Minimal API + CI

**What you can build right now:**
- FastAPI app with one “Hello World” endpoint
- One pytest test for the endpoint
- GitHub Actions CI with stable job names (`lint`, `format`, `test`)
- Basic README documentation

**What you must NOT build yet unless I explicitly move to that phase:**
- Multiple endpoints (Phase 2)
- Query parameters or request validation (Phase 2)
- External API calls (Phase 3)
- Docker containers (Phase 4)
- Any infrastructure (Phase 5+)

**If I ask for something out of scope:** remind me which phase it belongs to and ask whether to move phases now.

---

## 4) Execution rules (MUST follow)

### Rule 0: Code vs Coach (Meta rule)
- **App code:** Codex can implement.
- **DevOps config:** Codex must coach (skeleton + guidance), unless I explicitly request full solution after trying.

### Rule 1: One concept per PR
- Each PR adds ONE new capability.
- If multiple requests arrive, split into multiple PRs.

### Rule 2: Tests are mandatory (behavior-based)
- Every new endpoint must have at least one test.
- Every new **behavior** must be covered (happy + at least one failure path when relevant).
- Do NOT create a “test per function” rule; focus on behavior coverage.

### Rule 3: Document decisions
Maintain `DECISIONS.md` as a per-phase decision log:
- Decision taken
- Alternatives considered
- Why (trade-offs)
- Deferred production items

### Rule 4: Stable naming for CI
CI job names must remain stable: `lint`, `format`, `test`.

### Rule 5: No secrets in code
- Use environment variables for config.
- Use `.env.example` only when needed (Phase 3+).
- Never commit real keys/tokens.

### Rule 6: Minimize dependencies
- Add only what the current phase needs.
- Document why each new dependency exists.

---

## 5) Repository structure (target)
This is the intended shape over time (do not create future-phase files early).

```text
hello_ops/
├── AGENTS.md
├── README.md
├── DECISIONS.md
├── requirements.txt               # or pyproject.toml (choose one and stick to it)
├── .gitignore
├── .env.example                   # Phase 3+
├── app/
│   ├── __init__.py
│   ├── main.py                    # Phase 1
│   ├── config.py                  # Phase 3
│   ├── services/
│   │   ├── __init__.py
│   │   └── weather.py             # Phase 3
│   └── metrics.py                 # Phase 7
├── tests/
│   ├── __init__.py
│   ├── test_main.py               # Phase 1+
│   └── test_weather.py            # Phase 3
├── .github/
│   └── workflows/
│       └── ci.yml                 # Phase 1
├── Dockerfile                     # Phase 4
├── .dockerignore                  # Phase 4
├── infra/
│   └── terraform/                 # Phase 5
└── deploy/
    └── k8s/                       # Phase 6+
