from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import language_typed_argument_pilot as pilot


WITNESS_IDS = {"zh_fr", "es_it", "de_es", "zh_it"}
RESULT_PATH = Path(__file__).with_name(
    f"language_typed_argument_crossmodel_{pilot.MODEL.replace(':', '_').replace('.', '_')}.json"
)


def main() -> None:
    rows: list[dict[str, Any]] = []
    for task in (item for item in pilot.TASKS if item["id"] in WITNESS_IDS):
        baseline_response = pilot.chat([{"role": "user", "content": task["prompt"]}], [pilot.TOOL])
        baseline_arguments = pilot.first_tool_arguments(baseline_response)
        row: dict[str, Any] = {
            "task_id": task["id"],
            "target_language": task["target_language"],
            "baseline": {
                "arguments": baseline_arguments,
                "score": pilot.score(task, baseline_arguments),
                "usage": pilot.usage(baseline_response),
            },
        }
        if baseline_arguments is None:
            for mode in ("whole_refine", "field_render"):
                row[mode] = {
                    "arguments": None,
                    "score": pilot.score(task, None),
                    "usage": pilot.usage(baseline_response),
                    "note": "baseline tool call missing",
                }
        else:
            whole_arguments, whole_response = pilot.refine_whole_call(task, baseline_arguments)
            field_arguments, field_response = pilot.render_body(task, baseline_arguments)
            row["whole_refine"] = {
                "arguments": whole_arguments,
                "score": pilot.score(task, whole_arguments),
                "usage": pilot.combined_usage([baseline_response, whole_response]),
            }
            row["field_render"] = {
                "arguments": field_arguments,
                "score": pilot.score(task, field_arguments),
                "usage": pilot.combined_usage([baseline_response, field_response]),
            }
        rows.append(row)
        print(
            json.dumps(
                {
                    "task_id": task["id"],
                    "scores": {
                        mode: row[mode]["score"]
                        for mode in ("baseline", "whole_refine", "field_render")
                    },
                },
                ensure_ascii=False,
            )
        )

    result = {
        "model": pilot.MODEL,
        "temperature": 0,
        "seed": 7,
        "witness_ids": sorted(WITNESS_IDS),
        "summary": {
            mode: pilot.summarize(rows, mode)
            for mode in ("baseline", "whole_refine", "field_render")
        },
        "rows": rows,
        "scope_note": "Four hard witnesses selected before the cross-model run from the qwen2.5:7b control experiment.",
    }
    RESULT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(json.dumps(result["summary"], ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
