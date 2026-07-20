import numpy as np
from vireon.sdk.anonymizer import TemporalJittering, ChannelPermutation, SpectralMasking, ReidentificationRiskScorer

def test_temporal_jittering():
    jitter = TemporalJittering(max_jitter_ms=10, sample_rate=100)
    chunk = np.ones((2, 100))
    result = jitter.apply(chunk)
    assert result.shape == chunk.shape
    
def test_channel_permutation():
    perm = ChannelPermutation(symmetric_pairs=[(0, 1)])
    chunk = np.array([[1.0, 1.0], [2.0, 2.0]])
    result = perm.apply(chunk)
    assert result.shape == chunk.shape
    
def test_spectral_masking():
    masking = SpectralMasking(cutoff_hz=10.0, sample_rate=100)
    chunk = np.random.rand(2, 100)
    result = masking.apply(chunk)
    assert result.shape == chunk.shape

def test_risk_scorer():
    scorer = ReidentificationRiskScorer()
    history = [{"timestamp": 1.0}, {"timestamp": 2.5}]
    score = scorer.score_risk(history)
    assert isinstance(score, float)
    assert 0.0 <= score <= 1.0

