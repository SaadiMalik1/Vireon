# Provider Conformance Report (v1.0)

## 1. Compliance Status
- **Status**: **PARTIALLY COMPLIANT**

## 2. Standardization Deficits
- **Lifecycle Standardization**: Currently, providers do not conform to a strict, uniform lifecycle (e.g., `Initialize`, `Negotiate`, `Run`, `Halt`, `Teardown`). Some providers initialize asynchronously without waiting for Kernel synchronization.
- **Provider Manifests**: Lacking. Providers must emit a standardized `Provider Manifest` declaring dependencies, required interfaces, and memory footprints.
- **Capability Manifests**: Lacking. Providers must formally negotiate capabilities (e.g., File I/O, Network, State Mutation) before execution.

## 3. Isolation & Sandboxing
- Providers run in the same process space as the orchestrator. A transition to gRPC/IPC or WASM via `neurodsl` is strictly mandated.
- No provider may bypass the SDK.

## 4. Remediation Plan
- Draft `ADR-003-provider-capability-manifest.md`.
- Refactor the Provider interface in the SDK to mandate strict Manifest declarations and Capability bounds.
