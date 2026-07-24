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
Synthetic Biopotential Signal Generators for ECG, EMG, Motor Imagery EEG, and SSVEP.
"""

from typing import Dict, Any, List, Optional
import numpy as np


class ECGDataGenerator:
    """
    Generates synthetic Electrocardiogram (ECG) telemetry streams with 
    P-Q-R-S-T wave morphology, heart rate variability (HRV), and arrhythmia pulse anomalies.
    """

    def __init__(self, seed: int = 42, sample_rate: float = 250.0, base_bpm: float = 60.0):
        self.seed = seed
        self.sample_rate = sample_rate
        self.base_bpm = base_bpm
        self._rng = np.random.default_rng(seed)

    def generate_ecg_stream(
        self,
        duration_sec: float = 10.0,
        hrv_std_bpm: float = 3.0,
        noise_level: float = 0.05,
        arrhythmia_rate: float = 0.0,
    ) -> Dict[str, Any]:
        """Generates 12-lead or 1-lead synthetic ECG signals."""
        num_samples = int(duration_sec * self.sample_rate)
        t = np.linspace(0, duration_sec, num_samples, endpoint=False)
        ecg_signal = np.zeros(num_samples, dtype=np.float32)

        # Generate heartbeat timing points with HRV
        current_time = 0.0
        beat_times = []
        while current_time < duration_sec:
            bpm = self.base_bpm + self._rng.normal(0, hrv_std_bpm)
            bpm = max(40.0, min(180.0, bpm))
            rr_interval = 60.0 / bpm
            beat_times.append(current_time)
            current_time += rr_interval

        # Synthesize P-Q-R-S-T wave for each beat
        for beat_t in beat_times:
            is_ectopic = (arrhythmia_rate > 0.0) and (self._rng.uniform() < arrhythmia_rate)
            amplitude_mult = 1.8 if is_ectopic else 1.0

            # P wave: Gaussian at -0.18s
            p_wave = 0.15 * np.exp(-0.5 * ((t - (beat_t + 0.1)) / 0.02) ** 2)
            # Q wave: Negative dip at -0.05s
            q_wave = -0.15 * np.exp(-0.5 * ((t - (beat_t + 0.18)) / 0.008) ** 2)
            # R wave: Sharp positive peak at 0.0s
            r_wave = 1.2 * amplitude_mult * np.exp(-0.5 * ((t - (beat_t + 0.20)) / 0.01) ** 2)
            # S wave: Negative dip at +0.04s
            s_wave = -0.25 * np.exp(-0.5 * ((t - (beat_t + 0.22)) / 0.012) ** 2)
            # T wave: Broad positive curve at +0.25s
            t_wave = 0.3 * np.exp(-0.5 * ((t - (beat_t + 0.38)) / 0.04) ** 2)

            ecg_signal += p_wave + q_wave + r_wave + s_wave + t_wave

        if noise_level > 0.0:
            ecg_signal += self._rng.normal(0.0, noise_level, size=num_samples).astype(np.float32)

        return {
            "num_samples": num_samples,
            "sample_rate": self.sample_rate,
            "data": ecg_signal.reshape(-1, 1),
            "beat_count": len(beat_times),
            "base_bpm": self.base_bpm,
        }


class EMGDataGenerator:
    """
    Generates synthetic Electromyogram (EMG) muscle activation signals with 
    burst contractions and fatigue spectrum shifts.
    """

    def __init__(self, seed: int = 42, num_channels: int = 4, sample_rate: float = 1000.0):
        self.seed = seed
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self._rng = np.random.default_rng(seed)

    def generate_emg_bursts(
        self,
        duration_sec: float = 5.0,
        burst_interval_sec: float = 1.5,
        burst_duration_sec: float = 0.5,
        contraction_intensity: float = 1.0,
    ) -> Dict[str, Any]:
        """Generates burst muscle contractions with Gaussian envelope."""
        num_samples = int(duration_sec * self.sample_rate)
        t = np.linspace(0, duration_sec, num_samples, endpoint=False)
        emg = self._rng.normal(0.0, 0.05, size=(num_samples, self.num_channels)).astype(np.float32)

        # Envelope construction for periodic bursts
        envelope = np.zeros(num_samples, dtype=np.float32)
        burst_times = np.arange(0.5, duration_sec, burst_interval_sec)
        for b_t in burst_times:
            envelope += contraction_intensity * np.exp(-0.5 * ((t - b_t) / (burst_duration_sec / 3.0)) ** 2)

        # High frequency raw EMG modulated by contraction envelope
        carrier_freqs = [50.0, 80.0, 120.0, 150.0]
        for ch in range(self.num_channels):
            fc = carrier_freqs[ch % len(carrier_freqs)]
            raw_carrier = np.sin(2 * np.pi * fc * t) + self._rng.normal(0.0, 0.5, size=num_samples)
            emg[:, ch] += (raw_carrier * envelope).astype(np.float32)

        return {
            "num_samples": num_samples,
            "num_channels": self.num_channels,
            "sample_rate": self.sample_rate,
            "data": emg,
            "burst_count": len(burst_times),
        }


class MotorImageryEEGGenerator:
    """
    Generates synthetic Motor Imagery EEG signals exhibiting Event-Related Desynchronization (ERD)
    in Mu (8-12 Hz) and Beta (13-30 Hz) bands during imagined limb movements.
    """

    CLASSES = ["left_hand", "right_hand", "feet", "tongue"]

    def __init__(self, seed: int = 42, num_channels: int = 8, sample_rate: float = 250.0):
        self.seed = seed
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self._rng = np.random.default_rng(seed)

    def generate_trial(
        self,
        target_class: str = "left_hand",
        trial_duration_sec: float = 4.0,
        cue_time_sec: float = 1.0,
    ) -> Dict[str, Any]:
        if target_class not in self.CLASSES:
            raise ValueError(f"Invalid class {target_class}. Must be one of {self.CLASSES}")

        num_samples = int(trial_duration_sec * self.sample_rate)
        t = np.linspace(0, trial_duration_sec, num_samples, endpoint=False)
        data = np.zeros((num_samples, self.num_channels), dtype=np.float32)

        # Baseline Mu (10Hz) and Beta (20Hz) rhythms
        baseline_mu = np.sin(2 * np.pi * 10.0 * t) * 20.0
        baseline_beta = np.sin(2 * np.pi * 20.0 * t) * 10.0

        cue_mask = (t >= cue_time_sec) & (t <= cue_time_sec + 2.5)

        for ch in range(self.num_channels):
            channel_data = baseline_mu + baseline_beta
            # ERD suppression on contralateral channels during hand motor imagery
            if target_class == "left_hand" and ch in [3, 4]:  # C4 right motor cortex
                channel_data[cue_mask] *= 0.3
            elif target_class == "right_hand" and ch in [1, 2]:  # C3 left motor cortex
                channel_data[cue_mask] *= 0.3
            elif target_class == "feet" and ch in [0, 7]:  # Cz central motor cortex
                channel_data[cue_mask] *= 0.2

            data[:, ch] = channel_data

        # Add background EEG noise
        data += self._rng.normal(0.0, 3.0, size=data.shape).astype(np.float32)

        return {
            "num_samples": num_samples,
            "num_channels": self.num_channels,
            "sample_rate": self.sample_rate,
            "target_class": target_class,
            "cue_time_sec": cue_time_sec,
            "data": data,
        }


class SSVEPDataGenerator:
    """
    Generates Steady-State Visual Evoked Potential (SSVEP) signals with target flickering
    frequencies and fundamental/harmonic frequency components in occipital channels.
    """

    def __init__(self, seed: int = 42, num_channels: int = 8, sample_rate: float = 250.0):
        self.seed = seed
        self.num_channels = num_channels
        self.sample_rate = sample_rate
        self._rng = np.random.default_rng(seed)

    def generate_ssvep_trial(
        self,
        flicker_freq_hz: float = 12.0,
        duration_sec: float = 3.0,
        occipital_channels: Optional[List[int]] = None,
    ) -> Dict[str, Any]:
        """Generates SSVEP target trial with fundamental and harmonic responses."""
        if occipital_channels is None:
            occipital_channels = [5, 6, 7]  # O1, Oz, O2

        num_samples = int(duration_sec * self.sample_rate)
        t = np.linspace(0, duration_sec, num_samples, endpoint=False)
        data = self._rng.normal(0.0, 5.0, size=(num_samples, self.num_channels)).astype(np.float32)

        # Inject fundamental + 2nd harmonic into occipital channels
        f0 = flicker_freq_hz
        ssvep_wave = 15.0 * np.sin(2 * np.pi * f0 * t) + 7.0 * np.sin(2 * np.pi * (2 * f0) * t)

        for ch in occipital_channels:
            if 0 <= ch < self.num_channels:
                data[:, ch] += ssvep_wave.astype(np.float32)

        return {
            "num_samples": num_samples,
            "num_channels": self.num_channels,
            "sample_rate": self.sample_rate,
            "flicker_freq_hz": flicker_freq_hz,
            "occipital_channels": occipital_channels,
            "data": data,
        }
