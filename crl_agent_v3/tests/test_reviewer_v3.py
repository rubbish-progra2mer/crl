from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

import pytest

import crl_v3.reviewer_runtime as reviewer_runtime
from conftest import make_run, record_successful_attempt
from crl_v3.recorded import run_recorded
from crl_v3.reviewer_protocol import (
    DIAGNOSTIC_FIELDS,
    DIMENSION_WEIGHTS,
    ROLES,
    canonical_evaluation,
    create_evaluation,
    finalize_evaluation,
    implementation_measurement_history,
    normalize_codex_cli_version,
    role_score_basis_points,
)
from crl_v3.reviewer_runtime import _event_is_forbidden
from crl_v3.decision import delivery_material_errors, read_delivery
from crl_v3.seed_support import final_evidence_closure
from crl_v3.workspace import ResearchWorkspace


def _review_output(role: str, score: int) -> dict[str, object]:
    return {
        "review_protocol": "CRL-IR-1.0",
        "reviewer_role": role,
        "evaluator_version": "CRL-EVAL-1.0",
        "model_identity": "gpt-5.6-sol",
        "reasoning_effort": "xhigh",
        "scores": {name: score for name in DIMENSION_WEIGHTS[role]},
        "reasons": {name: f"traceable reason for {name}" for name in DIMENSION_WEIGHTS[role]},
        "diagnostics": {name: f"traceable diagnostic for {name}" for name in DIAGNOSTIC_FIELDS[role]},
        "critical_risk": "none",
        "confidence": "medium",
        "free_review": f"fixed {role} review",
    }


def _write_role_reports(
    root: Path,
    score: int,
    *,
    valid: bool = True,
    codex_version: str = "codex-cli 0.147.0",
) -> None:
    request_data = (root / "request.json").read_bytes()
    request = json.loads(request_data.decode("utf-8"))
    for role in ROLES:
        directory = root / role
        directory.mkdir()
        envelope = {
            "request_sha256": hashlib.sha256(request_data).hexdigest(),
            "packet_key": request["packet_key"],
            "measurement_key": request["measurement_key"],
            "runtime": {"codex_version": codex_version},
            "valid": valid,
            "invalid_reasons": [] if valid else ["forbidden tool event"],
            "output": _review_output(role, score),
        }
        (directory / "report.json").write_text(
            json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )


def _fixture(tmp_path: Path) -> tuple[Path, Path, ResearchWorkspace, dict[int, list[str]]]:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_seed("# Seed\n\nBound final research seed.")
    overview = run / "overview_v001.md"
    overview.write_text("Mechanism overview.\n", encoding="utf-8", newline="\n")
    source = workspace.workbench_path / "input.txt"
    source.parent.mkdir()
    source.write_text("independent fixture input\n", encoding="utf-8", newline="\n")
    completed = record_successful_attempt(product, run, "v001", source)
    assert completed.returncode == 0, completed.stderr.decode("utf-8", errors="replace")
    run_recorded(
        workspace,
        "exploration-one",
        [sys.executable, "-c", "print('recorded')"],
    )
    comparison = workspace.experiment_path / "comparisons" / "comparison-one"
    comparison.mkdir(parents=True)
    (comparison / "comparison.json").write_text(
        json.dumps(
            {
                "candidate_attempt": {"attempt_id": "attempt-001"},
                "baseline_attempts": [{"attempt_id": "attempt-baseline"}],
            },
            sort_keys=True,
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )
    sections = {
        1: ["seed_v001.md", "overview_v001.md"],
        3: ["experiment_v001/attempts/attempt-001/execution.json"],
        6: ["experiment_v001/attempts/attempt-001/spec.json"],
    }
    return product, run, workspace, sections


def _write_seed_mapping(
    workspace: ResearchWorkspace,
    mapping: dict[str, object] | None,
    *,
    body: str,
) -> None:
    metadata = {
        "schema_version": 1,
        "hypothesis_ids": [],
        "claim_ids": [],
        "falsified_claim_dispositions": [],
        "metric_mappings": [] if mapping is None else [mapping],
    }
    marker = "<!-- CRL_SEED_SUPPORT_META " + json.dumps(
        metadata, ensure_ascii=False, separators=(",", ":")
    ) + " -->"
    workspace.seed_path.write_text(
        f"# Seed\n\n{body}\n\n{marker}\n",
        encoding="utf-8",
        newline="\n",
    )


def _valid_mapping() -> dict[str, object]:
    return {
        "seed_text": "Observed metric is 0.5。",
        "seed_value": 0.5,
        "source_path": "experiment_v001/attempts/attempt-001/metrics.json",
        "json_pointer": "/records/0/value",
    }


def _expand_metrics(run: Path, count: int) -> None:
    attempt = run / "experiment_v001/attempts/attempt-001"
    metrics_path = attempt / "metrics.json"
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))
    template = metrics["records"][0]
    metrics["records"] = [
        {**template, "replicate": index} for index in range(count)
    ]
    data = (
        json.dumps(metrics, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    metrics_path.write_bytes(data)
    execution_path = attempt / "execution.json"
    execution = json.loads(execution_path.read_text(encoding="utf-8"))
    execution["metrics"]["snapshot"]["size_bytes"] = len(data)
    execution["metrics"]["snapshot"]["sha256"] = hashlib.sha256(data).hexdigest()
    execution_path.write_text(
        json.dumps(execution, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def test_packet_has_seven_sections_inventory_and_three_identity_keys(tmp_path: Path) -> None:
    _, _, workspace, sections = _fixture(tmp_path)

    request = create_evaluation(workspace, sections, final_delivery=True)
    root = Path(request["path"])
    packet = (root / "packet.md").read_text(encoding="utf-8")
    inventory = json.loads((root / "evidence_inventory.json").read_text(encoding="utf-8"))

    assert all(f"## {number}." in packet for number in range(1, 8))
    assert packet.count("NOT PROVIDED") == 4
    assert len(request["implementation_key"]) == 64
    assert len(request["packet_key"]) == 64
    assert len(request["measurement_key"]) == 64
    formal = next(item for item in inventory["formal_attempts"] if item["attempt_id"] == "attempt-001")
    assert formal["association"] == "MATCH"
    assert formal["selected_in_core"] is True
    assert formal["valid_review_support"] is True
    assert inventory["recorded_attempt_count"] == 1
    assert inventory["recorded_attempts"][0]["selected_in_core"] is False
    assert inventory["comparison_count"] == 1


def test_correct_explicit_mapping_is_bound_into_final_review_and_delivery(
    tmp_path: Path,
) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    _write_seed_mapping(
        workspace, _valid_mapping(), body="Observed metric is 0.5。"
    )

    request = create_evaluation(workspace, sections, final_delivery=True)
    root = Path(request["path"])
    packet = (root / "packet.md").read_text(encoding="utf-8")
    assert len(request["final_core_evidence_sha256"]) == 64
    assert "seed_metric_mapping_resolved" in packet
    assert '"source_value": 0.5' in packet

    _write_role_reports(root, 3)
    aggregate = finalize_evaluation(workspace, request["evaluation_id"])
    request_data = (root / "request.json").read_bytes()
    assert aggregate["request_sha256"] == hashlib.sha256(request_data).hexdigest()
    workspace.write_review_decision(
        "显式映射已由机器核验；科学充分性由主研究者裁决。",
        measurement_key=request["measurement_key"],
    )
    assert delivery_material_errors(workspace, ("attempt-001",)) == ()


def test_delivery_revalidates_explicit_mapping_against_current_seed(
    tmp_path: Path,
) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    _write_seed_mapping(
        workspace, _valid_mapping(), body="Observed metric is 0.5。"
    )
    request = create_evaluation(workspace, sections, final_delivery=True)
    _write_role_reports(Path(request["path"]), 3)
    finalize_evaluation(workspace, request["evaluation_id"])
    workspace.write_review_decision(
        "评审完成。", measurement_key=request["measurement_key"]
    )

    changed = _valid_mapping()
    changed["seed_text"] = "Observed metric is 0.9。"
    changed["seed_value"] = 0.9
    _write_seed_mapping(workspace, changed, body="Observed metric is 0.9。")

    errors = delivery_material_errors(workspace, ("attempt-001",))
    assert any("explicit Seed metric mapping failed" in item for item in errors)
    assert any("final core evidence changed" in item for item in errors)


def test_delivery_rejects_packet_bytes_changed_after_canonical_review(
    tmp_path: Path,
) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    request = create_evaluation(workspace, sections, final_delivery=True)
    root = Path(request["path"])
    _write_role_reports(root, 3)
    finalize_evaluation(workspace, request["evaluation_id"])
    workspace.write_review_decision(
        "评审完成。", measurement_key=request["measurement_key"]
    )
    packet_path = root / "packet.md"
    packet_path.write_bytes(packet_path.read_bytes() + b"\nchanged after review\n")

    errors = delivery_material_errors(workspace, ("attempt-001",))

    assert any("packet.md changed after canonical measurement" in item for item in errors)


def test_tampered_request_cannot_rebind_changed_seed_and_core_evidence(
    tmp_path: Path,
) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    _write_seed_mapping(
        workspace, _valid_mapping(), body="Observed metric is 0.5。"
    )
    request = create_evaluation(workspace, sections, final_delivery=True)
    root = Path(request["path"])
    _write_role_reports(root, 3)
    finalize_evaluation(workspace, request["evaluation_id"])
    workspace.write_review_decision(
        "评审完成。", measurement_key=request["measurement_key"]
    )

    _write_seed_mapping(
        workspace,
        _valid_mapping(),
        body="Observed metric is 0.5。\n\nChanged conclusion after Review.",
    )
    current_seed_sha = workspace.read_seed().sha256
    closure = final_evidence_closure(workspace, ["attempt-001"])
    closure_data = (
        json.dumps(closure, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    ).encode("utf-8")
    request_path = root / "request.json"
    tampered = json.loads(request_path.read_text(encoding="utf-8"))
    for source in tampered["source_materials"]:
        if source["path"] == "seed_v001.md":
            source["sha256"] = current_seed_sha
            source["size_bytes"] = workspace.seed_path.stat().st_size
    tampered["final_core_evidence_sha256"] = hashlib.sha256(
        closure_data
    ).hexdigest()
    request_path.write_text(
        json.dumps(tampered, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    errors = delivery_material_errors(workspace, ("attempt-001",))

    assert any("request.json changed after canonical measurement" in item for item in errors)
    assert not any("final core evidence changed" in item for item in errors)
    assert not any("final Seed is not byte-bound" in item for item in errors)


@pytest.mark.parametrize("mutation", ["text", "source", "pointer", "value"])
def test_invalid_explicit_mapping_is_rejected_only_at_final_closeout(
    tmp_path: Path,
    mutation: str,
) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    mapping = _valid_mapping()
    body = "Observed metric is 0.5。"
    if mutation == "text":
        mapping["seed_text"] = "Absent metric text is 0.5。"
    elif mutation == "source":
        mapping["source_path"] = "experiment_v001/attempts/missing/metrics.json"
    elif mutation == "pointer":
        mapping["json_pointer"] = "/records/99/value"
    else:
        mapping["seed_text"] = "Observed metric is 0.9。"
        mapping["seed_value"] = 0.9
        body = "Observed metric is 0.9。"
    _write_seed_mapping(workspace, mapping, body=body)

    non_final = create_evaluation(workspace, sections, final_delivery=False)
    assert non_final["final_delivery_review"] is False
    with pytest.raises(ValueError, match="explicit evidence mapping is invalid"):
        create_evaluation(workspace, sections, final_delivery=True)


def test_final_packet_auto_exposes_bounded_core_spec_metrics_and_unmapped_advisory(
    tmp_path: Path,
) -> None:
    _, run, workspace, _ = _fixture(tmp_path)
    _write_seed_mapping(workspace, None, body="Observed but unmapped value is 0.5。")
    _expand_metrics(run, 100)
    sections = {
        1: ["seed_v001.md"],
        3: ["experiment_v001/attempts/attempt-001/stderr.bin"],
    }

    request = create_evaluation(workspace, sections, final_delivery=True)
    packet_bytes = (Path(request["path"]) / "packet.md").read_bytes()
    packet = packet_bytes.decode("utf-8")

    assert "Final Core Evidence Closure" in packet
    assert "seed_numeric_literals_unmapped" in packet
    assert '"explicit_metric_mapping_count": 0' in packet
    assert '"research_question": "测试问题？"' in packet
    assert '"claim-experiment-attempt-001"' in packet
    assert '"value": 0.5' in packet
    assert '"record_count": 100' in packet
    assert '"included_record_count": 64' in packet
    assert '"omitted_record_count": 36' in packet
    assert "def method()" not in packet
    assert len(packet_bytes) < 1024 * 1024


def test_three_roles_receive_identical_final_packet_bytes(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    request = create_evaluation(workspace, sections, final_delivery=True)
    received: dict[str, bytes] = {}

    def fake_invoke(
        role: str, packet: bytes, *, timeout_seconds: float
    ) -> dict[str, object]:
        received[role] = packet
        output = _review_output(role, 2)
        raw = (json.dumps(output, sort_keys=True) + "\n").encode("utf-8")
        return {
            "valid": True,
            "invalid_reasons": [],
            "runtime": {
                "timeout_seconds": timeout_seconds,
                "codex_version": "codex-cli 0.147.0",
            },
            "events": b"",
            "stderr": b"",
            "raw_output": raw,
            "output": output,
        }

    monkeypatch.setattr(reviewer_runtime, "_invoke_role", fake_invoke)
    aggregate = reviewer_runtime.run_evaluation(workspace, request["evaluation_id"])

    root = Path(request["path"])
    frozen = (root / "packet.md").read_bytes()
    request_data = (root / "request.json").read_bytes()
    assert set(received) == set(ROLES)
    assert all(value == frozen for value in received.values())
    assert aggregate["request_sha256"] == hashlib.sha256(request_data).hexdigest()
    for role in ROLES:
        report = json.loads((root / role / "report.json").read_text(encoding="utf-8"))
        assert report["request_sha256"] == aggregate["request_sha256"]
        assert report["packet_key"] == request["packet_key"]
        assert report["measurement_key"] == request["measurement_key"]


def test_review_inputs_cannot_be_rebound_between_execution_and_finalize(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    request = create_evaluation(workspace, sections, final_delivery=True)
    root = Path(request["path"])

    def fake_invoke(
        role: str, packet: bytes, *, timeout_seconds: float
    ) -> dict[str, object]:
        output = _review_output(role, 2)
        return {
            "valid": True,
            "invalid_reasons": [],
            "runtime": {
                "timeout_seconds": timeout_seconds,
                "codex_version": "codex-cli 0.147.0",
            },
            "events": b"",
            "stderr": b"",
            "raw_output": (json.dumps(output, sort_keys=True) + "\n").encode("utf-8"),
            "output": output,
        }

    def replace_with_self_consistent_packet_b(
        current_workspace: ResearchWorkspace, evaluation_id: str
    ) -> dict[str, object]:
        packet_path = root / "packet.md"
        packet_b = packet_path.read_bytes() + b"\nPacket B after Reviewer execution.\n"
        packet_path.write_bytes(packet_b)
        request_path = root / "request.json"
        changed = json.loads(request_path.read_text(encoding="utf-8"))
        changed["packet_key"] = hashlib.sha256(packet_b).hexdigest()
        changed["measurement_key"] = hashlib.sha256(
            (
                changed["implementation_key"]
                + changed["packet_key"]
                + changed["evaluator_definition_sha256"]
            ).encode("ascii")
        ).hexdigest()
        request_path.write_text(
            json.dumps(changed, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        return finalize_evaluation(current_workspace, evaluation_id)

    monkeypatch.setattr(reviewer_runtime, "_invoke_role", fake_invoke)
    monkeypatch.setattr(
        reviewer_runtime, "finalize_evaluation", replace_with_self_consistent_packet_b
    )

    with pytest.raises(ValueError, match="reviewer execution input identity mismatch"):
        reviewer_runtime.run_evaluation(workspace, request["evaluation_id"])
    assert not (root / "aggregate.json").exists()


def test_request_cannot_change_between_execution_and_finalize(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    request = create_evaluation(workspace, sections, final_delivery=True)
    root = Path(request["path"])

    def fake_invoke(
        role: str, packet: bytes, *, timeout_seconds: float
    ) -> dict[str, object]:
        output = _review_output(role, 2)
        return {
            "valid": True,
            "invalid_reasons": [],
            "runtime": {
                "timeout_seconds": timeout_seconds,
                "codex_version": "codex-cli 0.147.0",
            },
            "events": b"",
            "stderr": b"",
            "raw_output": (json.dumps(output, sort_keys=True) + "\n").encode("utf-8"),
            "output": output,
        }

    def change_request_only(
        current_workspace: ResearchWorkspace, evaluation_id: str
    ) -> dict[str, object]:
        request_path = root / "request.json"
        changed = json.loads(request_path.read_text(encoding="utf-8"))
        changed["source_materials"][0]["sha256"] = "0" * 64
        request_path.write_text(
            json.dumps(changed, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
            encoding="utf-8",
            newline="\n",
        )
        return finalize_evaluation(current_workspace, evaluation_id)

    monkeypatch.setattr(reviewer_runtime, "_invoke_role", fake_invoke)
    monkeypatch.setattr(reviewer_runtime, "finalize_evaluation", change_request_only)

    with pytest.raises(ValueError, match="request_sha256"):
        reviewer_runtime.run_evaluation(workspace, request["evaluation_id"])
    assert not (root / "aggregate.json").exists()


@pytest.mark.parametrize("field", ["request_sha256", "packet_key", "measurement_key"])
def test_finalize_rejects_role_report_input_identity_mismatch(
    tmp_path: Path, field: str
) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    request = create_evaluation(workspace, sections)
    root = Path(request["path"])
    _write_role_reports(root, 3)
    report_path = root / "EMP" / "report.json"
    report = json.loads(report_path.read_text(encoding="utf-8"))
    report[field] = "0" * 64
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
        newline="\n",
    )

    with pytest.raises(ValueError, match=field):
        finalize_evaluation(workspace, request["evaluation_id"])
    assert not (root / "aggregate.json").exists()


def test_expected_codex_cli_version_matches_recorded_runtime(
    tmp_path: Path,
) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    request = create_evaluation(workspace, sections)
    root = Path(request["path"])
    _write_role_reports(root, 3, codex_version="codex-cli 0.147.0")

    aggregate = finalize_evaluation(workspace, request["evaluation_id"])

    assert normalize_codex_cli_version("0.147.0") == "0.147.0"
    assert normalize_codex_cli_version("codex-cli 0.147.0") == "0.147.0"
    assert aggregate["valid"] is True
    assert aggregate["measurement_kind"] == "CANONICAL_IMPLEMENTATION_SCORE"
    for role in ROLES:
        report = json.loads((root / role / "report.json").read_text(encoding="utf-8"))
        assert report["runtime"]["codex_version"] == "codex-cli 0.147.0"


def test_mismatched_codex_cli_version_cannot_occupy_canonical_or_stability(
    tmp_path: Path,
) -> None:
    _, _, workspace, sections = _fixture(tmp_path)

    mismatched_first = create_evaluation(workspace, sections)
    first_root = Path(mismatched_first["path"])
    _write_role_reports(
        first_root, 4, codex_version="codex-cli 0.999.0"
    )
    first_aggregate = finalize_evaluation(
        workspace, mismatched_first["evaluation_id"]
    )

    assert first_aggregate["valid"] is False
    assert first_aggregate["measurement_kind"] == "INVALID_MEASUREMENT"
    assert first_aggregate["canonical_evaluation_id"] is None
    assert any(
        "expected 0.147.0, actual 0.999.0" in item
        for item in first_aggregate["invalid_reasons"]
    )
    first_report = json.loads(
        (first_root / "SCI" / "report.json").read_text(encoding="utf-8")
    )
    assert first_report["runtime"]["codex_version"] == "codex-cli 0.999.0"
    assert canonical_evaluation(
        workspace, mismatched_first["measurement_key"]
    ) is None

    matching = create_evaluation(workspace, sections)
    _write_role_reports(Path(matching["path"]), 2)
    matching_aggregate = finalize_evaluation(workspace, matching["evaluation_id"])
    assert matching_aggregate["measurement_kind"] == "CANONICAL_IMPLEMENTATION_SCORE"

    mismatched_later = create_evaluation(workspace, sections)
    _write_role_reports(
        Path(mismatched_later["path"]),
        4,
        codex_version="codex-cli 0.999.0",
    )
    later_aggregate = finalize_evaluation(
        workspace, mismatched_later["evaluation_id"]
    )

    assert later_aggregate["valid"] is False
    assert later_aggregate["measurement_kind"] == "INVALID_MEASUREMENT"
    assert later_aggregate["canonical_evaluation_id"] is None
    canonical = canonical_evaluation(workspace, matching["measurement_key"])
    assert canonical is not None
    assert canonical["evaluation_id"] == matching["evaluation_id"]


def test_first_valid_triplet_is_canonical_and_same_packet_only_stability(tmp_path: Path) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    first = create_evaluation(workspace, sections)
    _write_role_reports(Path(first["path"]), 2)
    first_aggregate = finalize_evaluation(workspace, first["evaluation_id"])

    second = create_evaluation(workspace, sections)
    _write_role_reports(Path(second["path"]), 4)
    second_aggregate = finalize_evaluation(workspace, second["evaluation_id"])

    assert first["measurement_key"] == second["measurement_key"]
    assert first_aggregate["measurement_kind"] == "CANONICAL_IMPLEMENTATION_SCORE"
    assert first_aggregate["overall_score_percent"] == "50.0000"
    assert second_aggregate["measurement_kind"] == "STABILITY_MEASUREMENT"
    assert second_aggregate["canonical_evaluation_id"] == first["evaluation_id"]
    assert second_aggregate["overall_score_percent"] == "100.0000"
    unchanged = json.loads(
        (Path(first["path"]) / "aggregate.json").read_text(encoding="utf-8")
    )
    assert unchanged["overall_score_percent"] == "50.0000"


def test_invalid_first_group_does_not_occupy_canonical(tmp_path: Path) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    invalid = create_evaluation(workspace, sections)
    _write_role_reports(Path(invalid["path"]), 4, valid=False)
    invalid_aggregate = finalize_evaluation(workspace, invalid["evaluation_id"])
    valid = create_evaluation(workspace, sections)
    _write_role_reports(Path(valid["path"]), 1)
    valid_aggregate = finalize_evaluation(workspace, valid["evaluation_id"])

    assert invalid_aggregate["measurement_kind"] == "INVALID_MEASUREMENT"
    assert valid_aggregate["measurement_kind"] == "CANONICAL_IMPLEMENTATION_SCORE"


def test_same_implementation_changed_packet_is_linked_but_new_measurement(tmp_path: Path) -> None:
    _, run, workspace, sections = _fixture(tmp_path)
    first = create_evaluation(workspace, sections)
    _write_role_reports(Path(first["path"]), 2)
    finalize_evaluation(workspace, first["evaluation_id"])
    (run / "overview_v001.md").write_text(
        "Mechanism overview with a disclosed limitation.\n",
        encoding="utf-8",
        newline="\n",
    )
    second = create_evaluation(workspace, sections)
    _write_role_reports(Path(second["path"]), 3)
    finalize_evaluation(workspace, second["evaluation_id"])

    assert first["implementation_key"] == second["implementation_key"]
    assert first["packet_key"] != second["packet_key"]
    assert first["measurement_key"] != second["measurement_key"]
    history = implementation_measurement_history(workspace, first["implementation_key"])
    assert {item["measurement_key"] for item in history} == {
        first["measurement_key"], second["measurement_key"]
    }


def test_fixed_integer_scoring_and_tool_event_detection() -> None:
    assert role_score_basis_points("SCI", {name: 4 for name in DIMENSION_WEIGHTS["SCI"]}) == 10000
    assert role_score_basis_points("EMP", {name: 2 for name in DIMENSION_WEIGHTS["EMP"]}) == 5000
    assert _event_is_forbidden({"type": "item.completed", "item": {"type": "agent_message"}}) is False
    assert _event_is_forbidden({"type": "item.started", "item": {"type": "command_execution"}}) is True


def test_v3_delivery_binds_final_implementation_packet_and_canonical_review(
    tmp_path: Path,
) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    request = create_evaluation(workspace, sections, final_delivery=True)
    _write_role_reports(Path(request["path"]), 3)
    finalize_evaluation(workspace, request["evaluation_id"])
    decision = workspace.write_review_decision(
        "主研究者已阅读三份固定评审并决定交付。",
        measurement_key=request["measurement_key"],
    )

    assert decision.measurement_key == request["measurement_key"]
    assert delivery_material_errors(workspace, ("attempt-001",)) == ()
    terminal = workspace.write_delivery(supporting_attempt_ids=("attempt-001",))

    assert terminal.status == "DELIVERED"
    assert request["measurement_key"] in terminal.content
    assert read_delivery(workspace).sha256 == terminal.sha256


def test_changed_final_implementation_cannot_use_old_high_review(tmp_path: Path) -> None:
    _, _, workspace, sections = _fixture(tmp_path)
    request = create_evaluation(workspace, sections, final_delivery=True)
    _write_role_reports(Path(request["path"]), 4)
    finalize_evaluation(workspace, request["evaluation_id"])
    workspace.write_review_decision(
        "暂定交付。", measurement_key=request["measurement_key"]
    )
    (workspace.implementation_path / "method.py").write_text(
        "def method():\n    return 'changed implementation'\n",
        encoding="utf-8",
        newline="\n",
    )

    errors = delivery_material_errors(workspace, ("attempt-001",))

    assert any("implementation differs" in error for error in errors)
