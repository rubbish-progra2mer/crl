#!/usr/bin/env python3
"""The hypothesis-distinctness probe: cosine gate vs NLI cross-encoder (§3, §7).

The claim under test:

    "NLI classification is a polarity-valid distinctness proxy: hypothesis pairs
    that decide OPPOSITE things read as contradiction (maximally distinct), and
    the SAME decision reworded reads as bidirectional entailment (duplicate)."

Framing: FALSIFIER, not certifier. This probe can KILL the claim (separation
<= 0, or the fatal error class: genuine contests judged DUPLICATE). A pass
certifies nothing beyond this corpus.

Probe purity: this file never tunes either proxy. It calls the NLI classifier
exactly as shipped (argmax verdicts, no thresholds), and the production
embedder exactly as shipped (``MRLEmbeddingRouter.batch_embed`` — the same
path the audited duplicate gate consumes).

Corpus provenance — honest note. The original 16-pair corpus was run from a
scratch script that was never committed; only 5 pairs survive verbatim in the
original report. The DEV corpus below therefore carries those 5 verbatim pairs
plus 11 reconstructed in the same adversarial style (each tagged
``verbatim``/``reconstructed``). To keep the old-vs-new comparison
apples-to-apples, this probe RE-RUNS the cosine baseline on this exact corpus
rather than citing the earlier numbers. Pair texts reference the audited
system's own components and infrastructure by name: they are that project's
real hypothesis contests, kept verbatim because editing them would change the
experiment.

Hold-out discipline ("widen it, but do not tune against it"): the HOLDOUT set —
including the hardest classes: antonyms with no negation word, and SAME
decisions where only one side uses negation — is run via ``--holdout``, once,
after the probe is final. Neither proxy has a tunable threshold, so the
hold-out guards the *author*, not the model.

Old-gate simulation: ``cos > 0.85`` (the audited system's shipped
duplicate-gate threshold, read from its production source) => "duplicate" —
reproduced here on the same pairs so both proxies face identical evidence.

Usage:
    python harness/r14_nli_distinctness/run_r14_falsifier.py
    python harness/r14_nli_distinctness/run_r14_falsifier.py --holdout
"""

from __future__ import annotations

import argparse
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
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from harness.audited_system import (  # noqa: E402
    DEFAULT_MODEL_ID,
    DEFAULT_MODEL_REVISION,
    DUPLICATE_GATE_THRESHOLD,
    VERDICT_CONTRADICTS,
    VERDICT_DUPLICATE,
    TransformersNLIClassifier,
    pair_polarity,
)

RESULTS_DIR = _REPO_ROOT / "results" / "r14_nli_distinctness"

# --------------------------------------------------------------------------
# Corpus. class OPPOSITE = the two texts decide opposite things (maximally
# distinct hypotheses — the gate must let them through). class SAME = one
# decision, reworded (genuine duplicates — the gate must catch them).
# provenance: "verbatim" = quoted verbatim from the original report;
# "reconstructed" = rebuilt in the same adversarial style for this probe.
# Release note: internal host/system names in pair texts were renamed
# like-for-like before the public re-run (see README, "Redaction");
# "verbatim" refers to the original sentence shape under those renames.
# --------------------------------------------------------------------------

DEV_PAIRS = [
    # --- OPPOSITE (8) ---
    ("OPPOSITE", "verbatim", "Ship the release now.", "Do not ship the release now."),
    ("OPPOSITE", "verbatim", "Retire the Crucible pipeline.", "Keep the Crucible pipeline."),
    # The original report truncates this pair with an ellipsis; the head words are verbatim.
    ("OPPOSITE", "reconstructed", "Increase the drift threshold.", "Decrease the drift threshold."),
    ("OPPOSITE", "reconstructed", "Merge the branch to main today.", "Do not merge the branch to main today."),
    ("OPPOSITE", "reconstructed", "Enable the cosine gate in production.", "Disable the cosine gate in production."),
    ("OPPOSITE", "reconstructed", "Route all inference to the local fleet.", "Route no inference to the local fleet."),
    ("OPPOSITE", "reconstructed", "Trust the declared diversity axes.", "Never trust the declared diversity axes."),
    ("OPPOSITE", "reconstructed", "Give the worker a larger context window.", "Give the worker a smaller context window."),
    # --- SAME (8) ---
    ("SAME", "verbatim", "Halt the release until the scorer is fixed.", "Block shipping pending repair of the ambiguity module."),
    ("SAME", "verbatim", "Give each agent a smaller context window.", "Trim the prompt budget allocated per worker."),
    ("SAME", "reconstructed", "Escalate this decision to the operator.", "Route the call up to the human operator for a verdict."),
    ("SAME", "reconstructed", "Cache the embeddings on disk.", "Persist the vector representations to local storage."),
    ("SAME", "reconstructed", "Run the falsifier before trusting the component.", "Execute the disconfirming probe prior to relying on the new module."),
    ("SAME", "reconstructed", "Restart the relay node tonight.", "Reboot the relay machine this evening."),
    ("SAME", "reconstructed", "Write the findings into a report file in the repo.", "Persist the findings as a document inside the repository."),
    ("SAME", "reconstructed", "Use a smaller model for the router.", "Adopt a more compact model to do the routing."),
]

HOLDOUT_PAIRS = [
    # --- OPPOSITE (4) — incl. the classes geometry fails worst on ---
    ("OPPOSITE", "holdout", "It is safe to arm the gate.", "Arming the gate is dangerous."),  # antonym, no negation word
    ("OPPOSITE", "holdout", "Centralize all logging on the archive host.", "Scatter the logs across every node."),  # antonym verbs
    ("OPPOSITE", "holdout", "The scorer fix must land before the polarity module.", "The polarity module must land before the scorer fix."),  # order inversion
    ("OPPOSITE", "holdout", "Keep the test suite fully synchronous.", "Make the test suite fully asynchronous."),
    # --- SAME (4) — incl. negation on ONE side only (the hardest duplicate) ---
    ("SAME", "holdout", "Do not ship until the scorer is fixed.", "Hold the release back while the scorer remains broken."),
    ("SAME", "holdout", "We should not delete the legacy anchors yet.", "Keep the legacy anchors for now."),
    ("SAME", "holdout", "Pin the model revision in the config.", "Freeze the exact model version in the configuration."),
    ("SAME", "holdout", "Every open loop needs its own file.", "Each unresolved thread must get a durable home on disk."),
]


def mean(xs: list[float]) -> float:
    return sum(xs) / len(xs) if xs else float("nan")


def run_probe(pairs, embedder, classifier) -> dict:
    """Both proxies over one corpus. Returns the full evidence dict."""
    rows = []
    for klass, provenance, a, b in pairs:
        # --- OLD proxy: production embedding path (batch_embed = what the
        # audited duplicate gate calls), cosine of the L2-normalised vectors.
        va, vb = embedder.batch_embed([a, b])
        cos = float((va * vb).sum())
        old_verdict_duplicate = cos > DUPLICATE_GATE_THRESHOLD

        # --- NEW proxy: the pinned NLI classifier, both directions.
        pp = pair_polarity(a, b, classifier)
        rows.append(
            {
                "class": klass,
                "provenance": provenance,
                "a": a,
                "b": b,
                "cosine": round(cos, 4),
                "old_gate_says_duplicate": old_verdict_duplicate,
                "nli": {
                    "forward": {
                        "contradiction": round(pp.forward.contradiction, 4),
                        "entailment": round(pp.forward.entailment, 4),
                        "neutral": round(pp.forward.neutral, 4),
                    },
                    "backward": {
                        "contradiction": round(pp.backward.contradiction, 4),
                        "entailment": round(pp.backward.entailment, 4),
                        "neutral": round(pp.backward.neutral, 4),
                    },
                    "contradiction": round(pp.contradiction, 4),
                    "duplication": round(pp.duplication, 4),
                    "distinctness": round(pp.distinctness, 4),
                    "verdict": pp.verdict,
                },
            }
        )
    return {"rows": rows, "summary": summarize(rows)}


def summarize(rows: list[dict]) -> dict:
    opp = [r for r in rows if r["class"] == "OPPOSITE"]
    same = [r for r in rows if r["class"] == "SAME"]

    # OLD proxy. Correct direction: duplicates (SAME) should sit CLOSER than
    # genuine contests (OPPOSITE)  =>  separation_old > 0.
    separation_old = mean([r["cosine"] for r in same]) - mean(
        [r["cosine"] for r in opp]
    )

    # NEW proxy. Correct direction: OPPOSITE more distinct than SAME  =>  > 0.
    separation_new = mean([r["nli"]["distinctness"] for r in opp]) - mean(
        [r["nli"]["distinctness"] for r in same]
    )
    separation_contradiction = mean([r["nli"]["contradiction"] for r in opp]) - mean(
        [r["nli"]["contradiction"] for r in same]
    )

    return {
        "n_opposite": len(opp),
        "n_same": len(same),
        # old proxy
        "old_mean_cos_opposite": round(mean([r["cosine"] for r in opp]), 4),
        "old_mean_cos_same": round(mean([r["cosine"] for r in same]), 4),
        "old_separation_same_minus_opposite": round(separation_old, 4),
        "old_false_duplicates": sum(r["old_gate_says_duplicate"] for r in opp),
        "old_missed_duplicates": sum(not r["old_gate_says_duplicate"] for r in same),
        # new proxy — the distinctness channel (the drop-in analogue)
        "new_mean_distinctness_opposite": round(
            mean([r["nli"]["distinctness"] for r in opp]), 4
        ),
        "new_mean_distinctness_same": round(
            mean([r["nli"]["distinctness"] for r in same]), 4
        ),
        "new_separation_opposite_minus_same": round(separation_new, 4),
        # new proxy — the polarity channel (what geometry cannot see at all)
        "new_mean_contradiction_opposite": round(
            mean([r["nli"]["contradiction"] for r in opp]), 4
        ),
        "new_mean_contradiction_same": round(
            mean([r["nli"]["contradiction"] for r in same]), 4
        ),
        "new_contradiction_separation": round(separation_contradiction, 4),
        # verdict confusion — the FATAL error class is a genuine contest
        # (OPPOSITE) judged DUPLICATE.
        "new_fatal_contest_judged_duplicate": sum(
            r["nli"]["verdict"] == VERDICT_DUPLICATE for r in opp
        ),
        "new_contests_seen_as_contradiction": sum(
            r["nli"]["verdict"] == VERDICT_CONTRADICTS for r in opp
        ),
        "new_duplicates_caught": sum(
            r["nli"]["verdict"] == VERDICT_DUPLICATE for r in same
        ),
        "new_duplicates_judged_contradiction": sum(
            r["nli"]["verdict"] == VERDICT_CONTRADICTS for r in same
        ),
    }


def print_block(title: str, result: dict) -> None:
    print(f"\n=== {title} ===")
    for r in result["rows"]:
        n = r["nli"]
        print(
            f"[{r['class']:8s}|{r['provenance'][:5]:5s}] cos={r['cosine']:+.4f} "
            f"old_dup={'Y' if r['old_gate_says_duplicate'] else 'n'} | "
            f"contra={n['contradiction']:.4f} dup={n['duplication']:.4f} "
            f"distinct={n['distinctness']:.4f} -> {n['verdict']:11s} | "
            f"{r['a'][:38]!r} / {r['b'][:38]!r}"
        )
    print(json.dumps(result["summary"], indent=2))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument(
        "--holdout",
        action="store_true",
        help="ALSO run the held-out set (run this exactly once, after the probe is final)",
    )
    args = ap.parse_args()

    t0 = time.time()
    print("[R14] local signature:", "redacted", platform.platform())
    print(f"[R14] NLI artifact: {DEFAULT_MODEL_ID} @ {DEFAULT_MODEL_REVISION} (CPU)")
    print(f"[R14] old-gate threshold (the audited system's shipped value): {DUPLICATE_GATE_THRESHOLD}")

    from harness.audited_system import MRLEmbeddingRouter

    embedder = MRLEmbeddingRouter()
    classifier = TransformersNLIClassifier()
    t_load = time.time() - t0

    out: dict = {
        "experiment": "hypothesis-distinctness probe (cosine gate vs NLI)",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "node": "redacted",
        "platform": platform.platform(),
        "nli_model": {"id": DEFAULT_MODEL_ID, "revision": DEFAULT_MODEL_REVISION, "device": "cpu"},
        "embedder": "MRLEmbeddingRouter (nomic-embed-text-v1.5, MRL-256, CPU) via batch_embed",
        "old_gate_threshold": DUPLICATE_GATE_THRESHOLD,
        "load_seconds": round(t_load, 2),
    }

    t1 = time.time()
    dev = run_probe(DEV_PAIRS, embedder, classifier)
    out["dev"] = dev
    print_block("DEV (16 pairs: 5 verbatim + 11 same-style reconstructions)", dev)

    if args.holdout:
        holdout = run_probe(HOLDOUT_PAIRS, embedder, classifier)
        out["holdout"] = holdout
        print_block("HOLDOUT (8 pairs, run once — hard classes included)", holdout)

    out["probe_seconds"] = round(time.time() - t1, 2)

    sep = dev["summary"]["new_separation_opposite_minus_same"]
    fatal = dev["summary"]["new_fatal_contest_judged_duplicate"]
    verdict = "SURVIVES" if (sep > 0 and fatal == 0) else "FALSIFIED"
    out["verdict"] = {
        "dev_separation": sep,
        "dev_fatal_contest_judged_duplicate": fatal,
        "rule": "FALSIFIED if separation <= 0 "
        "or any genuine contest is judged DUPLICATE (the fatal error class)",
        "verdict": verdict,
    }
    if args.holdout and "holdout" in out:
        hs = out["holdout"]["summary"]
        caveats = []
        if hs["new_fatal_contest_judged_duplicate"] > 0:
            caveats.append(
                f"{hs['new_fatal_contest_judged_duplicate']}/{hs['n_opposite']} held-out "
                "genuine contests judged DUPLICATE (the fatal error class is "
                "NONZERO outside the negation class)"
            )
        if hs["new_duplicates_judged_contradiction"] > 0:
            caveats.append(
                f"{hs['new_duplicates_judged_contradiction']}/{hs['n_same']} held-out "
                "duplicates judged CONTRADICTS (a cross-vocabulary paraphrase could "
                "be credited as a contest)"
            )
        if hs["new_separation_opposite_minus_same"] <= 0:
            caveats.append("held-out separation <= 0")
        out["verdict"]["holdout_separation"] = hs["new_separation_opposite_minus_same"]
        out["verdict"]["holdout_caveats"] = caveats
        if caveats:
            verdict = "SURVIVES-WITH-CAVEATS"
            out["verdict"]["verdict"] = verdict
    print(f"\n[R14] DEV separation (new proxy, correct-direction>0): {sep:+.4f}")
    print(f"[R14] DEV fatal errors (contest judged DUPLICATE): {fatal}")
    for c in out["verdict"].get("holdout_caveats", []):
        print(f"[R14] HOLDOUT CAVEAT: {c}")
    print(f"[R14] VERDICT: {verdict}")
    print(f"[R14] probe wall time: {out['probe_seconds']}s (+{out['load_seconds']}s load)")

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%d")
    dest = RESULTS_DIR / f"r14_falsifier_rerun_{stamp}{'_holdout' if args.holdout else ''}.json"
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"[R14] evidence written: {dest}")
    return 0 if verdict.startswith("SURVIVES") else 1


if __name__ == "__main__":
    raise SystemExit(main())
