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
from typing import List, Dict, Optional
from vireon.sdk.state import IStateStore

from .base import ISignalModifier

class NoiseInjectionAttack(ISignalModifier):
    def __init__(self, target_channels: List[int], noise_level_microvolts: float = 50.0):
        self.target_channels = target_channels
        self.noise_level = noise_level_microvolts

    def apply(self, data: np.ndarray, eeg_channels: List[int], sample_rate: int, state_store: IStateStore, rng: Optional[np.random.Generator] = None) -> np.ndarray:
        mutated_data = data.copy()
        for ch in self.target_channels:
            if ch in eeg_channels:
                # Add Gaussian noise
                noise = (rng if rng is not None else np.random).normal(0, self.noise_level, size=data.shape[1])
                mutated_data[ch, :] += noise
        return mutated_data


class SignalDriftAttack(ISignalModifier):
    def __init__(self, target_channels: List[int], drift_rate_uv_per_sec: float = 20.0):
        self.target_channels = target_channels
        self.drift_rate = drift_rate_uv_per_sec
        # Maintain drift offsets across calls
        self.offsets: Dict[int, float] = {ch: 0.0 for ch in target_channels}

    def apply(self, data: np.ndarray, eeg_channels: List[int], sample_rate: int, state_store: IStateStore, rng: Optional[np.random.Generator] = None) -> np.ndarray:
        mutated_data = data.copy()
        num_samples = data.shape[1]
        dt = num_samples / sample_rate

        for ch in self.target_channels:
            if ch in eeg_channels:
                start_offset = self.offsets.get(ch, 0.0)
                # Compute linear drift vector for this block
                drift_vector = np.linspace(start_offset, start_offset + self.drift_rate * dt, num_samples)
                mutated_data[ch, :] += drift_vector
                # Store final offset for the next chunk
                self.offsets[ch] = start_offset + self.drift_rate * dt
        return mutated_data


class ImpedanceSpikeAttack(ISignalModifier):
    def __init__(self, target_channels: List[int], spike_value_kohm: float = 150.0, powerline_noise_amplitude: float = 100.0):
        self.target_channels = target_channels
        self.spike_value = spike_value_kohm
        self.powerline_noise_amplitude = powerline_noise_amplitude
        self.time_counter = 0.0

    def apply(self, data: np.ndarray, eeg_channels: List[int], sample_rate: int, state_store: IStateStore, rng: Optional[np.random.Generator] = None) -> np.ndarray:
        mutated_data = data.copy()
        num_samples = data.shape[1]

        # Create a powerline interference (50 Hz sine wave)
        t = self.time_counter + np.arange(num_samples) / sample_rate
        powerline_noise = self.powerline_noise_amplitude * np.sin(2 * np.pi * 50.0 * t)
        self.time_counter += num_samples / sample_rate

        for ch in self.target_channels:
            if ch in eeg_channels:
                # Update impedance in digital twin to spike value
                if hasattr(state_store, "set"):
                    state_store.set(f"impedance_ch{ch}", self.spike_value, source="attack_engine")
                elif hasattr(state_store, "update_impedance"):
                    state_store.update_impedance(ch, self.spike_value)
                elif hasattr(state_store, "electrode_impedances"):
                    state_store.electrode_impedances[ch] = self.spike_value

                # Zero out clean signal and inject powerline noise + high random noise
                high_noise = (rng if rng is not None else np.random).normal(0, 30.0, size=num_samples)
                mutated_data[ch, :] = powerline_noise + high_noise

        return mutated_data

    def revert(self, state_store: IStateStore) -> None:
        """Revert impedance to nominal 5.0 kOhm."""
        for ch in self.target_channels:
            if hasattr(state_store, "set"):
                state_store.set(f"impedance_ch{ch}", 5.0, source="attack_engine")


class SignalSuppressionAttack(ISignalModifier):
    def __init__(self, target_channels: List[int], attenuation_factor: float = 0.05):
        self.target_channels = target_channels
        self.attenuation_factor = attenuation_factor

    def apply(self, data: np.ndarray, eeg_channels: List[int], sample_rate: int, state_store: IStateStore, rng: Optional[np.random.Generator] = None) -> np.ndarray:
        mutated_data = data.copy()
        for ch in self.target_channels:
            if ch in eeg_channels:
                # Attenuate the signal
                mutated_data[ch, :] *= self.attenuation_factor
        return mutated_data


