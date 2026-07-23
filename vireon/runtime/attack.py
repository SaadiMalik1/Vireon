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
VIREON Signal Attack Engine and Base Attack Modifiers.
Provides threat injection capabilities for neurosecurity laboratory simulations.
"""

from abc import ABC, abstractmethod
import threading
import numpy as np
from typing import List, Optional, Dict, Any

class ISignalModifier(ABC):
    """Abstract interface for signal attack modifiers."""
    
    @abstractmethod
    def apply(
        self,
        data: np.ndarray,
        eeg_channels: List[int],
        sample_rate: int,
        twin: Any,
        rng: Optional[np.random.Generator] = None
    ) -> np.ndarray:
        """Applies signal modification to input EEG data block."""
        pass

class NoiseInjectionAttack(ISignalModifier):
    """Injects additive Gaussian noise across target EEG channels."""
    def __init__(self, std_dev: float = 25.0):
        self.std_dev = std_dev

    def apply(
        self,
        data: np.ndarray,
        eeg_channels: List[int],
        sample_rate: int,
        twin: Any,
        rng: Optional[np.random.Generator] = None
    ) -> np.ndarray:
        generator = rng if rng is not None else np.random.default_rng()
        modified = data.copy()
        for ch in eeg_channels:
            if ch < modified.shape[0]:
                noise = generator.normal(0, self.std_dev, size=modified.shape[1])
                modified[ch, :] += noise
        return modified

class SignalDriftAttack(ISignalModifier):
    """Injects linear DC offset drift into target channels."""
    def __init__(self, drift_rate: float = 5.0):
        self.drift_rate = drift_rate

    def apply(
        self,
        data: np.ndarray,
        eeg_channels: List[int],
        sample_rate: int,
        twin: Any,
        rng: Optional[np.random.Generator] = None
    ) -> np.ndarray:
        modified = data.copy()
        num_samples = modified.shape[1]
        drift = np.linspace(0, self.drift_rate, num_samples)
        for ch in eeg_channels:
            if ch < modified.shape[0]:
                modified[ch, :] += drift
        return modified

class ImpedanceSpikeAttack(ISignalModifier):
    """Simulates electrode impedance spikes or disconnections."""
    def __init__(self, spike_amplitude: float = 150.0):
        self.spike_amplitude = spike_amplitude

    def apply(
        self,
        data: np.ndarray,
        eeg_channels: List[int],
        sample_rate: int,
        twin: Any,
        rng: Optional[np.random.Generator] = None
    ) -> np.ndarray:
        generator = rng if rng is not None else np.random.default_rng()
        modified = data.copy()
        for ch in eeg_channels:
            if ch < modified.shape[0]:
                spike = generator.normal(self.spike_amplitude, 20.0, size=modified.shape[1])
                modified[ch, :] += spike
        return modified

class SignalSuppressionAttack(ISignalModifier):
    """Suppresses neural telemetry signals on target channels to zero amplitude."""
    def __init__(self, damping_factor: float = 0.0):
        self.damping_factor = damping_factor

    def apply(
        self,
        data: np.ndarray,
        eeg_channels: List[int],
        sample_rate: int,
        twin: Any,
        rng: Optional[np.random.Generator] = None
    ) -> np.ndarray:
        modified = data.copy()
        for ch in eeg_channels:
            if ch < modified.shape[0]:
                modified[ch, :] *= self.damping_factor
        return modified

class TemporalEvasionAttack(ISignalModifier):
    """Injects intermittent pulsed noise bursts designed to evade continuous threshold detection."""
    def __init__(self, burst_amplitude: float = 40.0, duty_cycle: float = 0.3):
        self.burst_amplitude = burst_amplitude
        self.duty_cycle = duty_cycle

    def apply(
        self,
        data: np.ndarray,
        eeg_channels: List[int],
        sample_rate: int,
        twin: Any,
        rng: Optional[np.random.Generator] = None
    ) -> np.ndarray:
        generator = rng if rng is not None else np.random.default_rng()
        modified = data.copy()
        num_samples = modified.shape[1]
        mask = generator.uniform(0, 1, size=num_samples) < self.duty_cycle
        for ch in eeg_channels:
            if ch < modified.shape[0]:
                burst = generator.normal(0, self.burst_amplitude, size=num_samples) * mask
                modified[ch, :] += burst
        return modified

class SignalAttackEngine:
    """
    Orchestrates physical signal threat vectors and applies attack modifiers during simulation.
    """
    def __init__(self, twin: Any, event_bus: Optional[Any] = None):
        self.twin = twin
        self.event_bus = event_bus
        self.lock = threading.Lock()
        self.active_attacks: Dict[str, ISignalModifier] = {}

    def register_attack(self, name: str, attack: ISignalModifier):
        """Registers a named attack vector."""
        with self.lock:
            self.active_attacks[name] = attack

    def remove_attack(self, name: str):
        """Removes a registered attack vector."""
        with self.lock:
            self.active_attacks.pop(name, None)

    def apply_attacks(
        self,
        data: np.ndarray,
        eeg_channels: List[int],
        sample_rate: int,
        rng: Optional[np.random.Generator] = None
    ) -> np.ndarray:
        """Applies all currently active registered attacks to the telemetry chunk."""
        with self.lock:
            modified = data.copy()
            for name, attack in self.active_attacks.items():
                modified = attack.apply(modified, eeg_channels, sample_rate, self.twin, rng)
            return modified
