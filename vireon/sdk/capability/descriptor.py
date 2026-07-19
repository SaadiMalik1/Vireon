from typing import List, Optional, Dict
from pydantic import BaseModel, Field

class CapabilityDescriptor(BaseModel):
    """
    Universal ABI Descriptor for a VIREON Provider.
    Defines capabilities, interfaces, and permissions.
    """
    id: str = Field(..., description="Unique provider ID (e.g., 'neuroips')")
    implements: List[str] = Field(default_factory=list, description="Interfaces implemented (e.g., 'IIDSProviderV1')")
    requires: Dict[str, str] = Field(default_factory=dict, description="Required runtime features and dependencies")
    permissions: List[str] = Field(default_factory=list, description="Requested permissions (e.g., 'state.read', 'event.publish')")
    features: List[str] = Field(default_factory=list, description="Optional features (e.g., 'spectral', 'ewma')")
    latency: str = Field(default="best-effort", description="Latency class: 'best-effort', 'soft-realtime', 'hard-realtime'")
