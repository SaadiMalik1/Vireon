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
Exhaustive Phase 5 Multi-Channel Physiological Dataset & Artifact Generator.
"""

from typing import Dict, Any, List, Optional
import numpy as np


class SyntheticDataGenerator:
    """
    Generates reproducible multi-band physiological telemetry streams with 
    configurable noise, powerline hum, P300 ERP spikes, packet loss, and channel dropouts.
    """

    def __init__(self, seed: int = 42, num_channels: int = 8, sample_rate: float = 250.0):
        self.seed = seed
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self._rng = np.random.default_rng(seed)

    def generate_eeg_stream(
        self,
        duration_sec: float = 1.0,
        noise_level: float = 0.1,
        include_p300: bool = False,
        powerline_hum_freq: Optional[float] = 60.0,
        packet_loss_rate: float = 0.0,
        dropout_channels: Optional[List[int]] = None
    ) -> Dict[str, Any]:
        """Generates multi-frequency EEG (Delta, Theta, Alpha, Beta, Gamma) signals."""
        num_samples = int(duration_sec * self.sample_rate)
        t = np.linspace(0, duration_sec, num_samples, endpoint=False)

        data = np.zeros((num_samples, self.num_channels), dtype=np.float32)

        for ch in range(self.num_channels):
            # Delta (2Hz), Alpha (10Hz), Beta (20Hz), Gamma (40Hz) composition
            delta = np.sin(2 * np.pi * 2.0 * t) * 15.0
            alpha = np.sin(2 * np.pi * (10.0 + ch * 0.2) * t) * 25.0
            beta = np.sin(2 * np.pi * 20.0 * t) * 5.0
            gamma = np.sin(2 * np.pi * 40.0 * t) * 2.0
            
            data[:, ch] = delta + alpha + beta + gamma

            # Optional 50Hz / 60Hz powerline noise
            if powerline_hum_freq:
                data[:, ch] += np.sin(2 * np.pi * powerline_hum_freq * t) * 8.0

        # Inject P300 Event-Related Potential spike at t=300ms if requested
        if include_p300:
            p300_idx = int(0.3 * self.sample_rate)
            if p300_idx < num_samples:
                # Gaussian pulse (300ms latency, 50ms width, +40uV peak)
                pulse = 40.0 * np.exp(-0.5 * ((t - 0.3) / 0.05) ** 2)
                for ch in range(self.num_channels):
                    data[:, ch] += pulse

        # Add Gaussian white noise
        if noise_level > 0.0:
            data += self._rng.normal(0.0, noise_level * 10.0, size=data.shape).astype(np.float32)

        # Apply electrode channel dropouts
        if dropout_channels:
            for ch in dropout_channels:
                if 0 <= ch < self.num_channels:
                    data[:, ch] = 0.0

        # Apply random BLE packet loss frames
        if packet_loss_rate > 0.0:
            loss_mask = self._rng.uniform(0.0, 1.0, size=num_samples) < packet_loss_rate
            data[loss_mask, :] = 0.0

        return {
            "num_samples": num_samples,
            "num_channels": self.num_channels,
            "sample_rate": self.sample_rate,
            "data": data,
            "seed": self.seed,
            "p300_included": include_p300
        }
