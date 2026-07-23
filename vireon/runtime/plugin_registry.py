# Copyright 2026 VIREON Contributors
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
VIREON Plugin Registry.
Manages dynamic discovery, registration, and instantiation of simulation plugins.
"""

import importlib
import logging
from dataclasses import dataclass
from typing import Dict, Any, List, Type

logger = logging.getLogger(__name__)

@dataclass
class PluginInfo:
    name: str
    category: str
    description: str
    plugin_class: Type[Any]
    version: str = "1.0.0"

class PluginRegistry:
    def __init__(self):
        self._plugins: Dict[str, Dict[str, PluginInfo]] = {}

    def register(self, info: PluginInfo):
        if info.category not in self._plugins:
            self._plugins[info.category] = {}
        self._plugins[info.category][info.name] = info

    def get(self, category: str, name: str) -> PluginInfo:
        if category not in self._plugins or name not in self._plugins[category]:
            raise KeyError(f"Plugin '{name}' not found in category '{category}'")
        return self._plugins[category][name]

    def create(self, category: str, name: str, **kwargs) -> Any:
        info = self.get(category, name)
        return info.plugin_class(**kwargs)

    def list_categories(self) -> List[str]:
        return list(self._plugins.keys())

    def list_category(self, category: str) -> List[PluginInfo]:
        return list(self._plugins.get(category, {}).values())

def register_builtin_plugins(registry: PluginRegistry):
    """Registers built-in simulation plugins dynamically."""
    _safe_register = registry.register
    registry.register = _safe_register  # type: ignore[method-assign]

    # --- Attack Modifiers ---
    attack_mod = importlib.import_module("vireon.runtime.attack")
    NoiseInjectionAttack = getattr(attack_mod, "NoiseInjectionAttack")
    SignalDriftAttack = getattr(attack_mod, "SignalDriftAttack")
    ImpedanceSpikeAttack = getattr(attack_mod, "ImpedanceSpikeAttack")
    SignalSuppressionAttack = getattr(attack_mod, "SignalSuppressionAttack")

    registry.register(PluginInfo(
        name="noise",
        category="attacks",
        description="Gaussian noise injection attack",
        plugin_class=NoiseInjectionAttack,
        version="1.0.0"
    ))
    registry.register(PluginInfo(
        name="drift",
        category="attacks",
        description="Signal baseline drift attack",
        plugin_class=SignalDriftAttack,
        version="1.0.0"
    ))
    registry.register(PluginInfo(
        name="impedance",
        category="attacks",
        description="Electrode impedance spike / disconnection attack",
        plugin_class=ImpedanceSpikeAttack,
        version="1.0.0"
    ))
    registry.register(PluginInfo(
        name="suppression",
        category="attacks",
        description="Signal suppression attack",
        plugin_class=SignalSuppressionAttack,
        version="1.0.0"
    ))

    # --- Security & Clinical ---
    ids_mod = importlib.import_module("providers.ids.detection")
    SecurityEngine = getattr(ids_mod, "SecurityEngine")

    clinical_mod = importlib.import_module("vireon.runtime.clinical")
    NeuroIPS = getattr(clinical_mod, "NeuroIPS")
    BLELinkGuard = getattr(clinical_mod, "BLELinkGuard")

    privacy_mod = importlib.import_module("providers.privacy.leakage")
    P300Analyzer = getattr(privacy_mod, "P300Analyzer")

    e2ee_mod = importlib.import_module("providers.authentication.e2ee")
    E2EEChannel = getattr(e2ee_mod, "E2EEChannel")

    auth_mod = importlib.import_module("providers.authentication.tokens")
    BiometricGate = getattr(auth_mod, "BiometricGate")

    zta_mod = importlib.import_module("vireon.runtime.zta")
    ZTAPolicyEngine = getattr(zta_mod, "ZTAPolicyEngine")

    intel_mod = importlib.import_module("providers.threat_models.intel")
    ThreatIntelligence = getattr(intel_mod, "ThreatIntelligence")

    registry.register(PluginInfo(
        name="ids",
        category="security",
        description="Intrusion Detection System for neural anomalies",
        plugin_class=SecurityEngine,
        version="1.0.0"
    ))
    registry.register(PluginInfo(
        name="ips",
        category="security",
        description="Intrusion Prevention System for neural anomaly mitigation",
        plugin_class=NeuroIPS,
        version="1.0.0"
    ))
    registry.register(PluginInfo(
        name="ble_guard",
        category="security",
        description="BLE link-layer security and MTU guard",
        plugin_class=BLELinkGuard,
        version="1.0.0"
    ))
    registry.register(PluginInfo(
        name="p300_analyzer",
        category="security",
        description="Privacy leakage analyzer for P300 potentials",
        plugin_class=P300Analyzer,
        version="1.0.0"
    ))
    registry.register(PluginInfo(
        name="e2ee_channel",
        category="security",
        description="End-to-end encrypted channel wrapper",
        plugin_class=E2EEChannel,
        version="1.0.0"
    ))
    registry.register(PluginInfo(
        name="biometric_gate",
        category="security",
        description="Biometric gate authentication manager",
        plugin_class=BiometricGate,
        version="1.0.0"
    ))
    registry.register(PluginInfo(
        name="zta_engine",
        category="security",
        description="Zero Trust Architecture policy engine",
        plugin_class=ZTAPolicyEngine,
        version="1.0.0"
    ))
    registry.register(PluginInfo(
        name="threat_intel",
        category="security",
        description="Threat Intelligence mapping resolver",
        plugin_class=ThreatIntelligence,
        version="1.0.0"
    ))
