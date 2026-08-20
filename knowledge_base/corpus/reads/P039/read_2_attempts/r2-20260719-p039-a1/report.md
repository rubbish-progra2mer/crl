# P039 独立二读报告

- Attempt：`r2-20260719-p039-a1`
- PDF SHA-256：`6588af66fd477d9764c20c52c2adb7d92fcbf6a788fe09713bc71916862d3009`
- 阅读范围：物理页 1–18，逐页全文
- 二读结论：`ACCEPT_WITH_NARROWING`

## 1. 方法与被改变的计算

- [AUTHOR_FACT] ToolFailBench 含 1,000 个单轮任务、5 个专业领域，其中 750 个必须调用工具、250 个无需工具；tool-required 任务让 mock return 与“可能的参数记忆值”冲突。（物理页 1–3，摘要/§3.1/图 1）
- [AUTHOR_FACT] 每条轨迹被分为 Tool-Skip、Result-Ignore、Output-Fabrication、Unnecessary-Tool-Use 等互斥失败类型；标签来自确定性规则和两个 LLM judge 的多数票。（物理页 3–4，§3.2–§3.4/表 1）
- [READER_INTERPRETATION] 论文改变的是诊断分辨率：把最终失败拆成“是否调用、是否采信返回、是否编造、是否过度调用”；它是 failure taxonomy/benchmark，不是改善工具使用的 operator。

## 2. 协议、基线与主要结果

- [AUTHOR_FACT] 所有模型使用相同任务、schema、domain prompt、temperature=0、max_tokens=1024；第一步 `tool_choice=auto`，若调用则执行 mock tool，第二步强制 `tool_choice=none` 生成最终回答。（物理页 4、10，§4.2/§B2）
- [AUTHOR_FACT] 19 个 headline 模型中最好 ensemble CTUR 为 Grok-4.3 的 86.33%；最强几名 Wilson 区间重叠，作者将其视为领先簇而非严格排名。（物理页 5、10，表 2/表 6）
- [AUTHOR_FACT] 大多数模型 control UTR≤1.61%、CTRL-Acc>95%；Llama-3.1-70B 的 UTR 77.73%、CTRL-Acc 8.91%，Llama-3.1-8B 为 98.39% 和 0%。（物理页 5–6，图 2/表 3）
- [AUTHOR_FACT] 同规模 Llama-3.1-70B 与 Qwen2.5-72B 的 control accuracy 相差约 89 点，作者据此把 Always-Call 描述为 family/training-specific，而非单由规模决定。（物理页 6，§5.3/表 3）
- [READER_INTERPRETATION] 该同输入、同 prompt 的家族对比有诊断价值，但不是训练机制因果实验；训练数据、chat template、tool-call tuning 均未被隔离。

## 3. Prompt、oracle 与测量混杂

- [AUTHOR_FACT] system prompt 极强地规定“tool return is ground truth”、必须逐字引用值、概念题不得用工具，并强制统一回答模板。（物理页 12–15，§E3–E4，定位词 “EXTREME IMPORTANT”）
- [READER_INTERPRETATION] 因而 CTUR 测的是在明确行为规则和 mock ground truth 下的协议遵循，不等同于开放环境中判断工具是否可信、是否陈旧或是否被攻击。
- [AUTHOR_FACT] “parametric prior”只是任务设计术语；作者明确不声称能观察冲突值来自记忆、幻觉或其他内部机制。（物理页 3、9，§3.1/§A2）
- [AUTHOR_FACT] 两个 judge 分别为 Qwen3.5-397B-A17B-FP8 与 GLM-4.7-FP8；judge–judge κ=0.773，三方 Fleiss κ=0.693，三方完全分歧占 1.5%，两 judge 联合推翻规则占 8.4%。（物理页 4、6、11，§4.3/§5.4/§C）
- [AUTHOR_FACT] Unnecessary-Tool-Use 的 Fleiss κ 仅 0.23，尽管 raw agreement 为 0.95；Result-Ignore κ 为 0.53。（物理页 11，表 8）
- [READER_INTERPRETATION] 多数票降低字符串规则脆弱性，但 judge 共模盲点仍存在；低流行率标签不应只看 κ 或只看 raw agreement。

## 4. 负向结果、范围与工程失败

- [AUTHOR_FACT] 单轮协议不覆盖多工具链、从先前错误恢复或交互状态更新；只含五个领域，未来还可能产生训练—测试重叠。（物理页 7，Limitations）
- [AUTHOR_FACT] 两个非 headline 模型没有干净执行的 tool call；其中 Mistral 可能受 parser 影响。另一个 DeepSeek run 因 chat-template/detokenizer 输出原始 token 而排除。（物理页 11–12，§D1–D2）
- [READER_INTERPRETATION] harness 解析失败必须与模型行为失败分开；把未执行的“tool-like text”判为 Tool-Skip是合理的轨迹事实，但不应进一步归因模型不会选择工具。
- [AUTHOR_FACT] 规则分类通过期望字符串检查结果使用，可能漏掉忠实释义；ensemble 平均 CTUR 75.02%，规则均值 71.05%。（物理页 6，§5.4）
- [OPEN_QUESTION] 任务值、控制题答案和 1,000 条数据的人工验证规模在论文中未见完整报告；mock return 的“反常度”是否跨领域等价也未充分建立。

## 5. 可抽取内容

- [READER_INTERPRETATION] Failure 候选：`需要工具却跳过`；`调用后忽略返回`；`在返回之外编造结构化字段`；`概念题无必要调用工具`；`parser/template 故障伪装成模型失败`。
- [READER_INTERPRETATION] 评测 Operator 候选：`以 paired tool-required trap + no-tool control 同时测 tool trust 与 restraint`；`轨迹级互斥失败类型替代单一总分`。
- [READER_INTERPRETATION] 窄 Claim：在强提示、单轮 mock-tool 协议中，不同模型表现出可区分的工具采信和过度调用画像；不能据此声称已识别内部参数记忆机制，也不能外推到长程 agent。
- [OPEN_QUESTION] 该论文为 2026 workshop/arXiv、单作者工作，且 benchmark 数据质量验证较薄；若用于核心 Claim 或强 baseline，建议第三读并在可联网阶段核对代码/版本，否则可作为新近诊断证据收窄入库。

## 6. 解析与访问声明

- [AUTHOR_FACT] 解析覆盖物理页 1–18，正文、表格、prompt 和 rubric 可读，未发现影响判断的文本—可视版冲突。
- [AUTHOR_FACT] 实际模型/版本 `unknown`；程序性盲化。冻结后只读指定 PDF 与 invocation 内统一 prompt；使用本地 PowerShell、`Get-FileHash`、Python/PyMuPDF；未联网。冻结前仅用 `rg` 定位指定路径，未读论文。只写本报告。
