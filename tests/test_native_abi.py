import os
import subprocess
import pytest
from vireon.runtime.orchestrator import VireonOrchestrator

class DummyStateStore:
    def __init__(self):
        self.data = {"battery_voltage": 3.7, "tissue_temperature": 37.0}
    def get(self, key, default=None):
        return self.data.get(key, default)
    def set(self, key, value, source=None):
        self.data[key] = value

class DummyEventBus:
    def publish(self, event):
        pass

def test_native_abi_compiles_and_runs():
    base_dir = os.path.dirname(os.path.dirname(__file__))
    dummy_c = os.path.join(base_dir, "vireon", "reference_providers", "native_dummy", "dummy.c")
    dummy_so = os.path.join(base_dir, "vireon", "reference_providers", "native_dummy", "dummy.so")
    
    # Compile the shared library
    compile_cmd = ["gcc", "-shared", "-fPIC", "-o", dummy_so, dummy_c]
    res = subprocess.run(compile_cmd, capture_output=True)
    assert res.returncode == 0, f"Compilation failed: {res.stderr.decode()}"
    
    assert os.path.exists(dummy_so), "Shared library was not created"
    
    try:
        store = DummyStateStore()
        bus = DummyEventBus()
        
        orchestrator = VireonOrchestrator(store, bus)
        
        # Load the native provider
        orchestrator.load_native_provider(dummy_so)
        
        # Verify it was registered
        assert "vireon.reference.native_dummy" in orchestrator.providers
        provider = orchestrator.providers["vireon.reference.native_dummy"]
        
        # Initialize
        orchestrator.initialize_all()
        
        # Verify health
        health = provider.health()
        assert health.get("status") == "ok"
        assert health.get("native") is True
        
        # Start and Tick
        orchestrator.start_all()
        orchestrator.tick_all(0.1)
        
        # The C code should have read battery_voltage and set tissue_temperature to 38.5 + dt (0.1)
        assert store.data["tissue_temperature"] == pytest.approx(38.6)
        
    finally:
        if os.path.exists(dummy_so):
            os.remove(dummy_so)
