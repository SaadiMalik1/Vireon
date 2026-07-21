import warnings
from providers.privacy.leakage import *  # noqa: F403

warnings.warn(
    "vireon.runtime.privacy_leakage is deprecated and will be removed in v2.0. "
    "Import from providers.privacy.leakage instead.",
    DeprecationWarning,
    stacklevel=2
)
