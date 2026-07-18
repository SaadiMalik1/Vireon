import warnings
from vireon.services.spdf_auditor import *

warnings.warn(
    "vireon.runtime.spdf_auditor is deprecated and will be removed in v2.0. "
    "Import from vireon.services.spdf_auditor instead.",
    DeprecationWarning,
    stacklevel=2
)
