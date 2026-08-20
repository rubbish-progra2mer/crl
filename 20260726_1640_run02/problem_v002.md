# Research Problem

## User intent

Continuation of the user-approved controlled Commissioning run02 after v001
closed with all kernels probe-killed and the user granted deepseek paid-API
preauthorization. v002 re-opens from a different failure structure.

## Use Thesis and real consumer

Builders of long-horizon agent memory systems in the 2025-2026 mainstream
design family: memory stores organized as UNSTRUCTURED similarity
association graphs over multi-granularity units, retrieved with graph
propagation (association edges built from embedding similarity; retrieval
scores spread via Personalized-PageRank-style diffusion). This family
deliberately avoids entity/triple extraction to stay schema-free and
low-maintenance.

Their current decision: adopt propagation-based retrieval for its recall
gains on associative queries, with no temporal semantics on association
edges. Observable limitation: when the underlying history contains updated
facts (the user changed jobs, a preference was revised, a config value was
replaced), the old and new versions of the same fact are the MOST
surface-similar items in the store, therefore receive the STRONGEST
association edges, and propagation amplifies them together.

Consequence of error: on update-sensitive queries the retriever returns
the stale version alongside or ranked above the current one; the reader
answers from outdated state; the agent silently acts on superseded facts.
Existing temporal-validity mechanisms (bi-temporal entity-KG edge
invalidation; deterministic triple supersession ledgers) all require
structured fact extraction, which this design family has explicitly opted
out of - so its builders currently have NO compatible staleness defense.

## Decision interface

The implement sits inside the retrieval propagation computation. Input:
the query, the multi-granularity unit store, the similarity association
graph with per-unit timestamps (available for free in any conversational
log). Output: the ranked unit set handed to the reader. The real decision
it changes: how relevance mass flows across association edges - from
time-symmetric diffusion to temporally-directed diffusion (edges between
near-duplicate units pass mass toward the newer unit and attenuate toward
the older one), with no entity extraction, no schema, no LLM calls added
at query time.

## Value Bridge and proxy limit

Primary proxy: retrieval-stage stale-vs-current outcome on annotated
update queries (does the returned set contain the current value; is the
stale version ranked above it) at equal returned-token budget, plus
end-task answer correctness with a fixed reader on the same queries. The
bridge: reading from a context where the stale version dominates is a
direct, mechanically traceable cause of wrong answers on update queries;
public long-memory benchmarks annotate exactly this query class.

Cannot prove: gains on memory workloads without updates (predicted
neutral; must be verified as a no-harm control, not assumed); transfer to
stores whose units carry no usable timestamps; reader-stage robustness
when both versions are returned with explicit recency labels.

## Mechanism Demand before carrier selection

Causal stage X: association-graph propagation during memory retrieval.
Information I available at time T (query arrival): query text, unit
embeddings, association edges, per-unit ingestion timestamps. NOT
available: gold answers, update annotations, entity schemas.

Decision change A to B: A = time-symmetric propagation over similarity
edges (current mainstream). B = the same propagation with temporal
direction on high-similarity edge pairs: between two units whose
similarity exceeds the near-duplicate band, mass flow toward the older
unit is attenuated by a function of (similarity, time gap); all other
edges unchanged.

Predicted mechanism signature S (stratified): (1) on update-class queries,
the symmetric-propagation system retrieves the stale version at or above
the current version significantly more often than no-propagation direct
retrieval - i.e. propagation itself AMPLIFIES staleness (failure
confirmation, testable before any repair); (2) temporal direction removes
most of that amplification while (3) non-update queries are statistically
unharmed; (4) a global recency-boost heuristic (the obvious cheap
alternative) either harms non-update queries needing old information or
fails to fix update queries - the repair must be edge-local, not global.

Cost constraint C: equal returned-token budget across arms; no additional
LLM calls at query time; timestamps only (no extraction pipeline).

Decisive counterexample R (cheapest workbench falsifier): if, on a small
annotated workbench slice, symmetric propagation does NOT retrieve stale
versions more often than direct no-propagation retrieval (no amplification
exists), the mechanism demand is void and the kernel dies before any
implementation.

### Carrier-independent statement

In memory stores organized as similarity association graphs, graph-
propagation retrieval systematically amplifies superseded versions of
updated facts, because old and new versions of the same fact form the
strongest similarity edges; making propagation temporally directed on
near-duplicate edges removes this amplification without structured fact
extraction and without harming non-update queries.

### Predictions on two other carrier classes

1. Agent experience stores: after a policy/environment change, old and
   new experience entries for the same task family are strongly similar;
   propagation-based experience retrieval should measurably amplify
   obsolete experiences, and temporal edge direction should suppress them
   without harming stable-task recall.
2. Versioned document/wiki retrieval with association graphs: revisions
   of the same page are near-duplicates; the same amplification and the
   same edge-local repair signature should appear.

## Text/tool LLM Agent scope

Text-only agent memory subsystems. No embodied/multimodal scope. The
intervention is a retrieval-computation change inside the agent's memory
read path.

## Soft constraints

Local encoders and graph computation on the shared venv/GPU; deepseek-chat
(preauthorized) for memory construction (summaries/keywords where the
carrier pipeline requires them), reading, and judging, spent judiciously
with per-experiment usage reporting. Public data only.

## Hard exclusions

No entity/triple extraction pipeline as part of the proposed mechanism (it
is the incumbents' territory and breaks the schema-free Use Thesis). No
environment-feedback learning. No claim over stores lacking timestamps.

## Cost authorization

PAID_API_PROVIDERS: deepseek (user-granted 2026-07-26, budget
user-unlimited, spend judiciously). Key held only in process-scoped
temporary environment variables at execution time; never written to any
file, argv, artifact, packet or log.
