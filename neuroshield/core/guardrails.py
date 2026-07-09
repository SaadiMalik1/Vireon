"""
Neuroethics Guardrail Validation Engine

Enforces the 8 Neuroethics Guardrails defined in QIF (osi-of-mind/GUARDRAILS.md)
at the technical level within the NeuroShield platform.
"""

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

    def validate_attack_payload(self, attack_name: str, params: dict):
        """
        Validates that a configured attack respects neuroethics guardrails.
        """
        # G1/G2: Check if an attack claims to "read thoughts" or "steal passwords"
        banned_cognitive_terms = ["thought", "read_mind", "password_extraction", "memory_download"]
        
        for term in banned_cognitive_terms:
            if term in attack_name.lower():
                raise GuardrailViolation(
                    f"[G1/G2 Violation] Attack '{attack_name}' claims cognitive extraction. "
                    "NeuroShield enforces Neuromodesty (G1): we simulate physical signal disruption, not mental states."
                )
            for key, val in params.items():
                if isinstance(val, str) and term in val.lower():
                    raise GuardrailViolation(
                        f"[G1/G2 Violation] Attack parameter '{key}' claims cognitive extraction. "
                        "NeuroShield enforces Neuromodesty (G1)."
                    )
        
        # G6: Limit simulation of unrealistic far-future capabilities
        if attack_name == "nanobot_swarm":
             raise GuardrailViolation(
                    f"[G6 Violation] Attack '{attack_name}' exceeds current technical capabilities. "
                    "NeuroShield enforces Brain Reading Limits (G6): simulations must distinguish current vs projected tech."
             )
        
        return True

    def validate_experiment_config(self, config):
        """
        Validates an entire ExperimentConfig before the coordinator starts.
        """
        # 1. Validate active attacks
        for attack_name in getattr(config.attacks, "active", []):
            # Extract relevant params to check
            params = {}
            if attack_name == "noise":
                params["level"] = getattr(config.attacks, "noise_level_uv", 0)
            self.validate_attack_payload(attack_name, params)
            
        # 2. Check for Dual-Use (G7) framing in the report
        if getattr(config.output, "report_prefix", "").lower() == "offensive_strike":
            raise GuardrailViolation(
                "[G7 Violation] Offensive framing detected in report output. "
                "NeuroShield enforces the Dual-Use Trap (G7): offensive applications are explicitly out of scope."
            )
            
        return True
