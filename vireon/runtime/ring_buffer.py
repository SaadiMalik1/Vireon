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
Non-Blocking Lockless Ring Buffer Implementation (ADR-015).

Provides single-producer single-consumer (SPSC) lock-free ring buffer for
high-frequency telemetry frame streaming (30kHz+ sample ingestion).
"""

import threading
from typing import Generic, TypeVar, Optional, List

T = TypeVar("T")


class SPSCRingBuffer(Generic[T]):
    """
    Thread-Safe Single-Producer Single-Consumer Ring Buffer (ADR-015).
    """

    def __init__(self, capacity: int = 1024):
        self.capacity = capacity
        self._buffer: List[Optional[T]] = [None] * capacity
        self._head = 0  # Write pointer
        self._tail = 0  # Read pointer
        self.dropped_samples = 0
        self._lock = threading.Lock()

    def push(self, item: T) -> bool:
        with self._lock:
            next_head = (self._head + 1) % self.capacity
            if next_head == self._tail:
                # Overwrite oldest sample on buffer overflow to protect producer lock-freedom
                self._tail = (self._tail + 1) % self.capacity
                self.dropped_samples += 1

            self._buffer[self._head] = item
            self._head = next_head
            return True

    def pop(self) -> Optional[T]:
        with self._lock:
            if self._head == self._tail:
                return None  # Empty buffer

            item = self._buffer[self._tail]
            self._buffer[self._tail] = None
            self._tail = (self._tail + 1) % self.capacity
            return item

    def is_empty(self) -> bool:
        with self._lock:
            return self._head == self._tail

    def size(self) -> int:
        with self._lock:
            if self._head >= self._tail:
                return self._head - self._tail
            return self.capacity - (self._tail - self._head)
