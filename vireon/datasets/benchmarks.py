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
Benchmark Dataset Interfaces for Neuroscience and Physiological AI Research.
"""

from typing import Dict, Any, Tuple
import numpy as np
from vireon.datasets.biopotentials import MotorImageryEEGGenerator, ECGDataGenerator


class BCICompetitionIVDataset:
    """
    Interface and mock loader for BCI Competition IV 2a/2b Motor Imagery and P300 datasets.
    """

    def __init__(self, subject_id: int = 1, seed: int = 42):
        self.subject_id = subject_id
        self.seed = seed + subject_id
        self.sample_rate = 250.0
        self.num_channels = 22  # Standard 22 EEG channel montage for BCI Comp IV 2a

    def load_trials(self, num_trials: int = 40) -> Tuple[np.ndarray, np.ndarray]:
        """
        Loads or generates benchmark motor imagery trials.
        Returns:
            X: np.ndarray of shape (num_trials, num_samples, num_channels)
            y: np.ndarray of shape (num_trials,) with target class labels (0 to 3)
        """
        gen = MotorImageryEEGGenerator(seed=self.seed, num_channels=self.num_channels, sample_rate=self.sample_rate)
        classes = ["left_hand", "right_hand", "feet", "tongue"]

        X_list = []
        y_list = []

        for i in range(num_trials):
            target_class_idx = i % len(classes)
            target_class = classes[target_class_idx]
            trial = gen.generate_trial(target_class=target_class, trial_duration_sec=4.0)

            X_list.append(trial["data"])
            y_list.append(target_class_idx)

        X = np.array(X_list, dtype=np.float32)
        y = np.array(y_list, dtype=np.int64)

        return X, y


class PhysioNetDatasetLoader:
    """
    Interface and loader for PhysioNet EEG Motor Movement/Imagery and ECG databases.
    """

    def __init__(self, dataset_name: str = "eegmmidb", seed: int = 42):
        self.dataset_name = dataset_name
        self.seed = seed

    def fetch_subject_data(self, subject_id: int = 1) -> Dict[str, Any]:
        """
        Simulates fetching or reading subject recording data from PhysioNet.
        """
        if self.dataset_name == "eegmmidb":
            gen = MotorImageryEEGGenerator(seed=self.seed + subject_id, num_channels=64, sample_rate=160.0)
            trial = gen.generate_trial(target_class="right_hand", trial_duration_sec=10.0)
            return {
                "subject_id": subject_id,
                "dataset_name": self.dataset_name,
                "sample_rate": 160.0,
                "num_channels": 64,
                "data": trial["data"],
            }
        elif self.dataset_name == "mitdb":
            ecg_gen = ECGDataGenerator(seed=self.seed + subject_id, sample_rate=360.0, base_bpm=72.0)
            stream = ecg_gen.generate_ecg_stream(duration_sec=10.0)
            return {
                "subject_id": subject_id,
                "dataset_name": self.dataset_name,
                "sample_rate": 360.0,
                "num_channels": 1,
                "data": stream["data"],
            }
        else:
            raise ValueError(f"Unknown PhysioNet dataset: {self.dataset_name}")
