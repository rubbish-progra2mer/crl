# P038 独立二读报告

- Attempt：`r2-20260719-p038-a1`
- PDF SHA-256：`26a3f0426ee1d533e4dd9f62d1343a7a1d231fe718cfaf3a362cc7de829ae913`
- 阅读范围：物理页 1–26，逐页全文
- 二读结论：`ACCEPT_WITH_NARROWING`

## 1. 方法与被改变的计算

- [AUTHOR_FACT] AgentDojo 是有状态、可扩展的 prompt-injection 安全评测环境，初版含 4 个环境、97 个 user task、27 个 injection target，笛卡尔积形成 629 个安全测试。（物理页 1–6，摘要/§3/表 1）
- [AUTHOR_FACT] user task 与 injection task 都以确定性函数检查执行前后环境状态，而非让另一个 LLM 判断成功；每个任务还保存 ground-truth tool-call 序列以放置攻击和辅助适配。（物理页 3–5，§3.1，定位词 “utility function”“security function”）
- [READER_INTERPRETATION] 基准改变的是安全评价计算：同时测 benign utility、attack 下 utility 与 targeted ASR，并把攻击放进实际会被工具读取的不可信数据；不是只做静态提示分类。

## 2. 防御 Operator 与计算差异

- [AUTHOR_FACT] 实验比较 data delimiters、prompt-injection detector、重复用户 prompt 和 tool filter；tool filter 在读取不可信数据前先限制本任务可用工具集合。（物理页 8–9、16、19，§4.3/图 12/18）
- [AUTHOR_FACT] GPT-4o 条件下，无防御 benign utility 69.0%、utility-under-attack 50.01%、targeted ASR 57.69%；tool filter 分别为 73.13%、56.28%、6.84%，detector 为 41.49%、21.14%、7.95%。（物理页 20，表 5）
- [READER_INTERPRETATION] 可抽取的强 Operator 是“在接触不可信内容前，按用户任务预承诺最小工具权限”；它直接改变可执行动作集合，而不只是追加安全提示。
- [AUTHOR_FACT] 作者指出该防御在约 17% 的测试中失效边界明确：用户任务所需工具本身足以完成攻击；任务必须根据中间结果动态选工具时也难以预先过滤。（物理页 9，Strengths and limitations）

## 3. 攻击、基线与公平性

- [AUTHOR_FACT] 主要攻击是通用 “Important message”，不同攻击文本效果差异很大；表 4 中该攻击 targeted ASR 57.7%，而 TODO 为 3.66%、ignore-previous 为 5.41%、InjecAgent 为 5.72%。（物理页 8、19–20，图 8/表 4）
- [AUTHOR_FACT] 攻击位置越接近工具输出末尾越有效；攻击者正确知道用户/模型只增加约 1.9 点，而猜错会降低约 22 点。（物理页 8、20–21，表 2/图 21）
- [AUTHOR_FACT] 不同模型并非同 prompt：Claude 额外使用供应商建议 prompt，Llama 使用适配后的工具调用 prompt；Llama 也没有官方 function calling。（物理页 6–7、17–18，§4/图 15–16）
- [READER_INTERPRETATION] 跨模型 utility/ASR 同时受模型、function-calling 接口和 prompt 影响；论文更适合支持防御机制边界，不宜用作纯模型安全排名。
- [AUTHOR_FACT] 完整 GPT-4o 安全套件成本估计约 35 美元，97 个 benign utility 测试约 4 美元。（物理页 20，Cost of running a suite）

## 4. 负向结果和未测试边界

- [AUTHOR_FACT] 更高 benign utility 的模型可能更容易完成攻击目标；同时大多数模型在攻击下绝对 utility 下降约 10–25 点。（物理页 7，图 6/§4.1）
- [AUTHOR_FACT] prompt detector 虽降低 ASR，但假阳性显著损伤正常 utility；重复 prompt 对当前攻击有效，但作者明确认为可能无法抵抗适应性攻击。（物理页 9，§4.3）
- [AUTHOR_FACT] 作者强调默认攻击不足以声称鲁棒，数据卡把“只用默认攻击评估防御”列为不适合用途；未来还需更强自适应攻击、多任务持续上下文和多模态场景。（物理页 9–10、24–26，Conclusion/Data card）
- [READER_INTERPRETATION] 真实 Failure：`固定攻击上的低 ASR 不等于安全`；`检测型防御以拒绝/中止换安全`；`最小权限在读写工具分离时有效，在同一工具同时满足用户与攻击目标时失效`。

## 5. 可抽取内容

- [READER_INTERPRETATION] Operator 候选：`pre-data least-privilege tool filtering`；`用确定性 state checks 分离 utility 与 targeted security`；`防御必须接受适应性攻击评测`。
- [READER_INTERPRETATION] Failure 候选：`untrusted tool output 劫持后续工具调用`；`delimiter/重复提示不提供自适应保证`；`PI detector 假阳性破坏 utility`；`同权限工具使过滤失效`。
- [READER_INTERPRETATION] 窄 Claim：在 AgentDojo 2024 初版和指定通用攻击下，预先工具过滤显著降低 GPT-4o targeted ASR 且保持 benign utility；不能宣称对自适应攻击、持续多任务上下文或所有 prompt injection 安全。
- [OPEN_QUESTION] 若将 tool filtering 作为安全方向核心 implement，必须在正式实验中加入适应性攻击与同工具攻击目标；本次文献入库本身无需第三读。

## 6. 解析与访问声明

- [AUTHOR_FACT] 解析覆盖物理页 1–26，正文、表格、代码和 prompts 可读，未发现影响判断的文本—可视版冲突。
- [AUTHOR_FACT] 实际模型/版本 `unknown`；程序性盲化。冻结后只读指定 PDF 与 invocation 内统一 prompt；使用本地 PowerShell、`Get-FileHash`、Python/PyMuPDF；未联网。冻结前仅用 `rg` 定位指定路径，未读论文。只写本报告。
