from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

import pytest

import tools.manage_run as manage_run_module
from tools.manage_run import advance_version, main, pause_run, start_run, terminate_run
from tools.inspect_run import inspect_run
from crl_v3.workspace import ResearchWorkspace
from conftest import publish_synthetic_fixed_review, record_successful_attempt


FIXED_NOW = datetime(2026, 7, 31, 14, 35, tzinfo=ZoneInfo("Asia/Shanghai"))


def _transition() -> dict[str, object]:
    return {
        "CHANGED_COORDINATE": "failure phenomenon",
        "SURVIVING_FRONTIER": "A distinct evaluation opportunity remains.",
        "NEXT_HIGH_INFORMATION_ACTION": "Run the discriminating experiment.",
    }


def _existing_run(
    root: Path, name: str, status: str, *, contract_version: str = "3"
) -> Path:
    run = root / name
    run.mkdir()
    (run / "RUN_STATUS.md").write_text(
        f"RUN_ID: {name}\nSTATUS: {status}\nCURRENT_VERSION: v001\nMODE: AUTONOMOUS\n",
        encoding="utf-8",
        newline="\n",
    )
    (run / "RUN_CHARTER.md").write_bytes(
        (
            f"# Run Charter\n\nRUN_ID: {name}\n"
            f"CRL_CONTRACT_VERSION: {contract_version}\n"
            "DEFAULT_DOMAIN: TEXT_AND_TOOL_LLM_AGENT\nMODE: AUTONOMOUS\n"
        ).encode("utf-8")
    )
    (run / "RUN_LEDGER.md").write_bytes(b"# Run Ledger\n\n- EVENT: CREATED\n")
    return run


def _publish_delivery(root: Path, run: Path) -> None:
    workspace = ResearchWorkspace(run, product_root=root)
    workspace.write_seed("# Seed\n\nvalidated")
    source = run / "workbench_v001" / "input.txt"
    source.parent.mkdir()
    source.write_text("evidence input\n", encoding="utf-8", newline="\n")
    completed = record_successful_attempt(root, run, "v001", source)
    assert completed.returncode == 0, completed.stderr.decode(
        "utf-8", errors="replace"
    )
    workspace.write_review_request("review", ["seed_v001.md"])
    for number in (1, 2, 3):
        workspace.write_reviewer_report(number, f"resume-task-{number}", "opinion")
    publish_synthetic_fixed_review(
        workspace,
        supporting_attempt_id="attempt-001",
        final_delivery=True,
    )
    workspace.write_review_decision("deliver")
    workspace.write_delivery(supporting_attempt_ids=("attempt-001",))


def _publish_historical_no_delivery(
    run: Path, reason: str = "当前路线无价值。"
) -> None:
    terminal = (
        "# CRL No-Go Conclusion\n"
        '<!-- CRL_TERMINAL_META {"status":"CONCLUDED_NO_DELIVERY",'
        '"version":"v001"} -->\n\n'
        f"{reason}\n"
    )
    (run / "NO_DELIVERY.md").write_bytes(terminal.encode("utf-8"))
    status_path = run / "RUN_STATUS.md"
    status = status_path.read_text(encoding="utf-8").replace(
        "STATUS: ACTIVE", "STATUS: CONCLUDED_NO_DELIVERY"
    )
    status_path.write_text(status, encoding="utf-8", newline="\n")


def test_start_directly_creates_new_autonomous_run_without_machine_gate(tmp_path: Path) -> None:
    root = tmp_path / "product"
    root.mkdir()
    _existing_run(root, "20260728_0111_run04", "ACTIVE")
    payload = start_run(root, now=FIXED_NOW)

    assert payload["action"] == "create"
    assert payload["run_id"] == "20260731_1435_run05"
    assert payload["mode"] == "AUTONOMOUS"
    created = Path(payload["run_root"])
    assert sorted(path.name for path in created.iterdir()) == [
        "RUN_CHARTER.md",
        "RUN_LEDGER.md",
        "RUN_STATUS.md",
    ]
    charter = (created / "RUN_CHARTER.md").read_text(encoding="utf-8")
    assert "CRL_CONTRACT_VERSION: 3" in charter
    assert "文本与工具型 LLM Agent" in charter
    assert "READY" not in charter
    assert "COMMISSION" not in charter.upper()
    assert "SEED_UPGRADE" not in charter
    terminal = ResearchWorkspace(created, product_root=root).write_no_delivery(
        "After real backtracking and re-expansion, expected further research value is insufficient."
    )
    assert terminal.status == "CONCLUDED_NO_DELIVERY"
    assert (created / "NO_DELIVERY.md").is_file()
    assert "STATUS: CONCLUDED_NO_DELIVERY" in (created / "RUN_STATUS.md").read_text(
        encoding="utf-8"
    )


def test_v2_run_cannot_resume_into_v3(tmp_path: Path) -> None:
    root = tmp_path / "product"
    root.mkdir()
    run = _existing_run(
        root, "20260731_1200_run01", "ACTIVE", contract_version="2"
    )
    before = {path.name: path.read_bytes() for path in run.iterdir()}
    with pytest.raises(ValueError, match="read-only"):
        start_run(root, requested_run=run.name)
    assert {path.name: path.read_bytes() for path in run.iterdir()} == before


def test_direction_is_recorded_as_hard_boundary(tmp_path: Path) -> None:
    root = tmp_path / "product"
    root.mkdir()
    payload = start_run(root, direction="仅研究图神经网络鲁棒性", now=FIXED_NOW)
    charter = (Path(payload["run_root"]) / "RUN_CHARTER.md").read_text(encoding="utf-8")
    assert payload["mode"] == "DIRECTED"
    assert "仅研究图神经网络鲁棒性" in charter
    assert "定向 Run 不得越出用户方向" in charter
    terminal = ResearchWorkspace(
        Path(payload["run_root"]), product_root=root
    ).write_no_delivery("该明确方向已经耗尽。")
    assert terminal.status == "CONCLUDED_NO_DELIVERY"


def test_direction_preserves_meaningful_whitespace_and_normalizes_lf(tmp_path: Path) -> None:
    root = tmp_path / "product"
    root.mkdir()
    direction = "  第一段\r\n\r\n- 保留缩进\r\n"
    payload = start_run(root, direction=direction, now=FIXED_NOW)
    data = (Path(payload["run_root"]) / "RUN_CHARTER.md").read_bytes()
    assert b"\r" not in data
    assert "  第一段\n\n- 保留缩进\n" in data.decode("utf-8")


def test_resume_must_be_explicit_and_invalid_or_permanent_terminal_is_rejected(
    tmp_path: Path,
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    active = _existing_run(root, "20260728_0111_run04", "ACTIVE")
    delivered = _existing_run(root, "20260726_1955_run03", "DELIVERED")

    payload = start_run(root, requested_run="run04")
    assert payload["action"] == "resume"
    assert Path(payload["run_root"]) == active
    with pytest.raises(ValueError, match="matching valid conclusion"):
        start_run(root, requested_run=delivered.name)

    absolute = start_run(root, requested_run=str(active.resolve()))
    assert Path(absolute["run_root"]) == active

    (active / "NO_DELIVERY.md").write_bytes(b"terminal\n")
    with pytest.raises(ValueError, match="NO_DELIVERY.md") as caught:
        start_run(root, requested_run=str(active.resolve()))
    assert "missing or duplicate bounded metadata" in str(caught.value)


def test_invalid_delivery_resume_error_preserves_artifact_and_parser_reason(
    tmp_path: Path,
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    run = _existing_run(root, "20260728_0111_run04", "ACTIVE")
    (run / "DELIVERY.md").write_bytes(b"terminal\n")

    with pytest.raises(ValueError, match="DELIVERY.md") as caught:
        start_run(root, requested_run=run.name)

    assert "missing or duplicate bounded terminal metadata" in str(caught.value)


def test_explicit_resume_of_no_delivery_preserves_history_and_advances_version(
    tmp_path: Path,
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    run = _existing_run(root, "20260728_0111_run04", "ACTIVE")
    _publish_historical_no_delivery(run)
    original = (run / "NO_DELIVERY.md").read_bytes()

    with pytest.raises(FileExistsError, match="no-delivery Run"):
        advance_version(root, run.name, transition=_transition(), now=FIXED_NOW)

    payload = start_run(root, requested_run=run.name)

    assert payload["status"] == "ACTIVE"
    assert payload["current_version"] == "v002"
    assert (run / "NO_DELIVERY.md").read_bytes() == original
    status = (run / "RUN_STATUS.md").read_text(encoding="utf-8")
    ledger = (run / "RUN_LEDGER.md").read_text(encoding="utf-8")
    assert "STATUS: ACTIVE" in status
    assert "CURRENT_VERSION: v002" in status
    assert "EVENT: NO_DELIVERY_RUN_RESUMED" in ledger
    assert "PRIOR_NO_DELIVERY_SHA256:" in ledger
    report = inspect_run(run, product_root=root)
    assert report["no_delivery_count"] == 1
    assert report["no_delivery_history"][0]["version"] == "v001"
    assert "ACTIVE_CURRENT_VERSION_EMPTY" in report["errors"]


def test_ordinary_start_does_not_resume_no_delivery_run(tmp_path: Path) -> None:
    root = tmp_path / "product"
    root.mkdir()
    run = _existing_run(root, "20260728_0111_run04", "ACTIVE")
    _publish_historical_no_delivery(run)
    original_status = (run / "RUN_STATUS.md").read_bytes()

    payload = start_run(root, now=FIXED_NOW)

    assert payload["action"] == "create"
    assert Path(payload["run_root"]) != run
    assert (run / "RUN_STATUS.md").read_bytes() == original_status


def test_no_delivery_resume_rolls_back_controls_without_touching_history(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    run = _existing_run(root, "20260728_0111_run04", "ACTIVE")
    _publish_historical_no_delivery(run)
    original_status = (run / "RUN_STATUS.md").read_bytes()
    original_ledger = (run / "RUN_LEDGER.md").read_bytes()
    original_no_delivery = (run / "NO_DELIVERY.md").read_bytes()
    real_write = manage_run_module._atomic_write_text
    calls = 0

    def fail_second_write(path, content, *, within=None):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("simulated no-delivery resume failure")
        return real_write(path, content, within=within)

    monkeypatch.setattr(manage_run_module, "_atomic_write_text", fail_second_write)
    with pytest.raises(OSError, match="simulated no-delivery resume failure"):
        start_run(root, requested_run=run.name)

    assert (run / "RUN_STATUS.md").read_bytes() == original_status
    assert (run / "RUN_LEDGER.md").read_bytes() == original_ledger
    assert (run / "NO_DELIVERY.md").read_bytes() == original_no_delivery


def test_explicit_resume_of_delivered_run_preserves_delivery_and_advances_version(
    tmp_path: Path,
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    run = _existing_run(root, "20260728_0111_run04", "ACTIVE")
    _publish_delivery(root, run)
    original_delivery = (run / "DELIVERY.md").read_bytes()

    payload = start_run(root, requested_run=run.name)

    assert payload["action"] == "resume"
    assert payload["status"] == "ACTIVE"
    assert payload["current_version"] == "v002"
    assert (run / "DELIVERY.md").read_bytes() == original_delivery
    assert "STATUS: ACTIVE" in (run / "RUN_STATUS.md").read_text(encoding="utf-8")
    assert "CURRENT_VERSION: v002" in (run / "RUN_STATUS.md").read_text(
        encoding="utf-8"
    )
    ledger = (run / "RUN_LEDGER.md").read_text(encoding="utf-8")
    assert "EVENT: DELIVERED_RUN_RESUMED" in ledger
    assert "PRIOR_DELIVERY_SHA256:" in ledger
    report = inspect_run(run, product_root=root)
    assert report["status"] == "ACTIVE"
    assert report["terminal"] is False
    assert report["delivery_count"] == 1
    assert report["delivery_history"][0]["version"] == "v001"
    assert "ACTIVE_CURRENT_VERSION_EMPTY" in report["errors"]


def test_delivered_resume_rolls_back_controls_without_touching_delivery(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    run = _existing_run(root, "20260728_0111_run04", "ACTIVE")
    _publish_delivery(root, run)
    original_status = (run / "RUN_STATUS.md").read_bytes()
    original_ledger = (run / "RUN_LEDGER.md").read_bytes()
    original_delivery = (run / "DELIVERY.md").read_bytes()
    real_write = manage_run_module._atomic_write_text
    calls = 0

    def fail_second_write(path, content, *, within=None):
        nonlocal calls
        calls += 1
        if calls == 2:
            raise OSError("simulated delivered resume failure")
        return real_write(path, content, within=within)

    monkeypatch.setattr(manage_run_module, "_atomic_write_text", fail_second_write)
    with pytest.raises(OSError, match="simulated delivered resume failure"):
        start_run(root, requested_run=run.name)

    assert (run / "RUN_STATUS.md").read_bytes() == original_status
    assert (run / "RUN_LEDGER.md").read_bytes() == original_ledger
    assert (run / "DELIVERY.md").read_bytes() == original_delivery


def test_new_run_number_uses_names_not_historical_status_validity(tmp_path: Path) -> None:
    root = tmp_path / "product"
    root.mkdir()
    old = root / "20260722_1550_run09"
    old.mkdir()
    (old / "RUN_STATUS.md").write_text("historical format", encoding="utf-8")
    payload = start_run(root, now=FIXED_NOW)
    assert payload["run_number"] == "run10"


def test_cli_supports_direction_file_and_has_no_removed_modes(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    direction = tmp_path / "direction.md"
    direction.write_text("限定方向", encoding="utf-8")
    code = main(
        [
            "start",
            "--product-root",
            str(root),
            "--direction-file",
            str(direction),
        ]
    )
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["mode"] == "DIRECTED"

    with pytest.raises(SystemExit):
        main(["start", "--product-root", str(root), "--commissioning"])


def test_advance_version_help_declares_transition_json(capsys: pytest.CaptureFixture[str]) -> None:
    with pytest.raises(SystemExit) as error:
        main(["advance-version", "--help"])
    assert error.value.code == 0
    help_text = capsys.readouterr().out
    assert "JSON object" in help_text
    assert "CHANGED_COORDINATE" in help_text


def test_explicit_version_advance_synchronizes_status_ledger_inspect_and_resume(
    tmp_path: Path,
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    run = _existing_run(root, "20260728_0111_run04", "ACTIVE")
    negative = run / "failure_attribution_v001.md"
    negative.write_text("局部候选被反证。\n", encoding="utf-8", newline="\n")
    negative_before = negative.read_bytes()
    payload = advance_version(
        root, run.name, transition=_transition(), now=FIXED_NOW
    )
    assert payload["previous_version"] == "v001"
    assert payload["current_version"] == "v002"
    status = (run / "RUN_STATUS.md").read_text(encoding="utf-8")
    ledger = (run / "RUN_LEDGER.md").read_text(encoding="utf-8")
    assert "CURRENT_VERSION: v002" in status
    assert "FROM_VERSION: v001" in ledger and "VERSION: v002" in ledger
    continuation = run / "selection_context_v002.md"
    assert continuation.is_file()
    continuation_text = continuation.read_text(encoding="utf-8")
    assert "CHANGED_COORDINATE" in continuation_text
    assert "SURVIVING_FRONTIER" in continuation_text
    assert "NEXT_HIGH_INFORMATION_ACTION" in continuation_text
    assert "LAST_DURABLE_ARTIFACT: selection_context_v002.md" in status
    assert "CONTINUATION_SHA256" in ledger
    assert "STATUS: ACTIVE" in status
    assert negative.read_bytes() == negative_before
    assert not (run / "NO_DELIVERY.md").exists()
    ResearchWorkspace(run, version="v002", product_root=root).write_problem(
        "# 新研究问题\n\n结构不同的 v002 探索。"
    )
    assert (run / "problem_v002.md").is_file()
    report = inspect_run(run, product_root=root)
    assert report["current_version"] == "v002"
    assert report["status_current_version"] == "v002"
    resumed = start_run(root, requested_run=run.name)
    assert resumed["current_version"] == "v002"


def test_version_advance_rejects_terminal_and_conflicting_future_artifacts(
    tmp_path: Path,
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    terminal = _existing_run(root, "20260728_0111_run04", "DELIVERED")
    with pytest.raises(FileExistsError, match="delivered Run"):
        advance_version(
            root, terminal.name, transition=_transition(), now=FIXED_NOW
        )

    active = _existing_run(root, "20260728_0112_run05", "ACTIVE")
    (active / "candidate_v002.md").write_text(
        "future\n", encoding="utf-8", newline="\n"
    )
    with pytest.raises(ValueError, match="newer than CURRENT_VERSION"):
        advance_version(
            root, active.name, transition=_transition(), now=FIXED_NOW
        )
    with pytest.raises(ValueError, match="newer than CURRENT_VERSION"):
        start_run(root, requested_run=active.name)


@pytest.mark.parametrize("failure_call", [1, 2, 3])
def test_version_advance_rolls_back_every_publication_failure(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    failure_call: int,
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    run = _existing_run(root, "20260728_0111_run04", "ACTIVE")
    original_status = (run / "RUN_STATUS.md").read_bytes()
    original_ledger = (run / "RUN_LEDGER.md").read_bytes()
    real_write = manage_run_module._atomic_write_text
    calls = 0

    def fail_selected_write(path, content, *, within=None):
        nonlocal calls
        calls += 1
        if calls == failure_call:
            raise OSError(f"simulated publication failure {failure_call}")
        return real_write(path, content, within=within)

    monkeypatch.setattr(manage_run_module, "_atomic_write_text", fail_selected_write)
    with pytest.raises(OSError, match="simulated"):
        advance_version(root, run.name, transition=_transition(), now=FIXED_NOW)
    assert (run / "RUN_STATUS.md").read_bytes() == original_status
    assert (run / "RUN_LEDGER.md").read_bytes() == original_ledger
    assert not (run / "selection_context_v002.md").exists()


def test_version_advance_requires_three_nonempty_continuation_fields(
    tmp_path: Path,
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    run = _existing_run(root, "20260728_0111_run04", "ACTIVE")
    with pytest.raises(ValueError, match="missing=.*SURVIVING_FRONTIER"):
        advance_version(
            root,
            run.name,
            transition={
                "CHANGED_COORDINATE": "problem",
                "NEXT_HIGH_INFORMATION_ACTION": "test",
            },
            now=FIXED_NOW,
        )
    assert "CURRENT_VERSION: v001" in (run / "RUN_STATUS.md").read_text(
        encoding="utf-8"
    )
    assert not (run / "selection_context_v002.md").exists()


def test_pause_requires_explicit_resume_and_user_termination_is_permanent(
    tmp_path: Path,
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    run = _existing_run(root, "20260728_0111_run04", "ACTIVE")
    paused = pause_run(root, run.name, note="稍后继续", now=FIXED_NOW)
    assert paused["status"] == "PAUSED_BY_USER"
    workspace = __import__("crl_v3.workspace", fromlist=["ResearchWorkspace"]).ResearchWorkspace(
        run, product_root=root
    )
    with pytest.raises(PermissionError, match="paused"):
        workspace.write_problem("must not write")
    resumed = start_run(root, requested_run=run.name)
    assert resumed["status"] == "ACTIVE"
    terminated = terminate_run(root, run.name, note="用户永久结束", now=FIXED_NOW)
    assert terminated["status"] == "TERMINATED_BY_USER"
    assert (run / "TERMINATED_BY_USER.md").is_file()
    with pytest.raises(ValueError, match="terminal Run"):
        start_run(root, requested_run=run.name)


def test_user_termination_can_follow_no_delivery_history_and_is_permanent(
    tmp_path: Path,
) -> None:
    root = tmp_path / "product"
    root.mkdir()
    run = _existing_run(root, "20260728_0111_run04", "ACTIVE")
    _publish_historical_no_delivery(run)
    no_delivery_bytes = (run / "NO_DELIVERY.md").read_bytes()
    start_run(root, requested_run=run.name)

    terminated = terminate_run(root, run.name, note="用户永久结束", now=FIXED_NOW)

    assert terminated["status"] == "TERMINATED_BY_USER"
    assert (run / "NO_DELIVERY.md").read_bytes() == no_delivery_bytes
    assert (run / "TERMINATED_BY_USER.md").is_file()
    report = inspect_run(run, product_root=root)
    assert report["no_delivery_count"] == 1
    assert report["status"] == "TERMINATED_BY_USER"
    assert report["errors"] == []
    with pytest.raises(ValueError, match="terminal Run"):
        start_run(root, requested_run=run.name)
