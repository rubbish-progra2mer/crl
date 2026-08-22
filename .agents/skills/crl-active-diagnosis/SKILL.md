---
name: crl-active-diagnosis
description: 在 Contract v3 CRL Run 的长周期科研中，当大量阅读、想法趋同、实验连续失败、候选收敛、成对偏好连续不变、准备固定评审或中断后恢复使当前轨迹难以判断时使用；按需收集 Run 内 facts-only 诊断并交回主 AI 研究者解释，不创建状态机或科研 Gate。
---

# CRL Active Diagnosis

## 何时触发

仅在已绑定可写 Contract v3 Run，且事实全景比继续读取单一文件更有信息量时考虑调用，例如：

- 大量阅读或检索后，需要检查证据、候选、实现和实验是否脱节；
- 想法持续趋同，或失败、冲突结果反复出现；
- 准备收敛候选、形成 Review packet，或长时间中断后恢复；
- 主研究者对 current-version 与 Run-wide 的权威事实没有把握。
- facts-only 事实已显示模式版本 2 的尾部连续 5 个候选在没有绑定实验规格、Recorded 或 Formal 的情况下关闭；这是必须诊断并改写策略的研究者触发条件，不是脚本 Gate。
- 最近三项由主研究者用 `PREFERENCE_UPDATE` 声明的高信息量动作可能既未改变 Pairwise Verdict，也未减少致命不确定性，需要核对是否形成 `PREFERENCE_STAGNATION_WARNING`。

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
- 阅读当前 selection context 六项模板，以及其中可恢复的 `INCUMBENT_SET`、`CHALLENGERS`、`A_PREFERRED`、`B_PREFERRED`、`INCOMPARABLE`、`INSUFFICIENT_EVIDENCE` 四值成对 Verdict、决定性证据、反转条件、仍存致命不确定性、区分动作、候选准入合同、局部奖励合同、开发/准入证据声明、实现工件、`DECLARED_SESSION` 自报标识、显式实现彩票例外和 `PREFERENCE_UPDATE`。重复结构字段必须保留出现次数；完全相同重复也看作 advisory，冲突块按 `AMBIGUOUS`/`UNKNOWN` 处理且不得用于停滞结论。全部成对比较按无序候选对归一化，反向 Pair 的 A/B 标签按实际候选身份解释；同对冲突 Verdict 整组为 `AMBIGUOUS` 且没有机械胜者，相同实际 Verdict 的重复块保留并发 advisory。冲突的 `INCUMBENT_SET`/`CHALLENGERS` 不得合并，同次声明混写空标记与候选标识时不得保留候选列表。旧格式或缺失字段显示 `UNAVAILABLE`/`UNKNOWN` 时不得补猜。
- 对 `DECISIVE_EVIDENCE`、`EVIDENCE_PATHS`、`DEVELOPMENT_EVIDENCE`、`ADMISSION_EVIDENCE` 中疑似 Run-local 路径核对边界、存在性和普通文件身份；普通 DOI、arXiv 与明确文献事实保持 declared text。只有 Pair、Verdict、决定性证据、仍存致命不确定性、反转条件和区分动作均可解析且决定性证据没有 `UNVERIFIED` 路径时，Preferred 才有机械可用胜者；否则 declared Verdict 仍保留，但比较为 `UNKNOWN` 且胜者为空。含 `UNVERIFIED EVIDENCE_PATHS` 的更新为 `UNKNOWN`、不可用于停滞；同一动作和归一化受影响 Pair 的冲突重复更新整组为 `AMBIGUOUS`。实现工件、冻结 Candidate Card 和忠实度文件的 `VERIFIED_ARTIFACT` 与 SHA-256 只证明文件和字节身份；相同字节工件只计一次，不同路径、不同哈希或 `DECLARED_SESSION` 都不自动证明真实会话隔离或科学独立性。
- 同时阅读逐候选实验绑定、尾部连续实验前关闭、尾部 `prior_collision` 实验前关闭，以及最近结构化候选、Recorded、Formal、Prior Audit 的原始版本事实。后四项距离不是科研质量指标；模式版本 1 或绑定不可恢复时接受 `UNKNOWN`，不得补猜。
- 将单一实现支撑想法级偏好或死亡、同一工件重复冒充独立实现、以及有本地实验活动却缺少局部奖励合同视为 advisory 风险；不得据此由脚本撤销比较、关闭 Hypothesis 或形成终局。机械唯一实现或结构性反证例外必须有可核验理由与路径。
- Diagnosis 只整理可追溯事实，是 `ADVISORY_NON_AUTHORITATIVE`；它不解释科学含义，不自动选择、淘汰、转向、推进版本、结束 Run，也不认证 Novelty、实验充分性或交付资格。
- 将事实与来源路径交回当前主 AI 研究者，由其按照 `crl_agent_v3/CRL.md` 的唯一完整科研语义解释杀伤范围、候选生命力、下一高信息量行动和是否继续研究。
- 不读取其他 Run，不把诊断材料写入共享论文知识库，不新增计数器、后台轮询、定时任务、状态迁移、质量评分或强制阶段。

## 诊断后的研究者响应

Diagnosis 交回后，主研究者必须继续承担科学解释，不得只保存报告：

1. 阅读 facts-only 报告及其明确引用的 Run 内路径；
2. 在当前版本更新 `selection_context_vNNN.md` 的“当前最佳候选集合、新增正向证据、已失效或被杀范围、剩余致命不确定性、下一项最高信息量动作、策略变化”六项短模板；在第一项保留 Incumbent 与 Challenger，按 `A_PREFERRED`、`B_PREFERRED`、`INCOMPARABLE`、`INSUFFICIENT_EVIDENCE` 写成对证据、反转条件和区分动作；固定 Review 已锁定该文件时不覆盖，按 `CRL.md` 处理版本边界；
3. 分开判断候选投资成熟度与科研信息增益，不能把候选被杀带来的信息增益写成候选质量提高；
4. 检查已进入实现或实验迭代的活动候选是否具有局部奖励合同，开发证据与准入证据是否分离，想法级经验判断是否有同一冻结 Candidate Card 下由主研究者实际隔离完成的两份实现、盲忠实度检查或明确例外；把 `DECLARED_SESSION` 与不同 `VERIFIED_ARTIFACT` 当作可审计线索而非独立性认证。局部奖励不得决定新颖性、终局或 Delivery；
5. 明确停止重复什么动作，尤其不得继续相同的 method-first 文献碰撞循环；
6. 选择一个直接处理剩余致命不确定性的不同高信息量动作后继续研究：回溯、正交扩展、现象优先、改变贡献形态，或执行长期推迟的高信息量实验。

尾部连续实验前关闭达到 5 个时，上述响应必须立即发生，但不自动暂停、结束 Run 或形成 No-Delivery。停滞只按每个 `ACTION_ID` 的最后出现位置选最近三个不同动作，同一动作的多个 pair update 仍只计一个动作；含冲突字段、同一动作/同一归一化 Pair 的冲突重复结果或 `UNVERIFIED EVIDENCE_PATHS` 的更新使判断为 `UNKNOWN`，不得用自报 Verdict 变化伪造进展或误报停滞。只有三个可解释动作均未改变四值偏好且未减少致命不确定性时才输出 `PREFERENCE_STAGNATION_WARNING`。若报告出现该警告，主研究者必须更新 selection context，写明 `STOP_REPEATING`，扩大至少一个真实科研坐标并声明新的区分动作；Run 保持 `ACTIVE`。最佳候选集合可为空或包含任意数量不可比或并列项；候选退出集合只能由主研究者根据新增证据说明实际死亡范围。Diagnosis 不得自动推进版本、切换候选、暂停、终止或形成 No-Delivery。
