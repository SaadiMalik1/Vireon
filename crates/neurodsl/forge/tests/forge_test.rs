use forge::compile;

#[test]
fn test_compile_basic() {
    let source = "SET_AMP 100\nSET_FREQ 50\nEND";
    let result = compile(source);
    assert!(result.is_ok());
    let bytecode = result.unwrap();
    // SET_AMP (1) 100, SET_FREQ (2) 0, 50, END (255)
    assert_eq!(bytecode, vec![1, 100, 2, 0, 50, 255]);
}

#[test]
fn test_compile_invalid_amp() {
    let source = "SET_AMP 256";
    let result = compile(source);
    assert!(result.is_err());
}
