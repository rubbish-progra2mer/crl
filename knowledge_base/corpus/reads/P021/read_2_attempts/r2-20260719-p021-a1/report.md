# P021 独立二读报告

## 1. 读取边界与方法

- 本报告对应 `r2-20260719-p021-a1/invocation.md`；只核读该 invocation、统一二读问题和其中指定的 45 页 PDF，未读取 read_1、Cards、其他报告或 blind query，未联网。
- [AUTHOR_FACT] PDF 正文与附录均已逐页检查；关键定位包括 §2–§4、Table 1–3、Figure 3 及附录训练/推理设置。
- [OPEN_QUESTION] 本次核读使用 PDF 文本层，没有逐页生成位图；未发现文本顺序或表格字段的明显断裂，但不能技术性排除复杂图形的视觉解析偏差。

## 2. 方法改变的计算

- [AUTHOR_FACT] AgentFlow 把轨迹计算拆成 Planner、Executor、Verifier、Generator，并维护随轮次更新的显式 memory；Planner 在每轮根据问题、知识和当前 memory 产生子目标、工具与上下文，后续模块执行、验证并更新状态（§2，物理页 3–5，“Planner / Executor / Verifier / Generator”附近）。
- [AUTHOR_FACT] 训练只更新 Planner，使用 Flow-GRPO；最终轨迹奖励广播给各轮，再在同一问题的采样组内归一化（§3，物理页 5–6，算法与 reward 定义）。
- [READER_INTERPRETATION] 真正 changed computation 不是“多加一次反思”，而是让策略学习决定每一步下一项子任务、工具和证据上下文；其余模块构成固定执行支架。

## 3. 输入、输出、干预时点

- [AUTHOR_FACT] 输入为问题 `q`、知识 `K` 和当前 memory `M_t`；Planner 输出阶段性目标及动作上下文，Executor 返回工具结果，Verifier 返回是否完成，Generator 输出最终回答（§2，物理页 3–5）。
- [AUTHOR_FACT] 训练奖励在完整轨迹结束后计算，训练时每题采样 8 条 rollout；训练最大 3 轮，评估最大 10 轮（§4 与附录设置，物理页 7、14–16）。
- [READER_INTERPRETATION] 干预发生在行动选择层，优势是能学习流程控制；代价是回报仍是轨迹级、轮级 credit 由广播近似，不是精确因果归因。

## 4. 基线、结果与归因边界

- [AUTHOR_FACT] Table 1–2 报告 AgentFlow 在多类 agent benchmark 上优于所列单体与 agent 系统；更接近的内部基线是同一四模块支架但不做 Flow-GRPO 的 frozen AgentFlow（物理页 7–9）。
- [AUTHOR_FACT] Table 3 中 frozen scaffold 平均 38.5，SFT 为 19.5，Flow-GRPO 为 55.7，GPT-4o Planner 为 44.3（物理页 9）。
- [AUTHOR_FACT] 轮次预算从训练时 3 轮扩展到评估时 10 轮会继续提高准确率（Figure 3，物理页 10）。
- [READER_INTERPRETATION] Table 3 支持“在该支架与奖励设置中，on-policy Planner 训练优于离线 SFT 和冻结 Planner”；不能把完整系统对较弱系统的优势全部归因于 Flow-GRPO。
- [READER_INTERPRETATION] 若比较对象没有相同 10 轮、工具和检索预算，轮数与工具机会是实质混杂因素。

## 5. Oracle、成本与公平性

- [AUTHOR_FACT] 实验使用 Qwen2.5-7B-Instruct 作为模块基础模型及五类工具；奖励包含 GPT-4o judge，检索工具还依赖 OpenAI embedding 和外部服务（§4、附录实现，物理页 7、14–18）。
- [READER_INTERPRETATION] 文中所谓最终奖励具有可判定接口，但其中 LLM judge 并非形式化可验证 oracle；外部模型/服务成本也不是只用本地 7B 推理的成本。
- [OPEN_QUESTION] 原文没有给出对所有基线严格等额的 token、tool-call、外部 API 成本核算，因此不能断言单位成本更优。

## 6. 负向结果与未测试边界

- [AUTHOR_FACT] SFT 相比冻结支架明显退化；作者将其联系到静态示范与交互策略学习不匹配（Table 3，物理页 9）。
- [AUTHOR_FACT] 错误案例包括错误工具选择、过早终止和检索证据不足；附录给出模块 prompts、解析规则和轨迹示例（物理页 20–45）。
- [READER_INTERPRETATION] 可记录的 Failure 是：把离线步骤示范直接拟合成多轮控制策略可能使已有支架能力坍塌；扩大行动预算也可能制造表面提升而非策略本身改善。
- [OPEN_QUESTION] 未隔离“轨迹奖励广播”相对更精细 credit assignment 的独立贡献，也未证明结果能迁移到不同工具集或不同 Planner/Executor 模型组合。

## 7. 可抽取资产

- [READER_INTERPRETATION] Operator 候选：`Outcome-trained planner over explicit execution state`——固定执行/验证模块，仅训练每轮决定子目标、工具和证据上下文的 Planner。
- [READER_INTERPRETATION] Failure 候选：`Offline imitation collapse in interactive planning`；`Extra-turn budget masquerading as policy gain`。
- [READER_INTERPRETATION] 窄 Claim：在论文给定的四模块支架、任务、工具和 outcome reward 下，Flow-GRPO Planner 比冻结 Planner 与其 SFT 版本表现更好。
- [READER_INTERPRETATION] 不支持：广播最终奖励一般性解决长程 credit assignment；该方法在系统总成本上优于所有 agent 基线；完整增益完全来自 Planner RL。

## 8. 独立二读建议

`ACCEPT_WITH_NARROWING`。机制与关键消融清楚，适合作为 planning/agent learning Operator 来源；正式吸收时必须保留轮次预算、外部 judge/embedding 和 scaffold 贡献边界。本建议仅供主 Codex reconciliation。
