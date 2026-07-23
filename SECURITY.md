# Security Policy & Disclosure

**Audience**: Security Researchers, BCI Engineers, Open Source Contributors

## Purpose
This document outlines the security architecture, threat model, and disclosure process for the VIREON runtime ecosystem.

## Scope
This policy applies to the VIREON core engine, SDK, capability engine, and NeuroDSL compiler. Educational attack scenarios and CTF modules are isolated within the `vireon-lab` repository.

---

## 1. Security Mechanisms & Disclosures

### Cryptographic Signatures & Integrity
- **Ed25519 Manifest & Trace Signatures**: Capability manifests and trace bundles support Ed25519 asymmetric signatures. Note that `CapabilityEngine.validate_manifest()` verifies signatures when a `trusted_public_key` parameter is provided to the call.
- **Hashing & Merkle Tracing**: State graph mutation trees generate SHA-256 binary digests and rolling CRC32 hex checksums (ADR-014).

### Process Sandboxing Defaults
- **Conditional OS Seccomp Enforcement**: `sandbox.py` utilizes Linux `prctl(PR_SET_NO_NEW_PRIVS)`. Strict mode seccomp filters (`SECCOMP_MODE_STRICT`) are executed **only** when the environment variable `VIREON_ENFORCE_SECCOMP=1` is set. In default development or test environments, seccomp execution logs a debug message and returns `True` without applying system call restrictions.

---

## 2. Supported Versions

| Version | Supported | Maturity / Classification |
| ------- | --------- | ------------------------- |
| 1.1.x   | :white_check_mark: | Active Pre-Alpha Research Prototype |
| < 1.1   | :x: | Deprecated |

---

## 3. Reporting a Vulnerability

Please **do not** open public GitHub issues for security vulnerabilities.

Report vulnerabilities securely to: **security@vireon.io**

### Response SLA
- **Acknowledgement**: Within 24 hours.
- **Assessment & Triage**: Within 48 hours.
- **Patch Release**: Within 7 business days.

---

## 4. Related Documents
- [System Limitations](LIMITATIONS.md)
- [Known Issues](KNOWN_ISSUES.md)
- [Governance Model](GOVERNANCE.md)
- [Contributing Guidelines](CONTRIBUTING.md)
