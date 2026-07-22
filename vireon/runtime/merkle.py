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
Merkle Tree Cryptographic Tracing Implementation (ADR-014).

Computes cryptographic Merkle tree accumulators over simulation state transitions
enabling O(log N) inclusion proof verification for audit evidence bundles.
"""

import hashlib
from typing import List, Optional


class MerkleTree:
    """
    Merkle Tree Accumulator (ADR-014).
    """

    def __init__(self, leaves: Optional[List[bytes]] = None):
        self.leaves: List[bytes] = [self._hash(leaf) for leaf in (leaves or [])]
        self.tree: List[List[bytes]] = []
        if self.leaves:
            self._build_tree()

    @staticmethod
    def _hash(data: bytes) -> bytes:
        return hashlib.sha256(data).digest()

    def add_leaf(self, data: bytes) -> None:
        self.leaves.append(self._hash(data))
        self._build_tree()

    def _build_tree(self) -> None:
        if not self.leaves:
            self.tree = []
            return

        current_level = self.leaves
        self.tree = [current_level]

        while len(current_level) > 1:
            next_level = []
            for i in range(0, len(current_level), 2):
                left = current_level[i]
                right = current_level[i + 1] if i + 1 < len(current_level) else left
                combined = self._hash(left + right)
                next_level.append(combined)
            current_level = next_level
            self.tree.append(current_level)

    def get_root(self) -> Optional[bytes]:
        if not self.tree or not self.tree[-1]:
            return None
        return self.tree[-1][0]

    def get_root_hex(self) -> str:
        root = self.get_root()
        return root.hex() if root else ""
