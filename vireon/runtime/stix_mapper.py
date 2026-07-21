import warnings
from vireon.libraries.stix.stix_mapper import *  # noqa: F403

warnings.warn(
    "vireon.runtime.stix_mapper is deprecated and will be removed in v2.0. "
    "Import from vireon.libraries.stix.stix_mapper instead.",
    DeprecationWarning,
    stacklevel=2
)
