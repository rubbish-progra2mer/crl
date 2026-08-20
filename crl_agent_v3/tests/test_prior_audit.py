from __future__ import annotations

import json
from io import BytesIO
from pathlib import Path
from urllib.error import URLError
from urllib.parse import urlsplit

import pytest

import crl_v3.literature as literature_module
import crl_v3.prior_audit as prior_audit_module
import tools.audit_prior as audit_prior_tool
from conftest import make_run, set_current_version
from crl_v3.diagnosis import _facts, _prior_collision_facts, _render_report
from crl_v3.hypotheses import (
    add_hypothesis,
    create_hypothesis_record,
    empty_portfolio,
)
from crl_v3.knowledge import KnowledgeStore, Paper
from crl_v3.prior_audit import (
    create_prior_audit,
    download_prior_candidate_pdf,
    load_prior_audit,
)
from crl_v3.research_context import render_research_context
from crl_v3.seed_support import audit_seed_support
from crl_v3.workspace import ResearchWorkspace


class _Response:
    def __init__(self, content: bytes, *, status: int = 200) -> None:
        self._stream = BytesIO(content)
        self.status = status
        self.headers = {}

    def read(self, size: int = -1) -> bytes:
        return self._stream.read(size)

    def __enter__(self):
        return self

    def __exit__(self, *args: object) -> None:
        return None


def _semantic_payload(*, title: str = "Shared Agent Work") -> bytes:
    return json.dumps(
        {
            "data": [
                {
                    "paperId": "S2-IDENTITY",
                    "title": title,
                    "authors": [{"name": "Ada One"}],
                    "year": 2025,
                    "venue": "ACL",
                    "externalIds": {
                        "DOI": "10.1000/SHARED.WORK",
                        "ArXiv": "2501.00001v1",
                    },
                    "abstract": "Semantic abstract.",
                    "url": "https://www.semanticscholar.org/paper/S2-IDENTITY",
                    "openAccessPdf": {"url": "https://example.test/shared.pdf"},
                }
            ]
        }
    ).encode("utf-8")


def _arxiv_feed() -> bytes:
    return b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>https://arxiv.org/abs/2501.00001v3</id>
    <published>2025-01-02T00:00:00Z</published>
    <title>Shared Agent Work</title>
    <summary>arXiv abstract.</summary>
    <author><name>Ada One</name></author>
    <arxiv:doi>10.1000/shared.work</arxiv:doi>
    <link href="https://arxiv.org/abs/2501.00001v3" rel="alternate" type="text/html" />
    <link href="https://arxiv.org/pdf/2501.00001v3" type="application/pdf" />
  </entry>
</feed>
"""


def _workspace(tmp_path: Path) -> tuple[Path, Path, ResearchWorkspace]:
    product, run = make_run(tmp_path)
    workspace = ResearchWorkspace(run, product_root=product, version="v001")
    document = workspace.write_hypotheses(
        empty_portfolio(run.name, "v001"), expected_sha256=None, create_only=True
    )
    record = create_hypothesis_record(
        {"hypothesis_id": "hypothesis-001", "title": "候选假设"}
    )
    portfolio = add_hypothesis(document.portfolio, record)
    workspace.write_hypotheses(portfolio, expected_sha256=document.sha256)
    return product, run, workspace


def _all_sources(request, *, timeout):
    host = urlsplit(request.full_url).netloc
    if host == "api.semanticscholar.org":
        return _Response(_semantic_payload())
    if host == "export.arxiv.org":
        return _Response(_arxiv_feed())
    raise AssertionError(f"unexpected URL: {request.full_url}")


def test_audit_merges_multisource_identity_and_writes_only_run_local_snapshot(
    tmp_path: Path, monkeypatch
) -> None:
    product, run, workspace = _workspace(tmp_path)
    portfolio = (run / "hypotheses_v001" / "portfolio.json").read_bytes()
    nearest = run / "nearest_prior_v001.md"
    nearest.write_bytes("人工最近先行。\n".encode("utf-8"))
    knowledge = product / "knowledge_base"
    knowledge.mkdir()
    sentinel = knowledge / "sentinel.bin"
    sentinel.write_bytes(b"production knowledge sentinel")
    monkeypatch.setattr(literature_module, "urlopen", _all_sources)

    publication = create_prior_audit(
        workspace,
        "hypothesis-001",
        ("agent planning",),
        "audit-001",
        max_retries=0,
        now="2026-08-10T00:00:00Z",
    )

    destination = run / "hypotheses_v001" / "priors" / "audit-001"
    assert Path(publication.path) == destination
    assert sorted(path.name for path in destination.iterdir()) == [
        "assessment.md",
        "candidates.json",
        "report.md",
        "request.json",
    ]
    candidates = json.loads((destination / "candidates.json").read_text(encoding="utf-8"))
    assert candidates["degraded"] is False
    assert len(candidates["candidates"]) == 1
    candidate = candidates["candidates"][0]
    assert len(candidate["provenance"]) == 2
    assert {item["source"] for item in candidate["provenance"]} == {
        "Semantic Scholar",
        "arXiv",
    }
    ids = {(item["kind"], item["value"]) for item in candidate["source_ids"]}
    assert ("doi", "10.1000/shared.work") in ids
    assert ("arxiv", "2501.00001v3") in ids
    assert ("arxiv_versionless", "2501.00001") in ids
    request = json.loads((destination / "request.json").read_text(encoding="utf-8"))
    assert len(request["network_responses"]) == 2
    assert all(item["body_sha256"] for item in request["network_responses"])
    assert request["schema_version"] == 3
    assert "collision_kind" not in request
    report = (destination / "report.md").read_text(encoding="utf-8")
    assert "machine-owned immutable snapshot" in report
    assert "请勿编辑" in report
    assert "由主研究者填写" not in report
    assert "Shared Agent Work" not in report
    assert "novelty" not in report.casefold()
    assessment = (destination / "assessment.md").read_text(encoding="utf-8")
    assert "可在阅读候选、PDF、Evidence 和实验后继续修订" in assessment
    assert "碰撞类型：`UNCLASSIFIED`" in assessment
    assert "仍存贡献增量" in assessment
    assert (run / "hypotheses_v001" / "portfolio.json").read_bytes() == portfolio
    assert nearest.read_bytes() == "人工最近先行。\n".encode("utf-8")
    assert sentinel.read_bytes() == b"production knowledge sentinel"
    assert not (run / "candidate_v001.md").exists()


def test_partial_source_failure_is_published_as_degraded(
    tmp_path: Path, monkeypatch
) -> None:
    _, run, workspace = _workspace(tmp_path)

    def partial(request, *, timeout):
        if urlsplit(request.full_url).netloc == "export.arxiv.org":
            raise URLError("controlled arXiv failure")
        return _Response(_semantic_payload())

    monkeypatch.setattr(literature_module, "urlopen", partial)
    publication = create_prior_audit(
        workspace,
        "hypothesis-001",
        ("agent planning",),
        "audit-degraded",
        max_retries=0,
    )

    assert publication.degraded is True
    snapshot = load_prior_audit(workspace, "audit-degraded")
    assert snapshot.candidates["degraded"] is True
    attempts = snapshot.candidates["source_attempts"]
    assert any(item["source"] == "arXiv" and item["status"] == "error" for item in attempts)
    assert len(snapshot.candidates["candidates"]) == 1
    assert not (run / "nearest_prior_v001.md").exists()


def test_malformed_remote_response_is_published_as_degraded(
    tmp_path: Path, monkeypatch
) -> None:
    _, _, workspace = _workspace(tmp_path)

    def malformed_semantic(request, *, timeout):
        if urlsplit(request.full_url).netloc == "api.semanticscholar.org":
            return _Response(b"{not-json")
        return _Response(_arxiv_feed())

    monkeypatch.setattr(literature_module, "urlopen", malformed_semantic)
    publication = create_prior_audit(
        workspace,
        "hypothesis-001",
        ("agent planning",),
        "audit-format-degraded",
        max_retries=0,
    )

    assert publication.degraded is True
    snapshot = load_prior_audit(workspace, "audit-format-degraded")
    assert any(
        item["source"] == "Semantic Scholar"
        and item["status"] == "error"
        and item["error_type"] == "LiteratureResponseError"
        for item in snapshot.candidates["source_attempts"]
    )
    assert len(snapshot.candidates["candidates"]) == 1


def test_unexpected_program_error_propagates_without_publishing(
    tmp_path: Path, monkeypatch
) -> None:
    _, run, workspace = _workspace(tmp_path)

    def programming_error(request, *, timeout):
        raise RuntimeError("controlled implementation defect")

    monkeypatch.setattr(literature_module, "urlopen", programming_error)

    with pytest.raises(RuntimeError, match="implementation defect"):
        create_prior_audit(
            workspace,
            "hypothesis-001",
            ("agent planning",),
            "audit-program-error",
            max_retries=0,
        )

    assert not (
        run / "hypotheses_v001" / "priors" / "audit-program-error"
    ).exists()
    assert not (run / "hypotheses_v001" / "priors").exists()


def test_environment_api_key_is_used_but_redacted_from_every_artifact(
    tmp_path: Path, monkeypatch
) -> None:
    _, run, workspace = _workspace(tmp_path)
    secret = "never-persist-this-s2-key"
    seen_headers = []

    def fake_urlopen(request, *, timeout):
        if urlsplit(request.full_url).netloc == "api.semanticscholar.org":
            seen_headers.append(request.headers)
            return _Response(_semantic_payload(title=f"Echo {secret}"))
        return _Response(_arxiv_feed())

    monkeypatch.setenv("S2_API_KEY", secret)
    monkeypatch.setattr(literature_module, "urlopen", fake_urlopen)
    create_prior_audit(
        workspace,
        "hypothesis-001",
        ("agent planning",),
        "audit-secret",
        max_retries=0,
    )

    assert seen_headers and seen_headers[0]["X-api-key"] == secret
    destination = run / "hypotheses_v001" / "priors" / "audit-secret"
    for path in destination.iterdir():
        assert secret.encode("utf-8") not in path.read_bytes()


@pytest.mark.parametrize("audit_id", ["UPPER", "../escape", "x", "has space"])
def test_invalid_audit_id_has_no_side_effect(
    tmp_path: Path, monkeypatch, audit_id: str
) -> None:
    _, run, workspace = _workspace(tmp_path)
    monkeypatch.setattr(
        literature_module,
        "urlopen",
        lambda *args, **kwargs: pytest.fail("invalid AUDIT_ID must fail before HTTP"),
    )

    with pytest.raises(ValueError, match="AUDIT_ID"):
        create_prior_audit(
            workspace, "hypothesis-001", ("query",), audit_id, max_retries=0
        )

    assert not (run / "hypotheses_v001" / "priors").exists()


def test_closed_and_wrong_version_runs_fail_before_network(
    tmp_path: Path, monkeypatch
) -> None:
    _, run, workspace = _workspace(tmp_path)
    monkeypatch.setattr(
        literature_module,
        "urlopen",
        lambda *args, **kwargs: pytest.fail("invalid Run state must fail before HTTP"),
    )
    status = (run / "RUN_STATUS.md").read_text(encoding="utf-8")
    (run / "RUN_STATUS.md").write_text(
        status.replace("STATUS: ACTIVE", "STATUS: DELIVERED"),
        encoding="utf-8",
        newline="\n",
    )
    with pytest.raises(FileExistsError, match="read-only"):
        create_prior_audit(
            workspace, "hypothesis-001", ("query",), "audit-closed", max_retries=0
        )

    (run / "RUN_STATUS.md").write_text(status, encoding="utf-8", newline="\n")
    set_current_version(run, "v002")
    with pytest.raises(ValueError, match="version"):
        create_prior_audit(
            workspace, "hypothesis-001", ("query",), "audit-version", max_retries=0
        )
    assert not (run / "hypotheses_v001" / "priors").exists()


def test_run_outside_product_is_rejected(tmp_path: Path) -> None:
    product, _, _ = _workspace(tmp_path)
    outside = tmp_path / "20260731_1200_run99"
    outside.mkdir()
    with pytest.raises(ValueError, match="direct child"):
        ResearchWorkspace(outside, product_root=product, version="v001")


def test_audit_id_is_never_overwritten(tmp_path: Path, monkeypatch) -> None:
    _, run, workspace = _workspace(tmp_path)
    monkeypatch.setattr(literature_module, "urlopen", _all_sources)
    create_prior_audit(
        workspace, "hypothesis-001", ("query",), "audit-once", max_retries=0
    )
    before = {
        path.name: path.read_bytes()
        for path in (run / "hypotheses_v001" / "priors" / "audit-once").iterdir()
    }
    with pytest.raises(FileExistsError, match="already exists"):
        create_prior_audit(
            workspace, "hypothesis-001", ("different",), "audit-once", max_retries=0
        )
    after = {
        path.name: path.read_bytes()
        for path in (run / "hypotheses_v001" / "priors" / "audit-once").iterdir()
    }
    assert after == before


def test_explicit_candidate_download_failure_cleans_all_files(
    tmp_path: Path, monkeypatch
) -> None:
    _, run, workspace = _workspace(tmp_path)
    monkeypatch.setattr(literature_module, "urlopen", _all_sources)
    create_prior_audit(
        workspace, "hypothesis-001", ("query",), "audit-download", max_retries=0
    )
    snapshot = load_prior_audit(workspace, "audit-download")
    candidate_id = snapshot.candidates["candidates"][0]["candidate_id"]
    monkeypatch.setattr(
        literature_module,
        "urlopen",
        lambda request, *, timeout: _Response(b"not a PDF"),
    )

    with pytest.raises(ValueError, match="PDF header"):
        download_prior_candidate_pdf(
            workspace, "audit-download", "hypothesis-001", candidate_id
        )

    destination = run / "hypotheses_v001" / "priors" / "audit-download"
    assert not (destination / "downloads").exists()
    assert sorted(path.name for path in destination.iterdir()) == [
        "assessment.md",
        "candidates.json",
        "report.md",
        "request.json",
    ]


def test_atomic_publish_failure_leaves_no_audit_directory(
    tmp_path: Path, monkeypatch
) -> None:
    _, run, workspace = _workspace(tmp_path)
    monkeypatch.setattr(literature_module, "urlopen", _all_sources)
    monkeypatch.setattr(
        prior_audit_module,
        "_rename_directory",
        lambda source, destination: (_ for _ in ()).throw(OSError("controlled rename")),
    )

    with pytest.raises(OSError, match="controlled rename"):
        create_prior_audit(
            workspace, "hypothesis-001", ("query",), "audit-atomic", max_retries=0
        )

    priors = run / "hypotheses_v001" / "priors"
    assert not (priors / "audit-atomic").exists()
    assert not list(priors.glob(".*.tmp"))


def test_cli_creates_audit_with_mocked_network(
    tmp_path: Path, monkeypatch, capsys
) -> None:
    product, run, _ = _workspace(tmp_path)
    monkeypatch.setattr(literature_module, "urlopen", _all_sources)

    exit_code = audit_prior_tool.main(
        [
            "--product-root",
            str(product),
            "--run-root",
            str(run),
            "--hypothesis-id",
            "hypothesis-001",
            "--query",
            "agent planning",
            "--audit-id",
            "audit-cli",
            "--max-retries",
            "0",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output["action"] == "create"
    assert output["audit_id"] == "audit-cli"
    assessment_path = Path(output["assessment_path"])
    assert assessment_path.name == "assessment.md"
    assert assessment_path.parent.name == "audit-cli"
    assert (run / "hypotheses_v001" / "priors" / "audit-cli").is_dir()


@pytest.mark.parametrize(
    "collision_kind",
    [
        "DIRECT_EXACT",
        "EMPIRICAL_ABSORPTION",
        "CONSTRUCTIVE_COMPOSITE",
        "ANALOGICAL_REDUCTION",
    ],
)
def test_prior_audit_records_collision_strength_without_changing_candidate_state(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, collision_kind: str
) -> None:
    _, run, workspace = _workspace(tmp_path)
    monkeypatch.setattr(literature_module, "urlopen", _all_sources)

    create_prior_audit(
        workspace,
        "hypothesis-001",
        ("agent planning",),
        "audit-" + collision_kind.casefold().replace("_", "-"),
        collision_kind=collision_kind,
        max_retries=0,
    )

    audit = next((run / "hypotheses_v001" / "priors").glob("audit-*"))
    request = json.loads((audit / "request.json").read_text(encoding="utf-8"))
    snapshot = load_prior_audit(workspace, audit.name)
    portfolio = json.loads(
        (run / "hypotheses_v001" / "portfolio.json").read_text(encoding="utf-8")
    )
    assert "collision_kind" not in request
    assert snapshot.collision_kind == collision_kind
    assert snapshot.assessment is not None
    assert f"碰撞类型：`{collision_kind}`" in snapshot.assessment
    assert portfolio["hypotheses"][0]["status"] == "draft"
    assert not (run / "NO_DELIVERY.md").exists()


def test_cli_injects_real_knowledge_store_for_hypothesis_evidence_ids(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys
) -> None:
    product, run = make_run(tmp_path)
    knowledge = product / "knowledge_base"
    knowledge.mkdir()
    database = knowledge / "knowledge.sqlite"
    store = KnowledgeStore(database, read_only=False)
    paper_hash = "a" * 64
    store.add_paper(
        Paper(
            paper_id="paper-001",
            title="Evidence paper",
            year=2026,
            source="test",
            venue="test",
            publication_status="published",
            fulltext_path="papers/evidence.pdf",
            fulltext_sha256=paper_hash,
        ),
        (),
    )
    store.add_evidence(
        evidence_id="E-CLI-001",
        paper_id="paper-001",
        fulltext_sha256=paper_hash,
        evidence_kind="author_fact",
        section="1",
        page_start=1,
        page_end=1,
        locator="page 1",
        source_content="Evidence source.",
        codex_note="Evidence note.",
    )
    workspace = ResearchWorkspace(
        run, knowledge_store=store, product_root=product, version="v001"
    )
    document = workspace.write_hypotheses(
        empty_portfolio(run.name, "v001"), expected_sha256=None, create_only=True
    )
    record = create_hypothesis_record(
        {
            "hypothesis_id": "hypothesis-evidence",
            "title": "证据假设",
            "target_failure": {
                "summary": "",
                "card_ids": [],
                "evidence_ids": ["E-CLI-001"],
            },
        }
    )
    portfolio = add_hypothesis(document.portfolio, record, knowledge_store=store)
    workspace.write_hypotheses(portfolio, expected_sha256=document.sha256)
    store.close()
    monkeypatch.setattr(literature_module, "urlopen", _all_sources)

    exit_code = audit_prior_tool.main(
        [
            "--product-root",
            str(product),
            "--run-root",
            str(run),
            "--hypothesis-id",
            "hypothesis-evidence",
            "--query",
            "agent planning",
            "--audit-id",
            "audit-evidence-cli",
            "--max-retries",
            "0",
        ]
    )

    output = json.loads(capsys.readouterr().out)
    assert exit_code == 0
    assert output["audit_id"] == "audit-evidence-cli"
    request = json.loads(
        (
            run
            / "hypotheses_v001"
            / "priors"
            / "audit-evidence-cli"
            / "request.json"
        ).read_text(encoding="utf-8")
    )
    assert request["hypothesis"]["hypothesis_id"] == "hypothesis-evidence"


def test_researcher_assessment_can_change_without_invalidating_machine_facts(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, run, workspace = _workspace(tmp_path)
    monkeypatch.setattr(literature_module, "urlopen", _all_sources)
    create_prior_audit(
        workspace,
        "hypothesis-001",
        ("agent planning",),
        "audit-editable",
        max_retries=0,
    )
    root = run / "hypotheses_v001" / "priors" / "audit-editable"
    frozen = {
        name: (root / name).read_bytes()
        for name in ("request.json", "candidates.json", "report.md")
    }
    assessment = (root / "assessment.md").read_text(encoding="utf-8")
    assessment = assessment.replace(
        "碰撞类型：`UNCLASSIFIED`",
        "碰撞类型：`PROBLEM_OCCUPIED_METHOD_OPEN`",
    ).replace(
        "<!-- 由主研究者填写；引用 candidate / PDF / Evidence 身份。 -->",
        "Candidate `prior-0123456789abcdef` 是当前最危险先行。",
    )
    (root / "assessment.md").write_text(
        assessment, encoding="utf-8", newline="\n"
    )

    snapshot = load_prior_audit(workspace, "audit-editable")

    assert snapshot.collision_kind == "PROBLEM_OCCUPIED_METHOD_OPEN"
    assert "最危险先行" in (snapshot.assessment or "")
    assert snapshot.assessment_warnings == ()
    assert {
        name: (root / name).read_bytes()
        for name in ("request.json", "candidates.json", "report.md")
    } == frozen

    (root / "assessment.md").write_text(
        "自由解释仍在修订中。\n", encoding="utf-8", newline="\n"
    )
    still_valid = load_prior_audit(workspace, "audit-editable")
    assert still_valid.request == snapshot.request
    assert still_valid.candidates == snapshot.candidates
    assert still_valid.collision_kind is None
    assert still_valid.assessment_warnings


def test_unclassified_and_revised_assessments_flow_to_direct_readers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, run, workspace = _workspace(tmp_path)
    monkeypatch.setattr(literature_module, "urlopen", _all_sources)
    create_prior_audit(
        workspace,
        "hypothesis-001",
        ("agent planning",),
        "audit-reader",
        max_retries=0,
    )

    initial = _prior_collision_facts(workspace)
    assert initial["prior_audit_count"] == 1
    assert initial["collision_kind_distribution"] == {}
    assert initial["unclassified_audit_count"] == 1
    assert initial["assessment_warning_audit_count"] == 0
    assert initial["assessment_warnings"] == []
    rendered = render_research_context(workspace).decode("utf-8")
    assert "prior-audit:audit-reader:machine-report" in rendered
    assert "prior-audit:audit-reader:assessment" in rendered
    assert "碰撞类型：`UNCLASSIFIED`" in rendered
    assert "PRIOR_ASSESSMENT_WARNING" not in rendered
    seed_support = audit_seed_support(
        workspace, as_of_utc="2026-08-10T00:00:00Z"
    )
    codes = {item["code"] for item in seed_support["findings"]}
    assert "prior_audit_material_present" in codes
    assert "prior_audit_unreadable" not in codes

    path = run / "hypotheses_v001" / "priors" / "audit-reader" / "assessment.md"
    text = path.read_text(encoding="utf-8").replace(
        "碰撞类型：`UNCLASSIFIED`",
        "碰撞类型：`METHOD_KILLED_PHENOMENON_SURVIVES`",
    )
    path.write_text(text, encoding="utf-8", newline="\n")

    revised = _prior_collision_facts(workspace)
    assert revised["collision_kind_distribution"] == {
        "METHOD_KILLED_PHENOMENON_SURVIVES": 1
    }
    assert revised["unclassified_audit_count"] == 0


@pytest.mark.parametrize(
    ("case", "expected_warning"),
    [
        ("missing-marker", "assessment collision marker is missing"),
        ("invalid-marker", "assessment collision kind is unknown"),
        ("duplicate-marker", "assessment collision marker is ambiguous"),
        ("wrong-identity", "assessment audit identity is missing or different"),
        ("unreadable", "assessment is unreadable"),
        ("missing-file", "assessment.md is missing"),
    ],
)
def test_assessment_warnings_are_visible_without_invalidating_machine_facts(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    case: str,
    expected_warning: str,
) -> None:
    _, run, workspace = _workspace(tmp_path)
    monkeypatch.setattr(literature_module, "urlopen", _all_sources)
    audit_id = "audit-" + case
    create_prior_audit(
        workspace,
        "hypothesis-001",
        ("agent planning",),
        audit_id,
        max_retries=0,
    )
    root = run / "hypotheses_v001" / "priors" / audit_id
    frozen = {
        name: (root / name).read_bytes()
        for name in ("request.json", "candidates.json", "report.md")
    }
    assessment_path = root / "assessment.md"
    if case == "missing-file":
        assessment_path.unlink()
    elif case == "unreadable":
        assessment_path.write_bytes(b"\xff\xfe")
    else:
        text = assessment_path.read_text(encoding="utf-8")
        if case == "missing-marker":
            text = text.replace(
                "- 碰撞类型：`UNCLASSIFIED`",
                "- 碰撞说明仍在自由修订。",
            )
        elif case == "invalid-marker":
            text = text.replace(
                "- 碰撞类型：`UNCLASSIFIED`",
                "- 碰撞类型：`NOT_A_COLLISION_KIND`",
            )
        elif case == "duplicate-marker":
            text += "- 碰撞类型：`DIRECT_EXACT`\n"
        else:
            text = text.replace(
                f"- 审计标识：`{audit_id}`",
                "- 审计标识：`audit-different`",
            )
        assessment_path.write_text(text, encoding="utf-8", newline="\n")

    snapshot = load_prior_audit(workspace, audit_id)

    assert snapshot.request["audit_id"] == audit_id
    assert snapshot.candidates["audit_id"] == audit_id
    assert snapshot.collision_kind is None
    assert any(expected_warning in item for item in snapshot.assessment_warnings)
    assert {
        name: (root / name).read_bytes()
        for name in ("request.json", "candidates.json", "report.md")
    } == frozen

    rendered = render_research_context(workspace).decode("utf-8")
    assert "PRIOR_ASSESSMENT_WARNING" in rendered
    assert expected_warning in rendered
    if case in {"unreadable", "missing-file"}:
        assert f"prior-audit:{audit_id}:assessment-warning" in rendered
    else:
        assert f"prior-audit:{audit_id}:assessment-with-warnings" in rendered

    collision_facts = _prior_collision_facts(workspace)
    assert collision_facts["unclassified_audit_count"] == 0
    assert collision_facts["assessment_warning_audit_count"] == 1
    assert collision_facts["assessment_warning_count"] >= 1
    assert collision_facts["assessment_warnings"][0]["audit_id"] == audit_id
    diagnosis_facts = _facts(workspace, "warning-check")
    diagnosis_report = _render_report(diagnosis_facts, "a" * 64).decode("utf-8")
    assert "## Prior assessment warnings" in diagnosis_report
    assert expected_warning in diagnosis_report


@pytest.mark.parametrize("file_name", ["request.json", "candidates.json", "report.md"])
def test_machine_owned_prior_facts_still_detect_tampering(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, file_name: str
) -> None:
    _, run, workspace = _workspace(tmp_path)
    monkeypatch.setattr(literature_module, "urlopen", _all_sources)
    create_prior_audit(
        workspace,
        "hypothesis-001",
        ("agent planning",),
        "audit-tamper",
        max_retries=0,
    )
    path = run / "hypotheses_v001" / "priors" / "audit-tamper" / file_name
    path.write_bytes(path.read_bytes() + b"\n")

    with pytest.raises(ValueError):
        load_prior_audit(workspace, "audit-tamper")


@pytest.mark.parametrize("schema", [1, 2])
def test_historical_prior_schema_remains_readable(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, schema: int
) -> None:
    _, run, workspace = _workspace(tmp_path)
    monkeypatch.setattr(literature_module, "urlopen", _all_sources)
    audit_id = f"audit-schema-{schema}"
    create_prior_audit(
        workspace,
        "hypothesis-001",
        ("agent planning",),
        audit_id,
        max_retries=0,
    )
    root = run / "hypotheses_v001" / "priors" / audit_id
    (root / "assessment.md").unlink()
    historical_collision = "DIRECT_EXACT" if schema == 2 else None
    report = (
        prior_audit_module._legacy_report_bytes(audit_id)
        if schema == 1
        else prior_audit_module._report_bytes(audit_id, historical_collision)
    )
    (root / "report.md").write_bytes(report)
    request = json.loads((root / "request.json").read_text(encoding="utf-8"))
    request["schema_version"] = schema
    if historical_collision is not None:
        request["collision_kind"] = historical_collision
    request["artifact_hashes"]["report_md_sha256"] = prior_audit_module._sha256(
        report
    )
    (root / "request.json").write_bytes(prior_audit_module._json_bytes(request))

    snapshot = load_prior_audit(workspace, audit_id)

    assert snapshot.request["schema_version"] == schema
    assert snapshot.assessment is None
    assert snapshot.collision_kind == historical_collision
    diagnosis = _prior_collision_facts(workspace)
    if historical_collision is None:
        assert diagnosis["unclassified_audit_count"] == 1
    else:
        assert diagnosis["collision_kind_distribution"] == {"DIRECT_EXACT": 1}
