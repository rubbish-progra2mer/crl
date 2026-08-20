from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.manage_review import main
from conftest import make_run
from crl_v3.workspace import ResearchWorkspace


def _call(argv: list[str], capsys: pytest.CaptureFixture[str]) -> dict[str, object]:
    assert main(argv) == 0
    return json.loads(capsys.readouterr().out)


def test_cli_creates_request_saves_raw_reports_and_reports_status(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    product, run = make_run(tmp_path)
    (run / "candidate_v001.md").write_bytes("候选\n".encode("utf-8"))
    (run / "seed_v001.md").write_bytes("种子\n".encode("utf-8"))
    note = tmp_path / "note.md"
    note.write_bytes("自由形成科学意见。\n".encode("utf-8"))
    request = _call(
        [
            "create-request",
            "--product-root",
            str(product),
            "--run-root",
            str(run),
            "--body-file",
            str(note),
            "--reading",
            "seed_v001.md",
            "--reading",
            "candidate_v001.md",
        ],
        capsys,
    )
    assert Path(str(request["path"])).name == "request.md"

    for number in (1, 2, 3):
        report_file = tmp_path / f"report-{number}.md"
        report_file.write_bytes(f"原始意见 {number}\n第二行\n".encode("utf-8"))
        payload = _call(
            [
                "save-report",
                "--product-root",
                str(product),
                "--run-root",
                str(run),
                "--reviewer-number",
                str(number),
                "--reviewer-id",
                f"task-{number}",
                "--report-file",
                str(report_file),
            ],
            capsys,
        )
        assert payload["reviewer_id"] == f"task-{number}"
        assert f"原始意见 {number}" in Path(str(payload["path"])).read_text(
            encoding="utf-8"
        )

    status = _call(
        ["status", "--product-root", str(product), "--run-root", str(run)], capsys
    )
    assert status["request_exists"] is True
    assert len(status["reviewers"]) == 3


def test_cli_has_no_packet_or_staging_commands(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    with pytest.raises(SystemExit):
        main(["freeze-packet", "--product-root", str(product), "--run-root", str(run)])
    with pytest.raises(SystemExit):
        main(["compare-staged", "--product-root", str(product), "--run-root", str(run)])


def test_cli_render_input_writes_only_deterministic_complete_stdout(
    tmp_path: Path, capsysbinary: pytest.CaptureFixture[bytes]
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_seed("种子与 English claim")
    workspace.write_candidate("候选正文")
    workspace.write_review_request(
        "寻找最小反例。",
        ["seed_v001.md", "candidate_v001.md"],
    )
    before = sorted(
        path.relative_to(run).as_posix() for path in run.rglob("*") if path.is_file()
    )
    arguments = [
        "render-input",
        "--product-root",
        str(product),
        "--run-root",
        str(run),
        "--version",
        "v001",
    ]

    assert main(arguments) == 0
    first = capsysbinary.readouterr().out
    assert main(arguments) == 0
    second = capsysbinary.readouterr().out

    assert first == second
    assert "种子与 English claim".encode("utf-8") in first
    assert first.count(b"===== BEGIN MATERIAL =====") == 2
    assert sorted(
        path.relative_to(run).as_posix() for path in run.rglob("*") if path.is_file()
    ) == before


def test_cli_rejects_duplicate_reviewer_context(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    product, run = make_run(tmp_path)
    (run / "candidate_v001.md").write_bytes(b"candidate\n")
    (run / "seed_v001.md").write_bytes(b"seed\n")
    note = tmp_path / "note.md"
    note.write_bytes(b"review\n")
    assert main(
        [
            "create-request",
            "--product-root",
            str(product),
            "--run-root",
            str(run),
            "--body-file",
            str(note),
            "--reading",
            "seed_v001.md",
            "--reading",
            "candidate_v001.md",
        ]
    ) == 0
    capsys.readouterr()
    report = tmp_path / "report.md"
    report.write_bytes(b"opinion\n")
    base = ["--product-root", str(product), "--run-root", str(run), "--reviewer-id", "same", "--report-file", str(report)]
    assert main(["save-report", *base, "--reviewer-number", "1"]) == 0
    capsys.readouterr()
    assert main(["save-report", *base, "--reviewer-number", "2"]) == 1
    assert "already used" in capsys.readouterr().err
