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

import numpy as np
from typing import List, Optional
from vireon.runtime.event_bus import EventBus, Event

from .base import ISignalModifier

class SignalAttackEngine:
    def __init__(self, state_store, event_bus: Optional[EventBus] = None):
        self.state_store = state_store
        self.event_bus = event_bus
        self.modifiers: List[ISignalModifier] = []
        import threading
        self.lock = threading.RLock()

    def add_modifier(self, modifier: ISignalModifier):
        with self.lock:
            self.modifiers.append(modifier)

        if self.event_bus:
            # Extract parameters
            params = {}
            if hasattr(modifier, "noise_level"):
                params["noise_level_uv"] = modifier.noise_level
            elif hasattr(modifier, "drift_rate"):
                params["drift_rate_uv_per_sec"] = modifier.drift_rate
            elif hasattr(modifier, "spike_value"):
                params["spike_value_kohm"] = modifier.spike_value
            elif hasattr(modifier, "attenuation_factor"):
                params["attenuation_factor"] = modifier.attenuation_factor

            sim_clock = self.state_store.get("sim_clock", 0.0) if hasattr(self.state_store, "get") else getattr(self.state_store, "sim_clock", 0.0)
            self.event_bus.publish(Event(
                topic="attack.modifier_added",
                data={
                    "type": modifier.__class__.__name__,
                    "target_channels": getattr(modifier, "target_channels", []),
                    "params": params,
                    "sim_clock": sim_clock
                },
                source="attack_engine"
            ))

    def remove_modifier(self, modifier: ISignalModifier):
        removed = False
        with self.lock:
            if modifier in self.modifiers:
                self.modifiers.remove(modifier)
                removed = True

        if removed:
            modifier.revert(self.state_store)

        if removed and self.event_bus:
            sim_clock = self.state_store.get("sim_clock", 0.0) if hasattr(self.state_store, "get") else getattr(self.state_store, "sim_clock", 0.0)
            self.event_bus.publish(Event(
                topic="attack.modifier_removed",
                data={
                    "type": modifier.__class__.__name__,
                    "sim_clock": sim_clock
                },
                source="attack_engine"
            ))

    def apply_attacks(self, data: np.ndarray, eeg_channels: List[int], sample_rate: int, rng: Optional[np.random.Generator] = None) -> np.ndarray:
        processed_data = data.copy()
        with self.lock:
            active_mods = list(self.modifiers)

        # Reset twin-level properties that might have been left over
        if hasattr(self.state_store, "set"):
            self.state_store.set("rf_packet_drop_rate", 0.0, source="attack_engine")

        for modifier in active_mods:
            processed_data = modifier.apply(processed_data, eeg_channels, sample_rate, self.state_store, rng)

        if active_mods and self.event_bus:
            sim_clock = self.state_store.get("sim_clock", 0.0) if hasattr(self.state_store, "get") else getattr(self.state_store, "sim_clock", 0.0)
            self.event_bus.publish(Event(
                topic="attack.applied",
                data={
                    "active_modifiers_count": len(active_mods),
                    "sim_clock": sim_clock
                },
                source="attack_engine"
            ))

        return processed_data

