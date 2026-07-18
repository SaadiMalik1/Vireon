import warnings
from vireon.reference_providers.clinical.compliance import *

warnings.warn(
    "vireon.runtime.compliance is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.clinical.compliance instead.",
    DeprecationWarning,
    stacklevel=2
)
