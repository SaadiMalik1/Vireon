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
Phase 7 Security & Adversarial Validation Suite.
"""

import pytest
from cryptography.hazmat.primitives.asymmetric import ed25519
from vireon.runtime.guardrails import GuardrailValidator, GuardrailViolation
from vireon.runtime.trace_bundle import TraceBundle
from vireon.runtime.merkle import MerkleTree
from vireon.sdk.manifest import CapabilityManifest
from vireon.runtime.capability_engine import CapabilityEngine
from vireon.runtime.configuration import ExperimentConfig, SecurityConfig, OutputConfig


def test_signature_forgery_rejection():
    key1 = ed25519.Ed25519PrivateKey.generate()
    key2 = ed25519.Ed25519PrivateKey.generate()
    pub2 = key2.public_key()

    tree = MerkleTree([b"trace_0", b"trace_1"])
    bundle = TraceBundle(merkle_root_hex=tree.get_root_hex(), pin_hash="valid_pin")

    # Sign with key1
    bundle.sign(key1)

    # Verification against key2's public key MUST fail
    assert bundle.verify_signature(pub2) is False


def test_neuroethics_guardrail_g6_bandwidth_cap():
    validator = GuardrailValidator()

    # 10,000 channels at 10,000 Hz, 32 bits = 3.2 Gbps (> 50 Mbps cap)
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
    cfg = ExperimentConfig(
        output=OutputConfig(report_prefix="offensive_strike_run")
    )

    with pytest.raises(GuardrailViolation) as exc_info:
        validator.validate_experiment_config(cfg)

    assert "[G7 Violation]" in str(exc_info.value)


def test_zero_trust_host_access_denial():
    cfg = ExperimentConfig(
        security=SecurityConfig(enabled=True, enable_zta=True)
    )
    engine = CapabilityEngine(cfg)

    untrusted_manifest = CapabilityManifest(
        name="malicious_plugin",
        version="1.0.0",
        category="plugin",
        requires_host_access=True
    )

    assert engine.validate_manifest(untrusted_manifest) is False
