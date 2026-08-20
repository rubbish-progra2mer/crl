<!-- CRL_CARD_META {"schema_version":1,"card_id":"operator-dynamic-reflection-gate","card_kind":"operator","paper_id":"P014","evidence_ids":["ev-p014-dynamic-reflection-gate"],"source_refs":[{"path":"papers/P014_instruct_of_reflection.pdf","sha256":"57a01e87496308e3345839c48f085516dd2824ec5aaacf51b71f127c12f42bb7"}]} -->
# Dynamic Stop–Select–Refresh Reflection Gate

## Intervention target
[AUTHOR_FACT] 在每轮反思后增加 select、stop 或 refresh 指令决策。[[evidence:ev-p014-dynamic-reflection-gate]]

## Before and after computation
[CODEX_SYNTHESIS] Baseline 是固定次数“生成—批评—改写”；changed computation 是比较候选后动态保留、停止或重启。

## Inputs outputs information and timing
[CODEX_SYNTHESIS] 输入为问题、basic/reflected response、抽取答案与 meta criterion，输出为被选响应或下一轮控制指令。

## Mechanism hypothesis
[CODEX_SYNTHESIS] 显式控制器减少正确答案被后续反思破坏、无效重复和错误吸引子停留。

## Predicted observable signature
[CODEX_HYPOTHESIS] 控制器应降低 correct→wrong transition 与无效迭代，而不是只靠增加最大轮数改善。

## Preconditions and transfer risks
[CODEX_SYNTHESIS] 需要可比较候选和可靠 selector；开放工具轨迹难以用答案 equality 直接迁移。

## Source lineage
[CODEX_SYNTHESIS] IoRT 是直接来源；本 Operator 位于反思候选产生后的动态控制节点。

## Evidence ledger
[AUTHOR_FACT] `ev-p014-dynamic-reflection-gate` 定位到 PDF p.6 的指令三分支。[[evidence:ev-p014-dynamic-reflection-gate]]

## Retrieval vocabulary
[CODEX_SYNTHESIS] reflection controller；stop select refresh；adaptive reflection；candidate selection gate；动态反思停止。
