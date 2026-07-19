#include <stdio.h>
#include <string.h>
#include "../../sdk/abi/vireon_abi.h"

// Static reference to the injected services
static VireonRuntimeServices g_services;

const char* vireon_get_descriptor(void) {
    // Return a JSON string representing the CapabilityDescriptor
    return "{"
           "\"id\": \"vireon.reference.native_dummy\","
           "\"implements\": [\"IPhysicsProviderV1\"],"
           "\"requires\": {\"api\": \"IStateAPI\"},"
           "\"permissions\": ["
           "    \"state.read:battery_voltage\","
           "    \"state.mutate:tissue_temperature\""
           "],"
           "\"features\": [\"c_abi_test\"],"
           "\"latency\": \"hard-realtime\""
           "}";
}

int vireon_initialize(const VireonRuntimeServices* services) {
    g_services = *services;
    if (g_services.log_info) {
        g_services.log_info("Native Dummy Provider Initialized via C ABI.");
    }
    return 0; // Success
}

const char* vireon_health(void) {
    return "{\"status\": \"ok\", \"native\": true}";
}

void vireon_physics_step(float dt) {
    if (!g_services.state_get_float || !g_services.state_set_float) {
        return;
    }
    
    float battery = 0.0f;
    // Attempt to read battery voltage
    bool read_success = g_services.state_get_float("battery_voltage", &battery);
    
    if (read_success && g_services.log_info) {
        char buf[64];
        snprintf(buf, sizeof(buf), "Read battery_voltage: %.2f", battery);
        g_services.log_info(buf);
    }
    
    // Attempt to mutate tissue temperature
    g_services.state_set_float("tissue_temperature", 38.5f + dt);
}
