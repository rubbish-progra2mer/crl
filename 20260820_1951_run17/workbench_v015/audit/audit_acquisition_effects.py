from __future__ import annotations

import argparse
import ast
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Iterable


ACQUISITION_PREFIXES = ("get_", "list_", "search_", "find_", "show_", "read_")
CONTEXT_MUTATORS = {
    "add_to_database",
    "remove_from_database",
    "update_database",
}
PERSISTENCE_METHODS = {
    "save",
    "delete",
    "create",
    "commit",
    "flush",
    "write",
    "write_text",
    "write_bytes",
    "unlink",
    "mkdir",
    "rename",
    "replace",
}
CONTAINER_MUTATORS = {"append", "extend", "insert", "pop", "remove", "clear", "update"}


def parse_file(path: Path) -> ast.Module:
    return ast.parse(path.read_text(encoding="utf-8"), filename=str(path))


def git_revision(root: Path) -> str | None:
    result = subprocess.run(
        ["git", "-C", str(root), "rev-parse", "HEAD"],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.stdout.strip() if result.returncode == 0 else None


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def call_name(call: ast.Call) -> str | None:
    function = call.func
    if isinstance(function, ast.Name):
        return function.id
    if isinstance(function, ast.Attribute):
        return function.attr
    return None


def decorator_call(function: ast.FunctionDef | ast.AsyncFunctionDef, method: str) -> ast.Call | None:
    for decorator in function.decorator_list:
        if not isinstance(decorator, ast.Call):
            continue
        target = decorator.func
        if isinstance(target, ast.Attribute) and target.attr == method:
            return decorator
        if isinstance(target, ast.Name) and target.id == method:
            return decorator
    return None


def module_functions(tree: ast.Module) -> Iterable[ast.FunctionDef | ast.AsyncFunctionDef]:
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            yield node


def nested_constant(node: ast.AST, key: str) -> Any:
    if isinstance(node, ast.Dict):
        for key_node, value_node in zip(node.keys, node.values, strict=True):
            if isinstance(key_node, ast.Constant) and key_node.value == key:
                if isinstance(value_node, ast.Constant):
                    return value_node.value
                value = nested_constant(value_node, key)
                if value is not None:
                    return value
        for value_node in node.values:
            value = nested_constant(value_node, key)
            if value is not None:
                return value
    return None


def tau_tool_name(class_node: ast.ClassDef, fallback: str) -> str:
    for item in class_node.body:
        if not isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)) or item.name != "get_info":
            continue
        for node in ast.walk(item):
            if isinstance(node, ast.Return) and node.value is not None:
                value = nested_constant(node.value, "name")
                if isinstance(value, str):
                    return value
    return fallback


def expression_rooted_in_alias(node: ast.AST, aliases: set[str]) -> bool:
    if isinstance(node, ast.Name):
        return node.id in aliases
    if isinstance(node, (ast.Attribute, ast.Subscript)):
        return expression_rooted_in_alias(node.value, aliases)
    return False


def data_aliases(function: ast.FunctionDef | ast.AsyncFunctionDef) -> set[str]:
    aliases = {"data"}
    changed = True
    while changed:
        changed = False
        for node in ast.walk(function):
            if not isinstance(node, (ast.Assign, ast.AnnAssign)):
                continue
            value = node.value
            targets = node.targets if isinstance(node, ast.Assign) else [node.target]
            if value is None or not expression_rooted_in_alias(value, aliases):
                continue
            for target in targets:
                if isinstance(target, ast.Name) and target.id not in aliases:
                    aliases.add(target.id)
                    changed = True
    return aliases


def tau_data_mutations(function: ast.FunctionDef | ast.AsyncFunctionDef) -> list[dict[str, Any]]:
    aliases = data_aliases(function)
    findings: list[dict[str, Any]] = []
    for node in ast.walk(function):
        targets: list[ast.AST] = []
        kind = None
        if isinstance(node, ast.Assign):
            targets = node.targets
            kind = "assignment"
        elif isinstance(node, ast.AnnAssign):
            targets = [node.target]
            kind = "assignment"
        elif isinstance(node, ast.AugAssign):
            targets = [node.target]
            kind = "augmented_assignment"
        elif isinstance(node, ast.Delete):
            targets = node.targets
            kind = "delete"
        if kind:
            for target in targets:
                if isinstance(target, (ast.Attribute, ast.Subscript)) and expression_rooted_in_alias(
                    target, aliases
                ):
                    findings.append({"line": node.lineno, "kind": kind})
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in CONTAINER_MUTATORS and expression_rooted_in_alias(
                node.func.value, aliases
            ):
                findings.append({"line": node.lineno, "kind": f"method:{node.func.attr}"})
    return sorted(findings, key=lambda item: (item["line"], item["kind"]))


def audit_tau(root: Path) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for path in sorted((root / "tau_bench" / "envs").glob("*/tools/*.py")):
        if path.name == "__init__.py":
            continue
        tree = parse_file(path)
        for class_node in (node for node in tree.body if isinstance(node, ast.ClassDef)):
            invoke = next(
                (
                    node
                    for node in class_node.body
                    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "invoke"
                ),
                None,
            )
            if invoke is None:
                continue
            name = tau_tool_name(class_node, path.stem)
            if not name.startswith(ACQUISITION_PREFIXES):
                continue
            items.append(
                {
                    "tool": name,
                    "file": str(path.relative_to(root)).replace("\\", "/"),
                    "state_write_flags": tau_data_mutations(invoke),
                }
            )
    return {
        "benchmark": "tau-bench",
        "revision": git_revision(root),
        "acquisition_tools": len(items),
        "flagged_tools": sum(bool(item["state_write_flags"]) for item in items),
        "items": items,
    }


def registered_tool(function: ast.FunctionDef | ast.AsyncFunctionDef) -> bool:
    return decorator_call(function, "register_as_tool") is not None


def context_mutations(function: ast.FunctionDef | ast.AsyncFunctionDef) -> list[dict[str, Any]]:
    findings = []
    for node in ast.walk(function):
        if isinstance(node, ast.Call) and call_name(node) in CONTEXT_MUTATORS:
            findings.append({"line": node.lineno, "kind": f"call:{call_name(node)}"})
    return sorted(findings, key=lambda item: (item["line"], item["kind"]))


def audit_toolsandbox(root: Path) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for path in sorted((root / "tool_sandbox" / "tools").glob("*.py")):
        tree = parse_file(path)
        for function in module_functions(tree):
            if not registered_tool(function) or not function.name.startswith(ACQUISITION_PREFIXES):
                continue
            items.append(
                {
                    "tool": function.name,
                    "file": str(path.relative_to(root)).replace("\\", "/"),
                    "state_write_flags": context_mutations(function),
                }
            )
    return {
        "benchmark": "ToolSandbox",
        "revision": git_revision(root),
        "acquisition_tools": len(items),
        "flagged_tools": sum(bool(item["state_write_flags"]) for item in items),
        "items": items,
    }


def appworld_get_decorator(function: ast.FunctionDef | ast.AsyncFunctionDef) -> ast.Call | None:
    for decorator in function.decorator_list:
        if not isinstance(decorator, ast.Call):
            continue
        target = decorator.func
        if (
            isinstance(target, ast.Attribute)
            and target.attr == "get"
            and isinstance(target.value, ast.Name)
            and target.value.id == "app"
        ):
            return decorator
    return None


def conservative_write_flags(function: ast.FunctionDef | ast.AsyncFunctionDef) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    for node in ast.walk(function):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            method = node.func.attr
            if method in PERSISTENCE_METHODS:
                findings.append({"line": node.lineno, "kind": f"call:{method}"})
        if isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Attribute):
                    findings.append({"line": node.lineno, "kind": "attribute_assignment"})
        elif isinstance(node, ast.AugAssign) and isinstance(node.target, ast.Attribute):
            findings.append({"line": node.lineno, "kind": "attribute_augmented_assignment"})
    return sorted(findings, key=lambda item: (item["line"], item["kind"]))


def audit_appworld(root: Path, wheel: Path) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for path in sorted((root / "apps").glob("*/apis.py")):
        tree = parse_file(path)
        for function in module_functions(tree):
            decorator = appworld_get_decorator(function)
            if decorator is None:
                continue
            route = None
            if decorator.args and isinstance(decorator.args[0], ast.Constant):
                route = decorator.args[0].value
            items.append(
                {
                    "tool": function.name,
                    "route": route,
                    "file": str(path.relative_to(root)).replace("\\", "/"),
                    "state_write_flags": conservative_write_flags(function),
                }
            )
    return {
        "benchmark": "AppWorld",
        "source_artifact": str(wheel),
        "source_sha256": sha256(wheel),
        "get_tools": len(items),
        "flagged_tools": sum(bool(item["state_write_flags"]) for item in items),
        "items": items,
    }


def salesforce_write_flags(function: ast.FunctionDef | ast.AsyncFunctionDef) -> list[dict[str, Any]]:
    findings: list[dict[str, Any]] = []
    write_names = {"create", "update", "upsert", "delete", "insert", "merge", "undelete"}
    for node in ast.walk(function):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in write_names:
                findings.append({"line": node.lineno, "kind": f"call:{node.func.attr}"})
    return sorted(findings, key=lambda item: (item["line"], item["kind"]))


def audit_crmarena(root: Path) -> dict[str, Any]:
    path = root / "crm_sandbox" / "env" / "functions.py"
    tree = parse_file(path)
    items = []
    for function in module_functions(tree):
        if function.name.startswith("_"):
            continue
        items.append(
            {
                "tool": function.name,
                "file": str(path.relative_to(root)).replace("\\", "/"),
                "state_write_flags": salesforce_write_flags(function),
            }
        )
    return {
        "benchmark": "CRMArena",
        "revision": git_revision(root),
        "public_functions": len(items),
        "flagged_functions": sum(bool(item["state_write_flags"]) for item in items),
        "items": items,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tau-root", type=Path, required=True)
    parser.add_argument("--toolsandbox-root", type=Path, required=True)
    parser.add_argument("--appworld-root", type=Path, required=True)
    parser.add_argument("--appworld-wheel", type=Path, required=True)
    parser.add_argument("--crmarena-root", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = {
        "scope": (
            "Conservative source audit of nominal acquisition actions. Flags are candidates for manual "
            "inspection, not proof of an externally consequential state mutation."
        ),
        "benchmarks": [
            audit_tau(args.tau_root.resolve()),
            audit_toolsandbox(args.toolsandbox_root.resolve()),
            audit_appworld(args.appworld_root.resolve(), args.appworld_wheel.resolve()),
            audit_crmarena(args.crmarena_root.resolve()),
        ],
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")


if __name__ == "__main__":
    main()
