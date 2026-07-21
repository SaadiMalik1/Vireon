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

import os
import ast


def test_no_vireon_lab_imports_in_vireon():
    """Enforces Rule 3: Vireon core runtime must NEVER import from vireon-lab or vireon_lab."""
    vireon_pkg_dir = os.path.abspath(
        os.path.join(os.path.dirname(__file__), "..", "vireon")
    )
    assert os.path.exists(vireon_pkg_dir), f"Directory {vireon_pkg_dir} does not exist"

    violations = []

    for root, _, files in os.walk(vireon_pkg_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                try:
                    tree = ast.parse(content, filename=filepath)
                except SyntaxError:
                    continue

                for node in ast.walk(tree):
                    if isinstance(node, ast.Import):
                        for alias in node.names:
                            if alias.name.startswith("vireon_lab") or alias.name.startswith("providers."):
                                violations.append((filepath, alias.name))
                    elif isinstance(node, ast.ImportFrom):
                        if node.module and (node.module.startswith("vireon_lab") or node.module.startswith("providers")):
                            violations.append((filepath, node.module))

    assert not violations, f"Forbidden imports found in Vireon runtime: {violations}"
