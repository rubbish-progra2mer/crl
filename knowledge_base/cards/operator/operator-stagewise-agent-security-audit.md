<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-stagewise-agent-security-audit","card_kind":"operator","paper_id":"P008","evidence_ids":["ev-p008-stagewise-attack-surface"],"source_refs":[{"path":"papers/P008_agent_security_bench.pdf","sha256":"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9"}]} -->
# Stagewise Agent Security Audit

## Intervention target
[AUTHOR_FACT] 按 system prompt、user prompt、tool use 与 memory retrieval 等 operational steps 分解攻击与防御。[[evidence:ev-p008-stagewise-attack-surface]]

## Before and after computation
[CODEX_SYNTHESIS] Baseline 是只报总体 attack success；changed computation 是按干预入口分别施加攻击并测 utility/security。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为阶段化攻击载荷与 Agent 执行，输出为攻击、防御和任务效用指标；干预点随阶段而变。分入口攻击/防御会增加评测条件；当前 Evidence 未量化或配平各条件的 token、调用数与时延。

## Mechanism hypothesis
[CODEX_SYNTHESIS] 阶段化分解能区分同一表面失败究竟来自 prompt、memory 还是 tool channel。

## Predicted observable signature
[CODEX_HYPOTHESIS] 有效防御应在目标入口降低攻击成功，同时不过度损伤无攻击任务效用。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 攻击模板与 Agent architecture 必须对应；benchmark 覆盖不代表开放世界攻击完备性。

## Source lineage
[CODEX_SYNTHESIS] ASB 是 safety/evaluation 来源；该 Operator 是诊断框架，不是自动防御器。

## Evidence ledger
[AUTHOR_FACT] `ev-p008-stagewise-attack-surface` 定位到 PDF p.2 的阶段与攻击类型。[[evidence:ev-p008-stagewise-attack-surface]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] agent security benchmark；prompt injection；memory poisoning；tool attack；stagewise attack surface；Agent 安全入口。
