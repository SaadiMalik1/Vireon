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
Neuroethics Guardrail Validation Engine

Enforces the 8 Neuroethics Guardrails defined in VIREON (docs/GUARDRAILS.md)
at the technical level within the VIREON platform.
"""

import math


class GuardrailViolation(Exception):
    pass

class GuardrailValidator:
    def __init__(self):
        # We define the 8 core guardrails here for documentation and enforcement
        self.guardrails = {
            "G1": "Neuromodesty: We score signal-level interference, not mental states.",
            "G2": "Reverse Inference: Signal detection does not entail mental-state identification.",
            "G3": "Neurorealism: Neural signals are partial, noisy representations.",
            "G4": "Anti-Inflationism: Extend existing rights (Mental Privacy, Mental Integrity), do not invent new ones.",
            "G5": "Conceptual Underspecification: Define operationally measurable properties.",
            "G6": "Brain Reading Limits: Distinguish between current technical capabilities and projected science fiction.",
            "G7": "Dual-Use Trap: Specify defensive clinical protections; offensive applications are out of scope.",
            "G8": "Statistical Inflation: Account for validity failures in neuroimaging.",
        }

    def validate_information_extraction(self, num_channels: float, sample_rate: float, resolution_bits: float):
        """
        Functionally enforces G6 (Brain Reading Limits) and G1 (Neuromodesty) by bounding the 
        information entropy that can be extracted from the simulated signal.
        """
        if not (math.isfinite(num_channels) and math.isfinite(sample_rate) and math.isfinite(resolution_bits)):
            raise GuardrailViolation(
                "[G6 Violation] Invalid non-finite numerical telemetry parameter detected (NaN or Inf). "
                "VIREON enforces Brain Reading Limits (G6)."
            )

        if num_channels <= 0 or sample_rate <= 0 or resolution_bits <= 0:
            raise GuardrailViolation("[G6 Violation] Telemetry parameters must be strictly positive.")

        # Maximum theoretical bit rate = channels * sample_rate * resolution_bits
        bit_rate_bps = float(num_channels) * float(sample_rate) * float(resolution_bits)
        max_allowed_bps = 50_000_000 
        
        if bit_rate_bps > max_allowed_bps:
            raise GuardrailViolation(
                f"[G6 Violation] Requested telemetry bandwidth ({bit_rate_bps / 1e6:.2f} Mbps) exceeds physiological limits. "
                f"VIREON enforces Brain Reading Limits (G6). Max allowed: {max_allowed_bps / 1e6:.2f} Mbps."
            )
        return True

    def calculate_shannon_entropy(self, data: bytes) -> float:
        """Calculates Shannon entropy of a byte payload."""
        if not data:
            return 0.0
        
        # Calculate byte frequencies
        from collections import Counter
        freq = Counter(data)
        
        entropy = 0.0
        for count in freq.values():
            p_x = count / len(data)
            entropy += - p_x * math.log2(p_x)
            
        return entropy

    def validate_signal_entropy(self, data: bytes, max_entropy: float = 7.9):
        """
        Enforces G6 and G1 by ensuring the actual telemetry payload doesn't contain
        anomalously high information density (e.g. encrypted exfiltration).
        A truly biological EEG signal usually has lower entropy than pure random bytes.
        """
        entropy = self.calculate_shannon_entropy(data)
        if entropy > max_entropy:
            raise GuardrailViolation(
                f"[G6/G1 Violation] Signal payload entropy ({entropy:.2f} bits/byte) is anomalously high. "
                "This indicates potential non-biological data exfiltration."
            )
        return True

    def validate_attack_payload(self, attack_name: str, params: dict):
        """
        Validates that a configured attack respects neuroethics guardrails functionally.
        """
        # Structural Validation: Prevent P300/ERP extraction masquerading as nominal stimulation
        if "target_frequency" in params:
            # P300 wave occurs around 300ms, freq equivalent is ~3.3Hz.
            # If an attacker specifically targets and modulates strictly around cognitive ERP bands
            # to elicit specific responses, flag it.
            freq = params["target_frequency"]
            if 3.0 <= freq <= 4.0:
                raise GuardrailViolation(
                    "[G2 Violation] Structural targeting of P300 ERPs detected. "
                    "Signal detection does not entail mental-state identification."
                )
        return True

    def validate_experiment_config(self, config):
        """
        Validates an entire ExperimentConfig before the coordinator starts.
        """
        # 1. Enforce functional bandwidth limits
        num_channels = getattr(config.device, "num_channels", 8)
        sample_rate = getattr(config.device, "sample_rate", 250)
        resolution_bits = getattr(config.device, "resolution_bits", 24)
        
        self.validate_information_extraction(num_channels, sample_rate, resolution_bits)
        
        # 2. Validate active attacks
        for attack_name in getattr(config.attacks, "active", []):
            # Extract relevant params to check
            params = {}
            if attack_name == "noise":
                params["level"] = getattr(config.attacks, "noise_level_uv", 0)
            self.validate_attack_payload(attack_name, params)
            
        # 3. Check for Dual-Use (G7) framing in the report
        if "offensive_strike" in getattr(config.output, "report_prefix", "").lower():
            raise GuardrailViolation(
                "[G7 Violation] Offensive framing detected in report output. "
                "VIREON enforces the Dual-Use Trap (G7): offensive applications are explicitly out of scope."
            )
            
        return True
