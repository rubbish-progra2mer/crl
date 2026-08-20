# v104 失败归因

## 失败类型

`SEARCH_VISIBILITY_FRONTIER_KILLED_BY_COVERAGE_ORDER_STOPPING_AND_COUNTERFACTUAL_PRIORS`

## 直接原因

- 候选可见范围被精确自适应检索与覆盖义务吸收；
- 顺序效应被列表位置偏差工作覆盖，并受 v005 零效应约束；
- 追加搜索被结构化停止和边际价值工作覆盖；
- 关键证据替换被配对证据干预和 v006 覆盖。

## 范围

这是先行工作碰撞，不是实验反证；未涉及 v029 安全路径。只淘汰当前检索可见性候选，Run 保持 `ACTIVE`。
