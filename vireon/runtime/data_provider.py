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
VIREON Data Provider Adapters.
Adapts physical hardware emulators and pre-recorded datasets into standard telemetry providers.
"""

import numpy as np
from typing import Any

class DeviceProviderAdapter:
    """Adapts a hardware device emulator instance into a telemetry provider interface."""
    def __init__(self, device_instance: Any):
        self.device_instance = device_instance

    def read_chunk(self, num_samples: int) -> np.ndarray:
        if hasattr(self.device_instance, "read_chunk"):
            return self.device_instance.read_chunk(num_samples)
        elif hasattr(self.device_instance, "get_sample"):
            return np.array([self.device_instance.get_sample() for _ in range(num_samples)]).T
        return np.zeros((8, num_samples))

class DatasetProviderAdapter:
    """Adapts pre-recorded EEG dataset readers into standard chunked telemetry stream providers."""
    def __init__(self, dataset_reader: Any):
        self.dataset_reader = dataset_reader

    def read_chunk(self, num_samples: int) -> np.ndarray:
        if hasattr(self.dataset_reader, "read_chunk"):
            return self.dataset_reader.read_chunk(num_samples)
        return np.zeros((8, num_samples))
