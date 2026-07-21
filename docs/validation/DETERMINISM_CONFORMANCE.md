# Determinism Conformance Report (v1.0)

## 1. Compliance Status
- **Status**: **NON-COMPLIANT** (Critical Blocker for Research Reproducibility)

## 2. Determinism Violations
- **Host Clock Reliance**: The current runtime event loop advances based on the host operating system's wall-time rather than a strict, deterministic internal logical clock.
- **RNG Seeding**: Random Number Generators across simulation providers and physics engines are locally seeded, preventing split-seed deterministic reproducibility.
- **Threading Anomalies**: Race conditions in multi-threaded providers yield non-deterministic state graph outcomes depending on scheduler interleaving.

## 3. Required Kernel Transition
To achieve the Phase 8 requirements:
1. **Clock Ownership**: The Kernel must fully own the simulation clock. Providers may only advance state based on the Kernel's tick.
2. **Seed Ownership**: The Kernel must initialize and distribute a deterministic RNG seed to all sandboxed providers via the capability manifest.
3. **Replay Bundles**: Scientific runs must emit trace logging (input state, capability grants, logical clock ticks, RNG seeds) enabling 100% hash-validated reproducibility.

## 4. Next Steps
- Draft `ADR-004-deterministic-execution.md` to define the architectural shift.
- Implement Certification Mode and HIL Mode.
