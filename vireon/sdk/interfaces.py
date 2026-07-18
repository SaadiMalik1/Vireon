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

from abc import ABC, abstractmethod
from typing import Any
from vireon.sdk.manifest import CapabilityManifest

class OrchestratorContext:
    """Proxy object given to providers during initialization."""
    def __init__(self, event_bus: Any, state_store: Any):
        self.event_bus = event_bus
        self.state_store = state_store

class IProvider(ABC):
    @property
    @abstractmethod
    def manifest(self) -> CapabilityManifest:
        """Returns the capabilities required by this provider."""
        pass
        
    @abstractmethod
    def initialize(self, context: OrchestratorContext) -> None:
        """Called by the Orchestrator after capabilities are resolved."""
        pass
        
    def on_tick(self, sim_clock: float, dt: float) -> None:
        """Called every simulation tick if the provider subscribes to time."""
        pass
        
    def shutdown(self) -> None:
        """Called during graceful shutdown."""
        pass

class IFirmwareProvider(IProvider):
    @abstractmethod
    def write_memory(self, address: int, data: bytes) -> bool:
        pass
        
    @abstractmethod
    def read_memory(self, address: int, size: int) -> bytes:
        pass
