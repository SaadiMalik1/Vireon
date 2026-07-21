# Contributing to VIREON

Thank you for contributing to the VIREON ecosystem!

## 1. Environment Setup
To set up the distributed monorepo for local development, run:
```bash
git clone --recurse-submodules <workspace-repo-url>
cd workspace
just setup-all
```

## 2. Architectural Constraints
Before submitting a PR, ensure your code respects the fundamental constraints outlined in `ARCHITECTURE_VALIDATION.md`. Specifically:
- **No external dependencies** in `vireon.runtime` without TSC approval.
- **Max 300 LOC** per file in `vireon/runtime/`.
- All tests must pass: `just test-all`.

## 3. Pull Request Process
1. Create a descriptive branch (e.g., `feat/add-thermal-provider`).
2. Write unit tests for your changes.
3. Submit a PR against `main`.
4. Wait for CI constraint checks and architecture AST validation to pass.
5. Obtain approval from at least one core Maintainer.
