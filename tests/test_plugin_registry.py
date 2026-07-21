import pytest
from vireon.runtime.plugin_registry import PluginRegistry, PluginInfo, register_builtin_plugins

def test_registry_register_and_get():
    registry = PluginRegistry()
    info = PluginInfo(name="test_plugin", category="test", description="A test plugin")
    registry.register(info)
    
    retrieved = registry.get("test", "test_plugin")
    assert retrieved.name == "test_plugin"
    assert retrieved.category == "test"
    
def test_registry_duplicate_register():
    registry = PluginRegistry()
    info = PluginInfo(name="test_plugin", category="test")
    registry.register(info)
    
    with pytest.raises(ValueError):
        registry.register(info)

def test_registry_unregister():
    registry = PluginRegistry()
    info = PluginInfo(name="test_plugin", category="test")
    registry.register(info)
    
    assert registry.unregister("test", "test_plugin") is True
    assert registry.unregister("test", "test_plugin") is False
    
    with pytest.raises(KeyError):
        registry.get("test", "test_plugin")

def test_registry_create_with_class():
    class DummyPlugin:
        def __init__(self, value):
            self.value = value
            
    registry = PluginRegistry()
    info = PluginInfo(name="dummy", category="test", plugin_class=DummyPlugin)
    registry.register(info)
    
    instance = registry.create("test", "dummy", value=42)
    assert isinstance(instance, DummyPlugin)
    assert instance.value == 42

def test_registry_create_with_factory():
    def dummy_factory(value):
        return {"value": value}
        
    registry = PluginRegistry()
    info = PluginInfo(name="dummy_factory", category="test", factory=dummy_factory)
    registry.register(info)
    
    instance = registry.create("test", "dummy_factory", value=42)
    assert instance["value"] == 42

def test_registry_create_invalid():
    registry = PluginRegistry()
    info = PluginInfo(name="invalid", category="test")
    registry.register(info)
    
    with pytest.raises(ValueError):
        registry.create("test", "invalid")

def test_registry_list_methods():
    registry = PluginRegistry()
    info1 = PluginInfo(name="plugin1", category="cat1")
    info2 = PluginInfo(name="plugin2", category="cat1")
    info3 = PluginInfo(name="plugin3", category="cat2")
    
    registry.register(info1)
    registry.register(info2)
    registry.register(info3)
    
    categories = registry.list_categories()
    assert set(categories) == {"cat1", "cat2"}
    
    plugins_cat1 = registry.list_category("cat1")
    assert {p.name for p in plugins_cat1} == {"plugin1", "plugin2"}

def test_register_builtin_plugins():
    registry = PluginRegistry()
    register_builtin_plugins(registry)
    
    # Check that some expected builtins are registered
    cats = registry.list_categories()
    assert "security" in cats
    
    sec_plugins = registry.list_category("security")
    sec_plugin_names = {p.name for p in sec_plugins}
    # At least some of the builtins should be present
    assert "ids" in sec_plugin_names or "zta_engine" in sec_plugin_names
