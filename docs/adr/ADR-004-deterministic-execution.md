# ADR 004: Strict Deterministic Execution

## Status
Accepted — Implemented (v1.1.0 — DeterministicClock & DeterministicRNG)

## Context
Scientific reproducibility is impossible if simulation outcomes rely on non-deterministic factors like host CPU scheduling, wall-time clocks, or locally seeded random number generators (RNGs) within providers. A core objective of the ecosystem is to generate reproducible scientific trace bundles.

## Decision
We enforce **Strict Deterministic Execution**.
1. **Clock Ownership**: The Kernel dictates all time. Providers may not invoke `time.time()` or equivalent OS calls. They must synchronize with the Kernel's logical `tick()`.
2. **RNG Ownership**: The Kernel generates a master seed and securely splittable sub-seeds, distributed to providers via the capability manifest. Providers must use these seeds for all internal randomness.
3. **Replay Bundles**: The Kernel will cryptographically hash and sign every input, seed, and capability grant to produce a verifiable `Trace Bundle`.

## Consequences
- **Positive**: 100% hash-validated scientific reproducibility. Simulations run on Anthropic's cluster will yield the exact same binary output as simulations run on a local laptop.
- **Negative**: Vendor providers that rely on hardware-accelerated RNGs or multi-threaded race conditions will fail the validation tests.
- **Migration**: All providers must remove OS time/randomness dependencies and link against the new deterministic SDK bindings.
