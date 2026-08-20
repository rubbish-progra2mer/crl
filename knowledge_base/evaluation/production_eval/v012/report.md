# v012 内容修复回放报告

性质：`CONTENT_REPAIR_REGRESSION_REPLAY`

本次评测只验证：收窄 P091 Paper Card 中一段越出行内 Evidence 的作者事实并全量重建 Card 全文索引后，既有客观研究查询仍能发现相应的外部论文知识。它不是新的隐藏盲测，不增加相关性标注，也不证明科研机器通过任何产品验收。

## 输入与修复边界

- 正式外部论文：99 篇；Passage：3995；Evidence：224，均未改动。
- Card：228 张，其中 Paper 99、Operator 66、Failure 63；仅 `paper-p091.md` 的 `Problem and setting` 作者事实被收窄。
- Card source signature：`a512499ae91e0b24c3aa13f9d2ae0a5a7bc3e790152bef5e80500573997c60f9`。
- 查询与直接阅读相关性标注复用 v011 已冻结的 20 条 Calibration 和 18 条 Blind 客观查询；本次只在当前索引上重放，不产生新的判断标签。

## 结果

- Calibration：20/20 top-5 命中；critical 8/8。
- Blind replay：17/18 top-5 命中；critical 5/5。
- 原始逐查询结果：`content_repair_replay.json`。

## P091 相关读面抽查

- Failure 冻结查询仍以 `failure-cosine-cannot-separate-contradiction-from-duplicate` 为 top-1。
- Operator 冻结查询仍以 `operator-deterministic-sro-supersession-ledger` 为 top-1。
- Paper 诊断查询 `temporal validity stale current retrieval memory supersession` 仍以 `paper-p091` 为 top-1。

## 结论边界

本次事实收窄没有破坏 P091 所在的记忆时效性知识发现路径。唯一普通 Blind 查询 miss 与 v011 相同，继续作为非阻断诊断保留；检索结果不是科研证据，正式结论仍须回到 Card、Evidence 和论文原文。
