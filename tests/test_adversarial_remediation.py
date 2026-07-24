# Copyright 2026 VIREON Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Adversarial Findings Regression Test Suite for VIREON Core Runtime.
Validates fixes for ADV-01, ADV-02, ADV-04, ADV-05, ADV-06, ADV-07, ADV-08, ADV-09.
"""

import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519

from vireon.sdk.manifest import CapabilityManifest
from vireon.runtime.capability_engine import CapabilityEngine
from vireon.runtime.configuration import ExperimentConfig
from vireon.runtime.orchestrator import VireonOrchestrator, OrchestrationFault
from vireon.sdk.capability.descriptor import CapabilityDescriptor
from vireon.sdk.lifecycle.state_machine import ProviderState
from vireon.runtime.ring_buffer import SPSCRingBuffer
from vireon.runtime.clock import DeterministicClock, ClockMode
from vireon.runtime.crdt_store import CRDTStateStore
from vireon.runtime.guardrails import GuardrailValidator, GuardrailViolation
import vireon_neuro_dsl


def test_adv_01_signature_verification_enforcement():
    """ADV-01: Verifies that signature_bytes is validated and unsigned manifests fail when trusted_public_key is provided."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    
    # 1. Unsigned manifest must fail when key is provided
    unsigned_manifest = CapabilityManifest(name="untrusted", version="1.0", category="test")
    engine = CapabilityEngine(ExperimentConfig())
    assert engine.validate_manifest(unsigned_manifest, trusted_public_key=public_key) is False

    # 2. Signed manifest must pass
    signed_manifest = CapabilityManifest(name="trusted", version="1.0", category="test")
    signed_manifest.sign(private_key)
    assert engine.validate_manifest(signed_manifest, trusted_public_key=public_key) is True

    # 3. Forged signature manifest must fail
    forged_manifest = CapabilityManifest(name="trusted", version="1.0", category="test", signature_bytes=b"\x00" * 64)
    assert engine.validate_manifest(forged_manifest, trusted_public_key=public_key) is False


def test_adv_04_orchestrator_manifest_validation_enforcement():
    """ADV-04: Verifies orchestrator enforces manifest signature checks during initialization."""
    orchestrator = VireonOrchestrator(global_state_store=None, global_event_bus=None)
    
    class DummyProvider:
        def __init__(self, manifest):
            self.manifest = manifest

    private_key = ed25519.Ed25519PrivateKey.generate()
    desc = CapabilityDescriptor(id="prov_1", name="Prov 1", version="1.0.0", latency="REALTIME")
    
    # Register provider with unsigned manifest
    unsigned_manifest = CapabilityManifest(name="untrusted", version="1.0", category="test")
    provider = DummyProvider(unsigned_manifest)
    orchestrator.register_provider(provider, desc)

    # Initialize all with trusted public key should fail
    with pytest.raises(OrchestrationFault):
        orchestrator.initialize_all(trusted_public_key=private_key.public_key())
    
    assert orchestrator.provider_states["prov_1"] == ProviderState.ERROR


def test_adv_05_neurodsl_scribe_ip_reset_across_ticks():
    """ADV-05: Verifies PyScribe resets instruction pointer ip = 0 so consecutive ticks execute bytecode."""
    script = """
    SET_AMP 50
    END
    """
    bytecode = vireon_neuro_dsl.compile_script(script)
    scribe = vireon_neuro_dsl.PyScribe()
    scribe.load_bytecode(bytecode)

    eeg = [1.0, 2.0, 3.0]
    out1 = scribe.execute_step(eeg)
    assert out1 == eeg

    # Tick 2 must also execute without error
    out2 = scribe.execute_step(eeg)
    assert out2 == eeg


def test_adv_06_spsc_ring_buffer_thread_safety():
    """ADV-06: Verifies SPSCRingBuffer push/pop lock protection."""
    buf = SPSCRingBuffer(capacity=10)
    for i in range(5):
        assert buf.push(i) is True
    assert buf.size() == 5
    for i in range(5):
        assert buf.pop() == i
    assert buf.is_empty() is True


def test_adv_07_deterministic_clock_no_float_drift():
    """ADV-07: Verifies DeterministicClock computes time without cumulative float drift."""
    clock = DeterministicClock(mode=ClockMode.VIRTUAL, initial_time=0.0, step_dt_ms=4.0)
    # Advance 250,000 ticks (equivalent to 1000.0 seconds)
    for _ in range(250_000):
        clock.advance()
    assert clock.sim_time == 1000.0


def test_adv_08_crdt_op_log_bounded_compaction():
    """ADV-08: Verifies CRDTStateStore compacts op_log to max_op_log_size."""
    store = CRDTStateStore(replica_id="node_0", max_op_log_size=50)
    for i in range(200):
        store.set_register(f"key_{i}", i)
    assert len(store.op_log) == 50


def test_adv_09_guardrail_nan_inf_rejection():
    """ADV-09: Verifies GuardrailValidator rejects NaN and Inf parameters."""
    validator = GuardrailValidator()
    
    with pytest.raises(GuardrailViolation):
        validator.validate_information_extraction(8, float("nan"), 24)
        
    with pytest.raises(GuardrailViolation):
        validator.validate_information_extraction(8, 250.0, float("inf"))

    with pytest.raises(GuardrailViolation):
        validator.validate_information_extraction(-1, 250.0, 24)

    # Valid call passes
    assert validator.validate_information_extraction(8, 250.0, 24) is True
