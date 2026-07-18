import warnings
from vireon.reference_providers.security.authentication import *

warnings.warn(
    "vireon.runtime.authentication is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.security.authentication instead.",
    DeprecationWarning,
    stacklevel=2
)
