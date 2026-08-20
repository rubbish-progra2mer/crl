from __future__ import annotations

import json
from pathlib import Path

from tools.audit_knowledge_base import main
from test_knowledge_audit import make_audit_fixture


def test_cli_defaults_to_stdout_and_optional_report_stays_outside_run(
    tmp_path: Path, capsys
) -> None:
    project, knowledge, _ = make_audit_fixture(tmp_path)

    assert main(["--project-root", str(project), "--knowledge-root", str(knowledge)]) == 0
    payload = json.loads(capsys.readouterr().out)
    assert payload["audit_kind"] == "independent_knowledge_base_maintenance_audit"
    assert not (knowledge / "knowledge_audit.json").exists()

    maintenance = project / "maintenance" / "audit-001"
    assert main(
        [
            "--project-root",
            str(project),
            "--knowledge-root",
            str(knowledge),
            "--write-report",
            str(maintenance),
        ]
    ) == 0
    written = maintenance / "knowledge_audit.json"
    assert json.loads(written.read_text(encoding="utf-8"))["audit_kind"] == payload["audit_kind"]


def test_cli_rejects_report_inside_formal_run(tmp_path: Path, capsys) -> None:
    project, knowledge, _ = make_audit_fixture(tmp_path)
    run = project / "20260810_1200_run01"
    run.mkdir()

    assert main(
        [
            "--project-root",
            str(project),
            "--knowledge-root",
            str(knowledge),
            "--write-report",
            str(run / "maintenance"),
        ]
    ) == 2
    assert "formal Run" in capsys.readouterr().err
    assert list(run.iterdir()) == []

