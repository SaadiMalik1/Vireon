# VIREON Ecosystem Evolution & Roadmap

This document outlines the evolutionary roadmap for VIREON, separating current verified capabilities from future technical ambitions.

---

## 1. Current State (v1.1.0 Pre-Alpha Prototype)

- **Runtime Kernel:** Domain-agnostic event orchestrator (`VireonOrchestrator`), virtual clock (`DeterministicClock`), priority event bus, and thread-safe key-value store with Merkle leaf accumulation.
- **Provider SDK:** `vireon.sdk` v1.1.0 with V1 provider interfaces (`IPhysicsProviderV1`, `IDynamicsProviderV1`, `IIDSProviderV1`, `IClinicalProviderV1`, `IPowerProviderV1`).
- **Sandboxing & Capability Engine:** Process isolation via Linux `prctl(PR_SET_NO_NEW_PRIVS)` and Seccomp BPF profile generation (requires `VIREON_ENFORCE_SECCOMP=1`). Capability proxies for `EventBus` and `StateStore`.
- **NeuroDSL Engine:** Embedded Rust bytecode compiler (`forge`) and VM (`scribe`) wrapped via PyO3 C-extensions (`crates/neurodsl`).
- **Test Suite Status:** 66 Python tests passed, 44 Rust tests passed (110 total, 0 failed).

---

## 2. Near-Term Roadmap (6-12 Months)

- **Architecture:** Complete zero-copy shared memory SPSC ring buffer streaming between Python runtime and Rust `neurodsl` VM.
- **Security:** Kernel-level eBPF bytecode attachments (ADR-006 proposal) and Wasmtime sandbox module (RFC-001 specification).
- **DevOps:** Automated SBOM generation (CycloneDX) and signed evidence bundle releases.

---

## 3. Long-Term Vision (2-5 Years)

- **Academic & Regulatory Integration:** Submitting computational model validation evidence frameworks for FDA computational modeling (ASME V&V 40) research.
- **GPU Acceleration:** Sub-cellular modeling and large-scale neural dynamics utilizing GPU offloading (CUDA/Metal) in the `neurodsl` engine.
- **Cloud Simulation:** Managed cloud control plane enabling Monte Carlo simulations across virtual patient cohorts.
