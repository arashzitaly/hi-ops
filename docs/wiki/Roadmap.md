# Roadmap

## Implemented
- Phase 1: Minimal API + CI
- Phase 2: Required params + health + logging
- Phase 3: Optional params + weather external integration

## Next Phases

### Phase 4 - Containerization
- Add `Dockerfile` and `.dockerignore`.
- Add run/build docs.

### Phase 5 - Terraform IaC (learning scope)
- Add `infra/terraform/` with minimal learning resources.
- Document `plan/apply/destroy` workflow.

### Phase 6 - Kubernetes deployment (dev-grade)
- Add `deploy/k8s/` manifests (Deployment/Service/config refs).
- Document one break/fix drill.

### Phase 7 - Observability
- Add metrics endpoint and scrape config.
- Add basic Grafana dashboard and alert examples.

## Phase Gates
- Tests added for each new capability.
- CI passes (`lint`, `format`, `test`).
- Decisions documented in `DECISIONS.md`.
- README/wiki updated with runnable usage.
