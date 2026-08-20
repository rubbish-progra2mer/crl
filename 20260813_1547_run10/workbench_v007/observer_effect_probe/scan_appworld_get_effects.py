from __future__ import annotations

import ast
import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent
APPWORLD_ROOT = ROOT.parents[1] / "external" / "appworld"
APPS_ROOT = APPWORLD_ROOT / "src" / "appworld" / "apps"
OUTPUT = ROOT / "static_get_effect_candidates.json"


def decorator_endpoint(node: ast.FunctionDef) -> tuple[str, str] | None:
    for decorator in node.decorator_list:
        if not isinstance(decorator, ast.Call):
            continue
        function = decorator.func
        if not (
            isinstance(function, ast.Attribute)
            and isinstance(function.value, ast.Name)
            and function.value.id == "app"
            and function.attr in {"get", "post", "put", "delete", "patch"}
        ):
            continue
        endpoint = "<dynamic>"
        if decorator.args and isinstance(decorator.args[0], ast.Constant):
            endpoint = str(decorator.args[0].value)
        return function.attr.upper(), endpoint
    return None


def mutation_signals(node: ast.FunctionDef) -> list[dict[str, Any]]:
    signals: list[dict[str, Any]] = []
    for child in ast.walk(node):
        if isinstance(child, ast.Call):
            name = None
            if isinstance(child.func, ast.Attribute):
                name = child.func.attr
            elif isinstance(child.func, ast.Name):
                name = child.func.id
            if name in {
                "save",
                "delete",
                "create",
                "update",
                "request_payment_card_debit",
                "create_file",
                "send_email",
            }:
                signals.append({"kind": "call", "name": name, "line": child.lineno})
        elif isinstance(child, (ast.Assign, ast.AnnAssign, ast.AugAssign)):
            targets: list[ast.expr] = []
            if isinstance(child, ast.Assign):
                targets = list(child.targets)
            else:
                targets = [child.target]
            for target in targets:
                if isinstance(target, (ast.Attribute, ast.Subscript)):
                    signals.append(
                        {
                            "kind": "assignment",
                            "target": ast.unparse(target),
                            "line": child.lineno,
                        }
                    )
    unique: list[dict[str, Any]] = []
    seen: set[tuple[tuple[str, Any], ...]] = set()
    for signal in signals:
        key = tuple(sorted(signal.items()))
        if key not in seen:
            seen.add(key)
            unique.append(signal)
    return sorted(unique, key=lambda item: (int(item["line"]), item["kind"]))


def description(node: ast.FunctionDef) -> str | None:
    doc = ast.get_docstring(node)
    if not doc:
        return None
    for line in doc.splitlines():
        stripped = line.strip()
        if stripped.startswith("description:"):
            return stripped.removeprefix("description:").strip()
    return None


def main() -> None:
    records: list[dict[str, Any]] = []
    for path in sorted(APPS_ROOT.glob("*/apis.py")):
        source = path.read_text(encoding="utf-8")
        tree = ast.parse(source, filename=str(path))
        for node in tree.body:
            if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                continue
            endpoint = decorator_endpoint(node)
            if endpoint is None or endpoint[0] != "GET":
                continue
            signals = mutation_signals(node)
            if not signals:
                continue
            records.append(
                {
                    "app": path.parent.name,
                    "function": node.name,
                    "endpoint": endpoint[1],
                    "description": description(node),
                    "line_start": node.lineno,
                    "line_end": node.end_lineno,
                    "mutation_signals": signals,
                }
            )
    output = {
        "artifact_class": "scratch_static_probe",
        "scope": "AppWorld GET endpoints whose Python bodies contain persistent-mutation signals",
        "appworld_root": str(APPWORLD_ROOT),
        "candidate_count": len(records),
        "candidates": records,
        "limitations": (
            "Static syntax only: create/save can initialize default state without user-visible harm, "
            "and mutation through helper calls can be missed. Dynamic isolated state diffs are required."
        ),
    }
    OUTPUT.write_text(json.dumps(output, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
