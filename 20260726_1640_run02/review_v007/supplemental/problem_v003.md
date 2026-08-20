# Research Problem

## User intent

Continuation of controlled Commissioning run02. v003 opens from the
first-hand v002 workbench observation, per the machine's new
first-hand-workbench-failure generation channel.

## Occupancy scan before problem commitment

Failure space: stale versions of updated facts polluting agent memory
retrieval. Intervenable causal nodes and their occupancy (scanned
2026-07-26, open web + corpus):

- Write-side typed-state adjudication: OCCUPIED (STALE/CUPMEM, P030;
  Memory-R1 learned CRUD, P062; Mem0 LLM update ops).
- Entity-KG temporal edge invalidation: OCCUPIED (Zep/Graphiti,
  arXiv:2501.13956) - requires entity extraction.
- Structured triple supersession ledger: OCCUPIED (MemStrata,
  arXiv:2606.26511) - requires (s,r,o) normalization.
- Answer-assembly deterministic recency: OCCUPIED (arXiv:2606.01435,
  candidate extraction + max(serial/timestamp) on serialized synthetic
  facts) - assumes extractive QA downstream and retrieval already
  returning both versions.
- Use-side hypothesis verification / selective re-execution: OCCUPIED
  (GLOVE arXiv:2601.19249; EDV arXiv:2606.24428).
- Propagation-layer temporal direction: TESTED AND DEAD (run02 v002
  falsifier: propagation does not amplify staleness; +0.07 stale@10).
- RETRIEVAL-SCORING-LAYER pairwise temporal arbitration inside
  near-duplicate unit pairs, schema-free, old units kept reachable:
  OPEN. No occupant found; nearest neighbors are global recency priors
  (engineering heuristic, harms old-information queries) and index-
  governance dedup (offline ops practice, removes rather than reorders).

This problem targets the open node.

## Use Thesis and real consumer

Builders of schema-free conversational agent memory (no entity/triple
extraction). First-hand evidence from v002 workbench (14 knowledge-update
items, LongMemEval-s W bucket): the stale evidence session's best unit
OUTRANKS the current one in plain cosine retrieval in 9/14 items (stale
at rank 0 in 9). Their retriever silently prefers superseded state; every
downstream computation inherits it. Consequence: wrong answers and
actions on updated facts, invisible unless both versions are compared.

## Decision interface

Inside retrieval scoring, after per-unit similarity, before final top-k:
input = query, unit embeddings, per-unit timestamps; output = adjusted
ranking. Changed decision: relative order WITHIN near-duplicate
cross-session unit pairs (older member attenuated), all other scores
untouched. No extraction, no LLM calls, no removal of old units.

## Value Bridge and proxy limit

Proxy: current-vs-stale ordering and evidence coverage at fixed k on
annotated update queries; no-harm control on non-update queries; then
end-task answer accuracy with a fixed reader (deepseek-chat) at equal
returned-token budget. Bridge: reader receives stale-dominated context in
the failure case by direct mechanical causation. Cannot prove: gains when
timestamps are absent or unreliable; reader-stage robustness given both
versions with labels; transfer beyond conversational memory without new
experiments.

## Mechanism Demand before carrier selection

Causal stage X: retrieval scoring layer. Information I at query time:
query, embeddings, timestamps. NOT available: gold answers, annotations,
schemas. Decision change A to B: A = rank purely by query-unit
similarity; B = same, plus edge-local temporal arbitration inside
near-duplicate cross-session pairs (attenuate the older member by a
fixed factor), leaving non-duplicate units and old-information
reachability intact.

Predicted signature S (stratified): update queries - current version's
best unit rises above stale in most items where inversion existed;
non-update queries - evidence hit@k statistically unchanged (the
arbitration only touches near-duplicate pairs, which are rare outside
update chains); global-recency comparator fails one side (harms
old-information queries or under-fixes pair inversions).

Cost constraint C: equal k and returned-token budget; zero additional
model calls at query time.

Decisive counterexample R (cheapest falsifier, W bucket only): if
pairwise arbitration at preregistered default parameters fails to fix
the majority of observed inversions, or breaks non-update evidence
hit@k, the kernel dies.

### Carrier-independent statement

In schema-free memory retrieval, surface similarity does not encode
temporal validity, so superseded versions of updated facts systematically
outrank current ones; arbitrating order only inside near-duplicate
cross-context unit pairs using timestamps repairs this inversion at zero
query-time model cost, without removing old units and without a global
recency prior.

### Predictions on two other carrier classes

1. Agent experience stores: obsolete strategies outrank revised ones for
   the same task family; pair arbitration should restore revised-first
   ordering without harming queries about deprecated behavior.
2. Versioned internal wikis/docs with flat embedding retrieval: old
   revisions outrank current after minor edits; same repair signature.

## Text/tool LLM Agent scope

Text-only agent memory retrieval computation.

## Soft constraints

Falsifier and retrieval-stage work fully local (MiniLM, GPU). Reader/judge
stages use preauthorized deepseek within charter boundary, usage reported.

## Hard exclusions

No entity/triple extraction; no environment-feedback learning; no claims
where timestamps are absent; no removal/deletion of old units.

## Cost authorization

Per RUN_CHARTER: deepseek preauthorized (user-unlimited 2026-07-26),
key never written to files; local computation otherwise.
