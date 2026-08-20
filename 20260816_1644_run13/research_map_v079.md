# v079 研究图谱

## Run 内重复：跨工具数值语义

- v038 已完整审计单位、比例尺度、时间基准和舍入约定在跨工具传递中的丢失。
- MeNTi 已执行单位不匹配检测、额外转换工具选择、嵌套调用、结果整合和参数回填；CalcQA 已单独评价单位换算准确率。
- 因此 v078 末尾提出的量纲/统计口径方向违反当前 Run 的既有负记忆，不再外部检索或实验。

## 同时资源争用

- *DPBench* 以哲学家就餐问题直接评价八种同时协调条件；GPT-5.2、Claude Opus 4.5 和 Grok 4.1 在部分条件下死锁率超过 95%，并把失败归因于多个模型独立收敛到相同策略。
  - https://arxiv.org/abs/2602.13255
- *Provable Coordination for LLM Agents via Message Sequence Charts* 已用消息序列图检查死锁和消息类型不匹配，并允许模型动态生成仍受结构保证约束的协调工作流。
  - https://arxiv.org/abs/2604.17612

## 共享状态并发一致性

- *Verified Detection and Prevention of Concurrency Anomalies in Multi-Agent Large Language Model Systems* 已形式化陈旧生成、幽灵工具、因果级联和工具效果重排，给出 TLA+ 反例、Verus 证明、三个 Rust 运行时和真实框架复现。
  - https://arxiv.org/abs/2606.17182
- *CoAgent* 直接研究长时间读—生成—写事务、宽而不透明的读集与即时生效写操作，在十个争用工作负载上比较串行正确性与并发收益。
  - https://arxiv.org/abs/2606.15376

## 经过时间与工具刷新

- *Your LLM Agents are Temporally Blind* 构造 TicToc：76 个多轮场景覆盖高、中、低时间敏感性，收集“调用工具/直接回答”的人类偏好；即使给出时间戳，没有模型的归一化对齐率超过 65%。
  - https://aclanthology.org/2026.findings-acl.1848/

## 结论

四条候选分别被当前 Run 负记忆、直接现象基准、形式化协议、机器验证并发层级或时间工具调用基准覆盖。本版不注册实验。
