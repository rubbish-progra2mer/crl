# Research Problem

## User intent

User-approved controlled real-chain Commissioning test (run02). No research
sub-direction was given; the Main Codex selects the problem from the shared
knowledge base. The purpose of the run is to exercise the full chain under
real authenticity requirements and surface machine defects.

## Use Thesis and real consumer

Builders of long-horizon LLM agents with persistent external memory
(conversational assistants, long-lived task agents) must decide, at memory
build time, what unit their memory store indexes: single turns, whole
sessions, or constructed topical chunks. Today that unit is fixed globally
before any query arrives, and the retriever returns top-k units of that one
granularity for every query.

Observable limitation: oracle-retrieval experiments show a large gap between
what retrieval currently delivers and what the reader could do with the
right evidence (30-60 percent accuracy drop when reading full history versus
oracle evidence sessions), and turn-, session-, and summary-level units each
exhibit distinct retrieval and semantic-quality failures, so any single
fixed unit is mismatched for part of the query load.

Consequence of error: missing or noise-diluted evidence at read time causes
wrong answers and fabricated details in downstream agent responses; the
agent silently answers from partial memory.

## Decision interface

The implement sits in the memory read path. Input: the current query text
plus a memory store that maintains representations at more than one
granularity (fine units, their parent coarse containers, temporal
metadata). Output: the set of memory units handed to the reader, under a
fixed retrieval token budget. The real decision it changes: which
granularity's units (or which mix) are retrieved for this specific query,
instead of one global fixed choice for all queries.

## Value Bridge and proxy limit

Experimental proxy: retrieval-stage evidence quality (whether the units
handed to the reader cover the annotated evidence) under an equal returned-
token budget. The bridge to end value rests on the oracle-retrieval
evidence: when the reader is given the right evidence units, end-task
accuracy recovers most of the gap, so retrieval-stage coverage is a
causally-connected proxy, not an arbitrary one.

This proxy cannot prove: the size of the end-to-end answer-accuracy gain
for any specific reader model; reading-stage interaction effects (a reader
may still fail on covered evidence); or gains outside the tested memory
workload distribution.

## Mechanism Demand before carrier selection

Causal stage X: candidate-unit selection at memory read time.
Information I available at time T (query arrival): the query text, the
multi-granularity memory representations, temporal metadata. NOT available:
the answer, evidence annotations, or any outcome signal.

Decision change A to B: A = top-k retrieval over one globally fixed
granularity. B = allocate the same retrieval budget across granularities
conditioned on query-side features computable at time T (for example,
whether the query asks for a single fact, an aggregation over episodes, or
a multi-hop join).

Predicted mechanism signature S: stratified, non-uniform effects. Queries
needing aggregation over many episodes lose evidence coverage under fine
units and gain under coarse units; single-fact queries show the opposite or
no effect; query-conditioned allocation matches or beats every fixed
granularity on the mixed load while the per-stratum selection pattern
aligns with query type. A uniform average gain without stratum alignment
does NOT satisfy the signature.

Cost/permission/interface constraint C: equal returned-context token budget
across all compared arms; no arm may answer with more returned tokens; no
extra LLM calls at decision time beyond what fixed-granularity retrieval
already uses (query-side features must be computable with the local
encoder or cheaper).

Decisive counterexample R: if, on held-out annotated data, one fixed
granularity is simultaneously optimal (or statistically indistinguishable
from optimal) for every query type, then there is no type-by-granularity
interaction and the mechanism demand is void. This is the cheapest
workbench falsifier and must be attacked before full implementation.

### Carrier-independent statement

At memory read time, replace "retrieve top-k units from one globally fixed
granularity" with "allocate a fixed retrieval budget across coexisting
granularities of the same underlying history, conditioned on query features
available at query arrival", predicting that on mixed query loads evidence
coverage matches or exceeds every fixed-granularity baseline at equal
returned-token budget, with per-query-type selection patterns aligned to
information need.

### Predictions on two other carrier classes

1. Agent experience/insight stores (trajectory-level vs step-level vs
   distilled-insight units): queries about "how did we previously handle
   situations like this overall" should gain from coarse units; queries
   about "what exact call fixed error E" should gain from fine units;
   query-conditioned allocation should dominate any fixed unit on a mixed
   diagnostic load.
2. Repository-level code retrieval (function vs file vs module summaries):
   cross-cutting architecture queries should gain from coarse summaries;
   single-symbol queries from fine units; the same budget-allocation
   mechanism should transfer with the same stratified signature.

## Text/tool LLM Agent scope

Text-only long-horizon agent memory; no embodied, multimodal, or robotic
scope. The mechanism concerns the retrieval decision computation inside an
agent's memory subsystem.

## Soft constraints

Local execution: shared Python 3.11.15 venv, RTX 5060 Ti, local encoders
(sentence-transformers). Public, freely downloadable data only. Controlled
test: modest experiment scale with honest claim narrowing rather than
scale inflation.

## Hard exclusions

No paid API calls (none preauthorized in RUN_CHARTER). No environment-
feedback learning / execution recovery direction (corpus scope exclusion).
No claim about reading-stage or generation-stage improvements without
direct evidence.

## Cost authorization

PAID_API_PROVIDERS: NONE. PAID_API_BUDGET_CEILING: NONE. No key is stored.
Free public retrieval and local computation only; any step requiring paid
API moves the Run to BLOCKED_EXTERNAL first.
