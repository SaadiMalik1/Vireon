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

from typing import Any
def format_telemetry_table(twin: Any) -> str:
    """Formats the current digital twin state as an ASCII table."""
    state = twin.get_state() if hasattr(twin, "get_state") else {}
    
    lines = []
    lines.append("=" * 60)
    lines.append(f" VIREON TELEMETRY - {state.get('device_id', 'VIRTUAL_DEVICE').upper()}")
    lines.append("=" * 60)
    lines.append(f" Connection Status : {'CONNECTED' if state.get('connected', True) else 'DISCONNECTED':<12} | Battery Level : {state.get('battery_level', 100.0)}%")
    lines.append(f" Firmware Version  : {state.get('firmware_version', 'v1.1.0'):<12} | Sample Rate   : {state.get('sample_rate', 250)} Hz")
    lines.append("-" * 60)
    
    # Electrode Impedances
    imp_strs = []
    impedances = state.get('electrode_impedances', {})
    for ch, val in sorted(impedances.items(), key=lambda x: int(x[0])):
        imp_strs.append(f"Ch{ch}: {val}kΩ")
    
    # Group impedances into 4 per line
    for i in range(0, len(imp_strs), 4):
        lines.append(" " + " | ".join(imp_strs[i:i+4]))
        
    lines.append("-" * 60)
    lines.append(f" Clinical Status   : {state.get('clinical_status', 'Nominal'):<12} | Alert Active  : {str(state.get('clinical_alert_active', False)).upper()}")
    lines.append(f" Dec. Confidence   : {state.get('decoder_confidence', 0.98):.2f}         | Therapy State : {'ACTIVE' if state.get('stimulation_enabled', False) else 'SUSPENDED'}")
    if state['stimulation_enabled']:
        lines.append(f" Stimulation Params: {state['stimulation_amplitude_ma']} mA @ {state['stimulation_frequency_hz']} Hz")
    lines.append("-" * 60)
    lines.append(f" Hazard State (ISO): {state.get('hazard_state', 'NOMINAL'):<12} | Severity      : {state.get('iso_severity', 'NEGLIGIBLE')}")
    lines.append(f" Tissue Damage Risk: {state.get('tissue_damage_risk', 'NONE'):<12} | Risk Action   : {state.get('clinical_action', 'MONITOR')}")
    lines.append("=" * 60)
    
    return "\n".join(lines)
