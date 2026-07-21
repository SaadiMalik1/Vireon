# ADR 015: Non-Blocking Ring Buffers with Overwrite

## Status
Accepted — Deferred (Phase C)

## Context
Providers communicate with each other via point-to-point SPSC (Single-Producer Single-Consumer) queues negotiated by the Kernel. If a low-priority logging provider is too slow to read telemetry from a high-priority hardware emulator, the channel's memory buffer will fill up. If the hardware emulator uses a blocking write when the buffer is full, it will halt (Priority Inversion), miss its real-time Wall-Time deadline, and crash the simulation.

## Decision
We mandate **Non-Blocking Ring Buffers with Overwrite semantics** for all asynchronous inter-provider telemetry channels.
- When a channel is full, the Producer MUST NOT block.
- Instead, the Producer overwrites the oldest unread data in the ring buffer.
- The Consumer detects this overwrite via an atomic sequence counter and logs a `DroppedFrames` warning.
- Critical state mutations (e.g., CRDT State Store merges) bypass this and use the synchronous Zero-Copy Pointer Handoff (ADR-007) with Unidirectional Protections (ADR-012).

## Consequences
- **Positive**: Guarantees that slow, low-priority observers (like UI renderers or disk loggers) can never stall high-priority physics and firmware threads.
- **Negative**: Applications consuming the telemetry must be robust enough to handle dropped packets gracefully.
