# Workspace Architecture

The `workspace` repository acts as the sole integration hub for the VIREON ecosystem.

## Ownership
It owns ONLY:
- Integration tests
- Contract tests
- Compatibility tests
- Release validation
- Docker Compose
- Example deployments
- Benchmarks
- Version matrix
- Dependency locking
- Cross-repository CI
- Release orchestration
- Architecture governance

It MUST NOT contain production logic or educational content.
