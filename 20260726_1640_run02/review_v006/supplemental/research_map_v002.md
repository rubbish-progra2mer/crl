<!-- crl-v3-evidence-ids
["ev-p030-failure-core","ev-p030-recognition-application-gap","ev-p064-experience-following-error","ev-p011-failure-core","ev-p063-dynamic-link-generation"]
-->
# Research Map

## Observed Failure and boundary

- [AUTHOR_FACT] In STALE, explicit recognition of an outdated memory does
  not reliably transfer to applying the updated state downstream; late
  fusion exposes both versions with no authority.
  [[evidence:ev-p030-failure-core]] [[evidence:ev-p030-recognition-application-gap]]
- [AUTHOR_FACT] Retrieved records with high input similarity induce
  imitation and repeat/compound stored errors.
  [[evidence:ev-p064-experience-following-error]]
- [AUTHOR_FACT] Turn/session/summary units exhibit distinct retrieval and
  semantic failures; the 2025 design response is multi-granularity stores
  with similarity association and propagation. [[evidence:ev-p011-failure-core]]
- [AUTHOR_FACT] A-Mem builds dynamic links from similarity at write time
  and retrieves through them, with no temporal semantics on links.
  [[evidence:ev-p063-dynamic-link-generation]]
- [CODEX_SYNTHESIS] Structural failure prediction (not yet in any source):
  in similarity-association stores, the old and new versions of an updated
  fact are the most surface-similar pair, hence get the strongest edges;
  time-symmetric propagation (PPR-style) then amplifies the stale version
  into retrieval results precisely on update-sensitive queries. This
  UPSTREAM amplification is distinct from P030's downstream
  recognition-vs-application gap: P030 assumes both versions arrive at the
  reader; we predict propagation makes the stale one arrive MORE.
- [CODEX_HYPOTHESIS] Temporally directing only the near-duplicate edges
  (attenuate mass flow toward the older unit) removes the amplification
  without schemas, extraction, or query-time LLM calls, and without
  harming non-update queries.

## Intervention stage

Association-graph propagation inside memory retrieval: after per-unit
similarity scoring, before final ranking. Reads: query, embeddings, edges,
per-unit timestamps. Outputs: ranked unit set under fixed token budget.

## Use Thesis, Value Bridge and Mechanism Demand

Bound to problem_v002.md (SHA b84f9092b6acd4d889c4e7838fb66d324b7f07c597
1640325db0ebe114b12e4b), fixed before any carrier outcome was read. No
Promotion carrier outcome has been read in this version.

## Operator shortlist and source recheck

Formal card queries (2026-07-26, three kinds): top failure hit
failure-retrieved-update-lacks-decision-authority (P030); top operator
hits operator-write-side-state-adjudication (P030; write-side, requires
typed state - different causal node, complementary incumbent),
operator-dynamic-linked-memory-evolution (P063 A-Mem; the in-corpus
representative of the similarity-link family and a predicted victim of
the failure), operator-learned-memory-crud-control (P062; learned write
ops, orthogonal), operator-experience-insight-update (P018).

Lineage chain (memory cluster): MemGPT paging -> LongMemEval stage
decomposition -> SeCom topical construction -> A-Mem linked evolution ->
Memory-R1 learned CRUD -> STALE adjudicated state. External continuation
(post-corpus-freeze, read directly): MemGAS multi-granularity association
+ entropy routing + PPR (arXiv:2505.19549v2, local PDF SHA 256eba243061
1820eb4b18978fdd35f05a3bcf26c7b808b03ef0971ab3bc49c8); HippoRAG 2 as its
strongest graph baseline. Next natural step along the chain that is NOT
occupied: temporal semantics of the similarity edges themselves.

Cross-cluster probe: the failure structure "propagation over similarity
edges amplifies wrong items" mirrors multi-agent correlated-error
propagation (dense topologies spread errors; failure-sparse-topology hit)
- the shared property is untyped high-similarity edges carrying trust.
Accepted as supporting intuition only; no operator transferred.

## Competing method kernels

K5 (PRIMARY) - Temporally-directed propagation on near-duplicate edges.
  Carrier-independent statement: in problem_v002.md. Generation channel:
  incumbent-limitation analysis (MemGAS/A-Mem structural reading) +
  Failure-native (P030/P064). Changed computation: edge-local temporal
  attenuation inside PPR-style diffusion; timestamps only. Predicted
  signature: stratified (amplification confirmed on update queries under
  symmetric propagation vs direct retrieval; directed propagation removes
  it; non-update queries unharmed; global recency boost fails one side).
  Cheapest falsifier: workbench slice - if symmetric propagation does not
  amplify staleness vs direct retrieval, kernel dies. Fresh Promotion
  carrier: available (update-annotated long-memory QA, commit-reveal
  bucketing; carriers not yet downloaded, no outcome read).
  Novelty probes (2026-07-26, all read at least at abstract level, key
  ones at full text): Zep/Graphiti = entity-KG bi-temporal edge
  invalidation, requires extraction; MemStrata (arXiv:2606.26511) =
  deterministic (s,r,o) supersession ledger, explicitly does not study
  propagation; MemGAS/HippoRAG 2/A-Mem = similarity graphs WITHOUT
  temporal edge semantics. Component collision: recency weighting in
  ranking is standard engineering - but it is global and rank-level, not
  edge-local and propagation-level; kept as a mandatory comparator.
  Disposition: KEEP.

K6 - Reader-side authority prompting (label retrieved units with recency
  and instruct the reader to prefer current state). Same causal node as
  P030's diagnosed failure; P030 shows recognition does not transfer to
  application, and prompting-level fixes at the reader are the incumbent
  territory plus a prompt-family change only. Disposition: KILL (occupied
  + weakest causal leverage).

K7 - Write-time near-duplicate edge pruning (resolve at association
  construction: do not link old/new versions, or link with supersession
  mark). Same information as K5 but destroys graph history irreversibly,
  requires online conflict detection at every write, and cannot be
  applied retroactively to an existing store; K5 is query-time, reversible
  and store-preserving. Both share the one unverified leap (temporal
  direction on near-duplicate edges controls staleness amplification);
  K7 kept as a natural ablation arm inside K5's experiment rather than a
  separate candidate. Disposition: REFRAME into K5 ablation.

## Natural-language disposition

K5 keep: only route whose causal node (propagation computation) is
unoccupied across all probes; evidence-backed failure prediction; cheap
decisive falsifier exists; carrier and comparators runnable with local
compute plus preauthorized deepseek; not chosen for carrier convenience -
chosen because the failure is structurally implied by the incumbent
design family and no compatible defense exists for that family. K6 kill:
occupied causal node with demonstrated weakness (P030). K7 reframe:
same scientific leap as K5, strictly worse operational properties;
retained as ablation. Workbench probes for K5's falsifier are the next
step and MUST precede candidate freezing.

## Family Viability

Family opens with K5. Reset conditions per CRL.md apply; the single
unverified scientific leap is the amplification-and-repair mechanism;
support components (encoders, PPR, benchmark harness) are all known.

## Candidate Promotion Audit

Deferred until after the workbench decisive falsifier (correct order:
falsifier may kill before any Candidate is frozen).

## Seed Readiness Audit

Not yet applicable.

## Unique narrow Gap

Temporal semantics of similarity-association edges during retrieval
propagation in schema-free memory stores: the amplification failure is
unmeasured and the edge-local repair is unowned. Still missing
computation: the falsifier measurement itself, then the directed-
diffusion implementation and equal-budget comparators.


## Workbench decisive falsifier - EXECUTED, K5 KILLED

Executed 2026-07-26 on the WORKBENCH bucket only (14 knowledge-update
items of LongMemEval-s; split commitment SHA 00A30A73B532E1334EC4AA23976C
53381DDB359E2BE995B72D83FBC30849F4E3). Local compute only: MiniLM turn
units, kNN-10 symmetric similarity graph, PPR (damping 0.5, 30 iters),
K=10, single preregistered default configuration, no tuning loop. Script
and raw per-item results retained in the session scratchpad
(falsifier_k5.py / falsifier_k5_results.json).

Preregistered kill condition: if symmetric propagation does not retrieve
stale versions more than direct retrieval, the mechanism demand is void.

Result: KILL. PPR mean stale@10 = 4.79 vs direct 4.71 (+0.07, noise
level); per-item direction unstable (5 more / 3 less / 6 equal). The
amplification arrow of K5 is refuted at the cheapest stage.

NEW FIRST-HAND OBSERVATION (workbench-grade, not yet fresh-verified): in
9/14 items the stale evidence session's best unit OUTRANKS the current
evidence session's best unit already in DIRECT retrieval (stale at rank 0
in 9 items). Staleness inversion is a base-similarity-layer property -
surface similarity does not encode temporal validity - and propagation
merely inherits it. Any future kernel must target the scoring layer or
the near-duplicate pair ordering, not the propagation computation.

## Version closure

All v002 kernels are now dead (K6/K7 pre-freeze, K5 by falsifier). Per
CRL.md section 6 problem-level-kill semantics, v002 closes with
problem_v002.md and this research map; no Candidate, experiment or
decision documents are owed. The next problem enters v003. Data-role
state carried forward: LongMemEval-s W bucket is exposed workbench; D
and C buckets remain unread; the split commitment remains binding for
any future version that uses this dataset.
