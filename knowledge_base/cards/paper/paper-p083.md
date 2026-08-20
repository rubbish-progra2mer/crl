<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p083","card_kind":"paper","paper_id":"P083","evidence_ids":["ev-p083-three-surface-adversarial-failure","ev-p083-lightweight-defense-failure","ev-p083-simulated-tool-boundary"],"source_refs":[{"path":"papers/P083_tamas.pdf","sha256":"4ad6d486003dc7268c80cdc2f49224a955792843d57155915d5f77889f7f7bdd"}]} -->
# TAMAS: A Comprehensive Benchmark for Multi-Agent System Safety

## Role in the knowledge base
[CODEX_SYNTHESIS] 多 Agent 安全的负向覆盖锚点；用于把个体模型、消息/工具环境与协作拓扑的攻击面分开。

## Problem and setting
[CODEX_SYNTHESIS] 多 Agent 系统把用户、工具环境与其他 Agent 的信息跨信任边界传播，单模型安全评测不足。

## Changed computation
[CODEX_SYNTHESIS] 本文不提出已验证成功算子，而是系统化改变攻击注入面与协作配置进行评测。

## Evidence-backed findings
[AUTHOR_FACT] 基准覆盖 prompt-level、environment-level 与 compromised-agent attacks。[[evidence:ev-p083-three-surface-adversarial-failure]]

## Limitations and failure signals
[AUTHOR_FACT] paraphrasing、delimiter 与 monitor 等轻量防御仅有限或不稳定降低攻击，monitor 还有频繁 false positives。[[evidence:ev-p083-lightweight-defense-failure]]
[AUTHOR_FACT] 所有工具均为 simulated tools，用于可复现并隔离外部 API 波动。[[evidence:ev-p083-simulated-tool-boundary]]

## Lineage and baselines
[CODEX_SYNTHESIS] 论文没有验证一个足以登记为可复用成功防御算子的机制，因此本轮只建立 Failure Card。

## Evidence ledger
[CODEX_SYNTHESIS] 攻击面、轻量防御失败和 simulated-tool 边界分别有原文 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] multi agent safety benchmark; prompt environment compromised agent attack; lightweight defense false positive; simulated adversarial tool; orchestration trust surface
