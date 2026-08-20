#!/usr/bin/env python3
"""执行 v007 的回归、有限模型与两服务扩大实验。"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path


HERE = Path(__file__).resolve().parent
RUN_ROOT = HERE.parent


def _run(argv, *, cwd=HERE):
    return subprocess.run(
        argv,
        cwd=cwd,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
    )


def _json_stdout(completed, label):
    if completed.returncode != 0:
        raise RuntimeError(
            f"{label} 失败：退出码={completed.returncode}\n{completed.stderr}"
        )
    payload = completed.stdout.strip()
    if not payload:
        raise RuntimeError(f"{label} 没有 JSON 标准输出")
    try:
        return json.loads(payload)
    except json.JSONDecodeError:
        lines = [line for line in payload.splitlines() if line.strip()]
        return json.loads(lines[-1])


def _write_json(path, value):
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", required=True)
    args = parser.parse_args()
    output_dir = Path(args.output_dir).resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    pytest_run = _run([sys.executable, "-B", "-m", "pytest", "-q", "test_protocol.py"])
    (output_dir / "pytest.txt").write_text(
        pytest_run.stdout + pytest_run.stderr,
        encoding="utf-8",
        newline="\n",
    )
    if pytest_run.returncode != 0:
        raise RuntimeError("协议测试失败")

    old_reproduction_run = _run(
        [sys.executable, "-B", str(RUN_ROOT / "workbench_v007" / "reproduce_v006_soundness.py")]
    )
    old_reproduction = _json_stdout(old_reproduction_run, "v006 反例复现")
    _write_json(output_dir / "v006_counterexamples.json", old_reproduction)

    attack_run = _run([sys.executable, "-B", "attack_audit.py"])
    attack = _json_stdout(attack_run, "v007 攻击审计")
    _write_json(output_dir / "attack_audit.json", attack)

    small_model_run = _run([sys.executable, "-B", "small_model_audit.py"])
    small_model = _json_stdout(small_model_run, "有限模型审计")
    _write_json(output_dir / "small_model_audit.json", small_model)

    pilot_run = _run(
        [sys.executable, "-B", "large_pilot.py", "--output-dir", str(output_dir)]
    )
    pilot = _json_stdout(pilot_run, "两服务扩大实验")

    engine_facts = json.loads((output_dir / "engine_facts.json").read_text(encoding="utf-8"))
    conditional = pilot["metrics_trusted_observer_identifiable_contracts"]["candidate"]
    trusted = pilot["metrics_trusted_observer"]["candidate"]
    expected = {
        "pytest_exit_zero": pytest_run.returncode == 0,
        "v006_counterexamples_all_reproduced": all(old_reproduction.values()),
        "v007_attack_scenarios_all_passed": attack["failed"] == 0,
        "small_model_candidate_oracle_zero_disagreement": (
            small_model["candidate_oracle_disagreements"] == 0
        ),
        "pilot_has_820_cases": pilot["case_count"] == 820,
        "trusted_identifiable_false_admission_zero": conditional["false_admission"] == 0,
        "trusted_identifiable_false_rejection_zero": conditional["false_rejection"] == 0,
        "trusted_all_false_admission_zero": trusted["false_admission"] == 0,
        "observer_masking_counterexamples_present": (
            pilot["candidate_false_admissions_by_category"]["observer_masking"] > 0
        ),
        "git_converged_clean": engine_facts["git"]["working_tree_clean"],
        "sqlite_and_git_use_distinct_observation_stores": (
            engine_facts["sqlite"]["adapter_path"]
            != engine_facts["git"]["adapter_path"]
        ),
    }
    summary = {
        "schema": "v007-full-evidence-1",
        "checks": expected,
        "all_checks_passed": all(expected.values()),
        "pytest_summary": pytest_run.stdout.strip(),
        "old_soundness_counterexample_count": len(old_reproduction),
        "v007_attack_scenario_count": attack["scenario_count"],
        "small_model": small_model,
        "pilot_key_results": {
            "case_count": pilot["case_count"],
            "probe_calls": pilot["probe_calls"],
            "trusted_identifiable_candidate": conditional,
            "trusted_all_candidate": trusted,
            "all_candidate": pilot["metrics_all"]["candidate"],
            "observer_masking_false_admissions": pilot[
                "candidate_false_admissions_by_category"
            ]["observer_masking"],
        },
        "scope_warning": (
            "通过条件只覆盖有限公式/投影域、受信签发者且观察器诚实的条件；"
            "观察器可签名谎报时的错误接纳是保留的反例，不属于通过项。"
        ),
    }
    _write_json(output_dir / "summary.json", summary)
    print(json.dumps(summary, ensure_ascii=False, sort_keys=True))
    return 0 if summary["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
