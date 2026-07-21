import numpy as np
import importlib
StateStore = importlib.import_module('vireon.runtime.state_store').StateStore
EventBus = importlib.import_module('vireon.runtime.event_bus').EventBus
from vireon.libraries.attack_factory.attack.adversarial import (
    AdversarialOptimizerAttack,
    RFJammingAttack,
    FramingDesynchronizationAttack,
    SessionReplayAttack
)

def test_adversarial_optimizer_attack():
    twin = StateStore(EventBus())
    twin.set("num_channels", 8)
    twin.set("stimulation_enabled", False)
    attack = AdversarialOptimizerAttack(target_channels=[0, 1], population_size=4)
    data = np.zeros((8, 100))
    rng = np.random.default_rng(42)
    
    # Run through the population to trigger evolution
    for _ in range(10):
        data = attack.apply(data, eeg_channels=list(range(8)), sample_rate=250, state_store=twin, rng=rng)
        
    assert attack.generation > 0

def test_rf_jamming_attack():
    twin = StateStore(EventBus())
    twin.set("num_channels", 8)
    twin.set("stimulation_enabled", False)
    attack = RFJammingAttack(drop_rate=0.8)
    data = np.zeros((8, 100))
    
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=250, state_store=twin)
    assert np.array_equal(result, data)
    assert twin.get("rf_packet_drop_rate") == 0.8

def test_framing_desynchronization_attack():
    twin = StateStore(EventBus())
    twin.set("num_channels", 8)
    twin.set("stimulation_enabled", False)
    attack = FramingDesynchronizationAttack(target_channels=[0], inject_start_byte=True)
    data = np.zeros((8, 100))
    
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=250, state_store=twin)
    # Target channel should be non-zero now
    assert np.all(result[0, :] != 0)
    assert np.all(result[1, :] == 0)

def test_session_replay_attack():
    twin = StateStore(EventBus())
    twin.set("num_channels", 8)
    twin.set("stimulation_enabled", False)
    attack = SessionReplayAttack(target_channels=[0], capture_duration_sec=0.1)
    data = np.ones((8, 10))
    
    # First phase: capturing (10 samples at 100Hz = 0.1s). Will finish capture in this call.
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=100, state_store=twin)
    
    # Second phase: should start replaying once captured enough
    for _ in range(5):
        result = attack.apply(np.zeros((8, 10)), eeg_channels=list(range(8)), sample_rate=100, state_store=twin)
        
    assert not attack.is_capturing
    assert np.all(result[0, :] == 1) # Replaying the ones we captured

from vireon.libraries.attack_factory.attack.adversarial import TemporalEvasionAttack
def test_temporal_evasion_attack():
    twin = StateStore(EventBus())
    twin.set("num_channels", 8)
    twin.set("stimulation_enabled", False)
    attack = TemporalEvasionAttack(target_channels=[0], burst_duration_sec=0.1, quiet_duration_sec=0.1, amplitude=50.0)
    data = np.zeros((8, 100))
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=100, state_store=twin)
    assert result is not None
