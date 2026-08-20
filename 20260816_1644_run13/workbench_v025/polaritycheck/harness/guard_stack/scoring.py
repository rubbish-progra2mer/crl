"""Shared scoring definitions for the drift-guard corpora (§6).

The two catch predicates below are the WHOLE definition of "a layer caught a
mutation"; keeping them in one module means no two runners can silently
disagree about what a catch is. Pure stdlib at import time.
"""

from __future__ import annotations

import json
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parents[2]

#: The in-sample corpus (26 mutations + 5 faithful controls).
CORPUS_PATH = _REPO_ROOT / "corpus" / "negation_corpus.json"
#: The held-out corpus (30 mutations + 10 faithful controls), authored under
#: documented isolation — see its ``authoring_isolation`` field.
HELDOUT_PATH = _REPO_ROOT / "corpus" / "heldout_drift_corpus.json"

#: Classes whose cases are genuine mutations (a catch is a TRUE POSITIVE).
MUTATION_CLASSES = (
    "negation_flip",
    "scope_inversion",
    "constraint_deletion",
    "quantity_unit_drift",
    "modal_downgrade",
)
#: Negative-control class (a fire is a FALSE POSITIVE).
CONTROL_CLASSES = ("faithful_control",)
ALL_CLASSES = MUTATION_CLASSES + CONTROL_CLASSES

#: Mirrors the audited system's verdict literal.
VERDICT_CONTRADICTS = "CONTRADICTS"


def load_corpus(path: "Path | str | None" = None) -> dict:
    """Load and return a corpus JSON as a dict (defaults to the in-sample corpus)."""
    p = Path(path) if path is not None else CORPUS_PATH
    with open(p, "r", encoding="utf-8") as fh:
        return json.load(fh)


def cosine_catches(similarity: float, drift_threshold: float) -> bool:
    """The cosine drift tripwire FIRES when root<->mutated cosine similarity falls
    strictly BELOW the shipped drift threshold (< threshold == catastrophic drift)."""
    return similarity < drift_threshold


def nli_catches(verdict: str) -> bool:
    """The NLI tripwire FIRES when the shipped argmax verdict is CONTRADICTS."""
    return verdict == VERDICT_CONTRADICTS


def is_mutation(case: dict) -> bool:
    return case["mutation_class"] in MUTATION_CLASSES


def is_control(case: dict) -> bool:
    return case["mutation_class"] in CONTROL_CLASSES
