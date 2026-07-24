import os
import re

def fix_docs(repo_root):
    doc_path = os.path.join(repo_root, "IMPLEMENTATION_STATUS.md")
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    # The errors from the validator output
    errors_raw = """
ERROR: Function/Class/Method 'stop_all' claimed in vireon/runtime/orchestrator.py does not exist.
ERROR: Function/Class/Method 'set_sim_time' claimed in vireon/runtime/clock.py does not exist.
ERROR: Function/Class/Method 'get_wall_time' claimed in vireon/runtime/clock.py does not exist.
ERROR: Function/Class/Method 'get_sim_time' claimed in vireon/runtime/clock.py does not exist.
ERROR: Function/Class/Method 'get_event_history' claimed in vireon/runtime/event_bus.py does not exist.
ERROR: Function/Class/Method 'delete' claimed in vireon/runtime/state_store.py does not exist.
ERROR: Function/Class/Method 'create_event_bus_proxy' claimed in vireon/runtime/capability_engine.py does not exist.
ERROR: Function/Class/Method 'create_state_store_proxy' claimed in vireon/runtime/capability_engine.py does not exist.
ERROR: Method 'set' of class 'LWWRegister' claimed in vireon/runtime/crdt_store.py does not exist.
ERROR: Function/Class/Method 'peek' claimed in vireon/runtime/ring_buffer.py does not exist.
ERROR: Function/Class/Method 'clear' claimed in vireon/runtime/ring_buffer.py does not exist.
ERROR: Function/Class/Method 'export_bundle' claimed in vireon/runtime/trace_bundle.py does not exist.
ERROR: Function/Class/Method 'format_telemetry_table' claimed in vireon/runtime/coordinator.py does not exist.
ERROR: Function/Class/Method 'run_dashboard_loop' claimed in vireon/runtime/coordinator.py does not exist.
ERROR: Method 'from_yaml' of class 'CapabilityManifest' claimed in vireon/sdk/manifest.py does not exist.
ERROR: Method 'load_so' of class 'NativeProviderLoader' claimed in vireon/sdk/native_provider.py does not exist.
ERROR: Function/Class/Method 'call_init' claimed in vireon/sdk/native_provider.py does not exist.
ERROR: Function/Class/Method 'call_step' claimed in vireon/sdk/native_provider.py does not exist.
ERROR: Method 'start' of class 'SubprocessProvider' claimed in vireon/sdk/subprocess_provider.py does not exist.
ERROR: Function/Class/Method 'send_cmd' claimed in vireon/sdk/subprocess_provider.py does not exist.
ERROR: Function/Class/Method 'receive_telemetry' claimed in vireon/sdk/subprocess_provider.py does not exist.
ERROR: Function/Class/Method 'apply_temporal_jitter' claimed in vireon/sdk/anonymizer.py does not exist.
ERROR: Function/Class/Method 'permute_channels' claimed in vireon/sdk/anonymizer.py does not exist.
ERROR: Function/Class/Method 'apply_spectral_mask' claimed in vireon/sdk/anonymizer.py does not exist.
ERROR: Function/Class/Method 'calculate_privacy_risk' claimed in vireon/sdk/anonymizer.py does not exist.
ERROR: Function/Class/Method 'generate_chunk' claimed in vireon/datasets/synthetic.py does not exist.
ERROR: Function/Class/Method 'run_full_benchmark_matrix' claimed in scripts/run_validation.py does not exist.
    """
    
    # Extract terms to remove
    to_remove = []
    for line in errors_raw.split('\n'):
        if not line.strip(): continue
        match = re.search(r"'(.*?)' claimed in", line)
        if match:
            term = match.group(1)
            # handle class.method format
            to_remove.append(term)
            
    # Also sandbox issues from our changes
    to_remove.extend(['generate_seccomp_profile', 'set_seccomp_strict_mode'])

    # Modify lines
    new_lines = []
    for line in content.split('\n'):
        if line.startswith('|'):
            parts = line.split('|')
            if len(parts) >= 5:
                methods_str = parts[4]
                # we want to strip the items to_remove from the methods_str
                # methods are formatted like `method1`, `method2`
                # Let's rebuild the methods str
                claimed = re.findall(r'`([^`]+)`', methods_str)
                kept = [c for c in claimed if c not in to_remove and not any(c.endswith("." + r) for r in to_remove if "." not in r)]
                
                # Special fix for sandbox
                if 'sandbox.py' in line:
                    if 'generate_profile' not in kept:
                        kept.append('SeccompProfileGenerator.generate_profile')
                    if 'set_seccomp_filter_mode' not in kept:
                        kept.append('set_seccomp_filter_mode')
                        
                parts[4] = " " + ", ".join([f"`{c}`" for c in kept]) + " "
                line = "|".join(parts)
        new_lines.append(line)
        
    with open(doc_path, "w", encoding="utf-8") as f:
        f.write("\n".join(new_lines))

if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    fix_docs(repo_root)
