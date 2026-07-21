# ADR 007: Zero-Copy Pointer Handoff

## Status
Accepted — Deferred (Phase C)

## Context
The Data Plane handles high-frequency neuro-telemetry (e.g., 30kHz multi-channel spike data). Inter-Process Communication (IPC) via gRPC or even raw sockets introduces serialization and context-switching overhead. If data is serialized and copied across memory spaces, the orchestrator will bottleneck and fail real-time validation constraints.

## Decision
We will implement a **Zero-Copy Pointer Handoff** mechanism for high-bandwidth data streams between the Kernel and Plugins.
- Upon initialization, the Kernel allocates shared memory ring buffers using `memfd_create` (or equivalent).
- The Kernel passes the file descriptor to the Plugin over standard IPC.
- Data is written directly to the shared memory ring buffer. The Kernel and Plugins exchange only memory offset pointers/semaphores to signify data availability, transferring ownership rather than copying bytes.

## Consequences
- **Positive**: Achieves theoretical maximum throughput for neuro-telemetry between isolated processes.
- **Positive**: Reduces CPU cache thrashing caused by constant serialization/deserialization.
- **Negative**: Increases the risk of segmentation faults or data races if the shared memory is improperly managed. We will mitigate this using Rust's memory safety rules at the API boundary.
