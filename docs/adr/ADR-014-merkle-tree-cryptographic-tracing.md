# ADR 014: Merkle Tree Cryptographic Tracing

## Status
Accepted — Implemented (StateStore auto-append & Ed25519 trace signing)


## Context
Trace bundles contain the absolute truth of a validation run. A malicious actor could decompress a trace bundle, alter the recorded State Graph to hide a critical device failure, recompress it, and submit it for FDA approval.

## Decision
We will enforce **Merkle Tree Cryptographic Tracing** for all validation bundles.
- Every event logged by the Kernel (capability grants, RNG seeds, state mutations) is hashed.
- The hash of event $N$ is computed as $Hash(Payload_N || Hash_{N-1})$.
- The Genesis Block is signed by the Kernel's private key at the start of the run.
- The Final Block is signed by the Kernel at termination.
- Any attempt to alter a single bit of telemetry in the middle of the bundle will corrupt the cryptographic chain, making it mathematically impossible to forge a passing validation run.

## Consequences
- **Positive**: Provides undeniable cryptographically secure proof of a device's validation history.
- **Negative**: Hashing every mutation adds CPU overhead to the logging thread. We must use high-throughput, non-cryptographic hashes (like BLAKE3) for the internal chain to maintain real-time speeds, falling back to RSA/Ed25519 only for the Genesis and Final signatures.
