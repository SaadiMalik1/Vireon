> [!NOTE]
> **Notice:** This document is an internally generated, AI-assisted self-review produced during development. It is not an independent or third-party audit.

# VIREON System Limitations

This document lists the technical and operational limitations verified against the current `vireon` codebase (v1.1.0).

## 1. Operating System & Sandboxing Primitives
- **Conditional Seccomp Enforcement:** `set_seccomp_strict_mode()` in `vireon/runtime/sandbox.py` only issues OS-level `prctl(PR_SET_SECCOMP, SECCOMP_MODE_STRICT)` syscalls when the environment variable `VIREON_ENFORCE_SECCOMP=1` is explicitly set. In default development and testing environments, seccomp execution is bypassed to avoid unexpected test-process termination.
- **Linux Platform Restriction:** OS-level isolation mechanisms (`prctl`, `PR_SET_NO_NEW_PRIVS`, `SECCOMP_MODE_STRICT`) are Linux-specific. On non-Linux platforms (macOS, Windows), `sandbox.py` sandbox application methods safely return `False`.
- **eBPF Profile Translation:** Network and syscall capability manifests generate Seccomp-BPF JSON profiles (`SeccompProfileGenerator`), but kernel-level eBPF bytecode loading is currently a proposed specification (ADR-006).

## 2. Capability Engine & Security Defaults
- **Optional Signature Verification:** `CapabilityEngine.validate_manifest()` verifies cryptographic Ed25519 vendor signatures (`manifest.verify_signature`) only when a `trusted_public_key` argument is explicitly provided. When unsupplied, capability manifests are validated solely against access flags.
- **Global Security Bypass:** If `config.security.enabled` is set to `False` in `ExperimentConfig`, `CapabilityEngine.validate_manifest()` short-circuits and approves all requested capabilities without verification.

## 3. Performance & Real-Time Constraints
- **Python Memory & GC Overhead:** High-frequency digital twin tick loops (e.g., 30 kHz sampling) in pure Python create heap allocation and garbage collection overhead. Zero-allocation execution relies on pre-allocated NumPy buffers or the Rust `neurodsl` / `scribe` bytecode VM.
- **RTOS Scheduling:** Sub-millisecond real-time preemption guarantees require a Linux kernel compiled with the `PREEMPT_RT` patch and pinned CPU cores.

## 4. Hardware Realism & Cyber-Physical Emulation
- **Hardware Mode Emulation:** In `DigitalTwin(hardware_mode=True)`, thermal shutdown and hardware failsafes trigger software state transitions (`HARDWARE_SHUTDOWN`). Physical serial, SPI, or implant hardware controllers are emulated via software adapters.
