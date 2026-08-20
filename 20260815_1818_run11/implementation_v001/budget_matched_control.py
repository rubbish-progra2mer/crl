from __future__ import annotations

import argparse
import json
import math
import random
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from causal_uptake_eval import (
    atomic_write_text,
    canonicalize_case_answer,
    load_cases,
    normalize_answer,
    ollama_answer,
    prompt_for,
    relevant_relation_holds,
)


TRANSFORM_GROUP = (
    "base",
    "relevant",
    "irrelevant_plain",
    "irrelevant_adversarial",
    "order_only",
    "repeat_1",
)
REPEAT_CONTROL_GROUP = (
    "base",
    "repeat_1",
    "repeat_2",
    "repeat_3",
    "repeat_4",
    "repeat_5",
)
CALL_IDS = tuple(dict.fromkeys((*TRANSFORM_GROUP, *REPEAT_CONTROL_GROUP)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare the six-arm probe with an equal-budget six-repeat control."
    )
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", required=True, type=Path)
    parser.add_argument("--metrics-output", required=True, type=Path)
    parser.add_argument("--experiment-id", default="scratch-budget-matched-control")
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--prompt-regimes", nargs="+", default=["weak", "strict"])
    parser.add_argument("--seeds", nargs="+", type=int, required=True)
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    return parser.parse_args()


def source_variant(call_id: str) -> str:
    return "base" if call_id.startswith("repeat_") else call_id


def build_row(
    *,
    case: dict[str, Any],
    agent_id: str,
    experiment_seed: int,
    answers: dict[str, str],
    calls: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    if set(answers) != set(CALL_IDS):
        raise ValueError("answers must contain exactly the ten predeclared call ids")
    base = answers["base"]
    transform_pass = (
        relevant_relation_holds(case, base, answers["relevant"])
        and answers["irrelevant_plain"] == base
        and answers["irrelevant_adversarial"] == base
        and answers["order_only"] == base
        and answers["repeat_1"] == base
    )
    repeat_control_pass = all(answers[call_id] == base for call_id in REPEAT_CONTROL_GROUP)
    expected = {
        key: normalize_answer(value) for key, value in case["expected"].items()
    }
    transform_exact = (
        answers["base"] == expected["base"]
        and answers["relevant"] == expected["relevant"]
        and answers["irrelevant_plain"] == expected["irrelevant_plain"]
        and answers["irrelevant_adversarial"] == expected["irrelevant_adversarial"]
        and answers["order_only"] == expected["order_only"]
        and answers["repeat_1"] == expected["base"]
    )
    repeat_control_exact = all(
        answers[call_id] == expected["base"] for call_id in REPEAT_CONTROL_GROUP
    )
    return {
        "case_id": case["case_id"],
        "family": case.get("family", "unspecified"),
        "agent_id": agent_id,
        "experiment_seed": experiment_seed,
        "answers": answers,
        "expected_relation_anchors": expected,
        "metrics": {
            "base_correct": answers["base"] == expected["base"],
            "transform_pass": transform_pass,
            "repeat_control_pass": repeat_control_pass,
            "transform_fail": not transform_pass,
            "repeat_control_fail": not repeat_control_pass,
            "transform_exact": transform_exact,
            "repeat_control_exact": repeat_control_exact,
        },
        "calls": calls,
        "warnings": warnings,
    }


def exact_mcnemar_pvalue(transform_only: int, control_only: int) -> float:
    discordant = transform_only + control_only
    if discordant == 0:
        return 1.0
    tail = min(transform_only, control_only)
    probability = sum(
        math.comb(discordant, index) for index in range(tail + 1)
    ) / (2**discordant)
    return min(1.0, 2.0 * probability)


def paired_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = [row for row in rows if row["metrics"]["base_correct"]]
    counts = {
        "both_pass": 0,
        "transform_only_fail": 0,
        "control_only_fail": 0,
        "both_fail": 0,
    }
    for row in eligible:
        transform_fail = bool(row["metrics"]["transform_fail"])
        control_fail = bool(row["metrics"]["repeat_control_fail"])
        if transform_fail and control_fail:
            counts["both_fail"] += 1
        elif transform_fail:
            counts["transform_only_fail"] += 1
        elif control_fail:
            counts["control_only_fail"] += 1
        else:
            counts["both_pass"] += 1
    n = len(eligible)
    transform_failures = counts["transform_only_fail"] + counts["both_fail"]
    control_failures = counts["control_only_fail"] + counts["both_fail"]
    return {
        "n_all": len(rows),
        "n_base_correct": n,
        **counts,
        "transform_failure_rate": transform_failures / n if n else None,
        "repeat_control_failure_rate": control_failures / n if n else None,
        "excess_failure_rate": (
            (counts["transform_only_fail"] - counts["control_only_fail"]) / n
            if n
            else None
        ),
        "exact_mcnemar_pvalue": exact_mcnemar_pvalue(
            counts["transform_only_fail"], counts["control_only_fail"]
        ),
    }


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_seed: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_agent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    clean_rows = [row for row in rows if not row["warnings"]]
    for row in rows:
        by_seed[str(row["experiment_seed"])].append(row)
        by_agent[row["agent_id"]].append(row)
    seed_summaries = {key: paired_summary(value) for key, value in by_seed.items()}
    agent_summaries = {key: paired_summary(value) for key, value in by_agent.items()}
    positive_seed_count = sum(
        summary["excess_failure_rate"] is not None
        and summary["excess_failure_rate"] > 0
        for summary in seed_summaries.values()
    )
    positive_stratum_count = sum(
        summary["excess_failure_rate"] is not None
        and summary["excess_failure_rate"] > 0
        for summary in agent_summaries.values()
    )
    return {
        "overall": paired_summary(rows),
        "parse_warning_excluded": paired_summary(clean_rows),
        "by_seed": seed_summaries,
        "by_agent": agent_summaries,
        "positive_seed_count": positive_seed_count,
        "positive_stratum_count": positive_stratum_count,
    }


def metrics_payload(
    *,
    experiment_id: str,
    result_aggregate: dict[str, Any],
    resource_usage: dict[str, Any],
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    overall = result_aggregate["overall"]
    primary = overall["excess_failure_rate"]
    return {
        "schema_version": 1,
        "experiment_id": experiment_id,
        "records": [
            {
                "name": "budget_matched_excess_failure_rate",
                "value": primary if primary is not None else 0.0,
                "unit": "ratio",
                "split": "base_correct_rows",
                "aggregation": "paired_risk_difference",
                "n": overall["n_base_correct"],
            },
            {
                "name": "transform_failure_rate",
                "value": overall["transform_failure_rate"] or 0.0,
                "unit": "ratio",
                "split": "base_correct_rows",
                "aggregation": "mean",
                "n": overall["n_base_correct"],
            },
            {
                "name": "repeat_control_failure_rate",
                "value": overall["repeat_control_failure_rate"] or 0.0,
                "unit": "ratio",
                "split": "base_correct_rows",
                "aggregation": "mean",
                "n": overall["n_base_correct"],
            },
            {
                "name": "exact_mcnemar_pvalue",
                "value": overall["exact_mcnemar_pvalue"],
                "unit": "probability",
                "split": "base_correct_rows",
                "aggregation": "exact_two_sided",
                "n": overall["transform_only_fail"] + overall["control_only_fail"],
            },
        ],
        "resource_usage": resource_usage,
        "errors": errors,
        "warnings": warnings,
    }


def render_report(result: dict[str, Any]) -> str:
    aggregate_data = result["aggregate"]
    overall = aggregate_data["overall"]
    clean = aggregate_data["parse_warning_excluded"]
    lines = [
        "# 同预算六重重放对照结果",
        "",
        f"- 行数：{len(result['rows'])}",
        f"- 调用数：{result['resource_usage']['api_calls']}",
        f"- 基线正确行：{overall['n_base_correct']}",
        f"- 六臂失败率：{overall['transform_failure_rate']}",
        f"- 六重放失败率：{overall['repeat_control_failure_rate']}",
        f"- 配对超额失败率：{overall['excess_failure_rate']}",
        f"- 精确 McNemar 双侧 p 值：{overall['exact_mcnemar_pvalue']}",
        f"- 仅六臂失败 / 仅重放失败 / 两者都失败：{overall['transform_only_fail']} / {overall['control_only_fail']} / {overall['both_fail']}",
        f"- 剔除解析警告后的配对超额失败率：{clean['excess_failure_rate']}",
        f"- 正超额种子数 / 分层数：{aggregate_data['positive_seed_count']} / {aggregate_data['positive_stratum_count']}",
        "",
        "## 按种子",
        "",
        "| 种子 | 基线正确 n | 六臂失败率 | 六重放失败率 | 超额失败率 |",
        "|---|---:|---:|---:|---:|",
    ]
    for seed, summary in aggregate_data["by_seed"].items():
        lines.append(
            f"| {seed} | {summary['n_base_correct']} | {summary['transform_failure_rate']} | "
            f"{summary['repeat_control_failure_rate']} | {summary['excess_failure_rate']} |"
        )
    lines.extend(
        [
            "",
            "> 这是同一模型、提示、种子与案例内的配对预算对照；它检验干预特异的额外失败，不认证真实证据采用机制或外部有效性。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    cases = load_cases(args.cases)
    started = time.perf_counter()
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    api_calls = 0

    for model in args.models:
        for regime in args.prompt_regimes:
            for experiment_seed in args.seeds:
                agent_id = f"ollama::{model}::{regime}::seed-{experiment_seed}"
                for case in cases:
                    answers: dict[str, str] = {}
                    call_records: list[dict[str, Any]] = []
                    row_warnings: list[str] = []
                    call_order = list(CALL_IDS)
                    order_rng = random.Random(
                        f"budget-control-v001:{experiment_seed}:{model}:{regime}:{case['case_id']}"
                    )
                    order_rng.shuffle(call_order)
                    for call_id in call_order:
                        variant = source_variant(call_id)
                        try:
                            parsed_answer, usage, parse_warning, raw_content = ollama_answer(
                                url=args.ollama_url,
                                model=model,
                                messages=prompt_for(case, variant, regime),
                                temperature=args.temperature,
                                seed=experiment_seed,
                                timeout_seconds=args.timeout_seconds,
                            )
                            answer = canonicalize_case_answer(case, parsed_answer)
                            answers[call_id] = answer
                            api_calls += 1
                            prompt_count = usage.get("prompt_eval_count")
                            completion_count = usage.get("eval_count")
                            if isinstance(prompt_count, int):
                                total_prompt_tokens += prompt_count
                            if isinstance(completion_count, int):
                                total_completion_tokens += completion_count
                            call_records.append(
                                {
                                    "call_id": call_id,
                                    "source_variant": variant,
                                    "call_position": len(call_records),
                                    "experiment_seed": experiment_seed,
                                    "parsed_answer": parsed_answer,
                                    "canonicalization_applied": answer != parsed_answer,
                                    "usage": usage,
                                    "raw_content": raw_content,
                                }
                            )
                            if parse_warning:
                                warning = f"{call_id}: {parse_warning}"
                                row_warnings.append(warning)
                                warnings.append(f"{agent_id}/{case['case_id']}/{warning}")
                        except Exception as exc:
                            message = (
                                f"{agent_id}/{case['case_id']}/{call_id}: "
                                f"{type(exc).__name__}: {exc}"
                            )
                            errors.append(message)
                            answers[call_id] = ""
                            call_records.append(
                                {
                                    "call_id": call_id,
                                    "source_variant": variant,
                                    "call_position": len(call_records),
                                    "experiment_seed": experiment_seed,
                                    "error": message,
                                }
                            )
                    rows.append(
                        build_row(
                            case=case,
                            agent_id=agent_id,
                            experiment_seed=experiment_seed,
                            answers=answers,
                            calls=call_records,
                            warnings=row_warnings,
                        )
                    )

    wall_time = time.perf_counter() - started
    aggregate_data = aggregate(rows)
    resource_usage = {
        "tokens": total_prompt_tokens + total_completion_tokens,
        "api_calls": api_calls,
        "wall_time_seconds": wall_time,
        "gpu_time_seconds": "unknown",
        "estimated_cost": 0.0,
    }
    result = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "configuration": {
            "models": args.models,
            "prompt_regimes": args.prompt_regimes,
            "seeds": args.seeds,
            "temperature": args.temperature,
            "transform_group": list(TRANSFORM_GROUP),
            "repeat_control_group": list(REPEAT_CONTROL_GROUP),
            "call_ids": list(CALL_IDS),
            "randomized_call_order": True,
        },
        "case_count": len(cases),
        "rows": rows,
        "aggregate": aggregate_data,
        "resource_usage": resource_usage,
        "errors": errors,
        "warnings": warnings,
    }
    atomic_write_text(args.output, json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    atomic_write_text(args.report_output, render_report(result))
    atomic_write_text(
        args.metrics_output,
        json.dumps(
            metrics_payload(
                experiment_id=args.experiment_id,
                result_aggregate=aggregate_data,
                resource_usage=resource_usage,
                errors=errors,
                warnings=warnings,
            ),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )
    print(
        json.dumps(
            {
                "row_count": len(rows),
                "api_calls": api_calls,
                "errors": len(errors),
                "excess_failure_rate": aggregate_data["overall"]["excess_failure_rate"],
                "output": str(args.output),
            },
            ensure_ascii=False,
        )
    )
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())
