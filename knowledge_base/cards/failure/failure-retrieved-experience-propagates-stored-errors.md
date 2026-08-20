<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-retrieved-experience-propagates-stored-errors","card_kind":"failure","paper_id":"P064","evidence_ids":["ev-p064-experience-following-error","ev-p064-evaluator-reliability"],"source_refs":[{"path":"papers/P064_experience_following_memory.pdf","sha256":"2c3992d238f5d6dec4ed96faae0a82e3b88edc6e37b26d8622a2b780f2160400"}]} -->
# Retrieved Experience Can Reproduce and Compound Stored Errors

## Observed failure
[AUTHOR_FACT] 与当前 query 具有高 input similarity 的 retrieved record 会诱导 Agent 模仿输出，并重复、累积错误经验。[[evidence:ev-p064-experience-following-error]]

## Conditions and scope
[CODEX_SYNTHESIS] 绑定经验检索/跟随设置；不扩展为用户排除的环境反馈学习或执行恢复方向。

## Failed intervention
[CODEX_SYNTHESIS] 仅按 input/query similarity 召回并遵循历史，不保证 recalled trajectory 正确或适用于当前状态。

## Evidence and alternative explanations
[AUTHOR_FACT] vanilla LLM trajectory evaluator 也可能比小型 curated set 更损害 memory quality。[[evidence:ev-p064-evaluator-reliability]]

## Warning for future candidates
[CODEX_SYNTHESIS] memory 增益必须报告错误写入、错误召回与 follow-through，而不能只报 recall coverage。

## Possible repair boundary
[CODEX_HYPOTHESIS] 可靠性门控可能有用，但本 Evidence 不支持自动 verifier 必然修复。

## Evidence ledger
[CODEX_SYNTHESIS] error propagation 与 evaluator unreliability 分别有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] memory error propagation; wrong experience retrieval; experience following; unreliable trajectory evaluator
