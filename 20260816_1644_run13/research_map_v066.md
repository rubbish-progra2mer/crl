# v066 研究图谱

## 主动诊断事实

`crl-active-diagnosis` 生成 `v066-frontier-reset-006`，权威为 `ADVISORY_NON_AUTHORITATIVE`，facts SHA-256 为 `709d0a79feee77bbbeaf0a6f9c6afe8d88106e18e45c98a87a2eda0a36295133`。FTS 为 READY，semantic 因 `semantic_index_missing` 为 DEGRADED；Run-wide 有 65 个科学版本、9 次 Recorded、3 次 Formal/Review-support、16 个搜索快照，Recall contamination 为 false、陈旧源为 0。诊断不做科研裁决。

主研究者解释：近期失败集中于把经典分布式系统原语迁入智能体；下一高信息量动作应先验证跨模型稳定现象，再决定是否生成方法。

## 最近工作边界

- [Verified Tool Calls](https://arxiv.org/abs/2608.02645) 用只读后置条件验证器并明确称重复验证不会引入副作用，因而暴露“验证读取是否真的纯”这一环境假设。
- [ETAS](https://arxiv.org/abs/2607.17780) 已把工具调用、内存读写、授权与外部动作纳入一般效果行和轨迹语义；全文公开语义未出现消费型资源或非幂等读取，`affine` 只约束处理器恢复次数。
- [ToolSandbox](https://aclanthology.org/2025.naacl-findings.65/) 与 [ComplexMCP](https://openreview.net/pdf/e5d4569a13646e399cb4f140dee92a200e9ddcb7.pdf) 已覆盖有状态工具和显式 `mark as read` 等副作用，但未见“读取接口的消费语义是否被模型稳定执行”的配对诊断。
- [TVCACHE](https://arxiv.org/abs/2602.10986) 通过完整工具历史匹配保证缓存时环境状态一致，不解决单次观察本身消费资源。

## 潜在方法边界

只有普通文档下跨模型存在稳定“低成本消费型读偏好”，且不含推荐答案的效果标签能纠正，才值得在后续版本研究线性观察资源。否则 v066 直接否决。
