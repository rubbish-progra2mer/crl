<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-llm-freshness-judgment-prior-override-and-drift","card_kind":"failure","paper_id":"P095","evidence_ids":["ev-p095-prior-override-drift","ev-p095-matched-comparison"],"source_refs":[{"path":"papers/P095_deterministic_freshness.pdf","sha256":"60f5542186d6e629e00885922dd57ee18e55f7775932c6991c2d76796c75b4a1"}]} -->
# LLM Freshness Judgment Fails via Prior-Override and Serial-Comparison Drift

## Observed failure
[AUTHOR_FACT] 两个命名失败模式：(1) prior-override——真实世界实体带强训练先验时，即使 prompt 有显式 "newer wins" 规则，LLM 仍输出先验值；(2) serial-comparison drift——候选池随上下文变长而增大时，LLM 跟丢最大序号（75%@64K→61%@262K）。[[evidence:ev-p095-prior-override-drift]]

## Conditions and scope
[AUTHOR_FACT] MAB FactConsolidation 载体、显式全序版本标记在场；matched 对照（同骨干/检索/切分/TOP_K/n）下换成 extract + Python max(serial) 得 +10.8pp，且作者自注这是管线级归因（resolver/prompt/温度联动）。[[evidence:ev-p095-matched-comparison]]
[CODEX_SYNTHESIS] 双作者 preprint；三骨干全 OpenAI 系（无跨家族）；SubEM 子串匹配利好冗长输出（作者自注略抬长上下文 oracle 基线），对短实体/弃答输出反而更严。

## Failed intervention
[CODEX_SYNTHESIS] 把"应用显式新鲜度规则"交给 LLM 上下文判断——规则在 prompt 里、版本标记在数据里，失败仍系统发生。

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 缺"共享抽取+LLM 挑最新"对照（作者自列 future work），resolver 单独贡献文内无法分离；LongMemEval 移植仅打平（57.8 vs 64.4）——载体有时间戳全序标记，平局源于问题型超出 current-value 域（max 为错算子），不证跨载体优势。间隙随上下文加宽（+8pp@6K→+21pp@262K）支持 drift 的机制解释。

## Warning for future candidates
[CODEX_SYNTHESIS] “LLM 能按明示规则做时序裁决”不能作为候选方法的未经验证假设；Yes/No、historical、aggregation 问题型是 max 的错算子域，可作为预注册分层维度。

## Possible repair boundary
[CODEX_HYPOTHESIS] 确定性装配层的适用前提是显式全序版本标记；无标记场景的时序裁决仍开放。

## Evidence ledger
[CODEX_SYNTHESIS] 两失败模式与 matched 对照+管线级自注分别绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] prior-override; serial-comparison drift; newer wins rule; freshness judgment; deterministic max; version marker; FactConsolidation; pipeline-level attribution; training prior overrides the newer fact; losing track of the largest serial; ignoring an explicit freshness rule; version tracking drift; failing to pick the most recent value
