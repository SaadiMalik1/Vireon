# VIREON Physiological Datasets & Telemetry Loaders Guide

VIREON provides a comprehensive dataset module (`vireon.datasets`) designed for synthetic biopotential signal generation, standard neuroscience file format ingestion, and benchmark dataset loading for neurotechnology AI models.

---

## 1. Synthetic Biopotential Signal Generators

Module: `vireon.datasets.biopotentials` & `vireon.datasets.synthetic`

### `SyntheticDataGenerator` (Multi-Band EEG)
Generates multi-band (Delta, Theta, Alpha, Beta, Gamma) EEG telemetry streams with configurable noise, powerline hum (50Hz/60Hz), P300 Event-Related Potential (ERP) spikes, channel dropouts, and BLE packet loss.

```python
from vireon.datasets import SyntheticDataGenerator

gen = SyntheticDataGenerator(seed=42, num_channels=8, sample_rate=250.0)
stream = gen.generate_eeg_stream(duration_sec=2.0, noise_level=0.1, include_p300=True)
print(stream["data"].shape)  # (500, 8)
```

### `ECGDataGenerator` (Electrocardiogram)
Synthesizes ECG signals with realistic P-Q-R-S-T wave morphology, heart rate variability (HRV), and ectopic arrhythmia pulses.

```python
from vireon.datasets import ECGDataGenerator

ecg_gen = ECGDataGenerator(seed=100, sample_rate=250.0, base_bpm=60.0)
stream = ecg_gen.generate_ecg_stream(duration_sec=10.0, hrv_std_bpm=3.0)
```

### `EMGDataGenerator` (Electromyogram)
Generates multi-channel EMG muscle activation signals with envelope-controlled contraction bursts and fatigue spectral shifts.

```python
from vireon.datasets import EMGDataGenerator

emg_gen = EMGDataGenerator(seed=42, num_channels=4, sample_rate=1000.0)
emg_bursts = emg_gen.generate_emg_bursts(duration_sec=5.0, burst_interval_sec=1.5)
```

### `MotorImageryEEGGenerator` (Mu/Beta ERD Task Signals)
Generates Motor Imagery trial signals exhibiting Event-Related Desynchronization (ERD) in Mu (8–12 Hz) and Beta (13–30 Hz) bands across 4 task classes: `left_hand`, `right_hand`, `feet`, `tongue`.

```python
from vireon.datasets import MotorImageryEEGGenerator

mi_gen = MotorImageryEEGGenerator(seed=777, num_channels=8, sample_rate=250.0)
trial = mi_gen.generate_trial(target_class="left_hand", trial_duration_sec=4.0)
```

### `SSVEPDataGenerator` (Steady-State Visual Evoked Potentials)
Synthesizes SSVEP signals with fundamental flickering frequencies (e.g. 12 Hz, 15 Hz) and harmonics injected into occipital channels.

```python
from vireon.datasets import SSVEPDataGenerator

ssvep_gen = SSVEPDataGenerator(seed=55, num_channels=8, sample_rate=250.0)
ssvep_trial = ssvep_gen.generate_ssvep_trial(flicker_freq_hz=12.0, duration_sec=3.0)
```

---

## 2. File-Based Dataset Loaders

Module: `vireon.datasets.loaders`

### `NPZDatasetReader`
Loads pre-recorded NumPy `.npz` files containing telemetry arrays and label arrays.

```python
from vireon.datasets import NPZDatasetReader

reader = NPZDatasetReader("path/to/recording.npz")
chunk = reader.read_chunk(start_sample=0, num_samples=250)
```

### `CSVDatasetReader`
Loads multi-channel CSV time-series telemetry recordings.

```python
from vireon.datasets import CSVDatasetReader

reader = CSVDatasetReader("path/to/telemetry.csv", delimiter=",", skip_header=1)
chunk = reader.read_chunk(start_sample=0, num_samples=100)
```

### `EDFDatasetReader`
Loads European Data Format (`.edf`/`.bdf`) physiological signal recordings with pure-Python header parsing and sample decoding.

```python
from vireon.datasets import EDFDatasetReader

reader = EDFDatasetReader("path/to/subject.edf")
print(reader.header["labels"])
chunk = reader.read_chunk(start_sample=0, num_samples=500)
```

---

## 3. Benchmark Dataset Interfaces

Module: `vireon.datasets.benchmarks`

### `BCICompetitionIVDataset`
Provides a standard benchmark interface for BCI Competition IV 2a/2b motor imagery datasets across 22 EEG channels.

```python
from vireon.datasets import BCICompetitionIVDataset

bci = BCICompetitionIVDataset(subject_id=1, seed=42)
X, y = bci.load_trials(num_trials=40)  # X shape: (40, 1000, 22), y shape: (40,)
```

### `PhysioNetDatasetLoader`
Interface for PhysioNet benchmark databases such as EEG Motor Movement/Imagery (`eegmmidb`) and ECG (`mitdb`).

```python
from vireon.datasets import PhysioNetDatasetLoader

loader = PhysioNetDatasetLoader(dataset_name="eegmmidb")
record = loader.fetch_subject_data(subject_id=1)
```
