<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-higher-order-message-exposure","card_kind":"operator","paper_id":"P022","evidence_ids":["ev-p022-operator-core"],"source_refs":[{"path":"papers/P022_moc.pdf","sha256":"ba1d15b954937e17f660891e1f3b52bde6d19aa7d4f4759ca3ca98703975ea83"}]} -->
# Source-Aware Higher-Order Message Exposure

## Intervention target
[CODEX_SYNTHESIS] The information visible to a downstream agent in a communication graph.

## Before and after computation
[CODEX_SYNTHESIS] A target reads only immediate predecessors. The changed computation exposes multi-hop ancestor messages in topological order and consolidates them when a message budget is exceeded.

## Inputs outputs information and timing
[CODEX_SYNTHESIS] Input: ordered ancestor messages plus graph distances. Output: a bounded consolidated context for the target agent. Timing: before the target response.

## Mechanism hypothesis
[CODEX_HYPOTHESIS] Expanding the receptive field can recover useful distant evidence that local communication omits.

## Predicted observable signature
[CODEX_HYPOTHESIS] Benefits should appear when decisive evidence originates multiple hops away; consolidation cost and minority-evidence loss should be measured separately.

## Preconditions and transfer risks
[CODEX_SYNTHESIS] Distillation adds hidden calls and latency, and higher order can saturate or erase source distinctions.

## Source lineage
[CODEX_SYNTHESIS] Static topology propagation → higher-order receptive fields → potentially dynamic message selection.

## Evidence ledger
[AUTHOR_FACT] Source passages establish the intervention identity and stated scope. [[evidence:ev-p022-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] MOC; higher-order communication; ancestor messages; topological-semantic consolidation; agent receptive field

