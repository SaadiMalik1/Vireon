# Scientific Validity Assessment — Architecture Review Board

**Subject:** Vireon Lab — Neural Signal Integrity Platform
**Review Date:** 2025
**Verdict:** **1 / 10** — Illusory Rigor

> The system creates a convincing illusion of scientific rigor through terminology (NISS scores, DSM-5 mapping, ISO 27005 severity levels, STRIDE threat models) without the underlying empirical validation that would make any of these meaningful. A researcher **cannot trust** results produced by this platform in its current state.

---

## 1. Determinism Failures

**Severity: Critical**

The `ReplayPackage` stores numpy random seeds with the explicit intent of enabling deterministic replay of attack simulations. However, this design rests on a fundamental misunderstanding of numerical determinism:

- **Numpy is not deterministic across platforms or versions.** The CPython/numpy PRNG implementation has changed between minor versions (1.19→1.20→1.24), altering the exact sequence of floats produced from identical seeds. A replay package created on numpy 1.24.0 on x86_64 Linux will produce different results on numpy 1.26.0 or on aarch64 macOS.
- **Floating-point operation ordering is not guaranteed** across compilers, optimization levels, or CPU architectures. IEEE 754 defines the *representation* of floats, not the *order* in which operations are evaluated. SIMD vectorization (AVX2 vs. SSE), FMA instructions, and compiler flags (`-ffast-math`, `-O2` vs. `-O3`) all change summation order and therefore results.
- **The claimed "compiler-pinned determinism" (referenced as ADR-013) does not exist.** There is no ADR-013 in the repository. The entire determinism guarantee is a phantom reference.
- **No cross-platform reproducibility testing exists.** There are no CI matrices that run the replay engine across OS/architecture/compiler combinations to validate deterministic behavior.

**Implication:** A researcher who publishes results from this platform cannot guarantee that another lab will reproduce identical numbers. The seed-based "determinism" is a false promise.

---

## 2. Benchmark Reproducibility

**Severity: Critical**

No meaningful benchmarks exist in this project:

- The `benchmarks/` directory is a stub containing placeholder files with no executable benchmark code.
- The only performance data referenced anywhere in the codebase is **0.86–1.5 ms latency on synthetic data**, which is reported without: hardware specifications, software versions, dataset size, attack complexity, statistical confidence intervals, or comparison baselines.
- The synthetic evaluation dataset exhibits **perfect separability (AUC = 1.000)**. This means the classification task is trivially easy — the attacks are so obviously different from clean signals that any linear classifier achieves perfect performance. This proves nothing about the system's ability to detect subtle, realistic adversarial perturbations.
- No comparison against established baselines (e.g., standard anomaly detection on EEG signals) is provided.
- No benchmark framework (e.g., Criterion.rs, pytest-benchmark, asv) is integrated.

**Implication:** There is no evidence the system performs well on anything other than a trivially easy toy problem. Performance claims are unverifiable.

---

## 3. Experiment Verification

**Severity: High**

The `ValidationArtifact` data structure is intended to capture and verify experimental results, but lacks fundamental integrity mechanisms:

- **No schema versioning.** If the shape of `ValidationArtifact` changes between releases, older experiment artifacts cannot be validated or migrated. There is no version field, no schema registry, and no migration path.
- **No standardized experiment format.** Experiments are defined ad-hoc in code with no machine-readable specification (no MLflow, no W&B integration, no DVC tracking, no experiment YAML/JSON schema).
- **ReplayPackage has no provenance chain.** There is no record of: which code version produced the package, what configuration was used, what random seed (beyond the per-attack seed), who ran it, or when. This is the minimum required for scientific reproducibility (cf. the "Reproducibility Spectrum" from ACM BADS).
- **No experiment registry.** There is no central catalog of experiments that have been run, their status, and their results.

**Implication:** A researcher cannot determine whether a given `ValidationArtifact` was produced by the current code, a previous version, or was manually modified. There is no chain of custody for experimental results.

---

## 4. Documented Assumptions

**Severity: High**

### Threat Models

The threat modeling uses STRIDE methodology, which is appropriate for software security. However:

- **No attack probability estimates** are provided. STRIDE identifies *possible* threats, not *probable* ones. A threat model without probability weighting cannot guide resource allocation.
- **No adversary capability model** exists. What resources does the attacker have? Physical access to the device? Network access? Can they modify firmware? Can they collude with a clinician? Without defining the adversary, the threat model is a list of hypotheticals.
- **No success criteria** for attacks are defined. What constitutes a "successful" adversarial perturbation? A 5% shift in alpha band power? A misdiagnosis? A patient harm event? Without defining success, the model cannot distinguish nuisance from danger.

### Clinical Simulations

- **No validation against real patient data.** All simulations use synthetic EEG data generated from statistical models. Synthetic EEG does not capture the full complexity of real neural signals, including artifact patterns, electrode impedance variation, amplifier noise profiles, or inter-subject variability.
- **No clinical domain expert review** is documented. DSM-5 mapping and NISS scoring appear to be the product of engineering judgment, not clinical validation.

**Implication:** The threat model is a useful engineering exercise but cannot be cited as evidence of clinical risk. The clinical simulations prove the system works on synthetic data, which was already known by construction.

---

## 5. Replay Guarantees

**Severity: Critical**

The `ReplayEngine` is a core component that plays back recorded neural signal data through attack pipelines. Its integrity depends on a chain of dependencies, **none of which are pinned or validated**:

| Dependency | Required for Determinism | Pinned? | Validated at Replay Time? |
|---|---|---|---|
| numpy version | PRNG sequence | ❌ | ❌ |
| Python version | Float coercion, int behavior | ❌ | ❌ |
| scipy/sklearn versions | Algorithm implementations | ❌ | ❌ |
| OS / kernel | FPU behavior, thread scheduling | ❌ | ❌ |
| CPU architecture | SIMD instructions, FMA | ❌ | ❌ |
| Compiler flags | Optimization-level-dependent FP | ❌ | ❌ |
| Rust toolchain | Signal processing kernels | ❌ | ❌ |

- **No lockfile exists** (no `poetry.lock`, `uv.lock`, `requirements.txt` with hashes, or `Cargo.lock`).
- **No runtime environment validation.** The replay engine does not check whether the current environment matches the recording environment before playback.
- **No container-based reproducibility.** No Dockerfile, no OCI image, no Nix flake — there is no way to create a reproducible execution environment.

**Implication:** Replay results are not reproducible across any two distinct environments. The core value proposition of the platform — deterministic replay of attack scenarios — is fundamentally broken.

---

## 6. Evidence Pipeline Integrity

**Severity: Critical**

The evidence pipeline uses cryptographic hashes to ostensibly guarantee result integrity:

- **Dummy SHA-256 signatures are used.** The hash computation exists, but there is no key management, no signature verification, and no trust anchor. The hashes are computed and stored but never verified against a known-good value.
- **No code signing.** There is no mechanism to verify that the analysis code itself has not been tampered with. A malicious actor could modify the detection algorithm and re-compute the hashes.
- **No immutable audit log.** Results are stored in mutable files with no append-only storage, no Merkle tree, no blockchain anchoring, not even a write-once S3 bucket.
- **No separation of duties.** The same code that generates results also generates their hashes. There is no independent verification path.

**Implication:** A researcher cannot verify that results haven't been tampered with — by anyone, including the platform developers. The cryptographic infrastructure provides a false sense of integrity.

---

## 7. DSM-5 Mapping Validity

**Severity: High**

The `ThreatAtlas` maps adversarial attack patterns to DSM-5 diagnostic clusters. While creative, this mapping has severe scientific limitations:

- **No clinical validation has been performed.** No IRB-approved study, no clinical expert panel review, no patient data correlation.
- **The mapping is a taxonomic exercise, not a clinical finding.** It is a structural analogy ("this type of signal interference is *similar in pattern* to this diagnostic cluster"), not an empirical claim supported by evidence.
- **No false-positive/false-negative analysis.** If the system maps an artifact to a DSM-5 cluster, how often is that mapping clinically meaningful vs. spurious?
- **Potential for clinical harm.** If this mapping is ever used in a clinical decision-support context, it could lead to misdiagnosis. The documentation does not include adequate warnings about this risk.
- **DSM-5 itself has known limitations** (reliability concerns, categorical vs. dimensional debate) that are not acknowledged.

**Implication:** The DSM-5 mapping is an interesting hypothesis for future research, but presenting it as a feature of a production system is scientifically irresponsible.

---

## 8. NISS Scoring Validity

**Severity: High**

The Neural Impact Severity Score (NISS, 0–10 scale) is presented as a quantitative measure of neurological harm from adversarial signal interference:

- **No clinical validation exists.** The score has not been validated against any clinical outcome measure.
- **The mapping from signal interference metrics to neurological harm is unvalidated.** The relationship between (e.g.) alpha-band power suppression and cognitive impact is an active area of neuroscience research with no consensus.
- **No inter-rater reliability data.** If two clinicians were asked to rate the same attack's severity, would they agree? This is unknown.
- **No sensitivity/specificity data.** Does a NISS of 7 accurately distinguish between harmful and benign interference? Unknown.
- **The 0–10 scale implies precision that does not exist.** There is no evidence that the difference between NISS 4.2 and 4.3 is meaningful.

**Implication:** NISS is an engineering score with a medical-sounding name. Without clinical validation, it should not be used in any context where it might influence clinical decisions or be cited in scientific literature as a measure of harm.

---

## 9. Physics Fidelity

**Severity: Medium**

The platform includes physics-based simulations for hardware effects:

### Battery Simulation (Peukert's Law)
- Peukert's Law is a reasonable first-order model for lead-acid battery discharge.
- However: no validation against hardware measurements from actual EEG amplifier batteries. Real-world battery behavior is affected by temperature, age, charge cycles, and cell imbalance — none of which are modeled.
- The model parameters (Peukert exponent) are assumed, not measured.

### ADC Saturation (ADS1299 Limits)
- The ADS1299 reference limits are correctly cited from the datasheet.
- However: no validation that the simulation produces output matching real ADS1299 behavior under saturation. Real ADC behavior includes non-linear clipping, input multiplexer crosstalk, and reference voltage drift under load.

**Implication:** These are reasonable engineering approximations for a v0.1 prototype, but they should not be presented as validated physics models. The gap between simulation and hardware could be significant enough to invalidate security conclusions drawn from the simulation.

---

## 10. Statistical Rigor

**Severity: Critical**

The quantitative validation presented in the codebase has severe methodological problems:

### Synthetic Corpus Validation

- **95% CI for Sensitivity: 38.9% – 75.0%.** This enormous confidence interval reflects a tiny sample size or high variance — likely both. A sensitivity that could be as low as 38.9% is clinically unacceptable for any safety-critical application.
- **No power analysis** was performed to determine the required sample size. The sample size appears to be arbitrary.

### Real-World EDF Test

- **AUC = 1.000** on the real-world EDF test dataset. This is a red flag indicating a trivially easy problem:
  - Synthetic attacks injected into known-clean data are *obviously* different from the baseline. Any competent anomaly detector would achieve perfect separation.
  - This does not test the system's ability to distinguish adversarial perturbations from natural signal variation, electrode artifacts, or benign interference.
  - A realistic evaluation would use adversarial examples specifically designed to evade detection, not synthetic attacks with obviously different statistical properties.
- **No cross-validation.** A single train/test split with AUC 1.0 provides no estimate of generalization performance.
- **No comparison to baselines.** Without knowing what a simple threshold detector or standard ML classifier would achieve on the same data, the AUC of 1.0 is uninterpretable.

### General Statistical Issues

- No multiple comparison correction (Bonferroni, FDR) is applied anywhere.
- No effect size reporting (Cohen's d, odds ratios).
- No normality testing before parametric tests.
- Confidence intervals are reported for some metrics but not others, with no consistent policy.

**Implication:** The statistical evidence presented does not support the claimed capabilities of the system. The perfect AUC indicates a flawed evaluation methodology, not a perfect system.

---

## Summary

| Dimension | Status | Impact on Scientific Trust |
|---|---|---|
| Determinism | **Broken** | Results are not reproducible across environments |
| Benchmarks | **Absent** | Performance claims are unverifiable |
| Experiment Verification | **Absent** | No provenance chain for results |
| Assumptions | **Undocumented** | Threat model has no calibrated risk assessment |
| Replay Guarantees | **Broken** | Core feature does not work as documented |
| Evidence Integrity | **Theatrical** | Cryptographic hashes provide no real integrity |
| DSM-5 Mapping | **Unvalidated** | Taxonomic exercise presented as clinical insight |
| NISS Scoring | **Unvalidated** | Engineering score with no clinical grounding |
| Physics Fidelity | **Approximate** | Reasonable first-order, no hardware validation |
| Statistical Rigor | **Deficient** | Flawed methodology, trivial evaluation |

### Final Score: 1 / 10

The single point is awarded for the *ambition* of the system design — the ADRs describe an architecture that, if fully implemented and validated, would be scientifically valuable. But ambition is not evidence. The system as it exists today is a sophisticated taxonomic and architectural framework wrapped around toy implementations and unvalidated claims. No researcher should trust, cite, or build upon results from this platform without independent re-implementation and validation.

---

*This review was conducted by an independent architecture review board. Findings are based on static analysis of the source code, documentation, and test infrastructure as of the review date.*