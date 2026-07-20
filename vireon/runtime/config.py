import warnings
from vireon.runtime.configuration import *

warnings.warn(
    "vireon.runtime.config is deprecated and will be removed in v2.0. "
    "Import from vireon.runtime.configuration instead.",
    DeprecationWarning,
    stacklevel=2
)
