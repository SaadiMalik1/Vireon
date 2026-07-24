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
Unit Tests for Biopotential Signal Generators (ECG, EMG, Motor Imagery, SSVEP).
"""

import pytest
import numpy as np
from vireon.datasets import (
    ECGDataGenerator,
    EMGDataGenerator,
    MotorImageryEEGGenerator,
    SSVEPDataGenerator,
)


def test_ecg_generator_reproducibility_and_shape():
    gen1 = ECGDataGenerator(seed=100, sample_rate=250.0, base_bpm=60.0)
    gen2 = ECGDataGenerator(seed=100, sample_rate=250.0, base_bpm=60.0)

    res1 = gen1.generate_ecg_stream(duration_sec=2.0)
    res2 = gen2.generate_ecg_stream(duration_sec=2.0)

    assert res1["num_samples"] == 500
    assert res1["data"].shape == (500, 1)
    assert np.array_equal(res1["data"], res2["data"])
    assert res1["beat_count"] > 0


def test_emg_generator_bursts():
    gen = EMGDataGenerator(seed=42, num_channels=4, sample_rate=1000.0)
    res = gen.generate_emg_bursts(duration_sec=3.0, burst_interval_sec=1.0)

    assert res["num_samples"] == 3000
    assert res["num_channels"] == 4
    assert res["data"].shape == (3000, 4)
    assert res["burst_count"] == 3


def test_motor_imagery_generator_classes_and_erd():
    gen = MotorImageryEEGGenerator(seed=777, num_channels=8, sample_rate=250.0)

    trial_lh = gen.generate_trial(target_class="left_hand", trial_duration_sec=4.0)
    trial_rh = gen.generate_trial(target_class="right_hand", trial_duration_sec=4.0)

    assert trial_lh["data"].shape == (1000, 8)
    assert trial_rh["data"].shape == (1000, 8)

    with pytest.raises(ValueError):
        gen.generate_trial(target_class="invalid_class")


def test_ssvep_generator_frequencies():
    gen = SSVEPDataGenerator(seed=55, num_channels=8, sample_rate=250.0)
    res = gen.generate_ssvep_trial(flicker_freq_hz=15.0, duration_sec=2.0, occipital_channels=[5, 6, 7])

    assert res["num_samples"] == 500
    assert res["flicker_freq_hz"] == 15.0
    assert res["data"].shape == (500, 8)
