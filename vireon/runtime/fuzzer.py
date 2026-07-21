import warnings
from vireon.reference_providers.protocol.fuzzer import *  # noqa: F403

warnings.warn(
    "vireon.runtime.fuzzer is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.protocol.fuzzer instead.",
    DeprecationWarning,
    stacklevel=2
)
