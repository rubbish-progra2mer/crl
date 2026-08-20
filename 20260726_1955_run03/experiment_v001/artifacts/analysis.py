"""Implementation v001: independent metric recomputation.

Reads per-instance probe_result JSON files plus results.jsonl produced by
run_promotion.py and recomputes every preregistered metric from the frozen
raw artifacts (no cached aggregates trusted). Usage:

    python analysis.py <config.json> <analysis_out.json>
"""

from __future__ import annotations

import json
import statistics
import sys
from pathlib import Path

IMPL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(IMPL_DIR))

import tp_lib  # noqa: E402


def category_cases(instance, probe_result):
    """Yield (category, enforced, default_verdict, witness_confirmed)."""
    probes = probe_result.get("probes") or {}
    default = probe_result.get("default") or {}
    verdicts = default.get("verdicts") or {}
    for category, p in probes.items():
        if not p.get("applicable"):
            continue
        enforced = p.get("enforced")
        if enforced is False:
            if category == "cuisine":
                confirmed = all(
                    bool(e.get("witness_violates_reference"))
                    for e in p["per_cuisine"].values()
                    if e.get("result") == "sat"
                )
            else:
                confirmed = bool(p.get("witness_violates_reference"))
        else:
            confirmed = None
        yield category, enforced, verdicts.get(category), confirmed


def main() -> int:
    config = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    out_dir = Path(config["out_dir"])
    results = [
        json.loads(line)
        for line in (out_dir / "results.jsonl").read_text(encoding="utf-8").splitlines()
    ]

    per_instance = []
    for row in results:
        idx = row["orig_index"]
        inst_dir = out_dir / f"idx{idx:03d}"
        instance = json.loads((inst_dir / "instance.json").read_text(encoding="utf-8"))
        arms = {}
        for arm in ("F1", "F2"):
            probe_path = inst_dir / f"{arm}_probe_result.json"
            if probe_path.is_file():
                arms[arm] = json.loads(probe_path.read_text(encoding="utf-8"))
        per_instance.append({"row": row, "instance": instance, "arms": arms})

    report: dict = {"n_rows": len(results)}

    # ---- F1 core metrics ----
    f1_ok, f1_pass, f1_masked_instances = [], [], []
    fault_cases = []  # (idx, category, masked/caught, density, luck)
    false_alarm_pool = []
    for item in per_instance:
        idx = item["row"]["orig_index"]
        pr = item["arms"].get("F1")
        if pr is None:
            continue
        status = pr.get("status")
        if status != "ok":
            continue
        f1_ok.append(idx)
        default_pass = pr["default"]["solution_level_pass"]
        if default_pass:
            f1_pass.append(idx)
        luck = pr.get("luck_sampling") or {}
        any_masked = False
        for category, enforced, default_verdict, confirmed in category_cases(
            item["instance"], pr
        ):
            if enforced is False:
                kind = "masked" if default_verdict is True else "caught"
                if kind == "masked":
                    any_masked = True
                fault_cases.append(
                    {
                        "orig_index": idx,
                        "category": category,
                        "kind": kind,
                        "witness_confirmed": confirmed,
                        "violating_option_density": tp_lib.violating_option_density(
                            item["instance"], category
                        ),
                        "luck_index": luck.get(category),
                        "default_pass": default_pass,
                    }
                )
            elif enforced is True:
                false_alarm_pool.append({"orig_index": idx, "category": category})
        if default_pass and any_masked:
            f1_masked_instances.append(idx)

    n_pass = len(f1_pass)
    n_masked = len(f1_masked_instances)
    low, high = tp_lib.wilson_interval(n_masked, n_pass)
    report["M1_fault_cases"] = fault_cases
    report["M1_per_category_faults"] = {}
    for case in fault_cases:
        report["M1_per_category_faults"].setdefault(case["category"], 0)
        report["M1_per_category_faults"][case["category"]] += 1
    report["M2"] = {
        "n_f1_ok": len(f1_ok),
        "n_certification_pass": n_pass,
        "n_masked_instances": n_masked,
        "masked_instance_ids": f1_masked_instances,
        "masking_rate": n_masked / n_pass if n_pass else None,
        "wilson_95": [low, high],
        "SIG1_lower_bound_gt_0": low > 0.0,
    }
    report["all_witnesses_checker_confirmed"] = all(
        c["witness_confirmed"] for c in fault_cases if c["kind"] in ("masked", "caught")
    ) if fault_cases else None

    # ---- statuses / A2 ----
    status_counts: dict[str, int] = {}
    for item in per_instance:
        pr = item["arms"].get("F1")
        status = pr.get("status") if pr else item["row"].get("F1_api", {}).get("status", "missing")
        status_counts[status] = status_counts.get(status, 0) + 1
    report["F1_statuses"] = status_counts
    report["A2_note"] = (
        "error signals (formalization_error/default_unsat/unknown) are instance-"
        "level; by construction they are absent on certification-PASS instances, "
        "so their coverage of masked cases is 0 (analytic, not empirical)."
    )

    # ---- M4 detector comparison (on F1 certificate cases) ----
    a3_eval = {"covered": 0, "missed": 0, "unavailable": 0, "false_alarms": 0,
               "false_alarm_denominator": 0}
    a4_eval = {"covered": 0, "missed": 0, "unavailable": 0, "false_alarms": 0,
               "false_alarm_denominator": 0}
    by_idx = {item["row"]["orig_index"]: item for item in per_instance}
    for case in fault_cases:
        item = by_idx[case["orig_index"]]
        a3 = item["row"].get("A3") or {}
        verdicts = a3.get("verdicts") or {}
        entry = verdicts.get(case["category"])
        if a3.get("status") != "ok" or not isinstance(entry, dict):
            a3_eval["unavailable"] += 1
        elif entry.get("enforced") is False:
            a3_eval["covered"] += 1
        else:
            a3_eval["missed"] += 1
        flags = (item["arms"].get("F1") or {}).get("behavioral_tests") or {}
        flag_entry = flags.get(case["category"])
        if not isinstance(flag_entry, dict) or "flag_unenforced" not in flag_entry:
            a4_eval["unavailable"] += 1
        elif flag_entry.get("flag_unenforced"):
            a4_eval["covered"] += 1
        else:
            a4_eval["missed"] += 1
    for pool_case in false_alarm_pool:
        item = by_idx[pool_case["orig_index"]]
        a3 = item["row"].get("A3") or {}
        verdicts = a3.get("verdicts") or {}
        entry = verdicts.get(pool_case["category"])
        if a3.get("status") == "ok" and isinstance(entry, dict):
            a3_eval["false_alarm_denominator"] += 1
            if entry.get("enforced") is False and entry.get("stated") is True:
                a3_eval["false_alarms"] += 1
        flags = (item["arms"].get("F1") or {}).get("behavioral_tests") or {}
        flag_entry = flags.get(pool_case["category"])
        if isinstance(flag_entry, dict) and "flag_unenforced" in flag_entry:
            a4_eval["false_alarm_denominator"] += 1
            if flag_entry.get("flag_unenforced"):
                a4_eval["false_alarms"] += 1
    report["M4_A3_selfcheck"] = a3_eval
    report["M4_A4_behavioral"] = a4_eval

    # ---- M5 slack mechanism ----
    masked = [c for c in fault_cases if c["kind"] == "masked"]
    caught = [c for c in fault_cases if c["kind"] == "caught"]

    def median_of(cases, key):
        values = [c[key] for c in cases if c.get(key) is not None]
        return statistics.median(values) if values else None

    luck_masked = median_of(masked, "luck_index")
    luck_caught = median_of(caught, "luck_index")
    density_masked = median_of(masked, "violating_option_density")
    density_caught = median_of(caught, "violating_option_density")
    budget_margins = []
    for item in per_instance:
        pr = item["arms"].get("F1")
        if pr is None or pr.get("status") != "ok":
            continue
        for case in fault_cases:
            if (case["orig_index"] == item["row"]["orig_index"]
                    and case["category"] == "budget" and case["kind"] == "masked"):
                cost = pr["default"]["total_cost"]
                budget = item["instance"]["budget"]
                budget_margins.append(
                    {"orig_index": case["orig_index"],
                     "margin_fraction": (budget - cost) / budget,
                     "flip_threshold_cost": cost}
                )
    report["M5"] = {
        "median_luck_masked": luck_masked,
        "median_luck_caught": luck_caught,
        "SIG2_primary_median_luck_masked_gt_0.5": (
            luck_masked is not None and luck_masked > 0.5
        ),
        "SIG2_secondary_luck_ordering": (
            None if (luck_masked is None or luck_caught is None)
            else luck_masked > luck_caught
        ),
        "median_density_masked": density_masked,
        "median_density_caught": density_caught,
        "density_ordering_masked_lt_caught": (
            None if (density_masked is None or density_caught is None)
            else density_masked < density_caught
        ),
        "masked_budget_margins": budget_margins,
        "n_masked_cases": len(masked),
        "n_caught_cases": len(caught),
    }

    # ---- F2 contrast ----
    f2 = {"n_ok": 0, "n_pass": 0, "n_masked": 0, "faults": {}}
    for item in per_instance:
        pr = item["arms"].get("F2")
        if pr is None or pr.get("status") != "ok":
            continue
        f2["n_ok"] += 1
        default_pass = pr["default"]["solution_level_pass"]
        if default_pass:
            f2["n_pass"] += 1
        any_masked = False
        for category, enforced, default_verdict, _ in category_cases(
            item["instance"], pr
        ):
            if enforced is False:
                f2["faults"][category] = f2["faults"].get(category, 0) + 1
                if default_verdict is True and default_pass:
                    any_masked = True
        if any_masked:
            f2["n_masked"] += 1
    report["F2_contrast"] = f2

    # ---- usage ----
    usage = {"calls": 0, "prompt_tokens": 0, "completion_tokens": 0}
    for row in results:
        for key in ("F1_api", "F2_api", "A3"):
            u = (row.get(key) or {}).get("usage") or {}
            if u:
                usage["calls"] += 1
                usage["prompt_tokens"] += u.get("prompt_tokens", 0)
                usage["completion_tokens"] += u.get("completion_tokens", 0)
    report["api_usage"] = usage

    Path(sys.argv[2]).write_text(
        json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    print(json.dumps({
        "M2": report["M2"],
        "SIG2_primary": report["M5"]["SIG2_primary_median_luck_masked_gt_0.5"],
        "witnesses_confirmed": report["all_witnesses_checker_confirmed"],
    }, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
