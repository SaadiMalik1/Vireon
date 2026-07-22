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
Phase 4 Automated System Performance & Latency Benchmarking Suite.
"""

import time
import json
import numpy as np
from typing import Dict, Any
from vireon.runtime.event_bus import EventBus, Event
from vireon.runtime.state_store import StateStore
from vireon.runtime.clock import DeterministicClock
from vireon.runtime.ring_buffer import SPSCRingBuffer
from vireon.runtime.orchestrator import VireonOrchestrator
from vireon.sdk.manifest import CapabilityManifest
from vireon.sdk.capability.descriptor import CapabilityDescriptor
from vireon.sdk.provider_interfaces.v1 import IPhysicsProviderV1



class DummyPhysicsProvider(IPhysicsProviderV1):
    def health(self) -> dict:
        return {"status": "ok"}

    def step_physics(self, dt: float) -> None:
        _ = dt * 1.0001


def benchmark_event_bus_throughput(iterations: int = 50000) -> float:
    bus = EventBus()
    count = 0

    def handler(e):
        nonlocal count
        count += 1

    bus.subscribe("benchmark.topic", handler)
    event = Event(topic="benchmark.topic", data={"val": 1.0})

    t0 = time.perf_counter()
    for _ in range(iterations):
        bus.publish(event)
    t1 = time.perf_counter()

    ops_per_sec = iterations / (t1 - t0)
    return ops_per_sec


def benchmark_state_store_latency(iterations: int = 50000) -> float:
    bus = EventBus()
    store = StateStore(bus)

    t0 = time.perf_counter()
    for i in range(iterations):
        store.set("key", i)
        _ = store.get("key")
    t1 = time.perf_counter()

    avg_latency_us = ((t1 - t0) / (iterations * 2)) * 1e6
    return avg_latency_us


def benchmark_ring_buffer_speed(iterations: int = 100000) -> float:
    ring = SPSCRingBuffer[float](capacity=1024)

    t0 = time.perf_counter()
    for i in range(iterations):
        ring.push(float(i))
        ring.pop()
    t1 = time.perf_counter()

    ops_per_sec = (iterations * 2) / (t1 - t0)
    return ops_per_sec


def benchmark_orchestrator_provider_scalability(num_providers: int = 100, ticks: int = 1000) -> float:
    bus = EventBus()
    store = StateStore(bus)
    orch = VireonOrchestrator(store, bus)

    for i in range(num_providers):
        p = DummyPhysicsProvider()
        desc = CapabilityDescriptor(id=f"provider_{i}", implements=["IPhysicsProviderV1"])
        orch.register_provider(p, desc)

    orch.initialize_all()
    orch.start_all()

    t0 = time.perf_counter()
    for _ in range(ticks):
        orch.tick_all(0.004)
    t1 = time.perf_counter()

    avg_tick_us = ((t1 - t0) / ticks) * 1e6
    return avg_tick_us


def run_full_benchmark_matrix() -> Dict[str, Any]:
    print("[BENCHMARK] Running VIREON System Performance Matrix...")
    event_bus_ops = benchmark_event_bus_throughput(20000)
    state_latency_us = benchmark_state_store_latency(20000)
    ring_buffer_ops = benchmark_ring_buffer_speed(50000)
    tick_latency_10p_us = benchmark_orchestrator_provider_scalability(10, 500)
    tick_latency_100p_us = benchmark_orchestrator_provider_scalability(100, 500)

    results = {
        "event_bus_throughput_ops_sec": round(event_bus_ops, 2),
        "state_store_latency_us": round(state_latency_us, 3),
        "spsc_ring_buffer_throughput_ops_sec": round(ring_buffer_ops, 2),
        "orchestrator_tick_latency_10_providers_us": round(tick_latency_10p_us, 2),
        "orchestrator_tick_latency_100_providers_us": round(tick_latency_100p_us, 2)
    }
    return results


if __name__ == "__main__":
    res = run_full_benchmark_matrix()
    print(json.dumps(res, indent=2))
