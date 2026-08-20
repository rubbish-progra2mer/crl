# v104 假设组合

## H1：可见集合不完备感知

- 状态：`KILLED_BY_COVERAGE_AND_ADAPTIVE_RETRIEVAL_PRIORS`
- 原因：精确自适应检索、分页覆盖和依赖闭合 Top-K 已覆盖候选可见范围。

## H2：排序不变的证据选择

- 状态：`KILLED_BY_POSITION_BIAS_PRIOR_AND_V005`
- 原因：列表重排位置偏差已有直接工作；Run v005 的严格工具结果排列又未观察到效应。

## H3：证据边际价值停止

- 状态：`KILLED_BY_DIRECT_PRIORS_AND_RUN_MEMORY`
- 原因：多轮 RAG 停止、边际价值和长搜索利用诊断已直接覆盖，v081/v095 已关闭相邻路线。

## H4：配对关键证据响应

- 状态：`KILLED_BY_DIRECT_PRIOR_AND_V006`
- 原因：配对证据干预和 Run 内反事实工具结果利用是同一核心计算。

## 实验决定

不注册排序、隐藏候选、追加轮次或证据替换实验；正反结果均只复现既有问题。
