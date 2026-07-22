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

import numpy as np
from vireon.runtime.control_plane import ControlPlaneServer, ProviderLifecycleState
from vireon.runtime.shared_mem import SharedMemoryBuffer
from vireon.runtime.ring_buffer import SPSCRingBuffer
from vireon.sdk.manifest import CapabilityManifest


def test_control_plane_lifecycle():
    server = ControlPlaneServer()
    manifest = CapabilityManifest(name="test_provider", version="1.0.0", category="device")

    assert server.register_provider("p1", manifest) is True
    assert server.get_provider_state("p1") == ProviderLifecycleState.REGISTERED

    server.transition_state("p1", ProviderLifecycleState.RUNNING)
    assert server.get_provider_state("p1") == ProviderLifecycleState.RUNNING


def test_shared_memory_zero_copy_handoff():
    shm_name = "test_vireon_shm_buffer"
    writer = SharedMemoryBuffer(name=shm_name, size_bytes=1024, create=True)
    reader = SharedMemoryBuffer(name=shm_name, size_bytes=1024, create=False)

    data = np.array([1.0, 2.0, 3.0, 4.0], dtype=np.float32)
    writer.write_array(data)

    read_data = reader.read_array(shape=(4,), dtype=np.float32)
    assert (data == read_data).all()

    writer.close()
    reader.close()
    writer.unlink()


def test_spsc_ring_buffer_push_pop():
    rb = SPSCRingBuffer[int](capacity=4)
    rb.push(10)
    rb.push(20)

    assert rb.pop() == 10
    assert rb.pop() == 20
    assert rb.pop() is None
