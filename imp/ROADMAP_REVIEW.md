# Roadmap Review: Vireon Ecosystem

> An independent assessment of the implied roadmap derived from 15 Architecture Decision Records, evaluated against the actual implementation state.

---

## 1. Claimed Architecture (from 15 ADRs)

The ADRs collectively describe an ambitious systems architecture:

| ADR | Feature | Scope |
|-----|---------|-------|
| ADR-001 | Standalone Validation OS kernel with providers as untrusted user-space processes | Kernel architecture |
| ADR-002 | gRPC control plane + lock-free shared memory data plane at 30kHz+ | Control/data plane split |
| ADR-003 | Cryptographically signed capability manifests, fail-closed enforcement | Security model |
| ADR-004 | Owned clocks, owned RNG, compiler-pinned determinism, signed trace bundles | Determinism guarantees |
| ADR-005 | Virtual-time and wall-time bifurcated clock scheduler | Temporal control |
| ADR-006 | OS-level enforcement via eBPF + cgroups | Capability enforcement |
| ADR-007 | Direct memory sharing between kernel and providers (zero-copy pointer handoff) | Memory architecture |
| ADR-008 | Conflict-free replicated data types (CRDTs) for global state | Distributed state |
| ADR-009 | Consistent Rust/Python error handling across FFI boundary | Interop layer |
| ADR-010 | External hardware watchdog for kernel stalls | Reliability |
| ADR-011 | Epoched garbage collection for CRDT tombstones | Memory management |
| ADR-012 | Unidirectional memory protections between trust boundaries | Memory safety |
| ADR-013 | Compiler-level determinism guarantees (beyond ADR-004) | Compiler toolchain |
| ADR-014 | Merkle tree hash chain integrity for execution traces | Cryptographic tracing |
| ADR-015 | SPSC ring buffers with overwrite semantics for high-frequency data | Data plane transport |

Taken together, these ADRs describe a bespoke operating system kernel with:

- A trust-boundary architecture separating a validation kernel from untrusted BCI provider processes
- Lock-free, zero-copy inter-process communication at real-time frequencies (30kHz+)
- Cryptographic integrity guarantees at every layer (manifests, traces, evidence bundles)
- A deterministic execution model with owned clocks, owned RNG, and compiler-pinned semantics
- OS-level capability enforcement via eBPF and cgroups
- A custom DSL (NeuroDSL) with a virtual machine
- A CRDT-based replicated state store with epoched garbage collection
- Hardware watchdog integration for hard-real-time reliability guarantees

This is, without exaggeration, the architecture of a safety-critical real-time operating system with cryptographic attestation — comparable in scope to aerospace or medical device certification platforms.

---

## 2. Reality Check

None of these ADRs have working implementations. The actual codebase state is:

| Claimed Feature | Actual Implementation |
|-----------------|----------------------|
| Standalone validation OS kernel | Python synchronous `EventBus` with `threading.Lock` for state |
| Lock-free shared memory data plane at 30kHz+ | JSON-RPC over stdin/stdout |
| Cryptographically signed capability manifests | Unimplemented |
| Deterministic execution with owned clocks/RNG | Unimplemented |
| Bifurcated clock scheduler | No scheduler exists |
| eBPF capability enforcement | No eBPF code exists anywhere in the repository |
| Zero-copy pointer handoff | No shared memory region exists |
| CRDT state store | No CRDT implementation exists |
| FFI error mapping (Rust/Python) | No Rust code exists in the repository |
| Hardware watchdog | Unimplemented |
| Epoched CRDT GC | Unimplemented (no CRDT to collect) |
| Unidirectional memory protections | Unimplemented |
| Compiler-pinned determinism | Unimplemented; no custom compiler exists |
| Merkle tree cryptographic tracing | Unimplemented |
| Non-blocking ring buffers (SPSC) | Unimplemented; no ring buffer exists |

### Additional Ground Truth

- **NeuroDSL VM**: 256 bytes of memory and 9 instructions — a teaching demo, not a production VM.
- **Evidence pipeline**: Uses SHA-256 hash (no key, no HMAC, no signature) as a "cryptographic signature" — this provides no authenticity guarantee.
- **Neuroethics guardrails**: Unvalidated DSM-5 mapping and NISS scoring — taxonomic exercises with no clinical validation.
- **Vendor SDK**: A set of Python abstract classes with no implementation guides, no FlatBuffer schemas (the directory doesn't exist), and no reference vendor integration.
- **CI/CD**: Broken. Missing `.gitmodules`, no build system at workspace root, tests that don't run.
- **V1→V2 migration**: ~77% of the runtime is deprecated shim code with no migration timeline.

---

## 3. Roadmap Assessment

### 3.1 Scale Mismatch

The 15 ADRs describe **3–5 years of systems engineering work** requiring a team of **5–10 senior engineers** with expertise in:

- Operating systems / kernel development
- Real-time systems (hard real-time at 30kHz+)
- Cryptography (signatures, Merkle trees, HSMs)
- Formal methods / deterministic execution
- eBPF / Linux kernel internals
- CRDTs / distributed systems theory
- Embedded systems / hardware integration (watchdog)
- Compiler toolchain development

This project has **1 primary author**.

### 3.2 Implementation Rate

Based on commit history, code completeness, and the gap between design and implementation, the current implementation rate suggests the ADRs are **aspirational, not planned**. There is no evidence of a phased implementation strategy, no dependencies between ADRs mapped, and no incremental delivery path.

### 3.3 Missing Roadmap Essentials

- **No milestones**: No definition of what "done" looks like for any phase
- **No timeline**: No dates, no sprint cadence, no release cadence
- **No resource allocation**: No team plan, no funding model, no contributor growth path
- **No V1→V2 completion criteria**: The migration has been ongoing but there is no definition of what remains or when it will be complete
- **No dependency graph**: The ADRs have implicit dependencies (e.g., ring buffers depend on shared memory, Merkle trees depend on deterministic execution) but these are not documented
- **No risk register**: No identification of technical risks, no mitigation strategies

---

## 4. A Realistic 18–24 Month Roadmap

If the project is to become functional, it must abandon the ADR-described architecture as a near-term goal and instead focus on building a solid foundation. The following is the **minimum viable path** to a functional neurotechnology security simulation framework:

### Phase 1: Foundation Repair (Months 1–3)

**Goal:** The project builds, tests pass, and a new contributor can onboard.

- Fix broken CI/CD pipeline
- Add missing `.gitmodules` or migrate dependencies
- Create a working build system at the workspace root (hatch, uv, or similar)
- Complete V2 migration with concrete completion criteria
- Delete all deprecated V1 shims
- Write onboarding documentation that actually works
- Add CLA/DCO for contributors

**Deliverables:** Green CI, buildable workspace, working onboarding guide, V1 code deleted.

### Phase 2: Core Functionality (Months 4–6)

**Goal:** The system is testable, benchmarkable, and publishable.

- Implement real integration tests (currently absent)
- Create benchmark suite for the event bus and data pipeline
- Publish vireon and vireon-lab to PyPI
- Fix circular dependency between vireon and vireon-lab
- Implement async event bus (replacing synchronous `EventBus` + `threading.Lock`)
- Document all public APIs with working examples

**Deliverables:** PyPI packages, test coverage > 60%, benchmark baseline, async event bus.

### Phase 3: Real Security (Months 7–9)

**Goal:** The security model works, even if at application level rather than OS level.

- Implement real capability enforcement (application-level with proper access control)
- Replace SHA-256 hashing with actual cryptographic signatures (Ed25519 or similar)
- Implement evidence pipeline with verifiable, signed evidence bundles
- Add proper TLS certificate management (remove certs from repo)
- Implement provider sandboxing (at minimum, process isolation on all platforms)

**Deliverables:** Working capability enforcement, signed evidence, proper TLS, sandboxed providers.

### Phase 4: NeuroDSL Maturation (Months 10–12)

**Goal:** NeuroDSL becomes a real, usable DSL with a formal specification.

- Add source locations to NeuroDSL programs
- Add labels and named instructions
- Expand VM instruction set beyond 9 instructions
- Write a formal specification document
- Create a reference implementation with test vectors
- Integrate NeuroDSL with the evidence pipeline

**Deliverables:** Formal NeuroDSL spec, expanded VM, test vectors, pipeline integration.

### Phase 5: Performance Foundation (Months 13–18)

**Goal:** The data plane moves beyond JSON-RPC over stdin/stdout.

- Implement shared memory data plane (Python `multiprocessing.shared_memory` or similar)
- Implement real scheduler (at minimum, a priority queue with timing guarantees)
- Replace JSON-RPC with binary serialization (protobuf or FlatBuffers)
- Create actual FlatBuffer/protobuf schemas (the directory currently doesn't exist)
- Benchmark data plane latency and throughput

**Deliverables:** Shared memory IPC, working scheduler, binary serialization, performance benchmarks.

### Phase 6: Integration Readiness (Months 19–24)

**Goal:** External parties can integrate with the system.

- Implement gRPC control plane (even if the data plane remains simpler)
- Create vendor integration SDK with working examples and implementation guide
- Build reference vendor integration (at least one, fully functional)
- Create SBOM generation in CI
- Write regulatory compliance documentation (actual artifacts, not simulated ones)
- Publish at least one research paper demonstrating the system in use

**Deliverables:** gRPC API, vendor SDK with reference integration, SBOM, research paper.

---

## 5. What the ADRs Actually Represent

The 15 ADRs describe features that would come **after** the Phase 1–6 foundation is solid. Specifically:

| ADR | Earliest Realistic Phase |
|-----|--------------------------|
| ADR-001 (Kernel) | Phase 7+ (Year 3+) — requires funded team |
| ADR-002 (Control/Data Plane) | Phase 5–6 (data plane), Phase 7+ (gRPC at claimed performance) |
| ADR-003 (Capability Manifests) | Phase 3 (app-level), Phase 7+ (cryptographic, fail-closed) |
| ADR-004 (Deterministic Execution) | Phase 7+ — requires custom runtime |
| ADR-005 (Bifurcated Clocks) | Phase 5 (basic scheduler), Phase 7+ (claimed architecture) |
| ADR-006 (eBPF Enforcement) | Phase 8+ — requires kernel-level work |
| ADR-007 (Zero-Copy) | Phase 5 (shared memory), Phase 7+ (claimed architecture) |
| ADR-008 (CRDT Store) | Phase 7+ — requires distributed architecture |
| ADR-009 (FFI Error Mapping) | Phase 7+ — requires Rust implementation |
| ADR-010 (Hardware Watchdog) | Phase 7+ — requires hardware integration |
| ADR-011 (Epoched CRDT GC) | Phase 7+ — requires CRDTs to exist |
| ADR-012 (Memory Protections) | Phase 7+ — requires OS-level work |
| ADR-013 (Compiler Pinned) | Phase 8+ — requires custom compiler |
| ADR-014 (Merkle Tracing) | Phase 6 (basic), Phase 7+ (claimed architecture) |
| ADR-015 (Ring Buffers) | Phase 5 (shared memory), Phase 7+ (claimed performance) |

---

## 6. Conclusion

The roadmap implied by the ADRs is not a roadmap — it is a **vision document** for a system that would require a funded team of 5–10 engineers working for 3–5 years. The current project has 1 author, no working CI, no build system, and 77% deprecated code. There is no path from the current state to the ADR-described state without first completing a foundational 18–24 month effort that is not described in any existing planning document.

The most critical recommendation: **write a real roadmap** with milestones, timelines, resource requirements, and completion criteria. The ADRs are good design thinking, but design without execution is documentation, not software.