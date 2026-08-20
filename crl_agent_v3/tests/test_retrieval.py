from __future__ import annotations

import hashlib

import numpy as np
import pytest

import crl_v3.vector as vector_module
from crl_v3.knowledge import KnowledgeStore, Paper, Passage
from crl_v3.retrieval import hybrid_search
from crl_v3.vector import rebuild_vector_index, semantic_search


OFFLINE_ENCODER_ID = "tests:retrieval-encoder-v1"


def _sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _paper(paper_id: str, title: str) -> Paper:
    return Paper(
        paper_id=paper_id,
        title=title,
        year=2025,
        source="local",
        venue="Test Venue",
        publication_status="preprint",
        fulltext_path=f"{paper_id}.pdf",
        fulltext_sha256=_sha256(f"pdf:{paper_id}"),
    )


def _passage(
    passage_id: str, paper_id: str, section: str, text: str, page: int
) -> Passage:
    return Passage(
        passage_id=passage_id,
        paper_id=paper_id,
        section=section,
        page_start=page,
        page_end=page,
        char_start=20,
        char_end=20 + len(text),
        text=text,
        text_sha256=_sha256(text),
    )


def _encoder(texts: list[str]) -> np.ndarray:
    vectors = []
    for text in texts:
        value = text.casefold()
        if value.strip() == "keyword_only":
            vectors.append([1.0, 0.0, 0.0])
        elif any(term in value for term in ("cat", "feline", "kitten")):
            vectors.append([1.0, 0.0, 0.0])
        elif any(term in value for term in ("sqlite", "database", "keyword_only")):
            vectors.append([0.0, 1.0, 0.0])
        else:
            vectors.append([0.0, 0.0, 1.0])
    return np.asarray(vectors, dtype=np.float32)


def _store_with_two_passages(tmp_path) -> tuple[KnowledgeStore, object]:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    store.add_paper(
        _paper("paper-cat", "Feline Study"),
        [_passage("cat-1", "paper-cat", "Results", "A cat rests on a mat.", 3)],
    )
    store.add_paper(
        _paper("paper-db", "Storage Study"),
        [
            _passage(
                "db-1",
                "paper-db",
                "Methods",
                "keyword_only SQLite storage details.",
                8,
            )
        ],
    )
    index_path = tmp_path / "vectors.npz"
    rebuild_vector_index(
        store,
        index_path,
        encoder=_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )
    return store, index_path


def test_hybrid_recall_supports_keyword_semantic_and_dual_route_hits(tmp_path) -> None:
    store, index_path = _store_with_two_passages(tmp_path)

    keyword = hybrid_search(
        store,
        index_path,
        "keyword_only",
        limit=2,
        route_limit=1,
        encoder=_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
    )
    semantic = hybrid_search(
        store,
        index_path,
        "feline behavior",
        limit=1,
        route_limit=1,
        encoder=_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
    )
    dual = hybrid_search(
        store,
        index_path,
        "cat",
        limit=2,
        route_limit=2,
        encoder=_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
    )

    assert {hit.passage_id: hit.routes for hit in keyword.hits} == {
        "db-1": ("fts",),
        "cat-1": ("vector",),
    }
    assert [(hit.passage_id, hit.routes) for hit in semantic.hits] == [
        ("cat-1", ("vector",))
    ]
    assert dual.hits[0].passage_id == "cat-1"
    assert dual.hits[0].routes == ("fts", "vector")
    assert [hit.passage_id for hit in dual.hits].count("cat-1") == 1
    assert dual.hits[0].fused_score == pytest.approx(2 / 61)
    assert dual.hits[0].fts_score is not None
    assert dual.hits[0].vector_score == pytest.approx(1.0)
    store.close()


def test_hybrid_hit_preserves_authoritative_provenance(tmp_path) -> None:
    store, index_path = _store_with_two_passages(tmp_path)

    result = hybrid_search(
        store,
        index_path,
        "feline behavior",
        limit=1,
        encoder=_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
    )
    hit = result.hits[0]
    passage = store.get_passage("cat-1")
    paper = store.get_paper("paper-cat")

    assert passage is not None and paper is not None
    assert (
        hit.paper_id,
        hit.title,
        hit.section,
        hit.page_start,
        hit.page_end,
        hit.char_start,
        hit.char_end,
        hit.text,
        hit.fulltext_sha256,
        hit.text_sha256,
    ) == (
        paper.paper_id,
        paper.title,
        passage.section,
        passage.page_start,
        passage.page_end,
        passage.char_start,
        passage.char_end,
        passage.text,
        paper.fulltext_sha256,
        passage.text_sha256,
    )
    store.close()


def test_missing_or_stale_vector_index_degrades_to_fts_with_reason(tmp_path) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    paper = _paper("paper-db", "Storage Study")
    original = _passage(
        "db-1", "paper-db", "Methods", "SQLite keyword survives degradation.", 2
    )
    store.add_paper(paper, [original])
    index_path = tmp_path / "missing.npz"

    missing = hybrid_search(
        store,
        index_path,
        "SQLite",
        encoder=_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
    )
    assert [hit.passage_id for hit in missing.hits] == ["db-1"]
    assert missing.hits[0].routes == ("fts",)
    assert missing.degraded is True
    assert missing.degradation_reason == "index_missing"

    rebuild_vector_index(
        store,
        index_path,
        encoder=_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )
    changed = _passage(
        "db-1", "paper-db", "Methods", "SQLite keyword remains after change.", 4
    )
    store.add_paper(paper, [changed])
    stale = hybrid_search(
        store,
        index_path,
        "SQLite",
        encoder=_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
    )
    assert [hit.passage_id for hit in stale.hits] == ["db-1"]
    assert stale.degraded is True
    assert stale.degradation_reason == "passage_bindings_changed"
    store.close()


def test_temporary_vector_failure_degrades_to_fts_with_error(tmp_path) -> None:
    store, index_path = _store_with_two_passages(tmp_path)

    def unavailable_encoder(texts: list[str]) -> np.ndarray:
        raise RuntimeError("model temporarily unavailable")

    result = hybrid_search(
        store,
        index_path,
        "cat",
        limit=1,
        encoder=unavailable_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
    )

    assert [hit.passage_id for hit in result.hits] == ["cat-1"]
    assert result.hits[0].routes == ("fts",)
    assert result.degraded is True
    assert result.degradation_reason is not None
    assert result.degradation_reason.startswith("vector_search_failed:RuntimeError:")
    store.close()


@pytest.mark.parametrize("encoder_id", [None, "tests:wrong-encoder-v1"])
def test_custom_encoder_identity_failure_degrades_to_fts(tmp_path, encoder_id) -> None:
    store, index_path = _store_with_two_passages(tmp_path)

    result = hybrid_search(
        store,
        index_path,
        "cat",
        limit=1,
        encoder=_encoder,
        encoder_id=encoder_id,
    )

    assert [hit.passage_id for hit in result.hits] == ["cat-1"]
    assert result.hits[0].routes == ("fts",)
    assert result.degraded is True
    assert result.degradation_reason is not None
    assert result.degradation_reason.startswith("vector_search_failed:ValueError:")
    assert "encoder_id" in result.degradation_reason
    store.close()


def test_custom_encoder_impersonating_builtin_index_degrades_to_fts(
    tmp_path, monkeypatch
) -> None:
    class FakeTokenizer:
        def num_special_tokens_to_add(self, *, pair: bool) -> int:
            return 2

        def encode(self, text: str, **kwargs) -> list[int]:
            return list(range(min(len(text), 4)))

    class FakeBuiltinModel:
        max_seq_length = 32
        tokenizer = FakeTokenizer()

        def encode(self, texts: list[str], **kwargs) -> np.ndarray:
            return np.asarray(
                [[1.0, 0.0, 0.0] for _ in texts], dtype=np.float32
            )

    cache_key = (
        vector_module.DEFAULT_MODEL,
        vector_module.DEFAULT_MODEL_REVISION,
    )
    monkeypatch.setitem(vector_module._MODEL_CACHE, cache_key, FakeBuiltinModel())
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    index_path = tmp_path / "passages.npz"
    passage = _passage(
        "cat-1", "paper-cat", "Results", "A cat keyword remains available.", 1
    )
    store.add_paper(_paper("paper-cat", "Study"), [passage])
    rebuild_vector_index(store, index_path)
    builtin_encoder_id = str(
        vector_module.vector_index_status(store, index_path)["encoder_id"]
    )

    result = hybrid_search(
        store,
        index_path,
        "cat",
        encoder=_encoder,
        encoder_id=builtin_encoder_id,
    )

    assert [hit.passage_id for hit in result.hits] == ["cat-1"]
    assert result.hits[0].routes == ("fts",)
    assert result.degraded is True
    assert result.degradation_reason is not None
    assert result.degradation_reason.startswith("vector_search_failed:ValueError:")
    assert "built-in" in result.degradation_reason
    store.close()


def test_long_passage_tail_is_semantically_recalled_as_authoritative_passage(tmp_path) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    prefix = "neutral material " * 90
    long_text = prefix + "hidden_tail_concept reveals a rare mechanism"
    long_passage = _passage(
        "long-1", "paper-long", "Discussion", long_text, 11
    )
    other_passage = _passage(
        "other-1", "paper-other", "Background", "ordinary unrelated material", 1
    )
    store.add_paper(_paper("paper-long", "Long Study"), [long_passage])
    store.add_paper(_paper("paper-other", "Other Study"), [other_passage])
    index_path = tmp_path / "vectors.npz"

    def tail_encoder(texts: list[str]) -> np.ndarray:
        return np.asarray(
            [
                [1.0, 0.0]
                if "hidden_tail_concept" in text or "rare mechanism" in text
                else [0.0, 1.0]
                for text in texts
            ],
            dtype=np.float32,
        )

    rebuild_vector_index(
        store,
        index_path,
        encoder=tail_encoder,
        encoder_id="tests:tail-encoder-v1",
        model_name="offline-tail-encoder",
    )
    vector_hits = semantic_search(
        store,
        index_path,
        "rare mechanism",
        limit=1,
        encoder=tail_encoder,
        encoder_id="tests:tail-encoder-v1",
    )
    hybrid = hybrid_search(
        store,
        index_path,
        "rare mechanism",
        limit=1,
        encoder=tail_encoder,
        encoder_id="tests:tail-encoder-v1",
    )

    assert vector_hits[0].passage_id == "long-1"
    assert vector_hits[0].text == long_text
    assert vector_hits[0].text_sha256 == long_passage.text_sha256
    assert hybrid.hits[0].passage_id == "long-1"
    with np.load(index_path, allow_pickle=False) as data:
        assert data["vector_passage_ids"].tolist().count("long-1") > 1
    store.close()
