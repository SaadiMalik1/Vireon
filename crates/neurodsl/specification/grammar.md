# NeuroDSL Specification (v1.0)

**The Domain-Specific Language for Neurotechnology Stimulation & Sensing Protocols**

---

## 1. Formal Grammar (EBNF)

```ebnf
program        = { statement | line_comment } ;

statement      = set_amp | set_freq | shape | wait | read_sensor
               | loop_start | loop_end | jump_if | end ;

set_amp        = "SET_AMP" , number ;
set_freq       = "SET_FREQ" , number ;
shape          = "SHAPE" , shape_type , number ;
wait           = "WAIT" , number ;
read_sensor    = "READ_SENSOR" , number , number ;
loop_start     = "LOOP_START" , number ;
loop_end       = "LOOP_END" ;
jump_if        = "JUMP_IF" , number , number , number ;
end            = "END" ;

shape_type     = "CIRCLE" | "SQUARE" | "TRIANGLE" ;
number         = digit , { digit } ;
digit          = "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" ;
line_comment   = "//" , { any_character } , new_line ;
```

---

## 2. Opcode Reference Table & Encoding

| Instruction | Opcode (Hex) | Operand 1 | Operand 2 | Operand 3 | Description |
|-------------|--------------|-----------|-----------|-----------|-------------|
| `SET_AMP` | `0x01` | `u8` (amplitude) | — | — | Sets stimulation amplitude (0-255 mA) |
| `SET_FREQ` | `0x02` | `u16` (frequency) | — | — | Sets stimulation frequency (Hz, 16-bit) |
| `SHAPE` | `0x03` | `u8` (shape ID) | `u8` (size) | — | Sets stimulation waveform shape (1=Circle, 2=Square, 3=Triangle) |
| `WAIT` | `0x04` | `u16` (milliseconds) | — | — | Suspends execution for specified ticks/ms |
| `READ_SENSOR`| `0x05` | `u8` (sensor_id) | `u8` (addr) | — | Reads sensor channel value into VM memory address |
| `LOOP_START` | `0x06` | `u8` (iterations) | — | — | Begins a counted loop block |
| `LOOP_END` | `0x07` | — | — | — | Ends loop block and decrements iteration counter |
| `JUMP_IF` | `0x08` | `u8` (addr) | `u8` (value) | `u16` (target) | Conditional jump to target offset if `memory[addr] == value` |
| `END` | `0xFF` | — | — | — | Terminates VM program execution |

---

## 3. Type System & Execution Semantics

- **Numeric Limits**:
  - Amplitude values: 8-bit unsigned integer (`0..255`).
  - Frequency & Wait values: 16-bit unsigned integer (`0..65535`).
  - Memory Addresses: 8-bit unsigned index (`0..255`).
- **Execution Semantics**:
  - The interpreter (`scribe`) maintains a logical instruction pointer `pc`, a 256-byte linear memory array `memory`, and an execution gas counter.
  - Gas Limit: Defaults to 10,000 instructions max to prevent infinite loops.
  - Fail-Safe: Attempting an unknown opcode raises `ScribeError::InvalidOpcode`. Exceeding gas raises `ScribeError::OutOfGas`.

---

## 4. Integration Protocol (Rust ↔ Python)

The Python runtime interfaces with NeuroDSL via Maturin extension module `vireon_neuro_dsl`:

```python
import vireon_neuro_dsl

# Compile source .ndsl string to binary bytecode
bytecode = vireon_neuro_dsl.compile_ndsl("""
SET_AMP 50
SET_FREQ 100
SHAPE SQUARE 10
END
""")

# Execute bytecode on Scribe VM context
result = vireon_neuro_dsl.execute_bytecode(bytecode)
print("Execution Result:", result)
```

---

## 5. Security Model

- **Deterministic Replay**: Given identical bytecode and identical sensor inputs, `scribe` produces deterministic memory states.
- **Resource Sandboxing**: The VM operates entirely in memory with no raw OS syscall access.
