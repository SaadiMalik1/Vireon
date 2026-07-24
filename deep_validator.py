import re
import os
import ast

def check_file(repo_dir, filepath, methods_str):
    full_path = os.path.join(repo_dir, filepath)
    if not os.path.exists(full_path):
        return f"MISSING FILE: {filepath}"
    
    with open(full_path, 'r') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        return f"SYNTAX ERROR: {filepath}"

    # Extract all function names
    found_methods = set()
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            found_methods.add(node.name)
        elif isinstance(node, ast.ClassDef):
            for item in node.body:
                if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    found_methods.add(f"{node.name}.{item.name}")
                    found_methods.add(item.name)

    claimed_methods = [m.strip().replace('`', '') for m in methods_str.split(',')]
    missing_methods = []
    for claimed in claimed_methods:
        if claimed and claimed not in found_methods:
            # Handle cases like Class.method
            if '.' in claimed:
                if claimed not in found_methods:
                     missing_methods.append(claimed)
            else:
                 missing_methods.append(claimed)

    if missing_methods:
        return f"PARTIAL/MISSING METHODS in {filepath}: {', '.join(missing_methods)}"
    return None


def main():
    status_file = "/home/ronin/Documents/vireon/IMPLEMENTATION_STATUS.md"
    with open(status_file, 'r') as f:
        lines = f.readlines()
    
    print("--- DEEP VALIDATION ---")
    in_table = False
    for line in lines:
        if line.startswith("| **"):
            in_table = True
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 5:
                filepath = parts[2].replace('`', '')
                if filepath.endswith('/'): continue # Skip directories
                methods = parts[4]
                
                # Check file
                res = check_file("/home/ronin/Documents/vireon", filepath, methods)
                if res:
                    print(res)

if __name__ == "__main__":
    main()
