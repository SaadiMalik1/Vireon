# VIREON Multi-Channel Dataset & Synthetic Generator Validation

**Standard:** `gemi3.6r/vvvv` (Phase 5 Datasets)  

## Synthetic Generator Capabilities (`vireon/datasets/synthetic.py`)
- **Multi-Frequency EEG Composition:** Delta (2Hz), Alpha (10Hz), Beta (20Hz), Gamma (40Hz).
- **ERP Spike Injection:** P300 spike (+40µV peak at t=300ms) validation.
- **Artifact & Noise Modeling:** 50/60Hz powerline hum, Gaussian noise, channel dropouts, BLE packet loss.
