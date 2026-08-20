from __future__ import annotations

import argparse
import hashlib
import json
import platform
import re
import subprocess
import sys
from pathlib import Path
from typing import Any


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def task_digest(task_id: str) -> bytes:
    return hashlib.sha256(task_id.encode("utf-8")).digest()


def run_git(repo: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )
    return result.stdout.strip()


def write_sparse_patterns(repo: Path, patterns: list[str]) -> None:
    sparse_path = repo / ".git" / "info" / "sparse-checkout"
    sparse_path.parent.mkdir(parents=True, exist_ok=True)
    sparse_path.write_text(
        "\n".join(sorted(set(patterns))) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def initialize_repository(
    root: Path,
    repository_url: str,
    commit: str,
) -> Path:
    repo = root / "repository"
    repo.mkdir(parents=True, exist_ok=False)
    run_git(repo, "init")
    run_git(repo, "config", "core.longpaths", "true")
    run_git(repo, "remote", "add", "origin", repository_url)
    run_git(
        repo,
        "fetch",
        "--depth=1",
        "--filter=blob:none",
        "origin",
        commit,
    )
    fetched = run_git(repo, "rev-parse", "FETCH_HEAD")
    if fetched != commit:
        raise ValueError(f"Fetched commit {fetched} does not match {commit}")
    run_git(repo, "sparse-checkout", "init", "--no-cone")
    return repo


def checkout_task_metadata(
    repo: Path,
    commit: str,
    task_ids: list[str],
) -> None:
    patterns = [f"/tasks/{task_id}/*/task.json" for task_id in task_ids]
    write_sparse_patterns(repo, patterns)
    run_git(repo, "checkout", "--detach", "--force", commit)


def metadata_trajectory_paths(
    repo: Path,
    task_ids: list[str],
    positive_classification: str,
) -> tuple[list[dict[str, Any]], list[str]]:
    metadata: list[dict[str, Any]] = []
    paths: list[str] = []
    for task_id in task_ids:
        task_files = sorted((repo / "tasks" / task_id).glob("*/task.json"))
        if not task_files:
            raise FileNotFoundError(f"No task metadata for {task_id}")
        for task_file in task_files:
            record = json.loads(task_file.read_text(encoding="utf-8"))
            model = str(record["model"])
            if task_file.parent.name != model:
                raise ValueError(f"Model directory mismatch in {task_file}")
            relative_task = task_file.relative_to(repo).as_posix()
            paths.append(f"/{relative_task}")
            baselines = [
                item
                for item in record["baselines"]
                if float(item["reward"]) == 1.0
            ]
            positives = [
                item
                for item in record["trajectories"]
                if item["classification"] == positive_classification
                and float(item["reward"]) == 1.0
            ]
            for item in baselines:
                label = str(item["label"])
                paths.append(
                    f"/tasks/{task_id}/{model}/baseline_trajectories/"
                    f"{label}/trial/agent/trajectory.json"
                )
            for item in positives:
                label = str(item["trajectory_label"])
                paths.append(
                    f"/tasks/{task_id}/{model}/stripped_trajectories/"
                    f"{label}/trial/agent/trajectory.json"
                )
            metadata.append(
                {
                    "path": relative_task,
                    "record": record,
                    "baselines": baselines,
                    "positives": positives,
                }
            )
    return metadata, paths


def checkout_trajectories(repo: Path, patterns: list[str]) -> None:
    write_sparse_patterns(repo, patterns)
    run_git(repo, "read-tree", "-mu", "HEAD")


_KEYSTROKES = re.compile(
    r"keystrokes=(.*?)(?:\r?\n?;\s*duration=|\}\s*$)",
    flags=re.DOTALL,
)


def command_from_arguments(arguments: Any) -> str:
    if isinstance(arguments, dict):
        value = arguments.get("keystrokes", "")
        return str(value)
    text = str(arguments)
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        parsed = None
    if isinstance(parsed, dict) and "keystrokes" in parsed:
        return str(parsed["keystrokes"])
    match = _KEYSTROKES.search(text)
    return match.group(1) if match else text


def terminal_text(result: Any) -> str:
    if isinstance(result, dict):
        return str(result.get("content", ""))
    text = str(result)
    match = re.match(r"^@\{content=(.*)\}$", text, flags=re.DOTALL)
    return match.group(1) if match else text


def action_surface(path: Path) -> dict[str, Any]:
    trajectory = json.loads(path.read_text(encoding="utf-8"))
    commands: list[str] = []
    outputs: list[str] = []
    task_prompt = ""
    for step in trajectory["steps"]:
        source = str(step["source"])
        if source == "user" and not task_prompt:
            task_prompt = str(step.get("message", ""))
        if source != "agent":
            continue
        for call in step.get("tool_calls", []):
            commands.append(command_from_arguments(call.get("arguments", "")))
        observation = step.get("observation") or {}
        for result in observation.get("results", []):
            outputs.append(terminal_text(result))
    if not commands:
        raise ValueError(f"No commands extracted from {path}")
    return {
        "schema_version": trajectory["schema_version"],
        "task_prompt": task_prompt,
        "commands": commands,
        "terminal_outputs": outputs,
    }


def make_row(
    repo: Path,
    task: dict[str, Any],
    item: dict[str, Any],
    *,
    kind: str,
    label: str,
) -> tuple[dict[str, Any], dict[str, Any]]:
    record = task["record"]
    task_id = str(record["task_id"])
    model = str(record["model"])
    tree = "baseline_trajectories" if kind == "baseline" else "stripped_trajectories"
    relative = (
        Path("tasks")
        / task_id
        / model
        / tree
        / label
        / "trial"
        / "agent"
        / "trajectory.json"
    )
    source_path = repo / relative
    surface = action_surface(source_path)
    source_hash = sha256_file(source_path)
    classification = (
        "baseline" if kind == "baseline" else str(item["classification"])
    )
    row_id = hashlib.sha256(
        f"{task_id}\0{model}\0{kind}\0{label}".encode("utf-8")
    ).hexdigest()
    row = {
        "row_id": row_id,
        "task_id": task_id,
        "model": model,
        "kind": kind,
        "label": label,
        "target": 0 if kind == "baseline" else 1,
        "classification": classification,
        "source_dataset": record["source_dataset"],
        "source_datasets": record["source_datasets"],
        "observed_categories": (
            [] if kind == "baseline" else item.get("observed_categories", [])
        ),
        "task_prompt": surface["task_prompt"],
        "commands": surface["commands"],
        "terminal_outputs": surface["terminal_outputs"],
        "source_relative_path": relative.as_posix(),
        "source_sha256": source_hash,
        "trajectory_schema_version": surface["schema_version"],
    }
    source = {
        "relative_path": relative.as_posix(),
        "sha256": source_hash,
        "bytes": source_path.stat().st_size,
    }
    return row, source


def build_dataset(
    repo: Path,
    metadata: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    sources: list[dict[str, Any]] = []
    for task in metadata:
        for item in task["baselines"]:
            row, source = make_row(
                repo,
                task,
                item,
                kind="baseline",
                label=str(item["label"]),
            )
            rows.append(row)
            sources.append(source)
        for item in task["positives"]:
            row, source = make_row(
                repo,
                task,
                item,
                kind="hack",
                label=str(item["trajectory_label"]),
            )
            rows.append(row)
            sources.append(source)
    rows.sort(key=lambda row: (row["task_id"], row["model"], row["kind"], row["label"]))
    sources.sort(key=lambda item: item["relative_path"])
    return rows, sources


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("development", "confirmation"), required=True)
    parser.add_argument("--config", required=True)
    parser.add_argument("--output-dir", required=True)
    parser.add_argument("--work-root", required=True)
    args = parser.parse_args()

    config_path = Path(args.config).resolve()
    config = json.loads(config_path.read_text(encoding="utf-8"))
    output = Path(args.output_dir).resolve()
    work_root = Path(args.work_root).resolve()
    output.mkdir(parents=True, exist_ok=False)
    work_root.mkdir(parents=True, exist_ok=False)

    repo = initialize_repository(
        work_root,
        str(config["repository_url"]),
        str(config["repository_commit"]),
    )
    all_task_ids = run_git(
        repo,
        "ls-tree",
        "-d",
        "--name-only",
        f"{config['repository_commit']}:tasks",
    ).splitlines()
    bucket = int(
        config[
            "development_bucket"
            if args.phase == "development"
            else "confirmation_bucket"
        ]
    )
    task_ids = sorted(
        task_id
        for task_id in all_task_ids
        if task_digest(task_id)[0] % int(config["bucket_modulus"]) == bucket
    )
    checkout_task_metadata(repo, str(config["repository_commit"]), task_ids)
    metadata, patterns = metadata_trajectory_paths(
        repo,
        task_ids,
        str(config["positive_classification"]),
    )
    checkout_trajectories(repo, patterns)
    rows, sources = build_dataset(repo, metadata)
    metadata_sources = [
        {
            "relative_path": str(task["path"]),
            "sha256": sha256_file(repo / str(task["path"])),
            "bytes": (repo / str(task["path"])).stat().st_size,
        }
        for task in metadata
    ]
    sources = sorted(
        metadata_sources + sources,
        key=lambda item: item["relative_path"],
    )

    dataset_path = output / "dataset.jsonl"
    with dataset_path.open("w", encoding="utf-8", newline="\n") as stream:
        for row in rows:
            stream.write(
                json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n"
            )
    counts = {
        "tasks_selected": len(task_ids),
        "task_model_records": len(metadata),
        "rows": len(rows),
        "baselines": sum(row["target"] == 0 for row in rows),
        "serious_exploits": sum(row["target"] == 1 for row in rows),
    }
    manifest = {
        "phase": args.phase,
        "repository_url": config["repository_url"],
        "repository_commit": config["repository_commit"],
        "checked_out_commit": run_git(repo, "rev-parse", "HEAD"),
        "git_version": subprocess.run(
            ["git", "--version"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
        ).stdout.strip(),
        "python_executable": sys.executable,
        "python": platform.python_version(),
        "bucket": bucket,
        "bucket_modulus": config["bucket_modulus"],
        "task_ids": task_ids,
        "selection_exposed_task_ids": config["selection_exposed_task_ids"],
        "counts": counts,
        "dataset_sha256": sha256_file(dataset_path),
        "config_sha256": sha256_file(config_path),
        "source_files": sources,
    }
    (output / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"phase": args.phase, **counts}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
