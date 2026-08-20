<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p058","card_kind":"paper","paper_id":"P058","evidence_ids":["ev-p058-mcts-workflow-search","ev-p058-validation-selection-loop"],"source_refs":[{"path":"papers/P058_aflow.pdf","sha256":"9be15f695f11dd5bc634c1c026bd2270eff3d3c4a53c4d9b51c012b7bd03d521"}]} -->
# AFlow: Automating Agentic Workflow Generation

## Role in the knowledge base
[CODEX_SYNTHESIS] 完整可执行 workflow 的 MCTS 搜索来源；用于区分机制发现与大额反复选择预算。

## Problem and setting
[AUTHOR_FACT] 方法用 MCTS 变体搜索 complete executable workflows，并以实际执行反馈更新搜索。[[evidence:ev-p058-mcts-workflow-search]]

## Changed computation
[CODEX_SYNTHESIS] 把 Agent workflow 作为可执行程序节点，迭代生成、运行、选择与回传。

## Evidence-backed findings
[AUTHOR_FACT] workflow selection 与 backpropagation 都反复使用 validation subset。[[evidence:ev-p058-validation-selection-loop]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 搜索轮数、候选评估次数与最终选择必须计入 discovery budget。

## Lineage and baselines
[CODEX_SYNTHESIS] ADAS code generation → AFlow MCTS executable-workflow refinement。

## Evidence ledger
[CODEX_SYNTHESIS] 搜索计算与反复 validation 选择分别由两条 Evidence 支撑。

## Retrieval vocabulary
[CODEX_SYNTHESIS] MCTS workflow search; executable agent workflow; validation reuse; workflow discovery budget
