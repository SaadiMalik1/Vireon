import warnings
from providers.threat_models.redteam import *  # noqa: F403

warnings.warn(
    "vireon.runtime.redteam is deprecated and will be removed in v2.0. "
    "Import from providers.threat_models.redteam instead.",
    DeprecationWarning,
    stacklevel=2
)
