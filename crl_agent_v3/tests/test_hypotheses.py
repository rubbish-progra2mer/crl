from __future__ import annotations

import hashlib
from dataclasses import replace
from pathlib import Path

import pytest

import crl_v3.hypotheses as hypotheses_module
from conftest import (
    make_directory_reparse_point,
    make_file_symlink,
    make_run,
    set_current_version,
)
from crl_v3.hypotheses import (
    add_hypothesis,
    create_hypothesis_record,
    decision_warning_codes,
    empty_portfolio,
    portfolio_from_mapping,
    portfolio_to_dict,
    render_portfolio_markdown,
    transition_hypothesis,
    update_hypothesis,
    validate_portfolio,
)
from crl_v3.knowledge import Evidence
from crl_v3.workspace import ResearchWorkspace


class FakeStore:
    def __init__(self, *evidence: Evidence) -> None:
        self.items = {item.evidence_id: item for item in evidence}

    def get_evidence(self, evidence_id: str) -> Evidence | None:
        return self.items.get(evidence_id)


def _evidence(
    evidence_id: str = "E-001", *, current: bool = True, passage_current: bool | None = None
) -> Evidence:
    source = "论文中的外部证据。"
    return Evidence(
        evidence_id=evidence_id,
        paper_id="paper-001",
        fulltext_sha256="a" * 64,
        evidence_kind="author_fact",
        section="4",
        page_start=1,
        page_end=1,
        locator="page 1",
        source_content=source,
        source_content_sha256=hashlib.sha256(source.encode("utf-8")).hexdigest(),
        codex_note="用于机械绑定测试。",
        passage_id=None,
        passage_text_sha256=None,
        quote_start=None,
        quote_end=None,
        fulltext_is_current=current,
        passage_is_current=passage_current,
    )


def _record_payload(
    hypothesis_id: str,
    *,
    parents: list[str] | None = None,
    evidence_ids: list[str] | None = None,
    complete: bool = False,
) -> dict[str, object]:
    filled = "明确记录" if complete else ""
    return {
        "hypothesis_id": hypothesis_id,
        "title": f"候选 {hypothesis_id}" if complete else "",
        "parent_ids": parents or [],
        "lineage_note": "由父候选拆分、修复或合并。" if parents else "根候选。",
        "problem": filled,
        "target_failure": {
            "summary": filled,
            "card_ids": ["failure-card-001"] if complete else [],
            "evidence_ids": evidence_ids or [],
        },
        "changed_computation": {
            "baseline": filled,
            "intervention": filled,
            "information_available": filled,
            "timing": filled,
            "budget_effect": filled,
        },
        "mechanism_claim": filled,
        "falsifier": filled,
        "minimal_killer_experiment": filled,
        "nearest_prior_risk": filled,
        "alternative_explanations": ["替代解释"] if complete else [],
        "descriptors": {
            "problem_family": filled,
            "computation_stage": filled,
            "intervention_family": filled,
            "information_source": filled,
            "timing_class": filled,
            "budget_class": filled,
            "evaluation_mode": filled,
        },
        "literature_refs": ["paper-001"] if complete else [],
    }


def _decision(**overrides: object) -> dict[str, object]:
    value: dict[str, object] = {
        "evidence_fidelity": "SCREENING",
        "kill_target": "METHOD_CORE",
        "subject_scope": {
            "models": ["local-proxy"],
            "tasks": ["probe"],
            "datasets": ["fixture"],
            "seeds": ["1"],
            "environment": "local",
        },
        "independent_implementation_count": 1,
        "structural_refutation": False,
        "structural_refutation_reason": "",
        "killed": "当前方法核主张",
        "survives": "现象与评价机会仍需检查",
        "why": "筛选实验给出负结果。",
    }
    value.update(overrides)
    return value


def _workspace(
    tmp_path: Path, *, store: FakeStore | None = None, status: str = "ACTIVE"
) -> tuple[Path, Path, ResearchWorkspace]:
    product, run = make_run(tmp_path, status=status)
    workspace = ResearchWorkspace(
        run, knowledge_store=store, product_root=product, version="v001"
    )
    return product, run, workspace


def _init(workspace: ResearchWorkspace):
    return workspace.write_hypotheses(
        empty_portfolio(workspace.workspace_path.name, workspace.version),
        expected_sha256=None,
        create_only=True,
    )


def _add(workspace: ResearchWorkspace, document, payload: dict[str, object]):
    portfolio = add_hypothesis(
        document.portfolio,
        create_hypothesis_record(payload),
        knowledge_store=workspace.knowledge_store,
    )
    return workspace.write_hypotheses(portfolio, expected_sha256=document.sha256)


def test_portfolio_is_utf8_lf_atomic_and_can_hold_twenty_records(tmp_path: Path) -> None:
    _, run, workspace = _workspace(tmp_path)
    document = _init(workspace)
    for index in range(20):
        document = _add(workspace, document, _record_payload(f"hypothesis-{index:03d}"))

    data = (run / "hypotheses_v001" / "portfolio.json").read_bytes()
    assert not data.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in data
    assert len(document.portfolio.hypotheses) == 20
    assert len({item.hypothesis_id for item in document.portfolio.hypotheses}) == 20
    assert not list((run / "hypotheses_v001").glob(".*.tmp"))
    assert not (run / "candidate_v001.md").exists()


def test_split_repair_merge_lineage_and_cycle_rejection(tmp_path: Path) -> None:
    _, _, workspace = _workspace(tmp_path)
    document = _init(workspace)
    for payload in (
        _record_payload("root"),
        _record_payload("split-a", parents=["root"]),
        _record_payload("split-b", parents=["root"]),
        _record_payload("repair", parents=["split-a"]),
        _record_payload("merge", parents=["repair", "split-b"]),
    ):
        document = _add(workspace, document, payload)

    merge = document.portfolio.hypotheses[-1]
    assert merge.parent_ids == ("repair", "split-b")
    with pytest.raises(ValueError, match="cycle"):
        update_hypothesis(
            document.portfolio,
            "root",
            {"parent_ids": ["merge"]},
            knowledge_store=workspace.knowledge_store,
        )


def test_unknown_parent_and_duplicate_ids_are_rejected(tmp_path: Path) -> None:
    _, _, workspace = _workspace(tmp_path)
    document = _init(workspace)
    with pytest.raises(ValueError, match="unknown parents"):
        add_hypothesis(
            document.portfolio,
            create_hypothesis_record(_record_payload("child", parents=["missing"])),
        )
    document = _add(workspace, document, _record_payload("same"))
    with pytest.raises(ValueError, match="unique"):
        add_hypothesis(
            document.portfolio, create_hypothesis_record(_record_payload("same"))
        )


def test_unknown_stale_evidence_and_invalid_card_id_are_rejected(tmp_path: Path) -> None:
    store = FakeStore(_evidence(), _evidence("E-stale", current=False))
    _, _, workspace = _workspace(tmp_path, store=store)
    document = _init(workspace)
    with pytest.raises(KeyError, match="unknown evidence"):
        add_hypothesis(
            document.portfolio,
            create_hypothesis_record(
                _record_payload("unknown", evidence_ids=["E-missing"])
            ),
            knowledge_store=store,
        )
    with pytest.raises(ValueError, match="not current"):
        add_hypothesis(
            document.portfolio,
            create_hypothesis_record(
                _record_payload("stale", evidence_ids=["E-stale"])
            ),
            knowledge_store=store,
        )
    payload = _record_payload("bad-card", complete=True)
    payload["target_failure"]["card_ids"] = ["Bad/Card"]
    with pytest.raises(ValueError, match="invalid Card ID"):
        add_hypothesis(
            document.portfolio,
            create_hypothesis_record(payload),
            knowledge_store=store,
        )


def test_status_changes_only_by_transition_and_active_requires_record_completeness(
    tmp_path: Path,
) -> None:
    _, _, workspace = _workspace(tmp_path)
    document = _add(workspace, _init(workspace), _record_payload("draft"))
    with pytest.raises(ValueError, match="use transition"):
        update_hypothesis(document.portfolio, "draft", {"status": "active"})
    with pytest.raises(ValueError, match="record-incomplete"):
        transition_hypothesis(document.portfolio, "draft", "active", "开始检验")
    with pytest.raises(ValueError, match="invalid hypothesis status"):
        transition_hypothesis(document.portfolio, "draft", "accepted", "非法状态")

    complete_patch = _record_payload("ignored", complete=True)
    complete_patch.pop("hypothesis_id")
    completed = update_hypothesis(document.portfolio, "draft", complete_patch)
    active = transition_hypothesis(completed, "draft", "active", "主研究者显式采纳")
    assert active.hypotheses[0].status == "active"


def test_complete_record_can_transition_without_scientific_score(tmp_path: Path) -> None:
    _, _, workspace = _workspace(tmp_path)
    document = _add(workspace, _init(workspace), _record_payload("complete", complete=True))
    active = transition_hypothesis(
        document.portfolio, "complete", "active", "主研究者显式采纳"
    )
    assert active.hypotheses[0].status == "active"
    assert active.hypotheses[0].revision == 2
    serialized = str(portfolio_to_dict(active))
    assert "quality_score" not in serialized
    assert "publishability_score" not in serialized


def test_schema_2_decision_history_is_append_only_and_warns_without_judging(
    tmp_path: Path,
) -> None:
    _, _, workspace = _workspace(tmp_path)
    document = _add(
        workspace, _init(workspace), _record_payload("decision", complete=True)
    )
    active = transition_hypothesis(
        document.portfolio, "decision", "active", "主研究者采纳"
    )
    with pytest.raises(ValueError, match="requires decision metadata"):
        transition_hypothesis(active, "decision", "falsified", "负结果")
    falsified = transition_hypothesis(
        active,
        "decision",
        "falsified",
        "负结果",
        decision=_decision(),
    )
    history = falsified.hypotheses[0].decision_history
    assert [(item.from_status, item.to_status) for item in history] == [
        ("draft", "active"),
        ("active", "falsified"),
    ]
    assert decision_warning_codes(history[-1]) == (
        "screening_paper_level_kill_without_structural_refutation",
        "single_implementation_paper_level_kill",
    )
    assert portfolio_to_dict(falsified)["schema_version"] == 2


def test_structural_refutation_reason_and_representative_scope_are_mechanical(
    tmp_path: Path,
) -> None:
    _, _, workspace = _workspace(tmp_path)
    document = _add(
        workspace, _init(workspace), _record_payload("scope", complete=True)
    )
    active = transition_hypothesis(
        document.portfolio, "scope", "active", "主研究者采纳"
    )
    with pytest.raises(ValueError, match="structural_refutation_reason"):
        transition_hypothesis(
            active,
            "scope",
            "falsified",
            "结构反例",
            decision=_decision(
                structural_refutation=True,
                structural_refutation_reason="",
            ),
        )
    representative = _decision(
        evidence_fidelity="REPRESENTATIVE",
        kill_target="LOCAL_EMPIRICAL_CLAIM",
        independent_implementation_count=2,
        subject_scope={
            "models": [],
            "tasks": [],
            "datasets": [],
            "seeds": [],
            "environment": "",
        },
    )
    closed = transition_hypothesis(
        active,
        "scope",
        "falsified",
        "代表性声明",
        decision=representative,
    )
    assert decision_warning_codes(closed.hypotheses[0].decision_history[-1]) == (
        "representative_subject_scope_empty",
    )


def test_schema_1_portfolio_remains_readable_without_migration() -> None:
    portfolio = empty_portfolio("20260731_1200_run01", "v001")
    portfolio = add_hypothesis(
        portfolio, create_hypothesis_record(_record_payload("legacy"))
    )
    mapping = portfolio_to_dict(portfolio)
    mapping["schema_version"] = 1
    for record in mapping["hypotheses"]:
        record.pop("decision_history")
    legacy = portfolio_from_mapping(mapping)
    assert legacy.schema_version == 1
    assert legacy.hypotheses[0].decision_history == ()


def test_update_recursively_patches_structured_fields(tmp_path: Path) -> None:
    _, _, workspace = _workspace(tmp_path)
    document = _add(workspace, _init(workspace), _record_payload("patch"))
    updated = update_hypothesis(
        document.portfolio,
        "patch",
        {"changed_computation": {"intervention": "新计算"}},
    )
    record = updated.hypotheses[0]
    assert record.changed_computation.intervention == "新计算"
    assert record.changed_computation.baseline == ""
    assert record.revision == 2


def test_timestamp_order_uses_parsed_utc_instants_not_lexical_strings() -> None:
    created = "2026-01-01T00:00:00Z"
    later_fraction = "2026-01-01T00:00:00.1Z"
    portfolio = empty_portfolio("20260731_1200_run01", "v001", now=created)
    record = create_hypothesis_record(_record_payload("fraction"), now=created)
    portfolio = add_hypothesis(portfolio, record, now=later_fraction)
    record = replace(record, updated_at_utc=later_fraction)
    portfolio = replace(portfolio, hypotheses=(record,))

    validate_portfolio(portfolio)


def test_validate_portfolio_rechecks_public_dataclass_schema_types() -> None:
    portfolio = empty_portfolio("20260731_1200_run01", "v001")
    with pytest.raises(ValueError, match="non-negative integer"):
        validate_portfolio(replace(portfolio, revision=True))

    record = create_hypothesis_record(_record_payload("typed"))
    valid = add_hypothesis(portfolio, record)
    invalid_record = replace(record, problem=42)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="problem must be text"):
        validate_portfolio(replace(valid, hypotheses=(invalid_record,)))


def test_stale_sha_rejects_concurrent_overwrite(tmp_path: Path) -> None:
    _, _, workspace = _workspace(tmp_path)
    original = _init(workspace)
    first = add_hypothesis(
        original.portfolio, create_hypothesis_record(_record_payload("first"))
    )
    current = workspace.write_hypotheses(first, expected_sha256=original.sha256)
    stale = add_hypothesis(
        original.portfolio, create_hypothesis_record(_record_payload("stale"))
    )
    with pytest.raises(FileExistsError, match="changed since"):
        workspace.write_hypotheses(stale, expected_sha256=original.sha256)
    assert workspace.read_hypotheses().sha256 == current.sha256


def test_atomic_replace_failure_preserves_previous_portfolio(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, run, workspace = _workspace(tmp_path)
    original = _init(workspace)
    updated = add_hypothesis(
        original.portfolio, create_hypothesis_record(_record_payload("new"))
    )

    def fail_replace(source: Path, destination: Path) -> None:
        raise OSError("injected replace failure")

    monkeypatch.setattr(hypotheses_module, "_replace_file", fail_replace)
    with pytest.raises(OSError, match="replace failure"):
        workspace.write_hypotheses(updated, expected_sha256=original.sha256)
    assert workspace.read_hypotheses().sha256 == original.sha256
    assert not list((run / "hypotheses_v001").glob(".*.tmp"))
    assert not list((run / "hypotheses_v001").glob("*.lock"))


def test_closed_run_and_current_version_mismatch_block_writes(tmp_path: Path) -> None:
    for status in ("PAUSED_BY_USER", "DELIVERED", "CONCLUDED_NO_DELIVERY", "TERMINATED_BY_USER"):
        _, _, workspace = _workspace(tmp_path / status, status=status)
        with pytest.raises((PermissionError, FileExistsError)):
            _init(workspace)

    product, run = make_run(tmp_path / "version")
    set_current_version(run, "v002")
    old = ResearchWorkspace(run, product_root=product, version="v001")
    with pytest.raises(ValueError, match="CURRENT_VERSION"):
        _init(old)


def test_portfolio_content_version_mismatch_is_rejected(tmp_path: Path) -> None:
    _, run, workspace = _workspace(tmp_path)
    document = _init(workspace)
    data = (run / "hypotheses_v001" / "portfolio.json").read_text(encoding="utf-8")
    (run / "hypotheses_v001" / "portfolio.json").write_text(
        data.replace('"version": "v001"', '"version": "v002"'),
        encoding="utf-8",
        newline="\n",
    )
    with pytest.raises(ValueError, match="workspace version"):
        workspace.read_hypotheses()
    assert document.portfolio.version == "v001"


def test_render_is_deterministic_and_does_not_write_seed(tmp_path: Path) -> None:
    _, run, workspace = _workspace(tmp_path)
    document = _add(workspace, _init(workspace), _record_payload("render", complete=True))
    first = render_portfolio_markdown(document.portfolio)
    second = render_portfolio_markdown(document.portfolio)
    assert first == second
    assert "non-authoritative" in first
    assert "render" in first
    assert not (run / "seed_v001.md").exists()


def test_legacy_run_without_portfolio_remains_usable(tmp_path: Path) -> None:
    _, run, workspace = _workspace(tmp_path)
    assert workspace.read_hypotheses(required=False) is None
    workspace.write_candidate("旧 Run 的候选仍兼容。")
    assert (run / "candidate_v001.md").is_file()


def test_portfolio_file_symlink_is_rejected(tmp_path: Path) -> None:
    _, run, workspace = _workspace(tmp_path)
    directory = run / "hypotheses_v001"
    directory.mkdir()
    outside = tmp_path / "outside.json"
    outside.write_text("{}\n", encoding="utf-8", newline="\n")
    make_file_symlink(directory / "portfolio.json", outside)
    with pytest.raises(ValueError, match="reparse point"):
        workspace.read_hypotheses()


@pytest.mark.windows
def test_hypotheses_directory_junction_is_rejected_before_external_write(
    tmp_path: Path,
) -> None:
    _, run, workspace = _workspace(tmp_path)
    outside = tmp_path / "outside"
    make_directory_reparse_point(run / "hypotheses_v001", outside)
    with pytest.raises(ValueError, match="reparse point"):
        _init(workspace)
    assert not (outside / "portfolio.json").exists()
