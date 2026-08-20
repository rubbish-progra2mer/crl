"""CRL 科研搜索奖励校准的纯计算内核。

本模块只服务于 Run 外的机器校准实验。它不会读取或改变 CRL 候选状态，
不会认证新颖性，也不会形成 Delivery 或 No-Delivery。
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

import numpy as np


CALIBRATION_SCHEMA_VERSION = 1
CALIBRATION_ARMS = ("heuristic", "naive_scalar", "constrained_reward")
CALIBRATION_PHASES = ("preflight", "pilot", "confirm", "temporal", "report")
TAU2_DOMAINS = ("mock", "airline", "retail", "telecom")
LOW_FIDELITY_COUNTS = {"airline": 8, "retail": 8, "telecom": 8}
HIGH_FIDELITY_COUNTS = {"airline": 20, "retail": 28, "telecom": 48}
COMPLETED_STATUS = "completed"
MECHANICAL_STATUSES = {
    "infra_failure",
    "runner_failure",
    "timeout",
    "invalid_output",
}


def build_frozen_task_split(
    tau2_root: str | Path, *, seed: int = 20260819
) -> dict[str, Any]:
    """从 τ² v1.0.1 任务文件构造确定、分层且互斥的任务划分。"""

    root = Path(tau2_root)
    task_sets: dict[str, list[dict[str, Any]]] = {}
    source_hashes: dict[str, str] = {}
    source_split_hashes: dict[str, str] = {}
    for domain in TAU2_DOMAINS:
        path = root / "data" / "tau2" / "domains" / domain / "tasks.json"
        tasks, source_hash = _load_tau2_tasks(path, domain)
        base_ids, split_hash = _load_tau2_base_ids(path.parent / "split_tasks.json", domain)
        tasks_by_id = {str(task["id"]): task for task in tasks}
        missing = set(base_ids) - set(tasks_by_id)
        if missing:
            raise ValueError(f"τ² {domain} base split refers to missing tasks: {sorted(missing)}")
        task_sets[domain] = [tasks_by_id[task_id] for task_id in base_ids]
        source_hashes[domain] = source_hash
        source_split_hashes[domain] = split_hash

    smoke = sorted(
        (_task_fact("mock", task) for task in task_sets["mock"]),
        key=lambda item: _natural_identifier_key(item["task_id"]),
    )
    if len(smoke) != 10:
        raise ValueError(f"τ² mock task count must be 10, got {len(smoke)}")

    low: dict[str, list[dict[str, Any]]] = {}
    high: dict[str, list[dict[str, Any]]] = {}
    for domain in ("airline", "retail", "telecom"):
        facts = [_task_fact(domain, task) for task in task_sets[domain]]
        low[domain] = _stratified_task_sample(
            facts,
            LOW_FIDELITY_COUNTS[domain],
            seed=seed,
            salt=f"{domain}:low",
        )
        low_ids = {item["task_id"] for item in low[domain]}
        remaining = [item for item in facts if item["task_id"] not in low_ids]
        high[domain] = _stratified_task_sample(
            remaining,
            HIGH_FIDELITY_COUNTS[domain],
            seed=seed,
            salt=f"{domain}:high",
        )

    split = {
        "schema_version": CALIBRATION_SCHEMA_VERSION,
        "benchmark": {"name": "tau2-bench", "version": "1.0.1"},
        "seed": seed,
        "stratification": {
            "field": "evaluation_criteria.actions count",
            "bins": ["zero", "one_two", "three_five", "six_plus"],
            "selection": "proportional largest remainder then stable SHA-256 order",
        },
        "source_task_sha256": source_hashes,
        "source_split_sha256": source_split_hashes,
        "smoke": {"mock": smoke},
        "low_fidelity": low,
        "high_fidelity": high,
        "repetitions": {"smoke": 1, "low_fidelity": 1, "high_fidelity": 3},
    }
    validate_frozen_task_split(split)
    split["split_sha256"] = _canonical_sha256(split)
    return split


def validate_frozen_task_split(value: Mapping[str, Any]) -> None:
    """核验冻结划分的数量、唯一性、互斥性和自散列。"""

    if value.get("schema_version") != CALIBRATION_SCHEMA_VERSION:
        raise ValueError("unsupported calibration task-split schema")
    benchmark = value.get("benchmark")
    if not isinstance(benchmark, Mapping) or benchmark.get("version") != "1.0.1":
        raise ValueError("task split must bind tau2-bench v1.0.1")
    smoke = _task_list(value, "smoke", "mock")
    if len(smoke) != 10:
        raise ValueError("smoke split must contain all 10 mock tasks")
    _require_unique_task_ids(smoke, "smoke/mock")

    for domain in ("airline", "retail", "telecom"):
        low = _task_list(value, "low_fidelity", domain)
        high = _task_list(value, "high_fidelity", domain)
        if len(low) != LOW_FIDELITY_COUNTS[domain]:
            raise ValueError(f"wrong low-fidelity task count for {domain}")
        if len(high) != HIGH_FIDELITY_COUNTS[domain]:
            raise ValueError(f"wrong high-fidelity task count for {domain}")
        _require_unique_task_ids(low, f"low_fidelity/{domain}")
        _require_unique_task_ids(high, f"high_fidelity/{domain}")
        overlap = {item["task_id"] for item in low} & {
            item["task_id"] for item in high
        }
        if overlap:
            raise ValueError(f"low/high task overlap for {domain}: {sorted(overlap)}")

    declared_hash = value.get("split_sha256")
    if declared_hash is not None:
        unsigned = dict(value)
        unsigned.pop("split_sha256", None)
        if declared_hash != _canonical_sha256(unsigned):
            raise ValueError("task split SHA-256 does not match its content")


def naive_scalar_reward(outcomes: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """计算故意粗糙的标量对照：平均通过率，执行失败按 0 计。"""

    values: list[int] = []
    mechanical_zero_count = 0
    for index, outcome in enumerate(outcomes):
        status = _outcome_status(outcome, index)
        if status == COMPLETED_STATUS:
            values.append(int(_binary_success(outcome, index)))
        elif status in MECHANICAL_STATUSES:
            values.append(0)
            mechanical_zero_count += 1
        else:
            raise ValueError(f"unsupported execution status at outcome {index}: {status}")
    return {
        "reward": None if not values else float(sum(values) / len(values)),
        "observation_count": len(values),
        "mechanical_failures_counted_as_zero": mechanical_zero_count,
        "scientific_interpretation": "forbidden",
    }


def paired_effect_posterior(
    candidate_outcomes: Sequence[Mapping[str, Any]],
    baseline_outcomes: Sequence[Mapping[str, Any]],
    *,
    draws: int = 20_000,
    seed: int = 0,
    meaningful_delta: float = 0.05,
) -> dict[str, Any]:
    """在共同任务—种子单元上计算贝叶斯自助法配对效应。"""

    if draws < 100:
        raise ValueError("Bayesian-bootstrap draws must be at least 100")
    if not 0 < meaningful_delta < 1:
        raise ValueError("meaningful_delta must be between 0 and 1")
    paired = paired_outcome_differences(candidate_outcomes, baseline_outcomes)
    differences = np.asarray(paired["differences"], dtype=float)
    if differences.size == 0:
        return {
            **{key: value for key, value in paired.items() if key != "differences"},
            "posterior_mean": None,
            "p0": None,
            "p5": None,
            "lcb10": None,
            "meaningful_delta": meaningful_delta,
            "draws": 0,
            "status": "UNAVAILABLE",
        }
    generator = np.random.default_rng(seed)
    weights = generator.dirichlet(np.ones(differences.size), size=draws)
    samples = weights @ differences
    return {
        **{key: value for key, value in paired.items() if key != "differences"},
        "posterior_mean": float(samples.mean()),
        "p0": float(np.mean(samples > 0.0)),
        "p5": float(np.mean(samples > meaningful_delta)),
        "lcb10": float(np.quantile(samples, 0.10)),
        "meaningful_delta": meaningful_delta,
        "draws": draws,
        "status": "READY",
    }


def paired_outcome_differences(
    candidate_outcomes: Sequence[Mapping[str, Any]],
    baseline_outcomes: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """恢复科学有效的配对差；机械失败单独计数而不伪装成负结果。"""

    candidate = _index_outcomes(candidate_outcomes, "candidate")
    baseline = _index_outcomes(baseline_outcomes, "baseline")
    shared = sorted(set(candidate) & set(baseline))
    differences: list[int] = []
    excluded_mechanical = 0
    excluded_invalid = 0
    for key in shared:
        left = candidate[key]
        right = baseline[key]
        left_status = _outcome_status(left, key)
        right_status = _outcome_status(right, key)
        if left_status in MECHANICAL_STATUSES or right_status in MECHANICAL_STATUSES:
            excluded_mechanical += 1
            continue
        if left_status != COMPLETED_STATUS or right_status != COMPLETED_STATUS:
            excluded_invalid += 1
            continue
        differences.append(int(_binary_success(left, key)) - int(_binary_success(right, key)))
    return {
        "differences": differences,
        "paired_scientific_unit_count": len(differences),
        "shared_unit_count": len(shared),
        "candidate_only_unit_count": len(set(candidate) - set(baseline)),
        "baseline_only_unit_count": len(set(baseline) - set(candidate)),
        "excluded_mechanical_pair_count": excluded_mechanical,
        "excluded_invalid_pair_count": excluded_invalid,
        "sampling_unit": "paired_task_seed_outcome",
    }


def expected_entropy_reduction_per_cost(
    successes: int, failures: int, expected_cost: float
) -> float:
    """Beta-Bernoulli 一步观察的预测熵期望下降除以预期成本。"""

    if successes < 0 or failures < 0:
        raise ValueError("successes and failures must be non-negative")
    if not math.isfinite(expected_cost) or expected_cost <= 0:
        raise ValueError("expected_cost must be positive and finite")
    alpha = successes + 1.0
    beta = failures + 1.0
    total = alpha + beta
    probability = alpha / total
    current = _binary_entropy(probability)
    after_success = _binary_entropy((alpha + 1.0) / (total + 1.0))
    after_failure = _binary_entropy(alpha / (total + 1.0))
    expected_after = probability * after_success + (1.0 - probability) * after_failure
    return max(0.0, current - expected_after) / expected_cost


def nondominated_archive(
    candidates: Sequence[Mapping[str, Any]],
    *,
    maximize: Sequence[str] = ("p0", "p5", "lcb10"),
    minimize: Sequence[str] = ("expected_cost", "infra_rate"),
) -> list[dict[str, Any]]:
    """在满足硬约束的候选中保留 Pareto 非支配集合，不产生总分。"""

    eligible = [dict(item) for item in candidates if _hard_constraints_pass(item)]
    archive: list[dict[str, Any]] = []
    for index, item in enumerate(eligible):
        _require_finite_metrics(item, (*maximize, *minimize))
        dominated = any(
            other_index != index
            and _dominates(other, item, maximize=maximize, minimize=minimize)
            for other_index, other in enumerate(eligible)
        )
        if not dominated:
            archive.append(item)
    return sorted(archive, key=lambda item: str(item.get("candidate_id", "")))


def allocate_constrained_parents(
    candidates: Sequence[Mapping[str, Any]],
    *,
    offspring_count: int,
    seed: int,
    structural_coverage: Mapping[str, int] | None = None,
) -> list[dict[str, str]]:
    """按 50% 后验抽样、25% 高熵、25% 低覆盖结构单元分配父代。"""

    if offspring_count < 1:
        raise ValueError("offspring_count must be positive")
    pool = [dict(item) for item in candidates if _hard_constraints_pass(item)]
    if not pool:
        raise ValueError("no hard-constraint-passing parent candidate")
    for item in pool:
        _candidate_id(item)
        _posterior_counts(item)
        _structural_cell(item)

    quotas = _largest_remainder_counts(
        {"posterior_thompson": 0.50, "highest_entropy": 0.25, "least_covered": 0.25},
        offspring_count,
        tie_seed=seed,
    )
    generator = np.random.default_rng(seed)
    coverage = Counter(structural_coverage or {})
    selected: list[dict[str, str]] = []
    available = list(pool)
    for mode in ("posterior_thompson", "highest_entropy", "least_covered"):
        for _ in range(quotas[mode]):
            if not available:
                available = list(pool)
            if mode == "posterior_thompson":
                scores = []
                for item in available:
                    successes, failures = _posterior_counts(item)
                    scores.append(float(generator.beta(successes + 1, failures + 1)))
                chosen_index = max(
                    range(len(available)),
                    key=lambda idx: (scores[idx], _candidate_id(available[idx])),
                )
            elif mode == "highest_entropy":
                chosen_index = max(
                    range(len(available)),
                    key=lambda idx: (
                        _candidate_posterior_entropy(available[idx]),
                        _stable_fraction(seed, mode, _candidate_id(available[idx])),
                    ),
                )
            else:
                chosen_index = min(
                    range(len(available)),
                    key=lambda idx: (
                        coverage[_structural_cell(available[idx])],
                        _stable_fraction(seed, mode, _candidate_id(available[idx])),
                    ),
                )
            chosen = available.pop(chosen_index)
            cell = _structural_cell(chosen)
            coverage[cell] += 1
            selected.append({"candidate_id": _candidate_id(chosen), "allocation": mode})
    return selected


def select_stratified_high_fidelity(
    candidates: Sequence[Mapping[str, Any]], *, count: int = 36, seed: int = 0
) -> list[str]:
    """跨低保真 p0 四分位与结构单元抽取高保真样本，避免只测排行榜顶部。"""

    if count < 1:
        raise ValueError("count must be positive")
    if len(candidates) < count:
        raise ValueError("not enough candidates for requested high-fidelity sample")
    ordered = sorted(
        (dict(item) for item in candidates),
        key=lambda item: (float(item["p0"]), _candidate_id(item)),
    )
    groups: dict[tuple[int, str], list[dict[str, Any]]] = defaultdict(list)
    population = len(ordered)
    for rank, item in enumerate(ordered):
        p0 = float(item["p0"])
        if not math.isfinite(p0) or not 0 <= p0 <= 1:
            raise ValueError("candidate p0 must be finite and between 0 and 1")
        quartile = min(3, (rank * 4) // population)
        groups[(quartile, _structural_cell(item))].append(item)
    for key, items in groups.items():
        items.sort(
            key=lambda item: _stable_fraction(seed, str(key), _candidate_id(item))
        )
    group_keys = sorted(
        groups,
        key=lambda key: (_stable_fraction(seed, "group", str(key)), key),
    )
    selected: list[str] = []
    while len(selected) < count:
        progressed = False
        for key in group_keys:
            if groups[key]:
                selected.append(_candidate_id(groups[key].pop(0)))
                progressed = True
                if len(selected) == count:
                    break
        if not progressed:
            raise RuntimeError("stratified selection exhausted unexpectedly")
    return selected


def fit_logistic_bridge(records: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """拟合 logit P(high success)=β0+β1 logit(p0)。"""

    x, y = _bridge_arrays(records)
    if x.size < 2:
        raise ValueError("at least two bridge observations are required")
    if np.all(y == y[0]):
        mean = float(np.clip(y.mean(), 1e-6, 1 - 1e-6))
        return {
            "beta0": float(_logit(mean)),
            "beta1": 0.0,
            "converged": False,
            "observation_count": int(y.size),
            "reason": "single_class",
        }
    design = np.column_stack([np.ones(x.size), x])
    coefficients = np.zeros(2, dtype=float)
    converged = False
    for _ in range(100):
        probability = _sigmoid(design @ coefficients)
        weights = np.clip(probability * (1.0 - probability), 1e-8, None)
        gradient = design.T @ (y - probability)
        hessian = design.T @ (weights[:, None] * design)
        hessian[1, 1] += 1e-8
        step = np.linalg.lstsq(hessian, gradient, rcond=None)[0]
        coefficients += step
        if float(np.max(np.abs(step))) < 1e-8:
            converged = True
            break
    return {
        "beta0": float(coefficients[0]),
        "beta1": float(coefficients[1]),
        "converged": converged,
        "observation_count": int(y.size),
        "reason": None if converged else "iteration_limit_or_separation",
    }


def block_heldout_bridge_validation(
    records: Sequence[Mapping[str, Any]],
) -> dict[str, Any]:
    """按配对块留一验证桥接模型，并与训练折基准率比较 Brier 分数。"""

    blocks = sorted({_required_text(item.get("block_id"), "block_id") for item in records})
    if len(blocks) < 2:
        raise ValueError("block-heldout validation requires at least two blocks")
    predictions: list[float] = []
    base_predictions: list[float] = []
    observed: list[int] = []
    for block in blocks:
        train = [item for item in records if item.get("block_id") != block]
        test = [item for item in records if item.get("block_id") == block]
        x_train, y_train = _bridge_arrays(train)
        if y_train.size == 0 or not test:
            raise ValueError("each held-out fold needs non-empty train and test data")
        base_rate = float(np.clip(y_train.mean(), 1e-6, 1 - 1e-6))
        model = fit_logistic_bridge(train)
        for item in test:
            p0 = _probability(item.get("p0"), "p0")
            prediction = float(
                _sigmoid(
                    np.asarray(
                        [model["beta0"] + model["beta1"] * _logit(p0)], dtype=float
                    )
                )[0]
            )
            predictions.append(prediction)
            base_predictions.append(base_rate)
            observed.append(int(_binary_value(item.get("high_success"), "high_success")))
    prediction_array = np.asarray(predictions)
    base_array = np.asarray(base_predictions)
    observed_array = np.asarray(observed)
    brier = float(np.mean((prediction_array - observed_array) ** 2))
    base_brier = float(np.mean((base_array - observed_array) ** 2))
    improvement = None if base_brier == 0 else (base_brier - brier) / base_brier
    final_model = fit_logistic_bridge(records)
    ordered = sorted(records, key=lambda item: float(item["p0"]))
    quartile_size = max(1, len(ordered) // 4)
    bottom = ordered[:quartile_size]
    top = ordered[-quartile_size:]
    return {
        "validation": "leave_one_block_out",
        "block_count": len(blocks),
        "observation_count": len(observed),
        "brier": brier,
        "base_rate_brier": base_brier,
        "relative_brier_improvement": improvement,
        "beta0": final_model["beta0"],
        "beta1": final_model["beta1"],
        "fit_converged": final_model["converged"],
        "top_quartile_success_rate": float(
            np.mean([int(item["high_success"]) for item in top])
        ),
        "bottom_quartile_success_rate": float(
            np.mean([int(item["high_success"]) for item in bottom])
        ),
    }


def evaluate_pilot_gate(summary: Mapping[str, Any]) -> dict[str, Any]:
    """机械判定是否具备进入确认实验的校准条件，不作科研候选裁决。"""

    checks = {
        "implementation_rate_at_least_60pct": float(summary.get("implementation_rate", -1))
        >= 0.60,
        "contains_high_fidelity_pass": int(summary.get("high_fidelity_pass_count", 0)) > 0,
        "contains_high_fidelity_failure": int(summary.get("high_fidelity_failure_count", 0))
        > 0,
        "bridge_brier_improves_at_least_10pct": float(
            summary.get("relative_brier_improvement", -math.inf)
        )
        >= 0.10,
        "bridge_slope_positive": float(summary.get("beta1", -math.inf)) > 0,
        "top_quartile_beats_bottom": float(
            summary.get("top_quartile_success_rate", -math.inf)
        )
        > float(summary.get("bottom_quartile_success_rate", math.inf)),
        "isolation_valid": summary.get("isolation_valid") is True,
        "evaluator_lock_valid": summary.get("evaluator_lock_valid") is True,
    }
    failed = [name for name, passed in checks.items() if not passed]
    return {
        "passed": not failed,
        "checks": checks,
        "failed_checks": failed,
        "authority": "calibration_phase_only",
        "scientific_delivery_authority": False,
    }


def evaluate_confirmation_gate(summary: Mapping[str, Any]) -> dict[str, Any]:
    """核验冻结确认标准；结果只回答搜索策略是否值得采用。"""

    block_advantages = [float(value) for value in summary.get("block_advantages", [])]
    candidate_posteriors = summary.get("candidate_posteriors", [])
    if not isinstance(candidate_posteriors, Sequence) or isinstance(
        candidate_posteriors, (str, bytes)
    ):
        raise ValueError("candidate_posteriors must be a sequence")
    meaningful_candidate = any(
        isinstance(item, Mapping)
        and float(item.get("p5", -math.inf)) >= 0.95
        and float(item.get("lcb10", -math.inf)) > 0
        for item in candidate_posteriors
    )
    checks = {
        "eight_new_blocks": len(block_advantages) == 8,
        "wins_at_least_seven_blocks": sum(value > 0 for value in block_advantages) >= 7,
        "median_advantage_at_least_5pp": bool(block_advantages)
        and float(np.median(block_advantages)) >= 0.05,
        "meaningful_candidate_posterior": meaningful_candidate,
        "domain_regression_constraints_pass": summary.get(
            "domain_regression_constraints_pass"
        )
        is True,
        "diversity_constraints_pass": summary.get("diversity_constraints_pass") is True,
        "isolation_valid": summary.get("isolation_valid") is True,
        "evaluator_lock_valid": summary.get("evaluator_lock_valid") is True,
    }
    failed = [name for name, passed in checks.items() if not passed]
    return {
        "passed": not failed,
        "checks": checks,
        "failed_checks": failed,
        "authority": "search_policy_adoption_only",
        "scientific_delivery_authority": False,
    }


def validate_temporal_packet(packet: Mapping[str, Any]) -> dict[str, Any]:
    """拒绝时间洁净层中的 2026 材料泄漏和主结论式大模型辅助标注。"""

    cutoff_year = packet.get("visible_through_year")
    if cutoff_year != 2025:
        raise ValueError("temporal clean packet must freeze visibility through 2025")
    visible = packet.get("visible_artifacts")
    if not isinstance(visible, Sequence) or isinstance(visible, (str, bytes)):
        raise ValueError("visible_artifacts must be a sequence")
    for index, artifact in enumerate(visible):
        if not isinstance(artifact, Mapping):
            raise ValueError(f"visible artifact {index} must be an object")
        year = artifact.get("year")
        if not isinstance(year, int) or year > 2025:
            raise ValueError(f"visible artifact {index} violates the 2025 cutoff")
    heldout = packet.get("heldout_artifacts")
    if not isinstance(heldout, Sequence) or isinstance(heldout, (str, bytes)):
        raise ValueError("heldout_artifacts must be a sequence")
    heldout_ids = {
        _required_text(item.get("artifact_id"), "heldout artifact_id")
        for item in heldout
        if isinstance(item, Mapping)
    }
    expected = {"P072", "P074", "P087"}
    if heldout_ids != expected:
        raise ValueError("temporal heldout set must be exactly P072, P074, P087")
    for annotation in packet.get("annotations", []):
        if not isinstance(annotation, Mapping):
            raise ValueError("temporal annotations must be objects")
        if annotation.get("annotator_type") == "llm_auxiliary":
            if annotation.get("use") != "auxiliary_only":
                raise ValueError("llm_auxiliary annotations must remain auxiliary_only")
    return {
        "status": "VALID",
        "visible_artifact_count": len(visible),
        "heldout_artifact_ids": sorted(heldout_ids),
        "primary_scientific_conclusion_from_llm": False,
    }


def _load_tau2_tasks(path: Path, domain: str) -> tuple[list[dict[str, Any]], str]:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"τ² task JSON must not contain a BOM: {path}")
    try:
        value = json.loads(data.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid τ² task JSON for {domain}: {path}") from error
    if not isinstance(value, list):
        raise ValueError(f"τ² task JSON root must be an array: {path}")
    tasks: list[dict[str, Any]] = []
    seen: set[str] = set()
    for index, item in enumerate(value):
        if not isinstance(item, dict):
            raise ValueError(f"τ² {domain} task {index} must be an object")
        task_id = _required_text(item.get("id"), f"{domain} task id")
        if task_id in seen:
            raise ValueError(f"duplicate τ² task id in {domain}: {task_id}")
        seen.add(task_id)
        tasks.append(item)
    return tasks, hashlib.sha256(data).hexdigest()


def _load_tau2_base_ids(path: Path, domain: str) -> tuple[list[str], str]:
    data = path.read_bytes()
    if data.startswith(b"\xef\xbb\xbf"):
        raise ValueError(f"τ² split JSON must not contain a BOM: {path}")
    try:
        value = json.loads(data.decode("utf-8", errors="strict"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValueError(f"invalid τ² split JSON for {domain}: {path}") from error
    if not isinstance(value, dict):
        raise ValueError(f"τ² split JSON root must be an object: {path}")
    base = value.get("base")
    if not isinstance(base, list) or not all(
        isinstance(item, str) and item for item in base
    ):
        raise ValueError(f"τ² {domain} split must provide non-empty base task IDs")
    if len(base) != len(set(base)):
        raise ValueError(f"τ² {domain} base split contains duplicate task IDs")
    return base, hashlib.sha256(data).hexdigest()


def _task_fact(domain: str, task: Mapping[str, Any]) -> dict[str, Any]:
    criteria = task.get("evaluation_criteria")
    if not isinstance(criteria, Mapping):
        raise ValueError(f"τ² task {task.get('id')} has no evaluation_criteria")
    actions = criteria.get("actions")
    if actions is None:
        action_count = 0
    elif isinstance(actions, Sequence) and not isinstance(actions, (str, bytes)):
        action_count = len(actions)
    else:
        raise ValueError(f"τ² task {task.get('id')} actions must be an array or null")
    communicate = criteria.get("communicate_info")
    communication_count = (
        len(communicate)
        if isinstance(communicate, Sequence) and not isinstance(communicate, (str, bytes))
        else 0
    )
    reward_basis = criteria.get("reward_basis")
    if not isinstance(reward_basis, Sequence) or isinstance(reward_basis, (str, bytes)):
        reward_basis = []
    return {
        "task_id": _required_text(task.get("id"), f"{domain} task id"),
        "domain": domain,
        "action_count": action_count,
        "action_stratum": _action_stratum(action_count),
        "communication_count": communication_count,
        "reward_basis": sorted(str(item) for item in reward_basis),
    }


def _stratified_task_sample(
    tasks: Sequence[Mapping[str, Any]], count: int, *, seed: int, salt: str
) -> list[dict[str, Any]]:
    if count > len(tasks):
        raise ValueError(f"cannot select {count} tasks from {len(tasks)}")
    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for raw in tasks:
        item = dict(raw)
        groups[str(item["action_stratum"])].append(item)
    allocations = _proportional_allocation(
        {key: len(items) for key, items in groups.items()}, count, seed=seed, salt=salt
    )
    selected: list[dict[str, Any]] = []
    for stratum, items in groups.items():
        items.sort(
            key=lambda item: _stable_fraction(seed, salt, stratum, str(item["task_id"]))
        )
        selected.extend(items[: allocations[stratum]])
    return sorted(selected, key=lambda item: _natural_identifier_key(item["task_id"]))


def _proportional_allocation(
    sizes: Mapping[str, int], count: int, *, seed: int, salt: str
) -> dict[str, int]:
    total = sum(sizes.values())
    if count > total:
        raise ValueError("allocation count exceeds population")
    raw = {key: count * size / total for key, size in sizes.items()}
    result = {key: min(sizes[key], math.floor(value)) for key, value in raw.items()}
    remaining = count - sum(result.values())
    order = sorted(
        sizes,
        key=lambda key: (
            -(raw[key] - math.floor(raw[key])),
            _stable_fraction(seed, salt, key),
        ),
    )
    while remaining:
        progressed = False
        for key in order:
            if result[key] < sizes[key]:
                result[key] += 1
                remaining -= 1
                progressed = True
                if not remaining:
                    break
        if not progressed:
            raise RuntimeError("proportional allocation could not finish")
    return result


def _largest_remainder_counts(
    shares: Mapping[str, float], count: int, *, tie_seed: int
) -> dict[str, int]:
    if not math.isclose(sum(shares.values()), 1.0, rel_tol=0, abs_tol=1e-12):
        raise ValueError("allocation shares must sum to one")
    raw = {key: value * count for key, value in shares.items()}
    result = {key: math.floor(value) for key, value in raw.items()}
    remaining = count - sum(result.values())
    order = sorted(
        shares,
        key=lambda key: (
            -(raw[key] - math.floor(raw[key])),
            _stable_fraction(tie_seed, "quota", key),
        ),
    )
    for key in order[:remaining]:
        result[key] += 1
    return result


def _action_stratum(count: int) -> str:
    if count == 0:
        return "zero"
    if count <= 2:
        return "one_two"
    if count <= 5:
        return "three_five"
    return "six_plus"


def _task_list(value: Mapping[str, Any], phase: str, domain: str) -> list[Mapping[str, Any]]:
    phase_value = value.get(phase)
    if not isinstance(phase_value, Mapping):
        raise ValueError(f"task split section is missing: {phase}")
    tasks = phase_value.get(domain)
    if not isinstance(tasks, list) or not all(isinstance(item, Mapping) for item in tasks):
        raise ValueError(f"task list is invalid: {phase}/{domain}")
    return tasks


def _require_unique_task_ids(tasks: Sequence[Mapping[str, Any]], label: str) -> None:
    identifiers = [_required_text(item.get("task_id"), f"{label} task_id") for item in tasks]
    if len(identifiers) != len(set(identifiers)):
        raise ValueError(f"duplicate task id in {label}")


def _index_outcomes(
    outcomes: Sequence[Mapping[str, Any]], label: str
) -> dict[tuple[str, str, str, int], Mapping[str, Any]]:
    indexed: dict[tuple[str, str, str, int], Mapping[str, Any]] = {}
    for index, item in enumerate(outcomes):
        key = (
            _required_text(item.get("block_id"), f"{label}[{index}].block_id"),
            _required_text(item.get("domain"), f"{label}[{index}].domain"),
            _required_text(item.get("task_id"), f"{label}[{index}].task_id"),
            _nonnegative_int(item.get("repetition"), f"{label}[{index}].repetition"),
        )
        if key in indexed:
            raise ValueError(f"duplicate {label} paired outcome unit: {key}")
        indexed[key] = item
    return indexed


def _outcome_status(item: Mapping[str, Any], label: object) -> str:
    return _required_text(item.get("execution_status"), f"{label}.execution_status")


def _binary_success(item: Mapping[str, Any], label: object) -> bool:
    return _binary_value(item.get("success"), f"{label}.success")


def _binary_value(value: object, label: str) -> bool:
    if type(value) is not bool:
        raise ValueError(f"{label} must be boolean")
    return value


def _hard_constraints_pass(item: Mapping[str, Any]) -> bool:
    constraints = item.get("hard_constraints")
    return isinstance(constraints, Mapping) and bool(constraints) and all(
        value is True for value in constraints.values()
    )


def _dominates(
    left: Mapping[str, Any],
    right: Mapping[str, Any],
    *,
    maximize: Sequence[str],
    minimize: Sequence[str],
) -> bool:
    no_worse = all(float(left[key]) >= float(right[key]) for key in maximize) and all(
        float(left[key]) <= float(right[key]) for key in minimize
    )
    strictly_better = any(float(left[key]) > float(right[key]) for key in maximize) or any(
        float(left[key]) < float(right[key]) for key in minimize
    )
    return no_worse and strictly_better


def _require_finite_metrics(item: Mapping[str, Any], fields: Iterable[str]) -> None:
    for field in fields:
        value = item.get(field)
        if isinstance(value, bool) or not isinstance(value, (int, float)):
            raise ValueError(f"candidate metric {field} must be numeric")
        if not math.isfinite(float(value)):
            raise ValueError(f"candidate metric {field} must be finite")


def _candidate_id(item: Mapping[str, Any]) -> str:
    return _required_text(item.get("candidate_id"), "candidate_id")


def _posterior_counts(item: Mapping[str, Any]) -> tuple[int, int]:
    return (
        _nonnegative_int(item.get("successes"), "successes"),
        _nonnegative_int(item.get("failures"), "failures"),
    )


def _candidate_posterior_entropy(item: Mapping[str, Any]) -> float:
    successes, failures = _posterior_counts(item)
    return _binary_entropy((successes + 1) / (successes + failures + 2))


def _structural_cell(item: Mapping[str, Any]) -> str:
    cell = item.get("structural_cell")
    if isinstance(cell, str) and cell.strip():
        return cell.strip()
    descriptors = item.get("descriptors")
    if isinstance(descriptors, Mapping) and descriptors:
        return _canonical_sha256(dict(descriptors))[:16]
    raise ValueError("candidate must declare structural_cell or descriptors")


def _bridge_arrays(records: Sequence[Mapping[str, Any]]) -> tuple[np.ndarray, np.ndarray]:
    x: list[float] = []
    y: list[int] = []
    for index, item in enumerate(records):
        p0 = _probability(item.get("p0"), f"bridge[{index}].p0")
        x.append(_logit(p0))
        y.append(int(_binary_value(item.get("high_success"), f"bridge[{index}].high_success")))
    return np.asarray(x, dtype=float), np.asarray(y, dtype=float)


def _probability(value: object, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{label} must be numeric")
    number = float(value)
    if not math.isfinite(number) or not 0 <= number <= 1:
        raise ValueError(f"{label} must be between 0 and 1")
    return number


def _logit(probability: float) -> float:
    clipped = min(1 - 1e-6, max(1e-6, probability))
    return math.log(clipped / (1.0 - clipped))


def _sigmoid(value: np.ndarray) -> np.ndarray:
    clipped = np.clip(value, -40, 40)
    return 1.0 / (1.0 + np.exp(-clipped))


def _binary_entropy(probability: float) -> float:
    if probability <= 0 or probability >= 1:
        return 0.0
    return -probability * math.log(probability) - (1.0 - probability) * math.log(
        1.0 - probability
    )


def _required_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be non-empty text")
    return value.strip()


def _nonnegative_int(value: object, label: str) -> int:
    if isinstance(value, bool) or not isinstance(value, int) or value < 0:
        raise ValueError(f"{label} must be a non-negative integer")
    return value


def _canonical_sha256(value: object) -> str:
    return hashlib.sha256(
        json.dumps(
            value, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
    ).hexdigest()


def _stable_fraction(*parts: object) -> float:
    digest = hashlib.sha256("\0".join(str(part) for part in parts).encode("utf-8")).digest()
    return int.from_bytes(digest[:8], "big") / 2**64


def _natural_identifier_key(value: object) -> tuple[int, int | str]:
    text = str(value)
    return (0, int(text)) if text.isdigit() else (1, text)
