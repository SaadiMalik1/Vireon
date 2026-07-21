import warnings
from vireon.reference_providers.security.zta import *  # noqa: F403

warnings.warn(
    "vireon.runtime.zta is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.security.zta instead.",
    DeprecationWarning,
    stacklevel=2
)
