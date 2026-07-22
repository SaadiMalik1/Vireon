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
Exhaustive Phase 3 Multi-Seed Bit-Identical Determinism & Replay Proof Suite.
"""

import json
import hashlib
from typing import Dict, List
from vireon.runtime.rng import DeterministicRNG
from vireon.runtime.clock import DeterministicClock, ClockMode
from vireon.runtime.event_bus import EventBus
from vireon.runtime.state_store import StateStore


def run_simulation_stream(seed: int = 42, steps: int = 500) -> Dict[str, str]:
    """
    Executes a multi-channel deterministic simulation tick loop and 
    returns SHA-256 state hashes and final rolling CRC32 checksums.
    """
    clock = DeterministicClock(mode=ClockMode.VIRTUAL, step_dt_ms=4.0)
    rng = DeterministicRNG(seed=seed)
    bus = EventBus()
    store = StateStore(bus)

    history: List[tuple] = []
    for step in range(steps):
        clock.advance()
        val_ch0 = rng.normal(loc=0.0, scale=1.0)
        val_ch1 = rng.uniform(low=-10.0, high=10.0)
        store.set(f"signal_ch0", float(val_ch0))
        store.set(f"signal_ch1", float(val_ch1))
        
        state_crc = store.get_state_checksum()
        history.append((step, clock.sim_time, val_ch0, val_ch1, state_crc))

    canonical_bytes = json.dumps(history, sort_keys=True).encode("utf-8")
    full_sha = hashlib.sha256(canonical_bytes).hexdigest()
    final_crc = store.get_state_checksum()

    return {
        "seed": seed,
        "steps": steps,
        "sha256_hash": full_sha,
        "final_crc32_hex": final_crc
    }


def test_bit_identical_replay_reproducibility_across_seeds():
    """Proves Phase 3 requirement: Bit-identical state hash reproduction for seeds 42, 1337, 9999."""
    seeds_to_test = [42, 100, 777, 1337, 9999]
    report_data = {}

    for seed in seeds_to_test:
        baseline = run_simulation_stream(seed=seed, steps=300)
        report_data[f"seed_{seed}"] = baseline

        # Repeat 5 trials per seed to verify 100% bit-identical output
        for trial in range(5):
            trial_res = run_simulation_stream(seed=seed, steps=300)
            assert trial_res["sha256_hash"] == baseline["sha256_hash"], (
                f"Determinism drift detected for seed {seed} on trial {trial + 1}"
            )
            assert trial_res["final_crc32_hex"] == baseline["final_crc32_hex"], (
                f"CRC32 checksum drift detected for seed {seed} on trial {trial + 1}"
            )

    # Save determinism_report.json
    with open("determinism_report.json", "w", encoding="utf-8") as f:
        json.dump(report_data, f, indent=2)


def test_rng_reseed_identity():
    rng1 = DeterministicRNG(seed=8888)
    seq1 = [rng1.uniform() for _ in range(100)]

    rng2 = DeterministicRNG(seed=8888)
    seq2 = [rng2.uniform() for _ in range(100)]

    assert seq1 == seq2
