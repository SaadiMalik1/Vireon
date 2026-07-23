> [!NOTE]
> **Notice:** This document is an internally generated, AI-assisted self-review produced during development. It is not an independent or third-party audit.

# SDK Conformance Report (v1.0)

## 1. Overview
The VIREON SDK is the critical contract between the Validation OS (Kernel) and the vendor ecosystem. It must be treated as if thousands of vendors rely on it.

## 2. Interface Audit
- **Language Bindings**: Heavy Python bias. Needs stable C-ABI and gRPC definitions for true language independence.
- **Backward Compatibility**: SemVer guarantees are currently implicit. Must be enforced via CI ABI checkers.
- **Exceptions**: Domain-specific exceptions are inconsistent. The SDK must standardize error propagation across language boundaries (e.g., mapping Rust `Result` to Python `Exception` via standard FFI boundaries).

## 3. Provider Interactions
- The SDK correctly avoids containing device-specific clinical logic.
- However, the SDK leaks internal orchestrator types in some legacy `vireon-lab` endpoints.

## 4. Remediation Plan
- Strictly isolate the public SDK from internal Kernel imports.
- Implement Contract Testing for the SDK using schema validation (e.g., Protobuf/FlatBuffers).
- Formalize deprecation windows and migration policies.
