from __future__ import annotations

import hashlib
from pathlib import Path

import pymupdf
import pytest

import crl_v3.pdf as pdf_module
from crl_v3.knowledge import KnowledgeStore, Paper, Passage
from crl_v3.pdf import (
    _canonical_document_pages,
    _canonical_page_text,
    _repeated_edge_noise,
    _split_page,
    ingest_pdf,
    pdf_qa_statistics,
)


_PAPERS = Path(__file__).parents[2] / "knowledge_base" / "papers"
_MAD_PDF = _PAPERS / "P015_should_we_be_going_mad.pdf"
_REACT_PDF = _PAPERS / "P001_react.pdf"
_MAD_SHA256 = "8d0330933f495a3804842e8c8b0f778d8529fefeaf8d2a2dbf89d94f97bd0e70"


def _sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def _make_pdf(path: Path) -> None:
    document = pymupdf.open()
    page = document.new_page()
    page.insert_text((72, 72), "1 Introduction", fontsize=16)
    page.insert_text((72, 100), "Deterministic oranges appear on the first page.", fontsize=11)
    document.new_page()
    page = document.new_page()
    page.insert_text((72, 72), "2 Methods", fontsize=16)
    page.insert_text((72, 100), "Reliable bananas appear in the method section.", fontsize=11)
    page.insert_text((72, 140), "2.1 Data", fontsize=14)
    page.insert_text((72, 168), "Coordinates remain exactly reproducible.", fontsize=11)
    document.save(path)
    document.close()


def _make_repeated_edge_pdf(path: Path) -> None:
    document = pymupdf.open()
    for page_number in range(1, 5):
        page = document.new_page()
        page.insert_text((72, 30), "Repeated Running Header", fontsize=10)
        page.insert_text((72, 120), "User Message:", fontsize=11)
        page.insert_text(
            (72, 145), f"Unique body content on page {page_number}.", fontsize=11
        )
        page.insert_text((72, 820), "Repeated Running Footer", fontsize=10)
    document.save(path)
    document.close()


def _page_text(path: Path, page_number: int) -> str:
    with pymupdf.open(path) as document:
        return document[page_number - 1].get_text("text", sort=True).replace("\r\n", "\n").replace("\r", "\n")


def test_ingest_real_multipage_pdf_with_sections_and_reproducible_coordinates(tmp_path) -> None:
    pdf_path = tmp_path / "input.pdf"
    database = tmp_path / "knowledge.sqlite"
    _make_pdf(pdf_path)
    original_bytes = pdf_path.read_bytes()

    store = KnowledgeStore(database, read_only=False)
    paper, passages = ingest_pdf(
        store,
        pdf_path,
        expected_sha256=_sha256_bytes(original_bytes),
        paper_id="paper-pdf",
        title="PDF Study",
        year=2025,
        source="local",
        venue="Test Venue",
        publication_status="preprint",
    )

    assert paper == Paper(
        paper_id="paper-pdf",
        title="PDF Study",
        year=2025,
        source="local",
        venue="Test Venue",
        publication_status="preprint",
        fulltext_path=str(pdf_path.resolve()),
        fulltext_sha256=_sha256_bytes(original_bytes),
    )
    assert [passage.page_start for passage in passages] == [1, 3, 3]
    assert [passage.page_end for passage in passages] == [1, 3, 3]
    assert [passage.section for passage in passages] == [
        "1 Introduction",
        "2 Methods",
        "2.1 Data",
    ]
    assert [passage.passage_id for passage in passages] == [
        "paper-pdf:p0001:s0001",
        "paper-pdf:p0003:s0001",
        "paper-pdf:p0003:s0002",
    ]
    for passage in passages:
        page_text = _page_text(pdf_path, passage.page_start)
        assert page_text[passage.char_start : passage.char_end] == passage.text
        assert passage.text_sha256 == hashlib.sha256(passage.text.encode("utf-8")).hexdigest()

    assert [hit.passage_id for hit in store.search("oranges")] == ["paper-pdf:p0001:s0001"]
    assert [hit.passage_id for hit in store.search("bananas")] == ["paper-pdf:p0003:s0001"]
    assert pdf_path.read_bytes() == original_bytes
    store.close()


def test_ingest_stream_hashes_before_and_after_direct_path_parsing(
    tmp_path, monkeypatch
) -> None:
    pdf_path = tmp_path / "single-snapshot.pdf"
    _make_pdf(pdf_path)
    expected_sha256 = _sha256_bytes(pdf_path.read_bytes())
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    hash_calls: list[Path] = []
    open_calls: list[tuple[tuple[object, ...], dict[str, object]]] = []
    original_file_sha256 = pdf_module._file_sha256
    original_open = pdf_module.pymupdf.open

    def recording_file_sha256(path: Path) -> str:
        hash_calls.append(path)
        return original_file_sha256(path)

    def recording_open(*args, **kwargs):
        open_calls.append((args, kwargs))
        return original_open(*args, **kwargs)

    monkeypatch.setattr(pdf_module, "_file_sha256", recording_file_sha256)
    monkeypatch.setattr(pdf_module.pymupdf, "open", recording_open)

    paper, passages = ingest_pdf(
        store,
        pdf_path,
        expected_sha256=expected_sha256,
        paper_id="single-snapshot",
        title="Single Snapshot",
        year=2026,
        source="local",
        venue="Test Venue",
        publication_status="preprint",
    )

    assert hash_calls == [pdf_path.resolve(), pdf_path.resolve()]
    assert len(open_calls) == 1
    args, kwargs = open_calls[0]
    assert args == (pdf_path.resolve(),)
    assert kwargs == {}
    assert paper.fulltext_sha256 == expected_sha256
    assert passages
    store.close()


def test_wrong_expected_sha256_preserves_existing_database_state(tmp_path) -> None:
    pdf_path = tmp_path / "replacement.pdf"
    _make_pdf(pdf_path)
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    existing = Paper(
        paper_id="paper-pdf",
        title="Existing",
        year=2024,
        source="local",
        venue="Existing Venue",
        publication_status="published",
        fulltext_path="existing.pdf",
        fulltext_sha256="a" * 64,
    )
    existing_passage = Passage(
        passage_id="existing-passage",
        paper_id="paper-pdf",
        section="Existing",
        page_start=1,
        page_end=1,
        char_start=0,
        char_end=16,
        text="surviving_keyword",
        text_sha256=hashlib.sha256(b"surviving_keyword").hexdigest(),
    )
    store.add_paper(existing, [existing_passage])

    with pytest.raises(ValueError, match="SHA-256"):
        ingest_pdf(
            store,
            pdf_path,
            expected_sha256="0" * 64,
            paper_id="paper-pdf",
            title="Replacement",
            year=2026,
            source="local",
            venue="Test Venue",
            publication_status="preprint",
        )

    assert store.get_paper("paper-pdf") == existing
    assert store.get_passage("existing-passage") == existing_passage
    assert [hit.passage_id for hit in store.search("surviving_keyword")] == [
        "existing-passage"
    ]
    store.close()


def test_pdf_change_during_parse_is_rejected_before_database_write(
    tmp_path, monkeypatch
) -> None:
    pdf_path = tmp_path / "changing.pdf"
    _make_pdf(pdf_path)
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    original = pdf_module._canonical_document_pages

    def mutate_after_parse(document):
        pages = original(document)
        with pdf_path.open("ab") as handle:
            handle.write(b"changed")
        return pages

    monkeypatch.setattr(pdf_module, "_canonical_document_pages", mutate_after_parse)
    with pytest.raises(ValueError, match="changed while"):
        ingest_pdf(
            store,
            pdf_path,
            paper_id="changing",
            title="Changing",
            year=2026,
            source="local",
            venue="Test",
            publication_status="preprint",
        )
    assert store.get_paper("changing") is None
    store.close()


def test_repeated_pdf_ingest_is_deterministic_and_does_not_duplicate(tmp_path) -> None:
    pdf_path = tmp_path / "input.pdf"
    _make_pdf(pdf_path)
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    metadata = dict(
        paper_id="paper-pdf",
        title="PDF Study",
        year=2025,
        source="local",
        venue="Test Venue",
        publication_status="preprint",
    )

    first_paper, first_passages = ingest_pdf(store, pdf_path, **metadata)
    second_paper, second_passages = ingest_pdf(store, pdf_path, **metadata)

    assert second_paper == first_paper
    assert second_passages == first_passages
    assert len(store.search("oranges")) == 1
    assert len(store.search("bananas")) == 1
    store.close()


@pytest.mark.real_pdf
def test_real_two_column_page_reads_left_column_before_right_column() -> None:
    original = _MAD_PDF.read_bytes()
    with pymupdf.open(_MAD_PDF) as document:
        page = document[1]
        interleaved = page.get_text("text", sort=True)
        ordered = _canonical_page_text(page)
        cleaned = _canonical_document_pages(document)[1]

    assert interleaved.index("nullify the effects of agent order") < interleaved.index(
        "Current state-of-the-art models"
    )
    assert (
        ordered.index("Current state-of-the-art models")
        < ordered.index("ChatEval (Chan et al., 2023)")
        < ordered.index("nullify the effects of agent order")
        < ordered.index("Self-consistency (Wang et al., 2023b)")
    )
    assert "Should we be going MAD? A Look at Multi-Agent Debate" not in cleaned
    assert (
        cleaned.index("Current state-of-the-art models")
        < cleaned.index("ChatEval (Chan et al., 2023)")
        < cleaned.index("nullify the effects of agent order")
        < cleaned.index("Self-consistency (Wang et al., 2023b)")
    )
    assert sorted("".join(ordered.split())) == sorted("".join(interleaved.split()))
    assert hashlib.sha256(original).hexdigest() == _MAD_SHA256
    assert _MAD_PDF.read_bytes() == original


@pytest.mark.real_pdf
def test_real_single_column_page_keeps_existing_text_order() -> None:
    with pymupdf.open(_REACT_PDF) as document:
        page = document[5]
        existing = page.get_text("text", sort=True).replace("\r\n", "\n").replace(
            "\r", "\n"
        )
        assert _canonical_page_text(page) == existing
        cleaned = _canonical_document_pages(document)[5]
    assert cleaned == existing.replace(
        "Published as a conference paper at ICLR 2023\n", "", 1
    )


def test_repeated_edge_noise_requires_edge_position_and_preserves_body(tmp_path) -> None:
    pdf_path = tmp_path / "repeated-edges.pdf"
    _make_repeated_edge_pdf(pdf_path)
    original = pdf_path.read_bytes()

    with pymupdf.open(pdf_path) as document:
        assert len(_repeated_edge_noise(document)) == 2
        page_texts = _canonical_document_pages(document)

    assert all("Repeated Running Header" not in text for text in page_texts)
    assert all("Repeated Running Footer" not in text for text in page_texts)
    assert sum(text.count("User Message:") for text in page_texts) == 4
    assert all(
        f"Unique body content on page {page_number}." in page_texts[page_number - 1]
        for page_number in range(1, 5)
    )

    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    _, passages = ingest_pdf(
        store,
        pdf_path,
        paper_id="edge-noise",
        title="Edge Noise",
        year=2025,
        source="local",
        venue="",
        publication_status="test",
    )
    for passage in passages:
        page_text = page_texts[passage.page_start - 1]
        assert page_text[passage.char_start : passage.char_end] == passage.text
    assert pdf_path.read_bytes() == original
    store.close()


@pytest.mark.real_pdf
def test_real_repeated_headers_are_removed_but_camel_messages_remain() -> None:
    cases = [
        (
            _REACT_PDF,
            "Published as a conference paper at ICLR 2023",
            33,
            0,
        ),
        (
            _MAD_PDF,
            "Should we be going MAD? A Look at Multi-Agent Debate Strategies for LLMs",
            23,
            1,
        ),
    ]
    normalize = lambda text: " ".join(text.split())
    for path, repeated_text, before_count, after_count in cases:
        with pymupdf.open(path) as document:
            before = tuple(_canonical_page_text(page) for page in document)
            after = _canonical_document_pages(document)
        assert sum(repeated_text in normalize(text) for text in before) == before_count
        assert sum(repeated_text in normalize(text) for text in after) == after_count

@pytest.mark.real_pdf
def test_real_two_column_ingest_is_deterministic_and_coordinates_recover_text(
    tmp_path,
) -> None:
    original = _MAD_PDF.read_bytes()
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    metadata = dict(
        paper_id="mad-real",
        title="Should We Be Going MAD?",
        year=2023,
        source="arxiv",
        venue="arXiv",
        publication_status="preprint",
    )

    first_paper, first_passages = ingest_pdf(store, _MAD_PDF, **metadata)
    second_paper, second_passages = ingest_pdf(store, _MAD_PDF, **metadata)

    assert second_paper == first_paper
    assert second_passages == first_passages
    assert first_paper.fulltext_sha256 == _MAD_SHA256
    page_two = [passage for passage in first_passages if passage.page_start == 2]
    assert page_two
    with pymupdf.open(_MAD_PDF) as document:
        page_text = _canonical_document_pages(document)[1]
    for passage in page_two:
        assert page_text[passage.char_start : passage.char_end] == passage.text
        assert passage.text_sha256 == hashlib.sha256(
            passage.text.encode("utf-8")
        ).hexdigest()
    assert _MAD_PDF.read_bytes() == original
    store.close()


@pytest.mark.real_pdf
def test_real_section_titles_survive_without_numeric_and_list_false_headings() -> None:
    cases = [
        (_MAD_PDF, 1, "Front Matter", {"Abstract", "1. Introduction"}),
        (_MAD_PDF, 5, "Results", set()),
        (_REACT_PDF, 5, "3.2  METHODS", {"3.3  RESULTS AND OBSERVATIONS"}),
    ]

    for path, page_number, current_section, expected_new_sections in cases:
        with pymupdf.open(path) as document:
            chunks, _ = _split_page(
                _canonical_page_text(document[page_number - 1]), current_section
            )
        sections = {section for section, _, _ in chunks}
        assert expected_new_sections <= sections

    with pymupdf.open(_MAD_PDF) as document:
        mad_sections = {
            section
            for section, _, _ in _split_page(
                _canonical_page_text(document[4]), "Results"
            )[0]
        }
    assert not any(section.startswith("0.") for section in mad_sections)

    with pymupdf.open(_REACT_PDF) as document:
        react_front_sections = {
            section
            for section, _, _ in _split_page(
                _canonical_page_text(document[0]), "Front Matter"
            )[0]
        }
        react_results_sections = {
            section
            for section, _, _ in _split_page(
                _canonical_page_text(document[4]), "3.2  METHODS"
            )[0]
        }
    assert not any(section.startswith("2023 ") for section in react_front_sections)
    assert "50.0               ReAct" not in react_results_sections
    assert "26                                                      CoT" not in react_results_sections

def test_pdf_parse_failure_preserves_existing_paper_and_fts(tmp_path) -> None:
    database = tmp_path / "knowledge.sqlite"
    store = KnowledgeStore(database, read_only=False)
    existing = Paper(
        paper_id="paper-pdf",
        title="Existing",
        year=2024,
        source="local",
        venue="Existing Venue",
        publication_status="published",
        fulltext_path="existing.pdf",
        fulltext_sha256="a" * 64,
    )
    existing_passage = Passage(
        passage_id="existing-passage",
        paper_id="paper-pdf",
        section="Existing",
        page_start=1,
        page_end=1,
        char_start=0,
        char_end=16,
        text="surviving_keyword",
        text_sha256=hashlib.sha256(b"surviving_keyword").hexdigest(),
    )
    store.add_paper(existing, [existing_passage])
    broken_pdf = tmp_path / "broken.pdf"
    broken_pdf.write_bytes(b"not a pdf")

    with pytest.raises(Exception):
        ingest_pdf(
            store,
            broken_pdf,
            paper_id="paper-pdf",
            title="Broken Replacement",
            year=2025,
            source="local",
            venue="Test Venue",
            publication_status="preprint",
        )

    assert store.get_paper("paper-pdf") == existing
    assert store.get_passage("existing-passage") == existing_passage
    assert [hit.passage_id for hit in store.search("surviving_keyword")] == ["existing-passage"]
    store.close()


def test_all_blank_pdf_is_rejected_without_database_rows(tmp_path) -> None:
    blank_pdf = tmp_path / "blank.pdf"
    document = pymupdf.open()
    document.new_page()
    document.new_page()
    document.save(blank_pdf)
    document.close()
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)

    with pytest.raises(ValueError, match="no extractable text"):
        ingest_pdf(
            store,
            blank_pdf,
            paper_id="blank-paper",
            title="Blank",
            year=None,
            source="local",
            venue="",
            publication_status="unknown",
        )

    assert store.get_paper("blank-paper") is None
    store.close()


def test_pdf_qa_statistics_reports_structured_page_anomalies_without_changing_text() -> None:
    pages = ("", "brief", "x" * 101, "ordinary extracted page")

    result = pdf_qa_statistics(
        pages,
        very_short_non_whitespace_chars=5,
        extreme_page_chars=100,
    )

    assert result.page_count == 4
    assert result.extractable_page_count == 3
    assert result.blank_page_count == 1
    assert result.minimum_page_char_count == 0
    assert result.maximum_page_char_count == 101
    assert [warning.code for warning in result.warnings] == [
        "PDF_PAGE_BLANK",
        "PDF_PAGE_VERY_SHORT",
        "PDF_PAGE_EXTREME_LONG",
    ]
    assert result.warnings[-1].page_number == 3
    assert pages == ("", "brief", "x" * 101, "ordinary extracted page")


def test_pdf_qa_statistics_rejects_invalid_thresholds() -> None:
    with pytest.raises(ValueError, match="exceed"):
        pdf_qa_statistics(["page"], very_short_non_whitespace_chars=10, extreme_page_chars=10)
