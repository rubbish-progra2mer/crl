<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p082","card_kind":"paper","paper_id":"P082","evidence_ids":["ev-p082-future-token-loss-filtered-calls","ev-p082-top-k-single-call-boundary","ev-p082-chaining-cost-sparsity-boundary"],"source_refs":[{"path":"papers/P082_toolformer.pdf","sha256":"6d7483d94653008e40c2058a1c22441c92e3713dae278b6361e8efc447c99522"}]} -->
# Toolformer: Language Models Can Teach Themselves to Use Tools

## Role in the knowledge base
[CODEX_SYNTHESIS] 用 future-token likelihood 自监督筛选工具调用的基础谱系；适合作为“无需任务标签”的工具学习基线，也暴露 proxy mismatch。

## Problem and setting
[CODEX_SYNTHESIS] 在缺少大规模人工 tool-use 标注时，模型需要自行生成并筛选调用监督。

## Changed computation
[AUTHOR_FACT] 模型从少量 API 示例生成候选调用，执行后仅保留帮助预测后续 token 的调用，再在增强语料上微调。[[evidence:ev-p082-future-token-loss-filtered-calls]]

## Evidence-backed findings
[CODEX_SYNTHESIS] 论文展示同一 LM 可以学习何时及如何调用多种文本接口工具，但其筛选目标仍是语言建模 likelihood。

## Limitations and failure signals
[AUTHOR_FACT] 解码把 API token 放宽到 top-10 触发，但每个输入最多一次调用。[[evidence:ev-p082-top-k-single-call-boundary]]
[AUTHOR_FACT] 当前方法不能链式或交互式用工具，某些工具数据极稀疏，并且调用决策不计 tool-dependent cost。[[evidence:ev-p082-chaining-cost-sparsity-boundary]]

## Lineage and baselines
[CODEX_SYNTHESIS] 是 self-supervised tool learning 祖先；未来 Agent comparison 必须增加 task utility、chaining 与 cost-aware baselines。

## Evidence ledger
[CODEX_SYNTHESIS] training filter、inference trigger 与交互/成本限制均由原文 Evidence 支撑。

## Retrieval vocabulary
[CODEX_SYNTHESIS] self-supervised tool learning; future token loss API filter; single-call tool use; tool chaining limitation; call cost utility mismatch
