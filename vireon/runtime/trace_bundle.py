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
Signed Trace Bundle Implementation (ADR-014).

Packages simulation Merkle root, Ed25519 signatures, environment hashes, and provider
metadata into verifiable regulatory trace packages.
"""

from dataclasses import dataclass, field
import json
from typing import Dict, Any, Optional
from cryptography.hazmat.primitives.asymmetric import ed25519


@dataclass
class TraceBundle:
    """
    Signed Regulatory Evidence Trace Bundle (ADR-014).
    """

    merkle_root_hex: str
    pin_hash: str
    metadata: Dict[str, Any] = field(default_factory=dict)
    signature_bytes: Optional[bytes] = None

    def canonical_bytes(self) -> bytes:
        data = {
            "merkle_root": self.merkle_root_hex,
            "pin_hash": self.pin_hash,
            "metadata": self.metadata,
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
