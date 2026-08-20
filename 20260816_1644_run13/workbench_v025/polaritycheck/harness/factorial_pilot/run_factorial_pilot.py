#!/usr/bin/env python3
"""Block A factorial pilot — does cosine still fail once lexical overlap is balanced?

THE QUESTION THIS EXISTS TO SETTLE
----------------------------------
Every prior result in this repository compares OPPOSITE-decision pairs that are
lexically near-identical against SAME-decision pairs that are full rewrites. So
lexical overlap is perfectly confounded with the class label, and the measured
inversion (AUROC 0.0000) is partly a property of the corpus design. A reviewer
says this first, and they are right to.

The 2x2 decouples the two factors:

                    lexically CLOSE      lexically DISTANT
    opposite/violation    cell A                cell B
    same/faithful         cell C                cell D

with the SAME anchor text in all four cells, so the anchor is controlled.

That yields two questions instead of one, and the contrast between the answers is
the finding:

  DECISION AXIS, within a lexical stratum  -- can cosine tell OPPOSITE from SAME
      when surface overlap is held roughly constant? A>C within CLOSE, B>D within
      DISTANT. This is the property the gate is deployed to enforce.
  LEXICAL AXIS, within a decision stratum  -- can cosine tell CLOSE from DISTANT
      when the decision is held constant? A>B within OPPOSITE, C>D within SAME.
      This is the POSITIVE CONTROL: it should be strong.

The paper's claim, if it survives, is the contrast: cosine scores near 1.0 on the
axis nobody asked about and near 0.5 on the axis the gate exists to enforce. That
is much harder to attack than a single inverted contrast, because "recalibrate it"
and "your corpus was confounded" are both already answered.

PRE-REGISTERED DECISION RULE (committed before any encoder ran)
-------------------------------------------------------------------------------
Primary outcome: decision-axis AUROC within each lexical stratum.

    <= 0.55  -> CLAIM HOLDS. Cosine is blind to the decision axis with the
                confounder balanced. Block B authorised.
    >= 0.70  -> CLAIM SHRINKS. The inversion was largely a corpus artefact; the
                honest finding becomes "cosine tracks lexical overlap, which is
                confounded with polarity in naturally-occurring pairs." Publish
                the smaller claim; reclaim ten weeks.
    between  -> INCONCLUSIVE AT PILOT n. Expand the corpus before deciding.

Written down before the encoder was run. At n=10 per cell the confidence intervals
will be wide, and that is the honest reading: this pilot is powered to detect a
gross effect, not to estimate one.

MANIPULATION CHECK RUNS FIRST, and can invalidate the whole run
--------------------------------------------------------------
Before any encoder loads:
  1. Do the assigned CLOSE/DISTANT labels separate on MEASURED overlap? Must be
     high or the lexical axis is fiction.
  2. Is measured overlap BALANCED across the decision axis within each stratum?
     This is the decoupling. If overlap still differs between A and C, the
     confound survived the redesign and no encoder number from this corpus means
     anything.

Usage:
    python harness/factorial_pilot/run_factorial_pilot.py
    python harness/factorial_pilot/run_factorial_pilot.py --task distinctness
"""

from __future__ import annotations

import argparse
import json
import platform
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve()
_REPO_ROOT = _HERE.parents[2]
for _p in (str(_REPO_ROOT),):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from harness.factorial_pilot import encoders as enc_registry  # noqa: E402
from harness.factorial_pilot.lexical import PRIMARY_METRIC, all_metrics  # noqa: E402
from harness.lib import stats  # noqa: E402

CORPUS_DIR = _REPO_ROOT / "corpus"
RESULTS_DIR = _REPO_ROOT / "results" / "factorial_pilot"

# decision-axis class names per task: (positive_for_similarity, negative)
# positive = the class a similarity gate SHOULD score higher (the duplicate /
# faithful side); negative = the class it must score lower.
AXIS = {
    "distinctness": {"pos": "SAME", "neg": "OPPOSITE", "file": "distinctness_2x2.jsonl"},
    "constraint": {"pos": "FAITHFUL", "neg": "VIOLATION", "file": "constraint_2x2.jsonl"},
}

HOLDS, SHRINKS = 0.55, 0.70

# Cosine thresholds found in SHIPPED code and vendor guidance by the prevalence
# survey (survey/prevalence_survey_2026-07-26.md). Not chosen by us, and not
# fitted to anything -- these are constants other people typed into gates.
SHIPPED_THRESHOLDS = [
    (0.30, "innovation64/BMAM long_term_memory"),
    (0.40, "innovation64/BMAM; the audited system's advertised config drift_threshold"),
    (0.80, "the audited system's EFFECTIVE gate boundary (cos < 0.80); framework defaults"),
    (0.85, "the audited system's shipped duplicate-gate threshold; neuralmind REVIEW_FLAG; "
           "vendor guidance 'cosine distance > 0.15'"),
    (0.95, "AG3NT DEDUP_SIMILARITY_THRESHOLD; Maria DEFAULT_SEMANTIC_THRESHOLD; "
           "neuralmind AUTO_MERGE_THRESHOLD"),
]


def load(task: str) -> list[dict]:
    path = CORPUS_DIR / AXIS[task]["file"]
    rows = [json.loads(ln) for ln in path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    for r in rows:
        r["lexical_metrics"] = all_metrics(r["text_a"], r["text_b"])
        r["overlap"] = r["lexical_metrics"][PRIMARY_METRIC]
    return rows


def sel(rows, **kw):
    return [r for r in rows if all(r[k] == v for k, v in kw.items())]


# ---------------------------------------------------------------- manipulation


def manipulation_check(rows: list[dict], task: str) -> dict:
    pos, neg = AXIS[task]["pos"], AXIS[task]["neg"]
    print(f"\n{'-' * 78}\nMANIPULATION CHECK ({task}) — validating the DESIGN before the encoder")
    print(f"{'-' * 78}")

    out: dict = {"primary_metric": PRIMARY_METRIC, "cells": {}}
    print(f"\n  measured {PRIMARY_METRIC} by cell:")
    for cell, dec, lex in [("A", neg, "CLOSE"), ("B", neg, "DISTANT"),
                           ("C", pos, "CLOSE"), ("D", pos, "DISTANT")]:
        sub = sel(rows, decision=dec, lexical=lex)
        vals = [r["overlap"] for r in sub]
        mean = sum(vals) / len(vals)
        out["cells"][cell] = {
            "decision": dec, "lexical": lex, "n": len(sub),
            "mean_overlap": round(mean, 4),
            "min": round(min(vals), 4), "max": round(max(vals), 4),
        }
        print(f"    {cell}  {dec:<9s} x {lex:<7s} n={len(sub):>2d}  "
              f"mean={mean:.4f}  range [{min(vals):.4f}, {max(vals):.4f}]")

    # (1) does the assigned lexical label separate on measured overlap?
    close = [r["overlap"] for r in sel(rows, lexical="CLOSE")]
    distant = [r["overlap"] for r in sel(rows, lexical="DISTANT")]
    lab = stats.summarise("assigned CLOSE vs DISTANT, on measured overlap",
                          close, distant, "CLOSE", "DISTANT")
    out["lexical_labels_separate"] = lab
    print(f"\n  (1) the lexical axis is real, not asserted:")
    print(stats.fmt(lab))
    ok1 = lab["auroc"] >= 0.9
    print(f"      -> {'PASS' if ok1 else 'FAIL'} (need AUROC >= 0.90)")

    # (2) THE DECOUPLING: is overlap balanced across the decision axis?
    print(f"\n  (2) THE DECOUPLING — is overlap balanced across the decision axis")
    print(f"      within each lexical stratum? A NON-significant difference is what")
    print(f"      we want; a significant one means the confound survived.")
    out["balance"] = {}
    ok2 = True
    for lex in ("CLOSE", "DISTANT"):
        a = [r["overlap"] for r in sel(rows, lexical=lex, decision=neg)]
        b = [r["overlap"] for r in sel(rows, lexical=lex, decision=pos)]
        t = stats.permutation_test_mean_diff(a, b)
        out["balance"][lex] = t
        flag = "balanced" if t["p_two_sided"] > 0.05 else "*** IMBALANCED ***"
        ok2 &= t["p_two_sided"] > 0.05
        print(f"      {lex:<7s} mean({neg})={t['mean_a']:.4f} vs mean({pos})={t['mean_b']:.4f}"
              f"  diff={t['observed_diff']:.4f}  perm p={t['p_two_sided']:.4f}  {flag}")

    out["design_valid"] = bool(ok1 and ok2)
    print(f"\n  DESIGN VALID: {out['design_valid']}"
          + ("" if out["design_valid"] else "   <-- encoder results below are NOT interpretable"))

    # annotator agreement, when a second labeller has filled the slots
    ind = [r for r in rows if r.get("independent_decision_label")]
    if ind:
        out["kappa_decision"] = stats.cohens_kappa(
            [r["decision"] for r in ind], [r["independent_decision_label"] for r in ind])
        out["kappa_lexical"] = stats.cohens_kappa(
            [r["lexical"] for r in ind],
            [r["independent_lexical_label"] for r in ind if r.get("independent_lexical_label")])
        print(f"\n  annotator agreement (n={len(ind)}): "
              f"decision kappa={out['kappa_decision'].get('kappa')}")
    else:
        out["kappa_decision"] = None
        print("\n  annotator agreement: NOT AVAILABLE — no independent labels yet."
              "\n    Gate 3 is open. Fill `independent_decision_label` /"
              " `independent_lexical_label`\n    in the corpus JSONL and re-run; kappa"
              " computes automatically.")
    return out


# ------------------------------------------------------------------- encoder run


def measure(rows: list[dict], task: str, encoder) -> dict:
    pos, neg = AXIS[task]["pos"], AXIS[task]["neg"]
    cos = encoder.cosines([(r["text_a"], r["text_b"]) for r in rows])
    for r, c in zip(rows, cos):
        r["_cos"] = c

    def c(**kw):
        return [r["_cos"] for r in sel(rows, **kw)]

    res: dict = {"encoder": encoder.name, "family": encoder.family, "cell_mean_cosine": {}}

    print(f"\n  2x2 mean cosine:")
    print(f"    {'':<12s} {'CLOSE':>10s} {'DISTANT':>10s}")
    for dec in (neg, pos):
        cl, di = c(decision=dec, lexical="CLOSE"), c(decision=dec, lexical="DISTANT")
        res["cell_mean_cosine"][dec] = {
            "CLOSE": round(sum(cl) / len(cl), 4), "DISTANT": round(sum(di) / len(di), 4)}
        print(f"    {dec:<12s} {sum(cl) / len(cl):>10.4f} {sum(di) / len(di):>10.4f}")

    # --- PRIMARY: decision axis within each lexical stratum -----------------
    print(f"\n  PRIMARY OUTCOME — decision axis ({pos} should score HIGHER than {neg}),")
    print(f"  measured WITHIN each lexical stratum so overlap cannot do the work:")
    res["decision_axis_within_lexical"] = {}
    for lex in ("CLOSE", "DISTANT"):
        rec = stats.summarise(f"decision axis | lexical={lex}",
                              c(decision=pos, lexical=lex), c(decision=neg, lexical=lex),
                              pos, neg)
        res["decision_axis_within_lexical"][lex] = rec
        print(stats.fmt(rec))

    # stratified: average of the within-stratum AUROCs, equal cell sizes
    aur = [res["decision_axis_within_lexical"][k]["auroc"] for k in ("CLOSE", "DISTANT")]
    res["decision_axis_stratified_auroc"] = round(sum(aur) / len(aur), 4)
    print(f"\n    STRATIFIED decision-axis AUROC (mean of strata) = "
          f"{res['decision_axis_stratified_auroc']:.4f}   [chance = 0.5000]")

    # --- POSITIVE CONTROL: lexical axis within each decision stratum --------
    print(f"\n  POSITIVE CONTROL — lexical axis (CLOSE should score HIGHER than DISTANT),")
    print(f"  measured WITHIN each decision stratum. Strong here = the measure is not")
    print(f"  noise, it is measuring the wrong thing:")
    res["lexical_axis_within_decision"] = {}
    for dec in (neg, pos):
        rec = stats.summarise(f"lexical axis | decision={dec}",
                              c(decision=dec, lexical="CLOSE"),
                              c(decision=dec, lexical="DISTANT"), "CLOSE", "DISTANT")
        res["lexical_axis_within_decision"][dec] = rec
        print(stats.fmt(rec))
    lex_aur = [res["lexical_axis_within_decision"][d]["auroc"] for d in (neg, pos)]
    res["lexical_axis_stratified_auroc"] = round(sum(lex_aur) / len(lex_aur), 4)
    print(f"\n    STRATIFIED lexical-axis AUROC = {res['lexical_axis_stratified_auroc']:.4f}")

    # --- what the CONFOUNDED design would have reported ---------------------
    naive = stats.summarise(
        "NAIVE pooled decision axis (confounded)",
        c(decision=pos, lexical="DISTANT"), c(decision=neg, lexical="CLOSE"), pos, neg)
    res["naive_confounded_auroc"] = naive
    print(f"\n  For comparison — what the OLD confounded design measures on this same")
    print(f"  corpus (cell D vs cell A, the historical setup):")
    print(stats.fmt(naive))

    res["confound_inflation"] = round(
        abs(naive["auroc"] - res["decision_axis_stratified_auroc"]), 4)
    print(f"\n    gap between confounded and stratified = {res['confound_inflation']:.4f}"
          f"  <- how much of the historical result was the confounder")

    # --- CAN ONE FIXED THRESHOLD SERVE A REAL GATE? -------------------------
    # A deployed gate has ONE number and does not know which lexical stratum the
    # pair in front of it belongs to. So the honest ceiling is not the mean of
    # per-stratum ceilings -- it is the best SINGLE threshold across both strata.
    # The gap between them is the price of not knowing the confounder at runtime,
    # and it is the number a practitioner actually needs.
    pooled_pos = c(decision=pos)
    pooled_neg = c(decision=neg)
    single_ba, single_t, single_pol = stats.oracle_best_threshold(pooled_pos, pooled_neg)
    per_stratum = {}
    for lex in ("CLOSE", "DISTANT"):
        ba, t, _ = stats.oracle_best_threshold(c(decision=pos, lexical=lex),
                                               c(decision=neg, lexical=lex))
        per_stratum[lex] = {"balanced_accuracy": round(ba, 4), "threshold": round(t, 6)}
    mean_stratum_ba = sum(v["balanced_accuracy"] for v in per_stratum.values()) / 2
    res["one_threshold_reality_check"] = {
        "single_global_threshold": {
            "balanced_accuracy": round(single_ba, 4),
            "threshold": round(single_t, 6),
            "polarity": single_pol,
        },
        "per_stratum_oracle": per_stratum,
        "mean_per_stratum_balanced_accuracy": round(mean_stratum_ba, 4),
        "cost_of_one_threshold": round(mean_stratum_ba - single_ba, 4),
        "threshold_spread_between_strata": round(
            abs(per_stratum["CLOSE"]["threshold"] - per_stratum["DISTANT"]["threshold"]), 6),
    }
    # --- AND WHAT DO THE ACTUALLY-SHIPPED THRESHOLDS ACHIEVE? ---------------
    # The oracle single threshold above is fitted on this data and is therefore
    # generous. Deployed gates do not use an oracle -- they use a constant someone
    # typed. These are the constants the prevalence survey actually found in
    # shipped code and vendor guidance, and this is the number a practitioner
    # recognises. Reported so the claim is about real gates, not ideal ones.
    res["shipped_threshold_performance"] = []
    for thr, prov in SHIPPED_THRESHOLDS:
        tpr = sum(v >= thr for v in pooled_pos) / len(pooled_pos)
        tnr = sum(v < thr for v in pooled_neg) / len(pooled_neg)
        res["shipped_threshold_performance"].append({
            "threshold": thr, "provenance": prov,
            "balanced_accuracy": round((tpr + tnr) / 2, 4),
            "true_positive_rate": round(tpr, 4), "true_negative_rate": round(tnr, 4),
        })
    print(f"\n  AT THE THRESHOLDS ACTUALLY SHIPPED (not oracle-fitted) — balanced accuracy")
    print(f"  on the decision axis, pooled across strata as a real gate would see it:")
    for s in res["shipped_threshold_performance"]:
        print(f"    cos >= {s['threshold']:.2f}  bal-acc {s['balanced_accuracy']:.4f}  "
              f"(TPR {s['true_positive_rate']:.2f} / TNR {s['true_negative_rate']:.2f})   {s['provenance']}")
    best_shipped = max(s["balanced_accuracy"] for s in res["shipped_threshold_performance"])
    res["best_shipped_threshold_balanced_accuracy"] = round(best_shipped, 4)
    print(f"    best of the shipped constants: {best_shipped:.4f}   [chance = 0.5000]")

    r = res["one_threshold_reality_check"]
    print(f"\n  ONE-THRESHOLD REALITY CHECK — a deployed gate has one number and does")
    print(f"  not know which stratum a pair is in. All thresholds fitted on this data:")
    print(f"    best per-stratum:  CLOSE  bal-acc {per_stratum['CLOSE']['balanced_accuracy']:.4f} "
          f"@ cos={per_stratum['CLOSE']['threshold']:.4f}")
    print(f"                       DISTANT bal-acc {per_stratum['DISTANT']['balanced_accuracy']:.4f} "
          f"@ cos={per_stratum['DISTANT']['threshold']:.4f}")
    print(f"    the two optimal thresholds differ by {r['threshold_spread_between_strata']:.4f} cosine")
    print(f"    best SINGLE global threshold: bal-acc {r['single_global_threshold']['balanced_accuracy']:.4f} "
          f"@ cos={r['single_global_threshold']['threshold']:.4f}")
    print(f"    cost of having only one threshold = {r['cost_of_one_threshold']:+.4f} balanced accuracy")
    return res


def verdict(per_encoder: list[dict]) -> dict:
    """Apply the pre-registered rule to the stratified decision-axis AUROC."""
    vals = [e["decision_axis_stratified_auroc"] for e in per_encoder]
    worst = max(vals)  # the least favourable to our claim
    if worst <= HOLDS:
        v, action = "CLAIM HOLDS", "Block B authorised."
    elif worst >= SHRINKS:
        v, action = "CLAIM SHRINKS", "Publish the smaller claim; reclaim ten weeks."
    else:
        v, action = "INCONCLUSIVE AT PILOT n", "Expand the corpus before deciding."
    return {
        "rule": f"<= {HOLDS} holds; >= {SHRINKS} shrinks; between = inconclusive",
        "pre_registered": True,
        "stratified_decision_auroc_by_encoder": {
            e["encoder"]: e["decision_axis_stratified_auroc"] for e in per_encoder},
        "least_favourable": worst,
        "verdict": v,
        "action": action,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--task", choices=["distinctness", "constraint", "both"], default="both")
    args = ap.parse_args()
    tasks = ["distinctness", "constraint"] if args.task == "both" else [args.task]

    print("=" * 78)
    print("BLOCK A FACTORIAL PILOT")
    print(f"  {"redacted"}  {platform.platform()}")
    print("=" * 78)

    ready, absent = enc_registry.resolve()
    print(f"\nENCODERS: {len(ready)} available, {len(absent)} absent")
    for e in ready:
        print(f"  [ready ] {e.family:8s} {e.name}")
    for n, why in absent:
        print(f"  [ABSENT] {n}\n             {why}")
    if not ready:
        print("\nNo encoder available — cannot run.")
        return 1
    if len(ready) < 3:
        print(f"\n  !! GATE 1 NOT SATISFIED: {len(ready)} encoder(s). One checkpoint failing is")
        print("     not a claim about embeddings. This run is a DESIGN test and a")
        print("     single-encoder reading, not the multi-encoder evidence the paper needs.")

    out: dict = {
        "experiment": "block-a factorial pilot (2x2: decision axis x lexical axis)",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "node": "redacted", "platform": platform.platform(),
        "primary_metric": PRIMARY_METRIC,
        "decision_rule": {"holds_at_or_below": HOLDS, "shrinks_at_or_above": SHRINKS,
                          "pre_registered_before_any_encoder_ran": True},
        "encoders_available": [e.name for e in ready],
        "encoders_absent": [{"name": n, "why": w} for n, w in absent],
        "gate1_satisfied": len(ready) >= 6,
        "tasks": {},
    }

    for task in tasks:
        rows = load(task)
        print(f"\n\n{'=' * 78}\nTASK: {task}   ({len(rows)} pairs, {len(rows) // 4} matched anchors x 4 cells)")
        print("=" * 78)
        block: dict = {"n_pairs": len(rows), "n_anchors": len(rows) // 4}
        block["manipulation_check"] = manipulation_check(rows, task)

        block["per_encoder"] = []
        for e in ready:
            print(f"\n{'-' * 78}\nENCODER: {e.name}\n{'-' * 78}")
            block["per_encoder"].append(measure(rows, task, e))
        block["verdict"] = verdict(block["per_encoder"])
        print(f"\n  {'=' * 74}")
        print(f"  VERDICT ({task}): {block['verdict']['verdict']}")
        print(f"    least-favourable stratified decision AUROC = {block['verdict']['least_favourable']:.4f}")
        print(f"    rule (pre-registered): {block['verdict']['rule']}")
        print(f"    action: {block['verdict']['action']}")
        print(f"  {'=' * 74}")
        block["per_row"] = [
            {k: r[k] for k in ("id", "cell", "decision", "lexical", "anchor_group",
                               "subclass", "text_a", "text_b", "lexical_metrics")}
            for r in rows
        ]
        out["tasks"][task] = block

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    dest = RESULTS_DIR / f"factorial_pilot_rerun_{time.strftime('%Y-%m-%d')}.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[pilot] evidence written: {dest.relative_to(_REPO_ROOT)}")

    if not out["gate1_satisfied"]:
        print("[pilot] REMINDER: Gate 1 needs 6+ encoders. See encoders.py to add them.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
