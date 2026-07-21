# VIREON Architecture Guide

This guide details the structural design of the VIREON runtime.

## Core Components
1. **SimulationBuilder**: The factory that constructs the initial `StateStore` and resolves plugin dependencies via topological sort.
2. **EventBus**: The unidirectional routing layer for telemetry.
3. **PluginRegistry**: The capability-enforcing loader for third-party libraries.
4. **StateStore (formerly DigitalTwin)**: The immutable representation of the simulation at time *t*.

For deeper rationale, please see the `DESIGN_RATIONALE.md` document.
