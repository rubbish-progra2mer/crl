<!-- CRL_CARD_META {"schema_version":1,"card_id":"failure-untrusted-agent-metadata-privileged-control-flow","card_kind":"failure","paper_id":"P076","evidence_ids":["ev-p076-metadata-control-flow-laundering","ev-p076-refusal-not-system-safety","ev-p076-controlled-lab-boundary"],"source_refs":[{"path":"papers/P076_mas_malicious_code.pdf","sha256":"5fb79d30a11ef7b2e28d5eadc53af9b7ecb41d8ee60c8e04c2ec3c59e8b1fb11"}]} -->
# Untrusted Agent Metadata Can Launder Privileged Control Flow

## Observed failure
[AUTHOR_FACT] 外部内容可被前线 Agent 重述为内部 error/status metadata，orchestrator 再据此改变后续 Agent/capability 调用。[[evidence:ev-p076-metadata-control-flow-laundering]]

## Conditions and scope
[AUTHOR_FACT] 证据来自 controlled lab 而非生产攻击。[[evidence:ev-p076-controlled-lab-boundary]] [CODEX_SYNTHESIS] 还需存在不可信内容入口、adaptive orchestration 与可达高权限 capability。

## Failed intervention
[AUTHOR_FACT] 单个 Agent 的 refusal 或 warning 不能保证系统停止，其他 Agent 仍可能完成执行。[[evidence:ev-p076-refusal-not-system-safety]]

## Evidence and alternative explanations
[CODEX_SYNTHESIS] 来源支持 metadata/control-flow 差异，但模板按 orchestrator 调整、能力配置不同且缺少严格 matched component controls。

## Warning for future candidates
[CODEX_SYNTHESIS] multi-Agent Candidate 不得把 per-Agent alignment score 当系统安全；实验应追踪 provenance、authority 与最终 capability invocation。

## Possible repair boundary
[CODEX_HYPOTHESIS] typed provenance、least privilege 或 capability-side validation 是可实验边界，但 P076 未验证，不能登记为成功 Operator。

## Evidence ledger
[CODEX_SYNTHESIS] Failure path、refusal反例与实验边界均有 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] untrusted metadata authority; confused deputy agent; orchestrator hijack; refusal not compositional; privileged tool invocation
