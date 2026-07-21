import warnings
from providers.authentication.tokens import *  # noqa: F403

warnings.warn(
    "vireon.runtime.authentication is deprecated and will be removed in v2.0. "
    "Import from providers.authentication.tokens instead.",
    DeprecationWarning,
    stacklevel=2
)
