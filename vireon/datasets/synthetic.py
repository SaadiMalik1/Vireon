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
Phase 5 Deterministic Synthetic Dataset & Artifact Generator.
"""

from typing import Dict, Any, List
import numpy as np


class SyntheticDataGenerator:
    """
    Generates reproducible synthetic physiological telemetry streams with 
    configurable noise, packet loss, electrode dropouts, and adversarial injection (Phase 5).
    """

    def __init__(self, seed: int = 42, num_channels: int = 8, sample_rate: float = 250.0):
        self.seed = seed
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self._rng = np.random.default_rng(seed)

    def generate_chunk(
        self,
        duration_sec: float = 1.0,
        noise_level: float = 0.1,
        packet_loss_rate: float = 0.0,
        dropout_channels: List[int] = None,
        jitter_ms: float = 0.0
    ) -> Dict[str, Any]:
        """Generates a synthetic telemetry chunk with deterministic artifacts."""
        num_samples = int(duration_sec * self.sample_rate)
        t = np.linspace(0, duration_sec, num_samples, endpoint=False)

        # Baseline sine + alpha band activity (10Hz)
        data = np.zeros((num_samples, self.num_channels), dtype=np.float32)
        for ch in range(self.num_channels):
            freq = 10.0 + (ch * 0.5)
            data[:, ch] = np.sin(2 * np.pi * freq * t) * 20.0

        # Add Gaussian noise
        if noise_level > 0.0:
            data += self._rng.normal(0.0, noise_level * 10.0, size=data.shape).astype(np.float32)

        # Apply electrode dropouts
        if dropout_channels:
            for ch in dropout_channels:
                if 0 <= ch < self.num_channels:
                    data[:, ch] = 0.0

        # Apply packet loss (random zeroing of sample frames)
        if packet_loss_rate > 0.0:
            loss_mask = self._rng.uniform(0.0, 1.0, size=num_samples) < packet_loss_rate
            data[loss_mask, :] = 0.0

        return {
            "num_samples": num_samples,
            "num_channels": self.num_channels,
            "sample_rate": self.sample_rate,
            "data": data,
            "seed": self.seed
        }
