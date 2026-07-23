# Security Architecture Design

## 1. Goal & Architecture Scope
VIREON provides process isolation, capability manifest validation, and neuroethics guardrails for executing third-party plugins (e.g., vendor firmware, clinical models) without risking host system integrity or data leakage.

---

## 2. Current Implementation (v1.1.0)

### 2.1 Capability Isolation Levels
- **Level 0 (In-Process Proxy):** Trusted open-source providers. Enforced via object capability proxies (`EventBusProxy`, `StateStoreProxy`) restricting topic publishing and state key access (`vireon/runtime/capability_engine.py`).
- **Level 1 (Subprocess IPC):** Isolated provider execution using child process wrappers (`vireon/sdk/subprocess_provider.py`) communicating via `stdin`/`stdout` IPC pipes.
- **Native Process Sandboxing:** `vireon/runtime/sandbox.py` invokes Linux `prctl(PR_SET_NO_NEW_PRIVS)`. Strict mode seccomp filters (`SECCOMP_MODE_STRICT`) generate Seccomp-BPF profiles.
  - *Security Disclosure:* Seccomp enforcement requires `VIREON_ENFORCE_SECCOMP=1` to be set in the host environment; otherwise, it logs a debug message and returns success. Linux-only primitive.

### 2.2 Neuroethics Guardrails & Anonymization
- **Neuroethics Constraints:** G1-G8 safety rules enforced in `vireon/runtime/guardrails.py` (e.g., G2 P300 block, G6 50Mbps bandwidth cap, G7 framing check).
- **Differential Privacy Anonymizer:** `vireon/sdk/anonymizer.py` applies temporal jitter, channel permutation, and spectral masking.

---

## 3. Proposed Specifications & Long-Term Roadmap

- **Level 2 (WASM Sandbox):** Executing black-box binaries inside a WebAssembly sandbox (e.g., `wasmtime`) without filesystem or network access (RFC-001 specification).
- **Kernel-Level eBPF Loading:** Translating YAML capability manifests into direct Linux kernel eBPF bytecode attachments (ADR-006 proposal).
- **gRPC Shared Memory Data Plane:** High-throughput shared memory IPC channels for heavy neural array streaming.
