from __future__ import annotations

import importlib.util
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any


HERE = Path(__file__).resolve().parent
REPO = HERE / "agent-diff-lite"
ENGINE_PATH = (
    REPO
    / "backend"
    / "src"
    / "platform"
    / "evaluationEngine"
    / "assertion.py"
)
SUITES = {
    "box": REPO / "backend" / "seeds" / "testsuites" / "box_bench.json",
    "calendar": REPO
    / "backend"
    / "seeds"
    / "testsuites"
    / "calendar_bench.json",
    "linear": REPO / "backend" / "seeds" / "testsuites" / "linear_bench.json",
    "slack": REPO / "backend" / "seeds" / "testsuites" / "slack_bench_v2.json",
}
SCHEMAS = {
    service: REPO
    / "backend"
    / "src"
    / "services"
    / service
    / "database"
    / "schema.py"
    for service in SUITES
}


def load_assertion_engine() -> type:
    spec = importlib.util.spec_from_file_location("agent_diff_assertion", ENGINE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {ENGINE_PATH}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.AssertionEngine


def table_names(path: Path) -> set[str]:
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r'__tablename__\s*=\s*["\']([^"\']+)["\']', text))


def empty_diff() -> dict[str, list[dict[str, Any]]]:
    return {"inserts": [], "updates": [], "deletes": []}


def main() -> None:
    engine_cls = load_assertion_engine()
    service_tables = {name: table_names(path) for name, path in SCHEMAS.items()}

    total_tasks = 0
    total_assertions = 0
    invariant_unasserted_entity = 0
    tasks_with_real_unasserted_entity = 0
    single_assertion_tasks = 0
    same_entity_invariant_on_empty = 0
    by_service: dict[str, dict[str, Any]] = {}
    assertion_kinds: Counter[str] = Counter()

    for service, suite_path in SUITES.items():
        suite = json.loads(suite_path.read_text(encoding="utf-8"))
        service_task_count = 0
        service_assertion_count = 0
        service_invariant_count = 0
        tables = service_tables[service]

        for task in suite["tests"]:
            assertions = task["assertions"]
            spec = {
                "version": "0.1",
                "assertions": assertions,
                "ignore_fields": suite.get("ignore_fields", {}),
            }
            engine = engine_cls(spec)
            asserted_entities = {a["entity"] for a in assertions}
            unasserted_entities = sorted(tables - asserted_entities)

            total_tasks += 1
            service_task_count += 1
            total_assertions += len(assertions)
            service_assertion_count += len(assertions)
            assertion_kinds.update(a["diff_type"] for a in assertions)

            if unasserted_entities:
                tasks_with_real_unasserted_entity += 1
                baseline = empty_diff()
                mutated = empty_diff()
                mutated["inserts"].append(
                    {
                        "__table__": unasserted_entities[0],
                        "id": "crl-unrequested-change",
                    }
                )
                before = engine.evaluate(baseline)
                after = engine.evaluate(mutated)
                if before == after:
                    invariant_unasserted_entity += 1
                    service_invariant_count += 1

            if len(assertions) == 1:
                single_assertion_tasks += 1
                entity = assertions[0]["entity"]
                baseline = empty_diff()
                mutated = empty_diff()
                mutated["inserts"].append(
                    {"__table__": entity, "id": "crl-nonmatching-extra-row"}
                )
                if engine.evaluate(baseline) == engine.evaluate(mutated):
                    same_entity_invariant_on_empty += 1

        by_service[service] = {
            "tasks": service_task_count,
            "assertions": service_assertion_count,
            "schema_tables": len(tables),
            "tasks_invariant_to_real_unasserted_entity_insert": service_invariant_count,
        }

    box_suite = json.loads(SUITES["box"].read_text(encoding="utf-8"))
    box_test_1 = next(test for test in box_suite["tests"] if test["id"] == "test_1")
    witness_spec = {
        "version": "0.1",
        "assertions": box_test_1["assertions"],
        "ignore_fields": box_suite.get("ignore_fields", {}),
    }
    witness_engine = engine_cls(witness_spec)
    requested = {
        "__table__": "box_folders",
        "id": "requested-folder",
        "name": "Admin User",
        "parent_id": "0",
    }
    unrequested_same_entity = {
        "__table__": "box_folders",
        "id": "unrequested-folder",
        "name": "Unrequested Extra Folder",
        "parent_id": "0",
    }
    unrequested_other_entity = {
        "__table__": "box_comments",
        "id": "unrequested-comment",
        "message": "unrequested side effect",
    }
    requested_only = {
        "inserts": [requested],
        "updates": [],
        "deletes": [],
    }
    with_unrequested_changes = {
        "inserts": [requested, unrequested_same_entity, unrequested_other_entity],
        "updates": [],
        "deletes": [],
    }
    witness_before = witness_engine.evaluate(requested_only)
    witness_after = witness_engine.evaluate(with_unrequested_changes)

    result = {
        "repository_commit": "3bb9c40707df23d89e5dbc0e40c424ba38c69ff8",
        "suite_scope": "current repository four 65-task suites",
        "total_tasks": total_tasks,
        "total_assertions": total_assertions,
        "assertion_kinds": dict(sorted(assertion_kinds.items())),
        "tasks_with_real_unasserted_entity": tasks_with_real_unasserted_entity,
        "tasks_invariant_to_real_unasserted_entity_insert": invariant_unasserted_entity,
        "single_assertion_tasks": single_assertion_tasks,
        "single_assertion_tasks_invariant_to_minimal_same_entity_nonmatch_on_empty_diff": same_entity_invariant_on_empty,
        "by_service": by_service,
        "passing_witness": {
            "suite": "box_bench.json",
            "task_id": box_test_1["id"],
            "prompt": box_test_1["prompt"],
            "requested_only_result": witness_before,
            "with_two_unrequested_changes_result": witness_after,
            "verdict_unchanged": witness_before == witness_after,
            "both_pass": bool(witness_before["passed"] and witness_after["passed"]),
        },
        "interpretation_limit": (
            "The task-wide mutation check compares evaluator outputs on an empty base diff; "
            "it proves score invariance to a real but unasserted entity, not that the empty "
            "base itself is a successful trajectory. The Box witness separately proves a "
            "passing score remains passing after two unrequested changes."
        ),
    }
    output = HERE / "assertion_closure_audit.json"
    with output.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
