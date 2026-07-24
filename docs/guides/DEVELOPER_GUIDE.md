# VIREON Developer Guide

This guide is for developers writing core ecosystem code or creating new plugins.

## 1. Local Development
The recommended IDE is VSCode or RustRover with the provided `devcontainer.json`. This ensures exact parity with the CI environment.

## 2. Writing a Plugin
All plugins must implement `vireon.sdk.base_interfaces.IProvider`.

```python
from vireon.sdk.base_interfaces import IProvider

class MyCustomProvider(IProvider):
    def initialize(self, seed: int):
        pass
        
    def step(self, state, dt):
        return state
```

## 3. Telemetry and Logging
Use `vireon.sdk.logger` exclusively. Do not use Python's built-in `print` or `logging` modules directly, as they bypass the determinism trace logs.

## 4. Datasets & Telemetry Loaders
For synthetic physiological signal generation (EEG, ECG, EMG, Motor Imagery, SSVEP) and file loaders (NPZ, CSV, EDF), import from `vireon.datasets`. See [DATASETS_GUIDE.md](DATASETS_GUIDE.md) for detailed usage instructions.

