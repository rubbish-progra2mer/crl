<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-unfiltered-reflection-contamination","card_kind":"failure","paper_id":"P018","evidence_ids":["ev-p018-raw-reflection-contamination"],"source_refs":[{"path":"papers/P018_expel.pdf","sha256":"01e533d81fb4a5f91797c073a9b1929acbaa64da45a592b26563ca7d135024f3"}]} -->
# Adding Retry Reflections Can Hurt ExpeL Insight Generation

## Observed failure
[AUTHOR_FACT] ExpeL 消融中，把 reflections 加入 insight generation 会降低表现。[[evidence:ev-p018-raw-reflection-contamination]]

## Conditions and scope
[CODEX_SYNTHESIS] 结论绑定本文的 HotpotQA/insight pipeline，不表示所有 reflection memory 都有害。

## Failed intervention
[CODEX_SYNTHESIS] 在该 HotpotQA 消融中，retry reflections 被直接加入 insight construction；原文仅推测其中的 hallucination 可能误导该阶段，未唯一识别伤害机制。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 伤害可能来自噪声、重复、相互矛盾或 prompt 变长；消融证明加入方式有害，不唯一识别原因。

## Warning for future candidates
[CODEX_SYNTHESIS] 长期 memory 写入必须区分局部反思、可重复 failure pattern 与经多轨迹支持的规则。

## Possible repair boundary
[CODEX_HYPOTHESIS] 成败对比、跨任务投票或 provenance-aware filtering 可能降低污染，需独立消融。

## Evidence ledger
[AUTHOR_FACT] `ev-p018-raw-reflection-contamination` 定位到 PDF p.10 的直接消融结论。[[evidence:ev-p018-raw-reflection-contamination]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] reflection memory pollution；noisy insight；long-term memory contamination；raw reflection；反思污染长期记忆。
