import warnings
from providers.threat_models.intel import *  # noqa: F403

warnings.warn(
    "vireon.runtime.threat_intel is deprecated and will be removed in v2.0. "
    "Import from providers.threat_models.intel instead.",
    DeprecationWarning,
    stacklevel=2
)
