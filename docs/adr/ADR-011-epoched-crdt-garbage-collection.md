# ADR 011: Epoched CRDT Garbage Collection

## Status
Accepted — Implemented (v1.1.0 — CRDTStateStore epoched tombstone garbage collection)

## Context
ADR-008 mandates CRDTs for the State Store. CRDTs track causality via metadata (e.g., Vector Clocks, tombstones). In a 30kHz neuro-simulation, maintaining infinite causality history for every node in the State Graph will trigger Out-Of-Memory (OOM) failures within seconds due to metadata explosion.

## Decision
We will implement **Epoched State Garbage Collection**.
- The Kernel defines an `Epoch` (e.g., every 1,000,000 ticks).
- At the Epoch boundary, the Kernel halts asynchronous CRDT merges and computes a mathematically sound, locked snapshot of the State Graph.
- All Vector Clocks and tombstones prior to the Epoch boundary are discarded.
- Providers are forced to re-sync their local replica with the new clean Epoch state.

## Consequences
- **Positive**: bounds the memory usage of the State Store to $O(N)$ where $N$ is the state size within the current Epoch, rather than growing infinitely over time.
- **Negative**: Introduces a periodic blocking operation (the Epoch barrier), which must be tightly optimized to avoid missing real-time deadlines in Wall-Time mode.
