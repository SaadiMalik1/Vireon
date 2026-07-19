# Copyright 2026 VIREON Contributors
# Universal Event Schema Registry

from typing import Any, Dict, Optional
from pydantic import BaseModel, Field

class BaseEvent(BaseModel):
    """Base universal event structure."""
    topic: str = Field(..., description="Routing topic")
    source_id: str = Field(..., description="Provider ID that emitted the event")
    timestamp: float = Field(..., description="Simulation clock timestamp")

class TelemetryEvent(BaseEvent):
    topic: str = "telemetry"
    channel: int
    value: float
    unit: str = "uV"

class ThreatDetectedEvent(BaseEvent):
    topic: str = "threat.detected"
    threat_class: str = Field(..., description="e.g., 'stimulation_leakage', 'spoofing'")
    confidence: float = Field(..., ge=0.0, le=1.0)
    evidence: Dict[str, Any] = Field(default_factory=dict)

class BatteryChangedEvent(BaseEvent):
    topic: str = "hardware.battery"
    voltage: float
    percentage: float = Field(..., ge=0.0, le=100.0)

class PacketReceivedEvent(BaseEvent):
    topic: str = "protocol.packet"
    payload: bytes
    protocol_type: str = "BLE"

class FirmwareFaultEvent(BaseEvent):
    topic: str = "firmware.fault"
    fault_code: int
    register_state: Dict[str, int]

class SimulationStartedEvent(BaseEvent):
    topic: str = "simulation.started"
    seed: Optional[int] = None
