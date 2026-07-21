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
from vireon.runtime.detection import (
    calculate_spectral_features,
    LinearAutoencoderIDS,
    SecurityEngine,
    CoherenceEngine,
    TORCH_AVAILABLE
)

def test_calculate_spectral_features():
    signal = np.sin(2 * np.pi * 10 * np.linspace(0, 1, 250))
    entropy, crest = calculate_spectral_features(signal)
    assert isinstance(entropy, float)
    assert isinstance(crest, float)

def test_linear_autoencoder_ids():
    ids = LinearAutoencoderIDS(n_components=2)
    data = np.random.randn(8, 100)
    
    # Should buffer and return 0
    err = ids.detect(data)
    assert err == 0.0
    
    # Force calibration by feeding 100 times
    for _ in range(105):
        err = ids.detect(data)
    
    assert ids.is_fitted is True
    assert err >= 0.0

def test_coherence_engine():
    engine = CoherenceEngine()
    
    # Not stimulating
    score = engine.evaluate(False, 4.0)
    assert score > 0
    
    # Stimulating but body not reacting
    for _ in range(15):
        score = engine.evaluate(True, 4.0)
    assert score < 1.0

def test_security_engine_score_signal():
    twin = StateStore(EventBus())
    twin.set("num_channels", 8)
    twin.set("stimulation_enabled", False)
    engine = SecurityEngine(twin)
    
    data = np.random.randn(8, 10)
    score = engine.score_signal(data)
    assert score >= 0.0
    
    # Test NaN
    nan_data = np.full((8, 10), np.nan)
    assert engine.score_signal(nan_data) == float('inf')

def test_security_engine_analyze_commands():
    twin = StateStore(EventBus())
    twin.set("num_channels", 8)
    twin.set("stimulation_enabled", False)
    engine = SecurityEngine(twin)
    
    anomalies = engine.analyze_commands(1.0, 130.0)
    assert len(anomalies) == 0
    
    # High frequency changes
    for _ in range(6):
        twin.set("sim_clock", twin.get("sim_clock", 0.0) + 0.1)
        anomalies = engine.analyze_commands(np.random.rand(), 130.0)
        
    assert "HIGH_FREQUENCY_COMMAND_ANOMALY" in anomalies

def test_security_engine_slow_drift():
    twin = StateStore(EventBus())
    twin.set("num_channels", 8)
    twin.set("stimulation_enabled", False)
    engine = SecurityEngine(twin)
    engine.dynamic_baseline_enabled = True
    
    # Initialize baseline
    engine.analyze_signal(np.zeros((8, 100)))
    
    # Inject slow drift
    drift_data = np.ones((8, 100)) * 5.0
    for _ in range(10):
        anomalies = engine.analyze_signal(drift_data)
        if "SLOW_DRIFT_ANOMALY" in anomalies:
            break
            
def test_spectral_spoofing():
    twin = StateStore(EventBus())
    twin.set("num_channels", 8)
    twin.set("stimulation_enabled", False)
    engine = SecurityEngine(twin)
    
    # Pure tone signal (high spectral crest factor, low spectral entropy)
    t = np.linspace(0, 1, 100)
    data = np.zeros((8, 100))
    for i in range(8):
        data[i, :] = 1000.0 * np.sin(2 * np.pi * 50 * t)
    
    anomalies = engine.analyze_signal(data)
    assert "SPECTRAL_SPOOFING_ANOMALY" in anomalies

if TORCH_AVAILABLE:
    from vireon.runtime.detection import DeepAutoencoderIDS
    
    def test_deep_autoencoder_ids():
        ids = DeepAutoencoderIDS(input_dim=8)
        data = np.random.randn(8, 100)
        
        # Buffer
        err = ids.detect(data)
        assert err == 0.0
        
        # Force calibration
        for _ in range(55):
            err = ids.detect(data)
        
        assert ids.is_fitted is True
        assert err >= 0.0
