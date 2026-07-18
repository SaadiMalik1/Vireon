import warnings
from vireon.services.sbom import *

warnings.warn(
    "vireon.runtime.sbom is deprecated and will be removed in v2.0. "
    "Import from vireon.services.sbom instead.",
    DeprecationWarning,
    stacklevel=2
)
