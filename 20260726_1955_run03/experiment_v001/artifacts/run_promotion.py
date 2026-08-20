"""Implementation v001: Promotion Development orchestrator (D bucket, TP-SC3).

Per instance (interleaved, model-drift control): F1 free-form formalization ->
F2 checklist formalization -> A3 self-check on the F1 code; then the solver
payload (default solve, A5 probes, A4 behavioral tests, M5c sampling) runs in
the z3 exception environment for F1 and F2.

Line-level checkpointing: each completed instance appends one JSON line to
results.jsonl; on restart, instances already present are skipped (external
API discipline per CRL.md section 7).

Configuration comes exclusively from the frozen config.json passed as argv;
the DeepSeek key exists only in the process environment.
"""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

IMPL_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(IMPL_DIR))

import tp_lib  # noqa: E402
from tp_api import call_deepseek, extract_code, extract_json, redact  # noqa: E402
from tp_prompt import build_a3, build_f1, build_f2  # noqa: E402


def load_done(results_path: Path) -> set[int]:
    done = set()
    if results_path.is_file():
        for line in results_path.read_text(encoding="utf-8").splitlines():
            try:
                done.add(json.loads(line)["orig_index"])
            except (json.JSONDecodeError, KeyError):
                continue
    return done


def main() -> int:
    config = json.loads(Path(sys.argv[1]).read_text(encoding="utf-8"))
    commit_dir = Path(config["commit_dir"])
    out_dir = Path(config["out_dir"])
    z3_python = Path(config["z3_python"])
    solve_probe = Path(config["solve_probe"])
    raw_log = out_dir / "deepseek_raw.jsonl"
    results_path = out_dir / "results.jsonl"
    out_dir.mkdir(parents=True, exist_ok=True)

    entries = tp_lib.load_bucket(commit_dir, config["bucket"])
    instances = []
    for entry in entries:
        instance = tp_lib.normalize_sc3(entry)
        if instance is not None:
            instances.append(instance)
    instances.sort(key=lambda x: x["orig_index"])
    if config.get("max_instances"):
        instances = instances[: config["max_instances"]]

    done = load_done(results_path)
    print(json.dumps({"n_instances": len(instances), "already_done": len(done)}))

    for instance in instances:
        idx = instance["orig_index"]
        if idx in done:
            continue
        tag = f"idx{idx:03d}"
        inst_dir = out_dir / tag
        inst_dir.mkdir(exist_ok=True)
        (inst_dir / "instance.json").write_text(
            json.dumps(instance, ensure_ascii=False, indent=2), encoding="utf-8"
        )
        row: dict = {
            "orig_index": idx,
            "level": instance["level"],
            "applicable_locals": [
                k for k, v in instance["local_constraint"].items() if v is not None
            ],
        }

        # --- API stage (interleaved F1 -> F2 -> A3) ---
        codes: dict[str, str | None] = {}
        for arm, builder in (("F1", build_f1), ("F2", build_f2)):
            try:
                body = call_deepseek(
                    builder(instance["query"]), raw_log=raw_log,
                    request_id=f"dev_{tag}_{arm}",
                )
                content = body["choices"][0]["message"]["content"]
                (inst_dir / f"{arm}_response.md").write_text(content, encoding="utf-8")
                code = extract_code(content)
                codes[arm] = code
                if code:
                    (inst_dir / f"{arm}_code.py").write_text(code, encoding="utf-8")
                row[f"{arm}_api"] = {
                    "status": "ok" if code else "no_code_block",
                    "response_model": body.get("model"),
                    "usage": body.get("usage"),
                }
            except Exception as error:  # noqa: BLE001
                codes[arm] = None
                row[f"{arm}_api"] = {"status": "call_failed",
                                     "error": redact(str(error))[:300]}

        if codes.get("F1"):
            try:
                body = call_deepseek(
                    build_a3(instance["query"], codes["F1"]), raw_log=raw_log,
                    request_id=f"dev_{tag}_A3",
                )
                content = body["choices"][0]["message"]["content"]
                (inst_dir / "A3_response.md").write_text(content, encoding="utf-8")
                parsed = extract_json(content)
                row["A3"] = {
                    "status": "ok" if parsed else "parse_error",
                    "verdicts": parsed,
                    "response_model": body.get("model"),
                    "usage": body.get("usage"),
                }
            except Exception as error:  # noqa: BLE001
                row["A3"] = {"status": "call_failed",
                             "error": redact(str(error))[:300]}

        # --- solver stage per formalization arm ---
        for arm in ("F1", "F2"):
            if not codes.get(arm):
                continue
            probe_out = inst_dir / f"{arm}_probe_result.json"
            completed = subprocess.run(
                [str(z3_python), str(solve_probe),
                 str(inst_dir / "instance.json"),
                 str(inst_dir / f"{arm}_code.py"),
                 str(probe_out), "full"],
                capture_output=True, text=True, timeout=1800,
            )
            row[f"{arm}_probe_exit"] = completed.returncode
            if completed.returncode != 0:
                row[f"{arm}_probe_stderr"] = redact(completed.stderr[-400:])
                continue
            probe_result = json.loads(probe_out.read_text(encoding="utf-8"))
            summary = {"status": probe_result["status"]}
            if probe_result.get("default"):
                summary["solution_level_pass"] = (
                    probe_result["default"]["solution_level_pass"]
                )
                summary["verdicts"] = probe_result["default"]["verdicts"]
                summary["total_cost"] = probe_result["default"]["total_cost"]
            if probe_result.get("probes"):
                summary["not_enforced"] = [
                    c for c, p in probe_result["probes"].items()
                    if p.get("applicable") and p.get("enforced") is False
                ]
                summary["enforced"] = [
                    c for c, p in probe_result["probes"].items()
                    if p.get("applicable") and p.get("enforced") is True
                ]
                witness_ok = []
                for c, p in probe_result["probes"].items():
                    if p.get("applicable") and p.get("enforced") is False:
                        if c == "cuisine":
                            witness_ok.extend(
                                bool(e.get("witness_violates_reference"))
                                for e in p["per_cuisine"].values()
                                if e.get("result") == "sat"
                            )
                        else:
                            witness_ok.append(bool(p.get("witness_violates_reference")))
                summary["all_witnesses_checker_confirmed"] = (
                    all(witness_ok) if witness_ok else None
                )
            if probe_result.get("luck_sampling"):
                summary["luck_sampling"] = probe_result["luck_sampling"]
            if probe_result.get("behavioral_tests"):
                summary["behavioral_flags"] = {
                    c: t.get("flag_unenforced")
                    for c, t in probe_result["behavioral_tests"].items()
                }
            row[arm] = summary

        with open(results_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(json.dumps({"instance": idx, "done": True}))

    print(json.dumps({"complete": True, "results": str(results_path)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
