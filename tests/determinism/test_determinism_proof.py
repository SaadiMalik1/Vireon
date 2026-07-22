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
Phase 3 Determinism Validation & Bit-Identical Replay Suite.
"""

import json
import hashlib
import numpy as np
from vireon.runtime.rng import DeterministicRNG
from vireon.runtime.clock import DeterministicClock, ClockMode
from vireon.runtime.event_bus import EventBus, Event
from vireon.runtime.state_store import StateStore


def run_single_simulation_stream(seed: int = 42, steps: int = 100) -> str:
    """Executes a synthetic simulation run and returns SHA-256 state hash."""
    clock = DeterministicClock(mode=ClockMode.VIRTUAL, step_dt_ms=4.0)
    rng = DeterministicRNG(seed=seed)
    bus = EventBus()
    store = StateStore(bus)

    history = []
    for _ in range(steps):
        clock.advance()
        val = rng.normal(loc=0.0, scale=1.0)
        store.set("signal", float(val))
        history.append((clock.sim_time, val, store.get_state_checksum()))

    canonical_bytes = json.dumps(history, sort_keys=True).encode("utf-8")
    return hashlib.sha256(canonical_bytes).hexdigest()


def test_bit_identical_replay_reproducibility():
    """Proves Phase 3 requirement: Same seed & steps produce bit-identical state hashes across 10 runs."""
    baseline_hash = run_single_simulation_stream(seed=1337, steps=250)

    for run_idx in range(9):
        current_hash = run_single_simulation_stream(seed=1337, steps=250)
        assert current_hash == baseline_hash, f"Determinism failure on replay run {run_idx + 1}"


def test_rng_reseed_identity():
    rng1 = DeterministicRNG(seed=999)
    seq1 = [rng1.uniform() for _ in range(50)]

    rng2 = DeterministicRNG(seed=999)
    seq2 = [rng2.uniform() for _ in range(50)]

    assert seq1 == seq2
