#!/usr/bin/env python3
import os
import re
import ast
import sys

def get_ast_names(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)
    
    names = set()
    class_methods = {}
    for node in tree.body:
        if isinstance(node, ast.FunctionDef):
            names.add(node.name)
        elif isinstance(node, ast.ClassDef):
            names.add(node.name)
            methods = set()
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    methods.add(item.name)
            class_methods[node.name] = methods
    return names, class_methods

def validate_docs(repo_root):
    doc_path = os.path.join(repo_root, "IMPLEMENTATION_STATUS.md")
    if not os.path.exists(doc_path):
        print(f"File not found: {doc_path}")
        return False
    
    with open(doc_path, "r", encoding="utf-8") as f:
        content = f.read()

    errors = 0
    # Parse markdown table
    for line in content.split("\n"):
        if line.strip().startswith("|") and not line.strip().startswith("| :---") and not line.strip().startswith("| Subsystem Component"):
            parts = [p.strip() for p in line.split("|")]
            if len(parts) >= 5:
                filepath = parts[2].replace("`", "")
                methods_str = parts[4]
                
                # Some are directories, skip them
                if filepath.endswith("/") or not filepath.endswith(".py"):
                    continue
                
                abs_filepath = os.path.join(repo_root, filepath)
                ast_data = get_ast_names(abs_filepath)
                if not ast_data:
                    # Ignore if file not found, we only validate claims for existing files
                    continue
                
                top_level_names, class_methods = ast_data
                
                # Extract claimed methods
                claimed = re.findall(r'`([^`]+)`', methods_str)
                for claim in claimed:
                    if "." in claim:
                        cls_name, method_name = claim.split(".", 1)
                        if cls_name not in top_level_names:
                            print(f"ERROR: Class '{cls_name}' claimed in {filepath} does not exist.")
                            errors += 1
                        elif method_name not in class_methods.get(cls_name, set()):
                            print(f"ERROR: Method '{method_name}' of class '{cls_name}' claimed in {filepath} does not exist.")
                            errors += 1
                    else:
                        found = False
                        if claim in top_level_names:
                            found = True
                        else:
                            for cls_name, methods in class_methods.items():
                                if claim in methods:
                                    found = True
                                    break
                        if not found:
                            print(f"ERROR: Function/Class/Method '{claim}' claimed in {filepath} does not exist.")
                            errors += 1

    if errors > 0:
        print(f"\nValidation failed with {errors} fabricated API claims.")
        return False
    
    print("Documentation accurately reflects codebase APIs.")
    return True

if __name__ == "__main__":
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if not validate_docs(repo_root):
        sys.exit(1)
    sys.exit(0)
