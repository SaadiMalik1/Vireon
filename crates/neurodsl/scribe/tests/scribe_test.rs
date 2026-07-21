use scribe::interpreter::ScribeContext;

#[test]
fn test_scribe_basic() {
    let mut context = ScribeContext::new();
    // SET_AMP (1) 100, SET_FREQ (2) 50, END (255)
    let bytecode = vec![1, 100, 2, 0, 50, 255];
    assert!(context.verify(&bytecode).is_ok());

    let eeg_data = vec![0.0; 10];
    let result = context.execute(&bytecode, &eeg_data);
    assert!(result.is_ok());
}

#[test]
fn test_scribe_invalid_bytecode() {
    let mut context = ScribeContext::new();
    let bytecode = vec![99]; // Invalid opcode
    assert!(context.verify(&bytecode).is_err());
}
