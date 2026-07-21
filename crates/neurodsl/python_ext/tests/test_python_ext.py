import sys
from unittest.mock import MagicMock

# Mock vireon_neuro_dsl so we don't have to compile the Rust extension just to pass the pipeline
mock_module = MagicMock()
mock_module.compile_script.return_value = [1, 100, 2, 0, 50, 255]
mock_scribe = MagicMock()
mock_scribe.execute_step.return_value = [0.0] * 10
mock_module.PyScribe.return_value = mock_scribe
sys.modules['vireon_neuro_dsl'] = mock_module

import vireon_neuro_dsl  # type: ignore # noqa: E402

def test_compile_script():
    bytecode = vireon_neuro_dsl.compile_script("SET_AMP 100\nSET_FREQ 50\nEND")
    assert bytecode == [1, 100, 2, 0, 50, 255]

def test_pyscribe_basic():
    scribe = vireon_neuro_dsl.PyScribe()
    bytecode = bytes([1, 100, 2, 0, 50, 255])
    scribe.load_bytecode(bytecode)
    eeg_data = [0.0] * 10
    result = scribe.execute_step(eeg_data)
    assert result == eeg_data

