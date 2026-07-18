import warnings
from vireon.reference_providers.telemetry.data_provider import *

warnings.warn(
    "vireon.runtime.data_provider is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.telemetry.data_provider instead.",
    DeprecationWarning,
    stacklevel=2
)
