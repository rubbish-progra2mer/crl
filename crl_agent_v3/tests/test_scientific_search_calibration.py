from __future__ import annotations

import copy
import hashlib
import json
import math
from collections import Counter
from pathlib import Path

import pytest

from crl_v3.decision import child_process_environment, environment_secrets

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
    _outcome_assets_valid,
    _preflight_unit_seed,
    _removed_legacy_summarize_pilot,
    _unsafe_legacy_summarize_confirmation,
    _unsafe_legacy_summarize_pilot,
    _validated_preflight_selection,
    build_calibration_report,
    build_evaluator_lock,
    lock_tau2_preflight_selection,
    repair_frozen_task_split,
    run_preflight,
    run_temporal_validation,
    summarize_confirmation,
    summarize_pilot,
    summarize_tau2_preflight,
    verify_evaluator_lock,
)
from evaluation.research_discovery.calibration_tau2 import (
    _committed_outcome_assets_valid,
    _enforce_locked_preflight_contract,
    _event_id,
    _evaluator_llm_args,
    _log_manifest,
    _quarantine_orphaned_unit,
    _recover_stale_staging,
    _selected_tasks,
    _short_identifier,
    _validate_path_component,
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


def _prepare_locked_preflight(
    workspace: CalibrationWorkspace, tau2_root: Path
) -> tuple[dict, dict, dict]:
    split = build_frozen_task_split(tau2_root)
    workspace.write_json_once("frozen_task_split.json", split)
    evaluator_lock = build_evaluator_lock(tau2_root)
    workspace.write_json_once("preflight/evaluator_lock.json", evaluator_lock)
    model_identities = {
        name: {
            "digest": hashlib.sha256(name.encode("utf-8")).hexdigest(),
            "size": 1,
            "modified_at": "2026-08-20T00:00:00Z",
            "details": {},
        }
        for name in ("qwen3:8b", "qwen2.5:7b", "qwen3:14b")
    }
    workspace.write_json_once(
        "preflight/current_static.json",
        {
            "tau2_root": str(tau2_root.resolve()),
            "task_split_sha256": split["split_sha256"],
            "evaluator_lock_sha256": evaluator_lock["lock_sha256"],
            "evaluator_lock": {"valid": True},
            "model_identities": model_identities,
            "static_gate": {"passed": True},
        },
    )
    baseline_scaffold = {
        "schema_version": 1,
        "candidate_id": "baseline",
        "mode": "baseline",
        "structural_cell": "official-default",
    }
    ground_truth_scaffold = {
        "schema_version": 1,
        "candidate_id": "ground-truth",
        "mode": "ground_truth",
        "structural_cell": "official-ground-truth",
    }
    workspace.write_json_once("scaffolds/baseline.json", baseline_scaffold)
    workspace.write_json_once("scaffolds/ground-truth.json", ground_truth_scaffold)
    selection = {
        "smoke": {
            "candidate_id": "baseline",
            "block_id": "smoke-valid",
            "attempt_id": "attempt-003",
            "fidelity": "smoke",
            "scaffold_path": "scaffolds/baseline.json",
            "base_seed": 11,
        },
        "baseline_a": {
            "candidate_id": "baseline",
            "block_id": "low-a",
            "attempt_id": "attempt-002",
            "fidelity": "low_fidelity",
            "scaffold_path": "scaffolds/baseline.json",
            "base_seed": 101,
        },
        "baseline_b": {
            "candidate_id": "baseline",
            "block_id": "low-b",
            "attempt_id": "attempt-001",
            "fidelity": "low_fidelity",
            "scaffold_path": "scaffolds/baseline.json",
            "base_seed": 202,
        },
        "ground_truth": {
            "candidate_id": "ground-truth",
            "block_id": "low-gt",
            "attempt_id": "attempt-001",
            "fidelity": "low_fidelity",
            "scaffold_path": "scaffolds/ground-truth.json",
            "base_seed": 303,
        },
    }
    selection_lock = lock_tau2_preflight_selection(workspace, selection)
    return split, selection, selection_lock


def _record_complete_preflight_attempt(
    workspace: CalibrationWorkspace,
    *,
    role: str,
    selection_lock: dict,
    pass_count: int,
) -> None:
    spec = selection_lock["selection"][role]
    execution = selection_lock["execution_contract"]
    dependency_versions = {"tau2": ["1.0.1"], "pydantic": ["2.0.0"]}
    dependency_hash = hashlib.sha256(
        json.dumps(
            dependency_versions,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
    ).hexdigest()
    expected_identities = {
        name: execution["model_identities"][name]
        for name in {
            execution["agent_model"],
            execution["user_model"],
            execution["evaluator_model"],
        }
    }
    manifest = {
        "schema_version": 1,
        "phase": "preflight",
        "fidelity": spec["fidelity"],
        "block_id": spec["block_id"],
        "attempt_id": spec["attempt_id"],
        "candidate_id": spec["candidate_id"],
        "mode": spec["scaffold_mode"],
        "structural_cell": spec["structural_cell"],
        "scaffold_sha256": spec["scaffold_sha256"],
        "task_split_sha256": selection_lock["task_split_sha256"],
        "selected_tasks": spec["selected_tasks"],
        "repetitions": spec["repetitions"],
        "base_seed": spec["base_seed"],
        "agent_model": execution["agent_model"],
        "user_model": execution["user_model"],
        "evaluator_model": execution["evaluator_model"],
        "model_identities": expected_identities,
        "max_steps": execution["max_steps"],
        "timeout_seconds": execution["timeout_seconds"],
        "enforce_communication_protocol": False,
        "ollama_url": execution["ollama_url"],
        "tau2_root": execution["tau2_root"],
        "evaluator_lock_sha256": execution["evaluator_lock_sha256"],
        "runtime_python": str(Path(execution["tau2_root"]) / ".venv/Scripts/python.exe"),
        "runtime_python_version": "3.12.0",
        "runtime_dont_write_bytecode": True,
        "runtime_pycache_prefix": str(Path(execution["tau2_root"]).parent / "unused-cache"),
        "runtime_dependencies": dependency_versions,
        "runtime_dependencies_sha256": dependency_hash,
        "runtime_dependency_tree": {
            "root": str(Path(execution["tau2_root"]) / ".venv/Lib/site-packages"),
            "file_count": 2,
            "sha256": "a" * 64,
            "bytecode_files_excluded": True,
        },
    }
    manifest_hash = hashlib.sha256(
        (json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
            "utf-8"
        )
    ).hexdigest()
    manifest["manifest_sha256"] = manifest_hash
    manifest_relative = (
        f"preflight/attempts/{spec['candidate_id']}/{spec['block_id']}/"
        f"{spec['attempt_id']}/manifest.json"
    )
    workspace.write_json_once(manifest_relative, manifest)
    index = 0
    for domain, task_ids in spec["selected_tasks"].items():
        for task_id in task_ids:
            seed = _preflight_unit_seed(
                spec["base_seed"], spec["block_id"], domain, task_id, 0
            )
            success = index < pass_count
            reward = 1.0 if success else 0.0
            unit_name = f"{_short_identifier(task_id)}-r0"
            raw_relative = (
                f"preflight/raw/{spec['candidate_id']}/{spec['block_id']}/"
                f"{spec['attempt_id']}/{spec['fidelity']}/{domain}/{unit_name}.json"
            )
            raw_value = {
                "task_id": task_id,
                "seed": seed,
                "termination_reason": "user_stop",
                "reward_info": {"reward": reward},
            }
            workspace.write_json_once(raw_relative, raw_value)
            raw_path = workspace.root / raw_relative
            log_relative = (
                f"preflight/llm_logs/{spec['candidate_id']}/{spec['block_id']}/"
                f"{spec['attempt_id']}/{spec['fidelity']}/{domain}/{unit_name}"
            )
            log_path = workspace.root / log_relative
            log_path.mkdir(parents=True)
            log_data = (json.dumps({"message": "ok"}, sort_keys=True) + "\n").encode()
            (log_path / "log.json").write_bytes(log_data)
            log_manifest = {
                "file_count": 1,
                "files": [
                    {
                        "name": "log.json",
                        "size": len(log_data),
                        "sha256": hashlib.sha256(log_data).hexdigest(),
                    }
                ],
            }
            workspace.record_event(
                "preflight",
                {
                    "event_id": f"{role}-outcome-{index:03d}",
                    "kind": "tau2_outcome",
                    "payload": {
                        "candidate_id": spec["candidate_id"],
                        "block_id": spec["block_id"],
                        "attempt_id": spec["attempt_id"],
                        "fidelity": spec["fidelity"],
                        "scaffold_sha256": spec["scaffold_sha256"],
                        "scaffold_mode": spec["scaffold_mode"],
                        "structural_cell": spec["structural_cell"],
                        "attempt_manifest_sha256": manifest_hash,
                        "domain": domain,
                        "task_id": task_id,
                        "repetition": 0,
                        "seed": seed,
                        "execution_status": "completed",
                        "success": success,
                        "reward": reward,
                        "termination_reason": "user_stop",
                        "wall_time_seconds": 1.0,
                        "agent_model": execution["agent_model"],
                        "user_model": execution["user_model"],
                        "evaluator_model": execution["evaluator_model"],
                        "max_steps": execution["max_steps"],
                        "timeout_seconds": execution["timeout_seconds"],
                        "enforce_communication_protocol": False,
                        "raw_result_path": raw_relative,
                        "raw_result_sha256": hashlib.sha256(raw_path.read_bytes()).hexdigest(),
                        "llm_log_path": log_relative,
                        "llm_log_manifest": log_manifest,
                    },
                },
            )
            index += 1
    workspace.record_event(
        "preflight",
        {
            "event_id": f"{role}-audit",
            "kind": "tau2_block_audit",
            "payload": {
                "candidate_id": spec["candidate_id"],
                "block_id": spec["block_id"],
                "attempt_id": spec["attempt_id"],
                "fidelity": spec["fidelity"],
                "scaffold_sha256": spec["scaffold_sha256"],
                "scaffold_mode": spec["scaffold_mode"],
                "structural_cell": spec["structural_cell"],
                "base_seed": spec["base_seed"],
                "evaluator_lock_valid_before": True,
                "evaluator_lock_valid_after": True,
                "candidate_write_scope": "declarative_scaffold_only",
                "evaluator_model": execution["evaluator_model"],
                "task_split_sha256": selection_lock["task_split_sha256"],
                "scheduled_unit_count": index,
                "attempt_manifest_sha256": manifest_hash,
                "attempt_manifest_path": manifest_relative,
                "budget_parity": {
                    "max_steps": execution["max_steps"],
                    "timeout_seconds": execution["timeout_seconds"],
                    "enforce_communication_protocol": False,
                },
            },
        },
    )


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
    assert posterior["paired_independent_task_count"] == 1
    assert posterior["excluded_mechanical_pair_count"] == 1
    assert posterior["posterior_mean"] == pytest.approx(1.0)
    assert posterior["p0"] is None
    assert posterior["p5"] is None
    assert posterior["lcb10"] is None
    assert posterior["status"] == "INSUFFICIENT_INDEPENDENT_TASKS"
    assert classify_tau2_execution("timeout", 0.0) == "infra_failure"
    assert classify_tau2_execution("max_steps", 0.0) == "completed"


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
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    split, selection, selection_lock = _prepare_locked_preflight(workspace, tau2_root)
    ground_truth_count = sum(
        int(item["action_count"]) > 0
        for domain in ("airline", "retail", "telecom")
        for item in split["low_fidelity"][domain]
    )
    counts = {
        "smoke": (10, 5),
        "baseline_a": (24, 6),
        "baseline_b": (24, 7),
        "ground_truth": (
            ground_truth_count,
            math.ceil(ground_truth_count * 0.70),
        ),
    }
    for role, (_, passes) in counts.items():
        _record_complete_preflight_attempt(
            workspace,
            role=role,
            selection_lock=selection_lock,
            pass_count=passes,
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
    assert summary["gate"]["failed_checks"] == []
    assert summary["attempts"]["baseline_a"]["observed_unit_count"] == 24
    assert summary["attempts"]["baseline_a"]["mechanical_failure_count"] == 0
    assert workspace.target("preflight", "authoritative_summary.json").is_file()


def test_incomplete_preflight_is_diagnostic_not_authoritative(tmp_path: Path) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    _, selection, selection_lock = _prepare_locked_preflight(workspace, tau2_root)
    _record_complete_preflight_attempt(
        workspace, role="smoke", selection_lock=selection_lock, pass_count=5
    )
    summary = summarize_tau2_preflight(workspace, selection)
    assert summary["gate"]["passed"] is False
    assert "all_attempts_complete" in summary["gate"]["failed_checks"]
    assert workspace.target("preflight", "current_diagnostic_summary.json").is_file()
    assert not workspace.target("preflight", "authoritative_summary.json").exists()


def test_preflight_summary_rejects_tampered_committed_assets(tmp_path: Path) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    split, selection, selection_lock = _prepare_locked_preflight(workspace, tau2_root)
    ground_truth_count = sum(
        int(item["action_count"]) > 0
        for domain in ("airline", "retail", "telecom")
        for item in split["low_fidelity"][domain]
    )
    passes = {
        "smoke": 5,
        "baseline_a": 6,
        "baseline_b": 7,
        "ground_truth": math.ceil(ground_truth_count * 0.70),
    }
    for role, pass_count in passes.items():
        _record_complete_preflight_attempt(
            workspace, role=role, selection_lock=selection_lock, pass_count=pass_count
        )
    event = next(
        item
        for item in workspace.read_events("preflight")
        if item.get("kind") == "tau2_outcome"
    )
    log_root = workspace.root / event["payload"]["llm_log_path"]
    (log_root / "log.json").write_text(
        json.dumps({"message": "tampered"}) + "\n", encoding="utf-8", newline="\n"
    )
    summary = summarize_tau2_preflight(workspace, selection)
    assert summary["gate"]["passed"] is False
    assert summary["gate"]["checks"]["all_role_contracts_valid"] is False
    assert not workspace.target("preflight", "authoritative_summary.json").exists()


def test_preflight_assets_bind_canonical_unit_and_raw_semantics(tmp_path: Path) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    _, _, selection_lock = _prepare_locked_preflight(workspace, tau2_root)
    _record_complete_preflight_attempt(
        workspace, role="smoke", selection_lock=selection_lock, pass_count=5
    )
    outcomes = [
        item
        for item in workspace.read_events("preflight")
        if item.get("kind") == "tau2_outcome"
    ]
    first = outcomes[0]["payload"]
    second = outcomes[1]["payload"]
    assert _outcome_assets_valid(workspace, first) is True
    reused = copy.deepcopy(first)
    reused["raw_result_path"] = second["raw_result_path"]
    reused["raw_result_sha256"] = second["raw_result_sha256"]
    reused["llm_log_path"] = second["llm_log_path"]
    reused["llm_log_manifest"] = second["llm_log_manifest"]
    assert _outcome_assets_valid(workspace, reused) is False

    raw_path = workspace.root / first["raw_result_path"]
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    raw["reward_info"]["reward"] = 0.0 if first["reward"] == 1.0 else 1.0
    raw_path.write_text(
        json.dumps(raw, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    changed = copy.deepcopy(first)
    changed["raw_result_sha256"] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    assert _outcome_assets_valid(workspace, changed) is False


def test_raw_secret_is_rejected_by_resume_and_summary_validation(tmp_path: Path) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    split, selection, selection_lock = _prepare_locked_preflight(workspace, tau2_root)
    ground_truth_count = sum(
        int(item["action_count"]) > 0
        for domain in ("airline", "retail", "telecom")
        for item in split["low_fidelity"][domain]
    )
    for role, pass_count in {
        "smoke": 5,
        "baseline_a": 6,
        "baseline_b": 7,
        "ground_truth": math.ceil(ground_truth_count * 0.70),
    }.items():
        _record_complete_preflight_attempt(
            workspace, role=role, selection_lock=selection_lock, pass_count=pass_count
        )
    event = next(
        item
        for item in workspace.read_events("preflight")
        if item.get("kind") == "tau2_outcome"
    )
    payload = copy.deepcopy(event["payload"])
    raw_path = workspace.root / payload["raw_result_path"]
    raw = json.loads(raw_path.read_text(encoding="utf-8"))
    raw["api_key"] = "sk-test-sensitive-credential"
    raw_path.write_text(
        json.dumps(raw, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    payload["raw_result_sha256"] = hashlib.sha256(raw_path.read_bytes()).hexdigest()
    assert _committed_outcome_assets_valid(workspace, payload) is False
    assert _outcome_assets_valid(workspace, payload) is False
    event["payload"] = payload
    unsigned = dict(event)
    unsigned.pop("event_integrity_sha256")
    event["event_integrity_sha256"] = hashlib.sha256(
        (json.dumps(unsigned, ensure_ascii=False, indent=2, sort_keys=True) + "\n").encode(
            "utf-8"
        )
    ).hexdigest()
    event_path = workspace.target("preflight", "events", f"{event['event_id']}.json")
    event_path.write_text(
        json.dumps(event, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    summary = summarize_tau2_preflight(workspace, selection)
    assert summary["gate"]["checks"]["all_role_contracts_valid"] is False
    assert not workspace.target("preflight", "authoritative_summary.json").exists()


def test_frozen_split_tampering_is_rejected_before_summary(tmp_path: Path) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    split, selection, _ = _prepare_locked_preflight(workspace, tau2_root)
    split["seed"] += 1
    workspace.target("frozen_task_split.json").write_text(
        json.dumps(split, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    with pytest.raises(ValueError, match="SHA-256"):
        summarize_tau2_preflight(workspace, selection)


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


def test_paired_effect_clusters_same_task_across_blocks() -> None:
    candidate = []
    baseline = []
    for block in ("b1", "b2"):
        for index in range(12):
            candidate.append(_outcome(str(index), True, block=block))
            baseline.append(_outcome(str(index), False, block=block))
    posterior = paired_effect_posterior(candidate, baseline, draws=100)
    assert posterior["paired_scientific_unit_count"] == 24
    assert posterior["paired_independent_task_count"] == 12
    assert posterior["status"] == "READY"


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
            "observation_count": 36,
            "block_count": 4,
            "fit_converged": True,
            "all_fold_models_converged": True,
            "minimum_heldout_block_observation_count": 12,
            "mechanical_observation_count": 0,
            "top_quartile_success_rate": 0.8,
            "bottom_quartile_success_rate": 0.2,
            "isolation_valid": True,
            "evaluator_lock_valid": True,
        }
    )
    assert pilot["passed"] is True
    assert pilot["scientific_delivery_authority"] is False
    fold_failure = {
        "implementation_rate": 0.75,
        "high_fidelity_pass_count": 10,
        "high_fidelity_failure_count": 10,
        "relative_brier_improvement": 0.2,
        "beta1": 0.5,
        "observation_count": 36,
        "block_count": 4,
        "fit_converged": True,
        "all_fold_models_converged": False,
        "minimum_heldout_block_observation_count": 12,
        "mechanical_observation_count": 0,
        "top_quartile_success_rate": 0.8,
        "bottom_quartile_success_rate": 0.2,
        "isolation_valid": True,
        "evaluator_lock_valid": True,
    }
    assert evaluate_pilot_gate(fold_failure)["passed"] is False
    assert "all_fold_models_converged" in evaluate_pilot_gate(fold_failure)["failed_checks"]
    confirmation = evaluate_confirmation_gate(
        {
            "block_advantages": [0.07] * 7 + [0.0],
            "block_ids": [f"b{index}" for index in range(8)],
            "candidate_posteriors": [
                {
                    "p5": 0.96,
                    "lcb10": 0.01,
                    "paired_independent_task_count": 24,
                    "paired_scientific_unit_count": 72,
                    "pre_registered_candidate": True,
                    "selection_adjustment_valid": True,
                }
            ],
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


def test_temporal_validation_and_report_use_explicit_authoritative_files(
    tmp_path: Path,
) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    workspace.write_json_once("frozen_task_split.json", build_frozen_task_split(tau2_root))
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
    workspace.write_json_once("temporal/packet.json", packet)
    temporal = run_temporal_validation(workspace, workspace.target("temporal", "packet.json"))
    assert temporal["validation"]["status"] == "VALID"

    workspace.write_json_once(
        "preflight/authoritative_summary.json",
        {"gate": {"passed": False, "failed_checks": ["smoke incomplete"]}},
    )
    report = build_calibration_report(workspace)
    assert report["temporal"]["packet_sha256"] == temporal["packet_sha256"]
    markdown = workspace.target("report.md").read_text(encoding="utf-8")
    assert "τ² 预检：未通过或材料不足" in markdown
    assert "小试：入口关闭" in markdown
    assert "smoke incomplete" in markdown

    changed_packet = copy.deepcopy(packet)
    changed_packet["visible_artifacts"].append({"artifact_id": "older", "year": 2024})
    workspace.write_json_once("temporal/changed-packet.json", changed_packet)
    with pytest.raises(FileExistsError, match="differs"):
        run_temporal_validation(
            workspace, workspace.target("temporal", "changed-packet.json")
        )


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
    persisted = workspace.read_events("pilot")[0]
    assert isinstance(persisted.get("event_integrity_sha256"), str)
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
    tampered = json.loads(raw.decode("utf-8"))
    tampered["payload"]["implemented"] = False
    (workspace.root / "pilot" / "events" / "candidate-001.json").write_text(
        json.dumps(tampered, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    with pytest.raises(ValueError, match="integrity"):
        workspace.read_events("pilot")
    with pytest.raises(ValueError, match="outside"):
        CalibrationWorkspace(tmp_path / "outside", research_root)


def test_credential_named_environment_is_always_withheld(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    value = "synthetic-credential-value-123456"
    monkeypatch.setenv("CRL_TEST_CREDENTIALS", value)
    child, allowed = child_process_environment()
    assert "CRL_TEST_CREDENTIALS" not in child
    assert allowed == ()
    assert value.encode("utf-8") in environment_secrets()


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
    (tau2_root / "src" / "tau2" / "evaluator" / "core.py").write_text(
        "VALUE = 1\n", encoding="utf-8", newline="\n"
    )
    lock = build_evaluator_lock(tau2_root)
    (tau2_root / "src" / "tau2" / "registry.py").write_text(
        "VALUE = 1\n", encoding="utf-8", newline="\n"
    )
    result = verify_evaluator_lock(tau2_root, lock)
    assert result["valid"] is False
    assert "src/tau2/registry.py" in result["added"]


def test_evaluator_lock_rejects_executable_bytecode_cache(tmp_path: Path) -> None:
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    cache = tau2_root / "src" / "tau2" / "__pycache__"
    cache.mkdir()
    (cache / "registry.cpython-312.pyc").write_bytes(b"bytecode")
    with pytest.raises(ValueError, match="bytecode"):
        build_evaluator_lock(tau2_root)


def test_path_aliases_and_event_identifier_collisions_are_rejected() -> None:
    for value in (".", "..", "name."):
        with pytest.raises(ValueError, match="path alias"):
            _validate_path_component(value, "block_id")
    dotted = _event_id("candidate", "a.b", "attempt", "smoke", "mock", "1", 0)
    dashed = _event_id("candidate", "a-b", "attempt", "smoke", "mock", "1", 0)
    assert dotted != dashed


def test_stale_staging_is_deleted_and_recorded(tmp_path: Path) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    stale = workspace.target("preflight", "staging", "crl-tau2-dead-unit")
    logs = stale / "logs"
    logs.mkdir(parents=True)
    (logs / "uncommitted.json").write_text(
        json.dumps({"api_key": "sk-test-uncommitted-secret"}) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    _recover_stale_staging(workspace, "preflight")
    assert not stale.exists()
    records = list(workspace.target("preflight", "orphaned", "staging").glob("*.json"))
    assert len(records) == 1
    record = json.loads(records[0].read_text(encoding="utf-8"))
    assert record["action"] == "deleted_without_scientific_interpretation"


def test_preflight_selection_rejects_role_reuse_and_posthoc_lock(tmp_path: Path) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    workspace.write_json_once("frozen_task_split.json", build_frozen_task_split(tau2_root))
    selection = {
        "smoke": {
            "candidate_id": "baseline",
            "block_id": "smoke",
            "attempt_id": "a1",
            "fidelity": "smoke",
            "scaffold_path": "scaffolds/baseline.json",
            "base_seed": 11,
        },
        "baseline_a": {
            "candidate_id": "baseline",
            "block_id": "low-a",
            "attempt_id": "a1",
            "fidelity": "low_fidelity",
            "scaffold_path": "scaffolds/baseline.json",
            "base_seed": 101,
        },
        "baseline_b": {
            "candidate_id": "baseline",
            "block_id": "low-b",
            "attempt_id": "a2",
            "fidelity": "low_fidelity",
            "scaffold_path": "scaffolds/baseline.json",
            "base_seed": 202,
        },
        "ground_truth": {
            "candidate_id": "ground-truth",
            "block_id": "low-gt",
            "attempt_id": "a1",
            "fidelity": "low_fidelity",
            "scaffold_path": "scaffolds/ground-truth.json",
            "base_seed": 303,
        },
    }
    reused = copy.deepcopy(selection)
    reused["baseline_b"] = dict(reused["baseline_a"])
    with pytest.raises(ValueError, match="distinct"):
        lock_tau2_preflight_selection(workspace, reused)
    disguised_reuse = copy.deepcopy(selection)
    disguised_reuse["baseline_b"].update(
        {
            "block_id": disguised_reuse["baseline_a"]["block_id"],
            "attempt_id": disguised_reuse["baseline_a"]["attempt_id"],
            "base_seed": disguised_reuse["baseline_a"]["base_seed"] + 1,
            "scaffold_path": "scaffolds/another-baseline.json",
        }
    )
    with pytest.raises(ValueError, match="distinct"):
        _validated_preflight_selection(disguised_reuse)
    workspace.record_event(
        "preflight",
        {
            "event_id": "posthoc-outcome",
            "kind": "tau2_outcome",
            "payload": {**selection["baseline_a"], "task_id": "1"},
        },
    )
    with pytest.raises(ValueError, match="post hoc"):
        lock_tau2_preflight_selection(workspace, selection)


def test_preflight_baseline_roles_require_identical_scaffold_bytes(tmp_path: Path) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    _, selection, _ = _prepare_locked_preflight(workspace, tau2_root)
    workspace.target("preflight", "selection_lock.json").unlink()
    workspace.write_json_once(
        "scaffolds/alternate-baseline.json",
        {
            "schema_version": 1,
            "candidate_id": "baseline",
            "mode": "baseline",
            "structural_cell": "different-official-default",
        },
    )
    selection["baseline_b"]["scaffold_path"] = "scaffolds/alternate-baseline.json"
    with pytest.raises(ValueError, match="same scaffold bytes"):
        lock_tau2_preflight_selection(workspace, selection)


def test_selected_attempt_contract_rejects_seed_drift(tmp_path: Path) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    tau2_root = _make_tau2_root(tmp_path / "tau2")
    _, _, selection_lock = _prepare_locked_preflight(workspace, tau2_root)
    role = selection_lock["selection"]["smoke"]
    execution = selection_lock["execution_contract"]
    manifest = {
        **role,
        "phase": "preflight",
        "mode": role["scaffold_mode"],
        "task_split_sha256": selection_lock["task_split_sha256"],
        "agent_model": execution["agent_model"],
        "user_model": execution["user_model"],
        "evaluator_model": execution["evaluator_model"],
        "model_identities": {
            name: execution["model_identities"][name]
            for name in {
                execution["agent_model"],
                execution["user_model"],
                execution["evaluator_model"],
            }
        },
        "max_steps": execution["max_steps"],
        "timeout_seconds": execution["timeout_seconds"],
        "enforce_communication_protocol": False,
        "ollama_url": execution["ollama_url"],
        "tau2_root": execution["tau2_root"],
        "evaluator_lock_sha256": execution["evaluator_lock_sha256"],
        "base_seed": role["base_seed"] + 1,
    }
    with pytest.raises(ValueError, match="immutable contract"):
        _enforce_locked_preflight_contract(workspace, manifest)


def test_pilot_and_confirmation_summaries_are_closed_until_raw_derivation(
    tmp_path: Path,
) -> None:
    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    with pytest.raises(RuntimeError, match="immutable tau2 outcome"):
        summarize_pilot(workspace)
    with pytest.raises(RuntimeError, match="immutable tau2 outcome"):
        summarize_confirmation(workspace)
    with pytest.raises(RuntimeError, match="permanently disabled"):
        _unsafe_legacy_summarize_pilot(workspace)
    with pytest.raises(RuntimeError, match="cannot be executed"):
        _removed_legacy_summarize_pilot(workspace)
    with pytest.raises(RuntimeError, match="permanently disabled"):
        _unsafe_legacy_summarize_confirmation(workspace)


def test_tau2_log_normalization_secret_scan_and_orphan_recovery(
    tmp_path: Path,
) -> None:
    logs = tmp_path / "logs"
    logs.mkdir()
    log = logs / "call.json"
    log.write_bytes(b'{"message":"ok"}\r\n')
    manifest = _log_manifest(logs)
    assert manifest["file_count"] == 1
    assert log.read_bytes() == b'{"message":"ok"}\n'
    log.write_bytes(b'{"api_key":"abcdefghijklmno"}\n')
    with pytest.raises(ValueError, match="credential"):
        _log_manifest(logs)

    research_root = tmp_path / "research_workspace"
    workspace = CalibrationWorkspace(research_root / "reward_calibration_v001", research_root)
    workspace.prepare()
    raw = workspace.target("preflight", "raw", "unit.json")
    raw.parent.mkdir(parents=True)
    raw.write_text("{}\n", encoding="utf-8", newline="\n")
    final_logs = workspace.target("preflight", "llm_logs", "unit")
    final_logs.mkdir(parents=True)
    (final_logs / "call.json").write_text("{}\n", encoding="utf-8", newline="\n")
    _quarantine_orphaned_unit(
        workspace,
        phase="preflight",
        event_id="unit-event",
        raw_path=raw,
        log_path=final_logs,
    )
    assert not raw.exists()
    assert not final_logs.exists()
    assert list(workspace.target("preflight", "orphaned", "unit-event").iterdir())
    with pytest.raises(ValueError, match="reserved Windows"):
        _validate_path_component("CON", "attempt_id")


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
