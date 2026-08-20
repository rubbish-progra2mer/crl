from __future__ import annotations

import hashlib
import inspect
import json
from io import BytesIO
from urllib.error import HTTPError
from urllib.parse import parse_qs, urlsplit

import pytest

import crl_v3.literature as literature


class _Response:
    def __init__(self, content: bytes) -> None:
        self._stream = BytesIO(content)

    def read(self, size: int = -1) -> bytes:
        return self._stream.read(size)

    def __enter__(self) -> _Response:
        return self

    def __exit__(self, *args: object) -> None:
        return None


class _InterruptedResponse(_Response):
    def __init__(self, first_chunk: bytes) -> None:
        super().__init__(first_chunk)
        self._reads = 0

    def read(self, size: int = -1) -> bytes:
        self._reads += 1
        if self._reads == 1:
            return super().read(size)
        raise OSError("controlled read interruption")


def _search_payload() -> bytes:
    return json.dumps(
        {
            "total": 3,
            "data": [
                {
                    "paperId": "S2-A",
                    "title": "Agent Search & Retrieval",
                    "authors": [{"authorId": "1", "name": "Ada One"}, {"name": "Bo Two"}],
                    "year": 2025,
                    "venue": "ACL",
                    "externalIds": {"DOI": "10.1000/agent.1", "ArXiv": "2501.00001"},
                    "abstract": "A complete abstract.",
                    "url": "https://www.semanticscholar.org/paper/S2-A",
                    "openAccessPdf": {"url": "https://example.test/a.pdf", "status": "GREEN"},
                },
                {
                    "paperId": "S2-B",
                    "title": "A Result with Missing Fields",
                    "authors": [],
                    "year": 2024,
                    "venue": "",
                    "externalIds": {"ArXiv": "2401.00002"},
                    "abstract": None,
                    "url": "https://www.semanticscholar.org/paper/S2-B",
                    "openAccessPdf": None,
                },
                {
                    "paperId": "S2-C",
                    "title": "The Third Result",
                    "authors": [{"name": "Cy Three"}],
                    "year": 2023,
                    "venue": "NeurIPS",
                    "externalIds": {},
                    "abstract": "Third abstract.",
                    "url": "https://www.semanticscholar.org/paper/S2-C",
                    "openAccessPdf": {"url": "https://example.test/c.pdf"},
                },
            ],
        }
    ).encode("utf-8")


def _arxiv_feed() -> bytes:
    return b"""<?xml version="1.0" encoding="UTF-8"?>
<feed xmlns="http://www.w3.org/2005/Atom"
      xmlns:arxiv="http://arxiv.org/schemas/atom">
  <entry>
    <id>https://arxiv.org/abs/2501.00001v2</id>
    <published>2025-01-02T03:04:05Z</published>
    <title>  Reliable LLM Agents:\n      Planning and Tool Use  </title>
    <summary>First line of the abstract.\n       Second   line with spacing.</summary>
    <author><name>Ada One</name></author>
    <author><name>Bo   Two</name></author>
    <arxiv:doi>10.1000/arxiv.agent.1</arxiv:doi>
    <arxiv:journal_ref>Proceedings of Agent Conf 2025</arxiv:journal_ref>
    <link href="https://arxiv.org/abs/2501.00001v2"
          rel="alternate" type="text/html" />
    <link href="https://arxiv.org/pdf/2501.00001v2"
          rel="related" type="application/pdf" title="pdf" />
  </entry>
  <entry>
    <id>https://arxiv.org/abs/2402.00002</id>
    <published>2024-02-03T04:05:06Z</published>
    <title>Agent Memory Without Optional Metadata</title>
    <summary>  A short abstract.  </summary>
    <author><name>Cy Three</name></author>
    <link href="https://arxiv.org/abs/2402.00002"
          rel="alternate" type="text/html" />
  </entry>
  <entry>
    <id>https://arxiv.org/abs/2303.00003</id>
    <published>2023-03-04T05:06:07Z</published>
    <title>Third Result Outside the Caller Limit</title>
  </entry>
</feed>
"""


def test_search_sends_exact_encoded_query_and_preserves_source_data(
    tmp_path, monkeypatch
) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(request, *, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        return _Response(_search_payload())

    def forbidden_download(*args, **kwargs):
        raise AssertionError("search must never call download_pdf")

    monkeypatch.setattr(literature, "urlopen", fake_urlopen)
    monkeypatch.setattr(literature, "download_pdf", forbidden_download)
    monkeypatch.chdir(tmp_path)

    candidates = literature.search_semantic_scholar(
        "LLM agents: planning & tools/行动?", 2, timeout=7.5
    )

    parsed = urlsplit(str(captured["url"]))
    parameters = parse_qs(parsed.query)
    assert parameters["query"] == ["LLM agents: planning & tools/行动?"]
    assert parameters["limit"] == ["2"]
    assert parameters["fields"] == [literature._SEARCH_FIELDS]
    assert "%26" in str(captured["url"])
    assert captured["timeout"] == 7.5
    assert len(candidates) == 2
    assert candidates[0] == literature.LiteratureCandidate(
        source="Semantic Scholar",
        source_id="S2-A",
        title="Agent Search & Retrieval",
        authors=("Ada One", "Bo Two"),
        year=2025,
        venue="ACL",
        doi="10.1000/agent.1",
        abstract="A complete abstract.",
        landing_page_url="https://www.semanticscholar.org/paper/S2-A",
        pdf_url="https://example.test/a.pdf",
        source_order=1,
    )
    assert candidates[1].source_id == "S2-B"
    assert candidates[1].authors == ()
    assert candidates[1].venue is None
    assert candidates[1].doi is None
    assert candidates[1].abstract is None
    assert candidates[1].pdf_url is None
    assert candidates[1].source_order == 2
    assert list(tmp_path.iterdir()) == []


def test_arxiv_search_sends_exact_query_and_normalizes_atom_feed(
    tmp_path, monkeypatch
) -> None:
    captured: dict[str, object] = {}

    def fake_urlopen(request, *, timeout):
        captured["url"] = request.full_url
        captured["timeout"] = timeout
        return _Response(_arxiv_feed())

    def forbidden_download(*args, **kwargs):
        raise AssertionError("search must never call download_pdf")

    monkeypatch.setattr(literature, "urlopen", fake_urlopen)
    monkeypatch.setattr(literature, "download_pdf", forbidden_download)
    monkeypatch.chdir(tmp_path)

    candidates = literature.search_arxiv(
        "LLM agents: planning & tools/行动?", 2, timeout=8.5
    )

    parsed = urlsplit(str(captured["url"]))
    parameters = parse_qs(parsed.query)
    assert parsed.netloc == "export.arxiv.org"
    assert parameters["search_query"] == ["all:LLM agents: planning & tools/行动?"]
    assert parameters["start"] == ["0"]
    assert parameters["max_results"] == ["2"]
    assert "%26" in str(captured["url"])
    assert captured["timeout"] == 8.5
    assert len(candidates) == 2
    assert candidates[0] == literature.LiteratureCandidate(
        source="arXiv",
        source_id="2501.00001v2",
        title="Reliable LLM Agents: Planning and Tool Use",
        authors=("Ada One", "Bo Two"),
        year=2025,
        venue="Proceedings of Agent Conf 2025",
        doi="10.1000/arxiv.agent.1",
        abstract="First line of the abstract. Second line with spacing.",
        landing_page_url="https://arxiv.org/abs/2501.00001v2",
        pdf_url="https://arxiv.org/pdf/2501.00001v2",
        source_order=1,
    )
    assert candidates[1].source == "arXiv"
    assert isinstance(candidates[1], literature.LiteratureCandidate)
    assert candidates[1].source_id == "2402.00002"
    assert candidates[1].year == 2024
    assert candidates[1].doi is None
    assert candidates[1].venue is None
    assert candidates[1].pdf_url is None
    assert candidates[1].source_order == 2
    assert list(tmp_path.iterdir()) == []


def test_semantic_scholar_failure_does_not_fall_back_to_arxiv(monkeypatch) -> None:
    requested_urls: list[str] = []

    def rate_limited(request, *, timeout):
        requested_urls.append(request.full_url)
        raise HTTPError(request.full_url, 429, "controlled rate limit", {}, None)

    monkeypatch.setattr(literature, "urlopen", rate_limited)

    with pytest.raises(HTTPError) as error:
        literature.search_semantic_scholar("LLM agents", 2)

    assert error.value.code == 429
    assert len(requested_urls) == 1
    assert urlsplit(requested_urls[0]).netloc == "api.semanticscholar.org"
    assert "search_arxiv" not in inspect.getsource(
        literature.search_semantic_scholar
    )
    assert "search_semantic_scholar" not in inspect.getsource(
        literature.search_arxiv
    )
    assert "download_pdf" not in inspect.getsource(literature.search_arxiv)


def test_download_writes_only_after_explicit_call_and_returns_hash(
    tmp_path, monkeypatch
) -> None:
    pdf_bytes = b"%PDF-1.7\n" + b"real pdf bytes" * 9000
    monkeypatch.setattr(
        literature, "urlopen", lambda request, *, timeout: _Response(pdf_bytes)
    )
    target = tmp_path / "caller-selected-name.pdf"

    assert not target.exists()
    result = literature.download_pdf(
        "https://example.test/selected.pdf", target, timeout=4.0
    )

    assert target.read_bytes() == pdf_bytes
    assert result.path == target.resolve()
    assert result.byte_count == len(pdf_bytes)
    assert result.sha256 == hashlib.sha256(pdf_bytes).hexdigest()
    assert list(tmp_path.iterdir()) == [target]


def test_download_refuses_to_overwrite_existing_target(tmp_path, monkeypatch) -> None:
    target = tmp_path / "existing.pdf"
    target.write_bytes(b"existing content")

    def forbidden_urlopen(*args, **kwargs):
        raise AssertionError("existing target must fail before HTTP")

    monkeypatch.setattr(literature, "urlopen", forbidden_urlopen)

    with pytest.raises(FileExistsError):
        literature.download_pdf("https://example.test/new.pdf", target)
    assert target.read_bytes() == b"existing content"


@pytest.mark.parametrize(
    "response",
    [
        _Response(b"<!doctype html>not a pdf"),
        _InterruptedResponse(b"%PDF-1.7\npartial"),
    ],
)
def test_invalid_or_interrupted_download_leaves_no_files(
    tmp_path, monkeypatch, response
) -> None:
    monkeypatch.setattr(literature, "urlopen", lambda request, *, timeout: response)
    target = tmp_path / "failed.pdf"

    with pytest.raises((ValueError, OSError)):
        literature.download_pdf("https://example.test/failure.pdf", target)

    assert not target.exists()
    assert list(tmp_path.iterdir()) == []


def test_http_failure_leaves_no_files(tmp_path, monkeypatch) -> None:
    def failed_urlopen(request, *, timeout):
        raise HTTPError(request.full_url, 503, "controlled HTTP failure", {}, None)

    monkeypatch.setattr(literature, "urlopen", failed_urlopen)
    target = tmp_path / "http-failure.pdf"

    with pytest.raises(HTTPError):
        literature.download_pdf("https://example.test/failure.pdf", target)

    assert not target.exists()
    assert list(tmp_path.iterdir()) == []


def test_literature_tool_has_no_research_pipeline_dependencies() -> None:
    source = inspect.getsource(literature)
    for forbidden in (
        "pymupdf",
        "KnowledgeStore",
        "semantic_search",
        "hybrid_search",
        "Campaign",
        "Round",
        "Gate",
        "Receipt",
        "provider",
        "plugin",
    ):
        assert forbidden not in source


def test_identifier_normalization_preserves_arxiv_version_and_doi_casefold() -> None:
    assert literature.normalize_doi("HTTPS://doi.org/10.1000/Agent.X") == "10.1000/agent.x"
    identity = literature.normalize_arxiv_id("https://arxiv.org/abs/2501.00001v12")
    assert identity == literature.ArxivIdentity("2501.00001v12", "2501.00001", 12)
    assert literature.normalize_semantic_scholar_id("CorpusID:0042") == "CorpusId:0042"


def test_retry_after_is_bounded_and_api_key_never_enters_response_record(monkeypatch) -> None:
    calls = []
    sleeps = []
    secret = "s2-secret-value"

    def fake_urlopen(request, *, timeout):
        calls.append(request)
        if len(calls) == 1:
            raise HTTPError(
                request.full_url,
                429,
                "rate limited",
                {"Retry-After": "0"},
                BytesIO(b"retry body"),
            )
        return _Response(_search_payload())

    monkeypatch.setattr(literature, "urlopen", fake_urlopen)
    responses = []
    records = literature.search_semantic_scholar_records(
        "agent planning",
        1,
        response_log=responses,
        max_retries=1,
        api_key=secret,
        sleep=sleeps.append,
    )

    assert len(records) == 1
    assert [item.http_status for item in responses] == [429, 200]
    assert sleeps == [0.0]
    assert all(secret not in repr(item) for item in responses)
    assert calls[0].headers["X-api-key"] == secret


def test_semantic_scholar_expansion_follows_finite_pagination(monkeypatch) -> None:
    offsets = []

    def fake_urlopen(request, *, timeout):
        parameters = parse_qs(urlsplit(request.full_url).query)
        offset = int(parameters["offset"][0])
        offsets.append(offset)
        paper = {
            "paperId": f"S2-{offset}",
            "title": f"Paper {offset}",
            "authors": [{"name": "Ada"}],
            "year": 2025,
            "externalIds": {},
        }
        payload = {"data": [{"citingPaper": paper}]}
        if offset == 0:
            payload["next"] = 1
        return _Response(json.dumps(payload).encode("utf-8"))

    monkeypatch.setattr(literature, "urlopen", fake_urlopen)
    responses = []
    found = literature.expand_semantic_scholar_records(
        "CorpusId:42",
        "citations",
        5,
        page_size=1,
        max_pages=2,
        response_log=responses,
        max_retries=0,
    )

    assert offsets == [0, 1]
    assert [item.candidate.source_id for item in found] == ["S2-0", "S2-1"]
    assert len(responses) == 2


def test_merge_is_identity_conservative_and_does_not_merge_near_titles() -> None:
    response = literature.NetworkResponseRecord(
        "fixture", "https://example.test/search", "2026-01-01T00:00:00Z", 200, "a" * 64
    )

    def sourced(source, source_id, title, doi, rank):
        candidate = literature.LiteratureCandidate(
            source, source_id, title, ("Ada One",), 2025, None, doi, None, None, None, rank
        )
        provenance = literature.SourceProvenance(
            source, source_id, "query", rank, response.normalized_url_identity,
            response.body_sha256, {"source_id": source_id}
        )
        return literature.SourcedCandidate(
            candidate, literature.normalize_doi(doi), None, None,
            source_id if source == "Semantic Scholar" else None, provenance
        )

    records = literature.merge_literature_records(
        (
            sourced("Semantic Scholar", "S2-A", "Agent Planning", "10.1/WORK", 1),
            sourced("arXiv", "2501.00001v2", "Agent Planning", "10.1/work", 2),
            sourced("arXiv", "2501.00002", "Agent Planning Methods", None, 3),
        )
    )

    assert len(records) == 2
    assert len(records[0].provenance) == 2
    assert records[1].title == "Agent Planning Methods"


def test_download_size_limit_removes_temporary_and_target(tmp_path, monkeypatch) -> None:
    pdf_bytes = b"%PDF-1.7\n" + b"x" * 100
    monkeypatch.setattr(
        literature, "urlopen", lambda request, *, timeout: _Response(pdf_bytes)
    )
    target = tmp_path / "too-large.pdf"

    with pytest.raises(ValueError, match="size limit"):
        literature.download_pdf(
            "https://example.test/large.pdf", target, max_bytes=20
        )

    assert list(tmp_path.iterdir()) == []
