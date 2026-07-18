import warnings
from vireon.reference_providers.physics.physics import *

warnings.warn(
    "vireon.runtime.physics is deprecated and will be removed in v2.0. "
    "Import from vireon.reference_providers.physics.physics instead.",
    DeprecationWarning,
    stacklevel=2
)
