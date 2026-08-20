# v102 失败归因

## 失败类型

`AGENT_RUNTIME_SCHEDULING_KILLED_BY_READINESS_CACHE_SANDBOX_AND_RESUME_PRIORS`

## 直接原因

- 就绪批处理被 TideRL 与 Ready Cohorts 直接覆盖；
- 细粒度缓存回收被 vToken 覆盖；
- 工具沙箱预热被 SpecBox 覆盖；
- 中断/崩溃恢复的恰好一次与一次消费被 Resume Contract 覆盖；
- 等待后的执行正确性残差与 v012/v052/v065/v075 同构。

## 非归因与范围

v102 未运行系统性能实验，不是经验反证；未研究或执行安全绕过；只淘汰上述运行系统路线，不改变宽 Charter 或 `ACTIVE` 状态。
