<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-p095","card_kind":"paper","paper_id":"P095","evidence_ids":["ev-p095-matched-comparison","ev-p095-prior-override-drift"],"source_refs":[{"path":"papers/P095_deterministic_freshness.pdf","sha256":"60f5542186d6e629e00885922dd57ee18e55f7775932c6991c2d76796c75b4a1"}]} -->
# Don't Ask the LLM to Track Freshness: Deterministic Conflict Resolution

## Role in the knowledge base
[CODEX_SYNTHESIS] 装配层确定性择新的直接比较谱系，也是 prior-override / serial-drift 两个命名失败模式的来源。

## Problem and setting
[CODEX_SYNTHESIS] 演化事实的记忆 QA：显式全序版本标记在场时，LLM 仍不能可靠应用 "newer wins" 规则。

## Changed computation
[AUTHOR_FACT] extract-then-max 三步管线：检索 → LLM 语义候选抽取 → Python max(serial) 确定性择新后直接返回该候选的抽取实体（无生成步，§3.1）；multi-hop 用 per-hop 确定性解析。[[evidence:ev-p095-matched-comparison]]

## Evidence-backed findings
[AUTHOR_FACT] matched 对照 +10.8pp（67.2→78.0），间隙随上下文加宽至 +21pp@262K；两失败模式有机制解释与量化（drift 75%→61%）。[[evidence:ev-p095-prior-override-drift]]
[CODEX_SYNTHESIS] union-accuracy 软天花板（88.5%；剩余 11.5% 为检索失败下界）+ McNemar 配对、互补性分析（21.3% vs 10.5%）是可复用评测算子。

## Limitations and failure signals
[CODEX_SYNTHESIS] +10.8pp 为管线级归因（作者四处自注）；实际两个干预点（索引期元数据保留 + 装配层）而 matched 对照只对齐后段；缺 LLM-picks-newest 对照；LongMemEval 平局；三骨干全 OpenAI 系；SubEM 子串匹配利好冗长输出（作者自注会略抬高长上下文 oracle 基线），对短实体/弃答输出反而更严；跨系统对比 chunking 不对齐。

## Lineage and baselines
[CODEX_SYNTHESIS] 与 P091（写侧）、P094（评测载体）三角互补；OP5 问题类型路由 proposed-untested。本文可支持比较谱系、失败模式和评测算子，但不能单独证明 resolver 的独立贡献。

## Evidence ledger
[CODEX_SYNTHESIS] matched 增益与失败模式绑定 exact Passage。

## Retrieval vocabulary
[CODEX_SYNTHESIS] deterministic freshness; extract-then-max; memory conflict resolution; prior-override; serial drift; assembly-level; CAR; FactConsolidation SOTA; deterministic memory conflict resolution; tracking freshness without the LLM; version conflict pipeline
