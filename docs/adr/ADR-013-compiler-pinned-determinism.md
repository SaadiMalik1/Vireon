# ADR 013: Compiler-Pinned Determinism

## Status
Accepted — Implemented (v1.1.0 — CompilerPin SHA-256 build verification)

## Context
If a Trace Bundle is used for regulatory submission (e.g., FDA clearance), the results must be mathematically reproducible. If the VIREON runtime is recompiled with a newer version of `rustc` or `gcc`, floating-point optimizations (like Fused Multiply-Add) or struct alignment changes can alter the mathematical outcome of the physics engine at the 15th decimal place. Over millions of ticks, this chaotic divergence completely invalidates the regulatory trace bundle.

## Decision
We mandate **Compiler-Pinned Determinism**.
- The VIREON Kernel and SDK must disable all compiler flags that introduce floating-point non-determinism (e.g., `-ffast-math` is strictly banned).
- All Trace Bundles must encapsulate the exact cryptographic hash of the compiler toolchain, the OS environment (via a Nix Flake or equivalent lockfile), and the CPU instruction set (e.g., AVX-512 vs SSE4) used during the run.
- To achieve identical reproduction, reviewers must use the identical toolchain hash. The runtime must warn if the host environment does not match the Trace Bundle's Genesis block.

## Consequences
- **Positive**: Guarantees true scientific and regulatory reproducibility over decades.
- **Negative**: Increases the difficulty of upgrading the underlying toolchains, as "bug fixes" in compiler math might intentionally break backward compatibility with old Trace Bundles.
