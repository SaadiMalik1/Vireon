import warnings
from providers.dynamics.kuramoto import *  # noqa: F403

warnings.warn(
    "vireon.runtime.dynamics is deprecated and will be removed in v2.0. "
    "Import from providers.dynamics.kuramoto instead.",
    DeprecationWarning,
    stacklevel=2
)
