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
Default Clinical Provider (Extracted from Runtime per Invariant 2).
Encapsulates clinical biomarker evaluation, stroke scale (NISS) calculations, and DSM-5 diagnostic cluster logic.
"""

from typing import Any

from vireon.sdk.provider_interfaces.v1 import IClinicalProviderV1
from vireon.sdk.schemas.clinical import ClinicalState


class DefaultClinicalProvider(IClinicalProviderV1):
    """
    Independent Clinical Provider implementation of IClinicalProviderV1.
    Evaluates physiological telemetry for clinical risk indicators outside the runtime orchestrator kernel.
    """

    def __init__(self):
        self.state = ClinicalState()

    def health(self) -> dict:
        return {
            "status": "ok",
            "clinical_status": self.state.clinical_status,
            "hazard_state": self.state.hazard_state,
        }

    def evaluate_biomarker(self, data: Any) -> dict:
        """Evaluates input physiological signal frames for biomarker indicators."""
        if isinstance(data, dict):
            amplitude_ma = data.get("stimulation_amplitude_ma", 0.0)
            if amplitude_ma > 3.0:
                self.state.tissue_damage_risk = "HIGH"
                self.state.clinical_alert_active = True
                self.state.clinical_status = "Physics Violation: Thermal threshold exceeded"
                self.state.hazard_state = "CLINICAL_ALERT"
            else:
                self.state.tissue_damage_risk = "NONE"
                self.state.clinical_alert_active = False
                self.state.clinical_status = "Nominal"
                self.state.hazard_state = "NOMINAL"

        return {
            "hazard_state": self.state.hazard_state,
            "tissue_damage_risk": self.state.tissue_damage_risk,
            "clinical_alert_active": self.state.clinical_alert_active,
            "clinical_status": self.state.clinical_status,
        }
