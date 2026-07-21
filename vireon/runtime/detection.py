import warnings
from providers.ids.detection import *

warnings.warn(
    "vireon.runtime.detection is deprecated and will be removed in v2.0. "
    "Import from providers.ids.detection instead.",
    DeprecationWarning,
    stacklevel=2
)
