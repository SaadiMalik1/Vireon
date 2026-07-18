import warnings
from vireon.reference_providers.ids.safety_envelope import *

warnings.warn(
    "vireon.runtime.safety_envelope is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.ids.safety_envelope instead.",
    DeprecationWarning,
    stacklevel=2
)
