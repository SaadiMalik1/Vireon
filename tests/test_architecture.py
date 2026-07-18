import ast
import os
import pytest

def get_all_python_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                yield os.path.join(root, file)

def get_imports(filepath):
    with open(filepath, 'r') as f:
        try:
            tree = ast.parse(f.read(), filename=filepath)
        except SyntaxError:
            return set()

    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                imports.add(node.module)
    return imports

def test_runtime_dependencies():
    """
    The runtime must be clean. It cannot import from domain libraries
    or from the providers layer.
    """
    runtime_dir = os.path.join(os.path.dirname(__file__), '../vireon/runtime')
    
    banned_external_libs = {'numpy', 'torch', 'brainflow', 'mne', 'bleak', 'scipy'}
    banned_internal_layers = {
        'vireon.reference_providers',
        'vireon.libraries',
        'vireon.services'
    }

    violations = []

    for filepath in get_all_python_files(runtime_dir):
        # Skip stub files which are explicitly allowed to import from providers 
        # for the Strangler Fig deprecation period
        with open(filepath, 'r') as f:
            content = f.read()
            if 'DeprecationWarning' in content:
                continue

        imports = get_imports(filepath)
        for imp in imports:
            # Check banned external
            base_module = imp.split('.')[0]
            if base_module in banned_external_libs:
                violations.append(f"{filepath} imports banned external library: {imp}")
            
            # Check banned internal
            for banned_layer in banned_internal_layers:
                if imp.startswith(banned_layer):
                    violations.append(f"{filepath} imports banned internal layer: {imp}")

    assert not violations, "Architecture violations found in runtime:\n" + "\n".join(violations)

def test_sdk_dependencies():
    """
    The SDK must be pure. It cannot import from runtime or providers.
    """
    sdk_dir = os.path.join(os.path.dirname(__file__), '../vireon/sdk')
    
    banned_internal_layers = {
        'vireon.runtime',
        'vireon.reference_providers',
        'vireon.libraries',
        'vireon.services'
    }

    violations = []

    for filepath in get_all_python_files(sdk_dir):
        imports = get_imports(filepath)
        for imp in imports:
            for banned_layer in banned_internal_layers:
                if imp.startswith(banned_layer):
                    violations.append(f"{filepath} imports banned internal layer: {imp}")

    assert not violations, "Architecture violations found in SDK:\n" + "\n".join(violations)
