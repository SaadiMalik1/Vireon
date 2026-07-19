# Copyright 2026 VIREON Contributors
# VIREON V2 Physics Provider Implementation

import os
import json
import logging
from dataclasses import dataclass
from typing import Any

from vireon.sdk.provider_interfaces.v1 import IPhysicsProviderV1
from vireon.sdk.capability.descriptor import CapabilityDescriptor
from vireon.sdk.services.apis import RuntimeServices

logger = logging.getLogger("V2PhysicsProvider")

@dataclass
class ThermodynamicConstants:
    rho_c: float = 3.6e6            # Tissue volumetric heat capacity (J/m^3K)
    w_b_rho_b_c_b: float = 40000.0  # Blood perfusion term (W/m^3K)
    Q_m: float = 10000.0            # Metabolic heat generation (W/m^3)
    vol_m3: float = 1.5e-9          # Assumed heated volume 1.5 mm^3
    pulse_width_s: float = 100e-6   # Default pulse width

def get_physics_descriptor() -> CapabilityDescriptor:
    """The formal declarative boundary of the Physics engine."""
    return CapabilityDescriptor(
        id="vireon.reference.physics.v1",
        implements=["IPhysicsProviderV1"],
        requires={"api": "IStateAPI"},
        permissions=[
            "state.read:stimulation_enabled",
            "state.read:stimulation_amplitude_ma",
            "state.read:stimulation_frequency_hz",
            "state.read:electrode_impedances",
            "state.read:hardware_mode",
            "state.read:temperature_celsius",
            "state.read:hazard_state",
            "state.read:iso_severity",
            "state.read:tissue_damage_risk",
            "state.mutate:temperature_celsius",
            "state.mutate:tissue_damage_risk",
            "state.mutate:clinical_alert_active",
            "state.mutate:clinical_status",
            "state.mutate:hazard_state",
            "state.mutate:iso_severity",
            "state.mutate:stimulation_enabled",
            "state.mutate:stimulation_amplitude_ma",
            "state.mutate:stimulation_frequency_hz",
        ],
        features=["thermodynamics", "rk4_integration"],
        latency="soft-realtime"
    )

class V2PhysicsProvider(IPhysicsProviderV1):
    def __init__(self):
        self.thermo_const = ThermodynamicConstants()
        self.max_temp_rise_c = 1.0     
        self.max_dc_leakage_ua = 0.4   
        self.services: RuntimeServices = None

    def initialize(self, services: RuntimeServices) -> None:
        self.services = services
        self._load_atlas_constants()
        logger.info("[V2PhysicsProvider] Bound to explicit capability proxies.")

    def _load_atlas_constants(self):
        # We assume threat_atlas.json is at vireon/plugins/clinical/data/threat_atlas.json
        atlas_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "plugins", "clinical", "data", "threat_atlas.json")
        if not os.path.exists(atlas_path):
            logger.warning("threat_atlas.json not found offline, using fallback physics constants.")
            return

        try:
            with open(atlas_path, "r", encoding="utf-8") as f:
                atlas_data = json.load(f)
            
            constants = atlas_data.get("physics", {}).get("constants", [])
            for c in constants:
                if c.get("parameter") == "Max safe tissue temp rise":
                    val_str = str(c.get("value", "")).replace("°C", "").strip()
                    try:
                        self.max_temp_rise_c = float(val_str)
                    except ValueError:
                        pass
                elif c.get("parameter") == "DC leakage tissue damage threshold":
                    val_str = str(c.get("value", "")).replace("µA", "").strip()
                    try:
                        self.max_dc_leakage_ua = float(val_str)
                    except ValueError:
                        pass
            logger.info(f"Loaded Physics Constants: MaxTempRise={self.max_temp_rise_c}°C, MaxLeakage={self.max_dc_leakage_ua}µA")
        except Exception as e:
            logger.error(f"Error parsing threat_atlas.json for physics constants: {e}")

    def step_physics(self, dt: float) -> None:
        if not self.services:
            return
            
        state = self.services.state
        
        # Read from strictly isolated state API
        stim_enabled = state.get("stimulation_enabled") or False
        stim_amp = state.get("stimulation_amplitude_ma") or 0.0
        stim_freq = state.get("stimulation_frequency_hz") or 0.0
        impedances = state.get("electrode_impedances") or {0: 5.0}
        hw_mode = state.get("hardware_mode") or False
        
        current_temp = state.get("temperature_celsius") or 37.0

        T_a = 37.0 - (self.thermo_const.Q_m / self.thermo_const.w_b_rho_b_c_b) 
        
        Q_ext = 0.0
        if stim_enabled and stim_amp > 0:
            I_A = stim_amp * 1e-3
            R_ohms = impedances.get(0, 5.0) * 1000.0
            duty_cycle = stim_freq * self.thermo_const.pulse_width_s
            power_W = (I_A ** 2) * R_ohms * duty_cycle
            Q_ext = power_W / self.thermo_const.vol_m3
            
        def get_dT_dt(T):
            return (self.thermo_const.w_b_rho_b_c_b * (T_a - T) + self.thermo_const.Q_m + Q_ext) / self.thermo_const.rho_c

        # RK4 Integration
        k1 = get_dT_dt(current_temp)
        k2 = get_dT_dt(current_temp + 0.5 * dt * k1)
        k3 = get_dT_dt(current_temp + 0.5 * dt * k2)
        k4 = get_dT_dt(current_temp + dt * k3)
        
        dT_total = (dt / 6.0) * (k1 + 2*k2 + 2*k3 + k4)
        new_temp = max(37.0, current_temp + dT_total)
        
        # Mutate through proxy
        state.set("temperature_celsius", new_temp)
        
        # Calculate theoretical DC leakage
        if stim_enabled and stim_amp > 0:
            leakage_ua = 0.1 * stim_amp * (stim_freq / 130.0)
        else:
            leakage_ua = 0.0

        # Check violations
        temp_rise = new_temp - 37.0
        violation_msg = None
        if temp_rise > self.max_temp_rise_c:
            violation_msg = f"Tissue temp rise limit exceeded: {temp_rise:.2f}°C > {self.max_temp_rise_c}°C"
        elif leakage_ua > self.max_dc_leakage_ua:
            violation_msg = f"DC leakage limit exceeded: {leakage_ua:.2f}µA > {self.max_dc_leakage_ua}µA"

        if violation_msg:
            if hw_mode:
                state.set("stimulation_enabled", False)
                state.set("stimulation_amplitude_ma", 0.0)
                state.set("stimulation_frequency_hz", 0.0)
                state.set("hazard_state", "HARDWARE_SHUTDOWN")
                state.set("iso_severity", "CRITICAL")
                state.set("clinical_alert_active", True)
                state.set("clinical_status", f"Hardware Failsafe: {violation_msg}")
            else:
                state.set("tissue_damage_risk", "HIGH")
                state.set("clinical_alert_active", True)
                
                curr_hazard = state.get("hazard_state") or "NOMINAL"
                curr_iso = state.get("iso_severity") or "NEGLIGIBLE"
                
                if curr_hazard != "WARNING" or curr_iso != "HIGH":
                    state.set("clinical_status", f"Physics Violation (Sim): {violation_msg}")
                    state.set("hazard_state", "WARNING")
                    state.set("iso_severity", "HIGH")
        else:
            curr_risk = state.get("tissue_damage_risk") or "NONE"
            curr_hazard = state.get("hazard_state") or "NOMINAL"
            
            if curr_risk == "HIGH" and curr_hazard == "WARNING":
                state.set("tissue_damage_risk", "NONE")
                state.set("clinical_alert_active", False)
                state.set("clinical_status", "Nominal")
                state.set("hazard_state", "NOMINAL")
                state.set("iso_severity", "NEGLIGIBLE")

    def health(self) -> dict:
        return {"status": "ok"}
