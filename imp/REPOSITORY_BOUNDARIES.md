# Repository Boundaries Review

**Date:** 2025-07-09
**Scope:** Structural analysis of the five-repository Vireon ecosystem
**Verdict:** The current boundary structure is fundamentally broken. Consolidation into a monorepo is strongly recommended.

---

## 1. Current Repository Split

| Repository | Intended Role | Actual Content |
|------------|--------------|----------------|
| `vireon` | Core runtime / SDK | 39 runtime files, ~30 are deprecated shims |
| `vireon-lab` | UI / experimentation layer | Clinical engine, providers, firmware testing, attack modules, reports |
| `neurodsl` | Domain-specific language | 9-instruction DSL, stub spec, broken example |
| `workspace` | Orchestration / SSoT | 15 ADRs, 5 stub directories, no application code |
| `.github` | Governance / CI | Policy documents, no CI workflows |

---

## 2. The Fundamental Problem

The boundaries are wrong. Code ownership does not match repository boundaries.

`vireon` (the "core" repo) contains 39 runtime files, of which **~30 are deprecated shims** that re-export from packages that don't exist in the repo:

```python
# vireon/vireon/crdt_store.py
# DEPRECATED: Re-exports from vireon_lab.crdt (which lives in another repo)
```

Meanwhile, the actual domain logic — physics simulation, clinical modules, intrusion detection, privacy engineering, device drivers — lives in `vireon-lab`, which is nominally the "UI layer."

---

## 3. vireon-lab Is Misnamed

`vireon-lab` is not a lab. It is not a UI. It is the **actual application**. It contains:

| Subsystem | Description |
|-----------|-------------|
| Clinical simulation engine | LFP generator, closed-loop DBS controller, neural signal processing |
| ThreatAtlas | 850 KB threat intelligence database |
| Provider ecosystem | Dataset readers, hardware emulators, firmware emulators, BLE protocol |
| Firmware security testing | Cortex-M integration, QEMU HIL testing |
| Attack scenario modules | Adversarial ML, data poisoning, side-channel analysis |
| Report generation | Automated security assessment reports |

Calling this a "lab" dramatically understates its role. It is the application core.

---

## 4. workspace Is Empty

| Directory | Status |
|-----------|--------|
| `docs/` | Contains 15 ADRs (real content) and 5 stub guides |
| `schemas/` | Empty |
| `tools/` | Empty |
| `config/` | Empty |
| `scripts/` | Empty |
| `examples/` | Empty |

**5 of 9 top-level directories are stubs.** The repo has:
- No application code
- No build system
- No working CI
- A missing `.gitmodules` file (references submodules that cannot be checked out)

Its primary asset is the 15 ADRs that describe unimplemented architecture.

---

## 5. .github Is a Policy Repo Without Automation

Contains governance documents (`GOVERNANCE.md`, `CONTRIBUTING.md`, `CODE_OF_CONDUCT.md`) but:

- **No CI workflows** — despite being the logical home for shared CI
- `dependabot.yml` exists but is missing Cargo ecosystem coverage (critical for `neurodsl`)
- No branch protection rules defined
- No issue/PR templates

---

## 6. neurodsl Is Disconnected

The DSL repository exists in isolation:

- **9 instructions**, 2 of which are no-ops (`NOP`, `HALT`)
- `examples/basic_simulation.ndsl` uses syntax the compiler **cannot parse**
- `specification/grammar.md` contains only a title line
- Python bindings (PyO3) are tested exclusively with mocks — no integration test has ever imported the compiled extension
- No integration with the Vireon runtime beyond a CLI command that attempts `import neurodsl` and fails if the `.so` is not built
- No version pinning to any Vireon release

---

## 7. The Submodule Model Doesn't Work

```
Expected:  workspace/
├── vireon/          (submodule)
├── vireon-lab/      (submodule)
├── neurodsl/        (submodule)
└── .gitmodules

Actual:  workspace/
├── (empty directories where submodules should be)
└── .gitmodules      (MISSING)
```

- `.gitmodules` is missing entirely
- CI manually checks out repos via `actions/checkout` instead of using submodules
- There is no version pinning across repos — any commit from any repo can be combined with any other
- No integration test validates cross-repo compatibility

---

## 8. Circular Dependency Risk

```
vireon (core SDK)
  └─ imports ─→ vireon_lab.*  (external package, from vireon-lab repo)

vireon-lab (application)
  └─ imports ─→ vireon.*      (core SDK, from vireon repo)
```

This is a **circular dependency at the package level**. It means:

- Neither repo can be built or tested in isolation
- Version compatibility must be manually maintained across repos
- A breaking change in either repo will cascade to the other with no automated detection

---

## 9. CODEOWNERS Inconsistency

| Repository | CODEOWNERS |
|------------|-----------|
| `vireon` | Present |
| `vireon-lab` | Missing |
| `neurodsl` | Missing |
| `workspace` | Missing |
| `.github` | Missing |

Only the core repo has ownership definitions. The four repos containing the actual application logic, documentation, and governance have no ownership model.

---

## 10. Recommended Structure: Monorepo

The "kernel" (`vireon`) and "providers" (`vireon-lab` domain logic) are so tightly coupled through import paths that separate repos create unnecessary friction. The recommended structure is a **single monorepo**:

```
vireon/                                    (single repository)
│
├── .github/
│   ├── workflows/                         (CI/CD — now actually runs)
│   ├── CODEOWNERS                         (one file, full coverage)
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── dependabot.yml                     (Python + Rust + Cargo)
│
├── core/                                  (formerly vireon/)
│   ├── src/
│   │   ├── crdt_store/
│   │   ├── ipc/
│   │   ├── tracing/
│   │   └── sdk/                          (public API surface)
│   ├── pyproject.toml
│   └── README.md                          (self-contained)
│
├── runtime/                               (clinical, physics, IDS, privacy)
│   ├── clinical/
│   │   ├── lfp_generator/
│   │   ├── closed_loop_dbs/
│   │   └── neural_signal/
│   ├── ids/
│   ├── privacy/
│   ├── physics/
│   └── device_drivers/
│
├── providers/                             (dataset readers, emulators, BLE)
│   ├── datasets/
│   ├── hardware_emulators/
│   ├── firmware_emulators/
│   └── ble_protocol/
│
├── security/                              (formerly split between repos)
│   ├── threat_atlas/                      (STIX bundle + Threat Atlas JSON)
│   ├── threat_model.md                    (narrative documentation)
│   ├── attack_scenarios/                  (adversarial ML, data poisoning, side-channel)
│   └── firmware_testing/                  (Cortex-M, QEMU HIL)
│
├── neurodsl/                              (with its own Cargo.toml)
│   ├── src/
│   ├── specification/
│   │   └── grammar.md                     (now actually written)
│   ├── examples/
│   │   └── basic_simulation.ndsl          (now actually parseable)
│   ├── python/                            (PyO3 bindings)
│   ├── Cargo.toml
│   └── README.md
│
├── docs/                                  (canonical, single location)
│   ├── adr/                               (15 ADRs — unchanged)
│   ├── guides/                            (now with real content)
│   ├── api/                               (mkdocstrings, no cross-repo confusion)
│   ├── architecture.md
│   ├── deployment.md
│   ├── troubleshooting.md
│   └── glossary.md
│
├── workspace/                             (top-level project coordination)
│   ├── schemas/                           (FlatBuffers, protobuf, etc.)
│   ├── tools/                             (code generators, linting configs)
│   ├── config/                            (shared configuration)
│   └── scripts/                           (release, deploy, bootstrap)
│
├── reports/                               (generated output, gitignored)
│
├── mkdocs.yml                             (single config, single source of truth)
├── pyproject.toml                         (workspace root)
├── Cargo.toml                             (workspace root, neurodsl member)
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── GOVERNANCE.md
├── CHANGELOG.md
└── README.md                              (real content, not a redirect)
```

---

## Current vs. Recommended — Visual Comparison

### Current (Broken)

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   vireon    │◄───►│  vireon-lab │     │  neurodsl   │
│  (core SDK) │     │  ("UI" ???) │     │  (isolated) │
│  30 shims,  │     │  ACTUAL APP │     │  9 instrs,  │
│  9 real     │     │  clinical   │     │  broken ex. │
│  files      │     │  security   │     │  no grammar │
└──────┬──────┘     └──────┬──────┘     └─────────────┘
       │                   │                   │
       │  circular deps    │  no version pin   │  no integration
       ▼                   ▼                   ▼
┌─────────────┐     ┌─────────────┐
│  workspace  │     │   .github   │
│  5 stub     │     │  policies   │
│  dirs, 15   │     │  NO CI      │
│  ADRs only  │     │  NO actions │
└─────────────┘     └─────────────┘

  .gitmodules: MISSING
  Cross-repo testing: NONE
  Developer experience: clone 5 repos, most are empty
```

### Recommended (Monorepo)

```
┌─────────────────────────────────────────────────────┐
│                     vireon/                          │
│                                                      │
│  ┌──────┐  ┌─────────┐  ┌──────────┐  ┌──────────┐ │
│  │ core │  │ runtime │  │providers │  │ security │ │
│  │ SDK  │──│ clinical│──│ datasets │──│ threat   │ │
│  │      │  │ physics │  │ emulators│  │ atlas    │ │
│  │      │  │ IDS     │  │ BLE      │  │ firmware │ │
│  └──────┘  └─────────┘  └──────────┘  └──────────┘ │
│       │                                              │
│       │          ┌──────────┐                        │
│       └─────────►│ neurodsl │                        │
│                  │ (Cargo)  │                        │
│                  └──────────┘                        │
│                                                      │
│  ┌──────┐  ┌──────┐  ┌──────────┐  ┌──────────────┐ │
│  │ docs │  │ work-│  │ .github/ │  │   README.md  │ │
│  │ ADRs │  │space │  │ CI/CD    │  │  (real info) │ │
│  │ guides│  │schemas│  │ CODEOWN │  │  CHANGELOG   │ │
│  └──────┘  └──────┘  └──────────┘  └──────────────┘ │
└─────────────────────────────────────────────────────┘

  Single clone. Single CI. Single version.
  No circular deps. No missing submodules.
  Every directory has real content.
```

---

## Migration Rationale

| Issue | Multi-repo (current) | Monorepo (recommended) |
|-------|---------------------|----------------------|
| Circular dependencies | Unresolvable at package level | Eliminated; same dependency graph, single resolve |
| Version pinning | Manual, error-prone, untested | Single version for entire codebase |
| CI complexity | 5 repos × N workflows, no integration tests | 1 repo, 1 workflow graph, integration tests run natively |
| Documentation SSoT | Contested between workspace and vireon | Undisputed: `docs/` at repo root |
| Onboarding | Clone 5 repos, figure out which are empty | `git clone` once, everything is there |
| CODEOWNERS | Only in vireon | One file covers all paths |
| Submodule hell | Missing .gitmodules, no pinning | Eliminated entirely |
| Refactoring across boundaries | Requires coordinated PRs across repos | Single PR, single review |

---

## Immediate Actions

1. **Stop creating new repos.** Any new code goes into one of the existing repos.
2. **Add a real README to every repo.** Even if the long-term plan is monorepo consolidation, each repo must be self-documenting today.
3. **Add `.gitmodules` or remove submodule references.** The current state (referencing submodules without a `.gitmodules` file) is broken.
4. **Pin cross-repo versions** in `pyproject.toml` and `Cargo.toml` to prevent silent breakage.
5. **Begin monorepo consolidation** by moving `vireon-lab` domain logic into `vireon` under a `providers/` or `runtime/` directory, then updating import paths.
6. **Move `neurodsl`** into the monorepo as a subdirectory with its own `Cargo.toml` (Cargo workspace member).
7. **Flatten `workspace`** into a `docs/` and `tools/` directory at the monorepo root. Delete the empty stub directories.