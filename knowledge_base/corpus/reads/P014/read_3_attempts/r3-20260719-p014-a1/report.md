# P014 fresh 独立第三读核源报告

## 0. Provenance 与边界

- [AUTHOR_FACT] 本报告对应 invocation `r3-20260719-p014-a1`；论文 canonical id 为 `ACL:2025.naacl-long.502`，PDF 记录的 SHA-256 为 `57a01e87496308e3345839c48f085516dd2824ec5aaacf51b71f127c12f42bb7`，统一 prompt 记录的 SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`。本次实际复核两个哈希均与 invocation 一致。
- [AUTHOR_FACT] 论文是 NAACL 2025 Long 版本，PDF 共 23 页，印刷页码 9956–9978。
- [READER_INTERPRETATION] 本读取是 `procedural_blinding`，不是可验证的文件级技术隔离。未枚举工作区，未读取 read_1、read_2、Cards、其他读者报告或 blind query，未联网。
- [READER_INTERPRETATION] 除 invocation、统一 prompt 和指定 PDF 外，运行时为遵循系统强制的 PDF 处理与完成前核验规范，还读取了 `C:/Users/g/.codex/skills/pdf/SKILL.md` 与 `C:/Users/g/.codex/plugins/cache/openai-curated-remote/superpowers/6.1.1/skills/verification-before-completion/SKILL.md`；两者均不是工作区研究材料。此项使实际文件访问集超出 invocation 列出的三份研究输入，故在此如实披露。
- [READER_INTERPRETATION] 实际模型/版本对读者不可见，记为 `unknown`；可见任务身份为 `/root/p014_third_read`。本报告不生成 Card，不作 Candidate、novelty 或研科价值判断。

## 1. 逐页覆盖记录

| PDF 页（印刷页） | 核查内容 |
|---|---|
| 1（9956） | 摘要、引言、图 1 的 redundant/drift/stubborn 示例 |
| 2（9957） | 三类问题定义、IoRT 三阶段概述、贡献 |
| 3（9958） | 相关工作、第 3.1 节、图 2 的 oracle/非 oracle 迭代曲线 |
| 4（9959） | 第 3.2 节、图 3 饼图、第 4 节开始 |
| 5（9960） | 图 4 总流程、第 4.1–4.2 节、式 (1)–(5) |
| 6（9961） | 第 4.3 节 select/stop/refresh、式 (6)–(7)、实验设置 |
| 7（9962） | 表 1–2 及数学/常识主结果 |
| 8（9963） | 表 3 消融、图 5、性能与开销讨论 |
| 9（9964） | 模型差异、结论、Limitations |
| 10（9965） | 参考文献 |
| 11（9966） | 参考文献 |
| 12（9967） | 参考文献结尾，附录 A/B，表 4–5，附录 C.1 |
| 13（9968） | 表 6 数据/少样本数，附录 C.2 refresh/self-reflect prompt |
| 14（9969） | 附录 C.3 instructor 的 select 与 refresh/stop prompt |
| 15（9970） | 表 7 StrategyQA stop 案例 |
| 16（9971） | 表 8 StrategyQA select 案例 |
| 17（9972） | 表 9 StrategyQA 反思漂移后 select 恢复案例 |
| 18（9973） | 表 10 StrategyQA refresh 后纠错案例 |
| 19（9974） | 表 11 GSM8K stop 案例 |
| 20（9975） | 表 12 GSM8K select 案例 |
| 21（9976） | 表 13 GSM8K select 案例及代码/执行结果疑点 |
| 22（9977） | 表 14 GSM8K refresh 案例前半 |
| 23（9978） | 表 14 refresh 后代码、抽取答案与 select 结论 |

## 2. 统一问题 1：方法究竟改变哪一步计算？

- [AUTHOR_FACT] 传统静态反思在第 `i` 轮直接由第 `i-1` 轮响应继续评估与修订；IoRT 在“反思响应已产生、下一轮尚未开始”的位置插入 instructor。定位：PDF p.2/p.4，印刷 p.9957/p.9959，§4 总览与图 4。
- [AUTHOR_FACT] instructor 之前，meta-thinker 根据检索的少样本对为问题 `x` 生成 meta-thought `m_x`，并将 `(x,m_x)` 追加到 meta memory（式 (1)–(4)）。定位：PDF p.5，印刷 p.9960，§4.1。
- [AUTHOR_FACT] reflector 使用问题、basic response/答案与评估反馈生成 reflective response（式 (5)）。随后，无 LLM 的 self-consistency classifier 只比较两个抽取答案是否相等。定位：PDF p.5–6，印刷 p.9960–9961，§4.2–4.3。
- [AUTHOR_FACT] 答案不一致时，instructor 根据问题、meta-thought 及两份响应选更好者；答案一致时，instructor 再决定 stop 或 refresh；达到最大迭代数 `N` 也停止。定位：PDF p.6，印刷 p.9961，§4.3、式 (6)–(7)；PDF p.14，印刷 p.9969，附录 C.3。
- [READER_INTERPRETATION] 因而新增的核心计算不是反思生成器本身，而是一个“答案一致性分支 + meta-thought 辅助的响应选择/停止/重新生成控制器”。
- [OPEN_QUESTION] §4.3 先以 `A_b^i=A_r^i` 定义一致，后文却写成 `R_b^i=R_r^i`；refresh 段又说新生成 `R_r^(i+1)`。这些记号是否仅为笔误，以及 refresh 究竟重跑 initial/refresh prompt 还是 reflector prompt，正文没有完全消除歧义。定位：PDF p.6，§4.3，refresh 条目。

## 3. 统一问题 2：输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 输入为问题 `x`；数学任务初始/刷新响应是可执行 Python 代码，常识任务是 CoT 文本与 T/F 答案。定位：PDF p.12–13，印刷 p.9967–9968，附录 A、C.2；表 6。
- [AUTHOR_FACT] 数学答案由代码执行器获取，代码出错时记为 `None`；StrategyQA 通过固定短语后的正则抽取答案。定位：PDF p.12，印刷 p.9967，附录 A。
- [AUTHOR_FACT] meta-thinker 可用信息包括人工定义的种子 meta-thought 示例、按问题向量余弦相似度召回的 top-k 问题/meta-thought 对，以及测试过程中追加的新对。表 6 给出 GSM8K/SVAMP/StrategyQA 的 meta 示例数分别为 8/8/6。定位：PDF p.5、p.13，§4.1、表 6。
- [AUTHOR_FACT] instructor 可用 `x,m_x,R_b^i,A_b^i,R_r^i,A_r^i`，输出当轮选定响应 `R_o^i` 或 stop/refresh 决策；不使用 oracle 正确性标签作为运行时分支条件。定位：PDF p.6，§4.3；PDF p.14，附录 C.3。
- [AUTHOR_FACT] 干预时点是每轮 reflector 输出之后、下一轮生成之前；停止后为统一评估，后续轮的输出被设成停止轮输出（式 (7)）。
- [OPEN_QUESTION] meta memory 是否按固定测试顺序在整个 test set 上持续更新，后来样本是否可检索到先前测试样本的 meta-thought，以及每个方法/轮次是否重置 memory，原文未说明。这不是 oracle 标签问题，但可能引入测试顺序和跨样本信息依赖。

## 4. 统一问题 3：最强基线与最接近组合基线

- [AUTHOR_FACT] 表 1 数学任务列出 CoT、PS、CoT+HSP、Self-Contrast、CoT-SC(8)、Multi-Agent、Self-Reflection、PoT、PoT+HSP、PoT-SC(8)、CRITIC；IoRT 也用 PoT 产生初始响应。表 2 的 StrategyQA 用 CoT 初始响应。定位：PDF p.6–7，§5.1、表 1–2。
- [READER_INTERPRETATION] 按结构接近性，CRITIC 是最接近的“PoT + 外部工具反馈 + 静态反思”基线；PoT+HSP（数学）/CoT+HSP（常识）是最接近的“初始推理 + 抽象提示”组合基线。它们分别隔离了动态控制与 meta-thought 位置的变化。
- [AUTHOR_FACT] 表 1 中不存在一个基线在所有模型/数据集单元格都最强。IoRT 之外的最高值主要来自 Self-Contrast、PoT+HSP、PoT-SC(8) 和 Multi-Agent。其中 Self-Contrast 在 GSM8K/Llama2-13B 为 42.3，高于 IoRT 40.8；在 SVAMP/GPT-3.5 为 89.0，高于 IoRT 88.1；在 GSM8K/GPT-4 与 IoRT 同为 95.4。定位：PDF p.7，表 1。
- [AUTHOR_FACT] 表 2 的每个 StrategyQA 模型列中，IoRT 数值都高于列出基线；但其 token 数 3877 高于 CoT 514、CoT+HSP 1018 和 PS 1090，低于 CoT-SC(8) 4145 和 Self-Reflection 5944。定位：PDF p.7，表 2。
- [OPEN_QUESTION] §5.2 文字说 Self-Contrast 在 GSM8K/Llama2-7B 超过 IoRT，但表 1 对应数值是 20.5 vs 24.0；真正超过 IoRT 的是 Llama2-13B（42.3 vs 40.8）。这是正文与表格的可复核不一致。
- [OPEN_QUESTION] §5.2 声称 IoRT 相对 PoT 平均约 `+4.4%`；若对表 1 的 10 个数学单元格做简单宏平均，差是 67.75−62.89=`+4.86` 个百分点。原文未说明 `+4.4%` 的聚合公式或是否纳入其他数据。

## 5. 统一问题 4：模型、token、tool-call、prompt 或 oracle 差异

- [AUTHOR_FACT] black-box LLM 和 reflector 分别使用 GPT-3.5-Turbo-0613、GPT-4-0613 或 Llama2-Chat 7B/13B/70B；但所有设置的 meta-thinker 和 instructor 固定用 GPT-3.5-Turbo-0613。温度 0.3，最大 4 轮，每数据集运行 5 次后报平均准确率。定位：PDF p.6，§5.1 Implementation Details。
- [READER_INTERPRETATION] 因此 Llama2 列并非纯 Llama2 系统；它们额外使用商业 GPT-3.5 作控制器。表 1/2 所示的“跨模型泛化”无法单独归因于被反思的 Llama2 本身。
- [AUTHOR_FACT] 表 1 的平均 LLM/API calls 为 IoRT 7.3，Self-Contrast 7.8，CoT/PoT 1，HSP 组合 2，SC(8) 8，Multi-Agent/Self-Reflection/CRITIC 9。定位：PDF p.7，表 1。
- [READER_INTERPRETATION] 主结果不是严格的计算量匹配对比：IoRT 比单次 PoT/CoT 和 HSP 组合使用更多 LLM 调用/token，却比固定多轮反思略少。评估的是不同准确率—计算量工作点，不能从表格排除计算量差异的贡献。
- [AUTHOR_FACT] 数学任务中 PoT 代码经代码执行器取答案，CRITIC 另以工具交互作外部反馈；文章只报 API/LLM calls，没有分项报代码执行器调用。定位：PDF p.3，§3.1；PDF p.6–7，§5.1、表 1；PDF p.12，附录 A。
- [OPEN_QUESTION] 代码执行器调用、试错次数、实际延迟与货币成本没有逐方法对齐，tool-call 差异的影响无法从现有报告分离。
- [AUTHOR_FACT] IoRT 为三个数据集使用不同数量的 meta/refresh/reflect 少样本；数学分别为 8/8/4，StrategyQA 为 6/5/3。部分 text-reasoning 基线结果又直接引自 Zhang et al. (2024)。定位：PDF p.7 表 1 注；PDF p.13 表 6。
- [OPEN_QUESTION] 基线是否采用同一系统 prompt、相同少样本、相同采样种子和相同 5 轮重复，原文未完整报告，因而 prompt/实验来源差异不能排除。
- [AUTHOR_FACT] 运行时分支不用 oracle 答案；第 3.1 节的 oracle 曲线是评估模拟，只让原本错误的样本继续纠错，并忽略正确改错的情形。定位：PDF p.3，§3.1、图 2。
- [READER_INTERPRETATION] 这支持“IoRT 的分支未直接查真值”，但不等于所有比较已排除 oracle/数据泄漏；人工种子 meta-thought 的选取过程、是否见过测试答案没有说明。

## 6. 统一问题 5：限制、负向结果与未测试边界

- [AUTHOR_FACT] 非 oracle 评估中，Self-Correct 和 CRITIC 在 GSM8K/SVAMP 的迭代性能不稳定，最大下降分别报为 2.4 和 3.0 个百分点；表 5 显示多轮中“正确改错”比例可接近或超过“错误改对”。定位：PDF p.3–4，§3.1–3.2、图 2；PDF p.12，表 5。
- [AUTHOR_FACT] 表 1/2 显示 Self-Reflection 在多个设置低于初始 PoT/CoT；正文汇总 StrategyQA 上平均下降 6.0 个百分点，且 CRITIC 相对 PoT 也报为下降 2.6 个百分点。定位：PDF p.7，§5.2、表 1–2。
- [AUTHOR_FACT] 表 3 中去掉 self-consistency 对平均准确率“无明显变化”（正文报 `-0.51%`），但会使方法每次都跑满 4 轮，而 IoRT 平均约 2.2 轮。去掉 meta-thought 平均下降 2.1 个百分点，但仍比初始响应高 2.9 个百分点。定位：PDF p.8，§5.3、表 3。
- [AUTHOR_FACT] 作者明示限制是 instructor 仍有偶发误判；在 GPT-3.5 数学实验中，oracle 最终轮比 IoRT 高 1.6 个百分点。同时，由于开源模型的抽象推理/指导能力限制，实验未用开源模型作 meta-thinker 或 instructor。定位：PDF p.9，印刷 p.9964，Limitations。
- [READER_INTERPRETATION] 实验边界仅有 GSM8K、SVAMP、StrategyQA，仅准确答案的数学/常识推理，且仅测到 `N=4`。它没有直接测试开放式长文本、代码修复、多步工具代理、事实核查、更长迭代或噪声/恶意 meta-thought。
- [OPEN_QUESTION] 虽然每设置跑 5 次，原文未报方差、置信区间或显著性检验；对 0.2–1 个百分点级别的差异，现有表格无法确定是否超出采样波动。

## 7. 统一问题 6：可抽取的 Operator 与真实 Failure

### 可抽取为机制单元的 Operator（非 Card）

- [AUTHOR_FACT] `Meta-thought retrieval/generation/update`：人工种子记忆→top-k 检索→生成 `m_x`→追加记忆。定位：PDF p.5，§4.1，式 (1)–(4)。
- [AUTHOR_FACT] `Answer-consistency gate`：不用 LLM，仅比较 basic/reflective 抽取答案相等性。定位：PDF p.6，§4.3。
- [AUTHOR_FACT] `Select on disagreement`：答案不同时，由带 meta-thought 的 instructor 选两响应中更好者。定位：PDF p.6，式 (6)；PDF p.14，select prompt。
- [AUTHOR_FACT] `Stop-or-refresh on agreement`：答案相同时，instructor 判定两者是否已合理；是则停，否则重新生成。定位：PDF p.6，§4.3；PDF p.14，refresh/stop prompt。
- [AUTHOR_FACT] `Carry-forward after stop + hard cap`：提前停止后把该轮输出复制到后续评估轮，或到 `N` 硬停。定位：PDF p.5–6，图 4、式 (7)。

### 原文中可定位的 Failure

- [AUTHOR_FACT] `Redundant`：正确答案在多轮始终正确，准确率不变但增加调用、token 和延迟。定位：PDF p.1–2，图 1、§1；PDF p.4，§3.2。
- [AUTHOR_FACT] `Drift`：迭代中正确答案被改错，或正误摇摆；表 5 给出 Self-Correct/CRITIC 的逐轮正误转移。定位：PDF p.1–4，图 1–3；PDF p.12，表 5。
- [AUTHOR_FACT] `Stubborn/invalid iteration`：错误答案经反思仍保持错误，或不一致地变化却始终未到正解。定位：PDF p.2、p.4，§1、§3.2；图 1、图 3。
- [AUTHOR_FACT] `Instructor misjudgment`：作者在 Limitations 明示报告，oracle 评估的最终轮仍高出 IoRT 1.6 个百分点。定位：PDF p.9，Limitations。
- [AUTHOR_FACT] `Reflector can introduce a wrong answer`：表 9 中 honey-bee 初始答案正确，self-reflect 的解释仍说蜜蜂只能蜇一次，却把最终 T/F 改为错误的 True；instructor 后续 select 恢复初始答案。定位：PDF p.17，表 9。
- [AUTHOR_FACT] `Refresh/trace inconsistency`：表 13 中 Code 0 与 Code 1 在可见 PDF 里的代码均写 `occupancy_rate = 3/4`并有相同主要计算，但抽取答案分别是 30.0 与 120.0，说明又称 Code 1 用了整数除法。定位：PDF p.21，表 13。
- [AUTHOR_FACT] `Non-executable displayed refresh code`：表 14 的 Code 2 在可见 PDF 中使用 `num_flowers mod 3`/`mod 2`，不是附录 A 所说的可执行 Python 语法；而且按展示公式会得到 `9-15=-6`，但页面报告抽取答案 6.0 且标正确。定位：PDF p.23，表 14，Code 2。
- [READER_INTERPRETATION] 表 13/14 的问题是论文可见执行 trace 与报告答案不自洽，不是仅由 PDF 文本解析器造成。
- [OPEN_QUESTION] 表 13/14 是排版转写错误、实际 prompt 中的代码与展示代码不同，还是执行/答案抽取记录有错，仅凭论文无法判定。

## 8. 统一问题 7：定位索引

- [AUTHOR_FACT] 方法主定义：PDF p.4–6（印刷 p.9959–9961），§4.1–4.3，图 4，式 (1)–(7)；短定位：“三阶段流程”、“答案一致性分支”。
- [AUTHOR_FACT] 基线/主结果：PDF p.6–8（印刷 p.9961–9963），§5.1–5.3，表 1–3，图 5；短定位：“数学主表”、“StrategyQA 最终轮”、“模块消融”。
- [AUTHOR_FACT] 静态反思负向结果：PDF p.1–4、p.12，图 1–3，表 4–5；短定位：“正误转移”、“多轮非 oracle 曲线”。
- [AUTHOR_FACT] 提示与输入细节：PDF p.12–14，附录 A、C.1–C.3，表 6；短定位：“答案抽取”、“刷新/反思 prompt”、“instructor prompt”。
- [AUTHOR_FACT] 案例与可见 failure：PDF p.15–23，表 7–14；短定位：“stop/select/refresh 案例”、“执行 trace”。
- [AUTHOR_FACT] 作者限制：PDF p.9（印刷 p.9964），Limitations；短定位：“instructor 误判”、“未用开源控制器”。

## 9. 统一问题 8：解析文本与可见 PDF 是否冲突？

- [AUTHOR_FACT] 23 页均可见渲染，未发现空页、页码缺失、旋转或表格/附录整块丢失。
- [AUTHOR_FACT] PDF p.4 的图 3 图内文字在 `pypdf` 抽取中大量显示为 `/uni...` 字形编码；可见渲染中四个饼图、图例和模型标签正常。因此该页是解析局部失真，不是可见 PDF 内容缺失。
- [AUTHOR_FACT] PDF p.5 图 4 的圆圈序号和多条流程箭头无法从纯文本完整恢复，但可见渲染与图注相符。
- [AUTHOR_FACT] PDF p.8 表 3 的列头在线性文本抽取中顺序粘连；根据可见表格与同页消融叙述，可确定数值列依次是 Initial、IoRT*、IoRT(w/o SC)、IoRT(w/o MT)、IoRT。
- [AUTHOR_FACT] PDF p.21 的 `3/4`、PDF p.23 的 `mod` 和对应抽取答案在可见页面上均能复核；第 7 节指出的案例不自洽不是文本解析伪影。
- [READER_INTERPRETATION] 除上述图内字形和表头线性化问题外，正文、式 (1)–(7)、表 1–6 主数值与附录案例的解析文本和可见 PDF 未发现其他实质冲突。

## 10. 可观察文件访问与工具轨迹

- [READER_INTERPRETATION] 读取：指定 invocation（PowerShell `Get-Content -Encoding UTF8`）；指定统一 prompt（`Get-Content`）；指定 PDF（`pypdf` 逐页文本/页数，PyMuPDF + Pillow 内存渲染缩略图和局部裁剪）；PDF 处理技能指令与完成前核验技能指令（`Get-Content`）。
- [READER_INTERPRETATION] 哈希：PowerShell `Get-FileHash -Algorithm SHA256` 对指定 prompt/PDF 复核。
- [READER_INTERPRETATION] 失败尝试：对指定 PDF 调用 `pdfinfo` 时本地环境报“找不到路径”，后改用 `pypdf`；该失败未读取其他文件。
- [READER_INTERPRETATION] 为确认工具返回对象形式，执行过一次不访问文件的 PowerShell 字面量输出测试。
- [READER_INTERPRETATION] 没有网络访问；没有临时文本/图像落盘；唯一写入是使用 `apply_patch` 创建本 `report.md`。
