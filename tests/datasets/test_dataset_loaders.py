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
Unit Tests for File-based Dataset Readers (NPZ, CSV, EDF).
"""

import os
import pytest
import numpy as np
from vireon.datasets import NPZDatasetReader, CSVDatasetReader, EDFDatasetReader


def test_npz_dataset_reader(tmp_path):
    npz_file = tmp_path / "sample_data.npz"
    dummy_x = np.random.randn(100, 8).astype(np.float32)
    dummy_y = np.random.randint(0, 2, size=100)
    np.savez(npz_file, x=dummy_x, y=dummy_y)

    reader = NPZDatasetReader(str(npz_file))
    assert reader.num_samples == 100
    assert reader.num_channels == 8

    chunk = reader.read_chunk(0, 50)
    assert chunk.shape == (50, 8)
    assert np.allclose(chunk, dummy_x[:50, :])

    chunk_end = reader.read_chunk(100, 50)
    assert chunk_end is None


def test_csv_dataset_reader(tmp_path):
    csv_file = tmp_path / "sample_telemetry.csv"
    data = np.arange(20, dtype=np.float32).reshape(10, 2)
    header = "ch1,ch2\n"
    with open(csv_file, "w") as f:
        f.write(header)
        np.savetxt(f, data, delimiter=",")

    reader = CSVDatasetReader(str(csv_file), delimiter=",", skip_header=1)
    assert reader.num_samples == 10
    assert reader.num_channels == 2

    chunk = reader.read_chunk(0, 5)
    assert chunk.shape == (5, 2)
    assert np.allclose(chunk, data[:5, :])


def test_edf_dataset_reader(tmp_path):
    edf_file = tmp_path / "dummy_record.edf"
    # Construct minimal 256-byte header + signal header
    header_str = "0       " + "PATIENT ".ljust(80) + "RECORDING ".ljust(80) + "01.01.26" + "12.00.00" + "512     " + " ".ljust(44) + "1       " + "1.0     " + "2   "
    header_bytes = header_str.encode("ascii").ljust(256)

    # Signal header: 2 signals -> 2 * 256 = 512 bytes total signal headers
    sig_labels = "EEG Ch1         EEG Ch2         ".encode("ascii").ljust(32)
    sig_headers = sig_labels.ljust(512 - 256)

    data_samples = np.array([100, 200, 300, 400, 500, 600], dtype=np.int16).tobytes()

    with open(edf_file, "wb") as f:
        f.write(header_bytes)
        f.write(sig_headers)
        f.write(data_samples)

    reader = EDFDatasetReader(str(edf_file))
    assert reader.header["version"] == "0"
    assert reader.num_channels == 2
    assert reader.num_samples == 3
    chunk = reader.read_chunk(0, 2)
    assert chunk is not None
    assert chunk.shape == (2, 2)
