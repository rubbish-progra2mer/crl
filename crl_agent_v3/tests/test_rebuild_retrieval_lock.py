from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

import tools.rebuild_retrieval_lock as lock_module
from conftest import make_directory_reparse_point
from test_knowledge_audit import make_audit_fixture
from tools.rebuild_retrieval_lock import rebuild_retrieval_lock


def _attempt(project: Path) -> Path:
    attempt = project / "knowledge_base" / "evaluation" / "accepted" / "v001"
    attempt.mkdir(parents=True)
    (attempt / "result.json").write_text(
        '{"measurement": 1}\n', encoding="utf-8", newline="\n"
    )
    (attempt / "report.md").write_text(
        "# Evaluation report\n", encoding="utf-8", newline="\n"
    )
    return attempt


def _asset_snapshot(knowledge: Path) -> dict[str, bytes]:
    names = ("knowledge.sqlite", "cards_fts.sqlite", "passages.npz")
    snapshot = {
        name: (knowledge / name).read_bytes()
        for name in names
        if (knowledge / name).is_file()
    }
    snapshot.update(
        {
            path.relative_to(knowledge).as_posix(): path.read_bytes()
            for directory in ("cards", "corpus", "papers")
            for path in (knowledge / directory).rglob("*")
            if path.is_file()
        }
    )
    return snapshot


def test_explicit_lock_rebuild_records_only_existing_verified_paths_and_not_assets(
    tmp_path: Path,
) -> None:
    project, knowledge, _ = make_audit_fixture(tmp_path)
    attempt = _attempt(project)
    output = project / "maintenance" / "rebuilt-lock.json"
    before = _asset_snapshot(knowledge)

    document = rebuild_retrieval_lock(
        knowledge_root=knowledge,
        project_root=project,
        accepted_attempt=attempt,
        output=output,
    )

    assert output.is_file()
    assert json.loads(output.read_text(encoding="utf-8")) == document
    assert document["accepted_attempt"] == attempt.relative_to(project).as_posix()
    assert set(document["accepted_evidence"]) == {"report", "result"}
    for entry in document["accepted_evidence"].values():
        path = project.joinpath(*Path(entry["path"]).parts)
        assert path.is_file()
        assert hashlib.sha256(path.read_bytes()).hexdigest() == entry["sha256"]
    for entry in document["source_snapshot"].values():
        if isinstance(entry, dict):
            assert project.joinpath(*Path(entry["path"]).parts).is_file()
    assert _asset_snapshot(knowledge) == before
    with pytest.raises(FileExistsError, match="--replace"):
        rebuild_retrieval_lock(
            knowledge_root=knowledge,
            project_root=project,
            accepted_attempt=attempt,
            output=output,
        )


@pytest.mark.parametrize(
    "bad_output",
    [
        lambda project, knowledge: project.parent / "outside.json",
        lambda project, knowledge: knowledge / "corpus" / "lock.json",
        lambda project, knowledge: project / "20260810_1200_run01" / "lock.json",
        lambda project, knowledge: project / "maintenance" / "lock.txt",
    ],
)
def test_rebuild_rejects_invalid_output_paths(tmp_path: Path, bad_output) -> None:
    project, knowledge, _ = make_audit_fixture(tmp_path)
    attempt = _attempt(project)
    (project / "20260810_1200_run01").mkdir(exist_ok=True)
    output = bad_output(project, knowledge)

    with pytest.raises(ValueError):
        rebuild_retrieval_lock(
            knowledge_root=knowledge,
            project_root=project,
            accepted_attempt=attempt,
            output=output,
        )


def test_atomic_replace_failure_preserves_old_lock_and_cleans_temporary(
    tmp_path: Path, monkeypatch
) -> None:
    project, knowledge, _ = make_audit_fixture(tmp_path)
    attempt = _attempt(project)
    output = project / "maintenance" / "lock.json"
    output.parent.mkdir()
    output.write_bytes(b"old-lock\n")

    def fail_replace(source: Path, destination: Path) -> None:
        raise OSError("injected atomic replace failure")

    monkeypatch.setattr(lock_module, "_replace", fail_replace)
    with pytest.raises(OSError, match="atomic replace"):
        rebuild_retrieval_lock(
            knowledge_root=knowledge,
            project_root=project,
            accepted_attempt=attempt,
            output=output,
            replace=True,
        )

    assert output.read_bytes() == b"old-lock\n"
    assert not list(output.parent.glob(".*.tmp"))


def test_matching_previous_lock_requires_accepted_result_and_report_hashes(
    tmp_path: Path,
) -> None:
    project, knowledge, _ = make_audit_fixture(tmp_path)
    attempt = _attempt(project)
    lock = knowledge / "evaluation" / "PRODUCTION_RETRIEVAL_LOCK.json"
    result = attempt / "result.json"
    report = attempt / "report.md"
    lock.write_text(
        json.dumps(
            {
                "schema_version": 2,
                "accepted_attempt": attempt.relative_to(project).as_posix(),
                "accepted_evidence": {
                    "result": {
                        "path": result.relative_to(project).as_posix(),
                        "sha256": "0" * 64,
                    },
                    "report": {
                        "path": report.relative_to(project).as_posix(),
                        "sha256": hashlib.sha256(report.read_bytes()).hexdigest(),
                    },
                },
                "source_snapshot": {},
            }
        )
        + "\n",
        encoding="utf-8",
        newline="\n",
    )

    with pytest.raises(ValueError, match="accepted evidence SHA-256 mismatch"):
        rebuild_retrieval_lock(
            knowledge_root=knowledge,
            project_root=project,
            accepted_attempt=attempt,
            output=project / "maintenance" / "lock.json",
        )


@pytest.mark.windows
def test_rebuild_rejects_accepted_attempt_with_reparse_ancestor(
    tmp_path: Path,
) -> None:
    project, knowledge, _ = make_audit_fixture(tmp_path)
    link = knowledge / "evaluation" / "accepted-link"
    target = project / "maintenance" / "accepted-real"
    make_directory_reparse_point(link, target)
    real_attempt = target / "v001"
    real_attempt.mkdir()
    (real_attempt / "result.json").write_text(
        '{"measurement": 1}\n', encoding="utf-8", newline="\n"
    )
    (real_attempt / "report.md").write_text(
        "# Evaluation report\n", encoding="utf-8", newline="\n"
    )
    output = project / "maintenance" / "rejected-lock.json"

    with pytest.raises(ValueError, match="reparse point"):
        rebuild_retrieval_lock(
            knowledge_root=knowledge,
            project_root=project,
            accepted_attempt=link / "v001",
            output=output,
        )

    assert not output.exists()
