# Copyright 2026 VIREON Contributors
# Provider Lifecycle State Machine

from enum import Enum, auto

class ProviderState(Enum):
    """
    The 13-stage deterministic lifecycle of a VIREON Provider.
    """
    UNLOADED = auto()
    DISCOVERED = auto()
    VALIDATING_MANIFEST = auto()
    RESOLVING_DEPENDENCIES = auto()
    NEGOTIATING_CAPABILITIES = auto()
    INITIALIZING = auto()
    READY = auto()
    STARTING = auto()
    RUNNING = auto()     # Tick state
    PAUSED = auto()      # Pause/Resume boundary
    CHECKPOINTING = auto()
    SHUTTING_DOWN = auto()
    ERROR = auto()

class ILifecycleManager:
    """Interface that orchestrators must implement to drive provider states."""
    def transition(self, provider_id: str, target_state: ProviderState) -> bool:
        pass

    def perform_health_check(self, provider_id: str) -> dict:
        pass
