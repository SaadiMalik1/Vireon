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
SDK Clinical State Schema Dataclass.
Extracted from runtime to ensure runtime kernel contains zero clinical algorithms or domain schemas (Invariant 2).
"""

from dataclasses import dataclass


@dataclass
class ClinicalState:
    niss_score: float = 0.0
    hazard_state: str = "NOMINAL"
    iso_severity: str = "NEGLIGIBLE"
    tissue_damage_risk: str = "NONE"
    clinical_status: str = "Nominal"
    clinical_alert_active: bool = False
    clinical_action: str = "MONITOR"
    dsm5_diagnosis: str = "UNKNOWN"
    diagnostic_cluster: str = "UNKNOWN"
    decoder_confidence: float = 1.0
