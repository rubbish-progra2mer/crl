<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p057","card_kind":"paper","paper_id":"P057","evidence_ids":["ev-p057-archive-code-search","ev-p057-search-evaluation-budget"],"source_refs":[{"path":"papers/P057_adas.pdf","sha256":"32eb1c1a6888e35fae0f618e33c58698b54d9c49bc063fef91ee591719fca376"}]} -->
# Automated Design of Agentic Systems

## Role in the knowledge base
[CODEX_SYNTHESIS] 以代码为搜索空间的 Agent-system discovery 祖先，提供 archive-conditioned search 与评估泄漏警告。

## Problem and setting
[AUTHOR_FACT] Meta agent 读取既有发现 archive 并编写新 Agent 代码。[[evidence:ev-p057-archive-code-search]]

## Changed computation
[CODEX_SYNTHESIS] 从人工设计 workflow 转为由 meta agent 迭代产生可执行 Agent implementation。

## Evidence-backed findings
[AUTHOR_FACT] ARC 搜索运行 25 轮，并重复使用 held-out test data 评价已发现 Agent。[[evidence:ev-p057-search-evaluation-budget]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 搜索预算与反复接触 test feedback 使最终选择不能被视为严格一次性 held-out 估计。

## Lineage and baselines
[CODEX_SYNTHESIS] GPTSwarm graph optimization → ADAS program search → AFlow workflow refinement。

## Evidence ledger
[CODEX_SYNTHESIS] archive-conditioned code search 与 selection/evaluation boundary 均有直接 Evidence。

## Retrieval vocabulary
[CODEX_SYNTHESIS] automated agent design; meta-agent code search; archive-conditioned discovery; test reuse; workflow generation
