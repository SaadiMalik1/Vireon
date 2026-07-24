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
File-based Dataset Readers for NPZ, CSV, and EDF/BDF Biopotential Recordings.
"""

import os
from typing import Dict, Any, Optional
import numpy as np


class NPZDatasetReader:
    """
    Reader for pre-recorded NumPy `.npz` dataset files containing multi-channel telemetry.
    """

    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"NPZ dataset file not found: {file_path}")
        self.file_path = file_path
        self._load_data()

    def _load_data(self):
        npz = np.load(self.file_path)
        if "x" in npz:
            self.data = npz["x"]
        elif "data" in npz:
            self.data = npz["data"]
        else:
            first_key = list(npz.keys())[0]
            self.data = npz[first_key]

        self.labels = npz.get("y", npz.get("labels", None))
        self.num_samples = self.data.shape[0] if self.data.ndim > 1 else len(self.data)
        self.num_channels = self.data.shape[1] if self.data.ndim > 1 else 1

    def read_chunk(self, start_sample: int, num_samples: int) -> Optional[np.ndarray]:
        """Reads a chunk of samples starting from start_sample."""
        if start_sample >= self.num_samples:
            return None
        end_sample = min(start_sample + num_samples, self.num_samples)
        if self.data.ndim == 1:
            return self.data[start_sample:end_sample].reshape(-1, 1)
        return self.data[start_sample:end_sample, :]


class CSVDatasetReader:
    """
    Reader for CSV multi-channel time-series dataset files.
    """

    def __init__(self, file_path: str, delimiter: str = ",", skip_header: int = 1):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"CSV dataset file not found: {file_path}")
        self.file_path = file_path
        self.delimiter = delimiter
        self.skip_header = skip_header
        self._load_data()

    def _load_data(self):
        self.data = np.loadtxt(self.file_path, delimiter=self.delimiter, skiprows=self.skip_header, dtype=np.float32)
        if self.data.ndim == 1:
            self.data = self.data.reshape(-1, 1)
        self.num_samples, self.num_channels = self.data.shape

    def read_chunk(self, start_sample: int, num_samples: int) -> Optional[np.ndarray]:
        """Reads a chunk of samples starting from start_sample."""
        if start_sample >= self.num_samples:
            return None
        end_sample = min(start_sample + num_samples, self.num_samples)
        return self.data[start_sample:end_sample, :]


class EDFDatasetReader:
    """
    Reader for European Data Format (.edf / .bdf) physiological signal recording files.
    Includes pure Python header parsing for standard EDF files.
    """

    def __init__(self, file_path: str):
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"EDF dataset file not found: {file_path}")
        self.file_path = file_path
        self.header: Dict[str, Any] = {}
        self.data: Optional[np.ndarray] = None
        self._parse_edf()

    def _parse_edf(self):
        """Parses standard EDF 256-byte main header and signal headers."""
        with open(self.file_path, "rb") as f:
            header_bytes = f.read(256)
            if len(header_bytes) < 256:
                raise ValueError("Invalid EDF file: header too short.")

            self.header["version"] = header_bytes[0:8].decode("ascii").strip()
            self.header["patient_id"] = header_bytes[8:88].decode("ascii").strip()
            self.header["recording_id"] = header_bytes[88:168].decode("ascii").strip()
            self.header["startdate"] = header_bytes[168:176].decode("ascii").strip()
            self.header["starttime"] = header_bytes[176:184].decode("ascii").strip()
            num_header_bytes = int(header_bytes[184:192].decode("ascii").strip())
            num_records = int(header_bytes[236:244].decode("ascii").strip())
            record_duration = float(header_bytes[244:252].decode("ascii").strip())
            num_signals = int(header_bytes[252:256].decode("ascii").strip())

            self.header["num_records"] = num_records
            self.header["record_duration"] = record_duration
            self.header["num_signals"] = num_signals

            # Read signal headers
            sig_headers_bytes = f.read(num_header_bytes - 256)
            labels = [sig_headers_bytes[i*16:(i+1)*16].decode("ascii").strip() for i in range(num_signals)]
            self.header["labels"] = labels

            # Read binary raw signal data (int16 per sample)
            raw_bytes = f.read()
            if len(raw_bytes) > 0:
                raw_int16 = np.frombuffer(raw_bytes, dtype=np.int16)
                num_samples = len(raw_int16) // max(1, num_signals)
                self.data = raw_int16[:num_samples * num_signals].reshape(-1, num_signals).astype(np.float32)
                self.num_samples = num_samples
                self.num_channels = num_signals
            else:
                self.data = np.zeros((0, num_signals), dtype=np.float32)
                self.num_samples = 0
                self.num_channels = num_signals

    def read_chunk(self, start_sample: int, num_samples: int) -> Optional[np.ndarray]:
        """Reads a chunk of samples starting from start_sample."""
        if self.data is None or start_sample >= self.num_samples:
            return None
        end_sample = min(start_sample + num_samples, self.num_samples)
        return self.data[start_sample:end_sample, :]
