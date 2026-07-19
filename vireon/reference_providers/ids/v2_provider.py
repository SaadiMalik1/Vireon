# Copyright 2026 VIREON Contributors
from typing import Any
import logging

from vireon.sdk.provider_interfaces.v1 import IIDSProviderV1
from vireon.sdk.capability.descriptor import CapabilityDescriptor
from vireon.reference_providers.ids.detection import SecurityEngine
from vireon.sdk.services.apis import RuntimeServices

logger = logging.getLogger(__name__)

def get_ids_descriptor() -> CapabilityDescriptor:
    return CapabilityDescriptor(
        id="vireon.reference.ids.v2",
        version="2.0.0",
        implements=["IIDSProviderV1"],
        permissions=[
            "state.read:num_channels",
            "state.read:stimulation_enabled",
            "state.read:stimulation_amplitude_ma",
            "state.read:stimulation_frequency_hz",
            "state.read:autonomic_pupil_dilation_mm",
            "state.read:sim_clock",
            "state.read:temperature_celsius",
            "state.mutate:active_anomalies",
            "state.mutate:last_anomaly_score",
            "event.publish:telemetry"
        ]
    )

class DigitalTwinProxy:
    """
    Adapter that exposes the required DigitalTwin properties to the legacy SecurityEngine
    by routing them through the zero-trust RuntimeServices state API.
    """
    def __init__(self, services: RuntimeServices):
        self.services = services
        self.brain_regions = {}

    @property
    def num_channels(self):
        return self.services.state.get("num_channels") or 8

    @property
    def stimulation_enabled(self):
        return self.services.state.get("stimulation_enabled") or False

    @property
    def stimulation_amplitude_ma(self):
        return self.services.state.get("stimulation_amplitude_ma") or 0.0

    @property
    def autonomic_pupil_dilation_mm(self):
        return self.services.state.get("autonomic_pupil_dilation_mm") or 4.0

    def get_sim_clock(self):
        return self.services.state.get("sim_clock") or 0.0

class V2IDSProvider(IIDSProviderV1):
    def __init__(self):
        self.services = None
        self.engine = None
        self.twin_proxy = None

    def initialize(self, services: RuntimeServices):
        self.services = services
        self.twin_proxy = DigitalTwinProxy(services)
        self.engine = SecurityEngine(twin=self.twin_proxy, event_bus=None)
        logger.info("[V2IDSProvider] Initialized")

    def analyze_window(self, data: Any) -> bool:
        if self.engine is None or data is None or len(data.shape) == 0 or data.shape[1] == 0:
            return False
            
        anomalies = self.engine.analyze_signal(data)
        score = self.engine.score_signal(data)
        
        # We publish the anomalies to the state store so other providers (like IPS)
        # or the dashboard can react without direct references.
        self.services.state.set("active_anomalies", anomalies)
        self.services.state.set("last_anomaly_score", score)
        
        return len(anomalies) > 0

    def health(self) -> dict:
        is_fitted = False
        if self.engine and hasattr(self.engine, 'autoencoder') and self.engine.autoencoder:
            is_fitted = getattr(self.engine.autoencoder, 'is_fitted', False)
        return {"status": "ok", "autoencoder_fitted": is_fitted}
