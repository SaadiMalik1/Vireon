# Contributing to VIREON

**Audience**: Developers, Security Researchers, Academic Researchers

First off, thank you for considering contributing to VIREON!

## Purpose
This document outlines the process for contributing to the VIREON project, including coding standards, branch management, and how to submit pull requests.

## Scope
These guidelines cover all contributions to the VIREON repository, including code (core engine, SDK, NeuroDSL, CLI), documentation, and tests.

## Prerequisites
- Python 3.10+
- Rust toolchain (stable)
- Git

## Onboarding Checklist for New Contributors
- [ ] Fork and clone the repository.
- [ ] Set up the development environment (`make install`).
- [ ] Run tests to ensure everything works locally (`make test`).
- [ ] Read the [Architecture Overview](docs/architecture.md).
- [ ] Pick an issue labeled `good first issue` or `help wanted`.
- [ ] Submit a Pull Request with a Signed-off-by line (DCO).

## Pull Requests & Approval Process
1. Fork the repo and create your branch from `main`.
2. Ensure commit messages adhere to DCO (`git commit -s`).
3. Add tests in `tests/` for all new code (minimum 80% coverage).
4. Update documentation if you altered public interfaces or configurations.
5. Ensure the full test suite and linters pass (`make lint && make test`).
6. Submit your PR!

### Approval Policy (per GOVERNANCE.md)
- **Standard PRs**: Require **1 approval** from a Core Maintainer.
- **Architectural / SDK / Security PRs**: Require **2 approvals** from Core Maintainers.

## Coding Standards
- PEP 8 standard. Enforced via `ruff check` and `mypy --strict`.
- All public functions must include docstrings detailing purpose, arguments, return values, and exceptions.
- Rust code must pass `cargo clippy --workspace -- -D warnings`.

## Related Documents
- [Governance Model](GOVERNANCE.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Security Policy](SECURITY.md)
