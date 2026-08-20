from __future__ import annotations

import hashlib
import shutil
import sys
from types import SimpleNamespace

import numpy as np
import pytest

import crl_v3.vector as vector_module
from crl_v3.knowledge import KnowledgeStore, Paper, Passage
from crl_v3.retrieval import hybrid_search
from crl_v3.vector import (
    rebuild_vector_index,
    semantic_search,
    vector_index_status,
)


OFFLINE_ENCODER_ID = "tests:offline-encoder-v1"


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
        fulltext_sha256=_sha256(f"fulltext:{paper_id}"),
    )


def _passage(passage_id: str, paper_id: str, section: str, text: str, page: int) -> Passage:
    return Passage(
        passage_id=passage_id,
        paper_id=paper_id,
        section=section,
        page_start=page,
        page_end=page,
        char_start=10,
        char_end=10 + len(text),
        text=text,
        text_sha256=_sha256(text),
    )


def _offline_encoder(texts: list[str]) -> np.ndarray:
    vectors = []
    for text in texts:
        value = text.casefold()
        if any(term in value for term in ("cat", "feline", "kitten")):
            vectors.append([1.0, 0.0, 0.0])
        elif any(term in value for term in ("database", "sqlite", "storage")):
            vectors.append([0.0, 1.0, 0.0])
        else:
            vectors.append([0.0, 0.0, 1.0])
    return np.asarray(vectors, dtype=np.float32)


def test_rebuild_and_semantic_search_preserve_passage_provenance(tmp_path) -> None:
    database = tmp_path / "knowledge.sqlite"
    index_path = tmp_path / "derived" / "passages.npz"
    store = KnowledgeStore(database, read_only=False)
    cat_paper = _paper("paper-cat", "Feline Study")
    db_paper = _paper("paper-db", "Storage Study")
    cat_passage = _passage(
        "cat-1", "paper-cat", "Results", "A feline rests quietly on the mat.", 3
    )
    db_passage = _passage(
        "db-1", "paper-db", "Methods", "SQLite stores durable research passages.", 7
    )
    store.add_paper(cat_paper, [cat_passage])
    store.add_paper(db_paper, [db_passage])

    built = rebuild_vector_index(
        store,
        index_path,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )
    hits = semantic_search(
        store,
        index_path,
        "a domestic cat",
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
    )

    assert built == {
        "index_path": str(index_path.resolve()),
        "model_name": "offline-test-encoder",
        "model_revision": "",
        "encoder_id": OFFLINE_ENCODER_ID,
        "dimensions": 3,
        "passages": 2,
    }
    assert index_path.is_file()
    assert [hit.passage_id for hit in hits] == ["cat-1", "db-1"]
    hit = hits[0]
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
        "paper-cat",
        "Feline Study",
        "Results",
        3,
        3,
        10,
        10 + len(cat_passage.text),
        cat_passage.text,
        cat_paper.fulltext_sha256,
        cat_passage.text_sha256,
    )
    assert hit.score == pytest.approx(1.0)
    assert vector_index_status(store, index_path)["ready"] is True
    store.close()


def test_vector_index_reloads_after_store_restart(tmp_path) -> None:
    database = tmp_path / "knowledge.sqlite"
    index_path = tmp_path / "passages.npz"
    store = KnowledgeStore(database, read_only=False)
    passage = _passage("cat-1", "paper-cat", "Results", "A kitten learns quickly.", 2)
    store.add_paper(_paper("paper-cat", "Persistent Feline Study"), [passage])
    rebuild_vector_index(
        store,
        index_path,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )
    store.close()

    reopened = KnowledgeStore(database, read_only=False)
    hits = semantic_search(
        reopened,
        index_path,
        "feline behavior",
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
    )
    assert [hit.passage_id for hit in hits] == ["cat-1"]
    assert hits[0].text == passage.text
    reopened.close()


def test_changed_passage_makes_index_stale_until_rebuilt(tmp_path) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    index_path = tmp_path / "passages.npz"
    paper = _paper("paper-a", "Changing Study")
    old = _passage("passage-a", "paper-a", "Old", "A feline observation.", 1)
    store.add_paper(paper, [old])
    rebuild_vector_index(
        store,
        index_path,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )

    new = _passage("passage-a", "paper-a", "New", "SQLite storage observation.", 4)
    store.add_paper(paper, [new])

    status = vector_index_status(store, index_path)
    assert status["ready"] is False
    assert status["reason"] == "passage_bindings_changed"
    with pytest.raises(ValueError, match="stale"):
        semantic_search(
            store,
            index_path,
            "database",
            encoder=_offline_encoder,
            encoder_id=OFFLINE_ENCODER_ID,
        )

    rebuild_vector_index(
        store,
        index_path,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )
    assert vector_index_status(store, index_path)["ready"] is True
    assert [hit.passage_id for hit in semantic_search(
        store,
        index_path,
        "database",
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
    )] == ["passage-a"]
    store.close()


def test_index_persists_passage_ids_hashes_and_uses_only_requested_path(tmp_path) -> None:
    index_path = tmp_path / "chosen" / "semantic.npz"
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    passage = _passage("passage-a", "paper-a", "Results", "A feline result.", 1)
    store.add_paper(_paper("paper-a", "Study"), [passage])

    rebuild_vector_index(
        store,
        index_path,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )

    with np.load(index_path, allow_pickle=False) as data:
        assert set(data.files) == {
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
        assert data["passage_ids"].tolist() == ["passage-a"]
        assert data["text_sha256"].tolist() == [passage.text_sha256]
        assert data["model_name"].item() == "offline-test-encoder"
        assert data["model_revision"].item() == ""
        assert data["encoder_id"].item() == OFFLINE_ENCODER_ID
        assert data["schema_version"].item() == "4"
        assert data["knowledge_revision"].item() == store.passage_revision()
        assert data["passage_generation_id"].item() == store.passage_identity()[1]
        assert data["embeddings"].shape == (1, 3)
        assert data["vector_passage_ids"].tolist() == ["passage-a"]
    assert list(tmp_path.rglob("*.npz")) == [index_path]
    store.close()


def test_failed_rebuild_does_not_replace_a_valid_index(tmp_path) -> None:
    index_path = tmp_path / "passages.npz"
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    passage = _passage("passage-a", "paper-a", "Results", "A feline result.", 1)
    store.add_paper(_paper("paper-a", "Study"), [passage])
    rebuild_vector_index(
        store,
        index_path,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )
    original = index_path.read_bytes()

    def failing_encoder(texts: list[str]) -> np.ndarray:
        raise RuntimeError("controlled encoding failure")

    with pytest.raises(RuntimeError, match="controlled encoding failure"):
        rebuild_vector_index(
            store,
            index_path,
            encoder=failing_encoder,
            encoder_id="tests:broken-encoder-v1",
            model_name="broken-encoder",
        )

    assert index_path.read_bytes() == original
    assert vector_index_status(store, index_path)["ready"] is True
    store.close()


def test_rebuild_rejects_incorrect_authoritative_text_hash(tmp_path) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    paper = _paper("paper-a", "Hash Study")
    passage = Passage(
        passage_id="passage-a",
        paper_id="paper-a",
        section="Results",
        page_start=1,
        page_end=1,
        char_start=0,
        char_end=4,
        text="real text",
        text_sha256="0" * 64,
    )
    store.add_paper(paper, [passage])

    with pytest.raises(ValueError, match="text_sha256"):
        rebuild_vector_index(
            store,
            tmp_path / "passages.npz",
            encoder=_offline_encoder,
            encoder_id=OFFLINE_ENCODER_ID,
            model_name="offline-test-encoder",
        )
    store.close()


def test_query_freshness_check_never_reads_or_rehashes_all_passages(
    tmp_path, monkeypatch
) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    index_path = tmp_path / "passages.npz"
    passage = _passage("cat-1", "paper-cat", "Results", "A feline result.", 1)
    store.add_paper(_paper("paper-cat", "Study"), [passage])
    rebuild_vector_index(
        store,
        index_path,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )

    def forbidden_full_read():
        raise AssertionError("query path must not read all passages")

    def forbidden_full_hash(passages):
        raise AssertionError("query path must not hash all passages")

    monkeypatch.setattr(store, "list_passages", forbidden_full_read)
    monkeypatch.setattr(vector_module, "_validate_passage_hashes", forbidden_full_hash)

    assert vector_index_status(store, index_path)["ready"] is True
    assert [
        hit.passage_id
        for hit in semantic_search(
            store,
            index_path,
            "feline",
            encoder=_offline_encoder,
            encoder_id=OFFLINE_ENCODER_ID,
        )
    ] == ["cat-1"]
    hybrid = hybrid_search(
        store,
        index_path,
        "feline",
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
    )
    assert [hit.passage_id for hit in hybrid.hits] == ["cat-1"]
    assert hybrid.degraded is False
    store.close()


def test_add_replace_delete_and_restart_invalidate_by_revision(tmp_path) -> None:
    database = tmp_path / "knowledge.sqlite"
    index_path = tmp_path / "passages.npz"
    store = KnowledgeStore(database, read_only=False)
    paper_a = _paper("paper-a", "Alpha")
    passage_a = _passage("a-1", "paper-a", "Results", "A feline result.", 1)
    store.add_paper(paper_a, [passage_a])
    rebuild_vector_index(
        store,
        index_path,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )

    paper_b = _paper("paper-b", "Beta")
    passage_b = _passage("b-1", "paper-b", "Methods", "SQLite storage.", 2)
    store.add_paper(paper_b, [passage_b])
    assert vector_index_status(store, index_path)["reason"] == "passage_bindings_changed"
    rebuild_vector_index(
        store,
        index_path,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )
    store.close()

    reopened = KnowledgeStore(database, read_only=False)
    assert vector_index_status(reopened, index_path)["ready"] is True
    replacement = _passage("a-2", "paper-a", "New", "A kitten replacement.", 3)
    reopened.add_paper(paper_a, [replacement])
    assert vector_index_status(reopened, index_path)["reason"] == "passage_bindings_changed"
    rebuild_vector_index(
        reopened,
        index_path,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )
    assert reopened.delete_paper("paper-b") is True
    assert vector_index_status(reopened, index_path)["reason"] == "passage_bindings_changed"
    reopened.close()

    restarted = KnowledgeStore(database, read_only=False)
    assert vector_index_status(restarted, index_path)["reason"] == "passage_bindings_changed"
    restarted.close()


def test_same_revision_from_independent_database_rejects_index(tmp_path) -> None:
    index_path = tmp_path / "passages.npz"
    passage = _passage("cat-1", "paper-cat", "Results", "A feline result.", 1)
    first = KnowledgeStore(tmp_path / "first.sqlite", read_only=False)
    first.add_paper(_paper("paper-cat", "Study"), [passage])
    rebuild_vector_index(
        first,
        index_path,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )

    second = KnowledgeStore(tmp_path / "second.sqlite", read_only=False)
    second.add_paper(_paper("paper-cat", "Study"), [passage])

    assert first.passage_revision() == second.passage_revision()
    assert first.passage_identity()[1] != second.passage_identity()[1]
    assert vector_index_status(second, index_path) == {
        "ready": False,
        "reason": "passage_bindings_changed",
        "index_path": str(index_path.resolve()),
    }
    first.close()
    second.close()


def test_closed_database_and_index_clone_reuses_until_clone_diverges(tmp_path) -> None:
    source = tmp_path / "source"
    clone = tmp_path / "clone"
    source.mkdir()
    clone.mkdir()
    source_database = source / "knowledge.sqlite"
    source_index = source / "passages.npz"
    store = KnowledgeStore(source_database, read_only=False)
    passage = _passage("cat-1", "paper-cat", "Results", "A feline result.", 1)
    paper = _paper("paper-cat", "Study")
    store.add_paper(paper, [passage])
    rebuild_vector_index(
        store,
        source_index,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )
    store.close()

    clone_database = clone / source_database.name
    clone_index = clone / source_index.name
    shutil.copy2(source_database, clone_database)
    shutil.copy2(source_index, clone_index)
    cloned = KnowledgeStore(clone_database, read_only=False)

    assert vector_index_status(cloned, clone_index)["ready"] is True
    assert [
        hit.passage_id
        for hit in semantic_search(
            cloned,
            clone_index,
            "feline",
            encoder=_offline_encoder,
            encoder_id=OFFLINE_ENCODER_ID,
        )
    ] == ["cat-1"]

    replacement = _passage(
        "cat-2", "paper-cat", "Results", "A kitten replacement.", 2
    )
    cloned.add_paper(paper, [replacement])
    assert vector_index_status(cloned, clone_index)["reason"] == "passage_bindings_changed"
    cloned.close()

    original = KnowledgeStore(source_database, read_only=False)
    assert vector_index_status(original, source_index)["ready"] is True
    original.close()


def test_schema_three_reports_explicit_reason_without_rewriting_file(tmp_path) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    index_path = tmp_path / "schema-three.npz"
    np.savez_compressed(index_path, schema_version=np.asarray("3"))
    original = index_path.read_bytes()

    status = vector_index_status(store, index_path)

    assert status == {
        "ready": False,
        "reason": "unsupported_vector_index_schema",
        "index_path": str(index_path.resolve()),
    }
    assert index_path.read_bytes() == original
    store.close()


def test_custom_encoder_requires_matching_caller_supplied_identity(tmp_path) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    index_path = tmp_path / "passages.npz"
    passage = _passage("cat-1", "paper-cat", "Results", "A feline result.", 1)
    store.add_paper(_paper("paper-cat", "Study"), [passage])

    with pytest.raises(ValueError, match="encoder_id"):
        rebuild_vector_index(
            store,
            index_path,
            encoder=_offline_encoder,
            model_name="offline-test-encoder",
        )

    rebuild_vector_index(
        store,
        index_path,
        encoder=_offline_encoder,
        encoder_id=OFFLINE_ENCODER_ID,
        model_name="offline-test-encoder",
    )
    with pytest.raises(ValueError, match="encoder_id"):
        semantic_search(store, index_path, "feline", encoder=_offline_encoder)
    with pytest.raises(ValueError, match="encoder_id"):
        semantic_search(
            store,
            index_path,
            "feline",
            encoder=_offline_encoder,
            encoder_id="tests:wrong-encoder-v1",
        )
    assert [
        hit.passage_id
        for hit in semantic_search(
            store,
            index_path,
            "feline",
            encoder=_offline_encoder,
            encoder_id=OFFLINE_ENCODER_ID,
        )
    ] == ["cat-1"]
    store.close()


def test_custom_encoder_cannot_impersonate_builtin_index(
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
    passage = _passage("cat-1", "paper-cat", "Results", "A feline result.", 1)
    store.add_paper(_paper("paper-cat", "Study"), [passage])
    rebuild_vector_index(store, index_path)
    builtin_encoder_id = str(vector_index_status(store, index_path)["encoder_id"])

    with pytest.raises(ValueError, match="built-in"):
        semantic_search(
            store,
            index_path,
            "feline",
            encoder=_offline_encoder,
            encoder_id=builtin_encoder_id,
        )
    store.close()


def test_default_model_revision_is_pinned_and_cache_keyed_by_revision(
    tmp_path, monkeypatch
) -> None:
    calls: list[tuple[str, str]] = []

    class FakeTokenizer:
        def num_special_tokens_to_add(self, *, pair: bool) -> int:
            assert pair is False
            return 2

        def encode(self, text: str, **kwargs) -> list[int]:
            return list(range(min(len(text), 4)))

    class FakeSentenceTransformer:
        max_seq_length = 32
        tokenizer = FakeTokenizer()

        def __init__(self, model_name: str, *, revision: str) -> None:
            calls.append((model_name, revision))

        def encode(self, texts: list[str], **kwargs) -> np.ndarray:
            return np.asarray([[1.0, 0.0] for _ in texts], dtype=np.float32)

    monkeypatch.setitem(
        sys.modules,
        "sentence_transformers",
        SimpleNamespace(SentenceTransformer=FakeSentenceTransformer),
    )
    vector_module._MODEL_CACHE.clear()
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    index_path = tmp_path / "passages.npz"
    passage = _passage("cat-1", "paper-cat", "Results", "A feline result.", 1)
    store.add_paper(_paper("paper-cat", "Study"), [passage])

    rebuild_vector_index(store, index_path)
    vector_module._MODEL_CACHE.clear()
    semantic_search(store, index_path, "feline")

    expected = (
        vector_module.DEFAULT_MODEL,
        "1110a243fdf4706b3f48f1d95db1a4f5529b4d41",
    )
    assert vector_module.DEFAULT_MODEL_REVISION == expected[1]
    assert calls == [expected, expected]
    assert set(vector_module._MODEL_CACHE) == {expected}
    with np.load(index_path, allow_pickle=False) as data:
        assert data["model_revision"].item() == expected[1]
        encoder_id = str(data["encoder_id"].item())
        assert "crl-encode-v1" in encoder_id
        assert expected[0] in encoder_id
        assert expected[1] in encoder_id
    store.close()


def test_non_default_builtin_model_requires_explicit_revision(tmp_path) -> None:
    store = KnowledgeStore(tmp_path / "knowledge.sqlite", read_only=False)
    passage = _passage("cat-1", "paper-cat", "Results", "A feline result.", 1)
    store.add_paper(_paper("paper-cat", "Study"), [passage])

    with pytest.raises(ValueError, match="model_revision"):
        rebuild_vector_index(
            store,
            tmp_path / "passages.npz",
            model_name="sentence-transformers/another-model",
        )
    store.close()
