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

from typing import Any, Dict
from abc import ABC, abstractmethod
from vireon.sdk.events import IEventBus

class IStateStore(ABC):
    """Interface for the central State Store."""
    event_bus: IEventBus
    
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        pass

    @abstractmethod
    def set(self, key: str, value: Any, source: str = "system") -> None:
        pass

    @abstractmethod
    def get_all(self) -> Dict[str, Any]:
        pass
