# ADR 001: Kernel Transition (SDK to Validation OS)

## Status
Accepted — Implemented (v1.1.0 — Thin domain-agnostic orchestrator & SDK)

## Context
VIREON was originally conceived as a software development kit (SDK) to help neurotechnology developers write simulation scripts. However, this has resulted in vendors leaking device-specific logic into the orchestrator and treating the `vireon` Python module as a library they can embed in their proprietary clinical applications. This violates the foundational requirement of strict isolation and vendor neutrality. 

## Decision
We will transition VIREON from an embeddable SDK into a standalone Validation Operating System (Kernel). 
- The Kernel will exclusively own the event loop, scheduling, and provider lifecycle.
- Providers (vendors) will be treated as untrusted user-space processes.
- The Kernel must remain strictly domain-agnostic (containing zero clinical or neurophysiological algorithms).

## Consequences
- **Positive**: Complete isolation of proprietary logic. The runtime becomes highly deterministic.
- **Negative**: Increased complexity for simple simulation scripts, as developers must now write formal `Providers` and declare manifests rather than simply importing `vireon`.
- **Migration**: Existing `vireon-lab` scripts must be refactored into formal Providers and executed via the new `vireon-kernel` binary.
