# Copyright 2026 VIREON Contributors
# Injected Runtime API Services

from abc import ABC, abstractmethod
from typing import Any

class IStateAPI(ABC):
    """Scoped State Access."""
    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any: pass
    
    @abstractmethod
    def set(self, key: str, value: Any) -> None: pass

class ITelemetryAPI(ABC):
    """Scoped Telemetry Access."""
    @abstractmethod
    def publish(self, channel: int, value: float) -> None: pass

class ILoggingAPI(ABC):
    """Structured Provider Logging."""
    @abstractmethod
    def debug(self, msg: str) -> None: pass
    
    @abstractmethod
    def info(self, msg: str) -> None: pass
    
    @abstractmethod
    def warn(self, msg: str) -> None: pass
    
    @abstractmethod
    def error(self, msg: str) -> None: pass

class IClockAPI(ABC):
    """Simulation Time Synchronization."""
    @abstractmethod
    def now(self) -> float: pass

class RuntimeServices:
    """
    Dependency Injection Container.
    The orchestrator provides only the specific APIs requested in the CapabilityDescriptor.
    """
    def __init__(self, 
                 state: IStateAPI = None, 
                 telemetry: ITelemetryAPI = None, 
                 logging: ILoggingAPI = None,
                 clock: IClockAPI = None):
        self.state = state
        self.telemetry = telemetry
        self.logging = logging
        self.clock = clock
