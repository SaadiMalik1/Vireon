import warnings
from vireon.reference_providers.physics.dynamics import *

warnings.warn(
    "vireon.runtime.dynamics is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.physics.dynamics instead.",
    DeprecationWarning,
    stacklevel=2
)
