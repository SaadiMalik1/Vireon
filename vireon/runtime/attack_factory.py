import warnings
from providers.threat_models.attacks import *  # noqa: F403

warnings.warn(
    "vireon.runtime.attack_factory is deprecated and will be removed in v2.0. "
    "Import from providers.threat_models.attacks instead.",
    DeprecationWarning,
    stacklevel=2
)
