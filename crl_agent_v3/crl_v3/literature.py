from __future__ import annotations

import hashlib
import json
import os
import re
import time
import unicodedata
import xml.etree.ElementTree as ET
from dataclasses import dataclass
from datetime import UTC, datetime
from email.utils import parsedate_to_datetime
from pathlib import Path
from typing import Callable, Iterable, Mapping, Sequence
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, quote, urlencode, urlsplit, urlunsplit
from urllib.request import Request, urlopen
from uuid import uuid4


_SEARCH_URL = "https://api.semanticscholar.org/graph/v1/paper/search"
_S2_PAPER_URL = "https://api.semanticscholar.org/graph/v1/paper"
_ARXIV_SEARCH_URL = "https://export.arxiv.org/api/query"
_SEARCH_FIELDS = ",".join(
    (
        "paperId",
        "title",
        "authors",
        "year",
        "venue",
        "externalIds",
        "abstract",
        "url",
        "openAccessPdf",
    )
)
_USER_AGENT = "crl-agent-v3/3.0.0-dev0"
_CHUNK_SIZE = 64 * 1024
_DEFAULT_MAX_PDF_BYTES = 50 * 1024 * 1024
_ATOM = "http://www.w3.org/2005/Atom"
_ARXIV = "http://arxiv.org/schemas/atom"
_XML_NAMESPACES = {"atom": _ATOM, "arxiv": _ARXIV}


@dataclass(frozen=True, slots=True)
class LiteratureCandidate:
    source: str
    source_id: str
    title: str | None
    authors: tuple[str, ...]
    year: int | None
    venue: str | None
    doi: str | None
    abstract: str | None
    landing_page_url: str | None
    pdf_url: str | None
    source_order: int


@dataclass(frozen=True, slots=True)
class PdfDownload:
    path: Path
    sha256: str
    byte_count: int


@dataclass(frozen=True, slots=True)
class NetworkResponseRecord:
    source: str
    normalized_url_identity: str
    requested_at_utc: str
    http_status: int
    body_sha256: str


@dataclass(frozen=True, slots=True)
class SourceProvenance:
    source: str
    source_id: str
    query: str
    source_rank: int
    normalized_url_identity: str
    response_body_sha256: str
    raw_record: object


@dataclass(frozen=True, slots=True)
class SourcedCandidate:
    candidate: LiteratureCandidate
    doi: str | None
    arxiv_id: str | None
    arxiv_versionless_id: str | None
    semantic_scholar_id: str | None
    provenance: SourceProvenance


@dataclass(frozen=True, slots=True)
class LiteratureRecord:
    candidate_id: str
    title: str | None
    authors: tuple[str, ...]
    year: int | None
    venue: str | None
    abstract: str | None
    urls: tuple[str, ...]
    landing_page_urls: tuple[str, ...]
    pdf_urls: tuple[str, ...]
    source_ids: tuple[tuple[str, str], ...]
    provenance: tuple[SourceProvenance, ...]


@dataclass(frozen=True, slots=True)
class ArxivIdentity:
    versioned_id: str
    versionless_id: str
    version: int | None


class LiteratureResponseError(ValueError):
    """A remote literature response is malformed or cannot be decoded."""


def search_semantic_scholar(
    query: str, limit: int, *, timeout: float = 30.0
) -> tuple[LiteratureCandidate, ...]:
    if not query.strip():
        raise ValueError("Search query must not be empty")
    if limit <= 0:
        raise ValueError("Search limit must be positive")

    parameters = urlencode(
        {"query": query, "limit": str(limit), "fields": _SEARCH_FIELDS}
    )
    request = Request(
        f"{_SEARCH_URL}?{parameters}",
        headers={"Accept": "application/json", "User-Agent": _USER_AGENT},
    )
    with urlopen(request, timeout=timeout) as response:
        payload = json.loads(response.read().decode("utf-8"))

    records = payload.get("data") or []
    return tuple(
        _candidate(record, source_order)
        for source_order, record in enumerate(records[:limit], start=1)
    )


def search_arxiv(
    query: str, limit: int, *, timeout: float = 30.0
) -> tuple[LiteratureCandidate, ...]:
    if not query.strip():
        raise ValueError("Search query must not be empty")
    if limit <= 0:
        raise ValueError("Search limit must be positive")

    parameters = urlencode(
        {"search_query": f"all:{query}", "start": "0", "max_results": str(limit)}
    )
    request = Request(
        f"{_ARXIV_SEARCH_URL}?{parameters}",
        headers={"Accept": "application/atom+xml", "User-Agent": _USER_AGENT},
    )
    with urlopen(request, timeout=timeout) as response:
        root = ET.fromstring(response.read())

    entries = root.findall("atom:entry", _XML_NAMESPACES)
    return tuple(
        _arxiv_candidate(entry, source_order)
        for source_order, entry in enumerate(entries[:limit], start=1)
    )


def normalize_doi(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    lowered = normalized.casefold()
    for prefix in ("https://doi.org/", "http://doi.org/", "doi:"):
        if lowered.startswith(prefix):
            normalized = normalized[len(prefix) :].strip()
            break
    normalized = normalized.casefold()
    return normalized if normalized.startswith("10.") and "/" in normalized else None


def normalize_arxiv_id(value: str | None) -> ArxivIdentity | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    split = urlsplit(normalized)
    if split.scheme and split.netloc:
        normalized = split.path
    normalized = normalized.removeprefix("/abs/").removeprefix("/pdf/")
    normalized = normalized.removeprefix("arXiv:").removeprefix("arxiv:")
    if normalized.endswith(".pdf"):
        normalized = normalized[:-4]
    normalized = normalized.strip()
    match = re.fullmatch(r"(.+?)(?:v([1-9][0-9]*))?", normalized)
    if match is None or not match.group(1):
        return None
    versionless = match.group(1)
    if re.fullmatch(r"(?:[a-z-]+(?:\.[a-z-]+)?/)?[0-9]{7}|[0-9]{4}\.[0-9]{4,5}", versionless, re.IGNORECASE) is None:
        return None
    version = int(match.group(2)) if match.group(2) else None
    versioned = versionless + (f"v{version}" if version is not None else "")
    return ArxivIdentity(versioned, versionless, version)


def normalize_semantic_scholar_id(value: str | None) -> str | None:
    if value is None:
        return None
    normalized = value.strip()
    if not normalized:
        return None
    if normalized.casefold().startswith("corpusid:"):
        corpus_id = normalized.partition(":")[2].strip()
        return f"CorpusId:{corpus_id}" if corpus_id.isdigit() else None
    if normalized.casefold().startswith("s2:"):
        normalized = normalized.partition(":")[2].strip()
    if re.fullmatch(r"[0-9a-fA-F]{40}", normalized):
        return normalized.casefold()
    return normalized if re.fullmatch(r"[A-Za-z0-9._-]+", normalized) else None


def normalize_title(value: str | None) -> str | None:
    if value is None:
        return None
    text = unicodedata.normalize("NFKC", value).casefold()
    text = " ".join(re.sub(r"[^\w]+", " ", text, flags=re.UNICODE).split())
    return text or None


def normalize_url_identity(value: str) -> str:
    split = urlsplit(value)
    if split.scheme not in {"http", "https"} or not split.netloc:
        raise ValueError("network URL must use HTTP or HTTPS")
    safe_query = [
        (key, val)
        for key, val in parse_qsl(split.query, keep_blank_values=True)
        if key.casefold() not in {"api_key", "apikey", "key", "token", "access_token"}
    ]
    safe_query.sort()
    return urlunsplit(
        (
            split.scheme.casefold(),
            split.netloc.casefold(),
            split.path,
            urlencode(safe_query),
            "",
        )
    )


def search_semantic_scholar_records(
    query: str,
    limit: int,
    *,
    response_log: list[NetworkResponseRecord],
    timeout: float = 30.0,
    max_retries: int = 2,
    api_key: str | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> tuple[SourcedCandidate, ...]:
    _search_arguments(query, limit, timeout, max_retries)
    parameters = urlencode(
        {"query": query, "limit": str(limit), "fields": _SEARCH_FIELDS}
    )
    url = f"{_SEARCH_URL}?{parameters}"
    body, response = _request_bytes(
        url,
        source="Semantic Scholar",
        accept="application/json",
        timeout=timeout,
        max_retries=max_retries,
        api_key=api_key,
        response_log=response_log,
        sleep=sleep,
    )
    payload = _json_response(body, "Semantic Scholar search")
    records = payload.get("data") or []
    if not isinstance(records, list):
        raise LiteratureResponseError("Semantic Scholar response data must be an array")
    found = []
    for rank, record in enumerate(records[:limit], start=1):
        _validate_semantic_record(record, "Semantic Scholar search")
        assert isinstance(record, dict)
        found.append(_sourced_semantic_candidate(record, rank, query, response))
    return tuple(found)


def search_arxiv_records(
    query: str,
    limit: int,
    *,
    response_log: list[NetworkResponseRecord],
    timeout: float = 30.0,
    max_retries: int = 2,
    sleep: Callable[[float], None] = time.sleep,
) -> tuple[SourcedCandidate, ...]:
    _search_arguments(query, limit, timeout, max_retries)
    parameters = urlencode(
        {"search_query": f"all:{query}", "start": "0", "max_results": str(limit)}
    )
    url = f"{_ARXIV_SEARCH_URL}?{parameters}"
    body, response = _request_bytes(
        url,
        source="arXiv",
        accept="application/atom+xml",
        timeout=timeout,
        max_retries=max_retries,
        api_key=None,
        response_log=response_log,
        sleep=sleep,
    )
    try:
        root = ET.fromstring(body)
    except ET.ParseError as error:
        raise LiteratureResponseError("arXiv search response is malformed XML") from error
    entries = root.findall("atom:entry", _XML_NAMESPACES)
    return tuple(
        _sourced_arxiv_candidate(entry, rank, query, response)
        for rank, entry in enumerate(entries[:limit], start=1)
    )


def expand_semantic_scholar_records(
    seed_paper_id: str,
    relation: str,
    limit: int,
    *,
    response_log: list[NetworkResponseRecord],
    page_size: int = 100,
    max_pages: int = 3,
    timeout: float = 30.0,
    max_retries: int = 2,
    api_key: str | None = None,
    sleep: Callable[[float], None] = time.sleep,
) -> tuple[SourcedCandidate, ...]:
    if relation not in {"citations", "references"}:
        raise ValueError("Semantic Scholar relation must be citations or references")
    _search_arguments(seed_paper_id, limit, timeout, max_retries)
    if page_size <= 0 or max_pages <= 0:
        raise ValueError("page_size and max_pages must be positive")
    lookup_id = _semantic_lookup_id(seed_paper_id)
    collected: list[SourcedCandidate] = []
    offset = 0
    paper_key = "citingPaper" if relation == "citations" else "citedPaper"
    for _ in range(max_pages):
        remaining = limit - len(collected)
        if remaining <= 0:
            break
        count = min(page_size, remaining)
        parameters = urlencode(
            {"offset": str(offset), "limit": str(count), "fields": _SEARCH_FIELDS}
        )
        url = f"{_S2_PAPER_URL}/{quote(lookup_id, safe=':')}/{relation}?{parameters}"
        body, response = _request_bytes(
            url,
            source="Semantic Scholar",
            accept="application/json",
            timeout=timeout,
            max_retries=max_retries,
            api_key=api_key,
            response_log=response_log,
            sleep=sleep,
        )
        payload = _json_response(body, "Semantic Scholar expansion")
        rows = payload.get("data") or []
        if not isinstance(rows, list):
            raise LiteratureResponseError(
                "Semantic Scholar expansion data must be an array"
            )
        for row in rows:
            if not isinstance(row, dict):
                raise LiteratureResponseError(
                    "Semantic Scholar expansion contains a malformed relation record"
                )
            paper = row.get(paper_key)
            if paper is None:
                continue
            _validate_semantic_record(paper, "Semantic Scholar expansion")
            assert isinstance(paper, dict)
            collected.append(
                _sourced_semantic_candidate(
                    paper,
                    len(collected) + 1,
                    f"{relation}:{lookup_id}",
                    response,
                    raw_record=row,
                )
            )
            if len(collected) >= limit:
                break
        next_offset = payload.get("next")
        if not rows or not isinstance(next_offset, int):
            break
        offset = next_offset
    return tuple(collected)


def merge_literature_records(
    candidates: Sequence[SourcedCandidate],
) -> tuple[LiteratureRecord, ...]:
    groups: list[list[SourcedCandidate]] = []
    for sourced in candidates:
        matches = [index for index, group in enumerate(groups) if _matches_group(sourced, group)]
        if not matches:
            groups.append([sourced])
            continue
        first = matches[0]
        groups[first].append(sourced)
        for index in reversed(matches[1:]):
            groups[first].extend(groups.pop(index))
    return tuple(_merged_record(group) for group in groups)


def download_pdf(
    pdf_url: str,
    target_path: str | Path,
    *,
    timeout: float = 60.0,
    max_bytes: int = _DEFAULT_MAX_PDF_BYTES,
) -> PdfDownload:
    if urlsplit(pdf_url).scheme not in {"http", "https"}:
        raise ValueError("PDF URL must use HTTP or HTTPS")
    if timeout <= 0:
        raise ValueError("PDF timeout must be positive")
    if max_bytes <= 0:
        raise ValueError("PDF size limit must be positive")

    target = Path(target_path).resolve()
    if target.exists():
        raise FileExistsError(target)
    if not target.parent.is_dir():
        raise FileNotFoundError(target.parent)

    temporary = target.parent / f".{target.name}.{uuid4().hex}.tmp"
    digest = hashlib.sha256()
    byte_count = 0
    request = Request(
        pdf_url,
        headers={"Accept": "application/pdf", "User-Agent": _USER_AGENT},
    )
    try:
        with urlopen(request, timeout=timeout) as response:
            content_length = _header_value(response, "Content-Length")
            if content_length is not None:
                try:
                    declared_length = int(content_length)
                except ValueError as error:
                    raise ValueError("Downloaded PDF has an invalid Content-Length") from error
                if declared_length > max_bytes:
                    raise ValueError("Downloaded PDF exceeds the size limit")
            first_chunk = response.read(_CHUNK_SIZE)
            if not first_chunk.startswith(b"%PDF-"):
                raise ValueError("Downloaded content does not have a PDF header")
            with temporary.open("xb") as stream:
                chunk = first_chunk
                while chunk:
                    stream.write(chunk)
                    digest.update(chunk)
                    byte_count += len(chunk)
                    if byte_count > max_bytes:
                        raise ValueError("Downloaded PDF exceeds the size limit")
                    chunk = response.read(_CHUNK_SIZE)
                stream.flush()
                os.fsync(stream.fileno())
        if target.exists():
            raise FileExistsError(target)
        os.replace(temporary, target)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise

    return PdfDownload(path=target, sha256=digest.hexdigest(), byte_count=byte_count)


def _search_arguments(query: str, limit: int, timeout: float, max_retries: int) -> None:
    if not isinstance(query, str) or not query.strip():
        raise ValueError("Search query must not be empty")
    if limit <= 0:
        raise ValueError("Search limit must be positive")
    if timeout <= 0:
        raise ValueError("Search timeout must be positive")
    if max_retries < 0 or max_retries > 10:
        raise ValueError("max_retries must be between 0 and 10")


def _json_response(body: bytes, label: str) -> dict[str, object]:
    try:
        payload = json.loads(body.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise LiteratureResponseError(f"{label} is not valid UTF-8 JSON") from error
    if not isinstance(payload, dict):
        raise LiteratureResponseError(f"{label} must be a JSON object")
    return payload


def _validate_semantic_record(value: object, label: str) -> None:
    if not isinstance(value, dict):
        raise LiteratureResponseError(f"{label} contains a non-object paper record")
    for field in ("externalIds", "openAccessPdf"):
        item = value.get(field)
        if item is not None and not isinstance(item, dict):
            raise LiteratureResponseError(
                f"{label} paper field {field} must be an object or null"
            )
    authors = value.get("authors")
    if authors is not None and (
        not isinstance(authors, list)
        or any(not isinstance(author, dict) for author in authors)
    ):
        raise LiteratureResponseError(
            f"{label} paper field authors must be an array of objects or null"
        )


def _request_bytes(
    url: str,
    *,
    source: str,
    accept: str,
    timeout: float,
    max_retries: int,
    api_key: str | None,
    response_log: list[NetworkResponseRecord],
    sleep: Callable[[float], None],
) -> tuple[bytes, NetworkResponseRecord]:
    normalized_url = normalize_url_identity(url)
    resolved_key = api_key if api_key is not None else (
        os.environ.get("S2_API_KEY") if source == "Semantic Scholar" else None
    )
    headers = {"Accept": accept, "User-Agent": _USER_AGENT}
    if resolved_key:
        headers["x-api-key"] = resolved_key
    for attempt in range(max_retries + 1):
        requested_at = _utc_now()
        request = Request(url, headers=headers)
        try:
            with urlopen(request, timeout=timeout) as response:
                body = response.read()
                record = NetworkResponseRecord(
                    source=source,
                    normalized_url_identity=normalized_url,
                    requested_at_utc=requested_at,
                    http_status=_response_status(response),
                    body_sha256=hashlib.sha256(body).hexdigest(),
                )
                response_log.append(record)
                return body, record
        except HTTPError as error:
            body = error.read() if error.fp is not None else b""
            response_log.append(
                NetworkResponseRecord(
                    source=source,
                    normalized_url_identity=normalized_url,
                    requested_at_utc=requested_at,
                    http_status=error.code,
                    body_sha256=hashlib.sha256(body).hexdigest(),
                )
            )
            if attempt >= max_retries or error.code not in {429, 500, 502, 503, 504}:
                raise
            sleep(_retry_delay(error.headers, attempt))
        except (TimeoutError, URLError, ConnectionError):
            if attempt >= max_retries:
                raise
            sleep(float(min(2**attempt, 8)))
    raise RuntimeError("unreachable network retry state")


def _retry_delay(headers: object, attempt: int) -> float:
    value = headers.get("Retry-After") if hasattr(headers, "get") else None
    if isinstance(value, str):
        try:
            return float(max(0, min(int(value), 60)))
        except ValueError:
            try:
                target = parsedate_to_datetime(value)
                if target.tzinfo is None:
                    target = target.replace(tzinfo=UTC)
                return float(max(0, min(int((target - datetime.now(UTC)).total_seconds()), 60)))
            except (TypeError, ValueError, OverflowError):
                pass
    return float(min(2**attempt, 8))


def _response_status(response: object) -> int:
    status = getattr(response, "status", None)
    if isinstance(status, int):
        return status
    getcode = getattr(response, "getcode", None)
    if callable(getcode):
        code = getcode()
        if isinstance(code, int):
            return code
    return 200


def _header_value(response: object, name: str) -> str | None:
    headers = getattr(response, "headers", None)
    if hasattr(headers, "get"):
        value = headers.get(name)
        return value if isinstance(value, str) else None
    getheader = getattr(response, "getheader", None)
    if callable(getheader):
        value = getheader(name)
        return value if isinstance(value, str) else None
    return None


def _sourced_semantic_candidate(
    record: Mapping[str, object],
    source_order: int,
    query: str,
    response: NetworkResponseRecord,
    *,
    raw_record: object | None = None,
) -> SourcedCandidate:
    raw = dict(record)
    candidate = _candidate(raw, source_order)
    external_ids = raw.get("externalIds")
    external = external_ids if isinstance(external_ids, dict) else {}
    doi = normalize_doi(_optional_text(external.get("DOI")))
    arxiv = normalize_arxiv_id(_optional_text(external.get("ArXiv")))
    semantic_id = normalize_semantic_scholar_id(candidate.source_id)
    return SourcedCandidate(
        candidate=candidate,
        doi=doi,
        arxiv_id=arxiv.versioned_id if arxiv is not None else None,
        arxiv_versionless_id=arxiv.versionless_id if arxiv is not None else None,
        semantic_scholar_id=semantic_id,
        provenance=SourceProvenance(
            source="Semantic Scholar",
            source_id=candidate.source_id,
            query=query,
            source_rank=source_order,
            normalized_url_identity=response.normalized_url_identity,
            response_body_sha256=response.body_sha256,
            raw_record=dict(raw_record) if isinstance(raw_record, Mapping) else raw,
        ),
    )


def _sourced_arxiv_candidate(
    entry: ET.Element,
    source_order: int,
    query: str,
    response: NetworkResponseRecord,
) -> SourcedCandidate:
    candidate = _arxiv_candidate(entry, source_order)
    arxiv = normalize_arxiv_id(candidate.source_id)
    return SourcedCandidate(
        candidate=candidate,
        doi=normalize_doi(candidate.doi),
        arxiv_id=arxiv.versioned_id if arxiv is not None else None,
        arxiv_versionless_id=arxiv.versionless_id if arxiv is not None else None,
        semantic_scholar_id=None,
        provenance=SourceProvenance(
            source="arXiv",
            source_id=candidate.source_id,
            query=query,
            source_rank=source_order,
            normalized_url_identity=response.normalized_url_identity,
            response_body_sha256=response.body_sha256,
            raw_record={"entry_xml": ET.tostring(entry, encoding="unicode")},
        ),
    )


def _semantic_lookup_id(value: str) -> str:
    doi = normalize_doi(value)
    if doi is not None:
        return f"DOI:{doi}"
    arxiv = normalize_arxiv_id(value)
    if arxiv is not None:
        return f"ARXIV:{arxiv.versionless_id}"
    semantic_id = normalize_semantic_scholar_id(value)
    if semantic_id is None:
        raise ValueError("seed paper ID is not a DOI, arXiv ID, or Semantic Scholar ID")
    return semantic_id


def _matches_group(candidate: SourcedCandidate, group: Sequence[SourcedCandidate]) -> bool:
    return any(_same_work(candidate, current) for current in group)


def _same_work(left: SourcedCandidate, right: SourcedCandidate) -> bool:
    for left_id, right_id in (
        (left.doi, right.doi),
        (left.arxiv_versionless_id, right.arxiv_versionless_id),
        (left.semantic_scholar_id, right.semantic_scholar_id),
    ):
        if left_id is not None and left_id == right_id:
            return True
    left_title = normalize_title(left.candidate.title)
    right_title = normalize_title(right.candidate.title)
    if left_title is None or left_title != right_title:
        return False
    if left.candidate.year is None or left.candidate.year != right.candidate.year:
        return False
    if not left.candidate.authors or not right.candidate.authors:
        return False
    return _normalized_author(left.candidate.authors[0]) == _normalized_author(
        right.candidate.authors[0]
    )


def _normalized_author(value: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", value).casefold().split())


def _merged_record(group: Sequence[SourcedCandidate]) -> LiteratureRecord:
    titles = [item.candidate.title for item in group if item.candidate.title]
    authors = [item.candidate.authors for item in group if item.candidate.authors]
    years = [item.candidate.year for item in group if item.candidate.year is not None]
    venues = [item.candidate.venue for item in group if item.candidate.venue]
    abstracts = [item.candidate.abstract for item in group if item.candidate.abstract]
    landing_page_urls = sorted(
        {item.candidate.landing_page_url for item in group if item.candidate.landing_page_url}
    )
    pdf_urls = sorted({item.candidate.pdf_url for item in group if item.candidate.pdf_url})
    urls = sorted(set(landing_page_urls) | set(pdf_urls))
    identifiers = sorted(
        {
            (kind, value)
            for item in group
            for kind, value in (
                ("doi", item.doi),
                ("arxiv", item.arxiv_id),
                ("arxiv_versionless", item.arxiv_versionless_id),
                ("semantic_scholar", item.semantic_scholar_id),
            )
            if value
        }
    )
    identity = _record_identity(group, identifiers)
    return LiteratureRecord(
        candidate_id="prior-" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:16],
        title=max(titles, key=len) if titles else None,
        authors=max(authors, key=len) if authors else (),
        year=years[0] if years else None,
        venue=max(venues, key=len) if venues else None,
        abstract=max(abstracts, key=len) if abstracts else None,
        urls=tuple(urls),
        landing_page_urls=tuple(landing_page_urls),
        pdf_urls=tuple(pdf_urls),
        source_ids=tuple(identifiers),
        provenance=tuple(item.provenance for item in group),
    )


def _record_identity(
    group: Sequence[SourcedCandidate], identifiers: Sequence[tuple[str, str]]
) -> str:
    priority = {"doi": 0, "arxiv_versionless": 1, "semantic_scholar": 2, "arxiv": 3}
    if identifiers:
        kind, value = min(identifiers, key=lambda item: (priority[item[0]], item[1]))
        return f"{kind}:{value}"
    first = group[0].candidate
    return "title:" + "|".join(
        (
            normalize_title(first.title) or "",
            str(first.year or ""),
            _normalized_author(first.authors[0]) if first.authors else "",
        )
    )


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")


def _candidate(record: dict[str, object], source_order: int) -> LiteratureCandidate:
    external_ids = record.get("externalIds") or {}
    open_access_pdf = record.get("openAccessPdf") or {}
    authors = record.get("authors") or []
    year = record.get("year")
    return LiteratureCandidate(
        source="Semantic Scholar",
        source_id=str(record.get("paperId") or ""),
        title=_optional_text(record.get("title")),
        authors=tuple(
            name
            for author in authors
            if (name := _optional_text(author.get("name"))) is not None
        ),
        year=year if isinstance(year, int) else None,
        venue=_optional_text(record.get("venue")),
        doi=_optional_text(external_ids.get("DOI")),
        abstract=_optional_text(record.get("abstract")),
        landing_page_url=_optional_text(record.get("url")),
        pdf_url=_optional_text(open_access_pdf.get("url")),
        source_order=source_order,
    )


def _arxiv_candidate(
    entry: ET.Element, source_order: int
) -> LiteratureCandidate:
    entry_id = _normalized_text(entry.findtext("atom:id", namespaces=_XML_NAMESPACES))
    published = _normalized_text(
        entry.findtext("atom:published", namespaces=_XML_NAMESPACES)
    )
    landing_page_url = None
    pdf_url = None
    for link in entry.findall("atom:link", _XML_NAMESPACES):
        href = _optional_text(link.get("href"))
        if link.get("rel") == "alternate" and link.get("type") == "text/html":
            landing_page_url = href
        if link.get("type") == "application/pdf":
            pdf_url = href

    source_id = ""
    if entry_id is not None:
        path = urlsplit(entry_id).path
        if path.startswith("/abs/"):
            source_id = path.removeprefix("/abs/")

    return LiteratureCandidate(
        source="arXiv",
        source_id=source_id,
        title=_normalized_text(
            entry.findtext("atom:title", namespaces=_XML_NAMESPACES)
        ),
        authors=tuple(
            name
            for author in entry.findall("atom:author", _XML_NAMESPACES)
            if (
                name := _normalized_text(
                    author.findtext("atom:name", namespaces=_XML_NAMESPACES)
                )
            )
            is not None
        ),
        year=(
            int(published[:4])
            if published is not None and published[:4].isdigit()
            else None
        ),
        venue=_normalized_text(
            entry.findtext("arxiv:journal_ref", namespaces=_XML_NAMESPACES)
        ),
        doi=_normalized_text(
            entry.findtext("arxiv:doi", namespaces=_XML_NAMESPACES)
        ),
        abstract=_normalized_text(
            entry.findtext("atom:summary", namespaces=_XML_NAMESPACES)
        ),
        landing_page_url=landing_page_url or entry_id,
        pdf_url=pdf_url,
        source_order=source_order,
    )


def _optional_text(value: object) -> str | None:
    return value if isinstance(value, str) and value else None


def _normalized_text(value: str | None) -> str | None:
    return " ".join(value.split()) if value and value.split() else None
