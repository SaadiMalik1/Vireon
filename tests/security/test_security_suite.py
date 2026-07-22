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
Exhaustive Phase 7 & Phase 8 Security, Adversarial & Clinical Safety Validation Suite.
"""

import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519
from vireon.runtime.guardrails import GuardrailValidator, GuardrailViolation
from vireon.runtime.trace_bundle import TraceBundle
from vireon.runtime.merkle import MerkleTree
from vireon.sdk.manifest import CapabilityManifest
from vireon.runtime.capability_engine import CapabilityEngine
from vireon.runtime.configuration import ExperimentConfig, SecurityConfig, OutputConfig
from vireon.validation.clinical_rules import ClinicalRuleEvaluator, ClinicalSafetyViolation


def test_signature_forgery_rejection():
    key1 = ed25519.Ed25519PrivateKey.generate()
    key2 = ed25519.Ed25519PrivateKey.generate()
    pub2 = key2.public_key()

    tree = MerkleTree([b"trace_0", b"trace_1"])
    bundle = TraceBundle(merkle_root_hex=tree.get_root_hex(), pin_hash="valid_pin")
    bundle.sign(key1)

    assert bundle.verify_signature(pub2) is False


def test_neuroethics_guardrail_g6_bandwidth_cap():
    validator = GuardrailValidator()
    with pytest.raises(GuardrailViolation) as exc_info:
        validator.validate_information_extraction(num_channels=10000, sample_rate=10000, resolution_bits=32)
    assert "[G6 Violation]" in str(exc_info.value)


def test_neuroethics_guardrail_g2_p300_targeting():
    validator = GuardrailValidator()
    with pytest.raises(GuardrailViolation) as exc_info:
        validator.validate_attack_payload("frequency_injection", {"target_frequency": 3.5})
    assert "[G2 Violation]" in str(exc_info.value)


def test_neuroethics_guardrail_g7_offensive_framing():
    validator = GuardrailValidator()
    cfg = ExperimentConfig(output=OutputConfig(report_prefix="offensive_strike_run"))
    with pytest.raises(GuardrailViolation) as exc_info:
        validator.validate_experiment_config(cfg)
    assert "[G7 Violation]" in str(exc_info.value)


def test_zero_trust_host_access_denial():
    cfg = ExperimentConfig(security=SecurityConfig(enabled=True, enable_zta=True))
    engine = CapabilityEngine(cfg)

    untrusted_manifest = CapabilityManifest(
        name="malicious_plugin",
        version="1.0.0",
        category="plugin",
        requires_host_access=True
    )
    assert engine.validate_manifest(untrusted_manifest) is False


def test_clinical_safety_iso14708_frequency_limit():
    evaluator = ClinicalRuleEvaluator()
    with pytest.raises(ClinicalSafetyViolation) as exc_info:
        evaluator.evaluate_stimulation_parameters(amplitude_ma=2.0, pulse_width_us=200, frequency_hz=250.0)
    assert "[ISO 14708-3] Stimulation frequency" in str(exc_info.value)


def test_clinical_safety_iso14708_charge_density_limit():
    evaluator = ClinicalRuleEvaluator()
    # High amplitude (10mA) and pulse width (500us) on small electrode (0.01 cm2) -> 500 uC/cm2 (>30 uC/cm2 cap)
    with pytest.raises(ClinicalSafetyViolation) as exc_info:
        evaluator.evaluate_stimulation_parameters(amplitude_ma=10.0, pulse_width_us=500, frequency_hz=50.0, electrode_area_cm2=0.01)
    assert "exceeds tissue damage threshold" in str(exc_info.value)


def test_clinical_safety_tissue_heating_limit():
    evaluator = ClinicalRuleEvaluator()
    assert evaluator.evaluate_tissue_heating(1.2) is True
    with pytest.raises(ClinicalSafetyViolation) as exc_info:
        evaluator.evaluate_tissue_heating(2.5)
    assert "exceeds safe maximum" in str(exc_info.value)
