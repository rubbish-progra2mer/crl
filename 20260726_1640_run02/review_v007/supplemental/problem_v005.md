# Research Problem

## User intent

Controlled Commissioning run02, v005. Directive: continue autonomously
until genuine delivery; the attribution candidate formed from the
v002-v004 first-hand mechanism map now enters the full chain.

## Occupancy scan before problem commitment

Prior scans (v003/v004) mapped all repair nodes. For the ATTRIBUTION
problem class: LongMemEval (P010) reports the oracle-retrieval gap and
stage decomposition but does NOT decompose stale-vs-current bias inside
update questions; MemStrata measures contradiction-vs-duplication
embedding confusion (AUROC 0.59) on synthetic triples, not conversational
evidence pairs, and does not quantify granularity or propagation
contributions; recency-bias studies (2509.11353) cover LLM rerankers,
not embedding retrieval bias decomposition. No occupant found for a
causal decomposition of stale bias in schema-free conversational memory
retrieval with an answer-level consequence arm. Node open.

## Use Thesis and real consumer

Builders of schema-free conversational agent memory, and maintainers of
long-memory benchmarks, deciding where staleness defenses must live.
Current decision practice assumes retrieval-layer recency heuristics are
a reasonable first line. The v002-v004 evidence says the assumption is
wrong for update questions, and locates why. If verified on fresh data
with quantified answer-level consequences, the finding redirects real
architecture investment (representation/write-side, not retrieval
patches) and motivates update-question design in benchmarks.

## Decision interface

Not an implement in the retrieval path: the deliverable is a verified
causal decomposition plus consequence quantification, changing
architecture-investment and benchmark-design decisions. The
"implementation" is the frozen measurement harness (deterministic,
local encoders + fixed reader protocol) that any third party can rerun.

## Value Bridge and proxy limit

The decomposition itself is retrieval-stage; the reader arm converts it
to answer-level consequences: with a fixed reader (deepseek-chat) at
equal returned-token budget, compare answer correctness when the top-k
context is stale-dominated (natural turn-level retrieval) vs when the
current evidence is present (sentence-level retrieval and oracle-current
control). Cannot prove: generalization beyond the tested encoder family
and dataset; write-side or LLM-gating solutions' actual effectiveness
(only that retrieval-layer patches fail); human-user consequences.

## Mechanism Demand before carrier selection

Fixed in v004 from first-hand evidence; v005 preregisters its fresh-data
verification: stale bias decomposes into phrasing isomorphism (dominant),
chunk dilution (secondary; removed by sentence units), propagation
(zero). Decisive counterexamples (kill conditions) on D bucket:
(1) D-bucket turn-level inversion rate is not materially above chance
    (below 40 percent) -> the phenomenon does not replicate;
(2) sentence-level indexing does NOT reduce inversions or improve the
    current-minus-stale margin -> dilution attribution fails;
(3) the reader arm shows no answer-accuracy difference between
    stale-dominated and current-included contexts at equal budget ->
    the bias has no downstream consequence and the Use Thesis collapses.

### Carrier-independent statement

In timestamped conversational memory with annotated update questions,
paired best-unit analysis under unit-granularity ablation and scoring-arm
ablation decomposes retrieval stale bias into phrasing-isomorphism,
dilution and propagation components; the method transfers to any
timestamped store with update annotations.

### Predictions on two other carrier classes

1. Agent experience stores with revision annotations: same
   decomposition; expect isomorphism dominance where task descriptions
   are reused verbatim.
2. Versioned wiki/document retrieval: dilution share should rise (edits
   embed in long pages), isomorphism share fall (queries rarely quote
   page openings).

## Text/tool LLM Agent scope

Text-only agent memory subsystems; measurement harness + fixed reader.

## Soft constraints

Retrieval stages local; reader arm uses preauthorized deepseek-chat with
full API discipline (raw jsonl, per-row model version, interleaved arms,
segment checkpoints, secret redaction). Usage reported.

## Hard exclusions

No claims about repair effectiveness of occupied nodes; no training; no
entity extraction; C bucket untouched until delivery.

## Cost authorization

Per RUN_CHARTER (deepseek preauthorized, user-unlimited 2026-07-26).
Estimated reader-arm usage: about 37 update questions x 3 context arms
x approx 2k tokens in / 100 out, plus judging - well under 1 USD; exact
usage will be reported.
