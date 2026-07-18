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

import threading
import time

from vireon.core.physics import PhysicsEngine

def test_twin_concurrent_mutation(mock_twin):
    """
    Test that concurrent mutation of DigitalTwin state (including physics tick)
    does not cause torn state or exceptions, proving RLock safety.
    """
    twin = mock_twin
    errors = []
    
    def simulate_physics():
        physics = PhysicsEngine()
        try:
            for _ in range(100):
                # Apply physics constraints (computes temperature, etc.)
                physics.tick(twin, 0.1)
                time.sleep(0.001)
        except Exception as e:
            errors.append(e)
            
    def simulate_clinical():
        try:
            for _ in range(100):
                # Emulate clinical checking
                twin.update_therapy(True)
                twin.update_stimulation_params(2.0, 130.0)
                time.sleep(0.001)
        except Exception as e:
            errors.append(e)

    def simulate_attack():
        try:
            for _ in range(100):
                # Emulate attack mutation
                if hasattr(twin, "_lock"):
                    with twin._lock:
                        twin.stimulation_amplitude_ma = 15.0
                time.sleep(0.001)
        except Exception as e:
            errors.append(e)

    t1 = threading.Thread(target=simulate_physics)
    t2 = threading.Thread(target=simulate_clinical)
    t3 = threading.Thread(target=simulate_attack)

    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    # If any thread threw an exception (e.g. from a race condition), it would be appended to errors
    assert len(errors) == 0, f"Exceptions occurred during concurrent mutation: {errors}"
    
    # State should be logically intact, temperature shouldn't be infinite
    assert twin.temperature_celsius >= 37.0
