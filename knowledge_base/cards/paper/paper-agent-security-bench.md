<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-agent-security-bench","card_kind":"paper","paper_id":"P008","evidence_ids":["ev-p008-stagewise-attack-surface","ev-p008-memory-defense-high-fnr"],"source_refs":[{"path":"papers/P008_agent_security_bench.pdf","sha256":"e2505f8632bfcb6a64a4390a3170b3ca1dfd3f9916d7c3cf9ba2b89887b3a0c9"}]} -->
# Agent Security Bench

## Role in the knowledge base
[CODEX_SYNTHESIS] Pilot 的 Agent safety 入口、攻击面分解与防御失败来源。

## Problem and setting
[CODEX_SYNTHESIS] 多场景 LLM Agents，覆盖 prompt、tool、memory 与 planning 相关攻击/防御和 utility-security 指标。

## Changed computation
[AUTHOR_FACT] Benchmark 按 Agent operational step 组织攻击与防御。[[evidence:ev-p008-stagewise-attack-surface]]

## Evidence-backed findings
[AUTHOR_FACT] 所测 LLM memory defenses 的平均 FNR 为 0.660。[[evidence:ev-p008-memory-defense-high-fnr]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 攻击模板、场景与防御实现限定结论；单一安全分数不能替代 FNR、FPR 与 clean utility。

## Lineage and baselines
[CODEX_SYNTHESIS] 该论文主要是 evaluation/failure 来源，不因防御榜单自动产生通用防御 Operator。

## Evidence ledger
[AUTHOR_FACT] p.2 支持阶段化攻击面；p.34 支持 memory defense 漏检。[[evidence:ev-p008-stagewise-attack-surface]] [[evidence:ev-p008-memory-defense-high-fnr]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] ASB；agent security；prompt injection；memory poisoning；false negative defense；Agent安全基准。

