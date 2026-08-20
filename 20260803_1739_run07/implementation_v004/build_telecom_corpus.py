"""Build a frozen telecom corpus with labels from official tau2 end states."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

from loguru import logger

logger.remove()

from tau2.domains.telecom.environment import get_environment, get_tasks


def digest(value: Any) -> str:
    data = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(data.encode("utf-8")).hexdigest()


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def action_dict(action: Any) -> dict[str, Any]:
    return {
        "name": action.name,
        "arguments": copy.deepcopy(action.arguments),
        "requestor": action.requestor,
    }


def initialize(environment: Any, task: Any) -> None:
    initial = task.initial_state
    environment.set_state(
        initialization_data=None if initial is None else initial.initialization_data,
        initialization_actions=None if initial is None else initial.initialization_actions,
        message_history=[] if initial is None or initial.message_history is None else list(initial.message_history),
    )


def flatten(value: Any, prefix: str = "") -> dict[str, Any]:
    if isinstance(value, dict):
        result: dict[str, Any] = {}
        for key in sorted(value):
            path = f"{prefix}.{key}" if prefix else str(key)
            result.update(flatten(value[key], path))
        return result
    if isinstance(value, list):
        result = {}
        for index, item in enumerate(value):
            result.update(flatten(item, f"{prefix}[{index}]"))
        if not value:
            result[prefix] = []
        return result
    return {prefix: value}


def complete_state(environment: Any) -> dict[str, Any]:
    agent = {} if environment.tools is None or environment.tools.db is None else environment.tools.db.model_dump(mode="json")
    user = {} if environment.user_tools is None or environment.user_tools.db is None else environment.user_tools.db.model_dump(mode="json")
    return {"agent": agent, "user": user}


def state_delta(before: dict[str, Any], after: dict[str, Any]) -> dict[str, Any]:
    left = flatten(before)
    right = flatten(after)
    missing = "<MISSING>"
    paths = sorted(path for path in set(left) | set(right) if left.get(path, missing) != right.get(path, missing))
    values = [(path, right.get(path, missing)) for path in paths]
    return {
        "state_delta_count": len(paths),
        "state_delta_paths": paths,
        "state_delta_digest": digest(values),
    }


def execute(task: Any, actions: list[dict[str, Any]]) -> dict[str, Any]:
    environment = get_environment()
    initialize(environment, task)
    before = complete_state(environment)
    errors: list[str] = []
    for action in actions:
        try:
            environment.make_tool_call(
                tool_name=action["name"],
                requestor=action["requestor"],
                **action["arguments"],
            )
        except Exception as error:
            errors.append(type(error).__name__)
            break
    after = complete_state(environment)
    delta = state_delta(before, after)
    agent_hash = environment.get_db_hash()
    user_hash = environment.get_user_db_hash()
    writes = [action for action in actions if action["mutates_state"]]
    reads = [action for action in actions if not action["mutates_state"]]
    return {
        "agent_db_hash": agent_hash,
        "user_db_hash": user_hash,
        "errors": errors,
        "features": {
            "write_count": len(writes),
            "write_names": [action["name"] for action in writes],
            "write_arguments_digest": digest([(action["name"], action["arguments"]) for action in writes]),
            "all_call_count": len(actions),
            "all_call_names": [action["name"] for action in actions],
            "read_count": len(reads),
            **delta,
            "final_state_pair_digest": digest([agent_hash, user_hash]),
            "tool_error_count": len(errors),
        },
    }


def perturb(value: Any, *, alternate: bool = False) -> Any:
    offset = 17 if alternate else 1
    if isinstance(value, bool):
        return not value
    if isinstance(value, int):
        return value + offset
    if isinstance(value, float):
        return value + float(offset)
    if isinstance(value, str):
        return ("heldout__" if alternate else "") + value + ("" if alternate else "__perturbed")
    if isinstance(value, list):
        return [*value, "heldout"] if alternate else (value[:-1] if value else ["perturbed"])
    if isinstance(value, dict) and value:
        result = copy.deepcopy(value)
        key = sorted(result)[-1 if alternate else 0]
        result[key] = perturb(result[key], alternate=alternate)
        return result
    return "heldout" if alternate else "perturbed"


def variants(actions: list[dict[str, Any]]) -> list[tuple[str, str, list[dict[str, Any]]]]:
    reads = [action for action in actions if not action["mutates_state"]]
    writes = [action for action in actions if action["mutates_state"]]
    result: list[tuple[str, str, list[dict[str, Any]]]] = [
        ("reference", "train_correct", actions),
        ("strip_reads", "train_correct", writes),
        ("duplicate_reads", "heldout_correct", [item for action in actions for item in ([action, copy.deepcopy(action)] if not action["mutates_state"] else [action])]),
        ("reads_first", "heldout_correct", reads + writes),
        ("writes_first", "heldout_correct", writes + reads),
    ]
    if not writes:
        return result
    first = next(index for index, action in enumerate(actions) if action["mutates_state"])
    last = max(index for index, action in enumerate(actions) if action["mutates_state"])
    result.extend(
        [
            ("drop_first_write", "train_harmful", actions[:first] + actions[first + 1 :]),
            ("drop_last_write", "heldout_harmful", actions[:last] + actions[last + 1 :]),
            ("duplicate_first_write", "heldout_harmful", actions[: first + 1] + [copy.deepcopy(actions[first])] + actions[first + 1 :]),
            ("reverse_writes", "heldout_harmful", list(reversed(writes)) + reads),
        ]
    )
    arguments = actions[first]["arguments"]
    if arguments:
        training = copy.deepcopy(actions)
        train_key = sorted(training[first]["arguments"])[0]
        training[first]["arguments"][train_key] = perturb(training[first]["arguments"][train_key])
        result.append(("perturb_first_write", "train_harmful", training))
        heldout = copy.deepcopy(actions)
        heldout_key = sorted(heldout[first]["arguments"])[-1]
        heldout[first]["arguments"][heldout_key] = perturb(heldout[first]["arguments"][heldout_key], alternate=True)
        result.append(("perturb_first_write_heldout", "heldout_harmful", heldout))
    return result


def build(max_tasks: int) -> list[dict[str, Any]]:
    tasks = get_tasks("base")[:max_tasks]
    records: list[dict[str, Any]] = []
    classifier = get_environment()
    for task in tasks:
        if task.evaluation_criteria is None:
            continue
        raw_actions = [action_dict(action) for action in (task.evaluation_criteria.actions or [])]
        for action in raw_actions:
            action["mutates_state"] = classifier._is_mutating_tool(action["name"])
        if not any(action["mutates_state"] for action in raw_actions):
            continue
        reference = execute(task, raw_actions)
        gold = (reference["agent_db_hash"], reference["user_db_hash"])
        seen: set[str] = set()
        built_variants: list[dict[str, Any]] = []
        for name, role, variant_actions in variants(raw_actions):
            action_signature = digest(variant_actions)
            if action_signature in seen:
                continue
            seen.add(action_signature)
            execution = execute(task, variant_actions)
            correct = (execution["agent_db_hash"], execution["user_db_hash"]) == gold
            built_variants.append(
                {
                    "name": name,
                    "role": role,
                    "official_db_correct": correct,
                    "features": execution["features"],
                    "errors": execution["errors"],
                }
            )
        records.append(
            {
                "domain": "telecom",
                "task_id": task.id,
                "reward_basis": [item.value for item in task.evaluation_criteria.reward_basis],
                "reference_action_count": len(raw_actions),
                "reference_write_count": sum(action["mutates_state"] for action in raw_actions),
                "variants": built_variants,
            }
        )
    return records


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tau2-root", type=Path, required=True)
    parser.add_argument("--source-input-root", type=Path)
    parser.add_argument("--source-commit")
    parser.add_argument("--max-tasks", type=int, default=1000)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    commit = args.source_commit or subprocess.check_output(
        ["git", "-C", str(args.tau2_root), "rev-parse", "HEAD"], text=True
    ).strip()
    source_root = args.source_input_root or args.tau2_root
    inputs = [
        source_root / "docs" / "evaluation.md",
        source_root / "data" / "tau2" / "domains" / "telecom" / "tasks.json",
        source_root / "data" / "tau2" / "domains" / "telecom" / "db.toml",
        source_root / "data" / "tau2" / "domains" / "telecom" / "user_db.toml",
    ]
    records = build(args.max_tasks)
    counts: dict[str, int] = {}
    for task in records:
        for variant in task["variants"]:
            key = f"{variant['role']}::{variant['official_db_correct']}"
            counts[key] = counts.get(key, 0) + 1
    payload = {
        "schema_version": 4,
        "source": "official tau2-bench v1.0.1 telecom base tasks",
        "source_commit": commit,
        "source_files": {str(path.relative_to(source_root)).replace("\\", "/"): file_digest(path) for path in inputs},
        "label_rule": "agent and user DB hashes equal the official reference-action end state",
        "compiler_independence": "This builder does not import the v004 evaluator or choose its mandatory anchor.",
        "counts": counts,
        "tasks": records,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"source_commit": commit, "tasks": len(records), "counts": counts}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
