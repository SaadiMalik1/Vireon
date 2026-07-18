import warnings
from vireon.reference_providers.clinical.validation import *

warnings.warn(
    "vireon.runtime.validation is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.clinical.validation instead.",
    DeprecationWarning,
    stacklevel=2
)
