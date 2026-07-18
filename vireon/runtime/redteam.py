import warnings
from vireon.libraries.redteam.redteam import *

warnings.warn(
    "vireon.runtime.redteam is deprecated and will be removed in v2.0. "
    "Import from vireon.libraries.redteam.redteam instead.",
    DeprecationWarning,
    stacklevel=2
)
