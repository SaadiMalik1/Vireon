import numpy as np
from vireon.runtime.twin import DigitalTwin
from vireon.libraries.attack_factory.attack.physical import (
    ElectrodeSaturationAttack,
    PacketLossAttack,
    TimingJitterAttack,
    DropoutAttack,
    ClippingAttack,
    AmplifierSaturationAttack,
    EMIAttack
)

def test_electrode_saturation_attack():
    twin = DigitalTwin(num_channels=8)
    attack = ElectrodeSaturationAttack(target_channels=[0, 1])
    data = np.zeros((8, 10))
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=100, twin=twin)
    assert np.all(result[0] == 1e6)
    assert np.all(result[1] == 1e6)
    assert np.all(result[2] == 0.0)

def test_packet_loss_attack():
    twin = DigitalTwin(num_channels=8)
    attack = PacketLossAttack(target_channels=[0], drop_prob=1.0)
    data = np.ones((8, 10))
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=100, twin=twin)
    assert np.all(result[0] == 0.0)
    assert np.all(result[1] == 1.0)

def test_timing_jitter_attack():
    twin = DigitalTwin(num_channels=8)
    attack = TimingJitterAttack(target_channels=[0], jitter_ms=10.0)
    data = np.zeros((8, 100))
    data[0, 50] = 1.0
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=100, twin=twin)
    # 10ms at 100Hz = 1 sample
    assert result[0, 51] == 1.0

def test_dropout_attack():
    twin = DigitalTwin(num_channels=8)
    attack = DropoutAttack(target_channels=[0], dropout_length_sec=0.05)
    data = np.ones((8, 100))
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=100, twin=twin)
    # 0.05s * 100 = 5 samples
    assert np.sum(result[0] == 0.0) == 5

def test_clipping_attack():
    twin = DigitalTwin(num_channels=8)
    attack = ClippingAttack(target_channels=[0], clip_value=10.0)
    data = np.ones((8, 10)) * 50.0
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=100, twin=twin)
    assert np.all(result[0] == 10.0)

def test_amplifier_saturation_attack():
    twin = DigitalTwin(num_channels=8)
    attack = AmplifierSaturationAttack(target_channels=[0])
    data = np.array([[1.0, -1.0, 0.0]] * 8)
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=100, twin=twin)
    assert result[0, 0] == 500.0
    assert result[0, 1] == -500.0
    assert result[0, 2] == -500.0

def test_emi_attack():
    twin = DigitalTwin(num_channels=8)
    attack = EMIAttack(target_channels=[0])
    data = np.zeros((8, 10))
    result = attack.apply(data, eeg_channels=list(range(8)), sample_rate=100, twin=twin)
    assert np.any(result[0] != 0.0)
