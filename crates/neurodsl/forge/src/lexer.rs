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

use crate::error::ForgeError;

#[derive(Debug, PartialEq, Clone)]
pub enum Token {
    SetAmp,
    SetFreq,
    Shape,
    Wait,
    End,
    ReadSensor,
    LoopStart,
    LoopEnd,
    JumpIf,
    Number(u16),
    Identifier(String),
}

pub fn lex(source: &str) -> Result<Vec<Token>, ForgeError> {
    let mut tokens = Vec::new();

    for line in source.lines() {
        let code_part = if let Some(idx) = line.find("//") {
            &line[..idx]
        } else {
            line
        };

        for word in code_part.split_whitespace() {
            let token = match word.to_uppercase().as_str() {
                "SET_AMP" => Token::SetAmp,
                "SET_FREQ" => Token::SetFreq,
                "SHAPE" => Token::Shape,
                "WAIT" => Token::Wait,
                "END" => Token::End,
                "READ_SENSOR" => Token::ReadSensor,
                "LOOP_START" => Token::LoopStart,
                "LOOP_END" => Token::LoopEnd,
                "JUMP_IF" => Token::JumpIf,
                _ => {
                    if let Ok(num) = word.parse::<u16>() {
                        Token::Number(num)
                    } else {
                        Token::Identifier(word.to_string())
                    }
                }
            };
            tokens.push(token);
        }
    }

    Ok(tokens)
}
