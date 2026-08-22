from __future__ import annotations

import argparse
import ast
import json
import subprocess
from pathlib import Path
from typing import Any


MUTATOR_METHODS = {
    "add_offset",
    "append",
    "clear",
    "create",
    "delete",
    "discard",
    "extend",
    "insert",
    "pop",
    "remove",
    "save",
    "setdefault",
    "shuffle",
    "sort",
    "update",
    "update_delay",
}
RNG_METHODS = {
    "choice",
    "choices",
    "gauss",
    "getrandbits",
    "normalvariate",
    "randint",
    "random",
    "randrange",
    "sample",
    "shuffle",
    "uniform",
}


def parse_file(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def git_revision(root: Path) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=True,
    )
    return result.stdout.strip()


def decorator_name(decorator: ast.AST) -> str | None:
    target = decorator.func if isinstance(decorator, ast.Call) else decorator
    if isinstance(target, ast.Name):
        return target.id
    if isinstance(target, ast.Attribute):
        return target.attr
    return None


def is_read_registered(function: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    for decorator in function.decorator_list:
        if not isinstance(decorator, ast.Call) or decorator_name(decorator) != "event_registered":
            continue
        for keyword in decorator.keywords:
            value = keyword.value
            if (
                keyword.arg == "operation_type"
                and isinstance(value, ast.Attribute)
                and value.attr == "READ"
            ):
                return True
    return False


def exposed_roles(function: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    roles = []
    mapping = {
        "app_tool": "agent",
        "data_tool": "data",
        "env_tool": "environment",
        "user_tool": "user",
    }
    for decorator in function.decorator_list:
        name = decorator_name(decorator)
        if name in mapping:
            roles.append(mapping[name])
    return sorted(set(roles))


def rooted_at_self(node: ast.AST) -> bool:
    if isinstance(node, ast.Name):
        return node.id == "self"
    if isinstance(node, (ast.Attribute, ast.Subscript)):
        return rooted_at_self(node.value)
    return False


def call_path(node: ast.AST) -> str | None:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = call_path(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return None


def conservative_flags(function: ast.FunctionDef | ast.AsyncFunctionDef) -> list[dict[str, Any]]:
    flags: list[dict[str, Any]] = []
    for node in ast.walk(function):
        targets: list[ast.AST] = []
        if isinstance(node, ast.Assign):
            targets = node.targets
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
        elif isinstance(node, ast.AugAssign):
            targets = [node.target]
        for target in targets:
            if isinstance(target, ast.Attribute):
                flags.append(
                    {
                        "line": node.lineno,
                        "kind": "attribute_assignment",
                        "target": call_path(target),
                        "self_rooted": rooted_at_self(target),
                    }
                )
            elif isinstance(target, ast.Subscript) and rooted_at_self(target):
                flags.append(
                    {
                        "line": node.lineno,
                        "kind": "self_subscript_assignment",
                        "target": call_path(target),
                        "self_rooted": True,
                    }
                )

        if not isinstance(node, ast.Call):
            continue
        name = None
        receiver = None
        if isinstance(node.func, ast.Attribute):
            name = node.func.attr
            receiver = node.func.value
        elif isinstance(node.func, ast.Name):
            name = node.func.id
        if name in MUTATOR_METHODS or name in RNG_METHODS:
            flags.append(
                {
                    "line": node.lineno,
                    "kind": f"call:{name}",
                    "target": call_path(node.func),
                    "self_rooted": rooted_at_self(receiver) if receiver is not None else False,
                }
            )
        elif receiver is not None and rooted_at_self(receiver):
            flags.append(
                {
                    "line": node.lineno,
                    "kind": "self_method_call",
                    "target": call_path(node.func),
                    "self_rooted": True,
                }
            )
    unique = {
        (item["line"], item["kind"], item["target"], item["self_rooted"]): item for item in flags
    }
    return sorted(unique.values(), key=lambda item: (item["line"], item["kind"], str(item["target"])))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--are-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    root = args.are_root.resolve()

    items = []
    apps_root = root / "are" / "simulation" / "apps"
    for path in sorted(apps_root.glob("*.py")):
        tree = parse_file(path)
        for class_node in (node for node in tree.body if isinstance(node, ast.ClassDef)):
            for function in (
                node
                for node in class_node.body
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
            ):
                if not is_read_registered(function):
                    continue
                roles = exposed_roles(function)
                if not roles:
                    continue
                flags = conservative_flags(function)
                items.append(
                    {
                        "class": class_node.name,
                        "function": function.name,
                        "roles": roles,
                        "file": str(path.relative_to(root)).replace("\\", "/"),
                        "line": function.lineno,
                        "flags": flags,
                    }
                )

    result = {
        "repository": "facebookresearch/meta-agents-research-environments",
        "revision": git_revision(root),
        "scope": (
            "Conservative AST audit of statically declared READ methods exposed as agent/data/environment/user tools. "
            "Flags require manual review and are not automatically interpreted as task-state effects."
        ),
        "declared_read_methods": len(items),
        "flagged_methods": sum(bool(item["flags"]) for item in items),
        "items": items,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
