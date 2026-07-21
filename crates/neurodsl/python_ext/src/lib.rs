// Copyright 2026 VIREON Contributors
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//     http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

use pyo3::exceptions::{PyRuntimeError, PyValueError};
use pyo3::prelude::*;
use scribe::interpreter::ScribeContext;

#[pyclass]
pub struct PyScribe {
    inner: ScribeContext,
    bytecode: Vec<u8>,
}

impl Default for PyScribe {
    fn default() -> Self {
        Self::new()
    }
}

#[pymethods]
impl PyScribe {

    #[new]
    pub fn new() -> Self {
        PyScribe {
            inner: ScribeContext::new(),
            bytecode: Vec::new(),
        }
    }

    pub fn load_bytecode(&mut self, bytecode: &[u8]) -> PyResult<()> {
        if let Err(e) = self.inner.verify(bytecode) {
            return Err(PyValueError::new_err(format!(
                "Bytecode validation failed: {:?}",
                e
            )));
        }
        self.bytecode = bytecode.to_vec();
        Ok(())
    }

    pub fn execute_step(&mut self, eeg_data: Vec<f32>) -> PyResult<Vec<f32>> {
        if self.bytecode.is_empty() {
            return Ok(eeg_data);
        }

        if let Err(e) = self.inner.execute(&self.bytecode, &eeg_data) {
            return Err(PyRuntimeError::new_err(format!(
                "Scribe execution error: {:?}",
                e
            )));
        }

        Ok(eeg_data)
    }
}

/// Compiles a NeuroDSL script string into bytecode.
#[pyfunction]
fn compile_script(source: &str) -> PyResult<Vec<u8>> {
    match forge::compile(source) {
        Ok(bytecode) => Ok(bytecode),
        Err(e) => Err(PyValueError::new_err(format!("Compile error: {:?}", e))),
    }
}

#[pymodule]
fn vireon_neuro_dsl(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<PyScribe>()?;
    m.add_function(wrap_pyfunction!(compile_script, m)?)?;
    Ok(())
}
