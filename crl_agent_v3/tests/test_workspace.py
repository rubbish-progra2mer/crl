from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from crl_v3.knowledge import Evidence
from crl_v3.workspace import ResearchWorkspace, safe_relative_path
from tools.inspect_run import inspect_run
from conftest import (
    make_directory_reparse_point,
    make_file_symlink,
    make_run,
    set_current_version,
)


class FakeStore:
    def __init__(self, evidence: Evidence) -> None:
        self.evidence = evidence

    def get_evidence(self, evidence_id: str) -> Evidence | None:
        return self.evidence if evidence_id == self.evidence.evidence_id else None


def _evidence() -> Evidence:
    source = "作者报告该机制在低资源条件下失效。"
    return Evidence(
        evidence_id="E-001",
        paper_id="P-001",
        fulltext_sha256="a" * 64,
        evidence_kind="author_fact",
        section="4.2",
        page_start=5,
        page_end=5,
        locator="page 5",
        source_content=source,
        source_content_sha256=hashlib.sha256(source.encode("utf-8")).hexdigest(),
        codex_note="与候选失败机制直接相关。",
        passage_id=None,
        passage_text_sha256=None,
        quote_start=None,
        quote_end=None,
        fulltext_is_current=True,
        passage_is_current=None,
    )


def test_versioned_documents_land_in_run_as_utf8_lf(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    set_current_version(run, "v007")
    workspace = ResearchWorkspace(
        run, FakeStore(_evidence()), version="v007", product_root=product
    )

    problem = workspace.write_problem("# 问题\n\n研究中文编码。")
    mapping = workspace.write_research_map("# 文献地图", ["E-001"])
    candidate = workspace.write_candidate("# 候选方法", ["E-001"])
    packet = workspace.write_evidence_packet(["E-001"], preface="关键证据。")
    workspace.write_nearest_prior("# 最近工作\n\n尚有差异。")
    workspace.write_selection_context("# 选择背景\n\n保留备选。")
    workspace.write_memory("# 运行内记忆\n\n只在本轮使用。")
    workspace.write_failure_attribution("# 失败归因\n\n不适用。")

    assert Path(problem.path).name == "problem_v007.md"
    assert mapping.evidence[0].evidence_id == "E-001"
    assert candidate.evidence[0].fulltext_is_current is True
    assert "作者报告" in packet.content
    for path in run.glob("*_v007.md"):
        data = path.read_bytes()
        assert not data.startswith(b"\xef\xbb\xbf")
        assert b"\r\n" not in data
        data.decode("utf-8")


def test_current_version_is_editable_until_review_request(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_problem("first")
    workspace.write_problem("second")
    assert workspace.read_problem().content == "second\n"

    workspace.write_seed("seed")
    workspace.write_review_request(
        "请独立审阅。", ["seed_v001.md", "problem_v001.md"]
    )
    with pytest.raises(FileExistsError, match="locked"):
        workspace.write_problem("third")

    with pytest.raises(ValueError, match=r"advance.*version|advance the Run version"):
        ResearchWorkspace(run, version="v002", product_root=product).write_problem(
            "major revision"
        )

    set_current_version(run, "v002")
    next_version = ResearchWorkspace(run, version="v002", product_root=product)
    next_version.write_problem("major revision")
    assert next_version.read_problem().content == "major revision\n"


def test_selection_context_is_revisable_until_review_locks_it(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_selection_context("## 当前最佳候选集合\n\nh-001\n")
    workspace.write_selection_context("## 当前最佳候选集合\n\nh-001 与 h-002\n")
    workspace.write_seed("seed")
    workspace.write_review_request(
        "锁定当前材料。", ["seed_v001.md", "selection_context_v001.md"]
    )

    with pytest.raises(FileExistsError, match="locked"):
        workspace.write_selection_context("不得覆盖")


@pytest.mark.windows
def test_selection_context_review_lock_is_case_insensitive_on_windows(
    tmp_path: Path,
) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product)
    workspace.write_selection_context("## 当前最佳候选集合\n\nh-001\n")
    workspace.write_seed("seed")
    workspace.write_review_request(
        "锁定当前材料。", ["seed_v001.md", "SELECTION_CONTEXT_V001.MD"]
    )

    with pytest.raises(FileExistsError, match="locked"):
        workspace.write_selection_context("不得用大小写差异覆盖")


def test_workspace_requires_explicit_valid_run_and_safe_paths(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        ResearchWorkspace(tmp_path / "missing", product_root=tmp_path)
    product, run = make_run(tmp_path)
    with pytest.raises(ValueError, match="version"):
        ResearchWorkspace(run, version="current", product_root=product)
    with pytest.raises(ValueError):
        safe_relative_path("../escape.txt")
    with pytest.raises(ValueError):
        safe_relative_path(Path("C:/escape.txt"))


def test_unknown_evidence_is_rejected_without_creating_document(tmp_path: Path) -> None:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, FakeStore(_evidence()), product_root=product)
    with pytest.raises(KeyError, match="unknown evidence"):
        workspace.write_candidate("candidate", ["missing"])
    assert not (run / "candidate_v001.md").exists()


def test_workspace_rejects_arbitrary_directories_and_invalid_control_encoding(
    tmp_path: Path,
) -> None:
    product = tmp_path / "product"
    product.mkdir()
    arbitrary = product / "notes"
    arbitrary.mkdir()
    with pytest.raises(ValueError, match="valid direct child"):
        ResearchWorkspace(arbitrary, product_root=product)

    _, run = make_run(tmp_path / "valid")
    (run / "RUN_STATUS.md").write_bytes(b"\xef\xbb\xbf# status\nSTATUS: ACTIVE\n")
    with pytest.raises(ValueError, match="without BOM"):
        ResearchWorkspace(run, product_root=run.parent)


def test_control_and_narrative_file_symlinks_are_rejected(tmp_path: Path) -> None:
    product, run = make_run(tmp_path / "control")
    status = run / "RUN_STATUS.md"
    outside_status = tmp_path / "outside-status.md"
    outside_status.write_bytes(status.read_bytes())
    status.unlink()
    make_file_symlink(status, outside_status)
    with pytest.raises(ValueError, match="reparse point"):
        ResearchWorkspace(run, product_root=product)

    product2, run2 = make_run(tmp_path / "narrative")
    workspace = ResearchWorkspace(run2, product_root=product2)
    problem = run2 / "problem_v001.md"
    outside_problem = tmp_path / "outside-problem.md"
    outside_problem.write_text("outside\n", encoding="utf-8", newline="\n")
    make_file_symlink(problem, outside_problem)
    with pytest.raises(ValueError, match="reparse point"):
        workspace.read_problem()


def test_v2_contract_is_readable_but_research_writes_are_rejected(tmp_path: Path) -> None:
    product, run = make_run(tmp_path, contract_version="2")
    (run / "problem_v001.md").write_text("historical\n", encoding="utf-8", newline="\n")
    before = {path.name: path.read_bytes() for path in run.iterdir()}
    workspace = ResearchWorkspace(run, product_root=product)
    assert workspace.historical_read_only is True
    assert workspace.read_problem().content == "historical\n"
    with pytest.raises(ValueError, match="read-only"):
        workspace.write_problem("new research")
    report = inspect_run(run, product_root=product)
    assert report["legacy_read_only"] is True
    assert {path.name: path.read_bytes() for path in run.iterdir()} == before


def test_unknown_contract_is_rejected_by_workspace_reader(tmp_path: Path) -> None:
    product, run = make_run(tmp_path, contract_version="99")
    with pytest.raises(ValueError, match="not supported"):
        ResearchWorkspace(run, product_root=product)


@pytest.mark.windows
def test_run_root_junction_to_another_directory_is_rejected(tmp_path: Path) -> None:
    product, _ = make_run(tmp_path / "real")
    target = product / "20260731_1201_run02"
    make_directory_reparse_point(target, tmp_path / "outside-run")
    with pytest.raises(ValueError, match="reparse point"):
        ResearchWorkspace(target, product_root=product)
