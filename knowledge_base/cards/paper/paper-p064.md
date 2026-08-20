<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p064","card_kind":"paper","paper_id":"P064","evidence_ids":["ev-p064-experience-following-error","ev-p064-evaluator-reliability"],"source_refs":[{"path":"papers/P064_experience_following_memory.pdf","sha256":"2c3992d238f5d6dec4ed96faae0a82e3b88edc6e37b26d8622a2b780f2160400"}]} -->
# How Memory Management Impacts LLM Agents

## Role in the knowledge base
[CODEX_SYNTHESIS] 仅作为 memory error-propagation 与 evaluator reliability 的负向来源，不把 experience-following 抽成 Operator。

## Problem and setting
[AUTHOR_FACT] 当前 query 与 retrieved record 的高 input similarity 可诱导 output imitation，并复现、放大错误 stored experience。[[evidence:ev-p064-experience-following-error]]

## Changed computation
[CODEX_SYNTHESIS] 论文分析 memory selection/evaluation 如何改变后续行为；本库不采纳环境反馈学习/执行恢复方向。

## Evidence-backed findings
[AUTHOR_FACT] vanilla LLM trajectory evaluator 可能比小型 curated set 更损害 memory quality。[[evidence:ev-p064-evaluator-reliability]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 结果依赖 evaluator 与任务分布，不能把相关性观察外推成通用因果规律。

## Lineage and baselines
[CODEX_SYNTHESIS] memory retrieval → experience following → stored-error propagation。

## Evidence ledger
[CODEX_SYNTHESIS] 错误跟随和 evaluator 边界分别由两条 Evidence 支撑。

## Retrieval vocabulary
[CODEX_SYNTHESIS] memory error propagation; experience following; trajectory evaluator reliability; wrong stored experience
