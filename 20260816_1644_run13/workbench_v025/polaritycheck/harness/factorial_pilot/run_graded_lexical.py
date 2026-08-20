#!/usr/bin/env python3
"""Graded lexical reanalysis — is the 0.975-1.000 lexical AUROC an artefact of pole placement?

THE OBJECTION THIS ANSWERS
--------------------------
The pilot reports that every encoder recovers the lexical axis at AUROC 0.975-1.000
and the decision axis at only 0.440-0.815, and calls that a dissociation. A reviewer
answers: *you constructed the lexical contrast with its poles ~0.66 token-Jaccard
apart (CLOSE ~0.72 vs DISTANT ~0.06) and took whatever nature gave you on the
decision axis. The gap reports your design, not two effect sizes.*

That objection is partly right and it has a cheap empirical test, run here.

The decision axis has NO magnitude dial -- it is contrasted at total reversal vs
identity, i.e. 100% of a binary construct's range. The lexical axis DOES have one.
So the question is only ever about the lexical side: **does cosine still track
lexical overlap when the poles are close together?**

    WIDE contrast   CLOSE stratum vs DISTANT stratum   (what the pilot reports)
    NARROW contrast within ONE stratum, median-split on token_jaccard

If the narrow contrast collapses toward chance, "cosine measures surface form
excellently" is over-stated -- it measures LARGE surface differences excellently,
and the dissociation is about magnitude rather than kind.

A continuous check runs alongside it: Spearman(cosine, token_jaccard) computed
WITHIN a stratum, where the spread is small. A pole artefact shows up as a strong
between-stratum relationship and a null within-stratum one.

Offline; reuses the pilot's own encoder registry and corpus. No new authoring.

    python harness/factorial_pilot/run_graded_lexical.py
"""

from __future__ import annotations

import json
import platform
import statistics
import sys
import time
from pathlib import Path

_HERE = Path(__file__).resolve().parent
_REPO_ROOT = _HERE.parents[1]
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from harness.factorial_pilot.encoders import resolve  # noqa: E402
from harness.factorial_pilot.lexical import PRIMARY_METRIC, token_jaccard  # noqa: E402
from harness.lib.evidence import Count  # noqa: E402
from harness.lib.stats import auroc, bootstrap_ci  # noqa: E402

assert PRIMARY_METRIC == "token_jaccard", (
    "the pilot's declared primary metric changed; this reanalysis must track it, "
    f"got {PRIMARY_METRIC!r}")

TASKS = ("distinctness", "constraint")
CORPUS = {t: _REPO_ROOT / "corpus" / f"{t}_2x2.jsonl" for t in TASKS}
OUT = _REPO_ROOT / "results" / "factorial_pilot" / f"graded_lexical_rerun_{time.strftime('%Y-%m-%d')}.json"


def spearman(xs: list[float], ys: list[float]) -> float | None:
    """Spearman rho with average ranks. None when undefined (n<3 or no variance)."""
    n = len(xs)
    if n < 3:
        return None

    def rank(v: list[float]) -> list[float]:
        order = sorted(range(n), key=lambda i: v[i])
        r = [0.0] * n
        i = 0
        while i < n:
            j = i
            while j + 1 < n and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r

    rx, ry = rank(xs), rank(ys)
    mx, my = statistics.fmean(rx), statistics.fmean(ry)
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    dx = sum((a - mx) ** 2 for a in rx) ** 0.5
    dy = sum((b - my) ** 2 for b in ry) ** 0.5
    if dx == 0 or dy == 0:
        return None
    return round(num / (dx * dy), 4)


def load(task: str) -> list[dict]:
    rows = [json.loads(ln) for ln in CORPUS[task].read_text(encoding="utf-8").splitlines() if ln.strip()]
    for r in rows:
        r["_jac"] = r["lexical_metrics"]["token_jaccard"] if "lexical_metrics" in r else None
    return rows


# No local jaccard: the pilot's own token_jaccard is imported above so the strata
# here are the same strata the manipulation check validated. A second definition
# would silently produce a different corpus.


def main() -> int:
    ready, absent = resolve()
    print(f"encoders: {len(ready)} available, {len(absent)} absent")
    for name, why in absent:
        print(f"  ABSENT (LOUD): {name} -- {why}")

    out: dict = {
        "experiment": "graded lexical reanalysis (pole-placement control)",
        "question": "does cosine still track lexical overlap when the poles are close?",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "node": "redacted",
        "platform": platform.platform(),
        "encoders_available": [e.name for e in ready],
        "encoders_absent": [{"name": n, "why": w} for n, w in absent],
        "tasks": {},
    }

    for task in TASKS:
        rows = load(task)
        for r in rows:
            if r["_jac"] is None:
                r["_jac"] = token_jaccard(r["text_a"], r["text_b"])
        pairs = [(r["text_a"], r["text_b"]) for r in rows]
        block: dict = {
            "n_pairs": len(rows),
            "coverage": str(Count(
                value=len(rows),
                what=f"{task} pairs",
                frame="the frozen 2x2 corpus",
                could_not_see="nothing — full enumeration of the frozen corpus file",
                caveats=[
                    "each stratum pools 2 cells (n=20); the median split gives 10v10, "
                    "except distinctness CLOSE which ties at 0.7143 and splits 7v13. "
                    "Every narrow contrast is directional, not an estimate",
                ],
            )),
            "per_encoder": [],
        }
        print(f"\n{'=' * 78}\n{task.upper()} -- n={len(rows)}\n{'=' * 78}")

        for enc in ready:
            cos = enc.cosines(pairs)
            rec: dict = {"encoder": enc.name, "family": enc.family, "strata": {}}

            # WIDE contrast, reproduced here so the comparison is like-for-like.
            close = [(c, r) for c, r in zip(cos, rows) if r["lexical"] == "CLOSE"]
            distant = [(c, r) for c, r in zip(cos, rows) if r["lexical"] == "DISTANT"]
            rec["wide_contrast"] = {
                "auroc": round(auroc([c for c, _ in close], [c for c, _ in distant]), 4),
                "n_high": len(close), "n_low": len(distant),
                "mean_jaccard_high": round(statistics.fmean([r["_jac"] for _, r in close]), 4),
                "mean_jaccard_low": round(statistics.fmean([r["_jac"] for _, r in distant]), 4),
            }
            rec["wide_contrast"]["jaccard_separation"] = round(
                rec["wide_contrast"]["mean_jaccard_high"] - rec["wide_contrast"]["mean_jaccard_low"], 4)

            # NARROW contrast: within each stratum, median-split on token_jaccard.
            for stratum, members in (("CLOSE", close), ("DISTANT", distant)):
                jacs = [r["_jac"] for _, r in members]
                med = statistics.median(jacs)
                hi = [c for c, r in members if r["_jac"] > med]
                lo = [c for c, r in members if r["_jac"] <= med]
                entry: dict = {
                    "n_high": len(hi), "n_low": len(lo), "median_jaccard": round(med, 4),
                    "jaccard_range": [round(min(jacs), 4), round(max(jacs), 4)],
                }
                if len(hi) >= 3 and len(lo) >= 3:
                    a = auroc(hi, lo)
                    entry["narrow_auroc"] = round(a, 4)
                    entry["narrow_jaccard_separation"] = round(
                        statistics.fmean([r["_jac"] for _, r in members if r["_jac"] > med])
                        - statistics.fmean([r["_jac"] for _, r in members if r["_jac"] <= med]), 4)
                    try:
                        lo95, hi95 = bootstrap_ci(hi, lo)
                        entry["ci95"] = [round(lo95, 3), round(hi95, 3)]
                    except Exception:
                        entry["ci95"] = None
                else:
                    entry["narrow_auroc"] = None
                    entry["why_absent"] = "median split leaves a side with n<3 (ties)"
                entry["spearman_cos_vs_jaccard_within_stratum"] = spearman(
                    [c for c, _ in members], jacs)
                rec["strata"][stratum] = entry

            block["per_encoder"].append(rec)
            cl, ds = rec["strata"]["CLOSE"], rec["strata"]["DISTANT"]
            print(f"  {enc.name[:46]:<48} wide {rec['wide_contrast']['auroc']:.3f}"
                  f" | narrow CLOSE {cl['narrow_auroc']} (rho {cl['spearman_cos_vs_jaccard_within_stratum']})"
                  f" | narrow DISTANT {ds['narrow_auroc']} (rho {ds['spearman_cos_vs_jaccard_within_stratum']})")

        # Summary across encoders, so the reader is never handed one row as the field.
        wides = [r["wide_contrast"]["auroc"] for r in block["per_encoder"]]
        narrows = [r["strata"][s]["narrow_auroc"] for r in block["per_encoder"]
                   for s in ("CLOSE", "DISTANT") if r["strata"][s]["narrow_auroc"] is not None]
        rhos = [r["strata"][s]["spearman_cos_vs_jaccard_within_stratum"] for r in block["per_encoder"]
                for s in ("CLOSE", "DISTANT")
                if r["strata"][s]["spearman_cos_vs_jaccard_within_stratum"] is not None]
        block["summary"] = {
            "wide_auroc": {"n": len(wides), "min": min(wides), "median": statistics.median(wides), "max": max(wides)},
            "narrow_auroc": ({"n": len(narrows), "min": min(narrows),
                              "median": statistics.median(narrows), "max": max(narrows)}
                             if narrows else {"n": 0, "note": "no computable narrow contrast"}),
            "within_stratum_spearman": ({"n": len(rhos), "min": min(rhos),
                                         "median": statistics.median(rhos), "max": max(rhos)}
                                        if rhos else {"n": 0}),
        }
        out["tasks"][task] = block
        s = block["summary"]
        print(f"\n  SUMMARY {task}: wide AUROC median {s['wide_auroc']['median']}"
              f" ({s['wide_auroc']['min']}-{s['wide_auroc']['max']}, n={s['wide_auroc']['n']})")
        print(f"           narrow AUROC median {s['narrow_auroc'].get('median')}"
              f" (n={s['narrow_auroc']['n']})")
        print(f"           within-stratum Spearman median {s['within_stratum_spearman'].get('median')}"
              f" (n={s['within_stratum_spearman'].get('n')})")

    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"\nwrote {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
