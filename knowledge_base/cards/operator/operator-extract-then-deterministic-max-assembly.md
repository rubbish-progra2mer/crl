<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-extract-then-deterministic-max-assembly","card_kind":"operator","paper_id":"P095","evidence_ids":["ev-p095-matched-comparison","ev-p095-prior-override-drift"],"source_refs":[{"path":"papers/P095_deterministic_freshness.pdf","sha256":"60f5542186d6e629e00885922dd57ee18e55f7775932c6991c2d76796c75b4a1"}]} -->
# Extract-Candidates-Then-Deterministic-Max Assembly for Version Conflicts

## Intervention target
[CODEX_SYNTHESIS] 检索后装配层：检回的多版本候选中，哪个值进入最终答案——把该裁决从 LLM 上下文判断移出。

## Before and after computation
[AUTHOR_FACT] Before：LLM 读全部候选并按规则挑最新。After：LLM 只做语义候选抽取（verbatim、不挑最优），Python max(serial) 做确定性择新；多跳经 per-hop 分解逐跳解析。整管线约 50 行。[[evidence:ev-p095-matched-comparison]]（verbatim/不挑最优指令与 ≈50 行细节出自 §3.1，PDF 直核；所绑引文为摘要段）

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入：检回 chunk + 显式全序版本标记（serial）。输出：单一当前值。时点：检索后、生成前；索引期 fact-level 切分保留版本元数据是第二个（前移的）干预点。

## Mechanism hypothesis
[AUTHOR_FACT] 结构化抽取消除两个失败模式：移除实体文本使先验无从覆盖；缩池到 1-3 候选使序号跟踪不再漂移，max() 精确。[[evidence:ev-p095-prior-override-drift]]

## Predicted observable signature
[CODEX_SYNTHESIS] 增益随上下文长度加宽（+8pp@6K→+21pp@262K 实测）；条件化于"事实确已检回"时退化定位在判断层（union-accuracy 88.5% 天花板 + McNemar p<0.001）。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 硬前提：显式全序版本标记（恰为 FactConsolidation 构造性质；LongMemEval 的会话时间戳亦构成全序）；LongMemEval 上仅打平——平局源于问题型超出 current-value 域（max 为错算子），跨载体优势不证。+10.8pp 是管线级效应（resolver 单独贡献无对照）；strict 抽取会过度拒绝；hybrid 回退实测无效（+0.2pp）。

## Source lineage
[CODEX_SYNTHESIS] LLM 时序判断线 → 确定性装配层（本文）；与 P091 写侧 supersession 分占管线两端。

## Evidence ledger
[AUTHOR_FACT] 管线定义/matched 增益与机制解释绑定 exact Passage。[[evidence:ev-p095-matched-comparison]] [[evidence:ev-p095-prior-override-drift]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] extract then aggregate; deterministic resolver; Python max serial; per-hop resolution; candidate extraction; assembly layer; version metadata; union accuracy; McNemar; deterministic freshness resolver; extract candidates then take the max; python max over serials; assembly-time version selection; taking freshness out of the LLM; picking the freshest candidate deterministically
