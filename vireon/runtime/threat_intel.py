import warnings
from vireon.libraries.stix.threat_intel import *

warnings.warn(
    "vireon.runtime.threat_intel is deprecated and will be removed in v2.0. "
    "Import from vireon.libraries.stix.threat_intel instead.",
    DeprecationWarning,
    stacklevel=2
)
