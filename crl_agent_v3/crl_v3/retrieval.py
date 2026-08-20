from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .knowledge import KnowledgeStore, SearchHit
from .vector import Encoder, VectorHit, semantic_search, vector_index_status


@dataclass(frozen=True, slots=True)
class HybridHit:
    paper_id: str
    passage_id: str
    title: str
    section: str
    page_start: int
    page_end: int
    char_start: int
    char_end: int
    text: str
    fulltext_sha256: str
    text_sha256: str
    routes: tuple[str, ...]
    fused_score: float
    fts_rank: int | None
    vector_rank: int | None
    fts_score: float | None
    vector_score: float | None


@dataclass(frozen=True, slots=True)
class HybridSearchResult:
    hits: tuple[HybridHit, ...]
    degraded: bool
    degradation_reason: str | None


def hybrid_search(
    store: KnowledgeStore,
    vector_index_path: str | Path,
    query: str,
    limit: int = 10,
    *,
    route_limit: int | None = None,
    rrf_k: int = 60,
    encoder: Encoder | None = None,
    encoder_id: str | None = None,
) -> HybridSearchResult:
    if limit <= 0:
        raise ValueError("Search limit must be positive")
    if rrf_k <= 0:
        raise ValueError("RRF constant must be positive")
    candidate_limit = route_limit if route_limit is not None else max(20, limit * 4)
    if candidate_limit <= 0:
        raise ValueError("Route limit must be positive")

    fts_hits = store.search(query, limit=candidate_limit)
    status = vector_index_status(store, vector_index_path)
    vector_hits: list[VectorHit] = []
    degraded = status["ready"] is not True
    reason = None if not degraded else str(status["reason"])
    if not degraded:
        try:
            vector_hits = semantic_search(
                store,
                vector_index_path,
                query,
                limit=candidate_limit,
                encoder=encoder,
                encoder_id=encoder_id,
            )
        except (ImportError, OSError, RuntimeError, ValueError) as exc:
            degraded = True
            reason = f"vector_search_failed:{type(exc).__name__}:{exc}"

    candidates: dict[str, dict[str, object]] = {}
    for rank, hit in enumerate(fts_hits, start=1):
        item = _candidate(candidates, hit)
        item["fts_rank"] = rank
        item["fts_score"] = hit.rank
        item["fused_score"] = float(item["fused_score"]) + 1 / (rrf_k + rank)
    for rank, hit in enumerate(vector_hits, start=1):
        item = _candidate(candidates, hit)
        item["vector_rank"] = rank
        item["vector_score"] = hit.score
        item["fused_score"] = float(item["fused_score"]) + 1 / (rrf_k + rank)

    ordered = sorted(
        candidates.values(),
        key=lambda item: (-float(item["fused_score"]), str(item["passage_id"])),
    )[:limit]
    return HybridSearchResult(
        hits=tuple(_hybrid_hit(item) for item in ordered),
        degraded=degraded,
        degradation_reason=reason,
    )


def _candidate(
    candidates: dict[str, dict[str, object]], hit: SearchHit | VectorHit
) -> dict[str, object]:
    existing = candidates.get(hit.passage_id)
    if existing is not None:
        if (
            existing["text_sha256"] != hit.text_sha256
            or existing["fulltext_sha256"] != hit.fulltext_sha256
        ):
            raise ValueError("Recall routes disagree on authoritative passage hashes")
        return existing
    item: dict[str, object] = {
        "paper_id": hit.paper_id,
        "passage_id": hit.passage_id,
        "title": hit.title,
        "section": hit.section,
        "page_start": hit.page_start,
        "page_end": hit.page_end,
        "char_start": hit.char_start,
        "char_end": hit.char_end,
        "text": hit.text,
        "fulltext_sha256": hit.fulltext_sha256,
        "text_sha256": hit.text_sha256,
        "fused_score": 0.0,
        "fts_rank": None,
        "vector_rank": None,
        "fts_score": None,
        "vector_score": None,
    }
    candidates[hit.passage_id] = item
    return item


def _hybrid_hit(item: dict[str, object]) -> HybridHit:
    routes = tuple(
        route
        for route, field in (("fts", "fts_rank"), ("vector", "vector_rank"))
        if item[field] is not None
    )
    return HybridHit(
        paper_id=str(item["paper_id"]),
        passage_id=str(item["passage_id"]),
        title=str(item["title"]),
        section=str(item["section"]),
        page_start=int(item["page_start"]),
        page_end=int(item["page_end"]),
        char_start=int(item["char_start"]),
        char_end=int(item["char_end"]),
        text=str(item["text"]),
        fulltext_sha256=str(item["fulltext_sha256"]),
        text_sha256=str(item["text_sha256"]),
        routes=routes,
        fused_score=float(item["fused_score"]),
        fts_rank=int(item["fts_rank"]) if item["fts_rank"] is not None else None,
        vector_rank=(
            int(item["vector_rank"]) if item["vector_rank"] is not None else None
        ),
        fts_score=float(item["fts_score"]) if item["fts_score"] is not None else None,
        vector_score=(
            float(item["vector_score"])
            if item["vector_score"] is not None
            else None
        ),
    )
