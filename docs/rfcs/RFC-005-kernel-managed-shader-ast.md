# RFC 005: Kernel-Managed Shader AST Sanitization

## Status
Proposed

## Motivation
RFC-001 proposed exposing GPU compute via WebGPU or WASI-NN. Unlike CPUs, which have mature, hardware-enforced MMUs (Memory Management Units) for strict context isolation, GPUs rely heavily on the driver software to isolate VRAM. A malicious vendor plugin could craft raw SPIR-V or PTX shader bytecode that executes an out-of-bounds array read, allowing them to scrape the VRAM of a competing vendor's plugin.

## Proposed Architecture
We propose that the Kernel acts as a strictly validating compiler for all GPU compute.
1. Providers are strictly banned from uploading pre-compiled SPIR-V or PTX bytecode.
2. Providers must submit mathematical operations using a high-level Abstract Syntax Tree (AST) defined by VIREON.
3. The VIREON Kernel traverses the AST, injects rigorous bounds-checking instructions at every memory access node, and natively compiles the sanitized AST into SPIR-V.
4. Only this Kernel-sanitized bytecode is dispatched to the GPU.

## Open Questions
- Does injecting software bounds-checks into every GPU shader memory access ruin the performance gains that necessitated GPU compute in the first place?
- Should we restrict GPU compute to a highly constrained subset of operations (e.g., dense Matrix Multiplication only) where the Kernel can pre-calculate the exact VRAM bounds before execution?

## Next Steps
Solicit feedback from graphics driver engineers and cryptography experts regarding known sandbox escapes in SPIR-V compilation.
