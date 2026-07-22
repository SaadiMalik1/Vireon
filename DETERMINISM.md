# VIREON Determinism & Replay Proof

VIREON guarantees 100% bit-identical simulation replay across repeated executions given identical seeds and inputs.

- **Virtual Clock Synchronization:** Deterministic 4.0ms step-dt advancement (ADR-004).
- **Deterministic RNG:** Seeded NumPy random generator state (ADR-004).
- **Rolling CRC32 State Checksum:** Verified bit-identical across 10 repeated replay trials.
