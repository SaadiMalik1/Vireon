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
Snapshot / Restore helpers extracted from DigitalTwin.

These pure functions operate on dictionaries to serialize
and deserialize twin state for experiment reproducibility.
"""

from typing import Dict, Any
from collections import deque


# --- Field lists for snapshot / restore ---

_SCALAR_FIELDS = [
    "device_id", "connected", "battery_level", "firmware_version",
    "sample_rate", "num_channels", "stimulation_enabled",
    "stimulation_amplitude_ma", "stimulation_frequency_hz",
    "decoder_confidence", "clinical_alert_active", "clinical_status",
    "hazard_state", "iso_severity", "tissue_damage_risk",
    "clinical_action", "dsm5_diagnosis", "diagnostic_cluster", "niss_score",
    "temperature_celsius", "flash_utilization_pct", "memory_usage_pct",
    "ble_pairing_state", "fallback_mode_enabled", "fallback_mode_active",
]

_SCALAR_DEFAULTS = {
    "amplifier_gain": 24,
    "communication_sessions": 0,
    "funnel_origin": "Ring 4: Cortical",
    "autonomic_pupil_dilation_mm": 4.0,
}


def create_snapshot(twin: Any, include_history: bool = False) -> Dict[str, Any]:
    """Return a complete frozen state copy suitable for serialization.

    Must be called while the twin's lock is held.
    """
    snap: Dict[str, Any] = {}
    for field in _SCALAR_FIELDS:
        snap[field] = getattr(twin, field)

    snap["electrode_impedances"] = dict(twin.electrode_impedances)

    for field, default in _SCALAR_DEFAULTS.items():
        snap[field] = getattr(twin, field, default)

    snap["sim_clock"] = twin._sim_clock
    snap["neural_dynamics"] = (
        twin.neural_dynamics.get_state()
        if hasattr(twin.neural_dynamics, "get_state")
        else None
    )
    snap["neural_coherence"] = twin.neural_dynamics.coherence
    snap["beta_power"] = twin.neural_dynamics.beta_power

    if include_history:
        snap["history"] = list(twin.history)

    return snap


def apply_snapshot(twin: Any, snap: Dict[str, Any]) -> None:
    """Restore state from a snapshot.

    Must be called while the twin's lock is held.
    """
    for field in _SCALAR_FIELDS:
        if field in snap:
            setattr(twin, field, snap[field])

    if "electrode_impedances" in snap:
        twin.electrode_impedances = snap["electrode_impedances"]

    for field, default in _SCALAR_DEFAULTS.items():
        setattr(twin, field, snap.get(field, default))

    if "neural_dynamics" in snap and snap["neural_dynamics"] is not None:
        if hasattr(twin.neural_dynamics, "restore_state"):
            twin.neural_dynamics.restore_state(snap["neural_dynamics"])

    if "history" in snap:
        twin.history = deque(snap["history"], maxlen=1000)

    twin._sim_clock = snap.get("sim_clock", twin._sim_clock)


def build_state_dict(twin: Any) -> Dict[str, Any]:
    """Build the telemetry state dict (called from get_state).

    Must be called while the twin's lock is held.
    """
    return {
        "device_id": twin.device_id,
        "connected": twin.connected,
        "battery_level": round(twin.battery_level, 2),
        "firmware_version": twin.firmware_version,
        "sample_rate": twin.sample_rate,
        "num_channels": twin.num_channels,
        "electrode_impedances": {str(k): round(v, 2) for k, v in twin.electrode_impedances.items()},
        "stimulation_enabled": twin.stimulation_enabled,
        "stimulation_amplitude_ma": round(twin.stimulation_amplitude_ma, 2),
        "stimulation_frequency_hz": round(twin.stimulation_frequency_hz, 2),
        "decoder_confidence": round(twin.decoder_confidence, 2),
        "clinical_alert_active": twin.clinical_alert_active,
        "clinical_status": twin.clinical_status,
        "hazard_state": twin.hazard_state,
        "iso_severity": twin.iso_severity,
        "tissue_damage_risk": twin.tissue_damage_risk,
        "clinical_action": twin.clinical_action,
        "dsm5_diagnosis": twin.dsm5_diagnosis,
        "diagnostic_cluster": twin.diagnostic_cluster,
        "niss_score": twin.niss_score,
        # Extended state
        "temperature_celsius": round(twin.temperature_celsius, 1),
        "flash_utilization_pct": round(twin.flash_utilization_pct, 1),
        "memory_usage_pct": round(twin.memory_usage_pct, 1),
        "ble_pairing_state": twin.ble_pairing_state,
        "amplifier_gain": twin.amplifier_gain,
        "communication_sessions": twin.communication_sessions,
        "funnel_origin": twin.funnel_origin,
        "autonomic_pupil_dilation_mm": round(twin.autonomic_pupil_dilation_mm, 2),
        "sim_clock": round(twin._sim_clock, 3),
        "neural_coherence": round(twin.neural_dynamics.coherence, 3),
        "beta_power": round(twin.neural_dynamics.beta_power, 2),
    }


# Make Any available without requiring callers to import typing
from typing import Any
