# Workspace Architecture

## Overview
The `workspace` repository serves as the centralized integration and orchestration hub for the entire VIREON ecosystem. In order to keep component repositories (`vireon`, `vireon-lab`, `neurodsl`) decoupled and focused strictly on their respective domains, the workspace assumes full responsibility for cross-repository concerns.

## Core Responsibilities

The workspace **ONLY** owns the following responsibilities. Any responsibility not explicitly listed here belongs in a component repository or the global `.github` governance repository.

1. **Integration Tests:** Cross-boundary tests that validate the interaction between the runtime, SDK, and DSL.
2. **Compatibility Testing:** Ensuring that specific versions of `neurodsl` correctly interface with different versions of the `vireon` runtime.
3. **Contract Tests:** Validating API stability and schema contracts across ecosystem boundaries.
4. **Example Deployments:** Reference architectures and deployments that span multiple components.
5. **Docker Compose:** The canonical `docker-compose.yml` that orchestrates the full ecosystem for local development and testing.
6. **Benchmark Orchestration:** Running end-to-end performance benchmarks that measure the overhead of the integrated system.
7. **Cross-repository CI:** CI pipelines that trigger across repository boundaries (e.g., testing `vireon` changes against `vireon-lab` downstream dependencies).
8. **Dependency Locking:** Managing ecosystem-wide lockfiles where global dependency consistency is required.
9. **Version Matrix:** The single source of truth for which versions of which components are known to work together.
10. **Release Validation:** Final stage verification before tagging an ecosystem-wide release.

## Directory Structure (Proposed)

```text
workspace/
├── docker-compose.yml       # Canonical ecosystem deployment
├── INTEGRATION.md           # Integration architecture & compatibility 
├── tests/
│   ├── integration/         # Cross-repo integration tests
│   ├── contract/            # Interface validation
│   └── compatibility/       # Version matrix tests
├── benchmarks/              # End-to-end benchmark orchestration
└── deployments/             # Example full-system deployments
```

## Guiding Principles

- **Zero Core Logic:** The workspace must not contain business logic, SDK code, or runtime code.
- **Fail Fast:** Workspace CI pipelines should act as the ultimate gatekeeper. If the workspace fails, the ecosystem is broken.
- **Decoupling:** Repositories should not hardcode paths to one another; they should be brought together exclusively within this workspace environment.
