from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Iterable, Iterator, Mapping, Optional, Union

from .audit import QueryRecord

ALIASES = {
    "N": ["N", "n", "pool_size", "corpus_size", "num_candidates",
          "total_tools", "total_docs", "total"],
    "K": ["K", "k", "depth", "top_k", "topk", "num_shown",
          "num_retrieved", "shortlist_size"],
    "hit": ["hit", "success", "found", "solved", "contains_relevant",
            "task_success", "label"],
    "R": ["R", "r", "relevant", "num_relevant", "n_relevant",
          "relevant_count"],
    "qid": ["qid", "query_id", "id", "request_id", "trace_id"],
}

_TRUE = {"true", "1", "yes", "y", "t", "hit", "success"}


def _resolve(row: Mapping, key: str, mapping: Optional[Mapping[str, str]]):
    if mapping and key in mapping:
        return row.get(mapping[key])
    for alias in ALIASES[key]:
        if alias in row:
            return row[alias]
    return None


def _to_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return value > 0
    return str(value).strip().lower() in _TRUE


def _rows_to_records(
    rows: Iterable[Mapping],
    mapping: Optional[Mapping[str, str]],
    default_R: Optional[int],
    R_frac: Optional[float],
    strict: bool,
) -> Iterator[QueryRecord]:
    for i, row in enumerate(rows):
        N = _resolve(row, "N", mapping)
        K = _resolve(row, "K", mapping)
        hit = _resolve(row, "hit", mapping)
        if N is None or K is None or hit is None:
            if strict:
                missing = [
                    name for name, v in (("N", N), ("K", K), ("hit", hit))
                    if v is None
                ]
                raise ValueError(
                    f"Row {i}: missing field(s) {missing}; "
                    f"keys present: {sorted(row.keys())}."
                )
            continue
        N, K = int(N), int(K)
        K = min(K, N)

        R = _resolve(row, "R", mapping)
        if R is not None:
            R = int(R)
        elif default_R is not None:
            R = default_R
        elif R_frac is not None:
            R = max(1, round(R_frac * N))
        else:
            raise ValueError(
                f"Row {i}: no relevant-count field found and no default_R "
                f"or R_frac given. Logs usually drop R; pass R_frac "
                f"(for example 0.05) as an explicit, reported estimate."
            )
        R = min(R, N)

        qid = _resolve(row, "qid", mapping)
        yield QueryRecord(
            N=N, R=R, K=K, hit=_to_bool(hit),
            qid=str(qid) if qid is not None else None,
        )


def from_jsonl(
    path: Union[str, Path],
    *,
    mapping: Optional[Mapping[str, str]] = None,
    default_R: Optional[int] = None,
    R_frac: Optional[float] = None,
    strict: bool = False,
) -> list:
    """Load QueryRecords from a JSONL retrieval log. Read-only and local."""
    rows = []
    with open(path) as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return list(_rows_to_records(rows, mapping, default_R, R_frac, strict))


def from_csv(
    path: Union[str, Path],
    *,
    mapping: Optional[Mapping[str, str]] = None,
    default_R: Optional[int] = None,
    R_frac: Optional[float] = None,
    strict: bool = False,
) -> list:
    """Load QueryRecords from a CSV retrieval log. Read-only and local."""
    with open(path, newline="") as f:
        rows = list(csv.DictReader(f))
    return list(_rows_to_records(rows, mapping, default_R, R_frac, strict))
