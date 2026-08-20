<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-sparse-topology-suppresses-correct-insight","card_kind":"failure","paper_id":"P017","evidence_ids":["ev-p017-failure-core"],"source_refs":[{"path":"papers/P017_information_propagation_topologies.pdf","sha256":"f94767d936354030dc25f10db92a2f6f85f49b7d7163ac45b253e047ca67bd8b"}]} -->
# Sparse Communication Suppresses Correct Insight

## Observed failure
[AUTHOR_FACT] Reducing connectivity can block useful agent-level evidence from reaching the final decision. [[evidence:ev-p017-failure-core]]

## Conditions and scope
[CODEX_SYNTHESIS] Multi-agent graphs with controlled correct-answer interventions and chosen aggregation protocols.

## Failed intervention
[CODEX_SYNTHESIS] Topology sparsification treats fewer edges as inherently beneficial and ignores loss of beneficial information flow.

## Evidence and alternative explanations
[CODEX_SYNTHESIS] Dense graphs can propagate errors and consume more budget; the result does not imply full connectivity is universally optimal.

## Warning for future candidates
[CODEX_SYNTHESIS] Any topology Candidate must measure both error and insight propagation at matched communication cost.

## Possible repair boundary
[CODEX_HYPOTHESIS] Selective higher-order exposure or evidence-aware routing may preserve decisive sources without full connectivity.

## Evidence ledger
[AUTHOR_FACT] The cited passages bind this failure to admitted PDF bytes and current Passage SHA values. [[evidence:ev-p017-failure-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] sparse topology; insight propagation; information bottleneck; multi-agent graph; communication tradeoff

