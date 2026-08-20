# v150 失败归因

## 类型

`SCIENTIFIC_DOCUMENT_MULTI_AGENT_EXTRACTION_CLOSED_BY_PROGRESSIVE_GLOBAL_FILLING_AND_DOCUMENT_PIPELINE_OPTIMIZATION_PRIORS`

## 直接原因

- HERMES 的真实数据生产结果有效，但没有组件消融或公平基线识别多智能体编排；
- 共享状态、可靠字段优先、跨字段约束和多轮审议由 SudokuFill 直接实现并消融；
- 文档分解、流水线重写、验证提示和成本—准确率搜索由 DocETL/MOAR 直接覆盖；
- 来源追踪、领域规则和人工复核分别属于已有来源治理、任务规格与人工在环数据生产；
- 跨域需要修改模式/规则，且高维表格属性召回明显不足。

## 非原因

- 不是系统无工程价值；
- 不是数据规模或专家裁定不足；
- 不是本地实验失败；
- 不是 Run 终局。

## 决定

归档超长科学文档多智能体抽取、共享填充状态和流水线优化路线。Run 保持 `ACTIVE`，下一前沿离开文档抽取、来源追踪、跨字段填充和人工复核。
