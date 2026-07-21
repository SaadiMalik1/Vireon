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

import time
from vireon.runtime.event_bus import EventBus
from vireon.sdk.events import Event
from vireon.runtime.twin import DigitalTwin


def test_event_bus_publish_subscribe():
    bus = EventBus()
    received_events = []

    def handler(event: Event):
        received_events.append(event)

    sub_id = bus.subscribe("telemetry.chunk", handler)
    event = Event(topic="telemetry.chunk", data={"samples": [0.1, 0.2, 0.3]}, timestamp=1.0)
    bus.publish(event)
    bus.flush()

    assert len(received_events) == 1
    assert received_events[0].topic == "telemetry.chunk"
    assert received_events[0].data["samples"] == [0.1, 0.2, 0.3]

    bus.unsubscribe(sub_id)
    bus.publish(event)
    bus.flush()
    assert len(received_events) == 1


def test_twin_event_lifecycle():
    twin = DigitalTwin(device_id="integration_device", sample_rate=250)
    bus = EventBus()
    events_logged = []

    def state_logger(event: Event):
        events_logged.append(event.data)

    bus.subscribe("twin.state_changed", state_logger)

    twin.set_sim_clock(0.004)
    bus.publish(Event(topic="twin.state_changed", data=twin.get_state()))
    bus.flush()

    assert len(events_logged) == 1
    assert events_logged[0]["device_id"] == "integration_device"
    assert events_logged[0]["sim_clock"] == 0.004
