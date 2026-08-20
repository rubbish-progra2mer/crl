<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-archive-conditioned-agent-code-search","card_kind":"operator","paper_id":"P057","evidence_ids":["ev-p057-archive-code-search","ev-p057-search-evaluation-budget"],"source_refs":[{"path":"papers/P057_adas.pdf","sha256":"32eb1c1a6888e35fae0f618e33c58698b54d9c49bc063fef91ee591719fca376"}]} -->
# Archive-Conditioned Agent-Code Search

## Intervention target
[CODEX_SYNTHESIS] Agent system 的可执行控制代码，不只修改单条 prompt。

## Before and after computation
[CODEX_SYNTHESIS] human-authored agent → meta-agent generates new code conditioned on prior discovery archive。[[evidence:ev-p057-archive-code-search]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为任务说明、archive 与反馈；输出为新 Agent program；在实验前 discovery 阶段发生并增加多次评估预算。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] archive 可保留已探索结构并促使下一轮在代码层做不同计算。

## Predicted observable signature
[CODEX_HYPOTHESIS] 新系统应包含可定位的 changed computation，且在未参与搜索的最终 holdout 保持效果。

## Preconditions and transfer risks
[AUTHOR_FACT] ARC 搜索重复使用 held-out test feedback。[[evidence:ev-p057-search-evaluation-budget]]

## Source lineage
[CODEX_SYNTHESIS] P056 graph search → P057 program search → P058 MCTS workflow refinement。

## Evidence ledger
[CODEX_SYNTHESIS] code-generation intervention 与 selection-budget risk 分别有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] automated agent design; meta-agent programming; archive-conditioned search; executable agent code
