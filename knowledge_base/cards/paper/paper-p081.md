<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p081","card_kind":"paper","paper_id":"P081","evidence_ids":["ev-p081-independent-path-majority-aggregation","ev-p081-forty-sample-baseline","ev-p081-fixed-answer-space-boundary"],"source_refs":[{"path":"papers/P081_self_consistency.pdf","sha256":"1a49ce0373afc89d2d6e97fb1aa8230f6b818c70590d732a3187f753f4df6aba"}]} -->
# Self-Consistency Improves Chain of Thought Reasoning in Language Models

## Role in the knowledge base
[CODEX_SYNTHESIS] test-time independent sampling 的强基线卡；用于审查 Agent 交互、reflection、debate 或 search 的收益是否只是更多独立候选。

## Problem and setting
[CODEX_SYNTHESIS] 单一路径 greedy reasoning 对一次不可靠解码高度敏感。

## Changed computation
[AUTHOR_FACT] 方法独立采样多条 reasoning paths，边缘化路径并选择最终答案集合中最一致的答案。[[evidence:ev-p081-independent-path-majority-aggregation]]

## Evidence-backed findings
[CODEX_SYNTHESIS] 论文报告独立路径聚合相对 greedy CoT 的显著增益，并将其作为无需额外训练的 test-time 算子。

## Limitations and failure signals
[AUTHOR_FACT] 主结果每次运行采样 40 个输出，而主要 CoT baseline 是 greedy decoding。[[evidence:ev-p081-forty-sample-baseline]]
[AUTHOR_FACT] 原方法直接适用于 fixed answer set；开放文本需要额外定义一致性度量。[[evidence:ev-p081-fixed-answer-space-boundary]]

## Lineage and baselines
[CODEX_SYNTHESIS] 它是所有增加 reasoning candidates 的 Agent 方法的强基础比较，但 equal samples 仍需进一步匹配 tokens、latency 与 tool calls。

## Evidence ledger
[CODEX_SYNTHESIS] computation、40-sample compute boundary 与 answer-space boundary 均绑定 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] self consistency baseline; independent reasoning paths; majority answer aggregation; equal candidate budget; test-time sampling; fixed answer parser
