import warnings
from providers.physics.thermal import *

warnings.warn(
    "vireon.runtime.physics is deprecated and will be removed in v2.0. "
    "Import from providers.physics.thermal instead.",
    DeprecationWarning,
    stacklevel=2
)
