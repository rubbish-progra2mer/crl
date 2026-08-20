from __future__ import annotations

import hashlib
import json
import os
import re
from dataclasses import asdict, dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Iterable, Mapping, Sequence
from uuid import uuid4

from . import cards as cards_module
from . import knowledge as knowledge_module
from . import retrieval as retrieval_module
from . import vector as vector_module
from .cards import (
    card_index_status,
    card_source_signature,
    parse_card,
    search_cards,
)
from .knowledge import KnowledgeStore, Paper, normalize_fts_query, paper_payload
from .retrieval import hybrid_search
from .vector import vector_index_status
from .workspace import (
    ResearchWorkspace,
    _is_reparse_point,
    _path_entry_exists,
    _sha256,
    _validate_utf8_lf,
)


QUERY_PURPOSES = ("problem", "failure", "operator", "prior", "measurement")
SNAPSHOT_FILES = ("request.json", "result.json", "report.md")

_PURPOSE_ROUTES = {
    "problem": ("paper", "failure", "passage", "operator"),
    "failure": ("failure", "passage", "operator", "paper"),
    "operator": ("operator", "paper", "passage", "failure"),
    "prior": ("paper", "operator", "failure", "passage"),
    "measurement": ("paper", "passage", "failure", "operator"),
}
_PURPOSE_FOCUS = {
    "problem": "recurring problems and unresolved task, horizon, and budget boundaries",
    "failure": "failure conditions, alternative explanations, and mechanism limits",
    "operator": "changed computation, intervention point, information, timing, and budget",
    "prior": "closest work, component overlap, and substantive computation differences",
    "measurement": "data, metrics, evaluator, ground truth, baselines, units, and budget",
}

_SEARCH_ID = re.compile(r"[a-z0-9][a-z0-9._-]{2,63}")
_REPORT_META_PREFIX = "<!-- CRL_RESEARCH_SEARCH_META "
_REPORT_META_SUFFIX = " -->"
_REPORT_FORMAT_COMPACT = "compact-v2"

_rename_directory = os.rename


@dataclass(frozen=True, slots=True)
class ResearchQuery:
    purpose: str
    text: str
    source: str


@dataclass(frozen=True, slots=True)
class ResearchBundle:
    request: dict[str, object]
    result: dict[str, object]


@dataclass(frozen=True, slots=True)
class ExistingSearchSnapshot:
    path: Path
    created_at_utc: str
    files: tuple[tuple[str, bytes], ...]


@dataclass(frozen=True, slots=True)
class SearchSnapshotPublication:
    path: str
    created_at_utc: str
    idempotent: bool
    files: tuple[tuple[str, str], ...]


def parse_explicit_queries(values: Iterable[str]) -> tuple[ResearchQuery, ...]:
    queries: list[ResearchQuery] = []
    for value in values:
        purpose, separator, text = value.partition("=")
        purpose = purpose.strip().casefold()
        text = text.strip()
        if not separator or purpose not in QUERY_PURPOSES or not text:
            raise ValueError(
                "--query must use PURPOSE=TEXT with PURPOSE in "
                + ", ".join(QUERY_PURPOSES)
            )
        queries.append(ResearchQuery(purpose, text, "explicit_query"))
    if not queries:
        raise ValueError("at least one explicit query is required")
    return tuple(queries)


def hypothesis_queries(record: object) -> tuple[ResearchQuery, ...]:
    fields = (
        ("problem", getattr(record, "problem", ""), "hypothesis.problem"),
        (
            "failure",
            getattr(getattr(record, "target_failure", None), "summary", ""),
            "hypothesis.target_failure.summary",
        ),
        (
            "operator",
            " ".join(
                item
                for item in (
                    getattr(
                        getattr(record, "changed_computation", None),
                        "intervention",
                        "",
                    ),
                    getattr(record, "mechanism_claim", ""),
                )
                if item
            ),
            "hypothesis.changed_computation.intervention+mechanism_claim",
        ),
        (
            "prior",
            getattr(record, "nearest_prior_risk", ""),
            "hypothesis.nearest_prior_risk",
        ),
        (
            "measurement",
            " ".join(
                item
                for item in (
                    getattr(record, "falsifier", ""),
                    getattr(record, "minimal_killer_experiment", ""),
                )
                if item
            ),
            "hypothesis.falsifier+minimal_killer_experiment",
        ),
    )
    queries = tuple(
        ResearchQuery(purpose, str(text).strip(), source)
        for purpose, text, source in fields
        if str(text).strip()
    )
    if not queries:
        raise ValueError("hypothesis has no searchable research fields")
    return queries


def build_research_bundle(
    product_root: str | Path,
    knowledge_root: str | Path,
    store: KnowledgeStore,
    queries: Sequence[ResearchQuery],
    *,
    input_mode: str,
    input_identity: Mapping[str, object],
    card_limit: int = 10,
    passage_limit: int = 10,
    additional_code_paths: Sequence[str | Path] = (),
) -> ResearchBundle:
    if input_mode not in {"hypothesis", "explicit"}:
        raise ValueError("input_mode must be hypothesis or explicit")
    if not queries:
        raise ValueError("research retrieval requires at least one query")
    if card_limit <= 0 or passage_limit <= 0:
        raise ValueError("retrieval limits must be positive")
    product, root = bind_research_knowledge_root(product_root, knowledge_root)
    database = root / "knowledge.sqlite"
    if store.database_path.resolve() != database:
        raise ValueError("KnowledgeStore must be bound to knowledge_root/knowledge.sqlite")

    normalized_queries = []
    for index, query in enumerate(queries, start=1):
        if query.purpose not in QUERY_PURPOSES:
            raise ValueError(f"unsupported query purpose: {query.purpose}")
        normalized = normalize_fts_query(query.text)
        normalized_queries.append(
            {
                "query_id": f"q{index:03d}",
                "purpose": query.purpose,
                "source": query.source,
                "original_query": normalized.original_query,
                "normalized_query": normalized.normalized_query,
                "english_keyword_hint": normalized.english_keyword_hint,
            }
        )

    knowledge_identity = _knowledge_identity(root, store)
    code_identity = _code_identity(additional_code_paths)
    query_results = tuple(
        _execute_query(
            product,
            root,
            store,
            query,
            card_limit=card_limit,
            passage_limit=passage_limit,
        )
        for query in normalized_queries
    )
    current_knowledge_identity = _knowledge_identity(root, store)
    if current_knowledge_identity != knowledge_identity:
        raise RuntimeError("knowledge identity changed during research retrieval")
    request = {
        "schema_version": 1,
        "bundle_kind": "run_local_non_authoritative_research_retrieval",
        "input_mode": input_mode,
        "input_identity": dict(input_identity),
        "queries": normalized_queries,
        "limits": {"card_per_route": card_limit, "passage_hybrid": passage_limit},
        "knowledge_identity": knowledge_identity,
        "code_identity": code_identity,
    }
    result = {
        "schema_version": 1,
        "bundle_kind": "run_local_non_authoritative_research_retrieval",
        "report_format": _REPORT_FORMAT_COMPACT,
        "queries": list(query_results),
        "compact_research_map": _compact_research_map(query_results),
        "diagnostics": _diagnostics(query_results),
    }
    return ResearchBundle(request=request, result=result)


def bind_research_knowledge_root(
    product_root: str | Path, knowledge_root: str | Path
) -> tuple[Path, Path]:
    product = Path(os.path.abspath(product_root))
    if not _path_entry_exists(product) or not product.is_dir():
        raise FileNotFoundError(f"product root is not an existing directory: {product}")
    if _is_reparse_point(product):
        raise ValueError(f"product root must not be a reparse point: {product}")
    resolved_product = product.resolve(strict=True)
    if resolved_product != product:
        raise ValueError(f"product root resolves away from its lexical path: {product}")
    root = Path(os.path.abspath(knowledge_root))
    if root != product / "knowledge_base":
        raise ValueError("knowledge_root must be the fixed product knowledge_base path")
    _bind_product_asset(product, root, required=True, directory=True)
    _bind_product_asset(
        product, root / "knowledge.sqlite", required=True, directory=False
    )
    cards_root = _bind_product_asset(
        product, root / "cards", required=True, directory=True
    )
    for kind in ("failure", "operator", "paper"):
        _bind_product_asset(
            product, cards_root / kind, required=False, directory=True
        )
    _bind_product_asset(
        product, root / "cards_fts.sqlite", required=False, directory=False
    )
    _bind_product_asset(
        product, root / "passages.npz", required=False, directory=False
    )
    return product, root


def verify_existing_search(
    workspace: ResearchWorkspace, search_id: str
) -> ExistingSearchSnapshot | None:
    identifier = validate_search_id(search_id)
    destination = _search_path(workspace, identifier)
    workspace.assert_write_target(destination)
    if not destination.exists() and not destination.is_symlink():
        return None
    if not destination.is_dir():
        raise ValueError(f"search snapshot path is not a directory: {destination}")
    names = tuple(sorted(path.name for path in destination.iterdir()))
    if names != tuple(sorted(SNAPSHOT_FILES)):
        raise ValueError("search snapshot must contain exactly request.json, result.json, report.md")
    files = {
        name: workspace.assert_read_target(destination / name).read_bytes()
        for name in SNAPSHOT_FILES
    }
    for name, data in files.items():
        _validate_utf8_lf(data, f"search snapshot {name}")
        if not data:
            raise ValueError(f"empty search snapshot file: {name}")

    request = _canonical_json_document(files["request.json"], "request.json")
    result = _canonical_json_document(files["result.json"], "result.json")
    if request.get("search_id") != identifier or result.get("search_id") != identifier:
        raise ValueError("search snapshot SEARCH_ID mismatch")
    created = request.get("created_at_utc")
    _validate_utc(created)
    if result.get("created_at_utc") != created:
        raise ValueError("search snapshot UTC identity mismatch")
    artifact_hashes = request.get("artifact_hashes")
    if not isinstance(artifact_hashes, dict) or set(artifact_hashes) != {
        "result_json_sha256",
        "report_md_sha256",
    }:
        raise ValueError("search snapshot artifact hashes are invalid")
    if artifact_hashes["result_json_sha256"] != _sha256(files["result.json"]):
        raise ValueError("search snapshot result.json hash mismatch")
    if artifact_hashes["report_md_sha256"] != _sha256(files["report.md"]):
        raise ValueError("search snapshot report.md hash mismatch")

    request_base = dict(request)
    request_base.pop("artifact_hashes")
    fingerprint = _sha256(_json_bytes(request_base))
    if result.get("request_fingerprint_sha256") != fingerprint:
        raise ValueError("search snapshot request fingerprint mismatch")
    report_text = files["report.md"].decode("utf-8")
    first_line = report_text.split("\n", 1)[0]
    if not first_line.startswith(_REPORT_META_PREFIX) or not first_line.endswith(
        _REPORT_META_SUFFIX
    ):
        raise ValueError("search snapshot report metadata is missing")
    try:
        report_meta = json.loads(
            first_line[len(_REPORT_META_PREFIX) : -len(_REPORT_META_SUFFIX)]
        )
    except json.JSONDecodeError as error:
        raise ValueError("search snapshot report metadata is invalid") from error
    expected_meta = {
        "created_at_utc": created,
        "request_fingerprint_sha256": fingerprint,
        "result_json_sha256": _sha256(files["result.json"]),
        "search_id": identifier,
    }
    if report_meta != expected_meta:
        raise ValueError("search snapshot report identity mismatch")
    if files["report.md"] != _render_report(result, expected_meta):
        raise ValueError("search snapshot report bytes are not canonical")
    return ExistingSearchSnapshot(
        path=destination,
        created_at_utc=str(created),
        files=tuple((name, files[name]) for name in SNAPSHOT_FILES),
    )


def publish_search_snapshot(
    workspace: ResearchWorkspace,
    search_id: str,
    bundle: ResearchBundle,
    *,
    now: str | None = None,
) -> SearchSnapshotPublication:
    workspace.assert_run_writable()
    identifier = validate_search_id(search_id)
    existing = verify_existing_search(workspace, identifier)
    created = existing.created_at_utc if existing is not None else (now or _utc_now())
    _validate_utc(created)
    materialized = _materialize(bundle, identifier, created)
    if existing is not None:
        if dict(existing.files) != materialized:
            raise FileExistsError(
                "SEARCH_ID already exists with different request, identity, or result"
            )
        return _publication(existing.path, created, materialized, idempotent=True)

    destination = _search_path(workspace, identifier)
    parent = workspace.assert_write_target(destination.parent)
    parent.mkdir(parents=True, exist_ok=True)
    workspace.assert_write_target(destination)
    temporary = workspace.assert_write_target(
        parent / f".{identifier}.{uuid4().hex}.tmp"
    )
    temporary.mkdir()
    try:
        for name in SNAPSHOT_FILES:
            path = temporary / name
            with path.open("xb") as handle:
                handle.write(materialized[name])
                handle.flush()
                os.fsync(handle.fileno())
        try:
            _rename_directory(temporary, destination)
        except OSError:
            raced = verify_existing_search(workspace, identifier)
            if raced is None:
                raise
            raced_materialized = _materialize(
                bundle, identifier, raced.created_at_utc
            )
            if dict(raced.files) != raced_materialized:
                raise FileExistsError(
                    "SEARCH_ID was concurrently created with different content"
                )
            return _publication(
                raced.path,
                raced.created_at_utc,
                raced_materialized,
                idempotent=True,
            )
    finally:
        if temporary.exists() and temporary.is_dir():
            for path in temporary.iterdir():
                path.unlink()
            temporary.rmdir()
    return _publication(destination, created, materialized, idempotent=False)


def validate_search_id(value: str) -> str:
    if not isinstance(value, str) or _SEARCH_ID.fullmatch(value) is None:
        raise ValueError(
            "SEARCH_ID must be 3-64 lowercase letters, digits, dot, underscore, or hyphen"
        )
    return value


def materialized_result(
    bundle: ResearchBundle, *, created_at_utc: str | None = None
) -> dict[str, object]:
    created = created_at_utc or _utc_now()
    _validate_utc(created)
    request = dict(bundle.request)
    request["created_at_utc"] = created
    fingerprint = _sha256(_json_bytes(request))
    result = dict(bundle.result)
    result.update(
        {
            "created_at_utc": created,
            "request_fingerprint_sha256": fingerprint,
        }
    )
    return {"request": request, "result": result}


def _execute_query(
    product_root: Path,
    root: Path,
    store: KnowledgeStore,
    query: Mapping[str, object],
    *,
    card_limit: int,
    passage_limit: int,
) -> dict[str, object]:
    original = str(query["original_query"])
    normalized = str(query["normalized_query"])
    purpose = str(query["purpose"])
    route_plan = _PURPOSE_ROUTES[purpose]
    routes = []
    for priority, route_kind in enumerate(route_plan, start=1):
        if route_kind == "passage":
            route = _passage_route(
                root,
                store,
                original,
                normalized,
                limit=passage_limit,
            )
        else:
            route = _card_route(
                product_root,
                root,
                store,
                original,
                normalized,
                kind=route_kind,
                limit=card_limit,
            )
        route["purpose_priority"] = priority
        route["hits"] = [
            _annotate_hit(
                hit,
                original,
                purpose_priority=priority,
                route_degraded=bool(route["degraded"]),
            )
            for hit in route["hits"]
        ]
        routes.append(route)
    return {
        **dict(query),
        "route_plan": list(route_plan),
        "output_focus": _PURPOSE_FOCUS[purpose],
        "routes": routes,
    }


def _card_route(
    product_root: Path,
    root: Path,
    store: KnowledgeStore,
    original: str,
    normalized: str,
    *,
    kind: str,
    limit: int,
) -> dict[str, object]:
    cards_root = root / "cards"
    index_path = root / "cards_fts.sqlite"
    status = card_index_status(cards_root, index_path)
    route = {
        "route": f"{kind}_card_fts",
        "query": original,
        "normalized_query": normalized,
        "source": str(index_path),
        "degraded": status.get("ready") is not True,
        "degradation_reason": None
        if status.get("ready") is True
        else str(status.get("reason")),
        "hits": [],
    }
    if status.get("ready") is not True:
        return route
    hits = search_cards(
        cards_root,
        index_path,
        original,
        kinds=(kind,),  # type: ignore[arg-type]
        limit=limit,
    )
    route["hits"] = [
        _expand_card_hit(product_root, root, store, hit, rank)
        for rank, hit in enumerate(hits, start=1)
    ]
    return route


def _expand_card_hit(
    product_root: Path,
    root: Path,
    store: KnowledgeStore,
    hit: object,
    route_rank: int,
) -> dict[str, object]:
    relative_path = str(getattr(hit, "relative_path"))
    card_path = _bind_product_asset(
        product_root,
        root / "cards" / relative_path,
        required=True,
        directory=False,
    )
    card = parse_card(card_path)
    if card.sha256 != getattr(hit, "markdown_sha256"):
        raise ValueError(f"Card hit hash mismatch: {card.metadata.card_id}")
    evidence_items = []
    papers: dict[str, dict[str, object]] = {}
    for evidence_id in card.metadata.evidence_ids:
        evidence = store.get_evidence(evidence_id)
        if evidence is None:
            raise ValueError(f"Card refers to missing Evidence: {evidence_id}")
        if not evidence.fulltext_is_current or evidence.passage_is_current is False:
            raise ValueError(f"Card refers to stale Evidence: {evidence_id}")
        paper = store.get_paper(evidence.paper_id)
        if paper is None:
            raise ValueError(f"Evidence refers to missing Paper: {evidence.paper_id}")
        papers[paper.paper_id] = _paper_identity(root, paper)
        evidence_items.append(
            {
                "evidence_id": evidence.evidence_id,
                "paper_id": evidence.paper_id,
                "locator": evidence.locator,
                "section": evidence.section,
                "page_start": evidence.page_start,
                "page_end": evidence.page_end,
                "passage_id": evidence.passage_id,
                "quote_start": evidence.quote_start,
                "quote_end": evidence.quote_end,
                "fulltext_sha256": evidence.fulltext_sha256,
                "source_content_sha256": evidence.source_content_sha256,
                "passage_text_sha256": evidence.passage_text_sha256,
                "fulltext_is_current": evidence.fulltext_is_current,
                "passage_is_current": evidence.passage_is_current,
            }
        )
    if card.metadata.paper_id is not None:
        paper = store.get_paper(card.metadata.paper_id)
        if paper is None:
            raise ValueError(f"Card refers to missing Paper: {card.metadata.paper_id}")
        papers[paper.paper_id] = _paper_identity(root, paper)
    return {
        "rank": route_rank,
        "score": float(getattr(hit, "rank")),
        "score_kind": "sqlite_fts5_bm25",
        "card_id": card.metadata.card_id,
        "card_kind": card.metadata.card_kind,
        "relative_path": relative_path,
        "title": str(getattr(hit, "title")),
        "snippet": str(getattr(hit, "snippet")),
        "card_markdown_sha256": card.sha256,
        "source_refs": [asdict(item) for item in card.metadata.source_refs],
        "evidence": evidence_items,
        "papers": [papers[key] for key in sorted(papers)],
    }


def _passage_route(
    root: Path,
    store: KnowledgeStore,
    original: str,
    normalized: str,
    *,
    limit: int,
) -> dict[str, object]:
    vector_path = root / "passages.npz"
    result = hybrid_search(store, vector_path, original, limit=limit)
    return {
        "route": "passage_hybrid",
        "query": original,
        "normalized_query": normalized,
        "source": {
            "fts": str(root / "knowledge.sqlite"),
            "vector": str(vector_path),
        },
        "degraded": result.degraded,
        "degradation_reason": result.degradation_reason,
        "hits": [
            {
                "rank": rank,
                "score": hit.fused_score,
                "score_kind": "reciprocal_rank_fusion",
                **asdict(hit),
            }
            for rank, hit in enumerate(result.hits, start=1)
        ],
    }


def _diagnostics(query_results: Sequence[Mapping[str, object]]) -> dict[str, object]:
    cards: set[str] = set()
    evidence: set[str] = set()
    passages: set[str] = set()
    paper_routes: dict[str, set[str]] = {}
    coverage = []
    noisy_hits = 0
    observation_count = 0
    for query in query_results:
        query_id = str(query["query_id"])
        for route in query["routes"]:  # type: ignore[index]
            route_name = str(route["route"])
            route_key = f"{query_id}:{route_name}"
            hits = route["hits"]
            coverage.append(
                {
                    "query_id": query_id,
                    "route": route_name,
                    "hit_count": len(hits),
                    "degraded": bool(route["degraded"]),
                }
            )
            for hit in hits:
                observation_count += 1
                if hit["noise_flags"]:
                    noisy_hits += 1
                if "card_id" in hit:
                    cards.add(str(hit["card_id"]))
                    for item in hit["evidence"]:
                        evidence.add(str(item["evidence_id"]))
                        paper_routes.setdefault(str(item["paper_id"]), set()).add(
                            route_key
                        )
                    for paper in hit["papers"]:
                        paper_routes.setdefault(str(paper["paper_id"]), set()).add(
                            route_key
                        )
                else:
                    passages.add(str(hit["passage_id"]))
                    paper_routes.setdefault(str(hit["paper_id"]), set()).add(
                        route_key
                    )
    return {
        "label": "diagnostics_only_not_scientific_judgment",
        "route_coverage": coverage,
        "unique_card_ids": sorted(cards),
        "unique_evidence_ids": sorted(evidence),
        "unique_passage_ids": sorted(passages),
        "observation_count": observation_count,
        "noisy_observation_count": noisy_hits,
        "paper_route_hits": [
            {"paper_id": paper_id, "routes": sorted(routes)}
            for paper_id, routes in sorted(paper_routes.items())
        ],
    }


def _annotate_hit(
    hit: Mapping[str, object],
    query: str,
    *,
    purpose_priority: int,
    route_degraded: bool,
) -> dict[str, object]:
    item = dict(hit)
    excerpt = str(item.get("snippet") or item.get("text") or item.get("title") or "")
    query_tokens = _diagnostic_tokens(query)
    excerpt_tokens = _diagnostic_tokens(excerpt)
    flags = []
    weight = 1.0 / purpose_priority
    if route_degraded:
        flags.append("route_degraded")
        weight *= 0.75
    if query_tokens and query_tokens.isdisjoint(excerpt_tokens):
        flags.append("weak_lexical_overlap")
        weight *= 0.6
    if len(excerpt.strip()) < 40:
        flags.append("short_excerpt")
        weight *= 0.85
    item["noise_flags"] = flags
    item["attention_weight"] = round(weight, 6)
    item["attention_weight_kind"] = (
        "transparent_route_priority_and_noise_diagnostic_not_relevance"
    )
    return item


def _diagnostic_tokens(value: str) -> set[str]:
    return {
        token.casefold()
        for token in re.findall(r"[^\W_]+", value, flags=re.UNICODE)
        if len(token) >= 2
    }


def _compact_research_map(
    query_results: Sequence[Mapping[str, object]],
) -> dict[str, object]:
    entries: dict[str, dict[str, object]] = {}
    for query in query_results:
        query_id = str(query["query_id"])
        purpose = str(query["purpose"])
        for route in query["routes"]:  # type: ignore[index]
            route_name = str(route["route"])
            priority = int(route["purpose_priority"])
            for hit in route["hits"]:
                papers = (
                    list(hit["papers"])
                    if "card_id" in hit
                    else [
                        {
                            "paper_id": hit["paper_id"],
                            "title": hit.get("title", ""),
                        }
                    ]
                )
                for paper in papers:
                    paper_id = str(paper["paper_id"])
                    entry = entries.setdefault(
                        paper_id,
                        {
                            "paper_id": paper_id,
                            "title": str(paper.get("title", "")),
                            "purposes": set(),
                            "routes": set(),
                            "card_ids": set(),
                            "evidence_ids": set(),
                            "passage_ids": set(),
                            "noise_flags": set(),
                            "observation_count": 0,
                            "best_observation": None,
                        },
                    )
                    entry["purposes"].add(purpose)  # type: ignore[union-attr]
                    entry["routes"].add(f"{query_id}:{route_name}")  # type: ignore[union-attr]
                    entry["noise_flags"].update(hit["noise_flags"])  # type: ignore[union-attr]
                    entry["observation_count"] = int(entry["observation_count"]) + 1
                    if "card_id" in hit:
                        entry["card_ids"].add(str(hit["card_id"]))  # type: ignore[union-attr]
                        entry["evidence_ids"].update(  # type: ignore[union-attr]
                            str(item["evidence_id"])
                            for item in hit["evidence"]
                            if str(item["paper_id"]) == paper_id
                        )
                    else:
                        entry["passage_ids"].add(str(hit["passage_id"]))  # type: ignore[union-attr]
                    observation = {
                        "query_id": query_id,
                        "purpose": purpose,
                        "route": route_name,
                        "purpose_priority": priority,
                        "rank": int(hit["rank"]),
                        "attention_weight": float(hit["attention_weight"]),
                        "noise_flags": list(hit["noise_flags"]),
                        "excerpt": str(
                            hit.get("snippet") or hit.get("text") or hit.get("title") or ""
                        )[:600],
                    }
                    best = entry["best_observation"]
                    if best is None or _observation_key(observation) < _observation_key(best):
                        entry["best_observation"] = observation
    compact_entries = []
    for paper_id, entry in entries.items():
        observations = int(entry["observation_count"])
        compact_entries.append(
            {
                "paper_id": paper_id,
                "title": entry["title"],
                "purposes": sorted(entry["purposes"]),
                "routes": sorted(entry["routes"]),
                "card_ids": sorted(entry["card_ids"]),
                "evidence_ids": sorted(entry["evidence_ids"]),
                "passage_ids": sorted(entry["passage_ids"]),
                "noise_flags": sorted(entry["noise_flags"]),
                "observation_count": observations,
                "duplicate_observation_count": max(0, observations - 1),
                "best_observation": entry["best_observation"],
            }
        )
    compact_entries.sort(
        key=lambda item: (
            *_observation_key(item["best_observation"]),
            str(item["paper_id"]),
        )
    )
    representatives = _representative_entries(query_results)
    return {
        "label": "compact_navigation_only_not_scientific_judgment",
        "deduplication_key": "paper_id",
        "ranking_kind": "transparent_attention_diagnostic_not_relevance",
        "entry_count": len(compact_entries),
        "entries": compact_entries,
        "representative_selection": "first_unique_paper_per_query_route_by_route_rank",
        "representative_entry_count": len(representatives),
        "representative_entries": representatives,
    }


def _representative_entries(
    query_results: Sequence[Mapping[str, object]],
) -> list[dict[str, object]]:
    selected_papers: set[str] = set()
    representatives: list[dict[str, object]] = []
    for query in query_results:
        for route in query["routes"]:  # type: ignore[index]
            representative = None
            for hit in route["hits"]:
                papers = (
                    list(hit["papers"])
                    if "card_id" in hit
                    else [
                        {
                            "paper_id": hit["paper_id"],
                            "title": hit.get("title", ""),
                        }
                    ]
                )
                for paper in papers:
                    paper_id = str(paper["paper_id"])
                    if paper_id in selected_papers:
                        continue
                    representative = {
                        "paper_id": paper_id,
                        "title": str(paper.get("title", "")),
                        "query_id": str(query["query_id"]),
                        "purpose": str(query["purpose"]),
                        "route": str(route["route"]),
                        "purpose_priority": int(route["purpose_priority"]),
                        "rank": int(hit["rank"]),
                        "card_id": str(hit["card_id"])
                        if "card_id" in hit
                        else None,
                        "card_kind": str(hit["card_kind"])
                        if "card_id" in hit
                        else None,
                        "evidence_ids": sorted(
                            str(item["evidence_id"])
                            for item in hit.get("evidence", [])
                            if str(item["paper_id"]) == paper_id
                        ),
                        "passage_id": str(hit["passage_id"])
                        if "passage_id" in hit
                        else None,
                        "noise_flags": list(hit["noise_flags"]),
                    }
                    selected_papers.add(paper_id)
                    break
                if representative is not None:
                    representatives.append(representative)
                    break
    return representatives


def _observation_key(observation: Mapping[str, object]) -> tuple[object, ...]:
    return (
        -float(observation["attention_weight"]),
        int(observation["purpose_priority"]),
        int(observation["rank"]),
        str(observation["query_id"]),
        str(observation["route"]),
    )


def _knowledge_identity(root: Path, store: KnowledgeStore) -> dict[str, object]:
    cards_root = root / "cards"
    card_index = root / "cards_fts.sqlite"
    vector_index = root / "passages.npz"
    revision, generation = store.passage_identity()
    return {
        "knowledge_root": str(root),
        "knowledge_sqlite": {
            **_file_identity(root / "knowledge.sqlite"),
            "passage_revision": revision,
            "passage_generation_id": generation,
        },
        "cards_fts_sqlite": {
            **_file_identity(card_index),
            "status": _plain(card_index_status(cards_root, card_index)),
            "card_source_signature": card_source_signature(cards_root),
        },
        "passages_npz": {
            **_file_identity(vector_index),
            "status": _plain(vector_index_status(store, vector_index)),
        },
    }


def _code_identity(additional_paths: Sequence[str | Path]) -> dict[str, object]:
    paths = [
        Path(cards_module.__file__),
        Path(knowledge_module.__file__),
        Path(retrieval_module.__file__),
        Path(vector_module.__file__),
        Path(__file__),
        *(Path(path) for path in additional_paths),
    ]
    unique = sorted({path.resolve() for path in paths}, key=str)
    return {
        "files": [
            {"path": str(path), "sha256": _file_sha256(path), "size_bytes": path.stat().st_size}
            for path in unique
        ]
    }


def _paper_identity(root: Path, paper: Paper) -> dict[str, object]:
    return paper_payload(root, paper)


def _file_identity(path: Path) -> dict[str, object]:
    if not path.is_file():
        return {"path": str(path), "exists": False, "size_bytes": None, "sha256": None}
    return {
        "path": str(path),
        "exists": True,
        "size_bytes": path.stat().st_size,
        "sha256": _file_sha256(path),
    }


def _file_sha256(path: Path) -> str:
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def _plain(value: object) -> object:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, Mapping):
        return {str(key): _plain(item) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        return [_plain(item) for item in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def _bind_product_asset(
    product_root: Path,
    path: str | Path,
    *,
    required: bool,
    directory: bool,
) -> Path:
    target = Path(os.path.abspath(path))
    try:
        relative = target.relative_to(product_root)
    except ValueError as error:
        raise ValueError(f"knowledge asset escapes product root: {target}") from error
    current = product_root
    for part in relative.parts:
        current = current / part
        if _path_entry_exists(current) and _is_reparse_point(current):
            raise ValueError(f"knowledge asset uses a reparse point: {current}")
    if not _path_entry_exists(target):
        if required:
            raise FileNotFoundError(f"required knowledge asset is missing: {target}")
        return target
    resolved = target.resolve(strict=True)
    try:
        resolved.relative_to(product_root)
    except ValueError as error:
        raise ValueError(f"knowledge asset resolves outside product root: {target}") from error
    if resolved != target:
        raise ValueError(f"knowledge asset resolves away from its lexical path: {target}")
    if directory and not resolved.is_dir():
        raise FileNotFoundError(f"knowledge asset is not a directory: {target}")
    if not directory and not resolved.is_file():
        raise FileNotFoundError(f"knowledge asset is not a regular file: {target}")
    return target


def _materialize(
    bundle: ResearchBundle, search_id: str, created_at_utc: str
) -> dict[str, bytes]:
    request_base = dict(bundle.request)
    request_base.update(
        {"search_id": search_id, "created_at_utc": created_at_utc}
    )
    fingerprint = _sha256(_json_bytes(request_base))
    result = dict(bundle.result)
    result.update(
        {
            "search_id": search_id,
            "created_at_utc": created_at_utc,
            "request_fingerprint_sha256": fingerprint,
        }
    )
    result_bytes = _json_bytes(result)
    report_meta = {
        "created_at_utc": created_at_utc,
        "request_fingerprint_sha256": fingerprint,
        "result_json_sha256": _sha256(result_bytes),
        "search_id": search_id,
    }
    report_bytes = _render_report(result, report_meta)
    request = dict(request_base)
    request["artifact_hashes"] = {
        "result_json_sha256": _sha256(result_bytes),
        "report_md_sha256": _sha256(report_bytes),
    }
    return {
        "request.json": _json_bytes(request),
        "result.json": result_bytes,
        "report.md": report_bytes,
    }


def _render_report(
    result: Mapping[str, object], metadata: Mapping[str, object]
) -> bytes:
    report_format = result.get("report_format")
    if report_format is None:
        return _render_legacy_report(result, metadata)
    if report_format != _REPORT_FORMAT_COMPACT:
        raise ValueError(f"unsupported research report format: {report_format}")
    return _render_compact_report(result, metadata)


def _render_compact_report(
    result: Mapping[str, object], metadata: Mapping[str, object]
) -> bytes:
    lines = [
        _REPORT_META_PREFIX
        + json.dumps(dict(metadata), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + _REPORT_META_SUFFIX,
        "# 研究检索导航",
        "",
        "> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。",
        "",
        f"- 搜索标识：`{metadata['search_id']}`",
        f"- 生成时间（协调世界时）：`{metadata['created_at_utc']}`",
        "",
    ]
    compact_map = result["compact_research_map"]  # type: ignore[index]
    lines.extend(
        [
            "## 紧凑研究地图",
            "",
            "> 跨路线按 Paper 去重；每个查询路线至多选一个尚未出现的最高排名代表项。完整原始命中保留在 `result.json`。",
            "",
        ]
    )
    for entry in compact_map["representative_entries"]:
        identities = []
        if entry["card_id"]:
            identities.append(
                f"Card `{entry['card_id']}`（{entry['card_kind']}）"
            )
        if entry["evidence_ids"]:
            identities.append(
                "Evidence " + ", ".join(f"`{item}`" for item in entry["evidence_ids"])
            )
        if entry["passage_id"]:
            identities.append(f"Passage `{entry['passage_id']}`")
        identity_text = "；".join(identities) or "无附加定位"
        lines.append(
            f"- Paper `{entry['paper_id']}` · {entry['title']}；"
            f"用途 `{entry['purpose']}`；路线 `{entry['query_id']}:{entry['route']}` "
            f"#{entry['rank']}；{identity_text}"
        )
    lines.extend(
        [
            "",
            f"- 代表项：{compact_map['representative_entry_count']} / "
            f"去重 Paper：{compact_map['entry_count']}",
            "",
            "## 查询与路线覆盖",
            "",
        ]
    )
    for query in result["queries"]:  # type: ignore[index]
        lines.extend(
            [
                f"### {query['query_id']} · {query['purpose']}",
                "",
                f"- 原始查询：`{query['original_query']}`",
                f"- 规范化查询：`{query['normalized_query']}`",
            ]
        )
        for route in query["routes"]:
            reason = route["degradation_reason"] or "无"
            lines.append(
                f"- 路线 `{route['route']}`：{len(route['hits'])} 条；"
                f"降级 {str(route['degraded']).lower()}（{reason}）"
            )
        lines.append("")
    diagnostics = result["diagnostics"]  # type: ignore[index]
    lines.extend(
        [
            "## 覆盖诊断",
            "",
            f"- 去重 Card：{len(diagnostics['unique_card_ids'])}",
            f"- 去重 Evidence：{len(diagnostics['unique_evidence_ids'])}",
            f"- 去重 Passage：{len(diagnostics['unique_passage_ids'])}",
            f"- 命中 Paper：{len(diagnostics['paper_route_hits'])}",
            f"- 原始观测：{diagnostics.get('observation_count', '未记录')}",
            f"- 带机械噪声标记的观测：{diagnostics.get('noisy_observation_count', '未记录')}",
            "",
        ]
    )
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def _render_legacy_report(
    result: Mapping[str, object], metadata: Mapping[str, object]
) -> bytes:
    lines = [
        _REPORT_META_PREFIX
        + json.dumps(dict(metadata), ensure_ascii=False, sort_keys=True, separators=(",", ":"))
        + _REPORT_META_SUFFIX,
        "# 研究检索导航",
        "",
        "> 本报告仅展示查询路线、来源、命中定位与覆盖；所有科研判断由主研究者完成。",
        "",
        f"- 搜索标识：`{metadata['search_id']}`",
        f"- 生成时间（协调世界时）：`{metadata['created_at_utc']}`",
        "",
    ]
    for query in result["queries"]:  # type: ignore[index]
        lines.extend(
            [
                f"## {query['query_id']} · {query['purpose']}",
                "",
                f"- 原始查询：`{query['original_query']}`",
                f"- 规范化查询：`{query['normalized_query']}`",
                "",
            ]
        )
        for route in query["routes"]:
            reason = route["degradation_reason"] or "无"
            lines.extend(
                [
                    f"### 路线 `{route['route']}`",
                    "",
                    f"- 命中数：{len(route['hits'])}",
                    f"- 降级：{str(route['degraded']).lower()}（{reason}）",
                    "",
                ]
            )
            for hit in route["hits"]:
                if "card_id" in hit:
                    evidence_ids = ", ".join(
                        f"`{item['evidence_id']}`" for item in hit["evidence"]
                    ) or "无"
                    lines.append(
                        f"- #{hit['rank']} Card `{hit['card_id']}`；"
                        f"路径 `{hit['relative_path']}`；Evidence {evidence_ids}"
                    )
                else:
                    lines.append(
                        f"- #{hit['rank']} Passage `{hit['passage_id']}`；"
                        f"Paper `{hit['paper_id']}`；页 {hit['page_start']}-{hit['page_end']}"
                    )
            lines.append("")
    compact_map = result.get("compact_research_map")
    if isinstance(compact_map, Mapping):
        lines.extend(
            [
                "## 紧凑研究地图",
                "",
                "> 按 Paper 去重；注意力权重只反映用途路线顺序和机械噪声标记，不是相关性或科研结论。",
                "",
            ]
        )
        for entry in compact_map["entries"]:
            best = entry["best_observation"]
            flags = "、".join(entry["noise_flags"]) or "无"
            lines.append(
                f"- Paper `{entry['paper_id']}`；用途 {', '.join(entry['purposes'])}；"
                f"观测 {entry['observation_count']}（重复 {entry['duplicate_observation_count']}）；"
                f"最佳导航路线 `{best['query_id']}:{best['route']}`；"
                f"噪声标记：{flags}"
            )
        lines.append("")
    diagnostics = result["diagnostics"]  # type: ignore[index]
    lines.extend(
        [
            "## 覆盖诊断",
            "",
            f"- 去重 Card：{len(diagnostics['unique_card_ids'])}",
            f"- 去重 Evidence：{len(diagnostics['unique_evidence_ids'])}",
            f"- 去重 Passage：{len(diagnostics['unique_passage_ids'])}",
            f"- 命中 Paper：{len(diagnostics['paper_route_hits'])}",
            f"- 原始观测：{diagnostics.get('observation_count', '未记录')}",
            f"- 带机械噪声标记的观测：{diagnostics.get('noisy_observation_count', '未记录')}",
            "",
        ]
    )
    return ("\n".join(lines).rstrip() + "\n").encode("utf-8")


def _canonical_json_document(data: bytes, label: str) -> dict[str, object]:
    try:
        value = json.loads(data)
    except json.JSONDecodeError as error:
        raise ValueError(f"invalid search snapshot JSON: {label}") from error
    if not isinstance(value, dict) or _json_bytes(value) != data:
        raise ValueError(f"search snapshot JSON is not canonical: {label}")
    return value


def _json_bytes(value: Mapping[str, object]) -> bytes:
    return (
        json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    ).encode("utf-8")


def _search_path(workspace: ResearchWorkspace, search_id: str) -> Path:
    return (
        workspace.workspace_path
        / f"hypotheses_{workspace.version}"
        / "searches"
        / search_id
    )


def _publication(
    destination: Path,
    created: str,
    files: Mapping[str, bytes],
    *,
    idempotent: bool,
) -> SearchSnapshotPublication:
    return SearchSnapshotPublication(
        path=str(destination),
        created_at_utc=created,
        idempotent=idempotent,
        files=tuple((name, _sha256(files[name])) for name in SNAPSHOT_FILES),
    )


def _validate_utc(value: object) -> None:
    if not isinstance(value, str) or not value.endswith("Z"):
        raise ValueError("search snapshot UTC must be ISO-8601 and end in Z")
    try:
        parsed = datetime.fromisoformat(value[:-1] + "+00:00")
    except ValueError as error:
        raise ValueError("search snapshot UTC is invalid") from error
    if parsed.utcoffset() != UTC.utcoffset(parsed):
        raise ValueError("search snapshot timestamp must be UTC")


def _utc_now() -> str:
    return datetime.now(UTC).isoformat().replace("+00:00", "Z")
