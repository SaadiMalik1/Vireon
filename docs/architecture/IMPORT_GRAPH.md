# VIREON Ecosystem Import Graph

This document isolates the internal Python/Rust import flows, validating architectural boundaries.

## 1. Python Namespace Boundaries

```mermaid
graph TD
    vireon.runtime.coordinator --> vireon.sdk.base_interfaces
    vireon.runtime.coordinator_builder --> vireon.sdk.base_interfaces
    vireon.runtime.plugin_registry --> vireon.sdk.base_interfaces
    
    vireon.libraries.attack_factory --> vireon.sdk.base_interfaces
    vireon.libraries.attack_factory --> vireon.runtime.utils
    
    providers.physics.thermal --> vireon.sdk.base_interfaces
    providers.dynamics.kuramoto --> vireon.sdk.base_interfaces
    providers.security.zta --> vireon.sdk.base_interfaces
```

## 2. Forbidden Import Enforcement
The import graph guarantees that no `providers.*` or `vireon.libraries.*` namespace is ever imported statically into `vireon.runtime.*`. Registration occurs strictly at runtime via dynamic instantiation.
