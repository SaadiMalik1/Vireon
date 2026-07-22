# ADR 016: Clinical Algorithm Decoupling from Runtime Kernel

## Status
Accepted — Implemented

## Context
Constitution Invariant 2 mandates: "The runtime shall never contain clinical algorithms."
Previously, `vireon.runtime.twin` contained an embedded `ClinicalState` dataclass (`niss_score`, `dsm5_diagnosis`, `tissue_damage_risk`, `hazard_state`) and evaluated clinical risk thresholds (`stimulation_amplitude_ma > 3.0`) directly inside the runtime physics loop. This embedded clinical domain concepts into the kernel orchestration layer.

## Decision
We decouple clinical algorithm evaluation and domain schemas from the runtime kernel:
1. **Schema Relocation:** `ClinicalState` dataclass is moved to `vireon/sdk/schemas/clinical.py` so external clinical providers can consume it via the SDK.
2. **Runtime Decoupling:** `DigitalTwin` retains only generic physical telemetry (`SignalState`, `PhysicsState`, `BatteryState`, `SimClock`).
3. **Provider Encapsulation:** Clinical risk, biomarker evaluation, and neurostimulation safety thresholds are delegated to external providers implementing `IClinicalProviderV1` (e.g., `DefaultClinicalProvider`).

## Consequences
- **Positive:** Ensures strict compliance with Constitution Invariant 2.
- **Positive:** Enables third-party medical device manufacturers and clinical researchers to plug in custom diagnostic algorithms without modifying the core runtime.
- **Negative:** Requires external clinical providers to subscribe to telemetry events to evaluate clinical risk.
