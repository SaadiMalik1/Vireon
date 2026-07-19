# Copyright 2026 VIREON Contributors
# Universal Provider Interfaces - V1

from abc import ABC, abstractmethod
from typing import Any

class IProviderV1(ABC):
    """
    Base Provider Interface.
    All providers must expose these baseline lifecycle and health endpoints.
    """
    @abstractmethod
    def health(self) -> dict:
        """Returns health status, metrics, and diagnostics."""
        pass

class IFirmwareProviderV1(IProviderV1):
    @abstractmethod
    def write_memory(self, address: int, data: bytes) -> bool:
        pass

    @abstractmethod
    def read_memory(self, address: int, size: int) -> bytes:
        pass

class IPhysicsProviderV1(IProviderV1):
    @abstractmethod
    def step_physics(self, dt: float) -> None:
        """Advance physical constraints (tissue temp, battery sag)."""
        pass

class ITelemetryProviderV1(IProviderV1):
    @abstractmethod
    def record_sample(self, channel: int, value: float) -> None:
        pass

class IThreatModelProviderV1(IProviderV1):
    @abstractmethod
    def inject_anomaly(self) -> None:
        pass

class IIDSProviderV1(IProviderV1):
    @abstractmethod
    def analyze_window(self, data: Any) -> bool:
        """Returns True if anomaly detected."""
        pass

class IProtocolProviderV1(IProviderV1):
    @abstractmethod
    def parse_packet(self, packet: bytes) -> dict:
        pass

class IClinicalProviderV1(IProviderV1):
    @abstractmethod
    def evaluate_biomarker(self, data: Any) -> dict:
        pass

class IVisualizationProviderV1(IProviderV1):
    @abstractmethod
    def render_frame(self) -> bytes:
        pass

class IStorageProviderV1(IProviderV1):
    @abstractmethod
    def store_blob(self, key: str, data: bytes) -> None:
        pass

class ISchedulerProviderV1(IProviderV1):
    @abstractmethod
    def next_tick(self) -> float:
        pass

class IDecoderProviderV1(IProviderV1):
    @abstractmethod
    def decode_intent(self, neural_data: Any) -> dict:
        pass

class IBenchmarkProviderV1(IProviderV1):
    @abstractmethod
    def run_suite(self) -> dict:
        pass
