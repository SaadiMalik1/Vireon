# ADR 010: Hardware Watchdog Precision

## Status
Accepted — Implemented (v1.1.0 — Orchestrator deadline kicking & watchdog timeout handling)

## Context
Untrusted provider plugins can enter infinite loops (e.g., executing dense neural decoders). Currently, the Kernel relies on asynchronous gRPC or IPC health checks to verify a provider is alive. If a provider is executing a heavy workload on the CPU, these application-level health checks might time out, causing the Kernel to assume the provider is dead when it is actually just slow, or conversely, waiting too long before terminating a truly deadlocked provider.

## Decision
We will implement an **Out-of-Band Hardware Watchdog**.
- Each provider is assigned a dedicated POSIX signal thread or dedicated memory-mapped "heartbeat" register.
- The provider must flip this heartbeat bit periodically.
- An isolated Kernel thread monitors these bits with real-time OS priority. If the bit is not flipped within the capability-defined deadline, the Kernel instantly issues a `SIGKILL` (or destroys the WASM instance) without waiting for asynchronous protocol timeouts.

## Consequences
- **Positive**: Provides microsecond-precision detection of provider deadlocks.
- **Positive**: Frees the application protocol (gRPC) from polling for health status.
- **Negative**: Adds strict scheduling requirements to providers; they must ensure their heartbeat thread is not starved by their own workload.
