import warnings
from vireon.reference_providers.security.privacy_leakage import *

warnings.warn(
    "vireon.runtime.privacy_leakage is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.security.privacy_leakage instead.",
    DeprecationWarning,
    stacklevel=2
)
