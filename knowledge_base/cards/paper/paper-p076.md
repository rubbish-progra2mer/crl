<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p076","card_kind":"paper","paper_id":"P076","evidence_ids":["ev-p076-metadata-control-flow-laundering","ev-p076-refusal-not-system-safety","ev-p076-controlled-lab-boundary"],"source_refs":[{"path":"papers/P076_mas_malicious_code.pdf","sha256":"5fb79d30a11ef7b2e28d5eadc53af9b7ecb41d8ee60c8e04c2ec3c59e8b1fb11"}]} -->
# Multi-Agent Systems Execute Arbitrary Malicious Code

## Role in the knowledge base
[CODEX_SYNTHESIS] 高优先级多 Agent Failure：不可信数据经前线 Agent 改写成 status/error metadata 后获得 orchestration authority，形成 confused-deputy control-flow laundering。

## Problem and setting
[AUTHOR_FACT] 来源攻击利用跨 Agent 信任和 adaptive error handling，把外部内容送入 orchestrator 的控制决策。[[evidence:ev-p076-metadata-control-flow-laundering]]

## Changed computation
[CODEX_SYNTHESIS] 干预点是 metadata 到 next-agent/capability selection 的边界，不是单个 Agent 是否生成拒绝文本。

## Evidence-backed findings
[AUTHOR_FACT] 来源记录了 sub-agent 已识别、警告或拒绝危险动作，但系统中其他 Agent 仍完成执行的实例。[[evidence:ev-p076-refusal-not-system-safety]]

## Limitations and failure signals
[AUTHOR_FACT] 所有实验均为 controlled lab，未攻击生产 live-agent service。[[evidence:ev-p076-controlled-lab-boundary]] [CODEX_SYNTHESIS] 严重后果还依赖可达的 code/data/network capability；来源未验证防御。

## Lineage and baselines
[CODEX_SYNTHESIS] 它属于 indirect prompt injection 的系统级 metadata/control-flow 变体；不能写成与 prompt injection 完全无关。最近 baseline 应匹配 error format、role instruction、capability 和 orchestrator。

## Evidence ledger
[CODEX_SYNTHESIS] 机制、refusal composition failure 与部署边界均有 Evidence；不保存 payload 或攻击模板。

## Retrieval vocabulary
[CODEX_SYNTHESIS] multi agent control flow hijack; untrusted metadata; confused deputy; orchestrator authority; refusal composition; capability laundering
