from __future__ import annotations

import json
import os
import pickle
from pathlib import Path
from typing import Any, Iterable

from retrieval import (
    DENSE_DIMENSIONS,
    DENSE_MODEL,
    cognition_inputs,
    normalize_code,
    read_jsonl,
    sha256_file,
)


def _quality(record: dict[str, Any]) -> tuple[int, int, int]:
    return (
        bool(str(record.get("question_text", "")).strip()),
        bool(str(record.get("variable_label", "")).strip()),
        len(str(record.get("question_text", ""))),
    )


def load_or_build_schema(
    metadata: Path,
    fixes: Path | None,
    cache_dir: Path,
) -> tuple[list[dict[str, str]], str]:
    cache_dir.mkdir(parents=True, exist_ok=True)
    cache_path = cache_dir / "schema_records.pkl"
    identity = {
        "metadata": sha256_file(metadata),
        "fixes": sha256_file(fixes) if fixes and fixes.exists() else None,
        "version": "hrs_product_table_exact_column_v1",
    }
    if cache_path.exists():
        with cache_path.open("rb") as handle:
            cached = pickle.load(handle)
        if cached.get("identity") == identity:
            return cached["rows"], cached["fingerprint"]

    occurrences: dict[tuple[str, str], dict[str, Any]] = {}
    paths = [metadata] + ([fixes] if fixes and fixes.exists() else [])
    for path in paths:
        for raw in read_jsonl(path):
            code = normalize_code(raw.get("variable_code", ""))
            if not code:
                continue
            table_key = str(raw.get("product_key", "")).strip()
            if not table_key:
                table_key = str(raw.get("product_title", "")).strip()
            if not table_key:
                table_key = str(raw.get("section_title", "")).strip()
            key = (table_key, code)
            prior = occurrences.get(key)
            if prior is None or _quality(raw) > _quality(prior):
                occurrences[key] = raw

    rows = []
    for (table_key, code), raw in sorted(occurrences.items()):
        rows.append(
            {
                "schema_id": f"{table_key}.{code}",
                "table_key": table_key,
                "table_name": str(raw.get("product_title", "")).strip() or table_key,
                "column_code": code,
                "label": str(raw.get("variable_label", "")).strip(),
                "description": str(raw.get("question_text", "")).strip()[:1200],
                "year": str(raw.get("year", "")).strip(),
                "product_family": str(raw.get("product_family", "")).strip(),
            }
        )
    fingerprint = _schema_fingerprint(rows)
    with cache_path.open("wb") as handle:
        pickle.dump(
            {"identity": identity, "rows": rows, "fingerprint": fingerprint},
            handle,
        )
    return rows, fingerprint


def _schema_fingerprint(rows: list[dict[str, str]]) -> str:
    import hashlib

    digest = hashlib.sha256()
    for row in rows:
        digest.update(
            json.dumps(row, sort_keys=True, separators=(",", ":")).encode("utf-8")
        )
        digest.update(b"\n")
    return digest.hexdigest()


def schema_document(row: dict[str, str]) -> str:
    return "\n".join(
        [
            f"Table: {row['table_name']}",
            f"Column: {row['column_code']}",
            f"Label: {row['label']}",
            f"Description: {row['description']}",
        ]
    )


def providers(name: str) -> list[str]:
    if name == "cuda":
        import onnxruntime as ort

        if hasattr(ort, "preload_dlls"):
            ort.preload_dlls(directory="")
        if "CUDAExecutionProvider" not in ort.get_available_providers():
            raise RuntimeError("CUDAExecutionProvider is unavailable")
        return ["CUDAExecutionProvider"]
    return ["CPUExecutionProvider"]


def build_schema_vectors(
    rows: list[dict[str, str]],
    fingerprint: str,
    cache_dir: Path,
    provider: str,
) -> Path:
    import numpy as np
    from fastembed import TextEmbedding

    path = cache_dir / "schema_vectors.npy"
    partial = cache_dir / "schema_vectors.partial.npy"
    progress_path = cache_dir / "schema_vectors.progress.json"
    meta_path = cache_dir / "schema_vectors.meta.json"
    identity = {"fingerprint": fingerprint, "model": DENSE_MODEL}
    if path.exists() and meta_path.exists():
        meta = json.loads(meta_path.read_text())
        if all(meta.get(key) == value for key, value in identity.items()):
            return path

    completed = 0
    if partial.exists() and progress_path.exists():
        progress = json.loads(progress_path.read_text())
        if all(progress.get(key) == value for key, value in identity.items()):
            completed = int(progress["completed"])
    mode = "r+" if completed else "w+"
    vectors = np.lib.format.open_memmap(
        partial,
        mode=mode,
        dtype=np.float32,
        shape=(len(rows), DENSE_DIMENSIONS),
    )
    model = TextEmbedding(
        model_name=DENSE_MODEL,
        cache_dir=str(cache_dir / "models"),
        providers=providers(provider),
    )
    for start in range(completed, len(rows), 1024):
        stop = min(start + 1024, len(rows))
        chunk = np.asarray(
            list(
                model.passage_embed(
                    [schema_document(row) for row in rows[start:stop]],
                    batch_size=128,
                )
            ),
            dtype=np.float32,
        )
        chunk /= np.maximum(np.linalg.norm(chunk, axis=1, keepdims=True), 1e-12)
        vectors[start:stop] = chunk
        vectors.flush()
        progress_path.write_text(
            json.dumps({**identity, "completed": stop}) + "\n", encoding="utf-8"
        )
        print(
            json.dumps({"stage": "schema_index", "completed": stop, "total": len(rows)}),
            flush=True,
        )
    del vectors
    os.replace(partial, path)
    progress_path.unlink(missing_ok=True)
    meta_path.write_text(json.dumps(identity) + "\n", encoding="utf-8")
    return path


def year_is_permitted(record_year: str, allowed_years: Iterable[str]) -> bool:
    allowed = {int(year) for year in allowed_years if str(year).isdigit()}
    if not allowed or not record_year:
        return True
    if record_year.isdigit():
        return int(record_year) in allowed
    endpoints = [
        int(value)
        for value in record_year.replace("–", "-").split("-")
        if value.isdigit()
    ]
    if len(endpoints) == 2:
        return any(endpoints[0] <= year <= endpoints[1] for year in allowed)
    return True


class DenseSchemaRetriever:
    def __init__(
        self,
        rows: list[dict[str, str]],
        vectors_path: Path,
        cache_dir: Path,
        provider: str,
    ) -> None:
        import numpy as np
        from fastembed import TextEmbedding

        self.rows = rows
        self.vectors = np.load(vectors_path, mmap_mode="r")
        self.model = TextEmbedding(
            model_name=DENSE_MODEL,
            cache_dir=str(cache_dir / "models"),
            providers=providers(provider),
        )

    def search(self, question: str, years: set[str], k: int) -> list[int]:
        import numpy as np

        query = np.asarray(
            list(self.model.query_embed([question], batch_size=1))[0],
            dtype=np.float32,
        )
        query /= max(float(np.linalg.norm(query)), 1e-12)
        scores = np.asarray(self.vectors @ query)
        permitted = np.asarray(
            [year_is_permitted(row["year"], years) for row in self.rows],
            dtype=bool,
        )
        scores[~permitted] = -np.inf
        count = min(k, int(permitted.sum()))
        if not count:
            return []
        positions = np.argpartition(scores, -count)[-count:]
        positions = positions[np.argsort(scores[positions])[::-1]]
        return [int(position) for position in positions]


def unique_codes(
    sequences: Iterable[Iterable[int]],
    rows: list[dict[str, str]],
    limit: int,
) -> list[str]:
    output: list[str] = []
    seen: set[str] = set()
    for sequence in sequences:
        for index in sequence:
            code = rows[int(index)]["column_code"]
            for value in cognition_inputs(code) or [code]:
                normalized = normalize_code(value)
                if normalized and normalized not in seen:
                    seen.add(normalized)
                    output.append(normalized)
                    if len(output) >= limit:
                        return output
    return output
