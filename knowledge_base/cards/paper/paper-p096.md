<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p096","card_kind":"paper","paper_id":"P096","evidence_ids":["ev-p096-simplification-inversion","ev-p096-shared-misinterpretation"],"source_refs":[{"path":"papers/P096_verisimpl.pdf","sha256":"81b34a7084aa5552ef9a1491ec5e5f9da5c149e80beb06fe81fc163ae4d595b3"}]} -->
# VeriSimpl: Simplification-Based Verification for Optimization Modeling

## Role in the knowledge base
[CODEX_SYNTHESIS] 结构化 LLM 裁决探针家族的定义实例（ICML 2026, PMLR 306），也是“共享误解通过验证”失败形态的书面来源。

## Problem and setting
[CODEX_SYNTHESIS] NL→优化建模的端到端验证对 LLM 过难；需要不依赖参考形式化的置信信号。

## Changed computation
[AUTHOR_FACT] solver 构造降维简化查询（约束三型突变/单变量+全变量掩码/类型检查）、LLM 裁决，字典序聚合为 best-of-K（K≤10）选择器 + all-pass 自验证门控。[[evidence:ev-p096-simplification-inversion]]（信号/聚合/门控细节出自 §3/Alg.1–3 与 §4.2，PDF 直核；所绑引文锚定反转机制）

## Evidence-backed findings
[CODEX_SYNTHESIS] 主结果跨三底座一致（GPT-4o 平均 65.5 / R1 72.8）；自验证 precision 91.5%（GPT-4o）/覆盖 23-34%；oracle 无泄漏（验证 oracle 由 solver 对候选自身模型算出）。

## Limitations and failure signals
[AUTHOR_FACT] 共享误解假阳性 + 两条能力边界自认（变量定义视为给定；遗漏方面无查询）。[[evidence:ev-p096-shared-misinterpretation]]
[CODEX_SYNTHESIS] 发表版自带缺陷连带引用：best-of-K 混杂无算力配平；CompOR n=17；有效分母与声明不符（疑未声明剔除）；A.2/A.3 案例 transcript 错配；R1 两套不一致数字；accuracy 判定标准未定义；R1 验证 precision 反低于 GPT-4o（78.5 vs 91.5，未解释）。

## Lineage and baselines
[CODEX_SYNTHESIS] 与 P097（solver 扰动、机器裁决）、P098（探针作训练信号）构成认证侧三条互补路线。

## Evidence ledger
[CODEX_SYNTHESIS] 机制与失败自认绑定 exact Passage；其余缺陷记录于 reconciliation。

## Retrieval vocabulary
[CODEX_SYNTHESIS] VeriSimpl; simplification-based verification; optimization modeling; NL4LP; shared misunderstanding; self-verification; ICML 2026; best-of-K selector; verifying optimization formulations; simplification-based diagnostic queries; natural language to optimization model
