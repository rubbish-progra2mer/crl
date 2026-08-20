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

    @property
    def label(self) -> str:
        return "YES" if any(r.code == self.target_code for r in self.records) else "NO"


def build_tasks(seed: int) -> list[Task]:
    rng = random.Random(seed)
    conditions = (
        ["easy_present"] * 3
        + ["old_present"] * 3
        + ["archived_present"] * 2
        + ["later_page_present"] * 2
        + ["absent"] * 2
    )
    tasks: list[Task] = []
    for index, condition in enumerate(conditions):
        target = f"needle-{index:03d}"
        records = [
            Record(f"r{index:02d}-{j}", f"other-{index:02d}-{j}", 95 - j * 13, j == 4)
            for j in range(6)
        ]
        if condition == "easy_present":
            records[0] = Record(records[0].record_id, target, 95, False)
        elif condition == "old_present":
            records[5] = Record(records[5].record_id, target, 4, False)
        elif condition == "archived_present":
            records[4] = Record(records[4].record_id, target, 43, True)
        elif condition == "later_page_present":
            records[3] = Record(records[3].record_id, target, 56, False)
        rng.shuffle(records)
        tasks.append(Task(f"task-{index:03d}", condition, target, tuple(records)))
    rng.shuffle(tasks)
    return tasks


def model_action(
    model: str,
    task: Task,
    mode: str,
    messages: list[dict[str, str]],
    seed: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    system = (
        "你是一个只能通过工具观察数据库的代理。你的每一步必须输出一个 JSON 对象，不能输出其他文字。"
        "可用工具 list_records 的参数为：from_day（可选整数，默认 30，0 表示全部历史）、"
        "include_archived（可选布尔值，默认 false）、cursor（可选整数，默认 0）。"
        "工具每页最多返回 2 条记录，next_cursor 为 null 才表示这个确切查询已经翻到末页。"
        "调用工具时输出 {\"action\":\"list\",\"from_day\":0,\"include_archived\":true,\"cursor\":0}；"
        "提交结论时输出 {\"action\":\"answer\",\"answer\":\"YES|NO|UNKNOWN\"}。"
        "最多可以采取 8 步。"
    )
    if mode == "reminder":
        system += (
            "重要：不能用默认时间窗、未包含归档或未完成分页的空/局部返回推出全局不存在；"
            "回答 NO 前必须覆盖全部历史、包含归档并完成所有分页。"
        )
    question = (
        f"请判断整个账户的全部历史（包括归档记录）中是否存在 code 等于 {task.target_code} 的记录。"
        "存在回答 YES，不存在回答 NO；确实无法确定时回答 UNKNOWN。"
    )
    payload = {
        "model": model,
        "messages": [{"role": "system", "content": system}, {"role": "user", "content": question}] + messages,
        "stream": False,
        "format": "json",
        "think": False,
        "keep_alive": "30m",
        "options": {"temperature": 0, "seed": seed, "num_predict": 180},
    }
    request = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        raw = json.loads(response.read().decode("utf-8"))
    content = raw.get("message", {}).get("content", "")
    try:
        action = json.loads(content)
    except json.JSONDecodeError:
        start = content.find("{")
        end = content.rfind("}")
        action = json.loads(content[start : end + 1]) if start >= 0 < end else {"action": "invalid"}
    usage = {
        "prompt_eval_count": raw.get("prompt_eval_count"),
        "eval_count": raw.get("eval_count"),
        "total_duration": raw.get("total_duration"),
    }
    return action, usage


def execute_list(task: Task, action: dict[str, Any]) -> dict[str, Any]:
    try:
        from_day = int(action.get("from_day", 30))
    except (TypeError, ValueError):
        from_day = 30
    include_archived = bool(action.get("include_archived", False))
    try:
        cursor = max(0, int(action.get("cursor", 0)))
    except (TypeError, ValueError):
        cursor = 0
    eligible = [
        r
        for r in task.records
        if (from_day == 0 or r.day >= from_day) and (include_archived or not r.archived)
    ]
    eligible.sort(key=lambda r: (-r.day, r.record_id))
    page = eligible[cursor : cursor + 2]
    next_cursor = cursor + 2 if cursor + 2 < len(eligible) else None
    return {
        "items": [asdict(record) for record in page],
        "next_cursor": next_cursor,
        "effective_scope": {
            "from_day": from_day,
            "include_archived": include_archived,
            "cursor": cursor,
            "page_size": 2,
        },
        "status": "ok",
        "truncated": next_cursor is not None,
    }


def has_complete_global_coverage(observations: list[dict[str, Any]]) -> bool:
    by_cursor = {
        obs["effective_scope"]["cursor"]: obs
        for obs in observations
        if obs["status"] == "ok"
        and obs["effective_scope"]["from_day"] == 0
        and obs["effective_scope"]["include_archived"] is True
    }
    cursor = 0
    visited: set[int] = set()
    while cursor in by_cursor and cursor not in visited:
        visited.add(cursor)
        next_cursor = by_cursor[cursor]["next_cursor"]
        if next_cursor is None:
            return True
        cursor = next_cursor
    return False


def has_positive_witness(task: Task, observations: list[dict[str, Any]]) -> bool:
    return any(
        item.get("code") == task.target_code
        for observation in observations
        for item in observation.get("items", [])
    )


def coverage_feedback(task: Task, observations: list[dict[str, Any]], answer: str) -> str | None:
    if answer == "YES" and not has_positive_witness(task, observations):
        return "覆盖门拒绝：YES 没有已返回记录作为正面见证。请继续查询或回答 UNKNOWN。"
    if answer == "NO" and not has_complete_global_coverage(observations):
        return (
            "覆盖门拒绝：NO 尚未由连续完整的全历史、含归档分页链支持。"
            "请从 cursor=0 使用 from_day=0、include_archived=true 查询，并沿 next_cursor 查到 null；"
            "否则回答 UNKNOWN。"
        )
    return None


def run_episode(model: str, task: Task, mode: str, seed: int) -> dict[str, Any]:
    messages: list[dict[str, str]] = []
    observations: list[dict[str, Any]] = []
    trajectory: list[dict[str, Any]] = []
    answer = "UNKNOWN"
    gate_rejections = 0
    usage_totals = {"prompt_eval_count": 0, "eval_count": 0, "total_duration": 0}
    for step in range(8):
        action, usage = model_action(model, task, mode, messages, seed + step)
        for key in usage_totals:
            usage_totals[key] += usage.get(key) or 0
        trajectory.append({"step": step, "action": action})
        messages.append({"role": "assistant", "content": json.dumps(action, ensure_ascii=False)})
        if action.get("action") == "list":
            observation = execute_list(task, action)
            observations.append(observation)
            trajectory[-1]["observation"] = observation
            messages.append(
                {"role": "user", "content": "工具返回：" + json.dumps(observation, ensure_ascii=False)}
            )
            continue
        if action.get("action") == "answer":
            proposed = str(action.get("answer", "UNKNOWN")).upper()
            if proposed not in {"YES", "NO", "UNKNOWN"}:
                proposed = "UNKNOWN"
            feedback = coverage_feedback(task, observations, proposed) if mode == "gate" else None
            if feedback is not None:
                gate_rejections += 1
                trajectory[-1]["gate_rejection"] = feedback
                messages.append({"role": "user", "content": feedback})
                continue
            answer = proposed
            break
        messages.append({"role": "user", "content": "无效动作；只允许 list 或 answer 的 JSON。"})

    complete_coverage = has_complete_global_coverage(observations)
    witness = has_positive_witness(task, observations)
    return {
        "task_id": task.task_id,
        "condition": task.condition,
        "target_code": task.target_code,
        "label": task.label,
        "mode": mode,
        "answer": answer,
        "correct": answer == task.label,
        "false_negative": task.label == "YES" and answer == "NO",
        "unsupported_no": answer == "NO" and not complete_coverage,
        "unsupported_yes": answer == "YES" and not witness,
        "abstained": answer == "UNKNOWN",
        "complete_global_coverage": complete_coverage,
        "positive_witness": witness,
        "tool_calls": len(observations),
        "gate_rejections": gate_rejections,
        "usage": usage_totals,
        "trajectory": trajectory,
    }


def summarize(results: list[dict[str, Any]]) -> dict[str, Any]:
    summary: dict[str, Any] = {}
    for mode in sorted({result["mode"] for result in results}):
        rows = [result for result in results if result["mode"] == mode]
        summary[mode] = {
            "episodes": len(rows),
            "accuracy": sum(row["correct"] for row in rows) / len(rows),
            "false_negatives": sum(row["false_negative"] for row in rows),
            "unsupported_no": sum(row["unsupported_no"] for row in rows),
            "unsupported_yes": sum(row["unsupported_yes"] for row in rows),
            "abstentions": sum(row["abstained"] for row in rows),
            "complete_coverage": sum(row["complete_global_coverage"] for row in rows),
            "mean_tool_calls": sum(row["tool_calls"] for row in rows) / len(rows),
            "gate_rejections": sum(row["gate_rejections"] for row in rows),
            "prompt_tokens": sum(row["usage"]["prompt_eval_count"] for row in rows),
            "generated_tokens": sum(row["usage"]["eval_count"] for row in rows),
        }
    return summary


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen3:8b")
    parser.add_argument("--seed", type=int, default=20260802)
    parser.add_argument("--modes", nargs="+", default=["raw", "reminder", "gate"])
    parser.add_argument("--limit", type=int, default=12)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    started = time.time()
    tasks = build_tasks(args.seed)[: args.limit]
    results: list[dict[str, Any]] = []
    for mode_index, mode in enumerate(args.modes):
        for task_index, task in enumerate(tasks):
            result = run_episode(args.model, task, mode, args.seed + mode_index * 1000 + task_index * 20)
            results.append(result)
            print(
                json.dumps(
                    {
                        "mode": mode,
                        "task": task.task_id,
                        "condition": task.condition,
                        "label": task.label,
                        "answer": result["answer"],
                        "correct": result["correct"],
                        "calls": result["tool_calls"],
                        "gate_rejections": result["gate_rejections"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
    document = {
        "experiment": "scope_gate_probe_v001",
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
