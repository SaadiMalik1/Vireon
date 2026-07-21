# Independent Repository Reviews

This document details the independent analysis of each repository in the VIREON ecosystem.

## 1. vireon (Core SDK & Runtime)
- **Purpose:** Provide the core Python SDK, Runtime Engine, and basic Reference Providers for neurotechnology validation.
- **Mission:** Act as the vendor-neutral, deterministic orchestration layer connecting simulations, models, and external plugins.
- **Public API:** `vireon.sdk` (Interfaces, exceptions, signals, types).
- **Internal API:** `vireon.runtime` (Coordinator, Event Bus, Plugin Registry).
- **Users:** Platform engineers, plugin authors, data scientists, vendors.
- **Stakeholders:** Protocol validators, security auditors, core architecture team.
- **Responsibilities:** Scheduling, state synchronization, plugin sandboxing, orchestration.
- **Non-goals:** End-user graphical interfaces, low-level high-performance parallel computing (delegated to Rust).
- **Dependencies:** `numpy`, `neurodsl` (Python bindings), standard Python library.
- **Consumers:** `vireon-lab`, third-party vendor plugins, custom validation scripts.
- **Maintainers:** Core Architecture Team.
- **Release strategy:** Continuous Integration to PyPI following Semantic Versioning.
- **Version strategy:** Strict SemVer strictly mirroring API contracts.
- **Lifecycle:** Long-term stable.
- **Migration Actions:** Extract any domain-specific providers (e.g., `providers.physics.thermal`) out of the core package and into independent plugins if possible, to keep the core strictly limited to orchestration.

## 2. vireon-lab (UI & Tools)
- **Purpose:** Provide graphical, web-based, and command-line interfaces for operating the VIREON engine.
- **Mission:** Deliver an accessible, visual developer experience (DX) for running, debugging, and analyzing VIREON digital twins.
- **Public API:** CLI commands (e.g., `vireon-lab run`, `vireon-lab serve`), REST/GraphQL API for UI.
- **Internal API:** Frontend-to-backend API wrappers.
- **Users:** Medical researchers, neuroengineers, compliance officers.
- **Stakeholders:** Product managers, UX designers, end-users.
- **Responsibilities:** Visualization, interactive configuration, log viewing, report generation.
- **Non-goals:** Heavy simulation computation, direct hardware interfacing.
- **Dependencies:** `vireon` (Core SDK), `fastapi`/`flask`, React/Vue (frontend).
- **Consumers:** Human users, automated reporting tools.
- **Maintainers:** UI/UX Team.
- **Release strategy:** Bundled desktop apps (Electron/Tauri) and Docker images.
- **Version strategy:** SemVer, tightly coupled with major `vireon` releases.
- **Lifecycle:** Iterative, high-velocity UX updates.
- **Migration Actions:** None required; boundaries are clean.

## 3. neurodsl (Rust Simulation Engine)
- **Purpose:** High-performance, memory-safe parallel execution environment for massive neural simulations and signal generation.
- **Mission:** Provide the underlying computational horsepower that the Python runtime orchestrates.
- **Public API:** `neurodsl` Rust crate, PyO3 Python bindings (`python_ext`).
- **Internal API:** `forge`, `scribe` internal crates.
- **Users:** `vireon` runtime, advanced users bypassing Python.
- **Stakeholders:** Simulation architects, performance engineers.
- **Responsibilities:** Fast Fourier Transforms, differential equation solving, large matrix operations, simulated physics at scale.
- **Non-goals:** Orchestrating complex user workflows, managing plugin ecosystems.
- **Dependencies:** `ndarray`, `serde`, `pyo3`.
- **Consumers:** `vireon` runtime, Rust-native simulation researchers.
- **Maintainers:** Rust/Simulation Team.
- **Release strategy:** Cargo crates, PyPI wheels (via `maturin`).
- **Version strategy:** SemVer.
- **Lifecycle:** Highly stable, performance-focused.
- **Migration Actions:** Introduce a strict Schema Registry (e.g., FlatBuffers) between `neurodsl` and `vireon` to formalize the FFI boundary.

## 4. workspace (Distributed Monorepo)
- **Purpose:** Act as the developer entry point and synchronization environment for the distributed ecosystem.
- **Mission:** Provide a unified onboarding, documentation, and local development environment spanning all repositories.
- **Public API:** `Makefile` or `justfile` commands (e.g., `make setup`, `make test-all`).
- **Internal API:** Git submodules.
- **Users:** All VIREON contributors and maintainers.
- **Stakeholders:** Developer Experience (DX) leads, DevOps.
- **Responsibilities:** Developer environment bootstrapping, cross-repo integration testing.
- **Non-goals:** Publishing its own independent software package.
- **Dependencies:** Git, Docker.
- **Consumers:** Developers.
- **Maintainers:** DevOps & Core Team.
- **Release strategy:** Tied to overarching ecosystem milestones.
- **Version strategy:** Calendar Versioning (CalVer) or milestone tracking.
- **Lifecycle:** Continuous evolution.
- **Migration Actions:** Move all architectural and reference documentation into `workspace/docs` to eliminate duplication across sub-repositories.

## 5. .github (CI/CD Ecosystem)
- **Purpose:** Centralized organization-wide GitHub Actions workflows, issue templates, and governance policies.
- **Mission:** Enforce uniform quality, security, and release standards across all repositories.
- **Public API:** Reusable GitHub workflows (`workflow_call`).
- **Internal API:** N/A.
- **Users:** Repository CI pipelines.
- **Stakeholders:** DevSecOps, Maintainers.
- **Responsibilities:** Standardized linting, testing, Docker building, dependency updating (Renovate), security scanning.
- **Non-goals:** Containing actual business logic or code.
- **Dependencies:** GitHub Actions ecosystem.
- **Consumers:** `vireon`, `vireon-lab`, `neurodsl`, `workspace`.
- **Maintainers:** DevSecOps Team.
- **Release strategy:** Tagged releases of workflows for pinning.
- **Version strategy:** SemVer tracking for workflow contracts.
- **Lifecycle:** Stable, security-focused.
- **Migration Actions:** None. Boundaries are well-established.
