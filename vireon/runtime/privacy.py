import warnings
from providers.privacy.analysis import *  # noqa: F403

warnings.warn(
    "vireon.runtime.privacy is deprecated and will be removed in v2.0. "
    "Import from providers.privacy.analysis instead.",
    DeprecationWarning,
    stacklevel=2
)
