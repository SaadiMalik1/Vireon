import numpy as np
from vireon.runtime.twin import DigitalTwin
from vireon.libraries.attack_factory.attack.adversarial import (
    AdversarialOptimizerAttack,
    RFJammingAttack,
    FramingDesynchronizationAttack,
    SessionReplayAttack
)

def test_adversarial_optimizer_attack():
    twin = DigitalTwin(num_channels=8)
    attack = AdversarialOptimizerAttack(target_channels=[0, 1], population_size=4)
    data = np.zeros((8, 100))
    rng = np.random.default_rng(42)
    
    # Run through the population to trigger evolution
    for _ in range(10):
        data = attack.apply(data, eeg_channels=list(range(8)), sample_rate=250, twin=twin, rng=rng)
        
    assert attack.generation > 0

def test_rf_jamming_attack():
    twin = DigitalTwin(num_channels=8)
    attack = RFJammingAttack(drop_rate=0.8)
    data = np.zeros((8, 100))
    
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=250, twin=twin)
    assert np.array_equal(result, data)
    assert getattr(twin, "rf_packet_drop_rate") == 0.8

def test_framing_desynchronization_attack():
    twin = DigitalTwin(num_channels=8)
    attack = FramingDesynchronizationAttack(target_channels=[0], inject_start_byte=True)
    data = np.zeros((8, 100))
    
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=250, twin=twin)
    # Target channel should be non-zero now
    assert np.all(result[0, :] != 0)
    assert np.all(result[1, :] == 0)

def test_session_replay_attack():
    twin = DigitalTwin(num_channels=8)
    attack = SessionReplayAttack(target_channels=[0], capture_duration_sec=0.1)
    data = np.ones((8, 10))
    
    # First phase: capturing (10 samples at 100Hz = 0.1s). Will finish capture in this call.
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=100, twin=twin)
    
    # Second phase: should start replaying once captured enough
    for _ in range(5):
        result = attack.apply(np.zeros((8, 10)), eeg_channels=list(range(8)), sample_rate=100, twin=twin)
        
    assert not attack.is_capturing
    assert np.all(result[0, :] == 1) # Replaying the ones we captured

from vireon.libraries.attack_factory.attack.adversarial import TemporalEvasionAttack
def test_temporal_evasion_attack():
    twin = DigitalTwin(num_channels=8)
    attack = TemporalEvasionAttack(target_channels=[0], burst_duration_sec=0.1, quiet_duration_sec=0.1, amplitude=50.0)
    data = np.zeros((8, 100))
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=100, twin=twin)
    assert result is not None
