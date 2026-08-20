<!-- crl-v3-evidence-ids
["ev-p030-failure-core","ev-p064-experience-following-error"]
-->
# Research Map

## Observed Failure and boundary

- [CODEX_SYNTHESIS] First-hand (run02 v002 workbench, frozen at
  data_split_commitment_v002/falsifier_k5_results.json SHA 58B6242A60CC15
  011283B455CEC85742AB63181337D803F3E228EC24831A18E1): stale evidence
  session outranks current in 9/14 knowledge-update items under plain
  cosine retrieval; propagation does not amplify (K5 killed).
- [AUTHOR_FACT] Recognition of outdated memory does not transfer to
  applying updated state; late fusion gives no authority.
  [[evidence:ev-p030-failure-core]]
- [AUTHOR_FACT] High-similarity retrieved records induce imitation and
  compound errors. [[evidence:ev-p064-experience-following-error]]
- [CODEX_HYPOTHESIS] The inversion lives in the scoring layer; repairing
  order inside near-duplicate cross-session pairs suffices to put the
  current version first without global recency or unit removal.

## Intervention stage

Retrieval scoring, post-similarity pre-top-k. Reads query/embeddings/
timestamps; outputs adjusted ranking.

## Use Thesis, Value Bridge and Mechanism Demand

Bound to problem_v003.md; fixed before any Promotion outcome was read.
D and C buckets remain unread; W bucket is exposed workbench.

## Operator shortlist and source recheck

Card queries (2026-07-26, v003 round): failure hits again top
failure-retrieved-update-lacks-decision-authority (P030),
failure-retrieved-experience-propagates-stored-errors (P064) - the
target failure family; operator hits operator-write-side-state-
adjudication (P030, occupied write-side incumbent),
operator-learned-memory-crud-control (P062, learned write ops,
orthogonal node), operator-evidence-audit-before-score (P068 lineage,
audit-then-score structure loosely analogous at a different layer).
No in-corpus operator occupies the retrieval-scoring pairwise node.

## Competing method kernels

K8 (PRIMARY) - Near-duplicate pairwise temporal arbitration at scoring.
  Generation channel: FIRST-HAND WORKBENCH FAILURE (v002 falsifier) +
  incumbent-limitation analysis (MemStrata's AUROC-0.59 argument shows
  similarity cannot separate contradiction from duplication, but uniform
  temporal down-weighting inside the near-dup band does not need that
  separation - their justification for structured extraction skips this
  cheaper intervention). Carrier-independent statement: in
  problem_v003.md. Probes: occupancy scan in problem_v003 found the node
  OPEN; mandatory comparators fixed = plain cosine, global recency
  prior, large-k + assembly-recency (2606.01435 structure, adapted
  honestly to unserialized dialogue), and (ablation) arbitration without
  the cross-session constraint. Falsifier: preregistered defaults, W
  bucket, kill conditions in problem_v003. Disposition: KEEP pending
  falsifier.

K9 - Global recency prior on all units. Engineering standard; kept as
  comparator, not a kernel. Predicted to harm old-information queries.
K10 - Write-time near-dup pruning. Destroys reachability of old units
  (breaks queries about superseded state), needs online detection at
  every write. Retained only as design contrast; not run.

## Natural-language disposition

K8 keep (open node, first-hand failure evidence, cheap decisive
falsifier, zero-cost mechanism, clean single delta vs plain scoring);
K9 comparator; K10 contrast. Falsifier next; no candidate frozen before
its outcome.

## Family Viability

New family (scoring-layer staleness repair). One unverified leap: pair
arbitration fixes inversion without collateral harm. All support
components known.

## Candidate Promotion Audit

Deferred until falsifier outcome.

## Seed Readiness Audit

Not yet applicable.

## Unique narrow Gap

Pairwise temporal arbitration inside near-duplicate cross-session unit
pairs at retrieval scoring, schema-free, reachability-preserving.
Missing computation: the falsifier itself, then D-bucket promotion with
the fixed comparator set and an end-task reader arm.


## Workbench decisive falsifier - EXECUTED, K8 KILLED

Executed 2026-07-26 on the physically-separated W bucket only (93 items:
14 knowledge-update with both evidence sessions in haystack, 79
non-update with evidence). Preregistered defaults, no tuning loop:
tau=0.80 cross-session near-dup band, min 1-day gap, gamma=0.5 older-
member attenuation; global-recency comparator with half-life = half the
history span; K=10. Artifacts: workbench_v003/falsifier_k8.py and
falsifier_k8_results.json.

Result vs preregistered kill conditions: KILL under condition (a). K8
repaired only 1 of 9 stale-over-current inversions (9 -> 8). No-harm held
(1/79 hurt) but is irrelevant given the repair failure. The comparator
prediction was confirmed exactly: global recency repairs 7/9 inversions
but hurts 29/79 non-update items (mean evidence hits 6.09 -> 5.47).

Mechanism diagnosis (first-hand): update pairs are NOT near-duplicates in
embedding space - current/stale evidence units fall in the 0.6-0.75
similarity range, overlapping ordinary related-content pairs. This is
the retrieval-layer counterpart of MemStrata's AUROC-0.59 finding,
independently confirmed and localized: the failure is PAIR DETECTION,
not arbitration. Widening the band would sweep in ordinary related
pairs (the recency arm's 29/79 harm quantifies that collateral risk).
Schema-free pairwise arbitration faces a band-width dilemma that
parameter tuning cannot escape; per Family Viability, K8 is dead and
tau/gamma retuning is forbidden same-family continuation.

## Accumulated first-hand negative results (workbench-grade)

1. Propagation does not amplify staleness (+0.07 stale@10; v002).
2. Stale-over-current inversion is a base-similarity property (9/14).
3. Update pairs are not embedding near-duplicates; detection, not
   arbitration, is the binding constraint (this version).
4. Global recency: repairs 7/9 inversions, harms 29/79 non-update items
   - the repair/harm trade-off is now quantified.

These four results form a coherent mechanism map of why cheap schema-free
fixes fail on stale memory retrieval. They are WORKBENCH-grade (W bucket
only) and do NOT qualify for knowledge-base reflux under the
INTERNAL_RUN_EVIDENCE gate (which requires fresh-data verification); a
future version choosing to verify any of them on the untouched D bucket
could both use it as promotion evidence and qualify it for reflux.

## Version closure

All v003 kernels dead (K8 by falsifier; K9 was comparator-only; K10
contrast-only). v003 closes per problem-level-kill semantics. The
remaining open routes in this failure space all collide with occupied
nodes (structured extraction, LLM write/read gating, query
classification) or dead families. Problem/family RESET required for
v004. Data-role state: W exposed; D (222) and C (185) remain unread;
split commitment binding.
