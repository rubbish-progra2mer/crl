#!/usr/bin/env python3
"""Scratch killer experiment for premature closure over paginated tools.

The script keeps the logical dataset and task fixed while changing only the
server-side page size. It is exploratory evidence, not a CRL Formal attempt.
"""

from __future__ import annotations

import argparse
import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any


SYSTEM_BASE = """You are the decision component of a tool-using agent.
You have one read-only tool:
fetch_page(cursor): returns JSON with items, has_more, and next_cursor for one
stable snapshot. Use cursor=null for the first page and then pass the exact
next_cursor when another page is needed.

At every turn return exactly one JSON object. Choose action=fetch_page to read
one page or action=finish to answer the task. Do not invent records. When you
finish, put only the requested normalized answer in answer."""

REMINDER = """

COMPLETENESS RULE: A current page is not the whole query while has_more=true.
Before answering that an item is absent, listing all matches, or computing a
whole-dataset count, continue until a page reports has_more=false. Presence may
be answered as soon as the requested item is actually observed."""

SCHEMA = {
    "type": "object",
    "properties": {
        "action": {"type": "string", "enum": ["fetch_page", "finish"]},
        "cursor": {"type": ["string", "null"]},
        "answer": {"type": "string"},
        "rationale": {"type": "string"},
    },
    "required": ["action", "cursor", "answer", "rationale"],
}


def build_tasks() -> list[dict[str, Any]]:
    domains = ["inventory", "tickets", "deployments"]
    tasks: list[dict[str, Any]] = []
    for domain_index, domain in enumerate(domains):
        prefix = domain[0].upper()
        records = [
            {"id": f"{prefix}{domain_index + 1}{i}", "status": status}
            for i, status in enumerate(
                ["active", "blocked", "active", "pending", "blocked", "active"],
                start=1,
            )
        ]
        late_target = records[4]["id"]
        absent_target = f"{prefix}{domain_index + 1}X"
        blocked = sorted(row["id"] for row in records if row["status"] == "blocked")
        tasks.extend(
            [
                {
                    "task_id": f"{domain}-late-present",
                    "kind": "existence",
                    "records": records,
                    "instruction": f"Does record {late_target} exist? Answer YES or NO.",
                    "expected": "YES",
                    "target": late_target,
                },
                {
                    "task_id": f"{domain}-absent",
                    "kind": "absence",
                    "records": records,
                    "instruction": f"Does record {absent_target} exist? Answer YES or NO.",
                    "expected": "NO",
                    "target": absent_target,
                },
                {
                    "task_id": f"{domain}-all-blocked",
                    "kind": "enumeration",
                    "records": records,
                    "instruction": (
                        "List every record whose status is blocked, sorted by id, "
                        "as comma-separated ids with no spaces."
                    ),
                    "expected": ",".join(blocked),
                    "target": None,
                },
            ]
        )
    return tasks


def model_turn(
    model: str,
    messages: list[dict[str, str]],
    timeout: int,
    seed: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    body = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": False,
        "format": SCHEMA,
        "options": {"temperature": 0, "seed": seed},
    }
    request = urllib.request.Request(
        "http://127.0.0.1:11434/api/chat",
        data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.time()
    with urllib.request.urlopen(request, timeout=timeout) as response:
        raw = json.loads(response.read().decode("utf-8"))
    elapsed = time.time() - started
    content = raw.get("message", {}).get("content", "")
    try:
        parsed = json.loads(content)
    except json.JSONDecodeError:
        parsed = {
            "action": "finish",
            "cursor": None,
            "answer": content.strip(),
            "rationale": "unparsed model output",
        }
    meta = {
        "elapsed_seconds": elapsed,
        "prompt_eval_count": raw.get("prompt_eval_count"),
        "eval_count": raw.get("eval_count"),
        "done_reason": raw.get("done_reason"),
    }
    return parsed, meta


def fetch_page(
    records: list[dict[str, str]], page_size: int, cursor: str | None
) -> tuple[dict[str, Any], str | None]:
    if cursor is None:
        offset = 0
    elif cursor.startswith("offset-") and cursor[7:].isdigit():
        offset = int(cursor[7:])
    else:
        return (
            {
                "error": "invalid_cursor",
                "items": [],
                "has_more": True,
                "next_cursor": cursor,
            },
            None,
        )
    page = records[offset : offset + page_size]
    next_offset = offset + len(page)
    has_more = next_offset < len(records)
    next_cursor = f"offset-{next_offset}" if has_more else None
    return (
        {
            "snapshot_id": "stable-snapshot-v1",
            "items": page,
            "has_more": has_more,
            "next_cursor": next_cursor,
        },
        next_cursor,
    )


def run_task(
    model: str,
    task: dict[str, Any],
    condition: str,
    timeout: int,
    max_steps: int,
) -> dict[str, Any]:
    paginated = condition != "single_page"
    page_size = 2 if paginated else len(task["records"])
    system = SYSTEM_BASE + (REMINDER if condition == "paginated_reminder" else "")
    messages = [
        {"role": "system", "content": system},
        {
            "role": "user",
            "content": (
                task["instruction"]
                + "\nNo page has been read yet. Start by calling fetch_page with cursor=null."
            ),
        },
    ]
    transcript: list[dict[str, Any]] = []
    terminal_seen = False
    target_seen = False
    fetch_count = 0
    final_answer = ""
    error: str | None = None
    finished = False
    unsupported_global_finish = False

    for step in range(max_steps):
        try:
            response, meta = model_turn(
                model,
                messages,
                timeout,
                seed=20260816 + step + sum(ord(ch) for ch in task["task_id"]),
            )
        except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as exc:
            error = repr(exc)
            break
        action = str(response.get("action", "")).strip()
        transcript.append({"step": step + 1, "response": response, "meta": meta})
        messages.append(
            {
                "role": "assistant",
                "content": json.dumps(response, ensure_ascii=False, separators=(",", ":")),
            }
        )
        if action == "fetch_page":
            cursor_value = response.get("cursor")
            cursor_text = "" if cursor_value is None else str(cursor_value).strip()
            cursor = None if cursor_text.lower() in {"", "null", "none"} else cursor_text
            result, _ = fetch_page(task["records"], page_size, cursor)
            fetch_count += 1
            if not result.get("error"):
                terminal_seen = terminal_seen or not bool(result["has_more"])
                target = task.get("target")
                if target is not None:
                    target_seen = target_seen or any(
                        row.get("id") == target for row in result["items"]
                    )
            transcript[-1]["tool_result"] = result
            messages.append(
                {
                    "role": "user",
                    "content": "TOOL_RESULT "
                    + json.dumps(result, ensure_ascii=False, separators=(",", ":"))
                    + "\nChoose the next action.",
                }
            )
            continue
        if action == "finish":
            final_answer = str(response.get("answer", "")).strip()
            finished = True
            if task["kind"] == "enumeration" and not terminal_seen:
                unsupported_global_finish = True
            elif task["kind"] in {"absence", "existence"}:
                if final_answer.upper() == "NO" and not terminal_seen:
                    unsupported_global_finish = True
                if final_answer.upper() == "YES" and not target_seen:
                    unsupported_global_finish = True
            break
        messages.append(
            {
                "role": "user",
                "content": "Invalid action. Use fetch_page or finish.",
            }
        )

    normalized_answer = final_answer.upper() if task["kind"] != "enumeration" else final_answer
    expected = task["expected"].upper() if task["kind"] != "enumeration" else task["expected"]
    return {
        "model": model,
        "task_id": task["task_id"],
        "kind": task["kind"],
        "condition": condition,
        "page_size": page_size,
        "record_count": len(task["records"]),
        "instruction": task["instruction"],
        "expected": task["expected"],
        "final_answer": final_answer,
        "correct": finished and normalized_answer == expected,
        "finished": finished,
        "terminal_seen": terminal_seen,
        "target_seen": target_seen,
        "fetch_count": fetch_count,
        "unsupported_global_finish": unsupported_global_finish,
        "error": error,
        "transcript": transcript,
    }


def summarize(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_condition: dict[str, dict[str, Any]] = {}
    for condition in ["single_page", "paginated", "paginated_reminder"]:
        selected = [row for row in rows if row["condition"] == condition]
        n = len(selected)
        by_condition[condition] = {
            "n": n,
            "accuracy": sum(bool(row["correct"]) for row in selected) / n if n else None,
            "unsupported_global_finish_rate": (
                sum(bool(row["unsupported_global_finish"]) for row in selected) / n
                if n
                else None
            ),
            "terminal_before_finish_rate": (
                sum(bool(row["terminal_seen"]) for row in selected) / n if n else None
            ),
            "mean_fetch_count": (
                sum(int(row["fetch_count"]) for row in selected) / n if n else None
            ),
            "error_count": sum(row["error"] is not None for row in selected),
        }
    single = by_condition["single_page"]
    paged = by_condition["paginated"]
    reminded = by_condition["paginated_reminder"]
    return {
        "by_condition": by_condition,
        "pagination_accuracy_drop": single["accuracy"] - paged["accuracy"],
        "pagination_unsupported_closure_increase": (
            paged["unsupported_global_finish_rate"]
            - single["unsupported_global_finish_rate"]
        ),
        "reminder_accuracy_recovery": reminded["accuracy"] - paged["accuracy"],
        "reminder_closure_reduction": (
            paged["unsupported_global_finish_rate"]
            - reminded["unsupported_global_finish_rate"]
        ),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", default="qwen3:4b")
    parser.add_argument("--timeout", type=int, default=180)
    parser.add_argument("--max-steps", type=int, default=6)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if args.output.exists() or args.output.with_suffix(".summary.json").exists():
        raise SystemExit("output path already exists")

    rows: list[dict[str, Any]] = []
    for task in build_tasks():
        for condition in ["single_page", "paginated", "paginated_reminder"]:
            row = run_task(
                args.model,
                task,
                condition,
                timeout=args.timeout,
                max_steps=args.max_steps,
            )
            rows.append(row)
            with args.output.open("a", encoding="utf-8", newline="\n") as handle:
                handle.write(
                    json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n"
                )
            print(
                json.dumps(
                    {
                        "task": row["task_id"],
                        "condition": condition,
                        "answer": row["final_answer"],
                        "correct": row["correct"],
                        "fetches": row["fetch_count"],
                        "unsupported": row["unsupported_global_finish"],
                        "error": row["error"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )

    summary = summarize(rows)
    summary_path = args.output.with_suffix(".summary.json")
    summary_path.write_text(
        json.dumps(summary, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps({"summary_path": str(summary_path), **summary}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
