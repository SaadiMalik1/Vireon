import os
import ast

def audit_file(filepath):
    if not os.path.exists(filepath):
        print(f"MISSING: {filepath}")
        return
    with open(filepath, 'r') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        print(f"SYNTAX ERROR: {filepath}")
        return

    issues = []
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.AsyncFunctionDef):
            body = node.body
            # Check if body is just pass or ...
            if len(body) == 1:
                if isinstance(body[0], ast.Pass):
                    issues.append(f"Function {node.name} is empty (pass).")
                elif isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and body[0].value.value is Ellipsis:
                    issues.append(f"Function {node.name} is empty (...).")
                elif isinstance(body[0], ast.Raise) and isinstance(body[0].exc, ast.Call) and getattr(body[0].exc.func, 'id', '') == 'NotImplementedError':
                    issues.append(f"Function {node.name} raises NotImplementedError.")
            
            # check for simple mock returns
            if len(body) == 1 and isinstance(body[0], ast.Return):
                issues.append(f"Function {node.name} just returns a single value, possible mock.")

    if "TODO" in content:
        issues.append("Contains TODOs.")
    if "mock" in content.lower():
        issues.append("Contains 'mock' in code/comments.")

    if issues:
        print(f"\n--- ISSUES IN {filepath} ---")
        for issue in issues:
            print("  - " + issue)

files_to_check = [
    "vireon/runtime/sandbox.py",
    "vireon/runtime/guardrails.py",
    "vireon/runtime/merkle.py",
    "vireon/runtime/crdt_store.py",
    "vireon/runtime/trace_bundle.py",
    "vireon/runtime/coordinator.py",
    "vireon/sdk/anonymizer.py",
    "scripts/generate_evidence.py",
    "../vireon-lab/vireon_lab/engine/generators/jansen_rit.py",
    "../vireon-lab/vireon_lab/engine/attacks/mutators.py",
    "../vireon-lab/dashboard/forensic_exporter.py"
]

for f in files_to_check:
    audit_file(f)
