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
Hardware Watchdog Implementation (ADR-010).

Monitors provider execution tick deadlines and triggers fail-safe hardware shutdown
upon stall or timing deadline overrun.
"""

import time
from typing import Callable, Optional


class HardwareWatchdog:
    """
    Hardware Execution Watchdog (ADR-010).
    """

    def __init__(self, timeout_sec: float = 1.0, on_stall_callback: Optional[Callable[[], None]] = None):
        self.timeout_sec = timeout_sec
        self.on_stall_callback = on_stall_callback
        self.last_heartbeat = time.monotonic()
        self.stalled = False

    def kick(self) -> None:
        self.last_heartbeat = time.monotonic()
        self.stalled = False

    def check(self) -> bool:
        elapsed = time.monotonic() - self.last_heartbeat
        if elapsed > self.timeout_sec:
            self.stalled = True
            if self.on_stall_callback:
                self.on_stall_callback()
            return False
        return True
