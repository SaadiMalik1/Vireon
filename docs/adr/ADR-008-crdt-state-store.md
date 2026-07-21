# ADR 008: CRDT State Store

## Status
Accepted — Deferred (Phase D)

## Context
The ecosystem maintains a global "Digital Twin" state graph representing the physical environment (e.g., neural tissue, device orientation). If two isolated plugins attempt to mutate this state graph simultaneously, the Kernel must resolve the mutation deterministically.
Traditional locking mechanisms (Mutex/RwLock) across IPC boundaries will introduce severe blocking, ruining the real-time throughput of the simulator.

## Decision
We will implement the State Store using **Conflict-free Replicated Data Types (CRDTs)**.
- Each plugin maintains a local replica of the State Graph.
- Mutations are made locally and streamed asynchronously to the Kernel.
- The Kernel merges the CRDT payloads and broadcasts the delta updates back to the plugins.

## Consequences
- **Positive**: Eliminates cross-boundary locks for state mutation.
- **Positive**: Guarantees deterministic convergence of the state graph regardless of the order in which network packets arrive from different providers.
- **Negative**: CRDTs carry metadata overhead (vector clocks or tombstone tracking), which increases memory usage and payload size.
