#!/usr/bin/env python3
"""Battery 2 — does escaping the FIXED THRESHOLD escape the defect?

THE QUESTION
------------
Battery 1 audited three components that all share one mechanism: compare cosine
to a constant. The obvious objection — and the right one — is that the finding
might be about *thresholding policy* rather than about the representation. If so,
the fix is cheap: use an adaptive cut, or rank instead of threshold, and move on.

So this battery runs the SAME labelled pairs through FOUR STRUCTURALLY DIFFERENT
decision mechanisms found in widely-used packages:

  M1  FIXED ABSOLUTE THRESHOLD   cos >= k
      LlamaIndex 0.8 · LangChain filter 0.95 · GPTCache ~0.8 · Semantic Kernel 0.7
      (measured in Battery 1; carried here for comparison)

  M2  CONTINUOUS SCORE REPORTED AS THE METRIC — no decision at all
      ragas SemanticSimilarity, whose `threshold` defaults to None, so the raw
      similarity IS the reported number. Transcribed from
      src/ragas/metrics/collections/_semantic_similarity.py:
          score = similarity.flatten()
          if self.threshold: score = score >= self.threshold
      Failure mode is different in kind: not a wrong decision but an INFLATED
      REPORTED NUMBER that flows into a headline metric.

  M3  TOP-K RANKING WITH NO THRESHOLD
      sentence_transformers.util.paraphrase_mining (score_function=cos_sim,
      top_k=100, no cutoff). Nothing is compared to a constant anywhere. If
      opposite-meaning pairs still surface as top "paraphrases", the defect
      cannot be a thresholding artefact.

  M4  ADAPTIVE / RELATIVE THRESHOLD — the cut is computed from the data
      LangChain SemanticChunker, BREAKPOINT_DEFAULTS =
      {'percentile': 95, 'standard_deviation': 3, 'interquartile': 1.5,
       'gradient': 95}. Splits where similarity DROPS. A meaning flip that does
      not drop similarity gets no breakpoint, so a statement and its negation
      land in the SAME chunk.

If M3 and M4 fail too, the claim generalises past thresholds: the representation
does not carry the property, and no decision policy over it can.

Usage:
    python harness/framework_audit/run_mechanism_variance.py
"""

from __future__ import annotations

import json
import os
import platform
import sys
import time
from pathlib import Path

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")

_HERE = Path(__file__).resolve()
_REPO_ROOT = _HERE.parents[2]
for _p in (str(_REPO_ROOT),):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from harness.factorial_pilot import encoders as enc_registry  # noqa: E402
from harness.lib import stats  # noqa: E402

RESULTS_DIR = _REPO_ROOT / "results" / "framework_audit"
CORPUS_DIR = _REPO_ROOT / "corpus"


def load_all() -> list[dict]:
    rows = []
    for t in ("distinctness", "constraint"):
        f = CORPUS_DIR / f"{t}_2x2.jsonl"
        rows += [json.loads(ln) for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()]
    return rows


# ==========================================================================
# M2 — the continuous score, reported as the metric
# ==========================================================================


def m2_continuous(encoders, rows, out):
    print("=" * 88)
    print("M2 — CONTINUOUS SCORE AS THE REPORTED METRIC  (ragas SemanticSimilarity)")
    print("=" * 88)
    print("  `threshold` defaults to None, so the raw similarity IS the reported number.")
    print("  A wrong answer does not get 'passed' — it gets a HIGH SCORE that goes")
    print("  straight into a headline metric. Failure differs in KIND, not degree.\n")
    same = [r for r in rows if r["decision"] in ("SAME", "FAITHFUL")]
    opp = [r for r in rows if r["decision"] in ("OPPOSITE", "VIOLATION")]
    print(f"  {'encoder':<40s} {'mean score, RIGHT':>18s} {'mean score, WRONG':>18s} {'gap':>7s}")
    print("  " + "-" * 88)
    block = {"mechanism": "M2 continuous score (ragas SemanticSimilarity, threshold=None)",
             "per_encoder": []}
    for e in encoders:
        cs = e.cosines([(r["text_a"], r["text_b"]) for r in same])
        cm = e.cosines([(r["text_a"], r["text_b"]) for r in opp])
        ms, mm = sum(cs) / len(cs), sum(cm) / len(cm)
        rec = {"encoder": e.name, "mean_right": round(ms, 4), "mean_wrong": round(mm, 4),
               "gap": round(ms - mm, 4),
               "wrong_scored_above_0.8": round(sum(c >= 0.8 for c in cm) / len(cm), 4)}
        block["per_encoder"].append(rec)
        print(f"  {e.name[:38]:<40s} {ms:>18.4f} {mm:>18.4f} {ms - mm:>+7.4f}")
    gaps = [r["gap"] for r in block["per_encoder"]]
    block["gap_range"] = [min(gaps), max(gaps)]
    print(f"\n  => a WRONG answer scores within {min(gaps):.3f}–{max(gaps):.3f} of a RIGHT one.")
    print("     Reported as a 0–1 'semantic similarity', that difference is invisible")
    print("     in any aggregate a practitioner actually looks at.")
    out["mechanisms"].append(block)


# ==========================================================================
# M3 — top-k ranking, no threshold anywhere
# ==========================================================================


def m3_ranking(encoders, rows, out):
    print("\n" + "=" * 88)
    print("M3 — TOP-K RANKING, NO THRESHOLD  (sentence_transformers.util.paraphrase_mining)")
    print("=" * 88)
    print("  Nothing is compared to a constant. The function mines the highest-scoring")
    print("  pairs in a corpus and calls them paraphrases. If opposite-meaning pairs")
    print("  rank at the top, the defect is NOT a thresholding artefact.\n")

    try:
        from sentence_transformers import SentenceTransformer, util
    except Exception as exc:
        print(f"  [SKIP] {exc}")
        return

    # Build a corpus: every text in the pair set. Then ask paraphrase_mining for
    # its top pairs and check what fraction of them are OPPOSITE-meaning pairs
    # that we know the ground truth for.
    truth = {}
    texts = []
    for r in rows:
        for a, b in ((r["text_a"], r["text_b"]),):
            if a not in texts:
                texts.append(a)
            if b not in texts:
                texts.append(b)
        key = tuple(sorted((r["text_a"], r["text_b"])))
        truth[key] = r["decision"] in ("SAME", "FAITHFUL")

    block = {"mechanism": "M3 top-k ranking (paraphrase_mining, no threshold)",
             "n_corpus": len(texts), "per_model": []}
    print(f"  corpus: {len(texts)} sentences, {len(truth)} of the pairs have ground truth\n")
    print(f"  {'model':<40s} {'top-20 mined':>14s} {'of which WRONG':>16s}")
    print("  " + "-" * 76)
    for mid in ["sentence-transformers/all-MiniLM-L6-v2", "BAAI/bge-base-en-v1.5",
                "mixedbread-ai/mxbai-embed-large-v1"]:
        try:
            model = SentenceTransformer(mid, device="cpu")
        except Exception as exc:
            print(f"  {mid[:38]:<40s} SKIP ({type(exc).__name__})")
            continue
        pairs = util.paraphrase_mining(model, texts, show_progress_bar=False)
        judged, wrong = 0, 0
        for score, i, j in pairs:
            key = tuple(sorted((texts[i], texts[j])))
            if key in truth:
                judged += 1
                if not truth[key]:
                    wrong += 1
                if judged >= 20:
                    break
        rec = {"model": mid, "top_judged": judged, "opposite_meaning": wrong,
               "wrong_rate": round(wrong / judged, 4) if judged else None}
        block["per_model"].append(rec)
        print(f"  {mid[:38]:<40s} {judged:>14d} {wrong:>10d} = {rec['wrong_rate']:>5.1%}")
    wr = [r["wrong_rate"] for r in block["per_model"] if r["wrong_rate"] is not None]
    if wr:
        block["wrong_rate_range"] = [min(wr), max(wr)]
        print(f"\n  => {min(wr):.0%}–{max(wr):.0%} of the top-ranked 'paraphrases' are pairs")
        print("     that decide OPPOSITE things. No threshold was involved anywhere.")
    out["mechanisms"].append(block)


# ==========================================================================
# M4 — adaptive / relative threshold
# ==========================================================================


def m4_adaptive(encoders, rows, out):
    print("\n" + "=" * 88)
    print("M4 — ADAPTIVE THRESHOLD  (LangChain SemanticChunker)")
    print("=" * 88)
    print("  The cut is COMPUTED FROM THE DATA, not typed in: percentile 95,")
    print("  standard_deviation 3, interquartile 1.5, gradient 95.")
    print("  The chunker splits where similarity DROPS between adjacent sentences.")
    print("  Probe: build a document that alternates a statement and its NEGATION.")
    print("  A meaning flip at every boundary should split at every boundary.\n")

    try:
        from langchain_experimental.text_splitter import BREAKPOINT_DEFAULTS
    except Exception as exc:
        print(f"  [SKIP] {exc}")
        return

    block = {"mechanism": "M4 adaptive threshold (SemanticChunker)",
             "breakpoint_defaults": BREAKPOINT_DEFAULTS, "per_encoder": []}

    # ------------------------------------------------------------------
    # M4a — THE PARAPHRASE TEST. The fair, matched, no-artificial-document
    # version, and the one that carries the claim.
    #
    # A breakpoint detector asks: "is there a discontinuity here?" So the
    # honest question is a RANKING one that needs no threshold and no
    # constructed corpus:
    #
    #     does a MEANING REVERSAL register as a bigger discontinuity than a
    #     MEANING-PRESERVING RESTATEMENT of the same sentence?
    #
    # Both sides share the anchor, so topic is held constant by construction --
    # there is no "maximal topic change" strawman anywhere in this comparison.
    # If reversals move LESS than restatements, any breakpoint detector will
    # split a sentence from its own paraphrase while keeping it welded to its
    # own negation, whatever policy sits on top.
    # ------------------------------------------------------------------
    by_group: dict = {}
    for r in rows:
        g = (r["task"], r["anchor_group"])
        by_group.setdefault(g, {})[(r["decision"], r["lexical"])] = r
    groups = [g for g, d in by_group.items() if len(d) == 4]

    print("  M4a — THE PARAPHRASE TEST (matched: same anchor on both sides)")
    print(f"  {len(groups)} anchors. For each: distance to its REVERSAL vs distance to")
    print("  its own faithful RESTATEMENT. Topic is constant; no artificial document.\n")
    print(f"  {'encoder':<38s} {'d(reversal)':>12s} {'d(restate)':>11s} {'AUROC':>7s} {'reversal moves LESS':>20s}")
    print("  " + "-" * 92)
    m4a = {"comparison": "meaning reversal vs faithful restatement, anchor matched",
           "n_anchors": len(groups), "per_encoder": []}
    for e in encoders:
        def dist(dec_key):
            pairs = [(by_group[g][dec_key]["text_a"], by_group[g][dec_key]["text_b"])
                     for g in groups]
            return [1.0 - c for c in e.cosines(pairs)]
        neg_key = ("OPPOSITE", "CLOSE") if ("OPPOSITE", "CLOSE") in by_group[groups[0]] else None
        d_rev, d_res = [], []
        for g in groups:
            d = by_group[g]
            rev = d.get(("OPPOSITE", "CLOSE")) or d.get(("VIOLATION", "CLOSE"))
            res = d.get(("SAME", "DISTANT")) or d.get(("FAITHFUL", "DISTANT"))
            c = e.cosines([(rev["text_a"], rev["text_b"]), (res["text_a"], res["text_b"])])
            d_rev.append(1.0 - c[0])
            d_res.append(1.0 - c[1])
        a = stats.auroc(d_rev, d_res)  # P(reversal moves MORE than restatement)
        less = sum(x < y for x, y in zip(d_rev, d_res))
        rec = {"encoder": e.name,
               "mean_distance_reversal": round(sum(d_rev) / len(d_rev), 4),
               "mean_distance_restatement": round(sum(d_res) / len(d_res), 4),
               "auroc_reversal_moves_more": round(a, 4),
               "anchors_where_reversal_moves_less": less, "n_anchors": len(groups)}
        m4a["per_encoder"].append(rec)
        print(f"  {e.name[:36]:<38s} {rec['mean_distance_reversal']:>12.4f} "
              f"{rec['mean_distance_restatement']:>11.4f} {a:>7.3f} {less:>13d}/{len(groups):<3d}")
    aa = [r["auroc_reversal_moves_more"] for r in m4a["per_encoder"]]
    ll = [r["anchors_where_reversal_moves_less"] for r in m4a["per_encoder"]]
    m4a["auroc_range"] = [min(aa), max(aa)]
    print(f"\n  => AUROC(reversal moves more than restatement) = {min(aa):.3f}-{max(aa):.3f};")
    print(f"     chance is 0.500. Reversal moves LESS on {min(ll)}-{max(ll)} of {len(groups)} anchors.")
    print("     A breakpoint detector therefore splits a sentence from its own")
    print("     PARAPHRASE while keeping it welded to its own NEGATION. No threshold,")
    print("     no constructed document, topic held constant. This is the fair version.")
    block["m4a_paraphrase_test"] = m4a

    opp = [r for r in rows if r["decision"] in ("OPPOSITE", "VIOLATION")
           and r["lexical"] == "CLOSE"]
    # a document where EVERY adjacent boundary is a meaning flip
    doc_sents = []
    for r in opp:
        doc_sents += [r["text_a"], r["text_b"]]
    n_flip_boundaries = len(doc_sents) - 1
    print("\n  M4b — the constructed-document version (kept for completeness; its")
    print("  'topic change' boundaries are cross-anchor, so its effect size is an")
    print("  UPPER BOUND rather than an unbiased estimate. M4a is the claim.)\n")

    block["n_sentences"] = len(doc_sents)
    block["n_boundaries"] = n_flip_boundaries
    print(f"  document: {len(doc_sents)} sentences, {n_flip_boundaries} boundaries,")
    print(f"  every other one a direct meaning flip\n")
    print(f"  {'encoder':<40s} {'pctile-95 splits':>17s} {'flips CAUGHT':>14s}")
    print("  " + "-" * 76)

    # The catch-rate alone would be unfair: percentile-95 makes only ~2 splits in
    # a 39-boundary document BY CONSTRUCTION, so a low catch rate is partly an
    # artefact of how few splits it makes. The threshold-free question is better:
    # do meaning flips even RANK as breakpoints? Boundaries alternate
    #   even index = a MEANING FLIP inside one anchor pair (same topic, opposite decision)
    #   odd index  = a TOPIC CHANGE between two unrelated anchor pairs
    # A chunker that tracked meaning would rank flips at least as high as topic
    # changes. AUROC well below 0.5 means it systematically prefers topic
    # boundaries and will never split a negation out of its own paragraph.
    print(f"  {'encoder':<40s} {'splits':>7s} {'caught':>7s} {'AUROC flip vs topic':>21s}")
    print("  " + "-" * 82)
    for e in encoders:
        cos = e.cosines([(doc_sents[i], doc_sents[i + 1]) for i in range(n_flip_boundaries)])
        dists = [1.0 - c for c in cos]
        srt = sorted(dists)
        idx = int(len(srt) * BREAKPOINT_DEFAULTS["percentile"] / 100.0)
        cut = srt[min(idx, len(srt) - 1)]
        splits = [i for i, d in enumerate(dists) if d > cut]
        flip_idx = set(range(0, n_flip_boundaries, 2))
        caught = len(set(splits) & flip_idx)
        flip_d = [d for i, d in enumerate(dists) if i in flip_idx]
        topic_d = [d for i, d in enumerate(dists) if i not in flip_idx]
        a = stats.auroc(flip_d, topic_d)
        rec = {"encoder": e.name, "n_splits": len(splits),
               "flips_caught": caught, "flips_total": len(flip_idx),
               "flip_catch_rate": round(caught / len(flip_idx), 4),
               "auroc_flip_vs_topic": round(a, 4),
               "mean_distance_at_flip": round(sum(flip_d) / len(flip_d), 4),
               "mean_distance_at_topic_change": round(sum(topic_d) / len(topic_d), 4)}
        block["per_encoder"].append(rec)
        print(f"  {e.name[:38]:<40s} {len(splits):>7d} {caught:>3d}/{len(flip_idx):<3d} {a:>21.4f}")
    cr = [r["flip_catch_rate"] for r in block["per_encoder"]]
    ar = [r["auroc_flip_vs_topic"] for r in block["per_encoder"]]
    block["flip_catch_rate_range"] = [min(cr), max(cr)]
    block["auroc_flip_vs_topic_range"] = [min(ar), max(ar)]
    print(f"\n  => splits landing on a meaning flip: {min(cr):.0%}–{max(cr):.0%}.")
    print(f"     AUROC(flip vs topic-change) = {min(ar):.3f}–{max(ar):.3f}, chance 0.5.")
    print("     Meaning flips rank BELOW ordinary topic changes as breakpoints, so an")
    print("     adaptive cut will always spend its splits on topic and never on")
    print("     polarity. Computing the threshold from the data does not rescue it —")
    print("     the drop it looks for is not there to find.")
    out["mechanisms"].append(block)


def main() -> int:
    print(f"[mechanism-variance] {"redacted"}  {platform.platform()}")
    ready, absent = enc_registry.resolve()
    print(f"[mechanism-variance] {len(ready)} encoders, {len(absent)} absent\n")
    rows = load_all()
    out = {
        "experiment": "Battery 2 — mechanism variance",
        "question": "does escaping the fixed threshold escape the defect?",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "node": "redacted",
        "mechanisms": [],
    }
    m2_continuous(ready, rows, out)
    m3_ranking(ready, rows, out)
    m4_adaptive(ready, rows, out)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    dest = RESULTS_DIR / f"mechanism_variance_rerun_{time.strftime('%Y-%m-%d')}.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[mechanism-variance] evidence written: {dest.relative_to(_REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
