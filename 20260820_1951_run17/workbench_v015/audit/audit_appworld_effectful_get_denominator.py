from __future__ import annotations

import argparse
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlsplit


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def sha256_values(values: set[str]) -> str:
    payload = "\n".join(sorted(values)).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def route_pattern(app: str, route: str) -> re.Pattern[str]:
    parts = re.split(r"(\{[^{}]+\})", f"/{app}{route}")
    expression = "".join(
        r"[^/]+" if part.startswith("{") else re.escape(part) for part in parts
    )
    return re.compile(rf"^{expression}/?$")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--acquisition-audit", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    acquisition = json.loads(
        args.acquisition_audit.read_text(encoding="utf-8")
    )
    appworld = next(
        row for row in acquisition["benchmarks"] if row["benchmark"] == "AppWorld"
    )

    endpoints: list[dict[str, Any]] = []
    for item in appworld["items"]:
        if not item["state_write_flags"]:
            continue
        app = Path(item["file"]).parts[1]
        label = f"{app}.{item['tool']}"
        endpoints.append(
            {
                "label": label,
                "app": app,
                "tool": item["tool"],
                "route": item["route"],
                "pattern": route_pattern(app, item["route"]),
                "state_write_flags": item["state_write_flags"],
            }
        )

    split_files = sorted((args.data_root / "datasets").glob("*.txt"))
    endpoint_calls: Counter[str] = Counter()
    endpoint_tasks: dict[str, set[str]] = defaultdict(set)
    endpoint_split_calls: dict[str, Counter[str]] = defaultdict(Counter)
    endpoint_split_tasks: dict[str, dict[str, set[str]]] = defaultdict(
        lambda: defaultdict(set)
    )
    split_task_counts: Counter[str] = Counter()
    split_available_api_call_tasks: dict[str, set[str]] = defaultdict(set)
    split_any_flagged_tasks: dict[str, set[str]] = defaultdict(set)
    split_all_get_calls: Counter[str] = Counter()
    split_all_calls: Counter[str] = Counter()
    missing_api_call_files: list[str] = []
    invalid_api_call_files: list[dict[str, str]] = []

    for split_file in split_files:
        split = split_file.stem
        task_ids = [
            line.strip()
            for line in split_file.read_text(encoding="utf-8").splitlines()
            if line.strip()
        ]
        split_task_counts[split] = len(task_ids)
        for task_id in task_ids:
            api_calls_path = (
                args.data_root
                / "tasks"
                / task_id
                / "ground_truth"
                / "api_calls.json"
            )
            if not api_calls_path.is_file():
                missing_api_call_files.append(f"{split}:{task_id}")
                continue
            try:
                calls = json.loads(api_calls_path.read_text(encoding="utf-8"))
            except (OSError, UnicodeError, json.JSONDecodeError) as exc:
                invalid_api_call_files.append(
                    {"task_ref": f"{split}:{task_id}", "error": str(exc)}
                )
                continue
            split_available_api_call_tasks[split].add(task_id)

            for call in calls:
                split_all_calls[split] += 1
                if str(call.get("method", "")).lower() != "get":
                    continue
                split_all_get_calls[split] += 1
                path = urlsplit(str(call.get("url", ""))).path
                for endpoint in endpoints:
                    if not endpoint["pattern"].fullmatch(path):
                        continue
                    label = endpoint["label"]
                    endpoint_calls[label] += 1
                    endpoint_tasks[label].add(task_id)
                    endpoint_split_calls[label][split] += 1
                    endpoint_split_tasks[label][split].add(task_id)
                    split_any_flagged_tasks[split].add(task_id)
                    break

    endpoint_results = []
    for endpoint in sorted(endpoints, key=lambda row: row["label"]):
        label = endpoint["label"]
        task_ids = endpoint_tasks[label]
        endpoint_results.append(
            {
                "label": label,
                "app": endpoint["app"],
                "tool": endpoint["tool"],
                "route": endpoint["route"],
                "state_write_flags": endpoint["state_write_flags"],
                "ground_truth_call_count": endpoint_calls[label],
                "ground_truth_task_count": len(task_ids),
                "ground_truth_task_set_sha256": sha256_values(task_ids),
                "by_split": {
                    split: {
                        "call_count": endpoint_split_calls[label][split],
                        "task_count": len(endpoint_split_tasks[label][split]),
                    }
                    for split in sorted(split_task_counts)
                },
            }
        )

    total_tasks = sum(split_task_counts.values())
    available_tasks = set().union(*split_available_api_call_tasks.values())
    tasks_with_any = set().union(*split_any_flagged_tasks.values())
    result = {
        "schema_version": 1,
        "scope": (
            "Frozen AppWorld ground-truth API-call traces for locally downloaded tasks. "
            "Counts establish a natural task denominator only; they do not measure model-agent "
            "behavior, evaluator sensitivity, or leaderboard impact."
        ),
        "inputs": {
            "data_version": (args.data_root / "version.txt")
            .read_text(encoding="utf-8")
            .strip(),
            "acquisition_audit_sha256": sha256_file(args.acquisition_audit),
            "split_file_sha256": {
                split_file.name: sha256_file(split_file) for split_file in split_files
            },
        },
        "dataset": {
            "task_count": total_tasks,
            "task_count_by_split": dict(sorted(split_task_counts.items())),
            "ground_truth_api_call_task_count": len(available_tasks),
            "ground_truth_api_call_coverage_fraction": (
                len(available_tasks) / total_tasks if total_tasks else None
            ),
            "ground_truth_call_count": sum(split_all_calls.values()),
            "ground_truth_get_call_count": sum(split_all_get_calls.values()),
            "tasks_with_any_flagged_get": len(tasks_with_any),
            "tasks_with_any_flagged_get_fraction_among_available": (
                len(tasks_with_any) / len(available_tasks)
                if available_tasks
                else None
            ),
            "tasks_with_any_flagged_get_lower_bound_fraction_over_all_listed": (
                len(tasks_with_any) / total_tasks if total_tasks else None
            ),
            "by_split": {
                split: {
                    "task_count": split_task_counts[split],
                    "ground_truth_api_call_task_count": len(
                        split_available_api_call_tasks[split]
                    ),
                    "ground_truth_call_count": split_all_calls[split],
                    "ground_truth_get_call_count": split_all_get_calls[split],
                    "tasks_with_any_flagged_get": len(
                        split_any_flagged_tasks[split]
                    ),
                    "tasks_with_any_flagged_get_fraction_among_available": (
                        len(split_any_flagged_tasks[split])
                        / len(split_available_api_call_tasks[split])
                        if split_available_api_call_tasks[split]
                        else None
                    ),
                }
                for split in sorted(split_task_counts)
            },
        },
        "flagged_endpoint_count": len(endpoints),
        "endpoints": endpoint_results,
        "integrity": {
            "missing_api_call_file_count": len(missing_api_call_files),
            "missing_task_ref_set_sha256": sha256_values(
                set(missing_api_call_files)
            ),
            "invalid_api_call_file_count": len(invalid_api_call_files),
            "invalid_api_call_files": invalid_api_call_files,
        },
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )


if __name__ == "__main__":
    main()
