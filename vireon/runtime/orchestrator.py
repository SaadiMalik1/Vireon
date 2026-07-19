# Copyright 2026 VIREON Contributors
# Vireon V2 Orchestrator Kernel

import logging
from typing import Dict, Any, List

from vireon.sdk.lifecycle.state_machine import ILifecycleManager, ProviderState
from vireon.sdk.capability.descriptor import CapabilityDescriptor
from vireon.sdk.provider_interfaces.v1 import IProviderV1
from vireon.sdk.services.apis import RuntimeServices
from vireon.runtime.enforcement import EnforcingStateAPI, EnforcingTelemetryAPI

logger = logging.getLogger(__name__)

class OrchestrationFault(Exception):
    pass

class VireonOrchestrator(ILifecycleManager):
    """
    The heart of the V2 Runtime.
    Manages provider registration, capability negotiation, dependency injection,
    and advances the 13-stage deterministic lifecycle.
    """
    def __init__(self, global_state_store: Any, global_event_bus: Any):
        self._global_state_store = global_state_store
        self._global_event_bus = global_event_bus
        
        self.providers: Dict[str, IProviderV1] = {}
        self.descriptors: Dict[str, CapabilityDescriptor] = {}
        self.provider_states: Dict[str, ProviderState] = {}
        self.injected_services: Dict[str, RuntimeServices] = {}

    def register_provider(self, provider: IProviderV1, descriptor: CapabilityDescriptor) -> None:
        """Stage 1: DISCOVERED"""
        p_id = descriptor.id
        if p_id in self.providers:
            raise OrchestrationFault(f"Provider {p_id} already registered.")
            
        self.providers[p_id] = provider
        self.descriptors[p_id] = descriptor
        self.provider_states[p_id] = ProviderState.DISCOVERED
        logger.info(f"Registered provider: {p_id} ({descriptor.latency} latency)")

    def load_native_provider(self, library_path: str) -> None:
        """Loads a C-ABI compliant provider and registers it."""
        from vireon.sdk.native_provider import NativeProviderLoader
        try:
            loader = NativeProviderLoader(library_path)
            self.register_provider(loader, loader.descriptor)
        except Exception as e:
            logger.error(f"Failed to load native provider from {library_path}: {e}")
            raise OrchestrationFault(f"Native loader error: {e}")

    def transition(self, provider_id: str, target_state: ProviderState) -> bool:
        """Advances a provider through the lifecycle safely."""
        current_state = self.provider_states.get(provider_id)
        if current_state == target_state:
            return True
            
        # Simplified linear progression enforcement for demonstration
        logger.debug(f"[{provider_id}] Transitioning: {current_state} -> {target_state}")
        self.provider_states[provider_id] = target_state
        return True

    def initialize_all(self):
        """Advances all providers through DISCOVERED -> READY"""
        for p_id, desc in self.descriptors.items():
            self.transition(p_id, ProviderState.VALIDATING_MANIFEST)
            # In a real environment, we'd check manifest signatures here
            
            self.transition(p_id, ProviderState.RESOLVING_DEPENDENCIES)
            # Ensure required capabilities are met by other registered providers
            
            self.transition(p_id, ProviderState.NEGOTIATING_CAPABILITIES)
            
            # Build injected services
            self.transition(p_id, ProviderState.INITIALIZING)
            
            state_api = EnforcingStateAPI(self._global_state_store, desc)
            telemetry_api = EnforcingTelemetryAPI(self._global_event_bus, desc)
            
            services = RuntimeServices(
                state=state_api,
                telemetry=telemetry_api
            )
            self.injected_services[p_id] = services
            
            # Call provider's initialize method if it has one (backward compat)
            provider = self.providers[p_id]
            if hasattr(provider, 'initialize'):
                provider.initialize(services)
                
            self.transition(p_id, ProviderState.READY)

    def start_all(self):
        for p_id in self.providers:
            self.transition(p_id, ProviderState.STARTING)
            # Trigger threads/subprocess boots here
            self.transition(p_id, ProviderState.RUNNING)

    def tick_all(self, dt: float, data: Any = None):
        """
        The deterministic tick driven by the Engine.
        Calls the appropriate ABI methods for each provider based on its declared interfaces.
        """
        for p_id, provider in self.providers.items():
            if self.provider_states[p_id] != ProviderState.RUNNING:
                continue
                
            desc = self.descriptors[p_id]
            
            if "IPhysicsProviderV1" in desc.implements:
                if hasattr(provider, "step_physics"):
                    provider.step_physics(dt)
                    
            if data is not None:
                if "IIDSProviderV1" in desc.implements:
                    if hasattr(provider, "analyze_window"):
                        provider.analyze_window(data)
                        
                if "IClinicalProviderV1" in desc.implements:
                    if hasattr(provider, "evaluate_biomarker"):
                        provider.evaluate_biomarker(data)

            if "ITelemetryProviderV1" in desc.implements:
                if hasattr(provider, "on_tick"):
                    # Backward compat or specific tick logic
                    provider.on_tick(dt)

    def shutdown_all(self):
        for p_id, provider in self.providers.items():
            self.transition(p_id, ProviderState.SHUTTING_DOWN)
            if hasattr(provider, 'shutdown'):
                provider.shutdown()
            self.transition(p_id, ProviderState.UNLOADED)

    def perform_health_check(self, provider_id: str) -> dict:
        provider = self.providers.get(provider_id)
        if provider and hasattr(provider, 'health'):
            return provider.health()
        return {"status": "unknown"}

    def gather_evidence(self, run_id: str):
        """
        Collects artifacts from the current run and generates a cryptographic evidence package.
        """
        from vireon.evidence.pipeline import EvidenceEngine
        from vireon.validation.artifacts import ThreatReport, ExecutionTrace
        import uuid
        
        engine = EvidenceEngine()
        
        # In a real system, we would query the global event bus or state store for all artifacts
        # Here we mock retrieving threat reports from the active anomalies
        active_anomalies = self._global_state_store.get("active_anomalies", [])
        
        threat_report = ThreatReport(
            artifact_id=str(uuid.uuid4()),
            run_id=run_id,
            provider_id="vireon.orchestrator",
            anomalies_detected=len(active_anomalies),
            confidence_scores=[1.0] * len(active_anomalies) if active_anomalies else []
        )
        engine.ingest(threat_report)
        
        trace = ExecutionTrace(
            artifact_id=str(uuid.uuid4()),
            run_id=run_id,
            provider_id="vireon.orchestrator",
            state_transitions=[{"state_keys_modified": len(self._global_state_store.get_all())}],
            events_published=0
        )
        engine.ingest(trace)
        
        return engine.sign_package(run_id)
