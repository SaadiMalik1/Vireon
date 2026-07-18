# VIREON

## What is this?
VIREON is the core runtime and SDK for the VIREON ecosystem. It provides the foundational architecture for plugin lifecycle management, provider execution, and the integration of the NeuroDSL language.

## Who is it for?
This repository is for core contributors, framework engineers, and developers building integrations, plugins, or providers on top of the VIREON SDK.

## Installation
```bash
pip install vireon[all]
```
For development installation, refer to the official [Installation Guide](docs/INSTALLATION.md).

## Quick Example
```python
from vireon.core import ReplayEngine
engine = ReplayEngine()
engine.start()
```

## Where is the documentation?
The canonical documentation for the entire VIREON ecosystem is located in the `vireon` repository under `docs/`.

## Repository Status
Active / Maintained. This is the canonical core repository.
