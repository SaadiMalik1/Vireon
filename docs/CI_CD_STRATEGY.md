# CI/CD & DevOps Strategy

## Overview
To prevent divergent workflows and ensure a uniform developer experience, all CI/CD pipelines, linting configurations, and quality gates across the VIREON ecosystem are centralized. Individual repositories do not invent their own CI pipelines.

## Ownership: `.github` Repository
All shared organizational configuration lives in the `.github` repository (e.g., `github.com/VIREON/.github`).
This repository is the canonical owner of:
1. **Shared GitHub Actions Workflows:** Reusable workflows (`workflow_call`) for testing, building, and publishing.
2. **Shared Dependabot Configuration:** Ecosystem-wide dependency update policies.
3. **Shared Renovate Configuration:** If used instead of Dependabot for more complex locking.
4. **Shared Issue & PR Templates:** Standardized across the org.
5. **Shared Labels:** Global `.github/labels.yml` to sync labels to all repos.

## Shared Tooling Configurations
Rather than duplicating `ruff.toml`, `mypy.ini`, or `.pre-commit-config.yaml` across every repository, we employ a shared-configuration strategy:
- **Linting & Formatting (Ruff / Black):** A core `vireon-config` package (or remote configuration URL) is published. All repositories extend this base configuration in their local `pyproject.toml`.
- **Pre-commit:** The canonical `.pre-commit-config.yaml` is maintained in the `.github` repository. A sync action copies or enforces it across component repositories.
- **Pytest:** Shared plugins and fixtures are published as a lightweight testing library, ensuring that coverage and reporting formats are identical everywhere.

## Release Workflow
- **Component CI:** Triggers on PRs to `vireon`, `vireon-lab`, or `neurodsl`. Uses the reusable `.github` workflow to run unit tests and linters.
- **Cross-Repo CI:** Upon a merge to `main` in any component, the `workspace` repository's E2E action is triggered via repository_dispatch to verify that the change did not break the integrated ecosystem.
- **Publishing:** Releases are strictly tagged (`vX.Y.Z`). The reusable release workflow in `.github` handles PyPI publishing for Python packages and Crates.io for Rust crates.
