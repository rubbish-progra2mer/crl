# v060 研究图谱

## 主动诊断事实

- `v060-frontier-reset-005` 是 `ADVISORY_NON_AUTHORITATIVE` 的机械事实视图，不是科研裁决。
- Run 已有 59 个科学版本、4 次 Recorded 尝试和 3 次 Formal / Review-support 尝试；全文索引就绪、无跨 Run 污染，语义索引缺失。
- 近期版本大量死于直接或部件级近邻碰撞，说明下一步应先建立跨模型稳定现象，再生成方法，而不是继续从相邻组件拼装。

## 压缩候选的直接近邻

- [U-Fold](https://arxiv.org/abs/2601.18285) 已把压缩丢失细粒度约束、中间事实和演化意图列为核心失败，并提出意图感知折叠。
- [State Compression in Two-Agent LLM Relays](https://arxiv.org/abs/2607.18265) 已直接比较无压缩、叙事摘要、结构化 JSON 提取和嵌入裁剪，显示叙事压缩破坏下游可行性而结构化交接改善结果。
- [AgentDebug](https://arxiv.org/abs/2509.25370) 的失效分类已包含过度简化/不完整摘要、进度误判和结果误读。
- [Context Folding](https://openreview.net/forum?id=lNRgWoGfYg) 已用“完成子任务后折叠”保护长程执行上下文。
- [RE-TRAC](https://openreview.net/forum?id=wjNTbZKIvC) 已在跨轨迹结构状态中保存证据、不确定性、失败和未来计划。
- 当前 Run 的 `v045`、`v053` 与 `v058` 也已分别否决通用上下文记忆、状态化遗忘和摘要/技能上下文候选。

## 差分审计

候选“把未完成义务、开放依赖和失败边界写入结构化控制状态，再只折叠完成分支”由上述工作直接给出。即使本地复现错误终止，方法差分仍只剩字段命名、任务外壳或检查器组合，不能支撑独立方法贡献。
