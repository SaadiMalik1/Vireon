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

use crate::ast::{Ast, Statement};
use crate::error::ForgeError;

pub fn verify_ast(ast: &Ast) -> Result<(), ForgeError> {
    let mut loop_depth = 0;

    for stmt in &ast.statements {
        match stmt {
            Statement::SetAmp(val) => {
                // Example guardrail: Amplitude should not exceed safety limits
                if *val > 100 {
                    return Err(ForgeError::ParserError(format!(
                        "Amplitude {} exceeds safety limit of 100",
                        val
                    )));
                }
            }
            Statement::SetFreq(val) => {
                // Example guardrail: Frequency bounds (e.g., must be <= 1000 Hz)
                if *val > 1000 {
                    return Err(ForgeError::ParserError(format!(
                        "Frequency {} exceeds safety limit of 1000Hz",
                        val
                    )));
                }
            }
            Statement::LoopStart(iters) => {
                // Limit maximum iterations per loop to prevent runaway
                if *iters > 100 {
                    return Err(ForgeError::ParserError(format!(
                        "Loop iterations {} exceeds limit of 100",
                        iters
                    )));
                }
                loop_depth += 1;
                // Limit nested loops to depth 3
                if loop_depth > 3 {
                    return Err(ForgeError::ParserError(
                        "Exceeded maximum loop nesting depth of 3".to_string(),
                    ));
                }
            }
            Statement::LoopEnd => {
                if loop_depth == 0 {
                    return Err(ForgeError::ParserError(
                        "Unmatched LOOP_END statement".to_string(),
                    ));
                }
                loop_depth -= 1;
            }
            Statement::JumpIf(_, _, target) if *target > 4096 => {
                return Err(ForgeError::ParserError(format!(
                    "JUMP_IF target {} is out of realistic program bounds",
                    target
                )));
            }

            _ => {}
        }
    }

    if loop_depth != 0 {
        return Err(ForgeError::ParserError(
            "Unmatched LOOP_START statement at end of program".to_string(),
        ));
    }

    Ok(())
}
