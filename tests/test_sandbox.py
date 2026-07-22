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
from vireon.sdk.manifest import CapabilityManifest
from vireon.runtime.sandbox import SeccompProfileGenerator, ProcessSandbox
from vireon.runtime.memory_protect import UnidirectionalMemoryGuard


def test_seccomp_profile_generation():
    manifest = CapabilityManifest(name="untrusted_provider", version="1.0.0", category="device", requires_host_access=False)
    profile = SeccompProfileGenerator.generate_profile(manifest)

    assert profile["defaultAction"] == "SCMP_ACT_KILL_PROCESS"
    syscall_names = [item["name"] for item in profile["syscalls"]]
    assert "read" in syscall_names
    assert "write" in syscall_names
    assert "open" not in syscall_names


def test_process_sandbox_policy():
    manifest = CapabilityManifest(name="sandboxed_p", version="1.0.0", category="plugin")
    sandbox = ProcessSandbox(manifest)

    assert sandbox.verify_isolation_policy() is True
    assert sandbox.apply_isolation_policy() is True


def test_unidirectional_memory_guard():
    data = np.array([1, 2, 3, 4], dtype=np.int32)
    readonly_view = UnidirectionalMemoryGuard.wrap_readonly(data)

    assert UnidirectionalMemoryGuard.verify_read_only(readonly_view) is True
    assert readonly_view.flags.writeable is False

