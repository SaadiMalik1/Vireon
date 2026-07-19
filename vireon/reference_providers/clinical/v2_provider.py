# Copyright 2026 VIREON Contributors
from typing import Any
import logging

from vireon.sdk.provider_interfaces.v1 import IClinicalProviderV1
from vireon.sdk.capability.descriptor import CapabilityDescriptor
from vireon.reference_providers.clinical.neuroips import NeuroIPS
from vireon.sdk.services.apis import RuntimeServices

logger = logging.getLogger(__name__)

def get_clinical_descriptor() -> CapabilityDescriptor:
    return CapabilityDescriptor(
        id="vireon.reference.clinical.v2",
        version="2.0.0",
        implements=["IClinicalProviderV1"],
        permissions=[
            "state.read:sim_clock",
            "state.read:active_anomalies",
            "state.read:temperature_celsius",
            "state.read:stimulation_amplitude_ma",
            "state.read:stimulation_frequency_hz",
            "state.mutate:clinical_alert_active",
            "state.mutate:clinical_status",
            "state.mutate:hazard_state",
            "state.mutate:iso_severity",
            "state.mutate:tissue_damage_risk",
            "state.mutate:stimulation_enabled",
            "state.mutate:stimulation_amplitude_ma",
            "state.mutate:stimulation_frequency_hz",
            "state.mutate:clinical_action",
            "state.mutate:decoder_confidence",
            "state.mutate:fallback_mode_enabled"
        ]
    )

class TwinProxy:
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

    def get(self, key, default=None):
        return self.services.state.get(key, default)

class V2ClinicalProvider(IClinicalProviderV1):
    def __init__(self, ids_provider):
        self.services = None
        self.ips = None
        self.ids_provider = ids_provider

    def initialize(self, services: RuntimeServices):
        self.services = services
        # We pass the state API down to NeuroIPS. It uses duck-typing, so EnforcingStateAPI will work.
        self.ips = NeuroIPS(state_store=self.services.state, ids=self.ids_provider.engine, event_bus=None)
        self.ips.twin = TwinProxy(services)
        logger.info("[V2ClinicalProvider] Initialized")

    def evaluate_biomarker(self, data: Any) -> dict:
        if self.ips is None or data is None or len(data.shape) == 0 or data.shape[1] == 0:
            return {}
            
        anomalies = self.services.state.get("active_anomalies")
        if anomalies is None:
            anomalies = []
            
        amp = self.services.state.get("stimulation_amplitude_ma")
        if amp is None:
            amp = 0.0
            
        freq = self.services.state.get("stimulation_frequency_hz")
        if freq is None:
            freq = 0.0
            
        self.ips.sanitize_stimulation_write(amp, freq)
        self.ips.mitigate_signal_anomalies(data, anomalies)
        self.ips.mitigate_pathological_sync(anomalies)
        
        return {"anomalies_processed": len(anomalies)}

    def health(self) -> dict:
        return {"status": "ok", "clamping_active": self.ips.clamping_active if self.ips else False}
