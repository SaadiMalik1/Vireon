# VIREON Ecosystem Governance Model

## 1. Project Management
The VIREON ecosystem is managed by the Core Maintainers team. All major architectural decisions must be documented via Architecture Decision Records (ADRs) in `docs/adr/`.

## 2. Roles and Responsibilities
- **Core Maintainers**: Have merge access to `vireon` and `vireon-lab`. Responsible for architectural direction and final review of PRs.
- **Contributors**: Can submit Pull Requests across either repository. Must adhere to `CONTRIBUTING.md` and signed DCO.

## 3. Decision Making & Approval Thresholds
PR approval rules depend on the scope of changes:
- **Standard PRs** (bug fixes, new non-breaking features, documentation improvements): Require **1 approval** from a Core Maintainer.
- **Architectural PRs** (ADR modifications, SDK interface changes, security capability changes, core runtime modifications): Require **2 approvals** from Core Maintainers.

## 4. Ecosystem Boundaries
- `vireon`: Production runtime engine, SDK, NeuroDSL compiler & VM, scheduler, capability engine, evidence pipeline, CLI, and ADR specifications.
- `vireon-lab`: Educational UI (Streamlit), interactive tutorials, attack scenarios, reference dataset management, and knowledge base.
- **Dependency Rule**: `vireon-lab` depends on `vireon` as a package. `vireon` NEVER depends on `vireon-lab`.

## 5. Security & Ethics
All contributions must respect the guardrails outlined in `SECURITY.md` and the neuroethics constraints (G1–G8 guardrails).
