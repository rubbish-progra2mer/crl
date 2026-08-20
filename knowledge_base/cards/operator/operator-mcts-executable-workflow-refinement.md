<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-mcts-executable-workflow-refinement","card_kind":"operator","paper_id":"P058","evidence_ids":["ev-p058-mcts-workflow-search","ev-p058-validation-selection-loop"],"source_refs":[{"path":"papers/P058_aflow.pdf","sha256":"9be15f695f11dd5bc634c1c026bd2270eff3d3c4a53c4d9b51c012b7bd03d521"}]} -->
# MCTS Refinement of Executable Agent Workflows

## Intervention target
[CODEX_SYNTHESIS] 完整 Agent workflow 程序及其 operator composition。

## Before and after computation
[CODEX_SYNTHESIS] single hand-written workflow → MCTS variant repeatedly proposes and executes workflow programs。[[evidence:ev-p058-mcts-workflow-search]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为当前 workflow、validation execution feedback 与搜索树；输出为下一 candidate workflow；部署前消耗多轮执行预算。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 结构化局部修改和 feedback backpropagation 比一次生成更易发现有效 composition。

## Predicted observable signature
[CODEX_HYPOTHESIS] 在独立 holdout 上仍优于相同 discovery budget 的随机/非树搜索，而非只在 validation 最优。

## Preconditions and transfer risks
[AUTHOR_FACT] selection 与 backpropagation 反复依赖 validation subset。[[evidence:ev-p058-validation-selection-loop]]

## Source lineage
[CODEX_SYNTHESIS] P057 program archive search 的 refinement；二者属于同一 automated workflow discovery family。

## Evidence ledger
[CODEX_SYNTHESIS] workflow MCTS 与 validation loop 均有直接 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] AFlow; MCTS workflow generation; executable workflow refinement; discovery budget
