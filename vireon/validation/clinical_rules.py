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
Phase 8 Clinical Safety & ISO 14708-3 / ISO 14971 Rule Evaluator.
"""

from typing import Dict, Any


class ClinicalSafetyViolation(Exception):
    """Raised when a clinical safety or neurostimulation parameter exceeds ISO standards."""
    pass


class ClinicalRuleEvaluator:
    """
    Evaluates neurostimulation parameters against ISO 14708-3 (Active Implantable Medical Devices)
    and ISO 14971 risk management standards.
    """

    MAX_THERMAL_DISSIPATION_C: float = 2.0
    MAX_CHARGE_DENSITY_UC_CM2: float = 30.0
    MAX_STIMULATION_FREQ_HZ: float = 180.0
    MAX_DATA_BANDWIDTH_MBPS: float = 50.0

    def evaluate_stimulation_parameters(
        self,
        amplitude_ma: float,
        pulse_width_us: float,
        frequency_hz: float,
        electrode_area_cm2: float = 0.05
    ) -> Dict[str, Any]:
        """Evaluates stimulation waveform parameters against safety thresholds."""

        # 1. Frequency ceiling check
        if frequency_hz > self.MAX_STIMULATION_FREQ_HZ:
            raise ClinicalSafetyViolation(
                f"[ISO 14708-3] Stimulation frequency {frequency_hz}Hz exceeds ceiling of {self.MAX_STIMULATION_FREQ_HZ}Hz"
            )

        # 2. Charge density per phase calculation (Phase Charge = Current * PulseWidth)
        phase_charge_uc = amplitude_ma * (pulse_width_us / 1000.0)
        charge_density = phase_charge_uc / electrode_area_cm2

        if charge_density > self.MAX_CHARGE_DENSITY_UC_CM2:
            raise ClinicalSafetyViolation(
                f"[ISO 14708-3] Charge density {charge_density:.2f} µC/cm² exceeds tissue damage threshold {self.MAX_CHARGE_DENSITY_UC_CM2} µC/cm²"
            )

        return {
            "status": "PASS",
            "phase_charge_uc": round(phase_charge_uc, 3),
            "charge_density_uc_cm2": round(charge_density, 2),
            "frequency_hz": frequency_hz
        }

    def evaluate_tissue_heating(self, measured_temp_delta_c: float) -> bool:
        """Evaluates tissue thermal dissipation limit."""
        if measured_temp_delta_c >= self.MAX_THERMAL_DISSIPATION_C:
            raise ClinicalSafetyViolation(
                f"[ISO 14708-3] Tissue heating delta {measured_temp_delta_c:.2f}°C exceeds safe maximum of {self.MAX_THERMAL_DISSIPATION_C}°C"
            )
        return True
