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
Unit Tests for Benchmark Dataset Loaders (BCI Competition IV, PhysioNet).
"""

import pytest
import numpy as np
from vireon.datasets import BCICompetitionIVDataset, PhysioNetDatasetLoader


def test_bci_competition_iv_dataset():
    bci_ds = BCICompetitionIVDataset(subject_id=1, seed=42)
    X, y = bci_ds.load_trials(num_trials=8)

    assert X.shape == (8, 1000, 22)
    assert y.shape == (8,)
    assert set(np.unique(y)).issubset({0, 1, 2, 3})


def test_physionet_dataset_loader_eeg():
    loader = PhysioNetDatasetLoader(dataset_name="eegmmidb", seed=42)
    res = loader.fetch_subject_data(subject_id=3)

    assert res["subject_id"] == 3
    assert res["num_channels"] == 64
    assert res["sample_rate"] == 160.0
    assert res["data"].shape == (1600, 64)


def test_physionet_dataset_loader_ecg():
    loader = PhysioNetDatasetLoader(dataset_name="mitdb", seed=42)
    res = loader.fetch_subject_data(subject_id=1)

    assert res["subject_id"] == 1
    assert res["num_channels"] == 1
    assert res["sample_rate"] == 360.0
    assert res["data"].shape == (3600, 1)


def test_physionet_invalid_dataset():
    loader = PhysioNetDatasetLoader(dataset_name="unknown_db")
    with pytest.raises(ValueError):
        loader.fetch_subject_data(subject_id=1)
