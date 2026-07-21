# Vireon Project — Recommendations

> **Date:** 2025-07-13
> **Reviewed by:** Independent Architecture Review Board
> **Classification:** Internal — For Project Leadership

---

These recommendations are ordered by priority tier. Each tier represents a different strategic posture: stop harm first, then rethink fundamentals, then fix what must work, then stop over-promising, and finally invest in growth.

---

## 1. DELETE — Stop Doing

> *These items create confusion, bloat, or noise. Remove them now.*

### 1.1 Delete the dual `pyproject.toml` in `vireon-lab`

`vireon-lab` contains its own `pyproject.toml` that conflicts with the root workspace configuration. Python package resolution treats this as a nested project, causing import errors and shadowing.

- **Action:** Remove `vireon-lab/pyproject.toml`. Keep only the root `pyproject.toml`.
- **Verification:** `python -c "import vireon_lab"` resolves correctly from the workspace root.

### 1.2 Delete the 30 deprecated shim files in `vireon/runtime/`

77% of the runtime directory is V1→V2 forwarding shims where the V2 target is `todo!()`. This half-migrated state is worse than either the old or new version alone. It inflates file counts, confuses navigation, and creates a false impression of completeness.

- **Action:** Either complete the V2 migration in one shot, or revert the shims and stabilise V1. The current state is not acceptable.
- **Verification:** `rg "todo!" vireon/runtime/` returns zero results.

### 1.3 Delete the invalid NeuroDSL example file (`basic_simulation.ndsl`)

The example file fails to parse against the current lexer. Shipping broken examples in a repository is worse than shipping no examples — it actively misleads users.

- **Action:** Delete `basic_simulation.ndsl` until a valid one can be written and verified by a round-trip test (parse → serialise → parse again).
- **Verification:** The remaining example files (if any) all pass the parser without errors.

### 1.4 Delete the legacy root `Dockerfile`

The workspace root contains a Dockerfile that is superseded by `docker/vireon.Dockerfile`. Two Dockerfiles with different configurations create confusion about which to use.

- **Action:** Delete the root `Dockerfile`. Ensure `docker/vireon.Dockerfile` builds successfully.
- **Verification:** `docker build -f docker/vireon.Dockerfile .` completes.

### 1.5 Delete the unused `serde`/`bincode` dependencies from `scribe`

The `scribe` crate depends on `serde` and `bincode` but does not use them. Unused dependencies inflate compile times and attack surface.

- **Action:** Remove `serde` and `bincode` from `scribe/Cargo.toml`.
- **Verification:** `cargo build -p scribe` succeeds; `cargo tree -p scribe` no longer lists them.

---

## 2. REDESIGN — Fundamental Changes

> *These items require architectural decisions. They cannot be patched; they must be rethought.*

### 2.1 Consolidate into a single monorepo

The current five-repo split (`vireon`, `vireon-lab`, `scribe`, `neuro-dsl`, plus the workspace) creates enormous coordination overhead for a project with fewer than 10 contributors. Cross-repo changes require simultaneous PRs. The submodule mechanism is broken (`.gitmodules` is missing). The complexity cost far exceeds the benefit of separation.

- **Action:** Collapse all repositories into a single Cargo workspace with a single Python package. Use Cargo workspace features and Python namespace packages to maintain logical boundaries.
- **Timeline:** 1–2 sprints.
- **Success criterion:** A fresh `git clone` followed by a single build command produces all artifacts.

### 2.2 Replace the EventBus with a proper message queue

The current `EventBus` is a synchronous, in-process channel. It has no backpressure, no batching, no persistence, and no fan-out. It will not scale to the stated 30 kHz telemetry target.

- **Action:** Replace with either:
  - A tokio-based async channel with backpressure (`tokio::sync::broadcast` or `mpsc` with bounded capacity)
  - A lightweight embedded message queue (e.g., a ring-buffer-based event log)
- **Requirement:** Support at least 30 kHz sustained throughput with < 1 ms p99 latency in benchmarks.
- **Verification:** Criterion benchmark under load.

### 2.3 Implement real capability enforcement or document the limitation

The current "capability system" is a set of Rust function calls within the same process address space. A provider module that ignores the capability check and calls `std::fs::read` directly will succeed. This is not a sandbox; it is a policy suggestion.

- **Option A (recommended for near-term):** Explicitly document that capability enforcement is *advisory* and not a security boundary. Remove all language suggesting providers are "sandboxed."
- **Option B (recommended for production):** Implement OS-level enforcement via:
  - Linux: seccomp-bpf (restrict syscalls) + cgroups (restrict resources)
  - A separate process per provider with IPC, so kernel isolation is the enforcement layer
- **Timeline:** Option A: 1 day. Option B: 2–4 sprints.

### 2.4 Replace the evidence pipeline's dummy SHA-256 with real cryptography

The evidence pipeline uses hardcoded `sha256(b"...")` values. This is not hashing; it is a placeholder that gives the appearance of integrity verification without providing it.

- **Action:**
  1. Replace all dummy hashes with calls to the `sha2` crate.
  2. Implement the Merkle tree described in ADR-014 with real `Hash256` nodes.
  3. Add asymmetric signing (Ed25519) for evidence provenance.
  4. Add unit tests against NIST SHA-256 test vectors.
- **Verification:** `cargo test -p vireon-evidence` passes; attestations can be independently verified.

### 2.5 Implement a real scheduler or remove the "bifurcated clock" from the roadmap

ADR-003 describes a "bifurcated clock" scheduler that decouples simulation time from wall-clock time. No implementation exists. The concept adds significant architectural complexity for unclear benefit in a framework that primarily processes real-time signals.

- **Action:** Either:
  - Implement a concrete scheduler with documented semantics and tests, or
  - Remove the bifurcated clock from the roadmap and ADR-003, and use a simple `tokio::time::interval`-based approach.
- **Principle:** Do not carry architectural complexity for features that are not being built.

---

## 3. FIX — Must-Have

> *These are table-stakes for any open-source project. They are not optional.*

### 3.1 Add `.gitmodules` to the workspace

Without this file, the multi-repo structure is non-functional.

- **Action:** Create `.gitmodules` with entries for all sub-repositories.
- **Verification:** `git clone --recursive <url>` on a fresh machine succeeds.

### 3.2 Fix CI workflow — wire up tests

CI currently runs no tests. This is the single highest-impact fix.

- **Action:**
  1. Add `submodules: recursive` to the checkout step.
  2. Install Rust toolchain via `dtolnay/rust-toolchain`.
  3. Install Python via `actions/setup-python` with `uv`.
  4. Run `cargo test --workspace` and `pytest` as separate jobs.
  5. Require both to pass before merge.
- **Verification:** A PR that introduces a failing test is blocked.

### 3.3 Add a `justfile` or `Makefile` with working build targets

Contributors should not need to read three different READMEs to figure out how to build.

- **Action:** Create a `justfile` (or `Makefile`) with targets:
  - `just build` — build all Rust and Python components
  - `just test` — run all tests
  - `just lint` — run clippy, ruff, and mypy
  - `just fmt` — format all code
  - `just dev` — start a development environment
- **Verification:** Every target succeeds on a fresh clone.

### 3.4 Add `.gitignore` to the workspace

A missing `.gitignore` leads to accidental commits of build artifacts, Python caches, IDE files, and OS metadata.

- **Action:** Create a comprehensive `.gitignore` covering Rust (`target/`), Python (`__pycache__/`, `.venv/`, `*.pyc`), IDE files (`.vscode/`, `.idea/`), and OS files (`.DS_Store`, `Thumbs.db`).
- **Verification:** `git status` is clean after a full build.

### 3.5 Complete the Code of Conduct

The current `CODE_OF_CONDUCT.md` is truncated. An incomplete CoC signals that the project does not take community governance seriously.

- **Action:** Replace with the full [Contributor Covenant v2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) or a custom policy of equivalent completeness.
- **Verification:** The file renders correctly and contains enforcement guidelines and contact information.

### 3.6 Add CLA/DCO

An Apache 2.0 project without a contribution agreement creates legal risk.

- **Action:** Add the [DCO](https://developercertificate.org/) as the minimum requirement. Use the `probot/dco` GitHub App for enforcement. If the project grows, consider a CLA via CLA Assistant.
- **Verification:** Commits without `Signed-off-by:` are rejected by the DCO bot.

### 3.7 Add PGP key for security reports

The `SECURITY.md` file should include a PGP key for encrypted vulnerability reports.

- **Action:** Generate a project PGP key; add it to `SECURITY.md` alongside reporting instructions.
- **Verification:** `gpg --import <key>` succeeds; an encrypted test message can be decrypted.

### 3.8 Pin all dependency versions with lock files

Without lock files, builds are non-reproducible.

- **Action:**
  1. Ensure `Cargo.lock` is committed at the workspace root.
  2. Add `uv.lock` for the Python component (using `uv` as the package manager).
  3. Pin all git dependencies to a specific `rev` SHA.
- **Verification:** `cargo build --locked` and `uv sync --locked` succeed.

### 3.9 Add `CODEOWNERS` to all repos

Without CODEOWNERS, changes to critical files (security, CI, crypto) can be reviewed by anyone.

- **Action:** Create `.github/CODEOWNERS` with:
  - `* @vireon-core` (default)
  - `/src/crypto/** @vireon-security`
  - `/.github/workflows/** @vireon-infra`
  - `/docs/adr/** @vireon-architecture`
- **Verification:** PRs to protected paths require review from the specified team.

### 3.10 Add source location tracking to the NeuroDSL lexer

The lexer produces tokens without line/column information. Parse errors are unhelpful: "unexpected token" with no indication of where.

- **Action:** Add `Span { line: u32, column: u32 }` to every token; propagate spans through the parser; include spans in all error messages.
- **Verification:** A parse error on line 5, column 12 reports that exact location.

---

## 4. DEFER — Stop Promising

> *These items are in the roadmap or documentation but have no implementation. Remove them until there is a concrete plan.*

### 4.1 Remove ADR-006 (eBPF) from the roadmap

eBPF offload for signal processing is an ambitious goal, but there is no prototype, no design document beyond the ADR, and no contributor with demonstrated eBPF expertise. Listing it in the roadmap creates expectations that cannot be met.

- **Action:** Mark ADR-006 as `Deferred`; remove it from any near-term roadmap or milestone. Revisit only when a contributor submits a working prototype.

### 4.2 Remove ADR-008 (CRDT) until there is a real distributed state requirement

CRDT-based distributed state is a solution in search of a problem. The project currently runs as a single-process application. CRDTs add significant complexity for a use case that has not been demonstrated.

- **Action:** Mark ADR-008 as `Deferred`; remove from roadmap. Revisit if and when multi-node operation becomes a requirement with documented use cases.

### 4.3 Remove ADR-014 (Merkle tree tracing) until the evidence pipeline uses real cryptography

A Merkle tree for evidence integrity is a sound design, but it is meaningless when the leaf hashes are dummy values. Implementing the tree on top of fake hashes would create a false sense of security.

- **Action:** Mark ADR-014 as `Blocked by R-004`. Revisit after the evidence pipeline uses real hashing (Recommendation 2.4).

### 4.4 Remove ADR-010 (Hardware watchdog) from the near-term roadmap

Hardware watchdog integration requires specific hardware, driver support, and real-time scheduling. None of these are in place. This is a long-term feature, not a near-term one.

- **Action:** Move ADR-010 to a "Future Considerations" section of the roadmap with no target date.

### 4.5 Stop claiming "Validation Operating System"

The project is a Python simulation framework with a Rust VM backend. It is not an operating system. Calling it one sets expectations for kernel-level isolation, process scheduling, and hardware management that are not met and are not planned.

- **Action:**
  1. Remove "Operating System" and "OS" from all user-facing descriptions.
  2. Replace with accurate language: "simulation framework," "validation runtime," or "neural signal processing platform."
  3. Update the README tagline and any marketing materials.
- **Principle:** Honest positioning builds trust faster than aspirational branding.

---

## 5. BUILD — If Continuing

> *These are investments that make sense **only after** the above fixes are in place. Do not start these until the project is buildable and testable.*

### 5.1 Create a working onboarding experience

The current onboarding path fails at every step. Until a new contributor can go from `git clone` to "running a simulation" in under 10 minutes, the project will not attract contributors.

- **Action:**
  1. Create `.devcontainer/devcontainer.json` with Rust, Python, and all system dependencies.
  2. Write a `scripts/setup.sh` that is tested in CI (not just documented).
  3. Add a "smoke test" CI job that runs the full onboarding flow on every push.
- **Success criterion:** A new contributor using VS Code Dev Containers can run the example simulation without reading any documentation.

### 5.2 Add real integration tests

Unit tests for individual components are necessary but insufficient. The most critical bugs live in the *interactions* between components.

- **Minimum viable suite:**
  1. Bootstrap the VM → verify it reaches IDLE state.
  2. Inject a signal → verify it reaches the processing pipeline.
  3. Trigger a capability check → verify it is enforced.
  4. Capture evidence → verify the attestation chain.
  5. Load a NeuroDSL program → verify execution to completion.
- **Verification:** `cargo test --test integration` passes; tests are run in CI.

### 5.3 Add a benchmark suite with CI tracking

Performance claims ("real-time," "30 kHz") are currently unsupported by any data.

- **Action:**
  1. Add `criterion` to dev-dependencies.
  2. Benchmark: VM instruction dispatch, signal pipeline throughput, event bus latency, evidence hashing.
  3. Use `github-action-benchmark` to track results over time.
  4. Set alerting thresholds (e.g., > 10% regression fails CI).
- **Verification:** Benchmark results are visible on every PR.

### 5.4 Publish wheels to PyPI and Docker images to a registry

The project cannot be used by external consumers without published artifacts.

- **Action:**
  1. Set up `maturin` or `setuptools-rust` to build Python wheels with the Rust extension.
  2. Publish to PyPI via Trusted Publishing (OIDC).
  3. Publish Docker images to GitHub Container Registry (`ghcr.io`) on every release tag.
  4. Add installation instructions to README: `pip install vireon` or `docker pull ghcr.io/.../vireon`.
- **Verification:** A user can install and run the project without cloning the repository.

### 5.5 Add label support to NeuroDSL (symbolic jump targets)

NeuroDSL currently lacks labels, making control flow fragile and programs unreadable. Jumps by numeric offset are error-prone.

- **Action:**
  1. Add a `label:` declaration to the grammar.
  2. Implement a first pass that resolves labels to instruction offsets.
  3. Support `JMP label_name` and `BRANCH label_name` syntax.
  4. Update the example file.
- **Verification:** A NeuroDSL program with labels parses, resolves, and executes correctly.

### 5.6 Implement SHAPE and WAIT in the VM

Of the 9 NeuroDSL opcodes, only 7 are meaningful (2 are no-ops). The VM needs more useful instructions to be a credible execution environment.

- **Action:**
  1. `SHAPE <dim1, dim2, ...>` — declare the shape of a signal tensor; validate on runtime access.
  2. `WAIT <ticks>` — pause VM execution for N simulation ticks, enabling timed sequences.
  3. Add unit tests for each new instruction.
  4. Update the NeuroDSL documentation.
- **Verification:** All new instructions have test coverage; the example program uses at least one new instruction.

---

## Priority Matrix

| Priority | Tier | Items | Effort | Impact |
|---|---|---|---|---|
| **P0 — This Week** | DELETE | 1.1–1.5 | Low | Reduces confusion immediately |
| **P0 — This Week** | FIX | 3.1–3.4 | Low-Medium | Unblocks all contributors |
| **P1 — Next Sprint** | FIX | 3.5–3.10 | Low | Governance and security basics |
| **P1 — Next Sprint** | DEFER | 4.1–4.5 | Low | Prevents false expectations |
| **P2 — This Quarter** | REDESIGN | 2.1–2.5 | High | Fundamental architectural health |
| **P3 — After P0–P2** | BUILD | 5.1–5.6 | Medium-High | Growth and adoption |

> **Key principle:** Do not invest in BUILD until the project is buildable (FIX), honest about scope (DEFER), and architecturally sound (REDESIGN).