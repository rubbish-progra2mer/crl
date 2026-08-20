<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-memory-defense-high-fnr","card_kind":"failure","paper_id":"P008","evidence_ids":["ev-p008-memory-defense-high-fnr"],"source_refs":[{"path":"papers/P008_agent_security_bench.pdf","sha256":"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9"}]} -->
# LLM-Based Memory Defense Misses Most Poisoning Attacks

## Observed failure
[AUTHOR_FACT] ASB 的 memory-attack defense 平均 FNR 为 0.660，即该设置下 66% 攻击未被检测。[[evidence:ev-p008-memory-defense-high-fnr]]

## Conditions and scope
[CODEX_SYNTHESIS] 数字绑定 ASB 的攻击模板、模型和检测防御，不外推到所有 memory security 设计。

## Failed intervention
[CODEX_SYNTHESIS] 外部 LLM detector 对 memory plans 中依赖上下文或推理链微妙变化的恶意指令识别不足。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 高 FNR 可能来自 detector 能力、prompt 和攻击分布；低 FPR 也不抵消漏检。

## Warning for future candidates
[CODEX_SYNTHESIS] Memory 防御不能只报 clean utility 或平均准确率，必须同时报告 FNR/FPR 与攻击覆盖。

## Possible repair boundary
[CODEX_HYPOTHESIS] 来源隔离、写入策略与执行前验证可能补足纯 LLM detector，但当前 Evidence 不证明具体修复有效。

## Evidence ledger
[AUTHOR_FACT] `ev-p008-memory-defense-high-fnr` 定位到 PDF p.34 的 FNR 结果。[[evidence:ev-p008-memory-defense-high-fnr]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] memory poisoning；false negative rate；LLM defense failure；agent memory security；记忆投毒漏检。
