# The Final Ecosystem Architecture

## Ecosystem Overview
The VIREON ecosystem has been redesigned into a professional, multi-repository infrastructure project. It operates on the principle that **every responsibility has exactly one owner**. Duplication of documentation, DevOps, CI, and governance has been strictly eliminated.

## 1. Repositories
The ecosystem is split into 5 distinct repositories:
- **`vireon`**: The core framework, runtime, SDK, and canonical documentation.
- **`neurodsl`**: The low-level Rust domain-specific language engine.
- **`vireon-lab`**: The educational platform, examples, and user tutorials.
- **`workspace`**: The integration hub (orchestration, E2E testing, version locking).
- **`.github`**: The global governance hub (community standards, reusable CI, security policies).

## 2. Documentation
- **Canonical Docs**: Hosted solely in `vireon/docs/`.
- **Tutorials/Examples**: Hosted in `vireon-lab`.
- **Architectural Specs**: Found in `vireon/docs/` (e.g., `CONSTITUTION.md`, `INTEGRATION.md`, `WORKSPACE_ARCHITECTURE.md`).
- **READMEs**: All repo READMEs are strictly minimal (What is it, Who is it for, How to install, Where are the docs).

## 3. CI / CD
- **Reusable Workflows**: Stored in the `.github` repository.
- **Integration CI**: Stored in the `workspace` repository.
- Component repositories only contain thin workflows that call the reusable actions in `.github`.

## 4. Docker
- **Base Image**: `vireon/Dockerfile` builds the canonical base image containing the runtime and Rust toolchain.
- **Downstream Images**: Other repos (if needed) use `FROM vireon`.
- **Orchestration**: A single `workspace/docker-compose.yml` spins up the entire integrated ecosystem.

## 5. Workspace & Integration
The `workspace` is the only repository aware of the full ecosystem graph. It conducts:
- **Contract Testing**: Ensures `neurodsl` and `vireon` APIs remain compatible.
- **Compatibility Matrix**: Validates the supported version combinations.
- **E2E Validation**: The final gatekeeper for releases.

## 6. Dependency Graph
```mermaid
graph TD
    subgraph Global Governance
        GH[.github]
    end

    subgraph Integration Hub
        W[workspace]
    end

    subgraph Component Ecosystem
        V[vireon]
        N[neurodsl]
        L[vireon-lab]
    end

    W -->|Tests & Orchestrates| V
    W -->|Tests & Orchestrates| N
    W -->|Tests & Orchestrates| L
    
    L -->|Consumes| V
    L -->|Consumes| N
    V -->|Implements| N

    GH -.->|Enforces CI & Policy| W
    GH -.->|Enforces CI & Policy| V
    GH -.->|Enforces CI & Policy| N
    GH -.->|Enforces CI & Policy| L
```

## Summary
By separating governance (`.github`), orchestration (`workspace`), and core logic (`vireon`, `neurodsl`), the VIREON project is now scalable, deterministic, and highly maintainable for hundreds of future contributors.
