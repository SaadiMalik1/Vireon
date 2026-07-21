# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-07-21 (Foundation Remediation Release)

### Added
- Repository consolidation: Absorbed `workspace`, `.github`, and `neurodsl` into `Vireon`.
- Root Cargo workspace `Cargo.toml` managing `crates/neurodsl/` Rust crates (`scribe`, `forge`, `python_ext`).
- `requirements-lock.txt` for reproducible dependency locking (Rule 21).
- Dedicated architecture, determinism, and integration test suites (`test_architecture.py`, `test_determinism.py`, `test_integration.py`).
- Formal EBNF grammar specification for NeuroDSL (`crates/neurodsl/specification/grammar.md`).
- Unified Makefile for `Vireon` (`install`, `test`, `test-integration`, `lint`, `docs`, `sbom`, `docker`, `clean`).
- Multi-job GitHub Actions CI pipelines for `Vireon` and `vireon-lab`.

### Changed
- Decomposed `DigitalTwin` God class into `SignalState`, `PhysicsState`, `BatteryState`, `ClinicalState`, and `SimClock` dataclasses (Rule 27).
- Refactored `EventBus` for decoupled publish/subscribe event dispatch.
- Updated all 15 ADR statuses in `docs/adr/` to `Accepted — Deferred (Phase X)` (Rule 24).
- Restored `CODE_OF_CONDUCT.md` to complete Contributor Covenant v2.1 (Rule 26).
- Resolved approval threshold conflict in `GOVERNANCE.md` (1 approval standard, 2 for architectural/security changes) (Rule 32).
- Added `CODEOWNERS` in both `Vireon` and `vireon-lab` (Rule 34).

### Removed
- Deleted 30 deprecated shim files in `vireon/runtime/` (Rule 3).
- Deleted dead directories (`vireon/libraries/`, `vireon/reference_providers/`).
- Deleted duplicate inner `vireon-lab/vireon_lab/pyproject.toml`.
- Deleted hardcoded TLS certs (`cert.pem`, `key.pem`) from git/repo (Rule 16).
- Replaced invalid `basic_simulation.ndsl` example with valid stimulation protocol script.
- Replaced README redirect stubs with substantive, self-contained documentation (Rule 23).

---

## [1.0.0] - Initial Release

- Initial release of Vireon framework.
