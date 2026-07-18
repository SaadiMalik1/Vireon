# Ecosystem Responsibilities & Governance

## 1. Repository Responsibility Matrix

Every responsibility has exactly one owner in the VIREON ecosystem:

| Component | Owner Repository |
|-----------|------------------|
| Runtime | `vireon` |
| SDK | `vireon` |
| Documentation | `vireon` (under `docs/`) |
| CI (Shared) | `.github` |
| CI (Integration) | `workspace` |
| Threat Models | `vireon` |
| Examples / Tutorials | `vireon-lab` |
| Benchmarks (Component)| `vireon` & `neurodsl` |
| Benchmarks (E2E) | `workspace` |
| Integration | `workspace` |
| Testing (Unit) | Each respective repo |
| Testing (Contract) | `workspace` |
| Releases | `.github` (Automation) & `vireon` (Changelog) |
| Docker (Base) | `vireon` |
| Docker (Compose) | `workspace` |
| Versioning Matrix | `workspace` |

## 2. Version Governance

### Semantic Versioning
- All components adhere to strict SemVer (MAJOR.MINOR.PATCH).
- `vireon` and `neurodsl` versions are decoupled.
- The `workspace` maintains the known-good compatibility matrix.

### Release Cadence & LTS
- **Core (`vireon`):** Minor releases every 3 months. LTS branches maintained for 12 months.
- **Lab (`vireon-lab`):** Continuous deployment. Tied to the latest stable `vireon` release.
- **DSL (`neurodsl`):** Ad-hoc releases based on syntax stabilization.

### Deprecation Policy
- APIs must be marked `@deprecated` for one full MINOR release cycle before removal in the next MAJOR release.

## 3. Testing Strategy

| Test Type | Owner | Execution Environment |
|-----------|-------|-----------------------|
| Unit Tests | `vireon`, `vireon-lab`, `neurodsl` | Local repo CI |
| Integration Tests | `workspace` | Cross-repo CI (`docker-compose`) |
| Contract Tests | `workspace` | Cross-repo CI |
| Performance Tests | `vireon` | Local repo CI |
| Benchmark Tests | `workspace` (E2E), Component repos | CI and specialized runners |
| Simulation Tests | `vireon-lab` | Lab CI |
| Educational Tests | `vireon-lab` | Lab CI |
| Vendor Validation | `vireon` | SDK test suite |

## 4. Open Source Governance

- **Repository Labels:** Maintained centrally via `.github` automation scripts.
- **Branch Strategy:** Main branch is `main`. Feature branches are used. Releases are tagged `vX.Y.Z`.
- **CODEOWNERS:** Maintained centrally in `.github/CODEOWNERS` (if supported by org-level scoping) or individually mirroring the responsibility matrix.
- **RFC Process:** Large architectural changes must submit an RFC to `vireon/docs/design-decisions/`.
- **Architecture Decision Records (ADR):** Tracked in `vireon/docs/design-decisions/`.
