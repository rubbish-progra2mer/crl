"""Build an external trajectory corpus from the official tau2-bench tasks.

This program does not import the CRL candidate compiler or its mutation list.
It executes deterministic trajectory variants in the official airline and
retail environments and labels them only by the official end-state DB hash
semantics.  The resulting JSON is a frozen input for the candidate evaluation.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any, Callable

from loguru import logger

# Remove the default sink before importing tau2 modules.  Some of those
# modules emit diagnostic messages during import; the formal runner treats
# stdout/stderr as evidence, so keep the corpus builder's output deterministic.
logger.remove()

from tau2.domains.airline.environment import get_environment as get_airline_environment
from tau2.domains.airline.environment import get_tasks as get_airline_tasks
from tau2.domains.retail.environment import get_environment as get_retail_environment
from tau2.domains.retail.environment import get_tasks as get_retail_tasks


def _digest(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def _file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _action_dict(action: Any) -> dict[str, Any]:
    return {
        "name": action.name,
        "arguments": copy.deepcopy(action.arguments),
        "requestor": action.requestor,
    }


def _initialize(environment: Any, task: Any) -> None:
    initial = task.initial_state
    environment.set_state(
        initialization_data=None if initial is None else initial.initialization_data,
        initialization_actions=None if initial is None else initial.initialization_actions,
        message_history=[] if initial is None or initial.message_history is None else list(initial.message_history),
    )


def _flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key in sorted(value):
            path = f"{prefix}.{key}" if prefix else str(key)
            result.update(_flatten(value[key], path))
        return result
    if isinstance(value, list):
        result = {}
        for index, item in enumerate(value):
            path = f"{prefix}[{index}]"
            result.update(_flatten(item, path))
        if not value:
            result[prefix] = []
        return result
    return {prefix: value}


def _state(environment: Any) -> dict[str, Any]:
    if environment.tools is None or environment.tools.db is None:
        return {}
    return environment.tools.db.model_dump(mode="json")


def _change_summary(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    left = _flatten(before)
    right = _flatten(after)
    paths = sorted(
        path for path in set(left) | set(right) if left.get(path, "<MISSING>") != right.get(path, "<MISSING>")
    )
    values = [(path, right.get(path, "<MISSING>")) for path in paths]
    return {
        "changed_count": len(paths),
        "changed_paths": paths,
        "changed_top_keys": sorted({path.split(".", 1)[0].split("[", 1)[0] for path in paths}),
        "changed_values_digest": _digest(values),
    }


def _execute(
    constructor: Callable[..., Any], task: Any, actions: list[dict[str, Any]]
) -> dict[str, Any]:
    environment = constructor()
    _initialize(environment, task)
    before = _state(environment)
    errors: list[str] = []
    for action in actions:
        try:
            environment.make_tool_call(
                tool_name=action["name"],
                requestor=action["requestor"],
                **action["arguments"],
            )
        except Exception as error:  # External tools define their own error types.
            errors.append(type(error).__name__)
            break
    after = _state(environment)
    summary = _change_summary(before, after)
    write_actions = [action for action in actions if action["mutates_state"]]
    read_actions = [action for action in actions if not action["mutates_state"]]
    return {
        "agent_db_hash": environment.get_db_hash(),
        "user_db_hash": environment.get_user_db_hash(),
        "errors": errors,
        "features": {
            "write_count": len(write_actions),
            "write_names": [action["name"] for action in write_actions],
            "write_arguments_digest": _digest(
                [(action["name"], action["arguments"]) for action in write_actions]
            ),
            "all_call_count": len(actions),
            "all_call_names": [action["name"] for action in actions],
            "read_count": len(read_actions),
            "changed_count": summary["changed_count"],
            "changed_paths": summary["changed_paths"],
            "changed_values_digest": summary["changed_values_digest"],
            "final_db_hash": environment.get_db_hash(),
            "tool_error_count": len(errors),
        },
    }


def _perturb(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 1
    if isinstance(value, float):
        return value + 1.0
    if isinstance(value, str):
        return value + "__perturbed"
    if isinstance(value, list):
        return value[:-1] if value else ["perturbed"]
    if isinstance(value, dict) and value:
        result = copy.deepcopy(value)
        key = sorted(result)[0]
        result[key] = _perturb(result[key])
        return result
    return "perturbed"


def _perturb_alt(value: Any) -> Any:
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + 17
    if isinstance(value, float):
        return value + 17.0
    if isinstance(value, str):
        return "heldout__" + value
    if isinstance(value, list):
        return [*value, "heldout"]
    if isinstance(value, dict) and value:
        result = copy.deepcopy(value)
        key = sorted(result)[-1]
        result[key] = _perturb_alt(result[key])
        return result
    return "heldout"


def _variants(actions: list[dict[str, Any]]) -> list[tuple[str, str, list[dict[str, Any]]]]:
    reads = [action for action in actions if not action["mutates_state"]]
    writes = [action for action in actions if action["mutates_state"]]
    variants: list[tuple[str, str, list[dict[str, Any]]]] = [
        ("reference", "train_correct", actions),
        ("strip_reads", "train_correct", writes),
        ("duplicate_reads", "heldout_correct", [item for action in actions for item in ([action, copy.deepcopy(action)] if not action["mutates_state"] else [action])]),
        ("reads_first", "heldout_correct", reads + writes),
        ("writes_first", "heldout_correct", writes + reads),
    ]
    if writes:
        first_index = next(index for index, action in enumerate(actions) if action["mutates_state"])
        last_index = max(index for index, action in enumerate(actions) if action["mutates_state"])
        variants.extend(
            (
                ("drop_first_write", "train_harmful", actions[:first_index] + actions[first_index + 1 :]),
                ("drop_last_write", "heldout_harmful", actions[:last_index] + actions[last_index + 1 :]),
                ("duplicate_first_write", "heldout_harmful", actions[: first_index + 1] + [copy.deepcopy(actions[first_index])] + actions[first_index + 1 :]),
                ("reverse_writes", "heldout_harmful", list(reversed(writes)) + reads),
            )
        )
        perturbed = copy.deepcopy(actions)
        arguments = perturbed[first_index]["arguments"]
        if arguments:
            key = sorted(arguments)[0]
            arguments[key] = _perturb(arguments[key])
            variants.append(("perturb_first_write", "train_harmful", perturbed))
            heldout = copy.deepcopy(actions)
            heldout_arguments = heldout[first_index]["arguments"]
            heldout_key = sorted(heldout_arguments)[-1]
            heldout_arguments[heldout_key] = _perturb_alt(
                heldout_arguments[heldout_key]
            )
            variants.append(
                ("perturb_first_write_heldout", "heldout_harmful", heldout)
            )
    return variants


def build_domain(
    name: str,
    constructor: Callable[..., Any],
    task_loader: Callable[..., list[Any]],
    max_tasks: int,
) -> list[dict[str, Any]]:
    tasks = task_loader("base")[:max_tasks]
    records: list[dict[str, Any]] = []
    classification_environment = constructor()
    for task in tasks:
        if task.evaluation_criteria is None:
            continue
        raw_actions = [_action_dict(action) for action in (task.evaluation_criteria.actions or [])]
        for action in raw_actions:
            action["mutates_state"] = classification_environment._is_mutating_tool(action["name"])
        if not any(action["mutates_state"] for action in raw_actions):
            continue
        reference = _execute(constructor, task, raw_actions)
        gold = (reference["agent_db_hash"], reference["user_db_hash"])
        variants: list[dict[str, Any]] = []
        seen: set[str] = set()
        for variant_name, role, variant_actions in _variants(raw_actions):
            signature = _digest(variant_actions)
            if signature in seen:
                continue
            seen.add(signature)
            execution = _execute(constructor, task, variant_actions)
            is_correct = (
                execution["agent_db_hash"], execution["user_db_hash"]
            ) == gold
            variants.append(
                {
                    "name": variant_name,
                    "role": role,
                    "official_db_correct": is_correct,
                    "features": execution["features"],
                    "errors": execution["errors"],
                }
            )
        records.append(
            {
                "domain": name,
                "task_id": task.id,
                "reward_basis": [item.value for item in task.evaluation_criteria.reward_basis],
                "reference_action_count": len(raw_actions),
                "reference_write_count": sum(action["mutates_state"] for action in raw_actions),
                "variants": variants,
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tau2-root", type=Path, required=True)
    parser.add_argument("--max-tasks-per-domain", type=int, default=120)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    logger.remove()
    commit = subprocess.check_output(
        ["git", "-C", str(args.tau2_root), "rev-parse", "HEAD"], text=True
    ).strip()
    inputs = [
        args.tau2_root / "docs" / "evaluation.md",
        args.tau2_root / "data" / "tau2" / "domains" / "airline" / "tasks.json",
        args.tau2_root / "data" / "tau2" / "domains" / "airline" / "db.json",
        args.tau2_root / "data" / "tau2" / "domains" / "retail" / "tasks.json",
        args.tau2_root / "data" / "tau2" / "domains" / "retail" / "db.json",
    ]
    records = []
    records.extend(build_domain("airline", get_airline_environment, get_airline_tasks, args.max_tasks_per_domain))
    records.extend(build_domain("retail", get_retail_environment, get_retail_tasks, args.max_tasks_per_domain))
    counts: dict[str, int] = {}
    for record in records:
        for variant in record["variants"]:
            key = f"{variant['role']}::{variant['official_db_correct']}"
            counts[key] = counts.get(key, 0) + 1
    payload = {
        "schema_version": 1,
        "source": "official tau2-bench v1.0.1 task end-state semantics",
        "source_commit": commit,
        "source_files": {str(path.relative_to(args.tau2_root)).replace("\\", "/"): _file_digest(path) for path in inputs},
        "label_rule": "agent and user DB hashes equal the official reference-action end state",
        "compiler_independence": "This builder does not import the CRL candidate compiler or its mutation list.",
        "counts": counts,
        "tasks": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"source_commit": commit, "tasks": len(records), "counts": counts}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
