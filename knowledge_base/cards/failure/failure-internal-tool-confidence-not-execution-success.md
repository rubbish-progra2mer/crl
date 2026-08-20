<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-internal-tool-confidence-not-execution-success","card_kind":"failure","paper_id":"P073","evidence_ids":["ev-p073-execution-supervised-probe","ev-p073-internal-confidence-misalignment"],"source_refs":[{"path":"papers/P073_probecal.pdf","sha256":"2c56eb776ba9caf9dbe0663fdabbafc2941c10c08394494df158c5980090cc53"}]} -->
# Internal Tool Confidence Is Not Execution Success Probability

## Observed failure
[AUTHOR_FACT] 两段表面相似的 tool code traces 可分别错误和正确，却得到相近的未校准 uncertainty。[[evidence:ev-p073-internal-confidence-misalignment]]

## Conditions and scope
[CODEX_SYNTHESIS] 适用于外部工具决定最终正确性的候选选择；不等于所有 LLM log probabilities 都毫无信息。

## Failed intervention
[CODEX_SYNTHESIS] 直接用 token/logit confidence 或等权 self-consistency 代表真实执行成功。

## Evidence and alternative explanations
[AUTHOR_FACT] P073 用执行结果监督的 MLP 替代原始 confidence。[[evidence:ev-p073-execution-supervised-probe]] [CODEX_SYNTHESIS] 收益可能依赖有标签、同分布数据及可访问 hidden embeddings。

## Warning for future candidates
[CODEX_SYNTHESIS] 任意“让 Agent 自评工具把握度”的 Candidate 都必须验证 confidence 与真实 execution outcome 的映射，不能只看语言一致性。

## Possible repair boundary
[CODEX_SYNTHESIS] 可用 matched offline execution labels 训练 probe，但必须暴露监督量、迁移 split 与 test-time 可用信息。

## Evidence ledger
[CODEX_SYNTHESIS] Failure 与来源中的 supervised repair 各有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] tool confidence miscalibration; execution success; trace uncertainty; self confidence failure; outcome supervision
