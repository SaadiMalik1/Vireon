import warnings
from providers.protocol.ble import *  # noqa: F403

warnings.warn(
    "vireon.runtime.protocol is deprecated and will be removed in v2.0. "
    "Import from providers.protocol.ble instead.",
    DeprecationWarning,
    stacklevel=2
)
