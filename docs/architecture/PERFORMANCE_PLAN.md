# VIREON Ecosystem Performance Optimization Plan

This document outlines the strategic roadmap for scaling the VIREON runtime to handle massive, high-channel-count neurotechnology simulations at kilohertz sampling rates.

## Identified Bottlenecks

### 1. Python Global Interpreter Lock (GIL) Contention
- **Analysis:** The `EventBus` in `vireon.runtime` utilizes Python threads and `asyncio` for routing telemetry between the Digital Twin, UI, and custom plugins. Under heavy load (e.g., 1024 channels at 30kHz), the GIL becomes a severe bottleneck.
- **Solution:** Transition the core telemetry routing layer to the Rust `neurodsl` engine. The Python `EventBus` should only handle low-frequency control plane events, while high-frequency data plane streams bypass Python entirely via Rust channels or zero-copy shared memory.

### 2. Serialization Overhead
- **Analysis:** Currently, data traversing the `vireon` <-> `vireon-lab` boundary or `vireon` <-> `neurodsl` boundary suffers from heavy JSON or standard Python serialization overhead.
- **Solution:** Mandate FlatBuffers or Apache Arrow for all internal data plane communications. This allows zero-copy deserialization directly into `numpy` or Rust `ndarray` structures.

### 3. State Synchronization
- **Analysis:** The `IStateStore` is currently a centralized Python dictionary. Heavy concurrent read/writes during adversarial modifier attacks cause lock contention.
- **Solution:** Re-architect the `StateStore` using an Actor model (e.g., Pykka or Rust Actix) where state mutations are strictly serialized through message queues, eliminating coarse-grained locks.

## Optimization Roadmap

### Phase A: Profiling (Month 1)
1. Instrument `vireon.runtime` with Py-Spy and memory profilers.
2. Establish baseline benchmarks for 10, 100, and 1000 channel setups in `neurodsl`.
3. Integrate CI benchmark regression tracking (`pytest-benchmark`).

### Phase B: Data Plane Offloading (Month 3)
1. Implement Apache Arrow for the Python <-> Rust boundary.
2. Move Fast Fourier Transforms (FFT) and RMS computations exclusively to Rust; Python SDK functions merely dispatch the calls.

### Phase C: Lockless Architecture (Month 6)
1. Replace the Python `EventBus` with a lockless ring-buffer architecture backed by Rust.
2. Implement Actor-based state management.
