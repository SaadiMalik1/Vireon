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
Signed Capability Manifest Implementation (ADR-003).

Enforces cryptography-backed Ed25519 digital signature validation for provider
capability descriptors to prevent tampered or unauthorized plugin loading.
"""

from dataclasses import dataclass, field
import json
from typing import List, Optional
from cryptography.hazmat.primitives.asymmetric import ed25519


@dataclass
class CapabilityManifest:
    """
    Capability Manifest Descriptor (ADR-003).
    Includes Ed25519 signature fields for zero-trust authorization.
    """

    name: str
    version: str
    category: str
    publishes_events: List[str] = field(default_factory=list)
    subscribes_events: List[str] = field(default_factory=list)
    mutates_state: List[str] = field(default_factory=list)
    reads_state: List[str] = field(default_factory=list)
    requires_host_access: bool = False
    signature_bytes: Optional[bytes] = None

    def canonical_bytes(self) -> bytes:
        data = {
            "name": self.name,
            "version": self.version,
            "category": self.category,
            "publishes_events": sorted(self.publishes_events),
            "subscribes_events": sorted(self.subscribes_events),
            "mutates_state": sorted(self.mutates_state),
            "reads_state": sorted(self.reads_state),
            "requires_host_access": self.requires_host_access,
        }
        return json.dumps(data, sort_keys=True).encode("utf-8")

    def sign(self, private_key: ed25519.Ed25519PrivateKey) -> bytes:
        payload = self.canonical_bytes()
        self.signature_bytes = private_key.sign(payload)
        return self.signature_bytes

    def verify_signature(self, public_key: ed25519.Ed25519PublicKey) -> bool:
        if self.signature_bytes is None:
            return False
        try:
            public_key.verify(self.signature_bytes, self.canonical_bytes())
            return True
        except Exception:
            return False
