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
Battery chemistry model extracted from DigitalTwin.

Implements Peukert's Law for non-linear capacity reduction and
physically consistent voltage sag modeling.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class BatteryState:
    """Snapshot of battery state for reporting."""
    level_pct: float
    effective_voltage_v: float
    brownout: bool


def tick_battery(
    battery_level: float,
    stimulation_enabled: bool,
    stimulation_amplitude_ma: float,
    stimulation_frequency_hz: float,
    dt: float,
) -> Dict[str, Any]:
    """Simulate battery discharge and voltage sag under load.

    Uses Peukert's Law for non-linear capacity reduction under high load.

    Returns a dict with keys: battery_level, brownout, effective_voltage_pct
    """
    # 1. Base current draw (mA)
    base_ma = 5.0

    # 2. Stimulation current draw (mA)
    stim_ma = 0.0
    if stimulation_enabled and stimulation_amplitude_ma > 0:
        stim_ma = stimulation_amplitude_ma * (stimulation_frequency_hz / 130.0) * 2.0

    total_ma = base_ma + stim_ma

    # Peukert's Law: Effective current = I^k (k ~ 1.2 for medical batteries)
    peukert_k = 1.2
    effective_ma = total_ma ** peukert_k

    # Calibrate so base_ma matches previous base_draw of 0.005 %/sec
    capacity_scaling = 0.005 / (base_ma ** peukert_k)

    total_draw_pct = effective_ma * capacity_scaling * dt
    new_level = max(0.0, battery_level - total_draw_pct)

    # 3. Physically consistent battery model: V = OCV(SoC) - I * R_int
    # OCV (Open Circuit Voltage) roughly 3.0V (0%) to 4.2V (100%)
    ocv_v = 3.0 + 1.2 * (new_level / 100.0)

    # Internal resistance (Ohms). Increases as SoC drops.
    r_int_ohms = 0.5 + 2.0 * (1.0 - (new_level / 100.0))

    # Voltage drop under load
    v_drop = (total_ma / 1000.0) * r_int_ohms
    effective_voltage_v = ocv_v - v_drop

    # Convert back to an "effective percentage" for the brownout logic (approx 3.15V cutoff ~ 5%)
    effective_voltage_pct = max(0.0, (effective_voltage_v - 3.15) / 1.05 * 100.0)

    return {
        "battery_level": new_level,
        "brownout": effective_voltage_pct < 5.0,
        "effective_voltage_pct": effective_voltage_pct,
    }
