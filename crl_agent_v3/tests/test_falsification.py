from __future__ import annotations

from pathlib import Path

import pytest

import crl_v3.falsification as falsification_module
from conftest import make_run
from crl_v3.falsification import (
    PARITY_FIELDS,
    add_claim,
    claim_from_mapping,
    create_experiment_spec,
    create_plan,
    experiment_spec_from_mapping,
    experiment_spec_warning_codes,
    read_plan,
    render_plan_markdown,
    update_claim,
    validate_repository,
)
from crl_v3.hypotheses import (
    add_hypothesis,
    create_hypothesis_record,
    empty_portfolio,
)
from crl_v3.workspace import ResearchWorkspace


def _hypothesis_payload(hypothesis_id: str) -> dict[str, object]:
    text = "明确科研记录"
    return {
        "hypothesis_id": hypothesis_id,
        "title": f"候选 {hypothesis_id}",
        "parent_ids": [],
        "lineage_note": "根候选",
        "problem": text,
        "target_failure": {
            "summary": text,
            "card_ids": ["failure-card-001"],
            "evidence_ids": [],
        },
        "changed_computation": {
            "baseline": text,
            "intervention": text,
            "information_available": text,
            "timing": text,
            "budget_effect": text,
        },
        "mechanism_claim": text,
        "falsifier": text,
        "minimal_killer_experiment": text,
        "nearest_prior_risk": text,
        "alternative_explanations": ["替代解释"],
        "descriptors": {
            "problem_family": text,
            "computation_stage": text,
            "intervention_family": text,
            "information_source": text,
            "timing_class": text,
            "budget_class": text,
            "evaluation_mode": text,
        },
        "literature_refs": ["paper-doi:10.1000/example"],
    }


def _workspace(
    tmp_path: Path,
    *,
    status: str = "ACTIVE",
    hypothesis_id: str = "h-001",
    run_name: str = "20260731_1200_run01",
) -> tuple[Path, Path, ResearchWorkspace]:
    product, run = make_run(tmp_path, status=status)
    if run.name != run_name:
        renamed = product / run_name
        run.rename(renamed)
        run = renamed
        for name in ("RUN_CHARTER.md", "RUN_STATUS.md"):
            path = run / name
            path.write_text(
                path.read_text(encoding="utf-8").replace(
                    "20260731_1200_run01", run_name
                ),
                encoding="utf-8",
                newline="\n",
            )
    workspace = ResearchWorkspace(run, product_root=product, version="v001")
    if status == "ACTIVE":
        document = workspace.write_hypotheses(
            empty_portfolio(run.name, "v001"),
            expected_sha256=None,
            create_only=True,
        )
        portfolio = add_hypothesis(
            document.portfolio,
            create_hypothesis_record(_hypothesis_payload(hypothesis_id)),
        )
        workspace.write_hypotheses(portfolio, expected_sha256=document.sha256)
    return product, run, workspace


def _claim(
    claim_id: str = "claim-001", *, killer: str = "experiment-001"
) -> dict[str, object]:
    return {
        "claim_id": claim_id,
        "claim_text": "该计算在声明范围内降低工具选择错误。",
        "scope": "固定工具集与相同信息条件",
        "observable": "独立标注的工具选择错误率",
        "falsifier": "错误率未达到预注册改善幅度。",
        "minimum_effect_or_decision_rule": "差值必须至少为 0.05，否则反证当前 Claim。",
        "alternative_explanations": ["提示长度差异", "采样波动"],
        "killer_experiment_id": killer,
        "supporting_experiment_ids": [],
        "status": "proposed",
        "status_reason": "主研究者提出，尚未运行实验。",
    }


def _plan(*claims: dict[str, object]) -> dict[str, object]:
    return {
        "hypothesis_id": "h-001",
        "plan_id": "plan-001",
        "claims": list(claims),
        "global_confounders": ["模型版本漂移", "任务难度不均"],
    }


def _parity() -> dict[str, object]:
    return {
        name: {
            "status": "unknown" if name == "budget" else "matched",
            "notes": "预算尚待校准" if name == "budget" else "按预注册保持一致",
        }
        for name in PARITY_FIELDS
    }


def _spec(
    experiment_id: str = "experiment-001",
    *,
    claim_ids: list[str] | None = None,
    hypothesis_id: str = "h-001",
    purpose: str = "independent_claim_validation",
) -> dict[str, object]:
    return {
        "experiment_id": experiment_id,
        "hypothesis_id": hypothesis_id,
        "claim_ids": claim_ids or ["claim-001"],
        "purpose": purpose,
        "research_question": "候选是否降低独立标签下的工具选择错误？",
        "independent_ground_truth": {
            "description": "由方法构造之外的人工标签给出正确工具。",
            "external_evidence_ids": [],
            "external_card_ids": ["failure-card-001"],
            "external_literature_refs": ["paper-doi:10.1000/example"],
            "run_local_fact_refs": ["workbench_v001/labels.json"],
        },
        "primary_metric": "独立标签上的工具选择错误率",
        "secondary_metrics": ["平均工具调用数"],
        "sampling_unit": "任务实例",
        "dataset": "Run-local 固定样本集",
        "model": "测试模型",
        "provider": "本地提供方",
        "revision": "固定修订版",
        "baseline_specs": ["相同模型、工具与信息的直接规划基线"],
        "parity_dimensions": _parity(),
        "seeds": [7, 11],
        "budget_ceiling": "每个方法至多 100 次模型调用",
        "expected_signatures": ["候选错误率下降至少 0.05"],
        "falsification_rule": "改善不足 0.05 即反证当前范围 Claim。",
        "confounders": ["任务顺序效应"],
        "declared_inputs": ["workbench_v001/labels.json"],
        "declared_outputs": ["experiment_v001/raw_metrics.json"],
    }


def test_plan_multiple_claims_and_three_purposes_use_fixed_paths(tmp_path: Path) -> None:
    _, run, workspace = _workspace(tmp_path)
    plan_document = create_plan(
        workspace,
        _plan(
            _claim("claim-001", killer="experiment-mechanism"),
            _claim("claim-002", killer="experiment-independent"),
            _claim("claim-003", killer="experiment-expansion"),
        ),
        now="2026-08-10T00:00:00Z",
    )
    assert Path(plan_document.path) == (
        run / "hypotheses_v001" / "falsification" / "plan-001.json"
    )
    assert len(plan_document.plan.claims) == 3

    for experiment_id, claim_id, purpose in (
        ("experiment-mechanism", "claim-001", "mechanism_consistency"),
        ("experiment-independent", "claim-002", "independent_claim_validation"),
        ("experiment-expansion", "claim-003", "expansion"),
    ):
        spec_document = create_experiment_spec(
            workspace,
            _spec(experiment_id, claim_ids=[claim_id], purpose=purpose),
        )
        assert Path(spec_document.path) == (
            run / "experiment_v001" / "specs" / f"{experiment_id}.json"
        )
        assert spec_document.spec.purpose == purpose
        assert spec_document.spec.schema_version == 2
        assert spec_document.spec.evidence_fidelity == "SCREENING"
        assert spec_document.spec.independent_implementation_count == 1
        assert spec_document.spec.subject_scope.models

    facts = validate_repository(workspace)
    assert facts == {
        "schema_version": 2,
        "plan_count": 1,
        "claim_count": 3,
        "experiment_spec_count": 3,
    }


def test_unknown_hypothesis_and_claim_are_rejected(tmp_path: Path) -> None:
    _, _, workspace = _workspace(tmp_path)
    unknown_plan = _plan()
    unknown_plan["hypothesis_id"] = "missing"
    with pytest.raises(KeyError, match="unknown hypothesis"):
        create_plan(workspace, unknown_plan)

    create_plan(workspace, _plan(_claim()))
    with pytest.raises(KeyError, match="unknown claim"):
        create_experiment_spec(
            workspace,
            _spec("unknown-claim-spec", claim_ids=["missing-claim"]),
        )


def test_duplicate_experiment_id_does_not_overwrite(tmp_path: Path) -> None:
    _, run, workspace = _workspace(tmp_path)
    create_plan(workspace, _plan(_claim()))
    first = create_experiment_spec(workspace, _spec())
    before = Path(first.path).read_bytes()
    duplicate = _spec()
    duplicate["research_question"] = "不得覆盖的另一问题"
    with pytest.raises(FileExistsError, match="already exists"):
        create_experiment_spec(workspace, duplicate)
    assert (run / "experiment_v001" / "specs" / "experiment-001.json").read_bytes() == before


def test_cross_run_document_and_run_local_path_escape_are_rejected(tmp_path: Path) -> None:
    _, _, first_workspace = _workspace(tmp_path / "first")
    _, second_run, second_workspace = _workspace(
        tmp_path / "second", run_name="20260731_1201_run02"
    )
    created = create_plan(first_workspace, _plan(_claim()))
    destination = second_run / "hypotheses_v001" / "falsification" / "plan-001.json"
    destination.parent.mkdir(parents=True)
    destination.write_bytes(Path(created.path).read_bytes())
    with pytest.raises(ValueError, match="run_id does not match"):
        read_plan(second_workspace, "plan-001")

    destination.unlink()
    create_plan(second_workspace, {**_plan(_claim()), "plan_id": "plan-002"})
    escaped = _spec()
    escaped["declared_inputs"] = ["../another-run/secret.json"]
    with pytest.raises(ValueError, match="safe relative path"):
        create_experiment_spec(second_workspace, escaped)


def test_illegal_parity_field_and_missing_primary_metric_are_rejected(tmp_path: Path) -> None:
    _, _, workspace = _workspace(tmp_path)
    create_plan(workspace, _plan(_claim()))
    bad_parity = _spec()
    bad_parity["parity_dimensions"]["quality_score"] = {
        "status": "matched",
        "notes": "非法自动科研字段",
    }
    with pytest.raises(ValueError, match="parity_dimensions fields"):
        create_experiment_spec(workspace, bad_parity)

    missing_metric = _spec()
    missing_metric.pop("primary_metric")
    with pytest.raises(ValueError, match="fields do not match"):
        create_experiment_spec(workspace, missing_metric)


def test_status_only_changes_explicitly_with_reason_and_results_do_not_change_it(
    tmp_path: Path,
) -> None:
    _, _, workspace = _workspace(tmp_path)
    created = create_plan(workspace, _plan(_claim()))
    with pytest.raises(ValueError, match="requires status_reason"):
        update_claim(workspace, "plan-001", "claim-001", {"status": "testing"})

    reason_only = update_claim(
        workspace,
        "plan-001",
        "claim-001",
        {"status_reason": "修正理由文本，但没有改变状态。"},
    )
    assert reason_only.plan.claims[0].status == "proposed"

    updated = update_claim(
        workspace,
        "plan-001",
        "claim-001",
        {"status": "testing", "status_reason": "开始执行预注册实验。"},
    )
    assert updated.plan.claims[0].status == "testing"
    workspace.write_experiment_result("实验完成，但 P5 工具不得自动解释结果。")
    reread = read_plan(workspace, "plan-001")
    assert reread.plan.claims[0].status == "testing"
    assert reread.sha256 != created.sha256


def test_atomic_update_failure_preserves_previous_plan(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, run, workspace = _workspace(tmp_path)
    original = create_plan(workspace, _plan(_claim()))

    def fail_replace(source: Path, destination: Path) -> None:
        raise OSError("injected atomic replace failure")

    monkeypatch.setattr(falsification_module, "_replace_file", fail_replace)
    with pytest.raises(OSError, match="replace failure"):
        update_claim(
            workspace,
            "plan-001",
            "claim-001",
            {"scope": "修改后的范围"},
        )
    assert read_plan(workspace, "plan-001").sha256 == original.sha256
    directory = run / "hypotheses_v001" / "falsification"
    assert not list(directory.glob(".*.tmp"))
    assert not list(directory.glob("*.lock"))


def test_closed_run_blocks_p5_writes(tmp_path: Path) -> None:
    product, run, workspace = _workspace(tmp_path)
    create_plan(workspace, _plan(_claim()))
    status_path = run / "RUN_STATUS.md"
    status_path.write_text(
        status_path.read_text(encoding="utf-8").replace("STATUS: ACTIVE", "STATUS: DELIVERED"),
        encoding="utf-8",
        newline="\n",
    )
    closed = ResearchWorkspace(run, product_root=product, version="v001")
    with pytest.raises(FileExistsError, match="read-only"):
        add_claim(closed, "plan-001", _claim("claim-002", killer="experiment-002"))
    with pytest.raises(FileExistsError, match="read-only"):
        create_experiment_spec(closed, _spec())


def test_render_is_deterministic_and_separates_authorities(tmp_path: Path) -> None:
    _, run, workspace = _workspace(tmp_path)
    plan = create_plan(workspace, _plan(_claim())).plan
    spec = create_experiment_spec(workspace, _spec()).spec
    portfolio = workspace.read_hypotheses()
    hypothesis = portfolio.portfolio.hypotheses[0]
    first = render_plan_markdown(plan, hypothesis=hypothesis, specs=(spec,))
    second = render_plan_markdown(plan, hypothesis=hypothesis, specs=(spec,))
    assert first == second
    assert "什么结果会杀死该 Claim" in first
    assert "主研究者声明的最便宜 killer experiment" in first
    assert "独立真值说明" in first
    assert "替代解释" in first
    assert "预算公平性未知项" in first
    assert "外部论文权威（不等同于 Run-local 实验事实）" in first
    assert "工具也不据此自动改变 Claim 状态" in first
    assert not (run / "seed_v001.md").exists()


def test_old_run_without_p5_files_remains_compatible(tmp_path: Path) -> None:
    _, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=run.parent, version="v001")
    assert validate_repository(workspace) == {
        "schema_version": 2,
        "plan_count": 0,
        "claim_count": 0,
        "experiment_spec_count": 0,
    }
    workspace.write_candidate("旧 Run 无 P5 文件时仍可正常使用。")
    assert (run / "candidate_v001.md").is_file()


def test_public_spec_validation_rejects_unsupported_purpose() -> None:
    mapping = {
        "schema_version": 1,
        "run_id": "20260731_1200_run01",
        "version": "v001",
        **_spec(purpose="automatic_scientific_judgment"),
    }
    with pytest.raises(ValueError, match="invalid experiment purpose"):
        experiment_spec_from_mapping(mapping)


def test_schema_1_experiment_spec_remains_readable_without_fidelity_fields() -> None:
    mapping = {
        "schema_version": 1,
        "run_id": "20260731_1200_run01",
        "version": "v001",
        **_spec(),
    }
    legacy = experiment_spec_from_mapping(mapping)
    assert legacy.schema_version == 1
    assert legacy.evidence_fidelity is None
    assert legacy.subject_scope.models == ()
    assert legacy.independent_implementation_count == 0


def test_representative_spec_with_empty_subject_scope_returns_advisory_warning(
    tmp_path: Path,
) -> None:
    _, _, workspace = _workspace(tmp_path)
    create_plan(workspace, _plan(_claim()))
    value = _spec()
    value.update(
        {
            "evidence_fidelity": "REPRESENTATIVE",
            "subject_scope": {
                "models": [],
                "tasks": [],
                "datasets": [],
                "seeds": [],
                "environment": "",
            },
            "independent_implementation_count": 2,
        }
    )
    spec = create_experiment_spec(workspace, value).spec
    assert experiment_spec_warning_codes(spec) == (
        "representative_subject_scope_empty",
    )


@pytest.mark.parametrize(
    "status",
    (
        "proposed",
        "testing",
        "falsified",
        "supported_locally",
        "scope_reduced",
        "unresolved",
    ),
)
def test_all_explicit_claim_statuses_are_supported(status: str) -> None:
    payload = _claim()
    payload["status"] = status
    payload["status_reason"] = f"主研究者显式记录状态 {status}。"
    assert claim_from_mapping(payload).status == status
