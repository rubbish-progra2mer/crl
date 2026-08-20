<!-- crl-v3-evidence-ids
["ev-p010-index-retrieve-read","ev-p030-failure-core","ev-p011-failure-core"]
-->
# Research Map

## Observed Failure and boundary

- [CODEX_SYNTHESIS] Five workbench experiments (frozen in
  workbench_v003/ and workbench_v004/, hashes in RUN_LEDGER) establish
  on W bucket: turn-level stale-over-current inversion 9/14; propagation
  contribution zero; store-side near-dup arbitration repairs 1/9 (pairs
  at 0.6-0.75 similarity); competitive-band arbitration repairs 1/9
  (band size 1 in 10/14); sentence-level units reduce inversions to 7/14
  and swing mean margin from -0.064 to +0.011; residual driver is
  phrasing isomorphism between queries and initial statements.
- [AUTHOR_FACT] Oracle evidence restores most long-history performance;
  stage decomposition separates indexing/retrieval/reading.
  [[evidence:ev-p010-index-retrieve-read]]
- [AUTHOR_FACT] Recognition of outdated memory does not transfer to
  application. [[evidence:ev-p030-failure-core]]
- [AUTHOR_FACT] Fixed memory units create granularity-specific failures.
  [[evidence:ev-p011-failure-core]]

## Intervention stage

Measurement harness over the retrieval stage plus a fixed-reader
consequence arm; no production-path intervention claimed.

## Use Thesis, Value Bridge and Mechanism Demand

Bound to problem_v005.md. Promotion data (D bucket) remains unread at
this writing; kill conditions preregistered in the Problem.

## Operator shortlist and source recheck

v005 card queries: operator-memory-stage-decomposition (P010) is the
direct methodological ancestor - our decomposition extends it INSIDE the
retrieval stage along the stale/current axis; operator-stagewise-mcp-
cost-attribution shows stagewise attribution precedent in another
cluster; paper-longmemeval binds the carrier. No in-corpus operator
performs stale-bias decomposition.

## Competing method kernels

K12 (PRIMARY, attribution class) - Stale-bias causal decomposition with
  consequence arm. Generation channel: first-hand workbench failure
  (entire v002-v004 chain). Components all known (paired best-unit
  analysis, granularity ablation, scoring-arm ablation, fixed-reader
  protocol); the single unverified scientific leap: the W-bucket
  decomposition pattern replicates on untouched data AND converts to
  answer-level consequences. Falsifiers = preregistered kill conditions
  in problem_v005. Fresh Promotion carrier: D bucket (untouched, 37
  update + 185 non-update questions among 222).
  Novelty probes: occupancy scan in problem_v005 (LongMemEval gap
  location, MemStrata scope, recency-bias-in-rerankers scope) - node
  open. Disposition: KEEP.

Alternative kernels: none formed - this is a verification-and-
-quantification candidate whose routes were exhausted by mechanism
evidence in v002-v004; per CRL.md, when only one reasonable kernel
exists the exclusion evidence must be stated: retrieval-layer repair
kernels are closed by first-hand falsification (three signal classes),
write-side/extraction/LLM-gating kernels are occupied territory
(P030/P062/Zep/MemStrata/Mem0), and a repair candidate cannot be honest
before the failure structure itself is fresh-verified - which is
exactly K12.

## Natural-language disposition

K12 keep. The v007 precedent (static audit insufficient for delivery)
is the known boundary risk; K12 differs from v007 in three audited
ways: (a) it changes a stated real decision (architecture investment
direction) rather than observing data construction; (b) it carries an
answer-level consequence arm with a fixed reader at equal budget; (c)
its decomposition is mechanism-level (three quantified components),
not descriptive. Whether that satisfies the delivery bar is exactly
what the three reviewers and the Decision must test - appropriate for
a Commissioning chain test.

## Family Viability

New family (attribution). Viable while D-bucket kill conditions remain
unmet.

## Candidate Promotion Audit

Pre-Promotion answers:
- Use Thesis/Value Bridge: above; consumer = memory-system builders and
  benchmark maintainers; decision changed = staleness-defense placement.
- Target Failure variable: stale-over-current inversion rate and its
  answer-level error consequence.
- Candidate changes which decision variable: none in production; it
  fixes the measurement that current architecture decisions lack.
- Why not just validity/format: the reader arm ties inversion directly
  to answer errors.
- Main unverified leap and falsifier: W-pattern replication + consequence
  conversion; kill conditions 1-3 preregistered.
- Promotion freshness: D bucket physically separated, never loaded by
  any analysis code; only question_id/question_type were extracted at
  split time.
- Closest existing composition: LongMemEval stage decomposition (P010)
  + MemStrata AUROC analysis; neither performs this decomposition nor
  the consequence arm; both are cited as components, not competitors.

## Seed Readiness Audit

Deferred until Promotion Development completes.

## Unique narrow Gap

A fresh-data-verified, consequence-quantified causal decomposition of
stale bias in schema-free conversational memory retrieval. Missing
computation: the D-bucket replication and reader arm themselves.
