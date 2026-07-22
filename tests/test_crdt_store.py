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

from vireon.runtime.crdt_store import CRDTStateStore, GCounter, LWWRegister
from vireon.runtime.crdt_gc import EpochedGarbageCollector


def test_gcounter_crdt_convergence():
    c1 = GCounter()
    c2 = GCounter()

    c1.increment("replica_A", 5)
    c2.increment("replica_B", 3)

    c1.merge(c2)
    assert c1.value() == 8


def test_lww_register_convergence():
    r1 = LWWRegister()
    r2 = LWWRegister()

    r1.assign("initial", timestamp=100.0)
    r2.assign("latest", timestamp=200.0)

    r1.merge(r2)
    assert r1.val == "latest"


def test_crdt_state_store_merge_and_gc():
    store1 = CRDTStateStore(replica_id="node_1")
    store2 = CRDTStateStore(replica_id="node_2")

    store1.set_register("amp", 10.0, timestamp=1.0)
    store2.set_register("amp", 25.0, timestamp=2.0)

    store1.increment_counter("ticks", 10)
    store2.increment_counter("ticks", 5)

    store1.merge(store2)
    assert store1.get_register("amp") == 25.0
    assert store1.get_counter("ticks") == 15

    gc = EpochedGarbageCollector(store1)
    gc.update_replica_epoch("node_1", 1)
    gc.update_replica_epoch("node_2", 1)
    cleaned = gc.collect(max_retain_ops=1)
    assert cleaned >= 0
