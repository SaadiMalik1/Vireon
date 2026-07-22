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

use scribe::interpreter::ScribeContext;

#[test]
fn test_scribe_basic_execution() {
    let mut context = ScribeContext::new();
    let bytecode = vec![1, 100, 2, 0, 50, 255]; // SET_AMP 100, SET_FREQ 50, END
    assert!(context.verify(&bytecode).is_ok());
    assert!(context.execute(&bytecode, &vec![0.0; 8]).is_ok());
}

#[test]
fn test_scribe_invalid_opcode() {
    let context = ScribeContext::new();
    let bytecode = vec![99, 255];
    assert!(context.verify(&bytecode).is_err());
}

#[test]
fn test_scribe_empty_bytecode() {
    let context = ScribeContext::new();
    let bytecode = vec![];
    assert!(context.verify(&bytecode).is_ok()); // Empty slice does not violate verify
}

#[test]
fn test_scribe_amp_security_violation() {
    let context = ScribeContext::new();
    let bytecode = vec![1, 101, 255]; // > 100 mA security limit
    assert!(context.verify(&bytecode).is_err());
}

macro_rules! generate_opcode_tests {
    ($($name:ident: $bytecode:expr, $should_pass:expr);* $(;)?) => {
        $(
            #[test]
            fn $name() {
                let mut context = ScribeContext::new();
                let result = context.verify(&$bytecode);
                if $should_pass {
                    assert!(result.is_ok(), "Expected bytecode {:?} to verify", $bytecode);
                    assert!(context.execute(&$bytecode, &vec![1.0; 8]).is_ok());
                } else {
                    assert!(result.is_err(), "Expected bytecode {:?} to fail verification", $bytecode);
                }
            }
        )*
    };
}

generate_opcode_tests! {
    test_amp_zero: vec![1, 0, 255], true;
    test_amp_min: vec![1, 1, 255], true;
    test_amp_fifty: vec![1, 50, 255], true;
    test_amp_max_allowed: vec![1, 100, 255], true;
    test_freq_zero: vec![2, 0, 0, 255], true;
    test_freq_low: vec![2, 0, 10, 255], true;
    test_freq_100: vec![2, 0, 100, 255], true;
    test_freq_130: vec![2, 0, 130, 255], true;
    test_freq_max_allowed: vec![2, 3, 232, 255], true;
    test_shape_circle: vec![3, 1, 10, 255], true;
    test_shape_square: vec![3, 2, 10, 255], true;
    test_shape_triangle: vec![3, 3, 10, 255], true;
    test_wait_10ms: vec![4, 0, 10, 255], true;
    test_wait_100ms: vec![4, 0, 100, 255], true;
    test_read_sensor_ch0: vec![5, 0, 10, 255], true;
    test_read_sensor_ch1: vec![5, 1, 11, 255], true;
    test_read_sensor_ch7: vec![5, 7, 17, 255], true;
    test_loop_single: vec![6, 1, 1, 10, 7, 255], true;
    test_loop_10_count: vec![6, 10, 1, 10, 7, 255], true;
    test_jump_if_valid: vec![8, 10, 0, 0, 5, 255], true; // target = offset 5 (END)

    test_combo_stimulation_protocol: vec![1, 20, 2, 0, 130, 3, 2, 5, 4, 0, 10, 255], true;
    test_combo_two_wait_cycles: vec![4, 0, 5, 4, 0, 5, 255], true;
    test_combo_amp_switch: vec![1, 10, 1, 20, 1, 30, 255], true;
    test_combo_freq_sweep: vec![2, 0, 10, 2, 0, 50, 2, 0, 100, 255], true;
    test_combo_all_shapes: vec![3, 1, 5, 3, 2, 5, 3, 3, 5, 255], true;
    test_combo_sensors_read: vec![5, 0, 0, 5, 1, 1, 5, 2, 2, 255], true;
    test_truncated_amp: vec![1], false;
    test_truncated_freq: vec![2, 0], false;
    test_truncated_shape: vec![3, 1], false;
    test_truncated_wait: vec![4], false;
    test_truncated_sensor: vec![5, 0], false;
    test_truncated_jump: vec![8, 1, 0], false;
    test_double_end: vec![255, 255], true;
    test_zero_filled_buffer: vec![0, 0, 0, 0, 255], false;
    test_max_byte_values: vec![255], true;
    test_nested_loops_valid: vec![6, 2, 6, 2, 7, 7, 255], true;
    test_sensor_addr_boundary: vec![5, 0, 255, 255], true;
    test_multiple_ends: vec![1, 10, 255, 1, 20, 255], true;
}
