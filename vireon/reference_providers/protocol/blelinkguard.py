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

from typing import Optional
import threading

from vireon.sdk.events import Event
from vireon.sdk.state import IStateStore

class BLEConstants:
    MIN_MTU_SIZE = 23
    MAX_MTU_SIZE = 512
    JAMMING_DROP_RATE_THRESHOLD = 0.3

class BLELinkGuard:
    """
    BLE Link Layer Guard.
    Prevents link-level boundary abuses and illegal MTU negotiations.
    """

    def __init__(self, state_store: IStateStore, event_bus: Optional[EventBus] = None):
        self.state_store = state_store
        self.event_bus = event_bus
        self.blocked_mtu_abuses = 0
        self.jamming_alerts = 0
        self.blocked_spoofing_attempts = 0
        self._lock = threading.RLock()

    def verify_connection(self, client_mac: str, is_paired: bool, bonding_db: dict) -> bool:
        with self._lock:
            return self._verify_connection(client_mac, is_paired, bonding_db)

    def _verify_connection(self, client_mac: str, is_paired: bool, bonding_db: dict) -> bool:
        """
        Defends against BLESA (BLE Spoofing Attack).
        Requires devices with known MAC addresses to prove they possess the IRK/LTK (via is_paired).
        If a device MAC is in bonding_db but is_paired is False, it's a spoofing attempt.
        """
        if client_mac in bonding_db:
            if not is_paired:
                self.blocked_spoofing_attempts += 1
                self.state_store.set("clinical_alert_active", True, "link_guard"); self.state_store.set("clinical_status", f"BLE Link Guard: Blocked Spoofing (BLESA) from {client_mac}", "link_guard")
                if self.event_bus:
                    self.event_bus.publish(Event(
                        topic="link_guard.spoofing_blocked",
                        data={"mac": client_mac, "sim_clock": self.state_store.get("sim_clock", 0.0)},
                        source="link_guard"
                    ))
                return False
        return True

    def check_rf_environment(self):
        with self._lock:
            return self._check_rf_environment()

    def _check_rf_environment(self):
        drop_rate = self.state_store.get("rf_packet_drop_rate", 0.0)
        # If dropping more than 30% of packets, trigger RF Jamming Alert
        if drop_rate >= BLEConstants.JAMMING_DROP_RATE_THRESHOLD:
            self.jamming_alerts += 1
            self.state_store.set("clinical_alert_active", True, "link_guard"); self.state_store.set("clinical_status", f"BLE Link Guard: Severe RF Jamming Detected ({drop_rate*100:.0f}% drops)", "link_guard")
            if self.event_bus:
                self.event_bus.publish(Event(
                    topic="link_guard.jamming_detected",
                    data={"drop_rate": drop_rate, "sim_clock": self.state_store.get("sim_clock", 0.0)},
                    source="link_guard"
                ))

    def verify_mtu(self, requested_mtu: int) -> int:
        with self._lock:
            return self._verify_mtu(requested_mtu)

    def _verify_mtu(self, requested_mtu: int) -> int:
        # BLE specification minimum MTU size is 23 bytes, maximum is 512 bytes (BLE 5.2)
        if requested_mtu < BLEConstants.MIN_MTU_SIZE or requested_mtu > BLEConstants.MAX_MTU_SIZE:
            self.blocked_mtu_abuses += 1
            self.state_store.set("clinical_alert_active", True, "link_guard"); self.state_store.set("clinical_status", "BLE Link Guard: Blocked MTU Abuse", "link_guard")

            if self.event_bus:
                self.event_bus.publish(Event(
                    topic="link_guard.mtu_abuse_blocked",
                    data={
                        "requested_mtu": requested_mtu,
                        "enforced_mtu": BLEConstants.MIN_MTU_SIZE,
                        "sim_clock": self.state_store.get("sim_clock", 0.0)
                    },
                    source="link_guard"
                ))

            # Enforce spec limits
            return max(BLEConstants.MIN_MTU_SIZE, min(requested_mtu, BLEConstants.MAX_MTU_SIZE))
        return requested_mtu
