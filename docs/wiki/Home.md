# hello_ops Wiki

This wiki is the project representation for `hello_ops`, organized like a classic code wiki.

## Quick Links
- [Getting Started](./GettingStarted.md)
- [Architecture](./Architecture.md)
- [API Reference](./ApiReference.md)
- [Testing and CI](./TestingAndCI.md)
- [Roadmap](./Roadmap.md)
- [Operations Notes](./Operations.md)
- [Decisions and Trade-offs](../../DECISIONS.md)

## Project Snapshot
- Goal: learn DevOps incrementally through a small Python API.
- Current implemented status: through Phase 3.
- Stack: FastAPI, pytest, Ruff, GitHub Actions.
- External integration: Open-Meteo weather APIs via geocoding + forecast.

## Current Capabilities
- `GET /` returns Hello World.
- `GET /health` returns service health.
- `GET /greet` requires `name` and `surname`.
- `GET /greet` optionally accepts `phone` and `city`.
- `GET /greet` adds weather data when `city` is provided.

## Scope Boundary
- In scope now: API behavior and CI quality gates through Phase 3.
- Deferred to later phases: containers, Terraform, Kubernetes, observability stack.

## How to Use This Wiki
1. Start at [Getting Started](./GettingStarted.md) to run locally.
2. Use [API Reference](./ApiReference.md) for endpoint behavior.
3. Use [Testing and CI](./TestingAndCI.md) for checks and pipeline behavior.
4. Use [Roadmap](./Roadmap.md) to plan next phase work.
