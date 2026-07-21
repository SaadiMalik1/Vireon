# Docker Architecture

## Overview
To prevent divergence and reduce maintenance overhead, the VIREON ecosystem utilizes a centralized Docker architecture. Individual repositories do not maintain their own isolated Docker environments unless they require a highly specialized deployment that cannot be inherited from the core image.

## Core Image (`vireon`)
The `vireon` repository contains the canonical `Dockerfile` for the ecosystem. This image includes:
- The `python:3.11-slim` base
- The Rust toolchain (nightly) required for `neurodsl`
- Maturin for building Rust extensions
- The `vireon` core framework
- Core system dependencies (`libpango`, `libharfbuzz`, etc.)

This image serves as the base for all other containerized applications in the ecosystem.

## Downstream Images (`vireon-lab`, etc.)
Other repositories (like `vireon-lab`) **must not** duplicate the core `Dockerfile`. 
If a downstream repository requires a container, it must use the `vireon` core image as its `FROM` base, and only install the differential dependencies (e.g., specific lab datasets or Jupyter environments).

## Orchestration (`workspace`)
All `docker-compose.yml` configurations have been removed from the component repositories. 
The canonical multi-container environment (which spins up the UI, databases, background workers, and lab environments) is exclusively maintained in `workspace/docker-compose.yml`.

To run the ecosystem locally:
```bash
cd workspace
docker compose up --build
```
