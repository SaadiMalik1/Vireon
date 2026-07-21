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
Architecture boundary tests (AT-01 through AT-08).

These tests enforce the VIREON Architecture Constitution:
- runtime/ is domain-agnostic infrastructure
- providers/ contain domain logic
- sdk/ defines contracts
- No layer may import from a layer it should not depend on
"""

import ast
import pathlib
from typing import List, Set, Tuple


ROOT_DIR = pathlib.Path(__file__).resolve().parent.parent.parent
VIREON_DIR = ROOT_DIR / "vireon"
RUNTIME_DIR = VIREON_DIR / "runtime"
SDK_DIR = VIREON_DIR / "sdk"
PROVIDERS_DIR = ROOT_DIR / "providers"
REF_PROVIDERS_DIR = VIREON_DIR / "reference_providers"
LAB_DIR = ROOT_DIR.parent / "vireon-lab"

# Known deprecation shim files in runtime/ that re-export from providers.
# These are the ONLY runtime files allowed to import from providers.
RUNTIME_SHIM_FILES = {
    "physics.py", "dynamics.py", "detection.py", "protocol.py",
    "authentication.py", "e2ee.py", "privacy.py", "privacy_leakage.py",
    "threat_intel.py", "compliance.py", "validation.py", "safety_envelope.py",
    "attack_factory.py", "redteam.py", "config.py", "engine.py",
    "fuzzer.py", "zta.py", "lsl_streamer.py", "sbom.py",
    "spdf_auditor.py", "stix_mapper.py", "stride.py", "data_provider.py",
    "interfaces.py", "twin.py",
}

# Known runtime files that still import from runtime (not counted as violations)
RUNTIME_INTERNAL_PREFIXES = {"vireon.runtime.", "vireon.sdk."}


def _get_py_files(directory: pathlib.Path) -> List[pathlib.Path]:
    """Get all .py files in directory recursively."""
    if not directory.exists():
        return []
    return list(directory.rglob("*.py"))


def _extract_imports(filepath: pathlib.Path) -> Set[str]:
    """Extract all import module paths from a Python file using AST."""
    try:
        source = filepath.read_text(encoding="utf-8")
        tree = ast.parse(source)
    except (SyntaxError, UnicodeDecodeError):
        return set()

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
    return imports


def _violations(
    source_dir: pathlib.Path,
    forbidden_prefixes: List[str],
    exclude_files: Set[str] = set(),
) -> List[Tuple[str, str]]:
    """Find files importing from forbidden prefixes.

    Returns list of (relative_filepath, offending_import) tuples.
    """
    violations = []
    for pyfile in _get_py_files(source_dir):
        if pyfile.name in exclude_files:
            continue
        # Skip __pycache__
        if "__pycache__" in str(pyfile):
            continue
        imports = _extract_imports(pyfile)
        for imp in imports:
            for prefix in forbidden_prefixes:
                if imp.startswith(prefix):
                    rel = pyfile.relative_to(source_dir)
                    violations.append((str(rel), imp))
    return violations


# ========== AT-01: Runtime must not import from providers ==========

def test_runtime_no_provider_imports():
    """AT-01: runtime/ must not import from providers/ or reference_providers/.

    Deprecation shim files are exempted since their purpose is to bridge
    old import paths to new provider locations.
    """
    violations = _violations(
        RUNTIME_DIR,
        ["providers.", "vireon.reference_providers."],
        exclude_files=RUNTIME_SHIM_FILES,
    )
    assert violations == [], (
        "AT-01 FAIL: runtime/ imports providers:\n"
        + "\n".join(f"  {f}: {imp}" for f, imp in violations)
    )


# ========== AT-02: Providers must not import from runtime ==========

def test_providers_no_runtime_imports():
    """AT-02: providers/ must not import from vireon.runtime.*.

    Providers should only depend on vireon.sdk and standard library.
    """
    violations = _violations(PROVIDERS_DIR, ["vireon.runtime."])
    assert violations == [], (
        "AT-02 FAIL: providers/ imports runtime:\n"
        + "\n".join(f"  {f}: {imp}" for f, imp in violations)
    )


# ========== AT-03: SDK must not import from runtime or providers ==========

def test_sdk_no_runtime_or_provider_imports():
    """AT-03: sdk/ must not import from vireon.runtime or providers/.

    The SDK defines pure contracts (ABCs, dataclasses, enums).
    """
    violations = _violations(
        SDK_DIR,
        ["vireon.runtime.", "providers.", "vireon.reference_providers."],
    )
    assert violations == [], (
        "AT-03 FAIL: sdk/ imports runtime/providers:\n"
        + "\n".join(f"  {f}: {imp}" for f, imp in violations)
    )


# ========== AT-05: No god classes ==========

def test_no_god_classes():
    """AT-05: No file in runtime/ should exceed 300 LOC.

    This excludes deprecation shim files and test files.
    Target is 200 LOC per the Constitution, but we allow 300 during migration.
    """
    MAX_LOC = 300
    oversized = []
    for pyfile in _get_py_files(RUNTIME_DIR):
        if pyfile.name in RUNTIME_SHIM_FILES:
            continue
        if "__pycache__" in str(pyfile):
            continue
        try:
            lines = pyfile.read_text(encoding="utf-8").splitlines()
            # Count non-empty, non-comment lines
            loc = sum(1 for line in lines if line.strip() and not line.strip().startswith("#"))
            if loc > MAX_LOC:
                rel = pyfile.relative_to(RUNTIME_DIR)
                oversized.append((str(rel), loc))
        except (UnicodeDecodeError, OSError):
            pass

    assert oversized == [], (
        f"AT-05 FAIL: Files exceeding {MAX_LOC} LOC in runtime/:\n"
        + "\n".join(f"  {f}: {loc} LOC" for f, loc in oversized)
    )


# ========== AT-06: Every provider has a manifest ==========

def test_every_provider_has_manifest():
    """AT-06: Every provider subdirectory must have an __init__.py."""
    if not PROVIDERS_DIR.exists():
        return  # Skip if providers/ doesn't exist yet

    missing = []
    for subdir in sorted(PROVIDERS_DIR.iterdir()):
        if subdir.is_dir() and subdir.name != "__pycache__":
            init = subdir / "__init__.py"
            if not init.exists():
                missing.append(subdir.name)

    assert missing == [], (
        "AT-06 FAIL: Provider directories missing __init__.py:\n"
        + "\n".join(f"  {d}" for d in missing)
    )


# ========== AT-08: No circular imports ==========

def test_no_circular_imports():
    """AT-08: Verify no circular import dependency between major packages.

    Check that runtime doesn't import providers (which import back to runtime).
    This is a simplified topological check: providers→sdk only, runtime→sdk only.
    """
    # Build a directed dependency graph
    packages = {
        "sdk": SDK_DIR,
        "runtime": RUNTIME_DIR,
        "providers": PROVIDERS_DIR,
    }

    deps = {}
    for pkg_name, pkg_dir in packages.items():
        pkg_deps = set()
        for pyfile in _get_py_files(pkg_dir):
            if pyfile.name in RUNTIME_SHIM_FILES:
                continue
            if "__pycache__" in str(pyfile):
                continue
            imports = _extract_imports(pyfile)
            for imp in imports:
                if imp.startswith("vireon.runtime."):
                    pkg_deps.add("runtime")
                elif imp.startswith("vireon.sdk."):
                    pkg_deps.add("sdk")
                elif imp.startswith("providers."):
                    pkg_deps.add("providers")
        # Remove self-dependencies
        pkg_deps.discard(pkg_name)
        deps[pkg_name] = pkg_deps

    # Check for cycles: sdk should have no deps, providers should not depend on runtime
    cycles = []
    if "runtime" in deps.get("sdk", set()):
        cycles.append("sdk → runtime (forbidden)")
    if "providers" in deps.get("sdk", set()):
        cycles.append("sdk → providers (forbidden)")
    if "runtime" in deps.get("providers", set()):
        cycles.append("providers → runtime (forbidden)")
    if "providers" in deps.get("runtime", set()):
        cycles.append("runtime → providers (forbidden)")

    assert cycles == [], (
        "AT-08 FAIL: Circular/forbidden dependencies detected:\n"
        + "\n".join(f"  {c}" for c in cycles)
    )
