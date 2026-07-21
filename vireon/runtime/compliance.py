import warnings
from providers.clinical.compliance import *  # noqa: F403

warnings.warn(
    "vireon.runtime.compliance is deprecated and will be removed in v2.0. "
    "Import from providers.clinical.compliance instead.",
    DeprecationWarning,
    stacklevel=2
)
