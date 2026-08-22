from __future__ import annotations

from pathlib import Path

import pytest

from conftest import make_run, prepare_experiment_spec
from crl_v3.diagnosis import collect_diagnosis
from crl_v3.workspace import ResearchWorkspace


def _selection_context(best: str, strategy: str = "NO_DECLARED_CHANGE") -> str:
    return f"""## 当前最佳候选集合

{best.strip()}

## 新增正向证据

UNAVAILABLE

## 已失效或被杀范围

UNAVAILABLE

## 剩余致命不确定性

UNKNOWN

## 下一项最高信息量动作

INSUFFICIENT

## 策略变化

{strategy.strip()}
"""


def _pair(a: str, b: str, verdict: str, *, suffix: str) -> str:
    return f"""PAIRWISE_COMPARISON:
  PAIR: {a} | {b}
  VERDICT: {verdict}
  DECISIVE_EVIDENCE: doi:10.1000/evidence-{suffix}
  A_SURVIVING_ADVANTAGES: A-{suffix}
  B_SURVIVING_ADVANTAGES: B-{suffix}
  SURVIVING_FATAL_UNCERTAINTIES: uncertainty-{suffix}
  REVERSAL_CONDITION: reversal-{suffix}
  NEXT_DISCRIMINATING_ACTION: action-{suffix}
"""


def _admission(candidate_id: str) -> str:
    return f"""CANDIDATE_ADMISSION: {candidate_id}
  TARGET_CLAIM: claim-{candidate_id}
  CONTRIBUTION_COORDINATE: coordinate-{candidate_id}
  CHANGED_COMPUTATION: computation-{candidate_id}
  RESEARCH_ARTIFACT: candidate_v001.md
  STRONGEST_CONSTRUCTIVE_BASELINE: baseline-{candidate_id}
  FATAL_UNCERTAINTY: uncertainty-{candidate_id}
  REVERSAL_TEST: reversal-{candidate_id}
"""


def _reward(candidate_id: str) -> str:
    return f"""LOCAL_REWARD_CONTRACT: {candidate_id}
  PRIMARY_OBSERVABLE: observable-{candidate_id}
  STRONG_BASELINE: baseline-{candidate_id}
  METRIC_DIRECTION: higher-is-better
  MINIMUM_MEANINGFUL_DELTA: 0.02
  REPETITIONS_OR_UNCERTAINTY: three-seeds-and-interval
  FAILURE_NEGATIVE_INCONCLUSIVE: explicit-three-way-rule
  EXECUTION_COST: one-local-hour
  LOW_FIDELITY_SCOPE: screening-only
  INDEPENDENT_ADMISSION_CHECK: held-out-probe
  SCALE_BRIDGE_ASSUMPTION: ordering-survives-scale
  MUTATION_ACCEPTANCE_CONDITION: exceeds-delta-without-regression
"""


def _implementation(
    candidate_id: str,
    implementation_id: str,
    artifact_path: str,
    session_id: str,
    frozen_path: str,
    fidelity_path: str,
) -> str:
    return f"""INDEPENDENT_IMPLEMENTATION: {candidate_id}
  IMPLEMENTATION_ID: {implementation_id}
  ARTIFACT_PATH: {artifact_path}
  FRESH_SESSION_ID: {session_id}
  FROZEN_CANDIDATE_PATH: {frozen_path}
  FIDELITY_CHECK_PATH: {fidelity_path}
"""


def _write_run_file(run: Path, relative: str, content: str = "trace\n") -> None:
    path = run / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8", newline="\n")


def _preference_facts(workspace: ResearchWorkspace, diagnosis_id: str) -> dict[str, object]:
    return collect_diagnosis(workspace, diagnosis_id)["facts"]["current_version"][
        "selection_context"
    ]["candidate_preference"]


def test_diagnosis_parses_incumbents_challengers_and_all_four_verdicts(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    best = """INCUMBENT_SET: candidate-a, candidate-b
CHALLENGERS:
- candidate-c
- candidate-d

""" + "\n".join(
        (
            _pair("candidate-a", "candidate-b", "A_PREFERRED", suffix="a"),
            _pair("candidate-a", "candidate-c", "B_PREFERRED", suffix="b"),
            _pair("candidate-b", "candidate-c", "INCOMPARABLE", suffix="c"),
            _pair(
                "candidate-c",
                "candidate-d",
                "INSUFFICIENT_EVIDENCE",
                suffix="d",
            ),
        )
    )
    workspace.write_selection_context(_selection_context(best))

    preference = _preference_facts(workspace, "four-verdicts")

    assert preference["incumbent_set"]["candidate_ids"] == [
        "candidate-a",
        "candidate-b",
    ]
    assert preference["challengers"]["candidate_ids"] == [
        "candidate-c",
        "candidate-d",
    ]
    assert [item["verdict"] for item in preference["pairwise_comparisons"]] == [
        "A_PREFERRED",
        "B_PREFERRED",
        "INCOMPARABLE",
        "INSUFFICIENT_EVIDENCE",
    ]
    assert [
        item["winner_candidate_id"]
        for item in preference["pairwise_comparisons"]
    ] == ["candidate-a", "candidate-c", None, None]
    incomparable = preference["pairwise_comparisons"][2]
    assert incomparable["verdict"] == "INCOMPARABLE"
    assert incomparable["winner_candidate_id"] is None
    insufficient = preference["pairwise_comparisons"][3]
    assert insufficient["fields"]["NEXT_DISCRIMINATING_ACTION"]["value"] == (
        "action-d"
    )


def test_same_unordered_pair_with_opposite_declared_verdicts_is_ambiguous(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    for relative in (
        "candidate_v001.md",
        "implementation_v001/a.py",
        "workbench_v001/fidelity-a.md",
    ):
        _write_run_file(run, relative, f"{relative}\n")
    best = f"""INCUMBENT_SET: candidate-a
CHALLENGERS: candidate-b

{_pair('candidate-a', 'candidate-b', 'A_PREFERRED', suffix='conflict-a')}
{_pair('candidate-a', 'candidate-b', 'B_PREFERRED', suffix='conflict-b')}
{_implementation('candidate-a', 'a-1', 'implementation_v001/a.py', 'declared-a', 'candidate_v001.md', 'workbench_v001/fidelity-a.md')}
"""
    workspace.write_selection_context(_selection_context(best))

    preference = _preference_facts(workspace, "unordered-pair-conflict")
    comparisons = preference["pairwise_comparisons"]

    assert [item["verdict"] for item in comparisons] == [
        "A_PREFERRED",
        "B_PREFERRED",
    ]
    assert all(item["normalized_pair"] == ["candidate-a", "candidate-b"] for item in comparisons)
    assert all(item["status"] == "AMBIGUOUS" for item in comparisons)
    assert all(item["winner_candidate_id"] is None for item in comparisons)
    assert all(
        item["mechanically_usable_for_inference"] is False
        for item in comparisons
    )
    assert preference["single_implementation_idea_level_risks"] == []
    assert any(
        item["code"] == "pairwise_group_verdict_conflict"
        for item in preference["advisories"]
    )


def test_reversed_pair_label_is_mapped_to_actual_candidate_identity(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_selection_context(
        _selection_context(
            "INCUMBENT_SET: candidate-a\nCHALLENGERS: candidate-b\n\n"
            + _pair(
                "candidate-b",
                "candidate-a",
                "A_PREFERRED",
                suffix="reversed",
            )
        )
    )

    comparison = _preference_facts(workspace, "reversed-pair-identity")[
        "pairwise_comparisons"
    ][0]

    assert comparison["normalized_pair"] == ["candidate-a", "candidate-b"]
    assert comparison["declared_preferred_candidate_id"] == "candidate-b"
    assert comparison["winner_candidate_id"] == "candidate-b"


def test_repeated_same_actual_verdict_is_preserved_with_advisory(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    best = "INCUMBENT_SET: candidate-a\nCHALLENGERS: candidate-b\n\n" + "\n".join(
        (
            _pair("candidate-a", "candidate-b", "A_PREFERRED", suffix="same-a"),
            _pair("candidate-b", "candidate-a", "B_PREFERRED", suffix="same-b"),
        )
    )
    workspace.write_selection_context(_selection_context(best))

    preference = _preference_facts(workspace, "repeated-same-actual-verdict")
    comparisons = preference["pairwise_comparisons"]

    assert len(comparisons) == 2
    assert all(item["status"] == "PRESENT" for item in comparisons)
    assert all(item["winner_candidate_id"] == "candidate-a" for item in comparisons)
    assert any(
        item["code"] == "pairwise_group_repeated_same_verdict"
        for item in preference["advisories"]
    )


def test_preferred_verdict_with_unverified_decisive_evidence_has_no_winner(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    best = """INCUMBENT_SET: candidate-a
CHALLENGERS: candidate-b

PAIRWISE_COMPARISON:
  PAIR: candidate-a | candidate-b
  VERDICT: A_PREFERRED
  DECISIVE_EVIDENCE: workbench_v001/missing-decisive.md
  A_SURVIVING_ADVANTAGES: declared-a
  B_SURVIVING_ADVANTAGES: declared-b
  SURVIVING_FATAL_UNCERTAINTIES: declared-uncertainty
  REVERSAL_CONDITION: declared-reversal
  NEXT_DISCRIMINATING_ACTION: declared-next-action
"""
    workspace.write_selection_context(_selection_context(best))

    comparison = _preference_facts(workspace, "unverified-preferred-evidence")[
        "pairwise_comparisons"
    ][0]

    assert comparison["verdict"] == "A_PREFERRED"
    assert comparison["declared_preferred_candidate_id"] == "candidate-a"
    assert comparison["fields"]["DECISIVE_EVIDENCE"]["status"] == "UNVERIFIED"
    assert comparison["status"] == "UNKNOWN"
    assert comparison["mechanically_usable_for_inference"] is False
    assert comparison["winner_candidate_id"] is None


def test_missing_pairwise_and_admission_fields_are_advisory_and_facts_only(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_candidate("# Candidate\n\nFrozen candidate facts.\n")
    workspace.write_selection_context(
        _selection_context(
            """INCUMBENT_SET: candidate-a
CHALLENGERS: candidate-b

PAIRWISE_COMPARISON:
  PAIR: candidate-a | candidate-b
  VERDICT: INSUFFICIENT_EVIDENCE

CANDIDATE_ADMISSION: candidate-a
  TARGET_CLAIM: claim-a
"""
        )
    )
    protected = {
        name: (run / name).read_bytes()
        for name in (
            "RUN_STATUS.md",
            "RUN_LEDGER.md",
            "candidate_v001.md",
            "selection_context_v001.md",
        )
    }

    preference = _preference_facts(workspace, "missing-advisories")

    unresolved_fields = {
        item["field"]
        for item in preference["advisories"]
        if item["code"] == "pairwise_required_field_unresolved"
    }
    assert {
        "DECISIVE_EVIDENCE",
        "SURVIVING_FATAL_UNCERTAINTIES",
        "REVERSAL_CONDITION",
        "NEXT_DISCRIMINATING_ACTION",
    } <= unresolved_fields
    admission = preference["candidate_admission_contracts"][0]
    assert "CONTRIBUTION_COORDINATE" in admission["missing_fields"]
    assert any(
        item["code"] == "candidate_admission_contract_fields_missing"
        for item in preference["advisories"]
    )
    for name, before in protected.items():
        assert (run / name).read_bytes() == before
    assert "STATUS: ACTIVE" in (run / "RUN_STATUS.md").read_text(encoding="utf-8")
    assert not (run / "NO_DELIVERY.md").exists()


def test_local_activity_requires_declared_local_reward_contract(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    prepare_experiment_spec(product, run, experiment_id="local")
    workspace = ResearchWorkspace(run, product_root=product)
    candidate_id = "hypothesis-local"
    workspace.write_selection_context(
        _selection_context(
            f"""INCUMBENT_SET: {candidate_id}
CHALLENGERS: EMPTY

{_admission(candidate_id)}
EVIDENCE_ROLE: {candidate_id}
  DEVELOPMENT_EVIDENCE: workbench_v001/development.md
  ADMISSION_EVIDENCE: workbench_v001/admission.md
"""
        )
    )

    preference = _preference_facts(workspace, "reward-missing")

    assert preference["candidate_admission_contracts"][0]["resolved_complete"] is True
    assert any(
        item["code"] == "local_reward_contract_missing_for_local_activity"
        and item["candidate_id"] == candidate_id
        for item in preference["advisories"]
    )


def test_complete_local_reward_contract_is_parsed_without_missing_advisory(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    prepare_experiment_spec(product, run, experiment_id="rewarded")
    workspace = ResearchWorkspace(run, product_root=product)
    candidate_id = "hypothesis-rewarded"
    workspace.write_selection_context(
        _selection_context(
            f"""INCUMBENT_SET: {candidate_id}
CHALLENGERS: EMPTY

{_admission(candidate_id)}
{_reward(candidate_id)}
EVIDENCE_ROLE: {candidate_id}
  DEVELOPMENT_EVIDENCE: workbench_v001/development.md
  ADMISSION_EVIDENCE: workbench_v001/admission.md
"""
        )
    )

    preference = _preference_facts(workspace, "reward-complete")

    reward = preference["local_reward_contracts"][0]
    assert reward["declared_complete"] is True
    assert reward["resolved_complete"] is True
    assert len(reward["fields"]) == 11
    assert not any(
        item["code"].startswith("local_reward_contract_fields_")
        for item in preference["advisories"]
    )


def test_development_and_admission_evidence_roles_preserve_overlap_fact(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    for relative in (
        "workbench_v001/shared.md",
        "workbench_v001/development.md",
        "workbench_v001/admission.md",
    ):
        _write_run_file(run, relative)
    workspace.write_selection_context(
        _selection_context(
            """INCUMBENT_SET: candidate-a
CHALLENGERS: candidate-b

EVIDENCE_ROLE: candidate-a
  DEVELOPMENT_EVIDENCE: workbench_v001/shared.md
  ADMISSION_EVIDENCE: workbench_v001/shared.md

EVIDENCE_ROLE: candidate-b
  DEVELOPMENT_EVIDENCE: workbench_v001/development.md
  ADMISSION_EVIDENCE: workbench_v001/admission.md
"""
        )
    )

    preference = _preference_facts(workspace, "evidence-roles")
    roles = {item["candidate_id"]: item for item in preference["evidence_roles"]}

    assert roles["candidate-a"]["reference_relationship"] == "OVERLAP"
    assert roles["candidate-a"]["overlapping_references"] == [
        "workbench_v001/shared.md"
    ]
    assert roles["candidate-b"]["reference_relationship"] == "DISTINCT_DECLARATIONS"
    assert roles["candidate-b"]["interpretation_policy"] == (
        "declared_references_and_verified_files_do_not_establish_scientific_independence"
    )


def test_implementation_counting_uses_artifact_bytes_not_declared_sessions_or_paths(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    _write_run_file(run, "candidate_v001.md", "frozen candidate\n")
    _write_run_file(run, "implementation_v001/a.py", "same-a-bytes\n")
    _write_run_file(run, "implementation_v001/a-copy.py", "same-a-bytes\n")
    _write_run_file(run, "implementation_v001/b1.py", "b-one\n")
    _write_run_file(run, "implementation_v001/b2.py", "b-two\n")
    for relative in (
        "workbench_v001/fidelity-a1.md",
        "workbench_v001/fidelity-a2.md",
        "workbench_v001/fidelity-b1.md",
        "workbench_v001/fidelity-b2.md",
        "workbench_v001/evidence-impl.md",
    ):
        _write_run_file(run, relative, f"{relative}\n")
    best = f"""INCUMBENT_SET: candidate-a
CHALLENGERS: candidate-b

{_pair('candidate-a', 'candidate-b', 'A_PREFERRED', suffix='impl')}
{_implementation('candidate-a', 'a-1', 'implementation_v001/a.py', 'session-a-1', 'candidate_v001.md', 'workbench_v001/fidelity-a1.md')}
    {_implementation('candidate-a', 'a-2', 'implementation_v001/a-copy.py', 'session-a-2', 'candidate_v001.md', 'workbench_v001/fidelity-a2.md')}
{_implementation('candidate-b', 'b-1', 'implementation_v001/b1.py', 'session-b-1', 'candidate_v001.md', 'workbench_v001/fidelity-b1.md')}
{_implementation('candidate-b', 'b-2', 'implementation_v001/b2.py', 'session-b-2', 'candidate_v001.md', 'workbench_v001/fidelity-b2.md')}
"""
    workspace.write_selection_context(_selection_context(best))

    preference = _preference_facts(workspace, "implementation-counting")
    summaries = {
        item["candidate_id"]: item
        for item in preference["independent_implementation_summaries"]
    }

    assert summaries["candidate-a"]["verified_artifact_count"] == 1
    assert summaries["candidate-a"]["declared_session_id_count"] == 2
    assert summaries["candidate-a"]["scientific_independence_certified"] is False
    assert summaries["candidate-b"]["verified_artifact_count"] == 2
    implementations = preference["independent_implementations"]
    assert implementations[0]["fields"]["ARTIFACT_PATH"]["evidence_class"] == (
        "VERIFIED_ARTIFACT"
    )
    assert implementations[0]["fields"]["FRESH_SESSION_ID"]["evidence_class"] == (
        "DECLARED_SESSION"
    )
    assert implementations[0]["fields"]["ARTIFACT_PATH"]["sha256"] == (
        implementations[1]["fields"]["ARTIFACT_PATH"]["sha256"]
    )
    assert any(
        item["code"] == "duplicate_implementation_artifact_bytes"
        and item["record_index"] == 2
        for item in preference["advisories"]
    )
    for field_name in (
        "ARTIFACT_PATH",
        "FROZEN_CANDIDATE_PATH",
        "FIDELITY_CHECK_PATH",
    ):
        assert implementations[0]["fields"][field_name]["sha256"]
    assert any(
        item["code"] == "single_implementation_idea_level_preference"
        and item["candidate_id"] == "candidate-a"
        for item in preference["single_implementation_idea_level_risks"]
    )
    report = (
        run / "workbench_v001" / "diagnosis" / "implementation-counting" / "report.md"
    ).read_text(encoding="utf-8")
    assert "DECLARED_SESSION" in report
    assert "VERIFIED_ARTIFACT" in report
    assert "脚本不能认证真实会话隔离或科学独立性" in report
    assert "qualified fresh-session" not in report


@pytest.mark.parametrize(
    "exception_type", ["MECHANICALLY_UNIQUE", "STRUCTURAL_REFUTATION"]
)
def test_explicit_file_backed_implementation_lottery_exceptions_are_preserved(
    tmp_path: Path, exception_type: str
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    for relative in (
        "candidate_v001.md",
        "implementation_v001/a.py",
        "workbench_v001/fidelity-a.md",
        "workbench_v001/exception-evidence.md",
        "workbench_v001/evidence-exception.md",
    ):
        _write_run_file(run, relative)
    best = f"""INCUMBENT_SET: candidate-a
CHALLENGERS: candidate-b

{_pair('candidate-a', 'candidate-b', 'A_PREFERRED', suffix='exception')}
{_implementation('candidate-a', 'a-1', 'implementation_v001/a.py', 'session-a-1', 'candidate_v001.md', 'workbench_v001/fidelity-a.md')}
IMPLEMENTATION_LOTTERY_EXCEPTION: candidate-a
  TYPE: {exception_type}
  REASON: explicit-test-reason
  EVIDENCE_PATH: workbench_v001/exception-evidence.md
"""
    workspace.write_selection_context(_selection_context(best))

    preference = _preference_facts(workspace, f"exception-{exception_type.lower()}")

    assert preference["implementation_lottery_exceptions"][0]["valid"] is True
    assert not any(
        item.get("candidate_id") == "candidate-a"
        and item["code"] == "single_implementation_idea_level_preference"
        for item in preference["single_implementation_idea_level_risks"]
    )


def _updates(*, third_after: str = "A_PREFERRED", third_reduced: str = "NO") -> str:
    blocks = []
    for index in range(1, 4):
        after = third_after if index == 3 else "A_PREFERRED"
        reduced = third_reduced if index == 3 else "NO"
        blocks.append(
            f"""PREFERENCE_UPDATE:
  ACTION_ID: action-{index}
  AFFECTED_PAIR: candidate-a | candidate-b
  VERDICT_BEFORE: A_PREFERRED
  VERDICT_AFTER: {after}
  FATAL_UNCERTAINTY_REDUCED: {reduced}
  EVIDENCE_PATHS: doi:10.1000/action-{index}
  STOP_REPEATING: repeated-action-{index}
  EXPANDED_COORDINATE: coordinate-{index}
"""
        )
    return "\n".join(blocks)


def test_three_unchanged_updates_emit_preference_stagnation_warning(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_selection_context(
        _selection_context(
            "INCUMBENT_SET: candidate-a\nCHALLENGERS: candidate-b",
            _updates(),
        )
    )
    status_before = (run / "RUN_STATUS.md").read_bytes()
    result = collect_diagnosis(workspace, "preference-stagnation")
    preference = result["facts"]["current_version"]["selection_context"][
        "candidate_preference"
    ]

    assert preference["preference_stagnation"] == {
        "assessment_status": "READY",
        "warning": True,
        "warning_code": "PREFERENCE_STAGNATION_WARNING",
        "evaluated_action_ids": ["action-1", "action-2", "action-3"],
        "selected_action_last_positions": [1, 2, 3],
        "required_researcher_response": {
            "update_selection_context": True,
            "declare_stop_repeating": True,
            "expand_contribution_coordinate": True,
            "declare_new_discriminating_action": True,
            "run_status_policy": "KEEP_ACTIVE",
        },
    }
    report = (Path(result["path"]) / "report.md").read_text(encoding="utf-8")
    assert "## PREFERENCE_STAGNATION_WARNING" in report
    assert "Run 保持 ACTIVE" in report
    assert (run / "RUN_STATUS.md").read_bytes() == status_before


def test_repeated_pair_updates_for_one_action_do_not_count_as_three_actions(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    repeated_action = _updates().replace("ACTION_ID: action-2", "ACTION_ID: action-1")
    repeated_action = repeated_action.replace("ACTION_ID: action-3", "ACTION_ID: action-1")
    workspace.write_selection_context(
        _selection_context(
            "INCUMBENT_SET: candidate-a\nCHALLENGERS: candidate-b",
            repeated_action,
        )
    )

    preference = _preference_facts(workspace, "one-repeated-action")

    assert preference["preference_stagnation"] == {
        "assessment_status": "INSUFFICIENT_HISTORY",
        "warning": False,
        "warning_code": None,
        "evaluated_action_ids": ["action-1"],
        "selected_action_last_positions": [3],
    }


@pytest.mark.parametrize(
    ("third_after", "third_reduced"),
    (("B_PREFERRED", "NO"), ("A_PREFERRED", "YES")),
)
def test_changed_verdict_or_reduced_uncertainty_clears_stagnation_warning(
    tmp_path: Path, third_after: str, third_reduced: str
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_selection_context(
        _selection_context(
            "INCUMBENT_SET: candidate-a\nCHALLENGERS: candidate-b",
            _updates(third_after=third_after, third_reduced=third_reduced),
        )
    )

    preference = _preference_facts(
        workspace, f"no-stagnation-{third_after.lower()}-{third_reduced.lower()}"
    )

    assert preference["preference_stagnation"]["assessment_status"] == "READY"
    assert preference["preference_stagnation"]["warning"] is False
    assert preference["preference_stagnation"]["warning_code"] is None


def test_unverified_preference_update_evidence_cannot_fake_progress(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    blocks = []
    for index in range(1, 4):
        blocks.append(
            f"""PREFERENCE_UPDATE:
  ACTION_ID: fake-progress-{index}
  AFFECTED_PAIR: candidate-a | candidate-b
  VERDICT_BEFORE: A_PREFERRED
  VERDICT_AFTER: B_PREFERRED
  FATAL_UNCERTAINTY_REDUCED: NO
  EVIDENCE_PATHS: workbench_v001/missing-progress-{index}.md
  STOP_REPEATING: declared-stop-{index}
  EXPANDED_COORDINATE: declared-coordinate-{index}
"""
        )
    workspace.write_selection_context(
        _selection_context(
            "INCUMBENT_SET: candidate-a\nCHALLENGERS: candidate-b",
            "\n".join(blocks),
        )
    )

    preference = _preference_facts(workspace, "unverified-update-progress")
    updates = preference["preference_updates"]
    stagnation = preference["preference_stagnation"]

    assert all(item["status"] == "UNKNOWN" for item in updates)
    assert all(item["evaluable_for_stagnation"] is False for item in updates)
    assert all(item["verdict_changed"] is None for item in updates)
    assert all(
        item["fields"]["EVIDENCE_PATHS"]["status"] == "UNVERIFIED"
        for item in updates
    )
    assert stagnation["assessment_status"] == "UNKNOWN"
    assert stagnation["warning"] is False
    assert any(
        item["code"] == "preference_update_unverified_evidence_not_evaluable"
        for item in preference["advisories"]
    )


def test_conflicting_duplicate_updates_for_same_action_and_unordered_pair_are_ambiguous(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    strategy = """PREFERENCE_UPDATE:
  ACTION_ID: duplicate-action
  AFFECTED_PAIR: candidate-a | candidate-b
  VERDICT_BEFORE: A_PREFERRED
  VERDICT_AFTER: A_PREFERRED
  FATAL_UNCERTAINTY_REDUCED: NO
  EVIDENCE_PATHS: doi:10.1000/duplicate-one
  STOP_REPEATING: declared-stop-one
  EXPANDED_COORDINATE: declared-coordinate-one

PREFERENCE_UPDATE:
  ACTION_ID: duplicate-action
  AFFECTED_PAIR: candidate-b | candidate-a
  VERDICT_BEFORE: B_PREFERRED
  VERDICT_AFTER: A_PREFERRED
  FATAL_UNCERTAINTY_REDUCED: NO
  EVIDENCE_PATHS: arXiv:2401.12345
  STOP_REPEATING: declared-stop-two
  EXPANDED_COORDINATE: declared-coordinate-two
"""
    workspace.write_selection_context(
        _selection_context(
            "INCUMBENT_SET: candidate-a\nCHALLENGERS: candidate-b",
            strategy,
        )
    )

    preference = _preference_facts(workspace, "conflicting-duplicate-updates")
    updates = preference["preference_updates"]

    assert all(
        item["normalized_affected_pair"] == ["candidate-a", "candidate-b"]
        for item in updates
    )
    assert all(item["status"] == "AMBIGUOUS" for item in updates)
    assert all(item["evaluable_for_stagnation"] is False for item in updates)
    assert all(item["verdict_changed"] is None for item in updates)
    assert any(
        item["code"] == "preference_update_group_conflict"
        for item in preference["advisories"]
    )


def test_candidate_set_repetitions_are_preserved_without_merging_conflicts(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_selection_context(
        _selection_context(
            """INCUMBENT_SET: candidate-a
INCUMBENT_SET: candidate-b
CHALLENGERS: candidate-c
CHALLENGERS: candidate-c
"""
        )
    )

    preference = _preference_facts(workspace, "candidate-set-repetitions")

    incumbent = preference["incumbent_set"]
    assert incumbent["status"] == "AMBIGUOUS"
    assert incumbent["candidate_ids"] == []
    assert incumbent["occurrence_count"] == 2
    assert [item["candidate_ids"] for item in incumbent["declarations"]] == [
        ["candidate-a"],
        ["candidate-b"],
    ]
    challenger = preference["challengers"]
    assert challenger["status"] == "PRESENT"
    assert challenger["candidate_ids"] == ["candidate-c"]
    assert challenger["occurrence_count"] == 2
    assert challenger["repetition"] == "IDENTICAL"
    assert {item["code"] for item in preference["advisories"]} >= {
        "candidate_set_declaration_conflict",
        "candidate_set_declaration_repeated",
    }


def test_single_candidate_set_declaration_cannot_mix_empty_and_candidate_id(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_selection_context(
        _selection_context(
            "INCUMBENT_SET: EMPTY, candidate-a\nCHALLENGERS: NONE"
        )
    )

    preference = _preference_facts(workspace, "mixed-empty-candidate-set")
    incumbent = preference["incumbent_set"]

    assert incumbent["status"] == "AMBIGUOUS"
    assert incumbent["candidate_ids"] == []
    assert incumbent["raw_values"] == ["EMPTY", "candidate-a"]
    assert incumbent["declarations"][0]["status"] == "AMBIGUOUS"
    assert incumbent["declarations"][0]["candidate_ids"] == []
    assert any(
        item["code"] == "candidate_set_empty_marker_conflict"
        and item["field"] == "INCUMBENT_SET"
        for item in preference["advisories"]
    )


def test_conflicting_and_identical_repeated_pair_fields_are_not_last_write_wins(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_selection_context(
        _selection_context(
            """INCUMBENT_SET: candidate-a
CHALLENGERS: candidate-b

PAIRWISE_COMPARISON:
  PAIR: candidate-a | candidate-b
  VERDICT: A_PREFERRED
  VERDICT: B_PREFERRED
  DECISIVE_EVIDENCE: doi:10.1000/example
  SURVIVING_FATAL_UNCERTAINTIES: still-unknown
  REVERSAL_CONDITION: same-reversal
  REVERSAL_CONDITION: same-reversal
  NEXT_DISCRIMINATING_ACTION: run-probe
"""
        )
    )

    preference = _preference_facts(workspace, "repeated-pair-fields")
    pair = preference["pairwise_comparisons"][0]

    assert pair["status"] == "AMBIGUOUS"
    assert pair["verdict"] is None
    assert pair["verdict_status"] == "AMBIGUOUS"
    assert pair["winner_candidate_id"] is None
    assert pair["verdict_fact"]["occurrence_count"] == 2
    assert pair["verdict_fact"]["occurrences"] == ["A_PREFERRED", "B_PREFERRED"]
    assert pair["fields"]["REVERSAL_CONDITION"]["occurrence_count"] == 2
    assert {item["code"] for item in pair["advisories"]} >= {
        "structured_field_conflict",
        "structured_field_repeated_identical",
    }


def test_conflicting_contract_role_implementation_and_update_blocks_are_ambiguous(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    for relative in (
        "candidate_v001.md",
        "implementation_v001/one.py",
        "implementation_v001/two.py",
        "workbench_v001/fidelity.md",
    ):
        _write_run_file(run, relative, f"{relative}\n")
    best = """INCUMBENT_SET: candidate-a
CHALLENGERS: EMPTY

CANDIDATE_ADMISSION: candidate-a
  TARGET_CLAIM: claim-one
  TARGET_CLAIM: claim-two
  CONTRIBUTION_COORDINATE: coordinate
  CHANGED_COMPUTATION: computation
  RESEARCH_ARTIFACT: candidate_v001.md
  STRONGEST_CONSTRUCTIVE_BASELINE: baseline
  FATAL_UNCERTAINTY: uncertainty
  REVERSAL_TEST: reversal

LOCAL_REWARD_CONTRACT: candidate-a
  PRIMARY_OBSERVABLE: observable-one
  PRIMARY_OBSERVABLE: observable-two
  STRONG_BASELINE: baseline
  METRIC_DIRECTION: higher
  MINIMUM_MEANINGFUL_DELTA: 0.1
  REPETITIONS_OR_UNCERTAINTY: repeats
  FAILURE_NEGATIVE_INCONCLUSIVE: three-way
  EXECUTION_COST: low
  LOW_FIDELITY_SCOPE: screening
  INDEPENDENT_ADMISSION_CHECK: held-out
  SCALE_BRIDGE_ASSUMPTION: bridge
  MUTATION_ACCEPTANCE_CONDITION: improves

EVIDENCE_ROLE: candidate-a
  DEVELOPMENT_EVIDENCE: development-one
  DEVELOPMENT_EVIDENCE: development-two
  ADMISSION_EVIDENCE: admission-fact

INDEPENDENT_IMPLEMENTATION: candidate-a
  IMPLEMENTATION_ID: implementation-one
  ARTIFACT_PATH: implementation_v001/one.py
  ARTIFACT_PATH: implementation_v001/two.py
  FRESH_SESSION_ID: declared-session
  FROZEN_CANDIDATE_PATH: candidate_v001.md
  FIDELITY_CHECK_PATH: workbench_v001/fidelity.md
"""
    ambiguous_update = """PREFERENCE_UPDATE:
  ACTION_ID: action-4
  AFFECTED_PAIR: candidate-a | candidate-b
  VERDICT_BEFORE: A_PREFERRED
  VERDICT_AFTER: A_PREFERRED
  VERDICT_AFTER: B_PREFERRED
  FATAL_UNCERTAINTY_REDUCED: NO
  EVIDENCE_PATHS: declared-literature-fact
  STOP_REPEATING: old-action
  EXPANDED_COORDINATE: new-coordinate
"""
    workspace.write_selection_context(
        _selection_context(best, _updates() + "\n" + ambiguous_update)
    )

    preference = _preference_facts(workspace, "ambiguous-structured-blocks")

    admission = preference["candidate_admission_contracts"][0]
    reward = preference["local_reward_contracts"][0]
    role = preference["evidence_roles"][0]
    implementation = preference["independent_implementations"][0]
    update = preference["preference_updates"][-1]
    assert admission["status"] == "AMBIGUOUS"
    assert admission["resolved_complete"] is False
    assert reward["status"] == "AMBIGUOUS"
    assert reward["resolved_complete"] is False
    assert role["status"] == "AMBIGUOUS"
    assert role["reference_relationship"] == "UNKNOWN"
    assert implementation["status"] == "AMBIGUOUS"
    assert implementation["eligible_verified_artifact_record"] is False
    assert preference["independent_implementation_summaries"][0][
        "verified_artifact_count"
    ] == 0
    assert update["status"] == "AMBIGUOUS"
    assert update["evaluable_for_stagnation"] is False
    assert preference["preference_stagnation"]["assessment_status"] == "UNKNOWN"
    assert preference["preference_stagnation"]["warning"] is False
    conflicted_markers = {
        item["marker"]
        for item in preference["advisories"]
        if item["code"] == "structured_field_conflict"
    }
    assert conflicted_markers >= {
        "CANDIDATE_ADMISSION",
        "LOCAL_REWARD_CONTRACT",
        "EVIDENCE_ROLE",
        "INDEPENDENT_IMPLEMENTATION",
        "PREFERENCE_UPDATE",
    }


def test_stagnation_uses_each_action_last_position_for_a_b_c_d_a_regression(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    blocks = []
    for index, action_id in enumerate(("A", "B", "C", "D", "A"), start=1):
        after = "B_PREFERRED" if index == 5 else "A_PREFERRED"
        blocks.append(
            f"""PREFERENCE_UPDATE:
  ACTION_ID: {action_id}
  AFFECTED_PAIR: candidate-a | candidate-b
  VERDICT_BEFORE: A_PREFERRED
  VERDICT_AFTER: {after}
  FATAL_UNCERTAINTY_REDUCED: NO
  EVIDENCE_PATHS: declared-action-{index}
  STOP_REPEATING: old-{index}
  EXPANDED_COORDINATE: coordinate-{index}
"""
        )
    workspace.write_selection_context(
        _selection_context(
            "INCUMBENT_SET: candidate-a\nCHALLENGERS: candidate-b",
            "\n".join(blocks),
        )
    )

    preference = _preference_facts(workspace, "last-action-position")
    stagnation = preference["preference_stagnation"]

    assert stagnation["assessment_status"] == "UNKNOWN"
    assert stagnation["warning"] is False
    assert stagnation["evaluated_action_ids"] == ["C", "D", "A"]
    assert stagnation["selected_action_last_positions"] == [3, 4, 5]
    assert preference["preference_updates"][0]["status"] == "AMBIGUOUS"
    assert preference["preference_updates"][4]["status"] == "AMBIGUOUS"
    assert any(
        item["code"] == "preference_update_group_conflict"
        for item in preference["advisories"]
    )


def test_run_local_evidence_paths_are_verified_without_reclassifying_literature(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    _write_run_file(run, "workbench_v001/present.md", "present evidence\n")
    outside = product / "outside.md"
    outside.write_text("outside\n", encoding="utf-8", newline="\n")
    best = f"""INCUMBENT_SET: candidate-a
CHALLENGERS: candidate-b

PAIRWISE_COMPARISON:
  PAIR: candidate-a | candidate-b
  VERDICT: INSUFFICIENT_EVIDENCE
  DECISIVE_EVIDENCE: workbench_v001/present.md; workbench_v001/missing.md; workbench_v001; {outside}; doi:10.1000/example; arXiv:2401.12345; Smith et al. 2024
  SURVIVING_FATAL_UNCERTAINTIES: uncertainty
  REVERSAL_CONDITION: reversal
  NEXT_DISCRIMINATING_ACTION: next

EVIDENCE_ROLE: candidate-a
  DEVELOPMENT_EVIDENCE: Smith et al. 2024
  ADMISSION_EVIDENCE: workbench_v001/missing.md
"""
    strategy = """PREFERENCE_UPDATE:
  ACTION_ID: evidence-action
  AFFECTED_PAIR: candidate-a | candidate-b
  VERDICT_BEFORE: INSUFFICIENT_EVIDENCE
  VERDICT_AFTER: INSUFFICIENT_EVIDENCE
  FATAL_UNCERTAINTY_REDUCED: NO
  EVIDENCE_PATHS: workbench_v001/present.md; workbench_v001/missing.md
  STOP_REPEATING: none
  EXPANDED_COORDINATE: declared-coordinate
"""
    workspace.write_selection_context(_selection_context(best, strategy))

    preference = _preference_facts(workspace, "evidence-path-validation")
    decisive = preference["pairwise_comparisons"][0]["fields"][
        "DECISIVE_EVIDENCE"
    ]
    entries = decisive["entries"]
    assert decisive["status"] == "UNVERIFIED"
    assert entries[0]["status"] == "VERIFIED_FILE"
    assert entries[0]["sha256"]
    assert [item["status"] for item in entries[1:4]] == [
        "UNVERIFIED",
        "UNVERIFIED",
        "UNVERIFIED",
    ]
    assert [item["status"] for item in entries[4:]] == [
        "DECLARED_TEXT",
        "DECLARED_TEXT",
        "DECLARED_TEXT",
    ]
    role = preference["evidence_roles"][0]
    assert role["development_evidence"]["entries"] == [
        {
            "kind": "DECLARED_TEXT",
            "status": "DECLARED_TEXT",
            "value": "Smith et al. 2024",
        }
    ]
    assert role["admission_evidence"]["entries"][0]["status"] == "UNVERIFIED"
    update_evidence = preference["preference_updates"][0]["fields"][
        "EVIDENCE_PATHS"
    ]
    assert [item["status"] for item in update_evidence["entries"]] == [
        "VERIFIED_FILE",
        "UNVERIFIED",
    ]
    unverified_fields = {
        item["field"]
        for item in preference["advisories"]
        if item["code"] == "declared_run_path_unverified"
    }
    assert unverified_fields >= {
        "DECISIVE_EVIDENCE",
        "ADMISSION_EVIDENCE",
        "EVIDENCE_PATHS",
    }
