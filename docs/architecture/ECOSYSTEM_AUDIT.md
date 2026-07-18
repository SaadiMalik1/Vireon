# Ecosystem Audit

## 1. vireon
- **Purpose**: Professional validation framework, runtime, SDK, security.
- **Scope**: Core execution and validation.
- **Dependencies**: None.
- **Violations Identified**: Contains `knowledge/` educational material (should be in vireon-lab).

## 2. vireon-lab
- **Purpose**: Educational platform, tutorials, dashboard.
- **Scope**: End-user examples and GUI.
- **Dependencies**: `vireon`, `neurodsl`.
- **Violations Identified**: Duplicated README logic.

## 3. neurodsl
- **Purpose**: Rust DSL, Compiler, Parser.
- **Scope**: Low-level execution.
- **Dependencies**: None.
- **Violations Identified**: Contains duplicated `knowledge/` and `experiments/` folders.

## 4. workspace
- **Purpose**: Integration hub, cross-repo testing.
- **Scope**: E2E validation, Docker Compose.

## 5. .github
- **Purpose**: Shared templates, CI workflows.
- **Scope**: Global governance.
