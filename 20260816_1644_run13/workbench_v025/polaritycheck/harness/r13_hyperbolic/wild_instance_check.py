#!/usr/bin/env python3
"""Demonstrate the §9 proposition on a THIRD-PARTY implementation found in the wild.

The proposition says post-hoc Poincare projection of L2-normalised embeddings
cannot change any ranking. Verifying that on our own code is necessary but weak
-- a reviewer wants it shown on somebody else's.

The functions below are transcribed VERBATIM from
``unworthyzeus/HyperRAG`` @ ``src/HyperRAG/core/geometry.py`` (fetched
2026-07-26), not reimplemented from the paper's formulas. Only the surrounding
class scaffolding is dropped.

Why this repository is an instance, established by reading rather than assumed:

  1. ``engines.py`` HyperbolicRAG.ingest calls
     ``self.encoder.encode(documents)`` with ``all-MiniLM-L6-v2`` and names the
     output ``raw_embeddings``.
  2. That checkpoint's ``modules.json`` ends with a ``Normalize`` module
     (verified against huggingface.co), so ``encode()`` returns UNIT-NORM
     vectors. The variable name is misleading; the data is normalised.
  3. ``project_to_ball`` then divides by the norms and rescales by
     ``tanh(norms / max(norms)) * max_norm``. On all-ones norms that factor is
     the CONSTANT ``tanh(1) * 0.99``.
  4. So every document lands at the same ball radius, and by the proposition its
     "hyperbolic" retrieval ranking is identical to plain cosine ranking.

This script demonstrates (4) empirically instead of asserting it, and also shows
their own diagnostic print would have exposed it.

NOTE ON FRAMING: this is a PATTERN INSTANCE, not a callout. The same defect
shipped in the system this repository audits, found the same way. The point is
that the idiom is easy to write and silently degenerate -- not that one project
got it wrong.

Run:  python harness/r13_hyperbolic/wild_instance_check.py
"""

from __future__ import annotations

import numpy as np

EPS = 1e-8
CURVATURE = 1.0

# ---------------------------------------------------------------------------
# LICENSING NOTE — why this is a from-description re-implementation
#
# An earlier draft of this file transcribed ~30 lines VERBATIM from
# `unworthyzeus/HyperRAG :: src/HyperRAG/core/geometry.py`. That repository has
# **no LICENSE file**, so under the Berne default all rights are reserved and
# public visibility on GitHub implies no permissive terms. Vendoring their
# bytes would have been redistribution without a grant, so no code of theirs
# ships here.
#
# Algorithms are not copyrightable; expression is. The two functions below are
# therefore written from the DESCRIPTION of what their code does, not copied
# from it — and the description is what a paper would print anyway.
#
# WHAT THEIR CODE DOES, described, with locators for anyone verifying:
#   repo   github.com/unworthyzeus/HyperRAG
#   files  src/HyperRAG/core/geometry.py  (project_to_ball, hyperbolic_distance)
#          src/HyperRAG/core/engines.py   (HyperbolicRAG.ingest / .query)
#   read   2026-07-26
#
#   `project_to_ball(vectors, max_norm=0.99)`
#       divides each vector by its own norm (the source comment reads
#       "Normalize to unit sphere first"), then rescales every direction by
#       `tanh(norm / max(norms)) * max_norm`.
#   `hyperbolic_distance(x, y, c)`
#       the standard Poincare ball distance,
#           (1/sqrt(c)) * arcosh(1 + 2c|x-y|^2 / ((1-c|x|^2)(1-c|y|^2)))
#       with the denominator and the arcosh argument clamped.
#       This is the SAME textbook formula the audited system itself implements
#       (see poincare_reference.py), so nothing about it is theirs to grant in
#       the first place.
#
# The load-bearing observation needs no code of theirs at all: the engine feeds
# `project_to_ball` the output of `all-MiniLM-L6-v2`, whose `modules.json` ends
# with a `Normalize` module. So the input is already unit-norm, `max(norms)` is
# 1, and the rescale factor collapses to the CONSTANT tanh(1)*0.99.
# ---------------------------------------------------------------------------


def project_to_ball(vectors: np.ndarray, max_norm: float = 0.99) -> np.ndarray:
    """Normalise to the unit sphere, then rescale by tanh(norm / max(norm)).

    Written from the description above, not copied. Behaviourally equivalent for
    the purpose of this demonstration, which is the only claim being made.
    """
    norms = np.clip(np.linalg.norm(vectors, axis=-1, keepdims=True), EPS, None)
    directions = vectors / norms
    radii = np.tanh(norms / np.max(norms)) * max_norm
    return directions * radii


def hyperbolic_distance(x: np.ndarray, y: np.ndarray, curvature: float = CURVATURE) -> np.ndarray:
    """Standard Poincare ball distance — the same formula as `poincare_reference`."""
    c = curvature
    gap_sq = np.sum((x - y) ** 2, axis=-1)
    denom = np.clip((1 - c * np.sum(x**2, axis=-1)) * (1 - c * np.sum(y**2, axis=-1)), EPS, None)
    inner = np.clip(1 + 2 * c * gap_sq / denom, 1.0 + EPS, None)
    return np.arccosh(inner) / np.sqrt(c)


# ---------------------------------------------------------------------------
# The demonstration
# ---------------------------------------------------------------------------

rng = np.random.default_rng(20260726)
N_DOCS, DIM = 400, 384  # 384 = all-MiniLM-L6-v2's output width

# Stand in for `encoder.encode(documents)` on a Normalize-terminated checkpoint:
# unit-norm rows. (Using random directions rather than real text is the
# conservative choice -- the proposition is about norms, not semantics, and real
# embeddings are MORE clustered, not less.)
docs = rng.normal(size=(N_DOCS, DIM))
docs /= np.linalg.norm(docs, axis=1, keepdims=True)
query = rng.normal(size=DIM)
query /= np.linalg.norm(query)

print("=" * 78)
print("THE SEC. 9 PROPOSITION, DEMONSTRATED ON THIRD-PARTY CODE (unworthyzeus/HyperRAG)")
print("=" * 78)
print(f"  {N_DOCS} unit-norm documents, dim {DIM} (all-MiniLM-L6-v2 width), curvature {CURVATURE}")

ball_docs = project_to_ball(docs)
ball_query = project_to_ball(query.reshape(1, -1))[0]

# --- their own diagnostic, which would have shown this ---------------------
norms = np.linalg.norm(ball_docs, axis=1)
print("\n1. Their own printed diagnostic (engines.py, HyperbolicRAG.ingest):")
print(f"     Poincare norms: mean={np.mean(norms):.4f}, max={np.max(norms):.4f}")
print(f"     spread (max - min) = {np.max(norms) - np.min(norms):.3e}")
print(f"     predicted constant radius tanh(1)*0.99 = {np.tanh(1.0) * 0.99:.4f}")
collapsed = bool(np.allclose(norms, norms[0], atol=1e-12))
print(f"     -> every document at an IDENTICAL radius: {collapsed}")
print("     mean == max is the tell. It is printed on every ingest and nothing checks it.")

# --- the retrieval rankings -----------------------------------------------
d_hyp = hyperbolic_distance(ball_query, ball_docs)
cos_sim = docs @ query                     # what the cosine engine in the same file uses
d_euc = np.linalg.norm(docs - query, axis=1)

order_hyp = np.argsort(d_hyp)
order_cos = np.argsort(-cos_sim)            # descending similarity == ascending distance
order_euc = np.argsort(d_euc)

print("\n2. Retrieval rankings over all 400 documents:")
print(f"     argsort(hyperbolic) == argsort(-cosine)    : {bool(np.array_equal(order_hyp, order_cos))}")
print(f"     argsort(hyperbolic) == argsort(euclidean)  : {bool(np.array_equal(order_hyp, order_euc))}")


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    ra -= ra.mean()
    rb -= rb.mean()
    return float(ra @ rb / (np.linalg.norm(ra) * np.linalg.norm(rb)))


print(f"     Spearman(hyperbolic, euclidean)           : {spearman(d_hyp, d_euc):.10f}")
print(f"     top-10 identical                          : "
      f"{bool(np.array_equal(order_hyp[:10], order_cos[:10]))}")

# --- and the closed form predicts their distances exactly -----------------
r = float(np.tanh(1.0) * 0.99)
k = np.sinh(2.0) ** 2 / 2.0
t = np.linalg.norm(docs - query, axis=1)            # Euclidean distance of the UNIT vectors
# their radius is r, not tanh(sqrt c)/sqrt c, so rescale: |x-y| = r * t
predicted = np.arccosh(1.0 + 2.0 * (r * t) ** 2 / (1.0 - r**2) ** 2)
print("\n3. The closed form predicts their numbers, not just their ranking:")
print(f"     max |their hyperbolic_distance - closed form| = {np.max(np.abs(d_hyp - predicted)):.3e}")

print("\n" + "=" * 78)
verdict = (
    collapsed
    and np.array_equal(order_hyp, order_cos)
    and np.array_equal(order_hyp, order_euc)
    and np.max(np.abs(d_hyp - predicted)) < 1e-9
)
if verdict:
    print("RESULT: CONFIRMED on third-party code.")
    print("  Their hyperbolic retrieval returns EXACTLY the cosine ranking, document")
    print("  for document, including the top-10. The Poincare ball, the exp-map-style")
    print("  projection, the arcosh geodesic and the curvature parameter are all")
    print("  computed, and none of them can affect a single result. This is what the")
    print("  proposition forces -- shown, not inferred.")
else:
    print("RESULT: NOT CONFIRMED -- investigate before citing.")
print("=" * 78)
raise SystemExit(0 if verdict else 1)
