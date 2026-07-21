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

from dataclasses import dataclass, field
from enum import Enum
import threading
from typing import Dict, Any, List, Optional
from collections import deque
from vireon.sdk.base_interfaces import ITwin
import logging

logger = logging.getLogger(__name__)


class ClockMode(str, Enum):
    VIRTUAL = "VIRTUAL"
    WALL = "WALL"


@dataclass
class SignalState:
    sample_rate: int = 250
    num_channels: int = 8
    channel_names: List[str] = field(default_factory=lambda: [f"CH{i+1}" for i in range(8)])
    current_index: int = 0
    adc_vref: float = 4.5
    adc_gain: float = 24.0
    adc_resolution_bits: int = 24
    amplifier_saturated: bool = False


@dataclass
class PhysicsState:
    stimulation_enabled: bool = False
    stimulation_amplitude_ma: float = 0.0
    stimulation_frequency_hz: float = 0.0
    electrode_impedances: Dict[int, float] = field(default_factory=lambda: {i: 5.0 for i in range(8)})
    tissue_contact_resistance: float = 5.0


@dataclass
class BatteryState:
    battery_level: float = 100.0
    charge_mah: float = 500.0
    capacity_mah: float = 500.0
    temperature_celsius: float = 37.0
    discharge_rate: float = 1.0


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


@dataclass
class SimClock:
    mode: ClockMode = ClockMode.VIRTUAL
    tick: int = 0
    sim_time: float = 0.0
    virtual_dt_ms: float = 4.0


class PhysicsEngine:
    def tick(self, twin: "DigitalTwin", dt: float) -> None:
        if twin.stimulation_enabled and twin.stimulation_amplitude_ma > 3.0:
            twin.clinical.tissue_damage_risk = "HIGH"
            twin.clinical.clinical_alert_active = True
            if twin.hardware_mode:
                twin.clinical.hazard_state = "HARDWARE_SHUTDOWN"
                twin.physics.stimulation_enabled = False
                twin.physics.stimulation_amplitude_ma = 0.0
                twin.clinical.clinical_status = "Hardware Failsafe: Thermal shutdown"
            else:
                twin.clinical.clinical_status = "Physics Violation: Thermal threshold exceeded"


class DigitalTwin(ITwin):
    """
    Decomposed DigitalTwin composition class (Rule 27).
    Composes SignalState, PhysicsState, BatteryState, ClinicalState, and SimClock.
    """

    def __init__(
        self,
        device_id: str = "virtual_openbci_board",
        sample_rate: int = 250,
        num_channels: int = 8,
        hardware_mode: bool = False,
        seed: Optional[int] = None,
    ):
        self._lock = threading.RLock()
        self.device_id = device_id
        self.connected = True
        self.firmware_version = "1.0.0-shield"
        self.hardware_mode = hardware_mode
        self.physics_engine = PhysicsEngine()


        # Decomposed Components
        self.signal = SignalState(
            sample_rate=sample_rate,
            num_channels=num_channels,
            channel_names=[f"CH{i+1}" for i in range(num_channels)],
        )
        self.physics = PhysicsState(
            electrode_impedances={i: 5.0 for i in range(num_channels)}
        )
        self.battery = BatteryState()
        self.clinical = ClinicalState()
        self.clock = SimClock(virtual_dt_ms=1000.0 / sample_rate)

        # Active modes
        self.dbs_mode = False
        self.secure_mode = False
        self.nsp_mode = False
        self.e2ee_mode = False
        self.active_attack = "none"

        self.history: deque = deque(maxlen=1000)
        self._log_state_change("Initialization")

    @property
    def sample_rate(self) -> int:
        return self.signal.sample_rate

    @sample_rate.setter
    def sample_rate(self, val: int):
        self.signal.sample_rate = val

    @property
    def num_channels(self) -> int:
        return self.signal.num_channels

    @num_channels.setter
    def num_channels(self, val: int):
        self.signal.num_channels = val

    @property
    def battery_level(self) -> float:
        return self.battery.battery_level

    @battery_level.setter
    def battery_level(self, val: float):
        self.battery.battery_level = val

    @property
    def stimulation_enabled(self) -> bool:
        return self.physics.stimulation_enabled

    @stimulation_enabled.setter
    def stimulation_enabled(self, val: bool):
        self.physics.stimulation_enabled = val

    @property
    def stimulation_amplitude_ma(self) -> float:
        return self.physics.stimulation_amplitude_ma

    @stimulation_amplitude_ma.setter
    def stimulation_amplitude_ma(self, val: float):
        self.physics.stimulation_amplitude_ma = val

    @property
    def stimulation_frequency_hz(self) -> float:
        return self.physics.stimulation_frequency_hz

    @stimulation_frequency_hz.setter
    def stimulation_frequency_hz(self, val: float):
        self.physics.stimulation_frequency_hz = val

    @property
    def electrode_impedances(self) -> Dict[int, float]:
        return self.physics.electrode_impedances

    @property
    def clinical_status(self) -> str:
        return self.clinical.clinical_status

    @clinical_status.setter
    def clinical_status(self, val: str):
        self.clinical.clinical_status = val

    @property
    def hazard_state(self) -> str:
        return self.clinical.hazard_state

    @hazard_state.setter
    def hazard_state(self, val: str):
        self.clinical.hazard_state = val

    @property
    def iso_severity(self) -> str:
        return self.clinical.iso_severity

    @iso_severity.setter
    def iso_severity(self, val: str):
        self.clinical.iso_severity = val

    @property
    def tissue_damage_risk(self) -> str:
        return self.clinical.tissue_damage_risk

    @tissue_damage_risk.setter
    def tissue_damage_risk(self, val: str):
        self.clinical.tissue_damage_risk = val

    @property
    def clinical_alert_active(self) -> bool:
        return self.clinical.clinical_alert_active

    @clinical_alert_active.setter
    def clinical_alert_active(self, val: bool):
        self.clinical.clinical_alert_active = val


    def set_sim_clock(self, t: float):
        with self._lock:
            dt = t - self.clock.sim_time
            self.clock.sim_time = t
            self.clock.tick += 1
            if dt > 0:
                self.battery.battery_level = max(0.0, self.battery.battery_level - 0.001 * dt)

    def get_sim_clock(self) -> float:
        return self.clock.sim_time

    def get_state(self) -> Dict[str, Any]:
        with self._lock:
            state = {
                "device_id": self.device_id,
                "connected": self.connected,
                "sim_clock": self.clock.sim_time,
                "tick": self.clock.tick,
                "battery_level": self.battery.battery_level,
                "stimulation_enabled": self.physics.stimulation_enabled,
                "stimulation_amplitude_ma": self.physics.stimulation_amplitude_ma,
                "stimulation_frequency_hz": self.physics.stimulation_frequency_hz,
                "electrode_impedances": self.physics.electrode_impedances,
                "clinical_status": self.clinical.clinical_status,
                "hazard_state": self.clinical.hazard_state,
                "iso_severity": self.clinical.iso_severity,
                "tissue_damage_risk": self.clinical.tissue_damage_risk,
                "clinical_alert_active": self.clinical.clinical_alert_active,
                "decoder_confidence": self.clinical.decoder_confidence,

                "signal": self.signal.__dict__,
                "physics": self.physics.__dict__,
                "battery": self.battery.__dict__,
                "clinical": self.clinical.__dict__,
            }
            return state

    def set_clinical_alert(self, active: bool, message: str):
        with self._lock:
            self.clinical.clinical_alert_active = active
            self.clinical.clinical_status = message

    def set_connection(self, status: bool):
        with self._lock:
            self.connected = status

    def update_therapy(self, enabled: bool):
        with self._lock:
            self.physics.stimulation_enabled = enabled

    def update_impedance(self, ch: int, val: float):
        with self._lock:
            self.physics.electrode_impedances[ch] = val

    def update_stimulation_params(self, amplitude: float = 0.0, frequency: float = 0.0):
        with self._lock:
            self.physics.stimulation_amplitude_ma = amplitude
            self.physics.stimulation_frequency_hz = frequency

    def update_clinical_risk(
        self,
        hazard_state: str = "NOMINAL",
        iso_severity: str = "NEGLIGIBLE",
        tissue_damage_risk: str = "NONE",
        clinical_action: str = "MONITOR",
        dsm5_diagnosis: str = "UNKNOWN",
        diagnostic_cluster: str = "UNKNOWN",
        niss_score: float = 0.0,
    ):
        with self._lock:
            self.clinical.hazard_state = hazard_state
            self.clinical.iso_severity = iso_severity
            self.clinical.tissue_damage_risk = tissue_damage_risk
            self.clinical.clinical_action = clinical_action
            self.clinical.dsm5_diagnosis = dsm5_diagnosis
            self.clinical.diagnostic_cluster = diagnostic_cluster
            self.clinical.niss_score = niss_score

    def update_decoder_confidence(self, conf: float):
        with self._lock:
            self.clinical.decoder_confidence = max(0.0, min(1.0, float(conf)))



    def get(self, key: str, default: Any = None) -> Any:
        return getattr(self, key, default)


    def set(self, key: str, value: Any, source: str = "system") -> None:
        setattr(self, key, value)

    def get_all(self) -> Dict[str, Any]:
        return self.get_state()

    def _log_state_change(self, event: str):
        state_copy = {
            "timestamp": self.clock.sim_time,
            "event": event,
            "connected": self.connected,
            "battery_level": self.battery.battery_level,
            "stimulation_enabled": self.physics.stimulation_enabled,
            "clinical_status": self.clinical.clinical_status,
            "hazard_state": self.clinical.hazard_state,
        }
        self.history.append(state_copy)

    def get_history(self) -> List[Dict[str, Any]]:
        with self._lock:
            return list(self.history)

    def snapshot(self, include_history: bool = False) -> Dict[str, Any]:
        with self._lock:
            snap = {
                "device_id": self.device_id,
                "connected": self.connected,
                "sim_clock": self.clock.sim_time,
                "signal": self.signal.__dict__.copy(),
                "physics": self.physics.__dict__.copy(),
                "battery": self.battery.__dict__.copy(),
                "clinical": self.clinical.__dict__.copy(),
            }
            if include_history:
                snap["history"] = list(self.history)
            return snap

    def restore(self, snap: Dict[str, Any]) -> None:
        with self._lock:
            if "sim_clock" in snap:
                self.clock.sim_time = snap["sim_clock"]
            if "device_id" in snap:
                self.device_id = snap["device_id"]
            if "connected" in snap:
                self.connected = snap["connected"]
            if "signal" in snap:
                self.signal.__dict__.update(snap["signal"])
            if "physics" in snap:
                self.physics.__dict__.update(snap["physics"])
            if "battery" in snap:
                self.battery.__dict__.update(snap["battery"])
            if "clinical" in snap:
                self.clinical.__dict__.update(snap["clinical"])

