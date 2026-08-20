#!/usr/bin/env python3
"""Surface-overlap metrics — the confounder, MEASURED rather than asserted.

The whole point of the factorial design is that the lexical axis is a *measured*
covariate, not a label the author gets to declare. If the assigned CLOSE/DISTANT
labels do not separate on these metrics, the design failed and no encoder result
from it means anything. That check runs before any encoder loads.

Three metrics, reported together because none is authoritative:

* ``token_jaccard``   — Jaccard over lowercased alphanumeric word sets. Primary.
  Interpretable, reviewable by hand, and the one a reader can recompute mentally.
* ``char4_jaccard``   — Jaccard over character 4-grams. Robust to morphology
  ("key"/"keys", "24"/"twenty-four") where token Jaccard is brittle.
* ``levenshtein_sim`` — 1 - normalised edit distance. Sensitive to word order,
  which the two Jaccards are blind to by construction.

Primary is declared in advance (token_jaccard) so the choice cannot be made after
seeing which metric flatters the design.
"""

from __future__ import annotations

import re

PRIMARY_METRIC = "token_jaccard"

_WORD = re.compile(r"[a-z0-9]+")


def tokens(text: str) -> list[str]:
    return _WORD.findall(text.lower())


def token_jaccard(a: str, b: str) -> float:
    sa, sb = set(tokens(a)), set(tokens(b))
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb)


def _ngrams(text: str, n: int = 4) -> set[str]:
    s = re.sub(r"\s+", " ", text.lower().strip())
    if len(s) < n:
        return {s}
    return {s[i : i + n] for i in range(len(s) - n + 1)}


def char4_jaccard(a: str, b: str) -> float:
    ga, gb = _ngrams(a), _ngrams(b)
    if not ga and not gb:
        return 1.0
    return len(ga & gb) / len(ga | gb)


def levenshtein(a: str, b: str) -> int:
    """Classic two-row dynamic program. O(len(a) * len(b)) time, O(len(b)) space."""
    if a == b:
        return 0
    if not a:
        return len(b)
    if not b:
        return len(a)
    prev = list(range(len(b) + 1))
    for i, ca in enumerate(a, 1):
        cur = [i]
        for j, cb in enumerate(b, 1):
            cur.append(min(prev[j] + 1, cur[j - 1] + 1, prev[j - 1] + (ca != cb)))
        prev = cur
    return prev[-1]


def levenshtein_sim(a: str, b: str) -> float:
    al, bl = a.lower(), b.lower()
    m = max(len(al), len(bl))
    return 1.0 - (levenshtein(al, bl) / m) if m else 1.0


def all_metrics(a: str, b: str) -> dict[str, float]:
    return {
        "token_jaccard": round(token_jaccard(a, b), 6),
        "char4_jaccard": round(char4_jaccard(a, b), 6),
        "levenshtein_sim": round(levenshtein_sim(a, b), 6),
    }


if __name__ == "__main__":
    pairs = [
        ("Deploy the migration to production tonight.",
         "Do not deploy the migration to production tonight."),
        ("Deploy the migration to production tonight.",
         "Cut the database change live before morning."),
        ("Never log the raw API key.", "Never log the raw API keys."),
    ]
    for a, b in pairs:
        print(f"{all_metrics(a, b)}\n  {a!r}\n  {b!r}")
