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

import os
import hashlib
from typing import List, Optional, Tuple


class MerkleTree:
    """
    Merkle Tree Accumulator (ADR-014).
    """

    def __init__(self, leaves: Optional[List[bytes]] = None, log_file: Optional[str] = None):
        self.log_file = log_file
        self.leaves: List[bytes] = []
        self.tree: List[List[bytes]] = []
        
        # Load from persistence if available
        self._load_from_log()
        
        # Add any explicitly passed leaves
        if leaves:
            for leaf in leaves:
                self._add_leaf_internal(leaf)
        
        if self.leaves:
            self._build_tree()

    def _load_from_log(self) -> None:
        if self.log_file and os.path.exists(self.log_file):
            with open(self.log_file, "r") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        self.leaves.append(bytes.fromhex(line))

    def _append_to_log(self, leaf_hash: bytes) -> None:
        if self.log_file:
            with open(self.log_file, "a") as f:
                f.write(leaf_hash.hex() + "\n")

    @staticmethod
    def _hash_leaf(data: bytes) -> bytes:
        # Prefix 0x00 for leaves to prevent second-preimage attacks
        return hashlib.sha256(b"\x00" + data).digest()

    @staticmethod
    def _hash_node(left: bytes, right: bytes) -> bytes:
        # Prefix 0x01 for internal nodes to prevent second-preimage attacks
        return hashlib.sha256(b"\x01" + left + right).digest()

    def _add_leaf_internal(self, data: bytes) -> None:
        leaf_hash = self._hash_leaf(data)
        self.leaves.append(leaf_hash)
        self._append_to_log(leaf_hash)

    def add_leaf(self, data: bytes) -> None:
        self._add_leaf_internal(data)
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
                combined = self._hash_node(left, right)
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

    def get_proof(self, index: int) -> List[Tuple[str, bytes]]:
        """
        Get the inclusion proof for a leaf at the specified index.
        Returns a list of (direction, sibling_hash) tuples.
        """
        if index < 0 or index >= len(self.leaves):
            raise ValueError("Index out of bounds")

        proof = []
        for level in self.tree[:-1]: # exclude the root level
            is_right_node = index % 2 == 1
            if is_right_node:
                sibling_index = index - 1
                direction = "left"
            else:
                sibling_index = index + 1
                direction = "right"

            if sibling_index < len(level):
                proof.append((direction, level[sibling_index]))
            else:
                # If there is no sibling, the node is duplicated
                proof.append((direction, level[index]))
            
            index //= 2

        return proof

    @classmethod
    def verify_proof(cls, leaf: bytes, proof: List[Tuple[str, bytes]], root: bytes) -> bool:
        """
        Verify an inclusion proof.
        """
        current_hash = cls._hash_leaf(leaf)
        for direction, sibling_hash in proof:
            if direction == "left":
                current_hash = cls._hash_node(sibling_hash, current_hash)
            else:
                current_hash = cls._hash_node(current_hash, sibling_hash)
        
        return current_hash == root
