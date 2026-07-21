import warnings
from providers.authentication.e2ee import *  # noqa: F403

warnings.warn(
    "vireon.runtime.e2ee is deprecated and will be removed in v2.0. "
    "Import from providers.authentication.e2ee instead.",
    DeprecationWarning,
    stacklevel=2
)
