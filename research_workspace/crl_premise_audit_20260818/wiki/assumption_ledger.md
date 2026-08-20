# 假设账本

## A-001：前沿模型全面等同合格研究生

- run_id: `CRL-PREMISE-AUDIT-001`
- run_ref_type: `explicit_run_id`
- assumption_id: `A-001`
- assumption: 当前前沿大语言模型在开放式、长期、低结构化科研中能够持续达到合格研究生的综合水平。
- source: 用户给出的 CRL 大前提的强解释。
- used_by: CRL 是否可被视为无需外部校准的自主主研究者。
- risk: 若错误，无限时间和资源不会自动转化为有效科研，反而可能放大漂移和自证循环。
- how_to_verify: 使用开放式科研、论文复现、长时研究工程和前瞻性候选执行结果与研究生/专家直接对照。
- status: `contradicted`
- related evidence: RE-Bench、PaperBench、MLR-Bench、GPT-5.6 Preview System Card；这些证据显示能力强但锯齿化，长时与开放式任务仍有明显差距。
- last_updated: `2026-08-18`

## A-002：有边界科研子任务达到研究生级实用能力

- run_id: `CRL-PREMISE-AUDIT-001`
- run_ref_type: `explicit_run_id`
- assumption_id: `A-002`
- assumption: 当前前沿模型在明确任务、工具、可执行反馈和检查点下，能在部分文献检索、编码、优化和实验迭代任务上达到或超过研究生/专家的实用水平。
- source: 外部基准和真实系统实验。
- used_by: 判断 CRL 是否拥有可利用的能力基础。
- risk: 若错误，CRL 只能生成语言材料，无法提供真实去风险价值。
- how_to_verify: 复核直接人类基线、隐藏测试和可执行证据，而非模型自评。
- status: `supported`
- related evidence: RE-Bench、PaperQA2、Co-Scientist、Empirical Research Assistance、当前 GPT-5.6 研究工程评估。
- last_updated: `2026-08-18`

## A-003：无限时间与自我迭代单调提高候选质量

- run_id: `CRL-PREMISE-AUDIT-001`
- run_ref_type: `explicit_run_id`
- assumption_id: `A-003`
- assumption: 在没有更强外部判据的情况下，增加模型运行时间、迭代次数和候选数量会单调提高最佳候选的真实科研价值。
- source: “不限制时间和额度、不断自我迭代”的朴素推断。
- used_by: CRL 长周期自主运行的价值解释。
- risk: 若错误，长运行可能只是重复、奖励投机、模式坍缩或上下文漂移。
- how_to_verify: 对固定任务绘制外部盲评/真实执行质量随迭代和成本的曲线，并与多次独立短运行比较。
- status: `contradicted`
- related evidence: RE-Bench 显示人类随时间收益更高；执行反馈研究显示前沿模型常早期饱和，强化学习出现模式坍缩；Co-Scientist 的正向时间曲线主要依赖系统内部 Elo，外部专家样本较小。
- last_updated: `2026-08-18`

## A-004：共享知识库足以支撑可靠的先行工作定位

- run_id: `CRL-PREMISE-AUDIT-001`
- run_ref_type: `explicit_run_id`
- assumption_id: `A-004`
- assumption: CRL 当前知识库的覆盖、证据粒度和检索策略足以发现最危险的最近先行，避免把已知工作误判为新机会。
- source: 用户对本地知识库信息充足性的预期。
- used_by: 新颖性审计和候选淘汰的可信度。
- risk: 若错误，系统会稳定地产生“库内新颖、现实已占据”的候选。
- how_to_verify: 在时间截断基准和已知最近先行集合上测量召回率、证据定位正确率与 Top-k 漏检率。
- status: `unverified`
- related evidence: PaperQA2 在受控文献任务上很强，但 AutoResearchBench 在开放式复杂文献发现上报告约 9% 的表现，说明能力高度依赖任务与检索设计。
- last_updated: `2026-08-18`

## A-005：本地小实验可预测大规模研究价值

- run_id: `CRL-PREMISE-AUDIT-001`
- run_ref_type: `explicit_run_id`
- assumption_id: `A-005`
- assumption: 在 CRL 涉及的多数候选类型上，本地低保真实验能保持候选在目标规模上的相对排序，或至少可靠识别值得继续投入者。
- source: 用户将 CRL 定位为用本地小实验验证候选构思“分数”。
- used_by: Delivery 是否值得用户投入大规模资源。
- risk: 若错误，CRL 会系统性杀死只在规模上成立的候选，或晋升只在代理环境有效的候选。
- how_to_verify: 对历史和未来候选成对记录本地代理结果与后续高保真结果，估计秩相关、阳性预测值、假阴性率，并按贡献类型分层。
- status: `unverified`
- related evidence: 小规模数据配方研究显示结论可因轻微超参数变化翻转；经目标对齐和专门校准后又可显著提高跨尺度相关，说明代理有效性必须逐类校准，不能默认成立。
- last_updated: `2026-08-18`

## A-006：固定评审分数代表用户的后续投入价值

- run_id: `CRL-PREMISE-AUDIT-001`
- run_ref_type: `explicit_run_id`
- assumption_id: `A-006`
- assumption: CRL 固定三评审器及其材料能够可靠排序候选的真实后续研究价值，而不只是语言完整度、局部实验真实性或评审模型偏好。
- source: CRL Delivery 评审仪器设计。
- used_by: 最终交付候选的选择和质量解释。
- risk: 若错误，机器会优化评审器可见特征而非真实研究价值。
- how_to_verify: 将盲评分数与后续独立复现、扩大实验、外部专家投入意愿和最终项目结果做前瞻相关分析。
- status: `unverified`
- related evidence: 构思阶段评价曾高估大模型构思，执行后发生排序反转；MLR-Bench 也发现语言输出与实验可靠性脱节。
- last_updated: `2026-08-18`

## A-007：执行真实性约束能显著降低伪科研

- run_id: `CRL-PREMISE-AUDIT-001`
- run_ref_type: `explicit_run_id`
- assumption_id: `A-007`
- assumption: 将主张绑定到真实运行日志、独立评价通道、实现哈希和失败记录，能显著降低虚构结果进入最终交付的概率。
- source: CRL Contract v3 设计与外部失败证据。
- used_by: 判断 CRL 相对于只生成完整论文的系统是否具有结构优势。
- risk: 若错误，复杂的完整性机制只增加摩擦而不能提高科研可靠性。
- how_to_verify: 对比启用和禁用真实性绑定的代理，在隐藏缺陷、执行失败和伪造结果测试上的进入终局率。
- status: `supported`
- related evidence: MLR-Bench 报告约 80% 实验案例存在虚构或无效结果，并显示检查代码与执行日志能发现问题；PaperBench 使用作者共同制定的细粒度量规和可执行复现评分。
- last_updated: `2026-08-18`

## A-008：Run 13 证明 CRL 机器不完善

- run_id: `legacy-unknown`
- run_ref_type: `legacy_unknown`
- assumption_id: `A-008`
- assumption: Run 13 的无响应和候选质量停滞主要由 CRL 机器缺陷造成，而不是当前模型能力、任务不可评分、外部服务、执行环境或科学盆地本身造成。
- source: 用户基于历史表现提出的怀疑；本阶段尚未读取 Run 13。
- used_by: 是否应修改 CRL 机器。
- risk: 误归因会导致修改协议却无法改善科研产出，甚至掩盖模型或评估边界。
- how_to_verify: 在完成外部前提审计后，对 Run 13 做事实型事件时间线、工具/模型响应、候选差分和高信息量实验轨迹诊断。
- status: `unverified`
- related evidence: 当前只有用户描述；不得视作已经定位原因。
- last_updated: `2026-08-18`

## A-009：CRL 相对强基线具有增量价值

- run_id: `CRL-PREMISE-AUDIT-001`
- run_ref_type: `explicit_run_id`
- assumption_id: `A-009`
- assumption: 在同等模型、知识、工具和费用下，CRL 长期闭环比一次性深度研究、多次独立短运行或人类提供方向后的执行代理，能产生更多真正值得继续投入的候选。
- source: CRL 的产品级价值主张。
- used_by: 是否值得继续完善 CRL。
- risk: 若错误，复杂机器只是增加等待时间和文档产物，没有提高候选质量。
- how_to_verify: 预注册对照评测，比较 Top-k 候选后续存活率、最近先行碰撞率、扩大实验成功率、成本和响应可靠性。
- status: `unverified`
- related evidence: Co-Scientist 与执行引导搜索支持结构化闭环可能有增益，但没有直接评估当前 CRL。
- last_updated: `2026-08-18`
