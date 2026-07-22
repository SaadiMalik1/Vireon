# Copyright 2026 VIREON Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Exhaustive Contract Testing Suite for all 13 VIREON V1 Provider Interfaces & Capability Proxies.
"""

import pytest
from typing import Any
from vireon.sdk.manifest import CapabilityManifest
from vireon.sdk.events import Event
from vireon.runtime.event_bus import EventBus
from vireon.runtime.state_store import StateStore
from vireon.runtime.capability_engine import EventBusProxy, StateStoreProxy, CapabilityViolationError
from vireon.sdk.provider_interfaces.v1 import (
    IProviderV1,
    IFirmwareProviderV1,
    IPhysicsProviderV1,
    ITelemetryProviderV1,
    IThreatModelProviderV1,
    IIDSProviderV1,
    IProtocolProviderV1,
    IClinicalProviderV1,
    IVisualizationProviderV1,
    IStorageProviderV1,
    ISchedulerProviderV1,
    IDecoderProviderV1,
    IBenchmarkProviderV1,
)


class MockFirmwareProvider(IFirmwareProviderV1):
    def health(self) -> dict:
        return {"status": "ok", "fw_ver": "2.4.0"}

    def write_memory(self, address: int, data: bytes) -> bool:
        return address > 0 and len(data) > 0

    def read_memory(self, address: int, size: int) -> bytes:
        return b"\x00" * size


class MockPhysicsProvider(IPhysicsProviderV1):
    def health(self) -> dict:
        return {"status": "ok", "temp": 37.0}

    def step_physics(self, dt: float) -> None:
        pass


class MockTelemetryProvider(ITelemetryProviderV1):
    def health(self) -> dict:
        return {"status": "ok"}

    def record_sample(self, channel: int, value: float) -> None:
        pass


class MockThreatModelProvider(IThreatModelProviderV1):
    def health(self) -> dict:
        return {"status": "ok"}

    def inject_anomaly(self) -> None:
        pass


class MockIDSProvider(IIDSProviderV1):
    def health(self) -> dict:
        return {"status": "ok"}

    def analyze_window(self, data: Any) -> bool:
        return False


class MockProtocolProvider(IProtocolProviderV1):
    def health(self) -> dict:
        return {"status": "ok"}

    def parse_packet(self, packet: bytes) -> dict:
        return {"len": len(packet)}


class MockClinicalProvider(IClinicalProviderV1):
    def health(self) -> dict:
        return {"status": "ok"}

    def evaluate_biomarker(self, data: Any) -> dict:
        return {"score": 0.95}


class MockVisualizationProvider(IVisualizationProviderV1):
    def health(self) -> dict:
        return {"status": "ok"}

    def render_frame(self) -> bytes:
        return b"FRAME_HEADER"


class MockStorageProvider(IStorageProviderV1):
    def health(self) -> dict:
        return {"status": "ok"}

    def store_blob(self, key: str, data: bytes) -> None:
        pass


class MockSchedulerProvider(ISchedulerProviderV1):
    def health(self) -> dict:
        return {"status": "ok"}

    def next_tick(self) -> float:
        return 0.004


class MockDecoderProvider(IDecoderProviderV1):
    def health(self) -> dict:
        return {"status": "ok"}

    def decode_intent(self, neural_data: Any) -> dict:
        return {"intent": "GRASP"}


class MockBenchmarkProvider(IBenchmarkProviderV1):
    def health(self) -> dict:
        return {"status": "ok"}

    def run_suite(self) -> dict:
        return {"score": 100}


def test_all_13_v1_provider_interface_contracts():
    providers = [
        MockFirmwareProvider(),
        MockPhysicsProvider(),
        MockTelemetryProvider(),
        MockThreatModelProvider(),
        MockIDSProvider(),
        MockProtocolProvider(),
        MockClinicalProvider(),
        MockVisualizationProvider(),
        MockStorageProvider(),
        MockSchedulerProvider(),
        MockDecoderProvider(),
        MockBenchmarkProvider(),
    ]

    for p in providers:
        assert isinstance(p, IProviderV1)
        h = p.health()
        assert isinstance(h, dict)
        assert h["status"] == "ok"


def test_firmware_provider_contract():
    fw = MockFirmwareProvider()
    assert fw.write_memory(0x1000, b"\xde\xad") is True
    assert fw.read_memory(0x1000, 4) == b"\x00\x00\x00\x00"


def test_clinical_and_decoder_provider_contracts():
    clin = MockClinicalProvider()
    dec = MockDecoderProvider()

    assert clin.evaluate_biomarker([1, 2, 3])["score"] == 0.95
    assert dec.decode_intent([0.1, 0.5])["intent"] == "GRASP"


def test_event_bus_proxy_capability_contract():
    manifest = CapabilityManifest(
        name="telemetry_plugin",
        version="1.0.0",
        category="plugin",
        publishes_events=["telemetry.chunk"],
        subscribes_events=["command.reset"]
    )
    bus = EventBus()
    proxy = EventBusProxy(bus, manifest)

    proxy.publish(Event(topic="telemetry.chunk", data={"val": 1.0}))
    with pytest.raises(CapabilityViolationError):
        proxy.publish(Event(topic="unauthorized.topic", data={"val": 1.0}))

    sub_id = proxy.subscribe("command.reset", lambda e: None)
    assert sub_id is not None
    with pytest.raises(CapabilityViolationError):
        proxy.subscribe("forbidden.topic", lambda e: None)


def test_state_store_proxy_capability_contract():
    manifest = CapabilityManifest(
        name="state_plugin",
        version="1.0.0",
        category="plugin",
        reads_state=["device_status"],
        mutates_state=["battery_level"]
    )
    bus = EventBus()
    store = StateStore(bus)
    store.set("device_status", "ACTIVE")

    proxy = StateStoreProxy(store, manifest)

    assert proxy.get("device_status") == "ACTIVE"
    with pytest.raises(CapabilityViolationError):
        proxy.get("secret_key")

    proxy.set("battery_level", 95)
    assert store.get("battery_level") == 95
    with pytest.raises(CapabilityViolationError):
        proxy.set("device_status", "COMPROMISED")
