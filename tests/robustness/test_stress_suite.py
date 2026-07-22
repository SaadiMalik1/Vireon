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
Phase 6 System Robustness & Stress Testing Suite.
"""

import pytest
import numpy as np
from vireon.datasets.synthetic import SyntheticDataGenerator
from vireon.runtime.event_bus import EventBus
from vireon.runtime.state_store import StateStore
from vireon.runtime.orchestrator import VireonOrchestrator, OrchestrationFault
from vireon.sdk.capability.descriptor import CapabilityDescriptor
from vireon.sdk.provider_interfaces.v1 import IPhysicsProviderV1


class FlakyProvider(IPhysicsProviderV1):
    def health(self) -> dict:
        return {"status": "degraded"}

    def step_physics(self, dt: float) -> None:
        pass


def test_synthetic_generator_reproducibility():
    gen1 = SyntheticDataGenerator(seed=777)
    gen2 = SyntheticDataGenerator(seed=777)

    chunk1 = gen1.generate_chunk(duration_sec=0.5, noise_level=0.2, packet_loss_rate=0.05)
    chunk2 = gen2.generate_chunk(duration_sec=0.5, noise_level=0.2, packet_loss_rate=0.05)

    assert np.array_equal(chunk1["data"], chunk2["data"])


def test_repeated_provider_registration_rejection():
    bus = EventBus()
    store = StateStore(bus)
    orch = VireonOrchestrator(store, bus)

    provider = FlakyProvider()
    desc = CapabilityDescriptor(id="flaky_01", implements=["IPhysicsProviderV1"])

    orch.register_provider(provider, desc)
    with pytest.raises(OrchestrationFault):
        orch.register_provider(provider, desc)


def test_high_frequency_ring_buffer_stress():
    from vireon.runtime.ring_buffer import SPSCRingBuffer
    ring = SPSCRingBuffer[int](capacity=100)

    # Push 500 items into buffer of size 100 to verify graceful overwrite protection
    for i in range(500):
        ring.push(i)

    assert ring.dropped_samples > 0
    assert ring.size() < 100
