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

from cryptography.hazmat.primitives.asymmetric import ed25519
from vireon.runtime.merkle import MerkleTree
from vireon.runtime.trace_bundle import TraceBundle
from vireon.runtime.watchdog import HardwareWatchdog


def test_merkle_tree_root_computation():
    tree1 = MerkleTree([b"event_1", b"event_2", b"event_3"])
    tree2 = MerkleTree([b"event_1", b"event_2", b"event_3"])
    tree3 = MerkleTree([b"event_1", b"event_2", b"event_TAMPERED"])

    assert tree1.get_root_hex() == tree2.get_root_hex()
    assert tree1.get_root_hex() != tree3.get_root_hex()


def test_signed_trace_bundle():
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    tree = MerkleTree([b"state_0", b"state_1"])
    bundle = TraceBundle(
        merkle_root_hex=tree.get_root_hex(),
        pin_hash="abc123pin",
        metadata={"experiment": "dbs_trial"}
    )

    bundle.sign(private_key)
    assert bundle.verify_signature(public_key) is True

    bundle.merkle_root_hex = "tampered_root"
    assert bundle.verify_signature(public_key) is False


def test_hardware_watchdog_timeout():
    stalled_called = False

    def on_stall():
        nonlocal stalled_called
        stalled_called = True

    wd = HardwareWatchdog(timeout_sec=0.01, on_stall_callback=on_stall)
    wd.kick()
    assert wd.check() is True

    import time
    time.sleep(0.02)
    assert wd.check() is False
    assert stalled_called is True


def test_state_store_merkle_and_checksum():
    from vireon.runtime.event_bus import EventBus
    from vireon.runtime.state_store import StateStore

    bus = EventBus()
    tree = MerkleTree()
    store = StateStore(bus, merkle_tree=tree)

    checksum_before = store.get_state_checksum()
    assert len(checksum_before) == 8

    store.set("tissue_temp", 37.5)
    store.set("battery_charge", 0.98)

    assert tree.get_root() is not None
    checksum_after = store.get_state_checksum()
    assert checksum_before != checksum_after

