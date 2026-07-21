import warnings
from providers.clinical.validation import *  # noqa: F403

warnings.warn(
    "vireon.runtime.validation is deprecated and will be removed in v2.0. "
    "Import from providers.clinical.validation instead.",
    DeprecationWarning,
    stacklevel=2
)
