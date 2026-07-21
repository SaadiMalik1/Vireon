# ADR 003: Provider Capability Manifests (Zero-Trust Sandbox)

## Status
Accepted — Deferred (Phase B)

## Context
Currently, providers execute in the same process space as the VIREON runtime, implicitly granting them unrestricted access to the host's filesystem, network, and memory. For VIREON to serve as a trusted, vendor-neutral validation platform, we must assume that proprietary provider binaries are untrusted and potentially malicious.

## Decision
We mandate a strict **Zero-Trust Sandbox** enforced by a `Capability Engine`.
1. Every provider must supply a cryptographically signed `Capability Manifest` prior to execution.
2. The manifest must explicitly request access to specific namespaces, memory bounds, random number generator (RNG) seeds, and telemetry streams.
3. The Kernel will parse the manifest and enforce it via OS-level primitives (e.g., `seccomp` filters, or eventually WASM components via `neurodsl`).
4. **Failure Philosophy**: Fail Closed. If a provider requests an ungranted capability, the Kernel terminates the provider immediately; it does not crash the Kernel.

## Consequences
- **Positive**: The ecosystem can safely host untrusted proprietary binaries.
- **Negative**: Debugging provider failures becomes harder due to opaque sandbox terminations.
- **Migration**: All existing `vireon-lab` providers must be retrofitted with a `manifest.yaml` and loaded via the new `Capability Engine`.
