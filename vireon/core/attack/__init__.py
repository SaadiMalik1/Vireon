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

from .base import ISignalModifier
from .engine import SignalAttackEngine
from .scenario import AttackStep, AttackScenario

from .cognitive import (
    NeuroPhishingAttack,
    FirmwareRollbackAttack,
    InsiderThreatAttack
)

from .adversarial import (
    AdversarialOptimizerAttack,
    TraceReplayAttack,
    RFJammingAttack,
    FramingDesynchronizationAttack,
    SessionReplayAttack,
    TemporalEvasionAttack
)

from .physical import (
    ElectrodeSaturationAttack,
    PacketLossAttack,
    TimingJitterAttack,
    DropoutAttack,
    ClippingAttack,
    AmplifierSaturationAttack,
    EMIAttack,
    MotionArtifactAttack,
    CrossTalkAttack,
    ClockSkewAttack
)

from .modifiers import (
    NoiseInjectionAttack,
    SignalDriftAttack,
    ImpedanceSpikeAttack,
    SignalSuppressionAttack
)

__all__ = [
    "ISignalModifier",
    "SignalAttackEngine",
    "AttackStep",
    "AttackScenario",
    "NeuroPhishingAttack",
    "FirmwareRollbackAttack",
    "InsiderThreatAttack",
    "AdversarialOptimizerAttack",
    "TraceReplayAttack",
    "RFJammingAttack",
    "FramingDesynchronizationAttack",
    "SessionReplayAttack",
    "TemporalEvasionAttack",
    "ElectrodeSaturationAttack",
    "PacketLossAttack",
    "TimingJitterAttack",
    "DropoutAttack",
    "ClippingAttack",
    "AmplifierSaturationAttack",
    "EMIAttack",
    "MotionArtifactAttack",
    "CrossTalkAttack",
    "ClockSkewAttack",
    "NoiseInjectionAttack",
    "SignalDriftAttack",
    "ImpedanceSpikeAttack",
    "SignalSuppressionAttack"
]
