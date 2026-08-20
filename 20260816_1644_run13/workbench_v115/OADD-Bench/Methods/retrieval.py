from __future__ import annotations

import hashlib
import json
import os
import pickle
import re
import sqlite3
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable


WAVE_PREFIX_YEAR = {
    "H": "2002",
    "J": "2004",
    "K": "2006",
    "L": "2008",
    "M": "2010",
    "N": "2012",
    "O": "2014",
    "P": "2016",
    "Q": "2018",
    "R": "2020",
    "S": "2022",
}
COGNITION_WAVE_PREFIX = {
    6: "H",
    7: "J",
    8: "K",
    9: "L",
    10: "M",
    11: "N",
    12: "O",
    13: "P",
    14: "Q",
    15: "R",
    16: "S",
}
DENSE_MODEL = "BAAI/bge-base-en-v1.5"
SPARSE_MODEL = "prithivida/Splade_PP_en_v1"
DENSE_DIMENSIONS = 768
SPARSE_DIMENSIONS = 30_522
RRF_CONSTANT = 60


def normalize_code(code: str) -> str:
    return re.sub(r"\s+", "", str(code)).upper()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_jsonl(path: Path) -> Iterable[dict[str, Any]]:
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.strip():
                yield json.loads(line)


def compact_text(record: dict[str, Any]) -> str:
    parts = [
        record.get("variable_code", ""),
        record.get("variable_label", ""),
        record.get("variable_label", ""),
        record.get("question_text", ""),
        record.get("question_text", ""),
        record.get("value_labels", ""),
        record.get("section_title", ""),
        record.get("product_title", ""),
        record.get("ref", ""),
    ]
    return "\n".join(str(part)[:1800] for part in parts if part)


def wave_year_from_code(code: str) -> str:
    match = re.match(r"^[RS](\d{1,2})(?=[A-Z_])", normalize_code(code))
    if not match:
        return ""
    wave = int(match.group(1))
    return str(1990 + 2 * wave) if 1 <= wave <= 30 else ""


def family_key(record: dict[str, Any]) -> str:
    code = normalize_code(record.get("variable_code", ""))
    product_family = str(record.get("product_family", ""))
    year = str(record.get("year", ""))
    if (
        product_family in {"core", "exit"}
        and len(code) >= 3
        and code[0] in WAVE_PREFIX_YEAR
        and WAVE_PREFIX_YEAR[code[0]] == year
    ):
        label = str(record.get("variable_label", "")).upper()
        label = re.sub(r"^\s*Q?\d+[A-Z]?(?:_[A-Z0-9]+)?[.:]\s*", "", label)
        label = label.replace("#", " NUM ")
        tokens = [
            token
            for token in re.findall(r"[A-Z0-9]+", label)
            if token not in {"WAY", "YOU", "FEEL", "SERIOUS"}
        ]
        semantic = "L-" + "-".join(tokens[:16])
        if len(semantic) >= 5:
            return f"HRS::{product_family}::{record.get('section', '')}::label::{semantic}"
        return f"HRS::{product_family}::{record.get('section', '')}::code::{code[1:]}"
    if product_family == "cognition":
        match = re.match(r"^([RS])(\d+)(.+)$", code)
        if match:
            suffix = re.sub(r"[PW]$", "", match.group(3))
            return f"HRS::cognition::{match.group(1).lower()}::{suffix.lower()}"
    return f"HRS::{record.get('product_key', '')}::{record.get('section', '')}::{code}"


def build_families(metadata: Path, fixes: Path | None) -> list[dict[str, Any]]:
    groups: dict[str, dict[str, Any]] = {}
    paths = [metadata] + ([fixes] if fixes and fixes.exists() else [])
    for path in paths:
        for record in read_jsonl(path):
            code = str(record.get("variable_code", "")).strip()
            if not code:
                continue
            key = family_key(record)
            group = groups.setdefault(
                key,
                {
                    "family_id": key,
                    "ids": [],
                    "years": [],
                    "label": str(record.get("variable_label", "")),
                    "text": "",
                    "product_family": str(record.get("product_family", "")),
                    "product_title": str(record.get("product_title", "")),
                    "_seen_ids": set(),
                },
            )
            normalized = normalize_code(code)
            if normalized not in group["_seen_ids"]:
                group["_seen_ids"].add(normalized)
                group["ids"].append(code)
                group["years"].append(
                    wave_year_from_code(code)
                    if str(record.get("product_family", "")) == "cognition"
                    else str(record.get("year", ""))
                )
            if not group["text"]:
                group["text"] = compact_text(record)

    families: list[dict[str, Any]] = []
    for group in groups.values():
        group.pop("_seen_ids")
        paired = sorted(
            zip(group["years"], group["ids"], strict=True),
            key=lambda item: (
                int(item[0]) if str(item[0]).isdigit() else 99999,
                item[0],
                item[1],
            ),
        )
        group["years"] = [year for year, _ in paired]
        group["ids"] = [code for _, code in paired]
        families.append(group)
    families.sort(key=lambda row: row["family_id"])
    return families


def family_fingerprint(families: list[dict[str, Any]]) -> str:
    digest = hashlib.sha256()
    for family in families:
        payload = {
            key: family[key]
            for key in ("family_id", "ids", "years", "label", "text", "product_title")
        }
        digest.update(
            json.dumps(
                payload,
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            ).encode("utf-8")
        )
        digest.update(b"\n")
    return digest.hexdigest()


def load_or_build_families(
    metadata: Path,
    fixes: Path | None,
    cache_dir: Path,
) -> tuple[list[dict[str, Any]], str]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / "families.pkl"
    identity = {
        "metadata": sha256_file(metadata),
        "fixes": sha256_file(fixes) if fixes and fixes.exists() else None,
        "version": "hrs_family_v2",
    }
    if cache_path.exists():
        with cache_path.open("rb") as handle:
            cached = pickle.load(handle)
        if cached.get("identity") == identity:
            return cached["families"], cached["fingerprint"]
    families = build_families(metadata, fixes)
    fingerprint = family_fingerprint(families)
    with cache_path.open("wb") as handle:
        pickle.dump(
            {"identity": identity, "families": families, "fingerprint": fingerprint},
            handle,
        )
    return families, fingerprint


def family_document(family: dict[str, Any]) -> str:
    return "\n".join(
        [
            "Identifiers: " + " ".join(family["ids"]),
            "Variable label: " + family["label"],
            "Codebook evidence: " + family["text"][:500],
            "Product: " + family["product_title"],
        ]
    )


class RetrievalIndex:
    def __init__(
        self,
        families: list[dict[str, Any]],
        fingerprint: str,
        cache_dir: Path,
        provider: str = "cpu",
    ) -> None:
        self.families = families
        self.fingerprint = fingerprint
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.provider = provider
        self.index_by_family = {
            family["family_id"]: index for index, family in enumerate(families)
        }

    def _providers(self) -> list[str]:
        if self.provider == "cuda":
            import onnxruntime as ort

            if hasattr(ort, "preload_dlls"):
                ort.preload_dlls(directory="")
            if "CUDAExecutionProvider" not in ort.get_available_providers():
                raise RuntimeError("CUDAExecutionProvider is unavailable")
            return ["CUDAExecutionProvider"]
        return ["CPUExecutionProvider"]

    @staticmethod
    def _fts_query(query: str) -> str:
        stop = {
            "the",
            "and",
            "with",
            "from",
            "into",
            "among",
            "using",
            "study",
            "health",
            "older",
            "adults",
            "could",
            "might",
        }
        tokens = re.findall(r"[A-Za-z0-9_+-]{2,}", query.lower())
        selected = [token.replace('"', "") for token in tokens if token not in stop]
        return " OR ".join(f'"{token}"' for token in selected[:40])

    def _build_fts(self) -> sqlite3.Connection:
        path = self.cache_dir / "catalog_fts.sqlite"
        meta_path = self.cache_dir / "catalog_fts.json"
        valid = False
        if path.exists() and meta_path.exists():
            valid = json.loads(meta_path.read_text()).get("fingerprint") == self.fingerprint
        if not valid:
            if path.exists():
                path.unlink()
            connection = sqlite3.connect(path)
            connection.execute(
                "CREATE VIRTUAL TABLE families_fts USING fts5("
                "family_id UNINDEXED, code, label, text, product)"
            )
            connection.executemany(
                "INSERT INTO families_fts(family_id, code, label, text, product) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    (
                        family["family_id"],
                        " ".join(family["ids"]),
                        family["label"],
                        family["text"],
                        family["product_title"],
                    )
                    for family in self.families
                ),
            )
            connection.commit()
            meta_path.write_text(
                json.dumps({"fingerprint": self.fingerprint}) + "\n",
                encoding="utf-8",
            )
            return connection
        return sqlite3.connect(path)

    def bm25(self, questions: list[str], top_k: int) -> list[list[int]]:
        connection = self._build_fts()
        rankings: list[list[int]] = []
        for question in questions:
            expression = self._fts_query(question)
            if not expression:
                rankings.append([])
                continue
            rows = connection.execute(
                "SELECT family_id FROM families_fts WHERE families_fts MATCH ? "
                "ORDER BY bm25(families_fts, 0.0, 2.0, 3.0, 1.5, 0.5) LIMIT ?",
                (expression, top_k),
            ).fetchall()
            rankings.append([self.index_by_family[row[0]] for row in rows])
        connection.close()
        return rankings

    def tfidf(self, questions: list[str], top_k: int) -> list[list[int]]:
        import numpy as np
        from sklearn.feature_extraction.text import TfidfVectorizer

        path = self.cache_dir / "tfidf.pkl"
        if path.exists():
            with path.open("rb") as handle:
                cached = pickle.load(handle)
        else:
            cached = {}
        if cached.get("fingerprint") == self.fingerprint:
            vectorizer, matrix = cached["vectorizer"], cached["matrix"]
        else:
            documents = [
                "\n".join(
                    [
                        " ".join(family["ids"]),
                        family["label"],
                        family["label"],
                        family["text"],
                        family["product_title"],
                    ]
                )
                for family in self.families
            ]
            vectorizer = TfidfVectorizer(
                lowercase=True,
                ngram_range=(1, 2),
                min_df=2,
                max_df=0.98,
                sublinear_tf=True,
                max_features=180_000,
                dtype=np.float32,
            )
            matrix = vectorizer.fit_transform(documents).tocsr()
            with path.open("wb") as handle:
                pickle.dump(
                    {"fingerprint": self.fingerprint, "vectorizer": vectorizer, "matrix": matrix},
                    handle,
                )
        query_matrix = vectorizer.transform(questions)
        rankings: list[list[int]] = []
        for row in range(len(questions)):
            scores = (matrix @ query_matrix.getrow(row).T).toarray().ravel()
            if not np.any(scores):
                rankings.append([])
                continue
            count = min(top_k, len(scores))
            indices = np.argpartition(scores, -count)[-count:]
            indices = indices[np.argsort(scores[indices])[::-1]]
            rankings.append([int(index) for index in indices])
        return rankings

    def _dense_paths(self) -> tuple[Path, Path, Path]:
        return (
            self.cache_dir / "bge_base_vectors.npy",
            self.cache_dir / "bge_base_vectors.partial.npy",
            self.cache_dir / "bge_base_vectors.meta.json",
        )

    def _build_dense(self) -> Path:
        import numpy as np
        from fastembed import TextEmbedding

        final, partial, meta_path = self._dense_paths()
        if final.exists() and meta_path.exists():
            meta = json.loads(meta_path.read_text())
            cached_fingerprint = meta.get("fingerprint", meta.get("catalog_fingerprint"))
            if cached_fingerprint == self.fingerprint and meta.get("model") == DENSE_MODEL:
                return final
        model = TextEmbedding(
            model_name=DENSE_MODEL,
            cache_dir=str(self.cache_dir / "models"),
            providers=self._providers(),
        )
        vectors = np.lib.format.open_memmap(
            partial,
            mode="w+",
            dtype=np.float32,
            shape=(len(self.families), DENSE_DIMENSIONS),
        )
        for start in range(0, len(self.families), 1024):
            stop = min(start + 1024, len(self.families))
            chunk = np.asarray(
                list(
                    model.passage_embed(
                        [family_document(row) for row in self.families[start:stop]],
                        batch_size=128,
                    )
                ),
                dtype=np.float32,
            )
            chunk /= np.maximum(np.linalg.norm(chunk, axis=1, keepdims=True), 1e-12)
            vectors[start:stop] = chunk
            vectors.flush()
            print(json.dumps({"stage": "bge_index", "completed": stop, "total": len(self.families)}), flush=True)
        del vectors
        os.replace(partial, final)
        meta_path.write_text(
            json.dumps({"fingerprint": self.fingerprint, "model": DENSE_MODEL}) + "\n",
            encoding="utf-8",
        )
        return final

    @staticmethod
    def _top_indices(scores: Any, top_k: int) -> list[int]:
        import numpy as np

        count = min(top_k, len(scores))
        if not count:
            return []
        indices = np.argpartition(scores, -count)[-count:]
        indices = indices[np.argsort(scores[indices])[::-1]]
        return [int(index) for index in indices]

    def bge(self, questions: list[str], top_k: int) -> list[list[int]]:
        import numpy as np
        from fastembed import TextEmbedding

        documents = np.load(self._build_dense(), mmap_mode="r")
        model = TextEmbedding(
            model_name=DENSE_MODEL,
            cache_dir=str(self.cache_dir / "models"),
            providers=self._providers(),
        )
        queries = np.asarray(
            list(model.query_embed(questions, batch_size=min(64, len(questions)))),
            dtype=np.float32,
        )
        queries /= np.maximum(np.linalg.norm(queries, axis=1, keepdims=True), 1e-12)
        return [self._top_indices(np.asarray(documents @ query), top_k) for query in queries]

    def _sparse_paths(self) -> tuple[Path, Path, Path]:
        return (
            self.cache_dir / "splade_matrix.npz",
            self.cache_dir / "splade_matrix.meta.json",
            self.cache_dir / f"splade_chunks_{self.fingerprint[:12]}",
        )

    @staticmethod
    def _sparse_matrix(embeddings: Iterable[Any], rows: int) -> Any:
        import numpy as np
        from scipy import sparse

        indices: list[int] = []
        values: list[float] = []
        indptr = [0]
        for embedding in embeddings:
            indices.extend(int(value) for value in embedding.indices)
            values.extend(float(value) for value in embedding.values)
            indptr.append(len(indices))
        if len(indptr) != rows + 1:
            raise RuntimeError("Sparse encoder returned an unexpected row count")
        return sparse.csr_matrix(
            (
                np.asarray(values, dtype=np.float32),
                np.asarray(indices, dtype=np.int32),
                np.asarray(indptr, dtype=np.int64),
            ),
            shape=(rows, SPARSE_DIMENSIONS),
            dtype=np.float32,
        )

    def _build_sparse(self) -> Path:
        from fastembed import SparseTextEmbedding
        from scipy import sparse

        final, meta_path, chunks = self._sparse_paths()
        if final.exists() and meta_path.exists():
            meta = json.loads(meta_path.read_text())
            cached_fingerprint = meta.get("fingerprint", meta.get("catalog_fingerprint"))
            if cached_fingerprint == self.fingerprint and meta.get("model") == SPARSE_MODEL:
                return final
        chunks.mkdir(parents=True, exist_ok=True)
        model = SparseTextEmbedding(
            model_name=SPARSE_MODEL,
            cache_dir=str(self.cache_dir / "models"),
            providers=self._providers(),
        )
        matrices = []
        for start in range(0, len(self.families), 1024):
            stop = min(start + 1024, len(self.families))
            chunk_path = chunks / f"{start:06d}_{stop:06d}.npz"
            if chunk_path.exists():
                matrix = sparse.load_npz(chunk_path).tocsr()
            else:
                matrix = self._sparse_matrix(
                    model.passage_embed(
                        [family_document(row) for row in self.families[start:stop]],
                        batch_size=64,
                    ),
                    stop - start,
                )
                temporary = chunk_path.with_suffix(".partial.npz")
                sparse.save_npz(temporary, matrix, compressed=True)
                os.replace(temporary, chunk_path)
            matrices.append(matrix)
            print(json.dumps({"stage": "splade_index", "completed": stop, "total": len(self.families)}), flush=True)
        full = sparse.vstack(matrices, format="csr")
        temporary = final.with_suffix(".partial.npz")
        sparse.save_npz(temporary, full, compressed=True)
        os.replace(temporary, final)
        meta_path.write_text(
            json.dumps({"fingerprint": self.fingerprint, "model": SPARSE_MODEL}) + "\n",
            encoding="utf-8",
        )
        return final

    def splade(self, questions: list[str], top_k: int) -> list[list[int]]:
        from fastembed import SparseTextEmbedding
        from scipy import sparse

        documents = sparse.load_npz(self._build_sparse()).tocsr()
        model = SparseTextEmbedding(
            model_name=SPARSE_MODEL,
            cache_dir=str(self.cache_dir / "models"),
            providers=self._providers(),
        )
        queries = self._sparse_matrix(
            model.query_embed(questions, batch_size=min(64, len(questions))),
            len(questions),
        )
        rankings: list[list[int]] = []
        for row in range(len(questions)):
            scores = (documents @ queries.getrow(row).transpose()).toarray().ravel()
            rankings.append(self._top_indices(scores, top_k))
        return rankings


def reciprocal_rank_fusion(rankings: Iterable[list[int]], top_k: int) -> list[int]:
    scores: dict[int, float] = defaultdict(float)
    for ranking in rankings:
        for rank, index in enumerate(ranking, start=1):
            scores[index] += 1.0 / (RRF_CONSTANT + rank)
    return [
        index
        for index, _ in sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:top_k]
    ]


def cognition_inputs(code: str) -> list[str]:
    match = re.fullmatch(
        r"R(?P<wave>\d+)(?P<measure>COGTOT|COG27|IMRC|DLRC|SER7|BWC20)(?P<mode>P|W)?",
        normalize_code(code),
    )
    if not match:
        return []
    wave = int(match.group("wave"))
    prefix = COGNITION_WAVE_PREFIX.get(wave)
    if not prefix:
        return []
    stem = f"{prefix}D"
    measure, mode = match.group("measure"), match.group("mode")
    if measure == "IMRC":
        return [f"{stem}174W" if mode == "W" and wave >= 14 else f"{stem}174"]
    if measure == "DLRC":
        return [f"{stem}184W" if mode == "W" and wave >= 14 else f"{stem}184"]
    if measure == "SER7":
        return [f"{stem}{number}" for number in range(142, 147)]
    if measure == "BWC20":
        return [f"{stem}124", f"{stem}129"]
    if measure == "COG27":
        values = [
            f"{stem}124",
            f"{stem}129",
            *(f"{stem}{number}" for number in range(142, 147)),
            f"{stem}174",
            f"{stem}184",
        ]
        if wave >= 14:
            values.extend([f"{stem}174W", f"{stem}184W"])
        return values
    return [
        f"{stem}124",
        f"{stem}129",
        *(f"{stem}{number}" for number in range(142, 147)),
        *(f"{stem}{number}" for number in range(151, 159)),
        f"{stem}174",
        f"{stem}184",
    ]


def ranking_to_columns(
    ranking: list[int],
    families: list[dict[str, Any]],
    allowed_years: set[str],
    limit: int,
) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for index in ranking:
        family = families[index]
        for year, code in zip(family["years"], family["ids"], strict=True):
            if allowed_years and year and year not in allowed_years:
                continue
            for value in cognition_inputs(code) or [normalize_code(code)]:
                if value in seen:
                    continue
                seen.add(value)
                output.append(value)
                if len(output) >= limit:
                    return output
    return output
