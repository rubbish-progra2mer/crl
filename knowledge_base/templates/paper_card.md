<!-- Replace this line with one valid CRL_CARD_META JSON object; see ../CARD_SCHEMA.md. -->
# Paper Card

## Role in the knowledge base

说明该论文是直接祖先、强基线、机制来源、负向证据还是评测依据，以及为何进入核心库。

## Problem and setting

区分文本/工具型 Agent 研究问题、实验载体、模型、工具、数据与预算。

## Changed computation

写清方法实际改变了哪一步计算；只有 prompt 文字变化时必须如实写明。

## Evidence-backed findings

每条内容以 `[AUTHOR_FACT]` 或 `[AUTHOR_INTERPRETATION]` 开头，并在同一段落或列表项内使用 `[[evidence:<id>]]` 引用 metadata 中存在的 Evidence。

## Limitations and failure signals

分别记录作者明示限制、实验负向信号和 Codex 解释，不将缺失实验自动写成失败事实。

## Lineage and baselines

记录直接祖先、最近同类工作、强基线与 closest-composition baseline。

## Evidence ledger

逐项列出 evidence_id、其支持的窄主张、需要回看的原始页码或图表。

## Retrieval vocabulary

列出能从真实问题找到本 Card 的英文技术词、常见同义表达和必要的中文别名；每项必须与正文证据一致，不得为命中评测而堆无关关键词。
