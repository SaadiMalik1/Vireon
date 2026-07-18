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

import numpy as np

def calculate_rms(signal: np.ndarray) -> float:
    """Calculates the Root Mean Square (RMS) of a 1D signal."""
    if len(signal) == 0:
        return 0.0
    return float(np.sqrt(np.mean(np.square(signal))))

def calculate_bandpower(signal: np.ndarray, sample_rate: int, band: tuple[float, float]) -> float:
    """
    Calculates the average power in a specific frequency band using FFT.
    Uses numpy FFT to avoid dependency on scipy.signal.
    """
    n = len(signal)
    if n == 0:
        return 0.0
    
    fft_vals = np.fft.rfft(signal)
    fft_freqs = np.fft.rfftfreq(n, 1.0 / sample_rate)
    
    psd = (np.abs(fft_vals) ** 2) / (sample_rate * n)
    
    idx = (fft_freqs >= band[0]) & (fft_freqs <= band[1])
    if not np.any(idx):
        return 0.0
        
    return float(np.mean(psd[idx]))
