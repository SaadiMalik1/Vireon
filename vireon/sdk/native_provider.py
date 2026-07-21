# Copyright 2026 VIREON Contributors

import ctypes
import json
import logging
from typing import Optional
from typing import Any

from vireon.sdk.provider_interfaces.v1 import (
    IPhysicsProviderV1,
    IIDSProviderV1,
    IClinicalProviderV1
)
from vireon.sdk.capability.descriptor import CapabilityDescriptor
from vireon.sdk.services.apis import RuntimeServices

logger = logging.getLogger(__name__)

# --- CTypes Definitions for vireon_abi.h ---
# typedef struct {
#     bool (*state_get_float)(const char* key, float* out_val);
#     bool (*state_set_float)(const char* key, float val);
#     bool (*state_get_string)(const char* key, char* out_buf, int max_len);
#     bool (*state_set_string)(const char* key, const char* val);
#     void (*telemetry_publish)(int channel, float value);
#     void (*log_info)(const char* msg);
#     void (*log_error)(const char* msg);
# } VireonRuntimeServices;

STATE_GET_FLOAT_FUNC = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_char_p, ctypes.POINTER(ctypes.c_float))
STATE_SET_FLOAT_FUNC = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_char_p, ctypes.c_float)
STATE_GET_STRING_FUNC = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p, ctypes.c_int)
STATE_SET_STRING_FUNC = ctypes.CFUNCTYPE(ctypes.c_bool, ctypes.c_char_p, ctypes.c_char_p)

TELEMETRY_PUBLISH_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_int, ctypes.c_float)
LOG_INFO_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p)
LOG_ERROR_FUNC = ctypes.CFUNCTYPE(None, ctypes.c_char_p)

class CVireonRuntimeServices(ctypes.Structure):
    _fields_ = [
        ("state_get_float", STATE_GET_FLOAT_FUNC),
        ("state_set_float", STATE_SET_FLOAT_FUNC),
        ("state_get_string", STATE_GET_STRING_FUNC),
        ("state_set_string", STATE_SET_STRING_FUNC),
        ("telemetry_publish", TELEMETRY_PUBLISH_FUNC),
        ("log_info", LOG_INFO_FUNC),
        ("log_error", LOG_ERROR_FUNC),
    ]


class NativeProviderLoader(IPhysicsProviderV1, IIDSProviderV1, IClinicalProviderV1):
    """
    Python wrapper that loads a C-ABI compliant shared library and 
    presents it to the Orchestrator as a standard Python provider.
    """
    def __init__(self, lib_path: str):
        self.lib_path = lib_path
        self._lib = ctypes.CDLL(lib_path)
        
        # Bind the exported functions
        self._lib.vireon_get_descriptor.restype = ctypes.c_char_p
        self._lib.vireon_initialize.argtypes = [ctypes.POINTER(CVireonRuntimeServices)]
        self._lib.vireon_initialize.restype = ctypes.c_int
        self._lib.vireon_health.restype = ctypes.c_char_p
        
        # Load capability descriptor
        desc_json = self._lib.vireon_get_descriptor().decode('utf-8')
        self._descriptor = CapabilityDescriptor.parse_raw(desc_json)
        self.services: Optional[RuntimeServices] = None
        self._c_services: Optional[CVireonRuntimeServices] = None
        
        # Try to load optional interface methods
        if "IPhysicsProviderV1" in self._descriptor.implements:
            self._lib.vireon_physics_step.argtypes = [ctypes.c_float]
            
        if "IIDSProviderV1" in self._descriptor.implements:
            # bool vireon_ids_analyze_window(const float* data, int num_samples, int num_channels);
            self._lib.vireon_ids_analyze_window.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int]
            self._lib.vireon_ids_analyze_window.restype = ctypes.c_bool
            
        if "IClinicalProviderV1" in self._descriptor.implements:
            # void vireon_clinical_evaluate_biomarker(const float* data, int num_samples, int num_channels);
            self._lib.vireon_clinical_evaluate_biomarker.argtypes = [ctypes.POINTER(ctypes.c_float), ctypes.c_int, ctypes.c_int]

    @property
    def descriptor(self) -> CapabilityDescriptor:
        return self._descriptor

    def initialize(self, services: RuntimeServices) -> None:
        self.services = services
        
        # Create C callbacks
        def _get_float(k, out):
            val = self.services.state.get(k.decode('utf-8'))
            if val is not None and isinstance(val, (int, float)):
                out[0] = float(val)
                return True
            return False
            
        def _set_float(k, val):
            self.services.state.set(k.decode('utf-8'), float(val))
            return True
            
        def _get_string(k, out_buf, max_len):
            val = self.services.state.get(k.decode('utf-8'))
            if val is not None:
                encoded = str(val).encode('utf-8')
                if len(encoded) < max_len:
                    ctypes.memmove(out_buf, encoded, len(encoded))
                    out_buf[len(encoded)] = 0
                    return True
            return False
            
        def _set_string(k, val):
            self.services.state.set(k.decode('utf-8'), val.decode('utf-8'))
            return True
            
        def _telemetry_publish(channel, val):
            if self.services.telemetry:
                self.services.telemetry.publish(channel, float(val))
                
        def _log_info(msg):
            logger.info(f"[{self._descriptor.id}] {msg.decode('utf-8')}")
            
        def _log_error(msg):
            logger.error(f"[{self._descriptor.id}] {msg.decode('utf-8')}")
            
        # Hold references to prevent garbage collection
        self._cb_get_float = STATE_GET_FLOAT_FUNC(_get_float)
        self._cb_set_float = STATE_SET_FLOAT_FUNC(_set_float)
        self._cb_get_string = STATE_GET_STRING_FUNC(_get_string)
        self._cb_set_string = STATE_SET_STRING_FUNC(_set_string)
        self._cb_telemetry_publish = TELEMETRY_PUBLISH_FUNC(_telemetry_publish)
        self._cb_log_info = LOG_INFO_FUNC(_log_info)
        self._cb_log_error = LOG_ERROR_FUNC(_log_error)
        
        self._c_services = CVireonRuntimeServices(
            self._cb_get_float,
            self._cb_set_float,
            self._cb_get_string,
            self._cb_set_string,
            self._cb_telemetry_publish,
            self._cb_log_info,
            self._cb_log_error
        )
        
        res = self._lib.vireon_initialize(ctypes.byref(self._c_services))
        if res != 0:
            raise RuntimeError(f"Native provider initialization failed with code {res}")
        logger.info(f"[NativeProviderLoader] Initialized {self._descriptor.id} from {self.lib_path}")

    def health(self) -> dict:
        health_json = self._lib.vireon_health().decode('utf-8')
        return json.loads(health_json)

    # IPhysicsProviderV1
    def step_physics(self, dt: float) -> None:
        self._lib.vireon_physics_step(ctypes.c_float(dt))
        
    # IIDSProviderV1
    def analyze_window(self, data: Any) -> bool:
        if data is None or len(data.shape) < 2:
            return False
        num_samples = data.shape[0]
        num_channels = data.shape[1]
        # Flatten and convert to ctypes array
        c_data = data.flatten().astype('float32').ctypes.data_as(ctypes.POINTER(ctypes.c_float))
        return self._lib.vireon_ids_analyze_window(c_data, ctypes.c_int(num_samples), ctypes.c_int(num_channels))
        
    # IClinicalProviderV1
    def evaluate_biomarker(self, data: Any) -> dict:
        if data is not None and len(data.shape) >= 2:
            num_samples = data.shape[0]
            num_channels = data.shape[1]
            c_data = data.flatten().astype('float32').ctypes.data_as(ctypes.POINTER(ctypes.c_float))
            self._lib.vireon_clinical_evaluate_biomarker(c_data, ctypes.c_int(num_samples), ctypes.c_int(num_channels))
        return {}
