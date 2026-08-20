<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-memory-stage-decomposition","card_kind":"operator","paper_id":"P010","evidence_ids":["ev-p010-index-retrieve-read"],"source_refs":[{"path":"papers/P010_longmemeval.pdf","sha256":"c6c6d75072d316d7b040dbbbb9caf7607821e6dd34d986e6f6c7e3e1721179f7"}]} -->
# Memory Index–Retrieve–Read Decomposition

## Intervention target
[AUTHOR_FACT] 将长期 Agent memory 拆为 indexing、retrieval 与 reading 三个执行阶段。[[evidence:ev-p010-index-retrieve-read]]

## Before and after computation
[CODEX_SYNTHESIS] Before 是只用最终 QA 结果作端到端判断；after 是分别观察 indexing 设计、retrieval 命中与给定 evidence context 后的 reading 表现。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入依次为交互历史、query 和 retrieved context，输出依次为 memory units、候选证据与最终回答。

## Mechanism hypothesis
[CODEX_SYNTHESIS] 分阶段诊断能避免把 reading overload 误判为 retrieval miss，也使局部干预可证伪。

## Predicted observable signature
[CODEX_HYPOTHESIS] 若瓶颈在某阶段，oracle 替换该阶段应显著恢复性能，而替换其他阶段不应同幅改善。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 需要阶段接口可观察；端到端黑盒 memory 或非文本状态可能无法清晰分解。

## Source lineage
[CODEX_SYNTHESIS] LongMemEval 是近期 evaluation/operator 来源；它不等同于某一特定 memory architecture。

## Evidence ledger
[AUTHOR_FACT] `ev-p010-index-retrieve-read` 定位到 PDF p.1 的三阶段定义。[[evidence:ev-p010-index-retrieve-read]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] memory indexing retrieval reading；long-term memory pipeline；retrieval miss vs reading overload；长期记忆分阶段。
