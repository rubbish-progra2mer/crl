# v146 失败归因

## 类型

`OFF_NOMINAL_AGENT_VALIDATION_CLOSED_BY_DIFFERENTIAL_MUTATION_TESTING_AND_SEMANTIC_CONTENT_BASELINE`

## 直接原因

- 差分故障注入的承重计算是软件测试，不是智能体决策；
- 异常场景生成、变形关系和成对旧/新比较受 AgentAssay、变异测试及本 Run `v062/v131` 直接覆盖；
- 自动注入点选择归入程序分析或主动测试；
- 相同 ISO 内容下 JSON 与自然语言正确率近似，结构载体没有独立收益。

## 非原因

- 不是实验失败；
- 不是宿主安全边界；
- 不是 Run 终局。

## 决定

归档异常路径验证与结构化需求路线。Run 保持 `ACTIVE`，继续 frontier discovery。
