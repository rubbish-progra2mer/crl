from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import fault_domain_routing_pilot as pilot


RESULT_PATH = Path(__file__).with_name(
    f"fault_domain_routing_{pilot.MODEL.replace(':', '_').replace('.', '_')}_state_card_r2.json"
)
MODE = "state_card"


def without_recommendation(card: str) -> str:
    lines = [line for line in card.splitlines() if "best viable fallback=" not in line]
    result = "\n".join(lines)
    if "best viable fallback=" in result:
        raise AssertionError("recommendation removal failed")
    return result


def main() -> None:
    rows: list[dict[str, Any]] = []
    for pair in pilot.PAIRS:
        for fault_type in ("common", "local"):
            task = dict(pair[fault_type])
            task["card"] = without_recommendation(task["card"])
            response = pilot.chat(task, "domain_card")
            choice = pilot.selected_tool(response)
            row = {
                "pair_id": task["pair_id"],
                "fault_type": fault_type,
                "correct_tool": task["correct_tool"],
                "tool_order": [item["function"]["name"] for item in task["tools"]],
                MODE: {
                    "selected_tool": choice,
                    "correct": choice == task["correct_tool"],
                    "content": response.get("message", {}).get("content", ""),
                    "prompt_tokens": int(response.get("prompt_eval_count", 0)),
                    "output_tokens": int(response.get("eval_count", 0)),
                    "elapsed_seconds": float(response.get("client_elapsed_seconds", 0.0)),
                },
            }
            rows.append(row)
            print(
                json.dumps(
                    {
                        "pair_id": task["pair_id"],
                        "fault_type": fault_type,
                        "correct_tool": task["correct_tool"],
                        "selected_tool": choice,
                    },
                    ensure_ascii=False,
                ),
                flush=True,
            )
    result = {
        "model": pilot.MODEL,
        "endpoint": pilot.ENDPOINT,
        "temperature": 0,
        "seed": 63,
        "pair_count": len(pilot.PAIRS),
        "task_count": len(rows),
        "condition": "state_card_without_best_fallback_line",
        "recommendation_omitted": True,
        "summary": pilot.summarize(rows, MODE),
        "rows": rows,
        "scope_note": "Synthetic benign fallback selection only. No represented fallback tool was executed.",
    }
    RESULT_PATH.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2), flush=True)


if __name__ == "__main__":
    main()
