# P018 独立二读核源报告

## 0. 身份、边界与定位约定

- 本报告对应 invocation snapshot：`r2-20260719-p018-a1`，即 `knowledge_base/pilot/reads/P018/read_2_attempts/r2-20260719-p018-a1/invocation.md`。
- 核验对象：*ExpeL: LLM Agents Are Experiential Learners*，canonical metadata 为 arXiv:2308.10144 / AAAI 2024 official proceedings PDF。
- PDF SHA-256 已实际复算为 `01e533d81fb4a5f91797c073a9b1929acbaa64da45a592b26563ca7d135024f3`，与 invocation 一致；全文共 38 个 PDF 物理页。
- 下文“p.X”均指 PDF 物理页（标题页为 p.1），不是正文印刷页码。短定位文本只用于核源，不是完整引文。
- 本任务是独立事实核验，不生成 Card，不评价 Candidate、novelty 或科研价值。

## 1. 方法究竟改变哪一步计算？

### 1.1 总体计算路径

- [AUTHOR_FACT] ExpeL 不更新 LLM 参数，而把计算改成三个阶段：训练任务上的经验收集、从经验中抽取自然语言 insight、评估时把 insight 与相似成功轨迹加入策略提示。定位：p.3 Fig.1 与 §4；短定位：“Collection … Extraction/abstraction … Application”。
- [AUTHOR_FACT] 经验收集阶段以 ReAct 为基础；训练任务失败后，Reflexion 根据失败轨迹生成反思并重试，成功或达到最大重试/步数后，把轨迹收入经验池。定位：p.4 §4.1，p.6 Alg.1；短定位：“continuously retry … at most Z times”。
- [AUTHOR_FACT] insight 抽取有两类输入：（a）同一任务的失败/成功轨迹对；（b）跨任务抽取的 L 条成功轨迹。LLM 对已有 insight 集合执行 `ADD`、`EDIT`、`UPVOTE`、`DOWNVOTE`；新 insight 初始重要度为 2，降到 0 时删除。定位：p.4 §4.2，p.6 Alg.2，p.3 Fig.1(B)；短定位：“importance count reaches zero … removed”。
- [AUTHOR_FACT] 成功轨迹召回使用 Faiss kNN、`all-mpnet-base-v2` embedding，并按评估任务与训练任务的最大内积相似度取 top-k。定位：p.4 “Similar Experiences as Demonstrations”，p.15 Table 4；短定位：“maximum inner-product task similarity”。
- [AUTHOR_FACT] 评估时，完整 insight 列表被拼入任务规格，top-k 相似成功轨迹作为动态 few-shot；策略 LLM 在未见任务上只尝试一次。定位：p.4–5 §4.3、p.5 Fig.3、p.6 Alg.3、p.16–17 Figs.7–10；短定位：“single try”。
- [AUTHOR_FACT] 转移设置把源域 insight 与少量目标域示例交给 GPT-4 改写，再在目标任务执行时复用同一批 few-shot；由于源、目标任务不同，不进行跨域经验池检索。定位：p.5 §4.4、p.8 §5.4、p.7 Fig.4；短定位：“finetune the insights”。
- [READER_INTERPRETATION] 因而被改变的核心不是 action decoder 或环境转移函数，而是策略调用前的上下文构造：从固定人工 few-shot，变为“离线经验学习所得 insight + 检索到的成功轨迹”。训练期的 Reflexion 重试是构造该上下文所需的数据采集器，评估期仍是单次 ReAct 式决策。

### 1.2 论文中可抽取的 Operator（仅列事实化机制，不生成正式 Card）

1. [AUTHOR_FACT] **失败后反思重试并存储全轨迹**：在训练任务上用环境反馈和失败轨迹产生累积反思，直至成功/耗尽预算；p.4 §4.1，p.6 Alg.1。
2. [AUTHOR_FACT] **同任务失败—成功对比抽象**：将 failure/success pair 输入 insight LLM；p.4 §4.2，p.6 Alg.2。
3. [AUTHOR_FACT] **跨任务成功模式抽象**：无放回抽取 L 条成功轨迹形成 chunk，寻找通用 good practices；p.4 §4.2，p.6 Alg.2。
4. [AUTHOR_FACT] **带投票计数的自然语言记忆维护**：`ADD/EDIT/UPVOTE/DOWNVOTE` 和归零删除；p.3 Fig.1(B)，p.4 §4.2。
5. [AUTHOR_FACT] **任务相似度成功轨迹召回**：Faiss + MPNet + top-k 最大内积；p.4 §4.2，p.15 Table 4。
6. [AUTHOR_FACT] **评估提示注入**：拼接完整 insight，并以检索轨迹替换/扩充 few-shot；p.5 Fig.3，p.16–17 Figs.7–10。
7. [AUTHOR_FACT] **源域 insight 的目标域示例改写**：用目标 few-shot 对源 insight 做自然语言适配；p.5 §4.4，p.7 Fig.4，p.8 §5.4。

## 2. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 任务形式为确定性文本交互环境：时刻 i 接收 observation，依据历史选择 action，以达成 goal；作者明确说“only deal with deterministic environments”。定位：p.2 §3。
- [AUTHOR_FACT] 训练/经验收集输入包括训练任务、人工 few-shot、环境 observation/reward/done、此前失败轨迹与累积 reflection；输出是含成功和失败轨迹的经验池。定位：p.4 §4.1，p.6 Alg.1。
- [AUTHOR_FACT] insight 抽取输入是经验池中的失败/成功对与成功 chunk、当前 insight 集；输出是带重要度计数的自然语言 insight 集。定位：p.4 §4.2，p.6 Alg.2。
- [AUTHOR_FACT] 评估输入是未见任务、当前轨迹、完整 insight 集和 top-k 相似成功轨迹；输出为动作序列及最终成功与否。定位：p.4–5 §4.3，p.6 Alg.3。
- [AUTHOR_FACT] 干预发生在每次评估策略调用的 prompt 内。附录可视模板显示紫色区域为“Extracted Insights”和“Retrieved successful trajectories”，其余白色区域沿用 ReAct 输入。定位：p.5 Fig.3，p.16–17 Figs.7–10。
- [AUTHOR_FACT] 基准为 HotpotQA、ALFWorld、WebShop，以及仅用于转移的 FEVER；主指标为成功率，WebShop 另有 [0,1] reward，ALFWorld 另报任务类型分解。定位：p.7 §5.1，p.14 §D.4，p.36 Table 5。
- [AUTHOR_FACT] 经验收集和评估中的 policy/reflection LLM 为 `gpt-3.5-turbo-0613`（超长反思切到 16k 版本），insight 抽取为 `gpt-4-0613`；temperature 0、greedy。定位：p.7 §5.1，p.15 §D.5 与 Table 4。
- [OPEN_QUESTION] 论文没有给出线上部署时是否必须保留/访问全部训练轨迹、检索索引构建与更新的实际延迟和费用，也未把离线 GPT-4 抽取成本纳入主要效率比较。

## 3. 最强基线与最接近组合基线

- [AUTHOR_FACT] 主图把 Act 和 ReAct 作为主要 planning-agent 基线，IL 数值取自 ReAct 论文；所有本研究评估阶段 agent 均以 `gpt-3.5-turbo-0613` 采取动作。定位：p.7 §5.1，p.8 Fig.5。
- [AUTHOR_FACT] 若允许测试时重试，Reflexion 是更强且计算制度不同的比较项：作者称 HotpotQA Reflexion R3 为 40%，ExpeL 单次为 39%；ALFWorld Reflexion R3 为 54%，ExpeL 单次为 59%；WebShop 的 ExpeL 仍低于 Reflexion 成功率区间。定位：p.7–8 §5.2 “Cross-task learning”。
- [AUTHOR_FACT] ALFWorld 的精确重试序列在 Table 2 为：ReAct+Reflexion 40.3/47.8/52.2/54.4%，ExpeL retrieve-only 54.5/57.5/59.7/60.4%，ExpeL+Reflexion 59.0/60.4/63.4/64.2%（R0–R3）。定位：p.9 Table 2。
- [READER_INTERPRETATION] 因此“最强基线”必须按部署约束区分：单次评估的直接基线是 ReAct/Act；允许同一测试任务多次执行时，Reflexion R3 更强但不再是等重试预算比较。
- [AUTHOR_FACT] 与完整 ExpeL 最接近的组件组合基线是 `ExpeL (insights-only)` 和 `ExpeL (retrieve-only)`。HotpotQA 为 36%/31%，ALFWorld 为 50%/55%，WebShop 为 37%/38%；完整 ExpeL 在三域均更高。定位：p.7 §5.2，p.8 Fig.5。
- [AUTHOR_FACT] 另一近邻组合是 ExpeL+Reflexion，它把跨任务记忆与测试时同任务重试叠加，但仅在 ALFWorld 做了初步实验。定位：p.9 §5.5 与 Table 2。
- [OPEN_QUESTION] 论文没有提供与等 token、等离线 API 成本、等数量随机文本/随机成功轨迹相匹配的统一强控制，因此“同算力最强基线”无法从原文确定。

## 4. 模型、token、tool-call、prompt 与 oracle 差异核验

### 4.1 已控制或可直接核实的部分

- [AUTHOR_FACT] 评估动作模型在所有 agent 间相同，均为 `gpt-3.5-turbo-0613`，温度 0、greedy；定位：p.7 §5.1，p.15 §D.5。
- [AUTHOR_FACT] 平均 action 次数没有显示 ExpeL 一律更多：HotpotQA 4.80（ReAct 5.18）、ALFWorld 14.30（14.82）、WebShop 4.33（4.47）。定位：p.38 Table 6。
- [AUTHOR_FACT] ALFWorld 的随机成功轨迹检索为 42.5±0.8%，reason-similarity 为 48.5±2.1%，任务相似度 ExpeL 为 59.0±0.3%。定位：p.10 Table 3（下）。这部分说明“有任意轨迹”不足以解释全部差异。

### 4.2 仍然存在的差异/混杂

- [AUTHOR_FACT] 完整 ExpeL 用 GPT-4 抽取 insight，而评估 policy 与多数数据收集用 GPT-3.5。将 insight LLM 换成 GPT-3.5 后，HotpotQA 从完整 ExpeL 的 39.0±1.7% 降至 32.0±0.4%。定位：p.4 §4.2，p.9 §5.6，p.10 Table 3（上）。
- [READER_INTERPRETATION] 这说明结果的一部分可以来自更强的离线模型，而不能全部归因于经验池数据结构或投票机制。论文把这一点作为“更好基础模型带来提升”，但没有与基线共享等量 GPT-4 离线处理。
- [AUTHOR_FACT] ExpeL 每轨迹总 token 明显高于 ReAct：HotpotQA 4310.06 vs 1319.75，ALFWorld 2856.70 vs 2051.49，WebShop 3291.31 vs 2575.41。定位：p.38 Table 6。
- [READER_INTERPRETATION] 主实验不是 token-matched；完整 insight 与检索轨迹增加上下文，性能增益可能同时包含“学习内容”和“更多上下文预算”两部分。
- [AUTHOR_FACT] prompt 本身就是方法差异：附录 Figs.7–10 的紫色块显式加入 insight 与 retrieved successful trajectories；定位：p.16–17。
- [AUTHOR_FACT] WebShop 被改为确定性价格（用均值代替随机采样），每页商品从 3 增至 10；同时 IL 数值直接取自 ReAct 论文。定位：p.14 §D.3、p.7 §5.1。
- [READER_INTERPRETATION] 本文内部重跑的 Act/ReAct 与 ExpeL 共享 WebShop 改动时可直接比较；但跨论文拿来的 IL 数值是否基于相同环境版本并不清楚。
- [AUTHOR_FACT] 训练期使用成功/失败判定和环境反馈来选择轨迹并构造配对；评估期只做一次尝试，不使用测试任务重试反馈。定位：p.4 §4.1，p.6 Algs.1/3。
- [READER_INTERPRETATION] 这不是测试标签泄漏的明示证据，但训练期确实存在 reward/done oracle；其强度应与“纯无反馈提示法”区分。
- [OPEN_QUESTION] 未报告检索 embedding、top-k 拼接、完整 insight 的精确输入 token 上限或截断策略，也未做等长无信息文本控制，无法分离内容质量与上下文长度。
- [OPEN_QUESTION] “四折验证”同时被描述为“一半训练、另一半评估，再反过来”，原文未清楚解释四个 fold 如何由这两个方向及随机性组成。定位：p.7 §5.1，p.14 §D.1。
- [OPEN_QUESTION] 未报告显著性检验或逐任务配对置信区间；只给均值与 standard error，因而小幅差异（例如 FEVER 65±1.7 vs 63±0.4）不能由本文直接判为稳健因果提升。

## 5. 作者明示限制、负向结果与未测试边界

### 5.1 明示限制与边界

- [AUTHOR_FACT] 只研究文本 observation；多模态/图像 observation 未测试。定位：p.10 §6 “Limitations”。
- [AUTHOR_FACT] 只用闭源 API LLM，开放权重模型未测试。定位：p.10 §6。
- [AUTHOR_FACT] 当前 insight 尚未超过上下文窗口；真正 lifelong learning 可能需要额外 insight 检索。定位：p.10 §6。
- [AUTHOR_FACT] prompt 方法缺少强化学习式理论基础，可能影响策略效率/最优性。定位：p.10 §6。
- [AUTHOR_FACT] 任务定义限于确定性环境；随机、非平稳和部分可观测条件没有实证。定位：p.2 §3。
- [AUTHOR_FACT] 转移实验假设源/目标共享知识，且只验证 HotpotQA→FEVER（共享 Wikipedia Docstore API）。定位：p.5 §4.4，p.8 §5.4。
- [AUTHOR_FACT] Broader Impacts 指出联网 autonomous program 可能造成意外伤害，RLHF 仅被表述为“potentially mitigate”。定位：p.14 Appendix B。
- [OPEN_QUESTION] 没有研究恶意/错误经验写入、记忆污染、insight 冲突、检索隐私、人工删除错误记忆后的恢复，也没有长期在线更新实验。

### 5.2 可记录的真实负向结果/Failure

- [AUTHOR_FACT] **仅从初始 few-shot 抽 insight 没有优于 ReAct**；作者据此称额外自主经验是必要的。定位：p.9 §5.6，Fig.6；短定位：“has no advantage compared to the ReAct agent”。
- [AUTHOR_FACT] **把 reflection 也加入 insight 构造会伤害性能**：HotpotQA `Insights with reflections` 29.0±0.4%，完整 ExpeL 39.0±1.7%；作者推测 reflection 有时 hallucinate 并误导抽取。定位：p.9 §5.6，p.10 Table 3。
- [AUTHOR_FACT] **较弱 insight LLM 明显下降**：GPT-3.5 insight 32.0±0.4%，GPT-4 完整 ExpeL 39.0±1.7%。定位：p.10 Table 3。
- [AUTHOR_FACT] **人工 insight 不及自动 GPT-4 insight**：32.0±1.1% vs 39.0±1.7%。定位：p.10 Table 3、p.19 Fig.12。
- [AUTHOR_FACT] **随机/推理相似度召回不及任务相似度**：42.5±0.8%、48.5±2.1%、59.0±0.3%。作者把 reason-similarity 的下降归因于单轨迹中 few-shot 动态变化造成不稳定。定位：p.9–10 §5.6、p.10 Table 3。
- [AUTHOR_FACT] **组件在子任务上并非一致占优**：ALFWorld `clean` 中完整 ExpeL 74，低于 insights-only 87；`cool` 中完整 ExpeL 67，低于 retrieve-only 71；`heat` 完整与 retrieve-only 同为 43；`puttwo` 三个 ExpeL 变体同为 29。定位：p.36 Table 5。
- [AUTHOR_FACT] **无效动作并未在所有域降低**：HotpotQA ExpeL 0.03，ReAct 0.00；ALFWorld 2.32 vs 2.84；WebShop 0.35 vs 0.42。定位：p.38 Table 6。
- [AUTHOR_FACT] **WebShop 相对 Reflexion 仍有改进空间**。定位：p.8 §5.2；短定位：“room for improvement”。
- [READER_INTERPRETATION] 上述可作为 Failure 记录的是“明确实验条件下的下降/无增益/边界”，而不是把作者的机制猜测（例如 hallucination 或 few-shot instability）当成已证明因果。

## 6. 结果与行为证据的强弱

- [AUTHOR_FACT] 主结果为三域成功率提升，且 insights-only 与 retrieve-only 的相对优势随域而变：HotpotQA 更依赖 insight，ALFWorld 更依赖具体轨迹，WebShop 两者接近。定位：p.7 §5.2，p.8 Fig.5。
- [AUTHOR_FACT] FEVER 转移成功率：Act 58±0.0，ReAct 63±0.4，ExpeL Transfer w/o Task Demos 65±1.7，ExpeL Transfer 70±0.7。定位：p.9 Table 1。
- [AUTHOR_FACT] 作者把若干行为称为 emergent abilities，包括 HotpotQA 在信息不足时基于已有 observation 作 educated guess、ALFWorld 更新物体位置先验和错误后自我纠正。定位：p.8 §5.3，p.23–26 Figs.16–19。
- [AUTHOR_FACT] 图注和正文对因果均使用保留表达，如“possible influencing insight”“possibly encouraged”；附录 H 还说明省略了 irrelevant/non-representative steps。定位：p.8 §5.3，p.22 Appendix H，p.23–26 Figs.16–19。
- [READER_INTERPRETATION] 这些轨迹能证明行为“在所展示样例中发生”，不能单独证明特定 insight 导致行为，也不能估计行为在全测试集中的频率；“emergent”应与量化主结果分开记录。
- [OPEN_QUESTION] 未给行为标签的盲评协议、完整轨迹抽样规则、出现频率或反事实删除 insight 实验，故行为机制归因仍未解决。

## 7. 重要实现与实验定位索引

| 内容 | 定位 | 核源短语/对象 |
|---|---|---|
| 三阶段框架 | p.3 Fig.1 | experience pool → insight extraction → evaluation recall |
| 经验收集 | p.4 §4.1；p.6 Alg.1 | Reflexion training retries |
| insight 维护算子 | p.4 §4.2；p.3 Fig.1(B) | ADD/EDIT/UPVOTE/DOWNVOTE |
| 相似轨迹检索 | p.4 §4.2；p.15 Table 4 | Faiss, kNN, all-mpnet-base-v2 |
| 评估提示 | p.5 Fig.3；p.16–17 Figs.7–10 | extracted insights + retrieved trajectories |
| 主结果 | p.7–8 §5.2；p.8 Fig.5 | HotpotQA/ALFWorld/WebShop |
| 转移结果 | p.8–9 §5.4；p.9 Table 1 | HotpotQA→FEVER |
| 重试组合 | p.9 §5.5；Table 2 | ExpeL+Reflexion |
| 负向消融 | p.9–10 §5.6；p.10 Table 3 | reflection/GPT-3.5/random retrieval |
| 明示限制 | p.10 §6 | text-only, closed API, context, theory |
| 环境改动 | p.14 §D.3 | deterministic price, 10 items/page |
| 模型与日期 | p.15 §D.5/Table 4 | GPT-3.5 policy, GPT-4 insights |
| 子任务分解 | p.36 Table 5 | ALFWorld/WebShop reward |
| token/tool 统计 | p.38 Table 6 | tokens/actions/invalid actions |

## 8. 解析文本与可视 PDF 冲突检查

- [AUTHOR_FACT] 已逐页读取 38 页文本层，并逐页渲染检查可视布局；对文本层未展开的图片化内容又重点放大核对了 Figs.7–19（提示模板、insight 列表、行为轨迹），同时检查了其余图表/轨迹页的完整页面布局。
- [READER_INTERPRETATION] 未发现会改变论文结论、数值或机制描述的实质冲突。
- [AUTHOR_FACT] 存在解析层面的非语义问题：双栏正文在 p.2–10 被文本提取器交错排序；p.1 的 arXiv 页眉标记插入摘要句中；Figs.7–24 的许多框内文字是图像，普通文本层只保留图注或极少文本。这些内容在可视 PDF 中布局正常。
- [OPEN_QUESTION] “无实质冲突”仅针对本次可观察的 PDF 渲染与 PyMuPDF 文本层；没有第二套独立 OCR 引擎可用来逐字复核所有图片内小字。

## 9. Provenance 与实际 trace

### 9.1 实际读取的文件

研究内容输入严格限于：

1. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/staging/papers/P018_expel.pdf`
2. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/templates/second_read_prompt.md`
3. `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/pilot/reads/P018/read_2_attempts/r2-20260719-p018-a1/invocation.md`

另按系统强制 PDF 技能规则读取了非研究内容的操作说明：

4. `C:/Users/g/.codex/skills/pdf/SKILL.md`

未枚举工作区，未读取 read_1、Cards、其他报告、blind query 或其他项目文件；未联网。

### 9.2 工具与可观察调用

- PowerShell `Get-Content -Encoding UTF8`：读取 prompt 与 invocation；首次未指定 UTF-8 的显示发生乱码，随后以 UTF-8 重新读取。
- PowerShell `Get-FileHash -Algorithm SHA256`：复算 PDF 哈希。
- Python `PyMuPDF/fitz`：读取 PDF metadata、页数、38 页文本层，并在内存中逐页渲染。
- Python `Pillow`：在内存中生成低分辨率逐页 contact sheet 和重点页面裁剪 JPEG，用于可视检查；没有写出中间图片文件。
- 一次 `pdfinfo` 调用尝试失败（本机找不到该命令/路径）；随后用 PyMuPDF 取得 metadata 与页数。
- `pytesseract` Python 模块不可用，系统也未发现 `tesseract` 命令；因此没有声称完成独立 OCR。部分较大 base64 渲染输出达到可观察输出上限而无法处理，随后改用低分辨率 contact sheet 与分块裁剪完成可视核对。
- 写入仅限本 `report.md`。

### 9.3 模型、任务与隔离声明

- Actual model/version：Codex，GPT-5 系列；精确服务版本 `unavailable`。
- Canonical task：`/root/p018_second_read`。
- Thread ID：`unavailable`。
- 技术性 path allowlist：`unavailable`；本次为 `procedural_blinding`，不得解释为技术隔离或可验证的只读沙箱。
- 可观察 file-access trace：仅能如上报告本代理实际发起的工具调用；底层系统级不可见访问为 `unavailable`。

