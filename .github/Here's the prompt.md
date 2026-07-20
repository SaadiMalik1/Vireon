Here's the prompt. It's designed to be self-contained — an LLM receiving it doesn't need your Constitution document, the audit, or our conversation. Everything it needs is embedded.

---

```
# Task: Execute the VIREON Architectural Extraction

You are refactoring the VIREON neurotechnology validation framework to align its implementation with its Architecture Constitution. The Constitution defines a thin, domain-agnostic runtime; the current implementation has domain logic folded into the runtime. Your job is to extract that domain logic into provider packages while preserving all existing behavior.

## Critical Rules

1. **MOVE ONLY.** When extracting a file from the runtime to a provider, do not refactor, optimize, or rewrite the code. Change only the import paths. The code after extraction must be behaviorally identical to the code before extraction. Refactoring happens later.
2. **CI MUST PASS AFTER EVERY FILE MOVE.** After moving each file, run the test suite. If it fails, fix the import paths and try again before moving the next file. Never accumulate broken moves.
3. **LEAF-FIRST ORDER.** Extract files that have no runtime dependents first. Extract files that are depended upon by other runtime modules last. This prevents circular dependencies during migration.
4. **NO NEW FEATURES.** Do not add functionality during the extraction. Bug fixes are allowed only if they are required to make tests pass after a move.

## The Current Structure

```

vireon/
    core/
        coordinator.py          (416 LOC — god class, splits later)
        twin.py                 (535 LOC — god class, splits later)
        detection.py            (568 LOC — IDS algorithms)
        capability_engine.py    (no-op validate_manifest)
        physics.py              (Pennes bioheat, thermal)
        dynamics.py             (Kuramoto oscillator, neural dynamics)
        safety_envelope.py      (clinical risk models)
        protocol.py             (BLE, serial, USB)
        privacy.py              (privacy analysis)
        privacy_leakage.py      (leakage quantification)
        attack_factory.py       (red-team attacks)
        redteam.py              (adversarial testing)
        threat_intel.py         (threat intelligence)
        compliance.py           (IEC 62304, ISO 14971)
        authentication.py       (auth tokens, sessions)
        validation.py           (clinical validation)
        e2ee.py                 (E2EE with X25519+AES-GCM)
        event_bus.py            (keep in runtime)
        state_store.py          (keep in runtime)
        lifecycle.py            (keep or create)
        config.py               (keep, rename to configuration.py)
    sdk/
        (existing interfaces)
vireon-lab/
    (reports, tutorials — couples to core internals)
neurodsl/
    (Rust forge + scribe + PyO3 — separate, leave alone)

```

## The Target Structure

```

vireon/
    runtime/
        orchestrator.py         # from coordinator.py (orchestration parts only)
        scheduler.py            # from coordinator.py (scheduling parts only)
        lifecycle.py            # from coordinator.py (lifecycle parts only)
        event_bus.py            # moved from core/event_bus.py
        state_store.py          # moved from core/state_store.py
        capability_engine.py    # FIXED — real enforcement, not no-op
        registry.py             # from coordinator.py (registration parts)
        provider_loader.py      # from coordinator.py (loading parts)
        configuration.py        # from core/config.py
        isolation.py            # new or extracted from provider_loader
        __init__.py
    sdk/
        interfaces.py           # Provider, Plugin, Capability base classes
        manifest.py             # CapabilityManifest schema
        events.py               # Event type definitions + EventBusProxy
        state.py                # StateStoreProxy
        capabilities.py         # Capability enums and helpers
        errors.py               # VIREON exception hierarchy
        __init__.py
providers/
    physics/
        __init__.py
        thermal.py              # from core/physics.py (Pennes equation)
        adc.py                  # from core/twin.py (ADC state)
        electrode.py            # from core/twin.py (electrode impedance)
    dynamics/
        __init__.py
        kuramoto.py             # from core/dynamics.py
        erp.py                  # from core/dynamics.py (P300, ERP)
    firmware/
        __init__.py
        cortexm.py              # from core/twin.py (firmware version, bootloader)
    protocol/
        __init__.py
        ble.py                  # from core/protocol.py
        serial.py               # from core/protocol.py
    ids/
        __init__.py
        cusum.py                # from core/detection.py
        spectral.py             # from core/detection.py
        autoencoder.py          # from core/detection.py
        coherence.py            # from core/detection.py
    authentication/
        __init__.py
        tokens.py               # from core/authentication.py
        e2ee.py                 # from core/e2ee.py
    privacy/
        __init__.py
        analysis.py             # from core/privacy.py
        leakage.py              # from core/privacy_leakage.py
    threat_models/
        __init__.py
        attacks.py              # from core/attack_factory.py
        redteam.py              # from core/redteam.py
        intel.py                # from core/threat_intel.py
    clinical/
        __init__.py
        safety.py               # from core/safety_envelope.py
        compliance.py           # from core/compliance.py
        validation.py           # from core/validation.py
    power/
        __init__.py
        battery.py              # from core/twin.py (battery chemistry)
vireon-lab/
    (unchanged except: all imports of vireon.core.*→ vireon.sdk.*)
neurodsl/
    (unchanged)

```

## Execution Phases

### Phase 1: Rename core → runtime

1. Rename `vireon/core/` to `vireon/runtime/`
2. Update every import statement in the entire codebase that references `vireon.core` → `vireon.runtime`
3. Run all tests. Fix any broken imports until the full suite passes.
4. Commit with message: "refactor: rename vireon/core to vireon/runtime"

Verify: `grep -r "vireon\.core" vireon/ vireon-lab/ tests/` returns zero matches.

### Phase 2: Extract domain logic (leaf-first)

Extract in this exact order. After each extraction, run tests and commit:

**Round 1 — Standalone modules (no runtime dependents):**
- `runtime/physics.py` → `providers/physics/thermal.py` + related
- `runtime/dynamics.py` → `providers/dynamics/kuramoto.py` + related
- `runtime/privacy.py` → `providers/privacy/analysis.py`
- `runtime/privacy_leakage.py` → `providers/privacy/leakage.py`
- `runtime/threat_intel.py` → `providers/threat_models/intel.py`
- `runtime/compliance.py` → `providers/clinical/compliance.py`
- `runtime/validation.py` → `providers/clinical/validation.py`

**Round 2 — Modules depended upon by Round 1:**
- `runtime/detection.py` → `providers/ids/cusum.py`, `spectral.py`, `autoencoder.py`, `coherence.py`
- `runtime/safety_envelope.py` → `providers/clinical/safety.py`
- `runtime/attack_factory.py` → `providers/threat_models/attacks.py`
- `runtime/redteam.py` → `providers/threat_models/redteam.py`

**Round 3 — Digital twin decomposition:**
- `runtime/twin.py` → Split into:
  - `providers/physics/adc.py` (ADC voltage ranges, resolution)
  - `providers/physics/electrode.py` (electrode impedance models)
  - `providers/firmware/cortexm.py` (firmware version, bootloader state)
  - `providers/power/battery.py` (battery chemistry, voltage curves)
  - `providers/dynamics/` (neural dynamics parameters)
  - Any pure orchestration state stays in `runtime/state_store.py`

**Round 4 — Protocol and authentication:**
- `runtime/protocol.py` → `providers/protocol/ble.py`, `serial.py`
- `runtime/authentication.py` → `providers/authentication/tokens.py`

**Round 5 — E2EE and capability engine:**
- `runtime/e2ee.py` → `providers/authentication/e2ee.py`
- Fix `runtime/capability_engine.py` (see Phase 5 spec below)

**Round 6 — Coordinator decomposition:**
- `runtime/coordinator.py` → Split into:
  - `runtime/orchestrator.py` (top-level coordination)
  - `runtime/scheduler.py` (task scheduling)
  - `runtime/lifecycle.py` (provider lifecycle management)
  - `runtime/registry.py` (provider registration)
  - `runtime/provider_loader.py` (dynamic loading)

After each round:
```bash
# Run existing tests
pytest tests/ -x

# Verify no runtime imports of provider packages
python -c "
import ast, sys, pathlib
for f in pathlib.Path('vireon/runtime').rglob('*.py'):
    tree = ast.parse(f.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if 'providers' in alias.name:
                    print(f'VIOLATION: {f} imports {alias.name}')
                    sys.exit(1)
        elif isinstance(node, ast.ImportFrom):
            if node.module and 'providers' in node.module:
                print(f'VIOLATION: {f} imports from {node.module}')
                sys.exit(1)
print('Clean: runtime does not import providers')
"
```

### Phase 3: Formalize runtime ↔ provider contracts

For each provider, create a `CapabilityManifest` that declares:

- `declared_capabilities`: list of Capability enums this provider implements
- `requested_state`: list of state namespaces this provider needs read/write access to
- `requested_events`: list of event channels this provider subscribes to or publishes
- `sandbox_level`: 0 (in-process), 1 (subprocess+bubblewrap), or 2 (proposed future)

The runtime loads providers ONLY through the registry. The runtime NEVER imports a provider module directly. All communication goes through:

- `EventBusProxy` (publish/subscribe with capability-filtered access)
- `StateStoreProxy` (get/set/watch with namespace-isolated access)
- `CapabilityEngine` (validate_manifest, enforce, grant, revoke)

Update `vireon/sdk/` to define these interfaces as abstract base classes.

### Phase 4: Implement architecture tests

Create `tests/architecture/` with these tests that run in CI:

```python
# tests/architecture/test_boundary.py

def test_runtime_no_provider_imports():
    """AT-01: runtime/ must never import from providers/"""
    # Scan all files in vireon/runtime/ for 'providers' in imports
    ...

def test_providers_no_runtime_imports():
    """AT-02: providers/ must only import from sdk/, never from runtime/"""
    ...

def test_sdk_no_runtime_or_provider_imports():
    """AT-03: sdk/ must import only from stdlib"""
    ...

def test_lab_no_runtime_internals():
    """AT-04: vireon-lab/ must import only from sdk/"""
    ...

def test_no_god_classes():
    """AT-05: no single file in runtime/ exceeds 200 LOC"""
    ...

def test_every_provider_has_manifest():
    """AT-06: every provider package has a valid CapabilityManifest"""
    ...

def test_no_hardcoded_config():
    """AT-07: no hardcoded configuration in runtime/"""
    ...

def test_no_circular_imports():
    """AT-08: no circular imports between any packages"""
    ...
```

### Phase 5: Fix the capability engine

Replace the no-op implementation with real enforcement:

```python
# vireon/runtime/capability_engine.py

class CapabilityEngine:
    """Enforces the constitutional invariant:
    Plugins shall never bypass capability validation."""

    def __init__(self, allowed_capabilities: set, policy: CapabilityPolicy):
        self._allowed = allowed_capabilities
        self._policy = policy
        self._grants: dict[str, set[Capability]] = {}

    def validate_manifest(self, manifest: CapabilityManifest) -> bool:
        # 1. Schema compliance
        if not manifest.schema_valid():
            return False
        # 2. All declared capabilities are in the allowlist
        for cap in manifest.declared_capabilities:
            if cap not in self._allowed:
                return False
        # 3. Requested state namespaces are permitted
        for ns in manifest.requested_state:
            if not self._policy.namespace_allowed(ns):
                return False
        # 4. Requested event channels are permitted
        for ch in manifest.requested_events:
            if not self._policy.event_channel_allowed(ch):
                return False
        # 5. Sandbox level is within policy bounds
        if manifest.sandbox_level > self._policy.max_sandbox_level:
            return False
        return True

    def enforce(self, provider_id: str, manifest: CapabilityManifest,
                event_bus: EventBus, state_store: StateStore) -> bool:
        """Wrap provider in filtered proxies. Fail closed."""
        if not self.validate_manifest(manifest):
            return False  # Provider disabled, simulation continues

        self._grants[provider_id] = set(manifest.declared_capabilities)

        # Wrap in capability-filtered proxies
        provider._event_proxy = EventBusProxy(
            event_bus,
            allowed_channels=manifest.requested_events
        )
        provider._state_proxy = StateStoreProxy(
            state_store,
            allowed_namespaces=manifest.requested_state
        )
        return True

    def revoke(self, provider_id: str) -> None:
        """Revoke all capabilities for a provider. Fail closed."""
        if provider_id in self._grants:
            del self._grants[provider_id]
```

__Implementation strategy for enforcement:__ Deploy in audit mode first (log violations but do not deny). After one sprint with zero logged violations, promote to enforcement mode. This prevents the capability engine from breaking existing workflows during the transition.

## vireon-lab Coupling Fix

Throughout Phase 2, simultaneously update `vireon-lab/` to import only from `vireon.sdk` instead of `vireon.runtime`. Specifically:

- `vireon_lab/reports/generator.py` currently imports from `vireon.core` internals — change to import from `vireon.sdk.interfaces`
- Any direct access to runtime state must go through `StateStoreProxy`
- Any direct event subscription must go through `EventBusProxy`

## Verification

After all phases are complete, the following must be true:

1. `grep -r "vireon\.runtime" providers/` returns zero matches (providers don't import runtime)
2. `grep -r "providers\." vireon/runtime/` returns zero matches (runtime doesn't import providers)
3. `grep -r "vireon\.runtime" vireon-lab/` returns zero matches (lab doesn't import runtime)
4. `pytest tests/` passes with zero failures
5. `pytest tests/architecture/` passes (all 8 architecture tests green)
6. The runtime directory contains ≤15 .py files, none exceeding 200 LOC
7. Every provider package has an `__init__.py` that exports a class implementing the Provider interface from sdk
8. The capability engine's `validate_manifest()` rejects invalid manifests (test this explicitly)

## What NOT to Do

- Do not rewrite algorithms during extraction (Kuramoto stays Kuramoto, just in a different directory)
- Do not add new capabilities, endpoints, or features
- Do not change the public API surface of vireon/sdk/
- Do not modify neurodsl/ at all
- Do not skip running tests after any file move
- Do not proceed to the next round if the current round has failing tests
- Do not "clean up" code while moving it — move only, refactor later

```

---

A few things I'd note about using this prompt:

**It's deliberately prescriptive about order.** The leaf-first extraction sequence matters — if you extract `coordinator.py` first, everything breaks because everything depends on it. If you extract `physics.py` first, nothing breaks because nothing in the runtime depends on physics.

**The "move only" rule is the most important line.** Every failed architectural extraction I've seen failed because someone tried to improve the code while moving it. Once you refactor and move at the same time, you can't tell which caused a regression.

**The architecture tests are the lock.** Without them, the extraction will gradually erode. Someone will add "just one small import" from a provider into the runtime, and within six months you're back where you started. The tests make the boundary machine-enforced, not convention-enforced.

**The audit-mode deployment for the capability engine prevents a hard cutover from breaking everything.** It's the same pattern as deploying a new firewall rule in log-only mode before switching to enforce.
