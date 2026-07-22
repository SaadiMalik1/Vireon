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
Phase 2 Contract Testing Suite for VIREON Provider Interfaces & Capability Proxies.
"""

import pytest
from vireon.sdk.manifest import CapabilityManifest
from vireon.sdk.events import Event
from vireon.runtime.event_bus import EventBus

from vireon.runtime.state_store import StateStore
from vireon.runtime.capability_engine import EventBusProxy, StateStoreProxy, CapabilityViolationError
from vireon.sdk.provider_interfaces.v1 import IPhysicsProviderV1


class SamplePhysicsProvider(IPhysicsProviderV1):
    def health(self) -> dict:
        return {"status": "ok", "temp": 37.0}

    def step_physics(self, dt: float) -> None:
        pass


def test_provider_health_contract():
    provider = SamplePhysicsProvider()
    health = provider.health()
    assert isinstance(health, dict)
    assert health.get("status") == "ok"


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

    # Allowed publish
    proxy.publish(Event(topic="telemetry.chunk", data={"val": 1.0}))

    # Forbidden publish
    with pytest.raises(CapabilityViolationError):
        proxy.publish(Event(topic="unauthorized.topic", data={"val": 1.0}))

    # Allowed subscribe
    sub_id = proxy.subscribe("command.reset", lambda e: None)
    assert sub_id is not None

    # Forbidden subscribe
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

    # Allowed read
    assert proxy.get("device_status") == "ACTIVE"

    # Forbidden read
    with pytest.raises(CapabilityViolationError):
        proxy.get("secret_key")

    # Allowed mutation
    proxy.set("battery_level", 95)
    assert store.get("battery_level") == 95

    # Forbidden mutation
    with pytest.raises(CapabilityViolationError):
        proxy.set("device_status", "COMPROMISED")
