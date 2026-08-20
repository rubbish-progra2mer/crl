---
name: crl-active-diagnosis
description: 在 Contract v3 CRL Run 的长周期科研中，当大量阅读、想法趋同、实验连续失败、候选收敛、准备固定评审或中断后恢复使当前轨迹难以判断时使用；按需收集 Run 内 facts-only 诊断并交回主 AI 研究者解释，不创建状态机或科研 Gate。
---

# CRL Active Diagnosis

## 何时触发

仅在已绑定可写 Contract v3 Run，且事实全景比继续读取单一文件更有信息量时考虑调用，例如：

- 大量阅读或检索后，需要检查证据、候选、实现和实验是否脱节；
- 想法持续趋同，或失败、冲突结果反复出现；
- 准备收敛候选、形成 Review packet，或长时间中断后恢复；
- 主研究者对 current-version 与 Run-wide 的权威事实没有把握。
- facts-only 事实已显示模式版本 2 的尾部连续 5 个候选在没有绑定实验规格、Recorded 或 Formal 的情况下关闭；这是必须诊断并改写策略的研究者触发条件，不是脚本 Gate。

不要定时运行，也不要因为出现一次失败就机械触发。若单一文件或一次窄检查足以回答当前问题，继续研究即可。

## 调用

先确认产品根、Run 根、科学版本及 `CRL_CONTRACT_VERSION: 3`，不得对 v2 历史 Run 写入。默认先刷新一次 FTS-only Recall，再收集并查看诊断：

```powershell
python tools\crl.py recall --product-root D:\Desktop\crl --run-root <RUN_ROOT> --version <vNNN> rebuild
python tools\crl.py diagnose --product-root D:\Desktop\crl --run-root <RUN_ROOT> --version <vNNN> collect --diagnosis-id <diagnosis-id>
python tools\crl.py diagnose --product-root D:\Desktop\crl --run-root <RUN_ROOT> --version <vNNN> show --diagnosis-id <diagnosis-id>
```

不默认构建 semantic Recall。若 FTS rebuild 失败，如实记录错误后仍可 collect；确认 `recall_status.status` 为 `UNAVAILABLE` 并保留结构化原因。FTS 可用而 semantic 未请求或降级时，FTS 仍为 `READY`，semantic 状态单独披露。

## Facts-only 边界与交回

- 同时阅读 `current_version` 与 `run_wide`，机械区分 Scratch、Recorded、Formal/Review-support，并留意事实包显式报告的缺失、降级、陈旧或解释层 warning。
- 阅读当前 selection context 六项模板、逐候选实验绑定、尾部连续实验前关闭、尾部 `prior_collision` 实验前关闭，以及最近结构化候选、Recorded、Formal、Prior Audit 的原始版本事实。后四项距离不是科研质量指标；模式版本 1 或绑定不可恢复时接受 `UNKNOWN`，不得补猜。
- Diagnosis 只整理可追溯事实，是 `ADVISORY_NON_AUTHORITATIVE`；它不解释科学含义，不自动选择、淘汰、转向、推进版本、结束 Run，也不认证 Novelty、实验充分性或交付资格。
- 将事实与来源路径交回当前主 AI 研究者，由其按照 `crl_agent_v3/CRL.md` 的唯一完整科研语义解释杀伤范围、候选生命力、下一高信息量行动和是否继续研究。
- 不读取其他 Run，不把诊断材料写入共享论文知识库，不新增计数器、后台轮询、定时任务、状态迁移、质量评分或强制阶段。

## 诊断后的研究者响应

Diagnosis 交回后，主研究者必须继续承担科学解释，不得只保存报告：

1. 阅读 facts-only 报告及其明确引用的 Run 内路径；
2. 在当前版本更新 `selection_context_vNNN.md` 的“当前最佳候选集合、新增正向证据、已失效或被杀范围、剩余致命不确定性、下一项最高信息量动作、策略变化”六项短模板；固定 Review 已锁定该文件时不覆盖，按 `CRL.md` 处理版本边界；
3. 分开判断候选投资成熟度与科研信息增益，不能把候选被杀带来的信息增益写成候选质量提高；
4. 明确停止重复什么动作，尤其不得继续相同的 method-first 文献碰撞循环；
5. 选择一个直接处理剩余致命不确定性的不同高信息量动作后继续研究：回溯、正交扩展、现象优先、改变贡献形态，或执行长期推迟的高信息量实验。

尾部连续实验前关闭达到 5 个时，上述响应必须立即发生，但不自动暂停、结束 Run 或形成 No-Delivery。最佳候选集合可为空或包含任意数量并列项；候选退出集合只能由主研究者根据新增证据说明实际死亡范围。
