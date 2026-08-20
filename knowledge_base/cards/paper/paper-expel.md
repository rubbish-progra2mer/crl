<!-- CRL_CARD_META {"schema_version":1,"card_id":"paper-expel","card_kind":"paper","paper_id":"P018","evidence_ids":["ev-p018-insight-update-operations","ev-p018-raw-reflection-contamination"],"source_refs":[{"path":"papers/P018_expel.pdf","sha256":"01e533d81fb4a5f91797c073a9b1929acbaa64da45a592b26563ca7d135024f3"}]} -->
# ExpeL

## Role in the knowledge base
[CODEX_SYNTHESIS] Agent experiential learning 与跨任务 memory 的机制来源，并提供 reflection contamination 消融。

## Problem and setting
[CODEX_SYNTHESIS] 从训练任务多次 trial 的成功/失败轨迹抽取经验，测试任务单次执行时复用，不更新参数。

## Changed computation
[AUTHOR_FACT] Insight library 通过 ADD、UPVOTE、DOWNVOTE、EDIT 维护。[[evidence:ev-p018-insight-update-operations]]

## Evidence-backed findings
[AUTHOR_FACT] 把 raw reflections 加入 insight generation 会降低表现。[[evidence:ev-p018-raw-reflection-contamination]]

## Limitations and failure signals
[CODEX_SYNTHESIS] 离线 GPT-4、更多 prompt tokens 与 retrieved trajectories 是额外资源；不能只归因于“经验学习”。

## Lineage and baselines
[CODEX_SYNTHESIS] Reflexion 是单任务 retry 祖先；ExpeL 将经验扩展到跨任务 insights 与成功轨迹 recall。

## Evidence ledger
[AUTHOR_FACT] p.3 支持 insight operations；p.10 支持 reflection ablation。[[evidence:ev-p018-insight-update-operations]] [[evidence:ev-p018-raw-reflection-contamination]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] ExpeL；experiential learning；insight extraction；successful trajectory recall；经验学习 Agent。

