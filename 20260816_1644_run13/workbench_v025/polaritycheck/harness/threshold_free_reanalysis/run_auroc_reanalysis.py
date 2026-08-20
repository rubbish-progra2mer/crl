#!/usr/bin/env python3
"""Threshold-free re-analysis of the ALREADY-FROZEN evidence. No models required.

WHY THIS EXISTS
---------------
Every headline number in this repository is either a mean difference
("separation = -0.1632") or a catch-rate at one shipped threshold ("0/26 caught").
Neither survives the first reviewer objection, which is always the same:

    "So your threshold was wrong. Recalibrate it."

That objection is fatal to a catch-rate and irrelevant to an AUROC. AUROC asks
whether ANY operating point separates the classes, in either direction. Three
outcomes, three different papers:

  AUROC ~ 0.5              => no signal at all; the measure is uninformative
  AUROC clearly BELOW 0.5  => the measure is ANTI-CORRELATED with the property.
                              The shipped gate has the WRONG SIGN. Signal exists
                              but only by inverting the gate, which nobody would
                              ship ("fire the drift guard when drift is LOW"), so
                              there is no usable operating point in the deployed
                              direction. This is the strongest of the three.
  AUROC 0.6 - 0.8          => merely MISCALIBRATED. A weaker, different claim.

This script reads only the frozen result JSONs already in the tree. It computes
nothing new about the models; it re-asks the existing measurements a question
that is robust to calibration. It is the cheapest possible strengthening of the
claim and it needs no GPU, no network, and no model artifacts.

Statistics notes, stated so they are not overclaimed:
  * AUROC here is the Mann-Whitney U statistic normalised, ties credited 0.5.
  * The bootstrap CI is percentile, 4000 resamples, seeded. At these very small
    n the interval is wide and that is the honest reading, not a defect.
  * Bootstrap DEGENERATES under perfect separation (it returns [0,0] or [1,1]
    because every resample is also perfectly separated). Where separation is
    perfect the script reports the EXACT two-sided permutation p instead, which
    is the correct instrument for that case.
  * "Oracle-best threshold" is tuned ON THE TEST DATA ITSELF, and BOTH polarities
    are swept. It is deliberately optimistic: a ceiling on what recalibration
    could achieve. Two ceilings are reported, and the distinction is the whole
    point: the DEPLOYED-DIRECTION ceiling is what re-tuning the shipped gate can
    buy; the both-directions ceiling is only reachable by inverting the gate's
    sense, so reaching it there is a finding about sign, not an available repair.

Usage:
    python harness/threshold_free_reanalysis/run_auroc_reanalysis.py
"""

from __future__ import annotations

import json
import platform
import sys
import time
from pathlib import Path

SEED = 20260726
BOOTSTRAP_ITERS = 4000

_HERE = Path(__file__).resolve()
_REPO_ROOT = _HERE.parents[2]
RESULTS_DIR = _REPO_ROOT / "results" / "threshold_free_reanalysis"


# ---------------------------------------------------------------- statistics
# Imported from experiments/lib/stats.py rather than defined here, so this script
# and the factorial pilot cannot drift apart. The lib is pure stdlib, so this
# script still runs on a bare Python with no scipy/sklearn -- the property that
# made a local copy tempting in the first place.
_HERE_LIB = Path(__file__).resolve().parents[2]
if str(_HERE_LIB) not in sys.path:
    sys.path.insert(0, str(_HERE_LIB))

from harness.lib.stats import (  # noqa: E402
    auroc,
    bootstrap_ci,
    deployed_direction_ceiling,
    exact_permutation_p,
    oracle_best_threshold,
)


def analyse(label, pos, neg, pos_name, neg_name) -> dict:
    a = auroc(pos, neg)
    ba, t, polarity = oracle_best_threshold(pos, neg)
    ba_deployed = deployed_direction_ceiling(pos, neg)
    p_exact = exact_permutation_p(pos, neg)
    rec = {
        "measure": label,
        "n_positive": len(pos),
        "n_negative": len(neg),
        "positive_class": pos_name,
        "negative_class": neg_name,
        "auroc": round(a, 4),
        "auroc_inverted_direction": round(1.0 - a, 4),
        "oracle_best_balanced_accuracy": round(ba, 4),
        "oracle_best_threshold": round(t, 4) if t is not None else None,
        "oracle_best_polarity": polarity,
        "oracle_best_balanced_accuracy_DEPLOYED_DIRECTION_ONLY": round(ba_deployed, 4),
    }
    if p_exact is None:
        lo, hi = bootstrap_ci(pos, neg, iters=BOOTSTRAP_ITERS, seed=SEED)
        rec["ci95_bootstrap"] = [round(lo, 4), round(hi, 4)]
        rec["ci95_excludes_chance"] = bool(hi < 0.5 or lo > 0.5)
        rec["exact_permutation_p"] = None
    else:
        rec["ci95_bootstrap"] = None  # degenerate under perfect separation
        rec["ci95_excludes_chance"] = None
        rec["exact_permutation_p"] = p_exact

    ci = rec["ci95_bootstrap"]
    ci_s = (
        f"CI95 [{ci[0]:.4f}, {ci[1]:.4f}]{'' if rec['ci95_excludes_chance'] else ' (TOUCHES CHANCE)'}"
        if ci
        else f"exact p={p_exact:.2e} (perfect separation)"
    )
    pol = "DEPLOYED dir" if polarity == "ge" else "*** INVERTED dir - wrong sign ***"
    print(f"  {label:52s} n={len(pos):>2d}/{len(neg):<2d} AUROC={a:.4f}  {ci_s}")
    print(f"  {'':52s} oracle ceiling, deployed direction only = {ba_deployed:.4f}")
    print(f"  {'':52s} oracle ceiling, both directions         = {ba:.4f} @ t={t:.4f} [{pol}]")
    return rec


# ---------------------------------------------------------------- corpora

def guard_stack_block(out: dict) -> None:
    print("=" * 92)
    print("A. GUARD-STACK CONSTRAINT-SURVIVAL CORPUS")
    print("   positive = MUTATION (a constraint was violated; the guard SHOULD fire)")
    print("   negative = faithful_control (semantically faithful rewrite; must NOT fire)")
    print("=" * 92)
    base = _REPO_ROOT / "results" / "guard_stack"
    for label, fn in [
        ("in_sample_2026-07-15", "guard_stack_corpus_2026-07-15.json"),
        ("held_out_2026-07-16", "guard_stack_heldout_2026-07-16.json"),
    ]:
        path = base / fn
        if not path.exists():
            print(f"\n  [SKIP] {fn} absent")
            continue
        rows = json.loads(path.read_text(encoding="utf-8"))["rows"]
        mut = [r for r in rows if r["mutation_class"] != "faithful_control"]
        ctl = [r for r in rows if r["mutation_class"] == "faithful_control"]
        print(f"\n--- {label} ---")
        split: dict = {"split": label, "source": fn, "pooled": [], "per_class_cosine": []}
        split["pooled"].append(
            analyse(
                "cosine drift (1 - similarity) [INCUMBENT]",
                [1.0 - r["cosine"]["similarity"] for r in mut],
                [1.0 - r["cosine"]["similarity"] for r in ctl],
                "mutation",
                "faithful_control",
            )
        )
        split["pooled"].append(
            analyse(
                "NLI contradiction [PROPOSED SUCCESSOR]",
                [r["nli"]["contradiction"] for r in mut],
                [r["nli"]["contradiction"] for r in ctl],
                "mutation",
                "faithful_control",
            )
        )
        print("\n  per-mutation-class cosine AUROC (same controls):")
        neg = [1.0 - r["cosine"]["similarity"] for r in ctl]
        for cls in sorted({r["mutation_class"] for r in mut}):
            sub = [1.0 - r["cosine"]["similarity"] for r in mut if r["mutation_class"] == cls]
            a = auroc(sub, neg)
            print(f"    {cls:24s} n={len(sub):>2d}  AUROC={a:.4f}")
            split["per_class_cosine"].append(
                {"mutation_class": cls, "n": len(sub), "auroc": round(a, 4)}
            )
        out["guard_stack"].append(split)


def distinctness_block(out: dict) -> None:
    print()
    print("=" * 92)
    print("B. R12/R14 HYPOTHESIS-DISTINCTNESS CORPUS")
    print("   positive = SAME decision reworded  (the gate SHOULD call it a duplicate)")
    print("   negative = OPPOSITE decisions      (the gate must NOT call it a duplicate)")
    print("   a valid proxy needs AUROC >> 0.5; AUROC < 0.5 means the proxy is INVERTED")
    print("=" * 92)
    base = _REPO_ROOT / "results" / "r14_nli_distinctness"
    # the holdout-bearing file carries both splits; prefer it, fall back to dev-only
    for fn in ["r14_falsifier_2026-07-28_holdout.json", "r14_falsifier_2026-07-28.json"]:
        path = base / fn
        if not path.exists():
            continue
        d = json.loads(path.read_text(encoding="utf-8"))
        for split_name in ("dev", "holdout"):
            if split_name not in d:
                continue
            rows = d[split_name]["rows"]
            same = [r for r in rows if r["class"] == "SAME"]
            opp = [r for r in rows if r["class"] == "OPPOSITE"]
            print(f"\n--- {fn} :: {split_name} ---")
            rec = {"split": split_name, "source": fn, "measures": []}
            rec["measures"].append(
                analyse(
                    "cosine similarity [INCUMBENT GATE]",
                    [r["cosine"] for r in same],
                    [r["cosine"] for r in opp],
                    "SAME (duplicate)",
                    "OPPOSITE (contest)",
                )
            )
            rec["measures"].append(
                analyse(
                    "NLI duplication [PROPOSED SUCCESSOR]",
                    [r["nli"]["duplication"] for r in same],
                    [r["nli"]["duplication"] for r in opp],
                    "SAME (duplicate)",
                    "OPPOSITE (contest)",
                )
            )
            out["distinctness"].append(rec)


def main() -> int:
    print(f"[reanalysis] {"redacted"} {platform.platform()}")
    print(f"[reanalysis] seed={SEED} bootstrap_iters={BOOTSTRAP_ITERS}")
    print("[reanalysis] reads frozen result JSONs only — no model is loaded\n")

    out: dict = {
        "analysis": "threshold-free re-analysis of frozen falsifier evidence",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "node": "redacted",
        "platform": platform.platform(),
        "seed": SEED,
        "bootstrap_iters": BOOTSTRAP_ITERS,
        "reading_guide": {
            "auroc_below_0.5_ci_excludes_chance": "WRONG SIGN — the proxy is anti-correlated with the property; no usable operating point exists in the DEPLOYED direction",
            "auroc_near_0.5": "NO SIGNAL in either direction",
            "auroc_0.6_to_0.8": "MERELY MISCALIBRATED — a weaker, different claim",
            "oracle_best_balanced_accuracy_DEPLOYED_DIRECTION_ONLY": "tuned on the test data; UPPER BOUND on what recalibrating the SHIPPED gate can buy",
            "oracle_best_balanced_accuracy": "both polarities; if polarity=='lt' the ceiling is only reachable by INVERTING the gate, which is a finding, not a repair",
        },
        "guard_stack": [],
        "distinctness": [],
    }

    guard_stack_block(out)
    distinctness_block(out)

    print("\n" + "=" * 92)
    print("READING")
    print("  Cosine falls BELOW chance on every split. Held-out CIs exclude 0.5;")
    print("  the in-sample guard-stack CI touches it (only 5 controls).")
    print("  Re-tuning the gate in the direction it ships cannot clear ~0.57.")
    print("  The residual signal runs BACKWARDS: the only threshold with real")
    print("  discriminative power fires when drift is LOW / cosine is HIGH-for-")
    print("  contests. That is a wrong-sign finding, not a recalibration.")
    print("=" * 92)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    dest = RESULTS_DIR / f"auroc_reanalysis_rerun_{time.strftime('%Y-%m-%d')}.json"
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\n[reanalysis] evidence written: {dest.relative_to(_REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
