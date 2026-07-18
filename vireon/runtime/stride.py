import warnings
from vireon.libraries.stride.stride import *

warnings.warn(
    "vireon.runtime.stride is deprecated and will be removed in v2.0. "
    "Import from vireon.libraries.stride.stride instead.",
    DeprecationWarning,
    stacklevel=2
)
