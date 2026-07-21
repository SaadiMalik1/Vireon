import warnings
from vireon.libraries.stride.stride import *  # noqa: F403

warnings.warn(
    "vireon.runtime.stride is deprecated and will be removed in v2.0. "
    "Import from vireon.libraries.stride.stride instead.",
    DeprecationWarning,
    stacklevel=2
)
