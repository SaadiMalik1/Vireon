from vireon.sdk.plugin import OrchestratorContext, IVireonPlugin, IFirmwareProvider
from vireon.sdk.manifest import CapabilityManifest
from unittest.mock import MagicMock

class DummyPlugin(IVireonPlugin):
    @property
    def manifest(self) -> CapabilityManifest:
        return CapabilityManifest(name="test", version="1", category="test")
        
    def initialize(self, context: OrchestratorContext) -> None:
        self.context = context

class DummyFirmware(IFirmwareProvider):
    @property
    def manifest(self) -> CapabilityManifest:
        return CapabilityManifest(name="fw", version="1", category="test")
        
    def initialize(self, context: OrchestratorContext) -> None:
        pass
        
    def write_memory(self, address: int, data: bytes) -> bool:
        return True
        
    def read_memory(self, address: int, size: int) -> bytes:
        return b'\x00' * size

def test_orchestrator_context():
    bus = MagicMock()
    store = MagicMock()
    ctx = OrchestratorContext(bus, store)
    assert ctx.event_bus == bus
    assert ctx.state_store == store

def test_plugin_base():
    plugin = DummyPlugin()
    ctx = OrchestratorContext(MagicMock(), MagicMock())
    plugin.initialize(ctx)
    assert plugin.context == ctx
    plugin.on_tick(0.0, 0.1)
    plugin.shutdown()

def test_firmware_provider():
    fw = DummyFirmware()
    assert fw.write_memory(0, b"data")
    assert fw.read_memory(0, 4) == b'\x00\x00\x00\x00'
