import warnings
from vireon.services.engine import *  # noqa: F403

warnings.warn(
    "vireon.runtime.engine is deprecated and will be removed in v2.0. "
    "Import from vireon.services.engine instead.",
    DeprecationWarning,
    stacklevel=2
)
