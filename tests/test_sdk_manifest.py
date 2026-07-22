# Copyright 2026 VIREON Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may me obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from cryptography.hazmat.primitives.asymmetric import ed25519
from vireon.sdk.manifest import CapabilityManifest


def test_capability_manifest_ed25519_signing():
    """Verify CapabilityManifest Ed25519 signature generation and verification (ADR-003)."""
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    manifest = CapabilityManifest(
        name="test_clinical_provider",
        version="1.0.0",
        category="clinical",
        publishes_events=["telemetry.alert"],
        requires_host_access=False,
    )

    # Initial signature verification should fail when unsigned
    assert manifest.verify_signature(public_key) is False

    # Sign manifest
    sig = manifest.sign(private_key)
    assert sig is not None
    assert len(sig) == 64

    # Signature verification should succeed
    assert manifest.verify_signature(public_key) is True

    # Tampered manifest data should fail verification
    manifest.version = "2.0.0"
    assert manifest.verify_signature(public_key) is False
