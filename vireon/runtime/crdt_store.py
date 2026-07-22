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
Conflict-Free Replicated Data Type (CRDT) State Store Implementation (ADR-008).

Provides lock-free distributed state graph convergence via GCounter and LWWRegister
data types and operation-based log replication.
"""

from dataclasses import dataclass, field
import time
from typing import Dict, Any, List, Optional


@dataclass
class GCounter:
    """Grow-Only Counter CRDT."""
    counts: Dict[str, int] = field(default_factory=dict)

    def increment(self, replica_id: str, value: int = 1) -> None:
        self.counts[replica_id] = self.counts.get(replica_id, 0) + value

    def value(self) -> int:
        return sum(self.counts.values())

    def merge(self, other: "GCounter") -> None:
        for replica_id, count in other.counts.items():
            self.counts[replica_id] = max(self.counts.get(replica_id, 0), count)


@dataclass
class LWWRegister:
    """Last-Write-Wins Register CRDT."""
    val: Any = None
    timestamp: float = 0.0

    def assign(self, val: Any, timestamp: Optional[float] = None) -> None:
        ts = timestamp if timestamp is not None else time.time()
        if ts >= self.timestamp:
            self.val = val
            self.timestamp = ts

    def merge(self, other: "LWWRegister") -> None:
        if other.timestamp >= self.timestamp:
            self.val = other.val
            self.timestamp = other.timestamp


class CRDTStateStore:
    """
    CRDT State Store (ADR-008).
    Backed by operation logs and LWWRegister/GCounter state views.
    """

    def __init__(self, replica_id: str = "node_0"):
        self.replica_id = replica_id
        self._registers: Dict[str, LWWRegister] = {}
        self._counters: Dict[str, GCounter] = {}
        self.op_log: List[Dict[str, Any]] = []

    def set_register(self, key: str, value: Any, timestamp: Optional[float] = None) -> None:
        if key not in self._registers:
            self._registers[key] = LWWRegister()
        reg = self._registers[key]
        reg.assign(value, timestamp)
        self.op_log.append({
            "op": "set_register",
            "key": key,
            "val": value,
            "ts": reg.timestamp,
            "replica": self.replica_id
        })

    def get_register(self, key: str) -> Any:
        reg = self._registers.get(key)
        return reg.val if reg else None

    def increment_counter(self, key: str, value: int = 1) -> None:
        if key not in self._counters:
            self._counters[key] = GCounter()
        self._counters[key].increment(self.replica_id, value)
        self.op_log.append({
            "op": "inc_counter",
            "key": key,
            "val": value,
            "replica": self.replica_id
        })

    def get_counter(self, key: str) -> int:
        counter = self._counters.get(key)
        return counter.value() if counter else 0

    def merge(self, other: "CRDTStateStore") -> None:
        for k, reg in other._registers.items():
            if k not in self._registers:
                self._registers[k] = LWWRegister()
            self._registers[k].merge(reg)

        for k, counter in other._counters.items():
            if k not in self._counters:
                self._counters[k] = GCounter()
            self._counters[k].merge(counter)
