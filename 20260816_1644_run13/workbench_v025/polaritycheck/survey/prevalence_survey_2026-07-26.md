# Prevalence survey — is anyone actually shipping these two patterns?

**Written:** 2026-07-26.
**Method:** GitHub code search via authenticated `gh search code`, **then opening the files** and
recording whether the hit is a real gate, plus a web pass over vendor and practitioner guidance.

**Two scope caveats stated up front.**

1. GitHub code search returns a ranked, capped sample, not a census. Counts are *lower bounds on
   existence*, not population estimates. A defensible prevalence *rate* needs a sampling frame — §3.
2. **A keyword hit is not an instance.** This document originally reported 36 unopened search hits
   as instances of the pattern. That was wrong, and wrong against evidence produced an hour earlier
   in this same survey: of three R13 candidates inspected, **two turned out not to be the defect.**
   A ranked-keyword hit rate is not a verified rate. §2 now reports only files that were opened and
   read, with the false positives named.

**Two patterns, two opposite answers.**

---

## 1. Post-hoc hyperbolic projection (R13) — RARE. Kill-condition #6 fires.

**Queries:** `expmap0 normalize`, `poincare_exp_map`, `expmap0 SentenceTransformer`,
`expmap0 encode normalize_embeddings`, `poincare retrieval embeddings hyperbolic rag`,
`geodesic_distance F.normalize embeddings` — all `language:python`.

**What came back: ~60 distinct repositories, and the overwhelming majority are NOT instances of the
defect.** They are legitimate hyperbolic-ML libraries and papers — HGCN/GraphZoo, HoroPCA, HTorch,
hypll/hypax-style manifold packages, hyperbolic ViTs, hyperbolic recommenders — where the
exponential map is applied to **trainable** representations whose norms are free to encode depth.
The proposition does not apply to them, and they are doing hyperbolic geometry correctly.

Three candidates looked like the pattern. On inspection:

| repo | verdict |
|---|---|
| `Erber102/Manifold-Rag` | **NOT the defect.** SBERT → a *trainable* `PoincareHead` (`self.proj_h(x) * self.scale_h`) before `expmap0`. Norms vary. Legitimate. |
| `sherkevin/HyperAmy` | **NOT the defect.** Uses `z_i(t) = tanh(√c/2 · R_i(t)) · μ_i` — an explicit time-varying radius. The norm channel is deliberately in use. |
| `unworthyzeus/HyperRAG` | **IS the defect — confirmed.** See below. |

### The one confirmed wild instance — demonstrated, not inferred

**Verified by execution**, not by reading:
[`experiments/r13_hyperbolic_hierarchy/wild_instance_check.py`](../experiments/r13_hyperbolic_hierarchy/wild_instance_check.py)
transcribes their `project_to_ball` and `hyperbolic_distance` **verbatim** and runs them on 400
unit-norm vectors at their dimensionality:

| check | result |
|---|---|
| every document at an identical ball radius | **True** — spread 3.3e−16, at the predicted `tanh(1)·0.99 = 0.7540` |
| `argsort(hyperbolic) == argsort(−cosine)` | **True**, all 400 documents |
| `argsort(hyperbolic) == argsort(euclidean)` | **True** |
| Spearman(hyperbolic, euclidean) | **1.0000000000** |
| top-10 retrieval identical to cosine | **True** |
| their distances vs the closed form (*) | max abs. error **1.3e−15** |

Their hyperbolic retrieval returns exactly the cosine ranking, document for document. The Poincaré
ball, the projection, the `arcosh` geodesic and the curvature parameter are all computed and none of
them can affect a single result.

**Framing note for the paper: cite this as a pattern instance, not as a callout of one project.**
The same defect shipped in the system this repository audits, found the same way. The point is that
the idiom is easy to write and silently degenerate.

### Why it is an instance — the reading

`unworthyzeus/HyperRAG`, `src/HyperRAG/core/geometry.py` + `core/engines.py`:

```python
def project_to_ball(self, vectors, max_norm=0.99):
    norms = np.linalg.norm(vectors, axis=-1, keepdims=True)
    unit_vectors = vectors / norms                          # "Normalize to unit sphere first"
    new_norms = np.tanh(norms / np.max(norms)) * max_norm
    return unit_vectors * new_norms
```

and its `hyperbolic_distance` is the *same formula* as the audited implementation here:
`(1/√c)·arcosh(1 + 2c‖x−y‖²/((1−c‖x‖²)(1−c‖y‖²)))`.

The engine feeds it `self.encoder.encode(documents)` from **`all-MiniLM-L6-v2`**. That checkpoint's
`modules.json` ends with a `Normalize` module — verified directly:

```json
{"idx": 2, "name": "2", "path": "2_Normalize", "type": "sentence_transformers.models.Normalize"}
```

So the input is already unit-norm despite being called `raw_embeddings`; `norms` is all-ones,
`np.max(norms)` is 1, and `new_norms` is the **constant** `tanh(1)·0.99`. By the proposition, its
"hyperbolic" retrieval ranking is *provably identical* to cosine ranking. Its own diagnostic would
reveal this — it prints `Poincaré norms: mean=…, max=…`, and those two numbers are equal — but
nothing checks it.

That is a clean, checkable, independently-authored instance, and it is a nice one because the
codebase contains the very print statement that would expose it.

### Verdict

**One confirmed instance is not prevalence.** Kill-condition #6 said: *"if the R13 prevalence pass
finds fewer than ~5 real instances, the note drops the prevalence claim and ships as
proof-plus-audit only."*

Combined with the novelty finding — that the constant-radius/Euclidean-isometry observation is
already in [arXiv:2309.10013](https://arxiv.org/abs/2309.10013) — **the standalone R13 note is
dead.** A proof that is essentially known, plus an audit of one's own repo and one hobby repo, is a
blog post, not an arXiv note. **Decision: fold R13 into Paper A as a section.**

Recording that plainly, because a pre-registered condition fired and the correct response is to
honour it rather than argue with it.

---

## 2. Cosine-threshold gates in agent systems (Paper A) — ABUNDANT

**Queries:** `cosine_similarity 0.85 duplicate threshold agent`,
`similarity_threshold 0.9 deduplicate memory agent`,
`semantic_similarity threshold drift guardrail` — all `language:python`, 12 results each.

### The strongest evidence first: it is *recommended practice*, in writing

This half needs no code inspection and has no false-positive problem. Practitioner and vendor
guidance recommends explicit operating points:

- *"cosine distance greater than 0.15 often indicating meaningful drift"*
- rolling-mean cosine baselines firing when a drop exceeds **2σ**

Those are quotable, published operating points, and they are exactly the operating points this
repository's evidence says do not exist. **Lead the paper's prevalence section with this.**

### The code evidence, verified by opening the files

36 hits came back across three capped queries. **11 were opened and read. 9 are real gates; 2 are
not.** Verified table — the grep line is the gating comparison:

| repo · file | function | evidence | verdict |
|---|---|---|---|
| `nammayatri/agents-platform` · `indexing/memory_extractor.py` | memory dedup | `if similarity > similarity_threshold:` | **gate** |
| `DemonDamon/AgenticX` · `core/memory_extraction.py` | memory extraction | `if similarity >= threshold:` | **gate** |
| `StigLidu/AdaExplore` · `skill_memory/deduplicate_knowledge.py` | knowledge dedup | dual band: `< hybrid_threshold_low` / `>= hybrid_threshold_high`, plus `>= similarity_threshold` | **gate** |
| `OriNachum/autonomous-intelligence` · `memory/deduplication.py` | memory dedup | `if similarity >= threshold:` | **gate** |
| `AP3X-Dev/AG3NT` · `agent/memory_search.py` | chunk dedup | `DEDUP_SIMILARITY_THRESHOLD = 0.95  # Cosine similarity threshold for deduplication` → `if similarity >= …:` | **gate** |
| `erykaitools-beep/Maria` · `world_model/belief_maintenance.py` | belief maintenance | `if sim < similarity_threshold:` + `DEFAULT_SEMANTIC_THRESHOLD = 0.95` | **gate** |
| `innovation64/BMAM` · `core/long_term_memory.py` | long-term memory | `if similarity >= similarity_threshold and …` + `threshold=0.4`, `0.3` | **gate** |
| `dfrostar/neuralmind` · `entity_resolution.py` | entity resolution | `AUTO_MERGE_THRESHOLD = 0.95` / `REVIEW_FLAG_THRESHOLD = 0.85` | **gate** |
| `astewartfritz/horizon-orchestra-full` · `code_agent/memory/consolidation.py` | memory consolidation | `if sim >= similarity_threshold:` | **gate** |
| `Maximilian-Winter/ToolAgents` · `agent_memory/semantic_memory/memory.py` | memory search | `if similarity > 0:  # Only include results with meaningful similarity` | **NOT a gate** — a ranking filter at zero |
| `wonjangcloud9/open-guardrail` · `guards/__init__.py` | guardrail | no threshold comparison in the file | **NOT verified** |

**9 / 11 verified (82%).** That is a defensible statement of typicality, and it is a much better hit
rate than the R13 search in §1 — which is the point: these are not exotic constructions, they are
the ordinary idiom.

**Two things worth noting from the verified set, both paper material.** Several gates make
*consequential* decisions, not just ranking: `dfrostar/neuralmind` **auto-merges entities** at 0.95
and flags for human review at 0.85; `erykaitools-beep/Maria` maintains *beliefs* in a world model.
And the observed thresholds — 0.95, 0.95, 0.95, 0.85, 0.4, 0.3 — span the range with no visible
validation behind any of them. Tabulating that distribution is Block B.6 item 3, and this
repository's own history is the cautionary case: its gate advertised `0.40` in config, docstring and
register while the *effective* boundary was `cos < 0.80`.

**This is the prevalence Paper A needs.** The pattern is not one abandoned project's mistake; it is
the default way agent frameworks decide whether two pieces of text mean the same thing, and it is
recommended in production guidance.

Note the asymmetry with §1 and what it implies: the *interesting* finding is not that people do
exotic geometry badly (they mostly don't), it is that people do the **most ordinary thing** —
threshold a cosine — as a control surface, at scale, unvalidated.

---

## 3. What a defensible prevalence number requires — not done here

Everything above establishes existence and typicality. It does not establish a rate, and the paper
must not imply one. To claim a rate, Block B.6 needs:

1. **A sampling frame.** E.g. the top *N* GitHub repositories by stars matching "LLM agent
   framework" / "agent memory", enumerated *before* inspection.
2. **A coding protocol.** Written criteria for "ships a cosine-threshold gate on a semantic
   property," applied by two coders, with agreement reported.
3. **The thresholds themselves, tabulated.** The distribution of hard-coded values is independently
   interesting — this repository's own gate was `0.85`, and R10a found the *effective* boundary was
   `0.80` while config, docstring, and register all advertised `0.40`.
4. **Function classification**, since a dedup gate and a safety gate carry different stakes.

Until then the honest phrasing is *"the pattern is widespread in shipped agent code and recommended
in practitioner guidance; we document N instances across M repositories"* — never a percentage.

---

## Reproducing this survey

GitHub code search results are ranked and change over time; these are not stable identifiers. The
queries are recorded above verbatim so the *method* reproduces even when the ranking does not. Run
with an authenticated `gh` and compare against the repositories named here.

---

# ⚠️ CORRECTION — 2026-07-26, prompted by Battery 5 v2

Battery 5 v2 found four ways `gh` search silently manufactures nulls. Asked whether those bugs
reached the other batteries, I tested rather than assumed. **Two of the four do not apply here; one
does, and it damages a claim in §1.**

## What does NOT apply

**Phrase-wrapping does not affect `gh search code`.** Verified: the same query as one argv element
and as separate elements both return 30 results. The bug that destroyed Battery 5 v1 did not touch
the code searches.

**Stale repo scope does not apply** — these were unscoped code searches, not `repo:`-scoped ones.

## What DOES apply: I was truncating, and I did not say so

`--limit` was set to 12–30 on every query in this survey. Re-run at `--limit 100`:

| query | distinct repos I saw | distinct repos available at limit 100 | I sampled |
|---|---|---|---|
| `poincare_exp_map` | 8 | **46** *(still capped)* | ~17% |
| `cosine_similarity 0.85 duplicate threshold agent` | 12 | **77** *(still capped)* | ~16% |
| `similarity_threshold 0.9 deduplicate memory agent` | 12 | **93** *(still capped)* | ~13% |

### For §2 (Paper A) this is safe — the error runs toward understatement

The claim is *"the pattern is widespread."* Finding 77–93 distinct repos where I reported 12 makes
that **more** true. The verified 9-of-11 hit rate is unaffected, since those were opened and read.
**Restate "36 distinct repositories" as a floor: at least 36, from queries that return 77–93 distinct
repositories at limit 100 and are still capped there.**

### For §1 (R13) the error runs the WRONG WAY, and the claim does not survive

§1 concluded the post-hoc-hyperbolic pattern is **RARE** — "~60 repositories surfaced, exactly one
confirmed instance." That is a null, and it now rests on having sampled **8 of at least 46**
repositories for the key query and inspected **three**. **A null drawn from a 17% truncated sample is
not evidence of rarity**, which is precisely the lesson Battery 5 was redone to learn.

> **Retracted:** *"the pattern is rare."* Not supported by this survey.
> **Stands:** *"one instance was confirmed, and confirmed rigorously"* — `unworthyzeus/HyperRAG`,
> demonstrated by execution, not inference.

### Does the R13 cancellation decision survive?

**Yes, on its other leg.** Cancelling the standalone R13 note rested on two independent conditions:

- **Kill-condition #6** (prevalence < ~5 instances) — **now weakened**; the sample cannot support it.
- **Kill-condition #4** (already published) — **unaffected.** [arXiv:2309.10013](https://arxiv.org/abs/2309.10013)
  states the constant-radius/Euclidean-isometry result, and that came from *reading the paper*, not
  from a search. R13 remains a section of Paper A rather than a standalone note.

The decision stands; one of its two supports does not. Recorded because the difference matters if
anyone revisits it.

## The generalisable lesson

**Every count in this document came from a ranked, capped sample, and a cap is invisible in the
output** — `gh` exits 0 with a clean, full-looking list. That is the same shape as the Battery 5
failure and the same shape as the finding this whole project is about: **an instrument that returns
a confident number while silently seeing only part of the field.** Any future prevalence work must
report the cap alongside every count.
