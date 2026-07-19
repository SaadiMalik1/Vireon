# VIREON Framework

[![Constitution](https://img.shields.io/badge/Architecture-Constitution-blue.svg)](.github/CONSTITUTION.md)

**VIREON** is the professional validation infrastructure and runtime orchestrator for the VIREON ecosystem. It provides the core foundational components—such as the `StateStore`, `EventBus`, and Capability Engine—that enable high-performance neuro-security testing, plugin lifecycle management, and integration with the NeuroDSL language.

## Architecture & Ecosystem

The VIREON ecosystem is split by design to ensure the core orchestrator remains highly performant and free of monolithic clutter. 
- **`vireon`** (This Repository): The core framework, public SDKs, and security validation infrastructure. Intended for professional use and proprietary integration.
- **`vireon-lab`**: The educational platform, Streamlit dashboards, and interactive attack scenarios. 
- **`neurodsl`**: The underlying Rust-based Domain Specific Language engine.

For comprehensive architectural design, refer to the [Ecosystem Overview](docs/architecture/ECOSYSTEM.md) and the [Architectural Constitution](.github/CONSTITUTION.md).

## Installation

Install the VIREON core SDK:
```bash
pip install vireon[all]
```
*Note: For a guided development setup, see [INSTALLATION.md](docs/INSTALLATION.md).*

## Quick Start

The VIREON runtime acts as a thin orchestrator.

```python
from vireon.sdk.state import IStateStore
from vireon.runtime.event_bus import EventBus
from vireon.services.engine import ReplayEngine

# 1. Initialize core infrastructure
state_store = IStateStore()
event_bus = EventBus()

# 2. Start the simulation engine
engine = ReplayEngine()
engine.start()
```

## Canonical Documentation

All official documentation for the VIREON ecosystem is hosted within this repository:
- [Architecture & Design](docs/architecture/)
- [API Reference](docs/api/)
- [Threat Models & Physics](docs/reference/)
