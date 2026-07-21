# VIREON Reference Documentation

Welcome to the official documentation for the **VIREON** ecosystem, an advanced Virtual Laboratory for Brain-Computer Interface (BCI) Security and Neuroethics.

## Overview

The rapid advancement of invasive and non-invasive BCIs introduces unprecedented security and ethical risks—from theoretical "neural ransomware" to cognitive state inference vulnerabilities. VIREON is built to model these threats safely in a digital environment before they manifest in clinical reality. 

### Core Features

1. **High-Fidelity State Store:** Emulates the physical constraints of an implantable/wearable BCI, including battery sag, ADC saturation, electrode impedance variance, and thermal tissue constraints.
2. **Deep Learning SecurityEngine:** An onboard Intrusion Detection System that falls back gracefully from a PyTorch-based Deep Autoencoder to a lightweight Numpy-based Linear Autoencoder, detecting anomalies in sub-millisecond windows.
3. **Standards-Based Threat Intelligence:** Directly integrates with established cybersecurity frameworks (STRIDE, MITRE) to map mathematical anomalies to real-world threat vectors.
4. **Strict Ecosystem Separation:** Employs a decoupled core engine with strict capability boundaries to support un-trusted vendor firmware plugins.

---

## Documentation Navigation

This documentation is divided into extensive standalone guides:

### 1. Architecture & Ecosystem Design
- **[Ecosystem Overview](architecture/ECOSYSTEM.md)**: Strict ownership mapping separating `vireon` (Framework/SDK), `vireon-lab` (Educational), and `neurodsl`.
- **[Architectural Boundaries](architecture/ARCHITECTURAL_BOUNDARIES.md)**: Boundaries between subsystems.
- **[Plugin Lifecycle Management](architecture/PLUGIN_LIFECYCLE.md)**: The state machine that safely discovers, validates, and spins up third-party plugins.
- **[Configuration Architecture](architecture/CONFIGURATION_ARCHITECTURE.md)**: Details on the declarative YAML configurations that govern threat models and capabilities.
- **[Testing Architecture](architecture/TESTING_ARCHITECTURE.md)**: Explains the multi-layered testing paradigm used to validate external plugins and the core engine.
- **[Versioning Strategy](architecture/VERSIONING_STRATEGY.md)**: SemVer guidelines to ensure external plugins remain compatible across SDK releases.

### 2. Development & Integration
- **[API & Interfaces](api/api.md)**: Python API reference detailing the `vireon.sdk` contracts and `vireon.core` orchestration.
- **[Plugin Development Guide](guides/plugin-development.md)**: How to write custom Firmware Providers and capabilities using the VIREON SDK.

### 3. Theory & Mechanics
- **[Physics Constraints](reference/physics.md)**: Physics boundary conditions and integration limits for the simulations.
- **[Threat Modeling](reference/threat-models/README.md)**: Comprehensive explanation of the SecurityEngine, Attack Surface, and how the standards-based Threat Intelligence is parsed.
- **[Standards Derivation Log](reference/STANDARDS-DERIVATION-LOG.md)**: The central architectural decision record tracing the alignment with clinical and cybersecurity industry standards.
- **[Glossary & Formal Definitions](reference/glossary.md)**: Mathematical and structural bounds defining the scope of theoretical attacks.
- **[Frequently Asked Questions](reference/faq.md)**: Troubleshooting installation, dashboards, and stream capturing.

---

*VIREON is an open-source project dedicated to the safe, transparent, and ethical advancement of neural engineering.*
