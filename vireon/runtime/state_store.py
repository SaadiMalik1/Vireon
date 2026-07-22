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

import threading
import json
import zlib
from typing import Any, Dict, Optional
from vireon.sdk.events import IEventBus, Event
from vireon.sdk.state import IStateStore
from vireon.runtime.merkle import MerkleTree


class StateStore(IStateStore):
    """
    Central, thread-safe Key-Value store replacing the DigitalTwin God-class.
    All state mutations are broadcast over the EventBus.
    Integrates live Merkle tree accumulation (ADR-014) and FDA rolling CRC32 checksums (§18.10).
    """
    def __init__(self, event_bus: IEventBus, merkle_tree: Optional[MerkleTree] = None):
        self._state: Dict[str, Any] = {}
        self._lock = threading.RLock()
        self.event_bus = event_bus
        self.merkle_tree = merkle_tree

    def attach_merkle_tree(self, merkle_tree: MerkleTree) -> None:
        """Attaches a Merkle tree accumulator for live state verification."""
        with self._lock:
            self.merkle_tree = merkle_tree

    def get(self, key: str, default: Any = None) -> Any:
        with self._lock:
            return self._state.get(key, default)

    def set(self, key: str, value: Any, source: str = "system") -> None:
        with self._lock:
            old_value = self._state.get(key)
            if old_value != value:
                self._state[key] = value
                
                # Live Merkle tree leaf accumulation (ADR-014)
                if self.merkle_tree is not None:
                    payload = json.dumps({"key": key, "val": str(value), "src": source}, sort_keys=True).encode("utf-8")
                    self.merkle_tree.add_leaf(payload)

                self.event_bus.publish(Event(
                    topic=f"state.changed.{key}",
                    data={"old": old_value, "new": value},
                    source=source
                ))

    def get_all(self) -> Dict[str, Any]:
        with self._lock:
            return dict(self._state)

    def get_state_checksum(self) -> str:
        """Computes rolling CRC32 checksum over canonical sorted state representation (§18.10)."""
        with self._lock:
            canonical = json.dumps(self._state, sort_keys=True, default=str).encode("utf-8")
            crc32_val = zlib.crc32(canonical) & 0xFFFFFFFF
            return f"{crc32_val:08x}"

