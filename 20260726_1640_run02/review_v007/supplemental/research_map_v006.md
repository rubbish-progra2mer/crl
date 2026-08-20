<!-- crl-v3-evidence-ids
[]
-->
# Research Map

## Version lineage

v006 inherits research_map_v005.md (SHA db970e14f49d56add825d1d95c4e0c
53eeea90ad97644a51495893bd1b321566) in full by reference; this map only
records the v005->v006 delta and its justification.

## Delta and justification

- [CODEX_SYNTHESIS] v005 dev_reader_001 raw rows show
  completion_tokens_details.reasoning_tokens consuming the entire
  100-token budget in 47/111 responses (empty answers 19/18/10 across
  arms - a confound, not signal). The reader model deepseek-v4-flash is
  a reasoning model; the defect is config-level, not mechanism-level.
- [CODEX_SYNTHESIS] Retrieval decomposition results from v005
  dev_local_001 stand: they used no reader and no API.
- [CODEX_HYPOTHESIS] Under max_tokens=1000 the answer-level ordering
  oracle_current > sentence_topk > turn_topk will emerge if and only if
  retrieval staleness converts to answer errors (Kill 3 decides).

## Candidate Promotion Audit (post-Development addendum for v006)

Deferred to after dev_reader attempt in v006; the pre-Promotion answers
of research_map_v005 remain binding.

## Unique narrow Gap

Unchanged from v005.


## Candidate Promotion Audit - post-Development answers

- Baseline shows Target Failure on Development data: yes - turn/direct
  inversion 22/37 (59.5%) on the fresh D bucket, and the failure
  converts to 5 confidently-wrong stale answers with a fixed reader.
- Isolation between Development and reserved Confirmation: question_id
  hash buckets (deterministic, physically separated files). Supports
  fixed-scope claims on this dataset/encoder/reader; does NOT support
  cross-dataset, cross-encoder or cross-reader generalization - claim
  contract already restricts accordingly.
- Clustering unit: question (haystacks independently sampled by the
  benchmark); no shared-template inflation identified within update
  items.
- Final outcome variable improved, not proxy only: answer accuracy with
  a fixed reader (81->92 percent turn->sentence; stale answers 5->~0),
  alongside retrieval-stage decomposition.
- Unique delta vs bundle: the measurement harness is the deliverable;
  arm deltas isolate each mechanism share (granularity, propagation,
  recency) by construction; reader arms share every parameter except
  context construction.
- Worth delivering as seed: yes - all three preregistered kills failed
  to trigger on untouched data; the contribution redirects a real
  architecture decision and its scale-up path is mechanical (more
  encoders, readers, datasets; then C bucket).

## Seed Readiness Audit

1. Carrier-independent statement: yes (problem_v005 sections
   incorporated in problem_v006; the decomposition method statement
   names no benchmark).
2. Preregistered mechanism signature observed in Promotion Development:
   yes at both stages - retrieval (dilution share 22->16 inversions,
   propagation ~0, recency bluntness 6/37 with harm) and answer level
   (stale-answer conversion; sentence removes it). Conditions where NOT
   observed: none contradicting; oracle<sentence on 2 items noted as
   boundary observation.
3. Closest-composition comparator: no external runnable decomposition
   exists (nearest_prior_v005); internal arm matrix serves as the
   comparator set; 2606.01435-style assembly-recency was considered and
   scoped as answer-layer, different node.
4. Strongest neighbors: P010 stage decomposition (ancestor), MemStrata
   AUROC study (different data regime), Re3/Chronos/MemReranker (repair
   systems, different class). Residual difference: causal decomposition
   + consequence arm on conversational memory, schema-free.
5. Reserved Confirmation: C bucket, 185 questions (27 update),
   physically separated file SHA 28a5710998..., untouched; proof =
   deterministic split rule re-runnable by receiver; plan = rerun the
   identical frozen harness (v006 artifacts) on the C file.
6. Where scale-up most likely breaks: (a) other encoders may not show
   the same isomorphism dominance (first scale-up step: repeat
   dev_local on 2-3 encoders); (b) stronger readers may self-correct
   stale contexts (second step: repeat reader arm with a stronger
   model); (c) datasets with paraphrased update annotations may shift
   shares. Cheapest verification order: encoders (local, hours) ->
   readers (API, <5 USD) -> C bucket -> new datasets.
7. Worth delivering: yes, as a measurement-grade seed with explicit
   v007-precedent discussion left to reviewers and Decision.
