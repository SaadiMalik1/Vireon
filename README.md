# VIREON Runtime & SDK

**Vendor-Neutral Neurotechnology Security Validation Framework**

VIREON is the core runtime engine for simulating, analyzing, and validating neurotechnology systems (BCIs, EEG devices, DBS closed-loop implants). It provides a deterministic execution environment, process isolation, neuroethics guardrails, and cryptographic evidence tracing.

---

## Architecture Overview

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
            │   Scheduler (ADR-005)│           │  DigitalTwin (Rule 27)│
            └──────────────────────┘           └──────────────────────┘
                                │
                        ┌───────▼─────────────────────────┐
                        │   NeuroDSL Execution Engine     │
                        │     (crates/neurodsl VM)        │
                        └─────────────────────────────────┘
```

---

## Prerequisites & Installation

- **Python**: 3.10+
- **Rust**: Stable toolchain (`cargo`, `rustc`)

```bash
# Clone the repository
git clone https://github.com/SaadiMalik1/Vireon.git
cd Vireon

# Build Rust extensions and install Python dependencies
make install
```

---

## Quick Start

```python
from vireon.runtime.twin import DigitalTwin
from vireon.runtime.event_bus import EventBus
from vireon.sdk.events import Event

# Initialize the Digital Twin state composition
twin = DigitalTwin(device_id="openbci_cyton", sample_rate=250)

# Initialize Event Bus
bus = EventBus()

def telemetry_handler(event: Event):
    print(f"[{event.timestamp}s] Received {event.topic}: {event.data}")

bus.subscribe("telemetry.chunk", telemetry_handler)

# Advance simulation clock
twin.set_sim_clock(0.004)
bus.publish(Event(topic="telemetry.chunk", data={"amplitude": 12.5}, timestamp=twin.get_sim_clock()))
bus.flush()
```

---

## Verification & Testing

```bash
make test       # Runs pytest + cargo test --workspace
make lint       # Runs ruff, mypy, cargo clippy, cargo fmt
make sbom       # Generates CycloneDX SBOM artifact
```

---

## Related Projects & Documentation

- **[vireon-lab](https://github.com/SaadiMalik1/vireon-lab)**: Interactive educational UI, Streamlit dashboard, and attack tutorials.
- **[Architecture Decision Records](docs/adr/)**: Specifications for all 15 system ADRs.
- **[Governance](GOVERNANCE.md)** & **[Contributing Guidelines](CONTRIBUTING.md)**.
