# ADR 005: Bifurcated Clock Scheduler

## Status
Accepted — Implemented (v2.0.0-alpha.2)

## Context
The VIREON ecosystem demands two contradictory clocking modes: 
1. **Scientific Determinism**: Requires a pure logical clock. If a provider drops a frame or takes too long to compute, the clock must wait to ensure reproducibility.
2. **Hardware-in-the-Loop (HIL) Real-Time**: Requires a wall-clock. Hardware devices emit telemetry at fixed intervals regardless of how fast the providers can process it. Dropping a packet here is reality, and the clock cannot pause.

Currently, the constitution mandates determinism without explicitly addressing the real-time requirements of HIL testing.

## Decision
We will implement a **Bifurcated Clock Scheduler** enforced at the compiler/kernel boundary.
- **Virtual-Time Mode (Default)**: The orchestration kernel governs all physics, networking, and firmware providers via a logical tick. Providers block until the tick completes.
- **Wall-Time Mode (HIL)**: A specialized kernel loop that syncs the logical tick with system `CLOCK_MONOTONIC`. Providers that fall behind are mathematically flagged for deadline misses, and frames are dropped.

The modes are mutually exclusive. A Simulation manifest must declare its time mode, and the Kernel will panic if a provider attempts to violate the mode's constraints.

## Consequences
- **Positive**: Resolves the contradiction between reproducible scientific pipelines and real-time medical device emulation.
- **Positive**: Forces providers to explicitly handle deadline misses in Wall-Time mode.
- **Negative**: Adds significant complexity to the `neurodsl` WASM scheduler, which must now support interrupt-driven time alongside pure logical stepping.
