# VIREON Architecture Constitution

This document is the single source of truth for the project. Every future feature, module, plugin, interface, or subsystem must be justified against this document. 

## 1. Mission

VIREON's mission is to provide a vendor-neutral, plugin-first validation framework for neurotechnology and brain-computer interfaces (BCIs), enabling secure, reproducible, and standardized testing without compromising proprietary intellectual property.

## 2. Vision

Over the next 5–10 years, VIREON will become the ubiquitous foundational infrastructure for neurotechnology validation—the equivalent of ROS or LLVM for the neuro-device ecosystem—where industry leaders (e.g., Neuralink, Synchron, Medtronic), researchers, and regulators seamlessly plug in proprietary components to benchmark safety, security, and efficacy in a universally trusted runtime.

## 3. Problem Statement

The neurotechnology industry currently lacks a standardized, secure, and vendor-neutral validation ecosystem. Developers are forced to build bespoke simulation and testing environments that tightly couple proprietary firmware, hardware emulation, and clinical models. This fragmentation prevents interoperability, hinders independent security validation, and makes scientific reproducibility across different devices impossible without exposing sensitive IP.

## 4. Why Existing Tools Are Insufficient

- **BrainFlow, MNE, OpenBCI**: These are data acquisition and signal processing tools. They are not designed for full-stack device simulation, firmware validation, or security threat modeling.
- **ROS, Gazebo, CARLA**: These are powerful orchestration and simulation frameworks for robotics and autonomous vehicles, but they lack the domain-specific primitives for neurophysiology, neural decoding, and clinical telemetry.
- **Simulink, ns-3**: These provide general-purpose system or network simulation, but they do not natively support the plugin-based isolation needed for vendors to execute proprietary biomedical algorithms without source code disclosure.
- **QEMU**: While excellent for hardware emulation, QEMU knows nothing about the brain, tissue interfaces, or clinical context, and must be orchestrated by a higher-level framework to test neuro-device efficacy.

VIREON fills the gap by providing the high-level runtime, orchestration, and validation interfaces specifically tailored to neurotechnology, leaving the low-level implementations to vendor plugins and external emulators.

## 5. Core Principles

- **Vendor Neutrality**: The framework must favor no specific hardware, protocol, or decoding paradigm.
- **Plugin-First Architecture**: Every domain-specific implementation must be a plugin.
- **Language Independence**: Plugins must interact via stable, language-agnostic interfaces (e.g., FFI, IPC, gRPC).
- **Explicit Assumptions**: All capabilities and constraints must be explicitly declared and validated at runtime.
- **Scientific Reproducibility**: Execution must be deterministic, allowing any researcher with the same plugins to reproduce validation results.
- **Security by Design**: The runtime must enforce isolation and capability boundaries between untrusted plugins.
- **Composability**: Subsystems must be independent and easily chained together.
- **Extensibility**: The system must easily adapt to future, unknown neurotechnologies.
- **Evidence Before Claims**: Benchmarking and validation results must be derived from auditable simulation traces.
- **Open Interfaces, Proprietary Implementations**: The framework remains open-source; the vendor payloads remain closed.

## 6. Scope

**VIREON IS:**
- A validation runtime for neurotechnology.
- A research framework for reproducible science and security testing.
- A plugin ecosystem for vendor integrations.
- A benchmarking platform for clinical and security efficacy.

**VIREON IS NOT:**
- A replacement for implant firmware.
- A cycle-accurate hardware emulator (this is delegated to QEMU/etc).
- A medical device.
- A clinical decision system.
- A proprietary device simulator (it only orchestrates them).

## 7. Stakeholders

- **Academic Researchers**: Gain a reproducible environment to test new decoders or physiological models without building custom infrastructure.
- **Security Researchers**: Gain a standardized platform to model threats, exploit vulnerabilities, and test mitigations across diverse architectures.
- **Medical-Device Manufacturers**: Gain a robust validation pipeline to test firmware against rigorous safety benchmarks before physical deployment.
- **Neurotechnology Companies**: Gain an ecosystem to safely validate their proprietary integrations against open-source models without IP leakage.
- **Regulatory Researchers (e.g., FDA)**: Gain a standardized toolkit to evaluate the safety and security claims of new neuro-devices.

## 8. Assumptions

- **Acceptable**: Vendors will conform to defined SDK provider interfaces to run their proprietary plugins within VIREON.
- **Needs Validation**: The overhead of strict plugin isolation (IPC/WASM/etc.) allows for real-time or near-real-time high-fidelity physiological simulation.
- **Forbidden**: Distributed execution of the simulation across multiple nodes (preventing physical latency violations of 30kHz sync).
- **Unacceptable**: Implicit trust. We will no longer assume any plugin or vendor implementation is safe, correct, or non-malicious. All capabilities (e.g., file access, network access, twin state mutation) must be explicitly requested and granted via OS-level primitives (e.g., eBPF, cgroups).
- **Mandatory**: Simulation Fidelity. Every trace bundle MUST include a Fidelity Score quantifying the abstraction level to ensure regulatory relevance.

## 9. Design Philosophy

- **Runtime**: The runtime is a thin, language-agnostic orchestrator. **The runtime contains no domain-specific neurophysiological, firmware, or device logic. It provides only orchestration, scheduling, capability enforcement, lifecycle management, and deterministic execution.**
- **Providers**: The sole mechanism for extending the framework. Everything from logging to physics is a provider complying with a strict, versioned interface.
- **Plugins**: Untrusted binary or script packages that fulfill a provider interface, executed in a sandboxed or IPC boundary.
- **Validation**: Validation must be objective, deterministic, and based on artifacts emitted by the runtime, decoupled from the simulation itself.
- **Simulation**: Handled exclusively by plugins. The framework merely advances the global clock and routes state changes.
- **Digital Twins**: Abstract state representations defined by the models loaded. The framework provides the lock-free data structures, while plugins define the schema and physics.
- **Benchmarking**: Extracted as a separate layer that observes telemetry streams and scores performance against predefined criteria.

## 10. Long-Term Architecture

Five years from now, the VIREON runtime will be a minimalist, high-performance orchestration kernel (likely written in Rust or C++) exposing stable C-ABI and gRPC endpoints. It will contain zero neurotechnology-specific code. 
Instead, it will dynamically load a `FirmwareProvider` (from Neuralink), a `PhysicsProvider` (from a university), and a `ThreatModelProvider` (from a security firm), orchestrating them via a zero-trust capability capability manifest. Researchers will download VIREON, `pip/cargo install` their required vendor SDKs, and run deterministic compliance suites that execute seamlessly across multiple languages.

## 11. Non-Goals

- Building cycle-accurate processor emulators (delegate to QEMU).
- Developing proprietary clinical decoders.
- Creating a unified "standard" for brain data formats (delegate to LSL/NWB).
- Replacing hospital clinical software.

## 12. Success Criteria

- Vendors can integrate proprietary plugins without modifying the framework.
- Researchers can reliably reproduce validation results across different host machines.
- New devices can be added simply by swapping out plugins, without changing the runtime.
- New programming languages can be integrated through stable SDK interfaces.
- The educational platform can evolve independently as a consumer of the framework.

Ecosystem Success:

- Third-party plugins exist.
- Independent researchers publish using VIREON.
- External contributors maintain providers.
- Multiple programming languages are supported.
- Independent organizations adopt the SDK.


## 13. Architectural Risks

1. **Performance/Overhead (Technical)**: Strict isolation and IPC between plugins may introduce unacceptable latency for high-frequency physics/firmware emulation.
2. **Adoption (Organisational)**: Vendors may refuse to adopt the provider SDK interfaces if they are too complex or restrictive.
3. **Scientific Validity (Scientific)**: Abstracting physical and clinical phenomena behind generic interfaces may oversimplify complex neuro-physiological realities.
4. **Maintenance (Maintenance)**: Supporting language-agnostic bindings (FFI/WASM/gRPC) across multiple platforms requires significant engineering effort.

## 14. Guiding Question

*If every line of code disappeared tomorrow, what architectural ideas would still make VIREON worth rebuilding?*

The concept of a secure, vendor-neutral, plugin-first orchestration engine that strictly isolates proprietary implementations while enabling objective, reproducible validation of neurotechnology.


## 15. Architecture Invariants

1. The runtime shall never contain device-specific logic.
2. The runtime shall never contain clinical algorithms.
3. Plugins shall never bypass capability validation.
4. Every provider shall communicate only through public interfaces.
5. The runtime shall never directly depend on educational components.
6. The runtime shall remain vendor-neutral.
7. All external integrations must pass through SDK interfaces.
8. Simulation state shall never be mutated outside approved APIs.


## 16. Quality Attributes

Priority:
1. Security
2. Reproducibility
3. Extensibility
4. Interoperability
5. Maintainability
6. Performance
7. Portability
8. Usability


## 17. Trade-offs

We deliberately accept higher latency in exchange for plugin isolation.
We deliberately accept additional abstraction in exchange for vendor neutrality.
We deliberately accept higher engineering effort in exchange for language independence.


## 18. Architectural Constraints

- The runtime must never perform signal processing.
- The runtime must never implement firmware logic.
- The runtime must never contain protocol-specific code.
- The runtime must never embed hardware assumptions.
- The runtime must enforce a bifurcated clock scheduler (Virtual-Time vs. Wall-Time modes are mutually exclusive).
- The runtime must use OS-level primitives (eBPF, cgroups) for capability and Out-of-Memory (OOM) sandboxing.
- Multi-threaded providers must use deterministic threading libraries linked to the logical clock.
- The host must run an RTOS (`PREEMPT_RT`) for Wall-Time mode.
- Dynamic heap allocation (`malloc`/`new`) is banned in the simulation loop; pre-allocated Arenas only.
- ECC memory is mandated for FDA validation runs, alongside rolling CRC32 state checksums.
- Strict Roll-Forward Semantics: The runtime refuses legacy plugin manifests to prevent downgrade attacks.
- State Store numbers must strictly use `f64` precision.


## 19. Evolution Policy

Changing this constitution requires:
RFC -> ADR -> Maintainer approval -> Migration strategy -> Version increment


## 20. Failure Philosophy

Fail Closed:
Capability denied -> Plugin disabled -> Simulation continues

(NOT: Capability denied -> Runtime crash)


## 21. Compatibility Policy

- Provider SDK uses Semantic Versioning.
- API stability guarantees.
- Defined deprecation windows.
- Migration guarantees between major versions.


## 22. Testing Philosophy

Architecture is validated by:
- Contract tests
- Integration tests
- Compatibility tests
- Benchmark suites
- Deterministic replay
- Property testing


## 23. Architecture Governance

Architecture follows:
- RFCs
- ADRs
- Evidence
- Benchmarks
- Scientific validation

not personal preference.


## 24. Architectural Decision Test

Every new feature must answer:
1. Does this increase vendor neutrality?
2. Does this improve reproducibility?
3. Does this belong in the runtime?
4. Could this instead be a provider?
5. Does this introduce hidden coupling?
6. Can it be implemented externally?
7. Does it preserve deterministic execution?
8. Does it preserve language independence?
9. Does it preserve plugin isolation?
10. Is there benchmark evidence?

If any answer is "No", the proposal requires an RFC.
