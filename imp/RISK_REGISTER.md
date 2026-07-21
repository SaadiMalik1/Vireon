# Vireon Project — Risk Register

> **Date:** 2025-07-13
> **Reviewed by:** Independent Architecture Review Board
> **Classification:** Internal — For Project Leadership

---

## Legend

| Field | Meaning |
|---|---|
| **Severity** | Inherent severity if the risk materialises: Critical / High / Medium / Low |
| **Likelihood** | Probability the risk has already occurred or will occur: **Confirmed** (observed) / **Likely** (strong evidence) / **Possible** (plausible) / **Unlikely** (low probability) |
| **Current Mitigation** | What, if anything, currently exists to address the risk |
| **Recommended Action** | Minimum viable remediation step |

---

## Critical Risks (Immediate Action Required)

| ID | Risk | Severity | Likelihood | Impact Description | Current Mitigation | Recommended Action |
|---|---|---|---|---|---|---|
| R-001 | **CI pipeline is broken — no tests actually execute** | Critical | **Confirmed** | Every push and PR passes without running a single test. Defects go undetected; merge gate is illusory. | None. CI workflows exist but call no test commands. | Wire `pytest` and `cargo test` into CI immediately. Make tests mandatory on PRs. |
| R-002 | **`.gitmodules` is missing from the workspace** | Critical | **Confirmed** | `git clone --recursive` fails. The five-repo split is inoperable without submodules. No contributor can build the project from a fresh clone. | None. The file was never committed. | Create `.gitmodules` pointing to all sub-repositories; verify with a clean clone. |
| R-003 | **Circular dependency between `vireon` and `vireon-lab`** | Critical | **Confirmed** | `vireon` depends on `vireon-lab` (workspace member) while `vireon-lab` depends on `vireon`. Cargo resolves this by accepting the local path, but it prevents independent publishing and creates fragile coupling. Any change in one crate can break the other without warning. | Cargo's workspace member mechanism masks the cycle at build time. | Break the cycle by extracting shared types into a `vireon-core` crate that both depend on; remove the mutual dependency. |
| R-004 | **Evidence pipeline uses dummy SHA-256 — results cannot be verified** | Critical | **Confirmed** | The integrity and provenance chain uses placeholder `sha256(b"...")` hardcoded constants instead of real hashing. Any attestation produced is trivially forgeable, undermining the entire trust model. | None. The dummy implementation is intentional. | Replace with real `sha2` crate hashing; add unit tests that verify digest correctness against known test vectors. |
| R-005 | **Capability enforcement is application-level, not OS-level — providers can bypass it** | Critical | **Confirmed** | Capability checks are Rust function calls within the same process. A compromised or malicious provider module can call any system function directly; the sandbox is not enforced by the kernel. | `capctl` crate is a dependency but is not wired into enforcement. | Implement seccomp-bpf or cgroup-based enforcement; document the trust boundary clearly; or explicitly downgrade claims to "application-level policy." |
| R-006 | **TLS certificates checked into the repository** | Critical | **Confirmed** | Private key material (or certificates that should be ephemeral) are committed. If any are private keys, this is an immediate credential leak. Even if only public certs, they imply a static rotation model with no automation. | None. | Remove all certificate files from git history (git-filter-branch or BFG); generate certs at deploy time via certbot/Let's Encrypt or Vault. |
| R-007 | **No lock files — reproducible builds are impossible** | Critical | **Confirmed** | Neither `Cargo.lock` (committed) nor a Python lock file (`uv.lock` / `poetry.lock`) is reliably maintained across the workspace. Dependency resolution can diverge between any two builds. | Partial — `Cargo.lock` may exist in individual sub-crates but is not enforced at the workspace level. | Commit `Cargo.lock` for the Rust workspace; add `uv.lock` for the Python component; pin all transitive dependencies. |

---

## High Risks (Address Within One Sprint)

| ID | Risk | Severity | Likelihood | Impact Description | Current Mitigation | Recommended Action |
|---|---|---|---|---|---|---|
| R-008 | **77% of runtime files are deprecated shims — migration has no timeline** | High | **Confirmed** | 30 of 39 files in `vireon/runtime/` are `V1` shims forwarding to V2 stubs. The V2 implementations are mostly unimplemented (`todo!()`). The codebase is in a half-migrated state that is neither stable nor progressing. | Shim forwarding pattern exists but V2 targets are empty. | Set a hard deadline: either complete the V2 migration or revert the shims and stabilise V1. |
| R-009 | **No working onboarding path — every documented instruction fails** | High | **Confirmed** | README, CONTRIBUTING, and quickstart guides all reference commands, paths, or tools that do not work (missing `.gitmodules`, broken CI, incorrect `pyproject.toml` layout). Zero-time-to-first-run is effectively infinite. | None. Documentation describes aspirational state, not actual state. | Create a devcontainer.json or Nix flake; add a smoke-test script that validates the onboarding path after every change. |
| R-010 | **15 ADRs describe unimplemented architecture — massive design debt** | High | **Confirmed** | Architecture Decision Records reference systems (eBPF offload, CRDT state, Merkle tracing, hardware watchdog, bifurcated clock) that have zero code. These ADRs create false expectations and guide contributors toward building features that may never ship. | ADRs are well-written but disconnected from implementation. | Tag each ADR with its implementation status; archive ADRs for features moved off the roadmap. |
| R-011 | **No benchmarks exist — performance claims are unsubstantiated** | High | **Confirmed** | The project claims real-time signal processing capability and targets 30 kHz telemetry throughput. No `criterion` benchmarks, no profiling data, no load tests exist to support any performance assertion. | None. | Add `criterion` benchmarks for hot paths; integrate `cargo bench` into CI; establish a performance budget. |
| R-012 | **NeuroDSL has 9 instructions, 2 are no-ops, example is invalid** | High | **Confirmed** | Of the 9 defined opcodes, `NOP` and `HALT` are trivial; the provided example file (`basic_simulation.ndsl`) fails to parse. The language is too immature to be a credible differentiator. | Lexer and parser exist but are untested. | Fix the example file; add at least one more meaningful instruction; add round-trip parser tests. |
| R-013 | **MCP server trust boundary is explicitly undefined** | High | **Likely** | The Model Context Protocol server accepts external tool definitions and executes them, but there is no documented trust boundary, no input validation policy, and no sandboxing for untrusted tool payloads. | None. The MCP implementation is functional but not security-reviewed. | Document the trust model; add input schema validation; restrict MCP tool registration to allowlisted providers. |
| R-014 | **No CLA/DCO for an Apache 2.0 project** | High | **Likely** | The project is licensed Apache 2.0 and accepts contributions, but there is no Contributor License Agreement or Developer Certificate of Origin. This creates legal ambiguity about the provenance and licensing of contributed code. | None. | Add a DCO via `DCO` bot or CLA Assistant; add `CONTRIBUTING.md` with the sign-off requirement. |
| R-015 | **Intentional crypto weaknesses with no technical guardrails** | High | **Confirmed** | ADR-014 and code comments explicitly describe weakened cryptography as a "trade-off" for performance, but there are no compile-time or runtime flags to enforce using strong cryptography in production. A user could unknowingly ship vulnerable attestations. | None. The weak implementation is the default and only option. | Add a `--hardened` feature flag that gates real cryptography; make the dummy implementation opt-in and emit a compile-time warning. |

---

## Medium Risks (Plan Within One Quarter)

| ID | Risk | Severity | Likelihood | Impact Description | Current Mitigation | Recommended Action |
|---|---|---|---|---|---|---|
| R-016 | **No SBOM generation in CI** | Medium | **Confirmed** | No Software Bill of Materials is produced during builds. Vulnerability tracking and license compliance auditing are impossible. | None. | Add `syft` or `cargo sbom` to CI; publish SBOMs alongside release artifacts. |
| R-017 | **No security scanning in CI** | Medium | **Confirmed** | No static analysis (`cargo clippy -- -W clippy::all`), no dependency vulnerability scanning (`cargo audit`), no SAST. Known CVEs in dependencies go undetected. | None. | Add `cargo audit`, `trivy`, or `osv-scanner` to CI; fail the build on high/critical findings. |
| R-018 | **No version pinning for git dependencies** | Medium | **Likely** | Dependencies specified as `git = "..."` without a `rev` pin will resolve to whatever the default branch points to at build time. Two builds on different days may use different dependency versions. | None. All git deps use floating references. | Pin every git dependency to a specific commit SHA; update via PR, not silently. |
| R-019 | **Python GIL prevents parallel signal processing** | Medium | **Likely** | The signal processing pipeline is written in Python. The GIL prevents true parallelism for CPU-bound signal work, creating a hard ceiling on throughput that no amount of async optimisation can overcome. | Rust extensions could release the GIL, but none do currently. | Offload signal processing to Rust via PyO3 or `numpy` with release-GIL extensions; benchmark the GIL impact. |
| R-020 | **EventBus cannot meet 30 kHz telemetry target** | Medium | **Likely** | The current `EventBus` is a synchronous, in-process channel with no backpressure handling or batched dispatch. At 30 kHz event rate, it will become a bottleneck and likely cause memory bloat or dropped events. | None. No load testing has been performed. | Prototype an async event bus (e.g., `tokio::sync::broadcast`) with backpressure; benchmark against the 30 kHz target. |
| R-021 | **No integration tests exist** | Medium | **Confirmed** | Unit tests are sparse; integration tests spanning multiple components (VM + scheduler + capability system) do not exist. Component interactions are unverified. | None. | Add at least 5 integration tests covering the critical path: bootstrap → VM init → signal inject → evidence capture. |
| R-022 | **No release process or artifacts** | Medium | **Confirmed** | There are no GitHub Releases, no published wheels, no Docker images in a registry, and no release automation. The project cannot be consumed by external users. | None. | Define a release workflow (tag → build → publish to PyPI + Docker Hub + crates.io). |
| R-023 | **No signed commits or branch protection rules visible** | Medium | **Likely** | Without signed commits and protected branches, the commit history's integrity is not verifiable. A compromised contributor account could inject malicious changes to protected branches. | May exist in GitHub settings but is not enforced or documented. | Enable `require signed commits` on main; add `CODEOWNERS`; enforce required reviews. |
| R-024 | **Dependabot missing Cargo ecosystem** | Medium | **Confirmed** | Dependabot is configured but only for GitHub Actions and npm. The Rust (Cargo) ecosystem — which constitutes the majority of the codebase — is not covered. Outdated or vulnerable Rust dependencies will not be flagged. | Dependabot config exists but is incomplete. | Add `cargo` ecosystem to `.github/dependabot.yml`. |
| R-025 | **Windows and macOS have zero sandboxing** | Medium | **Possible** | Seccomp is Linux-only. On Windows and macOS, the capability enforcement system has no equivalent, meaning providers run with full process privileges. | None. Cross-platform sandboxing is not designed. | Use `job objects` on Windows and `sandbox-exec`/App Sandbox on macOS; or document these platforms as unsupported for untrusted providers. |

---

## Low Risks (Track and Address Opportunistically)

| ID | Risk | Severity | Likelihood | Impact Description | Current Mitigation | Recommended Action |
|---|---|---|---|---|---|---|
| R-026 | **Copyright year 2026 appears forward-dated** | Low | **Confirmed** | Source file headers claim copyright © 2026, which is in the future. This may cause legal ambiguity and signals that boilerplate was generated rather than written. | None. | Update copyright headers to the actual year of creation or use a dynamic year via build script. |
| R-027 | **Edition 2024 Rust requires very recent nightly** | Low | **Confirmed** | `Cargo.toml` specifies `edition = "2024"`, which stabilised in Rust 1.85 (released Feb 2025). Contributors on older toolchains cannot compile. | `rust-toolchain.toml` may pin a nightly. | Add `rust-toolchain.toml` to every crate; document the minimum required Rust version in README. |
| R-028 | **Truncated Code of Conduct** | Low | **Confirmed** | The `CODE_OF_CONDUCT.md` file is incomplete — it references sections or content that is missing. This undermines the project's commitment to community standards. | None. | Complete the CoC using the Contributor Covenant template or a custom policy. |
| R-029 | **No `FUNDING.yml`** | Low | **Unlikely** | No GitHub Sponsors or Open Collective funding file exists. This limits the project's ability to attract financial support. | None. | Add `.github/FUNDING.yml` if financial support is desired. |
| R-030 | **No community chat channel** | Low | **Unlikely** | No Discord, Slack, Matrix, or Zulip space is linked. Contributors have no synchronous communication venue, which may slow collaboration. | GitHub Issues and Discussions exist. | Create a Matrix space or Discord server; link it in README and CONTRIBUTING. |

---

## Summary Statistics

| Severity | Count | IDs |
|---|---|---|
| Critical | 7 | R-001 – R-007 |
| High | 8 | R-008 – R-015 |
| Medium | 10 | R-016 – R-025 |
| Low | 5 | R-026 – R-030 |
| **Total** | **30** | |

### Likelihood Breakdown

| Likelihood | Count |
|---|---|
| Confirmed | 20 |
| Likely | 7 |
| Possible | 2 |
| Unlikely | 1 |

> **Note:** 20 of 30 risks (67%) are *confirmed* — they have been directly observed in the codebase. This is not a speculative register; it is a finding report.