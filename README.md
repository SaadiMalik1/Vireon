# VIREON Core Runtime & SDK

**Vendor-Neutral Neurotechnology Security Validation Framework**

> **Maturity Notice:** VIREON is currently a **Pre-Alpha Research Prototype** designed for simulated BCI testing, zero-trust sandboxing experiments, and deterministic digital twin modeling. It has not undergone third-party security audits, FDA regulatory submission, or hardware-in-the-loop validation on physical implants.

---

## 1. Current State (v1.1.0)

VIREON provides a Python/Rust runtime engine for simulating and analyzing neurotechnology workloads (BCIs, EEG streams, closed-loop DBS models):

- **Deterministic Execution:** Virtual step-dt advancement via `DeterministicClock` and multi-stream `DeterministicRNG`.
- **Process Sandboxing:** Linux `prctl(PR_SET_NO_NEW_PRIVS)` and Seccomp profile generation (`sandbox.py`).
  - *Security Disclosure:* OS-level `SECCOMP_MODE_STRICT` enforcement is disabled by default in test environments and requires `VIREON_ENFORCE_SECCOMP=1` to be set.
- **Capability Isolation:** Proxy wrappers (`EventBusProxy`, `StateStoreProxy`) enforcing topic whitelists and manifest authorization. Optional Ed25519 vendor signature verification when `trusted_public_key` is supplied.
- **NeuroDSL Engine:** Embedded Rust bytecode compiler (`forge`) and VM (`scribe`) wrapped via PyO3 C-extensions (`crates/neurodsl`).
- **Physiological Datasets & Loaders:** Comprehensive synthetic signal generators (EEG, ECG, EMG, Motor Imagery, SSVEP), standard format readers (`NPZ`, `CSV`, `EDF`), and benchmark loaders (`BCI Competition IV`, `PhysioNet`).
- **Test Suite Status:** 80 Python tests passed (`pytest`), 44 Rust tests passed (`cargo test`). Total: 124 passed, 0 failed.

---

## 2. Architecture Overview

```
                        ┌─────────────────────────────────┐
                        │      Public SDK & Interfaces    │
                        │    (IProvider, ITwin, Events)   │
                        └─────────────────┬───────────────┘
                                          │
                        ┌─────────────────▼───────────────┐
                        │        VireonOrchestrator       │
                        │  (Event Loop & Lifecycle Engine)│
                        └───────┬─────────────────┬───────┘
                                │                 │
            ┌───────────────────▼──┐           ┌──▼───────────────────┐
            │   Bifurcated Clock   │           │    State Store &     │
            │   Scheduler (ADR-005)│           │  DigitalTwin         │
            └──────────────────────┘           └──────────────────────┘
                                │
                        ┌───────▼─────────────────────────┐
                        │   NeuroDSL Execution Engine     │
                        │     (crates/neurodsl VM)        │
                        └─────────────────────────────────┘
```

---

## 3. Vision & Long-Term Roadmap

- **Kernel eBPF Loading:** Translating YAML capability manifests into direct Linux kernel eBPF bytecode attachments (ADR-006 proposal).
- **Physical HIL Integration:** Connecting digital twin software models to physical PCIe/SPI neural recording interfaces and RTOS hardware pins.
- **Zero-Knowledge Telemetry:** Implementing cryptographic zero-knowledge proof specifications (RFC-006) for anonymized clinical trial verification.

---

## 4. Prerequisites & Installation

- **Python**: 3.10+
- **Rust**: Stable toolchain (`cargo`, `rustc`)

```bash
# Clone the repository
git clone https://github.com/SaadiMalik1/Vireon.git
cd Vireon

# Build Rust extensions and install Python dependencies
.venv/bin/pip install --no-deps -e .
```

---

## 5. Verification & Testing

```bash
make test       # Runs pytest (66 tests) + cargo test --workspace (44 tests)
make lint       # Runs ruff check .
make verify     # Executes full evidence generation pipeline
```

---

## 6. Related Documentation

- **[vireon-lab](https://github.com/SaadiMalik1/vireon-lab)**: Interactive educational UI, Streamlit dashboard, and attack tutorials.
- **[Architectural Decision Records](docs/adr/)**: Specifications for system ADRs (ADR-001 through ADR-016).
- **[System Limitations](LIMITATIONS.md)** & **[Known Issues](KNOWN_ISSUES.md)**.
- **[Governance](GOVERNANCE.md)** & **[Contributing Guidelines](CONTRIBUTING.md)**.
