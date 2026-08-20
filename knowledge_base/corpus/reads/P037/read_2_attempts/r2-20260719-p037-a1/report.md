# P037 独立二读报告

- Attempt：`r2-20260719-p037-a1`
- PDF SHA-256：`3449baed1d8e0f4c07dbc859621899685eed8a6a0445a1ae8909c178e6b6173e`
- 阅读范围：物理页 1–24，逐页全文
- 二读结论：`ACCEPT_WITH_NARROWING`

## 1. 方法与被改变的计算

- [AUTHOR_FACT] ToolSandbox 提供有状态 Python 工具、LLM 用户模拟器、在线多轮交互，以及用 Milestone/Minefield DAG 匹配任意轨迹的动态评价。（物理页 1–5，摘要/§2，定位词 “stateful”“Milestones”“Minefields”）
- [AUTHOR_FACT] 1,032 个场景由两名内部领域专家构造和互审，覆盖 34 个工具；一个人创建场景与里程碑，另一个以 agent 身份验证，随后至少做四轮多模型测试。（物理页 5、17–19，§3/§B2）
- [READER_INTERPRETATION] 主要计算创新在评测：把单一最终答案匹配改为按拓扑顺序寻找轨迹快照与必需/禁止事件的最佳映射；不是提出 agent 的执行恢复算法。

## 2. 输入、输出和评价边界

- [AUTHOR_FACT] world state 和 message bus 保存在 Execution Context；LLM 不能直接修改状态，只能通过工具；异常会作为 stderr 返回，使轨迹可继续。（物理页 3、13–16，§2.1/§A1–A6）
- [AUTHOR_FACT] Milestone 相似度可组合数据库 exact match、ROUGE-L、AST tool-call match，并用几何平均；Minefield 一旦非零匹配，会把总分乘为零。（物理页 4–5、16，§2.3/公式 1–2）
- [READER_INTERPRETATION] 该评价允许多条合法路径和中间部分完成，比固定动作序列更能诊断“在哪里失败”；但人工 milestone 本身构成对正确过程的强先验。

## 3. 基线、结果与混杂

- [AUTHOR_FACT] 所有模型使用同一极简 agent prompt；Claude 与 Llama 等模型的接口能力并不完全相同，部分开源模型无法消费工具返回。（物理页 6–8、15、23，表 5/表 10）
- [AUTHOR_FACT] GPT-4o 总平均相似度 73.0，Claude-3-Opus 69.2；最强开源 Hermes-2-Pro-Mistral-7B 为 31.4。（物理页 7，表 5）
- [AUTHOR_FACT] ReAct 提示对四个代表模型只带来很小变化，例如 GPT-4o 73.0→73.6、Claude Opus 69.2→69.3。（物理页 22，表 9）
- [AUTHOR_FACT] 状态依赖类别中 GPT-3.5/Claude Sonnet 可高于部分更大模型，作者归因于更大模型错误并行调用有依赖的工具；执行环境会刻意让检测到的竞态发生。（物理页 7、16、21，State Dependency/图 17）
- [READER_INTERPRETATION] 模型间比较混合了原生 function-calling 支持与模型推理能力；无法消费 tool response 的模型不应被视为纯能力基线。

## 4. 用户模拟、负向证据与限制

- [AUTHOR_FACT] 用户模拟器为 GPT-4o；加入 Knowledge Boundary 与 Demonstration 后，人工标注的 hallucination 为 6.97%、instruction-following error 为 0.77%，总错误约 8%，且跨被测 agent 相近。（物理页 4，表 2–3）
- [READER_INTERPRETATION] 错误率跨 agent 相近有助于相对比较，但约 8% 的模拟器错误仍会污染绝对分数；few-shot demonstration 和部分 expected result 是给模拟器的 oracle 信息，不会直接泄漏给 agent。
- [AUTHOR_FACT] Insufficient Information 得分与其他能力大体负相关，弱模型因“不调用任何工具”反而可能得高分；作者明确称这是副作用，不是积极结果。（物理页 7–8，Insufficient Information）
- [AUTHOR_FACT] 作者限制包括 milestone/minefield 人工成本高、模拟器仍有非忽略错误、未覆盖强制确认/认证和 daemon 工具，少数外部 API 影响复现。（物理页 10，Limitations）
- [OPEN_QUESTION] 人工 milestone 的覆盖度和严格度是否在不同工具域同质，原文只给计数与验证流程，没有系统的遗漏率估计。

## 5. 可抽取内容与范围排除

- [READER_INTERPRETATION] Operator 候选仅限评测层：`用必需事件 DAG + 禁止事件 minefield 对动态轨迹做多路径、过程级评分`；它不是候选 research implement 的自动评分器。
- [READER_INTERPRETATION] Failure 候选：`最终成功分数遮蔽中间状态错误`；`强模型对有依赖工具错误并行`；`缺信息任务中模型幻觉工具/参数`；`弱模型因不行动获得虚高安全分`。
- [READER_INTERPRETATION] 按当前 CRL 范围，环境故障恢复、ConnectionError 回退、低电量/Wi-Fi 依赖等仅作为 benchmark 场景与失败证据记录，明确不把“环境反馈学习与执行恢复”升级为研究方向或 Operator 候选。
- [READER_INTERPRETATION] 窄 Claim：ToolSandbox 证明状态、对话和过程里程碑能揭示单轮函数调用评测遗漏的失败；不能从其相关结果推出某种恢复策略会提升真实 agent。
- [OPEN_QUESTION] 本文作为评测证据无需第三读；若未来直接复用 milestone 分数作主要实验指标，应单独审查每个场景定义。

## 6. 解析与访问声明

- [AUTHOR_FACT] 解析覆盖物理页 1–24，未发现影响结论的文本—可视版冲突；图中对话框细节在文本层较少，报告只采用作者正文明确解释的部分。
- [AUTHOR_FACT] 实际模型/版本 `unknown`；程序性盲化。冻结后只读指定 PDF 与 invocation 内统一 prompt；使用本地 PowerShell、`Get-FileHash`、Python/PyMuPDF；未联网。冻结前仅用 `rg` 定位指定路径，未读论文。只写本报告。
