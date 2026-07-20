from vireon.sdk.subprocess_provider import SubprocessProvider

from vireon.sdk.manifest import CapabilityManifest

def test_subprocess_provider_init():
    manifest = CapabilityManifest(name="test_provider", version="1.0.0", category="test", mutates_state=["state:read"])
    provider = SubprocessProvider(["echo", "test"], manifest)
    assert provider.manifest.name == "test_provider"
    assert provider.command == ["echo", "test"]
    assert provider.process is None
