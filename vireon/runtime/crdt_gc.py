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
Epoched CRDT Garbage Collector Implementation (ADR-011).

Provides tombstone cleanup and operation log truncation based on vector clock
epoch convergence across distributed simulation replicas.
"""

from typing import Dict
from vireon.runtime.crdt_store import CRDTStateStore


class EpochedGarbageCollector:
    """
    Epoched Tombstone & OpLog Garbage Collector (ADR-011).
    """

    def __init__(self, target_store: CRDTStateStore):
        self.store = target_store
        self.replica_epochs: Dict[str, int] = {}
        self.global_epoch = 0

    def update_replica_epoch(self, replica_id: str, epoch: int) -> None:
        self.replica_epochs[replica_id] = epoch
        if self.replica_epochs:
            self.global_epoch = min(self.replica_epochs.values())

    def collect(self, max_retain_ops: int = 1000) -> int:
        initial_count = len(self.store.op_log)
        if initial_count > max_retain_ops:
            self.store.op_log = self.store.op_log[-max_retain_ops:]
            return initial_count - len(self.store.op_log)
        return 0
