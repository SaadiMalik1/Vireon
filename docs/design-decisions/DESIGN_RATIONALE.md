# VIREON Ecosystem Design Rationale

This document explains the "Why" behind VIREON's foundational architectural decisions. It serves as the philosophical anchor for the ecosystem, preserving intent against future architectural drift.

## 1. Why a Provider Model vs. Monolith?
**Decision:** VIREON uses a strict dependency injection model where core orchestration (`vireon.runtime`) knows nothing about specific physics or hardware, relying instead on interchangeable `providers/`.
**Rationale:** Neurotechnology hardware is highly proprietary and heterogeneous. If VIREON were a monolith with hardcoded physics or firmware rules, vendors (e.g., Neuralink, Paradromics) could not use it without exposing their proprietary IP or forking the codebase. The provider model allows vendors to implement closed-source binary plugins (via Subprocess providers) while leveraging the open-source orchestrator.

## 2. Why Split Python and Rust?
**Decision:** The ecosystem is strictly bifurcated: Python handles orchestration, plugins, and UI (`vireon`, `vireon-lab`), while Rust handles the simulation engine (`neurodsl`).
**Rationale:** Python provides the unmatched ecosystem velocity required for data science, AI model integration, and rapid plugin development. However, simulating thousands of neurons at 30kHz requires extreme parallel performance, deterministic floating-point operations, and memory safety. Rust (`neurodsl`) guarantees these attributes. Forcing everything into one language would yield either a slow simulator (Python-only) or an impenetrable, hard-to-extend ecosystem (Rust-only).

## 3. Why Capability-Based Security?
**Decision:** Plugins and providers must declare capabilities (e.g., memory access, network access) to the `PluginRegistry` before being loaded.
**Rationale:** A medical-grade validation platform operates in a Zero Trust environment. A third-party neural decoder plugin cannot be allowed arbitrary access to the host system or the simulated patient's cryptographic keys. Capability-based security maps directly to FDA postmarket cybersecurity guidelines.

## 4. Why Deterministic Replay?
**Decision:** The entire ecosystem is mandated to operate deterministically based on a single master cryptographic seed propagated by the `SimulationBuilder`.
**Rationale:** Without absolute determinism, a bug in a vendor's firmware that only appears during a specific adversarial noise spike cannot be consistently reproduced. Determinism elevates VIREON from a "testing tool" to a "mathematical validation standard" suitable for academic peer review and FDA submission.
