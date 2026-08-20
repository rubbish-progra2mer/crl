<!-- Replace this line with one valid CRL_CARD_META JSON object; see ../CARD_SCHEMA.md. -->
# Operator Card

## Intervention target

说明要改变 Agent 决策过程中的哪个计算节点以及未改变的边界。

## Before and after computation

用精确的 Baseline -> Changed Computation 对照描述，不用“增强”“优化”代替机制。

## Inputs outputs information and timing

分别列出输入、输出、可访问的信息、干预发生时点和是否增加 token/tool/model 预算。

## Mechanism hypothesis

用 `[CODEX_SYNTHESIS]` 或 `[CODEX_HYPOTHESIS]` 描述为什么该变化可能有效；若转述作者解释则使用带 Evidence 的 `[AUTHOR_INTERPRETATION]`。

## Predicted observable signature

写出若机制成立应观察到、若仅是更多预算不应观察到的信号。

## Preconditions and transfer risks

记录所需假设、信息泄漏风险、任务载体依赖和可能不适用条件。

## Source lineage

列出来源论文、直接祖先、相近组合以及该 Operator 是原样借用还是抽象迁移；人工写明 canonical changed computation、aliases、与相近 Card 的 same-mechanism/refinement/contradiction 关系，以及共享作者、数据或模型造成的 Evidence family 依赖。近重复论文数不得冒充独立机制证据数。

## Evidence ledger

逐项列出支撑 changed computation、结果、边界与风险的 evidence_id。

## Retrieval vocabulary

列出该 computation、intervention point、机制签名和失败边界的常见同义表达；不得写与 Evidence 无关的热门词。
