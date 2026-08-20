from __future__ import annotations

import hashlib
import json
import shutil
from pathlib import Path

import pytest

from conftest import make_run, record_successful_attempt
from crl_v3.comparison import (
    PARITY_STATUSES,
    compare_attempts,
    render_comparison_report,
)
from crl_v3.experiment import experiment_material_errors
from crl_v3.workspace import ResearchWorkspace


def _fixture(tmp_path: Path) -> tuple[Path, Path, ResearchWorkspace]:
    product, run = make_run(tmp_path)
    source = run / "workbench_v001" / "source.py"
    source.parent.mkdir()
    source.write_bytes(b"print('fixture')\n")
    completed = record_successful_attempt(
        product, run, "v001", source, attempt_id="candidate"
    )
    assert completed.returncode == 0
    return product, run, ResearchWorkspace(run, product_root=product, version="v001")


def _clone_attempt(run: Path, source_id: str, target_id: str) -> Path:
    attempts = run / "experiment_v001" / "attempts"
    source = attempts / source_id
    target = attempts / target_id
    shutil.copytree(source, target)
    execution = _read_json(target / "execution.json")
    source_absolute = str(source.resolve())
    target_absolute = str(target.resolve())
    source_relative = source.relative_to(run).as_posix()
    target_relative = target.relative_to(run).as_posix()

    def replace(value: object) -> object:
        if isinstance(value, str):
            return value.replace(source_absolute, target_absolute).replace(
                source_relative, target_relative
            )
        if isinstance(value, list):
            return [replace(item) for item in value]
        if isinstance(value, dict):
            return {name: replace(item) for name, item in value.items()}
        return value

    execution = replace(execution)
    assert isinstance(execution, dict)
    execution["attempt_id"] = target_id
    _write_json(target / "execution.json", execution)
    return target


def _set_metrics(attempt: Path, records: list[dict[str, object]]) -> None:
    metrics_path = attempt / "metrics.json"
    metrics = _read_json(metrics_path)
    metrics["records"] = records
    _write_json(metrics_path, metrics)
    _refresh_snapshot(attempt, "metrics", metrics_path)


def _set_spec_value(attempt: Path, name: str, value: object) -> None:
    spec_path = attempt / "spec.json"
    spec = _read_json(spec_path)
    spec[name] = value
    _write_json(spec_path, spec)
    _refresh_snapshot(attempt, "experiment_spec", spec_path)


def _refresh_snapshot(attempt: Path, field: str, path: Path) -> None:
    execution_path = attempt / "execution.json"
    execution = _read_json(execution_path)
    data = path.read_bytes()
    execution[field]["snapshot"]["size_bytes"] = len(data)
    execution[field]["snapshot"]["sha256"] = hashlib.sha256(data).hexdigest()
    _write_json(execution_path, execution)


def _record(
    value: float,
    *,
    unit: str = "ratio",
    split: str = "test",
    aggregation: str = "raw_replicate",
    n: int = 1,
    seed: int | None = None,
    replicate: int | None = None,
) -> dict[str, object]:
    result: dict[str, object] = {
        "name": "test_primary_metric",
        "value": value,
        "unit": unit,
        "split": split,
        "aggregation": aggregation,
        "n": n,
    }
    if seed is not None:
        result["seed"] = seed
    if replicate is not None:
        result["replicate"] = replicate
    return result


def _read_json(path: Path) -> dict[str, object]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _write_json(path: Path, value: object) -> None:
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _mark_failed(attempt: Path, *, timed_out: bool = False) -> None:
    execution_path = attempt / "execution.json"
    execution = _read_json(execution_path)
    execution["command_exit_code"] = 1
    execution["runner_exit_code"] = 124 if timed_out else 1
    execution["command_error"] = "TimeoutExpired: test timeout" if timed_out else None
    execution["timed_out"] = timed_out
    execution["timeout_seconds"] = 0.01 if timed_out else None
    execution["termination_method"] = "test_process_tree_termination" if timed_out else None
    execution["process_tree_cleanup_ok"] = True if timed_out else None
    _write_json(execution_path, execution)


def test_multiple_baselines_keep_metric_units_splits_and_model_facts_separate(
    tmp_path: Path,
) -> None:
    _, run, workspace = _fixture(tmp_path)
    candidate = run / "experiment_v001/attempts/candidate"
    matched = _clone_attempt(run, "candidate", "baseline-matched")
    different = _clone_attempt(run, "candidate", "baseline-different")
    _set_metrics(
        candidate,
        [_record(0.6, seed=7, replicate=1), _record(0.8, seed=7, replicate=2)],
    )
    _set_metrics(
        matched,
        [_record(0.4, seed=7, replicate=1), _record(0.6, seed=7, replicate=2)],
    )
    _set_metrics(
        different,
        [
            _record(50.0, unit="percent", split="validation"),
            _record(60.0, unit="percent", split="validation"),
        ],
    )
    _set_spec_value(different, "model", "另一模型")

    publication = compare_attempts(
        workspace,
        "comparison-001",
        "candidate",
        ("baseline-matched", "baseline-different"),
    )
    output = Path(publication.path)
    payload = _read_json(output / "comparison.json")
    statuses = {
        item["status"]
        for ledger in payload["parity_ledgers"]
        for item in ledger["dimensions"]
    }
    assert statuses <= set(PARITY_STATUSES)
    assert [item["attempt_id"] for item in payload["baseline_attempts"]] == [
        "baseline-matched",
        "baseline-different",
    ]
    first_metric = payload["metric_facts"][0]["comparisons"][0]
    assert first_metric["difference_candidate_minus_baseline"] == pytest.approx(0.2)
    assert first_metric["ratio_candidate_over_baseline"] == pytest.approx(1.4)
    assert "paired raw-replicate" in first_metric["confidence_interval"]["method"]
    assert payload["metric_facts"][1]["comparisons"][0]["metric_presence"] != "both"
    different_dimensions = {
        item["dimension"]: item["status"]
        for item in payload["parity_ledgers"][1]["dimensions"]
    }
    assert different_dimensions["model"] == "mismatched"
    assert different_dimensions["dataset_split"] == "mismatched"
    seed_value = next(
        item["candidate"]["value"]
        for item in payload["parity_ledgers"][0]["dimensions"]
        if item["dimension"] == "seed"
    )
    assert seed_value["duplicate_metric_record_seeds"] == [7]
    rendered = render_comparison_report(payload)
    assert rendered == (output / "report.md").read_text(encoding="utf-8")
    assert "## 指标事实" in rendered
    assert "## Parity mismatch" in rendered
    assert "## 缺失信息" in rendered
    assert "## 人工解释（由主研究者填写）" in rendered
    assert "fairness_score" not in json.dumps(payload).lower()
    original = (output / "comparison.json").read_bytes()
    with pytest.raises(FileExistsError):
        compare_attempts(
            workspace,
            "comparison-001",
            "candidate",
            ("baseline-matched",),
        )
    assert (output / "comparison.json").read_bytes() == original


def test_mean_and_median_are_distinct_metric_identities_without_arithmetic_fact(
    tmp_path: Path,
) -> None:
    _, run, workspace = _fixture(tmp_path)
    candidate = run / "experiment_v001/attempts/candidate"
    baseline = _clone_attempt(run, "candidate", "baseline")
    _set_metrics(candidate, [_record(0.8, aggregation="mean", n=100)])
    _set_metrics(baseline, [_record(0.4, aggregation="median", n=25)])

    publication = compare_attempts(
        workspace, "comparison-aggregation-split", "candidate", ("baseline",)
    )
    path = Path(publication.path)
    payload = _read_json(path / "comparison.json")
    comparisons = payload["metric_facts"][0]["comparisons"]

    assert payload["schema_version"] == 2
    assert [item["metric_key"]["aggregation"] for item in comparisons] == [
        "mean",
        "median",
    ]
    assert [item["metric_presence"] for item in comparisons] == [
        "candidate_only",
        "baseline_only",
    ]
    for item in comparisons:
        assert item["candidate_fact_value"] is None
        assert item["baseline_fact_value"] is None
        assert item["difference_candidate_minus_baseline"] is None
        assert item["ratio_candidate_over_baseline"] is None
    assert comparisons[0]["candidate"]["aggregations"] == ["mean"]
    assert comparisons[0]["candidate"]["n"] == [100]
    assert comparisons[1]["baseline"]["aggregations"] == ["median"]
    assert comparisons[1]["baseline"]["n"] == [25]
    report = (path / "report.md").read_text(encoding="utf-8")
    assert "split / aggregation" in report
    assert "test_primary_metric / ratio / test / mean" in report
    assert "test_primary_metric / ratio / test / median" in report


def test_same_aggregation_keeps_unweighted_record_mean_and_provenance(
    tmp_path: Path,
) -> None:
    _, run, workspace = _fixture(tmp_path)
    candidate = run / "experiment_v001/attempts/candidate"
    baseline = _clone_attempt(run, "candidate", "baseline")
    _set_metrics(
        candidate,
        [
            _record(0.4, aggregation="mean", n=10, seed=1),
            _record(0.8, aggregation="mean", n=100, seed=2),
        ],
    )
    _set_metrics(
        baseline,
        [
            _record(0.2, aggregation="mean", n=5, seed=3),
            _record(0.6, aggregation="mean", n=1000, seed=4),
        ],
    )

    publication = compare_attempts(
        workspace, "comparison-same-aggregation", "candidate", ("baseline",)
    )
    metric = _read_json(Path(publication.path) / "comparison.json")["metric_facts"][0][
        "comparisons"
    ][0]

    assert metric["metric_key"]["aggregation"] == "mean"
    assert metric["fact_value_basis"] == (
        "arithmetic_mean_across_same_metric_unit_split_aggregation_records"
    )
    assert metric["candidate_fact_value"] == pytest.approx(0.6)
    assert metric["baseline_fact_value"] == pytest.approx(0.4)
    assert metric["difference_candidate_minus_baseline"] == pytest.approx(0.2)
    assert metric["candidate"]["n"] == [10, 100]
    assert metric["baseline"]["n"] == [5, 1000]
    assert metric["candidate"]["seeds"] == [1, 2]
    assert metric["baseline"]["seeds"] == [3, 4]


def test_raw_replicate_independent_confidence_interval_is_unchanged(
    tmp_path: Path,
) -> None:
    _, run, workspace = _fixture(tmp_path)
    candidate = run / "experiment_v001/attempts/candidate"
    baseline = _clone_attempt(run, "candidate", "baseline")
    _set_metrics(
        candidate,
        [_record(0.6, seed=1, replicate=1), _record(0.8, seed=1, replicate=2)],
    )
    _set_metrics(
        baseline,
        [_record(0.3, seed=2, replicate=1), _record(0.5, seed=2, replicate=2)],
    )

    publication = compare_attempts(
        workspace, "comparison-independent-ci", "candidate", ("baseline",)
    )
    metric = _read_json(Path(publication.path) / "comparison.json")["metric_facts"][0][
        "comparisons"
    ][0]

    assert metric["metric_key"]["aggregation"] == "raw_replicate"
    assert "independent raw-replicate" in metric["confidence_interval"]["method"]
    assert metric["confidence_interval"]["sample_sizes"] == {
        "candidate_replicates": 2,
        "baseline_replicates": 2,
    }
    assert metric["candidate"]["replicates"] == [1, 2]
    assert metric["baseline"]["replicates"] == [1, 2]


def test_unknown_budget_and_missing_replicates_are_explicit(tmp_path: Path) -> None:
    _, run, workspace = _fixture(tmp_path)
    baseline = _clone_attempt(run, "candidate", "baseline")
    for attempt in (run / "experiment_v001/attempts/candidate", baseline):
        execution_path = attempt / "execution.json"
        execution = _read_json(execution_path)
        execution["budget_facts"]["machine_readable_limits"] = None
        execution["budget_facts"]["actual"]["tokens"] = "unknown"
        _write_json(execution_path, execution)

    publication = compare_attempts(
        workspace, "comparison-missing", "candidate", ("baseline",)
    )
    payload = _read_json(Path(publication.path) / "comparison.json")
    dimensions = {
        item["dimension"]: item["status"]
        for item in payload["parity_ledgers"][0]["dimensions"]
    }
    assert dimensions["token_budget"] == "unknown"
    assert dimensions["replicate_count"] == "unknown"
    metric = payload["metric_facts"][0]["comparisons"][0]
    assert metric["confidence_interval"] is None
    assert "at least two raw replicate" in metric["confidence_interval_reason"]


@pytest.mark.parametrize("failed_side", ["candidate", "baseline"])
@pytest.mark.parametrize("timed_out", [False, True])
def test_failed_candidate_or_baseline_is_compared_as_a_failure_fact(
    tmp_path: Path, failed_side: str, timed_out: bool
) -> None:
    _, run, workspace = _fixture(tmp_path)
    _clone_attempt(run, "candidate", "baseline")
    failed = run / "experiment_v001/attempts" / failed_side
    _mark_failed(failed, timed_out=timed_out)

    publication = compare_attempts(
        workspace,
        f"comparison-failed-{failed_side}-{int(timed_out)}",
        "candidate",
        ("baseline",),
    )
    payload = _read_json(Path(publication.path) / "comparison.json")
    ledger = payload["parity_ledgers"][0]["dimensions"]
    failure = next(item for item in ledger if item["dimension"] == "failure_rate")
    failed_fact = failure[failed_side]["value"]
    assert failed_fact["failed_attempts"] == 1
    assert failed_fact["rate"] == 1.0
    assert failed_fact["timed_out"] is timed_out
    assert payload["metric_facts"][0]["comparisons"][0]["metric_presence"] == "both"
    assert experiment_material_errors(workspace, (failed_side,))


def test_failed_attempt_without_metrics_is_published_as_unavailable(tmp_path: Path) -> None:
    _, run, workspace = _fixture(tmp_path)
    baseline = _clone_attempt(run, "candidate", "baseline")
    _mark_failed(baseline)
    (baseline / "metrics.json").unlink()
    execution_path = baseline / "execution.json"
    execution = _read_json(execution_path)
    execution["metrics_contract_ok"] = False
    execution["metrics"]["snapshot"] = None
    execution["metrics"]["validation_errors"] = ["metrics output is missing"]
    _write_json(execution_path, execution)

    publication = compare_attempts(
        workspace, "comparison-metrics-unavailable", "candidate", ("baseline",)
    )
    path = Path(publication.path)
    payload = _read_json(path / "comparison.json")
    assert payload["baseline_attempts"][0]["metrics_availability"] == "unavailable"
    assert payload["baseline_attempts"][0]["metrics_sha256"] is None
    assert payload["metric_facts"][0]["comparisons"][0]["metric_presence"] == "candidate_only"
    report = (path / "report.md").read_text(encoding="utf-8")
    assert "没有有效指标快照" in report
    assert "metrics output is missing" in report


@pytest.mark.parametrize(
    "mutation, error_fragment",
    [
        ("cross-version", "version"),
        ("nan", "non-finite"),
        ("tampered", "SHA-256"),
    ],
)
def test_invalid_or_non_supporting_attempt_is_rejected_without_partial_output(
    tmp_path: Path, mutation: str, error_fragment: str
) -> None:
    _, run, workspace = _fixture(tmp_path)
    baseline = _clone_attempt(run, "candidate", "baseline")
    execution_path = baseline / "execution.json"
    if mutation == "failed":
        execution = _read_json(execution_path)
        execution["command_exit_code"] = 1
        _write_json(execution_path, execution)
    elif mutation == "cross-version":
        execution = _read_json(execution_path)
        execution["version"] = "v002"
        _write_json(execution_path, execution)
    elif mutation == "nan":
        metrics_path = baseline / "metrics.json"
        data = metrics_path.read_text(encoding="utf-8").replace('"value": 0.5', '"value": NaN')
        metrics_path.write_text(data, encoding="utf-8", newline="\n")
        _refresh_snapshot(baseline, "metrics", metrics_path)
    else:
        metrics_path = baseline / "metrics.json"
        metrics_path.write_bytes(metrics_path.read_bytes() + b" \n")

    with pytest.raises(ValueError, match=error_fragment):
        compare_attempts(
            workspace,
            f"comparison-{mutation}",
            "candidate",
            ("baseline",),
        )
    assert not (
        run / f"experiment_v001/comparisons/comparison-{mutation}"
    ).exists()


def test_rejects_duplicate_baselines_and_unsafe_cross_run_path(tmp_path: Path) -> None:
    _, run, workspace = _fixture(tmp_path)
    _clone_attempt(run, "candidate", "baseline")
    with pytest.raises(ValueError, match="unique"):
        compare_attempts(
            workspace, "comparison-duplicate", "candidate", ("baseline", "baseline")
        )
    with pytest.raises(ValueError, match="safe"):
        compare_attempts(
            workspace,
            "comparison-cross-run",
            "candidate",
            ("../another-run/attempt",),
        )
