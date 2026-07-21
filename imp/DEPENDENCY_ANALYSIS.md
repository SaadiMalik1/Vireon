# Dependency Analysis — Vireon Ecosystem

**Review Date:** 2025-07-11
**Scope:** vireon (core), vireon-lab, neurodsl, workspace
**Reviewer:** Architecture Review Board

---

## Dependency Health Score: 2.4 / 10 (Critical)

| Dimension                | Score | Weight | Weighted |
|--------------------------|-------|--------|----------|
| Dependency Pinning       | 1/10  | 0.20   | 0.20     |
| Circular Dependency Free | 1/10  | 0.25   | 0.25     |
| Lock File / Reproducible | 0/10  | 0.20   | 0.00     |
| Transitive Transparency   | 3/10  | 0.15   | 0.45     |
| Build Hermeticity        | 3/10  | 0.10   | 0.30     |
| SBOM / Supply Chain      | 2/10  | 0.10   | 0.20     |
| **Total**                |       | **1.0**| **2.40** |

This score falls in the **Critical** range (< 4.0). Immediate remediation is required before any production deployment.

---

## 1. Dependency Graph

### 1.1 Package-Level Dependency Graph (Directed)

```
                    ┌─────────────────────────────┐
                    │       EXTERNAL PACKAGES       │
                    │ (not in any repo)            │
                    │                             │
                    │  vireon_lab.*                │
                    │  vireon_neuro_dsl            │
                    │  providers.physics           │
                    │  providers.ids               │
                    │  providers.auth              │
                    │  providers.privacy           │
                    │  providers.dynamics          │
                    │  providers.clinical          │
                    │  brainflow                   │
                    └──────────┬──────────────────┘
                               │ imported by
                               ▼
┌──────────────┐       ┌──────────────┐
│   vireon     │◄──┐   │  vireon-lab  │
│   (core)     │───┘   │              │
│              │       │              │
│ pydantic     │       │ streamlit    │
│ cryptography │       │ pandas       │
│ click        │       │ plotly       │
│ websockets   │       │ brainflow    │
│ pyyaml       │       │ pyedflib     │
│ numpy        │       │ mne          │
│ mcp          │       │ scipy        │
│ pytest*      │       │ pylsl        │
│ pytest-async*│       │ weasyprint   │
│ pytest-cov*  │       │ bleak        │
│ mypy*        │       │ pyyaml (impl)│
│              │       │ jinja2 (impl)│
│              │       │ websockets   │
│              │       │ (implicit)   │
│              │       │ cryptography │
│              │       │ (implicit)   │
│              │       │ RPi.GPIO (impl)│
│              │       │ spidev (impl)│
└──────────────┘       └──────┬───────┘
                               │ git+https://...@main
                               ▼
                      ┌──────────────┐
                      │   vireon     │
                      │  (GitHub)    │
                      └──────────────┘

         ┌──────────────────────────────┐
         │           neurodsl           │
         │                              │
         │  forge ──── (ZERO deps)      │
         │  scribe ─── bincode 1.3 ✗    │
         │            serde 1.0  ✗      │
         │  python_ext ─ pyo3 0.23.0    │
         │               forge (path)   │
         │               scribe (path)  │
         │               bincode, serde │
         └──────────────────────────────┘

         ┌──────────────────────────────┐
         │          workspace           │
         │  (no pyproject.toml,         │
         │   no Cargo.toml,             │
         │   no package.json)           │
         └──────────────────────────────┘
```

### 1.2 Circular Dependency (Critical)

```
  vireon ──imports──▶ vireon_lab.* (external, not in repo)
      ▲                       │
      │        depends on     │
      └──── vireon-lab ◀──────┘
         (git+https://...@main)
```

- **Direction A:** `vireon` source code contains `import vireon_lab.*` statements, treating `vireon_lab` as an external provider package.
- **Direction B:** `vireon-lab` declares `vireon` as a git dependency in `pyproject.toml`.
- **Result:** You cannot install either package without the other. This is a **package-level circular dependency**.

---

## 2. Detailed Findings

### FINDING-DEP-01: Circular Dependency [CRITICAL]

| Field     | Value                                                        |
|-----------|--------------------------------------------------------------|
| Severity  | 🔴 Critical                                                  |
| Affected  | vireon, vireon-lab                                           |
| Effort    | 3–5 days                                                     |

`vireon` imports from `vireon_lab.*` (8 external provider packages), while `vireon-lab` depends on `vireon` via `git+https://github.com/SaadiMalik1/vireon.git@main`. This creates an unresolvable cycle for any package manager.

**Impact:**
- `pip install vireon` will fail unless `vireon-lab` is already installed globally.
- `pip install vireon-lab` will attempt to install `vireon` from git, which then fails because `vireon_lab` is not yet available.
- No CI pipeline can build either package in isolation.
- Tools like `pip-compile`, `poetry`, or `pdm` cannot resolve this graph.

**Remediation:** Extract the shared interface into a third package (e.g., `vireon-interfaces` or `vireon-core-types`) that both `vireon` and `vireon-lab` depend on. Remove the direct import of `vireon_lab.*` from `vireon` core.

---

### FINDING-DEP-02: Git Dependency on Core Package [CRITICAL]

| Field     | Value                                                        |
|-----------|--------------------------------------------------------------|
| Severity  | 🔴 Critical                                                  |
| Affected  | vireon-lab/pyproject.toml                                    |
| Effort    | 1 day                                                        |

```toml
vireon = {git = "https://github.com/SaadiMalik1/vireon.git@main"}
```

**Problems:**
- Always installs from `main` HEAD — no version pinning, no stability guarantee.
- Breaks in air-gapped / offline / corporate-proxy environments.
- No integrity verification beyond git's transport-level SHA.
- GitHub rate limits will block CI after ~60 unauthenticated requests/hour.
- If the repository is renamed, deleted, or made private, all downstream installs break permanently.

**Remediation:** Publish `vireon` to PyPI (or a private registry). Pin to semver ranges: `vireon >=0.1.0,<0.2.0`.

---

### FINDING-DEP-03: Unused Rust Dependencies [LOW]

| Field     | Value                                                        |
|-----------|--------------------------------------------------------------|
| Severity  | 🟡 Low                                                       |
| Affected  | neurodsl/scribe/Cargo.toml                                   |
| Effort    | 15 minutes                                                   |

`serde = "1.0"` and `bincode = "1.3"` are declared in `scribe/Cargo.toml` but never used in any source file. This increases compile time (serde's derive macro is heavy) and attack surface.

**Remediation:** Remove both entries from `Cargo.toml`.

---

### FINDING-DEP-04: Undeclared Python Dependencies [HIGH]

| Field     | Value                                                        |
|-----------|--------------------------------------------------------------|
| Severity  | 🟠 High                                                      |
| Affected  | vireon-lab/pyproject.toml (nested)                           |
| Effort    | 30 minutes                                                   |

The following packages are imported in `vireon-lab` source code but **not declared** in its `pyproject.toml`:

| Package      | Import Location(s)                        | Transport | Risk               |
|--------------|-------------------------------------------|-----------|--------------------|
| `jinja2`     | Template rendering paths                 | PyPI      | Missing at runtime |
| `markupsafe` | Used transitively by jinja2              | PyPI      | Version conflict   |
| `websockets` | Communication layer                       | PyPI      | Missing at runtime |
| `cryptography` | Evidence hashing, key management       | PyPI      | Missing at runtime |
| `brainflow`  | EEG acquisition                           | Native C  | Install failure    |
| `pyedflib`   | EDF file I/O                             | Native C  | Install failure    |
| `mne`        | EEG processing                            | PyPI      | Missing at runtime |
| `pylsl`      | Lab Streaming Layer                      | Native C  | Install failure    |
| `RPi.GPIO`   | Raspberry Pi GPIO                        | HW        | Platform lock      |
| `spidev`     | SPI bus communication                    | HW        | Platform lock      |

**Impact:** `pip install vireon-lab` will succeed but the application will crash at runtime with `ModuleNotFoundError` when any of these code paths are reached.

**Remediation:** Add all imports to `pyproject.toml` with appropriate markers:
```toml
[project.optional-dependencies]
eeg = ["brainflow~=5.0.0", "pyedflib~=0.1.30", "mne>=1.6.0", "pylsl~=1.16.2"]
rpi = ["RPi.GPIO>=0.7.0", "spidev>=3.5"]
templates = ["jinja2>=3.1.0"]
```

---

### FINDING-DEP-05: Heavy Optional Dependencies with Poor Fallback Testing [MEDIUM]

| Field     | Value                                                        |
|-----------|--------------------------------------------------------------|
| Severity  | 🟡 Medium                                                    |
| Affected  | vireon-lab                                                  |
| Effort    | 5–10 days                                                    |

`brainflow`, `mne`, and `pyedflib` require native C/C++ compilation with system libraries (liblsl, FFTW, LAPACK). They have graceful fallback paths in code, but:

- No CI job tests the fallback path (all CI environments install the full stack).
- The fallback behavior is undocumented — users don't know what features are degraded.
- No integration test verifies that the application starts successfully when these are missing.

**Remediation:** Add a CI matrix job that runs with `--no-deps` and only the core dependency set. Document degraded mode.

---

### FINDING-DEP-06: No Lock Files [CRITICAL]

| Field     | Value                                                        |
|-----------|--------------------------------------------------------------|
| Severity  | 🔴 Critical                                                  |
| Affected  | All Python packages                                          |
| Effort    | 1 day                                                        |

No lock files exist across the entire ecosystem:

| Lock File          | Exists? | Package        |
|--------------------|---------|----------------|
| `poetry.lock`      | ❌       | vireon         |
| `poetry.lock`      | ❌       | vireon-lab     |
| `Pipfile.lock`     | ❌       | vireon         |
| `Pipfile.lock`     | ❌       | vireon-lab     |
| `requirements.txt` | ❌       | vireon         |
| `uv.lock`          | ❌       | vireon         |
| `Cargo.lock`       | ✅       | neurodsl       |

**Impact:** Reproducible builds are impossible. A dependency releasing a breaking change will silently break all deployments.

**Remediation:** Adopt `uv` (fastest) or `poetry` and commit the lock file. For `vireon-lab`'s heavy native deps, use `--resolution lowest-direct` to minimize breakage.

---

### FINDING-DEP-07: No SBOM Generation in CI [MEDIUM]

| Field     | Value                                                        |
|-----------|--------------------------------------------------------------|
| Severity  | 🟡 Medium                                                    |
| Affected  | CI/CD pipelines                                             |
| Effort    | 2 hours                                                      |

The `vireon sbom` CLI command exists but is never invoked in any CI workflow. This means:

- No automated supply chain vulnerability scanning.
- No machine-readable inventory of transitive dependencies.
- Compliance requirements (FDA, HIPAA for medical device software) cannot be met.

**Remediation:** Add a CI step:
```yaml
- name: Generate SBOM
  run: vireon sbom --format cyclonedx > sbom.json
- name: Scan for vulnerabilities
  uses: advanced-security/sbom-action@v1
```

---

### FINDING-DEP-08: Rust Nightly Required [MEDIUM]

| Field     | Value                                                        |
|-----------|--------------------------------------------------------------|
| Severity  | 🟡 Medium                                                    |
| Affected  | neurodsl                                                    |
| Effort    | 2–4 days (per crate)                                         |

`neurodsl` uses `edition = "2024"` in `Cargo.toml`, which requires Rust nightly. This is documented only in `CONTRIBUTING.md` and nowhere else.

**Impact:**
- Standard `rustup` installations default to stable — contributors will hit confusing compile errors.
- CI must pin to a specific nightly version; if that nightly regresses, builds break.
- Edition 2024 features may change before stabilization.
- Cross-compilation for ARM (Raspberry Pi targets) with nightly is significantly harder.

**Remediation:** Either (a) downgrade to `edition = "2021"` (recommended for stability), or (b) add a `rust-toolchain.toml` file to the repo root and document the nightly requirement in `README.md`.

---

### FINDING-DEP-09: Python Version Mismatch [MEDIUM]

| Field     | Value                                                        |
|-----------|--------------------------------------------------------------|
| Severity  | 🟡 Medium                                                    |
| Affected  | vireon, vireon-lab, Dockerfiles                              |
| Effort    | 1 hour                                                       |

| Component                    | Python Requirement |
|------------------------------|-------------------|
| `vireon/pyproject.toml`      | `>=3.10`          |
| `vireon-lab/pyproject.toml`  | `>=3.10`          |
| `vireon-lab/nested/pyproject.toml` | `>=3.9`  |
| `workspace/Dockerfile` (root) | `3.11`           |
| `workspace/docker/Dockerfile` | `3.10`           |

**Impact:** A developer using Python 3.9 (valid per the nested `pyproject.toml`) will hit syntax errors from the core `vireon` package which uses 3.10+ features (match statements, `X | Y` union types).

**Remediation:** Standardize on `>=3.11` across all `pyproject.toml` files and both Dockerfiles. Python 3.10 reaches EOL in October 2026.

---

## 3. Workspace Dependency Gap

The workspace repository has **no dependency file at all**:

- No `pyproject.toml` (not a Python project)
- No `Cargo.toml` (not a Rust project)
- No `package.json` (not a Node project)

This means the workspace cannot be installed, built, or tested as a unit. It exists purely as a collection of stubs and configuration files. It should either become a proper monorepo (with a root `pyproject.toml` using workspace features) or be eliminated.

---

## 4. Transitive Dependency Risk Map

```
                  CRITICAL  HIGH  MEDIUM  LOW
                  ────────  ────  ──────  ───
Circular deps         █                            1
Git core dep          █                            1
No lock files         █                            1
Undeclared deps                 █                  10
Heavy native deps                      █            3
No SBOM in CI                          █            1
Rust nightly                           █            1
Python mismatch                        █            1
Unused Rust deps                                 █   2
                  ────────  ────  ──────  ───
                  3         1     4       2
```

---

## 5. Recommended Remediation Roadmap

### Phase 1 — Emergency (Week 1)
1. Break the circular dependency by extracting a `vireon-interfaces` package.
2. Publish `vireon` to PyPI; replace git dependency with versioned PyPI dependency.
3. Add all undeclared dependencies to `vireon-lab/pyproject.toml` with optional-dependencies groups.
4. Adopt `uv` and commit `uv.lock` for both Python packages.

### Phase 2 — Stabilization (Weeks 2–3)
5. Standardize Python version to `>=3.11` everywhere.
6. Add `rust-toolchain.toml` and document nightly requirement; evaluate downgrade to edition 2021.
7. Remove unused `serde` and `bincode` from `scribe/Cargo.toml`.
8. Add `vireon sbom` to CI pipeline.

### Phase 3 — Hardening (Weeks 4–6)
9. Add CI matrix job testing fallback paths without native deps.
10. Convert workspace to a proper monorepo with root `pyproject.toml` (workspace mode) or eliminate it.
11. Pin all transitive dependencies via lock file.
12. Set up Dependabot or Renovate for automated dependency updates.

---

## 6. Summary

The Vireon ecosystem's dependency management is in a **critical state**. The circular dependency between core and lab packages makes standard installation impossible. The reliance on a git-HEAD dependency eliminates any notion of version stability. The complete absence of lock files means no build has ever been truly reproducible. These are not minor inconveniences — they are **fundamental architectural flaws** that will block any production deployment, security audit, or regulatory compliance review.

The Rust side (neurodsl) is significantly healthier: it has a `Cargo.lock`, clear workspace boundaries, and zero unused transitive dependencies in the `forge` crate. The primary risk there is the nightly edition requirement.

**Immediate action is required on FINDING-DEP-01 and FINDING-DEP-06 before any other work proceeds.**
