from __future__ import annotations

import hashlib
import json
from pathlib import Path

from conftest import make_run, record_successful_attempt
from crl_v3.comparison import compare_attempts
from crl_v3.falsification import update_claim
from crl_v3.prior_audit import _report_bytes
from crl_v3.review import render_review_input, review_material_errors
from crl_v3.seed_support import (
    audit_seed_support,
    publish_seed_support_audit,
    render_seed_support_json,
    render_seed_support_markdown,
)
from crl_v3.workspace import ResearchWorkspace
from tools.audit_seed_support import main


def _write_json(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def _metadata(
    hypothesis_id: str,
    claim_id: str,
    *,
    mappings: list[dict[str, object]] | None = None,
    dispositions: list[dict[str, str]] | None = None,
) -> str:
    payload = {
        "schema_version": 1,
        "hypothesis_ids": [hypothesis_id],
        "claim_ids": [claim_id],
        "falsified_claim_dispositions": dispositions or [],
        "metric_mappings": mappings or [],
    }
    return "<!-- CRL_SEED_SUPPORT_META " + json.dumps(
        payload, ensure_ascii=False, separators=(",", ":")
    ) + " -->"


def _fixture(tmp_path: Path) -> tuple[Path, Path, ResearchWorkspace, str, str]:
    product, run = make_run(tmp_path)
    source = run / "workbench_v001" / "source.py"
    source.parent.mkdir()
    source.write_bytes(b"print('fixture')\n")
    completed = record_successful_attempt(
        product, run, "v001", source, attempt_id="support"
    )
    assert completed.returncode == 0, completed.stderr.decode("utf-8")
    workspace = ResearchWorkspace(run, product_root=product, version="v001")
    spec = json.loads(
        (run / "experiment_v001/attempts/support/spec.json").read_text(
            encoding="utf-8"
        )
    )
    return product, run, workspace, spec["hypothesis_id"], spec["claim_ids"][0]


def _prior(
    run: Path,
    workspace: ResearchWorkspace,
    hypothesis_id: str,
    *,
    created: str = "2026-08-10T00:00:00Z",
    queries: list[dict[str, str]] | None = None,
    candidates: list[dict[str, object]] | None = None,
    audit_id: str = "audit-001",
) -> None:
    portfolio = workspace.read_hypotheses(required=True)
    assert portfolio is not None
    hypothesis = next(
        item
        for item in portfolio.portfolio.hypotheses
        if item.hypothesis_id == hypothesis_id
    )
    destination = run / "hypotheses_v001" / "priors" / audit_id
    destination.mkdir(parents=True)
    candidate_payload = {
        "schema_version": 1,
        "artifact_kind": "run_local_non_authoritative_prior_candidates",
        "audit_id": audit_id,
        "created_at_utc": created,
        "degraded": False,
        "source_attempts": [],
        "candidates": (
            [{"candidate_id": "prior-0123456789abcdef"}]
            if candidates is None
            else candidates
        ),
    }
    candidate_bytes = (
        json.dumps(candidate_payload, ensure_ascii=False, indent=2, sort_keys=True)
        + "\n"
    ).encode("utf-8")
    report = _report_bytes(audit_id)
    request = {
        "schema_version": 1,
        "artifact_kind": "run_local_non_authoritative_prior_audit",
        "audit_id": audit_id,
        "created_at_utc": created,
        "run_id": run.name,
        "version": "v001",
        "hypothesis": {
            "hypothesis_id": hypothesis_id,
            "hypothesis_revision": hypothesis.revision,
            "portfolio_path": "hypotheses_v001/portfolio.json",
            "portfolio_sha256": portfolio.sha256,
        },
        "queries": queries if queries is not None else [{"query_id": "q001", "text": "agent support audit"}],
        "sources": ["test"],
        "seed_paper_id": None,
        "limits": {},
        "network_responses": [],
        "degraded": False,
        "artifact_hashes": {
            "candidates_json_sha256": hashlib.sha256(candidate_bytes).hexdigest(),
            "report_md_sha256": hashlib.sha256(report).hexdigest(),
        },
    }
    _write_json(destination / "request.json", request)
    (destination / "candidates.json").write_bytes(candidate_bytes)
    (destination / "report.md").write_bytes(report)


def _mapping() -> dict[str, object]:
    return {
        "seed_text": "独立错误率为 0.5。",
        "seed_value": 0.5,
        "source_path": "experiment_v001/attempts/support/metrics.json",
        "json_pointer": "/records/0/value",
    }


def _seed(
    workspace: ResearchWorkspace,
    hypothesis_id: str,
    claim_id: str,
    *,
    mappings: list[dict[str, object]] | None = None,
    dispositions: list[dict[str, str]] | None = None,
    body: str = "独立错误率为 0.5。",
) -> None:
    workspace.write_seed(
        "# Seed\n\n"
        + body
        + "\n\n"
        + _metadata(
            hypothesis_id,
            claim_id,
            mappings=mappings,
            dispositions=dispositions,
        )
        + "\n"
    )


def _codes(payload: dict[str, object]) -> set[str]:
    return {item["code"] for item in payload["findings"]}


def _refresh_spec_snapshot(attempt: Path, **patch: object) -> None:
    spec_path = attempt / "spec.json"
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    spec.update(patch)
    _write_json(spec_path, spec)
    execution_path = attempt / "execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    data = spec_path.read_bytes()
    execution["experiment_spec"]["snapshot"]["size_bytes"] = len(data)
    execution["experiment_spec"]["snapshot"]["sha256"] = hashlib.sha256(data).hexdigest()
    _write_json(execution_path, execution)


def _rewrite_execution_schema(attempt: Path, schema: int) -> None:
    execution_path = attempt / "execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    execution["schema_version"] = schema
    if schema in {5, 6}:
        if schema == 5:
            for name in (
                "timed_out",
                "timeout_seconds",
                "termination_method",
                "process_tree_cleanup_ok",
            ):
                execution.pop(name)
        for name in (
            "metrics_contract_ok",
            "experiment_spec",
            "metrics",
            "budget_facts",
            "warnings",
        ):
            execution.pop(name)
    if schema in {5, 6, 7}:
        environment = execution["environment_facts"]
        runner = environment["runner"]
        legacy_environment = {
            "platform": environment["platform"],
            "python": runner["python"],
            "executable": runner["executable"]["path"],
        }
        if schema == 7:
            legacy_environment.update(
                {
                    "cpu_count": environment["cpu_count"],
                    "git": environment["git"],
                    "dependencies": runner["dependencies"],
                    "nvidia": environment["nvidia"],
                    "runner_and_modules": runner["runner_and_modules"],
                    "declared_facts": environment["declared_facts"],
                }
            )
        execution["environment_facts"] = legacy_environment
    _write_json(execution_path, execution)


def test_resolves_seed_refs_prior_attempt_independent_validation_and_numeric_mapping(
    tmp_path: Path,
) -> None:
    _, run, workspace, hypothesis_id, claim_id = _fixture(tmp_path)
    _prior(run, workspace, hypothesis_id)
    _seed(workspace, hypothesis_id, claim_id, mappings=[_mapping()])

    payload = audit_seed_support(
        workspace, ["support"], as_of_utc="2026-08-10T00:00:00Z"
    )
    codes = _codes(payload)

    assert {
        "seed_hypothesis_reference_resolved",
        "seed_claim_reference_resolved",
        "prior_audit_material_present",
        "supporting_attempt_bound",
        "independent_claim_validation_present",
        "seed_metric_mapping_resolved",
    } <= codes
    assert "independent_claim_validation_missing" not in codes
    assert "seed_numeric_literals_unmapped" not in codes
    assert {item["kind"] for item in payload["findings"]} <= {
        "finding",
        "warning",
        "missing",
    }
    rendered = render_seed_support_json(payload)
    assert "PASS" not in rendered and "FAIL" not in rendered
    assert payload["mechanical_effects"]["makes_delivery_judgment"] is False
    attempt_fact = payload["facts"]["supporting_attempts"][0]
    assert attempt_fact["schema_version"] == 8
    assert attempt_fact["hypothesis_id"] == hypothesis_id
    assert attempt_fact["claim_ids"] == [claim_id]
    assert attempt_fact["purpose"] == "independent_claim_validation"
    assert attempt_fact["metric_record_count"] == 1


def test_seed_support_preserves_schema_5_to_8_reading_semantics(
    tmp_path: Path,
) -> None:
    for schema in (5, 6, 7, 8):
        _, run, workspace, hypothesis_id, claim_id = _fixture(
            tmp_path / f"schema-{schema}"
        )
        _prior(run, workspace, hypothesis_id)
        _seed(workspace, hypothesis_id, claim_id, mappings=[_mapping()])
        _rewrite_execution_schema(
            run / "experiment_v001/attempts/support", schema
        )

        payload = audit_seed_support(
            workspace, ["support"], as_of_utc="2026-08-10T00:00:00Z"
        )
        codes = _codes(payload)
        attempt_fact = payload["facts"]["supporting_attempts"][0]
        assert attempt_fact["schema_version"] == schema
        assert "supporting_attempt_integrity_warning" not in codes
        if schema in {7, 8}:
            assert {
                "supporting_attempt_bound",
                "independent_claim_validation_present",
                "seed_metric_mapping_resolved",
            } <= codes
            assert attempt_fact["hypothesis_id"] == hypothesis_id
            assert attempt_fact["claim_ids"] == [claim_id]
            assert attempt_fact["purpose"] == "independent_claim_validation"
            assert attempt_fact["metric_record_count"] == 1
        else:
            assert {
                "supporting_attempt_spec_missing",
                "supporting_attempt_claim_binding_missing",
                "supporting_attempt_metrics_missing",
                "independent_claim_validation_missing",
            } <= codes
            assert "supporting_attempt_bound" not in codes
            assert "hypothesis_id" not in attempt_fact
            assert "claim_ids" not in attempt_fact


def test_stale_prior_empty_candidates_and_unknown_seed_refs_are_advisory(
    tmp_path: Path,
) -> None:
    _, run, workspace, hypothesis_id, claim_id = _fixture(tmp_path)
    _prior(
        run,
        workspace,
        hypothesis_id,
        created="2025-01-01T00:00:00Z",
        candidates=[],
    )
    _seed(workspace, "unknown-hypothesis", "unknown-claim", body="没有实验数字。")

    payload = audit_seed_support(
        workspace, [], as_of_utc="2026-08-10T00:00:00Z"
    )
    codes = _codes(payload)

    assert "prior_audit_stale" in codes
    assert "prior_candidates_missing" in codes
    assert "seed_hypothesis_reference_unknown" in codes
    assert "seed_claim_reference_unknown" in codes
    assert "supporting_attempts_missing" in codes
    assert payload["mechanical_effects"]["makes_novelty_judgment"] is False


def test_unmapped_or_mismatched_seed_number_is_visible(tmp_path: Path) -> None:
    _, run, workspace, hypothesis_id, claim_id = _fixture(tmp_path)
    _prior(run, workspace, hypothesis_id)
    mapping = _mapping()
    mapping["seed_text"] = "独立错误率为 0.9。"
    mapping["seed_value"] = 0.9
    _seed(
        workspace,
        hypothesis_id,
        claim_id,
        mappings=[mapping],
        body="独立错误率为 0.9。",
    )

    payload = audit_seed_support(
        workspace, ["support"], as_of_utc="2026-08-10T00:00:00Z"
    )
    assert "seed_metric_mapping_value_mismatch" in _codes(payload)
    assert "seed_numeric_literals_unmapped" in _codes(payload)


def test_baseline_mismatch_and_unknown_are_read_from_verified_comparison(
    tmp_path: Path,
) -> None:
    product, run, workspace, hypothesis_id, claim_id = _fixture(tmp_path)
    source = run / "workbench_v001/source.py"
    completed = record_successful_attempt(
        product, run, "v001", source, attempt_id="baseline"
    )
    assert completed.returncode == 0
    _refresh_spec_snapshot(
        run / "experiment_v001/attempts/baseline", model="different-model"
    )
    compare_attempts(workspace, "comparison-001", "support", ["baseline"])
    _prior(run, workspace, hypothesis_id)
    _seed(workspace, hypothesis_id, claim_id, mappings=[_mapping()])

    payload = audit_seed_support(
        workspace, ["support"], as_of_utc="2026-08-10T00:00:00Z"
    )
    codes = _codes(payload)
    assert "baseline_parity_mismatched" in codes
    assert "baseline_parity_unknown" in codes


def test_schema_2_comparison_fact_remains_a_seed_metric_mapping_source(
    tmp_path: Path,
) -> None:
    product, run, workspace, hypothesis_id, claim_id = _fixture(tmp_path)
    source = run / "workbench_v001/source.py"
    completed = record_successful_attempt(
        product, run, "v001", source, attempt_id="baseline"
    )
    assert completed.returncode == 0
    publication = compare_attempts(
        workspace, "comparison-aggregation-aware", "support", ["baseline"]
    )
    comparison = json.loads(
        (Path(publication.path) / "comparison.json").read_text(encoding="utf-8")
    )
    assert comparison["schema_version"] == 2
    assert comparison["metric_facts"][0]["comparisons"][0]["metric_key"][
        "aggregation"
    ] == "mean"
    _prior(run, workspace, hypothesis_id)
    mapping = {
        "seed_text": "候选减基线为 0.0。",
        "seed_value": 0.0,
        "source_path": (
            "experiment_v001/comparisons/comparison-aggregation-aware/comparison.json"
        ),
        "json_pointer": (
            "/metric_facts/0/comparisons/0/difference_candidate_minus_baseline"
        ),
    }
    _seed(
        workspace,
        hypothesis_id,
        claim_id,
        mappings=[mapping],
        body="候选减基线为 0.0。",
    )

    payload = audit_seed_support(
        workspace, ["support"], as_of_utc="2026-08-10T00:00:00Z"
    )

    assert "comparison_snapshot" in _codes(payload)
    assert "seed_metric_mapping_resolved" in _codes(payload)
    assert "seed_metric_mapping_value_mismatch" not in _codes(payload)


def test_falsified_claim_requires_explicit_seed_disposition_text(tmp_path: Path) -> None:
    _, run, workspace, hypothesis_id, claim_id = _fixture(tmp_path)
    _prior(run, workspace, hypothesis_id)
    update_claim(
        workspace,
        "plan-experiment-support",
        claim_id,
        {"status": "falsified", "status_reason": "测试显式复现反证。"},
    )
    _seed(workspace, hypothesis_id, claim_id, mappings=[_mapping()])

    missing = audit_seed_support(
        workspace, ["support"], as_of_utc="2026-08-10T00:00:00Z"
    )
    assert "falsified_claim_disposition_missing" in _codes(missing)

    disposition_text = f"`{claim_id}` 的反证已复现，因此 Seed 收缩该主张。"
    _seed(
        workspace,
        hypothesis_id,
        claim_id,
        mappings=[_mapping()],
        dispositions=[{"claim_id": claim_id, "seed_text": disposition_text}],
        body="独立错误率为 0.5。\n\n" + disposition_text,
    )
    explicit = audit_seed_support(
        workspace, ["support"], as_of_utc="2026-08-10T00:00:00Z"
    )
    assert "falsified_claim_disposition_present" in _codes(explicit)


def test_missing_independent_validation_and_tampered_attempt_remain_findings(
    tmp_path: Path,
) -> None:
    _, run, workspace, hypothesis_id, claim_id = _fixture(tmp_path)
    _prior(run, workspace, hypothesis_id)
    _seed(workspace, hypothesis_id, claim_id, mappings=[_mapping()])
    attempt = run / "experiment_v001/attempts/support"
    _refresh_spec_snapshot(attempt, purpose="mechanism_consistency")

    mechanism_only = audit_seed_support(
        workspace, ["support"], as_of_utc="2026-08-10T00:00:00Z"
    )
    assert "independent_claim_validation_missing" in _codes(mechanism_only)

    metrics = attempt / "metrics.json"
    metrics.write_bytes(metrics.read_bytes() + b" \n")
    tampered = audit_seed_support(
        workspace, ["support"], as_of_utc="2026-08-10T00:00:00Z"
    )
    assert "supporting_attempt_integrity_warning" in _codes(tampered)
    assert {item["kind"] for item in tampered["findings"]} <= {
        "finding",
        "warning",
        "missing",
    }


def test_optional_saved_markdown_requires_explicit_review_inclusion_and_keeps_hash_chain(
    tmp_path: Path,
) -> None:
    _, run, workspace, hypothesis_id, claim_id = _fixture(tmp_path)
    _prior(run, workspace, hypothesis_id)
    _seed(workspace, hypothesis_id, claim_id, mappings=[_mapping()])
    payload = audit_seed_support(
        workspace, ["support"], as_of_utc="2026-08-10T00:00:00Z"
    )

    saved = publish_seed_support_audit(workspace, payload, "audit-001")
    assert not workspace.review_path.exists()
    markdown = saved["markdown"]
    workspace.write_review_request("请独立审阅，不运行工具。", ["seed_v001.md", markdown])
    first = render_review_input(workspace)
    second = render_review_input(workspace)
    assert first == second
    assert (run / markdown).read_bytes() in first
    for number in (1, 2, 3):
        workspace.write_reviewer_report(number, f"fresh-{number}", f"独立意见 {number}")
    assert review_material_errors(workspace) == ()

    markdown_text = render_seed_support_markdown(payload)
    assert "第四" not in markdown_text
    assert "PASS" not in markdown_text and "FAIL" not in markdown_text


def test_cli_stdout_is_advisory_and_saved_paths_never_overwrite(
    tmp_path: Path, capsys
) -> None:
    product, run, workspace, hypothesis_id, claim_id = _fixture(tmp_path)
    _prior(run, workspace, hypothesis_id)
    _seed(workspace, hypothesis_id, claim_id, mappings=[_mapping()])
    arguments = [
        "--product-root",
        str(product),
        "--run-root",
        str(run),
        "--version",
        "v001",
        "--supporting-attempt",
        "support",
        "--as-of-utc",
        "2026-08-10T00:00:00Z",
        "--save-audit-id",
        "cli-001",
    ]
    assert main(arguments) == 0
    output = json.loads(capsys.readouterr().out)
    assert output["advisory_only"] is True
    before = {
        path.name: path.read_bytes()
        for path in (run / "audit_v001").iterdir()
    }
    assert main(arguments) == 2
    assert "already exists" in capsys.readouterr().err
    after = {
        path.name: path.read_bytes()
        for path in (run / "audit_v001").iterdir()
    }
    assert after == before
