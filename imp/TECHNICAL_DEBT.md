# Technical Debt Catalog — Vireon Ecosystem

**Review Date:** 2025-07-11
**Scope:** vireon (core), vireon-lab, neurodsl, workspace
**Reviewer:** Architecture Review Board
**Total Items:** 18
**Estimated Total Remediation Effort:** 47–97 person-days

---

## Priority Matrix

| # | Item | Impact | Effort | Priority | Status |
|---|------|--------|--------|----------|--------|
| 1 | V1/V2 Strangler Fig Migration | 🔴 Critical | 10–15d | P0 | ⬜ Not started |
| 15 | Unimplemented ADRs (15) | 🔴 Critical | 20–40d | P0 | ⬜ Not started |
| 2 | Dead Code | 🟡 Low | 1d | P3 | ⬜ Not started |
| 3 | Unused Rust Dependencies | 🟡 Low | 0.25d | P4 | ⬜ Not started |
| 4 | Stub Directories | 🟠 Medium | 2d | P2 | ⬜ Not started |
| 5 | Broken CI | 🔴 Critical | 1d | P1 | ⬜ Not started |
| 6 | Missing Infrastructure Files | 🟠 Medium | 3d | P2 | ⬜ Not started |
| 7 | No-op Setup Script | 🟡 Low | 0.5d | P3 | ⬜ Not started |
| 8 | Invalid NeuroDSL Example | 🟠 Medium | 1d | P2 | ⬜ Not started |
| 9 | Empty Grammar Spec | 🟠 Medium | 3–5d | P1 | ⬜ Not started |
| 10 | No-op VM Instructions | 🟠 Medium | 2–3d | P2 | ⬜ Not started |
| 11 | Dummy Cryptography | 🔴 Critical | 3–5d | P0 | ⬜ Not started |
| 12 | Version Inconsistency | 🟠 Medium | 1d | P1 | ⬜ Not started |
| 13 | Dual Dockerfiles | 🟠 Medium | 1–2d | P2 | ⬜ Not started |
| 14 | Truncated Code of Conduct | 🟡 Low | 0.5d | P4 | ⬜ Not started |
| 16 | Architecture Boundary Tests | 🟡 Low | 0d (keep) | P5 | ⚠️ Observational |
| 17 | No Source Locations in NeuroDSL | 🟠 Medium | 3–5d | P2 | ⬜ Not started |
| 18 | Mocked Python Extension Tests | 🟠 Medium | 2–3d | P2 | ⬜ Not started |

**Priority Definitions:**
- **P0** — Blocks production / security risk. Must fix immediately.
- **P1** — Blocks correct CI/CD or developer onboarding. Fix this sprint.
- **P2** — Significant quality/maintainability issue. Fix next sprint.
- **P3** — Low-impact cleanup. Fix opportunistically.
- **P4** — Trivial fix. Fix when convenient.
- **P5** — No action needed; documented for awareness.

---

## Detailed Findings

### TD-01: V1/V2 Strangler Fig Migration (P0) 🔴

**Location:** `vireon/vireon/` — 30 of 39 runtime files

**Description:** The majority of `vireon/` runtime files are deprecated shims that re-export symbols from external provider packages (`vireon_lab.*`, `providers.*`). Only ~9 files contain actual core logic.

**Evidence:**
- 30 files follow the pattern:
  ```python
  """DEPRECATED: This module has moved to vireon_lab.*"""
  import warnings
  warnings.warn("...", DeprecationWarning, stacklevel=2)
  from vireon_lab.whatever import *  # re-exports everything
  ```
- No migration timeline exists.
- No completion criteria are defined.
- No deprecation warnings are actually raised (they're commented out or suppressed in some files).
- New contributors cannot distinguish real code from shims.

**Impact:**
- 77% of the core package is dead weight.
- Import paths are misleading — `vireon.foo` actually loads `vireon_lab.foo`.
- IDE navigation, code search, and static analysis are all degraded.
- Any refactoring of the shim layer risks breaking the (unknown) set of consumers.

**Estimated Effort:** 10–15 person-days

**Remediation Options:**
1. **Complete the migration** — Delete all shims; update all imports to use `vireon_lab.*` directly. Requires auditing all consumers.
2. **Reverse the migration** — Move actual implementations back into `vireon/`. High-risk if external packages have already diverged.
3. **Set a hard deadline** — Add real `DeprecationWarning`s that will become `ImportError` in version N+1.

**Recommendation:** Option 1 with a 2-release deprecation window.

---

### TD-02: Dead Code (P3) 🟡

**Location:** Multiple files across repos

**Instances:**

| File | Description |
|------|-------------|
| `vireon/libraries/__init__.py` | Empty file — directory serves no purpose |
| `vireon/reference_providers/__init__.py` | Empty file — directory serves no purpose |
| `providers/__init__.py` | Contains only a comment: `# Provider implementations` |
| `neurodsl/` (Rust) | `MemoryError` variant defined in error types but never constructed or matched |

**Estimated Effort:** 1 person-day

**Remediation:** Delete empty directories and files. Remove `MemoryError` variant or add a use case.

---

### TD-03: Unused Rust Dependencies (P4) 🟡

**Location:** `neurodsl/scribe/Cargo.toml`

**Description:** `serde = "1.0"` and `bincode = "1.3"` are declared as dependencies but never imported or used in any `.rs` file in the `scribe` crate.

**Impact:** Minor — increases compile time (~2s for serde's proc macros) and adds unnecessary entries to the dependency tree / SBOM.

**Estimated Effort:** 0.25 person-days (15 minutes)

**Remediation:** Remove both lines from `Cargo.toml`.

---

### TD-04: Stub Directories (P2) 🟠

**Location:** `workspace/` — 5 directories

**Description:** The workspace repository contains 5 directories that are stubs (empty or containing only placeholder files):

| Directory | Contents |
|-----------|----------|
| `benchmarks/` | Empty or single placeholder |
| `compatibility/` | Empty or single placeholder |
| `contracts/` | Empty or single placeholder |
| `integration/` | Empty or single placeholder |
| `release/` | Empty or single placeholder |

Additionally, `ARCHITECTURE_AUDIT/SECURITY_REVIEW.md` is referenced in documentation but returns 404 — the file does not exist.

**Impact:** Gives the false impression that infrastructure exists when it does not. Wastes developer time investigating empty directories.

**Estimated Effort:** 2 person-days (audit, document, delete or implement)

**Remediation:** Delete empty stubs. Create the missing security review document or remove the reference.

---

### TD-05: Broken CI (P1) 🔴

**Location:** `.github/workflows/integration.yml`

**Description:** The CI workflow uses a pattern like:
```yaml
- run: mv tmp_* ../
```
This is fundamentally broken on GitHub Actions runners:

- The working directory is a virtual filesystem mount — `../` may not resolve to the workspace root.
- Glob expansion (`*`) in `mv` may match zero files and produce an error.
- No `|| true` guard means the entire job fails silently.
- The tmp files may not exist yet (race condition with prior steps).

**Impact:** CI integration tests have likely never passed. This means the integration test suite provides zero value.

**Estimated Effort:** 1 person-day

**Remediation:** Use explicit file paths or `mkdir -p && cp` with proper error handling. Add a step that verifies the files exist before moving them.

---

### TD-06: Missing Infrastructure Files (P2) 🟠

**Location:** Across all repos

**Description:** Several expected infrastructure files are missing:

| File | Expected Location | Status | Impact |
|------|------------------|--------|--------|
| `.gitmodules` | workspace/ | Missing | Submodule references in docs are broken |
| `justfile` | workspace/ | Missing | `just` commands in docs don't work |
| `.gitignore` | workspace/ | Missing | Generated files may be committed |
| `devcontainer.json` | workspace/ | Missing | VS Code Codespaces experience broken |
| `DESIGN_RATIONALE.md` | workspace/ | Missing | Referenced in CONTRIBUTING.md |
| `schemas/` | workspace/ | Missing | Referenced in architecture docs |
| `Dockerfile` | vireon/ | Missing | `.dockerignore` exists but no Dockerfile to use it |

**Estimated Effort:** 3 person-days

**Remediation:** Create each file with appropriate content or remove references to non-existent files.

---

### TD-07: No-op Setup Script (P3) 🟡

**Location:** `workspace/setup-all.sh`

**Description:** The setup script is:
```bash
#!/bin/bash
echo "Setting up Vireon development environment..."
# (nothing else)
```

**Impact:** New developers running `./setup-all.sh` will see a success message but nothing will actually be set up. This is actively misleading.

**Estimated Effort:** 0.5 person-days

**Remediation:** Implement the script to actually clone repos, install dependencies, and verify the environment — or delete it and document the manual setup steps.

---

### TD-08: Invalid NeuroDSL Example (P2) 🟠

**Location:** `neurodsl/examples/basic_simulation.ndsl`

**Description:** The example file uses syntax that the NeuroDSL compiler cannot parse. Attempting to compile it produces a parser error.

**Impact:** This is the first thing a new contributor will try. A non-working example creates an immediate negative impression and blocks onboarding.

**Estimated Effort:** 1 person-day

**Remediation:** Fix the example to use valid syntax, or update the parser to accept it. Add a CI check that compiles all examples.

---

### TD-09: Empty Grammar Specification (P1) 🟠

**Location:** `neurodsl/specification/grammar.md`

**Description:** The grammar specification file contains only a title line. There is no formal grammar definition, no EBNF, no syntax rules.

**Impact:**
- Without a formal grammar, the compiler's parser is the only specification — and it's incomplete (see TD-08).
- Contributors have no reference for what syntax is valid.
- Future parser rewrites will have no oracle to test against.
- This is a prerequisite for TD-08 and TD-17.

**Estimated Effort:** 3–5 person-days

**Remediation:** Write a complete EBNF or PEG grammar covering all implemented and planned syntax. Use it to generate test cases.

---

### TD-10: No-op VM Instructions (P2) 🟠

**Location:** `neurodsl/forge/src/vm/` — `SHAPE` and `WAIT` opcodes

**Description:** Two VM instructions are fully parsed by the compiler and emitted as bytecode, but the VM execution engine does nothing when it encounters them:

```rust
Opcode::Shape => { /* no-op */ }
Opcode::Wait  => { /* no-op */ }
```

**Impact:**
- Code that uses these instructions will silently do nothing.
- Users who write `SHAPE` or `WAIT` in their programs will get no feedback that their intent is being ignored.
- This could lead to safety issues if `WAIT` is expected to introduce timing guarantees (e.g., in a BCI feedback loop).

**Estimated Effort:** 2–3 person-days

**Remediation:** Either implement the instructions or emit a compilation warning: `"instruction SHAPE is parsed but not yet executed — your program will not behave as expected"`.

---

### TD-11: Dummy Cryptography (P0) 🔴

**Location:** Evidence pipeline, MCP server

**Description:** Two critical cryptography failures:

1. **Evidence pipeline** — Uses plain SHA-256 hash and calls it a "signature":
   ```python
   evidence_hash = hashlib.sha256(data).hexdigest()
   # Stored as "digital_signature": evidence_hash
   ```
   This is **not a digital signature**. A hash provides integrity but not authenticity or non-repudiation. Anyone can compute the same hash for the same data.

2. **MCP server** — Stores the secret key as a plaintext file on disk:
   ```python
   SECRET_KEY_PATH = Path("~/.vireon/secret_key.pem").expanduser()
   ```
   No encryption at rest, no file permissions enforcement, no key rotation mechanism.

**Impact:**
- **Regulatory:** For a BCI/medical device system, evidence integrity is likely a regulatory requirement (FDA 21 CFR Part 11, EU MDR). SHA-256 without a real signature scheme is non-compliant.
- **Security:** The plaintext secret key can be read by any process running as the same user, or by anyone with filesystem access.
- **Legal:** Evidence tampering is trivial — modify the data, recompute the hash, replace the "signature."
- **Audit:** Any security auditor will flag this as a critical finding.

**Estimated Effort:** 3–5 person-days

**Remediation:**
1. Replace SHA-256 hash with actual digital signatures (Ed25519 or ECDSA-P256) using the `cryptography` library already in dependencies.
2. Store the secret key using the OS keyring (`keyring` package) or at minimum with restrictive file permissions (`0600`).
3. Implement key rotation.

---

### TD-12: Version Inconsistency (P1) 🟠

**Location:** `vireon-lab/`

**Description:** `vireon-lab` contains two `pyproject.toml` files with conflicting metadata:

| Field | Root `pyproject.toml` | Nested `pyproject.toml` |
|-------|-----------------------|------------------------|
| Version | (v1) | (v2, different) |
| Python requires | `>=3.10` | `>=3.9` |
| Dependencies | (full set) | (partial set) |

**Impact:** Package managers, linters, and IDEs may pick up either file, leading to inconsistent behavior. The Python 3.9 minimum in the nested file is incompatible with the core package's 3.10 minimum.

**Estimated Effort:** 1 person-day

**Remediation:** Consolidate to a single `pyproject.toml`. If a nested package is needed, use Python workspace mode (PEP 735) to avoid metadata duplication.

---

### TD-13: Dual Dockerfiles (P2) 🟠

**Location:** `workspace/`

**Description:** Two Dockerfiles exist with conflicting configurations:

| Aspect | `workspace/Dockerfile` | `workspace/docker/Dockerfile` |
|--------|----------------------|------------------------------|
| Base Python | 3.11 | 3.10 |
| Runs as | root | non-root user |
| Services | Streamlit + API | Streamlit only |
| Security | No hardening | Some hardening |
| ENTRYPOINT | Defined differently | Defined differently |

**Impact:** Deployment is ambiguous — which Dockerfile is canonical? The security posture difference (root vs. non-root) is a compliance concern.

**Estimated Effort:** 1–2 person-days

**Remediation:** Consolidate to a single Dockerfile using build targets (`--target dev`, `--target prod`). Always run as non-root. Standardize on Python 3.11+.

---

### TD-14: Truncated Code of Conduct (P4) 🟡

**Location:** `CODE_OF_CONDUCT.md`

**Description:** The Code of Conduct is truncated/incomplete:

- Missing enforcement guidelines (how to report violations, what happens next).
- Missing attribution (likely derived from Contributor Covenant but not properly attributed).
- No contact information for the committee.

**Impact:** Legal and community health risk. An unenforceable CoC is worse than no CoC.

**Estimated Effort:** 0.5 person-days

**Remediation:** Adopt the full Contributor Covenant v2.1 text with project-specific contact information.

---

### TD-15: Unimplemented ADRs — Largest Debt Item (P0) 🔴

**Location:** `workspace/architecture/decisions/` — 15 ADRs

**Description:** 15 Architecture Decision Records describe a sophisticated system. **None of these are implemented.**

| ADR | Decision | Implementation Status |
|-----|----------|----------------------|
| 01 | eBPF-based signal processing | ❌ Not implemented |
| 02 | CRDT-based state synchronization | ❌ Not implemented |
| 03 | WASM plugin runtime | ❌ Not implemented |
| 04 | Zero-copy data pipeline | ❌ Not implemented |
| 05 | Merkle-tree evidence chain | ❌ Partial (SHA-256 hash only, see TD-11) |
| 06 | Event-sourced architecture | ❌ Not implemented |
| 07 | Capability-based security | ❌ Not implemented |
| 08 | Hot-reloadable providers | ❌ Not implemented |
| 09 | Multi-tenant isolation | ❌ Not implemented |
| 10 | Structured logging with correlation IDs | ❌ Not implemented |
| 11 | Circuit-breaker pattern for providers | ❌ Not implemented |
| 12 | Backpressure-aware data ingestion | ❌ Not implemented |
| 13 | A/B testing framework for pipelines | ❌ Not implemented |
| 14 | Configurable serialization (protobuf/msgpack) | ❌ Not implemented |
| 15 | Distributed tracing (OpenTelemetry) | ❌ Not implemented |

**Impact:**
- This is **architectural fiction** — the documentation describes a system that does not exist.
- Every new contributor reads these ADRs and forms expectations that will not be met.
- Decisions were made (presumably after deliberation) but never executed, suggesting either scope creep or abandoned plans.
- The gap between documentation and reality undermines trust in all project documentation.

**Estimated Effort:** 20–40 person-days (to implement all 15), or 3–5 days to mark them as "Deferred" / "Rejected" with rationale.

**Remediation (Recommended):**
1. **Immediate:** Mark each ADR with accurate status: `Accepted` → `Deferred` or `Superseded`. Add a section explaining what *is* currently implemented instead.
2. **Short-term:** Delete ADRs for features that are clearly out of scope. Keep only the ones that represent a committed roadmap.
3. **Long-term:** Implement the top-priority ADRs one at a time, updating status as you go.

---

### TD-16: Architecture Boundary Tests (P5) ⚠️

**Location:** `vireon/tests/test_architecture.py`

**Description:** Tests use Python AST parsing to enforce layer boundaries — preventing imports between forbidden layers.

**Assessment:** This is actually a *positive* pattern. It indicates the team is aware that the architecture is fragile and has proactively added guardrails. The debt is not in the tests but in the architecture that requires them.

**Estimated Effort:** 0 person-days (no action — this is healthy defensive engineering)

**Recommendation:** Keep the tests. Once the strangler fig migration (TD-01) is complete, update the boundary rules to reflect the new architecture.

---

### TD-17: No Source Locations in NeuroDSL (P2) 🟠

**Location:** `neurodsl/forge/src/` — all compiler error paths

**Description:** All NeuroDSL error messages are bare strings with no line number, column number, or source snippet:

```
Error: unexpected token 'SHAPE'
```

Instead of:
```
Error: unexpected token 'SHAPE' at line 12, column 4
   12 │     SHAPE alpha_beta
      │     ^^^^^
```

**Impact:** Debugging NeuroDSL programs is unnecessarily difficult. Users must manually search for the offending syntax.

**Estimated Effort:** 3–5 person-days

**Remediation:** Add a `Span { start: usize, end: usize, file: String }` type. Thread it through the lexer, parser, and type checker. Use it in all error reporting. This is a well-understood compiler pattern (see `miette`, `ariadne`, or `codespan` crates).

---

### TD-18: Mocked Python Extension Tests (P2) 🟠

**Location:** `neurodsl/python_ext/tests/`

**Description:** The Python extension tests use `unittest.mock` to mock the Rust extension rather than testing the actual compiled `.so`/`.pyd` file:

```python
def test_compile():
    mock_extension.compile = MagicMock(return_value=bytecode)
    # Tests the mock, not the real extension
```

**Impact:** These tests verify the test harness, not the product. The actual Rust↔Python FFI boundary (the most likely source of bugs in a pyo3 extension) is completely untested.

**Estimated Effort:** 2–3 person-days

**Remediation:** Write integration tests that import the actual compiled extension module. Use `pytest` with a fixture that verifies `import forge` succeeds. Test real compilation of valid and invalid programs.

---

## Remediation Summary by Effort

### Quick Wins (< 1 day each) — Total: ~3.5 days

| Item | Effort |
|------|--------|
| TD-03: Unused Rust deps | 0.25d |
| TD-07: No-op setup script | 0.5d |
| TD-14: Truncated CoC | 0.5d |
| TD-05: Broken CI | 1d |
| TD-02: Dead code | 1d |
| TD-12: Version inconsistency | 1d |

### Medium Effort (1–5 days each) — Total: ~16.5 days

| Item | Effort |
|------|--------|
| TD-08: Invalid example | 1d |
| TD-13: Dual Dockerfiles | 1–2d |
| TD-04: Stub directories | 2d |
| TD-06: Missing infrastructure | 3d |
| TD-10: No-op VM instructions | 2–3d |
| TD-09: Empty grammar spec | 3–5d |
| TD-17: No source locations | 3–5d |
| TD-18: Mocked Python tests | 2–3d |

### Large Effort (5+ days each) — Total: ~33–60 days

| Item | Effort |
|------|--------|
| TD-11: Dummy cryptography | 3–5d |
| TD-01: Strangler fig migration | 10–15d |
| TD-15: Unimplemented ADRs | 20–40d |

---

## Technical Debt Ratio

```
Implemented features (approximate):    ████████░░  ~40 lines of actual core logic per file (9 files)
Strangler fig shims:                   ████████████████████████████████████░░░░  30 files
Stub/empty directories:                ██████░░  5 directories
Unimplemented ADRs:                    ████████████████████████████████████░░░░░░  15 ADRs
No-op VM instructions:                 ██░░  2 opcodes
```

**Rough estimate:** ~70% of the codebase is either non-functional, non-implemented, or actively misleading.

---

## Top 5 Actions (Ordered by Impact × Feasibility)

1. **Fix TD-11 (Cryptography)** — 3–5 days. Security and regulatory blocker. No production deployment without real signatures and proper key storage.
2. **Resolve TD-15 (ADRs)** — 3–5 days just to update status. Prevents continued architectural fiction from misleading contributors and stakeholders.
3. **Break circular dependency (DEP-01)** — 3–5 days. See DEPENDENCY_ANALYSIS.md. Prerequisite for any packaging work.
4. **Complete TD-01 (Strangler Fig)** — 10–15 days. Largest single codebase cleanup. Unlocks meaningful refactoring.
5. **Fix TD-05 (CI)** — 1 day. Enables actual integration testing to provide value.

**Total for top 5: 20–31 person-days (~4–6 weeks for a single developer).**