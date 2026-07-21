# VIREON Ecosystem Dependency Graph

This document isolates the detailed dependency mapping across all repositories.

## 1. Top-Level Package Dependencies

```mermaid
graph TD
    vireon-lab --> vireon
    vireon --> neurodsl
    vireon --> numpy
    vireon --> pydantic
    vireon-lab --> fastapi
    vireon-lab --> react
    neurodsl --> ndarray
    neurodsl --> serde
    neurodsl --> pyo3
```

## 2. Infrastructure Dependencies

```mermaid
graph TD
    vireon-lab_Docker --> vireon-base_Docker
    vireon_Docker --> vireon-base_Docker
    vireon-base_Docker --> python3.11-slim
    neurodsl_Docker --> rust:1.75-slim
```

## 3. Vulnerability Surface
- `numpy`, `pydantic`, `fastapi`, and `pyo3` represent the most critical software supply chain vectors. Strict hash pinning is required.
