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
Exhaustive Phase 4 Latency Distribution & System Performance Benchmarking Suite.
"""

import time
import json
import numpy as np
from typing import Dict, Any, List
from vireon.runtime.event_bus import EventBus, Event
from vireon.runtime.state_store import StateStore
from vireon.runtime.ring_buffer import SPSCRingBuffer
from vireon.runtime.orchestrator import VireonOrchestrator
from vireon.sdk.capability.descriptor import CapabilityDescriptor
from vireon.sdk.provider_interfaces.v1 import IPhysicsProviderV1
from cryptography.hazmat.primitives.asymmetric import ed25519
from vireon.runtime.trace_bundle import TraceBundle


class DummyPhysicsProvider(IPhysicsProviderV1):
    def health(self) -> dict:
        return {"status": "ok"}

    def step_physics(self, dt: float) -> None:
        _ = dt * 1.0001


def benchmark_event_bus_latency_distribution(iterations: int = 20000) -> Dict[str, float]:
    bus = EventBus()
    count = 0

    def handler(e):
        nonlocal count
        count += 1

    bus.subscribe("benchmark.topic", handler)
    event = Event(topic="benchmark.topic", data={"val": 1.0})

    latencies_us: List[float] = []
    t0_total = time.perf_counter()
    for _ in range(iterations):
        t0 = time.perf_counter()
        bus.publish(event)
        t1 = time.perf_counter()
        latencies_us.append((t1 - t0) * 1e6)
    t1_total = time.perf_counter()

    ops_sec = iterations / (t1_total - t0_total)
    arr = np.array(latencies_us)

    return {
        "ops_sec": round(ops_sec, 2),
        "p50_us": round(float(np.percentile(arr, 50)), 3),
        "p90_us": round(float(np.percentile(arr, 90)), 3),
        "p99_us": round(float(np.percentile(arr, 99)), 3),
        "p99_9_us": round(float(np.percentile(arr, 99.9)), 3),
    }


def benchmark_state_store_latency(iterations: int = 20000) -> Dict[str, float]:
    bus = EventBus()
    store = StateStore(bus)

    latencies_us: List[float] = []
    for i in range(iterations):
        t0 = time.perf_counter()
        store.set("key", i)
        _ = store.get("key")
        t1 = time.perf_counter()
        latencies_us.append(((t1 - t0) / 2.0) * 1e6)

    arr = np.array(latencies_us)
    return {
        "avg_latency_us": round(float(np.mean(arr)), 3),
        "p50_us": round(float(np.percentile(arr, 50)), 3),
        "p99_us": round(float(np.percentile(arr, 99)), 3),
    }


def benchmark_ring_buffer_speed(iterations: int = 50000) -> float:
    ring = SPSCRingBuffer[float](capacity=1024)

    t0 = time.perf_counter()
    for i in range(iterations):
        ring.push(float(i))
        ring.pop()
    t1 = time.perf_counter()

    ops_per_sec = (iterations * 2) / (t1 - t0)
    return round(ops_per_sec, 2)


def benchmark_ed25519_signing_latency(iterations: int = 1000) -> float:
    key = ed25519.Ed25519PrivateKey.generate()
    bundle = TraceBundle(merkle_root_hex="a" * 64, pin_hash="pin_123")

    t0 = time.perf_counter()
    for _ in range(iterations):
        bundle.sign(key)
    t1 = time.perf_counter()

    avg_ms = ((t1 - t0) / iterations) * 1000.0
    return round(avg_ms, 3)


def benchmark_orchestrator_provider_scalability(num_providers: int = 100, ticks: int = 500) -> float:
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
    return round(avg_tick_us, 2)


def run_full_benchmark_matrix() -> Dict[str, Any]:
    print("[BENCHMARK] Running Exhaustive VIREON Performance Matrix...")
    eb_metrics = benchmark_event_bus_latency_distribution(20000)
    ss_metrics = benchmark_state_store_latency(20000)
    ring_ops = benchmark_ring_buffer_speed(50000)
    signing_ms = benchmark_ed25519_signing_latency(1000)

    tick_10p_us = benchmark_orchestrator_provider_scalability(10, 500)
    tick_100p_us = benchmark_orchestrator_provider_scalability(100, 500)
    tick_1000p_us = benchmark_orchestrator_provider_scalability(1000, 100)

    results = {
        "event_bus_throughput_ops_sec": eb_metrics["ops_sec"],
        "event_bus_p50_us": eb_metrics["p50_us"],
        "event_bus_p99_us": eb_metrics["p99_us"],
        "state_store_avg_latency_us": ss_metrics["avg_latency_us"],
        "state_store_p99_us": ss_metrics["p99_us"],
        "spsc_ring_buffer_throughput_ops_sec": ring_ops,
        "ed25519_trace_signing_ms": signing_ms,
        "orchestrator_tick_latency_10_providers_us": tick_10p_us,
        "orchestrator_tick_latency_100_providers_us": tick_100p_us,
        "orchestrator_tick_latency_1000_providers_us": tick_1000p_us,
    }
    return results


if __name__ == "__main__":
    res = run_full_benchmark_matrix()
    print(json.dumps(res, indent=2))
