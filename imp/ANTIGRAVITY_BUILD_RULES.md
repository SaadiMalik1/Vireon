# ANTIGRAVITY BUILD RULES

**Engineering Directives for Building the VIREON Ecosystem**

**Scope**: All repositories.
**Enforcement**: A Rule is not satisfied until the code passes CI and tests prove it works.
**Philosophy**: Build what the ADRs describe. Ship what you build. Every design decision that survived the ADR process exists for a reason — implement it with the rigor it deserves.

---

## PART I: REPOSITORY STRUCTURE

### Rule 1 — Two Repos, Clear Mandate

Keep the two-repo split. It is the right call.

```
Vireon/                         vireon-lab/
├── Core runtime engine          ├── Educational UI (Streamlit)
├── SDK (public API surface)     ├── Student-friendly examples
├── Scheduler                     ├── Lab experiment templates
├── State store                   ├── Tutorial notebooks
├── Capability engine             ├── Simplified provider examples
├── Provider interfaces           ├── Knowledge base content
├── Evidence pipeline             ├── Report templates
├── NeuroDSL integration          ├── Dataset tools
├── CLI (run, validate, sbom)     └── Beginner-oriented docs
├── Tests (unit + integration)
├── Docker (production)
└── Docs (ADR, API, architecture)
```

**Vireon** is the serious runtime — the thing a BCI company would embed, a researcher would script, a regulator would evaluate. It has zero educational content, no Streamlit dashboards, no \"getting started\" tutorials. It has an API reference, architecture documentation, and a CLI.

**vireon-lab** is the on-ramp. A student clones it, runs `make demo`, sees a BCI attack simulation in a browser, reads the annotated source, and understands how Vireon works by example. It depends on Vireon as a package but never contributes core code.

**What this means in practice**: If you're unsure which repo something belongs in, ask: \"Would a BCI vendor's engineering team need this in their integration?\" If yes → Vireon. If \"a grad student learning neurosecurity would benefit\" → vireon-lab.

### Rule 2 — Absorb workspace, .github, and neurodsl

The other three repos become part of Vireon:

| Current Repo | Destination | Rationale |
|---|---|---|
| `workspace/` (ADRs, Docker, CI) | `Vireon/docs/`, `Vireon/docker/`, `Vireon/.github/` | Workspace has no code. Its assets belong in the repo they serve. |
| `.github/` (governance, templates) | `Vireon/.github/` | GitHub community profile features must be in the main repo to work. |
| `neurodsl/` (Rust DSL) | `Vireon/crates/neurodsl/` | NeuroDSL is a core runtime component. It compiles to a Python extension that Vireon imports. Separating them forces version skew and breaks CI. |

After this, the ecosystem is **two repos**:
- `Vireon/` — production runtime + SDK + NeuroDSL + CI + Docker + ADRs + governance
- `vireon-lab/` — educational platform + examples + tutorials + knowledge base

### Rule 3 — No Circular Dependencies

`vireon-lab` depends on `vireon` (pip package). `vireon` must NEVER depend on `vireon-lab`. Currently, `vireon/runtime/` has deprecated shims that import from `vireon_lab.*` and `providers.*`. These shims must be resolved one of two ways:

(a) **Move the code into Vireon** if it's core runtime functionality (e.g., if the clinical evaluator, physics engine, or IDS is needed by the runtime itself).

(b) **Delete the shim** if the code only exists in vireon-lab for educational/demo purposes. Vireon consumers import it from `vireon-lab`, not through a re-export in Vireon.

After resolution, `python -c \"import vireon\"` must work with ONLY the dependencies listed in Vireon's `pyproject.toml`. No phantom imports.

---

## PART II: BUILD EVERYTHING THE ADRs DESCRIBE

### Rule 4 — The ADRs Are the Specification, Not Aspirations

The 15 ADRs are accepted architectural decisions. They describe the system you are building. Each ADR must be implemented in order of dependency. The implementation order is:

```
Phase A: Foundation (no ADR dependencies)
  ADR-004  Deterministic Execution      → owned clock, owned RNG, seed management
  ADR-009  FFI Error Mapping            → consistent Rust↔Python error types

Phase B: Core Runtime (depends on Phase A)
  ADR-001  Kernel Transition           → VireonOrchestrator owns event loop
  ADR-003  Provider Capability Manifests → signed manifests, fail-closed loading
  ADR-005  Bifurcated Clock Scheduler   → virtual-time + wall-time modes
  ADR-013  Compiler-Pinned Determinism  → pinned toolchain for replay

Phase C: Data Plane (depends on Phase B)
  ADR-002  Control/Data Plane Split    → gRPC control, shared-memory data
  ADR-007  Zero-Copy Pointer Handoff    → direct memory sharing for telemetry
  ADR-015  Non-Blocking Ring Buffers    → SPSC queues for high-throughput data

Phase D: State & Security (depends on Phase C)
  ADR-006  eBPF Capability Enforcement  → OS-level sandboxing
  ADR-008  CRDT State Store            → conflict-free distributed state
  ADR-012  Unidirectional Memory Protections → memory safety at boundaries
  ADR-011  Epoched CRDT GC              → tombstone cleanup

Phase E: Integrity (depends on Phase D)
  ADR-010  Hardware Watchdog           → external stall detection
  ADR-014  Merkle Tree Tracing         → cryptographic trace bundles
```

Each phase is a PR (or series of PRs). Each PR includes implementation AND tests. Do not begin Phase B until Phase A passes all tests.

### Rule 5 — Each ADR Gets a Pass/Fail Test Suite

Before implementing an ADR, write the test suite that proves it works. This is your contract.

**Example — ADR-004 (Deterministic Execution)**:
```python
def test_deterministic_replay_produces_identical_results():
    \"\"\"Run the same experiment twice with the same seed.
    Every state transition, every event, every telemetry sample must be identical.\"\"\"
    config = load_config(\"tests/fixtures/deterministic_experiment.toml\")
    trace_1 = run_and_record(config, seed=42)
    trace_2 = run_and_record(config, seed=42)
    assert trace_1.state_transitions == trace_2.state_transitions
    assert trace_1.events_published == trace_2.events_published
    assert trace_1.telemetry_samples == trace_2.telemetry_samples

def test_deterministic_across_python_versions():
    \"\"\"Pin the Python version and verify replay works.\"\"\"
    # This test documents the version pinning requirement
    pass  # Verified by CI matrix, not runtime test
```

**Example — ADR-006 (eBPF Capability Enforcement)**:
```python
def test_provider_cannot_access_filesystem():
    \"\"\"A provider that attempts to open /etc/passwd gets killed.\"\"\"
    malicious_provider = Path(\"tests/fixtures/malicious_provider.py\")
    result = run_provider_isolated(malicious_provider, capabilities=[\"state.read:signal\"])
    assert result.exit_code != 0
    assert \"Permission denied\" in result.stderr

def test_provider_cannot_import_vireon_internals():
    \"\"\"A provider that tries 'from vireon.runtime.state import StateStore' fails.\"\"\"
    result = run_provider_isolated(
        Path(\"tests/fixtures/import_internal.py\"),
        capabilities=[\"event.publish:telemetry\"]
    )
    assert result.exit_code != 0
```

Write the test FIRST. Watch it fail. Then implement until it passes. This is not optional.

### Rule 6 — Build the Scheduler (ADR-005)

The current V1 Coordinator is a `while` loop. ADR-005 describes a bifurcated clock with two modes:

**Virtual-Time Mode**: The scheduler advances a logical tick counter. If a provider is slow, the scheduler waits. This guarantees deterministic replay — every provider sees the same tick sequence regardless of hardware speed.

**Wall-Time Mode**: The scheduler runs in real-time. If a provider misses a deadline, the scheduler drops its output and advances. This is for hardware-in-the-loop testing where real devices expect real-time responses.

**Implementation requirements**:
- A `Scheduler` trait/ABC with `virtual_time()` and `wall_time()` implementations
- Virtual-time mode: logical tick counter, tick duration is a configuration parameter
- Wall-time mode: `time.perf_counter_ns()` based, deadline tracking per provider, frame-drop counting
- Mode selection via experiment configuration
- All state transitions and timing decisions are recorded for replay
- Tests: deterministic replay produces identical tick sequences in virtual-time mode

### Rule 7 — Build the Real Capability Engine (ADR-003 + ADR-006)

The current implementation uses Python proxy wrappers. The ADRs describe signed manifests and OS-level enforcement. Build it in stages:

**Stage 1 — Signed Manifests**:
- `CapabilityManifest` gains a `signature: bytes` field
- Manifests are signed with Ed25519 at build/registration time
- The runtime verifies the signature before loading a provider
- A `vireon manifest sign` CLI command for provider authors
- Test: a tampered manifest fails to load

**Stage 2 — Process Isolation**:
- Providers run in child processes (already partially implemented via `popen_sandboxed`)
- Communication ONLY through defined IPC channels (stdin/stdout JSON-RPC, or shared memory)
- The parent process holds all real state; the child holds only what the manifest allows
- Test: a provider that tries to open a file, make a network connection, or import vireon internals is killed

**Stage 3 — OS-Level Enforcement (ADR-006)**:
- Use `seccomp-bpf` (via `python-seccomp` or the `seccomp` crate) to restrict syscalls
- Use Linux namespaces (via `unshare` or the native Python `os.unshare` if available) for filesystem and network isolation
- The capability manifest maps to a seccomp filter profile
- eBPF is used for monitoring/auditing, not enforcement (seccomp handles enforcement)
- Test: a provider that makes a disallowed syscall gets SIGSYS

**Stage 4 — eBPF Dynamic Enforcement**:
- Use eBPF programs attached to cgroups to dynamically allow/deny resource access
- This is the full ADR-006 vision
- Only needed if Stage 3 is insufficient

### Rule 8 — Build the Data Plane (ADR-002 + ADR-007 + ADR-015)

The ADRs describe gRPC for control, shared memory for data, and lock-free ring buffers for high-throughput telemetry.

**Control Plane (gRPC)**:
- Provider registration, capability negotiation, lifecycle management (init/tick/shutdown)
- Streaming RPCs for real-time telemetry where latency tolerance is higher (~1ms)
- Define `.proto` files in `Vireon/schemas/`
- Generate Python and Rust stubs
- Test: a provider registers via gRPC, receives ticks, publishes telemetry

**Data Plane (Shared Memory)**:
- `multiprocessing.shared_memory` (Python) or `shm_open`/`mmap` (Rust) for zero-copy data sharing
- FlatBuffers or Cap'n Proto for zero-copy deserialization (add `flatbuffers` or `capnp` to dependencies)
- Ring buffer implementation: `Vireon/crates/ringbuf/` (Rust, compiled to Python extension)
- SPSC (single-producer, single-consumer) semantics with overwrite for slow consumers
- Test: producer writes 1M samples, consumer reads without allocation, no data loss when consumer keeps up

**Integration**:
- Control plane runs on gRPC (low bandwidth, high reliability)
- Data plane runs on shared memory (high bandwidth, best-effort)
- The scheduler coordinates both
- Test: end-to-end — provider registers via gRPC, receives clock via shared memory, writes telemetry to ring buffer, consumer reads at 30kHz+

### Rule 9 — Build the CRDT State Store (ADR-008 + ADR-011)

The ADR describes conflict-free replicated data types for the global state graph. This eliminates cross-boundary locks and enables deterministic convergence.

**Implementation approach**:
- Start with a `GCounter` (grow-only counter) and `LWWRegister` (last-writer-wins register)
- Build a `StateStore` backed by CRDTs instead of a `threading.Lock` + `dict`
- Every state mutation produces an operation that is appended to a log (not overwritten)
- The log is the source of truth for replay
- Epoched garbage collection (ADR-011) removes operations that have been merged by all providers

**When this is actually needed**: CRDTs solve distributed state consistency. If all providers run in a single process with a single state store, a simple mutex is correct and simpler. CRDTs become necessary when:
- Providers run in separate processes with their own state views
- The state needs to be replicated (e.g., for distributed simulation)
- You want lock-free concurrent access from multiple providers

**Recommendation**: Build the simple `Lock + dict` StateStore first, make it work, write the tests. Then implement the CRDT version as an alternative backend that passes the same test suite. This gives you a working system immediately and a path to the full ADR vision.

### Rule 10 — Build Real Evidence Integrity (ADR-014)

The current evidence pipeline uses SHA-256 hashing and calls it a \"signature.\" ADR-014 describes Merkle tree cryptographic tracing. Build it:

**Stage 1 — Real Signatures**:
- Replace `SHA-256(data).hexdigest()` with `Ed25519.sign(private_key, data)`
- Generate a keypair at experiment initialization, include the public key in the `ReplayPackage`
- Verification: `Ed25519.verify(public_key, signature, data)`
- Test: a tampered evidence package fails verification

**Stage 2 — Merkle Tree**:
- Each state transition or event is a leaf in a Merkle tree
- The tree root is included in the `SignedEvidencePackage`
- Verification: recompute the tree from the replay package and compare roots
- This provides O(log n) verification of any individual event
- Test: altering a single event changes the Merkle root

**Stage 3 — Trace Bundles**:
- Bundle the Merkle root, signature, replay data, and provider versions into a `TraceBundle`
- Serialize to a canonical format (CBOR recommended — deterministic, binary, self-describing)
- The bundle is the artifact that gets published, archived, and verified

---

## PART III: NEURODSL RULES

### Rule 11 — NeuroDSL Is a Core Runtime Component

NeuroDSL lives in `Vireon/crates/neurodsl/` and is built as part of the Vireon release. It is not a separate project. It is to Vireon what the JVM is to Java — the execution engine for a domain-specific language.

### Rule 12 — Complete the Language

The current 9 instructions are a starting point. The ADRs and documentation reference richer capabilities. Build the language the examples imply:

**Phase 1 — Fix What Exists (Week 1-2)**:
- Source locations in lexer (line, column spans)
- Labels for jump targets (symbolic addressing)
- Comments (`//` line comments)
- Implement SHAPE and WAIT in the VM (store shape data, actual timing)
- Fix the invalid example file
- Write the formal specification (`grammar.md`)
- Error types implement `std::error::Error` and `Display`

**Phase 2 — Make It Usable (Week 3-4)**:
- Variables: `LET <name> = <value>` and `<name>` in expressions
- Arithmetic expressions: `SET_AMP (base_amp + offset * 2)`
- Named regions: `REGION cortex CHANNELS 8 SAMPLE_RATE 250`
- Conditional blocks: `IF memory[0] > 100 THEN ... END_IF`
- String identifiers for memory: `READ_SENSOR eeg_raw INTO raw_buffer`

**Phase 3 — Make It Powerful (Week 5-8)**:
- Functions: `FUNCTION apply_stimulus(amp, freq, duration) ... END_FUNCTION`
- Timelines: `TIMELINE rest_phase WAIT 500ms END_TIMELINE`
- Safety annotations: `@safety(max_amp=5.0, max_freq=100)` on functions
- Import/export: `IMPORT \"standard_protocols.ndsl\"`
- Types: `STIM_PATTERN` composite type with amplitude, frequency, duration, waveform

**Phase 4 — Make It Fast (Week 9-12)**:
- JIT compilation for hot loops (cranelift or wasmtime)
- Async I/O for READ_SENSOR (non-blocking EEG data ingestion)
- Multi-threaded execution for parallel region stimulation

### Rule 13 — NeuroDSL Specification Is a Deliverable

The `specification/grammar.md` file currently contains one line. It must contain:
- Formal BNF or PEG grammar for the complete language
- Type system rules
- Execution semantics for every instruction
- Memory model and safety invariants
- Opcode reference table with byte-level encoding
- Integration protocol (how the Python runtime calls the Rust VM)
- Security model (what the VM guarantees, what it doesn't)

This document is the contract between the compiler, the VM, and the runtime. It must be complete before Phase 3 features are added.

### Rule 14 — Test Floor

Current: 6 tests (2 mocked). Required:
- 100% opcode coverage (every instruction has positive + negative tests)
- Every security limit has a boundary test
- Parser error recovery tests (multiple errors reported)
- Source location accuracy tests
- Cross-platform reproducibility test (same bytecode → same execution on different platforms)
- Gas exhaustion test
- VM state serialization/deserialization test
- Python extension integration test (actual Rust, not mocks)
- Minimum: 50 tests before Phase 3

---

## PART IV: SECURITY RULES

### Rule 15 — Cryptographic Primitives Are Real or Clearly Labeled

For the production runtime (Vireon):
- All signatures use Ed25519 (via `cryptography` library or `ed25519-dalek` in Rust)
- All symmetric encryption uses AES-256-GCM with proper AAD
- All key derivation uses HKDF with a random salt
- All hashes use SHA-256 or SHA-3

For the educational platform (vireon-lab):
- Intentionally weak crypto is permitted for CTF/educational modules
- Must be in files or modules prefixed with `educational_` or `ctf_`
- Must have a docstring: \"INTENTIONALLY INSECURE — for educational purposes only. Do not use in production.\"
- Must raise a warning at import time when `VIREON_PRODUCTION_MODE=1` is set

### Rule 16 — No Secrets in the Repository
- Generate TLS certificates at Docker build time or runtime, not committed to git
- Add `*.pem`, `*.key`, `*.p12` to `.gitignore`
- Use environment variables or a secret manager for API keys
- The MCP secret key is derived from a machine-specific keyring entry, not a plaintext file
- If the old certificates are in git history, use BFG Repo Cleaner to remove them

### Rule 17 — Threat Models Reflect Reality

Update the threat models to match what actually exists, not the ADR vision:

| Claim | Reality | Action |
|---|---|---|
| \"Zero-trust provider isolation\" | Application-level proxy wrappers + bubblewrap (Linux only) | Document honestly. Build OS-level enforcement per Rule 7. |
| \"Cryptographic trace bundles\" | SHA-256 hash of evidence package | Implement Ed25519 + Merkle tree per Rule 10. |
| \"Fail-closed capability enforcement\" | Python `if cap not in manifest: raise` | Implement real enforcement per Rule 7. |
| \"eBPF sandbox\" | Not implemented | Mark as Phase D in roadmap. |
| \"CRDT state store\" | `threading.Lock` + `dict` | Implement per Rule 9. |

The threat model is a living document. Update it as each ADR is implemented.

---

## PART V: INFRASTRUCTURE RULES

### Rule 18 — The Build Must Work

A fresh clone on Ubuntu 22.04 must pass:

```bash
git clone https://github.com/SaadiMalik1/Vireon.git && cd Vireon
git submodule update --init --recursive   # pulls in crates/
make install    # installs Python deps, builds Rust extensions
make lint       # ruff, mypy, cargo clippy, cargo fmt --check
make test       # pytest + cargo test --all
```

If this fails, nothing else matters. Fix it before any feature work.

### Rule 19 — One Makefile Per Repo

**Vireon/Makefile**:
| Target | Purpose |
|--------|---------|
| `make install` | pip install -e \".[dev]\" + maturin develop for neurodsl |
| `make test` | pytest + cargo test --all |
| `make test-integration` | end-to-end provider lifecycle tests |
| `make lint` | ruff check + mypy + cargo clippy + cargo fmt --check |
| `make docs` | mkdocs build |
| `make sbom` | cyclonedx-py generate |
| `make docker` | docker build -f docker/Dockerfile . |
| `make clean` | remove build artifacts |

**vireon-lab/Makefile**:
| Target | Purpose |
|--------|---------|
| `make install` | pip install -e \".[dev]\" |
| `make test` | pytest |
| `make demo` | run the Streamlit dashboard with sample data |
| `make lint` | ruff check + mypy |
| `make docs` | mkdocs build |

### Rule 20 — CI Pipeline

**Vireon CI** (`.github/workflows/ci.yml`):
```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: \"3.11\" }
      - uses: dtolnay/rust-toolchain@nightly
      - run: make lint

  test-python:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: \"3.11\" }
      - run: make install
      - run: make test

  test-rust:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: dtolnay/rust-toolchain@nightly
      - run: cd crates/neurodsl && cargo test --all --locked

  test-integration:
    runs-on: ubuntu-latest
    needs: [test-python, test-rust]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: \"3.11\" }
      - run: make install
      - run: make test-integration

  security:
    runs-on: ubuntu-latest
    needs: lint
    steps:
      - uses: actions/checkout@v4
      - uses: aquasecurity/trivy-action@master
        with: { scan-type: \"fs\" }
      - run: pip install pip-audit && pip-audit
```

**vireon-lab CI** (`.github/workflows/ci.yml`):
```yaml
jobs:
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with: { python-version: \"3.11\" }
      - run: make install
      - run: make lint
      - run: make test
```

No `mv tmp_* ../`. No stale action versions. No missing submodules.

### Rule 21 — Lock Files Are Required
- `requirements-lock.txt` (generated via `pip-compile` or `pip freeze`)
- `Cargo.lock` (committed, not gitignored)
- Docker images pinned by digest in CI
- No `pip install` without `--require-hashes` or a lock file

### Rule 22 — Release Process

When you tag `v2.0.0`:
1. CI builds the wheel and Rust extension
2. CI runs the full test suite
3. CI publishes `vireon` to PyPI
4. CI builds and pushes the Docker image to `ghcr.io/vireon/vireon:v2.0.0`
5. CI generates and publishes the SBOM
6. CI builds and deploys documentation to GitHub Pages
7. A GitHub Release is created with the changelog

Same process for `vireon-lab`. Same process for `vireon-neuro-dsl`.

---

## PART VI: DOCUMENTATION RULES

### Rule 23 — READMEs Describe What Exists

**Vireon/README.md**:
- One paragraph: what Vireon is (neurotechnology security simulation runtime)
- Prerequisites and installation (`git clone && make install`)
- Quick start code example (5 lines)
- Architecture overview with ASCII diagram
- Link to full documentation
- Link to vireon-lab for educational content

**vireon-lab/README.md**:
- One paragraph: what vireon-lab is (educational platform for learning neurosecurity)
- Screenshot of the dashboard
- Installation and `make demo`
- Link to tutorials and knowledge base
- \"Built on Vireon\" with link

No redirect stubs. Both READMEs are self-contained.

### Rule 24 — ADR Status Must Be Honest

| Status | Meaning |
|--------|----------|
| `Accepted — Implemented` | Code ships, tests pass |
| `Accepted — In Progress` | PR is open with tests |
| `Accepted — Deferred` | Planned but not started. Must include estimated phase (A/B/C/D/E from Rule 4). |
| `Proposed` | Under discussion. |
| `Superseded by ADR-XXX` | Replaced. Must link to replacement. |

Currently all 15 say `Accepted`. Update them:
- ADR-004, ADR-009 → `Accepted — Deferred (Phase A)`
- ADR-001, ADR-003, ADR-005, ADR-013 → `Accepted — Deferred (Phase B)`
- ADR-002, ADR-007, ADR-015 → `Accepted — Deferred (Phase C)`
- ADR-006, ADR-008, ADR-012, ADR-011 → `Accepted — Deferred (Phase D)`
- ADR-010, ADR-014 → `Accepted — Deferred (Phase E)`

As you implement each ADR, update its status to `Accepted — Implemented`.

### Rule 25 — Guides Must Work

Every step in the Developer Guide, Integration Guide, Migration Guide, and Operations Guide must be executable on a fresh machine. If a guide references a file that doesn't exist, the guide is broken. Fix the file or fix the reference before any other documentation work.

### Rule 26 — Complete the Code of Conduct

Restore the full Contributor Covenant v2.x text. The current version is truncated at line 58, missing enforcement guidelines and attribution. An unenforceable CoC is worse than none.

---

## PART VII: CODE QUALITY RULES

### Rule 27 — Decompose the DigitalTwin

The DigitalTwin is a God-class. Decompose it into focused components:

```python
@dataclass
class SignalState:
    buffer: np.ndarray
    sample_rate: float
    channel_names: list[str]
    current_index: int

@dataclass  
class PhysicsState:
    stimulation_amplitude: float
    stimulation_frequency: float
    electrode_impedance: dict[int, float]
    tissue_contact_resistance: float

@dataclass
class BatteryState:
    charge_mah: float
    capacity_mah: float
    temperature_c: float
    discharge_rate: float  # Peukert's Law

@dataclass
class ClinicalState:
    niss_score: float  # 0-10
    hazard_state: HazardState  # ISO 14971
    iso_severity: SeverityLevel
    tissue_damage_risk: float

@dataclass
class SimClock:
    mode: ClockMode  # VIRTUAL | WALL
    tick: int
    wall_start_ns: int
    virtual_dt_ms: float

@dataclass
class DigitalTwin:
    signal: SignalState
    physics: PhysicsState
    battery: BatteryState
    clinical: ClinicalState
    clock: SimClock
    device_config: DeviceConfig
```

Each component gets its own file, its own tests, and its own documentation. The `DigitalTwin` becomes a thin composition layer.

### Rule 28 — EventBus: Pick One Model

Current: synchronous publish + ThreadPoolExecutor dispatch (worst of both worlds).

**Recommended: Asyncio**.
```python
class AsyncEventBus(IEventBus):
    async def publish(self, event: Event) -> None:
        for handler in self._subscribers[event.topic]:
            await handler(event)  # runs on the event loop
    
    async def subscribe(self, topic: str, handler: Callable) -> None:
        self._subscribers[topic].append(handler)
```

This enables:
- True concurrency for I/O-bound handlers (network, file, device I/O)
- Predictable ordering (single event loop)
- Native integration with `asyncio` providers
- No GIL contention for I/O-bound work
- Easy testing with `asyncio.test` utilities

CPU-bound work (signal processing, ML inference) runs in a `ProcessPoolExecutor` (bypasses the GIL).

### Rule 29 — Tests Before Features

For every module you write, the test file is in the same PR. No exceptions.
- Minimum 80% line coverage for new code
- Every public function has at least one test
- Integration tests for: provider lifecycle, event bus round-trip, config loading, replay, scheduler
- No mocked integration tests (the NeuroDSL Python tests that mock the Rust extension are unacceptable)

### Rule 30 — Type Strictness
- All new Python code passes `mypy --strict`
- `# type: ignore` requires a comment explaining why
- Tighten `ignore_missing_imports` to only untyped third-party libraries
- All Rust code passes `cargo clippy -- -D warnings`

### Rule 31 — No TODO Without a Ticket
```python
# TODO(#142): Replace SHA-256 hash with Ed25519 signature per ADR-014
```
No issue number = invalid TODO. Create the issue or fix the code.

---

## PART VIII: GOVERNANCE RULES

### Rule 32 — Resolve the Approval Conflict
- Standard PRs: 1 approval
- Architectural changes (ADR modifications, SDK interface changes, security changes): 2 approvals
- Document this in GOVERNANCE.md. Reference it from CONTRIBUTING.md.

### Rule 33 — Add DCO
Use the `probot/dco` bot. 30 minutes of work. Non-negotiable for an Apache 2.0 project.

### Rule 34 — CODEOWNERS in Both Repos

**Vireon/CODEOWNERS**:
```
* @SaadiMalik1
/crates/neurodsl/ @SaadiMalik1
/src/vireon/sdk/ @SaadiMalik1
/docs/adr/ @SaadiMalik1
```

**vireon-lab/CODEOWNERS**:
```
* @SaadiMalik1
/vireon_lab/providers/clinical/ @SaadiMalik1
/vireon_lab/knowledge/ @SaadiMalik1
```

### Rule 35 — PGP Key for Security Reports
Generate a PGP key pair. Publish the public key in the repo. Update SECURITY.md to reference it. This enables encrypted vulnerability disclosure.

---

## PART IX: REALISTIC ROADMAP

### Rule 36 — Build in Phases, Test Each Phase

| Phase | Duration | ADRs | Deliverable |
|-------|----------|------|-------------|
| **Foundation** | Weeks 1-3 | None | Working build, CI, tests, two-repo structure, lock files |
| **A: Determinism** | Weeks 4-6 | ADR-004, ADR-009 | Owned clock, owned RNG, FFI error mapping, deterministic replay tests |
| **B: Core Runtime** | Weeks 7-14 | ADR-001, ADR-003, ADR-005, ADR-013 | Real scheduler, signed manifests, kernel orchestrator, compiler pinning |
| **C: Data Plane** | Weeks 15-22 | ADR-002, ADR-007, ADR-015 | gRPC control, shared memory, ring buffers, 30kHz telemetry |
| **D: State & Security** | Weeks 23-34 | ADR-006, ADR-008, ADR-012, ADR-011 | eBPF enforcement, CRDT state, memory protections |
| **E: Integrity** | Weeks 35-40 | ADR-010, ADR-014 | Merkle tracing, hardware watchdog, signed trace bundles |
| **NeuroDSL** | Weeks 6-20 (parallel) | — | Source locations, labels, spec, 50+ tests, Phase 1-3 language features |
| **vireon-lab** | Weeks 3-8 (parallel) | — | Working demos, tutorials, dashboard, knowledge base |

Total: ~40 weeks (~10 months) for a single engineer working full-time on Vireon. NeuroDSL and vireon-lab run in parallel.

### Rule 37 — Each Phase Ends With a Release

- After Foundation: `v1.1.0` — working build, CI, cleaned-up codebase
- After Phase A: `v2.0.0-alpha.1` — deterministic replay
- After Phase B: `v2.0.0-alpha.2` — real scheduler + capability engine
- After Phase C: `v2.0.0-beta.1` — high-performance data plane
- After Phase D: `v2.0.0-beta.2` — OS-level security
- After Phase E: `v2.0.0` — full ADR implementation

Each release has a changelog, passes all tests, and publishes to PyPI.

### Rule 38 — The Constitution Is a Living Document

The Constitution (if one exists as a separate document from the ADRs) is reviewed after each phase. If a constitutional principle conflicts with what was built, the principle is updated to match reality — not the other way around. The code is the source of truth. Documentation describes the code.

---

## ENFORCEMENT

**These are not suggestions. They are the engineering contract for building what the ADRs describe.**

The order matters. Phase Foundation (Rules 18-22) is the prerequisite for everything else. Do not begin Phase A until a fresh clone passes `make install && make test`.

**The metric of success**: Can a researcher clone Vireon, implement a custom provider, run a deterministic simulation, and verify the evidence package — all within one afternoon? When that answer is yes, the foundation is solid. The ADRs describe the path to get there.

**The metric for the ADRs**: An ADR is not \"accepted\" when it's written. An ADR is accepted when the code ships and the tests pass. Update the status accordingly.