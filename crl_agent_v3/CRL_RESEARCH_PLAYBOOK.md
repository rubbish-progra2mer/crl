# CRL 默认科研循环（非权威建议）

本文只为同一个主 AI 研究者提供可选操作建议。`CRL.md` 是正式 Run 的唯一流程权威；本文不是固定阶段机、状态机、交付门槛或科研质量检查表。循环可在任何位置中断、回退、跳步或改序，未调用某个工具不能据此判定 Run 不合格。

一个通常有用、但可随时回退、跳步、分叉和重构的候选循环是：

```text
保留 Incumbent
→ 生成具有明确父候选与 changed computation 的 Challenger
→ 建立局部奖励合同
→ 写成对偏好与反转条件
→ 执行最可能改变偏好结论的动作
→ 更新证据与致命不确定性
→ 使用独立证据决定提升、并列、修订或退出
→ 停滞时扩大科研坐标
```

`INCUMBENT_SET` 与 `CHALLENGERS` 只是当前活动注意力，完整历史候选档案继续原位保留且不设数量上限。成对比较只使用 `A_PREFERRED`、`B_PREFERRED`、`INCOMPARABLE`、`INSUFFICIENT_EVIDENCE` 四值；不可比时保留二者，证据不足时执行能区分它们的动作。局部奖励只排序同一候选内部的实现变异与实验，不汇总成 idea 分数，也不裁决新颖性、终局或 Delivery。

开发证据可用于发现和修订，Challenger 替换 Incumbent 则需要未直接参与本次修订设计的准入检查；完全相同的开发样本反复运行不是独立准入。经验实现用于想法级偏好或死亡时，通常由主研究者依据同一冻结 Candidate Card 实际隔离完成至少两个实现并盲查实现忠实度；同字节工件只计一次。`FRESH_SESSION_ID` 只提供 `DECLARED_SESSION` 自报线索，文件边界与 SHA-256 核验只提供 `VERIFIED_ARTIFACT` 字节事实，脚本不能据此认证真实会话隔离或科学独立性。机械唯一实现或可核验结构反例须显式留下理由与证据路径。以上都不是固定阶段机、候选数量 Gate 或自动裁决，主研究者始终承担科学解释。

开始候选循环前仍应明确产品领域与本轮方向边界，并按需建立结构有差异的假设组合、Research Bundle 与实时最近先行对抗检索；把核心 Claim、可观察量、明确反证条件和 killer experiment 写清楚，优先运行能低成本否定最大不确定性的反证。根据真实证据由主研究者显式选择 kill、repair、split 或 escalate，再进入下一轮。

只有核心 Claim 已获得评价依据不与方法构造同源的独立支持后，才通常适合收口 Seed。工具输出、上下文视图、排序、相似度、覆盖度、状态字段和单个成功实验都不能替代这一科研判断；负面结果也只按其真实杀伤范围解释，不自动结束整个 Run。

当当前实现、候选或局部方法谱系被杀时，先 backtrack 到最近仍成立的证据，再重新扩张 research question / failure / operator 空间。对 AUTONOMOUS Run，暂未找到合格方向、候选耗尽、局部盆地失败、运行较久或多次验证无效都不形成科学终局；只要授权仍有效且不存在不可越过的真实外部边界，就保持 `ACTIVE`，按需复用 `tools/manage_run.py advance-version --transition-file <JSON>` 开启下一科学搜索时期，继续换题、正交扩展和验证。文献层面的“可能还有别的路线”或“未发现路线”都不等于真实 re-expansion；即使已经真实 backtracking、正交 re-expansion 与执行必要高信息量检查，AUTONOMOUS Run 也不得写 Run-level `NO_DELIVERY`。只有用户明确窄方向创建的 `DIRECTED` Run 才可在该 Charter 内形成 No-Delivery。

廉价 `SCREENING` 先排雷，仍有论文级 contribution delta 时再进入 `REPRESENTATIVE`、第二独立实现、明确结构性反证或真实资源 `escalated`。`evidence_fidelity` 与 `kill_target` 分轴记录：单次实现或本地代理模型负结果默认不关闭方法核或论文方向；最近先行杀死 Mechanism / Computation 后，仍需显式复查 Phenomenon / Evaluation / System Capability。机器只警告声明字段的高风险组合，不裁决解释。

当 prior collision 成为候选淘汰或终局判断的主要理由时，优先用现有 `tools/audit_prior.py` 保存 structured Prior Audit；它只增强可复查性，不是新颖性 Gate。固定 Reviewer 留到候选已具备明显生命力、强基线与真实 Formal 证据后使用；packet 优先紧凑摘要、代表性证据和 hash/path，原始大文件继续由 Evidence Inventory 指向。

`tools/render_research_context.py` 只把当前 Run、当前科学版本中的既有材料按来源与权威类别组成确定性只读视图。它默认写标准输出，不写回 Run、不冻结来源、不产生新科学内容，也不替代 `tools/manage_review.py render-input` 的同字节三审输入。

Active Diagnosis 按每个 `ACTION_ID` 的最后出现位置选择最近三个不同的 `PREFERENCE_UPDATE` 高信息量动作，同一动作的多组成对更新只计一个动作；冲突块为 `AMBIGUOUS`/`UNKNOWN`，不得参与停滞结论。只有最近三个可解释动作既未改变四值 Pairwise Verdict，也未减少致命不确定性时才给出 `PREFERENCE_STAGNATION_WARNING`。主研究者应更新六项 selection context，写明 `STOP_REPEATING`，扩大至少一个真实科研坐标并改用新的区分动作；Run 保持 `ACTIVE`。该建议不自动推进版本、切换候选、暂停、终止或形成 No-Delivery。
