# v001 失败模式证据勘探（Research Subagent 非权威草案）

- `run_id`: `20260813_1547_run10`
- `version`: `v001`
- `task_scope`: “表面成功但语义错误”的工具观测、长程状态漂移、错误放大与失败检测
- `epistemic_status`: 本文是独立子智能体草案；不构成 Candidate、Seed、Decision、Novelty 判断或主研究者裁决
- `workspace_boundary`: 只读取本 Run、`crl_agent_v3` 权威说明与冻结共享知识库；未读取任何其他 Run；未写回共享知识库

## 结论先行

1. 冻结知识库对若干关键子命题有可定位证据，但**没有一篇已核对论文直接覆盖完整因果链**：“多步工具 Agent 收到语法有效但语义错误的返回 → 在无隐藏真值下仅凭可见轨迹定位该返回 → 在等预算下选择性验证/回滚 → 独立终局成功率提高”。现有支撑分散在 false success、contract gate、stale memory、experience propagation、confidence calibration、tool-use diagnostics 与行为扰动验证中。
2. 最硬的直接边界来自 ToolGate：postcondition-gated commit 已经占据“验证后才写可信状态”的最近计算位置；但来源又明确显示 ToolBench 约 25% 无结构化 response schema 的工具被设为 `Q=True`。因此真正未被吸收的部分不是“加验证”，而是**当契约无法判定语义正确性时，如何保留 unknown、利用后续冗余定位漂移，并按预算选择验证/恢复**。
3. 失败检测不能依赖语言自信。P073 显示外观相似、执行正确性相反的工具代码轨迹可得到相近未校准不确定性；P064 又显示 vanilla LLM trajectory evaluator 可能比小型高质量标注集更损害记忆质量。单纯自评、通用反思或 LLM judge 不是可信默认检测器。
4. 存在一个必须显式写入 Claim 的可识别性边界：如果“正确世界”和“语义错误世界”在智能体全部可见轨迹上完全同分布，且没有后续约束、重复来源、行为后果或可执行不变量提供冗余，则任何无真值方法都不可能区分二者。可研究对象应收缩到**可见轨迹中存在诊断冗余，但 Agent 未能把它转化为验证/回滚决策**的错误。
5. 最可能杀死当前问题的实验事实是：在相同额外工具预算下，随机验证、固定周期验证或“总是验证最高影响步骤”已经达到同等终局收益；或者高覆盖 contract/invariant 足以捕捉绝大多数注入错误。若出现这两类结果，选择性轨迹诊断的独立方法价值会显著缩小。

## 检索记录与降级

### Snapshot 1：宽覆盖

- 路径：`hypotheses_v001/searches/subagent_failure_landscape_01/`
- 查询：
  - `problem=long-horizon tool-using LLM agent semantic observation error state drift error propagation`
  - `failure=tool returns syntactically valid but semantically wrong stale incomplete contradictory result silent failure`
  - `failure=incorrect tool observation compounds through downstream planning trajectory execution`
  - `measurement=controlled semantic tool-output corruption fault injection independent terminal success recovery detection budget`
  - `prior=trajectory verification fault localization rollback recovery selective verification tool agent`
- 覆盖：400 个原始观测、85 篇去重论文、160 个去重 Card、184 条去重 Evidence、81 个去重 Passage。
- 降级：所有 Paper/Failure/Operator/Passage 路线均 `degraded=false`；Cards FTS、Passage FTS 与向量检索均可用。1 个观测带机械噪声标记。

### Snapshot 2：稀有术语下钻

- 路径：`hypotheses_v001/searches/subagent_failure_landscape_02/`
- 查询：
  - `failure=semantic false commit`
  - `failure=observation corruption`
  - `failure=state drift downstream action`
  - `measurement=tool fault injection semantic output`
  - `problem=silent tool failure`
- 覆盖：319 个原始观测、76 篇去重论文、130 个去重 Card、157 条去重 Evidence、93 个去重 Passage。
- 降级：所有路线均 `degraded=false`；9 个观测带机械噪声标记。
- 重要稀疏信号：`observation corruption` 仅命中 2 个 Failure Card、3 个 Operator Card、4 个 Paper Card；排名靠前者主要是观测压缩和提示注入，不是自然发生的语义错误工具返回。这是**知识库直接覆盖不足**，不是研究空白证明。

### 工具执行记录

- 首次误用 `D:\Desktop\crl\env\crl_agent_v3\Scripts\python.exe`，该路径不存在；随后核对环境目录，改用 `D:\Desktop\crl\env\crl_agent_v3\python.exe`，两次正式检索均成功。
- 检索时出现 Hugging Face 未认证请求提示，但模型权重成功加载；快照中的向量路线没有报告降级。
- 未进行互联网最近工作扩展；因此本文不能承担 2026-08-13 截止的新颖性或穷尽性判断。

## 证据分层

### A. 对关键子命题的直接证据

| 论文 | 可直接支持的事实 | 定位 | 与本题的边界 |
|---|---|---|---|
| P040, *From Confident Closing to Silent Failure* | Agent 会声称任务完成，而独立环境状态显示未完成；覆盖 9,876 条 tau2-bench 与 1,879 条 AppWorld 轨迹。 | `ev-p040-failure-core`; PDF p.1；SHA-256 `ab1307...ba6a` | 直接证明 false success，不证明根因是错误工具观测，也不做在线早期定位。 |
| P074, *ToolGate* | precondition 控制可调用性，postcondition 控制返回能否进入可信符号状态；约 25% ToolBench 工具无结构化 response schema 时实现采用 `Q=True`。 | `ev-p074-contract-state-commit`, `ev-p074-missing-schema-true-postcondition`; PDF p.4；SHA-256 `7073bc...a289d` | 直接覆盖 conditional commit 与 contract 漏口；未测 schema-valid but semantically-wrong 注入下的 false commit 率。 |
| P073, *Uncertainty Calibration for Tool-Using Language Agents* | 两条外观相似的工具代码轨迹，一条错、一条对，却得到相近未校准 uncertainty；修复使用 execution-result-supervised MLP probe。 | `ev-p073-internal-confidence-misalignment`（PDF p.3）, `ev-p073-execution-supervised-probe`（PDF p.2）；SHA-256 `2c56eb...cc53` | 直接反证“语言/内部置信度等于执行成功率”；监督 probe 需要离线真值，不是本题的无真值在线解。 |
| P039, *ToolFailBench* | 总任务准确率会把 Tool-Skip 与 Result-Ignore 混在一起；论文分离 skipping、ignoring、fabrication、unnecessary use。 | `ev-p039-aggregate-score-masking`（PDF p.1）, `ev-p039-failure-core`（PDF p.3）；SHA-256 `6588af...3009` | 可用于阶段化诊断，但 PDF p.7 明确其 single-turn format 不覆盖 tool chaining、早期错误恢复和跨交互状态更新。 |
| P007, *tau-bench* | 终局评价比较 episode 末数据库状态与 ground-truth expected state；retail `pass^8 < 25%` 暴露重复可靠性塌缩。 | `ev-p007-terminal-state-evaluation`（PDF p.2）, `ev-p007-repeat-reliability-collapse`（PDF p.1）；SHA-256 `e2d45d...ada0` | 提供独立终局与重复可靠性载体，不包含受控语义错误工具返回注入。 |
| P037, *ToolSandbox* | Milestone DAG 允许多条合法状态轨迹；Minefield 对禁止事件施加零分。 | `ev-p037-evaluation-core`, `ev-p037-minefield-violation`; PDF p.5；SHA-256 `3449ba...6173e` | 可承载过程/终局测量；human-authored milestones 可能把过程先验写进评测。 |

### B. 相邻证据

| 论文 | 相邻事实 | 定位 | 为什么只能算相邻 |
|---|---|---|---|
| P030, *STALE* | 识别旧记忆不等于把新状态用于下游行为；示例从 Type-I SR 76.0% 降到 IPA 39.0%。 | `ev-p030-failure-core`, `ev-p030-recognition-application-gap`; PDF p.7；SHA-256 `388f71...5109` | 对“识别—应用断裂”是直接证据，但载体是记忆冲突，不是工具返回污染。 |
| P064, *How Memory Management Impacts LLM Agents* | 错误 retrieved experience 会被复制、放大，并在回写后传播到未来任务；vanilla LLM trajectory evaluator 可能损害记忆质量。 | `ev-p064-experience-following-error`（PDF p.2）, `ev-p064-evaluator-reliability`（PDF p.5）；SHA-256 `2c3992...0400` | 对错误放大直接，但机制经过长期记忆检索/回写；不能自动外推到单条在线轨迹。 |
| P095, *Don't Ask the LLM to Track Freshness* | LLM 存在 prior-override 与 serial-comparison drift；上下文增大时 freshness baseline 75%→61%，deterministic max pipeline 的 matched 比较为 +10.8pp。 | `ev-p095-prior-override-drift`（p.3）, `ev-p095-matched-comparison`（p.1） | 有显式全序 serial 标记，是比自然 API 语义一致性更强的结构信息；且增益是 whole-pipeline attribution。 |
| P097, *ReLoop* | 优化代码可 91.1% solver-feasible 但仅 0.5% formulation-correct；语法/可执行性成功不代表语义正确。 | `ev-p097-feasibility-gap`; PDF p.2；SHA-256 `856365...4c66` | 强力相邻反例，但对象是优化建模代码而非通用工具观测。其行为扰动需要可执行、可扰动的领域不变量。 |
| P013, *Large Language Models Cannot Self-Correct Reasoning Yet* | 无外部反馈时，自我修正可能退化；等模型响应数比较下也可能劣于无自修正方法。 | `ev-p013-intrinsic-self-correction-degrades`（PDF p.1）, `ev-p013-oracle-free-equal-budget-boundary`（PDF p.2）；SHA-256 `d172f0...042a` | 是推理任务证据，不直接覆盖工具环境；但要求把通用反思纳入等预算基线。 |
| P003, *LATS* | WebShop 中通用反思往往无用并陷入局部最小；完整 LATS 通过 selection/expansion/evaluation/simulation/backpropagation/reflection 改变搜索。 | `ev-p003-generic-reflection-local-minimum`（PDF p.8）, `ev-p003-search-control-loop`（PDF p.5）；SHA-256 `a6b846...ab19` | 表明“反思”本身不够，但 LATS 的多个组件和 rollout 预算共同变化。 |

### C. 当前仅能作为推断的命题

- [INFERENCE] 错误工具返回一旦被写成 accepted state，可能像 stale memory 或 retrieved experience 一样取得后续决策权并放大；目前没有本库直接实验把这条迁移链完整测出。
- [INFERENCE] 后续工具调用的参数、跨返回一致性、任务约束冲突和行为后果可形成“不依赖隐藏真值”的诊断冗余；尚无证据说明这些信号在真实多步任务中足以稳定定位首个污染转移。
- [INFERENCE] 将每个状态转移标成 `trusted / suspect / unknown`，并把验证预算分配给预期下游影响高且诊断冗余强的步骤，可能优于统一重试；这是待实验假设，不是现有文献结论。
- [INFERENCE] 可逆任务中的 rollback 与不可逆副作用任务中的 compensating action 不是同一算子；若混用，会把恢复能力夸大。

## 可反证失败模式

### FM-1：契约通过后的语义假提交

- 定义：工具返回语法、类型和值域均合法，甚至满足不完整 postcondition，但关键实体、时间、聚合值或隐含约束错误；Agent 将其写入可信状态。
- 可观察签名：`false_commit_rate` 上升；第一次污染转移后，后续参数与独立终局偏离；schema-only / ToolGate-style gate 对该错误子集召回低。
- 反证条件：在预注册的 schema-valid semantic corruption 下，高覆盖 contract/invariant 已以很低误报捕获绝大多数错误，或 corruption 不改变后续决策与独立终局。
- 证据等级：P074 对 gate 与 `Q=True` 漏口是直接证据；“漏口导致长期漂移”仍为推断。

### FM-2：识别—应用断裂造成持续漂移

- 定义：Agent 在语言中指出某返回可疑、陈旧或矛盾，却没有撤销其决策权；后续工具参数与计划继续依赖该状态。
- 可观察签名：高 detection recall 但低 repair uptake；`suspect` 标记后仍出现依赖污染节点的调用；终局成功没有同步提高。
- 反证条件：一旦 Agent 正确识别问题，其后续策略几乎总能隔离/替换该状态，识别率与恢复率高度一致。
- 证据等级：P030 对 memory recognition/application gap 是相邻直接证据；迁移到工具返回是推断。

### FM-3：早期错误的路径放大

- 定义：一个早期错误观测被压缩进计划摘要、工具参数、缓存或后续记忆，产生多个衍生错误；越晚验证，恢复成本越高。
- 可观察签名：注入位置越早或下游依赖出度越高，terminal failure、错误调用数与 rollback cost 越大；删除首个污染节点后多个下游错误同时消失。
- 反证条件：控制错误类型与严重度后，注入位置/依赖出度与终局损害、恢复成本无稳定剂量—反应关系；或 Agent 后续自然覆盖错误状态。
- 证据等级：P064 对 memory-based propagation 是相邻证据；当前轨迹内因果放大需要新实验。

### FM-4：自信与语言一致性盲区

- 定义：正确与错误轨迹表面相似，Agent 自报置信度、token confidence、通用 LLM judge 或自我反思无法区分，甚至把同源误读再次确证。
- 可观察签名：错误/正确样本的 confidence 分布重叠；等预算 self-reflection/self-consistency 对语义错误召回接近随机，或修坏原本正确轨迹。
- 反证条件：仅用可见轨迹训练或构造的检测器在未见错误类型、任务域和模型上仍保持良好校准，并显著优于随机、max-confidence 和 generic judge。
- 证据等级：P073 是工具执行轨迹的直接证据；P013、P003、P064 提供相邻负向边界。

### FM-5：验证预算错配

- 定义：统一重试/固定复查把预算花在低风险步骤，或重复同一生成过程得到相关错误；真正高影响污染节点未被验证。
- 可观察签名：相同额外调用数下，固定/随机验证的验证命中率低；收益主要来自增加总调用而非选择策略；多次重试输出高度相关。
- 反证条件：随机或固定周期验证在多个预算点上与拟议选择策略等价，或者“全部多调用一次”在相同总成本下稳定更优。
- 证据等级：等预算自我修正负结果由 P013 相邻支持；“下游影响感知分配更好”目前纯属待证假设。

## 强基线与公平比较要求

| 基线 | 必须配平的资源 | 它最可能吸收/杀死的主张 |
|---|---|---|
| 无验证 ReAct/原 Agent | 同模型、工具、任务、采样参数 | 给出 corruption 的原始损害与自然恢复率。 |
| 固定一次重试 / 固定周期验证 | 相同额外工具调用数、token、延迟 | 若已达到同等终局收益，则选择性分配没有价值。 |
| 随机选择步骤验证 | 相同预算与可验证候选集合 | 检验 selector 是否真有定位信息，而非验证本身有效。 |
| 按静态下游依赖出度或手写风险排序 | 相同轨迹图与预算 | 检验学习/语言判断是否胜过简单结构启发式。 |
| 自洽采样 / 独立轨迹多数或一致性选择 | 相同总模型响应数与工具调用数 | 检验收益是否只是更多采样；P013 要求等响应数比较。 |
| 通用事后反思 / LLM judge | 相同上下文、次数、停止条件 | 检验具体故障定位是否优于提示式自审；P003/P064 是负向边界。 |
| LATS 式搜索与回溯 | 相同 rollout 数、评价调用、工具预算 | 检验“风险定位”是否只是更充分搜索。 |
| ToolGate 式 contract-gated commit | 同一 contract 信息；另报 contract coverage | 最近计算基线；可能直接吸收 schema/值域可判错误。 |
| Bounded pre-execution reviewer（P049） | 相同 reviewer 次数与延迟 | 区分“调用前动作错误”与“调用后观测错误”；不能把前者修复算作本题收益。 |
| ProbeCal 式 outcome-supervised probe（P073） | 单独披露训练标签与 hidden embedding 权限 | 若允许离线终局标签，这是强监督基线；若本题禁止该信息，应标为非同信息上界而非公平基线。 |
| Oracle fault locator / oracle rollback | 仅作上界，不参与公平胜负 | 估计检测与恢复各自的最大可得收益，防止把恢复器上限误归因给 selector。 |

公平性还应报告：每类工具故障的预算—成功曲线、验证调用的实际命中率、误验证率、首次污染定位误差、回滚/补偿成本、正常无故障任务的性能损失，以及不同方法新引入错误的数量。

## 测量路径与证据缺口

### 可复用的已知测量部件

- P007：独立数据库终态与 `pass^k`；适合避免把 Agent 的关闭语句当作成功。
- P037：Milestone/Minefield DAG；适合容纳多条合法路径与禁止事件，但需防止过程标签泄漏给方法。
- P039：Tool-Skip / Result-Ignore / Fabrication / Unnecessary Use 分解；应扩展一个独立的 `Wrong-Observation-Commit` 与 `Detected-But-Used` 类别。
- P040：false-success 标签；适合作为终局后检测，不足以定位早期污染。
- P097：行为扰动“预期敏感性是否存在”；可作为特定工具域的外生可执行不变量，不应泛化成所有工具均可扰动。

### 关键缺口

1. **直接任务载体缺口**：未找到同时具备多步状态、语法有效语义错误注入、可控注入位置/类型、独立终局、等工具预算的现成基准。
2. **定位真值缺口**：终局失败不能唯一标注首个致因转移；需要注入日志或受控反事实 suffix rollout 作为实验期标签，但不能在测试时泄漏给候选。
3. **错误分类缺口**：陈旧、错误实体、局部缺失、相互矛盾、错误聚合和隐藏副作用的可识别性不同，不能只报一个 corruption 平均数。
4. **可识别性缺口**：需要预注册“轨迹中有何独立冗余”，例如跨工具一致性、任务约束、可执行不变量或后续行为后果；否则无真值检测主张不可证伪且可能信息论上不可能。
5. **恢复语义缺口**：数据库写入、邮件发送、支付等不可逆动作不能用简单 rewind；应区分纯内部状态回滚、幂等重试、补偿事务和不可恢复失败。
6. **预算归因缺口**：必须在多个额外调用预算点比较随机、固定、全验证和选择性验证，并核算 token、工具延迟及 reviewer 调用。
7. **分布外缺口**：检测器可能只学到注入模板、错误长度或工具名；需要未见错误生成器、未见工具域、未见基础模型与自然错误样本。
8. **最近工作缺口**：本子任务未做实时来源与引文扩展；任何“尚无人研究”的表述都不成立。

## 最可能杀死本问题的事实（按杀伤力排序）

1. **不可识别性成立**：在目标错误分布上，错误与正确返回的可见轨迹没有稳定冗余；所有 trajectory-only selector 在未见分布上与随机相当。此结果会杀死无外部真值的广义检测主张，只能收缩到具有可执行不变量或交叉来源的子域。
2. **强基线吸收**：ToolGate 的高覆盖 postcondition、简单 deterministic invariant 或静态依赖风险规则已覆盖大部分错误；新方法只剩 prompt/排序微调。
3. **预算解释全部收益**：固定重试、随机验证或自洽采样在相同调用/token/延迟下与候选相当，说明收益来自额外计算而非定位机制。
4. **根因错置**：P040 式 false success 主要由错误计划、调用选择、参数或用户模拟造成，而非语义错误工具返回；人为注入虽能制造效果，却不对应自然高频故障。
5. **注入伪影**：候选通过格式、长度、措辞或特定生成器识别 corruption；换错误生成器、工具域或模型后优势消失。
6. **恢复不可执行**：关键外部副作用不可逆或补偿代价过高；即便准确检测，终局成功也无法改善，方法只能做报警而不是恢复。
7. **检测—应用再次断裂**：selector 能标出风险，但 Agent 不会真正隔离状态、回滚依赖或重规划，复现 P030 的 recognition/application gap。

## 给主研究者的最小高信息量检查建议（非 Candidate）

在进入完整 implementation 前，可构造一个小型、可审计的二维试验：

- 轴一：错误可识别性——`有冗余`（后续返回/任务约束与错误冲突）对 `无冗余`（直到隐藏终局才可知）。
- 轴二：下游影响——`低依赖出度` 对 `高依赖出度`。
- 在固定 1 次额外工具调用预算下比较：随机验证、静态依赖出度、LLM 自评、contract gate、候选诊断信号。
- 预注册：首个污染定位准确率、false commit、detected-but-used、终局成功、额外调用、正常任务损失。

如果方法只在“有冗余、高出度”格有效，这是可解释的收缩边界；如果在“无冗余”格声称普遍检测，优先检查泄漏或注入伪影。
