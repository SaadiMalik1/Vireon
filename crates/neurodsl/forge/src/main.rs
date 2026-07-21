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

use forge::compile;
use std::io::{self, Read};

fn main() {
    let mut source = String::new();
    if let Err(e) = io::stdin().read_to_string(&mut source) {
        eprintln!("Error reading stdin: {}", e);
        std::process::exit(1);
    }

    match compile(&source) {
        Ok(bytecode) => {
            let hex: String = bytecode.iter().map(|b| format!("{:02X}", b)).collect();
            println!("{}", hex);
        }
        Err(e) => {
            eprintln!("Compilation failed: {:?}", e);
            std::process::exit(1);
        }
    }
}
