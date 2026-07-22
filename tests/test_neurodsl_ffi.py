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

import pytest
import vireon_neuro_dsl


def test_neurodsl_ffi_exception_exports():
    """Verify PyO3 FFI exception exports in vireon_neuro_dsl (ADR-009)."""
    assert hasattr(vireon_neuro_dsl, "VireonNeuroDSLError")
    assert hasattr(vireon_neuro_dsl, "NeuroDSLCompileError")
    assert hasattr(vireon_neuro_dsl, "NeuroDSLExecutionError")
    assert hasattr(vireon_neuro_dsl, "NeuroDSLSecurityViolation")

    assert issubclass(vireon_neuro_dsl.NeuroDSLCompileError, vireon_neuro_dsl.VireonNeuroDSLError)
    assert issubclass(vireon_neuro_dsl.NeuroDSLExecutionError, vireon_neuro_dsl.VireonNeuroDSLError)


def test_neurodsl_compile_error_exception():
    """Verify compile_script raises NeuroDSLCompileError on invalid syntax."""
    with pytest.raises(vireon_neuro_dsl.NeuroDSLCompileError):
        vireon_neuro_dsl.compile_script("SET_AMP INVALID_AMP_VALUE")


def test_neurodsl_pyscribe_execution():
    """Verify PyScribe bytecode loading and execution."""
    scribe = vireon_neuro_dsl.PyScribe()
    bytecode = vireon_neuro_dsl.compile_script("SET_AMP 50\nSET_FREQ 100\nEND\n")
    assert len(bytecode) > 0

    scribe.load_bytecode(bytecode)
    res = scribe.execute_step([0.0] * 8)
    assert len(res) == 8
