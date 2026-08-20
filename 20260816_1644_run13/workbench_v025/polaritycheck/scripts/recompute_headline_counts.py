#!/usr/bin/env python3
"""Recompute the paper's headline counts from the FROZEN results. No models needed.

Checks, against the frozen JSON shipped in ``results/``:

  1. §3 — the naive confounded design returns decision AUROC exactly 0.000 in
     13 of 18 encoder-task cells, and <= 0.040 in all 18.
  2. §3 — with lexical overlap held constant, reversal moves the embedding MORE
     than restatement in 29 of 36 encoder-task-stratum comparisons (recomputed
     from the frozen per-cell mean cosines).
  3. §5 — stratified decision AUROC spans 0.490–0.8075 (distinctness) and
     0.440–0.815 (constraint); the production configuration scores 0.535/0.440.
  4. §6 — the audited drift guard (threshold 0.4 on drift) fired on 0 of 56
     meaning-breaking mutations across the two corpora, and the
     withhold->administer specimen scores cosine 0.9608.
  5. §7 — the NLI drop-in's frozen AUROC: 0.831 in-sample, 0.533 held-out.
  6. §7 — the repair arms' balanced accuracies: encoder swap 0.485/0.433;
     conditioned gate 0.750 in-sample vs 0.533 held-out.

Exit code 0 iff every check passes.

Usage:
    python scripts/recompute_headline_counts.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
RESULTS = REPO_ROOT / "results"

failures: list[str] = []


def check(label: str, cond: bool, detail: str = "") -> None:
    tag = "PASS" if cond else "FAIL"
    print(f"  [{tag}] {label}" + (f"  --  {detail}" if detail else ""))
    if not cond:
        failures.append(label)


def load(rel: str) -> dict:
    return json.loads((RESULTS / rel).read_text(encoding="utf-8"))


# Per-task class names in the factorial corpus: (reversal side, restatement side)
CLASSES = {
    "distinctness": ("OPPOSITE", "SAME"),
    "constraint": ("VIOLATION", "FAITHFUL"),
}
PRODUCTION = "nomic-embed-text-v1.5 MRL-256 [PRODUCTION PATH, search_document:]"


def main() -> int:
    print("=" * 78)
    print("HEADLINE COUNTS, RECOMPUTED FROM FROZEN RESULTS (no models loaded)")
    print("=" * 78)

    fp = load("factorial_pilot/factorial_pilot_2026-07-26.json")

    # ------------------------------------------------------------- 1. 13 of 18
    print("\n1. The naive confounded design (frozen `naive_confounded_auroc` per cell):")
    zero, le, tot, mx = 0, 0, 0, 0.0
    for task in CLASSES:
        for pe in fp["tasks"][task]["per_encoder"]:
            a = pe["naive_confounded_auroc"]["auroc"]
            tot += 1
            mx = max(mx, a)
            zero += a == 0.0
            le += a <= 0.040
    check("naive AUROC exactly 0.000 in 13 of 18 cells", zero == 13 and tot == 18,
          f"{zero} of {tot}")
    check("naive AUROC <= 0.040 in all 18 cells", le == 18, f"{le} of {tot}, max {mx}")

    # ------------------------------------------------------------- 2. 29 of 36
    print("\n2. Matched-overlap direction (frozen per-cell mean cosines):")
    n_more, total = 0, 0
    for task, (rev_k, res_k) in CLASSES.items():
        for pe in fp["tasks"][task]["per_encoder"]:
            for stratum in ("CLOSE", "DISTANT"):
                total += 1
                # reversal moves MORE == its mean cosine is LOWER at matched overlap
                if pe["cell_mean_cosine"][rev_k][stratum] < pe["cell_mean_cosine"][res_k][stratum]:
                    n_more += 1
    check("reversal moves the embedding MORE than restatement in 29 of 36 "
          "encoder-task-stratum comparisons", n_more == 29 and total == 36,
          f"{n_more} of {total}")

    # ------------------------------------------- 3. stratified AUROC field + production
    print("\n3. The decision-axis field (frozen stratified AUROC):")
    for task, (lo_expect, hi_expect) in (("distinctness", (0.490, 0.8075)),
                                         ("constraint", (0.440, 0.815))):
        vals = {pe["encoder"]: pe["decision_axis_stratified_auroc"]
                for pe in fp["tasks"][task]["per_encoder"]}
        check(f"{task}: stratified decision AUROC spans {lo_expect}-{hi_expect}",
              min(vals.values()) == lo_expect and max(vals.values()) == hi_expect,
              f"observed {min(vals.values())}-{max(vals.values())}")
    prod_d = next(pe for pe in fp["tasks"]["distinctness"]["per_encoder"]
                  if pe["encoder"] == PRODUCTION)["decision_axis_stratified_auroc"]
    prod_c = next(pe for pe in fp["tasks"]["constraint"]["per_encoder"]
                  if pe["encoder"] == PRODUCTION)["decision_axis_stratified_auroc"]
    check("production configuration at 0.535 / 0.440", (prod_d, prod_c) == (0.535, 0.440),
          f"observed {prod_d} / {prod_c}")

    # ------------------------------------------------------------- 4. 0 of 56
    print("\n4. The audited drift guard (frozen guard-stack evidence):")
    fired = n_mut = 0
    for rel in ("guard_stack/guard_stack_corpus_2026-07-26.json",
                "guard_stack/guard_stack_heldout_2026-07-26.json"):
        rows = load(rel)["rows"]
        muts = [r for r in rows if r["mutation_class"] != "faithful_control"]
        n_mut += len(muts)
        fired += sum(r["cosine"]["caught"] for r in muts)
    check("drift guard fired on 0 of 56 meaning-breaking mutations",
          fired == 0 and n_mut == 56, f"{fired} of {n_mut}")
    ho = load("guard_stack/guard_stack_heldout_2026-07-26.json")["rows"]
    specimen = next(r for r in ho if r["root"].startswith("Withhold the study drug"))
    check("withhold->administer specimen scores cosine 0.9608",
          specimen["cosine"]["similarity"] == 0.9608,
          f"observed {specimen['cosine']['similarity']}, caught={specimen['cosine']['caught']}")

    # ------------------------------------------------------------- 5. NLI row
    print("\n5. The NLI drop-in (frozen threshold-free reanalysis):")
    re_ = load("threshold_free_reanalysis/auroc_reanalysis_2026-07-28.json")
    nli = {}
    for split in re_["guard_stack"]:
        for m in split["pooled"]:
            if m["measure"].startswith("NLI"):
                nli[split["split"]] = m
    check("NLI AUROC 0.8308 in-sample",
          nli["in_sample_2026-07-15"]["auroc"] == 0.8308,
          f"observed {nli['in_sample_2026-07-15']['auroc']}")
    check("NLI AUROC 0.5333 held-out, CI [0.36, 0.7067]",
          nli["held_out_2026-07-16"]["auroc"] == 0.5333
          and nli["held_out_2026-07-16"]["ci95_bootstrap"] == [0.36, 0.7067],
          f"observed {nli['held_out_2026-07-16']['auroc']} "
          f"CI {nli['held_out_2026-07-16']['ci95_bootstrap']}")

    # ------------------------------------------------------------- 6. repairs
    print("\n6. The repair arms (frozen H2 intervention results):")
    h2 = load("h2_intervention/h2_intervention_2026-07-27.json")["arms"]
    i1 = h2["I1_mxbai_cosine_only"]
    i2 = h2["I2_mxbai_confound_aware"]
    check("encoder swap (I1): 0.485 in-sample / 0.433 held-out",
          round(i1["in_sample"]["balanced_accuracy"], 3) == 0.485
          and round(i1["held_out"]["balanced_accuracy"], 3) == 0.433,
          f"observed {i1['in_sample']['balanced_accuracy']} / {i1['held_out']['balanced_accuracy']}")
    check("conditioned gate (I2): 0.750 in-sample / 0.533 held-out",
          round(i2["in_sample"]["balanced_accuracy"], 3) == 0.750
          and round(i2["held_out"]["balanced_accuracy"], 3) == 0.533,
          f"observed {i2['in_sample']['balanced_accuracy']} / {i2['held_out']['balanced_accuracy']}")

    print("\n" + "=" * 78)
    if failures:
        print(f"RESULT: {len(failures)} CHECK(S) FAILED")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("RESULT: ALL HEADLINE COUNTS RECOMPUTE FROM THE FROZEN RESULTS.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
