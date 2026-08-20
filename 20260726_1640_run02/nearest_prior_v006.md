# Main Codex Nearest Prior Record (v005)

## Frozen before review

Written 2026-07-26 before Packet freeze; SHA recorded in RUN_LEDGER at
commit time; source snapshots = the probe records below.

## Search views

- Changed computation (neutral language): causal decomposition of
  stale-versus-current ranking bias in embedding retrieval over
  timestamped conversational memory, with granularity and scoring-arm
  ablations and a fixed-reader consequence arm.
- Key components: paired best-unit rank analysis; unit-granularity
  ablation; PPR/recency scoring arms; equal-budget reader protocol.
- Full pipeline: annotated update questions -> multi-arm retrieval
  measurement -> decomposition shares -> reader-arm consequences.
- Component combinations: stage decomposition (P010) + bias measurement
  (MemStrata-style) + consequence quantification.

## Exact searches

2026-07-26, open web (recorded in session transcript; key queries):
"Mix-of-Granularity RAG router"; "adaptive retrieval granularity
conversational memory 2025 2026"; "temporal knowledge update memory
graph stale amplification Zep Graphiti"; "retrieval near-duplicate
temporal conflict stale outranks current"; "time-aware reranking
recency reranking top-k temporal"; plus arXiv abstract/full-text reads:
2505.19549 (MemGAS, full PDF, SHA 256eba24...), 2606.26511 (MemStrata),
2606.01435 (deterministic freshness recipe), 2501.13956 (Zep),
2509.01306 (Re3), 2607.04088 (LongEval temporal overlay), 2603.16862
(Chronos), 2605.06132 (MemReranker), 2509.11353 (LLM reranker recency
bias), 2310.07712 (permutation self-consistency), 2601.19249 (GLOVE),
2606.24428 (EDV), 2604.27283 (risk-sensitive retrieval bandits).

## Component collisions

- Stage decomposition: P010 (in-corpus) - ancestor, not competitor;
  does not split stale/current inside retrieval.
- Embedding confusion measurement: MemStrata AUROC 0.59 - synthetic
  (s,r,o) triples; no granularity/propagation axes; no reader arm; and
  our K8/K11 falsifiers independently confirm the detection failure on
  natural dialogue.
- Recency bias measurement: 2509.11353 - LLM rerankers, not embedding
  retrieval; opposite bias direction of interest.

## Composition collisions

None found combining decomposition + granularity ablation + consequence
arm on conversational memory. Temporal-IR systems (Re3, overlays,
Chronos, Mem0) are REPAIR systems without causal decomposition;
deterministic recipes (2606.01435) operate at answer assembly on
serialized facts.

## Full-pipeline collisions

None found as of 2026-07-26. "Not found" is not proof of novelty; the
Prior Reviewer's independent search is the second view.

## Comparator roles and relative differences

Private prior ranking: nearest = P010 stage decomposition (method
ancestor); closest measurement = MemStrata AUROC study (different data
regime, narrower axes); current-strongest adjacent repair = Re3
(learned, different problem class). Collision verdict: attribution node
open; strongest reviewer challenge expected on (a) v007-precedent
boundary (is attribution a deliverable seed) and (b) single
encoder/reader scope.

## Closest-composition conclusion

No runnable competing decomposition exists to compare against; the
honest comparator set is internal (arm ablations) plus the cited
component priors. Claims stay measurement-scoped to this encoder,
dataset and reader; the receiver's scale-up (more encoders/datasets) is
the generalization path.

## v006 addendum

Unchanged from v005 (no new external search performed between the
config repair and this freeze; the delta is execution-parameter only).
The Prior Reviewer's independent search remains the second view.
