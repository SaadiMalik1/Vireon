> [!NOTE]
> **Notice:** This document is an internally generated, AI-assisted self-review produced during development. It is not an independent or third-party audit.

# VIREON Known Issues & Tracked Deprecations

This document tracks active technical issues, environment gotchas, and security-relevant default behaviors in `vireon`.

## 1. CI / Environment Dependencies
- **GitHub Actions Node.js 20 Deprecation:** GitHub Actions runner workflows display deprecation warnings for `Node.js 20` when running standard actions (`actions/checkout@v4`, `actions/setup-python@v5`). Runs currently execute under forced Node 24 policy on runner hosts.

## 2. Security & Capability Enforcement Defaults
- **Seccomp Disabled by Default in Test Suite:** The OS-level seccomp sandbox (`vireon/runtime/sandbox.py`) requires `VIREON_ENFORCE_SECCOMP=1` to be active. If unset during standard test runs, `set_seccomp_strict_mode()` logs a debug message and returns `True` without applying process strict mode.
- **Unauthenticated Manifest Validation Default:** When `CapabilityEngine.validate_manifest()` is called without passing `trusted_public_key`, Ed25519 signature checks are skipped and manifests are accepted based on requested flags alone.
- **Security Master Switch:** Setting `config.security.enabled = False` bypasses all capability validation in `CapabilityEngine`.

## 3. Platform & Hardware Emulation
- **Non-Linux Platform Fallback:** Non-Linux operating systems (macOS/Windows) cannot execute Linux `prctl` syscalls. Sandbox security calls log warnings and return `False`.
- **Software Failsafe Emulation:** Hardware mode failsafe triggers (`HARDWARE_SHUTDOWN`) rely on internal software state updates rather than physical GPIO or hardware interrupt pins.
