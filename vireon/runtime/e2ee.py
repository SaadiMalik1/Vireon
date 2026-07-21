import warnings
from providers.authentication.e2ee import *

warnings.warn(
    "vireon.runtime.e2ee is deprecated and will be removed in v2.0. "
    "Import from providers.authentication.e2ee instead.",
    DeprecationWarning,
    stacklevel=2
)
