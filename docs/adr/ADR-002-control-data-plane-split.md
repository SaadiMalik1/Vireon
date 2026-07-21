# ADR 002: Control Plane vs Data Plane Split

## Status
Accepted — Deferred (Phase C)

## Context
Neuro-simulations require high-frequency, low-latency telemetry data (e.g., raw neural spikes sampled at 30kHz) mixed with low-frequency control messages (e.g., "start simulation", "capability requested"). The current architecture multiplexes both streams over a single Python `asyncio` event bus, causing unacceptable latency and jitter, violating the lock-free execution requirements of a true research platform.

## Decision
We will split the architecture into a **Control Plane** and a **Data Plane**.
1. **Control Plane**: Handled via gRPC. Responsible for provider registration, capability negotiation, lifecycle management, health checks, and slow-path logging.
2. **Data Plane**: Handled via lock-free shared memory ring buffers using opaque handles and FlatBuffers (orchestrated by the `neurodsl` Rust engine). This guarantees zero-copy buffer sharing between the Kernel and isolated Providers.

## Consequences
- **Positive**: Massively increased telemetry throughput. Providers written in C++ or Rust can communicate at native speeds without Python GIL interference.
- **Negative**: Complicates the provider SDK, as providers must now implement two separate interfaces (gRPC for control, Shared Memory for data).
- **Migration**: The `EventBus` module must be deprecated in favor of a dual-plane architecture.
