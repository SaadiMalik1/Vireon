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

from vireon.runtime.twin import DigitalTwin
from vireon.runtime.clock import DeterministicClock, ClockMode, BifurcatedScheduler
from vireon.runtime.rng import DeterministicRNG
from vireon.runtime.compiler_pin import CompilerPin


def test_deterministic_clock_advancement():
    """Verify that SimClock advances deterministically tick-by-tick."""
    twin1 = DigitalTwin(device_id="test_device_1", sample_rate=250)
    twin2 = DigitalTwin(device_id="test_device_1", sample_rate=250)

    for i in range(100):
        t = i * 0.004
        twin1.set_sim_clock(t)
        twin2.set_sim_clock(t)

    assert twin1.get_sim_clock() == twin2.get_sim_clock()
    assert twin1.clock.tick == twin2.clock.tick == 100
    assert twin1.get_history() == twin2.get_history()


def test_digital_twin_component_state():
    """Verify decomposed components in DigitalTwin reflect consistent state."""
    twin = DigitalTwin(device_id="neuro_device_42", sample_rate=500, num_channels=16)

    assert twin.signal.sample_rate == 500
    assert twin.signal.num_channels == 16
    assert twin.battery.battery_level == 100.0
    assert twin.physics.stimulation_enabled is False
    assert twin.clinical.clinical_status == "Nominal"

    twin.physics.stimulation_enabled = True
    twin.physics.stimulation_amplitude_ma = 2.5
    assert twin.stimulation_enabled is True
    assert twin.stimulation_amplitude_ma == 2.5


def test_deterministic_rng_reproducibility():
    """Verify DeterministicRNG stream reproducibility given identical seed (ADR-004)."""
    rng1 = DeterministicRNG(seed=1337)
    rng2 = DeterministicRNG(seed=1337)

    samples1 = rng1.normal(loc=0.0, scale=1.0, size=(8, 100))
    samples2 = rng2.normal(loc=0.0, scale=1.0, size=(8, 100))

    assert (samples1 == samples2).all()


def test_bifurcated_scheduler_tick():
    """Verify BifurcatedScheduler dispatches task callbacks at expected ticks (ADR-005)."""
    clock = DeterministicClock(mode=ClockMode.VIRTUAL, step_dt_ms=4.0)
    scheduler = BifurcatedScheduler(clock=clock)

    executed = []
    scheduler.schedule(delay_sec=0.008, callback=lambda: executed.append("task1"))

    # Step 1: 0.004s -> not executed
    scheduler.tick_and_dispatch()
    assert len(executed) == 0

    # Step 2: 0.008s -> executed
    scheduler.tick_and_dispatch()
    assert executed == ["task1"]


def test_compiler_pin_verification():
    """Verify CompilerPin generates deterministic environment hash (ADR-013)."""
    pin_hash = CompilerPin.compute_pin_hash()
    assert isinstance(pin_hash, str)
    assert len(pin_hash) == 64
    assert CompilerPin.verify_pin(pin_hash) is True
