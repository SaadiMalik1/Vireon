# ADR 012: Unidirectional Memory Protections

## Status
Accepted — Deferred (Phase D)

## Context
ADR-007 introduced Zero-Copy Pointer Handoff via shared memory rings. This creates a classic Time-of-Check to Time-of-Use (TOCTOU) vulnerability. A malicious plugin can write to the ring, wait for the Kernel to validate the headers/sizes, and then mutate the payload *before* the Kernel acts on it, leading to memory corruption or arbitrary code execution in the Kernel.

## Decision
We will enforce **Unidirectional Memory Protections via `mprotect`**.
- Shared memory mappings are strictly asymmetric.
- The Producer is granted `PROT_WRITE | PROT_READ`.
- The Consumer is granted `PROT_READ` only.
- Crucially, any metadata (array indices, lengths, payload sizes) that dictates Kernel control flow MUST be copied from the shared memory into the Kernel's private, unshared heap *before* any bounds checking or validation occurs. The Kernel must never validate a value residing in shared memory and then read that shared memory value again later expecting it to be unchanged.

## Consequences
- **Positive**: Completely eliminates TOCTOU vulnerabilities over the Zero-Copy boundary.
- **Negative**: Incurs a minor penalty because metadata headers must be deeply copied into private memory. However, the bulk payloads (e.g., matrix data) remain zero-copy.
