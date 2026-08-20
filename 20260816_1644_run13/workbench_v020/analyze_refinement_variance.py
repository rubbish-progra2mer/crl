"""Analyze the v020 independent-implementation refinement probe."""
from __future__ import annotations

import json
import math
from collections import defaultdict
from pathlib import Path

import numpy as np


ROOT = Path(__file__).resolve().parent
RECORDS_PATH = ROOT / "refinement_variance_runs" / "records.json"
OUT_JSON = ROOT / "refinement_variance_analysis.json"
OUT_MD = ROOT / "refinement_variance_report.md"
CONTROL_ID = "uniform_random"


def finite_score(record):
    score = record.get("score")
    if score is None:
        return None
    score = float(score)
    return score if math.isfinite(score) else None


def average_ranks(values):
    values = np.asarray(values, dtype=float)
    order = np.argsort(values, kind="mergesort")
    ranks = np.empty(len(values), dtype=float)
    start = 0
    while start < len(values):
        end = start + 1
        while end < len(values) and values[order[end]] == values[order[start]]:
            end += 1
        ranks[order[start:end]] = (start + 1 + end) / 2.0
        start = end
    return ranks


def spearman(x, y):
    rx = average_ranks(x)
    ry = average_ranks(y)
    if np.std(rx) == 0 or np.std(ry) == 0:
        return None
    return float(np.corrcoef(rx, ry)[0, 1])


def wilson_interval(successes, n, z=1.96):
    if n == 0:
        return [None, None]
    p = successes / n
    denom = 1 + z * z / n
    center = (p + z * z / (2 * n)) / denom
    radius = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [center - radius, center + radius]


def icc_oneway(matrix):
    array = np.asarray(matrix, dtype=float)
    groups, repeats = array.shape
    group_means = array.mean(axis=1)
    grand = array.mean()
    ss_between = repeats * np.sum((group_means - grand) ** 2)
    ss_within = np.sum((array - group_means[:, None]) ** 2)
    ms_between = ss_between / (groups - 1)
    ms_within = ss_within / (groups * (repeats - 1))
    denom = ms_between + (repeats - 1) * ms_within
    icc = (ms_between - ms_within) / denom if denom else None
    return {
        "ms_between": float(ms_between),
        "ms_within": float(ms_within),
        "icc": float(icc) if icc is not None else None,
    }


def main():
    records = json.loads(RECORDS_PATH.read_text(encoding="utf-8"))
    groups = defaultdict(list)
    for record in records:
        groups[(record["model"], record["idea_id"])].append(record)
    for rows in groups.values():
        rows.sort(key=lambda row: int(row["replicate"]))

    control_scores = [
        finite_score(record)
        for record in records
        if record["idea_id"] == CONTROL_ID and finite_score(record) is not None
    ]
    control = float(np.median(control_scores))

    group_rows = []
    recoveries = []
    for (model, idea_id), rows in sorted(groups.items()):
        scores = [finite_score(row) for row in rows]
        finite = [score for score in scores if score is not None]
        first = scores[0]
        later = [score for score in scores[1:] if score is not None]
        later_best = min(later) if later else None
        oracle_best = min(finite) if finite else None
        first_rejected = first is None or first > control
        later_beats_control = later_best is not None and later_best < control
        recoverable_rejection = (
            idea_id != CONTROL_ID and first_rejected and later_beats_control
        )
        if idea_id != CONTROL_ID:
            recoveries.append(recoverable_rejection)
        group_rows.append(
            {
                "model": model,
                "idea_id": idea_id,
                "scores": scores,
                "finite_count": len(finite),
                "finite_mean": float(np.mean(finite)) if finite else None,
                "finite_sd": float(np.std(finite, ddof=1)) if len(finite) > 1 else None,
                "finite_range": float(max(finite) - min(finite)) if len(finite) > 1 else None,
                "first_score": first,
                "later_best": later_best,
                "oracle_best": oracle_best,
                "first_rejected": first_rejected,
                "later_beats_control": later_beats_control,
                "recoverable_rejection": recoverable_rejection,
                "unique_code_hashes": len({row.get("code_sha256") for row in rows}),
                "n_error_replicates": sum(
                    (row.get("n_errors") or 0) > 0 or finite_score(row) is None
                    for row in rows
                ),
            }
        )

    sensitivity = {}
    for cap in (3.0, 4.0, 6.0):
        matrix = []
        rank_rows = []
        for row in group_rows:
            capped = [score if score is not None else cap for score in row["scores"]]
            capped = [min(score, cap) for score in capped]
            matrix.append(capped)
        for model in sorted({row["model"] for row in group_rows}):
            model_rows = [
                row for row in group_rows
                if row["model"] == model and row["idea_id"] != CONTROL_ID
            ]
            first = [
                min(row["first_score"], cap) if row["first_score"] is not None else cap
                for row in model_rows
            ]
            oracle = [
                min(row["oracle_best"], cap) if row["oracle_best"] is not None else cap
                for row in model_rows
            ]
            rank_rows.append(
                {
                    "model": model,
                    "spearman_first_vs_best_of_3": spearman(first, oracle),
                    "first": first,
                    "best_of_3": oracle,
                }
            )
        sensitivity[str(cap)] = {
            "variance_components": icc_oneway(matrix),
            "rank_stability": rank_rows,
        }

    finite_ranges = [
        row["finite_range"] for row in group_rows
        if row["idea_id"] != CONTROL_ID and row["finite_range"] is not None
    ]
    recover_count = int(sum(recoveries))
    recover_n = len(recoveries)
    result = {
        "n_records": len(records),
        "n_groups": len(group_rows),
        "models": sorted({record["model"] for record in records}),
        "control_mean_log_gap": control,
        "finite_scores": sum(finite_score(record) is not None for record in records),
        "infinite_or_missing_scores": sum(finite_score(record) is None for record in records),
        "records_with_runtime_errors": sum((record.get("n_errors") or 0) > 0 for record in records),
        "recoverable_first_rejections": recover_count,
        "noncontrol_groups": recover_n,
        "recoverable_first_rejection_rate": recover_count / recover_n,
        "recoverable_first_rejection_wilson95": wilson_interval(recover_count, recover_n),
        "median_within_group_finite_range": float(np.median(finite_ranges)),
        "group_rows": group_rows,
        "penalty_cap_sensitivity": sensitivity,
        "platform_note": (
            "The released POSIX SIGALRM driver was replaced by a Windows-compatible "
            "driver preserving suite, seeds, FEval budget, and score formula; a whole-"
            "suite subprocess timeout replaced per-tuple alarms."
        ),
    }
    OUT_JSON.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    lines = [
        "# v020 独立实现方差探针报告",
        "",
        f"- 记录数：{len(records)}；模型—构想组：{len(group_rows)}；每组 3 次独立实现。",
        f"- 均匀随机控制分数：`{control:.6f}`（越低越好）。",
        f"- 有限分数：{result['finite_scores']}/{len(records)}；无穷或缺失：{result['infinite_or_missing_scores']}/{len(records)}。",
        (
            f"- 非控制构想中，首次被控制门槛淘汰、但后两次至少一次反超控制："
            f"{recover_count}/{recover_n} = {recover_count / recover_n:.1%}；"
            f"Wilson 95% 区间 {result['recoverable_first_rejection_wilson95'][0]:.1%}–"
            f"{result['recoverable_first_rejection_wilson95'][1]:.1%}。"
        ),
        f"- 有至少两个有限实现的非控制组，其组内极差中位数：`{np.median(finite_ranges):.6f}`。",
        "",
        "## 分组结果",
        "",
        "| 模型 | 固定构想 | 三次分数 | 首次错杀后恢复 | 有限实现极差 |",
        "|---|---|---:|---:|---:|",
    ]
    for row in group_rows:
        score_text = ", ".join("NA" if score is None else f"{score:.6f}" for score in row["scores"])
        range_text = "NA" if row["finite_range"] is None else f"{row['finite_range']:.6f}"
        lines.append(
            f"| {row['model']} | {row['idea_id']} | {score_text} | "
            f"{'是' if row['recoverable_rejection'] else '否'} | {range_text} |"
        )
    lines.extend(["", "## 惩罚上限敏感性", ""])
    for cap, values in sensitivity.items():
        variance = values["variance_components"]
        lines.append(
            f"- 无效实现记为 `{cap}`：组间均方 `{variance['ms_between']:.4f}`，"
            f"组内均方 `{variance['ms_within']:.4f}`，单次实现组内相关系数 "
            f"`{variance['icc']:.4f}`。"
        )
        for rank in values["rank_stability"]:
            lines.append(
                f"  - {rank['model']} 首次分数与三次最佳分数的斯皮尔曼相关："
                f"`{rank['spearman_first_vs_best_of_3']:.4f}`。"
            )
    lines.extend(
        [
            "",
            "## 边界",
            "",
            "- 这是两个本地小模型、一个 CPU 黑箱优化探针，不足以证明前沿研究智能体上的普遍效应。",
            "- 三次独立实现是“可精炼性”的代理，不等同于沿同一代码分支持续修订。",
            "- 公开驱动的 POSIX 单例闹钟在 Windows 不可用；本地适配保留任务、随机种子、函数评估预算和计分公式，以整套进程超时替代单例闹钟。",
            "- 该结果只支持继续研究首次实现噪声与资源分配，不支持任何方法优越性结论。",
            "",
        ]
    )
    OUT_MD.write_text("\n".join(lines), encoding="utf-8", newline="\n")
    print(json.dumps({key: result[key] for key in (
        "n_records",
        "finite_scores",
        "infinite_or_missing_scores",
        "recoverable_first_rejections",
        "noncontrol_groups",
        "recoverable_first_rejection_rate",
        "median_within_group_finite_range",
    )}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
