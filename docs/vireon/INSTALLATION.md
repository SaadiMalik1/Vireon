# Installation

## Overview
This is the canonical installation guide for the VIREON ecosystem. Do not refer to individual repository `README.md` files for full installation instructions, as those are minimal by design.

## Quick Install (Production)

If you simply want to run VIREON with default capabilities:
```bash
pip install vireon[all]
```

## Development Installation

For contributors looking to modify VIREON, or develop plugins and providers, you must use the `workspace` environment.

1. **Clone the ecosystem:**
```bash
git clone https://github.com/VIREON/workspace.git
cd workspace
# Note: The workspace repository contains submodules or scripts to pull vireon, neurodsl, and vireon-lab
```

2. **Run the ecosystem via Docker Compose:**
```bash
docker compose up --build
```
This spins up the VIREON core, the `vireon-lab` Jupyter environment, and required databases.

## Vendor Development

If you are a vendor developing a new Plugin or Provider for the `vireon` SDK:
- Install the SDK using `pip install vireon-sdk`.
- Follow the [Plugin SDK Design](./PLUGIN_SDK_DESIGN.md) guide.
- You do *not* need to clone the entire workspace unless you are running full integration tests.

## Educational Users

If you are a student or researcher intending to run tutorials:
- Navigate to the `vireon-lab` repository.
- Use the quick-start instructions in `vireon-lab/README.md`.
- Or, use the hosted VIREON Lab environment (if available).

## CI / Automated Environments

For continuous integration, we recommend using the `vireon` Docker image as a base:
```dockerfile
FROM vireon:latest
```
This ensures the Rust toolchain (for `neurodsl`) and system dependencies are correctly configured.
