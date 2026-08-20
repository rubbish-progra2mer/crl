from __future__ import annotations

import hashlib
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable
from uuid import uuid4

import numpy as np

from .knowledge import KnowledgeStore, Passage


DEFAULT_MODEL = "sentence-transformers/all-MiniLM-L6-v2"
DEFAULT_MODEL_REVISION = "1110a243fdf4706b3f48f1d95db1a4f5529b4d41"
Encoder = Callable[[list[str]], np.ndarray]
_SCHEMA_VERSION = "4"
_ENCODER_PIPELINE = "crl-encode-v1"
_MODEL_CACHE: dict[tuple[str, str], object] = {}
_INDEX_FIELDS = {
    "schema_version",
    "knowledge_revision",
    "passage_generation_id",
    "model_name",
    "model_revision",
    "encoder_id",
    "passage_count",
    "dimensions",
    "passage_ids",
    "text_sha256",
    "vector_passage_ids",
    "embeddings",
}


class _UnsupportedVectorIndexSchema(ValueError):
    pass


@dataclass(frozen=True, slots=True)
class VectorHit:
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
    score: float


def rebuild_vector_index(
    store: KnowledgeStore,
    index_path: str | Path,
    *,
    encoder: Encoder | None = None,
    model_name: str = DEFAULT_MODEL,
    model_revision: str | None = None,
    encoder_id: str | None = None,
) -> dict[str, object]:
    resolved_model_revision, resolved_encoder_id = _build_encoder_identity(
        encoder=encoder,
        encoder_id=encoder_id,
        model_name=model_name,
        model_revision=model_revision,
    )
    knowledge_identity, passages = store.passage_snapshot()
    if not passages:
        raise ValueError("Cannot build vector index without passages")
    _validate_passage_hashes(passages)
    chunk_texts, vector_passage_ids = _passage_chunks(
        passages,
        encoder=encoder,
        model_name=model_name,
        model_revision=resolved_model_revision,
    )
    embeddings = _normalize_matrix(
        _encode(chunk_texts, encoder, model_name, resolved_model_revision),
        expected_rows=len(chunk_texts),
    )

    path = Path(index_path).resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.parent / f".{path.name}.{uuid4().hex}.tmp"
    try:
        with temporary.open("xb") as stream:
            np.savez_compressed(
                stream,
                schema_version=np.asarray(_SCHEMA_VERSION),
                knowledge_revision=np.asarray(knowledge_identity[0], dtype=np.int64),
                passage_generation_id=np.asarray(knowledge_identity[1]),
                model_name=np.asarray(model_name),
                model_revision=np.asarray(resolved_model_revision),
                encoder_id=np.asarray(resolved_encoder_id),
                passage_count=np.asarray(len(passages), dtype=np.int64),
                dimensions=np.asarray(embeddings.shape[1], dtype=np.int64),
                passage_ids=np.asarray(
                    [passage.passage_id for passage in passages], dtype=np.str_
                ),
                text_sha256=np.asarray(
                    [passage.text_sha256 for passage in passages], dtype=np.str_
                ),
                vector_passage_ids=np.asarray(vector_passage_ids, dtype=np.str_),
                embeddings=embeddings,
            )
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise

    return {
        "index_path": str(path),
        "model_name": model_name,
        "model_revision": resolved_model_revision,
        "encoder_id": resolved_encoder_id,
        "dimensions": int(embeddings.shape[1]),
        "passages": len(passages),
    }


def vector_index_status(
    store: KnowledgeStore, index_path: str | Path
) -> dict[str, object]:
    path = Path(index_path).resolve()
    if not path.is_file():
        return {"ready": False, "reason": "index_missing", "index_path": str(path)}
    try:
        header = _load_index_header(path)
        index_identity = (
            header["knowledge_revision"],
            header["passage_generation_id"],
        )
        if index_identity != store.passage_identity():
            return {
                "ready": False,
                "reason": "passage_bindings_changed",
                "index_path": str(path),
            }
        return {
            "ready": True,
            "reason": "ready",
            "index_path": str(path),
            "model_name": header["model_name"],
            "model_revision": header["model_revision"],
            "encoder_id": header["encoder_id"],
            "dimensions": header["dimensions"],
            "passages": header["passage_count"],
        }
    except _UnsupportedVectorIndexSchema:
        return {
            "ready": False,
            "reason": "unsupported_vector_index_schema",
            "index_path": str(path),
        }
    except Exception as exc:
        return {
            "ready": False,
            "reason": "index_invalid",
            "index_path": str(path),
            "error": str(exc),
        }


def semantic_search(
    store: KnowledgeStore,
    index_path: str | Path,
    query: str,
    limit: int = 10,
    *,
    encoder: Encoder | None = None,
    encoder_id: str | None = None,
) -> list[VectorHit]:
    if encoder is not None and not _is_nonempty(encoder_id):
        raise ValueError("A non-empty encoder_id is required for a custom encoder")
    if not query.strip():
        return []
    if limit <= 0:
        raise ValueError("Search limit must be positive")
    status = vector_index_status(store, index_path)
    if status["ready"] is not True:
        raise ValueError(
            f"Vector index is stale or unavailable: {status['reason']}; rebuild it"
        )

    index = _load_index(Path(index_path).resolve())
    _validate_query_encoder(index, encoder=encoder, encoder_id=encoder_id)
    query_vector = _normalize_matrix(
        _encode(
            [query],
            encoder,
            str(index["model_name"]),
            str(index["model_revision"]),
        ),
        expected_rows=1,
    )[0]
    vector_scores = index["embeddings"] @ query_vector
    best_scores: dict[str, float] = {}
    for passage_id, score in zip(index["vector_passage_ids"], vector_scores):
        key = str(passage_id)
        best_scores[key] = max(best_scores.get(key, float("-inf")), float(score))
    order = sorted(best_scores, key=lambda passage_id: (-best_scores[passage_id], passage_id))[
        : min(limit, len(best_scores))
    ]
    hits: list[VectorHit] = []
    for passage_id in order:
        passage = store.get_passage(passage_id)
        if passage is None:
            raise ValueError("Vector index became stale during search")
        paper = store.get_paper(passage.paper_id)
        if paper is None:
            raise ValueError("Knowledge store is missing the indexed paper")
        hits.append(
            VectorHit(
                paper_id=paper.paper_id,
                passage_id=passage.passage_id,
                title=paper.title,
                section=passage.section,
                page_start=passage.page_start,
                page_end=passage.page_end,
                char_start=passage.char_start,
                char_end=passage.char_end,
                text=passage.text,
                fulltext_sha256=paper.fulltext_sha256,
                text_sha256=passage.text_sha256,
                score=best_scores[passage_id],
            )
        )
    if store.passage_identity() != (
        index["knowledge_revision"],
        index["passage_generation_id"],
    ):
        raise ValueError("Vector index became stale during search")
    return hits


def _load_index(path: Path) -> dict[str, Any]:
    with np.load(path, allow_pickle=False) as data:
        header = _index_header(data)
        passage_ids = np.asarray(data["passage_ids"], dtype=np.str_)
        text_sha256 = np.asarray(data["text_sha256"], dtype=np.str_)
        vector_passage_ids = np.asarray(data["vector_passage_ids"], dtype=np.str_)
        embeddings = np.asarray(data["embeddings"], dtype=np.float32)
        if (
            passage_ids.ndim != 1
            or text_sha256.ndim != 1
            or vector_passage_ids.ndim != 1
            or embeddings.ndim != 2
            or embeddings.shape[1] == 0
            or len(passage_ids) != len(text_sha256)
            or len(vector_passage_ids) != embeddings.shape[0]
            or set(vector_passage_ids.tolist()) != set(passage_ids.tolist())
            or len(passage_ids) != header["passage_count"]
            or embeddings.shape[1] != header["dimensions"]
        ):
            raise ValueError("Invalid vector index dimensions")
        if not np.isfinite(embeddings).all():
            raise ValueError("Vector index contains non-finite values")
        return {
            "model_name": header["model_name"],
            "model_revision": header["model_revision"],
            "encoder_id": header["encoder_id"],
            "knowledge_revision": header["knowledge_revision"],
            "passage_generation_id": header["passage_generation_id"],
            "passage_ids": passage_ids,
            "text_sha256": text_sha256,
            "vector_passage_ids": vector_passage_ids,
            "embeddings": embeddings,
        }


def _load_index_header(path: Path) -> dict[str, object]:
    with np.load(path, allow_pickle=False) as data:
        return _index_header(data)


def _index_header(data: Any) -> dict[str, object]:
    if "schema_version" not in data.files:
        raise ValueError("Unsupported vector index schema")
    schema_version = str(data["schema_version"].item())
    if schema_version == "3":
        raise _UnsupportedVectorIndexSchema("Unsupported vector index schema")
    if set(data.files) != _INDEX_FIELDS or schema_version != _SCHEMA_VERSION:
        raise ValueError("Unsupported vector index schema")
    knowledge_revision = int(data["knowledge_revision"].item())
    passage_count = int(data["passage_count"].item())
    dimensions = int(data["dimensions"].item())
    passage_generation_id = str(data["passage_generation_id"].item())
    model_name = str(data["model_name"].item())
    model_revision = str(data["model_revision"].item())
    encoder_id = str(data["encoder_id"].item())
    if (
        knowledge_revision < 0
        or passage_count <= 0
        or dimensions <= 0
        or not passage_generation_id
        or not model_name
        or not encoder_id
    ):
        raise ValueError("Invalid vector index metadata")
    if model_revision and encoder_id != _builtin_encoder_id(
        model_name, model_revision
    ):
        raise ValueError("Vector index encoder identity does not match its model")
    return {
        "knowledge_revision": knowledge_revision,
        "passage_generation_id": passage_generation_id,
        "passage_count": passage_count,
        "dimensions": dimensions,
        "model_name": model_name,
        "model_revision": model_revision,
        "encoder_id": encoder_id,
    }


def _encode(
    texts: list[str],
    encoder: Encoder | None,
    model_name: str,
    model_revision: str,
) -> np.ndarray:
    if encoder is not None:
        return np.asarray(encoder(texts), dtype=np.float32)
    model = _get_model(model_name, model_revision)
    return np.asarray(
        model.encode(texts, convert_to_numpy=True, show_progress_bar=False),
        dtype=np.float32,
    )


def _passage_chunks(
    passages: list[Passage],
    *,
    encoder: Encoder | None,
    model_name: str,
    model_revision: str,
) -> tuple[list[str], list[str]]:
    model = (
        None
        if encoder is not None
        else _get_model(model_name, model_revision)
    )
    texts: list[str] = []
    passage_ids: list[str] = []
    for passage in passages:
        chunks = (
            _character_chunks(passage.text)
            if model is None
            else _token_chunks(passage.text, model)
        )
        for chunk in chunks:
            texts.append(chunk)
            passage_ids.append(passage.passage_id)
    return texts, passage_ids


def _character_chunks(
    text: str, *, max_chars: int = 512, overlap_chars: int = 128
) -> list[str]:
    if len(text) <= max_chars:
        return [text]
    step = max_chars - overlap_chars
    return [text[start : start + max_chars] for start in range(0, len(text), step)]


def _token_chunks(text: str, model: object) -> list[str]:
    tokenizer = model.tokenizer
    max_tokens = int(model.max_seq_length) - int(
        tokenizer.num_special_tokens_to_add(pair=False)
    )
    if max_tokens <= 0:
        raise ValueError("Embedding model has an invalid token limit")
    token_ids = tokenizer.encode(
        text, add_special_tokens=False, truncation=False, verbose=False
    )
    if len(token_ids) <= max_tokens:
        return [text]
    overlap = min(32, max_tokens // 8)
    step = max_tokens - overlap
    chunks = [
        tokenizer.decode(
            token_ids[start : start + max_tokens],
            skip_special_tokens=True,
            clean_up_tokenization_spaces=False,
        ).strip()
        for start in range(0, len(token_ids), step)
    ]
    return [chunk for chunk in chunks if chunk]


def _get_model(model_name: str, model_revision: str) -> object:
    cache_key = (model_name, model_revision)
    model = _MODEL_CACHE.get(cache_key)
    if model is None:
        from sentence_transformers import SentenceTransformer

        model = SentenceTransformer(model_name, revision=model_revision)
        _MODEL_CACHE[cache_key] = model
    return model


def _build_encoder_identity(
    *,
    encoder: Encoder | None,
    encoder_id: str | None,
    model_name: str,
    model_revision: str | None,
) -> tuple[str, str]:
    if not _is_nonempty(model_name):
        raise ValueError("model_name must be non-empty")
    if encoder is not None:
        if not _is_nonempty(encoder_id):
            raise ValueError("A non-empty encoder_id is required for a custom encoder")
        return "", str(encoder_id)

    if model_revision is None:
        if model_name != DEFAULT_MODEL:
            raise ValueError(
                "model_revision is required for a non-default built-in model"
            )
        resolved_revision = DEFAULT_MODEL_REVISION
    elif not _is_nonempty(model_revision):
        raise ValueError("model_revision must be non-empty for a built-in model")
    else:
        resolved_revision = model_revision
    resolved_encoder_id = _builtin_encoder_id(model_name, resolved_revision)
    if encoder_id is not None and encoder_id != resolved_encoder_id:
        raise ValueError("encoder_id does not match the built-in model configuration")
    return resolved_revision, resolved_encoder_id


def _builtin_encoder_id(model_name: str, model_revision: str) -> str:
    return (
        f"{_ENCODER_PIPELINE}|model={model_name}|revision={model_revision}"
    )


def _validate_query_encoder(
    index: dict[str, Any],
    *,
    encoder: Encoder | None,
    encoder_id: str | None,
) -> None:
    indexed_encoder_id = str(index["encoder_id"])
    if encoder is not None:
        if index["model_revision"]:
            raise ValueError("A custom encoder cannot query a built-in vector index")
        if encoder_id != indexed_encoder_id:
            raise ValueError("encoder_id does not match the vector index")
        return

    model_revision = str(index["model_revision"])
    if not model_revision:
        raise ValueError("A custom encoder is required for this vector index")
    expected_encoder_id = _builtin_encoder_id(
        str(index["model_name"]), model_revision
    )
    if indexed_encoder_id != expected_encoder_id:
        raise ValueError("Vector index encoder_id does not match its model")
    if encoder_id is not None and encoder_id != expected_encoder_id:
        raise ValueError("encoder_id does not match the vector index")


def _is_nonempty(value: str | None) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _normalize_matrix(vectors: np.ndarray, *, expected_rows: int) -> np.ndarray:
    matrix = np.asarray(vectors, dtype=np.float32)
    if matrix.ndim != 2 or matrix.shape[0] != expected_rows or matrix.shape[1] == 0:
        raise ValueError("Encoder returned an invalid vector matrix")
    if not np.isfinite(matrix).all():
        raise ValueError("Encoder returned non-finite values")
    norms = np.linalg.norm(matrix, axis=1, keepdims=True)
    if np.any(norms == 0):
        raise ValueError("Encoder returned a zero vector")
    return np.asarray(matrix / norms, dtype=np.float32)


def _validate_passage_hashes(passages: list[Passage]) -> None:
    for passage in passages:
        actual = hashlib.sha256(passage.text.encode("utf-8")).hexdigest()
        if actual != passage.text_sha256:
            raise ValueError(
                f"Passage {passage.passage_id} text_sha256 does not match its text"
            )
