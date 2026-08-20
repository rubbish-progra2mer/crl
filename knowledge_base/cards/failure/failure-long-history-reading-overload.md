<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-long-history-reading-overload","card_kind":"failure","paper_id":"P010","evidence_ids":["ev-p010-long-history-decline"],"source_refs":[{"path":"papers/P010_longmemeval.pdf","sha256":"c6c6d75072d316d7b040dbbbb9caf7607821e6dd34d986e6f6c7e3e1721179f7"}]} -->
# Full-History Reading Overload

## Observed failure
[AUTHOR_FACT] 相比只给 evidence sessions 的 oracle retrieval，读取完整 LONGMEMEVALS 历史造成 30%–60% 性能下降。[[evidence:ev-p010-long-history-decline]]

## Conditions and scope
[CODEX_SYNTHESIS] 结果针对约 50 sessions 的长历史与所测 long-context LLMs，不代表任意长度必然同幅下降。

## Failed intervention
[CODEX_SYNTHESIS] 直接把全部历史塞入 context 没有解决相关证据选择与阅读干扰。

## Evidence and alternative explanations
[CODEX_HYPOTHESIS] 长上下文定位、时间推理、信息冲突和 attention dilution 可能贡献。

[CODEX_SYNTHESIS] Oracle retrieval 是提供相关 evidence sessions 的上界条件。

## Warning for future candidates
[CODEX_SYNTHESIS] “更大 context”不能替代 memory retrieval；需要分开测 indexing、retrieval 与 reading。

## Possible repair boundary
[CODEX_HYPOTHESIS] 粒度控制、query expansion 与选择性阅读可能缓解，但应与 oracle retrieval gap 分阶段核验。

## Evidence ledger
[AUTHOR_FACT] `ev-p010-long-history-decline` 定位到 PDF p.6 的 oracle 对照。[[evidence:ev-p010-long-history-decline]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] long-context degradation；full-history overload；oracle retrieval gap；memory reading failure；长历史阅读干扰。
