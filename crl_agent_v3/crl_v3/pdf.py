from __future__ import annotations

import hashlib
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pymupdf

from .knowledge import KnowledgeStore, Paper, Passage


_NUMBERED_HEADING = re.compile(
    r"^(?P<number>[1-9]\d?(?:\.\d{1,2})*)(?P<trailing>\.?)\s+(?P<title>\S.*)$"
)
_TITLE_WORD = re.compile(r"[A-Za-z][A-Za-z0-9+()]*(?:-[A-Za-z0-9+()]+)*")
_LOWERCASE_TITLE_WORDS = {
    "a",
    "an",
    "and",
    "as",
    "at",
    "by",
    "for",
    "from",
    "in",
    "of",
    "on",
    "or",
    "the",
    "to",
    "with",
}
_COMMON_HEADINGS = {
    "abstract",
    "introduction",
    "background",
    "related work",
    "methods",
    "methodology",
    "experiments",
    "results",
    "discussion",
    "conclusion",
    "conclusions",
    "limitations",
    "references",
    "appendix",
}
_ACADEMIC_HEADING_ENDINGS = _COMMON_HEADINGS | {
    "analysis",
    "approach",
    "architecture",
    "benchmark",
    "benchmarks",
    "debate",
    "framework",
    "generation",
    "model",
    "models",
    "protocol",
    "protocols",
    "setup",
    "study",
    "studies",
    "system",
    "systems",
    "task",
    "tasks",
    "work",
}
_EDGE_LIMIT = 0.08
_MAX_EDGE_TEXT_LENGTH = 160

_EdgeBlockKey = tuple[str, str, int, int, int, int]


@dataclass(frozen=True, slots=True)
class PdfQaWarning:
    severity: str
    code: str
    page_number: int
    char_count: int
    non_whitespace_char_count: int
    message: str


@dataclass(frozen=True, slots=True)
class PdfQaStatistics:
    page_count: int
    extractable_page_count: int
    blank_page_count: int
    total_char_count: int
    minimum_page_char_count: int | None
    median_page_char_count: int | float | None
    maximum_page_char_count: int | None
    warnings: tuple[PdfQaWarning, ...]


def pdf_qa_statistics(
    page_texts: Iterable[str],
    *,
    very_short_non_whitespace_chars: int = 20,
    extreme_page_chars: int = 20_000,
) -> PdfQaStatistics:
    """Return reusable page-level extraction diagnostics without changing text.

    The thresholds are disclosed diagnostics for a future explicit corpus build;
    they neither alter :func:`ingest_pdf` nor certify extraction quality.
    """

    if very_short_non_whitespace_chars < 0:
        raise ValueError("very_short_non_whitespace_chars must be non-negative")
    if extreme_page_chars <= very_short_non_whitespace_chars:
        raise ValueError("extreme_page_chars must exceed the short-page threshold")
    pages = tuple(page_texts)
    if any(not isinstance(text, str) for text in pages):
        raise TypeError("page_texts must contain strings")
    warnings: list[PdfQaWarning] = []
    lengths = sorted(len(text) for text in pages)
    extractable = 0
    blank = 0
    for page_number, text in enumerate(pages, start=1):
        non_whitespace = sum(not character.isspace() for character in text)
        if non_whitespace == 0:
            blank += 1
            warnings.append(
                PdfQaWarning(
                    severity="WARNING",
                    code="PDF_PAGE_BLANK",
                    page_number=page_number,
                    char_count=len(text),
                    non_whitespace_char_count=0,
                    message="页面没有可提取的非空白文本。",
                )
            )
        else:
            extractable += 1
            if non_whitespace <= very_short_non_whitespace_chars:
                warnings.append(
                    PdfQaWarning(
                        severity="WARNING",
                        code="PDF_PAGE_VERY_SHORT",
                        page_number=page_number,
                        char_count=len(text),
                        non_whitespace_char_count=non_whitespace,
                        message="页面提取文本极短，需要未来维护构建时人工核对。",
                    )
                )
        if len(text) > extreme_page_chars:
            warnings.append(
                PdfQaWarning(
                    severity="WARNING",
                    code="PDF_PAGE_EXTREME_LONG",
                    page_number=page_number,
                    char_count=len(text),
                    non_whitespace_char_count=non_whitespace,
                    message="页面提取文本长度超过维护诊断阈值。",
                )
            )
    return PdfQaStatistics(
        page_count=len(pages),
        extractable_page_count=extractable,
        blank_page_count=blank,
        total_char_count=sum(lengths),
        minimum_page_char_count=lengths[0] if lengths else None,
        median_page_char_count=_median(lengths),
        maximum_page_char_count=lengths[-1] if lengths else None,
        warnings=tuple(warnings),
    )


def _median(values: list[int]) -> int | float | None:
    if not values:
        return None
    midpoint = len(values) // 2
    if len(values) % 2:
        return values[midpoint]
    value = (values[midpoint - 1] + values[midpoint]) / 2
    return int(value) if value.is_integer() else value


def ingest_pdf(
    store: KnowledgeStore,
    pdf_path: str | Path,
    *,
    expected_sha256: str | None = None,
    paper_id: str,
    title: str,
    year: int | None,
    source: str,
    venue: str,
    publication_status: str,
) -> tuple[Paper, tuple[Passage, ...]]:
    path, fulltext_sha256 = _verify_pdf_file(pdf_path, expected_sha256)
    passages: list[Passage] = []
    current_section = "Front Matter"
    with pymupdf.open(path) as document:
        if document.needs_pass:
            raise ValueError("Encrypted PDF requires a password")
        for page_number, page_text in enumerate(
            _canonical_document_pages(document), start=1
        ):
            if not page_text.strip():
                continue
            chunks, current_section = _split_page(page_text, current_section)
            for section_number, (section, start, end) in enumerate(chunks, start=1):
                text = page_text[start:end]
                passages.append(
                    Passage(
                        passage_id=(
                            f"{paper_id}:p{page_number:04d}:s{section_number:04d}"
                        ),
                        paper_id=paper_id,
                        section=section,
                        page_start=page_number,
                        page_end=page_number,
                        char_start=start,
                        char_end=end,
                        text=text,
                        text_sha256=hashlib.sha256(text.encode("utf-8")).hexdigest(),
                    )
                )

    if not passages:
        raise ValueError("PDF contains no extractable text")

    parsed_sha256 = _file_sha256(path)
    if parsed_sha256 != fulltext_sha256:
        raise ValueError(f"PDF changed while it was being parsed: {path}")
    if expected_sha256 is not None and parsed_sha256 != expected_sha256:
        raise ValueError(f"PDF SHA-256 mismatch after parsing: {path}")

    paper = Paper(
        paper_id=paper_id,
        title=title,
        year=year,
        source=source,
        venue=venue,
        publication_status=publication_status,
        fulltext_path=str(path),
        fulltext_sha256=fulltext_sha256,
    )
    store.add_paper(paper, passages)
    return paper, tuple(passages)


def _canonical_document_pages(document: pymupdf.Document) -> tuple[str, ...]:
    repeated_edge_noise = _repeated_edge_noise(document)
    return tuple(
        _canonical_page_text(page, repeated_edge_noise) for page in document
    )


def _repeated_edge_noise(document: pymupdf.Document) -> frozenset[_EdgeBlockKey]:
    pages_by_block: dict[_EdgeBlockKey, set[int]] = defaultdict(set)
    for page_number, page in enumerate(document, start=1):
        for block in page.get_text("blocks", sort=False):
            if block[6] != 0:
                continue
            key = _edge_block_key(page, block)
            if key is not None:
                pages_by_block[key].add(page_number)

    minimum_pages = max(3, (document.page_count + 1) // 2)
    return frozenset(
        key for key, pages in pages_by_block.items() if len(pages) >= minimum_pages
    )


def _edge_block_key(
    page: pymupdf.Page, block: tuple
) -> _EdgeBlockKey | None:
    text = " ".join(block[4].split())
    if not text or len(text) > _MAX_EDGE_TEXT_LENGTH:
        return None

    rect = page.rect
    if block[3] <= rect.y0 + rect.height * _EDGE_LIMIT:
        edge = "top"
    elif block[1] >= rect.y1 - rect.height * _EDGE_LIMIT:
        edge = "bottom"
    else:
        return None

    return (
        edge,
        text.casefold(),
        round((block[0] - rect.x0) / rect.width * 1000),
        round((block[1] - rect.y0) / rect.height * 1000),
        round((block[2] - rect.x0) / rect.width * 1000),
        round((block[3] - rect.y0) / rect.height * 1000),
    )


def _canonical_page_text(
    page: pymupdf.Page,
    repeated_edge_noise: frozenset[_EdgeBlockKey] = frozenset(),
) -> str:
    all_blocks = [
        block
        for block in page.get_text("blocks", sort=False)
        if block[6] == 0 and block[4].strip()
    ]
    removed_blocks = [
        block
        for block in all_blocks
        if _edge_block_key(page, block) in repeated_edge_noise
    ]
    blocks = [block for block in all_blocks if block not in removed_blocks]
    column_candidates = _two_column_candidates(page, blocks)
    if column_candidates is None:
        text = page.get_text("text", sort=True)
        if removed_blocks:
            text = _remove_edge_blocks_from_text(text, page, removed_blocks)
    else:
        top = min(block[1] for block in column_candidates)
        bottom = max(block[3] for block in column_candidates)
        middle = (page.rect.x0 + page.rect.x1) / 2
        before = [block for block in blocks if block[3] <= top]
        after = [block for block in blocks if block[1] >= bottom]
        body = [block for block in blocks if block not in before and block not in after]
        left = [block for block in body if block[0] < middle]
        right = [block for block in body if block[0] >= middle]
        ordered = (
            sorted(before, key=_block_position)
            + sorted(left, key=_block_position)
            + sorted(right, key=_block_position)
            + sorted(after, key=_block_position)
        )
        text = "".join(block[4] for block in ordered)
    return text.replace("\r\n", "\n").replace("\r", "\n")


def _remove_edge_blocks_from_text(
    text: str, page: pymupdf.Page, blocks: list[tuple]
) -> str:
    spans: list[tuple[int, int]] = []
    for block in blocks:
        key = _edge_block_key(page, block)
        if key is None:
            continue
        needle = block[4].replace("\r\n", "\n").replace("\r", "\n")
        index = text.find(needle) if key[0] == "top" else text.rfind(needle)
        if index < 0 and needle.endswith("\n"):
            needle = needle[:-1]
            index = text.find(needle) if key[0] == "top" else text.rfind(needle)
        if index < 0:
            continue
        if key[0] == "top" and index > max(200, len(text) // 10):
            continue
        if key[0] == "bottom" and index + len(needle) < len(text) * 9 // 10:
            continue
        start = text.rfind("\n", 0, index) + 1
        end = index + len(needle)
        if not needle.endswith("\n"):
            following_newline = text.find("\n", end)
            end = len(text) if following_newline < 0 else following_newline + 1
        spans.append((start, end))

    for start, end in sorted(spans, reverse=True):
        text = text[:start] + text[end:]
    return text


def _two_column_candidates(
    page: pymupdf.Page, blocks: list[tuple]
) -> list[tuple] | None:
    page_width = page.rect.width
    middle = (page.rect.x0 + page.rect.x1) / 2
    minimum_width = page_width * 0.34
    maximum_width = page_width * 0.48
    left: list[tuple] = []
    right: list[tuple] = []
    for block in blocks:
        width = block[2] - block[0]
        if not minimum_width <= width <= maximum_width:
            continue
        if block[2] < middle:
            left.append(block)
        elif block[0] >= middle:
            right.append(block)

    if (
        len(left) < 2
        or len(right) < 2
        or sum(len(block[4]) for block in left) < 200
        or sum(len(block[4]) for block in right) < 200
    ):
        return None

    left_range = (min(block[1] for block in left), max(block[3] for block in left))
    right_range = (min(block[1] for block in right), max(block[3] for block in right))
    overlap = max(
        0.0,
        min(left_range[1], right_range[1]) - max(left_range[0], right_range[0]),
    )
    shorter_span = min(
        left_range[1] - left_range[0], right_range[1] - right_range[0]
    )
    if shorter_span <= 0 or overlap < shorter_span * 0.35:
        return None
    return left + right


def _block_position(block: tuple) -> tuple[float, float, int]:
    return block[1], block[0], block[5]


def _split_page(
    page_text: str, current_section: str
) -> tuple[list[tuple[str, int, int]], str]:
    headings: list[tuple[int, str]] = []
    offset = 0
    for line in page_text.splitlines(keepends=True):
        value = line.strip()
        if _is_heading(value):
            headings.append((offset, value))
        offset += len(line)

    boundaries: list[tuple[int, str]] = []
    if not headings or headings[0][0] > 0:
        boundaries.append((0, current_section))
    boundaries.extend(headings)

    chunks: list[tuple[str, int, int]] = []
    for index, (start, section) in enumerate(boundaries):
        end = boundaries[index + 1][0] if index + 1 < len(boundaries) else len(page_text)
        start, end = _trim_whitespace(page_text, start, end)
        if start < end:
            chunks.append((section, start, end))
    if headings:
        current_section = headings[-1][1]
    return chunks, current_section


def _is_heading(value: str) -> bool:
    if not value or len(value) > 80:
        return False
    normalized = re.sub(r"\s+", " ", value).strip().casefold()
    if normalized in _COMMON_HEADINGS:
        return True

    match = _NUMBERED_HEADING.fullmatch(value)
    if match is None:
        return False
    number_parts = [int(part) for part in match["number"].split(".")]
    title = match["title"].strip()
    if (
        number_parts[0] > 20
        or any(part > 20 for part in number_parts[1:])
        or not title[0].isalpha()
        or re.search(r"\s{3,}", title)
        or " - " in title
        or "=" in title
        or title[-1] in ".,;:"
    ):
        return False

    words = _TITLE_WORD.findall(title)
    significant_words = [
        word for word in words if word.casefold() not in _LOWERCASE_TITLE_WORDS
    ]
    if not significant_words or any(
        not (word.isupper() or word[0].isupper()) for word in significant_words
    ):
        return False

    normalized_title = re.sub(r"\s+", " ", title).casefold()
    if len(number_parts) == 1 and len(words) == 1:
        return normalized_title in _COMMON_HEADINGS
    if len(number_parts) == 1 and match["trailing"] == ".":
        last_word = re.findall(r"[A-Za-z]+", title)[-1].casefold()
        return (
            normalized_title in _COMMON_HEADINGS
            or last_word in _ACADEMIC_HEADING_ENDINGS
        )
    return True


def _trim_whitespace(text: str, start: int, end: int) -> tuple[int, int]:
    while start < end and text[start].isspace():
        start += 1
    while end > start and text[end - 1].isspace():
        end -= 1
    return start, end


def _verify_pdf_file(
    pdf_path: str | Path, expected_sha256: str | None
) -> tuple[Path, str]:
    path = Path(pdf_path).resolve()
    if not path.is_file():
        raise FileNotFoundError(path)
    actual_sha256 = _file_sha256(path)
    if expected_sha256 is not None and actual_sha256 != expected_sha256:
        raise ValueError(f"PDF SHA-256 mismatch: {path}")
    return path, actual_sha256


def _file_sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()
