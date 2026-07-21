# RFC 001: WASM GPU Pass-through for Neural Decoding

## Status
Proposed

## Motivation
The VIREON ecosystem heavily relies on WASM/microVMs to isolate untrusted vendor plugins (e.g., proprietary clinical decoders). However, neural decoding algorithms often rely on heavy matrix multiplication, which standard CPU-bound WASM struggles to execute within strict real-time constraints (e.g., 30kHz).
If vendors cannot access hardware acceleration (GPUs or Neural Engines), they will refuse to adopt the VIREON sandboxing model.

## Proposed Architecture
We propose implementing a secure, limited WebGPU or WASI-NN (Neural Network) interface at the kernel boundary.
1. The kernel exposes a safe, abstract tensor-computation API to the WASM environment.
2. The plugin requests tensor operations.
3. The kernel executes the operation on the host GPU using native CUDA/Metal/Vulkan drivers.
4. The kernel writes the resulting tensor back to the WASM linear memory.

## Open Questions & Vendor Considerations
- **Security**: Can a malicious plugin craft a tensor shape or operation that crashes the host GPU or performs a denial-of-service (DoS) attack on the kernel?
- **Determinism**: Are floating-point matrix operations across different host GPUs deterministic enough to guarantee scientific reproducibility of the trace bundles? (Historically, CUDA FP32 operations are notoriously non-deterministic across different GPU architectures).

## Next Steps
We request comments from vendor cryptography and ML engineering teams on the minimum viable tensor operations required for their decoders.
