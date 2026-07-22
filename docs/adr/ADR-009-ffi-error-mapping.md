# ADR 009: FFI Error Mapping

## Status
Implemented (v2.0.0-alpha.1)

## Context
VIREON supports plugins written in various languages (Rust, Python, C++, WASM). The boundary between the Kernel and these plugins is an FFI (Foreign Function Interface) or IPC layer.
If a Rust plugin encounters a `panic!`, or a C++ plugin throws an unhandled exception, it can unwind the stack across the FFI boundary into the Kernel, causing a catastrophic, non-deterministic crash of the entire orchestrator. This violates the "Fail Closed, Simulation Continues" principle.

## Decision
We mandate a strict **Standardized C-ABI Error Mapping** at all cross-language boundaries.
- Plugins are strictly forbidden from allowing panics or exceptions to escape their primary entry points.
- All FFI boundaries must return a standardized, opaque `vireon_error_t` struct (or equivalent gRPC status code).
- The Kernel will treat any stack unwinding attempt across its boundaries as a hostile act, instantly killing the provider sandbox.

## Consequences
- **Positive**: Protects the orchestrator from catastrophic crashes caused by poorly written vendor plugins.
- **Positive**: Standardizes error telemetry across all languages.
- **Negative**: Increases the boilerplate required for developers to write VIREON plugins, as every entry point must wrap its execution in catch-all/catch-unwind blocks.
