import asyncio
from mcp.server.fastmcp import FastMCP
from typing import List, Optional
import json

from neuroshield.core.coordinator import Coordinator
from neuroshield.core.plugin_registry import PluginRegistry, register_builtin_plugins

# Create the MCP server instance
mcp = FastMCP("NeuroShield")

def _get_registry():
    registry = PluginRegistry()
    register_builtin_plugins(registry)
    return registry

@mcp.tool()
def get_available_plugins() -> str:
    """
    List all available plugins in the NeuroShield Reference Platform.
    This includes hardware devices, datasets, clinical evaluators, and attack modifiers.
    """
    registry = _get_registry()
    cats = registry.list_categories()
    
    result = {"categories": {}}
    for cat in cats:
        plugins = registry._registry.get(cat, {})
        result["categories"][cat] = [
            {"name": info.name, "description": info.description} 
            for info in plugins.values()
        ]
        
    return json.dumps(result, indent=2)

@mcp.tool()
def run_simulation(
    duration_sec: float = 5.0,
    attacks: Optional[List[str]] = None,
    secure_mode: bool = True,
    device: str = "synthetic",
    dbs_mode: bool = False,
    dbs_attack: Optional[str] = None
) -> str:
    """
    Run a NeuroShield simulation in headless mode and return the final clinical status.
    
    Args:
        duration_sec: How long to run the simulation in seconds.
        attacks: List of signal/firmware attacks (e.g., ["noise", "drift", "stimulation_leak"]).
        secure_mode: Whether the IDS/IPS security shield is active.
        device: The hardware board emulator to use (e.g., "synthetic", "pieeg").
        dbs_mode: Enable the Deep Brain Stimulation closed-loop model instead of standard EEG.
        dbs_attack: Inject a DBS-specific attack (e.g., "phase_shift").
        
    Returns:
        JSON string containing the final hazard state and clinical alerts.
    """
    # Build raw config dictionary equivalent to what the CLI would generate
    raw_config = {
        "experiment": {
            "name": "mcp_sim",
            "duration_sec": duration_sec
        },
        "device": {
            "type": device,
            "sample_rate": 250
        },
        "attacks": {
            "active": attacks or [],
            "noise_level_uv": 80.0,
            "drift_slope_uv_s": 25.0
        },
        "security": {
            "enabled": secure_mode
        },
        "emulation": {
            "dbs_mode": dbs_mode,
            "dbs_attack": dbs_attack
        }
    }

    # Initialize coordinator with the raw config
    coordinator = Coordinator(raw_config)
    coordinator.start_simulation()
    
    # Wait for the simulation to finish
    import time
    time.sleep(duration_sec + 1.0)
    
    # Capture the final state of the digital twin
    final_state = coordinator.twin.get_state()
    coordinator.stop_simulation()
    
    # Return key safety metrics
    return json.dumps({
        "status": "Simulation Complete",
        "duration_sec": duration_sec,
        "secure_mode": secure_mode,
        "attacks_injected": attacks or [],
        "dbs_attack_injected": dbs_attack,
        "final_hazard_state": final_state.get("hazard_state", "UNKNOWN"),
        "final_clinical_status": final_state.get("clinical_status", "UNKNOWN"),
        "tissue_damage_risk_pct": final_state.get("tissue_damage_risk", 0.0)
    }, indent=2)

if __name__ == "__main__":
    # Start the stdio MCP server
    mcp.run(transport="stdio")
