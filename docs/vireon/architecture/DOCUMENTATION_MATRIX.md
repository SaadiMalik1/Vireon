# Documentation Matrix

## Overview
This matrix defines the single authoritative owner for every piece of documentation in the VIREON ecosystem. Duplicated documentation across repositories is strictly prohibited.

| Topic / Document | Canonical Owner | Location | Status |
|------------------|-----------------|----------|--------|
| **Architecture** | `vireon` | `vireon/docs/CONSTITUTION.md` & `ARCHITECTURAL_BOUNDARIES.md` | Consolidated |
| **Installation** | `vireon` | `vireon/docs/INSTALLATION.md` | Centralized |
| **Quick Start** | `vireon-lab` | `vireon-lab/README.md` & `vireon-lab/tutorials/` | Re-homed to Lab |
| **API Reference** | `vireon` | `vireon/docs/api.md` | Unchanged |
| **Plugin SDK** | `vireon` | `vireon/docs/PLUGIN_SDK_DESIGN.md` | Unchanged |
| **Provider Lifecycle**| `vireon` | `vireon/docs/PLUGIN_LIFECYCLE.md` | Unchanged |
| **Glossary** | `vireon` | `vireon/docs/glossary.md` | Consolidated |
| **Research** | `neurodsl` | `neurodsl/docs/research/` | Scoped to DSL |
| **Threat Models** | `vireon` | `vireon/docs/threat-model/` | Centralized |
| **Contribution** | `.github` | `.github/CONTRIBUTING.md` | Centralized |
| **Developer Setup**| `workspace` | `workspace/INTEGRATION.md` | Re-homed to Workspace |
| **Migration Guides**| `vireon` | `vireon/docs/MIGRATION_GUIDE.md` | Unchanged |
| **Examples** | `vireon-lab` | `vireon-lab/examples/` | Re-homed to Lab |
| **Release Notes** | `.github` | Centralized GitHub Releases page | Removed from repos |

### Deletion Candidates
- Any `INSTALL.md` files in individual repositories.
- Any duplicated `DOCUMENTATION_PROGRESS_REPORT.md` (delete from lab and dsl).
- Any duplicated architectural files in `neurodsl` or `vireon-lab`.
