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
Process Isolation & Seccomp Profile Generator (ADR-006).

Maps provider capability manifests into Linux seccomp-bpf syscall filters and process
isolation profiles to enforce zero-trust OS boundary sandboxing.
"""

from typing import Dict, Any
from vireon.sdk.manifest import CapabilityManifest


class SeccompProfileGenerator:
    """
    Seccomp-BPF Profile Generator (ADR-006).
    """

    ALLOWED_BASE_SYSCALLS = ["read", "write", "exit", "exit_group", "futex", "sigreturn"]

    @classmethod
    def generate_profile(cls, manifest: CapabilityManifest) -> Dict[str, Any]:
        allowed_syscalls = set(cls.ALLOWED_BASE_SYSCALLS)

        if manifest.requires_host_access:
            allowed_syscalls.update(["open", "openat", "close", "fstat"])

        return {
            "defaultAction": "SCMP_ACT_KILL_PROCESS",
            "architectures": ["SCMP_ARCH_X86_64", "SCMP_ARCH_AARCH64"],
            "syscalls": [
                {
                    "name": syscall,
                    "action": "SCMP_ACT_ALLOW"
                }
                for syscall in sorted(allowed_syscalls)
            ]
        }


class ProcessSandbox:
    """
    Process Sandbox Controller (ADR-006).
    """

    def __init__(self, manifest: CapabilityManifest):
        self.manifest = manifest
        self.seccomp_profile = SeccompProfileGenerator.generate_profile(manifest)

    def verify_isolation_policy(self) -> bool:
        # Enforce that unauthorized syscall access raises SIGSYS
        return self.seccomp_profile["defaultAction"] == "SCMP_ACT_KILL_PROCESS"
