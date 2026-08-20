# P047 独立二读报告

## 来源与读取声明

- 冻结调用快照：`knowledge_base/corpus/reads/P047/read_2_attempts/r2-20260719-p047-a1/invocation.md`
- 论文：*tau2-Bench: Evaluating Conversational Agents in a Dual-Control Environment*
- PDF SHA-256：`0817e3fd33915326180d548caa900dcc5cba42ded27688105d8ce2f7e73aad84`
- [AUTHOR_FACT] 已逐页读取全部 47 个物理页，包括政策、工作流图与用户模拟器附录。

## 1. 改变的评测计算与环境 I/O

- [AUTHOR_FACT] tau2-Bench 将对话工具任务形式化为 agent 与 user simulator 都能通过工具改变共享世界的双控制 Dec-POMDP；新增 telecom 域，用户可在自己的设备上执行诊断/修复动作，服务代理操作账户/账单等。（物理页 2–5，Benchmark design）
- [AUTHOR_FACT] telecom 从 2,285 个程序化任务中抽样 114 个，覆盖 15 个 atomic subtask groups、3 类 intent；成功由环境断言判定，而不是 LLM judge。（物理页 4–6，Task generation/evaluation）
- [READER_INTERPRETATION] changed computation 主要是**把一部分控制权和私有观察放到模拟用户侧**，迫使代理通过对话协调；它不是一个新的代理算法。

## 2. 基线、oracle 消融与主要结果

- [AUTHOR_FACT] agent 包括 GPT-4.1-mini、GPT-4.1、o4-mini、Claude 3.7，user simulator 为 GPT-4.1，temperature 0；每题 4 次运行。文中估算 GPT-4.1 agent/user 每题约 0.086/0.059 美元，一次三域 trial 约 40 美元。（物理页 5–7，Experimental setup）
- [AUTHOR_FACT] telecom pass^1 大致为 GPT-4.1 .34、o4-mini .42、Claude 3.7 .49；主要比较不是单一“最强基线”，而是同模型在 Default、No-User、Oracle-Plan 与不同政策表述下的差异。（物理页 6–8，主图/表）
- [AUTHOR_FACT] 原政策下 GPT-4.1 的 Default/No-User/Oracle-Plan 约 .34/.52/.73，o4-mini 约 .42/.67/.96；workflow policy 下相应约 .52/.68/.57 与 .59/.72/.88。（物理页 7–8，ablation table）
- [AUTHOR_FACT] Oracle-Plan 直接提供 ground-truth action sequence；No-User 把用户工具移给代理并相应重写政策/任务信息。（物理页 7–8，Ablations；附录物理页 38）
- [READER_INTERPRETATION] Oracle-Plan 是明确 oracle 上界。No-User 同时改变控制接口、信息供给与部分政策措辞，不能作为“只去除沟通成本”的纯因果消融；Default→No-User 的 18/25 个点只能作为通信/分布式控制负担的组合证据。

## 3. 负向结果与模拟器质量

- [AUTHOR_FACT] 长轨迹失败明显：Default 超过约 7 个动作后成功率接近零；No-User 虽改善但仍随 horizon 增长下降。（物理页 8–9，Length analysis）
- [AUTHOR_FACT] workflow policy 在 Default/No-User 多数提高表现，却在 Oracle-Plan 中可下降，作者解释为计划与政策表达冲突。（物理页 7–9）
- [AUTHOR_FACT] 用户模拟器人工检查发现 airline 100 段中 47 个错误（13 个任务关键）、retail 50 段中 20 个错误（6 个任务关键）、telecom 50 段中 8 个错误（3 个任务关键）。telecom 的 8 个错误全部为模拟器在代理真正 transfer 前提前输出 `###TRANSFER###`。（物理页 10–11；附录物理页 43、47）
- [READER_INTERPRETATION] 成功率混入用户模拟器故障，尤其提前终止会把本可完成的代理轨迹判失败；文中未报告标注者一致性统计，误差估计还需保守使用。

## 4. 限制、Operator 与 Failure

- [AUTHOR_FACT] 作者明示限制：没有把用户工具机制扩展到 airline/retail；扩域需要大量人类专家工作；尚未显式建模 expert–novice 能力差。（物理页 11，Limitations）
- [OPEN_QUESTION] 用户模拟器质量标注未报告 inter-rater agreement，且双控制只在 telecom 实现；因此无法判断相同误差率和 Default→No-User 差异能否迁移到 airline/retail。
- [READER_INTERPRETATION] Operator 候选：以共享世界状态、双方工具、环境断言构建双控制会话评测；用 Default/No-User/Oracle-Plan 分别给出部署难度、集中控制参考和 oracle 上界，但不能混为因果消融。
- [READER_INTERPRETATION] Failure 候选：控制权分散与信息不对称造成通信瓶颈；长 horizon 失败；显式 workflow 与 oracle plan 冲突；user simulator 提前停止或遗漏约束。
- [READER_INTERPRETATION] 建议保留为双控制评测基础；任何“用户协作导致 X 点损失”结论均需注明 No-User 同时改接口/信息，且主结果含模拟用户错误。

## 5. 可视核验

- [AUTHOR_FACT] 已核对主结果表/图以及物理页 44–46 的三个 troubleshooting workflow 图；可视结构与附录政策文本一致，未见实质冲突。
