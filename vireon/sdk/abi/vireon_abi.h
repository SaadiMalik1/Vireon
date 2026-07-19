#ifndef VIREON_ABI_H
#define VIREON_ABI_H

#include <stdint.h>
#include <stdbool.h>

#ifdef __cplusplus
extern "C" {
#endif

// --- Runtime Services (Host -> Plugin) ---
// Injected by the orchestrator. Operations are backed by Zero-Trust Python Enforcement APIs.
typedef struct {
    bool (*state_get_float)(const char* key, float* out_val);
    bool (*state_set_float)(const char* key, float val);
    bool (*state_get_string)(const char* key, char* out_buf, int max_len);
    bool (*state_set_string)(const char* key, const char* val);
    
    void (*telemetry_publish)(int channel, float value);
    void (*log_info)(const char* msg);
    void (*log_error)(const char* msg);
} VireonRuntimeServices;

// --- Provider Interface (Plugin -> Host) ---
// All shared libraries (.so / .dll) MUST export these functions.

// 1. Return a JSON string representing the CapabilityDescriptor
const char* vireon_get_descriptor(void);

// 2. Initialize with injected services
int vireon_initialize(const VireonRuntimeServices* services);

// 3. Health check (returns JSON string)
const char* vireon_health(void);

// 4. Interface implementations (only export what you implement)
void vireon_physics_step(float dt);
bool vireon_ids_analyze_window(const float* data, int num_samples, int num_channels);
void vireon_clinical_evaluate_biomarker(const float* data, int num_samples, int num_channels);

#ifdef __cplusplus
}
#endif

#endif // VIREON_ABI_H
