# CRL 默认科研循环（非权威建议）

本文只为同一个主 AI 研究者提供可选操作建议。`CRL.md` 是正式 Run 的唯一流程权威；本文不是固定阶段机、状态机、交付门槛或科研质量检查表。循环可在任何位置中断、回退、跳步或改序，未调用某个工具不能据此判定 Run 不合格。

一个通常有用的循环是：先明确产品领域与本轮方向边界，再建立计算对象或干预机制具有结构差异的假设组合；对每个 active 候选按需建立 Research Bundle，并进行实时最近先行对抗检索；随后把核心 Claim、可观察量、明确反证条件和 killer experiment 写清楚，优先运行能低成本否定最大不确定性的反证；根据真实证据由主研究者显式选择 kill、repair、split 或 escalate，再进入下一轮。

只有核心 Claim 已获得评价依据不与方法构造同源的独立支持后，才通常适合收口 Seed。工具输出、上下文视图、排序、相似度、覆盖度、状态字段和单个成功实验都不能替代这一科研判断；负面结果也只按其真实杀伤范围解释，不自动结束整个 Run。

当当前实现、候选或局部方法谱系被杀时，先 backtrack 到最近仍成立的证据，再重新扩张 research question / failure / operator 空间。对 AUTONOMOUS Run，局部盆地耗尽而 Charter 内仍有合理正交空间时，复用 `tools/manage_run.py advance-version --transition-file <JSON>` 开启下一科学搜索时期；文献层面的“可能还有别的路线”或“未发现路线”都不等于真实 re-expansion。主研究者经过真实 backtracking、正交 re-expansion 与必要高信息量检查后，可在继续投入预期科研价值不足时写 Run-level `NO_DELIVERY`；它只关闭本次 Run，不表示领域穷尽，也不能由活动数量或时长推出。

廉价 `SCREENING` 先排雷，仍有论文级 contribution delta 时再进入 `REPRESENTATIVE`、第二独立实现、明确结构性反证或真实资源 `escalated`。`evidence_fidelity` 与 `kill_target` 分轴记录：单次实现或本地代理模型负结果默认不关闭方法核或论文方向；最近先行杀死 Mechanism / Computation 后，仍需显式复查 Phenomenon / Evaluation / System Capability。机器只警告声明字段的高风险组合，不裁决解释。

当 prior collision 成为候选淘汰或终局判断的主要理由时，优先用现有 `tools/audit_prior.py` 保存 structured Prior Audit；它只增强可复查性，不是新颖性 Gate。固定 Reviewer 留到候选已具备明显生命力、强基线与真实 Formal 证据后使用；packet 优先紧凑摘要、代表性证据和 hash/path，原始大文件继续由 Evidence Inventory 指向。

`tools/render_research_context.py` 只把当前 Run、当前科学版本中的既有材料按来源与权威类别组成确定性只读视图。它默认写标准输出，不写回 Run、不冻结来源、不产生新科学内容，也不替代 `tools/manage_review.py render-input` 的同字节三审输入。
