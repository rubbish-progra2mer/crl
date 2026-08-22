"""Deterministic context updates shared by rollout collection and inference."""

from __future__ import annotations

import unicodedata
from collections.abc import Iterable
from typing import Any


def _normalized_text(value: Any) -> str:
    return unicodedata.normalize("NFKC", str(value)).casefold()


def _document_key(document: dict[str, Any]) -> tuple[str, str]:
    return (
        _normalized_text(document.get("title", "")).strip(),
        _normalized_text(document.get("text", document.get("content", ""))).strip(),
    )


def append_and_deduplicate(
    context: Iterable[dict[str, Any]], documents: Iterable[dict[str, Any]]
) -> list[dict[str, Any]]:
    """Append documents in order and remove repeated title/text pairs."""

    combined: list[dict[str, Any]] = []
    seen: set[tuple[str, str]] = set()
    for document in [*context, *documents]:
        if not isinstance(document, dict):
            raise ValueError("context documents must be objects")
        key = _document_key(document)
        if key in seen:
            continue
        seen.add(key)
        combined.append(dict(document))
    return combined
