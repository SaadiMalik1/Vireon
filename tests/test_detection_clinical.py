from vireon.runtime.twin import DigitalTwin
from vireon.reference_providers.ids.detection import SecurityEngine

def test_analyze_clinical_pathological_sync():
    twin = DigitalTwin(num_channels=8)
    engine = SecurityEngine(twin)
    
    # Not enough history
    anomalies = engine.analyze_clinical(current_beta_power=40.0, stim_enabled=True, amplitude=2.0)
    assert not anomalies
    
    # Provide enough history and high beta power while stimulating
    for _ in range(5):
        anomalies = engine.analyze_clinical(current_beta_power=40.0, stim_enabled=True, amplitude=2.0)
    
    assert "PATHOLOGICAL_SYNCHRONIZATION_ATTACK" in anomalies

def test_analyze_clinical_no_anomaly():
    twin = DigitalTwin(num_channels=8)
    engine = SecurityEngine(twin)
    
    for _ in range(5):
        anomalies = engine.analyze_clinical(current_beta_power=10.0, stim_enabled=True, amplitude=2.0)
        
    assert "PATHOLOGICAL_SYNCHRONIZATION_ATTACK" not in anomalies
    
def test_analyze_clinical_low_amplitude():
    twin = DigitalTwin(num_channels=8)
    engine = SecurityEngine(twin)
    
    for _ in range(5):
        anomalies = engine.analyze_clinical(current_beta_power=40.0, stim_enabled=True, amplitude=0.5)
        
    assert "PATHOLOGICAL_SYNCHRONIZATION_ATTACK" not in anomalies

def test_log_detection():
    twin = DigitalTwin(num_channels=8)
    engine = SecurityEngine(twin)
    engine._log_detection("TEST_ANOMALY", channel=0, value=123.45)
    # Just checking it doesn't crash
