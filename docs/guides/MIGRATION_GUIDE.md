# VIREON Ecosystem Migration Guide

This guide details the procedure for migrating legacy `vireon` plugins to the new `vireon.sdk` architecture.

## Legacy to v1.0.0 Migration

### 1. Removing Logic from Constructors
**Legacy:**
```python
class OldProvider:
    def __init__(self):
        self.db = Database.connect() # Side effect on load
```

**New Standard:**
```python
class NewProvider(IProvider):
    def initialize(self, seed: int):
        # All side effects must happen here, seeded deterministically
        self.db = Database.connect(seed=seed) 
```

### 2. Porting Physics to Rust
If you have high-frequency physics models (e.g., Runge-Kutta 4th order ODEs) currently written in Python, you must migrate them to `neurodsl` using PyO3 bindings, and expose them back to Python solely as a control interface, rather than iterating through the ODE step within the Python `EventBus`.
