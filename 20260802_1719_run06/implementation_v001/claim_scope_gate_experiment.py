from __future__ import annotations

import argparse
import json
import random
import sys
import time
import urllib.request
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any


OLLAMA_URL = "http://127.0.0.1:11434/api/chat"


@dataclass(frozen=True)
class Record:
    record_id: str
    code: str
    day: int
    archived: bool


@dataclass(frozen=True)
class Task:
    task_id: str
    condition: str
    target_code: str
    records: tuple[Record, ...]
    global_access: bool = True

    @property
    def label(self) -> str:
        return "YES" if any(record.code == self.target_code for record in self.records) else "NO"


def build_tasks(seed: int, repeats: int) -> list[Task]:
    rng = random.Random(seed)
    conditions = (
        ["initial_witness"] * repeats
        + ["later_page_witness"] * repeats
        + ["old_witness"] * repeats
        + ["archived_witness"] * repeats
        + ["globally_absent"] * repeats
        + ["permission_hidden_witness"] * max(1, repeats // 2)
    )
    tasks: list[Task] = []
    for index, condition in enumerate(conditions):
        target = f"target-{index:03d}"
        records = [
            Record(f"r{index:03d}-{j}", f"other-{index:03d}-{j}", 96 - j * 14, j == 4)
            for j in range(6)
        ]
        global_access = condition != "permission_hidden_witness"
        if condition == "initial_witness":
            records[0] = Record(records[0].record_id, target, 96, False)
        elif condition == "later_page_witness":
            records[3] = Record(records[3].record_id, target, 54, False)
        elif condition == "old_witness":
            records[5] = Record(records[5].record_id, target, 6, False)
        elif condition in {"archived_witness", "permission_hidden_witness"}:
            records[4] = Record(records[4].record_id, target, 40, True)
        rng.shuffle(records)
        tasks.append(Task(f"task-{index:03d}", condition, target, tuple(records), global_access))
    rng.shuffle(tasks)
    return tasks


def call_model(model: str, task: Task, payload: dict[str, Any], reminder: bool, seed: int) -> tuple[str, dict[str, Any]]:
    system = (
        "你是工具型数据库代理的结论生成器。只能输出 JSON："
        "{\"answer\":\"YES|NO|UNKNOWN\"}。YES 表示存在目标记录，NO 表示不存在，"
        "UNKNOWN 表示当前证据不能确定。不要输出其他文字。"
    )
    if reminder:
        system += (
            "注意：结构合法的工具返回仍可能只覆盖默认时间窗、当前页或可见权限范围；"
            "没有看到目标不自动等于全局不存在。"
        )
    user = (
        f"问题：整个组织账户的全部历史（包括归档记录）中是否存在 code={task.target_code} 的记录？\n"
        f"系统预取工具的返回载荷：{json.dumps(payload, ensure_ascii=False)}"
    )
    body = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        "stream": False,
        "format": "json",
        "think": False,
        "keep_alive": "30m",
        "options": {"temperature": 0, "seed": seed, "num_predict": 80},
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        raw = json.loads(response.read().decode("utf-8"))
    content = raw.get("message", {}).get("content", "")
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {}
    answer = str(parsed.get("answer", "UNKNOWN")).upper()
    if answer not in {"YES", "NO", "UNKNOWN"}:
        answer = "UNKNOWN"
    usage = {
        "prompt_eval_count": raw.get("prompt_eval_count") or 0,
        "eval_count": raw.get("eval_count") or 0,
        "total_duration": raw.get("total_duration") or 0,
    }
    return answer, usage


def visible_records(task: Task, from_day: int, include_archived: bool) -> list[Record]:
    records = [
        record
        for record in task.records
        if (from_day == 0 or record.day >= from_day) and (include_archived or not record.archived)
    ]
    records.sort(key=lambda record: (-record.day, record.record_id))
    return records


def fetch_page(task: Task, from_day: int, include_archived: bool, cursor: int) -> tuple[dict[str, Any], dict[str, Any]]:
    records = visible_records(task, from_day, include_archived)
    page = records[cursor : cursor + 2]
    next_cursor = cursor + 2 if cursor + 2 < len(records) else None
    payload = {"status": "ok", "items": [asdict(record) for record in page]}
    capsule = {
        "from_day": from_day,
        "include_archived": include_archived,
        "cursor": cursor,
        "next_cursor": next_cursor,
        "permission_scope": "organization" if task.global_access else "personal_only",
        "truncated": next_cursor is not None,
    }
    return payload, capsule


def payload_has_witness(task: Task, payloads: list[dict[str, Any]]) -> bool:
    return any(
        item.get("code") == task.target_code
        for payload in payloads
        for item in payload.get("items", [])
    )


def close_scope(task: Task, initial_payload: dict[str, Any]) -> tuple[str, list[dict[str, Any]], list[dict[str, Any]]]:
    payloads = [initial_payload]
    capsules: list[dict[str, Any]] = []
    if payload_has_witness(task, payloads):
        return "YES", payloads, capsules
    if not task.global_access:
        return "UNKNOWN", payloads, capsules
    cursor = 0
    while True:
        payload, capsule = fetch_page(task, from_day=0, include_archived=True, cursor=cursor)
        payloads.append(payload)
        capsules.append(capsule)
        if payload_has_witness(task, [payload]):
            return "YES", payloads, capsules
        if capsule["next_cursor"] is None:
            return "NO", payloads, capsules
        cursor = capsule["next_cursor"]


def eager_scan(task: Task) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    payloads: list[dict[str, Any]] = []
    capsules: list[dict[str, Any]] = []
    if not task.global_access:
        payload, capsule = fetch_page(task, from_day=0, include_archived=True, cursor=0)
        capsule["permission_scope"] = "personal_only"
        return {"status": "ok", "items": payload["items"], "coverage": capsule}, [capsule]
    cursor = 0
    while True:
        payload, capsule = fetch_page(task, from_day=0, include_archived=True, cursor=cursor)
        payloads.append(payload)
        capsules.append(capsule)
        if capsule["next_cursor"] is None:
            break
        cursor = capsule["next_cursor"]
    merged = {
        "status": "ok",
        "items": [item for payload in payloads for item in payload["items"]],
        "coverage": {"from_day": 0, "include_archived": True, "pagination_complete": True, "permission_scope": "organization"},
    }
    return merged, capsules


def run_task(model: str, task: Task, mode: str, seed: int) -> dict[str, Any]:
    initial_payload, initial_capsule = fetch_page(task, from_day=30, include_archived=False, cursor=0)
    model_calls = 0
    usage = {"prompt_eval_count": 0, "eval_count": 0, "total_duration": 0}
    if mode == "eager_certified":
        model_payload, capsules = eager_scan(task)
        candidate_answer = "NOT_CALLED"
        tool_calls = len(capsules)
        if not task.global_access:
            answer = "UNKNOWN"
            certificate = "permission_partial"
        elif payload_has_witness(task, [model_payload]):
            answer = "YES"
            certificate = "positive_witness_after_full_scan"
        else:
            answer = "NO"
            certificate = "complete_negative_coverage"
    elif mode == "eager":
        model_payload, capsules = eager_scan(task)
        answer, model_usage = call_model(model, task, model_payload, reminder=False, seed=seed)
        model_calls = 1
        for key in usage:
            usage[key] += model_usage[key]
        tool_calls = len(capsules)
        certificate = "complete" if task.global_access else "permission_partial"
        candidate_answer = answer
    else:
        candidate_answer, model_usage = call_model(
            model, task, initial_payload, reminder=mode == "reminder", seed=seed
        )
        model_calls = 1
        for key in usage:
            usage[key] += model_usage[key]
        tool_calls = 1
        answer = candidate_answer
        certificate = "initial_payload_only"
        if mode == "gate":
            if candidate_answer == "YES" and payload_has_witness(task, [initial_payload]):
                answer = "YES"
                certificate = "positive_witness"
            else:
                answer, closure_payloads, closure_capsules = close_scope(task, initial_payload)
                tool_calls += len(closure_capsules)
                certificate = {
                    "YES": "positive_witness_after_closure",
                    "NO": "complete_negative_coverage",
                    "UNKNOWN": "permission_partial",
                }[answer]
    complete_scope = certificate in {"complete", "complete_negative_coverage"}
    witnessed = answer == "YES" and task.label == "YES"
    unsupported_no = answer == "NO" and not complete_scope and mode != "eager"
    if mode == "eager" and answer == "NO" and not task.global_access:
        unsupported_no = True
    return {
        "task_id": task.task_id,
        "condition": task.condition,
        "label": task.label,
        "mode": mode,
        "candidate_answer": candidate_answer,
        "answer": answer,
        "correct": answer == task.label,
        "accessible_correct": task.global_access and answer == task.label,
        "false_negative": task.label == "YES" and answer == "NO",
        "unsafe_overclaim": unsupported_no,
        "abstained": answer == "UNKNOWN",
        "positive_answer": witnessed,
        "tool_calls": tool_calls,
        "model_calls": model_calls,
        "certificate": certificate,
        "initial_payload": initial_payload,
        "initial_capsule": initial_capsule,
        "usage": usage,
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for mode in sorted({row["mode"] for row in results}):
        rows = [row for row in results if row["mode"] == mode]
        accessible = [row for row in rows if row["condition"] != "permission_hidden_witness"]
        summary[mode] = {
            "episodes": len(rows),
            "accuracy": sum(row["correct"] for row in rows) / len(rows),
            "accessible_accuracy": sum(row["correct"] for row in accessible) / len(accessible),
            "false_negatives": sum(row["false_negative"] for row in rows),
            "unsafe_overclaims": sum(row["unsafe_overclaim"] for row in rows),
            "abstentions": sum(row["abstained"] for row in rows),
            "mean_tool_calls": sum(row["tool_calls"] for row in rows) / len(rows),
            "mean_model_calls": sum(row["model_calls"] for row in rows) / len(rows),
            "prompt_tokens": sum(row["usage"]["prompt_eval_count"] for row in rows),
            "generated_tokens": sum(row["usage"]["eval_count"] for row in rows),
        }
    return summary


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen3:8b")
    parser.add_argument("--seed", type=int, default=20260802)
    parser.add_argument("--repeats", type=int, default=4)
    parser.add_argument("--limit", type=int)
    parser.add_argument(
        "--modes",
        nargs="+",
        default=["raw", "reminder", "gate", "eager", "eager_certified"],
    )
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    tasks = build_tasks(args.seed, args.repeats)
    if args.limit is not None:
        tasks = tasks[: args.limit]
    started = time.time()
    results: list[dict[str, Any]] = []
    for mode in args.modes:
        for task_index, task in enumerate(tasks):
            row = run_task(args.model, task, mode, args.seed + task_index)
            results.append(row)
            print(
                json.dumps(
                    {
                        "mode": mode,
                        "task": task.task_id,
                        "condition": task.condition,
                        "label": task.label,
                        "candidate": row["candidate_answer"],
                        "answer": row["answer"],
                        "correct": row["correct"],
                        "tools": row["tool_calls"],
                        "certificate": row["certificate"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
    document = {
        "experiment": "scope_closure_probe_v001",
        "model": args.model,
        "seed": args.seed,
        "task_count": len(tasks),
        "modes": args.modes,
        "elapsed_seconds": time.time() - started,
        "summary": summarize(results),
        "tasks": [
            {
                "task_id": task.task_id,
                "condition": task.condition,
                "target_code": task.target_code,
                "label": task.label,
                "global_access": task.global_access,
                "records": [asdict(record) for record in task.records],
            }
            for task in tasks
        ],
        "results": results,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps({"summary": document["summary"], "output": str(args.output)}, ensure_ascii=False))


if __name__ == "__main__":
    main()

