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
Unidirectional Memory Protection Implementation (ADR-012).

Enforces read-only memory view boundaries for untrusted providers to prevent state mutation
tampering across FFI/IPC shared memory segments.
"""

import numpy as np


class UnidirectionalMemoryGuard:
    """
    Unidirectional Memory Protection Boundary (ADR-012).
    """

    @staticmethod
    def wrap_readonly(array: np.ndarray) -> np.ndarray:
        view = array.view()
        view.flags.writeable = False
        return view

    @staticmethod
    def verify_read_only(array: np.ndarray) -> bool:
        return not array.flags.writeable
