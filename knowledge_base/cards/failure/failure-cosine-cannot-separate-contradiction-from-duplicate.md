<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-cosine-cannot-separate-contradiction-from-duplicate","card_kind":"failure","paper_id":"P091","evidence_ids":["ev-p091-cosine-auroc","ev-p091-retain-fabrication"],"source_refs":[{"path":"papers/P091_memstrata.pdf","sha256":"10349a31de86116b7e4cc5a8cb5e60766a55ab7dbab7894906841a6e3234171f"}]} -->
# Cosine Similarity Cannot Separate Contradiction from Duplicate; Co-Present Stale Facts Induce Fabrication

## Observed failure
[AUTHOR_FACT] 98 个标注对上（32 duplicate/22 merge/22 contradict/22 novel），cosine 区分 duplicate 与其余类的 AUROC 仅 0.5926——作者据此表述为 contradiction 与 duplicate 近随机不可分（0.59）。[[evidence:ev-p091-cosine-auroc]]
[AUTHOR_FACT] 去掉 supersession（retain-everything）后，evolving accuracy 0.99→0.33，conditional fabrication 均值 0.04→0.25（约 6 倍，峰值 0.56）——模型同时看到 stale 与 current 值且无法分辨时会编造答案。[[evidence:ev-p091-retain-fabrication]]

## Conditions and scope
[CODEX_SYNTHESIS] 演化知识上的检索记忆（marker-free 更新流）；7B 本地模型 + 消费级硬件；四个演化基准（code mutation / config migration / dependency bump / API evolution）。单作者 preprint，样本量 98 对偏小。

## Failed intervention
[CODEX_SYNTHESIS] 用嵌入相似度阈值判定"新记忆是否取代旧记忆"，或不做任何取代、把冲突留给读取时的 LLM 判断。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] AUROC 0.59 是单一嵌入器上的测量，未覆盖强嵌入器；但“矛盾对在字面上可能比 paraphrase 更相似于原文”的结构性原因与 P093 的 literal-bias 测量同向。fabrication 放大是同一读路径内的消融，归因较干净。

## Warning for future candidates
[CODEX_SYNTHESIS] 任何以相似度信号做记忆去重或更新裁决的候选方法都必须面对该测量；引用 AUROC 点值时必须注明单嵌入器条件。

## Possible repair boundary
[CODEX_HYPOTHESIS] 结构化 (S,R,O) supersession 已有本文覆盖；无显式结构时的时序裁决仍是不同问题。

## Evidence ledger
[CODEX_SYNTHESIS] AUROC 测量与 retain-ablation fabrication 放大分别绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] cosine AUROC 0.59; contradiction vs duplicate; stale fact; retain-everything; fabrication amplification; temporal validity; supersession ablation; MemStrata; embedding similarity fails contradiction detection; duplicate versus contradiction; co-present stale and current values; fabricated answers from conflicting memory; retaining everything is unsafe
