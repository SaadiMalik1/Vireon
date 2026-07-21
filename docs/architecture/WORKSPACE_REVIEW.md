# VIREON Workspace Distributed Monorepo Audit

This document reviews the `workspace` environment and its capacity to act as a unified, distributed monorepo.

## Workspace Topology

The VIREON ecosystem utilizes a distributed monorepo pattern managed via Git submodules within the `workspace` repository.

```
workspace/
├── .github/           (Submodule: Organization CI/CD)
├── vireon/            (Submodule: Core SDK & Runtime)
├── vireon-lab/        (Submodule: Presentation Layer)
└── neurodsl/          (Submodule: Rust Simulation Engine)
```

## Audit Dimensions

### 1. Cross-Repository Imports & Tooling
- **Status:** **PASS**
- **Analysis:** Local development seamlessly spans repositories. Python paths and Rust workspaces are properly configured.
- **Recommendation:** Implement a single top-level `justfile` (or `Makefile`) in `workspace` that abstracts away building and testing commands, e.g., `just test-all` spanning Cargo and Pytest.

### 2. Contract Compatibility
- **Status:** **FAIL**
- **Analysis:** The API boundary between `vireon.runtime` and `neurodsl` Rust engine relies on untracked Python interface expectations. If `neurodsl` changes a data shape, `vireon`'s CI only catches it if an integration test covers that specific edge case.
- **Recommendation:** Implement a shared `schemas/` directory within `workspace` housing Protobuf or FlatBuffer definitions. Both `vireon` and `neurodsl` must compile these schemas during build.

### 3. Docker & Environment Compatibility
- **Status:** **NEEDS IMPROVEMENT**
- **Analysis:** Each repository maintains its own Docker environment, leading to duplicated base images and conflicting Python versions across `vireon` and `vireon-lab`.
- **Recommendation:** Create a `docker/` directory in `workspace` containing the master `docker-compose.yml` and unified base image definitions (`vireon-base-python`, `vireon-base-rust`).

### 4. Continuous Integration
- **Status:** **PASS**
- **Analysis:** The `.github` submodule efficiently broadcasts reusable workflows (lint, test, publish) to the individual repositories.
- **Recommendation:** Introduce a nightly cross-ecosystem integration test triggered from the `workspace` repo that clones head on all submodules and runs the end-to-end simulation suite.

### 5. Dependency Locking
- **Status:** **FAIL**
- **Analysis:** `vireon` might depend on `neurodsl ^1.2.0`, but local development in `workspace` tests against `neurodsl` HEAD. This leads to "works on my machine" syndrome where developers test unreleased features locally that fail when published.
- **Recommendation:** Enforce strict semantic version pinning across submodules. Workspace local development should utilize `pip install -e` specifically managed by a tool like `uv` workspaces or `poetry` path dependencies.
