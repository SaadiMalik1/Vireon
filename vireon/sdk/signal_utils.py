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
Pure signal-processing utility functions for the VIREON SDK.

These are stateless functions with no dependencies on runtime
or provider internals — safe for use from any layer.
"""

import numpy as np
from typing import Any


def calculate_rms(signal: Any) -> float:
    """Calculates the Root Mean Square (RMS) of a 1D signal."""
    if len(signal) == 0:
        return 0.0
    return float(np.sqrt(np.mean(np.square(signal))))


def calculate_bandpower(signal: Any, sample_rate: int, band: tuple[float, float]) -> float:
    """
    Calculates the average power in a specific frequency band using FFT.
    Uses numpy FFT to avoid dependency on scipy.signal.
    """
    n = len(signal)
    if n == 0:
        return 0.0

    # Compute real FFT
    fft_vals = np.fft.rfft(signal)
    fft_freqs = np.fft.rfftfreq(n, 1.0 / sample_rate)

    # Power spectral density estimate
    psd = (np.abs(fft_vals) ** 2) / (sample_rate * n)

    # Find indices corresponding to the frequency band
    idx = (fft_freqs >= band[0]) & (fft_freqs <= band[1])
    if not np.any(idx):
        return 0.0

    return float(np.mean(psd[idx]))
