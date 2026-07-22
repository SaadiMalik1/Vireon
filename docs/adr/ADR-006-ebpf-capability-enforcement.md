# ADR 006: eBPF Capability Enforcement

## Status
Accepted — Implemented (`prctl(PR_SET_NO_NEW_PRIVS)` & `set_seccomp_strict_mode`)


## Context
The ecosystem relies on "Capability Manifests" (see ADR-003) to grant permissions to untrusted vendor plugins. Currently, capability enforcement is theoretical or application-level (e.g., the Kernel checking a boolean before invoking an API).
Application-level capability checks are insufficient. A malicious or compromised native plugin could bypass the runtime entirely and issue raw syscalls (e.g., `socket()`, `open()`) to exfiltrate proprietary IP or manipulate the host system.

## Decision
We will enforce capability manifests using OS-level primitives, specifically **eBPF (Extended Berkeley Packet Filter)** for network/system calls, and **cgroups** for resource isolation on Linux hosts.
- Before a provider is spawned, the Kernel translates its YAML Capability Manifest into strict eBPF profiles and Seccomp filters.
- If a plugin requests "No Network" but attempts a socket syscall, the OS kernel terminates the process, and the VIREON runtime logs a security violation.

## Consequences
- **Positive**: Provides true zero-trust security. Application-level bypasses are impossible.
- **Positive**: Hardens the runtime against zero-day exploits inside vendor binaries.
- **Negative**: Ties the deepest security guarantees of the runtime to Linux-specific primitives, increasing the complexity of porting the full secure runtime to Windows/macOS natively (though Windows Subsystem for Linux or Docker mitigates this).
