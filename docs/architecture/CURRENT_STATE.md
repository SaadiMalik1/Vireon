# Ecosystem Current State

## Repository Graph
```mermaid
graph TD
    Workspace[workspace (Distributed Monorepo)]
    Vireon[vireon (Core SDK & Runtime)]
    VireonLab[vireon-lab (UI & Tools)]
    NeuroDSL[neurodsl (Rust Simulation Engine)]
    GitHub[.github (CI/CD Ecosystem)]

    Workspace --> Vireon
    Workspace --> VireonLab
    Workspace --> NeuroDSL
    Workspace --> GitHub
    VireonLab --> Vireon
    Vireon --> NeuroDSL
```

## Dependency Graph
```mermaid
graph TD
    subgraph vireon-lab
        CLI[vireon_lab.cli]
        UI[vireon_lab.ui]
    end
    subgraph vireon
        SDK[vireon.sdk]
        Runtime[vireon.runtime]
        Providers[vireon.providers]
    end
    subgraph neurodsl
        PyExt[python_ext]
        Engine[neurodsl_core]
        Forge[forge]
        Scribe[scribe]
    end
    CLI --> SDK
    UI --> SDK
    Runtime --> PyExt
    Providers --> SDK
    PyExt -.-> Engine
    Engine --> Forge
    Engine --> Scribe
```

## Package Graph
```mermaid
graph TD
    pypi_vireon_lab[PyPI: vireon-lab]
    pypi_vireon[PyPI: vireon]
    pypi_neurodsl[PyPI: neurodsl]
    cargo_neurodsl[Cargo: neurodsl]
    cargo_forge[Cargo: forge]
    cargo_scribe[Cargo: scribe]

    pypi_vireon_lab --> pypi_vireon
    pypi_vireon --> pypi_neurodsl
    pypi_neurodsl -.-> cargo_neurodsl
```

## Import Graph (Python)
```mermaid
graph TD
    vireon.runtime --> vireon.sdk
    vireon.providers --> vireon.sdk
    vireon.providers --> vireon.runtime
    vireon_lab.app --> vireon.sdk
    vireon_lab.cli --> vireon.sdk
    vireon.runtime --> neurodsl
```

## Documentation Graph
```mermaid
graph TD
    DocsRoot[workspace/docs]
    ArchDocs[workspace/docs/architecture]
    ApiDocs[vireon/docs/api]
    GuideDocs[vireon-lab/docs/guides]
    RustDocs[neurodsl/docs/internals]

    DocsRoot --> ArchDocs
    DocsRoot --> ApiDocs
    DocsRoot --> GuideDocs
    DocsRoot --> RustDocs
```

## Ownership Graph
```mermaid
graph TD
    CoreTeam[Core Architecture Team]
    UI_Team[UI/UX Team]
    RustTeam[Simulation/Rust Team]
    DevOpsTeam[DevOps & SecOps]

    CoreTeam --> vireon
    UI_Team --> vireon-lab
    RustTeam --> neurodsl
    DevOpsTeam --> .github
```

## Architecture Graph
```mermaid
graph TD
    subgraph Presentation
        CLI
        UI
    end
    subgraph Orchestration
        SimulationBuilder
        EventBus
        StateStore
    end
    subgraph Providers
        Authentication
        Security
        Physics
        Protocol
    end
    subgraph Engine
        NeuroDSL_Rust
    end

    Presentation --> Orchestration
    Orchestration --> Providers
    Orchestration --> Engine
```

## CI Graph
```mermaid
graph TD
    Push[git push] --> Validation[workspace/validate]
    Validation --> Lint[ruff, cargo fmt]
    Validation --> Test[pytest, cargo test]
    Validation --> ArchTest[pytest tests/architecture]
    Validation --> Build[build wheels]
```

## Docker Graph
```mermaid
graph TD
    BaseImage[vireon-base]
    LabImage[vireon-lab]
    TestImage[vireon-test]
    
    BaseImage --> LabImage
    BaseImage --> TestImage
```

## Release Graph
```mermaid
graph TD
    Tag[git tag] --> Build[GitHub Actions Build]
    Build --> PublishPyPI[Publish to PyPI]
    Build --> PublishCrates[Publish to Crates.io]
    Build --> DockerPush[Push Docker Image]
```

## Testing Graph
```mermaid
graph TD
    Unit[Unit Tests]
    Integration[Integration Tests]
    Architecture[Architecture Tests]
    Regression[Regression Tests]
    Contract[Contract Tests]

    Unit --> Integration
    Integration --> Regression
    Architecture --> Unit
```

## Plugin Graph
```mermaid
graph TD
    PluginRegistry[vireon.runtime.plugin_registry]
    AuthPlugin[AuthPlugin]
    ThreatPlugin[ThreatPlugin]
    PhysicsPlugin[PhysicsPlugin]

    AuthPlugin --> PluginRegistry
    ThreatPlugin --> PluginRegistry
    PhysicsPlugin --> PluginRegistry
```

## Provider Graph
```mermaid
graph TD
    IProvider[vireon.sdk.base_interfaces.IProvider]
    ThermalPhysics[providers.physics.thermal]
    KuramotoDynamics[providers.dynamics.kuramoto]
    ZTA[providers.security.zta]

    ThermalPhysics --> IProvider
    KuramotoDynamics --> IProvider
    ZTA --> IProvider
```

## SDK Graph
```mermaid
graph TD
    SDK_Root[vireon.sdk]
    Interfaces[base_interfaces]
    Types[types]
    Utils[signal_utils]
    Errors[exceptions]

    SDK_Root --> Interfaces
    SDK_Root --> Types
    SDK_Root --> Utils
    SDK_Root --> Errors
```

## Workspace Graph
```mermaid
graph TD
    Workspace[workspace]
    Workspace --> Submodules
    Submodules --> vireon
    Submodules --> vireon-lab
    Submodules --> neurodsl
```

## Knowledge Graph
```mermaid
graph TD
    KnowledgeBase[workspace/docs/knowledge]
    FDA[FDA Regulations]
    ISO[ISO 14971]
    IEC[IEC 62304]
    ThreatModels[Threat Models]

    KnowledgeBase --> FDA
    KnowledgeBase --> ISO
    KnowledgeBase --> IEC
    KnowledgeBase --> ThreatModels
```
