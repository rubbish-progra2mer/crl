# v102 假设组合

## H1：工具等待感知的恢复批处理

- 状态：`KILLED_BY_DIRECT_SYSTEM_PRIORS`
- 原因：TideRL 与 Ready Cohorts 已直接使用代理就绪积压、到达状态和模型—工具控制转移进行批处理与资源调度。

## H2：跨暂停的语义键值缓存存活

- 状态：`KILLED_BY_CACHE_AND_SERVING_PRIORS`
- 原因：vToken 已处理细粒度存活与物理回收，代理前缀放置和缓存策略也属于成熟服务问题；没有新的语义真值或监督信号。

## H3：工具意图驱动的沙箱预热

- 状态：`KILLED_BY_DIRECT_PRIOR`
- 原因：SpecBox 已在令牌生成期间预测工具需求、预热隔离沙箱并沿依赖图预取后续环境。

## H4：恢复时效果与观察重认证

- 状态：`KILLED_BY_RESUME_CONTRACT_AND_RUN_MEMORY`
- 原因：Resume Contract 已覆盖恰好一次、一次消费和并发恢复；状态刷新、未来完成和迟到结果又分别由 v012/v052/v065 覆盖。

## 实验决定

不注册离散事件仿真或本地模型实验。它们无法超过直接系统论文的真实负载测量、机器检查契约和实现级结果。
