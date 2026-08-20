# v011 内容清洗回放报告

性质：`CONTENT_CLEAN_REGRESSION_REPLAY`

本次评测只验证：删除共享知识库中的科研运行派生叙述并重建 Card 全文索引后，既有客观研究查询仍能召回相应的外部论文知识。它不是新的隐藏盲测，也不证明科研机器已通过任何产品验收。

## 输入

- 正式外部论文：99 篇；Passage：3995；Evidence：224。
- Card：228 张，其中 Paper 99、Operator 66、Failure 63。
- Card source signature：`1a3e84835ff624b865c74d1f47c836d20d1658383963253ee5916f197b66329d`。
- 查询与直接阅读相关性标注取自清洗前最后一组只含客观研究问题的冻结评测；回放结果已自包含查询文本、相关 Card 和 top-10 Card ID，不依赖旧评测目录才能核验。

## 结果

- Calibration：20/20 top-5 命中；critical 8/8。
- Blind replay：17/18 top-5 命中；critical 5/5。
- 原始逐查询结果：`content_clean_replay.json`。

## 结论边界

清洗没有破坏关键 Card 的发现能力。唯一普通查询 miss 保留为非阻断诊断，不据此自动改写 Card。后续若知识内容再次发生实质变化，主 Sol 5.6 可按科研价值决定是否进行新的独立知识库评测；评测不是正式 Run 的状态门。
