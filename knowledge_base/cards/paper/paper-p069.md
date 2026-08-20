<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p069","card_kind":"paper","paper_id":"P069","evidence_ids":["ev-p069-description-induced-preference","ev-p069-identical-tool-order-bias"],"source_refs":[{"path":"papers/P069_tool_preferences.pdf","sha256":"bf2fb1bba7d9d028348bc9d8991d3ed01f78437c834fa4106d3abae048cbbac5"}]} -->
# Tool Preferences in Agentic LLMs are Unreliable

## Role in the knowledge base
[CODEX_SYNTHESIS] 工具描述与顺序造成 selection bias 的负向核心来源。

## Problem and setting
[AUTHOR_FACT] 仅编辑 tool description 可造成超过十倍的使用差异。[[evidence:ev-p069-description-induced-preference]]

## Changed computation
[CODEX_SYNTHESIS] 论文使用 functionally identical controls 分离真实工具能力与 presentation-induced selection。

## Evidence-backed findings
[AUTHOR_FACT] 即使工具功能相同，选择仍对排列顺序敏感。[[evidence:ev-p069-identical-tool-order-bias]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 该结果证明 choice instability，不自动证明某种 mitigation 已有效；正式 Candidate 需 counterbalance description/order。

## Lineage and baselines
[CODEX_SYNTHESIS] function-calling accuracy → identical-tool choice control → presentation-bias diagnosis。

## Evidence ledger
[CODEX_SYNTHESIS] 描述偏置与顺序偏置分别有直接 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] tool description bias; identical tools; order sensitivity; tool preference instability; function selection confound
