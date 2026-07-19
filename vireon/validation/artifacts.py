# Copyright 2026 VIREON Contributors
# Validation Artifact Schemas

from pydantic import BaseModel, Field
from typing import List, Dict, Any

class ValidationArtifact(BaseModel):
    """Base class for all artifacts produced during simulation."""
    artifact_id: str = Field(..., description="UUID of the artifact")
    run_id: str = Field(..., description="UUID of the simulation run")
    provider_id: str = Field(..., description="Provider that generated this")

class TelemetryArtifact(ValidationArtifact):
    data_uri: str = Field(..., description="Pointer to time-series blob")

class ExecutionTrace(ValidationArtifact):
    state_transitions: List[Dict[str, Any]]
    events_published: int

class ThreatReport(ValidationArtifact):
    anomalies_detected: int
    confidence_scores: List[float]

class ReplayPackage(BaseModel):
    """
    Deterministic reproduction package.
    """
    run_id: str
    provider_versions: Dict[str, str]
    random_seeds: Dict[str, int]
    configuration: Dict[str, Any]
    timeline_uri: str
