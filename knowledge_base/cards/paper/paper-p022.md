<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p022","card_kind":"paper","paper_id":"P022","evidence_ids":["ev-p022-operator-core"],"source_refs":[{"path":"papers/P022_moc.pdf","sha256":"ba1d15b954937e17f660891e1f3b52bde6d19aa7d4f4759ca3ca98703975ea83"}]} -->
# MOC: Multi-Order Communication in LLM-based Multi-Agent Systems

## Role in the knowledge base
[CODEX_SYNTHESIS] Multi-agent information-flow operator source.

## Problem and setting
[CODEX_SYNTHESIS] Directed multi-agent graphs where a target agent may need messages from multi-hop ancestors under a message budget.

## Changed computation
[CODEX_SYNTHESIS] MOC exposes higher-order messages and consolidates them with topology-aware semantic distillation.

## Evidence-backed findings
[AUTHOR_FACT] The source defines topology-semantic consolidation rather than merely adding more debate rounds. [[evidence:ev-p022-operator-core]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Distillation adds hidden cost and can erase minority evidence; larger communication order is not monotonically better.

## Lineage and baselines
[CODEX_SYNTHESIS] Extends static topology studies by changing each agent's receptive field.

## Evidence ledger
[AUTHOR_FACT] The cited Evidence is anchored to the admitted PDF and a current Passage SHA. [[evidence:ev-p022-operator-core]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] MOC; multi-order communication; higher-order messages; topology-semantic consolidation; receptive field

