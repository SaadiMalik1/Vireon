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

import numpy as np
import importlib
StateStore = importlib.import_module('vireon.runtime.state_store').StateStore
EventBus = importlib.import_module('vireon.runtime.event_bus').EventBus
from vireon.runtime.detection import SecurityEngine

def test_autoencoder_and_cusum():
    twin = StateStore(EventBus())
    twin.set("num_channels", 8)
    twin.set("stimulation_enabled", False)
    ids = SecurityEngine(twin)
    
    # Send nominal data (pink noise-like) to establish baseline
    for _ in range(50):
        data = np.random.normal(0, 1.0, (8, 250))
        anomalies = ids.analyze_signal(data)
        assert "SLOW_DRIFT_ANOMALY" not in anomalies
        
    # Introduce slow drift
    for i in range(15):
        data = np.random.normal(i * 1.5, 1.0, (8, 250))
        anomalies = ids.analyze_signal(data)
        if "SLOW_DRIFT_ANOMALY" in anomalies:
            break
            
    assert "SLOW_DRIFT_ANOMALY" in anomalies
    
    if ids.autoencoder is None:
        import pytest
        pytest.skip("Autoencoder not initialized (PyTorch missing)")

    # Test Autoencoder structural deviation
    # We send data with completely different covariance structure
    abnormal_data = np.random.normal(0, 100.0, (8, 250))
    # Inject anti-correlation to break learned PCA structure
    abnormal_data[1, :] = -abnormal_data[0, :] * 50.0
    
    anomalies = ids.analyze_signal(abnormal_data)
    if "STRUCTURAL_DEVIATION_ANOMALY" not in anomalies:
        # Give it another push
        anomalies = ids.analyze_signal(abnormal_data * 10)
        
    assert "STRUCTURAL_DEVIATION_ANOMALY" in anomalies
