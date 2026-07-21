import os
import tempfile
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


DUMMY_C_SOURCE = """
#include <stdio.h>
#include <string.h>

const char* vireon_get_descriptor() {
    return "{\\"id\\": \\"vireon.reference.native_dummy\\", \\"version\\": \\"1.0.0\\", \\"implements\\": []}";
}

int vireon_initialize(void* services) {
    return 0;
}

const char* vireon_health() {
    return "{\\"status\\": \\"ok\\", \\"native\\": true}";
}
"""


def test_native_abi_compiles_and_runs():
    with tempfile.TemporaryDirectory() as tmpdir:
        dummy_c = os.path.join(tmpdir, "dummy.c")
        dummy_so = os.path.join(tmpdir, "dummy.so")

        with open(dummy_c, "w") as f:
            f.write(DUMMY_C_SOURCE)

        compile_cmd = ["gcc", "-shared", "-fPIC", "-o", dummy_so, dummy_c]
        res = subprocess.run(compile_cmd, capture_output=True)
        if res.returncode != 0:
            pytest.skip("GCC compiler not available or shared compilation failed")

        store = DummyStateStore()
        bus = DummyEventBus()
        orchestrator = VireonOrchestrator(store, bus)

        orchestrator.load_native_provider(dummy_so)
        assert "vireon.reference.native_dummy" in orchestrator.providers
        provider = orchestrator.providers["vireon.reference.native_dummy"]
        health = provider.health()
        assert health.get("status") == "ok"
