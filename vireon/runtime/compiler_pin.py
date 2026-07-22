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
Compiler Pinned Determinism Implementation (ADR-013).

Provides environment hash validation (Python version, NumPy version, OS platform,
architecture) to guarantee deterministic binary bytecode compilation and execution.
"""

import hashlib
import platform
import sys
import numpy as np


class CompilerPin:
    """
    Compiler Pin Determinism Verifier (ADR-013).
    Ensures environment state matches expectations for binary reproducibility.
    """

    @staticmethod
    def get_environment_descriptor() -> dict:
        return {
            "python_version": sys.version.split()[0],
            "numpy_version": np.__version__,
            "platform": sys.platform,
            "architecture": platform.machine(),
            "processor": platform.processor(),
        }

    @classmethod
    def compute_pin_hash(cls) -> str:
        desc = cls.get_environment_descriptor()
        raw_repr = f"{desc['python_version']}:{desc['numpy_version']}:{desc['platform']}:{desc['architecture']}"
        return hashlib.sha256(raw_repr.encode("utf-8")).hexdigest()

    @classmethod
    def verify_pin(cls, expected_hash: str) -> bool:
        current_hash = cls.compute_pin_hash()
        return current_hash == expected_hash
