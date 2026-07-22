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
Phase 5 Dataset Validation Suite for Physiological Signals & Synthetic Generators.
"""

import numpy as np
from vireon.datasets.synthetic import SyntheticDataGenerator


def test_synthetic_eeg_stream_reproducibility():
    gen1 = SyntheticDataGenerator(seed=12345, num_channels=8, sample_rate=250.0)
    gen2 = SyntheticDataGenerator(seed=12345, num_channels=8, sample_rate=250.0)

    stream1 = gen1.generate_eeg_stream(duration_sec=2.0, noise_level=0.1, include_p300=True)
    stream2 = gen2.generate_eeg_stream(duration_sec=2.0, noise_level=0.1, include_p300=True)

    assert stream1["num_samples"] == 500
    assert np.array_equal(stream1["data"], stream2["data"])


def test_p300_erp_spike_injection():
    gen = SyntheticDataGenerator(seed=42)
    stream_no_p300 = gen.generate_eeg_stream(duration_sec=1.0, include_p300=False)
    
    gen_p300 = SyntheticDataGenerator(seed=42)
    stream_p300 = gen_p300.generate_eeg_stream(duration_sec=1.0, include_p300=True)

    # Spike at t=300ms (sample index 75 for 250Hz)
    p300_idx = 75
    diff = stream_p300["data"][p300_idx, 0] - stream_no_p300["data"][p300_idx, 0]
    assert diff > 35.0  # +40uV pulse peak verified


def test_channel_dropout_and_packet_loss():
    gen = SyntheticDataGenerator(seed=99)
    stream = gen.generate_eeg_stream(duration_sec=1.0, dropout_channels=[2, 5], packet_loss_rate=0.1)

    # Verify channels 2 and 5 are completely zeroed out
    assert np.all(stream["data"][:, 2] == 0.0)
    assert np.all(stream["data"][:, 5] == 0.0)
