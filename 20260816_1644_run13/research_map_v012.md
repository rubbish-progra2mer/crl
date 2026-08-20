# v012 研究图谱

- 固定知识库检索：`hypotheses_v012/searches/stale-observation-invalidation-001/`，91 篇论文、480 条观察。
- P030/ST​ALE 已研究隐式更新使旧记忆失效，并以前移的状态裁决处理冲突。
- ToolCacheAgent（OpenReview `tX3YcbNa5w`）已把工具分为 READ/WRITE，生成缓存策略，并用工具依赖规则使上游变化后的缓存结果失效；还在 τ-bench Retail 验证。
- Matrix（arXiv:2608.12761）记录事实依赖并选择性使受影响工作失效。
- MemTX（arXiv:2607.23929）用快照隔离、验证提交和级联修复管理状态型智能体记忆。
- 经验证的多智能体并发异常工作（arXiv:2606.17182）已形式化并实现陈旧生成、工具幻影和工具效果重排的检测/防止。
- EnvTrustBench（arXiv:2605.08828）已把陈旧、错误或恶意环境观察导致的错误行动作为环境落地缺陷评测。

结论：资源版本、读写依赖、失效传播和动作门控均已有直接实现；单智能体上下文内的实例化不足以形成新的 changed computation。
