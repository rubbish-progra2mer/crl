import json
from collections import defaultdict
from pathlib import Path

import scope_cell_semantic_rescore as semantic


HERE = Path(__file__).parent
INPUTS = [
    HERE / "scope_cell_synthesis_qwen2_5_7b.json",
    HERE / "scope_cell_synthesis_stress_qwen2_5_7b.json",
]
OUT = HERE / "exact_group_baseline_audit.json"
UNKNOWN = "未报告"


def exact_group(atoms, dimensions):
    names = list(dimensions)
    grouped = defaultdict(list)
    for atom in atoms:
        key = tuple(atom["conditions"].get(dim, UNKNOWN) for dim in names)
        grouped[key].append(atom)
    cells = []
    for key, members in grouped.items():
        directions = sorted({member["direction"] for member in members})
        cells.append(
            {
                "conditions": dict(zip(names, key)),
                "direction": directions[0] if len(directions) == 1 else "混合",
                "status": "支持" if len(directions) == 1 else "未解决",
                "source_ids": sorted({member["source_id"] for member in members}),
            }
        )
    return {"cells": cells, "global_claim": "无"}


def main():
    suites = []
    for path in INPUTS:
        data = json.loads(path.read_text(encoding="utf-8"))
        rows = []
        for record in data["records"]:
            dimensions = record["dimensions"]
            gold_atoms = record["gold_atoms"]
            gold = record["gold_partition"]
            grouped = exact_group(record["extraction"]["atoms"], dimensions)
            candidate = record["strategies"]["auto_partition"]["output"]
            grouped_score = semantic.score(grouped, gold, gold_atoms, dimensions)
            candidate_score = semantic.score(candidate, gold, gold_atoms, dimensions)
            rows.append(
                {
                    "task_id": record["task_id"],
                    "exact_group": {"output": grouped, "score": grouped_score},
                    "maximal_scope_partition": {"output": candidate, "score": candidate_score},
                    "cell_reduction": len(grouped["cells"]) - len(candidate["cells"]),
                }
            )
        suites.append(
            {
                "source": path.name,
                "tasks": len(rows),
                "exact_group_full_success": sum(row["exact_group"]["score"]["semantic_full_success"] for row in rows),
                "candidate_full_success": sum(row["maximal_scope_partition"]["score"]["semantic_full_success"] for row in rows),
                "exact_group_exact_semantics": sum(row["exact_group"]["score"]["exact_semantics"] for row in rows),
                "candidate_exact_semantics": sum(row["maximal_scope_partition"]["score"]["exact_semantics"] for row in rows),
                "exact_group_total_cells": sum(len(row["exact_group"]["output"]["cells"]) for row in rows),
                "candidate_total_cells": sum(len(row["maximal_scope_partition"]["output"]["cells"]) for row in rows),
                "rows": rows,
            }
        )
    result = {
        "model_rerun": False,
        "baseline": "同一自动证据抽取结果；按全部显式范围字段精确分组；同键相反方向标为未解决；不执行跨值合并。",
        "suites": suites,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8", newline="\n")
    print(
        json.dumps(
            [
                {
                    key: suite[key]
                    for key in [
                        "source",
                        "tasks",
                        "exact_group_full_success",
                        "candidate_full_success",
                        "exact_group_exact_semantics",
                        "candidate_exact_semantics",
                        "exact_group_total_cells",
                        "candidate_total_cells",
                    ]
                }
                for suite in suites
            ],
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
