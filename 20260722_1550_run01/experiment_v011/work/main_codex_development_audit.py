from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

import numpy as np


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def stable_ranking(names: list[str], scores: list[float]) -> list[str]:
    return [
        names[index]
        for index in sorted(
            range(len(names)),
            key=lambda index: (
                -float(scores[index]),
                hashlib.sha256(names[index].encode("utf-8")).hexdigest(),
            ),
        )
    ]


def metrics(
    rankings: list[list[str]], gold_sets: list[set[str]]
) -> tuple[np.ndarray, np.ndarray]:
    top1 = []
    reciprocal_rank = []
    for ranking, gold in zip(rankings, gold_sets):
        ranks = [ranking.index(name) + 1 for name in gold if name in ranking]
        best = min(ranks) if ranks else len(ranking) + 1
        top1.append(float(best == 1))
        reciprocal_rank.append(1.0 / best)
    return np.asarray(top1), np.asarray(reciprocal_rank)


def bootstrap(values: np.ndarray, repeats: int, seed: int) -> list[float]:
    generator = np.random.default_rng(seed)
    means = np.empty(repeats, dtype=np.float64)
    for start in range(0, repeats, 1000):
        count = min(1000, repeats - start)
        indices = generator.integers(0, len(values), size=(count, len(values)))
        means[start : start + count] = values[indices].mean(axis=1)
    return [float(np.quantile(means, 0.025)), float(np.quantile(means, 0.975))]


def close(left: object, right: object, tolerance: float = 1e-12) -> bool:
    return abs(float(left) - float(right)) <= tolerance


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--raw", required=True)
    parser.add_argument("--summary", required=True)
    parser.add_argument("--selected", required=True)
    parser.add_argument("--query-hashes", required=True)
    parser.add_argument("--execution", required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    paths = {
        "raw": Path(args.raw).resolve(),
        "summary": Path(args.summary).resolve(),
        "selected": Path(args.selected).resolve(),
        "query_hashes": Path(args.query_hashes).resolve(),
        "execution": Path(args.execution).resolve(),
    }
    rows = [
        json.loads(line)
        for line in paths["raw"].read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    summary = json.loads(paths["summary"].read_text(encoding="utf-8"))
    selected = json.loads(paths["selected"].read_text(encoding="utf-8"))
    query_hashes = json.loads(paths["query_hashes"].read_text(encoding="utf-8"))
    execution = json.loads(paths["execution"].read_text(encoding="utf-8"))

    methods = (
        "cross_encoder",
        "unanchored_related_adapter",
        "thin_anchor_adapter",
    )
    score_keys = {
        "cross_encoder": "cross_encoder_logit",
        "unanchored_related_adapter": "unanchored_score",
        "thin_anchor_adapter": "anchored_score",
    }
    rankings: dict[str, list[list[str]]] = {method: [] for method in methods}
    recorded_ranking_matches: dict[str, bool] = {method: True for method in methods}
    gold_sets: list[set[str]] = []
    vector_dimensions: set[int] = set()
    row_ids: list[str] = []
    observed_hashes: list[str] = []
    tool_count = 0
    score_changed_rows = {
        "unanchored_related_adapter": 0,
        "thin_anchor_adapter": 0,
    }
    ranking_changed_rows = {
        "unanchored_related_adapter": 0,
        "thin_anchor_adapter": 0,
    }
    for row in rows:
        row_ids.append(str(row["id"]))
        observed_hashes.append(str(row["query_sha256"]))
        gold_sets.append(set(row["gold"]))
        names = [tool["name"] for tool in row["tools"]]
        tool_count += len(names)
        for tool in row["tools"]:
            vector_dimensions.add(len(tool["cls_vector"]))
        for method in methods:
            recomputed = stable_ranking(
                names, [tool[score_keys[method]] for tool in row["tools"]]
            )
            rankings[method].append(recomputed)
            if recomputed != row["rankings"][method]:
                recorded_ranking_matches[method] = False
        baseline_scores = np.asarray(
            [tool["cross_encoder_logit"] for tool in row["tools"]]
        )
        for method, key in (
            ("unanchored_related_adapter", "unanchored_score"),
            ("thin_anchor_adapter", "anchored_score"),
        ):
            learned_scores = np.asarray([tool[key] for tool in row["tools"]])
            if not np.array_equal(learned_scores, baseline_scores):
                score_changed_rows[method] += 1
            if rankings[method][-1] != rankings["cross_encoder"][-1]:
                ranking_changed_rows[method] += 1

    metric_arrays: dict[str, tuple[np.ndarray, np.ndarray]] = {
        method: metrics(rankings[method], gold_sets) for method in methods
    }
    recomputed_metrics = {
        method: {
            "accuracy": float(values[0].mean()),
            "mrr": float(values[1].mean()),
        }
        for method, values in metric_arrays.items()
    }
    metric_matches = {
        method: all(
            close(recomputed_metrics[method][name], summary["metrics"][method][name])
            for name in ("accuracy", "mrr")
        )
        for method in methods
    }
    comparisons: dict[str, dict[str, object]] = {}
    for method, summary_key, seed in (
        ("unanchored_related_adapter", "unanchored_minus_cross_encoder", 20260733),
        ("thin_anchor_adapter", "thin_anchor_minus_cross_encoder", 20260723),
    ):
        top1_delta = (
            metric_arrays[method][0] - metric_arrays["cross_encoder"][0]
        )
        mrr_delta = metric_arrays[method][1] - metric_arrays["cross_encoder"][1]
        recomputed = {
            "accuracy": float(top1_delta.mean()),
            "mrr": float(mrr_delta.mean()),
            "accuracy_bootstrap_95": bootstrap(top1_delta, 20000, seed),
            "mrr_bootstrap_95": bootstrap(mrr_delta, 20000, seed + 1),
            "corrections": int(np.sum(top1_delta == 1.0)),
            "regressions": int(np.sum(top1_delta == -1.0)),
        }
        recorded = summary[summary_key]
        matches = (
            close(recomputed["accuracy"], recorded["accuracy"])
            and close(recomputed["mrr"], recorded["mrr"])
            and recomputed["corrections"] == recorded["corrections"]
            and recomputed["regressions"] == recorded["regressions"]
            and all(
                close(left, right)
                for left, right in zip(
                    recomputed["accuracy_bootstrap_95"],
                    recorded["accuracy_bootstrap_95"],
                )
            )
            and all(
                close(left, right)
                for left, right in zip(
                    recomputed["mrr_bootstrap_95"],
                    recorded["mrr_bootstrap_95"],
                )
            )
        )
        comparisons[method] = {"recomputed": recomputed, "matches_summary": matches}

    execution_outputs = {
        Path(record["path"]).name: record["after"]
        for record in execution["outputs"]
    }
    capture_hash_matches = {
        "raw": sha256_file(paths["raw"]) == execution_outputs["raw.jsonl"]["sha256"],
        "summary": sha256_file(paths["summary"])
        == execution_outputs["summary.json"]["sha256"],
        "selected": sha256_file(paths["selected"])
        == execution_outputs["selected_params.json"]["sha256"],
        "query_hashes": sha256_file(paths["query_hashes"])
        == execution_outputs["query_hashes.json"]["sha256"],
    }
    adapter = selected["adapter"]
    unanchored = np.asarray(adapter["unanchored_vector"], dtype=np.float64)
    anchored = np.asarray(adapter["anchored_vector"], dtype=np.float64)
    anchor_scale = float(adapter["anchor_scale"])
    full_adapter_relation_max_error = float(
        np.max(np.abs(anchored - anchor_scale * unanchored))
    )
    folds = selected["folds"]
    fold_rows = sum(int(record["heldout_rows"]) for record in folds)
    report = {
        "audit_kind": "main_codex_independent_raw_recomputation",
        "scientific_capture_exit_code": execution["exit_code"],
        "scientific_capture_duration_seconds": execution["duration_seconds"],
        "rows": len(rows),
        "unique_row_ids": len(set(row_ids)),
        "tools": tool_count,
        "vector_dimensions": sorted(vector_dimensions),
        "query_hashes_match": sorted(observed_hashes) == query_hashes,
        "recorded_ranking_matches": recorded_ranking_matches,
        "recomputed_metrics": recomputed_metrics,
        "metric_matches_summary": metric_matches,
        "comparisons": comparisons,
        "score_changed_rows": score_changed_rows,
        "ranking_changed_rows": ranking_changed_rows,
        "capture_hash_matches": capture_hash_matches,
        "fold_count": len(folds),
        "heldout_rows_total": fold_rows,
        "fold_anchor_scales": [record["anchor_scale"] for record in folds],
        "full_anchor_scale": anchor_scale,
        "full_adapter_relation_max_error": full_adapter_relation_max_error,
        "all_gates_passed_recorded": summary["all_gates_passed"],
        "all_checks_passed": (
            execution["exit_code"] == 0
            and len(rows) == 200
            and len(set(row_ids)) == 200
            and tool_count == 1121
            and vector_dimensions == {384}
            and sorted(observed_hashes) == query_hashes
            and all(recorded_ranking_matches.values())
            and all(metric_matches.values())
            and all(record["matches_summary"] for record in comparisons.values())
            and all(capture_hash_matches.values())
            and len(folds) == 5
            and fold_rows == 200
            and full_adapter_relation_max_error <= 1e-12
        ),
        "source_sha256": {name: sha256_file(path) for name, path in paths.items()},
    }
    Path(args.output).resolve().write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    print(
        json.dumps(
            {
                "all_checks_passed": report["all_checks_passed"],
                "rows": report["rows"],
                "tools": report["tools"],
                "candidate_top1": recomputed_metrics["thin_anchor_adapter"][
                    "accuracy"
                ],
                "candidate_ranking_changes": ranking_changed_rows[
                    "thin_anchor_adapter"
                ],
            },
            sort_keys=True,
        )
    )
    return 0 if report["all_checks_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
