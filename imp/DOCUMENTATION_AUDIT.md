# Documentation Audit

**Date:** 2025-07-09
**Scope:** All five repositories in the Vireon ecosystem
**Overall Score: 4 / 10**

> The ADRs are excellent design documents. Everything else ranges from incomplete to misleading.

---

## 1. Documentation Architecture

Documentation is scattered across all five repositories with no clear canonical location. The `workspace` repository is nominally the single source of truth (SSoT), but READMEs in each sub-repo redirect developers back to `workspace`, creating a circular reference loop:

```
Developer visits vireon-lab README
  → "See workspace for docs"
    → workspace docs reference vireon-lab for provider details
      → vireon-lab README says "See workspace"
        → …
```

No repository is self-contained. A developer cloning any single repo cannot get started without cloning at least two others.

---

## 2. Architecture Decision Records (ADRs)

**Location:** `workspace/docs/adr/` — 15 records

These are the **strongest documentation asset** in the entire ecosystem. They cover:

| ADR | Topic | Status |
|-----|-------|--------|
| ADR-001 | eBPF capability enforcement | Paper only |
| ADR-002 | CRDT state stores | Paper only |
| ADR-003 | Zero-copy IPC | Paper only |
| ADR-004 | Bifurcated clock scheduling | Paper only |
| ADR-005 | Merkle tree tracing | Paper only |
| ADR-006 | Hardware watchdogs | Paper only |
| … | … | … |

**Problem:** None of this is implemented. These are design documents for a system that exists only on paper. A new contributor reading these ADRs will form a mental model of the architecture that does not match any code in any repository. The gap between documented intent and actual implementation is total.

**Recommendation:** Clearly mark each ADR with an implementation status. Consider adding a `status: proposed | accepted | deprecated | superseded` frontmatter field and, critically, a `status: implemented | not-implemented | partial` field.

---

## 3. mkdocs.yml Configuration

The `mkdocs.yml` in `workspace` lists **40+ pages** covering:

- Architecture overview
- Tutorials (getting started, advanced)
- Threat modeling
- Validation framework
- Benchmarks
- 10 design decisions
- API reference (via `mkdocstrings`)
- Glossary
- Roadmap

**Problem:** The source files for most of these pages live in the `vireon` repo's `docs/` directory, not in `workspace`. This creates confusion about which location is canonical. A contributor updating documentation in one location may not realize a stale copy exists in the other.

**Recommendation:** Either consolidate all documentation source into `workspace` and remove it from `vireon`, or acknowledge that `workspace` is not the SSoT and designate `vireon` as the documentation host.

---

## 4. Guides

Five guides exist in `workspace/docs/`:

| Guide | Size | Status |
|-------|------|--------|
| Architecture Guide | <1 KB | References nonexistent files |
| Developer Guide | <1 KB | References nonexistent files |
| Migration Guide | <1 KB | References nonexistent files |
| Operations Guide | <1 KB | References nonexistent files |
| Integration Guide | <1 KB | References nonexistent files |

All are stub documents that reference files which do not exist anywhere in the ecosystem:

- `DESIGN_RATIONALE.md` — does not exist in any repo
- `schemas/*.fbs` — FlatBuffers schema files do not exist
- `devcontainer.json` — no devcontainer configuration exists

These guides are actively misleading. They give the appearance of documentation while directing developers to dead ends.

**Recommendation:** Remove these guides entirely until the referenced assets exist, or replace them with honest "TODO" placeholders that acknowledge the missing content.

---

## 5. README Quality

All five repositories have READMEs that function as **redirect stubs**:

```markdown
# vireon-lab
> See [workspace](https://github.com/...) for documentation.
```

A developer visiting any single repository gets **no useful information** about that repository's purpose, structure, entry points, or how to run it. This violates the principle that every repository should be self-documenting at the README level.

**Recommendation:** Each README must contain at minimum:
- What this repo is (one paragraph)
- Directory structure overview
- How to build/run locally
- Where to find detailed documentation

---

## 6. API Documentation

`mkdocs.yml` is configured with `mkdocstrings` for Python docstring generation. However:

- **SDK interfaces** (in `vireon/`): Have docstrings, but many are auto-generated stubs
- **Runtime modules** (39 files across `vireon/vireon/`): Largely lack docstrings entirely
- **Provider modules** (in `vireon-lab/`): Mixed; clinical modules have some documentation, provider infrastructure does not

Running `mkdocstrings` against the current codebase will produce incomplete API reference with dozens of undocumented modules and "No documentation found" warnings.

**Recommendation:** Establish a docstring coverage threshold (e.g., 80%) and enforce it in CI before generating API documentation.

---

## 7. Threat Model Documentation

**Location:** `vireon-lab/` — STIX 2.1 bundle (4,666 lines) and Threat Atlas (~850 KB JSON)

These are **substantial assets**:

- The STIX bundle contains structured threat intelligence in a standard format
- The Threat Atlas maps attack surfaces specific to neural interface systems

**Problem:** They exist only as raw JSON files with no narrative documentation. There is no guide explaining:
- How to read the STIX bundle
- How to use the Threat Atlas in testing
- How to extend the threat model for new attack surfaces
- How these artifacts integrate into the CI/CD pipeline

**Recommendation:** Add a `THREAT_MODEL.md` with a narrative walkthrough, usage examples, and maintenance procedures.

---

## 8. NeuroDSL Documentation

**Location:** `neurodsl/specification/grammar.md`

- `grammar.md` contains **only a title line** — no grammar, no syntax rules, no EBNF
- `examples/basic_simulation.ndsl` uses syntax the compiler **cannot parse**
- There is no opcode reference
- There is no tutorial
- There is no integration guide

The DSL has 9 instructions, 2 of which are no-ops, and its Python bindings are tested exclusively with mocks. A user cannot learn NeuroDSL from the existing documentation because the documentation does not exist.

**Recommendation:** At minimum, document the 9 instructions in a reference table. Ideally, provide a working example that the compiler can actually parse.

---

## 9. Constitution and Governance

**`GOVERNANCE.md`:** Defines a "benevolent dictator" model with an approval threshold for changes. However, the threshold is **inconsistent** — some sections require 1 approval, others require 2, with no clear rule for which applies.

**`CONTRIBUTING.md`:** Mentions `mypy` for type checking but does not list it as a prerequisite in the setup instructions. A contributor following the guide literally will skip `mypy` installation and fail at CI.

**Recommendation:** Harmonize approval thresholds into a single decision matrix. Make `CONTRIBUTING.md` prerequisites exhaustive and cross-reference `GOVERNANCE.md`.

---

## 10. Missing Documentation

The following documentation is entirely absent:

| Category | Impact |
|----------|--------|
| Architecture diagrams | No visual representation of system architecture (text-based ADR diagrams are the only exception) |
| Deployment guide | No instructions for deploying the system to any environment |
| Troubleshooting guide | No known-issues or FAQ document |
| Changelog format | No `CHANGELOG.md` or `HISTORY.md` in any repo; no convention defined (e.g., Keep a Changelog) |
| Versioning policy | No semver enforcement, no release process documented |
| Onboarding guide | No "first contribution" walkthrough |
| Testing guide | No explanation of test structure or how to run the test suite |
| Error code reference | Runtime error codes are undocumented |

---

## Summary Matrix

| Area | Score | Notes |
|------|-------|-------|
| ADRs | 9/10 | Excellent design documents; not implemented |
| Threat models | 7/10 | Substantial but lack narrative |
| mkdocs config | 5/10 | Ambitious but source files are in wrong repo |
| Governance | 4/10 | Inconsistent thresholds |
| API docs | 3/10 | Configured but most modules lack docstrings |
| READMEs | 2/10 | Redirect stubs with no useful content |
| Guides | 1/10 | Stub files referencing nonexistent assets |
| NeuroDSL | 1/10 | Effectively undocumented |
| Missing docs | 0/10 | Critical gaps in deployment, troubleshooting, versioning |

**Overall: 4 / 10**

The documentation describes an ambitious, well-architected system. The code describes something much smaller and less mature. Closing this gap — either by implementing the architecture or by aligning documentation with reality — is the single highest-priority action for this project.