#!/usr/bin/env python3
"""Encoder registry for the factorial pilot. One entry per checkpoint-and-configuration.

PREFIX CONVENTIONS ARE PART OF THE MEASUREMENT
----------------------------------------------
Several of these checkpoints require task prefixes and degrade without them.
Measuring a misconfigured encoder and reporting that it fails would be a strawman,
so each entry carries the prefix its own model card prescribes **for symmetric
semantic similarity** — which is what comparing two instructions is — not the
asymmetric retrieval prefix.

  MiniLM / mpnet / bge / gte     no prefix. (BGE's instruction is query-side and
                                 retrieval-only; the card says omit it for STS.)
  e5-base-v2                     "query: " on BOTH sides for symmetric tasks.
  mxbai-embed-large-v1           no prefix for STS; its prompt is retrieval-only.
                                 NOTE: this is the ONE checkpoint here with no
                                 Normalize module, so its raw output has varying
                                 norms. Cosine is taken over explicitly normalised
                                 vectors.
  nomic-embed-text-v1.5          documented prefixes are search_query / search_document
                                 / classification / clustering. "clustering: " is the
                                 symmetric-similarity choice.

SENSITIVITY VARIANTS, so configuration cannot be blamed for the result
----------------------------------------------------------------------
Where the right prefix is arguable, BOTH are registered and both are reported:

  * ``e5-base-v2`` with and without the "query: " prefix.
  * ``nomic`` as the audited production system actually runs it
    (``search_document: `` — see ``harness/audited_system.py``, an asymmetric
    retrieval prefix applied to a symmetric task, which is production's choice
    and not ours to fix mid-audit) AND with the documented ``clustering: ``
    prefix.

If the finding survives every configuration, "you configured it wrong" is closed.

TO ADD AN ENCODER
-----------------
1. Download once with network on:
       HF_HUB_OFFLINE=0 python -c "from sentence_transformers import SentenceTransformer as S; S('org/model')"
2. Add one ``SentenceTransformerEncoder`` line to ``REGISTRY``.
3. Re-run. It joins every table automatically.

Runs offline by default (``HF_HUB_OFFLINE=1``); an uncached checkpoint is skipped
LOUDLY, never silently.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

_REPO_ROOT = Path(__file__).resolve().parents[2]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


class Encoder:
    """Minimal contract: a name, a family, and cosine over a list of pairs."""

    name = "abstract"
    family = "abstract"
    prefix = ""
    note = ""

    def available(self) -> tuple[bool, str]:
        raise NotImplementedError

    def cosines(self, pairs: list[tuple[str, str]]) -> list[float]:
        raise NotImplementedError


class ProductionMRLEncoder(Encoder):
    """The audited production path: nomic-embed-text-v1.5, MRL-256, CPU.

    Routed through ``MRLEmbeddingRouter.batch_embed`` — the same embedding path
    the shipped gate calls (extracted verbatim in its math into
    ``harness/audited_system.py``) — so this measures production behaviour, not
    a lookalike. The router applies ``search_document: `` internally; that is
    production's choice and is reported, not corrected.
    """

    name = "nomic-embed-text-v1.5 MRL-256 [PRODUCTION PATH, search_document:]"
    family = "nomic"
    note = "production path; asymmetric retrieval prefix applied to a symmetric task"

    def __init__(self) -> None:
        self._router = None

    def available(self) -> tuple[bool, str]:
        try:
            from harness.audited_system import MRLEmbeddingRouter  # noqa: F401
        except Exception as exc:  # pragma: no cover - environment dependent
            return False, f"import failed: {type(exc).__name__}: {exc}"
        cache = Path.home() / ".cache/huggingface/hub"
        if not (cache / "models--nomic-ai--nomic-embed-text-v1.5").exists():
            return False, "nomic-ai/nomic-embed-text-v1.5 not in local HF cache; download once with HF_HUB_OFFLINE=0"
        return True, "ok"

    def cosines(self, pairs: list[tuple[str, str]]) -> list[float]:
        if self._router is None:
            from harness.audited_system import MRLEmbeddingRouter

            self._router = MRLEmbeddingRouter()
        out = []
        for a, b in pairs:
            va, vb = self._router.batch_embed([a, b])
            out.append(float((va * vb).sum()))
        return out


class SentenceTransformerEncoder(Encoder):
    """Any sentence-transformers checkpoint. Cosine over explicitly L2-normalised output."""

    def __init__(
        self,
        model_id: str,
        family: str,
        prefix: str = "",
        label: str | None = None,
        note: str = "",
    ) -> None:
        self.model_id = model_id
        self.family = family
        self.prefix = prefix
        self.note = note
        self.name = label or (model_id + (f" [{prefix.strip()}]" if prefix else ""))
        self._model = None

    def available(self) -> tuple[bool, str]:
        try:
            import sentence_transformers  # noqa: F401
        except Exception:
            return False, "sentence-transformers not installed"
        cache = Path.home() / ".cache/huggingface/hub"
        stub = "models--" + self.model_id.replace("/", "--")
        if not (cache / stub).exists():
            return False, f"not in local HF cache ({stub}); download once with HF_HUB_OFFLINE=0"
        return True, "ok"

    def cosines(self, pairs: list[tuple[str, str]]) -> list[float]:
        if self._model is None:
            from sentence_transformers import SentenceTransformer

            self._model = SentenceTransformer(self.model_id, device="cpu")
        flat = [self.prefix + t for pair in pairs for t in pair]
        # normalize_embeddings=True matters for mxbai, which has no Normalize module.
        emb = self._model.encode(flat, normalize_embeddings=True, show_progress_bar=False)
        return [float((emb[2 * i] * emb[2 * i + 1]).sum()) for i in range(len(pairs))]


# ---------------------------------------------------------------------------
# THE REGISTRY — 9 configurations across 7 checkpoints and 6 model families.
# ---------------------------------------------------------------------------
REGISTRY: list[Encoder] = [
    ProductionMRLEncoder(),
    SentenceTransformerEncoder(
        "nomic-ai/nomic-embed-text-v1.5", "nomic", prefix="clustering: ",
        label="nomic-embed-text-v1.5 [clustering: — documented symmetric prefix]",
        note="sensitivity variant against the production prefix"),
    SentenceTransformerEncoder("sentence-transformers/all-MiniLM-L6-v2", "minilm"),
    SentenceTransformerEncoder("sentence-transformers/all-mpnet-base-v2", "mpnet"),
    SentenceTransformerEncoder("BAAI/bge-base-en-v1.5", "bge",
                               note="no instruction: card says omit for STS"),
    SentenceTransformerEncoder("thenlper/gte-base", "gte"),
    SentenceTransformerEncoder("intfloat/e5-base-v2", "e5", prefix="query: ",
                               label="e5-base-v2 [query: — card's symmetric convention]"),
    SentenceTransformerEncoder("intfloat/e5-base-v2", "e5", prefix="",
                               label="e5-base-v2 [NO prefix — sensitivity variant]",
                               note="registered to show the result is not a prefix artefact"),
    SentenceTransformerEncoder("mixedbread-ai/mxbai-embed-large-v1", "mxbai",
                               note="NO Normalize module: raw norms vary; normalised here"),
]


def resolve() -> tuple[list[Encoder], list[tuple[str, str]]]:
    """Split the registry into (available, [(name, why_absent), ...])."""
    ready, absent = [], []
    for enc in REGISTRY:
        ok, why = enc.available()
        (ready if ok else absent).append(enc if ok else (enc.name, why))
    return ready, absent


if __name__ == "__main__":
    ready, absent = resolve()
    fams = sorted({e.family for e in ready})
    print(f"AVAILABLE: {len(ready)} configurations across {len(fams)} families {fams}")
    for e in ready:
        print(f"  {e.family:8s} {e.name}")
        if e.note:
            print(f"           note: {e.note}")
    print(f"\nABSENT: {len(absent)}")
    for n, w in absent:
        print(f"  {n}\n      {w}")
