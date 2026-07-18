import warnings
from vireon.reference_providers.protocol.protocol import *

warnings.warn(
    "vireon.runtime.protocol is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.protocol.protocol instead.",
    DeprecationWarning,
    stacklevel=2
)
