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
import numpy as np
from typing import List, Optional
from vireon.runtime.twin import DigitalTwin


class ISignalModifier(ABC):
    @abstractmethod
    def apply(self, data: np.ndarray, eeg_channels: List[int], sample_rate: int, twin: DigitalTwin, rng: Optional[np.random.Generator] = None) -> np.ndarray:
        """
        Mutates the incoming signal window and registers impacts
        on the DigitalTwin state (e.g. impedance changes, disconnection).
        """
        pass

    def revert(self, twin: DigitalTwin) -> None:
        """
        Reverts any persistent state changes made to the DigitalTwin when 
        the modifier is removed. Base implementation does nothing.
        """
        pass

