<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-multi-agent-adversarial-coordination-spans-trust-surfaces","card_kind":"failure","paper_id":"P083","evidence_ids":["ev-p083-three-surface-adversarial-failure","ev-p083-lightweight-defense-failure","ev-p083-simulated-tool-boundary"],"source_refs":[{"path":"papers/P083_tamas.pdf","sha256":"4ad6d486003dc7268c80cdc2f49224a955792843d57155915d5f77889f7f7bdd"}]} -->
# Multi-Agent Adversarial Coordination Spans Multiple Trust Surfaces

## Observed failure
[AUTHOR_FACT] TAMAS 分别攻击 user prompt、environment/tool observations 与 compromised agents，说明风险不止来自单个模型输入。[[evidence:ev-p083-three-surface-adversarial-failure]]

## Conditions and scope
[AUTHOR_FACT] 工具均为 simulated，而非 live APIs。[[evidence:ev-p083-simulated-tool-boundary]] [CODEX_SYNTHESIS] 结果支持 trust-surface failure，不直接量化真实部署损失。

## Failed intervention
[AUTHOR_FACT] paraphrasing、output delimiters 与 LLM monitoring 的防御有限且跨模型不稳定；monitor 频繁 false positive。[[evidence:ev-p083-lightweight-defense-failure]]

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 来源跨攻击面与 Agent 配置报告失效，但 simulated tools、模型与 framework compatibility 限制外推。

## Warning for future candidates
[CODEX_SYNTHESIS] 系统安全实验必须分别追踪 instruction provenance、message/tool validation、agent compromise 与最终 capability invocation；不能用单 Agent refusal 或一个 aggregate safety score代替。

## Possible repair boundary
[CODEX_HYPOTHESIS] 分层 authority/provenance validation 值得测试，但 P083 未验证，故不登记成功 Operator。

## Evidence ledger
[CODEX_SYNTHESIS] taxonomy、defense failure 与 deployment boundary 分别绑定 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] multi agent trust surface; prompt injection; compromised agent; tool observation attack; lightweight defense false positive; simulated tools
