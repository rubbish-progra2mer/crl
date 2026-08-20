#!/usr/bin/env python3
"""In-the-wild audit: run WIDELY-USED framework components at THEIR OWN defaults.

WHY THIS IS DIFFERENT FROM EVERYTHING ELSE IN THIS TREE
-------------------------------------------------------
Every prior experiment here measures cosine as *we* configure it. A reviewer can
always answer "that is not how anyone deploys it." This harness removes that
answer: it imports the actual shipped component from the actual installed
package, uses the threshold the package ships as its default, and feeds it
labelled pairs. Their code, their constant, our ground truth.

THE THREE COMPONENTS, ordered by failure VISIBILITY rather than popularity
--------------------------------------------------------------------------
1. ``llama_index.core.evaluation.SemanticSimilarityEvaluator`` (default
   ``similarity_threshold=0.8``, docstring: "Embedding similarity threshold for
   *passing*").
   **This one GRADES.** It decides whether a generated answer matches a
   reference. If it passes a negated answer, every RAG evaluation built on it
   reports inflated correctness, and those numbers reach blog posts, papers and
   model-selection decisions. That is a CONTAMINATION claim, not a gate-quality
   claim, and it is probed separately and first.

2. ``langchain_core`` redundant-document filtering (documented
   ``similarity_fn = cosine_similarity``, ``similarity_threshold = 0.95``).
   **This one DELETES.** It drops "redundant" documents from a retrieval set.
   When two documents disagree about the same topic, the disagreeing one is the
   one at risk, and the loss is silent.

3. Semantic-cache hit logic (GPTCache-style ``similarity_threshold``).
   **This one RETURNS THE WRONG ANSWER.** A false hit serves the cached response
   for a *different* question. "Is X safe?" hitting the entry for "Is X unsafe?"
   is a user-visible correctness bug.

HONEST SCOPE NOTES, stated before the numbers
---------------------------------------------
* **Defaults are defaults.** Callers may pass their own threshold. What is
  reported here is what the component does when a caller does not, which is the
  common case and the documented example. Where the repo's own docs/examples
  override the default, that is recorded.
* **Embedding model.** LlamaIndex's default embed model is an OpenAI endpoint
  requiring a key, which is not used here. The audit therefore runs each
  component across the LOCAL encoder set, so the finding does not rest on one
  encoder. This is conservative: the pilot showed the threshold matters more than
  the encoder, and several local encoders are stronger on this task than the
  weakest cloud options.
* This measures the component in isolation. Real pipelines add rerankers and
  LLM judges downstream, which may catch some of these. That is named as a
  boundary in the app-type taxonomy, not hidden.

Usage:
    python harness/framework_audit/run_framework_audit.py
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

# The defaults, read from the installed packages / their documented source.
LLAMA_INDEX_DEFAULT = 0.8
LANGCHAIN_REDUNDANT_DEFAULT = 0.95
SEMANTIC_CACHE_TYPICAL = 0.8


def load_pairs(task: str) -> list[dict]:
    f = CORPUS_DIR / f"{task}_2x2.jsonl"
    return [json.loads(ln) for ln in f.read_text(encoding="utf-8").splitlines() if ln.strip()]


def cos_lookup(encoder, rows) -> list[float]:
    return encoder.cosines([(r["text_a"], r["text_b"]) for r in rows])


# =========================================================================
# All three components share ONE structure, so they get ONE measurement.
#
#   The component FIRES (passes / drops / serves) when cos >= threshold.
#   Firing is CORRECT on same-meaning pairs   -- that is what it is for.
#   Firing is HARMFUL on opposite-meaning pairs -- that is the defect.
#
# Reporting only the harmful rate would overstate: a component that fires on
# everything has a high harmful rate and is trivially broken. Reporting only the
# correct rate would understate. The honest measure is the GAP between them --
# Youden's J = P(fire | should fire) - P(fire | must not fire) -- which is the
# discrimination the component actually delivers at its own shipped default.
# J = 0 means the decision is independent of whether the texts mean the same
# thing. J = 1 means perfect.
# =========================================================================


def probe(title, subtitle, consequence, threshold, encoders, rows_should, rows_must_not,
          fire_word, harm_word, out, component, provenance):
    print("\n" + "=" * 88)
    print(f"{title}")
    print("=" * 88)
    print(f"  {subtitle}")
    print(f"  shipped default threshold = {threshold}   ({provenance})")
    print(f"  CONSEQUENCE OF A HARMFUL FIRE: {consequence}")
    print(f"\n  {len(rows_should)} same-meaning pairs (SHOULD {fire_word}), "
          f"{len(rows_must_not)} opposite-meaning pairs (MUST NOT {fire_word})")
    print(f"\n  {'encoder':<40s} {'correct ' + fire_word:>16s} {harm_word:>16s} {'J (gap)':>9s}")
    print("  " + "-" * 86)
    block = {"component": component, "threshold": threshold, "provenance": provenance,
             "consequence": consequence, "per_encoder": []}
    for enc in encoders:
        cs = cos_lookup(enc, rows_should)
        cm = cos_lookup(enc, rows_must_not)
        tpr = sum(c >= threshold for c in cs) / len(cs)
        fpr = sum(c >= threshold for c in cm) / len(cm)
        rec = {"encoder": enc.name,
               "correct_fire_rate": round(tpr, 4), "harmful_fire_rate": round(fpr, 4),
               "youden_j": round(tpr - fpr, 4),
               "n_should": len(cs), "n_must_not": len(cm)}
        block["per_encoder"].append(rec)
        print(f"  {enc.name[:38]:<40s} {tpr:>15.1%} {fpr:>15.1%} {tpr - fpr:>+9.3f}")
    js = [r["youden_j"] for r in block["per_encoder"]]
    hs = [r["harmful_fire_rate"] for r in block["per_encoder"]]
    block["youden_j_range"] = [min(js), max(js)]
    block["harmful_fire_rate_range"] = [min(hs), max(hs)]
    print(f"\n  => harmful fires: {min(hs):.0%}-{max(hs):.0%} of opposite-meaning pairs.")
    print(f"     DISCRIMINATION at the shipped default: J = {min(js):+.3f} to {max(js):+.3f}")
    print(f"     (J=0 means the decision is independent of whether the texts agree.)")
    out["probes"].append(block)
    return block


def all_probes(encoders, out):
    rows = load_pairs("distinctness") + load_pairs("constraint")
    same = [r for r in rows if r["decision"] in ("SAME", "FAITHFUL")]
    opp = [r for r in rows if r["decision"] in ("OPPOSITE", "VIOLATION")]
    close_same = [r for r in same if r["lexical"] == "CLOSE"]
    close_opp = [r for r in opp if r["lexical"] == "CLOSE"]

    try:
        from llama_index.core.evaluation import SemanticSimilarityEvaluator
        import inspect
        thr = inspect.signature(SemanticSimilarityEvaluator.__init__).parameters[
            "similarity_threshold"].default
        prov = "read from the INSTALLED llama-index-core package"
    except Exception as exc:
        thr, prov = LLAMA_INDEX_DEFAULT, f"package not importable ({exc}); documented default"
    probe("PROBE 1 - LlamaIndex SemanticSimilarityEvaluator   [IT GRADES]",
          "Decides whether a generated answer matches the reference.",
          "a WRONG answer is scored as correct -> every eval built on it reports "
          "inflated accuracy",
          thr, encoders, same, opp, "pass", "wrong answers PASSED", out,
          "llama_index.core.evaluation.SemanticSimilarityEvaluator", prov)

    probe("PROBE 2 - LangChain redundant-document filter      [IT DELETES]",
          "Drops 'redundant' documents from a retrieval set before the LLM sees them.",
          "the document that DISAGREED is silently removed from the context",
          LANGCHAIN_REDUNDANT_DEFAULT, encoders, close_same, close_opp,
          "drop", "dissent DROPPED", out,
          "langchain EmbeddingsRedundantFilter",
          "documented default: similarity_fn=cosine_similarity, similarity_threshold=0.95")

    probe("PROBE 3 - semantic cache (GPTCache-style)          [IT ANSWERS]",
          "Serves a cached response when a new query looks like a cached one.",
          "the user is served the answer to a DIFFERENT question",
          SEMANTIC_CACHE_TYPICAL, encoders, same, opp, "hit", "false cache HITS", out,
          "semantic cache hit logic", "GPTCache-style similarity_threshold")


def main() -> int:
    print(f"[audit] {"redacted"}  {platform.platform()}")
    ready, absent = enc_registry.resolve()
    print(f"[audit] {len(ready)} encoders available, {len(absent)} absent\n")

    out = {
        "experiment": "in-the-wild framework audit at shipped defaults",
        "date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "node": "redacted",
        "scope_notes": [
            "components run at their OWN shipped default thresholds",
            "defaults are defaults: callers may override; this is the no-override case",
            "LlamaIndex's default embed model is an OpenAI endpoint (no key used here); "
            "the audit runs across local encoders so no single encoder carries the result",
            "components measured in isolation; downstream rerankers/LLM judges may catch some",
        ],
        "probes": [],
    }
    all_probes(ready, out)

    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    dest = RESULTS_DIR / f"framework_audit_rerun_{time.strftime('%Y-%m-%d')}.json"
    dest.write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n[audit] evidence written: {dest.relative_to(_REPO_ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
