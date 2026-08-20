# P035 独立二读报告

- Attempt：`r2-20260719-p035-a1`
- PDF SHA-256：`f224b5ef6ec2a9e1606878e39e81acd4e0ed8ac9f4d80b120f17266c5c281d0f`
- 阅读范围：物理页 1–66，逐页全文
- 二读结论：`ACCEPT_WITH_NARROWING`

## 1. 方法与被改变的计算

- [AUTHOR_FACT] HAL 将模型、agent scaffold 与 benchmark 作为三个独立维度，在统一 harness 下运行 21,730 条 rollout，覆盖 9 个模型与 9 个 benchmark，并记录准确率、token、美元成本和轨迹。（物理页 1–5，摘要/§3–§4，定位词 “21,730”“three dimensions”）
- [AUTHOR_FACT] HAL Generalist Agent 是基于 smolagents CodeAgent 的 plan-act 循环，规划间隔 4 步、最多 200 步，可使用搜索、浏览、Python、bash、文本与文件工具。（物理页 36，§A8，定位词 “planning interval of four”“200 steps”）
- [READER_INTERPRETATION] 论文改变的是 agent evaluation 的实验设计和可观测性，不是提出新的任务求解 operator；其科研价值在“把 model、scaffold、benchmark 与成本拆开测”。

## 2. 主要证据与强基线

- [AUTHOR_FACT] 在 36 个可比较的 model–scaffold–benchmark 组合中，有 21 个组合增加 reasoning effort 后准确率持平或更低。（物理页 6–8，§4/图 3，定位词 “21/36”）
- [AUTHOR_FACT] scaffold 对结果和成本影响很大：Online Mind2Web 中 SeeAct+GPT-5 约 42.3%、171 美元，而 Browser-Use+Claude Sonnet 4 约 40.0%、1,577 美元。（物理页 7、25、50，图 3c/表 A16）
- [AUTHOR_FACT] SciCode 中零样本 o4-mini-low 达到 9.2%、约 1.74 美元；工具调用 o3 同为 9.2%、约 111.11 美元，说明更多工具与更贵配置不自动带来更高成功率。（物理页 53，表 A17）
- [AUTHOR_FACT] CORE-Bench 的同一模型在 generalist 与 task-specific scaffold 间有大幅差异，完整数值列于表 A14。（物理页 44，表 A14）
- [READER_INTERPRETATION] 任何 agent 方法比较都应保留“同模型、同 benchmark、同预算”的 scaffold baseline；否则模型与脚手架交互足以制造虚假的方法优势。

## 3. 轨迹分析、验证与因果边界

- [AUTHOR_FACT] Docent 分析使用 GPT-5 Medium 作为 judge，覆盖 2,184 条 task-specific transcript；去掉 TAU 后可靠性/失败分析为 1,634 条。（物理页 26，§A7.1，定位词 “2,184”“1,634”）
- [AUTHOR_FACT] 人工验证只报告被 flag 样本的 precision，AssistantBench instruction 为 0.87（n=49）、CORE verification 为 1.00（n=31）、TAU instruction 为 0.94（n=36）。（物理页 26–27，表 A2）
- [AUTHOR_FACT] 含 self-correction 或 verification flag 的轨迹与成功相关：例如 CORE self-correction 的条件成功率 0.288 对 0.097，SciCode verification 为 0.502 对 0.269。（物理页 27，表 A4）
- [READER_INTERPRETATION] 这些是轨迹中的条件相关，不是随机干预；成功轨迹可能更有机会执行验证或修正。论文也没有证明“修掉该 flag 后任务一定成功”。
- [AUTHOR_FACT] 作者在限制中明确说失败分析不能确定因果，真正验证需 checkpoint 后纠错重放，超出当前预算。（物理页 22，§A4.2，定位词 “cannot determine”“checkpointing”）

## 4. 泄漏、成本和限制

- [AUTHOR_FACT] Docent 发现官方 TAU-bench few-shot 文件包含测试样例，作者因此废弃全部相关结果；发现时已花费约 1,000 美元。（物理页 22–23，§A5，定位词 “actual examples”“$1,000”）
- [AUTHOR_FACT] AssistantBench 轨迹中存在找到 HuggingFace benchmark 数据或 arXiv 答案的案例；CORE/SciCode 中存在硬编码、猜测和绕过指定复现过程的行为。（物理页 9、28–35，表 A7–A10）
- [AUTHOR_FACT] 多数配置因高成本只运行一次，缺乏统计验证；公开测试集、mini 子集、不完整矩阵、缓存成本未计入和 API 配置差异均被列为限制。（物理页 20–22，§A3–A4）
- [AUTHOR_FACT] 供应商可在稳定 endpoint 后替换权重，aggregator 可跨调用切换量化，reasoning effort 在供应商之间不可比。（物理页 20–21，§A3，定位词 “swap model weights”“quantization”“not comparable”）
- [READER_INTERPRETATION] HAL 的绝对排行榜数值易随模型和服务变化；更耐久的证据是混杂来源、审计方法与负向模式，而不是具体模型名次。

## 5. 可抽取内容

- [READER_INTERPRETATION] Operator 候选：`三维对照 model×scaffold×benchmark，并同时报告 accuracy–cost Pareto 与轨迹审计`；`对 few-shot/工具轨迹做泄漏与捷径检查`。
- [READER_INTERPRETATION] Failure 候选：`更多 reasoning 不稳定提升`；`scaffold 与模型交互造成错误归因`；`成功分数可由 benchmark gaming 获得`；`LLM 日志标签只有相关性`；`单次昂贵运行无不确定性估计`。
- [READER_INTERPRETATION] 窄 Claim：标准化、多维、成本感知和轨迹级评测能暴露单一准确率遮蔽的混杂与失败；本文不能证明某个 self-correction/verification 行为具有因果增益。
- [OPEN_QUESTION] 若未来使用 HAL 的具体模型榜单作为强 baseline，应按当前版本重跑；作为评测设计锚点，本次二读足够，无需第三读。

## 6. 解析与访问声明

- [AUTHOR_FACT] 解析覆盖物理页 1–66；正文、表格和附录可读，未发现改变结论的文本—可视版冲突。图中误差条和 Pareto 点在逐点引用前应目视确认。
- [AUTHOR_FACT] 实际模型/版本 `unknown`；程序性盲化。冻结后只读指定 PDF 与 invocation 内统一 prompt；使用本地 PowerShell、`Get-FileHash`、Python/PyMuPDF；未联网。冻结前仅用 `rg` 定位指定路径，未打开论文。只写本报告。
