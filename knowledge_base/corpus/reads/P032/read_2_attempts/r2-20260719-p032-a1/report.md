# P032 独立二读报告

- Attempt：`r2-20260719-p032-a1`
- PDF SHA-256：`30a3161dbbb9531528bf410bd1df84eeb9ada8151f614789ae80ca86b7b32c7e`
- 阅读范围：物理页 1–78，逐页全文
- 二读结论：`ACCEPT_WITH_NARROWING`

## 1. 方法与被改变的计算

- [AUTHOR_FACT] CRITIC 让同一个黑盒 LLM 先生成答案，再调用外部工具验证，并依据工具反馈迭代修正；实现中工具按任务固定：QA 用 Google Search、数学用 Python、毒性检测用 Perspective API。（物理页 1–5，摘要/§2–§3，定位词 “verify and correct”“external tools”）
- [READER_INTERPRETATION] 真正改变的计算是把一次生成改为“生成→外部验证→条件修正”的后处理闭环；关键因果差异应归于外部可检验反馈，而不是“模型自省”本身。
- [AUTHOR_FACT] 主要实验设置最多 7 次工具交互、3 次修正；QA 每个数据集抽取 500 样本以控制预算，初始回答使用 greedy decoding。（物理页 5–7，§3/实验设置，定位词 “500”“7 tool interactions”“3 corrections”）

## 2. 基线与主要结果

- [AUTHOR_FACT] 表 1 中 ChatGPT CoT 的 F1 为 64.3/79.2/42.8，CRITIC 为 74.9/81.7/52.9；去掉工具的版本为 67.3/79.9/46.1。（物理页 6，表 1，定位词 “ChatGPT”“CRITIC”“w/o tool”）
- [AUTHOR_FACT] ReAct 对照被改写以适配作者的 API/任务流程，并非原实现的严格复现。（物理页 6 及附录基线说明，定位词 “ReAct”）
- [AUTHOR_FACT] 数学结果不是单调正向：Text-Davinci-003 在 SVAMP 从 84.0 降到 80.7；无工具变体在部分条件也有正向或近中性变化。（物理页 7，数学结果表，定位词 “SVAMP”“84.0”“80.7”）
- [AUTHOR_FACT] HotpotQA 的 100 例人工错误分析中，幻觉比例由 36% 降至 7%，但拒答为 12%、错误修正为 10%；GSM8K 全集分析中，CRITIC 修复初始错误的 32.2%，同时破坏 4.3% 的原正确答案。（物理页 25–26，误差分析，定位词 “36%”“4.3%”）
- [READER_INTERPRETATION] 最强相关基线是同模型 CoT、无工具 CRITIC 和 ReAct；CRITIC 的主要优势在可执行/可检索 verifier，而非 token 或更强模型替换。

## 3. Oracle、prompt、成本与混杂

- [AUTHOR_FACT] `CRITIC*` 只在初始答案错误时启动修正，依赖正确性 oracle；它不能作为可部署的非 oracle 主结果。（物理页 6–8，表格脚注/设置，定位词 “CRITIC*”）
- [AUTHOR_FACT] 毒性任务由 Perspective API 提供反馈，并又以同一类 API 信号衡量毒性；搜索结果被缓存约 9GB，工具调用在论文成本核算中按免费处理。（物理页 8–9，毒性/成本设置，定位词 “Perspective”“9GB cache”）
- [READER_INTERPRETATION] 毒性实验存在反馈器—评测器耦合；QA/数学结果更适合作为机制证据。工具免费和未完整报告端到端延迟，使收益—成本比较不完整。
- [AUTHOR_FACT] 附录给出大量任务专用 few-shot 示例、反馈格式和提示词。（物理页 29–78，prompts/examples）
- [READER_INTERPRETATION] 结果包含显著 prompt 与任务适配贡献，不能外推为零配置、跨任务通用的自我改进能力。

## 4. 负向结果与限制

- [AUTHOR_FACT] 作者承认线性增加的工具/模型延迟、提示工程依赖、未覆盖任务和模型、仅文本输入，以及工具偏差与隐私风险。（物理页 21，Limitations，定位词 “latency”“prompt engineering”“privacy”）
- [AUTHOR_FACT] GSM8K 错误修正后仍有大量错误，其中错误修正占后续错误的 14.3%。（物理页 25–26，错误分类，定位词 “14.3%”）
- [READER_INTERPRETATION] 真实 Failure 不是“模型不会反思”这么宽，而是：外部 verifier 不完备时，循环会把正确答案改错；检索到的证据也可能被误读或过度采信。
- [OPEN_QUESTION] 在严格相同总 token、总调用次数和墙钟预算下，CRITIC 相对一次性更长 CoT 或多样本验证的净收益，原文没有完全隔离。

## 5. 可抽取内容

- [READER_INTERPRETATION] Operator 候选：`在最终提交前调用任务匹配的外部 verifier，并将结构化反馈送回同一模型做有限次修正`。
- [READER_INTERPRETATION] Failure 候选：`内在批评不足以稳定发现事实/计算错误`；`外部反馈仍会错误修正原正确答案`；`反馈器与指标共源可夸大收益`。
- [READER_INTERPRETATION] 窄 Claim：外部工具反馈在若干文本 QA、数学和毒性任务上能提升同模型的后验修正，但收益依赖任务工具、提示和预算，并存在回归。
- [OPEN_QUESTION] 仅在把 CRITIC 作为核心自修正锚点或要求精确复现实验时建议第三读；常规机制入库无需阻断。

## 6. 解析与访问声明

- [AUTHOR_FACT] 物理页 1–78 的解析文本可读，未发现影响结论的文本—可视版冲突；表格具体数值已按物理页定位。
- [AUTHOR_FACT] 实际模型/版本 `unknown`；程序性盲化，无技术 allowlist。冻结后只读取指定 PDF、invocation 中的统一 prompt；用本地 PowerShell、`Get-FileHash`、Python/PyMuPDF；未联网。冻结前只用 `rg` 定位指定路径，未读论文内容。仅写本报告。
