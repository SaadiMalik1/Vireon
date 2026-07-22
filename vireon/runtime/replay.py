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
Deterministic Replay Engine Implementation (ADR-004).

Records state transition sequences, clock ticks, and telemetry outputs
and validates strict execution reproducibility across identical seed runs.
"""

from dataclasses import dataclass, field
import hashlib
import json
from typing import List, Dict, Any


@dataclass
class ReplayTrace:
    seed: int
    ticks: int
    state_transitions: List[Dict[str, Any]] = field(default_factory=list)
    events_published: List[Dict[str, Any]] = field(default_factory=list)

    def compute_hash(self) -> str:
        data = {
            "seed": self.seed,
            "ticks": self.ticks,
            "state_transitions": self.state_transitions,
            "events": self.events_published,
        }
        encoded = json.dumps(data, sort_keys=True).encode("utf-8")
        return hashlib.sha256(encoded).hexdigest()


class ReplayEngine:
    """
    Deterministic Replay & Trace Verification Engine (ADR-004).
    """

    def __init__(self, seed: int = 42):
        self.seed = seed
        self.trace = ReplayTrace(seed=seed, ticks=0)

    def record_tick(self, tick: int, state: Dict[str, Any]) -> None:
        self.trace.ticks = tick
        self.trace.state_transitions.append({"tick": tick, "state": state})

    def record_event(self, topic: str, payload: Dict[str, Any]) -> None:
        self.trace.events_published.append({"topic": topic, "payload": payload})

    def export_trace(self) -> ReplayTrace:
        return self.trace

    @staticmethod
    def verify_reproducibility(trace1: ReplayTrace, trace2: ReplayTrace) -> bool:
        return trace1.compute_hash() == trace2.compute_hash()
