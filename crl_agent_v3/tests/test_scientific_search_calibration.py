from __future__ import annotations

import copy
import json
from collections import Counter
from pathlib import Path

import pytest

from evaluation.research_discovery.calibration import (
    allocate_constrained_parents,
    block_heldout_bridge_validation,
    build_frozen_task_split,
    evaluate_confirmation_gate,
    evaluate_pilot_gate,
    expected_entropy_reduction_per_cost,
    naive_scalar_reward,
    nondominated_archive,
    paired_effect_posterior,
    select_stratified_high_fidelity,
    validate_frozen_task_split,
    validate_temporal_packet,
)
from evaluation.research_discovery.calibration_runner import (
    CalibrationWorkspace,
    build_evaluator_lock,
    repair_frozen_task_split,
    run_preflight,
    summarize_tau2_preflight,
    verify_evaluator_lock,
)
from evaluation.research_discovery.calibration_tau2 import (
    _classify_tau2_exception,
    _evaluator_llm_args,
    _selected_tasks,
    _short_identifier,
    classify_tau2_execution,
    load_agent_scaffold,
    windows_utf8_subprocess_environment,
)


def _make_tau2_root(root: Path) -> Path:
    (root / "src" / "tau2" / "evaluator").mkdir(parents=True)
    (root / "src" / "tau2" / "runner").mkdir(parents=True)
    (root / "src" / "tau2" / "data_model").mkdir(parents=True)
    (root / "src" / "tau2" / "domains").mkdir(parents=True)
    (root / "pyproject.toml").write_text(
        '[project]\nname = "tau2"\nversion = "1.0.1"\n', encoding="utf-8", newline="\n"
    )
    for relative in (
        "src/tau2/evaluator/core.py",
        "src/tau2/runner/core.py",
        "src/tau2/data_model/core.py",
        "src/tau2/domains/core.py",
    ):
        (root / relative).write_text("VALUE = 1\n", encoding="utf-8", newline="\n")
    counts = {"mock": 10, "airline": 64, "retail": 128, "telecom": 160}
    for domain, count in counts.items():
        directory = root / "data" / "tau2" / "domains" / domain
        directory.mkdir(parents=True)
        tasks = []
        for index in range(count):
            action_count = index % 8
            tasks.append(
                {
                    "id": str(index),
                    "evaluation_criteria": {
                        "actions": [{"name": f"tool_{number}"} for number in range(action_count)],
                        "communicate_info": ["x"] if index % 3 == 0 else [],
                        "reward_basis": ["DB", "COMMUNICATE"],
                    },
                }
            )
        (directory / "tasks.json").write_text(
            json.dumps(tasks, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        (directory / "split_tasks.json").write_text(
            json.dumps({"base": [str(index) for index in range(count)]}, indent=2) + "\n",
            encoding="utf-8",
            newline="\n",
        )
    return root


def _outcome(
    task_id: str,
    success: bool,
    *,
    status: str = "completed",
    block: str = "b1",
    repetition: int = 0,
) -> dict[str, object]:
    return {
        "block_id": block,
        "domain": "airline",
        "task_id": task_id,
        "repetition": repetition,
        "execution_status": status,
        "success": success,
    }


def _candidate(identifier: str, p0: float, cell: str) -> dict[str, object]:
    return {
        "candidate_id": identifier,
        "p0": p0,
        "p5": max(0.0, p0 - 0.1),
        "lcb10": p0 - 0.2,
        "expected_cost": 1.0 + p0,
        "infra_rate": 0.0,
        "successes": round(p0 * 10),
        "failures": 10 - round(p0 * 10),
        "structural_cell": cell,
        "hard_constraints": {"isolation": True, "budget": True},
    }


def test_task_split_is_deterministic_stratified_and_disjoint(tmp_path: Path) -> None:
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    telecom_split = tau2_root / "data" / "tau2" / "domains" / "telecom" / "split_tasks.json"
    telecom_split.write_text(
        json.dumps({"base": [str(index) for index in range(114)]}, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    first = build_frozen_task_split(tau2_root, seed=17)
    second = build_frozen_task_split(tau2_root, seed=17)
    assert first == second
    assert len(first["smoke"]["mock"]) == 10
    assert {key: len(value) for key, value in first["low_fidelity"].items()} == {
        "airline": 8,
        "retail": 8,
        "telecom": 8,
    }
    assert {key: len(value) for key, value in first["high_fidelity"].items()} == {
        "airline": 20,
        "retail": 28,
        "telecom": 48,
    }
    for domain in ("airline", "retail", "telecom"):
        low = {item["task_id"] for item in first["low_fidelity"][domain]}
        high = {item["task_id"] for item in first["high_fidelity"][domain]}
        assert not low & high
        assert len({item["action_stratum"] for item in first["high_fidelity"][domain]}) > 1
    assert all(
        int(item["task_id"]) < 114
        for section in (first["low_fidelity"], first["high_fidelity"])
        for item in section["telecom"]
    )
    tampered = copy.deepcopy(first)
    tampered["high_fidelity"]["airline"][0]["task_id"] = "changed"
    with pytest.raises(ValueError, match="SHA-256"):
        validate_frozen_task_split(tampered)


def test_naive_scalar_counts_mechanics_as_zero_but_science_excludes_it() -> None:
    naive = naive_scalar_reward(
        [_outcome("1", True), _outcome("2", False, status="runner_failure")]
    )
    assert naive["reward"] == 0.5
    assert naive["mechanical_failures_counted_as_zero"] == 1
    candidate = [_outcome("1", True), _outcome("2", False, status="runner_failure")]
    baseline = [_outcome("1", False), _outcome("2", True)]
    posterior = paired_effect_posterior(candidate, baseline, draws=500, seed=3)
    assert posterior["paired_scientific_unit_count"] == 1
    assert posterior["excluded_mechanical_pair_count"] == 1
    assert posterior["posterior_mean"] == pytest.approx(1.0)
    assert posterior["p0"] == 1.0
    assert posterior["p5"] == 1.0
    assert posterior["lcb10"] == pytest.approx(1.0)
    assert classify_tau2_execution("timeout", 0.0) == "infra_failure"
    assert classify_tau2_execution("max_steps", 0.0) == "completed"


def test_expected_entity_absence_in_environment_evaluator_is_scientific() -> None:
    scientific = _classify_tau2_exception(
        ValueError("Task task_2 not found"),
        [r"C:\isolated\tau2\evaluator\evaluator_env.py", r"C:\domain\tools.py"],
    )
    assert scientific == (
        "completed",
        "environment_evaluator_expected_entity_absent",
    )
    assert _classify_tau2_exception(
        ValueError("Task task_2 not found"), [r"C:\domain\tools.py"]
    ) == ("runner_failure", None)


def test_windows_tau2_launcher_forces_utf8_mode() -> None:
    source = {"PYTHONUTF8": "0", "UNCHANGED": "yes"}
    updated = windows_utf8_subprocess_environment(
        source, os_name="nt", utf8_mode=0
    )
    assert updated == {
        "PYTHONUTF8": "1",
        "PYTHONIOENCODING": "utf-8",
        "UNCHANGED": "yes",
    }
    assert source["PYTHONUTF8"] == "0"
    assert (
        windows_utf8_subprocess_environment(source, os_name="nt", utf8_mode=1)
        is None
    )
    assert (
        windows_utf8_subprocess_environment(source, os_name="posix", utf8_mode=0)
        is None
    )
    assert _classify_tau2_exception(
        RuntimeError("Task task_2 not found"),
        [r"C:\isolated\tau2\evaluator\evaluator_env.py"],
    ) == ("runner_failure", None)


def test_nl_assertion_evaluator_uses_json_mode_only_for_evaluator() -> None:
    arguments = _evaluator_llm_args("http://127.0.0.1:11434/")
    assert arguments["api_base"] == "http://127.0.0.1:11434"
    assert arguments["temperature"] == 0.0
    assert arguments["response_format"] == {"type": "json_object"}
    task_slug = _short_identifier(
        "[service_issue]airplane_mode_on|break_apn_settings[PERSONA:None]"
    )
    assert len(task_slug) <= 59
    assert not set('<>:"/\\|?*') & set(task_slug)
    split = {
        "low_fidelity": {
            "airline": [
                {"task_id": "no-actions", "action_count": 0},
                {"task_id": "with-actions", "action_count": 2},
            ]
        }
    }
    assert _selected_tasks(
        split,
        "low_fidelity",
        ["airline"],
        require_expected_actions=True,
    ) == {"airline": ["with-actions"]}


def test_tau2_preflight_summary_uses_only_explicit_attempts(tmp_path: Path) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    selection = {
        "smoke": {
            "candidate_id": "baseline",
            "block_id": "smoke-valid",
            "attempt_id": "attempt-003",
            "fidelity": "smoke",
        },
        "baseline_a": {
            "candidate_id": "baseline",
            "block_id": "low-a",
            "attempt_id": "attempt-002",
            "fidelity": "low_fidelity",
        },
        "baseline_b": {
            "candidate_id": "baseline",
            "block_id": "low-b",
            "attempt_id": "attempt-001",
            "fidelity": "low_fidelity",
        },
        "ground_truth": {
            "candidate_id": "ground-truth",
            "block_id": "low-gt",
            "attempt_id": "attempt-001",
            "fidelity": "low_fidelity",
        },
    }
    counts = {
        "smoke": (10, 5),
        "baseline_a": (24, 6),
        "baseline_b": (24, 7),
        "ground_truth": (23, 18),
    }
    for role, (total, passes) in counts.items():
        spec = selection[role]
        for index in range(total):
            workspace.record_event(
                "preflight",
                {
                    "event_id": f"{role}-outcome-{index:03d}",
                    "kind": "tau2_outcome",
                    "payload": {
                        **spec,
                        "domain": "mock" if role == "smoke" else "airline",
                        "task_id": str(index),
                        "repetition": 0,
                        "execution_status": "completed",
                        "success": index < passes,
                    },
                },
            )
        workspace.record_event(
            "preflight",
            {
                "event_id": f"{role}-audit",
                "kind": "tau2_block_audit",
                "payload": {
                    **spec,
                    "evaluator_lock_valid_before": True,
                    "evaluator_lock_valid_after": True,
                    "scheduled_unit_count": total,
                },
            },
        )
    workspace.record_event(
        "preflight",
        {
            "event_id": "invalid-old-attempt",
            "kind": "tau2_outcome",
            "payload": {
                **selection["baseline_a"],
                "attempt_id": "attempt-001",
                "domain": "airline",
                "task_id": "old",
                "repetition": 0,
                "execution_status": "runner_failure",
                "success": False,
            },
        },
    )
    summary = summarize_tau2_preflight(workspace, selection)
    assert summary["gate"]["passed"] is True
    assert summary["attempts"]["baseline_a"]["observed_unit_count"] == 24
    assert summary["attempts"]["baseline_a"]["mechanical_failure_count"] == 0


def test_paired_units_reject_duplicates_and_empty_science_is_unavailable() -> None:
    duplicate = [_outcome("1", True), _outcome("1", False)]
    with pytest.raises(ValueError, match="duplicate candidate"):
        paired_effect_posterior(duplicate, [_outcome("1", False)], draws=100)
    unavailable = paired_effect_posterior(
        [_outcome("1", False, status="infra_failure")],
        [_outcome("1", True)],
        draws=100,
    )
    assert unavailable["status"] == "UNAVAILABLE"
    assert unavailable["p0"] is None


def test_entropy_acquisition_is_positive_and_cost_sensitive() -> None:
    cheap = expected_entropy_reduction_per_cost(2, 2, 1.0)
    expensive = expected_entropy_reduction_per_cost(2, 2, 4.0)
    assert cheap > 0
    assert cheap == pytest.approx(expensive * 4)


def test_nondominated_archive_obeys_hard_constraints_without_total_score() -> None:
    candidates = [
        _candidate("a", 0.8, "x"),
        _candidate("b", 0.7, "y"),
        _candidate("c", 0.9, "z"),
    ]
    candidates[0]["expected_cost"] = 1.0
    candidates[1]["expected_cost"] = 3.0
    candidates[2]["hard_constraints"] = {"isolation": False, "budget": True}
    archive = nondominated_archive(candidates)
    assert [item["candidate_id"] for item in archive] == ["a"]
    assert all("total_score" not in item for item in archive)


def test_parent_allocation_implements_fifty_twentyfive_twentyfive_policy() -> None:
    candidates = [_candidate(f"c{index}", 0.1 + index * 0.1, f"cell{index % 3}") for index in range(6)]
    selected = allocate_constrained_parents(candidates, offspring_count=6, seed=9)
    counts = Counter(item["allocation"] for item in selected)
    assert counts["posterior_thompson"] == 3
    assert sorted((counts["highest_entropy"], counts["least_covered"])) == [1, 2]
    assert len(selected) == 6


def test_high_fidelity_selection_covers_all_low_fidelity_quartiles() -> None:
    candidates = [
        _candidate(f"c{index:02d}", index / 39, f"cell{index % 4}")
        for index in range(40)
    ]
    selected = set(select_stratified_high_fidelity(candidates, count=36, seed=4))
    selected_ranks = [index for index in range(40) if f"c{index:02d}" in selected]
    assert min(selected_ranks) < 10
    assert any(10 <= rank < 20 for rank in selected_ranks)
    assert any(20 <= rank < 30 for rank in selected_ranks)
    assert max(selected_ranks) >= 30


def test_bridge_validation_and_phase_gates_are_explicit() -> None:
    records = []
    for block in ("b1", "b2", "b3", "b4"):
        for p0, success in ((0.1, False), (0.2, False), (0.8, True), (0.9, True)):
            records.append({"block_id": block, "p0": p0, "high_success": success})
    bridge = block_heldout_bridge_validation(records)
    assert bridge["beta1"] > 0
    assert bridge["top_quartile_success_rate"] > bridge["bottom_quartile_success_rate"]
    pilot = evaluate_pilot_gate(
        {
            "implementation_rate": 0.75,
            "high_fidelity_pass_count": 4,
            "high_fidelity_failure_count": 4,
            "relative_brier_improvement": 0.2,
            "beta1": 0.5,
            "top_quartile_success_rate": 0.8,
            "bottom_quartile_success_rate": 0.2,
            "isolation_valid": True,
            "evaluator_lock_valid": True,
        }
    )
    assert pilot["passed"] is True
    assert pilot["scientific_delivery_authority"] is False
    confirmation = evaluate_confirmation_gate(
        {
            "block_advantages": [0.07] * 7 + [0.0],
            "candidate_posteriors": [{"p5": 0.96, "lcb10": 0.01}],
            "domain_regression_constraints_pass": True,
            "diversity_constraints_pass": True,
            "isolation_valid": True,
            "evaluator_lock_valid": True,
        }
    )
    assert confirmation["passed"] is True
    assert confirmation["scientific_delivery_authority"] is False


def test_temporal_packet_rejects_2026_leakage_and_llm_primary_use() -> None:
    packet = {
        "visible_through_year": 2025,
        "visible_artifacts": [{"artifact_id": "old", "year": 2025}],
        "heldout_artifacts": [
            {"artifact_id": "P072", "year": 2026},
            {"artifact_id": "P074", "year": 2026},
            {"artifact_id": "P087", "year": 2026},
        ],
        "annotations": [{"annotator_type": "llm_auxiliary", "use": "auxiliary_only"}],
    }
    assert validate_temporal_packet(packet)["status"] == "VALID"
    leaked = copy.deepcopy(packet)
    leaked["visible_artifacts"].append({"artifact_id": "future", "year": 2026})
    with pytest.raises(ValueError, match="2025 cutoff"):
        validate_temporal_packet(leaked)
    promoted = copy.deepcopy(packet)
    promoted["annotations"][0]["use"] = "primary"
    with pytest.raises(ValueError, match="auxiliary_only"):
        validate_temporal_packet(promoted)


def test_workspace_resume_has_no_duplicates_and_rejects_secrets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    event = {
        "event_id": "candidate-001",
        "kind": "candidate_result",
        "payload": {"implemented": True},
    }
    assert workspace.record_event("pilot", event) is True
    assert workspace.record_event("pilot", event) is False
    changed = copy.deepcopy(event)
    changed["payload"]["implemented"] = False
    with pytest.raises(FileExistsError, match="differs"):
        workspace.record_event("pilot", changed)
    monkeypatch.setenv("CALIBRATION_TEST_TOKEN", "calibration-secret-123456")
    secret = {
        "event_id": "candidate-secret",
        "kind": "candidate_result",
        "payload": {"text": "calibration-secret-123456"},
    }
    with pytest.raises(ValueError, match="credential"):
        workspace.record_event("pilot", secret)
    raw = (workspace.root / "pilot" / "events" / "candidate-001.json").read_bytes()
    assert not raw.startswith(b"\xef\xbb\xbf")
    assert b"\r" not in raw
    with pytest.raises(ValueError, match="outside"):
        CalibrationWorkspace(tmp_path / "outside", research_root)


def test_evaluator_lock_detects_changes(tmp_path: Path) -> None:
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    lock = build_evaluator_lock(tau2_root)
    assert verify_evaluator_lock(tau2_root, lock)["valid"] is True
    (tau2_root / "src" / "tau2" / "evaluator" / "core.py").write_text(
        "VALUE = 2\n", encoding="utf-8", newline="\n"
    )
    result = verify_evaluator_lock(tau2_root, lock)
    assert result["valid"] is False
    assert "src/tau2/evaluator/core.py" in result["changed"]


def test_preflight_is_idempotent_and_scaffold_is_declarative(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    tau2_root = _make_tau2_root(workspace.root / "preflight" / "runtime" / "tau2")
    monkeypatch.setattr(
        "evaluation.research_discovery.calibration_runner.query_ollama_models",
        lambda _url: {"qwen3:8b", "qwen2.5:7b", "qwen3.5:9b"},
    )
    first = run_preflight(
        workspace,
        tau2_root=tau2_root,
        agent_model="qwen3:8b",
        user_model="qwen2.5:7b",
        reserve_model="qwen3.5:9b",
    )
    second = run_preflight(
        workspace,
        tau2_root=tau2_root,
        agent_model="qwen3:8b",
        user_model="qwen2.5:7b",
        reserve_model="qwen3.5:9b",
    )
    assert first == second
    assert first["static_gate"]["passed"] is True
    assert len(list((workspace.root / "preflight" / "snapshots").glob("*.json"))) == 1

    scaffold_path = workspace.root / "pilot" / "scaffolds" / "candidate-001.json"
    workspace.write_json_once(
        "pilot/scaffolds/candidate-001.json",
        {
            "schema_version": 1,
            "candidate_id": "candidate-001",
            "mode": "custom",
            "structural_cell": "policy-checklist",
            "instruction": "先核对政策，再选择一次工具调用或一次用户回复。",
        },
    )
    scaffold = load_agent_scaffold(workspace, scaffold_path)
    assert scaffold["mode"] == "custom"
    assert len(scaffold["scaffold_sha256"]) == 64
    executable = copy.deepcopy(scaffold)
    executable.pop("scaffold_sha256")
    executable.pop("_source_path")
    executable["python_code"] = "raise SystemExit"
    bad_path = workspace.root / "pilot" / "scaffolds" / "bad.json"
    workspace.write_json_once("pilot/scaffolds/bad.json", executable)
    with pytest.raises(ValueError, match="extra"):
        load_agent_scaffold(workspace, bad_path)

    previous = json.loads((workspace.root / "frozen_task_split.json").read_text(encoding="utf-8"))
    previous["split_sha256"] = "0" * 64
    (workspace.root / "frozen_task_split.json").write_text(
        json.dumps(previous, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    repair = repair_frozen_task_split(workspace, tau2_root=tau2_root)
    assert repair["changed"] is True
    assert (workspace.root / repair["invalidated_copy"]).is_file()
    validate_frozen_task_split(
        json.loads((workspace.root / "frozen_task_split.json").read_text(encoding="utf-8"))
    )
