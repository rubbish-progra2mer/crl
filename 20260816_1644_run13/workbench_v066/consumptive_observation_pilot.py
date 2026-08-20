from __future__ import annotations

import json
import os
import time
import urllib.request
from pathlib import Path
from typing import Any


MODEL = os.environ.get("CRL_V066_MODEL", "qwen2.5:7b")
ENDPOINT = "http://127.0.0.1:11434/api/chat"
RESULT_PATH = Path(__file__).with_name(
    f"consumptive_observation_{MODEL.replace(':', '_').replace('.', '_')}_r1.json"
)

DOMAINS = (
    "inbox",
    "queue",
    "token_pool",
    "job_pool",
    "alert_feed",
    "ticket_bin",
    "approval_box",
    "command_stream",
    "sensor_buffer",
    "voucher_stack",
    "reservation_hold",
    "work_item",
)


def build_pair(index: int, domain: str, mode: str) -> dict[str, Any]:
    alpha = f"access_{domain}_alpha"
    beta = f"access_{domain}_beta"
    consume_name, pure_name = (alpha, beta) if index % 2 == 0 else (beta, alpha)
    type_prefix = {
        consume_name: "observation_effect=CONSUMES_CURRENT_ITEM; " if mode == "effect_typed" else "",
        pure_name: "observation_effect=PURE_READ; " if mode == "effect_typed" else "",
    }
    descriptions = {
        consume_name: (
            type_prefix[consume_name]
            + f"Returns the current next {domain} entry at cost 1. In the same atomic call it removes that entry "
            "from availability and advances the shared cursor, so another worker cannot receive the same entry."
        ),
        pure_name: (
            type_prefix[pure_name]
            + f"Returns a current snapshot of the same next {domain} entry at cost 3. It does not acknowledge, "
            "remove, reserve, reorder, or advance any cursor, so availability remains unchanged."
        ),
    }
    order = (alpha, beta) if index % 4 in (0, 3) else (beta, alpha)
    tools = [
        {"name": name, "description": descriptions[name], "cost": 1 if name == consume_name else 3}
        for name in order
    ]
    return {
        "pair_id": f"{index + 1:02d}_{domain}",
        "domain": domain,
        "consume_tool": consume_name,
        "pure_tool": pure_name,
        "tools": tools,
    }


def chat(pair: dict[str, Any], task_type: str, mode: str) -> dict[str, Any]:
    if task_type == "preserve":
        task = (
            f"Inspect the current next {pair['domain']} entry for an audit. Leave its availability, ordering, "
            "acknowledgement state, reservation state, and shared cursor unchanged. Choose exactly one access interface."
        )
        correct = pair["pure_tool"]
    else:
        task = (
            f"Atomically claim the current next {pair['domain']} entry so no other worker can receive that same entry. "
            "After satisfying that semantic requirement, prefer lower cost. Choose exactly one access interface."
        )
        correct = pair["consume_tool"]
    payload = {
        "model": MODEL,
        "stream": False,
        "think": False,
        "format": {
            "type": "object",
            "properties": {
                "choice": {"type": "string", "enum": [item["name"] for item in pair["tools"]]},
                "reason": {"type": "string"},
            },
            "required": ["choice", "reason"],
            "additionalProperties": False,
        },
        "options": {"temperature": 0, "seed": 66, "num_predict": 160},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are selecting one interface for a stateful tool-using agent. Respect the requested state effect "
                    "before optimizing cost. Return only the required JSON object."
                ),
            },
            {
                "role": "user",
                "content": json.dumps(
                    {"task": task, "interfaces": pair["tools"], "documentation_mode": mode},
                    ensure_ascii=False,
                    indent=2,
                ),
            },
        ],
    }
    request = urllib.request.Request(
        ENDPOINT,
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )
    started = time.perf_counter()
    with urllib.request.urlopen(request, timeout=180) as response:
        raw = json.loads(response.read().decode("utf-8"))
    elapsed = time.perf_counter() - started
    content = raw.get("message", {}).get("content", "")
    parsed: dict[str, Any] | None = None
    try:
        candidate = json.loads(content)
        if isinstance(candidate, dict):
            parsed = candidate
    except json.JSONDecodeError:
        parsed = None
    choice = parsed.get("choice") if parsed else None
    return {
        "choice": choice,
        "correct_tool": correct,
        "correct": choice == correct,
        "valid_json": parsed is not None and choice in {item["name"] for item in pair["tools"]},
        "reason": parsed.get("reason", "") if parsed else "",
        "raw_content": content,
        "prompt_tokens": int(raw.get("prompt_eval_count", 0)),
        "output_tokens": int(raw.get("eval_count", 0)),
        "elapsed_seconds": elapsed,
    }


def summarize(rows: list[dict[str, Any]], mode: str) -> dict[str, Any]:
    preserve = [row for row in rows if row["task_type"] == "preserve"]
    claim = [row for row in rows if row["task_type"] == "claim"]
    by_pair: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        by_pair.setdefault(row["pair_id"], []).append(row)
    return {
        "n": len(rows),
        "paired_n": len(by_pair),
        "paired_correct": sum(
            len(group) == 2 and all(item[mode]["correct"] for item in group)
            for group in by_pair.values()
        ),
        "preserve_correct": sum(row[mode]["correct"] for row in preserve),
        "claim_correct": sum(row[mode]["correct"] for row in claim),
        "invalid_json": sum(not row[mode]["valid_json"] for row in rows),
        "prompt_tokens": sum(row[mode]["prompt_tokens"] for row in rows),
        "output_tokens": sum(row[mode]["output_tokens"] for row in rows),
        "elapsed_seconds": sum(row[mode]["elapsed_seconds"] for row in rows),
    }


def main() -> None:
    rows: list[dict[str, Any]] = []
    for index, domain in enumerate(DOMAINS):
        prose_pair = build_pair(index, domain, "prose")
        typed_pair = build_pair(index, domain, "effect_typed")
        for task_type in ("preserve", "claim"):
            row: dict[str, Any] = {"pair_id": prose_pair["pair_id"], "task_type": task_type}
            row["prose"] = chat(prose_pair, task_type, "prose")
            row["effect_typed"] = chat(typed_pair, task_type, "effect_typed")
            rows.append(row)
            print(
                json.dumps(
                    {
                        "pair_id": row["pair_id"],
                        "task_type": task_type,
                        "prose": row["prose"]["choice"],
                        "effect_typed": row["effect_typed"]["choice"],
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
    result = {
        "model": MODEL,
        "endpoint": ENDPOINT,
        "temperature": 0,
        "seed": 66,
        "pair_count": len(DOMAINS),
        "task_count": len(rows),
        "summary": {mode: summarize(rows, mode) for mode in ("prose", "effect_typed")},
        "rows": rows,
        "scope_note": "Synthetic benign interface selection only. No represented access interface was executed.",
    }
    RESULT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
