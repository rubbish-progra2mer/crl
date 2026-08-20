from __future__ import annotations

import argparse
import collections
import hashlib
import importlib.util
import json
import math
import random
import sys
from pathlib import Path, PurePosixPath
from typing import Any, Iterable, Sequence


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def canonical_sha256(value: Any) -> str:
    data = json.dumps(
        value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(data).hexdigest()


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(
            value,
            ensure_ascii=False,
            indent=2,
            sort_keys=True,
            allow_nan=False,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def manifest_path(root: Path, relative: str) -> Path:
    normalized = PurePosixPath(relative).as_posix()
    return root / ("input__" + normalized.replace("/", "__"))


def load_official_module(path: Path, expected_sha256: str):
    actual = sha256_file(path)
    if actual != expected_sha256:
        raise ValueError(
            f"official detect SHA mismatch: expected {expected_sha256}, got {actual}"
        )
    spec = importlib.util.spec_from_file_location("toolfailbench_official_detect", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot import official detector: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def rgp_classify(
    task: dict[str, Any],
    agent_trace: dict[str, Any],
    agent_answer: str,
    official: Any,
) -> str:
    if not task["evaluation_criteria"]["tool_must_be_called"]:
        return official.classify_failure_mode(task, agent_trace, agent_answer)
    if official.detect_tool_skip(task, agent_trace):
        return "tool_skip"
    if official._answer_correct(task, agent_answer):
        return "correct"
    if official.detect_output_fabrication(task, agent_trace, agent_answer):
        return "output_fabrication"
    return "result_ignore"


def macro_f1(truth: Sequence[str], prediction: Sequence[str]) -> float:
    labels = sorted(set(truth) | set(prediction))
    if not labels:
        return math.nan
    scores: list[float] = []
    for label in labels:
        tp = sum(t == label and p == label for t, p in zip(truth, prediction))
        fp = sum(t != label and p == label for t, p in zip(truth, prediction))
        fn = sum(t == label and p != label for t, p in zip(truth, prediction))
        denominator = 2 * tp + fp + fn
        scores.append(0.0 if denominator == 0 else (2 * tp) / denominator)
    return sum(scores) / len(scores)


def percentile(sorted_values: Sequence[float], q: float) -> float:
    if not sorted_values:
        raise ValueError("percentile requires at least one value")
    position = (len(sorted_values) - 1) * q
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return float(sorted_values[lower])
    fraction = position - lower
    return float(
        sorted_values[lower] * (1.0 - fraction)
        + sorted_values[upper] * fraction
    )


def grouped_accuracy(rows: Sequence[dict[str, Any]]) -> dict[str, Any]:
    eligible = [row for row in rows if row["unanimous_label"] is not None]
    count = len(eligible)
    official_correct = sum(
        row["official_label"] == row["unanimous_label"] for row in eligible
    )
    rgp_correct = sum(row["rgp_label"] == row["unanimous_label"] for row in eligible)
    return {
        "rows": count,
        "official_correct": official_correct,
        "rgp_correct": rgp_correct,
        "official_accuracy": official_correct / count if count else math.nan,
        "rgp_accuracy": rgp_correct / count if count else math.nan,
        "accuracy_delta": (rgp_correct - official_correct) / count
        if count
        else math.nan,
    }


def cluster_bootstrap(
    rows: Sequence[dict[str, Any]],
    *,
    resamples: int,
    seed: int,
) -> dict[str, Any]:
    grouped: dict[str, dict[str, int]] = {}
    for row in rows:
        truth = row["unanimous_label"]
        if truth is None:
            continue
        stats = grouped.setdefault(
            row["model_id"], {"rows": 0, "official_correct": 0, "rgp_correct": 0}
        )
        stats["rows"] += 1
        stats["official_correct"] += int(row["official_label"] == truth)
        stats["rgp_correct"] += int(row["rgp_label"] == truth)
    models = sorted(grouped)
    if not models:
        raise ValueError("no model clusters available for bootstrap")
    rng = random.Random(seed)
    samples: list[float] = []
    for _ in range(resamples):
        selected = [models[rng.randrange(len(models))] for _ in models]
        total = sum(grouped[model]["rows"] for model in selected)
        difference = sum(
            grouped[model]["rgp_correct"] - grouped[model]["official_correct"]
            for model in selected
        )
        samples.append(difference / total)
    samples.sort()
    return {
        "unit": "generator_model",
        "cluster_count": len(models),
        "resamples": resamples,
        "seed": seed,
        "lower_95": percentile(samples, 0.025),
        "median": percentile(samples, 0.5),
        "upper_95": percentile(samples, 0.975),
        "minimum": samples[0],
        "maximum": samples[-1],
    }


def transition_counts(
    rows: Iterable[dict[str, Any]], left: str, right: str
) -> dict[str, int]:
    counts: collections.Counter[str] = collections.Counter()
    for row in rows:
        counts[f"{row[left]} -> {row[right]}"] += 1
    return dict(sorted(counts.items()))


def per_group(
    rows: Sequence[dict[str, Any]], key: str
) -> dict[str, dict[str, Any]]:
    grouped: dict[str, list[dict[str, Any]]] = collections.defaultdict(list)
    for row in rows:
        grouped[str(row[key])].append(row)
    return {name: grouped_accuracy(grouped[name]) for name in sorted(grouped)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate Required-Grounding Precedence on fixed ToolFailBench traces."
    )
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--official-detect", required=True, type=Path)
    parser.add_argument("--config", required=True, type=Path)
    parser.add_argument("--rows-out", required=True, type=Path)
    parser.add_argument("--summary-out", required=True, type=Path)
    parser.add_argument("--cases-out", required=True, type=Path)
    return parser.parse_args()


def main() -> int:
    sys.dont_write_bytecode = True
    args = parse_args()
    config = load_json(args.config)
    manifest = load_json(args.manifest)
    if sha256_file(args.manifest) != config["development_manifest_sha256"]:
        raise ValueError("Development manifest does not match frozen config")
    if manifest["revision"] != config["dataset_revision"]:
        raise ValueError("dataset revision does not match frozen config")

    verified_files: list[dict[str, Any]] = []
    for entry in manifest["files"]:
        path = manifest_path(args.data_root, entry["path"])
        actual_bytes = path.stat().st_size
        actual_sha256 = sha256_file(path)
        if actual_bytes != entry["bytes"] or actual_sha256 != entry["sha256"]:
            raise ValueError(f"manifest verification failed: {entry['path']}")
        verified_files.append(
            {
                "path": entry["path"],
                "bytes": actual_bytes,
                "sha256": actual_sha256,
            }
        )

    official = load_official_module(
        args.official_detect, config["official_detect_sha256"]
    )
    supported = set(config["supported_labels"])
    passthrough = set(config["external_labels_passthrough"])
    trace_entries = [
        entry
        for entry in manifest["files"]
        if "/" not in entry["path"] and entry["path"].endswith(".json")
    ]
    judge_entries = [
        entry for entry in manifest["files"] if entry["path"].startswith("judge/")
    ]
    ensemble_entries = [
        entry
        for entry in manifest["files"]
        if entry["path"].startswith("judge_ensemble/")
    ]

    all_rows: list[dict[str, Any]] = []
    samples: list[dict[str, Any]] = []
    join_errors = 0
    baseline_identity_errors = 0
    unsupported_external_labels: collections.Counter[str] = collections.Counter()
    external_passthrough_count = 0

    for trace_entry in sorted(trace_entries, key=lambda item: item["path"]):
        trace_path = manifest_path(args.data_root, trace_entry["path"])
        traces = load_json(trace_path)
        if not isinstance(traces, list) or len(traces) != 1000:
            raise ValueError(f"trace file must contain exactly 1000 rows: {trace_path}")
        model_ids = {row["model_id"] for row in traces}
        if len(model_ids) != 1:
            raise ValueError(f"trace file contains multiple model IDs: {trace_path}")
        model_id = next(iter(model_ids))
        model_judges = sorted(
            [
                entry
                for entry in judge_entries
                if PurePosixPath(entry["path"]).name.startswith(model_id + "_judge_")
            ],
            key=lambda item: item["path"],
        )
        if len(model_judges) != 2:
            raise ValueError(f"expected two judge files for {model_id}")

        judge_maps: list[dict[str, dict[str, Any]]] = []
        for judge_entry in model_judges:
            judge_rows = load_json(manifest_path(args.data_root, judge_entry["path"]))
            if not isinstance(judge_rows, list) or len(judge_rows) != 1000:
                raise ValueError(
                    f"judge file must contain exactly 1000 rows: {judge_entry['path']}"
                )
            mapping = {row["task_id"]: row for row in judge_rows}
            if len(mapping) != 1000:
                raise ValueError(f"judge task IDs are not unique: {judge_entry['path']}")
            judge_maps.append(mapping)

        task_ids = [row["task"]["task_id"] for row in traces]
        if len(set(task_ids)) != 1000:
            raise ValueError(f"trace task IDs are not unique: {trace_path}")
        if set(task_ids) != set(judge_maps[0]) or set(task_ids) != set(judge_maps[1]):
            raise ValueError(f"trace/judge task IDs differ for {model_id}")

        for record in traces:
            task = record["task"]
            task_id = task["task_id"]
            judge_1 = judge_maps[0][task_id]
            judge_2 = judge_maps[1][task_id]
            for judge in (judge_1, judge_2):
                if (
                    judge["model_id"] != model_id
                    or judge["task_id"] != task_id
                    or judge["domain"] != task["domain"]
                    or judge["rule_based_classification"]
                    != record["classification"]
                ):
                    join_errors += 1

            released_label = record["classification"]
            recomputed_label = official.classify_failure_mode(
                task, record["agent_trace"], record["agent_answer"]
            )
            is_external = released_label not in supported
            if is_external:
                if released_label not in passthrough:
                    unsupported_external_labels[released_label] += 1
                external_passthrough_count += 1
                rgp_label = released_label
            else:
                if recomputed_label != released_label:
                    baseline_identity_errors += 1
                rgp_label = rgp_classify(
                    task, record["agent_trace"], record["agent_answer"], official
                )

            judge_1_label = judge_1["judge"]["failure_mode"]
            judge_2_label = judge_2["judge"]["failure_mode"]
            unanimous = (
                judge_1_label if judge_1_label == judge_2_label else None
            )
            tool_required = bool(
                task["evaluation_criteria"]["tool_must_be_called"]
            )
            expected_tool_called = bool(
                tool_required
                and not official.detect_tool_skip(task, record["agent_trace"])
            )
            required_satisfied = bool(
                official._answer_correct(task, record["agent_answer"])
            )
            fabrication_predicate = bool(
                tool_required
                and expected_tool_called
                and official.detect_output_fabrication(
                    task, record["agent_trace"], record["agent_answer"]
                )
            )
            changed = released_label != rgp_label
            correction = bool(
                unanimous is not None
                and released_label != unanimous
                and rgp_label == unanimous
            )
            regression = bool(
                unanimous is not None
                and released_label == unanimous
                and rgp_label != unanimous
            )
            row = {
                "model_id": model_id,
                "task_id": task_id,
                "domain": task["domain"],
                "official_label": released_label,
                "official_recomputed_label": recomputed_label,
                "rgp_label": rgp_label,
                "judge_1_label": judge_1_label,
                "judge_2_label": judge_2_label,
                "unanimous_label": unanimous,
                "tool_required": tool_required,
                "expected_tool_called": expected_tool_called,
                "required_satisfied": required_satisfied,
                "fabrication_predicate": fabrication_predicate,
                "external_release_label": is_external,
                "changed": changed,
                "correction": correction,
                "regression": regression,
                "trace_path": trace_entry["path"],
                "trace_sha256": trace_entry["sha256"],
                "judge_1_path": model_judges[0]["path"],
                "judge_1_sha256": model_judges[0]["sha256"],
                "judge_2_path": model_judges[1]["path"],
                "judge_2_sha256": model_judges[1]["sha256"],
                "task_json_sha256": canonical_sha256(task),
                "answer_sha256": hashlib.sha256(
                    record["agent_answer"].encode("utf-8")
                ).hexdigest(),
            }
            all_rows.append(row)
            if correction or regression:
                samples.append(
                    {
                        "kind": "correction" if correction else "regression",
                        "model_id": model_id,
                        "task_id": task_id,
                        "domain": task["domain"],
                        "official_label": released_label,
                        "rgp_label": rgp_label,
                        "judge_1_label": judge_1_label,
                        "judge_2_label": judge_2_label,
                        "agent_answer": record["agent_answer"],
                        "ground_truth": task["ground_truth"],
                        "mock_tool_return": task["mock_tool_return"],
                        "judge_1_reasoning": judge_1["judge"]["reasoning"],
                        "judge_2_reasoning": judge_2["judge"]["reasoning"],
                    }
                )

    all_rows.sort(key=lambda row: (row["model_id"], row["task_id"]))
    args.rows_out.parent.mkdir(parents=True, exist_ok=True)
    with args.rows_out.open("w", encoding="utf-8", newline="\n") as handle:
        for row in all_rows:
            handle.write(
                json.dumps(row, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
                + "\n"
            )

    unanimous_rows = [row for row in all_rows if row["unanimous_label"] is not None]
    truth = [row["unanimous_label"] for row in unanimous_rows]
    official_prediction = [row["official_label"] for row in unanimous_rows]
    rgp_prediction = [row["rgp_label"] for row in unanimous_rows]
    overall = grouped_accuracy(all_rows)
    corrections = sum(row["correction"] for row in all_rows)
    regressions = sum(row["regression"] for row in all_rows)
    per_model = per_group(all_rows, "model_id")
    per_domain = per_group(all_rows, "domain")
    bootstrap_config = config["bootstrap"]
    bootstrap = cluster_bootstrap(
        all_rows,
        resamples=bootstrap_config["resamples"],
        seed=bootstrap_config["seed"],
    )
    positive_models = sum(
        metrics["accuracy_delta"] > 0 for metrics in per_model.values()
    )
    positive_domains = sum(
        metrics["accuracy_delta"] > 0 for metrics in per_domain.values()
    )
    mechanism_rows = [
        row
        for row in all_rows
        if row["official_label"] == "output_fabrication"
        and row["rgp_label"] == "correct"
        and row["unanimous_label"] == "correct"
    ]
    mechanism_domains = sorted({row["domain"] for row in mechanism_rows})
    structural_violations = [
        row
        for row in all_rows
        if row["changed"]
        and (
            not row["tool_required"]
            or row["external_release_label"]
            or not row["expected_tool_called"]
            or not row["required_satisfied"]
        )
    ]
    gates = config["development_gates"]
    correction_ratio = corrections / regressions if regressions else None
    correction_margin_ok = (
        corrections > 0
        if regressions == 0
        else correction_ratio >= gates["minimum_corrections_per_regression"]
    )
    gate_checks = {
        "input_integrity": len(verified_files) == 40
        and len(trace_entries) == gates["expected_models"]
        and len(judge_entries) == 2 * gates["expected_models"]
        and len(ensemble_entries) == gates["expected_models"],
        "join_integrity": len(all_rows) == 10000 and join_errors == 0,
        "baseline_identity": baseline_identity_errors == 0
        and not unsupported_external_labels,
        "structural_invariance": not structural_violations,
        "primary_effect": overall["accuracy_delta"]
        >= gates["minimum_accuracy_delta"],
        "cluster_uncertainty": bootstrap["lower_95"]
        > gates["bootstrap_lower_bound_strictly_above"],
        "correction_margin": correction_margin_ok,
        "model_spread": positive_models >= gates["minimum_positive_models"],
        "domain_spread": positive_domains >= gates["minimum_positive_domains"],
        "mechanism_support": len(mechanism_rows)
        >= gates["minimum_supported_of_to_correct"]
        and len(mechanism_domains) >= gates["minimum_mechanism_domains"],
    }
    summary = {
        "schema_version": 1,
        "candidate_id": config["candidate_id"],
        "inputs": {
            "manifest_path": str(args.manifest),
            "manifest_sha256": sha256_file(args.manifest),
            "data_root": str(args.data_root),
            "official_detect_path": str(args.official_detect),
            "official_detect_sha256": sha256_file(args.official_detect),
            "config_path": str(args.config),
            "config_sha256": sha256_file(args.config),
            "verified_files": verified_files,
            "trace_files": len(trace_entries),
            "judge_files": len(judge_entries),
            "ensemble_files_verified_but_unused": len(ensemble_entries),
        },
        "integrity": {
            "rows": len(all_rows),
            "unanimous_rows": len(unanimous_rows),
            "judge_disagreement_rows": len(all_rows) - len(unanimous_rows),
            "join_errors": join_errors,
            "baseline_identity_errors": baseline_identity_errors,
            "external_passthrough_count": external_passthrough_count,
            "unsupported_external_labels": dict(
                sorted(unsupported_external_labels.items())
            ),
            "structural_invariance_violations": len(structural_violations),
        },
        "metrics": {
            "overall": overall,
            "official_macro_f1": macro_f1(truth, official_prediction),
            "rgp_macro_f1": macro_f1(truth, rgp_prediction),
            "macro_f1_delta": macro_f1(truth, rgp_prediction)
            - macro_f1(truth, official_prediction),
            "corrections": corrections,
            "regressions": regressions,
            "correction_to_regression_ratio": correction_ratio,
            "positive_models": positive_models,
            "positive_domains": positive_domains,
            "per_model": per_model,
            "per_domain": per_domain,
            "bootstrap": bootstrap,
            "mechanism_transition_count": len(mechanism_rows),
            "mechanism_domains": mechanism_domains,
            "official_to_unanimous": transition_counts(
                unanimous_rows, "official_label", "unanimous_label"
            ),
            "rgp_to_unanimous": transition_counts(
                unanimous_rows, "rgp_label", "unanimous_label"
            ),
            "official_to_rgp_all_rows": transition_counts(
                all_rows, "official_label", "rgp_label"
            ),
        },
        "gate_checks": gate_checks,
        "mechanical_gate_count": {
            "passed": sum(gate_checks.values()),
            "total": len(gate_checks),
        },
        "outputs": {
            "rows_path": str(args.rows_out),
            "rows_sha256": sha256_file(args.rows_out),
            "cases_path": str(args.cases_out),
        },
        "note": "Gate booleans are mechanical measurements; they do not authorize Confirmation or Delivery.",
    }

    limited_samples: list[dict[str, Any]] = []
    per_kind_limit = int(config["case_samples_per_kind"])
    for kind in ("correction", "regression"):
        selected = sorted(
            [sample for sample in samples if sample["kind"] == kind],
            key=lambda sample: (
                sample["model_id"],
                sample["domain"],
                sample["task_id"],
            ),
        )[:per_kind_limit]
        limited_samples.extend(selected)
    write_json(
        args.cases_out,
        {
            "schema_version": 1,
            "per_kind_limit": per_kind_limit,
            "samples": limited_samples,
        },
    )
    summary["outputs"]["cases_sha256"] = sha256_file(args.cases_out)
    write_json(args.summary_out, summary)

    print(f"rows={len(all_rows)}")
    print(f"unanimous_rows={len(unanimous_rows)}")
    print(f"accuracy_delta={overall['accuracy_delta']:.12f}")
    print(
        f"bootstrap_95=[{bootstrap['lower_95']:.12f},{bootstrap['upper_95']:.12f}]"
    )
    print(f"corrections={corrections} regressions={regressions}")
    print(
        f"positive_models={positive_models} positive_domains={positive_domains}"
    )
    print(
        f"mechanism_transitions={len(mechanism_rows)} "
        f"mechanism_domains={len(mechanism_domains)}"
    )
    print(
        "mechanical_gates="
        f"{sum(gate_checks.values())}/{len(gate_checks)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
