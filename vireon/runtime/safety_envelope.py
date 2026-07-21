import warnings
from providers.clinical.safety import *  # noqa: F403

warnings.warn(
    "vireon.runtime.safety_envelope is deprecated and will be removed in v2.0. "
    "Import from providers.clinical.safety instead.",
    DeprecationWarning,
    stacklevel=2
)
