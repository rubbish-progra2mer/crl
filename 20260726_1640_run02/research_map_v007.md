<!-- crl-v3-evidence-ids
["ev-p010-index-retrieve-read","ev-p030-failure-core","ev-p011-failure-core"]
-->
# Research Map

## Version lineage

v007 inherits research_map_v006 (SHA c997409105925155bd21bf168be9f4f3
ebc02bd56b42bb70f93f9c0858f0e4b9) with the decision_v006 corrections.
The audits of v006 remain the record of the pre-review state; this map
records the post-review repairs.

## Post-review corrections (bound to decision_v006)

- [CODEX_SYNTHESIS] Scoring record corrected: 29/34/32; judge frozen;
  full verdict table produced; two reviewers independently found the
  same error, confirming the review layer works.
- [CODEX_SYNTHESIS] The item-level conversion sentence of result_v006
  is retracted: frozen raw shows inverted items err at 4/22 vs 3/15
  non-inverted, and 2 of 5 stale answers occurred with current-first
  retrieval. The consequence story is context-composition-level.
- [CODEX_SYNTHESIS] "Causal decomposition" demoted for the residual
  component: dilution and propagation are interventional; phrasing
  isomorphism is residual attribution with an unregistered proxy.

## Named nearest neighbors (added per Reviewer 1)

- MemConflict (arXiv:2605.20926): closest external composition -
  multi-session dialogue conflicts incl. updates, white-box retrieval
  metrics (SEH@K, SRS) plus answer accuracy across six systems.
  Difference: no stale-vs-current inversion measurement, no
  granularity/propagation attribution, no per-component decomposition.
- Collapse of Dense Retrievers (arXiv:2503.05037): closest
  methodological structure - controlled bias diagnosis (literal
  matching, brevity, position) with RAG consequence experiment. Our
  residual component is plausibly their literal-matching bias
  instantiated on temporal update pairs; stated explicitly.
- MemoryAgentBench FactConsolidation (ICLR 2026): answer-level
  conflict/update evaluation; no retrieval-layer decomposition.
- Dense X Retrieval (arXiv:2312.06648), SGMem (arXiv:2509.21212):
  granularity-unit neighbors for the sentence-level component,
  alongside SeCom (P011, in-corpus).
- Unchanged from v005 scans: LongMemEval (ancestor), MemStrata,
  STALE, Zep/Graphiti, 2606.01435, Re3/Chronos/MemReranker,
  recency-bias-in-rerankers 2509.11353.

## Operator shortlist, kernels, viability

Unchanged from v006 (K12, attribution class). No new kernel; v007 is
a record repair. Family viable pending re-review.

## Candidate Promotion Audit / Seed Readiness Audit (v007 delta)

The v006 audits stand with these amendments: the consequence answer is
downgraded to directional-with-intervals; the "worth delivering"
answer now rests on (i) the verified harness, (ii) the temporal-
blindness finding and component shares as scoped, (iii) the enumerated,
cheap, preregistered falsification path for the receiver - and NOT on
any quantified consequence claim.

## Unique narrow Gap

Unchanged: fresh-data-verified, consequence-OBSERVED (directional)
decomposition harness for stale bias in schema-free conversational
memory retrieval; no occupant found by main-Codex scans plus Reviewer
1's independent 11-query open-web search as of 2026-07-26.
