<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p091","card_kind":"paper","paper_id":"P091","evidence_ids":["ev-p091-cosine-auroc","ev-p091-supersession-rule","ev-p091-retain-fabrication"],"source_refs":[{"path":"papers/P091_memstrata.pdf","sha256":"10349a31de86116b7e4cc5a8cb5e60766a55ab7dbab7894906841a6e3234171f"}]} -->
# MemStrata: Temporal Validity in Retrieval Memory

## Role in the knowledge base
[CODEX_SYNTHESIS] 双重知识角色：(a) cosine 无法分辨矛盾/重复的校准测量（AUROC 0.59）；(b) 写侧结构化 supersession 节点的直接先行工作。

## Problem and setting
[AUTHOR_FACT] 在 98 对标注样本（32 duplicate、22 merge、22 contradict、22 novel）上，cosine 区分 duplicate 与其余类别的 AUROC 为 0.5926。[[evidence:ev-p091-cosine-auroc]]

## Changed computation
[AUTHOR_FACT] 确定性 (S,R,O) supersession + bi-temporal ledger：新断言冲突时 retire 旧值，无阈值无 LLM 调用；静态侧保留 RAG 全召回。[[evidence:ev-p091-supersession-rule]]

## Evidence-backed findings
[AUTHOR_FACT] 消融：去 supersession → evolving accuracy 0.99→0.33（与 naive RAG 不可区分）、conditional fabrication ×6（峰值 0.56）——retain-everything 不仅更不准而且更不安全。[[evidence:ev-p091-retain-fabrication]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 单作者 preprint（draft 标记）；98 对标注样本小；四演化基准为合成流、键对齐难度低；单嵌入器单 7B 骨干；基准含文本 staleness marker 的污染风险由其自建 marker-free 口径规避——与 P094 的序号护栏口径不可直接比较。

## Lineage and baselines
[CODEX_SYNTHESIS] P030(STALE) 谱系的 2026 段最新步；与 P095（装配层 max）分占写侧/读后两个位置。任何 supersession 类候选方法都应以本文为最近先行工作。

## Evidence ledger
[CODEX_SYNTHESIS] AUROC 校准、supersession 定义、retain 消融三条绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] MemStrata; temporal validity; stale-fact error; bi-temporal ledger; supersession; evolving knowledge; marker-free benchmark; retrieval memory; retrieval memory temporal validity; stale fact retirement; evolving knowledge updates; deterministic supersession rule
