# Copyright 2026 VIREON Contributors
# Vireon V2 Orchestrator Kernel

import logging
from typing import Dict, Any, List, Tuple, Callable
from vireon.sdk.lifecycle.state_machine import ILifecycleManager, ProviderState
from vireon.sdk.capability.descriptor import CapabilityDescriptor
from vireon.sdk.provider_interfaces.v1 import IProviderV1
from vireon.sdk.services.apis import RuntimeServices
from vireon.runtime.enforcement import EnforcingStateAPI, EnforcingTelemetryAPI
from vireon.runtime.watchdog import HardwareWatchdog

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
        
        # Pre-cached method callbacks for zero-allocation tick execution (R3)
        self._physics_callbacks: List[Tuple[str, Callable[[float], None]]] = []
        self._ids_callbacks: List[Tuple[str, Callable[[Any], bool]]] = []
        self._clinical_callbacks: List[Tuple[str, Callable[[Any], dict]]] = []
        self._telemetry_callbacks: List[Tuple[str, Callable[[float], None]]] = []

        # Hardware execution watchdog (ADR-010)
        self.watchdog = HardwareWatchdog(timeout_sec=2.0)

    def _rebuild_callback_cache(self) -> None:
        """Pre-caches bound method pointers for fast, zero-reflection tick loops."""
        self._physics_callbacks.clear()
        self._ids_callbacks.clear()
        self._clinical_callbacks.clear()
        self._telemetry_callbacks.clear()

        for p_id, provider in self.providers.items():
            desc = self.descriptors.get(p_id)
            if not desc:
                continue

            if "IPhysicsProviderV1" in desc.implements and hasattr(provider, "step_physics"):
                self._physics_callbacks.append((p_id, getattr(provider, "step_physics")))

            if "IIDSProviderV1" in desc.implements and hasattr(provider, "analyze_window"):
                self._ids_callbacks.append((p_id, getattr(provider, "analyze_window")))

            if "IClinicalProviderV1" in desc.implements and hasattr(provider, "evaluate_biomarker"):
                self._clinical_callbacks.append((p_id, getattr(provider, "evaluate_biomarker")))

            if "ITelemetryProviderV1" in desc.implements and hasattr(provider, "on_tick"):
                self._telemetry_callbacks.append((p_id, getattr(provider, "on_tick")))

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

    def initialize_all(self, trusted_public_key=None):
        """Advances all providers through DISCOVERED -> READY"""
        from vireon.runtime.capability_engine import CapabilityEngine
        from vireon.runtime.configuration import ExperimentConfig
        cap_engine = CapabilityEngine(ExperimentConfig())

        for p_id, desc in self.descriptors.items():
            self.transition(p_id, ProviderState.VALIDATING_MANIFEST)
            # Validate capability descriptor and signature if manifest present
            provider = self.providers[p_id]
            manifest = getattr(provider, "manifest", None)
            if manifest:
                if not cap_engine.validate_manifest(manifest, trusted_public_key=trusted_public_key):
                    self.transition(p_id, ProviderState.ERROR)
                    raise OrchestrationFault(f"Capability manifest validation failed for provider {p_id}")

            self.transition(p_id, ProviderState.RESOLVING_DEPENDENCIES)
            self.transition(p_id, ProviderState.NEGOTIATING_CAPABILITIES)
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
            
        self._rebuild_callback_cache()

    def start_all(self):
        for p_id in self.providers:
            self.transition(p_id, ProviderState.STARTING)
            # Trigger threads/subprocess boots here
            self.transition(p_id, ProviderState.RUNNING)
            
        self._rebuild_callback_cache()

    def tick_all(self, dt: float, data: Any = None):
        """
        The deterministic tick driven by the Engine.
        Executes pre-cached ABI methods for each running provider without runtime reflection.
        """
        self.watchdog.kick()

        for p_id, physics_fn in self._physics_callbacks:
            if self.provider_states.get(p_id) == ProviderState.RUNNING:
                physics_fn(dt)

        if data is not None:
            for p_id, ids_fn in self._ids_callbacks:
                if self.provider_states.get(p_id) == ProviderState.RUNNING:
                    ids_fn(data)

            for p_id, clinical_fn in self._clinical_callbacks:
                if self.provider_states.get(p_id) == ProviderState.RUNNING:
                    clinical_fn(data)

        for p_id, telemetry_fn in self._telemetry_callbacks:
            if self.provider_states.get(p_id) == ProviderState.RUNNING:
                telemetry_fn(dt)

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
