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
import time
from vireon.runtime.twin import DigitalTwin
from vireon.runtime.attack import SignalAttackEngine
from vireon.runtime.engine import ReplayEngine
from vireon.runtime.state_store import StateStore
from vireon.runtime.event_bus import EventBus

class MockProvider:
    def __init__(self):
        self.device = self
        self.board = self
        self._stopped = False
    
    def get_eeg_channels(self):
        return [0, 1]
        
    def read_chunk(self, pos, num):
        if num == 0:
            return None
        return np.ones((4, num))
        
    def stop_stream(self):
        self._stopped = True
        
    def release_session(self):
        self._released = True

def test_replay_engine_start_stop():
    twin = DigitalTwin(num_channels=4)
    twin.sample_rate = 250
    event_bus = EventBus()
    state_store = StateStore(event_bus)
    state_store.set("sample_rate", 250)
    engine = SignalAttackEngine(twin)
    provider = MockProvider()
    
    replay = ReplayEngine(state_store, engine, provider=provider)
    replay.start(interval_sec=0.01)
    assert replay.running is True
    time.sleep(0.05)
    replay.stop()
    assert replay.running is False
    assert provider._stopped is True

def test_replay_engine_inject_attack():
    twin = DigitalTwin(num_channels=4)
    event_bus = EventBus()
    state_store = StateStore(event_bus)
    engine = SignalAttackEngine(twin)
    replay = ReplayEngine(state_store, engine)
    
    replay.inject_attack("noise")
    assert len(engine.modifiers) == 1
    
    replay.inject_attack("drift")
    assert len(engine.modifiers) == 1 # Replaced
    
    replay.inject_attack("none")
    assert len(engine.modifiers) == 0

def test_replay_engine_fetch_data():
    twin = DigitalTwin(num_channels=4)
    event_bus = EventBus()
    state_store = StateStore(event_bus)
    engine = SignalAttackEngine(twin)
    provider = MockProvider()
    
    replay = ReplayEngine(state_store, engine, provider=provider)
    data = replay._fetch_data(10, 4)
    assert data is not None
    assert data.shape == (4, 10)
    
    # Exhuast data loop test
    class ExhaustProvider:
        def get_eeg_channels(self): return [0]
        def read_chunk(self, p, n):
            if p > 0:
                raise ValueError("Exhausted")
            return np.ones((4, n))
            
    replay2 = ReplayEngine(state_store, engine, provider=ExhaustProvider(), loop_dataset=True)
    replay2.dataset_sample_position = 10
    data2 = replay2._fetch_data(10, 4)
    assert data2 is not None
    assert data2.shape == (4, 10)

def test_replay_engine_speed():
    twin = DigitalTwin(num_channels=4)
    event_bus = EventBus()
    state_store = StateStore(event_bus)
    engine = SignalAttackEngine(twin)
    replay = ReplayEngine(state_store, engine)
    
    replay.set_speed(2.0)
    assert replay.speed == 2.0
    
    replay.set_speed(0.05) # Test min clamp
    assert replay.speed == 0.1
