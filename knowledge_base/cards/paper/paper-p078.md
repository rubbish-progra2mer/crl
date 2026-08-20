<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p078","card_kind":"paper","paper_id":"P078","evidence_ids":["ev-p078-validated-tool-creation-retrieval","ev-p078-multiview-tool-retrieval","ev-p078-generic-tool-and-baseline-boundary","ev-p078-toolset-construction-cost","ev-p078-baseline-fairness-boundary"],"source_refs":[{"path":"papers/P078_craft.pdf","sha256":"59263fffdc51e21530d9dba1aeeeacefb2b5c4048012a7e385b4f555a362f155"}]} -->
# CRAFT: Customizing LLMs by Creating and Retrieving from Specialized Toolsets

## Role in the knowledge base
[CODEX_SYNTHESIS] 从任务数据生成、抽象、验证并检索专用代码工具的代表性方法；收录其文本/代码机制，不把 VQA 应用扩张为多模态研究方向。

## Problem and setting
[CODEX_SYNTHESIS] 通用或未筛选工具集可能给文本/代码求解增加无关工具与选择错误。

## Changed computation
[AUTHOR_FACT] 抽象工具必须能用适当参数重新解决原始问题，否则被丢弃。[[evidence:ev-p078-validated-tool-creation-retrieval]] [AUTHOR_FACT] 推理时用问题、函数名和 docstring 三视图召回并多数聚合。[[evidence:ev-p078-multiview-tool-retrieval]]

## Evidence-backed findings
[AUTHOR_FACT] 直接使用外部 Python 工具、LATM、CREATOR 与检索基线在多个数据集上并不稳定增益，部分设置还退化。[[evidence:ev-p078-generic-tool-and-baseline-boundary]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 原问题回放只验证同源适用性，不证明跨分布工具泛化；未来 Candidate 必须把 toolset 质量、retrieval 与 backbone tool-use ability 分开对照。
[AUTHOR_FACT] 论文估算离线工具库构建约 USD 2,500。[[evidence:ev-p078-toolset-construction-cost]] [AUTHOR_FACT] TabMWP 上 BM25 略高于 CRAFT，且 CREATOR comparison 移除了原 checking/rectifying loop。[[evidence:ev-p078-baseline-fairness-boundary]]

## Lineage and baselines
[CODEX_SYNTHESIS] 连接 tool creation、program abstraction 与 retrieval-augmented tool use；generic library、LATM、CREATOR 和 retrieval baselines 是必须保留的对照。

## Evidence ledger
[CODEX_SYNTHESIS] creation validation、三视图 retrieval、负向 baseline、离线成本与 comparator 修改均由原文 Evidence 约束。

## Retrieval vocabulary
[CODEX_SYNTHESIS] specialized tool library; tool abstraction verification; multi-view tool retrieval; function name docstring matching; generic tool distractor
