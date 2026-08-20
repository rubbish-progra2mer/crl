from __future__ import annotations

import shutil
from pathlib import Path

import pytest

from crl_v3.review import render_review_input, review_material_errors
from crl_v3.workspace import ResearchWorkspace
from conftest import (
    make_directory_reparse_point,
    make_file_symlink,
    make_run,
    publish_synthetic_fixed_review,
    set_current_version,
)


def _workspace(tmp_path: Path) -> ResearchWorkspace:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_problem("# Problem\n\ntext")
    workspace.write_candidate("# Candidate\n\ntext")
    workspace.write_experiment_plan("# Plan\n\ntext")
    workspace.write_experiment_result("# Result\n\ntext")
    workspace.write_seed("# Seed\n\ntext")
    return workspace


def test_one_request_and_three_free_independent_reports(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    request = workspace.write_review_request(
        "请自由判断其科学价值，不运行工具。",
        [
            "seed_v001.md",
            "problem_v001.md",
            "candidate_v001.md",
            "experiment_v001/plan.md",
            "experiment_v001/result.md",
        ],
    )
    assert request.reading_paths[0] == "seed_v001.md"
    assert "packet" not in Path(request.path).name.lower()

    reports = [
        workspace.write_reviewer_report(number, f"task-{number}", f"意见 {number}")
        for number in (1, 2, 3)
    ]
    assert [report.reviewer_id for report in reports] == ["task-1", "task-2", "task-3"]
    assert "意见 2" in reports[1].content
    assert review_material_errors(workspace) == ()


def test_render_review_input_is_deterministic_and_contains_exact_materials(
    tmp_path: Path,
) -> None:
    workspace = _workspace(tmp_path)
    workspace.write_review_request(
        "请寻找最小反例。",
        ["seed_v001.md", "candidate_v001.md"],
    )
    before = {
        path.relative_to(workspace.workspace_path).as_posix(): path.read_bytes()
        for path in workspace.workspace_path.rglob("*")
        if path.is_file()
    }

    first = render_review_input(workspace)
    second = render_review_input(workspace)

    assert first == second
    assert "请寻找最小反例。".encode("utf-8") in first
    assert (workspace.workspace_path / "seed_v001.md").read_bytes() in first
    assert (workspace.workspace_path / "candidate_v001.md").read_bytes() in first
    assert first.index(b"PATH: seed_v001.md") < first.index(
        b"PATH: candidate_v001.md"
    )
    after = {
        path.relative_to(workspace.workspace_path).as_posix(): path.read_bytes()
        for path in workspace.workspace_path.rglob("*")
        if path.is_file()
    }
    assert after == before


def test_render_review_input_rejects_changed_material(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    workspace.write_review_request("review", ["seed_v001.md"])
    workspace.seed_path.write_bytes(workspace.seed_path.read_bytes() + b"changed\n")

    with pytest.raises(ValueError, match="reviewed materials changed"):
        render_review_input(workspace)


def test_render_review_input_rejects_missing_material(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    workspace.write_review_request("review", ["seed_v001.md"])
    workspace.seed_path.unlink()

    with pytest.raises(FileNotFoundError, match="does not exist"):
        render_review_input(workspace)


def test_render_review_input_rejects_tampered_escape_path(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    workspace.write_review_request("review", ["seed_v001.md"])
    request = workspace.review_path / "request.md"
    request.write_bytes(request.read_bytes().replace(b"seed_v001.md", b"../outside.md"))

    with pytest.raises(ValueError, match="safe relative path"):
        render_review_input(workspace)


def test_render_review_input_rejects_tampered_wrong_version(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    workspace.write_review_request("review", ["seed_v001.md"])
    (workspace.workspace_path / "seed_v002.md").write_bytes(
        workspace.seed_path.read_bytes()
    )
    request = workspace.review_path / "request.md"
    request.write_bytes(request.read_bytes().replace(b"seed_v001.md", b"seed_v002.md"))

    with pytest.raises(ValueError, match="not associated with v001"):
        render_review_input(workspace)


def test_reports_require_distinct_context_ids_and_three_slots(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    workspace.write_review_request("review", ["seed_v001.md"])
    workspace.write_reviewer_report(1, "same-task", "one")
    with pytest.raises(ValueError, match="already used"):
        workspace.write_reviewer_report(2, "same-task", "two")
    errors = review_material_errors(workspace)
    assert any("expected 3" in item for item in errors)


def test_request_accepts_only_existing_run_local_utf8_text(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    binary = workspace.workspace_path / "invalid_v001.md"
    binary.write_bytes(b"\xff\xfe")
    with pytest.raises(ValueError, match="UTF-8"):
        workspace.write_review_request("review", ["seed_v001.md", "invalid_v001.md"])
    with pytest.raises(ValueError, match="safe relative"):
        workspace.write_review_request("review", ["seed_v001.md", "../outside.md"])
    with pytest.raises(FileNotFoundError):
        workspace.write_review_request("review", ["seed_v001.md", "missing.md"])


def test_published_request_and_reports_are_not_silently_replaced(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    workspace.write_review_request("review", ["seed_v001.md"])
    with pytest.raises(FileExistsError):
        workspace.write_review_request("changed", ["seed_v001.md"])
    workspace.write_reviewer_report(1, "task-1", "first")
    with pytest.raises(FileExistsError):
        workspace.write_reviewer_report(1, "task-1", "changed")


def test_report_body_may_quote_internal_metadata_prefix(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    workspace.write_review_request("review", ["seed_v001.md"])
    body = "正文可以自由讨论 <!-- CRL_REVIEW_REPORT_META 这个内部标记。"
    report = workspace.write_reviewer_report(1, "task-1", body)
    assert body in report.content


def test_review_cannot_read_another_version_or_reuse_prior_reviewer(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    candidate_v002 = workspace.workspace_path / "candidate_v002.md"
    candidate_v002.write_text("new candidate\n", encoding="utf-8", newline="\n")
    with pytest.raises(ValueError, match="not associated with v001"):
        workspace.write_review_request("review", ["candidate_v002.md"])

    workspace.write_review_request("review", ["seed_v001.md"])
    workspace.write_reviewer_report(1, "fresh-task-a", "opinion")

    set_current_version(workspace.workspace_path, "v002")
    next_version = ResearchWorkspace(
        workspace.workspace_path, version="v002", product_root=workspace.product_root
    )
    next_version.write_seed("new seed")
    next_version.write_review_request("review", ["seed_v002.md", "candidate_v002.md"])
    with pytest.raises(ValueError, match="already used"):
        next_version.write_reviewer_report(1, "fresh-task-a", "new opinion")


@pytest.mark.windows
def test_review_junction_is_rejected_before_external_write(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_candidate("candidate")
    workspace.write_seed("seed")
    outside = tmp_path / "outside-review"
    make_directory_reparse_point(run / "review_v001", outside)
    with pytest.raises(ValueError, match="reparse point"):
        workspace.write_review_request("review", ["seed_v001.md", "candidate_v001.md"])
    assert list(outside.iterdir()) == []


def test_review_hash_chain_detects_seed_and_report_byte_changes(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    workspace.write_review_request("review", ["seed_v001.md"])
    seed = workspace.seed_path
    original_seed = seed.read_bytes()
    seed.write_bytes(original_seed + b"changed\n")
    with pytest.raises(ValueError, match="reviewed materials changed"):
        workspace.write_reviewer_report(1, "task-a", "opinion")

    seed.write_bytes(original_seed)
    for number in (1, 2, 3):
        workspace.write_reviewer_report(number, f"task-{number}", "opinion")
    request = publish_synthetic_fixed_review(workspace)
    decision = workspace.write_review_decision("deliver")
    report = Path(str(request["path"])) / "EMP" / "report.json"
    report.write_bytes(report.read_bytes() + b"changed\n")
    with pytest.raises(ValueError, match="bound to different reviewer reports"):
        from crl_v3.reviewer_decision import read_fixed_review_decision

        read_fixed_review_decision(workspace)
    assert Path(decision.path).is_file()


def test_review_request_symlink_is_rejected_on_read(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    workspace.write_review_request("review", ["seed_v001.md"])
    request = workspace.review_path / "request.md"
    outside = tmp_path / "outside-request.md"
    outside.write_bytes(request.read_bytes())
    request.unlink()
    make_file_symlink(request, outside)
    with pytest.raises(ValueError, match="reparse point"):
        from crl_v3.review import read_review_request

        read_review_request(workspace)


@pytest.mark.windows
def test_review_directory_junction_is_rejected_on_read(tmp_path: Path) -> None:
    workspace = _workspace(tmp_path)
    workspace.write_review_request("review", ["seed_v001.md"])
    review = workspace.review_path
    outside = tmp_path / "outside-review-read"
    outside.mkdir()
    shutil.copy2(review / "request.md", outside / "request.md")
    (review / "request.md").unlink()
    review.rmdir()
    make_directory_reparse_point(review, outside)
    with pytest.raises(ValueError, match="reparse point"):
        from crl_v3.review import read_review_request

        read_review_request(workspace)
