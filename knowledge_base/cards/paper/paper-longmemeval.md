<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-longmemeval","card_kind":"paper","paper_id":"P010","evidence_ids":["ev-p010-index-retrieve-read","ev-p010-long-history-decline"],"source_refs":[{"path":"papers/P010_longmemeval.pdf","sha256":"c6c6d75072d316d7b040dbbbb9caf7607821e6dd34d986e6f6c7e3e1721179f7"}]} -->
# LongMemEval

## Role in the knowledge base
[CODEX_SYNTHESIS] 长期 memory evaluation、分阶段诊断与负向 reading evidence 的近期来源。

## Problem and setting
[CODEX_SYNTHESIS] 跨持续会话的 interactive memory QA，比较 long-context、commercial systems 与 memory pipeline choices。

## Changed computation
[AUTHOR_FACT] 将 memory design 分成 indexing、retrieval、reading。[[evidence:ev-p010-index-retrieve-read]]

## Evidence-backed findings
[AUTHOR_FACT] 完整历史阅读相对 oracle evidence sessions 下降 30%–60%。[[evidence:ev-p010-long-history-decline]]

## Limitations and failure signals
[CODEX_SYNTHESIS] Oracle retrieval 是上界；benchmark 的会话生成与 QA 载体不等同于所有长期 Agent 状态。

## Lineage and baselines
[CODEX_SYNTHESIS] Full-history long-context 与 oracle retrieval 是关键对照；具体 memory optimizations 是同一 evaluation 框架内的局部改动。

## Evidence ledger
[AUTHOR_FACT] p.1 支持三阶段；p.6 支持长历史负向差距。[[evidence:ev-p010-index-retrieve-read]] [[evidence:ev-p010-long-history-decline]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] LongMemEval；long-term memory；index retrieve read；oracle retrieval gap；长期交互记忆。

