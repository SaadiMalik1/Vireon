import warnings
from vireon.libraries.attack_factory.attack_factory import *

warnings.warn(
    "vireon.runtime.attack_factory is deprecated and will be removed in v2.0. "
    "Import from vireon.libraries.attack_factory.attack_factory instead.",
    DeprecationWarning,
    stacklevel=2
)
