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

import os
import sys
import logging
from vireon.runtime.event_bus import Event

logger = logging.getLogger(__name__)


class SimulationBuilder:
    def __init__(self, coordinator):
        self.c = coordinator
        self.config = coordinator.config

    def setup_attacks(self):
        """Configure signal modifiers from config."""
        target_channels = self.config.attacks.target_channels

        for attack_name in self.config.attacks.active:
            if attack_name == "noise":
                print(f"[VIREON] Injecting Noise Attack (SD={self.config.attacks.noise_level_uv} uV)")
                from vireon.runtime.attack import NoiseInjectionAttack
                self.c.attack_engine.add_modifier(
                    NoiseInjectionAttack(target_channels, self.config.attacks.noise_level_uv)
                )
            elif attack_name == "drift":
                print("[VIREON] Injecting Signal Drift Attack")
                from vireon.runtime.attack import SignalDriftAttack
                self.c.attack_engine.add_modifier(
                    SignalDriftAttack(target_channels, self.config.attacks.drift_rate_uv_per_sec)
                )
            elif attack_name == "impedance":
                print("[VIREON] Injecting Impedance Spike Attack")
                from vireon.runtime.attack import ImpedanceSpikeAttack
                self.c.attack_engine.add_modifier(
                    ImpedanceSpikeAttack(target_channels, self.config.attacks.spike_impedance_kohm)
                )
            elif attack_name == "suppression":
                print("[VIREON] Injecting Signal Suppression Attack")
                from vireon.runtime.attack import SignalSuppressionAttack
                self.c.attack_engine.add_modifier(
                    SignalSuppressionAttack(target_channels, self.config.attacks.attenuation_factor)
                )
            elif attack_name == "stimulation_leak":
                print("[VIREON] Injecting Stimulation Leak Attack")
                if self.config.security.enabled:
                    from vireon.runtime.detection import SecurityEngine
                    from vireon.runtime.clinical import NeuroIPS
                    temp_ids = SecurityEngine(self.c.twin)
                    temp_ips = NeuroIPS(self.c.twin, temp_ids)
                    amp, freq = temp_ips.sanitize_stimulation_write(10.0, 130.0)
                    self.c.twin.update_therapy(True)
                    self.c.twin.update_stimulation_params(amp, freq)
                else:
                    self.c.twin.update_therapy(True)
                    self.c.twin.update_stimulation_params(10.0, 130.0)
            else:
                print(f"[VIREON] Warning: Unknown attack type: {attack_name}")

        self.c.event_bus.publish(Event(
            topic="attack.configured",
            data={"attacks": self.config.attacks.active},
            source="coordinator"
        ))

    def setup_device(self):
        """Load device wrapper from config."""
        device_wrapper = None
        try:
            if self.c.registry.has("devices", self.config.device.type):
                device_wrapper = self.c.registry.create(
                    "devices", 
                    self.config.device.type,
                    serial_port=self.config.device.serial_port
                )
            else:
                print(f"[VIREON] Warning: Unknown device type '{self.config.device.type}'")
        except Exception as e:
            logger.error(f"Error loading device module: {e}", exc_info=True)
            sys.exit(1)
        return device_wrapper

    def setup_dataset(self):
        """Load dataset reader from config."""
        dataset_reader = None

        if self.config.emulation.hardware_loopback:
            print("[VIREON] Configuring Hardware-in-the-loop (HIL) Socket Bridge...")
            self.c.bridge = None
            dataset_reader = None
        elif self.config.dataset.path:
            path = self.config.dataset.path
            ext = os.path.splitext(path)[1].lower()
            if ext in [".edf", ".bdf", ".csv"]:
                print(f"[VIREON] Path dataset specified ({path}). Reading stream...")
                dataset_reader = None
            else:
                print(f"[VIREON] Unsupported dataset extension: {ext}. Using synthetic stream.")

        return dataset_reader

    def setup_lsl_streamer(self):
        """Initialize LSL Streamer."""
        print("[VIREON] Starting headless mode for automated testing. Initializing LSL Streamer...")
        try:
            from vireon.runtime.lsl_streamer import LSLStreamer
            self.c.lsl_streamer = LSLStreamer(num_channels=self.c.twin.num_channels, srate=self.c.twin.sample_rate)
            self.config.duration_sec = 100000.0  # Run indefinitely in LSL mode
        except Exception as e:
            logger.error(f"Failed to start LSL Streamer: {e}", exc_info=True)
            raise RuntimeError(f"LSL Streamer failed to initialize: {e}") from e

    def setup_web_server(self):
        """Start the Web UI dashboard stub."""
        import secrets
        self.c.admin_token = secrets.token_urlsafe(16)
        self.c.view_token = secrets.token_urlsafe(16)
        self.c.web_server = None
        self.c.ws_server = None

    def setup_ble(self):
        """Initialize BLE emulation stack."""
        self.c.ble_server = None
        self.c.ble_link = None
        self.c.ble_client = None

    def setup_security(self):
        """Configure security detection and defenses."""
        self.c.ids = self.c.registry.create("security", "ids", twin=self.c.twin, event_bus=self.c.event_bus)
        self.c.ips = None
        self.c.link_guard = None

        if self.config.security.enabled:
            self.c.ips = self.c.registry.create(
                "security", "ips",
                twin=self.c.twin, ids=self.c.ids, event_bus=self.c.event_bus,
                max_stimulation_amplitude_ma=self.config.security.max_stimulation_amplitude_ma
            )
            self.c.link_guard = self.c.registry.create("security", "ble_guard", twin=self.c.twin, event_bus=self.c.event_bus)

        self.c.nsp_wrapper = None
        self.c.emulator = None
        self.c.fw_monitor = None
        self.c.p300_analyzer = self.c.registry.create("security", "p300_analyzer")
        self.c.e2ee_channel = self.c.registry.create("security", "e2ee_channel")
        self.c.biometric_gate = self.c.registry.create("security", "biometric_gate", authorized_profile={"alpha_peak_hz": 10.0})

        if getattr(self.config.security, 'enable_zta', False):
            self.c.zta_engine = self.c.registry.create("security", "zta_engine", thresholds=getattr(self.config.security, 'zta_thresholds', {}))

    def setup_privacy(self):
        """Configure privacy filters and trackers."""
        self.c.privacy_filter = None
        self.c.privacy_tracker = None
        if self.config.privacy.enabled:
            from vireon.runtime.privacy import DifferentialPrivacyFilter, PrivacyBudgetTracker
            self.c.privacy_filter = DifferentialPrivacyFilter(epsilon=self.config.privacy.epsilon)
            self.c.privacy_tracker = PrivacyBudgetTracker(max_epsilon=10.0)

    def setup_clinical(self):
        """Configure clinical simulation components."""
        self.c.clinical_sim = None
        self.c.dbs_controller = None
