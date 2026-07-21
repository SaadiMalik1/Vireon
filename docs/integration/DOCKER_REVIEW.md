# VIREON Docker Ecosystem Review

This document evaluates the containerization strategy for VIREON, ensuring deployments are scalable, secure, and minimal.

## Docker Audit

### 1. Image Bloat & Multi-stage Builds
- **Status:** **FAIL**
- **Analysis:** Current Dockerfiles pull in the Rust toolchain (`cargo`), build the `neurodsl` engine, and leave the toolchain in the final image, resulting in image sizes > 1.5 GB.
- **Recommendation:** Implement strictly separated Multi-Stage builds. Stage 1 (Builder) compiles Rust and Python wheels. Stage 2 (Runtime) copies only the compiled `.whl` and `.so` files into a minimal `python:3.11-slim` or `distroless` base image.

### 2. Privilege Escalation & Security
- **Status:** **FAIL**
- **Analysis:** The `vireon-lab` container currently runs the Node/Python processes as `root`.
- **Recommendation:** Create a non-root `vireon` user in all Dockerfiles. Set `USER vireon` before the `CMD` instruction to prevent container breakout vulnerabilities.

### 3. Docker Compose Orchestration
- **Status:** **NEEDS IMPROVEMENT**
- **Analysis:** A unified `docker-compose.yml` does not exist to spin up the UI, the Engine, and a mock target device simultaneously.
- **Recommendation:** Create a `workspace/docker-compose.yml` defining services for `engine`, `ui`, `database` (for telemetry storage), and `mock-device`. Use environment variables to handle network routing.

### 4. Deterministic Reproducibility
- **Status:** **PASS**
- **Analysis:** Base images are pinned by major/minor tags (e.g., `python:3.11`).
- **Recommendation:** Pin base images strictly by SHA256 hashes (e.g., `python:3.11@sha256:...`) to guarantee absolute environment reproducibility for research validation.
