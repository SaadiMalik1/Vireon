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
Zero-Copy Shared Memory Implementation (ADR-007).

Provides zero-copy memory pointer handoff across host process boundaries using
Python multiprocessing.shared_memory for 30kHz+ high-throughput telemetry streams.
"""

from multiprocessing import shared_memory
import numpy as np


class SharedMemoryBuffer:
    """
    Zero-Copy Shared Memory Pointer Handoff (ADR-007).
    """

    def __init__(self, name: str, size_bytes: int, create: bool = True):
        self.name = name
        self.size_bytes = size_bytes
        self.create = create
        if create:
            self._shm = shared_memory.SharedMemory(name=name, create=True, size=size_bytes)
        else:
            self._shm = shared_memory.SharedMemory(name=name, create=False)

    def write_array(self, array: np.ndarray, offset: int = 0) -> int:
        assert self._shm.buf is not None
        buf_view = np.ndarray(array.shape, dtype=array.dtype, buffer=self._shm.buf[offset:])
        buf_view[...] = array[...]
        return array.nbytes

    def read_array(self, shape: tuple, dtype: np.dtype, offset: int = 0) -> np.ndarray:
        assert self._shm.buf is not None
        return np.ndarray(shape, dtype=dtype, buffer=self._shm.buf[offset:])


    def close(self) -> None:
        self._shm.close()

    def unlink(self) -> None:
        if self.create:
            try:
                self._shm.unlink()
            except FileNotFoundError:
                pass
