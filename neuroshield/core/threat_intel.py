import os
import json
from typing import Optional, Dict, Any, List

class ThreatIntelligence:
    """
    Threat Intelligence Engine backed by the TARA (Therapeutic Atlas of Risks and Applications) registry.
    Loads the neurosecurity/datalake/qtara-registrar.json file to map simulated anomalies
    to real-world documented neural threats and their corresponding NISS scores.
    """
    def __init__(self, registry_path: str):
        self.registry_path = registry_path
        self.techniques: Dict[str, Any] = {}
        self.tactics: Dict[str, Any] = {}
        self._load_registry()

    def _load_registry(self):
        try:
            with open(self.registry_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Load tactics
                for tactic in data.get('tactics', []):
                    self.tactics[tactic['id']] = tactic
                
                # Load techniques
                for tech in data.get('techniques', []):
                    self.techniques[tech['id']] = tech
            
            print(f"[ThreatIntel] Loaded {len(self.techniques)} TARA techniques and {len(self.tactics)} tactics.")
        except Exception as e:
            print(f"[ThreatIntel] Error loading TARA registry from {self.registry_path}: {e}")

    def resolve_attack(self, attack_name: str) -> Optional[Dict[str, Any]]:
        """
        Maps an internal simulation attack name to a TARA technique.
        Returns a dictionary containing the technique details and NISS score.
        """
        # Mapping simulation attack types to TARA IDs
        mapping = {
            "noise": "QIF-T0001",           # Signal injection
            "drift": "QIF-T0040",           # Signal drift/degradation (approximated, let's look for a better one later, fallback to a standard injection)
            "impedance": "QIF-T0025",       # Physical tampering / Electrode impedance manipulation
            "suppression": "QIF-T0042",     # Denial of service / Signal suppression
            "stimulation_leak": "QIF-T0002", # Neural ransomware / Closed-loop manipulation
            "pairing_fail": "QIF-T0088",    # BLE pairing disruption
            "mtu_abuse": "QIF-T0089",       # Protocol MTU abuse
        }
        
        # Some default mappings for common anomalies
        if attack_name == "drift":
            tara_id = "QIF-T0020" # Hardware/Sensor degradation
        elif attack_name == "suppression":
            tara_id = "QIF-T0045" # Neural DoS
        else:
            tara_id = mapping.get(attack_name)
        
        if not tara_id and attack_name != "none":
            # Just default to general signal injection for unknown simulated attacks
            tara_id = "QIF-T0001" 

        if tara_id and tara_id in self.techniques:
            tech = self.techniques[tara_id]
            return {
                "tara_id": tech.get("id"),
                "name": tech.get("attack", "Unknown Attack"),
                "severity": tech.get("severity", "unknown"),
                "niss_vector": tech.get("niss", {}).get("vector", "N/A"),
                "niss_score": tech.get("niss", {}).get("score", 0.0),
                "description": tech.get("notes", ""),
                "dual_use": tech.get("tara", {}).get("dual_use", "unknown"),
                "clinical_analog": tech.get("tara", {}).get("clinical", {}).get("therapeutic_analog", "None")
            }
        
        return None
