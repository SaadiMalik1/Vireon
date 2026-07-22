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
Exhaustive Phase 9 Cryptographic Signed Evidence Package Generator.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
import time
import hashlib
import platform
import subprocess
from cryptography.hazmat.primitives.asymmetric import ed25519
from vireon.runtime.merkle import MerkleTree
from vireon.runtime.trace_bundle import TraceBundle


def get_git_commit_sha() -> str:
    try:
        res = subprocess.run(["git", "rev-parse", "HEAD"], capture_output=True, text=True, check=True)
        return res.stdout.strip()
    except Exception:
        return "unknown_commit"


def compute_directory_source_checksum(directory: str) -> str:
    """Computes a combined SHA-256 digest of all source files in a directory."""
    hasher = hashlib.sha256()
    for root, _, files in sorted(os.walk(directory)):
        for fname in sorted(files):
            if fname.endswith((".py", ".rs", ".toml", ".h", ".c")):
                fpath = os.path.join(root, fname)
                with open(fpath, "rb") as f:
                    hasher.update(f.read())
    return hasher.hexdigest()


def generate_system_evidence_package(output_dir: str = "evidence") -> str:
    """Generates an exhaustive, cryptographically signed machine-readable evidence artifact (Phase 9)."""
    os.makedirs(output_dir, exist_ok=True)
    git_sha = get_git_commit_sha()

    vireon_src_digest = compute_directory_source_checksum("vireon")
    neurodsl_src_digest = compute_directory_source_checksum("crates/neurodsl")

    # Collect exhaustive system and build metadata
    meta = {
        "git_commit": git_sha,
        "timestamp": time.time(),
        "vireon_source_sha256": vireon_src_digest,
        "neurodsl_source_sha256": neurodsl_src_digest,
        "python_version": sys.version,
        "platform": platform.platform(),
        "processor": platform.processor(),
        "system": platform.system(),
        "architecture": platform.architecture()[0]
    }

    # Build Merkle tree from system metadata and digests
    leaf_bytes = json.dumps(meta, sort_keys=True).encode("utf-8")
    tree = MerkleTree([leaf_bytes])

    # Generate Ed25519 keypair for signing evidence package
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()
    pub_hex = public_key.public_bytes_raw().hex()

    bundle = TraceBundle(
        merkle_root_hex=tree.get_root_hex(),
        pin_hash=git_sha[:12],
        metadata=meta
    )

    sig = bundle.sign(private_key)
    verified = bundle.verify_signature(public_key)

    evidence_data = {
        "trace_bundle": {
            "merkle_root": bundle.merkle_root_hex,
            "pin_hash": bundle.pin_hash,
            "metadata": bundle.metadata,
            "signature_hex": sig.hex(),
            "public_key_hex": pub_hex,
            "signature_verified": verified
        }
    }

    file_path = os.path.join(output_dir, f"evidence_package_{bundle.pin_hash}.json")
    with open(file_path, "w", encoding="utf-8") as f:
        json.dump(evidence_data, f, indent=2)

    print(f"[EVIDENCE] Generated signed evidence artifact: {file_path}")
    return file_path


if __name__ == "__main__":
    generate_system_evidence_package()
