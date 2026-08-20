#!/usr/bin/env python3
"""Run the audited drift guard against the two constraint-drift corpora (§6).

Measures, per case, the two model-backed layers of the audited guard exactly as
production runs them:

  * **cosine** — ``MRLEmbeddingRouter.calculate_drift`` (the production
    embedding path: nomic-embed-text-v1.5, MRL-256, ``search_document:``
    prefix, CPU) against the shipped drift threshold of 0.40 on the drift
    scale (i.e. it fires when cosine similarity < 0.40 — never reached by any
    mutation in either corpus).
  * **nli** — the pinned NLI cross-encoder's argmax verdict (fires on
    CONTRADICTS; no tunable threshold by design).

SCOPE NOTE. The audited system's guard stack also contains a stdlib
constraint-ledger layer. That layer belongs to the audited system's internal
codebase and is not redistributed here; the frozen results under
``results/guard_stack/`` retain its columns (``ledger_apriori``,
``ledger_full``, ``composite``). The paper's §6/§7 numbers rest on the
``cosine`` and ``nli`` columns, which this runner reproduces bit-for-bit
(a reproduction check against the frozen evidence runs automatically).

Usage:
    python harness/guard_stack/run_guard_stack.py             # in-sample corpus
    python harness/guard_stack/run_guard_stack.py --heldout   # held-out corpus

Offline by default (HF_HUB_OFFLINE=1); both artifacts must be in the local HF cache.
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

from harness.guard_stack.scoring import (  # noqa: E402
    CONTROL_CLASSES,
    CORPUS_PATH,
    HELDOUT_PATH,
    MUTATION_CLASSES,
    cosine_catches,
    nli_catches,
)

RESULTS_DIR = _REPO_ROOT / "results" / "guard_stack"
LAYERS = ("cosine", "nli")

#: Frozen evidence to reproduce against, per corpus.
FROZEN = {
    "in_sample": "guard_stack_corpus_2026-07-26.json",
    "held_out": "guard_stack_heldout_2026-07-26.json",
}


def _score_case(case: dict, embedder, classifier, drift_threshold: float) -> dict:
    from harness.audited_system import pair_polarity

    root, mutated = case["root"], case["mutated"]
    sim = float(embedder.calculate_drift(root, mutated))
    pp = pair_polarity(root, mutated, classifier)
    return {
        "id": case["id"],
        "mutation_class": case["mutation_class"],
        "sub_form": case.get("sub_form", ""),
        "root": root,
        "mutated": mutated,
        "cosine": {
            "similarity": round(sim, 4),
            "caught": cosine_catches(sim, drift_threshold),
        },
        "nli": {
            "verdict": pp.verdict,
            "contradiction": round(pp.contradiction, 4),
            "duplication": round(pp.duplication, 4),
            "caught": nli_catches(pp.verdict),
        },
    }


def _rate(fired: int, n: int) -> float | None:
    return round(fired / n, 4) if n else None


def _summarize(rows: list[dict]) -> dict:
    out: dict = {}
    for cls in list(MUTATION_CLASSES) + list(CONTROL_CLASSES):
        crows = [r for r in rows if r["mutation_class"] == cls]
        n = len(crows)
        is_control = cls in CONTROL_CLASSES
        d = {"kind": "control" if is_control else "mutation", "n": n,
             "rate_meaning": "false_positive_rate" if is_control else "true_positive_catch_rate"}
        for layer in LAYERS:
            fired = sum(r[layer]["caught"] for r in crows)
            d[f"{layer}_fired"] = fired
            d[f"{layer}_rate"] = _rate(fired, n)
        out[cls] = d
    return out


def _aggregate(rows: list[dict]) -> dict:
    muts = [r for r in rows if r["mutation_class"] in MUTATION_CLASSES]
    ctrls = [r for r in rows if r["mutation_class"] in CONTROL_CLASSES]
    agg = {"n_mutations": len(muts), "n_controls": len(ctrls)}
    for layer in LAYERS:
        agg[f"{layer}_fired"] = sum(bool(r[layer]["caught"]) for r in muts)
        agg[f"{layer}_false_positives"] = sum(bool(r[layer]["caught"]) for r in ctrls)
    return agg


def _reproduce_frozen(rows: list[dict], frozen_name: str) -> dict:
    """Assert cosine similarity + NLI verdict reproduce the frozen evidence."""
    path = RESULTS_DIR / frozen_name
    if not path.exists():
        return {"available": False, "note": f"{frozen_name} absent"}
    prior = json.loads(path.read_text(encoding="utf-8"))
    prior_rows = {r["id"]: r for r in prior["rows"]}
    mismatches = []
    for r in rows:
        p = prior_rows.get(r["id"])
        if p is None:
            mismatches.append(f"{r['id']}: absent in frozen evidence")
            continue
        if abs(p["cosine"]["similarity"] - r["cosine"]["similarity"]) > 1e-6:
            mismatches.append(
                f"{r['id']}: cosine {p['cosine']['similarity']} != {r['cosine']['similarity']}")
        if p["nli"]["verdict"] != r["nli"]["verdict"]:
            mismatches.append(
                f"{r['id']}: nli {p['nli']['verdict']} != {r['nli']['verdict']}")
    return {"available": True, "source": frozen_name,
            "reproduces": not mismatches, "mismatches": mismatches}


def _print_table(out: dict) -> None:
    print("\n=== PER-CASE ===")
    for r in out["rows"]:
        print(f"[{r['id']:11s}|{r['mutation_class']:19s}] "
              f"cos={r['cosine']['similarity']:.4f} {'CAUGHT' if r['cosine']['caught'] else 'miss  '} "
              f"nli={r['nli']['verdict']:11s}{'CAUGHT' if r['nli']['caught'] else 'miss'}")
    print("\n=== PER-CLASS (cosine / nli) ===")
    for cls, s in out["per_class"].items():
        tag = "FPR" if s["kind"] == "control" else "TPR"
        print(f"{cls:19s} n={s['n']} | cos={s['cosine_fired']}/{s['n']} "
              f"nli {tag}={s['nli_fired']}/{s['n']}")
    a = out["aggregate"]
    print(f"\nAGG mutations n={a['n_mutations']}: cosine={a['cosine_fired']} nli={a['nli_fired']}")
    print(f"AGG controls n={a['n_controls']} false-positives: "
          f"cosine={a['cosine_false_positives']} nli={a['nli_false_positives']}")
    rep = out["reproduces_frozen"]
    print(f"\nFROZEN-EVIDENCE REPRODUCTION: {'PASS' if rep.get('reproduces') else 'MISMATCH/ABSENT'} ({rep})")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--heldout", action="store_true",
                    help="run the held-out corpus instead of the in-sample one")
    args = ap.parse_args()

    which = "held_out" if args.heldout else "in_sample"
    corpus_path = HELDOUT_PATH if args.heldout else CORPUS_PATH

    t0 = time.time()
    corpus = json.loads(corpus_path.read_text(encoding="utf-8"))

    from harness.audited_system import (
        DEFAULT_MODEL_ID,
        DEFAULT_MODEL_REVISION,
        DRIFT_THRESHOLD,
        MRLEmbeddingRouter,
        TransformersNLIClassifier,
    )

    print("[GS] local signature:", "redacted", platform.platform())
    print(f"[GS] cosine drift_threshold (shipped): {DRIFT_THRESHOLD}")
    print(f"[GS] corpus: {corpus_path.name} ({len(corpus['cases'])} cases)")

    embedder = MRLEmbeddingRouter()
    classifier = TransformersNLIClassifier()
    load_seconds = round(time.time() - t0, 2)

    t1 = time.time()
    rows = [_score_case(c, embedder, classifier, DRIFT_THRESHOLD) for c in corpus["cases"]]
    probe_seconds = round(time.time() - t1, 2)

    out = {
        "experiment": f"drift-guard measurement ({which} corpus)",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "node": "redacted",
        "platform": platform.platform(),
        "drift_threshold": DRIFT_THRESHOLD,
        "scope_note": (
            "cosine and nli are the audited guard's model-backed layers, reproduced "
            "exactly; the audited system's internal constraint-ledger layer is not "
            "redistributed — its columns live in the frozen evidence only"
        ),
        "corpus_provenance": {
            "path": str(corpus_path.relative_to(_REPO_ROOT)),
            "authoring_isolation": corpus.get("authoring_isolation", ""),
        },
        "models": {
            "cosine": "MRLEmbeddingRouter (nomic-embed-text-v1.5, MRL-256, CPU) via calculate_drift",
            "nli": {"id": DEFAULT_MODEL_ID, "revision": DEFAULT_MODEL_REVISION, "device": "cpu"},
        },
        "layers": list(LAYERS),
        "load_seconds": load_seconds,
        "probe_seconds": probe_seconds,
        "rows": rows,
        "per_class": _summarize(rows),
        "aggregate": _aggregate(rows),
        "reproduces_frozen": _reproduce_frozen(rows, FROZEN[which]),
    }

    _print_table(out)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y-%m-%d")
    dest = RESULTS_DIR / f"guard_stack_{which}_rerun_{stamp}.json"
    dest.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\n[GS] evidence written: {dest}")
    print(f"[GS] wall time: {probe_seconds}s probe (+{load_seconds}s load)")
    rep = out["reproduces_frozen"]
    if rep.get("available") and not rep.get("reproduces"):
        print("[GS] WARNING: cosine/NLI did NOT reproduce the frozen evidence — investigate.")
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
