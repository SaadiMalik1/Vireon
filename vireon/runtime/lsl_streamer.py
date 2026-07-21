import warnings
from vireon.reference_providers.telemetry.lsl_streamer import *  # noqa: F403

warnings.warn(
    "vireon.runtime.lsl_streamer is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.telemetry.lsl_streamer instead.",
    DeprecationWarning,
    stacklevel=2
)
