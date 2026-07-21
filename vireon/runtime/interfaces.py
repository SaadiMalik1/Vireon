import warnings
from vireon.sdk.base_interfaces import *  # noqa: F403

warnings.warn(
    "vireon.runtime.interfaces is deprecated and will be removed in v2.0. "
    "Import from vireon.sdk.base_interfaces instead.",
    DeprecationWarning,
    stacklevel=2
)
