# ANTIGRAVITY REMEDIATION RULES — INDEX

This is the complete set of remediation documents for the VIREON ecosystem.

**Philosophy**: Build what the ADRs and constitution describe. Ship what you build. Only prune what doesn't benefit the project.

## Documents

| # | File | What It Contains |
|---|------|-----------------|
| 1 | `ANTIGRAVITY_BUILD_RULES.md` | **The full rulebook.** 38 rules across 9 parts. The binding engineering contract. |
| 2 | `ANTIGRAVITY_BUILD_RULES_CHEATSHEET.md` | One-line summary of every rule. Quick reference. |
| 3 | `ANTIGRAVITY_PHASE_MAP.md` | Visual dependency map of all 6 build phases (Foundation → A → E) with release cadence. |
| 4 | `ANTIGRAVITY_DELETION_CHECKLIST.md` | What gets deleted (13 items) vs built (30 features) vs kept (15 components). |
| 5 | `ANTIGRAVITY_TWO_REPO_BOUNDARY_SPEC.md` | Exact directory structures, dependencies, and import boundaries for Vireon and vireon-lab. |
| 6 | `ANTIGRAVITY_FIRST_WEEK_CHECKLIST.md` | Day-by-day checklist for the first 7 days. |
| 7 | `EXECUTIVE_SUMMARY.md` | Audit findings and scores (the problem statement). |
| 8 | `ARCHITECTURE_AUDIT.md` | Deep architectural analysis. |
| 9 | `SECURITY_AUDIT.md` | Security findings and recommendations. |
| 10 | `PERFORMANCE_AUDIT.md` | Performance bottlenecks and targets. |
| 11 | `SCIENTIFIC_VALIDITY.md` | Determinism and reproducibility analysis. |
| 12 | `DEVELOPER_EXPERIENCE.md` | Onboarding and DX assessment. |
| 13 | `DOCUMENTATION_AUDIT.md` | Documentation quality and gaps. |
| 14 | `REPOSITORY_BOUNDARIES.md` | Repository structure analysis. |
| 15 | `DEPENDENCY_ANALYSIS.md` | Dependency graph and health. |
| 16 | `TECHNICAL_DEBT.md` | Catalog of 18 debt items. |
| 17 | `RISK_REGISTER.md` | 30 risks with severity and mitigation. |
| 18 | `RECOMMENDATIONS.md` | 30 actionable recommendations. |
| 19 | `ROADMAP_REVIEW.md` | Roadmap assessment and realistic timeline. |
| 20 | `FINAL_VERDICT.md` | Scores, verdict questions, top 10 blockers, realistic ceiling. |

## Key Decisions (User-Directed)

These reflect explicit user directives that override any audit recommendation to the contrary:

1. **Vireon and vireon-lab remain separate repos.** Vireon is for serious work (BCI vendor integrations, regulatory evaluation, security research). vireon-lab is for students and new researchers (educational UI, tutorials, knowledge base). They serve different audiences with different expectations.

2. **Build everything described in the ADRs and constitution if it benefits the project.** The 15 ADRs are treated as a specification to implement, not aspirations to defer. Each ADR gets a dedicated test suite and a build phase. If an ADR's implementation would not benefit the project (e.g., it solves a problem VIREON doesn't have), it gets pruned — but the default is build, not prune.

3. **workspace, .github, and neurodsl repos are absorbed into Vireon.** These three repos are either empty (workspace), governance-only (.github), or a core runtime component (neurodsl). They don't justify separate repos. Their assets move into Vireon's directory structure. See `ANTIGRAVITY_TWO_REPO_BOUNDARY_SPEC.md` for the exact layout.

4. **The circular dependency is resolved by direction.** vireon-lab depends on vireon. vireon never imports from vireon-lab. This is enforced by architecture boundary tests in CI. All domain logic currently in vireon-lab that vireon needs must be extracted into vireon or into a shared package.

## How to Use These Documents

1. Start with `ANTIGRAVITY_BUILD_RULES.md` — read it front to back. This is the contract.
2. Use `ANTIGRAVITY_BUILD_RULES_CHEATSHEET.md` for quick reference during coding.
3. Use `ANTIGRAVITY_PHASE_MAP.md` to understand what depends on what and when.
4. Use `ANTIGRAVITY_DELETION_CHECKLIST.md` to know exactly what's removed, built, and kept.
5. Use `ANTIGRAVITY_TWO_REPO_BOUNDARY_SPEC.md` for import boundaries and directory layout.
6. Use `ANTIGRAVITY_FIRST_WEEK_CHECKLIST.md` to start immediately.
7. The remaining documents (7–20) are the audit that produced these rules. Read them for context on why each rule exists.