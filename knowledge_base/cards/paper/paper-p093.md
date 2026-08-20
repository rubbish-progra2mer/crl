<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p093","card_kind":"paper","paper_id":"P093","evidence_ids":["ev-p093-foil-collapse","ev-p093-poison-rag","ev-p093-paired-protocol"],"source_refs":[{"path":"papers/P093_dense_retriever_collapse.pdf","sha256":"e62a61bf3e0bfbfcbd08f9fe09cdb29079f9e87035c32b3ee7eee89df1630fb1"}]} -->
# Collapse of Dense Retrievers: Short, Early, and Literal Biases

## Role in the knowledge base
[CODEX_SYNTHESIS] literal/brevity/position 偏差的受控测量协议（正式发表，ACL 2025），是检索残差分解的重要方法学先行工作。

## Problem and setting
[CODEX_SYNTHESIS] 稠密检索器的打分是否由事实证据（答案在场）驱动，还是被表面信号（长度/字面重合/位置/重复）压过。

## Changed computation
[AUTHOR_FACT] 评测计算：Re-DocRED 改造 + 单因素文档对 + 配对 t 检验（250 查询/设定），4 偏差（brevity/position/literal/repetition）+ 答案在场因素构成五个单因素设定，与 foil/poison 组合。[[evidence:ev-p093-paired-protocol]]

## Evidence-backed findings
[AUTHOR_FACT] 偏差叠加使 8 模型选含答案文档 <10%；poisoned 文档被偏好并使 RAG 劣于无文档。[[evidence:ev-p093-foil-collapse]] [[evidence:ev-p093-poison-rag]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 成对比较非真实 top-k（攻击叙事为拼接推断）；poison 数字含 GPT-4o judge 自环；无 BM25 对照；未测 2025–2026 强嵌入器（bge/gte/e5/nv-embed）；Table 3 与附录同设定数值有 ≤0.05 漂移（方向不受影响）。

## Lineage and baselines
[CODEX_SYNTHESIS] 检索器行为分析/探针线 → 受控偏差分解；可支持偏差存在性与测量协议，不支持外推端到端攻击成功率。

## Evidence ledger
[CODEX_SYNTHESIS] 三条 evidence 分别锚定崩塌量化、poison 后果、协议构造。

## Retrieval vocabulary
[CODEX_SYNTHESIS] dense retrieval collapse; retriever bias; answer importance; DecompX; ColDeR; foil; poison; controlled bias decomposition; ACL 2025; measuring retrieval biases; answer presence versus surface signals; biased foil documents; weaknesses of dense retrieval
