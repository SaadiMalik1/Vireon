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
gRPC Control Plane Service Implementation (ADR-002).

Manages provider registration, capability negotiation, lifecycle state transitions,
and RPC control signaling separated from high-throughput telemetry data planes.
"""

from enum import Enum
from typing import Dict, Any, Optional
from vireon.sdk.manifest import CapabilityManifest


class ProviderLifecycleState(str, Enum):
    REGISTERED = "REGISTERED"
    INITIALIZING = "INITIALIZING"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    FAILED = "FAILED"


class ControlPlaneServer:
    """
    Control Plane Server (ADR-002).
    Coordinates provider lifecycle signaling and capability registration.
    """

    def __init__(self, host: str = "127.0.0.1", port: int = 50051):
        self.host = host
        self.port = port
        self._providers: Dict[str, Dict[str, Any]] = {}

    def register_provider(self, provider_id: str, manifest: CapabilityManifest) -> bool:
        if provider_id in self._providers:
            return False

        self._providers[provider_id] = {
            "manifest": manifest,
            "state": ProviderLifecycleState.REGISTERED,
            "last_heartbeat": 0.0,
        }
        return True

    def transition_state(self, provider_id: str, new_state: ProviderLifecycleState) -> bool:
        if provider_id not in self._providers:
            return False
        self._providers[provider_id]["state"] = new_state
        return True

    def get_provider_state(self, provider_id: str) -> Optional[ProviderLifecycleState]:
        provider = self._providers.get(provider_id)
        return provider["state"] if provider else None

    def list_active_providers(self) -> Dict[str, str]:
        return {pid: data["state"].value for pid, data in self._providers.items()}
