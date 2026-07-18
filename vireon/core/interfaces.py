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

import abc
from typing import Any, List
import numpy as np

class ITwin(abc.ABC):
    """
    Interface for the Digital Twin.
    Represents the simulated state and physics of the target neurodevice.
    """
    sample_rate: int
    num_channels: int
    physics_engine: Any
    neural_dynamics: Any
    stimulation_amplitude_ma: float
    stimulation_frequency_hz: float
    hazard_state: str
    connected: bool

    @abc.abstractmethod
    def get_sim_clock(self) -> float:
        """Get the current monotonic simulation time."""
        pass
        
    @abc.abstractmethod
    def snapshot(self) -> dict:
        """Create a complete frozen state snapshot suitable for serialization."""
        pass
        
    @abc.abstractmethod
    def restore(self, snap: dict):
        """Restore the twin state from a serialized snapshot."""
        pass

    @abc.abstractmethod
    def set_sim_clock(self, clock: float):
        """Update the simulation clock time."""
        pass


class IDetector(abc.ABC):
    """
    Interface for intrusion detection and signal analysis algorithms.
    """
    @abc.abstractmethod
    def score_signal(self, data: np.ndarray) -> float:
        """Score the anomaly level of a signal window (0.0 to 1.0)."""
        pass
        
    @abc.abstractmethod
    def analyze_signal(self, data: np.ndarray) -> List[str]:
        """Analyze a signal window and return a list of detected threat signatures."""
        pass

class ICryptoChannel(abc.ABC):
    """
    Interface for end-to-end encryption channels.
    """
    @abc.abstractmethod
    def encrypt_data(self, plaintext: bytes) -> bytes:
        """Encrypt a block of plaintext data."""
        pass
        
    @abc.abstractmethod
    def decrypt_data(self, ciphertext: bytes) -> bytes:
        """Decrypt a block of ciphertext data."""
        pass

class ITransport(abc.ABC):
    """
    Interface for network or hardware transport layers (e.g. BLE, UDP).
    """
    @abc.abstractmethod
    def send(self, data: Any):
        """Send data over the transport."""
        pass
        
    @abc.abstractmethod
    def receive(self) -> Any:
        """Receive data from the transport."""
        pass
