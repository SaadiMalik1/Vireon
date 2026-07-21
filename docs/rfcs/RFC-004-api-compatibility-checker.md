# RFC 004: API Compatibility Checker

## Status
Proposed

## Motivation
The VIREON SDK promises strict Semantic Versioning. A breaking change to the C-ABI or gRPC interfaces will instantly break clinical validation pipelines that rely on pre-compiled vendor plugins.
Currently, detecting breaking changes relies on human review of pull requests and ADRs, which is highly error-prone.

## Proposed Architecture
We propose establishing an automated **API Compatibility Checker** that runs in CI for every pull request against the `workspace` or `vireon` repositories.
1. The tool parses the Abstract Syntax Trees (AST) of the SDK headers (Rust/C++) and Protobuf/FlatBuffers definitions.
2. It compares the PR's AST against the AST of the `main` branch.
3. It uses strict mathematical rules to classify the diff (e.g., adding a field to a struct is a minor bump, but changing a function signature or removing a field is a major breaking bump).
4. If a breaking change is detected without a corresponding major version bump in the `Cargo.toml`/Manifest, the CI build fails instantly.

## Open Questions
- Should we build a custom AST analyzer using `tree-sitter`, or rely on existing language-specific tools (e.g., `cargo-semver-checks` for Rust, and `buf` for Protobuf)?
- How do we handle conceptual breaking changes that do not alter the AST (e.g., changing the unit of measurement of a field from milliseconds to microseconds)?

## Next Steps
Investigate existing open-source API compatibility linters and propose a concrete integration pipeline.
