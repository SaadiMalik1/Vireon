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

use scribe::execute_bytecode;
use std::env;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() < 2 {
        eprintln!("Usage: scribe <hex_bytecode>");
        std::process::exit(1);
    }

    let hex_str = &args[1];
    let mut bytecode = Vec::new();
    let hex_chars: Vec<char> = hex_str.chars().collect();
    for chunk in hex_chars.chunks(2) {
        if chunk.len() == 2 {
            let byte_str: String = chunk.iter().collect();
            if let Ok(byte) = u8::from_str_radix(&byte_str, 16) {
                bytecode.push(byte);
            } else {
                eprintln!("Invalid hex byte: {}", byte_str);
                std::process::exit(1);
            }
        }
    }

    match execute_bytecode(&bytecode) {
        Ok(_) => println!("Execution successful"),
        Err(e) => {
            eprintln!("Execution failed: {:?}", e);
            std::process::exit(1);
        }
    }
}
