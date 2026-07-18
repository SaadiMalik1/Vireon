import warnings
from vireon.reference_providers.security.privacy import *

warnings.warn(
    "vireon.runtime.privacy is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.security.privacy instead.",
    DeprecationWarning,
    stacklevel=2
)
