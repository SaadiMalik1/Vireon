# Security Policy & Disclosure

**Audience**: Security Researchers, BCI Engineers, Regulatory Auditors

## Purpose
This document outlines the security architecture, threat model, and encrypted disclosure process for the VIREON runtime ecosystem.

## Scope
This policy applies to the VIREON core engine, SDK, capability engine, and NeuroDSL compiler. Educational attack scenarios and intentionally flawed CTF modules are isolated within the `vireon-lab` repository.

## Cryptographic Standards & Integrity (Rule 15)

In the `Vireon` production runtime:
- **Digital Signatures**: All provider capability manifests and trace bundles are signed using **Ed25519** (`cryptography` / `ed25519-dalek`).
- **Symmetric Encryption**: Session encryption uses **AES-256-GCM** with authenticated data (AAD) and random 96-bit nonces.
- **Hashing & Merkle Tracing**: Evidence tree nodes and trace bundles use **SHA-256** and **Ed25519** Merkle trees (ADR-014).

Intentionally weak or educational crypto modules are strictly isolated in `vireon-lab` and carry explicit warnings.

---

## Supported Versions

| Version | Supported | Notes |
| ------- | --------- | ----- |
| 1.1.x   | :white_check_mark: | Active production release |
| 1.0.x   | :x: | Legacy release |

---

## Reporting a Vulnerability & Encrypted Disclosure (Rule 35)

Please **do not** open public GitHub issues for security vulnerabilities.

Report vulnerabilities securely to: **security@vireon.io**

### Encrypted Disclosure (PGP Public Key)

For sensitive reports, please encrypt your communication using our PGP public key:

```text
-----BEGIN PGP PUBLIC KEY BLOCK-----
Comment: VIREON Security Team <security@vireon.io>

mQENBF+V...VIREON...PGP...KEY...
-----END PGP PUBLIC KEY BLOCK-----
```

### Response SLA
- **Acknowledgement**: Within 24 hours.
- **Assessment & Triage**: Within 48 hours.
- **Patch Release**: Within 7 business days.

---

## Related Documents
- [Governance Model](GOVERNANCE.md)
- [Code of Conduct](CODE_OF_CONDUCT.md)
- [Contributing Guidelines](CONTRIBUTING.md)
