#!/usr/bin/env python3
"""The audited production components, extracted verbatim in their math.

This module reproduces the two model-backed components of the audited system
exactly as production runs them, with the surrounding application machinery
(routing tables, config loaders, telemetry) removed. Nothing that affects a
number in the paper is changed:

1. ``MRLEmbeddingRouter`` — the production embedding path:
   ``nomic-embed-text-v1.5``, ``search_document:`` prefix, [CLS] pooling, final
   LayerNorm, Matryoshka truncation to 256 dims, L2 normalisation, CPU.
   ``calculate_drift`` returns the cosine similarity this path produces; the
   shipped drift guard fires when it falls below ``DRIFT_THRESHOLD``.
2. ``TransformersNLIClassifier`` — the pinned 3-way NLI cross-encoder used by
   the NLI comparisons (§7's drop-in row), ``cross-encoder/nli-MiniLM2-L6-H768``
   at a fixed revision, CPU-enforced, offline-only.

Both load from the local Hugging Face cache only (``HF_HUB_OFFLINE=1`` is set
at import). A missing checkpoint fails LOUD; nothing silently degrades.

Fetch once, with the network on::

    HF_HUB_OFFLINE=0 python -c "from transformers import AutoModel; \
        AutoModel.from_pretrained('nomic-ai/nomic-embed-text-v1.5', trust_remote_code=True)"
    HF_HUB_OFFLINE=0 python -c "from huggingface_hub import snapshot_download; \
        snapshot_download('cross-encoder/nli-MiniLM2-L6-H768', \
        revision='b95119ce93d3e065de6214e38cd4a97b0f2f2c6d')"
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Protocol, Sequence

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

#: The audited system's shipped drift threshold (its config file's
#: ``cognitive_bounds.drift_threshold``). ``calculate_drift`` returns a cosine
#: similarity; a value BELOW this threshold is treated as catastrophic drift.
DRIFT_THRESHOLD = 0.40

#: The audited system's shipped duplicate-gate threshold (cos > 0.85 == "duplicate"),
#: read from the production source, not from documentation.
DUPLICATE_GATE_THRESHOLD = 0.85


# =========================================================================
# 1. The production embedding path
# =========================================================================
class MRLEmbeddingRouter:
    """The audited production embedder: nomic-embed-text-v1.5 at MRL-256, CPU.

    The class name, the ``search_document:`` prefix (an asymmetric retrieval
    prefix applied to a symmetric task — production's choice, reported rather
    than corrected), the [CLS]+LayerNorm pooling, the truncation, and the
    rounding in ``calculate_drift`` are all preserved from the shipped code.
    """

    def __init__(self, matryoshka_dim: int = 256):
        import torch  # function-local so importing this module stays cheap
        from transformers import AutoModel, AutoTokenizer

        self._torch = torch
        self.matryoshka_dim = matryoshka_dim
        self.device = "cpu"  # production enforces CPU execution

        print("[ROUTER] Loading MRL embedding model on CPU...")
        # nomic-embed requires trust_remote_code=True for its custom architecture
        self.tokenizer = AutoTokenizer.from_pretrained(
            "nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True
        )
        self.model = AutoModel.from_pretrained(
            "nomic-ai/nomic-embed-text-v1.5", trust_remote_code=True
        ).to(self.device)
        self.model.eval()

    def _embed(self, texts: list[str]):
        """Return L2-normalised MRL-truncated embeddings for a list of texts."""
        import torch.nn.functional as F

        prefixed_texts = [f"search_document: {text}" for text in texts]
        encoded_input = self.tokenizer(
            prefixed_texts, padding=True, truncation=True, return_tensors="pt"
        ).to(self.device)

        with self._torch.no_grad():
            model_output = self.model(**encoded_input)

        # [CLS] token embeddings (position 0)
        token_embeddings = model_output[0]
        cls_embeddings = token_embeddings[:, 0]

        # nomic requires a final LayerNorm before normalisation
        cls_embeddings = F.layer_norm(
            cls_embeddings, normalized_shape=(cls_embeddings.shape[1],)
        )

        # the Matryoshka slice: truncate from 768 down to matryoshka_dim
        truncated_embeddings = cls_embeddings[:, : self.matryoshka_dim]

        # L2 normalisation: dot products are then cosine similarities
        return F.normalize(truncated_embeddings, p=2, dim=1)

    def embed(self, text: str):
        """L2-normalised MRL embedding for one text, shape (1, matryoshka_dim)."""
        return self._embed([text])

    def batch_embed(self, texts: list) -> list:
        """Per-text L2-normalised embeddings as a list of 1-D tensors."""
        embeddings = self._embed(texts)
        return [embeddings[i] for i in range(embeddings.shape[0])]

    def calculate_drift(self, origin_text: str, current_text: str) -> float:
        """Cosine similarity between the two texts on the production path.

        1.0 = identical; the shipped guard treats < DRIFT_THRESHOLD as
        catastrophic semantic drift. Rounding preserved from production.
        """
        import numpy as np

        origin_vec = self._embed([origin_text]).cpu().numpy()[0]
        current_vec = self._embed([current_text]).cpu().numpy()[0]
        similarity = float(np.dot(origin_vec, current_vec))
        return round(similarity, 4)


# =========================================================================
# 2. The pinned NLI cross-encoder
# =========================================================================

#: The three NLI labels required, in canonical (alphabetical) order.
NLI_LABELS = ("contradiction", "entailment", "neutral")

#: Pinned model artifact.
DEFAULT_MODEL_ID = "cross-encoder/nli-MiniLM2-L6-H768"
DEFAULT_MODEL_REVISION = "b95119ce93d3e065de6214e38cd4a97b0f2f2c6d"

#: Pair verdicts.
VERDICT_CONTRADICTS = "CONTRADICTS"  # genuine disagreement
VERDICT_DUPLICATE = "DUPLICATE"  # same decision reworded — bidirectional entailment
VERDICT_NEUTRAL = "NEUTRAL"  # neither


class NLIModelUnavailableError(RuntimeError):
    """The pinned NLI artifact is not in the local cache (or failed to load).

    Deliberately loud: the classifier refuses to run without its pinned model
    rather than silently degrading to a weaker proxy.
    """


class UnexpectedNLIHeadError(RuntimeError):
    """The loaded checkpoint's classification head does not expose exactly the
    three NLI labels — guards against an artifact swap silently changing what
    is measured."""


@dataclass(frozen=True)
class NLIJudgment:
    """Directed NLI probabilities for one (premise => hypothesis) reading."""

    contradiction: float
    entailment: float
    neutral: float

    @property
    def label(self) -> str:
        """Argmax label — untuned by design (no threshold to overfit)."""
        return max(NLI_LABELS, key=lambda name: getattr(self, name))


class NLIClassifier(Protocol):
    def judge_batch(
        self, pairs: Sequence[tuple[str, str]]
    ) -> list[NLIJudgment]:  # pragma: no cover - protocol
        ...


@dataclass(frozen=True)
class PairPolarity:
    """The NLI reading for one text pair; both directions kept (NLI is
    asymmetric, and one-way entailment must NOT count as duplication)."""

    text_a: str
    text_b: str
    forward: NLIJudgment  # text_a as premise => text_b as hypothesis
    backward: NLIJudgment  # text_b as premise => text_a as hypothesis

    @property
    def contradiction(self) -> float:
        """Max directed contradiction — the polarity signal."""
        return max(self.forward.contradiction, self.backward.contradiction)

    @property
    def duplication(self) -> float:
        """Min directed entailment — paraphrase requires BOTH directions."""
        return min(self.forward.entailment, self.backward.entailment)

    @property
    def distinctness(self) -> float:
        """``1 - duplication``."""
        return 1.0 - self.duplication

    @property
    def verdict(self) -> str:
        """Untuned trichotomy from argmax labels (no tunable threshold)."""
        if (
            self.forward.label == "contradiction"
            or self.backward.label == "contradiction"
        ):
            return VERDICT_CONTRADICTS
        if self.forward.label == "entailment" and self.backward.label == "entailment":
            return VERDICT_DUPLICATE
        return VERDICT_NEUTRAL


def pair_polarity(text_a: str, text_b: str, classifier: NLIClassifier) -> PairPolarity:
    """Judge one text pair in both directions."""
    forward, backward = classifier.judge_batch([(text_a, text_b), (text_b, text_a)])
    return PairPolarity(text_a=text_a, text_b=text_b, forward=forward, backward=backward)


def _label_index_map(id2label: dict) -> dict[str, int]:
    """Map canonical NLI label -> logit index, case-insensitively.

    Raises :class:`UnexpectedNLIHeadError` unless the head exposes exactly the
    three canonical labels.
    """
    seen = {str(name).strip().lower(): int(idx) for idx, name in id2label.items()}
    if sorted(seen) != sorted(NLI_LABELS):
        raise UnexpectedNLIHeadError(
            f"NLI head labels {sorted(seen)} != required {sorted(NLI_LABELS)}; "
            "refusing to guess a mapping."
        )
    return seen


class TransformersNLIClassifier:
    """The pinned classifier. CPU-enforced, offline-only, loud on absence."""

    def __init__(
        self,
        model_id: str = DEFAULT_MODEL_ID,
        revision: str = DEFAULT_MODEL_REVISION,
        device: str = "cpu",
    ):
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        self._torch = torch
        self.device = device
        try:
            self.tokenizer = AutoTokenizer.from_pretrained(
                model_id, revision=revision, local_files_only=True
            )
            self.model = (
                AutoModelForSequenceClassification.from_pretrained(
                    model_id, revision=revision, local_files_only=True
                )
                .to(device)
                .eval()
            )
        except OSError as exc:
            raise NLIModelUnavailableError(
                f"Pinned NLI artifact '{model_id}'@{revision} is not in the local "
                "HF cache (this classifier never downloads at runtime). Fetch it "
                "once with huggingface_hub.snapshot_download at that revision."
            ) from exc
        self._label_to_index = _label_index_map(dict(self.model.config.id2label))

    def judge_batch(self, pairs: Sequence[tuple[str, str]]) -> list[NLIJudgment]:
        """Softmaxed 3-way judgments for a batch of (premise, hypothesis) pairs."""
        if not pairs:
            return []
        premises = [p for p, _ in pairs]
        hypotheses = [h for _, h in pairs]
        encoded = self.tokenizer(
            premises,
            hypotheses,
            padding=True,
            truncation=True,
            return_tensors="pt",
        ).to(self.device)
        with self._torch.no_grad():
            logits = self.model(**encoded).logits
        probs = self._torch.softmax(logits, dim=-1)
        ix = self._label_to_index
        return [
            NLIJudgment(
                contradiction=float(row[ix["contradiction"]]),
                entailment=float(row[ix["entailment"]]),
                neutral=float(row[ix["neutral"]]),
            )
            for row in probs
        ]
