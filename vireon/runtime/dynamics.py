import warnings
from providers.dynamics.kuramoto import *

warnings.warn(
    "vireon.runtime.dynamics is deprecated and will be removed in v2.0. "
    "Import from providers.dynamics.kuramoto instead.",
    DeprecationWarning,
    stacklevel=2
)
