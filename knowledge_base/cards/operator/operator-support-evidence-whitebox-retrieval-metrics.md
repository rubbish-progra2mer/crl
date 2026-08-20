<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-support-evidence-whitebox-retrieval-metrics","card_kind":"operator","paper_id":"P092","evidence_ids":["ev-p092-whitebox-metrics","ev-p092-crs-low"],"source_refs":[{"path":"papers/P092_memconflict.pdf","sha256":"1918dd32c20affd501ac314ab4f1c5b67ab71dc2178784d31b6596030abbebce"}]} -->
# White-Box Support-Evidence Retrieval Metrics for Memory Conflicts

## Intervention target
[CODEX_SYNTHESIS] 记忆冲突评测的测量层：把"系统答对了吗"分解为"gold 一致的支持记忆项被检回了吗、排多高、证据在场但未被答案利用的差距（EUG）"。

## Before and after computation
[AUTHOR_FACT] Before：黑盒答案准确率。After：SEH@K 检查 top-K 检回集是否含与 gold 一致的记忆项；SRS 对其排名做对数折扣计分；配合 EUG（Evidence Utilization Gap＝SEH@3−AA，附录定义）诊断构成白盒层。[[evidence:ev-p092-whitebox-metrics]]

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入：每查询的 gold 一致记忆项标注 + 系统检回列表。输出：分冲突类型的检索侧指标面板。时点：评测时，与生成侧指标并行。

## Mechanism hypothesis
[CODEX_HYPOTHESIS] 冲突处理失败可发生在检索层（支持证据不在场）或裁决层（在场但未被选用）；白盒分解定位失败层，避免把裁决失败误诊为检索失败。

## Predicted observable signature
[AUTHOR_FACT] 实测解耦：AA 与 CRS 排序不一致（Memobase 高静态 AA + 最低 CRS），证明分解揭示黑盒不可见的结构。[[evidence:ev-p092-crs-low]]

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 前提是每个查询都有 gold 一致记忆项标注（构造性基准易得，野生数据昂贵）；K 的选择影响 SEH 口径。迁移到版本化记忆时，“支持证据”需映射为版本正确的事实块，并与 union-accuracy（P095 口径）对齐。

## Source lineage
[CODEX_SYNTHESIS] RAG 冲突研究的文档级指标 → 长期记忆条件下的记忆项级白盒指标（本文），可作为分层测量协议的候选组件。

## Evidence ledger
[AUTHOR_FACT] SEH@K/SRS 定义与 AA-CRS 解耦实测分别绑定 exact Passage。[[evidence:ev-p092-whitebox-metrics]] [[evidence:ev-p092-crs-low]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] white-box evaluation; support evidence hit at K; support rank score; evidence utilization gap; retrieval-generation decomposition; memory conflict metrics; white-box retrieval metrics; support evidence hit at k; retrieval versus adjudication decomposition; gold-consistent memory item; ranking supporting evidence
