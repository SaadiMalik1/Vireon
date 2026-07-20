import logging
from vireon.sdk.provider_interfaces.v1 import IPhysicsProviderV1
from vireon.sdk.capability.descriptor import CapabilityDescriptor
from vireon.runtime.orchestrator import VireonOrchestrator
from vireon.runtime.enforcement import SecurityFault

logging.basicConfig(level=logging.INFO)

class DummyPhysicsProvider(IPhysicsProviderV1):
    def __init__(self):
        self.state_api = None
        self.dt_accumulated = 0.0
        
    def initialize(self, services):
        print("[DummyPhysicsProvider] Initialized with injected services!")
        self.state_api = services.state
        # Try a legitimate read
        print(f"[DummyPhysicsProvider] Global Battery: {self.state_api.get('battery')}")
        
    def step_physics(self, dt: float) -> None:
        self.dt_accumulated += dt
        
        # Try a legitimate mutate
        self.state_api.set('tissue_temp', 37.0 + self.dt_accumulated)
        print(f"[DummyPhysicsProvider] Ticked {dt}s, Tissue Temp: 37.0 -> {37.0 + self.dt_accumulated}")
        
        # Try an ILLEGITIMATE mutate (Should fail!)
        try:
            self.state_api.set('firmware_root_key', 'hacked!')
        except SecurityFault as e:
            print(f"[DummyPhysicsProvider] SECURITY BLOCK SUCCESS: {e}")

    def health(self) -> dict:
        return {"status": "ok", "uptime_dt": self.dt_accumulated}

if __name__ == "__main__":
    print("--- Booting V2 Orchestrator ---")
    
    global_store = {"battery": 100.0, "tissue_temp": 37.0, "firmware_root_key": "secure"}
    global_event_bus = None
    
    orchestrator = VireonOrchestrator(global_store, global_event_bus)
    
    # 1. Define capability descriptor (Requires tissue_temp, but NOT firmware_root_key)
    desc = CapabilityDescriptor(
        id="dummy_physics",
        implements=["IPhysicsProviderV1"],
        permissions=["state.read:battery", "state.mutate:tissue_temp"],
        features=["thermal"],
        latency="soft-realtime"
    )
    
    provider = DummyPhysicsProvider()
    
    # 2. Register & advance lifecycle
    orchestrator.register_provider(provider, desc)
    orchestrator.initialize_all()
    orchestrator.start_all()
    
    # 3. Simulate an engine tick
    print("\n--- Engine Ticking Orchestrator ---")
    orchestrator.tick_all(0.1)
    
    # 4. Check Health
    print("\n--- Health Check ---")
    print(orchestrator.perform_health_check("dummy_physics"))
    
    print("\n--- Final Global State ---")
    print(global_store)
