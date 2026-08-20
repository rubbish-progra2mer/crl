# P086 独立二读报告

## 1. 读取身份与来源绑定

- Attempt ID：`r2-20260720-p086-a1`
- 角色：fresh independent source reader
- 唯一论文来源：`knowledge_base/staging/plan06_prior_gap/P086_meta_tool.pdf`
- PDF 实测：955,613 bytes；25 个物理页；SHA-256 `02064499a8345eb333e4fdd71abaa5ee69133af5be7b81626ba09816f48d194b`，与 invocation 一致。
- 本报告中的页码均为 PDF 从 1 开始的物理页码，不是论文印刷页码。
- 标签含义：`AUTHOR_FACT` 是论文直接陈述或表格数值；`AUTHOR_INTERPRETATION` 是作者对结果的解释；`AUDIT_JUDGMENT` 是本次独立二读判断。

## 2. Canonical metadata

`AUTHOR_FACT`

- 标题：*Meta-Tool: Unleash Open-World Function Calling Capabilities of General-Purpose Large Language Models*。
- 作者：Shengqian Qin、Yakun Zhu、Linjie Mu、Shaoting Zhang、Xiaofan Zhang（通讯作者）。
- 单位：Shanghai Jiao Tong University、SII、SPIRAL Lab。
- 出版信息：*Proceedings of the 63rd Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers)*，pp. 30653–30677，2025-07-27 至 2025-08-01。
- 定位：物理页 1，标题区、作者区及页脚会议行；PDF 元数据未填写 title/author 字段，因此 canonical metadata 取自论文页面本身。

## 3. Hypothesize–retrieve–invoke 的实际计算

`AUTHOR_FACT`

1. **Hypothesize**：LLM 先自主判断当前 system instruction 中没有合适工具，再调用标准 JSON 工具 `meta_tool`。该调用只有两个必填字段：`tool_description`（所需外部工具功能的自然语言描述）和 `param_description`（所需工具各参数描述组成的字符串数组）。短定位语：`"Use this tool when no suitable tool is available"`。定位：物理页 2，§1；物理页 3，§3.1；物理页 14，§A.4 / Figure 4。
2. **Retrieve**：对假想工具查询 `t_q` 与候选库工具 `t_v`，嵌入模型 `E` 分别编码工具描述 `des_t` 和参数描述 `des_p`。论文实验使用 `intfloat/multilingual-e5-large`。定位：物理页 4，§3.1；物理页 6，§4 “Experimental Setup”；物理页 16–17，§A.6 / Algorithm 1。
3. **Score**：Algorithm 1 给出
   - `S_t = cos_sim(e_t^q, e_t^v)`；
   - 对查询工具的每个必需参数 `i`，在候选工具的必需参数描述中取最大相似度：`S_p[i] = max_j cos_sim(e_p^q[i], e_p^v[j])`；
   - `S_p^mean = mean(S_p)`；
   - `tool_similarity = alpha * S_t + (1-alpha) * S_p^mean`。
   主实验设置 `alpha = 0.5`。定位：物理页 4，§3.1，短定位语 `"For each required parameter"`；物理页 16–17，§A.6 / Algorithm 1。
4. **Return and invoke**：retriever 在每条 function-missing 对话的预定义 1,000-tool pool 中排序，返回 top 5 工具定义；LLM 读取返回的名字、描述和参数 schema，再调用被选工具。定位：物理页 6，§3.3.1 “Category”与 §3.3.2 “Tool Retrieval”；物理页 18，Figure 12。

`AUDIT_JUDGMENT`

- 论文正文明确说相似度作用于嵌入；Algorithm 1 第 7 行排版却写成对 `des` 做 `cos_sim`，而不是前四行定义的 `e_p`。结合前后文，合理读取是“参数描述嵌入的余弦相似度”，但该符号不一致应保留为实现复现歧义，不能无提示改写成另一个算法。
- 参数匹配是逐个 query-required-parameter 的独立最大匹配；算法没有一一匹配、候选参数复用惩罚、参数个数差惩罚，也未定义 query required-parameter 为空时的 `mean([])` 行为。
- 参与检索的是工具描述与必需参数的**描述文本**。工具名、参数名、类型、枚举、默认值、可选参数、嵌套结构和跨字段约束没有进入 Algorithm 1 的显式分数。

`AUTHOR_INTERPRETATION`

- 作者把与关键词匹配的差别概括为：Meta-Tool 不只匹配工具本身，还考虑参数效果；假想描述即使不完全准确，也可用于检索。定位：物理页 3–4，§3.1 / Figure 2(a)。
- `alpha` 消融显示工具描述权重更重要，但适当加入参数描述有益；作者认为较优范围为 0.65–0.8，而不是主实验固定的 0.5。定位：物理页 20，§A.9 “The influence of Alpha”；物理页 22，Table 6。例如 Qwen 的 HR@1 从 `alpha=1.0` 的 38.00 上升到 `alpha=0.65` 的 59.75；LLaMA 从 59.75 上升到 68.25；Ours 在 `alpha=0.8` 为 62.50、在 `alpha=1.0` 为 60.00。

## 4. Meta-Bench：数量、类别与工具池

`AUTHOR_FACT`

- 总量：2,800 个 dialogues、7,361 个 tools；支持 multi-turn、open-world function calling 和 irrelevance detection。定位：物理页 1 摘要；物理页 2；物理页 3，Table 1；物理页 5，§3.3.1 / Figure 3。
- 论文称有 10 个场景。按 Figure 3 的层级组合可还原为：
  1. open-world/simple/chat；
  2. open-world/hard/chat；
  3. closed-world/simple/chat；
  4. closed-world/hard/chat；
  5. open-world/simple/function missing；
  6. open-world/hard/function missing；
  7. open-world/simple/function existing；
  8. open-world/hard/function existing；
  9. closed-world/simple/single-tool call；
  10. closed-world/hard/multi-tool call。
- Figure 3 的工具领域图例列出 29 类：Art、Artificial Intelligence、Automation、Commerce、Communication、Construction、Cybersecurity、Data、Devices、Economics、Education、Energy、Engineering、Entertainment、Environment、Events、Food、Gaming、Health、History、Lifestyle、Logistics、Medical、Nutrition、Others、Politics、Psychology、Science、Travel。定位：物理页 5，Figure 3（视觉复核）。
- simple/hard 依据对话内 function-call 次数划分，meta-tool 调用不计入；simple 删除 unused tools，hard 保留 unused tools，若不足则加入 irrelevant tools 直至 system-instruction 中相关候选总数达到 5。定位：物理页 5–6，§3.3.1 “Difficulty”。
- open-world 提供 meta-tool 访问外部库；closed-world 从 system instruction 中移除 meta-tool。定位：物理页 5–6，§3.3.1 “Open-world Function Calling”。
- function-missing 的检索 operational domain 是每条对话独立构造的 1,000-tool pool，其中包含 ground-truth invoked tools；检索返回 top 5。定位：物理页 6，§3.3.1 “Category”与 §3.3.2 “Tool Retrieval”。

## 5. 数据构造与 train/test 关系

`AUTHOR_FACT`

- 来源是完整 ToolACE 与 Glaive function-calling-v2 的一个子集。训练来源计数为：Glaive 中 2,000 条无工具 chat、2,000 条 single-tool dialogues，以及 ToolACE 的 8,591 条 dialogues；增强后训练数据总计 34,208 data points。定位：物理页 4–5，§3.2；物理页 11，§A.1–A.2。
- 原 instruction 中的工具按整段会话是否实际被调用分为 invoked tools 与 unused tools。删除 invoked tools、插入 meta-tool，再在目标工具首次调用前插入一次 meta-tool call 与返回结果；同一工具后续重复调用不再重复插入。定位：物理页 4，§3.2；物理页 11–12，§A.2；物理页 17–18，Figures 11–12。
- 为降低“查询描述与返回 schema 完全相同”的人工痕迹，使用 LLM 重写 meta-tool 的工具/参数描述；重写前后相似度低于 0.90 时迭代重写。另由更强 LLM 生成调用前的三步 reasoning supervision。定位：物理页 5，§3.2；物理页 12，§A.2–A.3；物理页 15，Figures 7–8。
- 验证包括：合法 JSON；函数名必须是 `meta-tool`；只允许 `tool_description`、`param_description` 且二者齐全；重写相似度；以及 GPT-4o 对 hallucination、consistency、multi-step reasoning 的二值检查。定位：物理页 5，§3.2；物理页 12–13，§A.3；物理页 16，Figure 9。
- 一半训练样本随机加入 meta-tool 相关对话；另一半删除 meta-tool turns，形成 closed-world 训练。Meta-Bench 从剩余数据随机抽样，dialogue 与训练集不重叠，但论文明确说二者分布“nearly identical”，且两边可能出现功能相同或相似的工具。定位：物理页 11，§A.1，短定位语 `"does not overlap"` 与 `"nearly identical"`。

`AUDIT_JUDGMENT`

- benchmark 的 dialogue-level 不重叠不等于工具或功能谱系隔离；本来源不支持据此声称对新分布、新工具 schema 或真实开放世界的 OOD 泛化。
- 训练中的 meta-tool target 从真实 invoked tool 反向构造，再做相似度至少 0.90 的改写；它模拟了假想查询噪声，但仍由答案工具生成，和部署时仅凭用户需求自由假想的 query distribution 不同。

## 6. Baselines、检索指标与关键结果

### 6.1 三种检索路径

`AUTHOR_FACT`

- **Dialogue History-Based**：被动地把 user query/dialogue history 直接与标准 tool JSON 做相似度；不让模型决定何时检索。定位：物理页 4，Figure 2(a)；物理页 6–7，§4 “Tool Retrieval Baseline Methods”。
- **Keyword-Based**：把 `ToolSearcher` 放入 prompt，由 LLM 自主决定调用并生成 keyword；keyword 与“tool name + tool description”的拼接文本做相似度。定位：物理页 7，§4；物理页 14，Figure 5。
- **Meta-Tool**：LLM 生成工具描述与参数描述，再按 Algorithm 1 的双通道分数检索。定位：物理页 3–4，§3.1；物理页 16–17，§A.6。

### 6.2 指标定义

`AUTHOR_FACT`

- **FMD (Function Missing Detection)**：模型发现缺失函数并以规定参数成功调用 meta-tool/ToolSearcher 的比例。
- **HR@1/3/5**：ground-truth tool 是否出现在返回排序的前 1/3/5 个。
- **T-Acc**：被调用工具名与 ground truth 对齐才正确。
- **P-Acc**：调用的全部参数值与 ground truth 精确匹配才正确。
- **IRR**：chat 中工具无关或信息不足时，调用任何工具均错，不调用工具才对。
- 定位：物理页 6，§3.3.2 “Common Function Calling / Tool Retrieval / Irrelevance Detection”。

### 6.3 Table 3 的关键检索结果（单位：%）

`AUTHOR_FACT`

| 方法/模型 | Simple FMD | Simple HR@1/3/5 | Hard FMD | Hard HR@1/3/5 |
|---|---:|---:|---:|---:|
| Dialogue History-Based | 100.00 | 63.45 / 81.81 / 88.13 | 100.00 | 0.49 / 1.30 / 1.83 |
| Keyword-Based / GPT-4o | 99.25 | 69.25 / 83.00 / 87.00 | 49.13 | 15.90 / 19.08 / 21.30 |
| Meta-Tool / GPT-4o | 98.00 | 63.75 / 83.00 / 89.25 | 60.89 | 34.18 / 46.10 / 49.13 |
| Keyword-Based / LLaMA-3.3-70B | 100.00 | 66.00 / 82.25 / 87.00 | 40.06 | 23.53 / 28.46 / 30.68 |
| Meta-Tool / LLaMA-3.3-70B | 100.00 | 67.25 / 86.25 / 92.00 | 62.80 | 34.82 / 46.26 / 50.24 |
| Meta-Tool / MT-LLaMA-8B | 92.25 | 53.00 / 69.50 / 74.75 | 75.75 | 33.54 / 45.83 / 48.66 |

定位：物理页 8，Table 3（表格视觉复核）。

`AUTHOR_INTERPRETATION`

- 作者认为 dialogue-history baseline 在 simple、尤其 single-turn 中好，但在 hard 中几乎失效；Meta-Tool 在 simple 与 hard 上整体优于 keyword-based。作者还强调 MT-LLaMA 的 hard FMD 比 GPT-4o 高 14.86 点、比其 LLaMA-3.1-8B base 高 28.20 点，但其 desired-tool 描述生成质量仍落后于更大的开源模型。定位：物理页 8，§4.2。

`AUDIT_JUDGMENT`

- Table 3 将“是否激活检索”（FMD）与“激活后 query 的排序质量”（HR）同时展示，这是必要区分；例如 MT-LLaMA 的 hard FMD 最高不意味着其 hard HR@1 最高，LLaMA-3.3-70B 的 HR@1/5 略高。
- dialogue-history 行的 FMD=100 是被动检索设置的操作性常量，不是模型成功识别 function missing 的能力证据。

## 7. Function-missing 后的选择、参数与 irrelevance

`AUTHOR_FACT`

Table 2 的代表性结果如下（T-Acc / P-Acc；IRR 单列，单位：%）：

| 设置 | GPT-4o | MT-LLaMA-8B |
|---|---:|---:|
| Simple open-world function missing | 91.50 / 72.00 | 96.75 / 69.50 |
| Hard open-world function missing | 78.81 / 49.85 | 81.49 / 46.32 |
| Simple open-world function existing | 97.75 / 77.25 | 94.00 / 69.25 |
| Hard open-world function existing | 74.09 / 29.54 | 84.26 / 45.52 |
| Simple open-world IRR | 11.30 | 95.07 |
| Hard open-world IRR | 2.00 | 28.00 |
| Simple closed-world IRR | 24.54 | 99.39 |
| Hard closed-world IRR | 6.00 | 56.00 |

定位：物理页 7，Table 2（表格视觉复核）。Table 4/5 的消融还显示，在 hard setting 中，MT-LLaMA 加 reasoning 后 function-missing T/P 从 23.51/17.05 升至 81.49/46.32；加入 `get_user_input` 后 open-/closed-world IRR 从 16/45 升至 28/56。定位：物理页 19–21，§A.9 / Tables 4–5。

`AUDIT_JUDGMENT`

- T-Acc 与 P-Acc 是 exact-match 调用指标，不是工具真实执行成功率；多数行 P-Acc 明显低于 T-Acc，说明检索/选对工具与填对参数是不同失败面。
- `get_user_input` 被训练为一个特殊“nonfunction”，但 IRR 的定义是“不调用任何工具”；论文将这种训练机制用于保持对话能力，评测表中的 IRR 仍不能解释成真实环境下澄清问题质量。

## 8. Generation、distribution 与 end-to-end 边界

`AUTHOR_FACT`

- 论文的“open-world”仍指访问**预定义外部工具库**，不是网络上无界发现工具。摘要、Figure 1 与 §3.3.2 均如此表述；function-missing 实验更具体地限制为每例 1,000-tool pool。
- retrieval 的 ground truth 是目标工具是否命中 top-k；后续 common function calling 以工具名和参数值 exact match 计分。论文没有报告真实 API 执行、环境状态改变或最终任务结果正确性。
- Limitations 只在 LLaMA-3.1-8B 上实施 fine-tuning；为检查一般能力是否受损，作者迄今只做了 irrelevance detection，称更多实验留待未来。定位：物理页 9，“Limitations”。

`AUDIT_JUDGMENT`

- **Generation boundary**：核心 query 是 LLM 生成的自然语言工具/参数描述，系统效果同时依赖 function-missing 判定、描述生成和 retriever；Table 3 虽分开 FMD 与 HR，仍没有独立标注 query 语义完整性、参数遗漏率或描述校准。
- **Schema boundary**：这是直接的“参数描述/required-parameter-aware retrieval”先行，不只是调用后 output validation；但它只利用 schema 的自然语言描述切片，不是完整 JSON Schema 推理。
- **Distribution boundary**：train/test dialogue 不重叠，但来源相同、分布近乎一致，且功能相同或相似工具可跨 split；因此不能把结果外推为跨库、跨 schema 风格、跨领域或时间漂移稳健性。
- **End-to-end boundary**：链条实际覆盖“决定检索 → 生成 meta-tool query → 静态库 top-k → 读取返回 schema → 生成 exact-match function call”；未覆盖真实工具可用性、权限/安全、参数运行时约束、API 错误、延迟/成本、工具版本漂移、执行结果真实性、结果整合与用户任务最终成功。

## 9. 与 parameter/schema-aware retrieval 的 prior 关系

`AUDIT_JUDGMENT`

- **结论：这是 direct prior，不是 only output validation。** Algorithm 1 在调用目标工具之前，直接把 required-parameter descriptions 纳入 retrieval score；Figure 2(a) 也把“双重考虑工具与参数效果”作为方法差异。
- 若待审主张仅是“在语义工具检索中加入参数/必需字段描述会改善召回”，本论文构成高度直接的 method/claim prior，且有 `alpha` 消融支持。
- 若待审主张是“完整 schema-aware retrieval”，本论文是强 partial prior 而非完全相同：它没有显式比较参数名、类型、枚举、optional/required 结构差异、嵌套 schema、约束满足或参数间依赖；其 `max` 聚合也不是 schema 对齐或可执行性验证。
- 论文确有 output/data validation（JSON 格式、重写相似度、GPT-4o reasoning 检查），但那是训练数据构造的质量控制，不能替代或抹去其前置检索 computation。

## 10. Runtime provenance 与可观察 trace

- Start time（invocation）：`2026-07-20T20:46:09+08:00`
- End time（报告内容完成并进入最终机械核验）：`2026-07-20T21:00:20.5246772+08:00`
- Task ID：`/root/p086_second_read`；Attempt ID：`r2-20260720-p086-a1`
- 模型可见标识：`Codex / GPT-5 family`；更细的模型构建号或版本号未向本代理暴露，未猜测。
- Internet access：未联网；未调用 web、浏览器、外部 API 或插件。
- 实际读取范围：工作区根 `AGENTS.md`；`crl_agent_v3/AGENTS.md`；`crl_agent_v3/CRL.md`；`crl_agent_v3/CRL_ENVIRONMENT.md`；`C:/Users/g/.codex/skills/pdf/SKILL.md`；指定 `invocation.md`；指定 P086 PDF 的全部 25 个物理页；以及本报告写后机械核验。未读取或枚举 invocation 禁止的资产。
- 可观察命令/工具轨迹：
  - PowerShell `Get-Content -Encoding UTF8` 分段完整读取治理文件、PDF skill 与 invocation；`Get-Item` / `Get-FileHash` 仅核对这些已授权文件的行数、bytes 与 SHA。
  - 使用项目固定解释器 `D:/Desktop/crl_judge/crl_agent_v3/.venv/python.exe` 与 PyMuPDF 1.28.0，仅对指定 PDF 在内存中执行 bytes/SHA/page-count/metadata、逐页文本抽取、页 5 span 坐标检查，以及物理页 4、5、7、8、17 的局部/整页栅格视觉复核；未保存抽取文本或图片。
  - 首次多页抽取因 PowerShell stdout 的 GBK 编码遇到字符 `©` 而退出码 1；设置进程级 `PYTHONIOENCODING=utf-8` 后重试。一次 1–5 页批量输出被工具显示层截断，随后以较小页组重读。早期两次内存 PNG 传输因工具输出截断无法显示，改用低质量灰度 JPEG；均未写文件。物理页 22 的一次局部裁剪为空白，Table 6 数值来自同页全文文本抽取。
  - 使用 `apply_patch` 新增本 `report.md`；未修改其他文件。
- 随机种子：未设置。预算：未设置。没有运行科研实验或模型推理 API。
- Output report SHA-256：在写入并完成 UTF-8/LF 机械核验后回填于交接消息；不在正文自指哈希中写入，以避免修改正文后使哈希失效。
- Mechanical result：PASS——初稿写后严格 UTF-8 解码成功、无 BOM、无 CR、以 LF 结尾；最终文件按同一条件再次核验，并在交接消息报告最终 bytes/SHA-256。
