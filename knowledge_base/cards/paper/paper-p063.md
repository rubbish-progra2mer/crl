<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p063","card_kind":"paper","paper_id":"P063","evidence_ids":["ev-p063-dynamic-link-generation","ev-p063-retrieval-k-varies","ev-p063-neighbor-rewrite-action"],"source_refs":[{"path":"papers/P063_a_mem.pdf","sha256":"fec32b521c4a1f793442bf1aeb26139c583078350d1cd4ab8f4eccc54a0694f0"}]} -->
# A-Mem: Agentic Memory for LLM Agents

## Role in the knowledge base
[CODEX_SYNTHESIS] 动态 note linking 与 neighbor evolution 的机制来源，同时是 memory rewrite provenance 的重点负向锚点。

## Problem and setting
[AUTHOR_FACT] 系统检索近邻 note，再让 LLM 在无预定义规则下生成 links。[[evidence:ev-p063-dynamic-link-generation]]

## Changed computation
[CODEX_SYNTHESIS] 新记忆写入同时触发 link generation，并允许更新已有邻居的 context/tags。

## Evidence-backed findings
[AUTHOR_FACT] evolution prompt 明确允许强化链接或重写邻居内容与标签。[[evidence:ev-p063-neighbor-rewrite-action]]

## Limitations and failure signals
[AUTHOR_FACT] 正文称 retrieval k 主要为 10，但允许按类别调整。[[evidence:ev-p063-retrieval-k-varies]]

## Lineage and baselines
[CODEX_SYNTHESIS] static vector memory → linked note memory → write-time neighbor evolution；需与仅 reranking 的增量改动区分。

## Evidence ledger
[CODEX_SYNTHESIS] 动态链接、k 边界、重写权限各有直接 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] agentic memory graph; dynamic note linking; memory evolution; neighbor rewrite; provenance loss
