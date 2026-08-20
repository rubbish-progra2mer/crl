<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-cascaded-multiagent-meta-routing","card_kind":"operator","paper_id":"P023","evidence_ids":["ev-p023-operator-core","ev-p023-cascaded-routing-core"],"source_refs":[{"path":"papers/P023_masrouter.pdf","sha256":"1bf45eaa68515ae2a6d3de2e2240ac321fef37a46ba831718aacee52bb12f457"}]} -->
# Cascaded Multi-Agent Meta-Routing

## Intervention target
[CODEX_SYNTHESIS] Query-conditioned selection of the multi-agent computation itself.

## Before and after computation
[CODEX_SYNTHESIS] A router selects one model. The changed computation chooses collaboration mode/scale, roles, and heterogeneous models in a cascade.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: query representation and available collaboration/model pool. Output: a configured multi-agent graph. Timing: before the main reasoning rollout.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] Different queries may require different coordination structure and model capacity rather than a fixed MAS.

## Predicted observable signature
[CODEX_HYPOTHESIS] At equal model/tool/token budget, routing should change which queries benefit and select distinct structures for distinct difficulty profiles.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Oracle-answer rewards, model-pool differences, and price variation can masquerade as routing value.

## Source lineage
[CODEX_SYNTHESIS] Single-model routing → collaboration routing → role/model allocation.

## Evidence ledger
[AUTHOR_FACT] The source establishes the overall MAS-routing scope and its cascaded selection of collaboration mode, dynamic agent count, roles, and per-agent LLMs. [[evidence:ev-p023-operator-core]] [[evidence:ev-p023-cascaded-routing-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] MasRouter; collaboration routing; role allocation; heterogeneous MAS; query-conditioned agent architecture
