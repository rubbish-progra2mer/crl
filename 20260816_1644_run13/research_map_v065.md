# v065 研究图谱

## 资源状态与调度

- 401/403/429 等认证、授权与重试窗口可由 v001 已测的类型化结果语义和标准协议字段表达，没有形成新计算。
- [TPS-Bench](https://aclanthology.org/2026.acl-long.1614/) 已系统评价复合任务的工具计划、依赖与执行调度。
- [Budget-Constrained Tool Learning](https://aclanthology.org/2024.findings-acl.536/) 已直接处理工具使用预算。
- [Scalable LLM Agent Tool Access in the Cloud](https://arxiv.org/abs/2607.15593) 已在 MCP 网关处理访问控制、兼容、推荐与有状态后端会话亲和性。
- [Agentic-V2X](https://arxiv.org/abs/2607.04290) 已提供截止时间约束下的验证和调度实例。

因此“资源契约卡/共享配额规划”被类型化错误、工具调度和经典资源约束规划吸收。

## 取消后的迟到完成

- [Stop Means Stop](https://arxiv.org/abs/2607.14166) 已在六个智能体框架测量暂停侧漏、重放双执行、取消孤儿与超时僵尸，并以外部效果门实现 `fence-on-cancel`。
- [InterruptBench](https://arxiv.org/abs/2604.00892) 已覆盖长程网页智能体中的新增、修订与撤回三类用户中断。
- [Atomix](https://openreview.net/attachment?id=UeRbEpSVUz&name=pdf) 已用 epoch、资源 frontier、事务提交/中止和补偿处理并发与迟到效果。
- [S-ORA](https://openreview.net/pdf/4dbda0dc1da2b73b64d0278154df41a7aaffc964.pdf) 已把工具建模为独立演化的异步对象。

世代栅栏、取消 fence 与迟到结果隔离均已有直接计算，不能注册重复实验。

## 检索说明

`crl recall` 的相关查询返回 `NON_AUTHORITATIVE_DERIVED_RECALL`，主要命中当前 Run 派生片段，且语义索引状态为 `DEGRADED / semantic_index_missing`。这些结果未被用于文献结论，也没有读取其他 Run。
