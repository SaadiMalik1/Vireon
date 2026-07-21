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

from vireon.runtime.twin import DigitalTwin, SimClock, ClockMode


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
