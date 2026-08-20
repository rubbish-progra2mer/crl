# P093 first read (W06) — P093 Collapse of Dense Retrievers：受控偏置分解与多偏置叠加崩塌

Status: `DRAFT_BEFORE_INDEPENDENT_READ`
Reader: main Codex
Read date: 2026-07-27 (Asia/Shanghai)

## Canonical source and bytes

- Title: Collapse of Dense Retrievers: Short, Early, and Literal Biases Outranking Factual Evidence
- Authors: Mohsen Fayyaz; Ali Modarressi; Hinrich Schütze; Nanyun Peng（UCLA + LMU）
- Identity: arXiv 2503.05037v2 (2025-06-02)；**ACL 2025 主会**（abs 页 venue 注记）；数据集/榜单 `huggingface.co/datasets/mohsenfayyaz/ColDeR`
- PDF: `knowledge_base/staging/w06_targeted/P093_dense_retriever_collapse.pdf`
- PDF SHA-256: `e62a61bf3e0bfbfcbd08f9fe09cdb29079f9e87035c32b3ee7eee89df1630fb1`
- Parse check: 17 physical pages

## Canonical contribution

把关系抽取数据集 Re-DocRED 改造成**受控文档对构造框架**：每查询绑定唯一含 head+tail 的证据句 Sev，用 S+h−t / S−h−t 句子库精确装配 D1/D2 文档对，使单一偏置成为唯一变量；用 250 对上的配对 t 检验量化五种偏置——answer importance（有无答案）、position（证据句位置）、literal（实体名面变体）、brevity（短文档偏好）、repetition（head 重复）——并测多偏置叠加与 RAG 后果。changed computation = 评测计算从"下游 nDCG"改为"受控文档对上的逐偏置配对分数差"。

## Evidence and closest lineage

- 单偏置结果：position 一致为负 t（Fig.4，所有模型偏文首）；literal 强正 t（Table 3，短-短 vs 短-长 +14.37/+16.62，Contriever-MSMARCO/Dragon+）；brevity 强正（Fig.1）；repetition 正（Fig.5：分数随 head 重复升、随长度降）；answer importance 为正但幅度不及干扰信号（Fig.1/3；无监督 Contriever 为 **−5.92**——完全不识别答案存在）。
- **多偏置叠加崩塌**（Table 4）：foil 文档（重复+位置偏置、无答案）vs 证据文档（答案埋在无关句中）——全部 8 个模型准确率 <10%（Dragon+ 1.2%、Contriever-MSMARCO 0.8%、ColBERTv2 7.6%、ReasonIR-8B 8.0%），t 统计 −21 到 −42。
- **RAG 后果**（Table 5）：检索器 100% 偏好毒化文档（Table A.9）；gpt-4o 用毒化文档 30.8% vs 无文档 64.8% vs 证据文档 93.6%——**毒化文档比不给文档低 34 点**。
- 机制可视化：DecompX 分解 token 贡献（Fig.2）。
- 谱系：Coelho 2024（position bias 起源于对比预训练）、Ram 2023（词面依赖）、Sciavolino 2021（实体偏置）、Usuha 2024（加句反降分）；与 BEIR 型下游评测互补。

## Measurement and fairness boundaries

- 文档对为**合成受控构造**（模板查询 + 装配文档），非真实检索分布；250 对/设置；被测模型为 2021-2023 世代 encoder（Dragon/Contriever/RetroMAE/COCO-DR/ColBERTv2，附加 ReasonIR-8B），**未测 2025-2026 主流 bge/gte/e5/nv-embed 系**。
- 偏好用配对 t 统计表达（非效应量），各设置严控其余变量；作者自认 Re-DocRED 标注噪声与 GPT-4o 评测方差（Limitations 节）。

## Draft knowledge objects

### Failure draft: `Dense Retrievers Prefer Biased Distractors over Answer-Bearing Evidence`

短、早、词面匹配、重复实体四种表面信号各自压过"答案存在"信号；叠加时 <10% 选中真证据；该失败可被利用（毒化文档 100% 被优先检回并使 RAG 低于无文档基线）。适用边界：encoder 世代与合成构造。

### Operator draft: `Controlled Paired-Document Bias Decomposition (Re-DocRED repurposing)`


## Draft Evidence locators

- Physical pp.1-2: Fig.1 五偏置 t 统计总览、Table 1 文档对构造实例。
- Physical pp.3-4: Re-DocRED 改造、S 记号、DecompX。
- Physical pp.5-7: 各偏置公式与结果（Fig.3/4/5、Table 3）。
- Physical p.8: Table 4 叠加崩塌、Table 5 RAG 后果与毒化构造。
- Physical p.9: Limitations。

All claims remain draft until independent read and reconciliation.
