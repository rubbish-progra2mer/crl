"""Workbench v001 orchestrator: K1 decisive falsifier.

Selects single-city 3-day W-bucket instances, obtains one free-form
formalization per instance from DeepSeek, then solves + probes enforcement in
the z3 exception environment. Aggregates the masking taxonomy that decides
whether kernel K1 lives.

Run from workbench_v001/ with the shared interpreter; DEEPSEEK_API_KEY must be
in the process environment.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import wb_lib
from wb_formalize import formalize, redact

WB = Path(__file__).resolve().parent
COMMIT = WB.parent / "data_split_commitment_v001"
OUT = WB / "out"
Z3_PYTHON = WB.parent / ".venv_z3" / "python.exe"
RAW_LOG = WB / "out" / "deepseek_raw.jsonl"


def main() -> int:
    max_instances = int(sys.argv[1]) if len(sys.argv) > 1 else 22
    entries = wb_lib.load_bucket(COMMIT, "W")
    selected = []
    for entry in entries:
        instance = wb_lib.normalize_sc3(entry)
        if instance is None:
            continue
        has_local = any(v is not None for v in instance["local_constraint"].values())
        selected.append((instance, has_local))
    # local-constraint instances first (the interesting audit surface), then easy
    selected.sort(key=lambda pair: (not pair[1], pair[0]["orig_index"]))
    selected = [instance for instance, _ in selected[:max_instances]]

    OUT.mkdir(exist_ok=True)
    summary = []
    for instance in selected:
        tag = f"idx{instance['orig_index']:03d}"
        inst_dir = OUT / tag
        inst_dir.mkdir(exist_ok=True)
        (inst_dir / "instance.json").write_text(
            json.dumps(instance, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        row: dict = {
            "orig_index": instance["orig_index"],
            "level": instance["level"],
            "applicable_locals": [
                k for k, v in instance["local_constraint"].items() if v is not None
            ],
        }
        try:
            info = formalize(
                instance["query"], inst_dir, RAW_LOG, request_id=f"wb_{tag}"
            )
            row["formalize"] = info
        except Exception as error:  # noqa: BLE001
            row["formalize"] = {"status": "call_failed", "error": redact(str(error))[:300]}
            summary.append(row)
            print(json.dumps(row, ensure_ascii=False))
            continue
        if row["formalize"]["status"] != "ok":
            summary.append(row)
            print(json.dumps(row, ensure_ascii=False))
            continue
        completed = subprocess.run(
            [
                str(Z3_PYTHON),
                str(WB / "wb_solve_probe.py"),
                str(inst_dir / "instance.json"),
                str(inst_dir / "generated_code.py"),
                str(inst_dir / "probe_result.json"),
            ],
            capture_output=True,
            text=True,
            timeout=900,
        )
        row["probe_exit"] = completed.returncode
        if completed.returncode != 0:
            row["probe_stderr"] = redact(completed.stderr[-400:])
        else:
            probe_result = json.loads(
                (inst_dir / "probe_result.json").read_text(encoding="utf-8")
            )
            row["status"] = probe_result["status"]
            if probe_result.get("default"):
                row["solution_level_pass"] = probe_result["default"]["solution_level_pass"]
                row["default_verdicts"] = probe_result["default"]["verdicts"]
            if probe_result.get("probes"):
                row["not_enforced"] = [
                    c
                    for c, p in probe_result["probes"].items()
                    if p.get("applicable") and p.get("enforced") is False
                ]
                row["enforced"] = [
                    c
                    for c, p in probe_result["probes"].items()
                    if p.get("applicable") and p.get("enforced") is True
                ]
        summary.append(row)
        print(json.dumps(row, ensure_ascii=False))

    (OUT / "falsifier_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    # decisive aggregation
    ran = [r for r in summary if r.get("status") == "ok" and "solution_level_pass" in r]
    masked_rows = []
    for r in ran:
        if not r.get("not_enforced"):
            continue
        masked_categories = [
            c
            for c in r["not_enforced"]
            if r["default_verdicts"].get(c) is True
        ]
        if masked_categories:
            masked_rows.append(
                {"orig_index": r["orig_index"], "masked_categories": masked_categories,
                 "solution_level_pass": r["solution_level_pass"]}
            )
    aggregate = {
        "n_selected": len(selected),
        "n_model_ran": len(ran),
        "n_with_any_unenforced_category": sum(1 for r in ran if r.get("not_enforced")),
        "n_solution_level_pass": sum(1 for r in ran if r["solution_level_pass"]),
        "n_masked_rows": len(masked_rows),
        "masked_rows": masked_rows,
        "n_pass_and_unenforced": sum(
            1 for r in ran if r["solution_level_pass"] and r.get("not_enforced")
        ),
    }
    (OUT / "falsifier_aggregate.json").write_text(
        json.dumps(aggregate, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print("AGGREGATE:", json.dumps(aggregate, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
