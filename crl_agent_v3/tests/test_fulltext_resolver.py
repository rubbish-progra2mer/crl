from __future__ import annotations

import hashlib
from pathlib import Path

import pytest

from crl_v3.knowledge import Paper, paper_payload, resolve_paper_fulltext


def _paper(path: str, data: bytes, *, digest: str | None = None) -> Paper:
    return Paper(
        paper_id="paper-a",
        title="Fixture",
        year=2026,
        source="fixture",
        venue="fixture",
        publication_status="test",
        fulltext_path=path,
        fulltext_sha256=digest or hashlib.sha256(data).hexdigest(),
    )


def test_resolves_knowledge_relative_pdf_and_exposes_current_payload(
    tmp_path: Path,
) -> None:
    root = tmp_path / "knowledge_base"
    pdf = root / "papers" / "paper-a.pdf"
    pdf.parent.mkdir(parents=True)
    data = b"fixture pdf"
    pdf.write_bytes(data)

    resolved = resolve_paper_fulltext(root, _paper("papers/paper-a.pdf", data))
    payload = paper_payload(root, _paper("papers/paper-a.pdf", data))

    assert resolved.resolved_path == str(pdf.resolve())
    assert resolved.resolution_mode == "knowledge_relative"
    assert payload["recorded_fulltext_path"] == "papers/paper-a.pdf"
    assert payload["fulltext_is_current"] is True


def test_missing_legacy_absolute_path_falls_back_by_filename(tmp_path: Path) -> None:
    root = tmp_path / "knowledge_base"
    pdf = root / "papers" / "paper-a.pdf"
    pdf.parent.mkdir(parents=True)
    data = b"legacy fixture pdf"
    pdf.write_bytes(data)

    resolved = resolve_paper_fulltext(
        root, _paper("Z:/retired-machine/library/paper-a.pdf", data)
    )

    assert resolved.resolution_mode == "legacy_filename_fallback"
    assert resolved.resolved_path == str(pdf.resolve())


def test_resolver_rejects_missing_hash_mismatch_and_relative_escape(
    tmp_path: Path,
) -> None:
    root = tmp_path / "knowledge_base"
    (root / "papers").mkdir(parents=True)
    data = b"fixture pdf"
    (root / "papers" / "paper-a.pdf").write_bytes(data)

    with pytest.raises(ValueError, match="hash mismatch"):
        resolve_paper_fulltext(root, _paper("papers/paper-a.pdf", data, digest="0" * 64))
    with pytest.raises(ValueError, match="missing"):
        resolve_paper_fulltext(root, _paper("Z:/retired/missing.pdf", data))
    with pytest.raises(ValueError, match="escapes"):
        resolve_paper_fulltext(root, _paper("../paper-a.pdf", data))
