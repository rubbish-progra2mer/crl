# CRL Fixed Review Packet

- Contract: 3
- Scientific version: v001
- Evaluator: CRL-EVAL-1.0
- Evaluator definition SHA-256: e0d35083b1427e9f8861ba576304b97657498fee46480d5e07e8e0b02cea6e5b
- Implementation key: 8d4b260c29a16166f69a628cc457cd675d2815b6782a376f82dcd2f27f2fe60b
- Implementation manifest SHA-256: 8d4b260c29a16166f69a628cc457cd675d2815b6782a376f82dcd2f27f2fe60b
- Evidence inventory SHA-256: 37a3584d7b79c77fe8dc89bcc0bfce231ad17e2995d2f1841228b05d0406b5cb

## 1. Implementation / Seed Overview

### Source: `seed_v001.md`

# 研究种子 v001：同预算工具结果变形脆弱性

## 一句话种子

在同一模型、提示、种子与案例内随机交织十次调用，把六臂工具结果变形与六次完全相同重放组成两个各六调用的共享配对组；冻结本地合成套件中，六臂失败率比一般重放不稳定高 40.43 个百分点，形成一颗值得在真实多步与跨谱系模型上扩大验证的干预特异脆弱性种子。

## 问题与边界

一次结构化工具任务答对，不代表回答对任务相关字段、无关诱饵、记录顺序或重复调用稳定；但把一次正确与六次合取直接比较，会机械增加失败暴露机会。本种子要回答的受限问题是：在相同六调用预算下，六臂字段/顺序变形是否比六次完全相同重放产生额外失败。

该问题不同于“模型是否真实读取了证据”。有限的变形关系可能被错误等变代理满足，变形也可能只是让任务更难。因此当前交付对象是**干预特异的关系脆弱性现象与配对评价协议**，不是因果采用验证器、无真值正确性指标、在线门控或部署失败率。

共享论文知识库中的 ToolFailBench（P039）说明汇总正确率会掩盖工具跳过与结果忽略，False Success（P040）说明自报完成可与环境真值分离，ReLoop（P097）和 Verus-SpecGym（P099）支持受控扰动与双向可执行检查。这些材料只给出问题入口，不直接证明本现象。

## 配对计算

每个模型—提示—种子—案例执行十次随机交织调用，形成两个共享 `base` 与 `repeat_1` 的六调用组：

- **六臂组**：`base`、任务相关字段变形、普通无关字段变形、答案形状诱饵变形、字段相同但记录顺序变化、`repeat_1`。
- **六重放组**：`base`、`repeat_1`、`repeat_2`、`repeat_3`、`repeat_4`、`repeat_5`；六次工具内容完全相同。

六臂组要求相关回答满足预声明标识双射或数值平移，两类无关回答、纯顺序回答和重放回答等于基线。六重放组要求六次回答都等于基线。主要指标在基线精确正确行上计算：

`配对超额失败率 = 六臂失败率 − 六重放失败率 = (仅六臂失败数 − 仅重放失败数) / 基线正确数`。

两个组各恰好六次调用，十个唯一调用按行级确定种子随机排序。标量答案只按预声明答案类型和明确结论形式规范化，不读取标准答案值；完整原始文本、解析答案、规范化标记、调用位置与资源均保留。独立家族求解器不导入生成器或主评估器，从原始工具字段重算五个源变体的答案与关系。

## 核心可证伪 Claim

在三个本地 Qwen 模型、严格/弱两种提示、种子 123/456/789 和二十个冻结案例上，六臂组相对六重放组应出现干预特异超额失败。预注册要求：总体配对超额至少 0.10；仅六臂失败严格多于仅重放失败且精确 McNemar 双侧 `p≤0.05`；剔除解析警告后超额至少 0.05；至少两个种子和六个模型—提示—种子分层为正。任一条件失败则 Claim 不支持。

Formal `attempt-budget-control-008` 绑定当前完整实现，独立求解器 20/20，通过 360 行、3600 次本地调用且无调用错误：

- 188 个基线正确行中，六臂失败 86 行，失败率为 0.4574468085106383；六重放失败 10 行，失败率为 0.05319148936170213。
- 仅六臂失败 76 行，仅重放失败 0 行，两组都失败 10 行；配对超额失败率为 0.40425531914893614。
- 精确 McNemar 双侧 p 值为 2.6469779601696886e-23。
- 剔除全部解析警告行后，186 个基线正确行中六臂失败 84、六重放失败 8，超额为 0.40860215053763443。
- 三个种子的超额依次为 0.4127、0.4032、0.3968；十八个模型—提示—种子分层全部为正。

这些结果排除了“更多调用的一般失败机会”作为全部解释，但不排除变形任务难度、有限关系代理或模型对表面结构的响应。

## 校准结果与退出的强主张

Formal `attempt-mutation-007` 的九策略校准中，六臂任务定向关系对作者定义行为标签的平衡准确率为 1.0，高于“相关变化加无关不变”的 0.8571 和“任意相关变化”的 0.7607；位置代理、方向错误和重放不稳定反例被拒绝。`eval-0005` 指出两个正类策略直接读取 `expected`，且未覆盖留出等变代理，因此该实验只证明评估器对已知脚本的内部判别，不证明真实证据采用。

Formal `attempt-qwen-007` 的 86/187 单次正确后六臂失败仍是有效描述事实，但原来的一次对六次比较不公平。新配对实验把其中 10/188 归为同预算重放不稳定，并留下 76/188 的仅六臂失败。旧“选择性采用机制”Claim 已降为 `scope_reduced`；最终核心只使用同预算超额现象。

## 最近先行与贡献差分

- LLMORPH 已实现 36 个自然语言处理变形关系，在四个基准和三个模型上执行超过 56 万次测试，并报告不同关系/任务的人工假阳性率差异很大；本种子不主张可扩展、无逐例标签的大模型变形测试工具。
- METAL 已系统使用大模型黑盒变形关系、输入扰动和重复一致性，本种子不主张发明变形测试。
- ReliabilityBench 已把变形关系用于智能体可靠性；CAIR、CVT-RL 分别覆盖智能体输出反事实影响和工具输出扰动式训练信用；PriVE-Tools 已提出证据提供不等于采用。
- 当前可辩护差分限于：结构化工具返回的任务相关/两类无关/纯顺序/精确重放析因六臂，配上严格同预算的六重放行内对照，以及由该载体复现的 40.43 个百分点局部超额现象。

这仍是 `ANALOGICAL_REDUCTION`：若已有工作使用同一工具字段干预和同预算重放对照，或该现象不能在真实多步与跨谱系模型复现，贡献应进一步降级。

## 贡献向量

- **问题/现象**：一次答对后的六臂关系失败显著超过相同调用预算下的一般重放不稳定。
- **评价/基准**：两个六调用组共享两次调用并在十次调用中随机交织，提供行内配对风险差和不一致行检验。
- **智能体特有约束**：干预位置是已经返回、即将进入回答上下文的结构化工具字段，而非普通用户文本。
- **经验发现**：当前套件总体超额 0.4043，三个种子和十八个模型分层均为正。
- **负面知识**：`tier_score` 家族超额为 0；关系通过与完整反事实精确正确仍完全重合；九策略校准不能认证真实采用。
- **系统能力**：实现可复现十调用配对、独立标签校验、原始输出审计和正式资源绑定。

## 局限与扩大判据

1. 二十例均为合成短标量答案；三个模型同属 Qwen 谱系，不能外推部署。
2. 六个模型—提示合并层均为正，但家族并不一致：`tier_score` 的六臂失败与六重放失败均为 6/18，配对超额为 0。
3. 当前样本内六臂关系通过与六臂完整精确正确同为 102/188；尚未证明关系信号相对完整反事实标签的无真值增量价值。
4. 解析警告涉及 12 行、62 次调用；警告剔除结果稳定，但没有盲人工复标开放式输出。
5. 模型文件、服务状态和主题依赖未完全固化；精确比例的跨机器复现仍有风险。
6. 下一阶段必须在真实多步工具任务和跨供应商模型上，由独立标注者定义关系；加入留出、非共线变形，比较 METAL 风格关系与完整标签，并检验是否增量预测独立终态、复核失败或修复收益。

这颗种子的价值是把一个原本受预算混杂的观察变成可证伪、配对且审计充分的局部现象；它值得扩大验证，但距离独立评价方法或 CCF-B 完整论文仍有显著缺口。

<!-- CRL_SEED_SUPPORT_META {"schema_version":1,"hypothesis_ids":["H001"],"claim_ids":["claim-budget-matched-excess"],"falsified_claim_dispositions":[],"metric_mappings":[{"seed_text":"六臂失败 86 行，失败率为 0.4574468085106383","seed_value":0.4574468085106383,"source_path":"experiment_v001/attempts/attempt-budget-control-008/metrics.json","json_pointer":"/records/1/value"},{"seed_text":"六重放失败 10 行，失败率为 0.05319148936170213","seed_value":0.05319148936170213,"source_path":"experiment_v001/attempts/attempt-budget-control-008/metrics.json","json_pointer":"/records/2/value"},{"seed_text":"配对超额失败率为 0.40425531914893614","seed_value":0.40425531914893614,"source_path":"experiment_v001/attempts/attempt-budget-control-008/metrics.json","json_pointer":"/records/0/value"},{"seed_text":"精确 McNemar 双侧 p 值为 2.6469779601696886e-23","seed_value":2.6469779601696886e-23,"source_path":"experiment_v001/attempts/attempt-budget-control-008/metrics.json","json_pointer":"/records/3/value"}]} -->

## 2. Closest Prior Evidence

### Source: `research_map_v001.md`

# 研究地图 v001

## 失败证据到干预

| 证据节点 | 已知缺口 | 本候选承接 | 边界 |
|---|---|---|---|
| P040 False Success | 自报完成可与环境真值分离 | 不信任单次自报与表面成功 | 不替代可用的环境终态检查 |
| P039 ToolFailBench | 总体正确率掩盖工具跳过与结果忽略 | 用字段级重放显式测工具结果响应 | 当前任务更小、更结构化 |
| P074 ToolGate | 后条件可约束可信工具状态，但部分工具缺少有效后条件 | 当完整后条件不可得时提供输出关系诊断 | 不提供提交门控或完整规格 |
| P097 ReLoop | 行为扰动能揭示可行性与正确性间隙 | 继承“受控扰动而非自然轨迹”的思想 | 干预对象改为工具返回字段 |
| P099 Verus-SpecGym | 双向可执行测试可暴露共享误读 | 同时检查应变与不变关系 | 不生成程序规格，不宣称正确性 |

## 最近方法谱系

1. 通用大模型变形测试：METAL 用输入扰动、相等/距离关系和相同输入重复评价多种大模型质量属性。
2. 反事实影响：CAIR 对智能体输出做反事实替换并测最终结果与工作流变化。
3. 变形可靠性：ReliabilityBench 以动作变形关系和终态等价性评价智能体系统。
4. 工具输出反事实贡献：CVT-RL 扰动工具输出，为可验证奖励下的强化学习分配信用。
5. 工具证据采用现象：PriVE-Tools 控制视觉工具证据视图，显示提供证据不保证模型使用证据。
6. 字段级采用诊断：本候选把任务相关等变、两类无关不变和精确重放组成四项黑盒关系，并与单次正确性正交报告。

## 关键碰撞判断

- 碰撞类型：`ANALOGICAL_REDUCTION`
- 已知一般成分并不新：反事实替换、变形关系、工具失败和结果忽略。
- 待守住的最小差分：变形对象是结构化工具返回字段；输出约束由任务关系预声明；普通无关字段与答案形状诱饵分别检验；精确重放排除随机性；结果以正确性×采用关系四象限呈现。
- 若最近先行已覆盖上述组合与同一诊断目标，应降级或终止。

### Source: `hypotheses_v001/priors/prior-009/assessment.md`

# 最近先行科研解释

> 本文件属于主研究者解释，可在阅读候选、PDF、Evidence 和实验后继续修订；它不进入机器事实快照哈希。

- 审计标识：`prior-009`
- 碰撞类型：`ANALOGICAL_REDUCTION`

## 真正的 nearest prior

1. **LLMORPH**（候选 `prior-f7354b01af09681b`，arXiv:2603.23611）是当前自动化系统与大规模评价上最近的先行。论文实现 36 个自然语言处理变形关系，在四个基准和三个模型上执行 561,267 次测试，并报告人工复核的变形违规假阳性率随任务和关系在 0%—70% 间变化。它使“可扩展、无逐例标签的大模型变形测试工具”不再构成贡献。
2. **METAL**（候选 `prior-05ce3bdb71373092`，arXiv:2312.06056）是方法骨架上最近的先行：模板化生成大模型变形关系，以输入扰动后的输出关系评价稳健性等质量属性，也覆盖非确定性。它否定“首次把变形关系用于大模型黑盒质量评价”。
3. **ReliabilityBench**（arXiv:2601.06112）把动作变形关系、任务扰动、终态等价和故障注入用于智能体可靠性；干预位置主要是任务输入与执行行为。
4. **CAIR**（ACL Anthology 2025.emnlp-main.958）和 **CVT-RL**（arXiv:2606.05263）分别通过替换智能体输出、扰动工具输出测量反事实影响或训练信用；目标不是行内同预算的黑盒关系脆弱性。
5. **PriVE-Tools**（arXiv:2607.16311）以受控视觉工具证据研究“证据提供不等于使用”；它与早期机制动机重合，但不提供当前结构化字段六臂与六重放配对协议。

## 实质组件重合

- 与 LLMORPH/METAL 重合：源输入与跟随输入、变形关系作为测试 oracle、黑盒多次调用、自动暴露不一致、无需每个跟随输入标签。
- 与 ReliabilityBench 重合：把变形关系用于智能体可靠性，而不是普通确定性软件。
- 与 CAIR/CVT-RL/PriVE-Tools 重合：用受控证据或工具输出变化观察下游回答变化。
- 当前 40.43 个百分点效应仍可能只是已知变形测试在工具字段场景中的一种实例，不构成新方法原语。

## 仍存贡献增量

- **干预位置**：只改变已经返回的结构化工具字段和记录顺序，不改用户任务、工具选择或执行动作。
- **析因关系**：任务相关等变、普通无关、答案形状诱饵、纯顺序和精确重放分别定义失败面。
- **公平基线**：同一行十次调用构成共享 `base` 与 `repeat_1` 的两个六调用组；六臂组与六次相同重放在模型、提示、种子、案例、信息和预算上配对，十调用随机交织。
- **局部现象**：188 个基线正确行中六臂失败 86、六重放失败 10；仅六臂失败 76、仅重放失败 0，配对超额 0.40425531914893614，三个种子与十八个模型分层均为正。
- **边界透明**：当前关系通过与完整反事实精确正确完全重合，`tier_score` 家族超额为 0；最终不主张无真值增量或真实采用机制。

## 最危险替代解释

最危险解释是：六臂变形只是比完全相同重放更难，40.43 个百分点效应属于一般变形稳健性，而不是工具证据采用。LLMORPH 已证明多种关系可大规模暴露不一致，也显示某些关系的假阳性率很高；如果当前效应不能在独立定义、真实多步、非共线工具字段变形上复现，或不能在控制完整正确性后预测独立终态，它只是一项工具场景的局部稳健性测量。

## 最小区分实验

1. 同一模型—提示—种子—案例内，以相同六调用预算比较六臂与六次完全重放；当前 `attempt-budget-control-008` 已通过这一预算混杂检查。
2. 在未见任务上由独立实现者提交不读取关键相关字段的等变代理，以及真正从工具字段求解的策略；若前者通过而后者被拒，采用机制解释死亡。
3. 使用多组可组合、非共线相关变形，使只读单一字段或单记录加常数的代理与真实任务函数产生不同关系。
4. 在真实多步工具任务和跨供应商模型上，与 LLMORPH/METAL 风格关系及完整反事实标签同预算比较。
5. 控制完整反事实正确性后，检验关系失败能否增量预测环境终态、盲复核失败或修复收益。

## 方法死亡后仍存现象

即使 LLMORPH/METAL 完全吸收方法新颖性，仍存的可扩大现象是：当前结构化工具短任务中，六臂字段/顺序变形在同预算下比六次完全重放多出 40.43 个百分点失败，且跨三个种子和十八个模型分层为正。这是受限稳健性现象，不是部署率；它是否跨家族、跨谱系和真实轨迹稳定仍未知。

## 背景与身份未解决项

- 本次自动审计因 Semantic Scholar HTTP 429 降级，候选主要来自 arXiv；候选身份、查询和响应哈希已保存。
- LLMORPH 的组件与 561,267 次测试、18% 平均失败率、0%—70% 人工假阳性范围来自论文 HTML 原文；正文描述每个源输入通常使用 2—3 次调用，未发现同预算六重放配对对照，但这不是穷尽性代码审计。
- CAIR、CVT-RL、ReliabilityBench 与 PriVE-Tools 来自先前已核对的论文原文，未进入本次 arXiv 候选前十五项。
- 尚未发现完全匹配“结构化工具字段析因六臂 + 行内同预算六重放 + 十调用随机交织 + 配对风险差”的论文，但不能据此宣称穷尽性新颖。

## 3. Core Experimental Evidence

### Source: `experiment_v001/result.md`

# 正式实验结果 v001

## 当前核心证据

Formal `attempt-budget-control-008` 绑定当前完整十调用实现：`runner_exit_code=0`、`command_exit_code=0`、`timed_out=false`、`metrics_contract_ok=true`、`output_contract_ok=true`、`evidence_contract_ok=true`。正式执行完成 360 行、3600 次本地调用、827968 个令牌，耗时 1595.689 秒，无调用错误。

独立家族求解器不读取声明的 `expected` 作为求解输入，也不导入生成器或主评估器；二十例的基线、相关、两类无关与纯顺序标签和关系全部重算一致，20/20 通过。这只证明冻结套件自洽。

## 预注册同预算结果

在 188 个基线精确正确行中：

| 配对结果 | 行数 |
|---|---:|
| 两组都通过 | 102 |
| 仅六臂失败 | 76 |
| 仅六重放失败 | 0 |
| 两组都失败 | 10 |

- 六臂失败率：86/188 = 0.4574468085106383。
- 六重放失败率：10/188 = 0.05319148936170213。
- 配对超额失败率：0.40425531914893614。
- 精确 McNemar 双侧 p 值：2.6469779601696886e-23。
- 12 行包含解析警告，共 62 次警告调用；剔除这些行后，186 个基线正确行中六臂失败 84、六重放失败 8，配对超额为 0.40860215053763443。
- 三个种子的超额依次为：123 为 0.4127，456 为 0.4032，789 为 0.3968；三者均为正。
- 十八个模型—提示—种子分层全部为正，超过预注册的六个分层门槛。

四项预注册签名全部成立。结果排除了“六次调用比一次调用拥有更多一般失败机会”作为全部解释，支持冻结套件中的干预特异关系脆弱性。

## 分层

合并三个种子后的模型—提示结果：

| 模型—提示 | 基线正确 n | 六臂失败 | 六重放失败 | 配对超额 |
|---|---:|---:|---:|---:|
| qwen2.5:7b—严格 | 17 | 11 | 3 | 0.4706 |
| qwen2.5:7b—弱 | 23 | 14 | 6 | 0.3478 |
| qwen3:4b—严格 | 36 | 23 | 0 | 0.6389 |
| qwen3:4b—弱 | 40 | 26 | 1 | 0.6250 |
| qwen3:8b—严格 | 27 | 3 | 0 | 0.1111 |
| qwen3:8b—弱 | 45 | 9 | 0 | 0.2000 |

按任务族：`count_open` 超额 22/49=0.4490；`filtered_argmin` 为 21/54=0.3889；`latest_confirmed` 为 (31−2)/58=0.5000；`valid_sum` 为 (6−2)/9=0.4444；`tier_score` 的六臂与六重放均失败 6/18，超额为 0。现象不是全家族一致。

## 完整性与解析审计

- 360 行均包含十个唯一调用标识和十个答案，合计 3600 次调用；所有 `repeat_*` 均映射到完全相同的基线工具内容。
- 十个调用标识都覆盖十个调用位置；每行调用顺序由模型、提示、种子、案例的确定字符串生成并打乱。
- 语义规范化触发 159 次调用；规范化不读取标准答案值。
- 当前基线正确子集上，六臂关系通过与六臂完整精确正确均为 102/188；六重放关系通过与六重放完整正确均为 178/188，二者都没有关系/完整标签不一致行。

最后一点是关键负面结果：当前数据没有证明关系信号相对完整反事实正确性的无真值增量价值。

## 旧证据的重新解释

`attempt-mutation-007` 的联合关系平衡准确率 1.0、弱基线 0.8571/0.7607 只作为作者定义行为的内部校准。`eval-0005` 指出正类读取 `expected` 且缺少留出代理，因此不再支持真实采用机制。

`attempt-qwen-007` 的 86/187 单次正确后六臂失败是有效描述，但单次对六次预算不公平。新实验中六臂同样失败 86/188，而六重放失败 10/188；核心效应改为配对超额 76/188，而不是原始 86/187 比例。

## 结论边界

当前证据只支持：冻结的二十例短答案套件上，六臂工具字段/顺序变形造成的关系失败显著超过等预算完全重放不稳定。它不证明模型真实采用了任务证据，不排除变形任务更难，不外推真实多步、开放式或跨供应商智能体，也不声称相对完整反事实标签的增量价值。

### Source: `experiment_v001/attempts/attempt-budget-control-008/execution.json`

{
  "argv": [
    "D:\\Desktop\\crl\\env\\crl_agent_v3\\python.exe",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\run_verified_budget_control.py",
    "--cases",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\cases.json",
    "--oracle-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-budget-control-008\\oracle.json",
    "--output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-budget-control-008\\result.json",
    "--report-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-budget-control-008\\report.md",
    "--metrics-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-budget-control-008\\metrics-output.json",
    "--experiment-id",
    "exp-budget-control-v008",
    "--models",
    "qwen2.5:7b",
    "qwen3:4b",
    "qwen3:8b",
    "--prompt-regimes",
    "weak",
    "strict",
    "--seeds",
    "123",
    "456",
    "789",
    "--ollama-url",
    "http://127.0.0.1:11434/api/chat",
    "--temperature",
    "0.2",
    "--timeout-seconds",
    "120"
  ],
  "attempt_id": "attempt-budget-control-008",
  "budget_facts": {
    "actual": {
      "api_calls": 3600,
      "duration_seconds": 1595.6894259,
      "gpu_time_seconds": "unknown",
      "tokens": 827968
    },
    "comparison": {
      "reason": "budget_ceiling is not a machine-readable JSON object",
      "status": "unavailable"
    },
    "machine_readable_limits": null,
    "spec_budget_ceiling": "3 模型 × 2 提示制度 × 3 种子 × 20 案例 × 10 调用 = 3600 次本地调用；单调用超时 120 秒。",
    "warnings": []
  },
  "capture": {
    "stderr": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-budget-control-008\\stderr.bin",
      "redaction_applied": false,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "size_bytes": 0
    },
    "stdout": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-budget-control-008\\stdout.bin",
      "redaction_applied": false,
      "sha256": "6add8397dc1b636da66fcff5e7872959a191e334caf863e1fb608d34b039e42c",
      "size_bytes": 394
    }
  },
  "command_error": null,
  "command_exit_code": 0,
  "cwd": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001",
  "duration_seconds": 1595.6894259,
  "environment_facts": {
    "cpu_count": 16,
    "declared_facts": {
      "dataset": "frozen-20-case-factorized-order-control",
      "dataset_revision": "suite-seed-20260815-factorized-order",
      "model": "qwen2.5:7b,qwen3:4b,qwen3:8b",
      "model_revision": "local-ollama-tags-bound-at-execution",
      "prompt_revision": "weak-and-strict-v001-budget-control-ten-call",
      "provider": "local-ollama"
    },
    "git": {
      "reason": "ValueError: command exited with code 128",
      "status": "unavailable"
    },
    "nvidia": {
      "cuda_version": "13.1",
      "gpus": [
        {
          "driver_version": "591.86",
          "index": "0",
          "memory_total_mib": "16311",
          "name": "NVIDIA GeForce RTX 5060 Ti"
        }
      ],
      "status": "available"
    },
    "platform": "Windows-10-10.0.26100-SP0",
    "runner": {
      "dependencies": {
        "scope": "formal_runner_machine_environment",
        "snapshot": {
          "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-budget-control-008\\dependencies.txt",
          "sha256": "480ab3b94b0b3b95bb6ff16eb9c4e138b942a818e488d43f71f810c5fe2e143a",
          "size_bytes": 769
        },
        "source_path": "D:\\Desktop\\crl\\crl_agent_v3\\CRL_ENVIRONMENT_LOCK.txt",
        "source_type": "lock_file",
        "subject_relationship": "unbound"
      },
      "executable": {
        "path": "D:\\Desktop\\crl\\env\\crl_agent_v3\\python.exe",
        "sha256": "0562f573871cb16a2fb8de16e3d486e3dfd74bb83c7e87db265561917d05ad1a",
        "size_bytes": 105288,
        "status": "bound"
      },
      "python": "3.11.15 | packaged by Anaconda, Inc. | (main, Jun 11 2026, 15:12:53) [MSC v.1942 64 bit (AMD64)]",
      "runner_and_modules": [
        {
          "path": "tools/run_local_experiment.py",
          "sha256": "1b88d8c58b14530f06e19ff3993a42cda2edac67b15dd229e9c567aba74434b7",
          "size_bytes": 37357
        },
        {
          "path": "crl_v3/experiment.py",
          "sha256": "4c513a8b90978e02f332292d3760dcdcc6cb3825c81833812f8b9e2f3c319e4c",
          "size_bytes": 45593
        },
        {
          "path": "crl_v3/falsification.py",
          "sha256": "5a852d0df4101c5b240363559d0cc05a2f64c725574d999b999e92deba97b9b8",
          "size_bytes": 40435
        },
        {
          "path": "crl_v3/workspace.py",
          "sha256": "a78a8c043ce52bed6048d307e85a8544c40ffb3bb5b98e5864654a2e7c3c8b7d",
          "size_bytes": 28943
        },
        {
          "path": "crl_v3/decision.py",
          "sha256": "8cacbfc82bc62362601264dd5cf0fde705c10faa754a10183d8ae37b67443b4f",
          "size_bytes": 45420
        }
      ]
    },
    "sensitive_environment_passthrough": [],
    "subject": {
      "argv0": "D:\\Desktop\\crl\\env\\crl_agent_v3\\python.exe",
      "dependencies": {
        "reason": "subject dependencies are not automatically inspected or inferred from runner dependencies",
        "status": "unbound"
      },
      "environment": {
        "policy": "sanitized_parent_with_explicit_sensitive_passthrough",
        "status": "partially_bound",
        "unbound_reason": "non-sensitive subject environment names and values are not persisted"
      },
      "executable": {
        "path": "D:\\Desktop\\crl\\env\\crl_agent_v3\\python.exe",
        "resolution": "absolute_path",
        "sha256": "0562f573871cb16a2fb8de16e3d486e3dfd74bb83c7e87db265561917d05ad1a",
        "size_bytes": 105288,
        "status": "bound"
      },
      "runner_relationship": "same_executable",
      "runtime": {
        "python": "3.11.15 | packaged by Anaconda, Inc. | (main, Jun 11 2026, 15:12:53) [MSC v.1942 64 bit (AMD64)]",
        "status": "bound_to_runner_python"
      }
    }
  },
  "evidence_contract_ok": true,
  "experiment_spec": {
    "snapshot": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-budget-control-008\\spec.json",
      "sha256": "82b9110e4c2f144c3eddc40866663dec7ae0367d23a5d43861d687bd2c11c485",
      "size_bytes": 5151
    },
    "source_path": "experiment_v001/specs/exp-budget-control-v008.json"
  },
  "finished_at_utc": "2026-08-15T14:07:49.501421Z",
  "implementation_files": [
    {
      "path": "implementation_v001/cases.json",
      "sha256": "253071c8ae1e34e90ca741da791e6541328f044c1936ca6c5e09060c10493038",
      "size_bytes": 76928
    },
    {
      "path": "implementation_v001/causal_uptake_eval.py",
      "sha256": "bac2a4da1b61e1a589cb1ecb716e12f36231d01622ab2da440d0b48ccc8fbee5",
      "size_bytes": 32120
    },
    {
      "path": "implementation_v001/generate_suite.py",
      "sha256": "cc490c3eee0edf9ceeefb81d7124e0606d6b1c67d7f4398eee4432b083198568",
      "size_bytes": 12645
    },
    {
      "path": "implementation_v001/independent_oracle.py",
      "sha256": "0067ea0695a5b6e0d0d1f744a2aa8b5196ce01b92b739ca40ea0edf5bdd4edd6",
      "size_bytes": 6370
    },
    {
      "path": "implementation_v001/run_verified_experiment.py",
      "sha256": "5b06306911b56a4a22de21368e300b30cfb8f11e7ab3406248ef13878f50bd03",
      "size_bytes": 2688
    },
    {
      "path": "implementation_v001/suite_spec.json",
      "sha256": "6b707be648e99c6c43aea2a0a5b28789dc03e8aaf7b0b54ae517550ebd0b2aa0",
      "size_bytes": 185
    },
    {
      "path": "implementation_v001/test_causal_uptake_eval.py",
      "sha256": "0f21020669e79fe40080870bc3dab408383feac2bd7161ce2e1e8c40f2930723",
      "size_bytes": 7940
    },
    {
      "path": "implementation_v001/budget_matched_control.py",
      "sha256": "9585276c4e566de63d469ac3e6cc4155b0b63dac6ef99f56c0fb1d9de1dccce3",
      "size_bytes": 16953
    },
    {
      "path": "implementation_v001/test_budget_matched_control.py",
      "sha256": "d3b5da884796f7c6e021c88fe5ed7ad2ec60f995113519eaab49a6def68a3373",
      "size_bytes": 3778
    },
    {
      "path": "implementation_v001/run_verified_budget_control.py",
      "sha256": "fd04ddbad2aa993c874d28befbebfdd73e3785551dc40a8d3417bc6600a4cede",
      "size_bytes": 2277
    }
  ],
  "inputs": [
    {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\cases.json",
      "sha256": "253071c8ae1e34e90ca741da791e6541328f044c1936ca6c5e09060c10493038",
      "size_bytes": 76928
    },
    {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\suite_spec.json",
      "sha256": "6b707be648e99c6c43aea2a0a5b28789dc03e8aaf7b0b54ae517550ebd0b2aa0",
      "size_bytes": 185
    }
  ],
  "metrics": {
    "contains_possible_credential": false,
    "credential_detection": [],
    "snapshot": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-budget-control-008\\metrics.json",
      "sha256": "957374383425a86e3f1e9b91b84af4de6aad1fa06fe1cb23c44016c5262e3a2b",
      "size_bytes": 8462
    },
    "source_path": "experiment_v001/attempts/attempt-budget-control-008/metrics-output.json",
    "source_sha256": "957374383425a86e3f1e9b91b84af4de6aad1fa06fe1cb23c44016c5262e3a2b",
    "source_size_bytes": 8462,
    "validation_errors": []
  },
  "metrics_contract_ok": true,
  "output_contract_ok": true,
  "outputs": [
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "910a6033fd73ce2454185f98ecc25ce5f0d22a265f62bd5191088a63d90a7525",
        "size_bytes": 13834
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-budget-control-008\\oracle.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "03549824b82e7bfe0bfa60574487d18f8a69240b6f86648993b4e3eaaf3180c3",
        "size_bytes": 2374607
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-budget-control-008\\result.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "fd52c0f4a928b0ce5810a15af233d133c042a9e465953b4bacc3d5afd5104a7a",
        "size_bytes": 986
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-budget-control-008\\report.md"
    }
  ],
  "process_tree_cleanup_ok": null,
  "run_root": "D:\\Desktop\\crl\\20260815_1818_run11",
  "runner_exit_code": 0,
  "schema_version": 8,
  "seed": {
    "status": "set",
    "value": "123"
  },
  "started_at_utc": "2026-08-15T13:41:13.812256Z",
  "stdout_as_evidence": true,
  "termination_method": null,
  "timed_out": false,
  "timeout_seconds": 4200.0,
  "version": "v001",
  "warnings": []
}

## 4. Baseline & Budget Facts

### Source: `experiment_v001/plan.md`

# 实验计划 v001

## 当前核心主张

最终主张为：在冻结本地合成套件的基线正确行上，六臂工具结果变形相对于同预算六次完全相同重放产生干预特异的额外关系失败。它不声称识别真实证据采用机制。

## 同预算杀手实验

- 规格：`exp-budget-control-v008`。
- 模型：`qwen2.5:7b`、`qwen3:4b`、`qwen3:8b`。
- 提示：弱、严格两种制度。
- 种子：123、456、789；温度 0.2。
- 数据：五个确定性任务族、每族四例，共二十例。
- 调用：每行十次随机交织调用，构成共享 `base` 和 `repeat_1` 的两个六调用组。
- 六臂组：`base`、`relevant`、`irrelevant_plain`、`irrelevant_adversarial`、`order_only`、`repeat_1`。
- 六重放组：`base`、`repeat_1`、`repeat_2`、`repeat_3`、`repeat_4`、`repeat_5`，内容完全相同。
- 主要指标：基线正确行上的配对超额失败率。
- 否证：超额低于 0.10；仅六臂失败不多于仅重放失败；精确 McNemar 双侧 p>0.05；警告剔除后超额低于 0.05；或正超额不跨至少两个种子和六个模型—提示—种子分层。
- 保留：完整原始输出、解析答案、规范化标记、调用位置、资源、错误和警告。

独立家族求解器在正式调用前从原始工具字段重算五个源变体，不导入生成器或主评估器，要求二十例全部通过。它只保证套件自洽，不证明外部有效性。

## 校准与历史边界

`exp-mutation-v007` 只校准评估器对九种作者定义行为的区分；`exp-qwen-v007` 只保留为单次对六次的描述历史。前三轮评审发现的重复遗漏、位置代理、顺序混杂与字符串误判已经在第七版修复；`eval-0005` 新发现的 oracle 捷径与预算不公平由强主张降级和第八版同预算杀手实验处理。

Scratch `budget-control-smoke` 只验证十调用程序可执行，不能支持 Claim。只有 Formal `attempt-budget-control-008` 进入当前核心支持链。

### Source: `experiment_v001/specs/exp-budget-control-v008.json`

{
  "baseline_specs": [
    "同一行内由 base、repeat_1、repeat_2、repeat_3、repeat_4、repeat_5 构成的六次完全相同重放组。",
    "六臂组由 base、relevant、irrelevant_plain、irrelevant_adversarial、order_only、repeat_1 构成。",
    "两组共享 base 与 repeat_1，均为六次调用；十个唯一调用随机交织，避免固定位置优势。"
  ],
  "budget_ceiling": "3 模型 × 2 提示制度 × 3 种子 × 20 案例 × 10 调用 = 3600 次本地调用；单调用超时 120 秒。",
  "claim_ids": [
    "claim-budget-matched-excess"
  ],
  "confounders": [
    "三种模型同属 Qwen 谱系，不能代表跨供应商泛化。",
    "合成任务输出短且字段显式，变形组可能因任务难度而非采用机制产生额外失败。",
    "两组共享 base 与 repeat_1，形成高效配对但不是两套独立调用样本。",
    "标量规范化是预声明启发式；必须保留原始内容和警告剔除分析。",
    "行级统计共享案例与模型，精确 McNemar 只检验当前配对样本，不提供总体部署区间。"
  ],
  "dataset": "五个确定性结构化工具任务族、每族四例、共二十例；四个字段臂共享记录排列，纯顺序臂使用字段相同的无固定点循环排列。",
  "declared_inputs": [
    "implementation_v001/cases.json",
    "implementation_v001/causal_uptake_eval.py",
    "implementation_v001/budget_matched_control.py",
    "implementation_v001/independent_oracle.py"
  ],
  "declared_outputs": [
    "experiment_v001/attempts/attempt-budget-control-008/oracle.json",
    "experiment_v001/attempts/attempt-budget-control-008/result.json",
    "experiment_v001/attempts/attempt-budget-control-008/report.md",
    "experiment_v001/attempts/attempt-budget-control-008/metrics.json"
  ],
  "expected_signatures": [
    "基线正确行上的配对超额失败率至少 0.10。",
    "仅六臂失败行严格多于仅重放失败行，精确 McNemar 双侧 p 值不高于 0.05。",
    "剔除解析警告后配对超额失败率至少 0.05。",
    "至少两个种子和至少六个模型—提示—种子分层呈正超额。"
  ],
  "experiment_id": "exp-budget-control-v008",
  "falsification_rule": "任一预声明签名不满足，则‘干预特异的额外关系失败’主张不支持；不得用原 86/187 单次对六次结果绕过同预算对照，也不得据正结果声称真实采用机制或部署外推。",
  "hypothesis_id": "H001",
  "independent_ground_truth": {
    "description": "独立家族求解器从原始工具字段重算基线及五个源变体的精确答案和关系语义，不导入本对照程序；正式运行前必须 20/20 通过。两组共享同一基线和一次重放，组内六调用预算严格相等。",
    "external_card_ids": [],
    "external_evidence_ids": [],
    "external_literature_refs": [
      "P039",
      "P040",
      "P097"
    ],
    "run_local_fact_refs": [
      "implementation_v001/independent_oracle.py",
      "implementation_v001/cases.json",
      "review_v001/evaluations/eval-0005/EMP/report.json"
    ]
  },
  "model": "qwen2.5:7b、qwen3:4b、qwen3:8b；严格与弱两种提示制度。",
  "parity_dimensions": {
    "budget": {
      "notes": "六臂组和完全重放组各恰好六次调用。",
      "status": "matched"
    },
    "information_access": {
      "notes": "两组使用同一任务、提示、模型、种子和基线工具结果；只在六臂组的四个中间调用中施加预声明变形。",
      "status": "matched"
    },
    "model_provider_revision": {
      "notes": "三种模型标签是预声明复现分层，实际模型与服务身份由执行环境绑定。",
      "status": "different"
    },
    "sampling_protocol": {
      "notes": "两组共享行、base 与 repeat_1；十个调用使用同一温度并按行内确定种子随机交织。",
      "status": "matched"
    },
    "tool_capability": {
      "notes": "所有调用接收相同格式的结构化工具结果，无外部工具执行。",
      "status": "matched"
    }
  },
  "primary_metric": "budget_matched_excess_failure_rate",
  "provider": "本机 Ollama 服务；模型与服务身份由正式执行记录和本机清单绑定。",
  "purpose": "independent_claim_validation",
  "research_question": "在相同六调用预算下，六臂字段/顺序变形是否比六次完全相同重放产生显著且分层稳定的额外失败？",
  "revision": "reviewer-killer-1 equal-budget paired ten-call protocol, full-manifest binding",
  "run_id": "20260815_1818_run11",
  "sampling_unit": "模型 × 提示制度 × 种子 × 冻结案例，共 360 行；每行十次随机交织调用，同时形成共享基线和 repeat_1 的两个六调用组。",
  "schema_version": 1,
  "secondary_metrics": [
    "transform_failure_rate",
    "repeat_control_failure_rate",
    "exact_mcnemar_pvalue",
    "transform_only_fail",
    "control_only_fail",
    "parse_warning_excluded_excess_failure_rate",
    "positive_seed_count",
    "positive_stratum_count"
  ],
  "seeds": [
    123,
    456,
    789
  ],
  "version": "v001"
}

## 5. Ablation / Robustness / Falsification Evidence

### Source: `experiment_v001/attempts/attempt-budget-control-008/report.md`

# 同预算六重重放对照结果

- 行数：360
- 调用数：3600
- 基线正确行：188
- 六臂失败率：0.4574468085106383
- 六重放失败率：0.05319148936170213
- 配对超额失败率：0.40425531914893614
- 精确 McNemar 双侧 p 值：2.6469779601696886e-23
- 仅六臂失败 / 仅重放失败 / 两者都失败：76 / 0 / 10
- 剔除解析警告后的配对超额失败率：0.40860215053763443
- 正超额种子数 / 分层数：3 / 18

## 按种子

| 种子 | 基线正确 n | 六臂失败率 | 六重放失败率 | 超额失败率 |
|---|---:|---:|---:|---:|
| 123 | 63 | 0.4603174603174603 | 0.047619047619047616 | 0.4126984126984127 |
| 456 | 62 | 0.45161290322580644 | 0.04838709677419355 | 0.4032258064516129 |
| 789 | 63 | 0.4603174603174603 | 0.06349206349206349 | 0.3968253968253968 |

> 这是同一模型、提示、种子与案例内的配对预算对照；它检验干预特异的额外失败，不认证真实证据采用机制或外部有效性。

### Source: `review_v001/row-audit-v008-compact.json`

{"schema_version":2,"purpose":"固定评审用紧凑逐行审计；保留每次解析答案、随机调用位置、规范化标记与行级指标；完整原始结果由 source_sha256 绑定","attempt_id":"attempt-budget-control-008","source_path":"experiment_v001/attempts/attempt-budget-control-008/result.json","source_sha256":"03549824b82e7bfe0bfa60574487d18f8a69240b6f86648993b4e3eaaf3180c3","configuration":{"models":["qwen2.5:7b","qwen3:4b","qwen3:8b"],"prompt_regimes":["weak","strict"],"seeds":[123,456,789],"temperature":0.2,"transform_group":["base","relevant","irrelevant_plain","irrelevant_adversarial","order_only","repeat_1"],"repeat_control_group":["base","repeat_1","repeat_2","repeat_3","repeat_4","repeat_5"],"call_ids":["base","relevant","irrelevant_plain","irrelevant_adversarial","order_only","repeat_1","repeat_2","repeat_3","repeat_4","repeat_5"],"randomized_call_order":true},"aggregate":{"overall":{"n_all":360,"n_base_correct":188,"both_pass":102,"transform_only_fail":76,"control_only_fail":0,"both_fail":10,"transform_failure_rate":0.4574468085106383,"repeat_control_failure_rate":0.05319148936170213,"excess_failure_rate":0.40425531914893614,"exact_mcnemar_pvalue":2.6469779601696886E-23},"parse_warning_excluded":{"n_all":348,"n_base_correct":186,"both_pass":102,"transform_only_fail":76,"control_only_fail":0,"both_fail":8,"transform_failure_rate":0.45161290322580644,"repeat_control_failure_rate":0.043010752688172046,"excess_failure_rate":0.40860215053763443,"exact_mcnemar_pvalue":2.6469779601696886E-23},"by_seed":{"123":{"n_all":120,"n_base_correct":63,"both_pass":34,"transform_only_fail":26,"control_only_fail":0,"both_fail":3,"transform_failure_rate":0.4603174603174603,"repeat_control_failure_rate":0.047619047619047616,"excess_failure_rate":0.4126984126984127,"exact_mcnemar_pvalue":2.980232238769531E-08},"456":{"n_all":120,"n_base_correct":62,"both_pass":34,"transform_only_fail":25,"control_only_fail":0,"both_fail":3,"transform_failure_rate":0.45161290322580644,"repeat_control_failure_rate":0.04838709677419355,"excess_failure_rate":0.4032258064516129,"exact_mcnemar_pvalue":5.960464477539063E-08},"789":{"n_all":120,"n_base_correct":63,"both_pass":34,"transform_only_fail":25,"control_only_fail":0,"both_fail":4,"transform_failure_rate":0.4603174603174603,"repeat_control_failure_rate":0.06349206349206349,"excess_failure_rate":0.3968253968253968,"exact_mcnemar_pvalue":5.960464477539063E-08}},"by_agent":{"ollama::qwen2.5:7b::weak::seed-123":{"n_all":20,"n_base_correct":8,"both_pass":3,"transform_only_fail":3,"control_only_fail":0,"both_fail":2,"transform_failure_rate":0.625,"repeat_control_failure_rate":0.25,"excess_failure_rate":0.375,"exact_mcnemar_pvalue":0.25},"ollama::qwen2.5:7b::weak::seed-456":{"n_all":20,"n_base_correct":8,"both_pass":3,"transform_only_fail":2,"control_only_fail":0,"both_fail":3,"transform_failure_rate":0.625,"repeat_control_failure_rate":0.375,"excess_failure_rate":0.25,"exact_mcnemar_pvalue":0.5},"ollama::qwen2.5:7b::weak::seed-789":{"n_all":20,"n_base_correct":7,"both_pass":3,"transform_only_fail":3,"control_only_fail":0,"both_fail":1,"transform_failure_rate":0.5714285714285714,"repeat_control_failure_rate":0.14285714285714285,"excess_failure_rate":0.42857142857142855,"exact_mcnemar_pvalue":0.25},"ollama::qwen2.5:7b::strict::seed-123":{"n_all":20,"n_base_correct":6,"both_pass":2,"transform_only_fail":3,"control_only_fail":0,"both_fail":1,"transform_failure_rate":0.6666666666666666,"repeat_control_failure_rate":0.16666666666666666,"excess_failure_rate":0.5,"exact_mcnemar_pvalue":0.25},"ollama::qwen2.5:7b::strict::seed-456":{"n_all":20,"n_base_correct":5,"both_pass":2,"transform_only_fail":3,"control_only_fail":0,"both_fail":0,"transform_failure_rate":0.6,"repeat_control_failure_rate":0.0,"excess_failure_rate":0.6,"exact_mcnemar_pvalue":0.25},"ollama::qwen2.5:7b::strict::seed-789":{"n_all":20,"n_base_correct":6,"both_pass":2,"transform_only_fail":2,"control_only_fail":0,"both_fail":2,"transform_failure_rate":0.6666666666666666,"repeat_control_failure_rate":0.3333333333333333,"excess_failure_rate":0.3333333333333333,"exact_mcnemar_pvalue":0.5},"ollama::qwen3:4b::weak::seed-123":{"n_all":20,"n_base_correct":13,"both_pass":4,"transform_only_fail":9,"control_only_fail":0,"both_fail":0,"transform_failure_rate":0.6923076923076923,"repeat_control_failure_rate":0.0,"excess_failure_rate":0.6923076923076923,"exact_mcnemar_pvalue":0.00390625},"ollama::qwen3:4b::weak::seed-456":{"n_all":20,"n_base_correct":13,"both_pass":5,"transform_only_fail":8,"control_only_fail":0,"both_fail":0,"transform_failure_rate":0.6153846153846154,"repeat_control_failure_rate":0.0,"excess_failure_rate":0.6153846153846154,"exact_mcnemar_pvalue":0.0078125},"ollama::qwen3:4b::weak::seed-789":{"n_all":20,"n_base_correct":14,"both_pass":5,"transform_only_fail":8,"control_only_fail":0,"both_fail":1,"transform_failure_rate":0.6428571428571429,"repeat_control_failure_rate":0.07142857142857142,"excess_failure_rate":0.5714285714285714,"exact_mcnemar_pvalue":0.0078125},"ollama::qwen3:4b::strict::seed-123":{"n_all":20,"n_base_correct":12,"both_pass":5,"transform_only_fail":7,"control_only_fail":0,"both_fail":0,"transform_failure_rate":0.5833333333333334,"repeat_control_failure_rate":0.0,"excess_failure_rate":0.5833333333333334,"exact_mcnemar_pvalue":0.015625},"ollama::qwen3:4b::strict::seed-456":{"n_all":20,"n_base_correct":12,"both_pass":4,"transform_only_fail":8,"control_only_fail":0,"both_fail":0,"transform_failure_rate":0.6666666666666666,"repeat_control_failure_rate":0.0,"excess_failure_rate":0.6666666666666666,"exact_mcnemar_pvalue":0.0078125},"ollama::qwen3:4b::strict::seed-789":{"n_all":20,"n_base_correct":12,"both_pass":4,"transform_only_fail":8,"control_only_fail":0,"both_fail":0,"transform_failure_rate":0.6666666666666666,"repeat_control_failure_rate":0.0,"excess_failure_rate":0.6666666666666666,"exact_mcnemar_pvalue":0.0078125},"ollama::qwen3:8b::weak::seed-123":{"n_all":20,"n_base_correct":15,"both_pass":12,"transform_only_fail":3,"control_only_fail":0,"both_fail":0,"transform_failure_rate":0.2,"repeat_control_failure_rate":0.0,"excess_failure_rate":0.2,"exact_mcnemar_pvalue":0.25},"ollama::qwen3:8b::weak::seed-456":{"n_all":20,"n_base_correct":15,"both_pass":12,"transform_only_fail":3,"control_only_fail":0,"both_fail":0,"transform_failure_rate":0.2,"repeat_control_failure_rate":0.0,"excess_failure_rate":0.2,"exact_mcnemar_pvalue":0.25},"ollama::qwen3:8b::weak::seed-789":{"n_all":20,"n_base_correct":15,"both_pass":12,"transform_only_fail":3,"control_only_fail":0,"both_fail":0,"transform_failure_rate":0.2,"repeat_control_failure_rate":0.0,"excess_failure_rate":0.2,"exact_mcnemar_pvalue":0.25},"ollama::qwen3:8b::strict::seed-123":{"n_all":20,"n_base_correct":9,"both_pass":8,"transform_only_fail":1,"control_only_fail":0,"both_fail":0,"transform_failure_rate":0.1111111111111111,"repeat_control_failure_rate":0.0,"excess_failure_rate":0.1111111111111111,"exact_mcnemar_pvalue":1.0},"ollama::qwen3:8b::strict::seed-456":{"n_all":20,"n_base_correct":9,"both_pass":8,"transform_only_fail":1,"control_only_fail":0,"both_fail":0,"transform_failure_rate":0.1111111111111111,"repeat_control_failure_rate":0.0,"excess_failure_rate":0.1111111111111111,"exact_mcnemar_pvalue":1.0},"ollama::qwen3:8b::strict::seed-789":{"n_all":20,"n_base_correct":9,"both_pass":8,"transform_only_fail":1,"control_only_fail":0,"both_fail":0,"transform_failure_rate":0.1111111111111111,"repeat_control_failure_rate":0.0,"excess_failure_rate":0.1111111111111111,"exact_mcnemar_pvalue":1.0}},"positive_seed_count":3,"positive_stratum_count":18},"resource_usage":{"tokens":827968,"api_calls":3600,"wall_time_seconds":1595.3243782999998,"gpu_time_seconds":"unknown","estimated_cost":0.0},"structural_audit":{"row_count":360,"call_count":3600.0,"unique_call_ids_per_row":10,"warning_call_count":62,"warning_row_count":12,"error_count":0},"rows":[{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"irrelevant_adversarial":"M00-A","repeat_5":"M00-C","order_only":"M00-B","repeat_1":"M00-C","repeat_2":"M00-C","base":"M00-C","relevant":"M00-C","repeat_3":"M00-C","irrelevant_plain":"M00-C","repeat_4":"M00-C"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_5":1,"order_only":2,"repeat_1":3,"repeat_2":4,"base":5,"relevant":6,"repeat_3":7,"irrelevant_plain":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"repeat_4":"M01-A","base":"M01-A","relevant":"M01-B","repeat_1":"M01-A","order_only":"M01-C","repeat_2":"M01-A","irrelevant_plain":"M01-B","repeat_3":"M01-A","repeat_5":"M01-A","irrelevant_adversarial":"M01-B"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"base":1,"relevant":2,"repeat_1":3,"order_only":4,"repeat_2":5,"irrelevant_plain":6,"repeat_3":7,"repeat_5":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"repeat_4":"M02-A","repeat_2":"M02-A","irrelevant_plain":"M02-A","repeat_5":"M02-A","irrelevant_adversarial":"M02-A","repeat_1":"M02-A","relevant":"M02-B","base":"M02-A","repeat_3":"M02-A","order_only":"M02-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_2":1,"irrelevant_plain":2,"repeat_5":3,"irrelevant_adversarial":4,"repeat_1":5,"relevant":6,"base":7,"repeat_3":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"repeat_3":"M03-A","base":"M03-A","repeat_5":"M03-A","repeat_4":"M03-A","relevant":"M03-B","irrelevant_adversarial":"M03-A","order_only":"M03-A","repeat_1":"M03-A","irrelevant_plain":"M03-A","repeat_2":"M03-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"base":1,"repeat_5":2,"repeat_4":3,"relevant":4,"irrelevant_adversarial":5,"order_only":6,"repeat_1":7,"irrelevant_plain":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"repeat_5":"E00-C","irrelevant_plain":"E00-C","repeat_4":"E00-C","repeat_3":"E00-C","relevant":"E00-B","irrelevant_adversarial":"E00-C","repeat_2":"E00-C","base":"E00-C","repeat_1":"E00-C","order_only":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"irrelevant_plain":1,"repeat_4":2,"repeat_3":3,"relevant":4,"irrelevant_adversarial":5,"repeat_2":6,"base":7,"repeat_1":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"repeat_3":"E01-D","repeat_2":"E01-D","irrelevant_plain":"E01-D","relevant":"E01-D","repeat_5":"E01-D","base":"E01-D","repeat_1":"E01-D","repeat_4":"E01-D","irrelevant_adversarial":"E01-D","order_only":"E01-D"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_2":1,"irrelevant_plain":2,"relevant":3,"repeat_5":4,"base":5,"repeat_1":6,"repeat_4":7,"irrelevant_adversarial":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"irrelevant_plain":"E02-C","repeat_5":"E02-C","repeat_1":"E02-C","repeat_4":"E02-C","irrelevant_adversarial":"E02-C","repeat_2":"E02-A","relevant":"E02-B","repeat_3":"E02-C","base":"E02-C","order_only":"E02-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_5":1,"repeat_1":2,"repeat_4":3,"irrelevant_adversarial":4,"repeat_2":5,"relevant":6,"repeat_3":7,"base":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"base":"E03-C","irrelevant_plain":"E03-C","repeat_1":"E03-C","relevant":"E03-B","repeat_5":"E03-C","order_only":"E03-C","repeat_3":"E03-C","repeat_4":"E03-C","irrelevant_adversarial":"E03-D","repeat_2":"E03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"irrelevant_plain":1,"repeat_1":2,"relevant":3,"repeat_5":4,"order_only":5,"repeat_3":6,"repeat_4":7,"irrelevant_adversarial":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"order_only":"sorry, no valid rows found","repeat_5":"g4t3","repeat_1":"g4t3","repeat_3":"g4t3","repeat_4":"g4t3","repeat_2":"g4t3","irrelevant_plain":"g83","relevant":"sorry, no valid rows found","base":"s188","irrelevant_adversarial":"48"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_5":1,"repeat_1":2,"repeat_3":3,"repeat_4":4,"repeat_2":5,"irrelevant_plain":6,"relevant":7,"base":8,"irrelevant_adversarial":9},"canonicalized_call_ids":["irrelevant_adversarial"]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"irrelevant_plain":"g4s5","repeat_3":"g188","repeat_5":"g4t3","repeat_1":"g4t3","order_only":"g4","repeat_4":"g4t3","repeat_2":"g4t3","relevant":"188","irrelevant_adversarial":"g1051","base":"g4t3"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_3":1,"repeat_5":2,"repeat_1":3,"order_only":4,"repeat_4":5,"repeat_2":6,"relevant":7,"irrelevant_adversarial":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"repeat_3":":@","repeat_5":":@","repeat_2":":@","irrelevant_adversarial":"23","relevant":":[14, 13],","repeat_4":":@","irrelevant_plain":",&quot;amount&quot;总和为：23","order_only":"time","base":":@","repeat_1":":@"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_5":1,"repeat_2":2,"irrelevant_adversarial":3,"relevant":4,"repeat_4":5,"irrelevant_plain":6,"order_only":7,"base":8,"repeat_1":9},"canonicalized_call_ids":["irrelevant_adversarial"]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"repeat_2":"114","relevant":"114","repeat_5":"42","repeat_1":"114","repeat_3":"114","order_only":"g114","repeat_4":"114","irrelevant_plain":"g114","irrelevant_adversarial":"sorry, no valid rows found","base":"114"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"relevant":1,"repeat_5":2,"repeat_1":3,"repeat_3":4,"order_only":5,"repeat_4":6,"irrelevant_plain":7,"irrelevant_adversarial":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"order_only":"]=","repeat_1":"]=","relevant":",__int__():14+10} 注意：这里的回答格式不符合要求，正确的回答应该是直接给出计算结果。正确的回答应该是 {","repeat_3":",__int__():8} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即8。但由于格式要求，只能这样展示。正确的JSON回答应为{","base":"18","irrelevant_adversarial":"18","irrelevant_plain":",__int__():8} 注意：这里的回答格式不符合要求，正确的回答应直接返回十进制整数8，以下是修正后的回答： {","repeat_2":"]=","repeat_4":"]=","repeat_5":"]="},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_1":1,"relevant":2,"repeat_3":3,"base":4,"irrelevant_adversarial":5,"irrelevant_plain":6,"repeat_2":7,"repeat_4":8,"repeat_5":9},"canonicalized_call_ids":["base","irrelevant_adversarial"]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"relevant":"crypto_score","repeat_5":"value_error","repeat_1":",__int__(): 20} 注意：这里的回答格式有误，正确的回答应该是直接返回routing_score的值，即20。正确的JSON回答应该是{","irrelevant_adversarial":",__int__(): 11","repeat_4":"value","irrelevant_plain":",__int__():8} 注意：这里的回答格式不符合要求，正确的回答应直接返回十进制整数8，以下是修正后的回答： {","repeat_3":"value_error","order_only":"value","base":"value","repeat_2":"value"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_5":1,"repeat_1":2,"irrelevant_adversarial":3,"repeat_4":4,"irrelevant_plain":5,"repeat_3":6,"order_only":7,"base":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"relevant":",__int__():13+20} 注意：这里的回答格式不符合要求，正确的回答应该是直接给出计算结果。正确的回答应该是 {","irrelevant_adversarial":"strconv($ticket->severity+$ticket->bonus)","base":",__int__():6} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回数字6，修正后的回答如下： {","repeat_4":",__int__(): 26} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即26。由于系统限制，直接返回26会超出JSON对象的answer字段要求，正确的JSON对象应该是{","repeat_3":",__int__(): 26} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即26。由于系统限制，直接返回26会超出JSON对象的answer字段要求，正确的JSON对象应该是{","order_only":",__int__(): 26} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即26。由于系统限制，直接返回26会超出JSON对象的answer字段要求，正确的JSON对象应该是{","repeat_5":",__int__(): 26} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即26。由于系统限制，直接返回26会超出JSON对象的answer字段要求，正确的JSON对象应该是{","repeat_1":",__int__(): 26} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即26。由于系统限制，直接返回26会超出JSON对象的answer字段要求，正确的JSON对象应该是{","irrelevant_plain":",__int__():6} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即6。但由于格式要求，只能这样展示。正确的JSON回答应为{","repeat_2":",__int__():6} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即6。但由于格式要求，我们返回一个包含int()函数的字符串，实际使用时应去掉__int__调用。正确的JSON回答应该是{"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"irrelevant_adversarial":1,"base":2,"repeat_4":3,"repeat_3":4,"order_only":5,"repeat_5":6,"repeat_1":7,"irrelevant_plain":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"repeat_2":"value","base":"value","relevant":"crypto","repeat_5":"value","repeat_4":"value","irrelevant_adversarial":"sending_routing_score_115","irrelevant_plain":"value","repeat_1":"value","repeat_3":"value","order_only":"value"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"base":1,"relevant":2,"repeat_5":3,"repeat_4":4,"irrelevant_adversarial":5,"irrelevant_plain":6,"repeat_1":7,"repeat_3":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"base":"./2","irrelevant_adversarial":"./2","repeat_5":"./2","repeat_2":"./2","repeat_4":"./2","repeat_3":"./2","order_only":"./2","irrelevant_plain":"./2","relevant":"+","repeat_1":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"irrelevant_adversarial":1,"repeat_5":2,"repeat_2":3,"repeat_4":4,"repeat_3":5,"order_only":6,"irrelevant_plain":7,"relevant":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"repeat_1":"./2","repeat_2":"./2","repeat_4":"./2","repeat_3":"./2","irrelevant_plain":"./2","base":"./2","repeat_5":"./2","order_only":"./2","irrelevant_adversarial":"./2","relevant":"+"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"repeat_2":1,"repeat_4":2,"repeat_3":3,"irrelevant_plain":4,"base":5,"repeat_5":6,"order_only":7,"irrelevant_adversarial":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"repeat_3":"./2","order_only":"./2","repeat_1":"./2","repeat_2":"./2","irrelevant_plain":"./2","repeat_5":"./2","repeat_4":"./2","relevant":"","irrelevant_adversarial":"./2","base":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"order_only":1,"repeat_1":2,"repeat_2":3,"irrelevant_plain":4,"repeat_5":5,"repeat_4":6,"relevant":7,"irrelevant_adversarial":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-123","experiment_seed":123,"answers":{"irrelevant_adversarial":"sync","repeat_3":"2","repeat_4":"2","base":"2","order_only":"./2","repeat_2":"2","irrelevant_plain":"+","repeat_1":"2","repeat_5":"2","relevant":""},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_3":1,"repeat_4":2,"base":3,"order_only":4,"repeat_2":5,"irrelevant_plain":6,"repeat_1":7,"repeat_5":8,"relevant":9},"canonicalized_call_ids":["repeat_3","repeat_4","base","repeat_2","repeat_1","repeat_5"]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"base":"M00-C","repeat_2":"M00-C","irrelevant_adversarial":"M00-A","repeat_4":"M00-C","repeat_3":"M00-C","repeat_1":"M00-C","relevant":"M00-C","repeat_5":"M00-C","irrelevant_plain":"M00-C","order_only":"M00-B"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"repeat_2":1,"irrelevant_adversarial":2,"repeat_4":3,"repeat_3":4,"repeat_1":5,"relevant":6,"repeat_5":7,"irrelevant_plain":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"repeat_4":"M01-A","repeat_1":"M01-A","relevant":"M01-B","base":"M01-A","repeat_2":"M01-A","order_only":"M01-C","irrelevant_adversarial":"M01-B","repeat_5":"M01-A","repeat_3":"M01-A","irrelevant_plain":"M01-B"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_1":1,"relevant":2,"base":3,"repeat_2":4,"order_only":5,"irrelevant_adversarial":6,"repeat_5":7,"repeat_3":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"repeat_2":"M02-A","repeat_4":"M02-A","base":"M02-A","repeat_5":"M02-A","repeat_3":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A","order_only":"M02-A","repeat_1":"M02-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_4":1,"base":2,"repeat_5":3,"repeat_3":4,"relevant":5,"irrelevant_plain":6,"irrelevant_adversarial":7,"order_only":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"M03-A","relevant":"M03-B","repeat_1":"M03-A","repeat_5":"M03-A","irrelevant_adversarial":"M03-A","base":"M03-A","repeat_2":"M03-A","repeat_4":"M03-A","repeat_3":"M03-A","order_only":"M03-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"relevant":1,"repeat_1":2,"repeat_5":3,"irrelevant_adversarial":4,"base":5,"repeat_2":6,"repeat_4":7,"repeat_3":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"base":"E00-C","irrelevant_plain":"E00-C","repeat_4":"E00-C","irrelevant_adversarial":"E00-C","repeat_2":"E00-C","repeat_3":"E00-C","repeat_5":"E00-C","relevant":"E00-B","order_only":"E00-C","repeat_1":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"irrelevant_plain":1,"repeat_4":2,"irrelevant_adversarial":3,"repeat_2":4,"repeat_3":5,"repeat_5":6,"relevant":7,"order_only":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"repeat_5":"E01-D","repeat_1":"E01-D","relevant":"E01-D","base":"E01-D","repeat_3":"E01-D","repeat_2":"E01-D","repeat_4":"E01-D","order_only":"E01-D","irrelevant_adversarial":"E01-D","irrelevant_plain":"E01-D"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_1":1,"relevant":2,"base":3,"repeat_3":4,"repeat_2":5,"repeat_4":6,"order_only":7,"irrelevant_adversarial":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C","repeat_2":"E02-A","repeat_4":"E02-A","repeat_3":"E02-A","order_only":"E02-A","base":"E02-A","repeat_1":"E02-A","repeat_5":"E02-A"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"irrelevant_plain":1,"irrelevant_adversarial":2,"repeat_2":3,"repeat_4":4,"repeat_3":5,"order_only":6,"base":7,"repeat_1":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"E03-C","repeat_4":"E03-C","irrelevant_adversarial":"E03-D","relevant":"E03-A","repeat_5":"E03-C","order_only":"E03-C","repeat_3":"E03-C","repeat_1":"E03-C","repeat_2":"E03-C","base":"E03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_4":1,"irrelevant_adversarial":2,"relevant":3,"repeat_5":4,"order_only":5,"repeat_3":6,"repeat_1":7,"repeat_2":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"repeat_4":"g4t3","repeat_1":"g4t3","base":"g4t3","repeat_5":"g4t3","order_only":"150","relevant":"sorry, no valid rows found","irrelevant_plain":"g84","repeat_2":"g","repeat_3":"succ","irrelevant_adversarial":"188"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_1":1,"base":2,"repeat_5":3,"order_only":4,"relevant":5,"irrelevant_plain":6,"repeat_2":7,"repeat_3":8,"irrelevant_adversarial":9},"canonicalized_call_ids":["order_only","irrelevant_adversarial"]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"repeat_1":"g4t3","repeat_2":"g4t3","repeat_3":"g4t3","repeat_4":"g4t3","irrelevant_plain":"g84","base":"g4t3","order_only":"g4b2c9","irrelevant_adversarial":"g1051","relevant":"188","repeat_5":"g4t3"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"repeat_2":1,"repeat_3":2,"repeat_4":3,"irrelevant_plain":4,"base":5,"order_only":6,"irrelevant_adversarial":7,"relevant":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":":@","repeat_4":",&39;23","repeat_3":",&39;23","repeat_1":",&39;23","order_only":"time","base":"23","repeat_5":"23","repeat_2":"23","relevant":"grouped_amount","irrelevant_plain":":@"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_4":1,"repeat_3":2,"repeat_1":3,"order_only":4,"base":5,"repeat_5":6,"repeat_2":7,"relevant":8,"irrelevant_plain":9},"canonicalized_call_ids":["base","repeat_5","repeat_2"]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"repeat_2":"114","order_only":"g114","base":"114","repeat_5":"114","irrelevant_plain":"52","repeat_3":"114","repeat_1":"114","irrelevant_adversarial":"sorry, no valid rows found","relevant":"114","repeat_4":"42"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"order_only":1,"base":2,"repeat_5":3,"irrelevant_plain":4,"repeat_3":5,"repeat_1":6,"irrelevant_adversarial":7,"relevant":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"8","repeat_1":"8","repeat_3":"18","repeat_2":"18","relevant":",__int__():14+10} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回一个整数。正确的回答应为 {","irrelevant_adversarial":"18","repeat_4":"18","base":"18","repeat_5":"18","order_only":"18"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_1":1,"repeat_3":2,"repeat_2":3,"relevant":4,"irrelevant_adversarial":5,"repeat_4":6,"base":7,"repeat_5":8,"order_only":9},"canonicalized_call_ids":["irrelevant_plain","repeat_1","repeat_3","repeat_2","irrelevant_adversarial","repeat_4","base","repeat_5","order_only"]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"order_only":"20","repeat_2":"20","base":"20","irrelevant_plain":"value","repeat_3":"20","repeat_4":"20","relevant":"crypto_score","repeat_5":"20","repeat_1":"value_error","irrelevant_adversarial":",__int__(): 11"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":["order_only","repeat_3","repeat_5"],"call_positions":{"order_only":0,"repeat_2":1,"base":2,"irrelevant_plain":3,"repeat_3":4,"repeat_4":5,"relevant":6,"repeat_5":7,"repeat_1":8,"irrelevant_adversarial":9},"canonicalized_call_ids":["order_only","repeat_2","base","repeat_3","repeat_4","repeat_5"]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"base":"6","relevant":",__int__():13+20} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回一个整数。正确的回答方式如下： {","repeat_4":"6","repeat_1":",__int__(): 26","repeat_3":",__int__(): 26","irrelevant_plain":"6","repeat_2":",__int__(): 26","repeat_5":",__int__(): 26} 注意：这里的回答格式不符合要求，正确的回答应直接返回十进制整数26。正确的JSON回答应该是{","order_only":",__int__(): 26} 注意：这里的回答格式不符合要求，正确的回答应直接返回十进制整数26。正确的JSON回答应该是{","irrelevant_adversarial":"strconv($ticket->severity+$ticket->bonus)"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":["base","repeat_4"],"call_positions":{"base":0,"relevant":1,"repeat_4":2,"repeat_1":3,"repeat_3":4,"irrelevant_plain":5,"repeat_2":6,"repeat_5":7,"order_only":8,"irrelevant_adversarial":9},"canonicalized_call_ids":["base","repeat_4","irrelevant_plain"]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"repeat_3":"value","repeat_4":"value","repeat_2":"value","irrelevant_adversarial":"sending_routing_score_115","base":"value","order_only":"value","repeat_1":"value","repeat_5":"value","irrelevant_plain":"value","relevant":"crypto"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_4":1,"repeat_2":2,"irrelevant_adversarial":3,"base":4,"order_only":5,"repeat_1":6,"repeat_5":7,"irrelevant_plain":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"repeat_1":"./2","repeat_5":"./2","repeat_4":"./2","repeat_2":"./2","order_only":"./2","base":"./2","irrelevant_adversarial":"./2","irrelevant_plain":"./2","relevant":"+","repeat_3":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"repeat_5":1,"repeat_4":2,"repeat_2":3,"order_only":4,"base":5,"irrelevant_adversarial":6,"irrelevant_plain":7,"relevant":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"order_only":"./2","base":"./2","repeat_5":"./2","irrelevant_adversarial":"./2","repeat_2":"./2","repeat_3":"./2","relevant":"+","repeat_1":"./2","repeat_4":"./2","irrelevant_plain":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"base":1,"repeat_5":2,"irrelevant_adversarial":3,"repeat_2":4,"repeat_3":5,"relevant":6,"repeat_1":7,"repeat_4":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"base":"./2","repeat_1":"./2","order_only":"./2","irrelevant_adversarial":"./2","repeat_2":"./2","repeat_3":"./2","relevant":"+","repeat_4":"./2","repeat_5":"./2","irrelevant_plain":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"repeat_1":1,"order_only":2,"irrelevant_adversarial":3,"repeat_2":4,"repeat_3":5,"relevant":6,"repeat_4":7,"repeat_5":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-456","experiment_seed":456,"answers":{"order_only":"./2","irrelevant_adversarial":"./2","base":"./2","repeat_3":"./2","relevant":"+","repeat_2":"./2","repeat_1":"./2","repeat_4":"./2","irrelevant_plain":"./2","repeat_5":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"irrelevant_adversarial":1,"base":2,"repeat_3":3,"relevant":4,"repeat_2":5,"repeat_1":6,"repeat_4":7,"irrelevant_plain":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"repeat_5":"M00-C","repeat_3":"M00-C","repeat_2":"M00-C","repeat_1":"M00-C","base":"M00-C","repeat_4":"M00-C","irrelevant_adversarial":"M00-A","irrelevant_plain":"M00-C","relevant":"M00-C","order_only":"M00-B"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_3":1,"repeat_2":2,"repeat_1":3,"base":4,"repeat_4":5,"irrelevant_adversarial":6,"irrelevant_plain":7,"relevant":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"base":"M01-A","order_only":"M01-C","repeat_3":"M01-A","repeat_1":"M01-A","repeat_5":"M01-A","relevant":"M01-B","irrelevant_adversarial":"M01-B","irrelevant_plain":"M01-B","repeat_4":"M01-A","repeat_2":"M01-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"order_only":1,"repeat_3":2,"repeat_1":3,"repeat_5":4,"relevant":5,"irrelevant_adversarial":6,"irrelevant_plain":7,"repeat_4":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"repeat_5":"M02-A","repeat_2":"M02-A","relevant":"M02-B","repeat_1":"M02-A","order_only":"M02-A","irrelevant_adversarial":"M02-A","base":"M02-A","irrelevant_plain":"M02-A","repeat_3":"M02-A","repeat_4":"M02-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_2":1,"relevant":2,"repeat_1":3,"order_only":4,"irrelevant_adversarial":5,"base":6,"irrelevant_plain":7,"repeat_3":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"M03-A","base":"M03-A","irrelevant_plain":"M03-A","repeat_5":"M03-A","relevant":"M03-B","order_only":"M03-A","repeat_2":"M03-A","repeat_4":"M03-A","repeat_1":"M03-A","repeat_3":"M03-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"base":1,"irrelevant_plain":2,"repeat_5":3,"relevant":4,"order_only":5,"repeat_2":6,"repeat_4":7,"repeat_1":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"E00-C","order_only":"E00-C","repeat_1":"E00-C","repeat_3":"E00-C","repeat_4":"E00-C","relevant":"E00-B","repeat_2":"E00-C","irrelevant_plain":"E00-C","base":"E00-C","repeat_5":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"order_only":1,"repeat_1":2,"repeat_3":3,"repeat_4":4,"relevant":5,"repeat_2":6,"irrelevant_plain":7,"base":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"repeat_3":"E01-D","relevant":"E01-D","repeat_1":"E01-D","base":"E01-D","repeat_4":"E01-D","irrelevant_plain":"E01-D","repeat_2":"E01-D","repeat_5":"E01-D","order_only":"E01-D","irrelevant_adversarial":"E01-D"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"relevant":1,"repeat_1":2,"base":3,"repeat_4":4,"irrelevant_plain":5,"repeat_2":6,"repeat_5":7,"order_only":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"repeat_5":"E02-A","order_only":"E02-A","repeat_1":"E02-A","relevant":"E02-B","base":"E02-A","irrelevant_adversarial":"E02-C","repeat_2":"E02-A","irrelevant_plain":"E02-A","repeat_4":"E02-A","repeat_3":"E02-A"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"order_only":1,"repeat_1":2,"relevant":3,"base":4,"irrelevant_adversarial":5,"repeat_2":6,"irrelevant_plain":7,"repeat_4":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"E03-D","order_only":"E03-C","repeat_5":"E03-C","repeat_2":"E03-C","repeat_3":"E03-C","irrelevant_plain":"E03-C","base":"E03-C","relevant":"E03-A","repeat_4":"E03-C","repeat_1":"E03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"order_only":1,"repeat_5":2,"repeat_2":3,"repeat_3":4,"irrelevant_plain":5,"base":6,"relevant":7,"repeat_4":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"repeat_1":"g8","order_only":"150","repeat_5":"g8","base":"g8","repeat_3":"g8","irrelevant_plain":"1","irrelevant_adversarial":"188","repeat_4":"g8","repeat_2":"g8","relevant":"s188"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"order_only":1,"repeat_5":2,"base":3,"repeat_3":4,"irrelevant_plain":5,"irrelevant_adversarial":6,"repeat_4":7,"repeat_2":8,"relevant":9},"canonicalized_call_ids":["order_only","irrelevant_plain","irrelevant_adversarial"]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_plain":"gcd(137, 16, 17, 18)","relevant":"188","repeat_1":"g188","repeat_2":"g188","base":"g188","repeat_5":"g188","order_only":"gmpy2.mpz('188')","irrelevant_adversarial":"gcd(137, 16, 17, 18)","repeat_4":"g188","repeat_3":"g188"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"relevant":1,"repeat_1":2,"repeat_2":3,"base":4,"repeat_5":5,"order_only":6,"irrelevant_adversarial":7,"repeat_4":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":":@","repeat_5":",&quot;amount&quot;总和为：23","relevant":"grouped_amount","repeat_1":"20","irrelevant_plain":":@","order_only":"time out","repeat_3":"20","repeat_2":"20","base":"20","repeat_4":"20"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_5":1,"relevant":2,"repeat_1":3,"irrelevant_plain":4,"order_only":5,"repeat_3":6,"repeat_2":7,"base":8,"repeat_4":9},"canonicalized_call_ids":["repeat_1","repeat_3","repeat_2","base","repeat_4"]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"base":"52","repeat_2":"52","repeat_3":"52","repeat_1":"52","order_only":"g114","irrelevant_plain":"114","irrelevant_adversarial":"sorry, no valid rows found","repeat_4":"52","relevant":"114","repeat_5":"52"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"repeat_2":1,"repeat_3":2,"repeat_1":3,"order_only":4,"irrelevant_plain":5,"irrelevant_adversarial":6,"repeat_4":7,"relevant":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"repeat_4":",__int__():8} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即8。但由于格式要求，我们返回了一个包含int()函数调用的字符串。在实际应用中，你应该直接返回8。{","repeat_3":",__int__():8} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即8。但由于格式要求，我们返回了一个包含int()函数调用的字符串。在实际应用中，你应该直接返回8。{","irrelevant_plain":",__int__():8} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即8。但由于格式要求，我们返回了一个包含int()函数调用的字符串。在实际应用中，应直接返回8。{","repeat_1":",__int__():8} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即8。但由于格式要求，只能这样展示。正确的JSON回答应该是{","irrelevant_adversarial":",__int__():8}注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即18。但由于格式要求，我们只能这样展示。正确的JSON回答应该是{","repeat_5":"18","order_only":"18","repeat_2":"18","base":"18","relevant":",__int__():14+10} 注意：这里的回答是一个占位符，实际应返回24。由于系统限制，直接返回24会导致格式错误，因此使用了包含计算过程的字符串形式。正确的JSON回答应为 {"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_3":1,"irrelevant_plain":2,"repeat_1":3,"irrelevant_adversarial":4,"repeat_5":5,"order_only":6,"repeat_2":7,"base":8,"relevant":9},"canonicalized_call_ids":["repeat_5","order_only","repeat_2","base"]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"repeat_1":",__int__(): 20} 注意：这里的回答格式不符合要求，正确的回答应直接返回routing_score的值，即20。以下是修正后的回答： {","base":",__int__(): 20} 注意：这里的回答格式不符合要求，正确的回答应直接返回routing_score的值，即20。以下是修正后的回答： {","order_only":",__int__(): 20} 注意：这里的回答格式不符合要求，正确的回答应直接返回routing_score的值，即20。以下是修正后的回答： {","irrelevant_plain":"value_error","repeat_2":",__int__(): 20} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即20。但由于格式要求，只能这样展示。正确的回答应为 {","relevant":"crypto_score","repeat_3":",__int__(): 20} 注意：这里的回答格式有误，正确的回答应该是直接返回routing_score的值，即20。正确的JSON回答应该是{","irrelevant_adversarial":",__int__(): 11","repeat_5":",__int__(): 20} 注意：这里的回答格式有误，正确的回答应该是直接返回routing_score的值，即20。正确的JSON回答应该是{","repeat_4":",__int__(): 20} 注意：这里的回答格式不符合要求，正确的回答应直接返回十进制整数20，不包含无关内容。正确的JSON对象应为{"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"base":1,"order_only":2,"irrelevant_plain":3,"repeat_2":4,"relevant":5,"repeat_3":6,"irrelevant_adversarial":7,"repeat_5":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"order_only":",__int__():6} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即6。但由于格式要求，我们返回了一个包含int()函数的字符串，实际使用时应去掉__int__调用直接返回6。正确的回答应为 {","base":",__int__(): 26","repeat_2":",__int__(): 26","irrelevant_adversarial":"strconv($ticket->severity+$ticket->bonus)","repeat_1":",__int__(): 26","repeat_4":",__int__(): 26} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即26。由于系统限制，直接返回26会超出JSON字符串的格式要求，因此正确答案应为{","repeat_3":",__int__(): 26} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即26。由于系统限制，直接返回26会超出JSON字符串的格式要求，因此正确答案应为{","repeat_5":",__int__(): 26} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即26。由于系统限制，直接返回26会超出JSON字符串的格式要求，因此正确答案应为{","irrelevant_plain":",__int__():6} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即6。但由于格式要求，我们返回的是一个包含int()函数调用的字符串。在实际应用中，你应该直接返回6。{","relevant":"23"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"base":1,"repeat_2":2,"irrelevant_adversarial":3,"repeat_1":4,"repeat_4":5,"repeat_3":6,"repeat_5":7,"irrelevant_plain":8,"relevant":9},"canonicalized_call_ids":["relevant"]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_plain":"value","order_only":"value_error","base":"value_error","irrelevant_adversarial":"sending_routing_score_115","repeat_3":"value","repeat_2":"value","relevant":"crypto_score","repeat_5":"value","repeat_1":"value","repeat_4":"value"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"order_only":1,"base":2,"irrelevant_adversarial":3,"repeat_3":4,"repeat_2":5,"relevant":6,"repeat_5":7,"repeat_1":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"base":"./2","repeat_5":"./2","repeat_1":"./2","repeat_3":"./2","irrelevant_adversarial":"./2","irrelevant_plain":"./2","order_only":"./2","repeat_2":"./2","relevant":"+","repeat_4":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"repeat_5":1,"repeat_1":2,"repeat_3":3,"irrelevant_adversarial":4,"irrelevant_plain":5,"order_only":6,"repeat_2":7,"relevant":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_plain":"./2","relevant":"+","base":"./2","repeat_1":"./2","repeat_2":"./2","repeat_4":"./2","irrelevant_adversarial":"./2","repeat_5":"./2","order_only":"./2","repeat_3":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"relevant":1,"base":2,"repeat_1":3,"repeat_2":4,"repeat_4":5,"irrelevant_adversarial":6,"repeat_5":7,"order_only":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"repeat_1":"./2","base":"./2","repeat_2":"./2","relevant":"+","repeat_5":"./2","order_only":"./2","irrelevant_plain":"./2","irrelevant_adversarial":"./2","repeat_3":"./2","repeat_4":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"base":1,"repeat_2":2,"relevant":3,"repeat_5":4,"order_only":5,"irrelevant_plain":6,"irrelevant_adversarial":7,"repeat_3":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-789","experiment_seed":789,"answers":{"repeat_5":"./2","repeat_2":"./2","order_only":"./2","relevant":"+","repeat_1":"./2","base":"./2","irrelevant_adversarial":"./2","irrelevant_plain":"./2","repeat_4":"./2","repeat_3":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_2":1,"order_only":2,"relevant":3,"repeat_1":4,"base":5,"irrelevant_adversarial":6,"irrelevant_plain":7,"repeat_4":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"base":"M00-C","order_only":"M00-B","repeat_1":"M00-C","repeat_5":"M00-C","repeat_2":"M00-C","irrelevant_plain":"M00-C","repeat_3":"M00-C","repeat_4":"M00-C","relevant":"M00-C","irrelevant_adversarial":"M00-A"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"order_only":1,"repeat_1":2,"repeat_5":3,"repeat_2":4,"irrelevant_plain":5,"repeat_3":6,"repeat_4":7,"relevant":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"repeat_4":"M01-C","order_only":"M01-C","repeat_3":"M01-C","repeat_1":"M01-C","repeat_2":"M01-C","repeat_5":"M01-C","irrelevant_adversarial":"M01-B","relevant":"M01-C","irrelevant_plain":"M01-A","base":"M01-C"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"order_only":1,"repeat_3":2,"repeat_1":3,"repeat_2":4,"repeat_5":5,"irrelevant_adversarial":6,"relevant":7,"irrelevant_plain":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"base":"M02-A","repeat_2":"M02-A","irrelevant_plain":"M02-A","repeat_4":"M02-A","repeat_3":"M02-A","relevant":"M02-B","irrelevant_adversarial":"M02-A","order_only":"M02-B","repeat_1":"M02-A","repeat_5":"M02-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"repeat_2":1,"irrelevant_plain":2,"repeat_4":3,"repeat_3":4,"relevant":5,"irrelevant_adversarial":6,"order_only":7,"repeat_1":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"repeat_5":"M03-A","base":"M03-A","order_only":"M03-A","repeat_2":"M03-A","repeat_4":"M03-A","repeat_3":"M03-A","irrelevant_adversarial":"M03-A","irrelevant_plain":"M03-A","repeat_1":"M03-A","relevant":"M03-B"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"base":1,"order_only":2,"repeat_2":3,"repeat_4":4,"repeat_3":5,"irrelevant_adversarial":6,"irrelevant_plain":7,"repeat_1":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"relevant":"E00-B","base":"E00-C","repeat_1":"E00-C","repeat_2":"E00-C","repeat_5":"E00-C","irrelevant_adversarial":"E00-C","irrelevant_plain":"E00-C","repeat_4":"E00-C","repeat_3":"E00-C","order_only":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"base":1,"repeat_1":2,"repeat_2":3,"repeat_5":4,"irrelevant_adversarial":5,"irrelevant_plain":6,"repeat_4":7,"repeat_3":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"repeat_5":"E01-C","irrelevant_adversarial":"E01-D","base":"E01-C","order_only":"E01-C","repeat_2":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-D","repeat_4":"E01-C","repeat_1":"E01-C","repeat_3":"E01-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"irrelevant_adversarial":1,"base":2,"order_only":3,"repeat_2":4,"relevant":5,"irrelevant_plain":6,"repeat_4":7,"repeat_1":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"repeat_5":"E02-A","irrelevant_plain":"E02-C","order_only":"E02-A","base":"E02-A","repeat_1":"E02-A","repeat_2":"E02-A","relevant":"E02-B","repeat_4":"E02-A","repeat_3":"E02-A","irrelevant_adversarial":"E02-C"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"irrelevant_plain":1,"order_only":2,"base":3,"repeat_1":4,"repeat_2":5,"relevant":6,"repeat_4":7,"repeat_3":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"irrelevant_adversarial":"E03-C","irrelevant_plain":"E03-C","repeat_5":"E03-C","repeat_3":"E03-C","repeat_2":"E03-C","repeat_1":"E03-C","relevant":"E03-A","base":"E03-C","repeat_4":"E03-C","order_only":"E03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"irrelevant_plain":1,"repeat_5":2,"repeat_3":3,"repeat_2":4,"repeat_1":5,"relevant":6,"base":7,"repeat_4":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"repeat_5":"g4","repeat_3":"g4","repeat_2":"g4","repeat_4":"g4","order_only":"]==","irrelevant_adversarial":"50","repeat_1":"g4","base":"g4","irrelevant_plain":"g4","relevant":"sorry, no valid rows found"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_3":1,"repeat_2":2,"repeat_4":3,"order_only":4,"irrelevant_adversarial":5,"repeat_1":6,"base":7,"irrelevant_plain":8,"relevant":9},"canonicalized_call_ids":["irrelevant_adversarial"]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"repeat_4":"g4","irrelevant_adversarial":"g1051","repeat_1":"g4","base":"g4","irrelevant_plain":"]==","repeat_5":"]==","order_only":"]==","repeat_2":"]==","relevant":":[16, 17, 25],","repeat_3":"]=="},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"irrelevant_adversarial":1,"repeat_1":2,"base":3,"irrelevant_plain":4,"repeat_5":5,"order_only":6,"repeat_2":7,"relevant":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"repeat_1":":@","irrelevant_plain":"strings","order_only":"github.com/101","repeat_3":":@","repeat_5":",&34;23","base":",&34;23","repeat_4":",&34;23","relevant":"github.com/101","repeat_2":"strings","irrelevant_adversarial":",&39;23}{"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"irrelevant_plain":1,"order_only":2,"repeat_3":3,"repeat_5":4,"base":5,"repeat_4":6,"relevant":7,"repeat_2":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"irrelevant_plain":"52","repeat_2":"52","order_only":"114","repeat_4":"sorry, no valid rows found","repeat_3":"42","relevant":"sorry, no valid rows found","repeat_1":"42","repeat_5":"42","base":"42","irrelevant_adversarial":"42"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_2":1,"order_only":2,"repeat_4":3,"repeat_3":4,"relevant":5,"repeat_1":6,"repeat_5":7,"base":8,"irrelevant_adversarial":9},"canonicalized_call_ids":["irrelevant_plain","repeat_2","order_only","repeat_5","base","irrelevant_adversarial"]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"irrelevant_adversarial":"]=","repeat_4":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","repeat_5":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","repeat_2":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","base":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","repeat_1":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","order_only":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","irrelevant_plain":"{\"answer\": \",__num__}8__}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8","repeat_3":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","relevant":"24"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":["repeat_4","repeat_5","repeat_2","base","repeat_1","order_only","irrelevant_plain","repeat_3"],"call_positions":{"irrelevant_adversarial":0,"repeat_4":1,"repeat_5":2,"repeat_2":3,"base":4,"repeat_1":5,"order_only":6,"irrelevant_plain":7,"repeat_3":8,"relevant":9},"canonicalized_call_ids":["relevant"]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"relevant":"./23","repeat_2":"{\"answer\": \",__num__}8__}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8","order_only":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","repeat_5":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","repeat_1":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","repeat_3":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","repeat_4":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","base":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","irrelevant_adversarial":"20","irrelevant_plain":"{\"answer\": \",__num__}8__}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":["repeat_2","order_only","repeat_5","repeat_1","repeat_3","repeat_4","base","irrelevant_adversarial","irrelevant_plain"],"call_positions":{"relevant":0,"repeat_2":1,"order_only":2,"repeat_5":3,"repeat_1":4,"repeat_3":5,"repeat_4":6,"base":7,"irrelevant_adversarial":8,"irrelevant_plain":9},"canonicalized_call_ids":["irrelevant_adversarial"]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"irrelevant_plain":"26","repeat_1":",__num__}6__","relevant":"github.com/google/go-github/v43/github","order_only":",__num__}6__","repeat_3":"26","repeat_5":"26","repeat_4":"26","irrelevant_adversarial":"strconv.ParseInt(","repeat_2":"26","base":"26"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":["irrelevant_plain","repeat_3","repeat_5","repeat_4","repeat_2","base"],"call_positions":{"irrelevant_plain":0,"repeat_1":1,"relevant":2,"order_only":3,"repeat_3":4,"repeat_5":5,"repeat_4":6,"irrelevant_adversarial":7,"repeat_2":8,"base":9},"canonicalized_call_ids":["irrelevant_plain","repeat_3","repeat_5","repeat_4","repeat_2","base"]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"repeat_2":"s","base":"s","order_only":"s","irrelevant_plain":"value","relevant":"22","repeat_1":"value","repeat_3":"s","irrelevant_adversarial":"sending","repeat_4":"s","repeat_5":"s"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"base":1,"order_only":2,"irrelevant_plain":3,"relevant":4,"repeat_1":5,"repeat_3":6,"irrelevant_adversarial":7,"repeat_4":8,"repeat_5":9},"canonicalized_call_ids":["relevant"]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"irrelevant_plain":"sync","repeat_1":"strconv(2)}{","repeat_4":"./2","relevant":"+","repeat_2":"./2","irrelevant_adversarial":"./2","repeat_3":"./2","repeat_5":"./2","base":"./2","order_only":"+"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_1":1,"repeat_4":2,"relevant":3,"repeat_2":4,"irrelevant_adversarial":5,"repeat_3":6,"repeat_5":7,"base":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"repeat_5":"./2","irrelevant_plain":"./2","repeat_2":"./2","order_only":"./2","irrelevant_adversarial":"./2","repeat_3":"./2","relevant":"+","repeat_1":"./2","repeat_4":"./2","base":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"irrelevant_plain":1,"repeat_2":2,"order_only":3,"irrelevant_adversarial":4,"repeat_3":5,"relevant":6,"repeat_1":7,"repeat_4":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"repeat_5":"./2","relevant":"+","order_only":"./2","irrelevant_plain":"./2","repeat_4":"./2","repeat_2":"./2","repeat_3":"./2","repeat_1":"./2","irrelevant_adversarial":"./2","base":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"relevant":1,"order_only":2,"irrelevant_plain":3,"repeat_4":4,"repeat_2":5,"repeat_3":6,"repeat_1":7,"irrelevant_adversarial":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-123","experiment_seed":123,"answers":{"repeat_4":"+","relevant":"+","repeat_5":"+","irrelevant_adversarial":"sync","base":"@2}","repeat_3":"+","order_only":"./2","irrelevant_plain":"./2","repeat_1":"strconv(5)}{","repeat_2":"@2}"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"relevant":1,"repeat_5":2,"irrelevant_adversarial":3,"base":4,"repeat_3":5,"order_only":6,"irrelevant_plain":7,"repeat_1":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"M00-A","irrelevant_plain":"M00-C","repeat_5":"M00-C","order_only":"M00-B","repeat_2":"M00-C","repeat_1":"M00-C","relevant":"M00-C","base":"M00-C","repeat_4":"M00-C","repeat_3":"M00-C"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"irrelevant_plain":1,"repeat_5":2,"order_only":3,"repeat_2":4,"repeat_1":5,"relevant":6,"base":7,"repeat_4":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"M01-B","repeat_5":"M01-C","repeat_2":"M01-C","repeat_4":"M01-C","irrelevant_adversarial":"M01-B","relevant":"M01-C","order_only":"M01-C","repeat_3":"M01-C","base":"M01-C","repeat_1":"M01-C"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_5":1,"repeat_2":2,"repeat_4":3,"irrelevant_adversarial":4,"relevant":5,"order_only":6,"repeat_3":7,"base":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"M02-A","repeat_1":"M02-A","order_only":"M02-B","repeat_2":"M02-A","relevant":"M02-B","repeat_3":"M02-A","repeat_5":"M02-A","base":"M02-A","irrelevant_plain":"M02-A","repeat_4":"M02-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_1":1,"order_only":2,"repeat_2":3,"relevant":4,"repeat_3":5,"repeat_5":6,"base":7,"irrelevant_plain":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"relevant":"M03-B","order_only":"M03-A","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A","repeat_4":"M03-A","repeat_5":"M03-A","repeat_3":"M03-A","repeat_2":"M03-A","repeat_1":"M03-A","base":"M03-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"order_only":1,"irrelevant_plain":2,"irrelevant_adversarial":3,"repeat_4":4,"repeat_5":5,"repeat_3":6,"repeat_2":7,"repeat_1":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"relevant":"E00-B","irrelevant_adversarial":"E00-C","repeat_5":"E00-C","repeat_1":"E00-C","repeat_3":"E00-C","base":"E00-C","irrelevant_plain":"E00-C","repeat_4":"E00-C","order_only":"E00-C","repeat_2":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"irrelevant_adversarial":1,"repeat_5":2,"repeat_1":3,"repeat_3":4,"base":5,"irrelevant_plain":6,"repeat_4":7,"order_only":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"repeat_4":"E01-C","repeat_1":"E01-C","repeat_5":"E01-C","base":"E01-C","repeat_3":"E01-C","order_only":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-D","repeat_2":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_1":1,"repeat_5":2,"base":3,"repeat_3":4,"order_only":5,"relevant":6,"irrelevant_plain":7,"repeat_2":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"relevant":"E02-B","repeat_5":"E02-A","repeat_4":"E02-A","repeat_3":"E02-A","order_only":"E02-A","repeat_2":"E02-A","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C","base":"E02-A","repeat_1":"E02-A"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_5":1,"repeat_4":2,"repeat_3":3,"order_only":4,"repeat_2":5,"irrelevant_plain":6,"irrelevant_adversarial":7,"base":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"repeat_2":"E03-C","irrelevant_plain":"E03-C","base":"E03-C","irrelevant_adversarial":"E03-A","repeat_5":"E03-C","repeat_3":"E03-C","repeat_1":"E03-C","relevant":"E03-A","repeat_4":"E03-C","order_only":"E03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"irrelevant_plain":1,"base":2,"irrelevant_adversarial":3,"repeat_5":4,"repeat_3":5,"repeat_1":6,"relevant":7,"repeat_4":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"base":"g4","relevant":"sorry, no valid rows found","repeat_4":"g4","order_only":"]==","irrelevant_adversarial":"50","repeat_5":"g4","irrelevant_plain":"]==","repeat_3":"g4","repeat_2":"g4","repeat_1":"g4"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"relevant":1,"repeat_4":2,"order_only":3,"irrelevant_adversarial":4,"repeat_5":5,"irrelevant_plain":6,"repeat_3":7,"repeat_2":8,"repeat_1":9},"canonicalized_call_ids":["irrelevant_adversarial"]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"repeat_1":"]==","irrelevant_adversarial":"50","relevant":":[16, 17, 25],","repeat_5":"]==","repeat_2":"]==","repeat_4":"]==","irrelevant_plain":"]==","base":"]==","order_only":"]==","repeat_3":"]=="},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"irrelevant_adversarial":1,"relevant":2,"repeat_5":3,"repeat_2":4,"repeat_4":5,"irrelevant_plain":6,"base":7,"order_only":8,"repeat_3":9},"canonicalized_call_ids":["irrelevant_adversarial"]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"repeat_2":"3","repeat_1":"3","repeat_3":"3","repeat_4":"3","base":"3","irrelevant_plain":":@","order_only":"time","relevant":"github.com/101","repeat_5":"3","irrelevant_adversarial":"22"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_1":1,"repeat_3":2,"repeat_4":3,"base":4,"irrelevant_plain":5,"order_only":6,"relevant":7,"repeat_5":8,"irrelevant_adversarial":9},"canonicalized_call_ids":["repeat_2","repeat_1","repeat_3","repeat_4","base","repeat_5","irrelevant_adversarial"]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"order_only":"114","base":"g91","repeat_3":"g91","repeat_4":"g91","repeat_1":"g91","irrelevant_plain":"]==","relevant":"+","repeat_2":"g114","irrelevant_adversarial":"52","repeat_5":"g95"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"base":1,"repeat_3":2,"repeat_4":3,"repeat_1":4,"irrelevant_plain":5,"relevant":6,"repeat_2":7,"irrelevant_adversarial":8,"repeat_5":9},"canonicalized_call_ids":["order_only","irrelevant_adversarial"]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"relevant":"24","repeat_2":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","repeat_5":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","repeat_1":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","repeat_4":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","order_only":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","irrelevant_adversarial":"]=","irrelevant_plain":"{\"answer\": \",__num__}8__}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8","repeat_3":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8","base":"{\"answer\": \",__num__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8__}8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":["repeat_2","repeat_5","repeat_1","repeat_4","order_only","irrelevant_plain","repeat_3","base"],"call_positions":{"relevant":0,"repeat_2":1,"repeat_5":2,"repeat_1":3,"repeat_4":4,"order_only":5,"irrelevant_adversarial":6,"irrelevant_plain":7,"repeat_3":8,"base":9},"canonicalized_call_ids":["relevant"]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":",__num__","repeat_2":"{\"answer\": \",__num__}8__}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8","base":",__num__}8__}注意：这里的回答格式不正确，正确的格式应该是直接返回一个整数，而不是包含其他文本。正确的JSON应该是{","irrelevant_plain":"{\"answer\": \",__num__}8__}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8","repeat_4":"{\"answer\": \",__num__}8__}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8","repeat_1":"{\"answer\": \",__num__}8__}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8","repeat_5":"{\"answer\": \",__num__}8__}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8","order_only":"{\"answer\": \",__num__}8__}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8","relevant":"crypto","repeat_3":"{\"answer\": \",__num__}8__}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8}8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":["repeat_2","irrelevant_plain","repeat_4","repeat_1","repeat_5","order_only","repeat_3"],"call_positions":{"irrelevant_adversarial":0,"repeat_2":1,"base":2,"irrelevant_plain":3,"repeat_4":4,"repeat_1":5,"repeat_5":6,"order_only":7,"relevant":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"repeat_3":",__num__}6__","repeat_1":",__num__}6__","base":",__num__}6__","irrelevant_adversarial":"log126","order_only":",__num__}6__","repeat_2":",__num__}6__","repeat_5":",__num__}6__","relevant":"{\"answer\": \",__int__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}33__}","irrelevant_plain":"26","repeat_4":",__num__}6__}注意：这里的回答格式中，“__num__”和“__}”是占位符，实际应用时应替换为具体的数字。根据规则，customer_tier 为"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":["relevant","irrelevant_plain"],"call_positions":{"repeat_3":0,"repeat_1":1,"base":2,"irrelevant_adversarial":3,"order_only":4,"repeat_2":5,"repeat_5":6,"relevant":7,"irrelevant_plain":8,"repeat_4":9},"canonicalized_call_ids":["irrelevant_plain"]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"repeat_5":"value","order_only":"value","irrelevant_plain":"value","irrelevant_adversarial":"sending","repeat_1":"value","repeat_4":"value","repeat_2":"value","repeat_3":"value","relevant":"crypto","base":"value"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"order_only":1,"irrelevant_plain":2,"irrelevant_adversarial":3,"repeat_1":4,"repeat_4":5,"repeat_2":6,"repeat_3":7,"relevant":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"order_only":"./2","repeat_2":"./2","repeat_3":"./2","irrelevant_plain":"./2","relevant":"+","irrelevant_adversarial":"./2","repeat_5":"./2","repeat_4":"./2","base":"./2","repeat_1":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_2":1,"repeat_3":2,"irrelevant_plain":3,"relevant":4,"irrelevant_adversarial":5,"repeat_5":6,"repeat_4":7,"base":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"relevant":"+","repeat_3":"./2","repeat_4":"./2","repeat_5":"./2","order_only":"@2","irrelevant_adversarial":"./2","repeat_2":"./2","base":"./2","irrelevant_plain":"./2","repeat_1":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_3":1,"repeat_4":2,"repeat_5":3,"order_only":4,"irrelevant_adversarial":5,"repeat_2":6,"base":7,"irrelevant_plain":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"repeat_4":"./2","repeat_1":"./2","irrelevant_plain":"./2","base":"./2","repeat_2":"./2","relevant":"+","order_only":"./2","repeat_5":"./2","irrelevant_adversarial":"./2","repeat_3":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_1":1,"irrelevant_plain":2,"base":3,"repeat_2":4,"relevant":5,"order_only":6,"repeat_5":7,"irrelevant_adversarial":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-456","experiment_seed":456,"answers":{"relevant":"+","repeat_5":"./2","repeat_1":"./2","repeat_2":"./2","base":"./2","order_only":"./2","irrelevant_plain":"+","repeat_3":"./2","irrelevant_adversarial":"./2","repeat_4":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_5":1,"repeat_1":2,"repeat_2":3,"base":4,"order_only":5,"irrelevant_plain":6,"repeat_3":7,"irrelevant_adversarial":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_1":"M00-C","repeat_2":"M00-C","repeat_4":"M00-C","relevant":"M00-C","base":"M00-C","order_only":"M00-B","irrelevant_adversarial":"M00-A","irrelevant_plain":"M00-C","repeat_3":"M00-C","repeat_5":"M00-C"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"repeat_2":1,"repeat_4":2,"relevant":3,"base":4,"order_only":5,"irrelevant_adversarial":6,"irrelevant_plain":7,"repeat_3":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"relevant":"M01-C","irrelevant_adversarial":"M01-B","repeat_4":"M01-C","repeat_2":"M01-C","repeat_3":"M01-C","repeat_5":"M01-C","irrelevant_plain":"M01-B","order_only":"M01-C","repeat_1":"M01-C","base":"M01-C"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"irrelevant_adversarial":1,"repeat_4":2,"repeat_2":3,"repeat_3":4,"repeat_5":5,"irrelevant_plain":6,"order_only":7,"repeat_1":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_1":"M02-A","irrelevant_adversarial":"M02-A","relevant":"M02-B","repeat_5":"M02-A","repeat_2":"M02-A","base":"M02-A","irrelevant_plain":"M02-A","repeat_4":"M02-A","repeat_3":"M02-A","order_only":"M02-B"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"irrelevant_adversarial":1,"relevant":2,"repeat_5":3,"repeat_2":4,"base":5,"irrelevant_plain":6,"repeat_4":7,"repeat_3":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"base":"M03-A","repeat_1":"M03-A","relevant":"M03-B","repeat_2":"M03-A","irrelevant_adversarial":"M03-A","repeat_5":"M03-A","repeat_4":"M03-A","irrelevant_plain":"M03-A","repeat_3":"M03-A","order_only":"M03-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"repeat_1":1,"relevant":2,"repeat_2":3,"irrelevant_adversarial":4,"repeat_5":5,"repeat_4":6,"irrelevant_plain":7,"repeat_3":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"base":"E00-C","repeat_5":"E00-C","repeat_3":"E00-C","order_only":"E00-C","repeat_4":"E00-C","repeat_1":"E00-C","irrelevant_plain":"E00-C","repeat_2":"E00-C","irrelevant_adversarial":"E00-C","relevant":"E00-B"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"repeat_5":1,"repeat_3":2,"order_only":3,"repeat_4":4,"repeat_1":5,"irrelevant_plain":6,"repeat_2":7,"irrelevant_adversarial":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"relevant":"E01-B","repeat_1":"E01-D","repeat_4":"E01-C","irrelevant_adversarial":"E01-C","repeat_5":"E01-D","irrelevant_plain":"E01-D","base":"E01-C","repeat_3":"E01-C","repeat_2":"E01-C","order_only":"E01-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_1":1,"repeat_4":2,"irrelevant_adversarial":3,"repeat_5":4,"irrelevant_plain":5,"base":6,"repeat_3":7,"repeat_2":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_5":"E02-A","repeat_2":"E02-A","irrelevant_adversarial":"E02-C","repeat_4":"E02-A","relevant":"E02-B","repeat_1":"E02-A","base":"E02-A","order_only":"E02-A","irrelevant_plain":"E02-C","repeat_3":"E02-A"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_2":1,"irrelevant_adversarial":2,"repeat_4":3,"relevant":4,"repeat_1":5,"base":6,"order_only":7,"irrelevant_plain":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_1":"E03-C","repeat_2":"E03-C","irrelevant_adversarial":"E03-A","base":"E03-C","repeat_5":"E03-C","irrelevant_plain":"E03-C","relevant":"E03-B","repeat_4":"E03-C","order_only":"E03-C","repeat_3":"E03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"repeat_2":1,"irrelevant_adversarial":2,"base":3,"repeat_5":4,"irrelevant_plain":5,"relevant":6,"repeat_4":7,"order_only":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"relevant":"sorry, no valid rows found","base":"g188","repeat_5":"g188","repeat_2":"g188","repeat_1":"g188","repeat_4":"g188","order_only":"]==","irrelevant_adversarial":"48","repeat_3":"g188","irrelevant_plain":"]=="},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"base":1,"repeat_5":2,"repeat_2":3,"repeat_1":4,"repeat_4":5,"order_only":6,"irrelevant_adversarial":7,"repeat_3":8,"irrelevant_plain":9},"canonicalized_call_ids":["irrelevant_adversarial"]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_2":"]==","base":"]==","repeat_1":"]==","order_only":"]==","irrelevant_plain":"]==","repeat_5":"]==","irrelevant_adversarial":"50","relevant":":[16, 17, 25],","repeat_4":"]==","repeat_3":"]=="},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"base":1,"repeat_1":2,"order_only":3,"irrelevant_plain":4,"repeat_5":5,"irrelevant_adversarial":6,"relevant":7,"repeat_4":8,"repeat_3":9},"canonicalized_call_ids":["irrelevant_adversarial"]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_1":"23","repeat_3":"22","repeat_5":"22","irrelevant_plain":":@","relevant":"grouped_amount","repeat_4":"22","repeat_2":"22","base":"22","irrelevant_adversarial":"23","order_only":"time"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"repeat_3":1,"repeat_5":2,"irrelevant_plain":3,"relevant":4,"repeat_4":5,"repeat_2":6,"base":7,"irrelevant_adversarial":8,"order_only":9},"canonicalized_call_ids":["repeat_1","repeat_3","repeat_5","repeat_4","repeat_2","base","irrelevant_adversarial"]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_2":"g114","irrelevant_adversarial":"52","repeat_3":"52","irrelevant_plain":"]==","repeat_4":"g91","repeat_5":"52","base":"52","order_only":"114","repeat_1":"g114","relevant":"+"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"irrelevant_adversarial":1,"repeat_3":2,"irrelevant_plain":3,"repeat_4":4,"repeat_5":5,"base":6,"order_only":7,"repeat_1":8,"relevant":9},"canonicalized_call_ids":["irrelevant_adversarial","repeat_3","repeat_5","base","order_only"]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_3":"18","order_only":",__non_zero__:1} 注意：根据规则，customer_tier 为","relevant":"24","repeat_5":"10","repeat_1":",__non_zero__:1} 注意：根据规则，customer_tier 为","repeat_4":",__non_zero__:1} 注意：根据规则，customer_tier 为","repeat_2":",__non_zero__:1} 注意：根据规则，customer_tier 为","irrelevant_plain":",__int__}8__+__10__}8+10{","base":",__non_zero__:1} 注意：根据规则，customer_tier 为","irrelevant_adversarial":",__num__"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":["repeat_5"],"call_positions":{"repeat_3":0,"order_only":1,"relevant":2,"repeat_5":3,"repeat_1":4,"repeat_4":5,"repeat_2":6,"irrelevant_plain":7,"base":8,"irrelevant_adversarial":9},"canonicalized_call_ids":["repeat_3","relevant","repeat_5"]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_5":",__nonzero__}注：由于规则要求customer_tier为gold或platinum时routing_score等于severity加bonus，否则等于severity，且ticket中的customer_tier为","order_only":",__int__}8__0__+__1__2__=__2__0__}{","irrelevant_plain":",__int__}8__0__+__1__2__=__2__0__}{","base":",__nonzero__}注：由于规则要求customer_tier为gold或platinum时routing_score等于severity加bonus，否则等于severity，且ticket中的customer_tier为","repeat_3":",__int__}8__0__+__1__2__=__2__0__}{","irrelevant_adversarial":"10","repeat_1":",__int__}8__0__+__1__2__=__2__0__}{","repeat_4":",__int__}8__0__+__1__2__=__2__0__}{","relevant":"crypto_score","repeat_2":",__nonzero__}注：由于规则要求customer_tier为gold或platinum时routing_score等于severity加bonus，否则等于severity，且ticket中的customer_tier为"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"order_only":1,"irrelevant_plain":2,"base":3,"repeat_3":4,"irrelevant_adversarial":5,"repeat_1":6,"repeat_4":7,"relevant":8,"repeat_2":9},"canonicalized_call_ids":["irrelevant_adversarial"]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_5":",__int__}6__+__20__}6){","repeat_3":",__int__}6__+__20__}6){","irrelevant_adversarial":"log126","repeat_1":",__int__}6__+__20__}6){","relevant":",__num__","irrelevant_plain":",__int__}26__int__}","repeat_2":",__int__}6__+__20__}6){","base":",__int__}6__+__20__}6){","repeat_4":",__int__}6__+__20__}6){","order_only":",__int__}6__+__20__}6){"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_3":1,"irrelevant_adversarial":2,"repeat_1":3,"relevant":4,"irrelevant_plain":5,"repeat_2":6,"base":7,"repeat_4":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_2":"value","order_only":"value","repeat_5":"value","repeat_3":"value","irrelevant_plain":"value","relevant":"crypto","irrelevant_adversarial":"srouting_score","base":"value","repeat_4":"value","repeat_1":"value"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"order_only":1,"repeat_5":2,"repeat_3":3,"irrelevant_plain":4,"relevant":5,"irrelevant_adversarial":6,"base":7,"repeat_4":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"relevant":"+","repeat_2":"./2","base":"./2","repeat_3":"./2","irrelevant_plain":"./2","repeat_4":"./2","irrelevant_adversarial":"./2","order_only":"./2","repeat_1":"./2","repeat_5":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_2":1,"base":2,"repeat_3":3,"irrelevant_plain":4,"repeat_4":5,"irrelevant_adversarial":6,"order_only":7,"repeat_1":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_5":"./2","irrelevant_plain":"./2","repeat_1":"./2","base":"./2","repeat_3":"./2","irrelevant_adversarial":"./2","order_only":"@","relevant":"+","repeat_4":"./2","repeat_2":"./2"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"irrelevant_plain":1,"repeat_1":2,"base":3,"repeat_3":4,"irrelevant_adversarial":5,"order_only":6,"relevant":7,"repeat_4":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_3":"./2","repeat_1":"./2","repeat_4":"./2","irrelevant_adversarial":"./2","repeat_5":"./2","order_only":"./2","repeat_2":"./2","base":"./2","irrelevant_plain":"./2","relevant":"+"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_1":1,"repeat_4":2,"irrelevant_adversarial":3,"repeat_5":4,"order_only":5,"repeat_2":6,"base":7,"irrelevant_plain":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-789","experiment_seed":789,"answers":{"repeat_3":"./2","repeat_2":"./2","base":"./2","irrelevant_adversarial":"./2","order_only":"./2","irrelevant_plain":"+","repeat_4":"./2","repeat_5":"./2","repeat_1":"./2","relevant":"+"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_2":1,"base":2,"irrelevant_adversarial":3,"order_only":4,"irrelevant_plain":5,"repeat_4":6,"repeat_5":7,"repeat_1":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"repeat_1":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","base":"M00-A","repeat_4":"M00-A","repeat_5":"M00-A","repeat_3":"M00-A","irrelevant_adversarial":"M00-A","order_only":"M00-A","repeat_2":"M00-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"relevant":1,"irrelevant_plain":2,"base":3,"repeat_4":4,"repeat_5":5,"repeat_3":6,"irrelevant_adversarial":7,"order_only":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"repeat_5":"M01-A","base":"M01-A","repeat_2":"M01-A","relevant":"M01-B","irrelevant_adversarial":"M01-A","repeat_4":"M01-A","repeat_1":"M01-A","irrelevant_plain":"M01-A","repeat_3":"M01-A","order_only":"M01-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"base":1,"repeat_2":2,"relevant":3,"irrelevant_adversarial":4,"repeat_4":5,"repeat_1":6,"irrelevant_plain":7,"repeat_3":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"repeat_4":"M02-A","irrelevant_adversarial":"M02-A","relevant":"M02-B","base":"M02-A","irrelevant_plain":"M02-C","repeat_1":"M02-A","repeat_5":"M02-A","repeat_2":"M02-A","order_only":"M02-A","repeat_3":"M02-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"irrelevant_adversarial":1,"relevant":2,"base":3,"irrelevant_plain":4,"repeat_1":5,"repeat_5":6,"repeat_2":7,"order_only":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"irrelevant_adversarial":"M03-C","repeat_1":"M03-A","relevant":"M03-B","repeat_5":"M03-A","repeat_3":"M03-A","order_only":"M03-C","repeat_4":"M03-A","irrelevant_plain":"M03-C","base":"M03-A","repeat_2":"M03-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_1":1,"relevant":2,"repeat_5":3,"repeat_3":4,"order_only":5,"repeat_4":6,"irrelevant_plain":7,"base":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"relevant":"E00-B","repeat_3":"E00-C","repeat_2":"E00-C","order_only":"E00-C","base":"E00-C","irrelevant_adversarial":"E00-C","repeat_1":"E00-C","repeat_4":"E00-C","repeat_5":"E00-C","irrelevant_plain":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_3":1,"repeat_2":2,"order_only":3,"base":4,"irrelevant_adversarial":5,"repeat_1":6,"repeat_4":7,"repeat_5":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"repeat_4":"E01-C","repeat_3":"E01-C","irrelevant_adversarial":"E01-C","repeat_2":"E01-C","base":"E01-C","irrelevant_plain":"E01-B","repeat_1":"E01-C","repeat_5":"E01-C","order_only":"E01-C","relevant":"E01-B"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_3":1,"irrelevant_adversarial":2,"repeat_2":3,"base":4,"irrelevant_plain":5,"repeat_1":6,"repeat_5":7,"order_only":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"repeat_1":"E02-C","order_only":"E02-A","repeat_5":"E02-C","base":"E02-C","repeat_2":"E02-C","repeat_3":"E02-C","relevant":"E02-B","repeat_4":"E02-C","irrelevant_adversarial":"E02-C","irrelevant_plain":"E02-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"order_only":1,"repeat_5":2,"base":3,"repeat_2":4,"repeat_3":5,"relevant":6,"repeat_4":7,"irrelevant_adversarial":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"relevant":"E03-B","repeat_5":"E03-C","repeat_3":"E03-C","repeat_4":"E03-C","irrelevant_adversarial":"E03-A","order_only":"E03-C","repeat_2":"E03-C","repeat_1":"E03-C","irrelevant_plain":"E03-C","base":"E03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_5":1,"repeat_3":2,"repeat_4":3,"irrelevant_adversarial":4,"order_only":5,"repeat_2":6,"repeat_1":7,"irrelevant_plain":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"relevant":"188","irrelevant_adversarial":"50","irrelevant_plain":"188","repeat_2":"188","repeat_3":"188","repeat_5":"188","base":"188","repeat_1":"188","repeat_4":"188","order_only":"50"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"irrelevant_adversarial":1,"irrelevant_plain":2,"repeat_2":3,"repeat_3":4,"repeat_5":5,"base":6,"repeat_1":7,"repeat_4":8,"order_only":9},"canonicalized_call_ids":["irrelevant_adversarial","order_only"]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"irrelevant_plain":"188","repeat_3":"188","repeat_2":"188","base":"188","repeat_4":"188","repeat_1":"188","relevant":"188","repeat_5":"188","irrelevant_adversarial":"137","order_only":"188"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_3":1,"repeat_2":2,"base":3,"repeat_4":4,"repeat_1":5,"relevant":6,"repeat_5":7,"irrelevant_adversarial":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"irrelevant_adversarial":"1023","repeat_1":"101","base":"101","irrelevant_plain":"101","repeat_4":"101","relevant":"101","repeat_3":"101","order_only":"答案","repeat_2":"101","repeat_5":"101"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_1":1,"base":2,"irrelevant_plain":3,"repeat_4":4,"relevant":5,"repeat_3":6,"order_only":7,"repeat_2":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"repeat_1":"52","irrelevant_adversarial":"52","repeat_2":"52","repeat_4":"52","irrelevant_plain":"52","repeat_5":"52","repeat_3":"52","relevant":"61","base":"52","order_only":"52"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"irrelevant_adversarial":1,"repeat_2":2,"repeat_4":3,"irrelevant_plain":4,"repeat_5":5,"repeat_3":6,"relevant":7,"base":8,"order_only":9},"canonicalized_call_ids":["repeat_1","irrelevant_adversarial","repeat_2","repeat_4","irrelevant_plain","repeat_5","repeat_3","relevant","base","order_only"]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"repeat_2":"答案","base":"答案","irrelevant_plain":"答案","repeat_1":"18","repeat_5":"18","irrelevant_adversarial":"117","repeat_4":"18","repeat_3":"18","order_only":"18","relevant":"14"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"base":1,"irrelevant_plain":2,"repeat_1":3,"repeat_5":4,"irrelevant_adversarial":5,"repeat_4":6,"repeat_3":7,"order_only":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"repeat_3":"答案","relevant":"11","base":"答案","repeat_1":"答案","irrelevant_adversarial":"119","repeat_4":"答案","order_only":"答案","irrelevant_plain":"答案","repeat_2":"答案","repeat_5":"答案"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"relevant":1,"base":2,"repeat_1":3,"irrelevant_adversarial":4,"repeat_4":5,"order_only":6,"irrelevant_plain":7,"repeat_2":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"repeat_3":"6","repeat_4":"6","irrelevant_adversarial":"12","repeat_2":"6","irrelevant_plain":"6","repeat_5":"6","relevant":"13","order_only":"6","repeat_1":"6","base":"6"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_4":1,"irrelevant_adversarial":2,"repeat_2":3,"irrelevant_plain":4,"repeat_5":5,"relevant":6,"order_only":7,"repeat_1":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"repeat_2":"8","order_only":"8","base":"8","repeat_3":"8","repeat_4":"8","irrelevant_plain":"8","irrelevant_adversarial":"16","repeat_1":"8","relevant":"14","repeat_5":"8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"order_only":1,"base":2,"repeat_3":3,"repeat_4":4,"irrelevant_plain":5,"irrelevant_adversarial":6,"repeat_1":7,"relevant":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"base":"2","relevant":"2","repeat_1":"2","irrelevant_adversarial":"2","repeat_2":"2","irrelevant_plain":"2","repeat_3":"2","order_only":"2","repeat_5":"2","repeat_4":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"relevant":1,"repeat_1":2,"irrelevant_adversarial":3,"repeat_2":4,"irrelevant_plain":5,"repeat_3":6,"order_only":7,"repeat_5":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"base":"2","order_only":"2","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat_2":"2","repeat_4":"2","relevant":"2","repeat_5":"2","repeat_3":"2","repeat_1":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"order_only":1,"irrelevant_plain":2,"irrelevant_adversarial":3,"repeat_2":4,"repeat_4":5,"relevant":6,"repeat_5":7,"repeat_3":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"repeat_4":"2","relevant":"2","irrelevant_plain":"2","repeat_3":"2","repeat_1":"2","base":"2","irrelevant_adversarial":"2","repeat_5":"2","order_only":"2","repeat_2":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"relevant":1,"irrelevant_plain":2,"repeat_3":3,"repeat_1":4,"base":5,"irrelevant_adversarial":6,"repeat_5":7,"order_only":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-123","experiment_seed":123,"answers":{"irrelevant_plain":"2","repeat_5":"2","base":"2","repeat_2":"2","relevant":"2","repeat_3":"2","repeat_4":"2","order_only":"2","irrelevant_adversarial":"2","repeat_1":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_5":1,"base":2,"repeat_2":3,"relevant":4,"repeat_3":5,"repeat_4":6,"order_only":7,"irrelevant_adversarial":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"repeat_4":"M00-A","repeat_2":"M00-A","relevant":"M00-B","repeat_3":"M00-A","order_only":"M00-A","irrelevant_plain":"M00-A","base":"M00-A","irrelevant_adversarial":"M00-A","repeat_1":"M00-A","repeat_5":"M00-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_2":1,"relevant":2,"repeat_3":3,"order_only":4,"irrelevant_plain":5,"base":6,"irrelevant_adversarial":7,"repeat_1":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"relevant":"M01-B","base":"M01-A","repeat_3":"M01-A","repeat_5":"M01-A","irrelevant_adversarial":"M01-A","repeat_4":"M01-A","irrelevant_plain":"M01-A","order_only":"M01-A","repeat_1":"M01-A","repeat_2":"M01-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"base":1,"repeat_3":2,"repeat_5":3,"irrelevant_adversarial":4,"repeat_4":5,"irrelevant_plain":6,"order_only":7,"repeat_1":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"M02-C","repeat_3":"M02-A","repeat_2":"M02-A","irrelevant_adversarial":"M02-A","repeat_1":"M02-A","order_only":"M02-A","base":"M02-A","relevant":"M02-B","repeat_4":"M02-A","repeat_5":"M02-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_3":1,"repeat_2":2,"irrelevant_adversarial":3,"repeat_1":4,"order_only":5,"base":6,"relevant":7,"repeat_4":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"M03-C","repeat_3":"M03-A","repeat_5":"M03-A","relevant":"M03-B","base":"M03-A","irrelevant_adversarial":"M03-C","repeat_1":"M03-A","repeat_4":"M03-A","repeat_2":"M03-A","order_only":"M03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_3":1,"repeat_5":2,"relevant":3,"base":4,"irrelevant_adversarial":5,"repeat_1":6,"repeat_4":7,"repeat_2":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"base":"E00-C","repeat_1":"E00-C","repeat_4":"E00-C","relevant":"E00-B","repeat_2":"E00-C","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C","repeat_5":"E00-C","repeat_3":"E00-C","order_only":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"repeat_1":1,"repeat_4":2,"relevant":3,"repeat_2":4,"irrelevant_plain":5,"irrelevant_adversarial":6,"repeat_5":7,"repeat_3":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"repeat_5":"E01-C","irrelevant_plain":"E01-C","base":"E01-C","repeat_2":"E01-C","irrelevant_adversarial":"E01-C","repeat_1":"E01-C","order_only":"E01-C","repeat_4":"E01-C","repeat_3":"E01-C","relevant":"E01-B"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"irrelevant_plain":1,"base":2,"repeat_2":3,"irrelevant_adversarial":4,"repeat_1":5,"order_only":6,"repeat_4":7,"repeat_3":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"repeat_4":"E02-C","base":"E02-C","repeat_5":"E02-C","repeat_3":"E02-C","order_only":"E02-A","relevant":"E02-B","irrelevant_adversarial":"E02-C","repeat_1":"E02-C","irrelevant_plain":"E02-C","repeat_2":"E02-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"base":1,"repeat_5":2,"repeat_3":3,"order_only":4,"relevant":5,"irrelevant_adversarial":6,"repeat_1":7,"irrelevant_plain":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"repeat_2":"E03-C","repeat_5":"E03-C","repeat_4":"E03-C","irrelevant_plain":"E03-C","relevant":"E03-B","base":"E03-C","repeat_3":"E03-C","repeat_1":"E03-C","irrelevant_adversarial":"E03-A","order_only":"E03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_5":1,"repeat_4":2,"irrelevant_plain":3,"relevant":4,"base":5,"repeat_3":6,"repeat_1":7,"irrelevant_adversarial":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"base":"188","repeat_2":"188","order_only":"50","repeat_5":"188","repeat_3":"188","repeat_1":"188","repeat_4":"188","irrelevant_adversarial":"1050","irrelevant_plain":"188","relevant":"188"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"repeat_2":1,"order_only":2,"repeat_5":3,"repeat_3":4,"repeat_1":5,"repeat_4":6,"irrelevant_adversarial":7,"irrelevant_plain":8,"relevant":9},"canonicalized_call_ids":["order_only"]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"repeat_4":"188","base":"188","repeat_2":"188","repeat_1":"188","relevant":"188","irrelevant_adversarial":"137","irrelevant_plain":"188","repeat_3":"188","order_only":"188","repeat_5":"188"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"base":1,"repeat_2":2,"repeat_1":3,"relevant":4,"irrelevant_adversarial":5,"irrelevant_plain":6,"repeat_3":7,"order_only":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"repeat_2":"101","irrelevant_adversarial":"1023","irrelevant_plain":"101","base":"101","repeat_3":"101","repeat_4":"101","relevant":"101","repeat_5":"101","order_only":"101","repeat_1":"101"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"irrelevant_adversarial":1,"irrelevant_plain":2,"base":3,"repeat_3":4,"repeat_4":5,"relevant":6,"repeat_5":7,"order_only":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"repeat_4":"52","repeat_5":"52","repeat_3":"52","irrelevant_adversarial":"52","order_only":"52","irrelevant_plain":"52","repeat_1":"52","repeat_2":"52","relevant":"61","base":"52"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_5":1,"repeat_3":2,"irrelevant_adversarial":3,"order_only":4,"irrelevant_plain":5,"repeat_1":6,"repeat_2":7,"relevant":8,"base":9},"canonicalized_call_ids":["repeat_4","repeat_5","repeat_3","irrelevant_adversarial","order_only","irrelevant_plain","repeat_1","repeat_2","relevant","base"]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"order_only":"答案","repeat_2":"18","repeat_5":"18","irrelevant_plain":"18","repeat_4":"答案","repeat_3":"18","repeat_1":"18","relevant":"14","base":"答案","irrelevant_adversarial":"18"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_2":1,"repeat_5":2,"irrelevant_plain":3,"repeat_4":4,"repeat_3":5,"repeat_1":6,"relevant":7,"base":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"repeat_2":"答案","repeat_3":"答案","repeat_5":"答案","irrelevant_plain":"答案","repeat_1":"答案","irrelevant_adversarial":"119","base":"答案","relevant":"11","order_only":"答案","repeat_4":"答案"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_3":1,"repeat_5":2,"irrelevant_plain":3,"repeat_1":4,"irrelevant_adversarial":5,"base":6,"relevant":7,"order_only":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"base":"6","order_only":"6","relevant":"13","repeat_5":"6","repeat_4":"6","irrelevant_adversarial":"12","repeat_1":"6","repeat_2":"6","repeat_3":"6","irrelevant_plain":"6"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"order_only":1,"relevant":2,"repeat_5":3,"repeat_4":4,"irrelevant_adversarial":5,"repeat_1":6,"repeat_2":7,"repeat_3":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"order_only":"8","base":"8","repeat_1":"8","repeat_3":"8","repeat_2":"8","repeat_5":"8","relevant":"14","irrelevant_adversarial":"16","irrelevant_plain":"8","repeat_4":"8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"base":1,"repeat_1":2,"repeat_3":3,"repeat_2":4,"repeat_5":5,"relevant":6,"irrelevant_adversarial":7,"irrelevant_plain":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"repeat_1":"2","relevant":"2","irrelevant_plain":"2","repeat_4":"2","order_only":"2","base":"2","repeat_2":"2","irrelevant_adversarial":"2","repeat_5":"2","repeat_3":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"relevant":1,"irrelevant_plain":2,"repeat_4":3,"order_only":4,"base":5,"repeat_2":6,"irrelevant_adversarial":7,"repeat_5":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"2","repeat_1":"2","base":"2","order_only":"2","irrelevant_adversarial":"2","repeat_4":"2","relevant":"2","repeat_2":"2","repeat_3":"2","repeat_5":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_1":1,"base":2,"order_only":3,"irrelevant_adversarial":4,"repeat_4":5,"relevant":6,"repeat_2":7,"repeat_3":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"repeat_4":"2","repeat_3":"2","repeat_5":"2","repeat_1":"2","base":"2","order_only":"2","irrelevant_plain":"2","relevant":"2","repeat_2":"2","irrelevant_adversarial":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_3":1,"repeat_5":2,"repeat_1":3,"base":4,"order_only":5,"irrelevant_plain":6,"relevant":7,"repeat_2":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"2","repeat_1":"2","repeat_5":"2","order_only":"2","irrelevant_plain":"2","repeat_2":"2","repeat_4":"2","relevant":"2","base":"2","repeat_3":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_1":1,"repeat_5":2,"order_only":3,"irrelevant_plain":4,"repeat_2":5,"repeat_4":6,"relevant":7,"base":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"M00-A","order_only":"M00-A","repeat_1":"M00-A","repeat_4":"M00-A","repeat_3":"M00-A","repeat_5":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","repeat_2":"M00-A","base":"M00-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"order_only":1,"repeat_1":2,"repeat_4":3,"repeat_3":4,"repeat_5":5,"relevant":6,"irrelevant_plain":7,"repeat_2":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"repeat_4":"M01-A","repeat_5":"M01-A","base":"M01-A","order_only":"M01-A","repeat_3":"M01-A","irrelevant_plain":"M01-A","relevant":"M01-B","repeat_1":"M01-A","repeat_2":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_5":1,"base":2,"order_only":3,"repeat_3":4,"irrelevant_plain":5,"relevant":6,"repeat_1":7,"repeat_2":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"M02-A","repeat_2":"M02-A","repeat_3":"M02-A","repeat_4":"M02-A","base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-C","order_only":"M02-A","repeat_1":"M02-A","repeat_5":"M02-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_2":1,"repeat_3":2,"repeat_4":3,"base":4,"relevant":5,"irrelevant_plain":6,"order_only":7,"repeat_1":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"repeat_1":"M03-A","repeat_2":"M03-A","base":"M03-A","repeat_3":"M03-A","irrelevant_plain":"M03-C","irrelevant_adversarial":"M03-C","order_only":"M03-C","repeat_4":"M03-A","relevant":"M03-B","repeat_5":"M03-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"repeat_2":1,"base":2,"repeat_3":3,"irrelevant_plain":4,"irrelevant_adversarial":5,"order_only":6,"repeat_4":7,"relevant":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"E00-C","base":"E00-C","repeat_1":"E00-C","repeat_3":"E00-C","irrelevant_plain":"E00-C","repeat_2":"E00-C","repeat_4":"E00-C","repeat_5":"E00-C","relevant":"E00-B","order_only":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"base":1,"repeat_1":2,"repeat_3":3,"irrelevant_plain":4,"repeat_2":5,"repeat_4":6,"repeat_5":7,"relevant":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"E01-C","repeat_3":"E01-C","order_only":"E01-C","repeat_5":"E01-C","irrelevant_plain":"E01-C","base":"E01-C","repeat_4":"E01-C","repeat_2":"E01-C","repeat_1":"E01-C","relevant":"E01-B"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_3":1,"order_only":2,"repeat_5":3,"irrelevant_plain":4,"base":5,"repeat_4":6,"repeat_2":7,"repeat_1":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"order_only":"E02-A","base":"E02-C","repeat_3":"E02-C","repeat_4":"E02-C","repeat_2":"E02-C","irrelevant_adversarial":"E02-C","relevant":"E02-B","repeat_5":"E02-C","irrelevant_plain":"E02-C","repeat_1":"E02-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"order_only":0,"base":1,"repeat_3":2,"repeat_4":3,"repeat_2":4,"irrelevant_adversarial":5,"relevant":6,"repeat_5":7,"irrelevant_plain":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"base":"E03-C","irrelevant_adversarial":"E03-A","repeat_5":"E03-C","relevant":"E03-B","order_only":"E03-C","repeat_3":"E03-C","repeat_4":"E03-C","repeat_1":"E03-C","repeat_2":"E03-C","irrelevant_plain":"E03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"irrelevant_adversarial":1,"repeat_5":2,"relevant":3,"order_only":4,"repeat_3":5,"repeat_4":6,"repeat_1":7,"repeat_2":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"base":"188","repeat_2":"188","relevant":"188","irrelevant_plain":"188","repeat_5":"188","irrelevant_adversarial":"1050","order_only":"50","repeat_3":"188","repeat_4":"188","repeat_1":"188"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"repeat_2":1,"relevant":2,"irrelevant_plain":3,"repeat_5":4,"irrelevant_adversarial":5,"order_only":6,"repeat_3":7,"repeat_4":8,"repeat_1":9},"canonicalized_call_ids":["order_only"]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"137","repeat_2":"188","repeat_5":"188","repeat_3":"188","relevant":"188","irrelevant_plain":"188","repeat_4":"188","base":"188","order_only":"188","repeat_1":"188"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_2":1,"repeat_5":2,"repeat_3":3,"relevant":4,"irrelevant_plain":5,"repeat_4":6,"base":7,"order_only":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"repeat_5":"101","irrelevant_plain":"101","order_only":"101","repeat_4":"101","relevant":"101","irrelevant_adversarial":"1023","base":"101","repeat_3":"101","repeat_2":"101","repeat_1":"101"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"irrelevant_plain":1,"order_only":2,"repeat_4":3,"relevant":4,"irrelevant_adversarial":5,"base":6,"repeat_3":7,"repeat_2":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"52","repeat_2":"52","repeat_4":"52","base":"52","relevant":"61","repeat_3":"52","repeat_5":"52","irrelevant_plain":"52","order_only":"52","repeat_1":"52"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_2":1,"repeat_4":2,"base":3,"relevant":4,"repeat_3":5,"repeat_5":6,"irrelevant_plain":7,"order_only":8,"repeat_1":9},"canonicalized_call_ids":["irrelevant_adversarial","repeat_2","repeat_4","base","relevant","repeat_3","repeat_5","irrelevant_plain","order_only","repeat_1"]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"repeat_2":"答案","repeat_4":"18","repeat_3":"18","base":"18","order_only":"18","repeat_1":"18","relevant":"14","irrelevant_plain":"18","repeat_5":"答案","irrelevant_adversarial":"18"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_4":1,"repeat_3":2,"base":3,"order_only":4,"repeat_1":5,"relevant":6,"irrelevant_plain":7,"repeat_5":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"repeat_1":"答案","repeat_3":"答案","order_only":"答案","irrelevant_plain":"答案","irrelevant_adversarial":"119","repeat_2":"答案","base":"答案","repeat_5":"答案","relevant":"11","repeat_4":"答案"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"repeat_3":1,"order_only":2,"irrelevant_plain":3,"irrelevant_adversarial":4,"repeat_2":5,"base":6,"repeat_5":7,"relevant":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"order_only":"6","repeat_1":"6","repeat_4":"6","repeat_5":"6","relevant":"13","irrelevant_plain":"6","base":"6","repeat_3":"6","repeat_2":"6","irrelevant_adversarial":"12"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_1":1,"repeat_4":2,"repeat_5":3,"relevant":4,"irrelevant_plain":5,"base":6,"repeat_3":7,"repeat_2":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"repeat_4":"8","repeat_1":"8","base":"8","relevant":"14","repeat_5":"8","irrelevant_plain":"8","repeat_2":"8","repeat_3":"8","irrelevant_adversarial":"16","order_only":"8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_1":1,"base":2,"relevant":3,"repeat_5":4,"irrelevant_plain":5,"repeat_2":6,"repeat_3":7,"irrelevant_adversarial":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"repeat_1":"2","repeat_4":"2","order_only":"2","repeat_2":"2","base":"2","relevant":"2","irrelevant_adversarial":"2","irrelevant_plain":"2","repeat_3":"2","repeat_5":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"repeat_4":1,"order_only":2,"repeat_2":3,"base":4,"relevant":5,"irrelevant_adversarial":6,"irrelevant_plain":7,"repeat_3":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"repeat_5":"2","repeat_2":"2","repeat_1":"2","base":"2","relevant":"2","order_only":"2","irrelevant_plain":"2","repeat_4":"2","irrelevant_adversarial":"2","repeat_3":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_2":1,"repeat_1":2,"base":3,"relevant":4,"order_only":5,"irrelevant_plain":6,"repeat_4":7,"irrelevant_adversarial":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"order_only":"2","repeat_1":"2","base":"2","irrelevant_plain":"2","repeat_3":"2","repeat_2":"2","irrelevant_adversarial":"2","relevant":"2","repeat_4":"2","repeat_5":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_1":1,"base":2,"irrelevant_plain":3,"repeat_3":4,"repeat_2":5,"irrelevant_adversarial":6,"relevant":7,"repeat_4":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-789","experiment_seed":789,"answers":{"repeat_5":"2","irrelevant_plain":"2","repeat_3":"2","repeat_1":"2","base":"2","repeat_2":"2","irrelevant_adversarial":"2","relevant":"2","repeat_4":"2","order_only":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"irrelevant_plain":1,"repeat_3":2,"repeat_1":3,"base":4,"repeat_2":5,"irrelevant_adversarial":6,"relevant":7,"repeat_4":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"repeat_5":"M00-A","repeat_3":"M00-A","repeat_1":"M00-A","repeat_2":"M00-A","relevant":"M00-B","irrelevant_adversarial":"M00-A","irrelevant_plain":"M00-A","order_only":"M00-A","repeat_4":"M00-A","base":"M00-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_3":1,"repeat_1":2,"repeat_2":3,"relevant":4,"irrelevant_adversarial":5,"irrelevant_plain":6,"order_only":7,"repeat_4":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"repeat_1":"M01-A","irrelevant_adversarial":"M01-A","relevant":"M01-B","repeat_4":"M01-A","base":"M01-A","repeat_2":"M01-A","order_only":"M01-A","repeat_3":"M01-A","irrelevant_plain":"M01-A","repeat_5":"M01-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"irrelevant_adversarial":1,"relevant":2,"repeat_4":3,"base":4,"repeat_2":5,"order_only":6,"repeat_3":7,"irrelevant_plain":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"order_only":"M02-B","repeat_1":"M02-A","irrelevant_plain":"M02-C","repeat_2":"M02-C","base":"M02-C","repeat_3":"M02-C","repeat_5":"M02-C","repeat_4":"M02-C","irrelevant_adversarial":"M02-A","relevant":"M02-B"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_1":1,"irrelevant_plain":2,"repeat_2":3,"base":4,"repeat_3":5,"repeat_5":6,"repeat_4":7,"irrelevant_adversarial":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"repeat_2":"M03-A","irrelevant_plain":"M03-C","order_only":"M03-C","repeat_4":"M03-A","irrelevant_adversarial":"M03-C","repeat_5":"M03-A","relevant":"M03-B","repeat_1":"M03-A","repeat_3":"M03-A","base":"M03-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"irrelevant_plain":1,"order_only":2,"repeat_4":3,"irrelevant_adversarial":4,"repeat_5":5,"relevant":6,"repeat_1":7,"repeat_3":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"irrelevant_adversarial":"E00-C","base":"E00-C","repeat_3":"E00-C","repeat_5":"E00-C","repeat_1":"E00-C","repeat_2":"E00-C","order_only":"E00-C","repeat_4":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"base":1,"repeat_3":2,"repeat_5":3,"repeat_1":4,"repeat_2":5,"order_only":6,"repeat_4":7,"relevant":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"order_only":"E01-C","repeat_5":"E01-C","relevant":"E01-B","repeat_4":"E01-C","base":"E01-C","repeat_1":"E01-C","irrelevant_adversarial":"E01-C","repeat_3":"E01-C","irrelevant_plain":"E01-C","repeat_2":"E01-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_5":1,"relevant":2,"repeat_4":3,"base":4,"repeat_1":5,"irrelevant_adversarial":6,"repeat_3":7,"irrelevant_plain":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"repeat_4":"E02-C","repeat_5":"E02-C","irrelevant_adversarial":"E02-C","repeat_1":"E02-C","irrelevant_plain":"E02-C","relevant":"E02-B","repeat_3":"E02-C","base":"E02-C","repeat_2":"E02-C","order_only":"E02-D"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_5":1,"irrelevant_adversarial":2,"repeat_1":3,"irrelevant_plain":4,"relevant":5,"repeat_3":6,"base":7,"repeat_2":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"irrelevant_adversarial":"E03-A","repeat_2":"E03-C","repeat_5":"E03-C","base":"E03-C","order_only":"E03-C","irrelevant_plain":"E03-C","repeat_3":"E03-C","repeat_1":"E03-C","repeat_4":"E03-C","relevant":"E03-B"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_2":1,"repeat_5":2,"base":3,"order_only":4,"irrelevant_plain":5,"repeat_3":6,"repeat_1":7,"repeat_4":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"irrelevant_plain":"18","repeat_3":"18","base":"18","repeat_5":"18","repeat_2":"18","repeat_4":"18","relevant":"188","order_only":"50","irrelevant_adversarial":"50","repeat_1":"18"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_3":1,"base":2,"repeat_5":3,"repeat_2":4,"repeat_4":5,"relevant":6,"order_only":7,"irrelevant_adversarial":8,"repeat_1":9},"canonicalized_call_ids":["order_only","irrelevant_adversarial"]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"relevant":"188","repeat_3":"18","base":"18","irrelevant_adversarial":"51","irrelevant_plain":"18","repeat_1":"18","order_only":"188","repeat_2":"18","repeat_5":"18","repeat_4":"18"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_3":1,"base":2,"irrelevant_adversarial":3,"irrelevant_plain":4,"repeat_1":5,"order_only":6,"repeat_2":7,"repeat_5":8,"repeat_4":9},"canonicalized_call_ids":["irrelevant_adversarial"]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"relevant":"101","order_only":"101","base":"101","repeat_2":"101","irrelevant_plain":"101","repeat_1":"101","repeat_5":"101","repeat_3":"101","irrelevant_adversarial":"1023","repeat_4":"101"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"order_only":1,"base":2,"repeat_2":3,"irrelevant_plain":4,"repeat_1":5,"repeat_5":6,"repeat_3":7,"irrelevant_adversarial":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"repeat_1":"52","relevant":"61","irrelevant_plain":"114","repeat_2":"52","irrelevant_adversarial":"52","repeat_5":"52","base":"52","repeat_4":"52","repeat_3":"52","order_only":"114"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"relevant":1,"irrelevant_plain":2,"repeat_2":3,"irrelevant_adversarial":4,"repeat_5":5,"base":6,"repeat_4":7,"repeat_3":8,"order_only":9},"canonicalized_call_ids":["repeat_1","relevant","repeat_2","irrelevant_adversarial","repeat_5","base","repeat_4","repeat_3"]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"repeat_4":"8","repeat_1":"8","relevant":"14","irrelevant_plain":"8","repeat_2":"8","base":"8","repeat_5":"8","repeat_3":"8","order_only":"8","irrelevant_adversarial":"18"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_1":1,"relevant":2,"irrelevant_plain":3,"repeat_2":4,"base":5,"repeat_5":6,"repeat_3":7,"order_only":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"relevant":"11","repeat_5":"8","repeat_1":"8","base":"8","irrelevant_plain":"8","order_only":"8","irrelevant_adversarial":"119","repeat_4":"8","repeat_2":"8","repeat_3":"8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_5":1,"repeat_1":2,"base":3,"irrelevant_plain":4,"order_only":5,"irrelevant_adversarial":6,"repeat_4":7,"repeat_2":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"repeat_3":"6","relevant":"13","repeat_1":"6","irrelevant_adversarial":"12","repeat_4":"6","irrelevant_plain":"6","repeat_5":"6","order_only":"6","repeat_2":"6","base":"6"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"relevant":1,"repeat_1":2,"irrelevant_adversarial":3,"repeat_4":4,"irrelevant_plain":5,"repeat_5":6,"order_only":7,"repeat_2":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"relevant":"14","irrelevant_adversarial":"16","repeat_5":"8","repeat_4":"8","repeat_3":"8","irrelevant_plain":"8","repeat_1":"8","order_only":"8","base":"8","repeat_2":"8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"irrelevant_adversarial":1,"repeat_5":2,"repeat_4":3,"repeat_3":4,"irrelevant_plain":5,"repeat_1":6,"order_only":7,"base":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"repeat_1":"2","irrelevant_plain":"2","base":"2","irrelevant_adversarial":"2","relevant":"3","repeat_4":"2","repeat_2":"2","repeat_5":"2","order_only":"2","repeat_3":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"irrelevant_plain":1,"base":2,"irrelevant_adversarial":3,"relevant":4,"repeat_4":5,"repeat_2":6,"repeat_5":7,"order_only":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"repeat_3":"2","relevant":"2","repeat_5":"2","repeat_4":"2","order_only":"2","base":"2","repeat_1":"2","repeat_2":"2","irrelevant_adversarial":"2","irrelevant_plain":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"relevant":1,"repeat_5":2,"repeat_4":3,"order_only":4,"base":5,"repeat_1":6,"repeat_2":7,"irrelevant_adversarial":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"repeat_2":"2","order_only":"2","repeat_1":"2","relevant":"2","irrelevant_adversarial":"2","base":"2","repeat_5":"2","repeat_4":"2","repeat_3":"2","irrelevant_plain":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"order_only":1,"repeat_1":2,"relevant":3,"irrelevant_adversarial":4,"base":5,"repeat_5":6,"repeat_4":7,"repeat_3":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-123","experiment_seed":123,"answers":{"repeat_5":"2","repeat_1":"2","repeat_2":"2","order_only":"2","repeat_4":"2","relevant":"2","irrelevant_adversarial":"2","base":"2","irrelevant_plain":"2","repeat_3":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_1":1,"repeat_2":2,"order_only":3,"repeat_4":4,"relevant":5,"irrelevant_adversarial":6,"base":7,"irrelevant_plain":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"repeat_2":"M00-A","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A","repeat_3":"M00-A","repeat_1":"M00-A","repeat_5":"M00-A","repeat_4":"M00-A","base":"M00-A","order_only":"M00-A","relevant":"M00-B"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"irrelevant_plain":1,"irrelevant_adversarial":2,"repeat_3":3,"repeat_1":4,"repeat_5":5,"repeat_4":6,"base":7,"order_only":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"M01-A","repeat_4":"M01-A","base":"M01-A","repeat_1":"M01-A","irrelevant_adversarial":"M01-A","order_only":"M01-A","repeat_2":"M01-A","repeat_5":"M01-A","repeat_3":"M01-A","relevant":"M01-B"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_4":1,"base":2,"repeat_1":3,"irrelevant_adversarial":4,"order_only":5,"repeat_2":6,"repeat_5":7,"repeat_3":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"repeat_3":"M02-C","irrelevant_adversarial":"M02-A","repeat_1":"M02-C","base":"M02-C","repeat_4":"M02-C","order_only":"M02-B","repeat_2":"M02-C","relevant":"M02-B","repeat_5":"M02-C","irrelevant_plain":"M02-C"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"irrelevant_adversarial":1,"repeat_1":2,"base":3,"repeat_4":4,"order_only":5,"repeat_2":6,"relevant":7,"repeat_5":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"M03-C","repeat_4":"M03-A","repeat_5":"M03-A","irrelevant_plain":"M03-C","repeat_2":"M03-A","order_only":"M03-C","base":"M03-A","repeat_3":"M03-A","relevant":"M03-C","repeat_1":"M03-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_4":1,"repeat_5":2,"irrelevant_plain":3,"repeat_2":4,"order_only":5,"base":6,"repeat_3":7,"relevant":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"repeat_4":"E00-C","irrelevant_adversarial":"E00-C","repeat_3":"E00-C","repeat_5":"E00-C","repeat_1":"E00-C","irrelevant_plain":"E00-C","base":"E00-C","repeat_2":"E00-C","order_only":"E00-C","relevant":"E00-B"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"irrelevant_adversarial":1,"repeat_3":2,"repeat_5":3,"repeat_1":4,"irrelevant_plain":5,"base":6,"repeat_2":7,"order_only":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"E01-C","repeat_1":"E01-C","repeat_4":"E01-C","repeat_2":"E01-C","repeat_3":"E01-C","base":"E01-C","irrelevant_plain":"E01-C","order_only":"E01-C","repeat_5":"E01-C","relevant":"E01-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_1":1,"repeat_4":2,"repeat_2":3,"repeat_3":4,"base":5,"irrelevant_plain":6,"order_only":7,"repeat_5":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"repeat_4":"E02-C","order_only":"E02-D","repeat_2":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","repeat_1":"E02-C","irrelevant_adversarial":"E02-C","base":"E02-C","repeat_5":"E02-C","repeat_3":"E02-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"order_only":1,"repeat_2":2,"relevant":3,"irrelevant_plain":4,"repeat_1":5,"irrelevant_adversarial":6,"base":7,"repeat_5":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"repeat_1":"E03-C","order_only":"E03-C","irrelevant_plain":"E03-C","base":"E03-C","repeat_4":"E03-C","repeat_2":"E03-C","repeat_5":"E03-C","irrelevant_adversarial":"E03-A","relevant":"E03-B","repeat_3":"E03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"order_only":1,"irrelevant_plain":2,"base":3,"repeat_4":4,"repeat_2":5,"repeat_5":6,"irrelevant_adversarial":7,"relevant":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"18","repeat_2":"18","irrelevant_adversarial":"50","repeat_4":"18","repeat_5":"18","base":"18","repeat_3":"18","repeat_1":"18","relevant":"188","order_only":"50"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_2":1,"irrelevant_adversarial":2,"repeat_4":3,"repeat_5":4,"base":5,"repeat_3":6,"repeat_1":7,"relevant":8,"order_only":9},"canonicalized_call_ids":["irrelevant_adversarial","order_only"]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"repeat_2":"18","repeat_5":"18","repeat_1":"18","order_only":"188","repeat_3":"18","repeat_4":"18","irrelevant_plain":"18","relevant":"188","irrelevant_adversarial":"51","base":"18"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_5":1,"repeat_1":2,"order_only":3,"repeat_3":4,"repeat_4":5,"irrelevant_plain":6,"relevant":7,"irrelevant_adversarial":8,"base":9},"canonicalized_call_ids":["irrelevant_adversarial"]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"repeat_2":"101","repeat_5":"101","repeat_3":"101","irrelevant_plain":"101","base":"101","relevant":"101","repeat_4":"101","irrelevant_adversarial":"1023","order_only":"101","repeat_1":"101"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_5":1,"repeat_3":2,"irrelevant_plain":3,"base":4,"relevant":5,"repeat_4":6,"irrelevant_adversarial":7,"order_only":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"base":"52","repeat_2":"52","irrelevant_plain":"114","irrelevant_adversarial":"52","order_only":"114","repeat_4":"52","repeat_3":"52","repeat_1":"52","repeat_5":"52","relevant":"61"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"repeat_2":1,"irrelevant_plain":2,"irrelevant_adversarial":3,"order_only":4,"repeat_4":5,"repeat_3":6,"repeat_1":7,"repeat_5":8,"relevant":9},"canonicalized_call_ids":["base","repeat_2","irrelevant_adversarial","repeat_4","repeat_3","repeat_1","repeat_5","relevant"]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"8","repeat_3":"8","repeat_4":"8","relevant":"14","order_only":"8","repeat_2":"8","repeat_1":"8","repeat_5":"8","irrelevant_adversarial":"18","base":"8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_3":1,"repeat_4":2,"relevant":3,"order_only":4,"repeat_2":5,"repeat_1":6,"repeat_5":7,"irrelevant_adversarial":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"relevant":"11","repeat_5":"8","irrelevant_adversarial":"119","repeat_4":"8","base":"8","order_only":"8","irrelevant_plain":"8","repeat_2":"8","repeat_1":"8","repeat_3":"8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_5":1,"irrelevant_adversarial":2,"repeat_4":3,"base":4,"order_only":5,"irrelevant_plain":6,"repeat_2":7,"repeat_1":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"repeat_1":"6","irrelevant_adversarial":"12","relevant":"13","order_only":"6","base":"6","repeat_4":"6","repeat_3":"6","repeat_5":"6","irrelevant_plain":"6","repeat_2":"6"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"irrelevant_adversarial":1,"relevant":2,"order_only":3,"base":4,"repeat_4":5,"repeat_3":6,"repeat_5":7,"irrelevant_plain":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"order_only":"8","base":"8","repeat_1":"8","relevant":"14","repeat_4":"8","irrelevant_adversarial":"16","irrelevant_plain":"8","repeat_5":"8","repeat_3":"8","repeat_2":"8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"base":1,"repeat_1":2,"relevant":3,"repeat_4":4,"irrelevant_adversarial":5,"irrelevant_plain":6,"repeat_5":7,"repeat_3":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"repeat_1":"2","repeat_3":"2","repeat_5":"2","base":"2","irrelevant_adversarial":"2","irrelevant_plain":"2","repeat_4":"2","order_only":"2","relevant":"3","repeat_2":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"repeat_3":1,"repeat_5":2,"base":3,"irrelevant_adversarial":4,"irrelevant_plain":5,"repeat_4":6,"order_only":7,"relevant":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"repeat_3":"2","repeat_4":"2","irrelevant_adversarial":"2","order_only":"2","base":"2","irrelevant_plain":"2","repeat_1":"2","repeat_5":"2","repeat_2":"2","relevant":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_4":1,"irrelevant_adversarial":2,"order_only":3,"base":4,"irrelevant_plain":5,"repeat_1":6,"repeat_5":7,"repeat_2":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"repeat_2":"2","relevant":"2","repeat_4":"2","base":"2","irrelevant_plain":"2","repeat_5":"2","repeat_1":"2","order_only":"2","repeat_3":"2","irrelevant_adversarial":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"relevant":1,"repeat_4":2,"base":3,"irrelevant_plain":4,"repeat_5":5,"repeat_1":6,"order_only":7,"repeat_3":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-456","experiment_seed":456,"answers":{"repeat_2":"2","repeat_5":"2","repeat_1":"2","relevant":"2","irrelevant_adversarial":"2","base":"2","repeat_3":"2","irrelevant_plain":"2","order_only":"2","repeat_4":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_5":1,"repeat_1":2,"relevant":3,"irrelevant_adversarial":4,"base":5,"repeat_3":6,"irrelevant_plain":7,"order_only":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"M00-A","repeat_1":"M00-A","repeat_5":"M00-A","irrelevant_plain":"M00-A","repeat_3":"M00-A","base":"M00-A","repeat_2":"M00-A","relevant":"M00-B","repeat_4":"M00-A","order_only":"M00-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_1":1,"repeat_5":2,"irrelevant_plain":3,"repeat_3":4,"base":5,"repeat_2":6,"relevant":7,"repeat_4":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"repeat_2":"M01-A","relevant":"M01-B","base":"M01-A","repeat_5":"M01-A","order_only":"M01-A","irrelevant_adversarial":"M01-A","repeat_3":"M01-A","irrelevant_plain":"M01-A","repeat_4":"M01-A","repeat_1":"M01-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"relevant":1,"base":2,"repeat_5":3,"order_only":4,"irrelevant_adversarial":5,"repeat_3":6,"irrelevant_plain":7,"repeat_4":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"relevant":"M02-B","order_only":"M02-B","repeat_3":"M02-C","repeat_1":"M02-C","irrelevant_adversarial":"M02-A","repeat_5":"M02-C","repeat_2":"M02-C","repeat_4":"M02-C","irrelevant_plain":"M02-C","base":"M02-C"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"order_only":1,"repeat_3":2,"repeat_1":3,"irrelevant_adversarial":4,"repeat_5":5,"repeat_2":6,"repeat_4":7,"irrelevant_plain":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"repeat_5":"M03-A","repeat_4":"M03-A","irrelevant_adversarial":"M03-C","repeat_1":"M03-A","base":"M03-A","irrelevant_plain":"M03-C","repeat_2":"M03-A","repeat_3":"M03-A","relevant":"M03-C","order_only":"M03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_4":1,"irrelevant_adversarial":2,"repeat_1":3,"base":4,"irrelevant_plain":5,"repeat_2":6,"repeat_3":7,"relevant":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"base":"E00-C","repeat_1":"E00-C","relevant":"E00-B","repeat_4":"E00-C","order_only":"E00-C","repeat_3":"E00-C","repeat_5":"E00-C","irrelevant_plain":"E00-C","repeat_2":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"repeat_1":1,"relevant":2,"repeat_4":3,"order_only":4,"repeat_3":5,"repeat_5":6,"irrelevant_plain":7,"repeat_2":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"repeat_2":"E01-C","repeat_3":"E01-C","base":"E01-C","repeat_4":"E01-C","irrelevant_plain":"E01-C","order_only":"E01-C","repeat_5":"E01-C","relevant":"E01-C","repeat_1":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_3":1,"base":2,"repeat_4":3,"irrelevant_plain":4,"order_only":5,"repeat_5":6,"relevant":7,"repeat_1":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"E02-C","repeat_1":"E02-C","repeat_5":"E02-C","repeat_2":"E02-C","irrelevant_plain":"E02-C","base":"E02-C","relevant":"E02-B","order_only":"E02-D","repeat_4":"E02-C","repeat_3":"E02-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_1":1,"repeat_5":2,"repeat_2":3,"irrelevant_plain":4,"base":5,"relevant":6,"order_only":7,"repeat_4":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"repeat_3":"E03-C","irrelevant_plain":"E03-C","relevant":"E03-B","repeat_1":"E03-C","order_only":"E03-C","repeat_5":"E03-C","irrelevant_adversarial":"E03-A","repeat_2":"E03-C","repeat_4":"E03-C","base":"E03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"irrelevant_plain":1,"relevant":2,"repeat_1":3,"order_only":4,"repeat_5":5,"irrelevant_adversarial":6,"repeat_2":7,"repeat_4":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"base":"18","relevant":"188","irrelevant_adversarial":"50","order_only":"50","irrelevant_plain":"18","repeat_2":"18","repeat_5":"18","repeat_4":"18","repeat_3":"18","repeat_1":"18"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"relevant":1,"irrelevant_adversarial":2,"order_only":3,"irrelevant_plain":4,"repeat_2":5,"repeat_5":6,"repeat_4":7,"repeat_3":8,"repeat_1":9},"canonicalized_call_ids":["irrelevant_adversarial","order_only"]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"repeat_5":"18","relevant":"188","irrelevant_adversarial":"137","repeat_4":"18","base":"18","irrelevant_plain":"18","order_only":"188","repeat_1":"18","repeat_2":"18","repeat_3":"18"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"relevant":1,"irrelevant_adversarial":2,"repeat_4":3,"base":4,"irrelevant_plain":5,"order_only":6,"repeat_1":7,"repeat_2":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"order_only":"101","irrelevant_adversarial":"1023","base":"101","repeat_2":"101","repeat_1":"101","repeat_4":"101","relevant":"101","repeat_5":"101","irrelevant_plain":"101","repeat_3":"101"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"irrelevant_adversarial":1,"base":2,"repeat_2":3,"repeat_1":4,"repeat_4":5,"relevant":6,"repeat_5":7,"irrelevant_plain":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"order_only":"114","irrelevant_plain":"114","irrelevant_adversarial":"52","base":"52","relevant":"61","repeat_3":"52","repeat_2":"52","repeat_4":"52","repeat_5":"52","repeat_1":"52"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"order_only":0,"irrelevant_plain":1,"irrelevant_adversarial":2,"base":3,"relevant":4,"repeat_3":5,"repeat_2":6,"repeat_4":7,"repeat_5":8,"repeat_1":9},"canonicalized_call_ids":["irrelevant_adversarial","base","relevant","repeat_3","repeat_2","repeat_4","repeat_5","repeat_1"]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"repeat_1":"8","relevant":"14","irrelevant_plain":"8","base":"8","repeat_3":"8","irrelevant_adversarial":"18","order_only":"8","repeat_4":"8","repeat_2":"8","repeat_5":"8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"relevant":1,"irrelevant_plain":2,"base":3,"repeat_3":4,"irrelevant_adversarial":5,"order_only":6,"repeat_4":7,"repeat_2":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"repeat_3":"8","order_only":"8","irrelevant_plain":"8","repeat_2":"8","repeat_5":"8","irrelevant_adversarial":"119","repeat_1":"8","base":"8","relevant":"11","repeat_4":"8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"order_only":1,"irrelevant_plain":2,"repeat_2":3,"repeat_5":4,"irrelevant_adversarial":5,"repeat_1":6,"base":7,"relevant":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"repeat_2":"6","repeat_3":"6","base":"6","order_only":"6","irrelevant_plain":"6","repeat_4":"6","relevant":"13","repeat_1":"6","repeat_5":"6","irrelevant_adversarial":"12"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_3":1,"base":2,"order_only":3,"irrelevant_plain":4,"repeat_4":5,"relevant":6,"repeat_1":7,"repeat_5":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"base":"8","relevant":"14","repeat_4":"8","irrelevant_plain":"8","repeat_3":"8","repeat_2":"8","repeat_5":"8","order_only":"8","irrelevant_adversarial":"16","repeat_1":"8"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"relevant":1,"repeat_4":2,"irrelevant_plain":3,"repeat_3":4,"repeat_2":5,"repeat_5":6,"order_only":7,"irrelevant_adversarial":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"repeat_5":"2","base":"2","order_only":"2","repeat_3":"2","repeat_2":"2","irrelevant_plain":"2","repeat_1":"2","repeat_4":"2","irrelevant_adversarial":"2","relevant":"3"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"base":1,"order_only":2,"repeat_3":3,"repeat_2":4,"irrelevant_plain":5,"repeat_1":6,"repeat_4":7,"irrelevant_adversarial":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"repeat_3":"2","repeat_5":"2","relevant":"2","base":"2","irrelevant_adversarial":"2","irrelevant_plain":"2","order_only":"2","repeat_1":"2","repeat_4":"2","repeat_2":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_5":1,"relevant":2,"base":3,"irrelevant_adversarial":4,"irrelevant_plain":5,"order_only":6,"repeat_1":7,"repeat_4":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"2","repeat_2":"2","repeat_1":"2","order_only":"2","repeat_3":"2","base":"2","relevant":"2","repeat_4":"2","repeat_5":"2","irrelevant_plain":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_2":1,"repeat_1":2,"order_only":3,"repeat_3":4,"base":5,"relevant":6,"repeat_4":7,"repeat_5":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-789","experiment_seed":789,"answers":{"repeat_3":"2","order_only":"2","irrelevant_adversarial":"2","relevant":"2","repeat_2":"2","irrelevant_plain":"2","repeat_1":"2","base":"2","repeat_5":"2","repeat_4":"2"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"order_only":1,"irrelevant_adversarial":2,"relevant":3,"repeat_2":4,"irrelevant_plain":5,"repeat_1":6,"base":7,"repeat_5":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"irrelevant_adversarial":"M00-A","repeat_1":"M00-A","repeat_2":"M00-A","repeat_5":"M00-A","relevant":"M00-B","base":"M00-A","repeat_3":"M00-A","repeat_4":"M00-A","irrelevant_plain":"M00-A","order_only":"M00-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_1":1,"repeat_2":2,"repeat_5":3,"relevant":4,"base":5,"repeat_3":6,"repeat_4":7,"irrelevant_plain":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"repeat_4":"M01-A","order_only":"M01-A","repeat_2":"M01-A","repeat_1":"M01-A","relevant":"M01-D","irrelevant_plain":"M01-D","repeat_5":"M01-A","irrelevant_adversarial":"M01-A","base":"M01-A","repeat_3":"M01-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"order_only":1,"repeat_2":2,"repeat_1":3,"relevant":4,"irrelevant_plain":5,"repeat_5":6,"irrelevant_adversarial":7,"base":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"relevant":"M02-B","base":"M02-A","irrelevant_adversarial":"M02-A","repeat_2":"M02-A","repeat_5":"M02-A","repeat_3":"M02-A","order_only":"M02-A","repeat_4":"M02-A","irrelevant_plain":"M02-A","repeat_1":"M02-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"base":1,"irrelevant_adversarial":2,"repeat_2":3,"repeat_5":4,"repeat_3":5,"order_only":6,"repeat_4":7,"irrelevant_plain":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"repeat_2":"M03-A","repeat_5":"M03-A","relevant":"M03-C","repeat_3":"M03-A","repeat_1":"M03-A","irrelevant_adversarial":"M03-C","order_only":"M03-A","repeat_4":"M03-A","base":"M03-A","irrelevant_plain":"M03-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_5":1,"relevant":2,"repeat_3":3,"repeat_1":4,"irrelevant_adversarial":5,"order_only":6,"repeat_4":7,"base":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"repeat_5":"E00-C","repeat_1":"E00-C","base":"E00-C","relevant":"E00-B","irrelevant_adversarial":"E00-C","repeat_3":"E00-C","irrelevant_plain":"E00-C","repeat_4":"E00-C","order_only":"E00-C","repeat_2":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_1":1,"base":2,"relevant":3,"irrelevant_adversarial":4,"repeat_3":5,"irrelevant_plain":6,"repeat_4":7,"order_only":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"repeat_4":"E01-D","repeat_1":"E01-D","irrelevant_plain":"E01-D","irrelevant_adversarial":"E01-B","order_only":"E01-C","relevant":"E01-D","repeat_5":"E01-D","base":"E01-D","repeat_2":"E01-D","repeat_3":"E01-D"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_1":1,"irrelevant_plain":2,"irrelevant_adversarial":3,"order_only":4,"relevant":5,"repeat_5":6,"base":7,"repeat_2":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"repeat_2":"E02-C","base":"E02-C","repeat_4":"E02-C","repeat_3":"E02-C","repeat_1":"E02-C","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C","relevant":"E02-B","repeat_5":"E02-C","order_only":"E02-D"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"base":1,"repeat_4":2,"repeat_3":3,"repeat_1":4,"irrelevant_plain":5,"irrelevant_adversarial":6,"relevant":7,"repeat_5":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"base":"E03-C","order_only":"E03-C","irrelevant_plain":"E03-C","repeat_3":"E03-C","repeat_2":"E03-C","repeat_1":"E03-C","repeat_5":"E03-C","irrelevant_adversarial":"E03-C","repeat_4":"E03-C","relevant":"E03-B"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"order_only":1,"irrelevant_plain":2,"repeat_3":3,"repeat_2":4,"repeat_1":5,"repeat_5":6,"irrelevant_adversarial":7,"repeat_4":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"order_only":"153","repeat_1":"140","irrelevant_plain":"34","repeat_2":"140","relevant":"155","repeat_3":"140","base":"140","irrelevant_adversarial":"1050","repeat_4":"140","repeat_5":"140"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_1":1,"irrelevant_plain":2,"repeat_2":3,"relevant":4,"repeat_3":5,"base":6,"irrelevant_adversarial":7,"repeat_4":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"order_only":"188","repeat_3":"188","irrelevant_plain":"35","irrelevant_adversarial":"35","repeat_4":"188","base":"188","repeat_2":"188","repeat_5":"188","repeat_1":"188","relevant":"158"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_3":1,"irrelevant_plain":2,"irrelevant_adversarial":3,"repeat_4":4,"base":5,"repeat_2":6,"repeat_5":7,"repeat_1":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"base":"101","irrelevant_adversarial":"21","repeat_2":"101","repeat_4":"101","repeat_5":"101","repeat_1":"101","irrelevant_plain":"101","repeat_3":"101","relevant":"128","order_only":"101"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"irrelevant_adversarial":1,"repeat_2":2,"repeat_4":3,"repeat_5":4,"repeat_1":5,"irrelevant_plain":6,"repeat_3":7,"relevant":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"order_only":"58","irrelevant_plain":"114","repeat_1":"114","base":"114","repeat_4":"114","repeat_5":"114","relevant":"113","repeat_3":"114","repeat_2":"114","irrelevant_adversarial":"105"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"irrelevant_plain":1,"repeat_1":2,"base":3,"repeat_4":4,"repeat_5":5,"relevant":6,"repeat_3":7,"repeat_2":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"irrelevant_plain":"18","repeat_3":"18","repeat_2":"18","relevant":"24","base":"18","repeat_1":"18","repeat_5":"18","irrelevant_adversarial":"18","repeat_4":"18","order_only":"18"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_3":1,"repeat_2":2,"relevant":3,"base":4,"repeat_1":5,"repeat_5":6,"irrelevant_adversarial":7,"repeat_4":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"relevant":"23","irrelevant_adversarial":"20","repeat_3":"20","repeat_2":"20","repeat_5":"20","repeat_4":"20","repeat_1":"20","base":"20","irrelevant_plain":"20","order_only":"20"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"irrelevant_adversarial":1,"repeat_3":2,"repeat_2":3,"repeat_5":4,"repeat_4":5,"repeat_1":6,"base":7,"irrelevant_plain":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"irrelevant_plain":"26","repeat_5":"26","relevant":"33","repeat_1":"26","order_only":"26","repeat_4":"26","base":"26","repeat_2":"26","repeat_3":"26","irrelevant_adversarial":"26"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_5":1,"relevant":2,"repeat_1":3,"order_only":4,"repeat_4":5,"base":6,"repeat_2":7,"repeat_3":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"repeat_2":"16","irrelevant_adversarial":"16","repeat_3":"16","order_only":"16","repeat_4":"16","repeat_1":"16","base":"16","repeat_5":"16","irrelevant_plain":"16","relevant":"22"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"irrelevant_adversarial":1,"repeat_3":2,"order_only":3,"repeat_4":4,"repeat_1":5,"base":6,"repeat_5":7,"irrelevant_plain":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"base":"2","repeat_2":"2","irrelevant_adversarial":"2","relevant":"3","irrelevant_plain":"2","order_only":"2","repeat_3":"2","repeat_1":"2","repeat_5":"2","repeat_4":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"repeat_2":1,"irrelevant_adversarial":2,"relevant":3,"irrelevant_plain":4,"order_only":5,"repeat_3":6,"repeat_1":7,"repeat_5":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"relevant":"3","repeat_2":"2","base":"2","repeat_5":"2","irrelevant_adversarial":"2","irrelevant_plain":"2","repeat_3":"2","repeat_1":"2","order_only":"2","repeat_4":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_2":1,"base":2,"repeat_5":3,"irrelevant_adversarial":4,"irrelevant_plain":5,"repeat_3":6,"repeat_1":7,"order_only":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"repeat_3":"2","repeat_5":"2","irrelevant_adversarial":"2","repeat_2":"2","relevant":"3","irrelevant_plain":"2","base":"2","repeat_1":"2","order_only":"2","repeat_4":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_5":1,"irrelevant_adversarial":2,"repeat_2":3,"relevant":4,"irrelevant_plain":5,"base":6,"repeat_1":7,"order_only":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-123","experiment_seed":123,"answers":{"relevant":"3","repeat_5":"2","repeat_1":"2","irrelevant_adversarial":"2","repeat_2":"2","order_only":"2","irrelevant_plain":"2","repeat_3":"2","repeat_4":"2","base":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_5":1,"repeat_1":2,"irrelevant_adversarial":3,"repeat_2":4,"order_only":5,"irrelevant_plain":6,"repeat_3":7,"repeat_4":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"base":"M00-A","repeat_5":"M00-A","relevant":"M00-B","repeat_3":"M00-A","order_only":"M00-A","irrelevant_adversarial":"M00-A","repeat_2":"M00-A","repeat_4":"M00-A","irrelevant_plain":"M00-A","repeat_1":"M00-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"repeat_5":1,"relevant":2,"repeat_3":3,"order_only":4,"irrelevant_adversarial":5,"repeat_2":6,"repeat_4":7,"irrelevant_plain":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"repeat_4":"M01-A","relevant":"M01-D","repeat_3":"M01-A","irrelevant_plain":"M01-D","repeat_5":"M01-A","base":"M01-A","repeat_2":"M01-A","irrelevant_adversarial":"M01-A","repeat_1":"M01-A","order_only":"M01-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"relevant":1,"repeat_3":2,"irrelevant_plain":3,"repeat_5":4,"base":5,"repeat_2":6,"irrelevant_adversarial":7,"repeat_1":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A","repeat_5":"M02-A","repeat_4":"M02-A","relevant":"M02-B","order_only":"M02-A","base":"M02-A","repeat_2":"M02-A","repeat_3":"M02-A","repeat_1":"M02-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"irrelevant_adversarial":1,"repeat_5":2,"repeat_4":3,"relevant":4,"order_only":5,"base":6,"repeat_2":7,"repeat_3":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"repeat_5":"M03-A","repeat_4":"M03-A","irrelevant_adversarial":"M03-C","repeat_3":"M03-A","repeat_1":"M03-A","irrelevant_plain":"M03-A","order_only":"M03-A","base":"M03-A","repeat_2":"M03-A","relevant":"M03-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_4":1,"irrelevant_adversarial":2,"repeat_3":3,"repeat_1":4,"irrelevant_plain":5,"order_only":6,"base":7,"repeat_2":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"repeat_1":"E00-C","repeat_3":"E00-C","repeat_2":"E00-C","relevant":"E00-B","repeat_4":"E00-C","repeat_5":"E00-C","irrelevant_adversarial":"E00-C","irrelevant_plain":"E00-C","order_only":"E00-C","base":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"repeat_3":1,"repeat_2":2,"relevant":3,"repeat_4":4,"repeat_5":5,"irrelevant_adversarial":6,"irrelevant_plain":7,"order_only":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"base":"E01-D","repeat_2":"E01-D","repeat_1":"E01-D","irrelevant_plain":"E01-D","repeat_5":"E01-D","relevant":"E01-D","order_only":"E01-C","irrelevant_adversarial":"E01-D","repeat_4":"E01-D","repeat_3":"E01-D"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"repeat_2":1,"repeat_1":2,"irrelevant_plain":3,"repeat_5":4,"relevant":5,"order_only":6,"irrelevant_adversarial":7,"repeat_4":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"E02-C","irrelevant_plain":"E02-C","relevant":"E02-B","repeat_3":"E02-C","repeat_1":"E02-C","order_only":"E02-D","base":"E02-C","repeat_4":"E02-C","repeat_2":"E02-C","repeat_5":"E02-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"irrelevant_plain":1,"relevant":2,"repeat_3":3,"repeat_1":4,"order_only":5,"base":6,"repeat_4":7,"repeat_2":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"repeat_1":"E03-C","irrelevant_plain":"E03-C","order_only":"E03-C","repeat_5":"E03-C","irrelevant_adversarial":"E03-C","repeat_2":"E03-C","base":"E03-C","relevant":"E03-B","repeat_3":"E03-C","repeat_4":"E03-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"irrelevant_plain":1,"order_only":2,"repeat_5":3,"irrelevant_adversarial":4,"repeat_2":5,"base":6,"relevant":7,"repeat_3":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"order_only":"153","repeat_2":"140","irrelevant_adversarial":"1050","repeat_3":"140","relevant":"155","irrelevant_plain":"34","repeat_5":"140","base":"140","repeat_1":"140","repeat_4":"140"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_2":1,"irrelevant_adversarial":2,"repeat_3":3,"relevant":4,"irrelevant_plain":5,"repeat_5":6,"base":7,"repeat_1":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"1051","relevant":"158","order_only":"188","repeat_5":"188","repeat_2":"188","repeat_1":"188","irrelevant_plain":"35","base":"188","repeat_4":"188","repeat_3":"188"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"relevant":1,"order_only":2,"repeat_5":3,"repeat_2":4,"repeat_1":5,"irrelevant_plain":6,"base":7,"repeat_4":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"101","irrelevant_adversarial":"21","base":"101","relevant":"128","repeat_3":"101","repeat_4":"101","repeat_1":"101","repeat_2":"101","order_only":"101","repeat_5":"101"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"irrelevant_adversarial":1,"base":2,"relevant":3,"repeat_3":4,"repeat_4":5,"repeat_1":6,"repeat_2":7,"order_only":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"repeat_3":"114","repeat_2":"114","relevant":"113","irrelevant_adversarial":"105","repeat_4":"114","repeat_5":"114","irrelevant_plain":"114","order_only":"58","repeat_1":"114","base":"114"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_2":1,"relevant":2,"irrelevant_adversarial":3,"repeat_4":4,"repeat_5":5,"irrelevant_plain":6,"order_only":7,"repeat_1":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"18","repeat_4":"18","order_only":"18","irrelevant_plain":"18","repeat_1":"18","repeat_3":"18","repeat_5":"18","relevant":"24","base":"18","repeat_2":"18"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_4":1,"order_only":2,"irrelevant_plain":3,"repeat_1":4,"repeat_3":5,"repeat_5":6,"relevant":7,"base":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"relevant":"23","base":"20","irrelevant_plain":"20","repeat_1":"20","irrelevant_adversarial":"20","repeat_4":"20","repeat_2":"20","repeat_3":"20","order_only":"20","repeat_5":"20"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"base":1,"irrelevant_plain":2,"repeat_1":3,"irrelevant_adversarial":4,"repeat_4":5,"repeat_2":6,"repeat_3":7,"order_only":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"26","base":"26","repeat_1":"26","order_only":"26","repeat_3":"26","irrelevant_plain":"26","relevant":"33","repeat_5":"26","repeat_2":"26","repeat_4":"26"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"base":1,"repeat_1":2,"order_only":3,"repeat_3":4,"irrelevant_plain":5,"relevant":6,"repeat_5":7,"repeat_2":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"repeat_3":"16","repeat_2":"16","repeat_1":"16","repeat_5":"16","order_only":"16","repeat_4":"16","relevant":"22","irrelevant_adversarial":"16","base":"16","irrelevant_plain":"16"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_2":1,"repeat_1":2,"repeat_5":3,"order_only":4,"repeat_4":5,"relevant":6,"irrelevant_adversarial":7,"base":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"repeat_4":"2","repeat_5":"2","order_only":"2","base":"2","repeat_1":"2","relevant":"3","repeat_2":"2","irrelevant_adversarial":"2","repeat_3":"2","irrelevant_plain":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_5":1,"order_only":2,"base":3,"repeat_1":4,"relevant":5,"repeat_2":6,"irrelevant_adversarial":7,"repeat_3":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"base":"2","repeat_3":"2","repeat_5":"2","relevant":"3","irrelevant_adversarial":"2","order_only":"2","repeat_1":"2","repeat_4":"2","repeat_2":"2","irrelevant_plain":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"repeat_3":1,"repeat_5":2,"relevant":3,"irrelevant_adversarial":4,"order_only":5,"repeat_1":6,"repeat_4":7,"repeat_2":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"repeat_5":"2","irrelevant_plain":"2","relevant":"3","repeat_2":"2","irrelevant_adversarial":"2","repeat_4":"2","repeat_1":"2","repeat_3":"2","base":"2","order_only":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"irrelevant_plain":1,"relevant":2,"repeat_2":3,"irrelevant_adversarial":4,"repeat_4":5,"repeat_1":6,"repeat_3":7,"base":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-456","experiment_seed":456,"answers":{"repeat_2":"2","repeat_3":"2","repeat_5":"2","base":"2","irrelevant_adversarial":"2","relevant":"3","repeat_4":"2","repeat_1":"2","irrelevant_plain":"2","order_only":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_3":1,"repeat_5":2,"base":3,"irrelevant_adversarial":4,"relevant":5,"repeat_4":6,"repeat_1":7,"irrelevant_plain":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_plain":"M00-A","repeat_3":"M00-A","repeat_4":"M00-A","repeat_1":"M00-A","repeat_2":"M00-A","base":"M00-A","relevant":"M00-B","order_only":"M00-A","repeat_5":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_3":1,"repeat_4":2,"repeat_1":3,"repeat_2":4,"base":5,"relevant":6,"order_only":7,"repeat_5":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_5":"M01-A","repeat_1":"M01-A","base":"M01-A","irrelevant_adversarial":"M01-A","relevant":"M01-D","irrelevant_plain":"M01-D","order_only":"M01-A","repeat_2":"M01-A","repeat_3":"M01-A","repeat_4":"M01-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_1":1,"base":2,"irrelevant_adversarial":3,"relevant":4,"irrelevant_plain":5,"order_only":6,"repeat_2":7,"repeat_3":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_3":"M02-A","repeat_4":"M02-A","irrelevant_adversarial":"M02-A","relevant":"M02-B","base":"M02-A","irrelevant_plain":"M02-A","repeat_2":"M02-A","order_only":"M02-A","repeat_1":"M02-A","repeat_5":"M02-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_4":1,"irrelevant_adversarial":2,"relevant":3,"base":4,"irrelevant_plain":5,"repeat_2":6,"order_only":7,"repeat_1":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_2":"M03-A","irrelevant_adversarial":"M03-C","repeat_1":"M03-A","repeat_5":"M03-A","repeat_3":"M03-A","base":"M03-A","relevant":"M03-B","repeat_4":"M03-A","irrelevant_plain":"M03-A","order_only":"M03-A"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"irrelevant_adversarial":1,"repeat_1":2,"repeat_5":3,"repeat_3":4,"base":5,"relevant":6,"repeat_4":7,"irrelevant_plain":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"order_only":"E00-C","repeat_4":"E00-C","repeat_1":"E00-C","relevant":"E00-B","irrelevant_adversarial":"E00-C","repeat_2":"E00-C","repeat_3":"E00-C","repeat_5":"E00-C","base":"E00-C","irrelevant_plain":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_4":1,"repeat_1":2,"relevant":3,"irrelevant_adversarial":4,"repeat_2":5,"repeat_3":6,"repeat_5":7,"base":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_2":"E01-D","relevant":"E01-D","repeat_3":"E01-D","irrelevant_plain":"E01-D","repeat_4":"E01-D","irrelevant_adversarial":"E01-B","repeat_5":"E01-D","order_only":"E01-C","repeat_1":"E01-D","base":"E01-D"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"relevant":1,"repeat_3":2,"irrelevant_plain":3,"repeat_4":4,"irrelevant_adversarial":5,"repeat_5":6,"order_only":7,"repeat_1":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_3":"E02-C","relevant":"E02-B","base":"E02-C","irrelevant_adversarial":"E02-C","repeat_5":"E02-C","repeat_1":"E02-C","repeat_2":"E02-C","repeat_4":"E02-C","irrelevant_plain":"E02-C","order_only":"E02-D"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"relevant":1,"base":2,"irrelevant_adversarial":3,"repeat_5":4,"repeat_1":5,"repeat_2":6,"repeat_4":7,"irrelevant_plain":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"relevant":"E03-B","base":"E03-C","repeat_5":"E03-C","repeat_1":"E03-C","repeat_4":"E03-C","irrelevant_adversarial":"E03-C","order_only":"E03-C","repeat_3":"E03-C","repeat_2":"E03-C","irrelevant_plain":"E03-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"base":1,"repeat_5":2,"repeat_1":3,"repeat_4":4,"irrelevant_adversarial":5,"order_only":6,"repeat_3":7,"repeat_2":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_2":"142","relevant":"155","repeat_5":"140","repeat_3":"142","base":"142","repeat_1":"142","irrelevant_plain":"34","order_only":"153","repeat_4":"142","irrelevant_adversarial":"1050"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"relevant":1,"repeat_5":2,"repeat_3":3,"base":4,"repeat_1":5,"irrelevant_plain":6,"order_only":7,"repeat_4":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_3":"188","irrelevant_adversarial":"35","repeat_4":"188","relevant":"158","base":"188","order_only":"188","repeat_5":"188","irrelevant_plain":"35","repeat_1":"188","repeat_2":"188"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"irrelevant_adversarial":1,"repeat_4":2,"relevant":3,"base":4,"order_only":5,"repeat_5":6,"irrelevant_plain":7,"repeat_1":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_5":"101","relevant":"128","base":"101","order_only":"101","repeat_4":"101","irrelevant_plain":"101","repeat_1":"101","irrelevant_adversarial":"23","repeat_2":"101","repeat_3":"101"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"relevant":1,"base":2,"order_only":3,"repeat_4":4,"irrelevant_plain":5,"repeat_1":6,"irrelevant_adversarial":7,"repeat_2":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_2":"114","irrelevant_plain":"114","repeat_5":"114","base":"114","order_only":"58","irrelevant_adversarial":"105","repeat_3":"114","repeat_1":"114","repeat_4":"114","relevant":"113"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"irrelevant_plain":1,"repeat_5":2,"base":3,"order_only":4,"irrelevant_adversarial":5,"repeat_3":6,"repeat_1":7,"repeat_4":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_3":"18","repeat_1":"18","relevant":"24","repeat_4":"18","order_only":"18","irrelevant_adversarial":"18","repeat_2":"18","irrelevant_plain":"18","repeat_5":"18","base":"18"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_1":1,"relevant":2,"repeat_4":3,"order_only":4,"irrelevant_adversarial":5,"repeat_2":6,"irrelevant_plain":7,"repeat_5":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_plain":"20","order_only":"20","repeat_3":"20","repeat_2":"20","relevant":"23","repeat_5":"20","irrelevant_adversarial":"20","base":"20","repeat_4":"20","repeat_1":"20"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"order_only":1,"repeat_3":2,"repeat_2":3,"relevant":4,"repeat_5":5,"irrelevant_adversarial":6,"base":7,"repeat_4":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_1":"26","irrelevant_plain":"26","base":"26","repeat_5":"26","relevant":"33","irrelevant_adversarial":"26","repeat_4":"26","order_only":"26","repeat_2":"26","repeat_3":"26"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"irrelevant_plain":1,"base":2,"repeat_5":3,"relevant":4,"irrelevant_adversarial":5,"repeat_4":6,"order_only":7,"repeat_2":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"relevant":"22","repeat_4":"16","repeat_5":"16","base":"16","order_only":"16","repeat_1":"16","repeat_2":"16","repeat_3":"16","irrelevant_plain":"16","irrelevant_adversarial":"16"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_4":1,"repeat_5":2,"base":3,"order_only":4,"repeat_1":5,"repeat_2":6,"repeat_3":7,"irrelevant_plain":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_1":"2","order_only":"2","repeat_3":"2","repeat_5":"2","relevant":"3","repeat_2":"2","irrelevant_plain":"2","base":"2","irrelevant_adversarial":"2","repeat_4":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"order_only":1,"repeat_3":2,"repeat_5":3,"relevant":4,"repeat_2":5,"irrelevant_plain":6,"base":7,"irrelevant_adversarial":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"irrelevant_adversarial":"2","repeat_1":"2","repeat_3":"2","relevant":"3","base":"2","repeat_4":"2","order_only":"2","repeat_2":"2","irrelevant_plain":"2","repeat_5":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_1":1,"repeat_3":2,"relevant":3,"base":4,"repeat_4":5,"order_only":6,"repeat_2":7,"irrelevant_plain":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_4":"2","repeat_2":"2","order_only":"2","base":"2","repeat_3":"2","irrelevant_adversarial":"2","repeat_5":"2","irrelevant_plain":"2","relevant":"3","repeat_1":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_2":1,"order_only":2,"base":3,"repeat_3":4,"irrelevant_adversarial":5,"repeat_5":6,"irrelevant_plain":7,"relevant":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-789","experiment_seed":789,"answers":{"repeat_3":"2","base":"2","repeat_5":"2","order_only":"2","relevant":"3","repeat_1":"2","irrelevant_plain":"2","repeat_2":"2","repeat_4":"2","irrelevant_adversarial":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"base":1,"repeat_5":2,"order_only":3,"relevant":4,"repeat_1":5,"irrelevant_plain":6,"repeat_2":7,"repeat_4":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_4":"M00-A","relevant":"M00-B","order_only":"M00-A","base":"M00-A","repeat_2":"M00-A","irrelevant_adversarial":"M00-A","repeat_3":"M00-A","repeat_5":"M00-A","repeat_1":"M00-A","irrelevant_plain":"M00-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"relevant":1,"order_only":2,"base":3,"repeat_2":4,"irrelevant_adversarial":5,"repeat_3":6,"repeat_5":7,"repeat_1":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_1":"M01-A","irrelevant_adversarial":"M01-A","repeat_2":"M01-A","irrelevant_plain":"M01-A","base":"M01-D","repeat_5":"M01-D","relevant":"M01-D","repeat_3":"M01-D","order_only":"M01-C","repeat_4":"M01-D"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"irrelevant_adversarial":1,"repeat_2":2,"irrelevant_plain":3,"base":4,"repeat_5":5,"relevant":6,"repeat_3":7,"order_only":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_4":"M02-A","repeat_5":"M02-A","repeat_3":"M02-A","order_only":"M02-A","repeat_2":"M02-A","relevant":"M02-B","base":"M02-A","repeat_1":"M02-A","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_5":1,"repeat_3":2,"order_only":3,"repeat_2":4,"relevant":5,"base":6,"repeat_1":7,"irrelevant_plain":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"order_only":"M03-A","repeat_2":"M03-C","irrelevant_plain":"M03-A","repeat_3":"M03-C","repeat_1":"M03-C","relevant":"M03-C","repeat_5":"M03-C","irrelevant_adversarial":"M03-C","repeat_4":"M03-C","base":"M03-C"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_2":1,"irrelevant_plain":2,"repeat_3":3,"repeat_1":4,"relevant":5,"repeat_5":6,"irrelevant_adversarial":7,"repeat_4":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_3":"E00-C","repeat_5":"E00-C","repeat_1":"E00-C","irrelevant_adversarial":"E00-C","base":"E00-C","irrelevant_plain":"E00-C","relevant":"E00-B","order_only":"E00-C","repeat_2":"E00-C","repeat_4":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_5":1,"repeat_1":2,"irrelevant_adversarial":3,"base":4,"irrelevant_plain":5,"relevant":6,"order_only":7,"repeat_2":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"irrelevant_plain":"E01-D","irrelevant_adversarial":"E01-D","repeat_5":"E01-D","repeat_1":"E01-D","relevant":"E01-D","repeat_4":"E01-D","repeat_3":"E01-D","order_only":"E01-C","repeat_2":"E01-D","base":"E01-D"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"irrelevant_adversarial":1,"repeat_5":2,"repeat_1":3,"relevant":4,"repeat_4":5,"repeat_3":6,"order_only":7,"repeat_2":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"relevant":"E02-B","repeat_3":"E02-C","order_only":"E02-D","base":"E02-C","repeat_1":"E02-C","repeat_4":"E02-C","repeat_2":"E02-C","repeat_5":"E02-C","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_3":1,"order_only":2,"base":3,"repeat_1":4,"repeat_4":5,"repeat_2":6,"repeat_5":7,"irrelevant_plain":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"order_only":"E03-C","irrelevant_plain":"E03-C","relevant":"E03-B","repeat_1":"E03-C","base":"E03-C","repeat_4":"E03-C","repeat_5":"E03-C","irrelevant_adversarial":"E03-C","repeat_2":"E03-C","repeat_3":"E03-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"order_only":0,"irrelevant_plain":1,"relevant":2,"repeat_1":3,"base":4,"repeat_4":5,"repeat_5":6,"irrelevant_adversarial":7,"repeat_2":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"order_only":"153","repeat_3":"40","repeat_1":"40","relevant":"55","repeat_2":"40","repeat_5":"40","irrelevant_plain":"32","base":"40","irrelevant_adversarial":"45","repeat_4":"50"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"repeat_3":1,"repeat_1":2,"relevant":3,"repeat_2":4,"repeat_5":5,"irrelevant_plain":6,"base":7,"irrelevant_adversarial":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"irrelevant_adversarial":"57","base":"35","irrelevant_plain":"35","order_only":"171","relevant":"58","repeat_4":"35","repeat_1":"35","repeat_3":"35","repeat_2":"35","repeat_5":"35"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"base":1,"irrelevant_plain":2,"order_only":3,"relevant":4,"repeat_4":5,"repeat_1":6,"repeat_3":7,"repeat_2":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_3":"118","relevant":"128","base":"118","repeat_2":"118","repeat_1":"118","order_only":"101","irrelevant_plain":"118","irrelevant_adversarial":"23","repeat_4":"111","repeat_5":"111"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"relevant":1,"base":2,"repeat_2":3,"repeat_1":4,"order_only":5,"irrelevant_plain":6,"irrelevant_adversarial":7,"repeat_4":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_2":"108","repeat_1":"108","repeat_4":"108","repeat_3":"108","base":"108","irrelevant_plain":"114","order_only":"48","relevant":"113","irrelevant_adversarial":"105","repeat_5":"108"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_1":1,"repeat_4":2,"repeat_3":3,"base":4,"irrelevant_plain":5,"order_only":6,"relevant":7,"irrelevant_adversarial":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_4":"","irrelevant_plain":"","irrelevant_adversarial":"18","repeat_5":"","base":"","order_only":"","repeat_1":"","repeat_3":"","repeat_2":"","relevant":"Heatmap"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"irrelevant_plain":1,"irrelevant_adversarial":2,"repeat_5":3,"base":4,"order_only":5,"repeat_1":6,"repeat_3":7,"repeat_2":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_4":"","irrelevant_adversarial":"20","base":"","order_only":"","repeat_3":"","repeat_1":"","irrelevant_plain":"","repeat_2":"","repeat_5":"","relevant":"23"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"irrelevant_adversarial":1,"base":2,"order_only":3,"repeat_3":4,"repeat_1":5,"irrelevant_plain":6,"repeat_2":7,"repeat_5":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_5":"}26","irrelevant_adversarial":"26","base":"https://www.163.com","irrelevant_plain":"{\"answer\": \"}</think>otlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlin","order_only":"}26","relevant":"}33","repeat_3":"}26","repeat_4":"}26","repeat_2":"}26","repeat_1":"}26"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":["irrelevant_plain"],"call_positions":{"repeat_5":0,"irrelevant_adversarial":1,"base":2,"irrelevant_plain":3,"order_only":4,"relevant":5,"repeat_3":6,"repeat_4":7,"repeat_2":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_1":"","relevant":"","irrelevant_plain":"","order_only":"","base":"math.ceil(8 + 8)","repeat_2":"math.ceil(8 + 8)","repeat_5":"math.ceil(8 + 8)","repeat_4":"math.ceil(8 + 8)","irrelevant_adversarial":"16","repeat_3":""},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_1":0,"relevant":1,"irrelevant_plain":2,"order_only":3,"base":4,"repeat_2":5,"repeat_5":6,"repeat_4":7,"irrelevant_adversarial":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_4":"2","repeat_1":"2","repeat_3":"2","relevant":"3","repeat_2":"2","repeat_5":"2","irrelevant_adversarial":"2","base":"2","irrelevant_plain":"2","order_only":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_1":1,"repeat_3":2,"relevant":3,"repeat_2":4,"repeat_5":5,"irrelevant_adversarial":6,"base":7,"irrelevant_plain":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_3":"2","base":"2","relevant":"3","order_only":"2","irrelevant_plain":"2","repeat_5":"2","repeat_4":"2","irrelevant_adversarial":"2","repeat_2":"2","repeat_1":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"base":1,"relevant":2,"order_only":3,"irrelevant_plain":4,"repeat_5":5,"repeat_4":6,"irrelevant_adversarial":7,"repeat_2":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"repeat_3":"2","irrelevant_plain":"2","relevant":"3","repeat_4":"2","base":"2","repeat_1":"2","order_only":"2","repeat_5":"2","irrelevant_adversarial":"2","repeat_2":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"irrelevant_plain":1,"relevant":2,"repeat_4":3,"base":4,"repeat_1":5,"order_only":6,"repeat_5":7,"irrelevant_adversarial":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-123","experiment_seed":123,"answers":{"irrelevant_adversarial":"2","repeat_4":"2","repeat_1":"2","repeat_2":"2","order_only":"2","repeat_5":"2","irrelevant_plain":"2","repeat_3":"2","relevant":"3","base":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_4":1,"repeat_1":2,"repeat_2":3,"order_only":4,"repeat_5":5,"irrelevant_plain":6,"repeat_3":7,"relevant":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"repeat_4":"M00-A","repeat_5":"M00-A","order_only":"M00-A","base":"M00-A","relevant":"M00-B","repeat_2":"M00-A","repeat_3":"M00-A","irrelevant_adversarial":"M00-A","repeat_1":"M00-A","irrelevant_plain":"M00-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_5":1,"order_only":2,"base":3,"relevant":4,"repeat_2":5,"repeat_3":6,"irrelevant_adversarial":7,"repeat_1":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"M01-D","relevant":"M01-D","base":"M01-D","order_only":"M01-C","repeat_4":"M01-D","repeat_3":"M01-D","repeat_5":"M01-D","repeat_2":"M01-D","irrelevant_plain":"M01-A","repeat_1":"M01-D"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"relevant":1,"base":2,"order_only":3,"repeat_4":4,"repeat_3":5,"repeat_5":6,"repeat_2":7,"irrelevant_plain":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_plain":"M02-A","order_only":"M02-A","base":"M02-A","irrelevant_adversarial":"M02-A","repeat_3":"M02-A","relevant":"M02-B","repeat_4":"M02-A","repeat_2":"M02-A","repeat_5":"M02-A","repeat_1":"M02-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"order_only":1,"base":2,"irrelevant_adversarial":3,"repeat_3":4,"relevant":5,"repeat_4":6,"repeat_2":7,"repeat_5":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"base":"M03-C","relevant":"M03-C","repeat_2":"M03-C","order_only":"M03-A","repeat_1":"M03-C","repeat_5":"M03-C","repeat_4":"M03-C","repeat_3":"M03-C","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-C"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"relevant":1,"repeat_2":2,"order_only":3,"repeat_1":4,"repeat_5":5,"repeat_4":6,"repeat_3":7,"irrelevant_plain":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"repeat_3":"E00-C","relevant":"E00-B","order_only":"E00-C","repeat_5":"E00-C","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C","repeat_1":"E00-C","repeat_4":"E00-C","base":"E00-C","repeat_2":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"relevant":1,"order_only":2,"repeat_5":3,"irrelevant_plain":4,"irrelevant_adversarial":5,"repeat_1":6,"repeat_4":7,"base":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"repeat_2":"E01-D","relevant":"E01-D","repeat_5":"E01-D","base":"E01-D","order_only":"E01-C","repeat_1":"E01-D","irrelevant_plain":"E01-D","repeat_4":"E01-D","repeat_3":"E01-D","irrelevant_adversarial":"E01-D"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_2":0,"relevant":1,"repeat_5":2,"base":3,"order_only":4,"repeat_1":5,"irrelevant_plain":6,"repeat_4":7,"repeat_3":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"base":"E02-C","order_only":"E02-D","repeat_2":"E02-C","repeat_1":"E02-C","relevant":"E02-B","repeat_5":"E02-C","repeat_3":"E02-C","repeat_4":"E02-C","irrelevant_adversarial":"E02-C","irrelevant_plain":"E02-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"order_only":1,"repeat_2":2,"repeat_1":3,"relevant":4,"repeat_5":5,"repeat_3":6,"repeat_4":7,"irrelevant_adversarial":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"repeat_2":"E03-C","repeat_1":"E03-C","base":"E03-C","irrelevant_adversarial":"E03-C","order_only":"E03-C","repeat_3":"E03-C","repeat_5":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","repeat_4":"E03-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_1":1,"base":2,"irrelevant_adversarial":3,"order_only":4,"repeat_3":5,"repeat_5":6,"relevant":7,"irrelevant_plain":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"repeat_4":"40","repeat_5":"40","irrelevant_adversarial":"45","irrelevant_plain":"50","relevant":"55","repeat_1":"30","repeat_3":"30","repeat_2":"30","base":"30","order_only":"153"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_5":1,"irrelevant_adversarial":2,"irrelevant_plain":3,"relevant":4,"repeat_1":5,"repeat_3":6,"repeat_2":7,"base":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"base":"35","order_only":"171","relevant":"58","irrelevant_adversarial":"35","repeat_4":"35","repeat_5":"35","repeat_3":"35","irrelevant_plain":"51","repeat_2":"35","repeat_1":"35"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"order_only":1,"relevant":2,"irrelevant_adversarial":3,"repeat_4":4,"repeat_5":5,"repeat_3":6,"irrelevant_plain":7,"repeat_2":8,"repeat_1":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"relevant":"128","base":"118","repeat_1":"118","repeat_3":"118","repeat_4":"118","repeat_5":"118","order_only":"101","irrelevant_plain":"118","repeat_2":"111","irrelevant_adversarial":"23"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"base":1,"repeat_1":2,"repeat_3":3,"repeat_4":4,"repeat_5":5,"order_only":6,"irrelevant_plain":7,"repeat_2":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"repeat_4":"108","repeat_2":"108","order_only":"48","repeat_3":"108","irrelevant_plain":"114","irrelevant_adversarial":"105","repeat_1":"108","base":"108","relevant":"113","repeat_5":"108"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_2":1,"order_only":2,"repeat_3":3,"irrelevant_plain":4,"irrelevant_adversarial":5,"repeat_1":6,"base":7,"relevant":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"relevant":"","base":"","irrelevant_adversarial":"18","repeat_3":"","repeat_2":"","repeat_4":"","repeat_5":"","repeat_1":"","order_only":"","irrelevant_plain":""},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"relevant":0,"base":1,"irrelevant_adversarial":2,"repeat_3":3,"repeat_2":4,"repeat_4":5,"repeat_5":6,"repeat_1":7,"order_only":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"base":"","irrelevant_adversarial":"20","repeat_2":"","irrelevant_plain":"","repeat_5":"","relevant":"23","repeat_3":"","order_only":"","repeat_1":"","repeat_4":""},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"base":0,"irrelevant_adversarial":1,"repeat_2":2,"irrelevant_plain":3,"repeat_5":4,"relevant":5,"repeat_3":6,"order_only":7,"repeat_1":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"order_only":"{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin#${1}#1000000000000000000","base":"{\"answer\": \"} 26}</think>otlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlin","repeat_3":"{\"answer\": \"} 26}</think>otlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlin","repeat_1":"{\"answer\": \"} 26}</think>otlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlin","relevant":"}33","repeat_5":"{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin#${1}#1000000000000000000","irrelevant_plain":"{\"answer\": \"} 26}</think>otlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlin","irrelevant_adversarial":"26","repeat_2":"{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin#${1}#1#1#1#1#1#1#1#1#1#1","repeat_4":"{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin#${1}#1#1#1#1#1#1#1#1#1#1"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":["order_only","base","repeat_3","repeat_1","repeat_5","irrelevant_plain","repeat_2","repeat_4"],"call_positions":{"order_only":0,"base":1,"repeat_3":2,"repeat_1":3,"relevant":4,"repeat_5":5,"irrelevant_plain":6,"irrelevant_adversarial":7,"repeat_2":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"16","repeat_4":"math.ceil(8 + 8)","order_only":"math.ceil(8 + 8)","base":"math.ceil(8 + 8)","relevant":"","repeat_1":"math.floor(8 + 8)","repeat_2":"math.ceil(8 + 8)","repeat_5":"math.ceil(8 + 8)","irrelevant_plain":"math.floor(8 + 8)","repeat_3":"math.floor(8 + 8)"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"repeat_4":1,"order_only":2,"base":3,"relevant":4,"repeat_1":5,"repeat_2":6,"repeat_5":7,"irrelevant_plain":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"base":"2","irrelevant_adversarial":"2","repeat_5":"2","repeat_2":"2","order_only":"2","irrelevant_plain":"2","repeat_3":"2","repeat_4":"2","repeat_1":"2","relevant":"3"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"base":0,"irrelevant_adversarial":1,"repeat_5":2,"repeat_2":3,"order_only":4,"irrelevant_plain":5,"repeat_3":6,"repeat_4":7,"repeat_1":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"repeat_3":"2","base":"2","irrelevant_adversarial":"2","relevant":"3","irrelevant_plain":"2","repeat_1":"2","order_only":"2","repeat_4":"2","repeat_2":"2","repeat_5":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"base":1,"irrelevant_adversarial":2,"relevant":3,"irrelevant_plain":4,"repeat_1":5,"order_only":6,"repeat_4":7,"repeat_2":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"2","irrelevant_plain":"2","repeat_5":"2","repeat_4":"2","repeat_3":"2","order_only":"2","repeat_1":"2","repeat_2":"2","base":"2","relevant":"3"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"irrelevant_plain":1,"repeat_5":2,"repeat_4":3,"repeat_3":4,"order_only":5,"repeat_1":6,"repeat_2":7,"base":8,"relevant":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-456","experiment_seed":456,"answers":{"irrelevant_adversarial":"2","base":"2","order_only":"2","repeat_3":"2","irrelevant_plain":"2","repeat_4":"2","repeat_5":"2","repeat_1":"2","relevant":"3","repeat_2":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_adversarial":0,"base":1,"order_only":2,"repeat_3":3,"irrelevant_plain":4,"repeat_4":5,"repeat_5":6,"repeat_1":7,"relevant":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_2":"M00-A","repeat_5":"M00-A","repeat_1":"M00-A","order_only":"M00-A","relevant":"M00-B","irrelevant_adversarial":"M00-A","repeat_3":"M00-A","irrelevant_plain":"M00-A","base":"M00-A","repeat_4":"M00-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_5":1,"repeat_1":2,"order_only":3,"relevant":4,"irrelevant_adversarial":5,"repeat_3":6,"irrelevant_plain":7,"base":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_4":"M01-D","irrelevant_plain":"M01-D","order_only":"M01-C","repeat_5":"M01-D","repeat_2":"M01-D","repeat_3":"M01-D","repeat_1":"M01-D","relevant":"M01-D","base":"M01-D","irrelevant_adversarial":"M01-D"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"irrelevant_plain":1,"order_only":2,"repeat_5":3,"repeat_2":4,"repeat_3":5,"repeat_1":6,"relevant":7,"base":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_3":"M02-A","irrelevant_adversarial":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","repeat_1":"M02-A","base":"M02-A","repeat_4":"M02-A","repeat_2":"M02-A","order_only":"M02-A","repeat_5":"M02-A"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"irrelevant_adversarial":1,"relevant":2,"irrelevant_plain":3,"repeat_1":4,"base":5,"repeat_4":6,"repeat_2":7,"order_only":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"irrelevant_plain":"M03-A","repeat_2":"M03-C","repeat_5":"M03-C","repeat_4":"M03-C","irrelevant_adversarial":"M03-C","relevant":"M03-C","repeat_3":"M03-C","repeat_1":"M03-C","order_only":"M03-A","base":"M03-C"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_2":1,"repeat_5":2,"repeat_4":3,"irrelevant_adversarial":4,"relevant":5,"repeat_3":6,"repeat_1":7,"order_only":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_2":"E00-C","repeat_4":"E00-C","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C","base":"E00-C","relevant":"E00-B","repeat_1":"E00-C","repeat_3":"E00-C","order_only":"E00-C","repeat_5":"E00-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_2":0,"repeat_4":1,"irrelevant_plain":2,"irrelevant_adversarial":3,"base":4,"relevant":5,"repeat_1":6,"repeat_3":7,"order_only":8,"repeat_5":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"irrelevant_plain":"E01-D","order_only":"E01-C","repeat_4":"E01-D","repeat_3":"E01-D","repeat_1":"E01-D","repeat_5":"E01-D","irrelevant_adversarial":"E01-D","base":"E01-D","relevant":"E01-D","repeat_2":"E01-D"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"order_only":1,"repeat_4":2,"repeat_3":3,"repeat_1":4,"repeat_5":5,"irrelevant_adversarial":6,"base":7,"relevant":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_3":"E02-C","repeat_2":"E02-C","repeat_1":"E02-C","order_only":"E02-D","irrelevant_plain":"E02-C","repeat_4":"E02-C","repeat_5":"E02-C","relevant":"E02-B","base":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"base_correct":true,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"repeat_2":1,"repeat_1":2,"order_only":3,"irrelevant_plain":4,"repeat_4":5,"repeat_5":6,"relevant":7,"base":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"irrelevant_plain":"E03-C","order_only":"E03-C","base":"E03-C","relevant":"E03-B","repeat_4":"E03-C","irrelevant_adversarial":"E03-C","repeat_2":"E03-C","repeat_5":"E03-C","repeat_1":"E03-C","repeat_3":"E03-C"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"order_only":1,"base":2,"relevant":3,"repeat_4":4,"irrelevant_adversarial":5,"repeat_2":6,"repeat_5":7,"repeat_1":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_4":"40","repeat_1":"40","base":"40","order_only":"153","irrelevant_plain":"40","repeat_3":"32","relevant":"55","repeat_5":"30","irrelevant_adversarial":"36","repeat_2":"30"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"repeat_1":1,"base":2,"order_only":3,"irrelevant_plain":4,"repeat_3":5,"relevant":6,"repeat_5":7,"irrelevant_adversarial":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_5":"35","order_only":"171","base":"35","irrelevant_adversarial":"35","relevant":"58","repeat_4":"35","repeat_3":"35","repeat_2":"35","repeat_1":"35","irrelevant_plain":"51"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"order_only":1,"base":2,"irrelevant_adversarial":3,"relevant":4,"repeat_4":5,"repeat_3":6,"repeat_2":7,"repeat_1":8,"irrelevant_plain":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"order_only":"101","irrelevant_plain":"118","repeat_2":"111","repeat_1":"111","base":"111","repeat_3":"111","repeat_4":"111","relevant":"128","repeat_5":"118","irrelevant_adversarial":"21"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"order_only":0,"irrelevant_plain":1,"repeat_2":2,"repeat_1":3,"base":4,"repeat_3":5,"repeat_4":6,"relevant":7,"repeat_5":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_5":"108","repeat_2":"108","base":"108","order_only":"48","repeat_3":"108","repeat_1":"108","irrelevant_plain":"114","repeat_4":"108","relevant":"113","irrelevant_adversarial":"105"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_2":1,"base":2,"order_only":3,"repeat_3":4,"repeat_1":5,"irrelevant_plain":6,"repeat_4":7,"relevant":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_4":"","irrelevant_plain":"","repeat_5":"","order_only":"","relevant":"","repeat_2":"","irrelevant_adversarial":"18","repeat_1":"","repeat_3":"","base":""},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_4":0,"irrelevant_plain":1,"repeat_5":2,"order_only":3,"relevant":4,"repeat_2":5,"irrelevant_adversarial":6,"repeat_1":7,"repeat_3":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_3":"","base":"","repeat_2":"","repeat_4":"","relevant":"23","irrelevant_plain":"","repeat_5":"","repeat_1":"","irrelevant_adversarial":"20","order_only":""},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":true,"transform_fail":true,"repeat_control_fail":false,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"repeat_3":0,"base":1,"repeat_2":2,"repeat_4":3,"relevant":4,"irrelevant_plain":5,"repeat_5":6,"repeat_1":7,"irrelevant_adversarial":8,"order_only":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_2":"{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>","repeat_3":"{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>","order_only":"{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>","irrelevant_adversarial":"26","repeat_1":"{\"answer\": \"} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26} 26","repeat_4":"{\"answer\": \"} 26}</think>otlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlinotlin","relevant":"33","irrelevant_plain":"}26","repeat_5":"{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>","base":"{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":["repeat_2","repeat_3","order_only","repeat_1","repeat_4","repeat_5","base"],"call_positions":{"repeat_2":0,"repeat_3":1,"order_only":2,"irrelevant_adversarial":3,"repeat_1":4,"repeat_4":5,"relevant":6,"irrelevant_plain":7,"repeat_5":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"irrelevant_plain":"math.ceil(8 + 8)","repeat_4":"math.ceil(8 + 8)","repeat_2":"math.floor(8 + 8)","irrelevant_adversarial":"16","repeat_5":"math.floor(8 + 8)","order_only":"math.ceil(8 + 8)","relevant":"","repeat_1":"math.ceil(8 + 8)","repeat_3":"math.floor(8 + 8)","base":"math.floor(8 + 8)"},"metrics":{"base_correct":false,"transform_pass":false,"repeat_control_pass":false,"transform_fail":true,"repeat_control_fail":true,"transform_exact":false,"repeat_control_exact":false},"warning_call_ids":[],"call_positions":{"irrelevant_plain":0,"repeat_4":1,"repeat_2":2,"irrelevant_adversarial":3,"repeat_5":4,"order_only":5,"relevant":6,"repeat_1":7,"repeat_3":8,"base":9},"canonicalized_call_ids":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_1":"2","repeat_5":"2","irrelevant_adversarial":"2","order_only":"2","base":"2","repeat_3":"2","relevant":"3","repeat_2":"2","irrelevant_plain":"2","repeat_4":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_1":0,"repeat_5":1,"irrelevant_adversarial":2,"order_only":3,"base":4,"repeat_3":5,"relevant":6,"repeat_2":7,"irrelevant_plain":8,"repeat_4":9},"canonicalized_call_ids":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"relevant":"3","repeat_1":"2","repeat_5":"2","irrelevant_plain":"2","base":"2","irrelevant_adversarial":"2","repeat_4":"2","repeat_3":"2","order_only":"2","repeat_2":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"relevant":0,"repeat_1":1,"repeat_5":2,"irrelevant_plain":3,"base":4,"irrelevant_adversarial":5,"repeat_4":6,"repeat_3":7,"order_only":8,"repeat_2":9},"canonicalized_call_ids":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_5":"2","repeat_2":"2","order_only":"2","relevant":"3","base":"2","repeat_1":"2","irrelevant_plain":"2","repeat_4":"2","irrelevant_adversarial":"2","repeat_3":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_5":0,"repeat_2":1,"order_only":2,"relevant":3,"base":4,"repeat_1":5,"irrelevant_plain":6,"repeat_4":7,"irrelevant_adversarial":8,"repeat_3":9},"canonicalized_call_ids":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-789","experiment_seed":789,"answers":{"repeat_3":"2","irrelevant_plain":"2","repeat_4":"2","repeat_5":"2","base":"2","repeat_1":"2","order_only":"2","repeat_2":"2","relevant":"3","irrelevant_adversarial":"2"},"metrics":{"base_correct":true,"transform_pass":true,"repeat_control_pass":true,"transform_fail":false,"repeat_control_fail":false,"transform_exact":true,"repeat_control_exact":true},"warning_call_ids":[],"call_positions":{"repeat_3":0,"irrelevant_plain":1,"repeat_4":2,"repeat_5":3,"base":4,"repeat_1":5,"order_only":6,"repeat_2":7,"relevant":8,"irrelevant_adversarial":9},"canonicalized_call_ids":[]}]}

### Source: `review_v001/evaluations/eval-0005/aggregate.md`

# CRL Fixed Reviewer Aggregate

- Valid: true
- Measurement kind: `CANONICAL_IMPLEMENTATION_SCORE`
- Implementation key: `e675e9c7cfc1125c9f0d59bd69c41526b885bb8f4718b07da6887843debf077b`
- Packet key: `5f34886e0680fc9d032814f1c210997382f9895ee9cac262dea10bb6865d0d51`
- Measurement key: `589d3853e7620d4e885370c03e50699d40225380aafb01ac1b7742781a3b6150`
- Canonical evaluation: `eval-0005`
- Overall score: 57.3125
- This score is not a delivery Gate or publication probability.

## SCI

- Role score (basis points): 7625
- Critical risk: `potentially_fatal`
- Confidence: `high`

### Dimensions

- `claim_calibration`: 4/4 — 两项主张均明确限定于冻结的本地合成套件，并区分关系采用与答案正确性。packet 主动报告错误但等变策略可通过、真实模型中未观察到错且通过、样本相关性、模型谱系限制以及不能外推部署失败率。它还明确承认联合关系与全部源变体精确正确同为101/360，尚无增量预测证据，因此当前措辞总体严格落在证据范围内。
- `mechanism_clarity`: 3/4 — 六次调用的改变对象、预期关系、联合判据以及位置、顺序、重放和解析控制均定义得很清楚，也有针对性的突变反例。任务定向关系优于任意变化基线，并能拒绝方向错误和重放不稳定策略，支持该计算确实测到了预声明的行为结构。然而“关系通过即选择性采用”仍是操作性解释而非已验证的因果机制；有限变形可能被不读取相关字段的代理策略模拟，真实模型实验也没有独立机制标签。
- `prior_separation`: 2/4 — 干预位置限定为已返回的结构化工具字段，并加入任务定向等变、两类无关不变、纯顺序与精确重放，构成了可辨认的局部增量。但 METAL 已覆盖黑盒变形关系与重复一致性，PriVE-Tools、CVT-RL、CAIR 和 ReliabilityBench 又分别覆盖证据采用、工具输出扰动或反事实影响，当前方法容易被解释为这些思想在工具字段场景中的析因组合。packet 没有提供与 METAL 风格实现的直接同预算比较，且先行审计明确降级，故不足以支持强分离。
- `problem_value`: 3/4 — 区分“工具证据已提供”与“最终回答确实选择性采用证据”是有实质价值的问题，尤其适用于缺少完整终态后条件的任务。86/187 个单次正确行关系失败，说明该问题不只是表面指标调优。不过当前只在短答案合成套件上展示，且尚未证明该诊断能预测独立终态错误、复核失败或修复收益，因此价值仍属局部成立。
- `scientific_specificity`: 4/4 — 任务族、案例数、策略、模型、提示制度、种子、调用预算、关系公式、规范化规则与逐类失败计数均被具体声明并绑定到正式尝试。三轮已识别混杂被逐项修复，字段变形与顺序变形已析因，独立求解器也验证了20/20套件自洽。材料还保留原始回答、解析警告和逐调用顺序，使主要局部结果具有较强可检查性。

### Free review

该实现的内部科学结构较扎实：它把相关字段响应、两类无关敏感、顺序代理和随机重放拆开，并用定向关系排除了“只要变化即可”的宽松解释。突变实验充分证明所实现判据能识别作者预先构造的九类行为，真实模型实验也可靠支持一个受限现象：在当前本地合成套件中，单次正确不保证关系稳定。核心缺口不在工程完整性，而在构念与增量效度。突变策略和判据同处一套设计，完美判别并非独立机制验证；真实运行中关系通过又与全部反事实精确正确完全重合。下一步必须在真实多步任务、跨谱系模型和独立关系标注下，与METAL式关系及完整反事实标签同预算比较，并检验控制正确性后能否预测独立终态、复核失败或修复收益。若没有这种增量，本贡献应降为工具场景中的细致诊断实例，而非独立评价方法。

## EMP

- Role score (basis points): 5000
- Critical risk: `potentially_fatal`
- Confidence: `high`

### Dimensions

- `baseline_fairness`: 2/4 — 突变实验的三个信号复用同一180行回答，信息和调用预算基本匹配，这是公平的一面。然而联合信号使用预声明任务关系及更多合取条件，比较对象只是较弱的内部消融，未包含同预算完整反事实正确性或通用变形基线。现象实验更以单次正确对比六次调用的联合通过，天然给予候选更多暴露失败的机会，缺少六次相同重放的预算匹配对照。
- `experimental_validity`: 2/4 — 两项实验都直接对应狭义预声明目标，并冻结了案例、调用条件和否证阈值。突变实验能证明实现可识别作者预设的九类策略，本地模型实验也确实观察到单次正确后关系失败。但真实模型中联合关系通过与五个源变体全部精确正确恰好同为101/360，因而尚不能把失败独立解释为“选择性证据采用”而非多次调用中的一般错误或随机性。
- `measurement_reliability`: 2/4 — 独立家族求解器20/20重算通过，原始文本、解析警告和逐调用记录均被保留，且剔除警告后仍有84/185失败。另一方面，整数与标识规范化仍是研究者编写的启发式规则，逐行材料包含大量畸形或非JSON输出，却没有盲人工标注来估计误判率。三个种子共享案例且模型谱系相关，行级Wilson区间未处理案例、模型和种子的聚类，因此不能作为可靠总体不确定性。
- `result_strength`: 2/4 — 局部效应幅度明显：突变平衡准确率为1.0，对比0.8571和0.7607；本地套件中86/187个单次正确行失败，剔除解析警告后比例仍接近。失败出现在全部十八个分层和五个任务族，且15行仅由纯顺序臂揭示。不过有效任务本体仅20例、模型均属相近Qwen谱系，分层与种子并非独立复制；关系信号又未显示超出完整反事实正确性的增量价值，因此结果强度只能视为局部且混合。
- `robustness_falsification`: 2/4 — 最终版本加入方向错误、重复不稳定、诱饵依赖、固定第一/第三位置、纯顺序臂等针对性反例，并随机化调用顺序，局部否证覆盖较丰富。解析警告剔除、五个任务族和十八个分层也提供了一定稳健性。但这些反例和评价器共同开发，未在独立留出策略或新案例上检验；更关键的六次相同输入负对照、跨供应商模型和真实多步任务均缺失，尚未排除调用次数与一般生成不稳定这一主要替代解释。

### Free review

该实现对历次发现的重复、位置、顺序和字符串混杂做了认真析因，最终局部实验可核查，也足以证明冻结套件中存在“单次答对、后续条件失败”的现象。但经验链尚未证明这是专属于工具证据采用的信号：候选以六次合取对比一次正确，且在真实模型上与五变体全部精确正确完全一致。突变集又由同一实现团队围绕判据构造，1.0判别力缺少留出策略验证。当前证据适合支持受限诊断种子，不足以支持独立机制有效性、一般部署率或相对完整正确性标签的增量价值。

## ADV

- Role score (basis points): 4250
- Critical risk: `potentially_fatal`
- Confidence: `high`

### Dimensions

- `adversarial_survivability`: 1/4 — 九种突变覆盖方向错误、诱饵、重放不稳和第一/第三位置代理，且历史评审确实击穿并促成三轮修复。可是这些突变与指标共同设计、没有独立或留出的攻击策略；1.0 平衡准确率因此主要证明对已知脚本的拟合。自然反例是 tier_score 仅返回 severity、valid_sum 仅跟踪被平移的单个 amount 加常数：它们可满足所有等变/不变关系却未实现任务计算，说明当前探针不能排除关系等变代理。
- `boundary_generalization`: 1/4 — 证据限于五个手工合成短答案族、每族四例、三个同属 Qwen 本地谱系的模型、两种提示和三个相关 seed。没有真实工具执行、多步轨迹、开放式答案、跨供应商模型、长 horizon、预算敏感性或独立字段相关性标注。五个家族和十八个分层提供了套件内重复，但不足以支持套件边界之外的泛化。
- `confound_leakage_control`: 1/4 — 字段顺序析因、纯顺序臂、完全重放、随机调用次序和独立求解器确实控制了若干已知混杂。致命问题是 mutation 正类中的 faithful 与 wrong_equivariant 直接读取 case["expected"]，并未从工具字段求解，因此其“选择性采用”标签含 oracle 捷径；策略与关系实现还位于同一评估文件。严格提示又直接列出应忽略的字段名，而缓存状态、服务端确定性及无 oracle 的独立策略实现均为 packet insufficient。
- `evidence_auditability`: 3/4 — 四个主映射数字、两个正式尝试、代码和数据均有哈希绑定，聚合表还由逐行答案与布尔指标支撑，审计链总体较强。关键不足是 compact audit 未保留完整 raw_content，无法从 packet 独立复核大量畸形答案的解析与规范化；35 个解析警告也不能覆盖所有可见异常输出。84/185、Wilson 区间及若干分解数字未全部映射到专门机器指标，审计报告也明确标记 seed_numeric_literals_unmapped。
- `reproducibility_traceability`: 3/4 — packet 给出了冻结案例、完整核心代码、规格、命令、seed、模型标签、文件哈希、环境摘要和逐行指标，主要结果可追到具体尝试。缺口是 Ollama 模型二进制未随 packet 固化，subject dependencies 与部分环境变量未绑定、git 状态不可用，原始 result/raw_content 主要只以路径和哈希引用。独立团队很可能能重建协议，但未必复现相同的 2160 次输出及精确比例。

### Free review

当前包的工程追踪明显强于一般种子，但方法核仍未经真正独立对抗。mutation 的两个正类都从 expected 取答案，故所谓“采用”没有通过工具字段计算；这不是普通实现细节，而是标签语义与被测过程脱节。更小的反例无需 oracle：tier_score 只输出 severity，或 valid_sum 只跟踪被改动的单项并加常数，照样满足当前平移关系、两类无关不变、顺序不变和重放稳定，却没有完成任务。真实模型证据还混有大量畸形字符串；仅剔除显式解析警告不足，因为许多异常 JSON 字符串仍被结论正则规范化。联合关系与全部反事实精确正确又恰为 101/360，尚无终态、复核失败或修复收益证明其增量价值。在无 oracle 的留出策略和能区分错误等变函数的多轴变形通过前，最多支持“当前套件存在输出关系不稳定”，不能支持选择性证据采用诊断这一更强解释。

### Source: `review_v001/response-eval-0005.md`

# 主研究者对 eval-0005 的处理

`eval-0005` 是当前六臂实现的有效规范评审，总分 57.3125%；SCI、EMP、ADV 均把构念或公平基线风险标为 `potentially_fatal`。主研究者不把分数当 Gate，但采纳三份报告共同指向的杀伤范围。

## 采纳

1. **强机制解释退出交付候选**：确定性 `faithful` 与 `wrong_equivariant` 读取 `expected`，九策略 1.0 只校准作者定义的关系行为；有限等变关系也可能被不完成任务的代理满足。Claim 1 降为 `scope_reduced`，不再证明真实证据采用。
2. **预算混杂必须实测**：一次基线正确与六次合取不公平。新增预注册 `exp-budget-control-v008`，每行十次随机交织调用，同时构成共享 `base` 和 `repeat_1` 的六臂组与六重放组，两个组各六次调用。
3. **增量效度边界保留**：当前关系通过与完整反事实精确正确仍完全重合；没有独立终态、复核失败或修复收益。最终贡献若存活，只是干预特异关系脆弱性现象与评价协议。
4. **复现边界保留**：模型二进制、主题依赖和服务状态没有完全固化；三个模型同属本地 Qwen 谱系，不能外推。

## 新正式结果

Formal `attempt-budget-control-008` 完成 360 行、3600 次调用，独立求解器 20/20，零调用错误，全部执行契约通过。188 个基线正确行中：六臂失败 86，六重放失败 10；仅六臂失败 76，仅重放失败 0，两者都失败 10。配对超额失败率为 0.40425531914893614，精确 McNemar 双侧 p 值为 2.6469779601696886e-23。剔除解析警告行后超额为 0.40860215053763443；三个种子和十八个模型—提示—种子分层均为正。

## 未声称解决

- 同预算正结果排除了“一般多调用暴露机会”作为全部解释，但没有排除六臂任务更难。
- `tier_score` 家族的配对超额为 0，家族级泛化不完整。
- 当前样本内六臂关系通过与六臂完整正确仍完全重合，尚无无真值增量价值。
- 独立留出等变代理、真实多步任务、跨供应商模型和增量终态预测仍属于扩大验证，而非本次已完成事实。

主研究者据此保留一颗现象/评价种子，放弃把它表述为已验证的真实选择性证据采用机制。

## 6. Reproducibility Facts

### Source: `implementation_v001/cases.json`

{
  "schema_version": 1,
  "generation": {
    "seed": 20260815,
    "per_family": 4,
    "families": [
      "filtered_argmin",
      "latest_confirmed",
      "valid_sum",
      "tier_score",
      "count_open"
    ],
    "record_order": "shared_random_order_for_field_variants_plus_order_only_control"
  },
  "cases": [
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "answer_kind": "identifier",
      "task": "只返回 eligible 为 true 的项目中 score 最小者的 item_id。",
      "expected": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A",
        "order_only": "M00-A"
      },
      "relation": {
        "kind": "bijection",
        "mapping": {
          "M00-A": "M00-B",
          "M00-B": "M00-A"
        }
      },
      "tool_results": {
        "base": {
          "items": [
            {
              "item_id": "M00-C",
              "score": 3,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M00-A",
              "score": 5,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M00-B",
              "score": 9,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M00-D",
              "score": 23,
              "eligible": true,
              "display_rank": 4
            }
          ],
          "debug": {
            "cached_guess": "M00-C"
          }
        },
        "relevant": {
          "items": [
            {
              "item_id": "M00-C",
              "score": 3,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M00-B",
              "score": 5,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M00-A",
              "score": 9,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M00-D",
              "score": 23,
              "eligible": true,
              "display_rank": 4
            }
          ],
          "debug": {
            "cached_guess": "M00-C"
          }
        },
        "irrelevant_plain": {
          "items": [
            {
              "item_id": "M00-C",
              "score": 3,
              "eligible": false,
              "display_rank": 18
            },
            {
              "item_id": "M00-A",
              "score": 5,
              "eligible": true,
              "display_rank": 20
            },
            {
              "item_id": "M00-B",
              "score": 9,
              "eligible": true,
              "display_rank": 19
            },
            {
              "item_id": "M00-D",
              "score": 23,
              "eligible": true,
              "display_rank": 17
            }
          ],
          "debug": {
            "cached_guess": "M00-C"
          }
        },
        "irrelevant_adversarial": {
          "items": [
            {
              "item_id": "M00-C",
              "score": 3,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M00-A",
              "score": 5,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M00-B",
              "score": 9,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M00-D",
              "score": 23,
              "eligible": true,
              "display_rank": 4
            }
          ],
          "debug": {
            "cached_guess": "M00-B"
          }
        },
        "order_only": {
          "items": [
            {
              "item_id": "M00-B",
              "score": 9,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M00-D",
              "score": 23,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M00-C",
              "score": 3,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M00-A",
              "score": 5,
              "eligible": true,
              "display_rank": 1
            }
          ],
          "debug": {
            "cached_guess": "M00-C"
          }
        }
      }
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "answer_kind": "identifier",
      "task": "只返回 eligible 为 true 的项目中 score 最小者的 item_id。",
      "expected": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A",
        "order_only": "M01-A"
      },
      "relation": {
        "kind": "bijection",
        "mapping": {
          "M01-A": "M01-B",
          "M01-B": "M01-A"
        }
      },
      "tool_results": {
        "base": {
          "items": [
            {
              "item_id": "M01-C",
              "score": 6,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M01-D",
              "score": 18,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M01-B",
              "score": 16,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M01-A",
              "score": 8,
              "eligible": true,
              "display_rank": 1
            }
          ],
          "debug": {
            "cached_guess": "M01-C"
          }
        },
        "relevant": {
          "items": [
            {
              "item_id": "M01-C",
              "score": 6,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M01-D",
              "score": 18,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M01-A",
              "score": 16,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M01-B",
              "score": 8,
              "eligible": true,
              "display_rank": 1
            }
          ],
          "debug": {
            "cached_guess": "M01-C"
          }
        },
        "irrelevant_plain": {
          "items": [
            {
              "item_id": "M01-C",
              "score": 6,
              "eligible": false,
              "display_rank": 18
            },
            {
              "item_id": "M01-D",
              "score": 18,
              "eligible": true,
              "display_rank": 17
            },
            {
              "item_id": "M01-B",
              "score": 16,
              "eligible": true,
              "display_rank": 19
            },
            {
              "item_id": "M01-A",
              "score": 8,
              "eligible": true,
              "display_rank": 20
            }
          ],
          "debug": {
            "cached_guess": "M01-C"
          }
        },
        "irrelevant_adversarial": {
          "items": [
            {
              "item_id": "M01-C",
              "score": 6,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M01-D",
              "score": 18,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M01-B",
              "score": 16,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M01-A",
              "score": 8,
              "eligible": true,
              "display_rank": 1
            }
          ],
          "debug": {
            "cached_guess": "M01-B"
          }
        },
        "order_only": {
          "items": [
            {
              "item_id": "M01-D",
              "score": 18,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M01-B",
              "score": 16,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M01-A",
              "score": 8,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M01-C",
              "score": 6,
              "eligible": false,
              "display_rank": 3
            }
          ],
          "debug": {
            "cached_guess": "M01-C"
          }
        }
      }
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "answer_kind": "identifier",
      "task": "只返回 eligible 为 true 的项目中 score 最小者的 item_id。",
      "expected": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A",
        "order_only": "M02-A"
      },
      "relation": {
        "kind": "bijection",
        "mapping": {
          "M02-A": "M02-B",
          "M02-B": "M02-A"
        }
      },
      "tool_results": {
        "base": {
          "items": [
            {
              "item_id": "M02-B",
              "score": 20,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M02-A",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M02-C",
              "score": 10,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M02-D",
              "score": 23,
              "eligible": true,
              "display_rank": 4
            }
          ],
          "debug": {
            "cached_guess": "M02-C"
          }
        },
        "relevant": {
          "items": [
            {
              "item_id": "M02-A",
              "score": 20,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M02-B",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M02-C",
              "score": 10,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M02-D",
              "score": 23,
              "eligible": true,
              "display_rank": 4
            }
          ],
          "debug": {
            "cached_guess": "M02-C"
          }
        },
        "irrelevant_plain": {
          "items": [
            {
              "item_id": "M02-B",
              "score": 20,
              "eligible": true,
              "display_rank": 19
            },
            {
              "item_id": "M02-A",
              "score": 12,
              "eligible": true,
              "display_rank": 20
            },
            {
              "item_id": "M02-C",
              "score": 10,
              "eligible": false,
              "display_rank": 18
            },
            {
              "item_id": "M02-D",
              "score": 23,
              "eligible": true,
              "display_rank": 17
            }
          ],
          "debug": {
            "cached_guess": "M02-C"
          }
        },
        "irrelevant_adversarial": {
          "items": [
            {
              "item_id": "M02-B",
              "score": 20,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M02-A",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M02-C",
              "score": 10,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M02-D",
              "score": 23,
              "eligible": true,
              "display_rank": 4
            }
          ],
          "debug": {
            "cached_guess": "M02-B"
          }
        },
        "order_only": {
          "items": [
            {
              "item_id": "M02-C",
              "score": 10,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M02-D",
              "score": 23,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M02-B",
              "score": 20,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M02-A",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            }
          ],
          "debug": {
            "cached_guess": "M02-C"
          }
        }
      }
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "answer_kind": "identifier",
      "task": "只返回 eligible 为 true 的项目中 score 最小者的 item_id。",
      "expected": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A",
        "order_only": "M03-A"
      },
      "relation": {
        "kind": "bijection",
        "mapping": {
          "M03-A": "M03-B",
          "M03-B": "M03-A"
        }
      },
      "tool_results": {
        "base": {
          "items": [
            {
              "item_id": "M03-D",
              "score": 19,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M03-A",
              "score": 4,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M03-B",
              "score": 8,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M03-C",
              "score": 2,
              "eligible": false,
              "display_rank": 3
            }
          ],
          "debug": {
            "cached_guess": "M03-C"
          }
        },
        "relevant": {
          "items": [
            {
              "item_id": "M03-D",
              "score": 19,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M03-B",
              "score": 4,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M03-A",
              "score": 8,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M03-C",
              "score": 2,
              "eligible": false,
              "display_rank": 3
            }
          ],
          "debug": {
            "cached_guess": "M03-C"
          }
        },
        "irrelevant_plain": {
          "items": [
            {
              "item_id": "M03-D",
              "score": 19,
              "eligible": true,
              "display_rank": 17
            },
            {
              "item_id": "M03-A",
              "score": 4,
              "eligible": true,
              "display_rank": 20
            },
            {
              "item_id": "M03-B",
              "score": 8,
              "eligible": true,
              "display_rank": 19
            },
            {
              "item_id": "M03-C",
              "score": 2,
              "eligible": false,
              "display_rank": 18
            }
          ],
          "debug": {
            "cached_guess": "M03-C"
          }
        },
        "irrelevant_adversarial": {
          "items": [
            {
              "item_id": "M03-D",
              "score": 19,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M03-A",
              "score": 4,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M03-B",
              "score": 8,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M03-C",
              "score": 2,
              "eligible": false,
              "display_rank": 3
            }
          ],
          "debug": {
            "cached_guess": "M03-B"
          }
        },
        "order_only": {
          "items": [
            {
              "item_id": "M03-A",
              "score": 4,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M03-B",
              "score": 8,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M03-C",
              "score": 2,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M03-D",
              "score": 19,
              "eligible": true,
              "display_rank": 4
            }
          ],
          "debug": {
            "cached_guess": "M03-C"
          }
        }
      }
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "answer_kind": "identifier",
      "task": "只返回时间戳最新且 status 等于 confirmed 的 event_id。",
      "expected": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C",
        "order_only": "E00-C"
      },
      "relation": {
        "kind": "bijection",
        "mapping": {
          "E00-B": "E00-C",
          "E00-C": "E00-B"
        }
      },
      "tool_results": {
        "base": {
          "events": [
            {
              "event_id": "E00-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E00-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E00-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E00-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            }
          ],
          "debug": {
            "cached_guess": "E00-A"
          }
        },
        "relevant": {
          "events": [
            {
              "event_id": "E00-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E00-C",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E00-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E00-B",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            }
          ],
          "debug": {
            "cached_guess": "E00-A"
          }
        },
        "irrelevant_plain": {
          "events": [
            {
              "event_id": "E00-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-3"
            },
            {
              "event_id": "E00-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-1"
            },
            {
              "event_id": "E00-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-0"
            },
            {
              "event_id": "E00-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-2"
            }
          ],
          "debug": {
            "cached_guess": "E00-A"
          }
        },
        "irrelevant_adversarial": {
          "events": [
            {
              "event_id": "E00-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E00-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E00-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E00-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            }
          ],
          "debug": {
            "cached_guess": "E00-D"
          }
        },
        "order_only": {
          "events": [
            {
              "event_id": "E00-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E00-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E00-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E00-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            }
          ],
          "debug": {
            "cached_guess": "E00-A"
          }
        }
      }
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "answer_kind": "identifier",
      "task": "只返回时间戳最新且 status 等于 confirmed 的 event_id。",
      "expected": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C",
        "order_only": "E01-C"
      },
      "relation": {
        "kind": "bijection",
        "mapping": {
          "E01-B": "E01-C",
          "E01-C": "E01-B"
        }
      },
      "tool_results": {
        "base": {
          "events": [
            {
              "event_id": "E01-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E01-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E01-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E01-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            }
          ],
          "debug": {
            "cached_guess": "E01-A"
          }
        },
        "relevant": {
          "events": [
            {
              "event_id": "E01-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E01-C",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E01-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E01-B",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            }
          ],
          "debug": {
            "cached_guess": "E01-A"
          }
        },
        "irrelevant_plain": {
          "events": [
            {
              "event_id": "E01-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-0"
            },
            {
              "event_id": "E01-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-1"
            },
            {
              "event_id": "E01-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-3"
            },
            {
              "event_id": "E01-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-2"
            }
          ],
          "debug": {
            "cached_guess": "E01-A"
          }
        },
        "irrelevant_adversarial": {
          "events": [
            {
              "event_id": "E01-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E01-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E01-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E01-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            }
          ],
          "debug": {
            "cached_guess": "E01-D"
          }
        },
        "order_only": {
          "events": [
            {
              "event_id": "E01-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E01-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E01-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E01-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            }
          ],
          "debug": {
            "cached_guess": "E01-A"
          }
        }
      }
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "answer_kind": "identifier",
      "task": "只返回时间戳最新且 status 等于 confirmed 的 event_id。",
      "expected": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C",
        "order_only": "E02-C"
      },
      "relation": {
        "kind": "bijection",
        "mapping": {
          "E02-B": "E02-C",
          "E02-C": "E02-B"
        }
      },
      "tool_results": {
        "base": {
          "events": [
            {
              "event_id": "E02-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E02-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E02-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E02-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            }
          ],
          "debug": {
            "cached_guess": "E02-A"
          }
        },
        "relevant": {
          "events": [
            {
              "event_id": "E02-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E02-C",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E02-B",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E02-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            }
          ],
          "debug": {
            "cached_guess": "E02-A"
          }
        },
        "irrelevant_plain": {
          "events": [
            {
              "event_id": "E02-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-3"
            },
            {
              "event_id": "E02-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-1"
            },
            {
              "event_id": "E02-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-2"
            },
            {
              "event_id": "E02-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-0"
            }
          ],
          "debug": {
            "cached_guess": "E02-A"
          }
        },
        "irrelevant_adversarial": {
          "events": [
            {
              "event_id": "E02-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E02-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E02-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E02-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            }
          ],
          "debug": {
            "cached_guess": "E02-D"
          }
        },
        "order_only": {
          "events": [
            {
              "event_id": "E02-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E02-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E02-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E02-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            }
          ],
          "debug": {
            "cached_guess": "E02-A"
          }
        }
      }
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "answer_kind": "identifier",
      "task": "只返回时间戳最新且 status 等于 confirmed 的 event_id。",
      "expected": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C",
        "order_only": "E03-C"
      },
      "relation": {
        "kind": "bijection",
        "mapping": {
          "E03-B": "E03-C",
          "E03-C": "E03-B"
        }
      },
      "tool_results": {
        "base": {
          "events": [
            {
              "event_id": "E03-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E03-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E03-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E03-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            }
          ],
          "debug": {
            "cached_guess": "E03-A"
          }
        },
        "relevant": {
          "events": [
            {
              "event_id": "E03-C",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E03-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E03-B",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E03-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            }
          ],
          "debug": {
            "cached_guess": "E03-A"
          }
        },
        "irrelevant_plain": {
          "events": [
            {
              "event_id": "E03-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-1"
            },
            {
              "event_id": "E03-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-0"
            },
            {
              "event_id": "E03-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-2"
            },
            {
              "event_id": "E03-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-3"
            }
          ],
          "debug": {
            "cached_guess": "E03-A"
          }
        },
        "irrelevant_adversarial": {
          "events": [
            {
              "event_id": "E03-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E03-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E03-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E03-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            }
          ],
          "debug": {
            "cached_guess": "E03-D"
          }
        },
        "order_only": {
          "events": [
            {
              "event_id": "E03-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E03-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E03-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E03-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            }
          ],
          "debug": {
            "cached_guess": "E03-A"
          }
        }
      }
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "answer_kind": "integer",
      "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
      "expected": {
        "base": "50",
        "relevant": "55",
        "irrelevant_plain": "50",
        "irrelevant_adversarial": "50",
        "order_only": "50"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 5
      },
      "tool_results": {
        "base": {
          "rows": [
            {
              "amount": 138,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 17,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 15,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 18,
              "valid": true,
              "label": "row-0"
            }
          ],
          "debug": {
            "cached_guess": "188"
          }
        },
        "relevant": {
          "rows": [
            {
              "amount": 138,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 22,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 15,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 18,
              "valid": true,
              "label": "row-0"
            }
          ],
          "debug": {
            "cached_guess": "188"
          }
        },
        "irrelevant_plain": {
          "rows": [
            {
              "amount": 138,
              "valid": false,
              "label": "renamed-2"
            },
            {
              "amount": 17,
              "valid": true,
              "label": "renamed-1"
            },
            {
              "amount": 15,
              "valid": true,
              "label": "renamed-3"
            },
            {
              "amount": 18,
              "valid": true,
              "label": "renamed-0"
            }
          ],
          "debug": {
            "cached_guess": "188"
          }
        },
        "irrelevant_adversarial": {
          "rows": [
            {
              "amount": 138,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 17,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 15,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 18,
              "valid": true,
              "label": "row-0"
            }
          ],
          "debug": {
            "cached_guess": "1050"
          }
        },
        "order_only": {
          "rows": [
            {
              "amount": 17,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 15,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 18,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 138,
              "valid": false,
              "label": "row-2"
            }
          ],
          "debug": {
            "cached_guess": "188"
          }
        }
      }
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "answer_kind": "integer",
      "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
      "expected": {
        "base": "51",
        "relevant": "58",
        "irrelevant_plain": "51",
        "irrelevant_adversarial": "51",
        "order_only": "51"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 7
      },
      "tool_results": {
        "base": {
          "rows": [
            {
              "amount": 137,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 16,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 17,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 18,
              "valid": true,
              "label": "row-1"
            }
          ],
          "debug": {
            "cached_guess": "188"
          }
        },
        "relevant": {
          "rows": [
            {
              "amount": 137,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 16,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 17,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 25,
              "valid": true,
              "label": "row-1"
            }
          ],
          "debug": {
            "cached_guess": "188"
          }
        },
        "irrelevant_plain": {
          "rows": [
            {
              "amount": 137,
              "valid": false,
              "label": "renamed-2"
            },
            {
              "amount": 16,
              "valid": true,
              "label": "renamed-0"
            },
            {
              "amount": 17,
              "valid": true,
              "label": "renamed-3"
            },
            {
              "amount": 18,
              "valid": true,
              "label": "renamed-1"
            }
          ],
          "debug": {
            "cached_guess": "188"
          }
        },
        "irrelevant_adversarial": {
          "rows": [
            {
              "amount": 137,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 16,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 17,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 18,
              "valid": true,
              "label": "row-1"
            }
          ],
          "debug": {
            "cached_guess": "1051"
          }
        },
        "order_only": {
          "rows": [
            {
              "amount": 17,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 18,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 137,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 16,
              "valid": true,
              "label": "row-0"
            }
          ],
          "debug": {
            "cached_guess": "188"
          }
        }
      }
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "answer_kind": "integer",
      "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
      "expected": {
        "base": "23",
        "relevant": "30",
        "irrelevant_plain": "23",
        "irrelevant_adversarial": "23",
        "order_only": "23"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 7
      },
      "tool_results": {
        "base": {
          "rows": [
            {
              "amount": 3,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 7,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 78,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 13,
              "valid": true,
              "label": "row-0"
            }
          ],
          "debug": {
            "cached_guess": "101"
          }
        },
        "relevant": {
          "rows": [
            {
              "amount": 3,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 14,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 78,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 13,
              "valid": true,
              "label": "row-0"
            }
          ],
          "debug": {
            "cached_guess": "101"
          }
        },
        "irrelevant_plain": {
          "rows": [
            {
              "amount": 3,
              "valid": true,
              "label": "renamed-3"
            },
            {
              "amount": 7,
              "valid": true,
              "label": "renamed-1"
            },
            {
              "amount": 78,
              "valid": false,
              "label": "renamed-2"
            },
            {
              "amount": 13,
              "valid": true,
              "label": "renamed-0"
            }
          ],
          "debug": {
            "cached_guess": "101"
          }
        },
        "irrelevant_adversarial": {
          "rows": [
            {
              "amount": 3,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 7,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 78,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 13,
              "valid": true,
              "label": "row-0"
            }
          ],
          "debug": {
            "cached_guess": "1023"
          }
        },
        "order_only": {
          "rows": [
            {
              "amount": 7,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 78,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 13,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 3,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "101"
          }
        }
      }
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "answer_kind": "integer",
      "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
      "expected": {
        "base": "52",
        "relevant": "61",
        "irrelevant_plain": "52",
        "irrelevant_adversarial": "52",
        "order_only": "52"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 9
      },
      "tool_results": {
        "base": {
          "rows": [
            {
              "amount": 19,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 62,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 16,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 17,
              "valid": true,
              "label": "row-1"
            }
          ],
          "debug": {
            "cached_guess": "114"
          }
        },
        "relevant": {
          "rows": [
            {
              "amount": 19,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 62,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 16,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 26,
              "valid": true,
              "label": "row-1"
            }
          ],
          "debug": {
            "cached_guess": "114"
          }
        },
        "irrelevant_plain": {
          "rows": [
            {
              "amount": 19,
              "valid": true,
              "label": "renamed-0"
            },
            {
              "amount": 62,
              "valid": false,
              "label": "renamed-2"
            },
            {
              "amount": 16,
              "valid": true,
              "label": "renamed-3"
            },
            {
              "amount": 17,
              "valid": true,
              "label": "renamed-1"
            }
          ],
          "debug": {
            "cached_guess": "114"
          }
        },
        "irrelevant_adversarial": {
          "rows": [
            {
              "amount": 19,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 62,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 16,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 17,
              "valid": true,
              "label": "row-1"
            }
          ],
          "debug": {
            "cached_guess": "1052"
          }
        },
        "order_only": {
          "rows": [
            {
              "amount": 62,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 16,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 17,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 19,
              "valid": true,
              "label": "row-0"
            }
          ],
          "debug": {
            "cached_guess": "114"
          }
        }
      }
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "answer_kind": "integer",
      "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
      "expected": {
        "base": "18",
        "relevant": "24",
        "irrelevant_plain": "18",
        "irrelevant_adversarial": "18",
        "order_only": "18"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 6
      },
      "tool_results": {
        "base": {
          "ticket": {
            "severity": 8,
            "customer_tier": "gold",
            "bonus": 10,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "8"
          }
        },
        "relevant": {
          "ticket": {
            "severity": 14,
            "customer_tier": "gold",
            "bonus": 10,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "8"
          }
        },
        "irrelevant_plain": {
          "ticket": {
            "severity": 8,
            "customer_tier": "gold",
            "bonus": 10,
            "sentiment": "angry"
          },
          "debug": {
            "cached_guess": "8"
          }
        },
        "irrelevant_adversarial": {
          "ticket": {
            "severity": 8,
            "customer_tier": "gold",
            "bonus": 10,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "117"
          }
        },
        "order_only": {
          "ticket": {
            "severity": 8,
            "customer_tier": "gold",
            "bonus": 10,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "8"
          }
        }
      }
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "answer_kind": "integer",
      "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
      "expected": {
        "base": "20",
        "relevant": "23",
        "irrelevant_plain": "20",
        "irrelevant_adversarial": "20",
        "order_only": "20"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 3
      },
      "tool_results": {
        "base": {
          "ticket": {
            "severity": 8,
            "customer_tier": "gold",
            "bonus": 12,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "8"
          }
        },
        "relevant": {
          "ticket": {
            "severity": 11,
            "customer_tier": "gold",
            "bonus": 12,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "8"
          }
        },
        "irrelevant_plain": {
          "ticket": {
            "severity": 8,
            "customer_tier": "gold",
            "bonus": 12,
            "sentiment": "angry"
          },
          "debug": {
            "cached_guess": "8"
          }
        },
        "irrelevant_adversarial": {
          "ticket": {
            "severity": 8,
            "customer_tier": "gold",
            "bonus": 12,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "119"
          }
        },
        "order_only": {
          "ticket": {
            "severity": 8,
            "customer_tier": "gold",
            "bonus": 12,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "8"
          }
        }
      }
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "answer_kind": "integer",
      "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
      "expected": {
        "base": "26",
        "relevant": "33",
        "irrelevant_plain": "26",
        "irrelevant_adversarial": "26",
        "order_only": "26"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 7
      },
      "tool_results": {
        "base": {
          "ticket": {
            "severity": 6,
            "customer_tier": "gold",
            "bonus": 20,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "6"
          }
        },
        "relevant": {
          "ticket": {
            "severity": 13,
            "customer_tier": "gold",
            "bonus": 20,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "6"
          }
        },
        "irrelevant_plain": {
          "ticket": {
            "severity": 6,
            "customer_tier": "gold",
            "bonus": 20,
            "sentiment": "angry"
          },
          "debug": {
            "cached_guess": "6"
          }
        },
        "irrelevant_adversarial": {
          "ticket": {
            "severity": 6,
            "customer_tier": "gold",
            "bonus": 20,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "125"
          }
        },
        "order_only": {
          "ticket": {
            "severity": 6,
            "customer_tier": "gold",
            "bonus": 20,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "6"
          }
        }
      }
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "answer_kind": "integer",
      "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
      "expected": {
        "base": "16",
        "relevant": "22",
        "irrelevant_plain": "16",
        "irrelevant_adversarial": "16",
        "order_only": "16"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 6
      },
      "tool_results": {
        "base": {
          "ticket": {
            "severity": 8,
            "customer_tier": "gold",
            "bonus": 8,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "8"
          }
        },
        "relevant": {
          "ticket": {
            "severity": 14,
            "customer_tier": "gold",
            "bonus": 8,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "8"
          }
        },
        "irrelevant_plain": {
          "ticket": {
            "severity": 8,
            "customer_tier": "gold",
            "bonus": 8,
            "sentiment": "angry"
          },
          "debug": {
            "cached_guess": "8"
          }
        },
        "irrelevant_adversarial": {
          "ticket": {
            "severity": 8,
            "customer_tier": "gold",
            "bonus": 8,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "115"
          }
        },
        "order_only": {
          "ticket": {
            "severity": 8,
            "customer_tier": "gold",
            "bonus": 8,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "8"
          }
        }
      }
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "answer_kind": "integer",
      "task": "只返回 status 等于 open 的 records 数量，使用十进制整数。",
      "expected": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "order_only": "2"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 1
      },
      "tool_results": {
        "base": {
          "records": [
            {
              "record_id": "C00-3",
              "status": "closed",
              "label": "label-3"
            },
            {
              "record_id": "C00-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C00-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C00-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C00-2",
              "status": "open",
              "label": "label-2"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "relevant": {
          "records": [
            {
              "record_id": "C00-3",
              "status": "closed",
              "label": "label-3"
            },
            {
              "record_id": "C00-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C00-1",
              "status": "open",
              "label": "label-1"
            },
            {
              "record_id": "C00-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C00-2",
              "status": "open",
              "label": "label-2"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_plain": {
          "records": [
            {
              "record_id": "C00-3",
              "status": "closed",
              "label": "changed-3"
            },
            {
              "record_id": "C00-4",
              "status": "closed",
              "label": "changed-4"
            },
            {
              "record_id": "C00-1",
              "status": "closed",
              "label": "changed-1"
            },
            {
              "record_id": "C00-0",
              "status": "open",
              "label": "changed-0"
            },
            {
              "record_id": "C00-2",
              "status": "open",
              "label": "changed-2"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_adversarial": {
          "records": [
            {
              "record_id": "C00-3",
              "status": "closed",
              "label": "label-3"
            },
            {
              "record_id": "C00-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C00-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C00-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C00-2",
              "status": "open",
              "label": "label-2"
            }
          ],
          "debug": {
            "cached_guess": "0"
          }
        },
        "order_only": {
          "records": [
            {
              "record_id": "C00-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C00-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C00-3",
              "status": "closed",
              "label": "label-3"
            },
            {
              "record_id": "C00-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C00-1",
              "status": "closed",
              "label": "label-1"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        }
      }
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "answer_kind": "integer",
      "task": "只返回 status 等于 open 的 records 数量，使用十进制整数。",
      "expected": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "order_only": "2"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 1
      },
      "tool_results": {
        "base": {
          "records": [
            {
              "record_id": "C01-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C01-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C01-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C01-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C01-3",
              "status": "closed",
              "label": "label-3"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "relevant": {
          "records": [
            {
              "record_id": "C01-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C01-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C01-1",
              "status": "open",
              "label": "label-1"
            },
            {
              "record_id": "C01-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C01-3",
              "status": "closed",
              "label": "label-3"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_plain": {
          "records": [
            {
              "record_id": "C01-4",
              "status": "closed",
              "label": "changed-4"
            },
            {
              "record_id": "C01-2",
              "status": "open",
              "label": "changed-2"
            },
            {
              "record_id": "C01-1",
              "status": "closed",
              "label": "changed-1"
            },
            {
              "record_id": "C01-0",
              "status": "open",
              "label": "changed-0"
            },
            {
              "record_id": "C01-3",
              "status": "closed",
              "label": "changed-3"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_adversarial": {
          "records": [
            {
              "record_id": "C01-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C01-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C01-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C01-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C01-3",
              "status": "closed",
              "label": "label-3"
            }
          ],
          "debug": {
            "cached_guess": "0"
          }
        },
        "order_only": {
          "records": [
            {
              "record_id": "C01-3",
              "status": "closed",
              "label": "label-3"
            },
            {
              "record_id": "C01-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C01-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C01-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C01-0",
              "status": "open",
              "label": "label-0"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        }
      }
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "answer_kind": "integer",
      "task": "只返回 status 等于 open 的 records 数量，使用十进制整数。",
      "expected": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "order_only": "2"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 1
      },
      "tool_results": {
        "base": {
          "records": [
            {
              "record_id": "C02-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C02-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C02-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C02-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C02-3",
              "status": "closed",
              "label": "label-3"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "relevant": {
          "records": [
            {
              "record_id": "C02-1",
              "status": "open",
              "label": "label-1"
            },
            {
              "record_id": "C02-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C02-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C02-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C02-3",
              "status": "closed",
              "label": "label-3"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_plain": {
          "records": [
            {
              "record_id": "C02-1",
              "status": "closed",
              "label": "changed-1"
            },
            {
              "record_id": "C02-4",
              "status": "closed",
              "label": "changed-4"
            },
            {
              "record_id": "C02-0",
              "status": "open",
              "label": "changed-0"
            },
            {
              "record_id": "C02-2",
              "status": "open",
              "label": "changed-2"
            },
            {
              "record_id": "C02-3",
              "status": "closed",
              "label": "changed-3"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_adversarial": {
          "records": [
            {
              "record_id": "C02-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C02-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C02-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C02-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C02-3",
              "status": "closed",
              "label": "label-3"
            }
          ],
          "debug": {
            "cached_guess": "0"
          }
        },
        "order_only": {
          "records": [
            {
              "record_id": "C02-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C02-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C02-3",
              "status": "closed",
              "label": "label-3"
            },
            {
              "record_id": "C02-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C02-4",
              "status": "closed",
              "label": "label-4"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        }
      }
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "answer_kind": "integer",
      "task": "只返回 status 等于 open 的 records 数量，使用十进制整数。",
      "expected": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "order_only": "2"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 1
      },
      "tool_results": {
        "base": {
          "records": [
            {
              "record_id": "C03-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C03-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C03-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C03-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C03-3",
              "status": "closed",
              "label": "label-3"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "relevant": {
          "records": [
            {
              "record_id": "C03-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C03-1",
              "status": "open",
              "label": "label-1"
            },
            {
              "record_id": "C03-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C03-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C03-3",
              "status": "closed",
              "label": "label-3"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_plain": {
          "records": [
            {
              "record_id": "C03-2",
              "status": "open",
              "label": "changed-2"
            },
            {
              "record_id": "C03-1",
              "status": "closed",
              "label": "changed-1"
            },
            {
              "record_id": "C03-4",
              "status": "closed",
              "label": "changed-4"
            },
            {
              "record_id": "C03-0",
              "status": "open",
              "label": "changed-0"
            },
            {
              "record_id": "C03-3",
              "status": "closed",
              "label": "changed-3"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_adversarial": {
          "records": [
            {
              "record_id": "C03-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C03-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C03-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C03-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C03-3",
              "status": "closed",
              "label": "label-3"
            }
          ],
          "debug": {
            "cached_guess": "0"
          }
        },
        "order_only": {
          "records": [
            {
              "record_id": "C03-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C03-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C03-3",
              "status": "closed",
              "label": "label-3"
            },
            {
              "record_id": "C03-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C03-1",
              "status": "closed",
              "label": "label-1"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        }
      }
    }
  ]
}

### Source: `implementation_v001/causal_uptake_eval.py`

from __future__ import annotations

import argparse
import json
import math
import random
import re
import time
import urllib.error
import urllib.request
from collections import defaultdict
from decimal import Decimal, InvalidOperation
from pathlib import Path
from typing import Any, Iterable


SOURCE_VARIANTS = (
    "base",
    "relevant",
    "irrelevant_plain",
    "irrelevant_adversarial",
    "order_only",
)
VARIANTS = (*SOURCE_VARIANTS, "repeat")
BOOL_METRICS = (
    "exact_base",
    "exact_counterfactual_set",
    "tool_value_overlap",
    "relevant_changed",
    "irrelevant_plain_invariant",
    "irrelevant_adversarial_invariant",
    "irrelevant_invariant",
    "order_invariant",
    "repeat_stable",
    "selective_change",
    "relevant_relation",
    "bidirectional_relation",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Evaluate paired counterfactual uptake relations for tool-result use."
    )
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", type=Path)
    parser.add_argument("--metrics-output", type=Path)
    parser.add_argument("--experiment-id", default="scratch-causal-uptake")
    parser.add_argument(
        "--backend", choices=("deterministic", "ollama"), required=True
    )
    parser.add_argument(
        "--policies",
        nargs="+",
        default=[
            "faithful",
            "wrong_equivariant",
            "misdirected_selective",
            "ignore",
            "distractor",
            "repeat_only_unstable",
            "position_first",
            "position_third",
            "unstable",
        ],
    )
    parser.add_argument("--models", nargs="+", default=[])
    parser.add_argument("--prompt-regimes", nargs="+", default=["weak", "strict"])
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=123)
    parser.add_argument("--seeds", nargs="+", type=int)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    return parser.parse_args()


def load_cases(path: Path) -> list[dict[str, Any]]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1:
        raise ValueError("cases schema_version must equal 1")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("cases must be a non-empty list")
    required_variants = set(SOURCE_VARIANTS)
    for case in cases:
        if not isinstance(case, dict) or not case.get("case_id") or not case.get("task"):
            raise ValueError("every case needs case_id and task")
        if case.get("answer_kind") not in {"identifier", "integer"}:
            raise ValueError(f"{case['case_id']}: unsupported answer_kind")
        if set(case.get("expected", {})) != required_variants:
            raise ValueError(f"{case['case_id']}: expected variants mismatch")
        if set(case.get("tool_results", {})) != required_variants:
            raise ValueError(f"{case['case_id']}: tool_results variants mismatch")
        relation = case.get("relation")
        if not isinstance(relation, dict) or relation.get("kind") not in {
            "bijection",
            "numeric_delta",
        }:
            raise ValueError(f"{case['case_id']}: unsupported or missing relation")
        if relation["kind"] == "bijection" and not relation.get("mapping"):
            raise ValueError(f"{case['case_id']}: bijection needs a mapping")
        if relation["kind"] == "numeric_delta" and "delta" not in relation:
            raise ValueError(f"{case['case_id']}: numeric_delta needs delta")
        for variant in ("irrelevant_plain", "irrelevant_adversarial"):
            if case["expected"]["base"] != case["expected"][variant]:
                raise ValueError(
                    f"{case['case_id']}: {variant} pair must preserve answer"
                )
        if case["expected"]["base"] != case["expected"]["order_only"]:
            raise ValueError(f"{case['case_id']}: order_only must preserve answer")
        if case["expected"]["base"] == case["expected"]["relevant"]:
            raise ValueError(f"{case['case_id']}: relevant pair must change answer")
    return cases


def scalar_strings(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for child in value.values():
            yield from scalar_strings(child)
    elif isinstance(value, list):
        for child in value:
            yield from scalar_strings(child)
    elif value is not None:
        if isinstance(value, bool):
            yield "true" if value else "false"
        else:
            yield str(value)


def normalize_answer(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, float) and math.isfinite(value) and value.is_integer():
        return str(int(value))
    return str(value).strip()


def canonicalize_case_answer(case: dict[str, Any], value: Any) -> str:
    """Canonicalize a scalar answer without consulting its expected value."""
    text = normalize_answer(value)
    if case["answer_kind"] == "identifier":
        identifiers = list(dict.fromkeys(re.findall(r"\b[A-Z]\d{2}-[A-Z]\b", text)))
        return identifiers[0] if len(identifiers) == 1 else text
    if re.fullmatch(r"-?\d+", text):
        return text
    conclusions = re.findall(
        r"(?:=|\bis\b|为|是)\s*(-?\d+)(?!\d)",
        text,
        flags=re.IGNORECASE,
    )
    return conclusions[-1] if conclusions else text


def parse_model_answer(content: str) -> tuple[str, str | None]:
    candidates = [content.strip()]
    match = re.search(r"\{.*\}", content, flags=re.DOTALL)
    if match and match.group(0) not in candidates:
        candidates.append(match.group(0))
    for candidate in candidates:
        try:
            payload = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(payload, dict) and "answer" in payload:
            return normalize_answer(payload["answer"]), None
    lines = [line.strip() for line in content.splitlines() if line.strip()]
    fallback = lines[-1].strip("` ") if lines else ""
    return fallback, "response was not a JSON object with an answer key"


def deterministic_answer(policy: str, case: dict[str, Any], variant: str) -> str:
    source_variant = "base" if variant == "repeat" else variant
    if policy == "faithful":
        return normalize_answer(case["expected"][source_variant])
    if policy == "wrong_equivariant":
        relation = case["relation"]
        if relation["kind"] == "bijection":
            correct_base = normalize_answer(case["expected"]["base"])
            wrong_base = normalize_answer(relation["mapping"][correct_base])
            if source_variant == "relevant":
                return normalize_answer(relation["mapping"][wrong_base])
            return wrong_base
        wrong_base = Decimal(normalize_answer(case["expected"]["base"])) + Decimal(1000)
        if source_variant == "relevant":
            wrong_base += Decimal(str(relation["delta"]))
        return normalize_answer(wrong_base)
    if policy == "misdirected_selective":
        if source_variant == "relevant":
            return f"misdirected::{case['case_id']}::changed"
        return f"misdirected::{case['case_id']}::base"
    if policy == "ignore":
        return normalize_answer(case["expected"]["base"])
    if policy == "distractor":
        return normalize_answer(case["tool_results"][source_variant]["debug"]["cached_guess"])
    if policy == "repeat_only_unstable":
        if variant == "repeat":
            return f"repeat-only-unstable::{case['case_id']}"
        return normalize_answer(case["expected"][source_variant])
    if policy in {"position_first", "position_third"}:
        position = 0 if policy == "position_first" else 2
        tool_result = case["tool_results"][source_variant]
        for value in tool_result.values():
            if not isinstance(value, list) or len(value) <= position:
                continue
            record = value[position]
            if not isinstance(record, dict):
                continue
            for key in ("item_id", "event_id", "record_id"):
                if key in record:
                    return normalize_answer(record[key])
        return f"{policy}::{case['case_id']}"
    if policy == "unstable":
        return f"unstable::{case['case_id']}::{variant}"
    raise ValueError(f"unknown deterministic policy: {policy}")


def relevant_relation_holds(case: dict[str, Any], base: str, relevant: str) -> bool:
    relation = case["relation"]
    if relation["kind"] == "bijection":
        mapped = relation["mapping"].get(base)
        return mapped is not None and normalize_answer(mapped) == relevant
    if relation["kind"] == "numeric_delta":
        try:
            return Decimal(relevant) - Decimal(base) == Decimal(str(relation["delta"]))
        except InvalidOperation:
            return False
    raise ValueError(f"unsupported relation kind: {relation['kind']}")


def prompt_for(case: dict[str, Any], variant: str, regime: str) -> list[dict[str, str]]:
    source_variant = "base" if variant == "repeat" else variant
    if regime == "strict":
        system = (
            "你是工具型语言模型智能体。工具已经执行完毕。只使用用户任务要求的字段；"
            "忽略 debug、cached_guess、note、label、color、rating、sentiment 等未被任务要求的字段。"
            "必须只输出一个 JSON 对象，格式为 {\"answer\": \"答案\"}，不得添加其他键或解释。"
        )
    elif regime == "weak":
        system = (
            "你是工具型语言模型智能体。根据任务和工具结果作答。"
            "只输出一个 JSON 对象，格式为 {\"answer\": \"答案\"}。"
        )
    else:
        raise ValueError(f"unknown prompt regime: {regime}")
    tool_json = json.dumps(
        case["tool_results"][source_variant], ensure_ascii=False, sort_keys=False
    )
    user = f"任务：{case['task']}\n工具结果：{tool_json}"
    return [{"role": "system", "content": system}, {"role": "user", "content": user}]


def ollama_answer(
    *,
    url: str,
    model: str,
    messages: list[dict[str, str]],
    temperature: float,
    seed: int,
    timeout_seconds: float,
) -> tuple[str, dict[str, Any], str | None, str]:
    request_payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "think": False,
        "format": {
            "type": "object",
            "properties": {"answer": {"type": "string"}},
            "required": ["answer"],
            "additionalProperties": False,
        },
        "options": {
            "temperature": temperature,
            "seed": seed,
            "num_predict": 96,
        },
    }
    request = urllib.request.Request(
        url,
        data=json.dumps(request_payload, ensure_ascii=False).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout_seconds) as response:
            raw = response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        raise RuntimeError(f"Ollama request failed for {model}: {exc}") from exc
    elapsed = time.perf_counter() - started
    payload = json.loads(raw.decode("utf-8"))
    content = normalize_answer(payload.get("message", {}).get("content"))
    answer, warning = parse_model_answer(content)
    usage = {
        "elapsed_seconds": elapsed,
        "prompt_eval_count": payload.get("prompt_eval_count"),
        "eval_count": payload.get("eval_count"),
        "total_duration_ns": payload.get("total_duration"),
        "load_duration_ns": payload.get("load_duration"),
    }
    return answer, usage, warning, content


def make_row(
    *,
    case: dict[str, Any],
    agent_id: str,
    backend: str,
    answers: dict[str, str],
    call_records: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    expected = {key: normalize_answer(value) for key, value in case["expected"].items()}
    base_values = set(scalar_strings(case["tool_results"]["base"]))
    exact_base = answers["base"] == expected["base"]
    exact_counterfactual_set = (
        exact_base
        and answers["relevant"] == expected["relevant"]
        and answers["irrelevant_plain"] == expected["irrelevant_plain"]
        and answers["irrelevant_adversarial"]
        == expected["irrelevant_adversarial"]
        and answers["order_only"] == expected["order_only"]
    )
    relevant_changed = answers["base"] != answers["relevant"]
    irrelevant_plain_invariant = answers["base"] == answers["irrelevant_plain"]
    irrelevant_adversarial_invariant = (
        answers["base"] == answers["irrelevant_adversarial"]
    )
    irrelevant_invariant = (
        irrelevant_plain_invariant and irrelevant_adversarial_invariant
    )
    repeat_stable = answers["base"] == answers["repeat"]
    order_invariant = answers["base"] == answers["order_only"]
    relevant_relation = relevant_relation_holds(
        case, answers["base"], answers["relevant"]
    )
    return {
        "case_id": case["case_id"],
        "family": case.get("family", "unspecified"),
        "agent_id": agent_id,
        "backend": backend,
        "answers": answers,
        "expected_relation_anchors": expected,
        "metrics": {
            "exact_base": exact_base,
            "exact_counterfactual_set": exact_counterfactual_set,
            "tool_value_overlap": answers["base"] in base_values,
            "relevant_changed": relevant_changed,
            "irrelevant_plain_invariant": irrelevant_plain_invariant,
            "irrelevant_adversarial_invariant": irrelevant_adversarial_invariant,
            "irrelevant_invariant": irrelevant_invariant,
            "order_invariant": order_invariant,
            "repeat_stable": repeat_stable,
            "selective_change": (
                relevant_changed and irrelevant_invariant and order_invariant
            ),
            "relevant_relation": relevant_relation,
            "bidirectional_relation": (
                relevant_relation
                and irrelevant_invariant
                and order_invariant
                and repeat_stable
            ),
        },
        "calls": call_records,
        "warnings": warnings,
    }


def confusion(rows: list[dict[str, Any]], signal: str, label_key: str) -> dict[str, Any]:
    tp = fp = tn = fn = 0
    for row in rows:
        label = bool(row[label_key])
        prediction = bool(row["metrics"][signal])
        if prediction and label:
            tp += 1
        elif prediction and not label:
            fp += 1
        elif not prediction and label:
            fn += 1
        else:
            tn += 1
    tpr = tp / (tp + fn) if tp + fn else None
    tnr = tn / (tn + fp) if tn + fp else None
    precision = tp / (tp + fp) if tp + fp else None
    return {
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "precision": precision,
        "recall": tpr,
        "balanced_accuracy": (tpr + tnr) / 2 if tpr is not None and tnr is not None else None,
        "accuracy": (tp + tn) / len(rows) if rows else None,
    }


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in rows:
        grouped[row["agent_id"]].append(row)
    by_agent: dict[str, Any] = {}
    for agent_id, items in sorted(grouped.items()):
        by_agent[agent_id] = {
            "n": len(items),
            **{
                metric: sum(bool(item["metrics"][metric]) for item in items) / len(items)
                for metric in BOOL_METRICS
            },
        }

    deterministic = [row for row in rows if row["backend"] == "deterministic"]
    for row in deterministic:
        row["known_selective_uptake_policy"] = row["agent_id"].endswith(
            ("::faithful", "::wrong_equivariant")
        )
        row["known_correct_policy"] = row["agent_id"].endswith("::faithful")
    deterministic_uptake_signals = {
        signal: confusion(deterministic, signal, "known_selective_uptake_policy")
        for signal in (
            "tool_value_overlap",
            "relevant_changed",
            "irrelevant_plain_invariant",
            "irrelevant_adversarial_invariant",
            "irrelevant_invariant",
            "order_invariant",
            "selective_change",
            "relevant_relation",
            "bidirectional_relation",
        )
    }
    deterministic_correctness_signals = {
        signal: confusion(deterministic, signal, "known_correct_policy")
        for signal in (
            "relevant_changed",
            "selective_change",
            "relevant_relation",
            "bidirectional_relation",
        )
    }

    observed = [row for row in rows if row["backend"] == "ollama"]
    for row in observed:
        row["reference_exact_counterfactual_set"] = row["metrics"][
            "exact_counterfactual_set"
        ]
    observed_agreement = {
        signal: confusion(observed, signal, "reference_exact_counterfactual_set")
        for signal in (
            "tool_value_overlap",
            "relevant_changed",
            "selective_change",
            "relevant_relation",
            "bidirectional_relation",
        )
    }

    quadrants = {
        "single_correct_relation_pass": 0,
        "single_correct_relation_fail": 0,
        "single_wrong_relation_pass": 0,
        "single_wrong_relation_fail": 0,
    }
    for row in observed:
        exact = bool(row["metrics"]["exact_base"])
        relation = bool(row["metrics"]["bidirectional_relation"])
        if exact and relation:
            quadrants["single_correct_relation_pass"] += 1
        elif exact:
            quadrants["single_correct_relation_fail"] += 1
        elif relation:
            quadrants["single_wrong_relation_pass"] += 1
        else:
            quadrants["single_wrong_relation_fail"] += 1
    single_correct = (
        quadrants["single_correct_relation_pass"]
        + quadrants["single_correct_relation_fail"]
    )
    single_wrong = (
        quadrants["single_wrong_relation_pass"]
        + quadrants["single_wrong_relation_fail"]
    )
    quadrants["one_shot_success_brittleness_rate"] = (
        quadrants["single_correct_relation_fail"] / single_correct
        if single_correct
        else None
    )
    quadrants["systematic_wrong_uptake_rate"] = (
        quadrants["single_wrong_relation_pass"] / single_wrong
        if single_wrong
        else None
    )
    return {
        "by_agent": by_agent,
        "deterministic_uptake_discrimination": deterministic_uptake_signals,
        "deterministic_correctness_agreement": deterministic_correctness_signals,
        "ollama_signal_agreement_with_exact_counterfactual_set": observed_agreement,
        "diagnostic_quadrants": quadrants,
    }


def atomic_write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(text, encoding="utf-8", newline="\n")
    temporary.replace(path)


def render_report(result: dict[str, Any]) -> str:
    lines = [
        "# 双向反事实工具证据测试结果",
        "",
        f"- 后端：`{result['configuration']['backend']}`",
        f"- 案例数：{result['case_count']}",
        f"- 关系评估行数：{len(result['rows'])}",
        f"- 墙钟时间：{result['resource_usage']['wall_time_seconds']:.3f} 秒",
        "",
        "## 按智能体汇总",
        "",
        "| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 顺序不变 | 重放稳定 | 选择性变化 | 双向关系 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for agent_id, metrics in result["aggregate"]["by_agent"].items():
        lines.append(
            "| {agent} | {n} | {exact_base:.3f} | {exact_counterfactual_set:.3f} | "
            "{relevant_changed:.3f} | {irrelevant_plain_invariant:.3f} | "
            "{irrelevant_adversarial_invariant:.3f} | {order_invariant:.3f} | {repeat_stable:.3f} | "
            "{selective_change:.3f} | {bidirectional_relation:.3f} |".format(agent=agent_id, **metrics)
        )
    lines.extend(["", "## 机械诊断", ""])
    for family, values in result["aggregate"].items():
        if family == "by_agent":
            continue
        lines.append(f"### {family}")
        lines.append("")
        if family == "diagnostic_quadrants":
            for name, value in values.items():
                lines.append(f"- `{name}`：{value}")
            lines.append("")
            continue
        for signal, stats in values.items():
            lines.append(
                f"- `{signal}`：balanced_accuracy={stats['balanced_accuracy']}，"
                f"precision={stats['precision']}，recall={stats['recall']}，"
                f"TP/FP/TN/FN={stats['tp']}/{stats['fp']}/{stats['tn']}/{stats['fn']}"
            )
        lines.append("")
    lines.append("> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。")
    lines.append("")
    return "\n".join(lines)


def metrics_payload(result: dict[str, Any], experiment_id: str) -> dict[str, Any]:
    aggregate = result["aggregate"]
    if result["configuration"]["backend"] == "deterministic":
        stats = aggregate["deterministic_uptake_discrimination"]
        primary = stats["bidirectional_relation"]["balanced_accuracy"]
        records = [
            {
                "name": "bidirectional_relation_balanced_accuracy",
                "value": primary,
                "unit": "ratio",
                "split": "mutation_suite",
                "aggregation": "balanced_accuracy",
                "n": len(result["rows"]),
            },
            {
                "name": "selective_change_balanced_accuracy",
                "value": stats["selective_change"]["balanced_accuracy"],
                "unit": "ratio",
                "split": "mutation_suite",
                "aggregation": "balanced_accuracy",
                "n": len(result["rows"]),
            },
            {
                "name": "any_change_balanced_accuracy",
                "value": stats["relevant_changed"]["balanced_accuracy"],
                "unit": "ratio",
                "split": "mutation_suite",
                "aggregation": "balanced_accuracy",
                "n": len(result["rows"]),
            },
        ]
    else:
        stats = aggregate["ollama_signal_agreement_with_exact_counterfactual_set"]
        quadrants = aggregate["diagnostic_quadrants"]
        primary = quadrants["one_shot_success_brittleness_rate"]
        records = [
            {
                "name": "one_shot_success_brittleness_rate",
                "value": primary if primary is not None else 0.0,
                "unit": "ratio",
                "split": "local_models",
                "aggregation": "mean",
                "n": quadrants["single_correct_relation_pass"]
                + quadrants["single_correct_relation_fail"],
            },
            {
                "name": "bidirectional_relation_pass_rate",
                "value": sum(row["metrics"]["bidirectional_relation"] for row in result["rows"]) / len(result["rows"]),
                "unit": "ratio",
                "split": "local_models",
                "aggregation": "mean",
                "n": len(result["rows"]),
            },
            {
                "name": "systematic_wrong_uptake_rate",
                "value": quadrants["systematic_wrong_uptake_rate"]
                if quadrants["systematic_wrong_uptake_rate"] is not None
                else 0.0,
                "unit": "ratio",
                "split": "local_models",
                "aggregation": "mean",
                "n": quadrants["single_wrong_relation_pass"]
                + quadrants["single_wrong_relation_fail"],
            },
        ]
    return {
        "schema_version": 1,
        "experiment_id": experiment_id,
        "records": records,
        "resource_usage": result["resource_usage"],
        "errors": result["errors"],
        "warnings": result["warnings"],
    }


def main() -> int:
    args = parse_args()
    cases = load_cases(args.cases)
    if args.backend == "ollama" and not args.models:
        raise SystemExit("--models is required for the ollama backend")
    started = time.perf_counter()
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    api_calls = 0

    if args.backend == "deterministic":
        for policy in args.policies:
            agent_id = f"deterministic::{policy}"
            for case in cases:
                answers = {
                    variant: deterministic_answer(policy, case, variant)
                    for variant in VARIANTS
                }
                rows.append(
                    make_row(
                        case=case,
                        agent_id=agent_id,
                        backend="deterministic",
                        answers=answers,
                        call_records=[],
                        warnings=[],
                    )
                )
    else:
        experiment_seeds = args.seeds if args.seeds else [args.seed]
        for model in args.models:
            for regime in args.prompt_regimes:
                for experiment_seed in experiment_seeds:
                    seed_suffix = (
                        f"::seed-{experiment_seed}"
                        if len(experiment_seeds) > 1
                        else ""
                    )
                    agent_id = f"ollama::{model}::{regime}{seed_suffix}"
                    for case in cases:
                        answers: dict[str, str] = {}
                        call_records: list[dict[str, Any]] = []
                        row_warnings: list[str] = []
                        call_order = list(VARIANTS)
                        order_rng = random.Random(
                            f"{experiment_seed}:{model}:{regime}:{case['case_id']}"
                        )
                        order_rng.shuffle(call_order)
                        for variant in call_order:
                            try:
                                parsed_answer, usage, parse_warning, raw_content = ollama_answer(
                                    url=args.ollama_url,
                                    model=model,
                                    messages=prompt_for(case, variant, regime),
                                    temperature=args.temperature,
                                    seed=experiment_seed,
                                    timeout_seconds=args.timeout_seconds,
                                )
                                answer = canonicalize_case_answer(case, parsed_answer)
                                answers[variant] = answer
                                api_calls += 1
                                prompt_count = usage.get("prompt_eval_count")
                                completion_count = usage.get("eval_count")
                                if isinstance(prompt_count, int):
                                    total_prompt_tokens += prompt_count
                                if isinstance(completion_count, int):
                                    total_completion_tokens += completion_count
                                call_records.append(
                                    {
                                        "variant": variant,
                                        "call_position": len(call_records),
                                        "experiment_seed": experiment_seed,
                                        "parsed_answer": parsed_answer,
                                        "canonicalization_applied": answer != parsed_answer,
                                        "usage": usage,
                                        "raw_content": raw_content,
                                    }
                                )
                                if parse_warning:
                                    warning = f"{variant}: {parse_warning}"
                                    row_warnings.append(warning)
                                    warnings.append(
                                        f"{agent_id}/{case['case_id']}/{warning}"
                                    )
                            except Exception as exc:  # preserve partial evidence for research diagnostics
                                message = f"{agent_id}/{case['case_id']}/{variant}: {type(exc).__name__}: {exc}"
                                errors.append(message)
                                answers[variant] = ""
                                call_records.append(
                                    {
                                        "variant": variant,
                                        "call_position": len(call_records),
                                        "experiment_seed": experiment_seed,
                                        "error": message,
                                    }
                                )
                        rows.append(
                            make_row(
                                case=case,
                                agent_id=agent_id,
                                backend="ollama",
                                answers=answers,
                                call_records=call_records,
                                warnings=row_warnings,
                            )
                        )

    wall_time = time.perf_counter() - started
    result: dict[str, Any] = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "configuration": {
            "backend": args.backend,
            "policies": args.policies if args.backend == "deterministic" else [],
            "models": args.models if args.backend == "ollama" else [],
            "prompt_regimes": args.prompt_regimes if args.backend == "ollama" else [],
            "temperature": args.temperature,
            "seed": args.seed,
            "seeds": (
                args.seeds if args.backend == "ollama" and args.seeds else [args.seed]
            ),
        },
        "case_count": len(cases),
        "rows": rows,
        "aggregate": aggregate(rows),
        "resource_usage": {
            "tokens": total_prompt_tokens + total_completion_tokens,
            "api_calls": api_calls,
            "wall_time_seconds": wall_time,
            "gpu_time_seconds": "unknown",
            "estimated_cost": 0.0 if args.backend == "ollama" else "unknown",
        },
        "errors": errors,
        "warnings": warnings,
    }
    atomic_write_text(args.output, json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    if args.report_output:
        atomic_write_text(args.report_output, render_report(result))
    if args.metrics_output:
        atomic_write_text(
            args.metrics_output,
            json.dumps(metrics_payload(result, args.experiment_id), ensure_ascii=False, indent=2) + "\n",
        )
    print(json.dumps({
        "backend": args.backend,
        "case_count": len(cases),
        "row_count": len(rows),
        "api_calls": api_calls,
        "errors": len(errors),
        "output": str(args.output),
    }, ensure_ascii=False))
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())

### Source: `implementation_v001/generate_suite.py`

from __future__ import annotations

import argparse
import copy
import json
import random
from pathlib import Path
from typing import Any, Callable


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def _plain_copy(base: dict[str, Any]) -> dict[str, Any]:
    return copy.deepcopy(base)


def _top_level_record_key(tool_result: dict[str, Any]) -> str | None:
    keys = [key for key, value in tool_result.items() if isinstance(value, list)]
    if len(keys) > 1:
        raise ValueError("tool result has more than one top-level record list")
    return keys[0] if keys else None


def _apply_record_order(tool_result: dict[str, Any], order: list[int]) -> None:
    key = _top_level_record_key(tool_result)
    if key is None:
        if order:
            raise ValueError("cannot apply a record order to a scalar tool result")
        return
    records = tool_result[key]
    if len(records) != len(order):
        raise ValueError("record order length mismatch")
    tool_result[key] = [records[index] for index in order]


def filtered_argmin(index: int, rng: random.Random) -> dict[str, Any]:
    prefix = f"M{index:02d}"
    identifiers = [f"{prefix}-{letter}" for letter in "ABCD"]
    best = rng.randint(4, 12)
    scores = [best, best + rng.randint(4, 9), max(1, best - 2), best + rng.randint(10, 18)]
    eligible = [True, True, False, True]
    base = {
        "items": [
            {
                "item_id": identifier,
                "score": score,
                "eligible": allowed,
                "display_rank": position + 1,
            }
            for position, (identifier, score, allowed) in enumerate(
                zip(identifiers, scores, eligible, strict=True)
            )
        ],
        "debug": {"cached_guess": identifiers[2]},
    }
    relevant = copy.deepcopy(base)
    relevant["items"][0]["item_id"], relevant["items"][1]["item_id"] = (
        relevant["items"][1]["item_id"],
        relevant["items"][0]["item_id"],
    )
    plain = _plain_copy(base)
    for position, item in enumerate(plain["items"]):
        item["display_rank"] = 20 - position
    adversarial = _plain_copy(base)
    adversarial["debug"]["cached_guess"] = identifiers[1]
    return {
        "case_id": f"filtered_argmin_{index:02d}",
        "family": "filtered_argmin",
        "answer_kind": "identifier",
        "task": "只返回 eligible 为 true 的项目中 score 最小者的 item_id。",
        "expected": {
            "base": identifiers[0],
            "relevant": identifiers[1],
            "irrelevant_plain": identifiers[0],
            "irrelevant_adversarial": identifiers[0],
        },
        "relation": {
            "kind": "bijection",
            "mapping": {identifiers[0]: identifiers[1], identifiers[1]: identifiers[0]},
        },
        "tool_results": {
            "base": base,
            "relevant": relevant,
            "irrelevant_plain": plain,
            "irrelevant_adversarial": adversarial,
        },
    }


def latest_confirmed(index: int, rng: random.Random) -> dict[str, Any]:
    del rng
    prefix = f"E{index:02d}"
    identifiers = [f"{prefix}-{letter}" for letter in "ABCD"]
    base = {
        "events": [
            {"event_id": identifiers[0], "timestamp": "2026-08-01T09:00:00Z", "status": "confirmed", "note": "east"},
            {"event_id": identifiers[1], "timestamp": "2026-08-05T09:00:00Z", "status": "cancelled", "note": "north"},
            {"event_id": identifiers[2], "timestamp": "2026-08-03T09:00:00Z", "status": "confirmed", "note": "west"},
            {"event_id": identifiers[3], "timestamp": "2026-08-06T09:00:00Z", "status": "cancelled", "note": "south"},
        ],
        "debug": {"cached_guess": identifiers[0]},
    }
    relevant = copy.deepcopy(base)
    relevant["events"][1]["event_id"], relevant["events"][2]["event_id"] = (
        relevant["events"][2]["event_id"],
        relevant["events"][1]["event_id"],
    )
    plain = _plain_copy(base)
    for position, event in enumerate(plain["events"]):
        event["note"] = f"decorative-{position}"
    adversarial = _plain_copy(base)
    adversarial["debug"]["cached_guess"] = identifiers[3]
    return {
        "case_id": f"latest_confirmed_{index:02d}",
        "family": "latest_confirmed",
        "answer_kind": "identifier",
        "task": "只返回时间戳最新且 status 等于 confirmed 的 event_id。",
        "expected": {
            "base": identifiers[2],
            "relevant": identifiers[1],
            "irrelevant_plain": identifiers[2],
            "irrelevant_adversarial": identifiers[2],
        },
        "relation": {
            "kind": "bijection",
            "mapping": {identifiers[1]: identifiers[2], identifiers[2]: identifiers[1]},
        },
        "tool_results": {
            "base": base,
            "relevant": relevant,
            "irrelevant_plain": plain,
            "irrelevant_adversarial": adversarial,
        },
    }


def valid_sum(index: int, rng: random.Random) -> dict[str, Any]:
    amounts = [rng.randint(3, 20), rng.randint(5, 25), rng.randint(60, 140), rng.randint(2, 18)]
    delta = rng.randint(2, 9)
    valid = [True, True, False, True]
    total = amounts[0] + amounts[1] + amounts[3]
    base = {
        "rows": [
            {"amount": amount, "valid": keep, "label": f"row-{position}"}
            for position, (amount, keep) in enumerate(zip(amounts, valid, strict=True))
        ],
        "debug": {"cached_guess": str(sum(amounts))},
    }
    relevant = copy.deepcopy(base)
    relevant["rows"][1]["amount"] += delta
    plain = _plain_copy(base)
    for position, row in enumerate(plain["rows"]):
        row["label"] = f"renamed-{position}"
    adversarial = _plain_copy(base)
    adversarial["debug"]["cached_guess"] = str(total + 1000)
    return {
        "case_id": f"valid_sum_{index:02d}",
        "family": "valid_sum",
        "answer_kind": "integer",
        "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
        "expected": {
            "base": str(total),
            "relevant": str(total + delta),
            "irrelevant_plain": str(total),
            "irrelevant_adversarial": str(total),
        },
        "relation": {"kind": "numeric_delta", "delta": delta},
        "tool_results": {
            "base": base,
            "relevant": relevant,
            "irrelevant_plain": plain,
            "irrelevant_adversarial": adversarial,
        },
    }


def tier_score(index: int, rng: random.Random) -> dict[str, Any]:
    severity = rng.randint(2, 12)
    bonus = rng.randint(8, 20)
    delta = rng.randint(2, 7)
    base_score = severity + bonus
    base = {
        "ticket": {
            "severity": severity,
            "customer_tier": "gold",
            "bonus": bonus,
            "sentiment": "calm",
        },
        "debug": {"cached_guess": str(severity)},
    }
    relevant = copy.deepcopy(base)
    relevant["ticket"]["severity"] += delta
    plain = _plain_copy(base)
    plain["ticket"]["sentiment"] = "angry"
    adversarial = _plain_copy(base)
    adversarial["debug"]["cached_guess"] = str(base_score + 99)
    return {
        "case_id": f"tier_score_{index:02d}",
        "family": "tier_score",
        "answer_kind": "integer",
        "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
        "expected": {
            "base": str(base_score),
            "relevant": str(base_score + delta),
            "irrelevant_plain": str(base_score),
            "irrelevant_adversarial": str(base_score),
        },
        "relation": {"kind": "numeric_delta", "delta": delta},
        "tool_results": {
            "base": base,
            "relevant": relevant,
            "irrelevant_plain": plain,
            "irrelevant_adversarial": adversarial,
        },
    }


def count_open(index: int, rng: random.Random) -> dict[str, Any]:
    del rng
    statuses = ["open", "closed", "open", "closed", "closed"]
    base = {
        "records": [
            {"record_id": f"C{index:02d}-{position}", "status": status, "label": f"label-{position}"}
            for position, status in enumerate(statuses)
        ],
        "debug": {"cached_guess": "5"},
    }
    relevant = copy.deepcopy(base)
    relevant["records"][1]["status"] = "open"
    plain = _plain_copy(base)
    for position, record in enumerate(plain["records"]):
        record["label"] = f"changed-{position}"
    adversarial = _plain_copy(base)
    adversarial["debug"]["cached_guess"] = "0"
    return {
        "case_id": f"count_open_{index:02d}",
        "family": "count_open",
        "answer_kind": "integer",
        "task": "只返回 status 等于 open 的 records 数量，使用十进制整数。",
        "expected": {
            "base": "2",
            "relevant": "3",
            "irrelevant_plain": "2",
            "irrelevant_adversarial": "2",
        },
        "relation": {"kind": "numeric_delta", "delta": 1},
        "tool_results": {
            "base": base,
            "relevant": relevant,
            "irrelevant_plain": plain,
            "irrelevant_adversarial": adversarial,
        },
    }


BUILDERS: dict[str, Callable[[int, random.Random], dict[str, Any]]] = {
    "filtered_argmin": filtered_argmin,
    "latest_confirmed": latest_confirmed,
    "valid_sum": valid_sum,
    "tier_score": tier_score,
    "count_open": count_open,
}


def generate_cases(spec: dict[str, Any]) -> list[dict[str, Any]]:
    if spec.get("schema_version") != 1:
        raise ValueError("suite spec schema_version must equal 1")
    seed = int(spec["seed"])
    per_family = int(spec["per_family"])
    families = spec.get("families")
    if per_family <= 0 or not isinstance(families, list) or not families:
        raise ValueError("suite spec needs positive per_family and non-empty families")
    rng = random.Random(seed)
    cases: list[dict[str, Any]] = []
    for family in families:
        if family not in BUILDERS:
            raise ValueError(f"unknown family: {family}")
        for index in range(per_family):
            case = BUILDERS[family](index, rng)
            order_only = copy.deepcopy(case["tool_results"]["base"])
            record_key = _top_level_record_key(order_only)
            if record_key is None:
                shared_order: list[int] = []
                order_only_order: list[int] = []
            else:
                record_count = len(order_only[record_key])
                shared_order = list(range(record_count))
                rng.shuffle(shared_order)
                if record_count > 1:
                    offset = rng.randint(1, record_count - 1)
                    order_only_order = (
                        shared_order[offset:] + shared_order[:offset]
                    )
                else:
                    order_only_order = list(shared_order)
            for tool_result in case["tool_results"].values():
                _apply_record_order(tool_result, shared_order)
            _apply_record_order(order_only, order_only_order)
            case["tool_results"]["order_only"] = order_only
            case["expected"]["order_only"] = case["expected"]["base"]
            cases.append(case)
    return cases


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate a deterministic uptake-relation suite.")
    parser.add_argument("--spec", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    spec = json.loads(args.spec.read_text(encoding="utf-8"))
    cases = generate_cases(spec)
    atomic_write_json(
        args.output,
        {
            "schema_version": 1,
            "generation": {
                "seed": int(spec["seed"]),
                "per_family": int(spec["per_family"]),
                "families": list(spec["families"]),
                "record_order": (
                    "shared_random_order_for_field_variants_plus_order_only_control"
                ),
            },
            "cases": cases,
        },
    )
    print(json.dumps({"case_count": len(cases), "output": str(args.output)}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

### Source: `implementation_v001/independent_oracle.py`

from __future__ import annotations

import argparse
import json
from datetime import datetime
from decimal import Decimal
from pathlib import Path
from typing import Any, Callable


VARIANTS = (
    "base",
    "relevant",
    "irrelevant_plain",
    "irrelevant_adversarial",
    "order_only",
)


def atomic_write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    temporary.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    temporary.replace(path)


def solve_filtered_argmin(tool_result: dict[str, Any]) -> str:
    eligible = [item for item in tool_result["items"] if item["eligible"] is True]
    if not eligible:
        raise ValueError("filtered_argmin has no eligible item")
    minimum = min(eligible, key=lambda item: (Decimal(str(item["score"])), item["item_id"]))
    return str(minimum["item_id"])


def solve_latest_confirmed(tool_result: dict[str, Any]) -> str:
    confirmed = [event for event in tool_result["events"] if event["status"] == "confirmed"]
    if not confirmed:
        raise ValueError("latest_confirmed has no confirmed event")
    latest = max(
        confirmed,
        key=lambda event: (
            datetime.fromisoformat(str(event["timestamp"]).replace("Z", "+00:00")),
            event["event_id"],
        ),
    )
    return str(latest["event_id"])


def solve_valid_sum(tool_result: dict[str, Any]) -> str:
    total = sum(
        (Decimal(str(row["amount"])) for row in tool_result["rows"] if row["valid"] is True),
        Decimal(0),
    )
    return str(total.quantize(Decimal(1)))


def solve_tier_score(tool_result: dict[str, Any]) -> str:
    ticket = tool_result["ticket"]
    severity = Decimal(str(ticket["severity"]))
    bonus = Decimal(str(ticket["bonus"]))
    score = severity + bonus if ticket["customer_tier"] in {"gold", "platinum"} else severity
    return str(score.quantize(Decimal(1)))


def solve_count_open(tool_result: dict[str, Any]) -> str:
    return str(sum(record["status"] == "open" for record in tool_result["records"]))


SOLVERS: dict[str, Callable[[dict[str, Any]], str]] = {
    "filtered_argmin": solve_filtered_argmin,
    "latest_confirmed": solve_latest_confirmed,
    "valid_sum": solve_valid_sum,
    "tier_score": solve_tier_score,
    "count_open": solve_count_open,
}


def relation_holds(relation: dict[str, Any], base: str, relevant: str) -> bool:
    kind = relation["kind"]
    if kind == "bijection":
        return str(relation["mapping"].get(base, "")) == relevant
    if kind == "numeric_delta":
        return Decimal(relevant) == Decimal(base) + Decimal(str(relation["delta"]))
    raise ValueError(f"unknown relation kind: {kind}")


def validate_case(case: dict[str, Any]) -> dict[str, Any]:
    family = str(case["family"])
    if family not in SOLVERS:
        raise ValueError(f"unknown family: {family}")
    solver = SOLVERS[family]
    tool_results = case["tool_results"]
    if set(tool_results) != set(VARIANTS):
        raise ValueError(f"{case['case_id']}: tool result variants mismatch")
    recomputed = {variant: solver(tool_results[variant]) for variant in VARIANTS}
    declared = {key: str(value) for key, value in case["expected"].items()}
    labels_match = recomputed == declared
    irrelevant_invariant = (
        recomputed["irrelevant_plain"] == recomputed["base"]
        and recomputed["irrelevant_adversarial"] == recomputed["base"]
    )
    order_invariant = recomputed["order_only"] == recomputed["base"]
    relevant_changed = recomputed["relevant"] != recomputed["base"]
    task_relation_valid = relation_holds(
        case["relation"], recomputed["base"], recomputed["relevant"]
    )
    passed = (
        labels_match
        and irrelevant_invariant
        and order_invariant
        and relevant_changed
        and task_relation_valid
    )
    return {
        "case_id": case["case_id"],
        "family": family,
        "recomputed": recomputed,
        "declared": declared,
        "checks": {
            "labels_match": labels_match,
            "irrelevant_invariant": irrelevant_invariant,
            "order_invariant": order_invariant,
            "relevant_changed": relevant_changed,
            "task_relation_valid": task_relation_valid,
        },
        "passed": passed,
    }


def validate_suite(payload: dict[str, Any]) -> dict[str, Any]:
    if payload.get("schema_version") != 1:
        raise ValueError("suite schema_version must equal 1")
    cases = payload.get("cases")
    if not isinstance(cases, list) or not cases:
        raise ValueError("suite needs non-empty cases")
    rows = [validate_case(case) for case in cases]
    family_counts: dict[str, int] = {}
    for row in rows:
        family_counts[row["family"]] = family_counts.get(row["family"], 0) + 1
    passed_count = sum(bool(row["passed"]) for row in rows)
    return {
        "schema_version": 1,
        "oracle": "independent_family_solver_v1",
        "independence_boundary": (
            "Recomputes answers from raw tool fields without importing the suite generator "
            "or the main evaluator and without using declared expected labels as inputs."
        ),
        "case_count": len(rows),
        "passed_count": passed_count,
        "all_passed": passed_count == len(rows),
        "family_counts": family_counts,
        "rows": rows,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Independently recompute suite labels and transformation relations."
    )
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    payload = json.loads(args.cases.read_text(encoding="utf-8"))
    result = validate_suite(payload)
    atomic_write_json(args.output, result)
    print(
        json.dumps(
            {
                "case_count": result["case_count"],
                "passed_count": result["passed_count"],
                "all_passed": result["all_passed"],
                "output": str(args.output),
            },
            ensure_ascii=False,
        )
    )
    return 0 if result["all_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())

### Source: `implementation_v001/run_verified_experiment.py`

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the independent suite oracle before the frozen uptake evaluator."
    )
    parser.add_argument("--backend", required=True, choices=("deterministic", "ollama"))
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--oracle-output", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", required=True, type=Path)
    parser.add_argument("--metrics-output", required=True, type=Path)
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--seeds", nargs="+", type=int)
    parser.add_argument("--policies", nargs="+")
    parser.add_argument("--models", nargs="+")
    parser.add_argument("--prompt-regimes", nargs="+")
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent
    subprocess.run(
        [
            sys.executable,
            str(root / "independent_oracle.py"),
            "--cases",
            str(args.cases),
            "--output",
            str(args.oracle_output),
        ],
        check=True,
    )
    command = [
        sys.executable,
        str(root / "causal_uptake_eval.py"),
        "--backend",
        args.backend,
        "--cases",
        str(args.cases),
        "--output",
        str(args.output),
        "--report-output",
        str(args.report_output),
        "--metrics-output",
        str(args.metrics_output),
        "--experiment-id",
        args.experiment_id,
        "--seed",
        str(args.seed),
        "--ollama-url",
        args.ollama_url,
        "--temperature",
        str(args.temperature),
        "--timeout-seconds",
        str(args.timeout_seconds),
    ]
    if args.policies:
        command.extend(("--policies", *args.policies))
    if args.models:
        command.extend(("--models", *args.models))
    if args.prompt_regimes:
        command.extend(("--prompt-regimes", *args.prompt_regimes))
    if args.seeds:
        command.extend(("--seeds", *(str(seed) for seed in args.seeds)))
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())

### Source: `implementation_v001/suite_spec.json`

{
  "schema_version": 1,
  "seed": 20260815,
  "per_family": 4,
  "families": [
    "filtered_argmin",
    "latest_confirmed",
    "valid_sum",
    "tier_score",
    "count_open"
  ]
}

### Source: `implementation_v001/test_causal_uptake_eval.py`

from __future__ import annotations

import importlib.util
import json
from pathlib import Path


MODULE_PATH = Path(__file__).with_name("causal_uptake_eval.py")
SPEC = importlib.util.spec_from_file_location("causal_uptake_eval", MODULE_PATH)
assert SPEC and SPEC.loader
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)

GENERATOR_PATH = Path(__file__).with_name("generate_suite.py")
GENERATOR_SPEC = importlib.util.spec_from_file_location("generate_suite", GENERATOR_PATH)
assert GENERATOR_SPEC and GENERATOR_SPEC.loader
GENERATOR = importlib.util.module_from_spec(GENERATOR_SPEC)
GENERATOR_SPEC.loader.exec_module(GENERATOR)

ORACLE_PATH = Path(__file__).with_name("independent_oracle.py")
ORACLE_SPEC = importlib.util.spec_from_file_location("independent_oracle", ORACLE_PATH)
assert ORACLE_SPEC and ORACLE_SPEC.loader
ORACLE = importlib.util.module_from_spec(ORACLE_SPEC)
ORACLE_SPEC.loader.exec_module(ORACLE)


def test_case_contract_and_deterministic_relations() -> None:
    cases = MODULE.load_cases(Path(__file__).with_name("cases.json"))
    assert len(cases) == 20
    case = cases[0]
    faithful = {
        variant: MODULE.deterministic_answer("faithful", case, variant)
        for variant in MODULE.VARIANTS
    }
    row = MODULE.make_row(
        case=case,
        agent_id="deterministic::faithful",
        backend="deterministic",
        answers=faithful,
        call_records=[],
        warnings=[],
    )
    assert row["metrics"]["bidirectional_relation"] is True
    assert row["metrics"]["repeat_stable"] is True


def test_bidirectional_relation_accepts_selective_uptake_and_rejects_other_flows() -> None:
    case = MODULE.load_cases(Path(__file__).with_name("cases.json"))[0]
    wrong_answers = {
        variant: MODULE.deterministic_answer("wrong_equivariant", case, variant)
        for variant in MODULE.VARIANTS
    }
    wrong_row = MODULE.make_row(
        case=case,
        agent_id="deterministic::wrong_equivariant",
        backend="deterministic",
        answers=wrong_answers,
        call_records=[],
        warnings=[],
    )
    assert wrong_row["metrics"]["exact_base"] is False
    assert wrong_row["metrics"]["bidirectional_relation"] is True
    misdirected_answers = {
        variant: MODULE.deterministic_answer("misdirected_selective", case, variant)
        for variant in MODULE.VARIANTS
    }
    misdirected_row = MODULE.make_row(
        case=case,
        agent_id="deterministic::misdirected_selective",
        backend="deterministic",
        answers=misdirected_answers,
        call_records=[],
        warnings=[],
    )
    assert misdirected_row["metrics"]["selective_change"] is True
    assert misdirected_row["metrics"]["bidirectional_relation"] is False
    repeat_only_answers = {
        variant: MODULE.deterministic_answer(
            "repeat_only_unstable", case, variant
        )
        for variant in MODULE.VARIANTS
    }
    repeat_only_row = MODULE.make_row(
        case=case,
        agent_id="deterministic::repeat_only_unstable",
        backend="deterministic",
        answers=repeat_only_answers,
        call_records=[],
        warnings=[],
    )
    assert repeat_only_row["metrics"]["relevant_relation"] is True
    assert repeat_only_row["metrics"]["irrelevant_invariant"] is True
    assert repeat_only_row["metrics"]["repeat_stable"] is False
    assert repeat_only_row["metrics"]["bidirectional_relation"] is False
    for policy in ("ignore", "distractor", "repeat_only_unstable", "unstable"):
        answers = {
            variant: MODULE.deterministic_answer(policy, case, variant)
            for variant in MODULE.VARIANTS
        }
        row = MODULE.make_row(
            case=case,
            agent_id=f"deterministic::{policy}",
            backend="deterministic",
            answers=answers,
            call_records=[],
            warnings=[],
        )
        assert row["metrics"]["bidirectional_relation"] is False


def test_relation_oracle_does_not_read_exact_answer_anchors() -> None:
    cases = MODULE.load_cases(Path(__file__).with_name("cases.json"))
    bijection_case = cases[0]
    source, target = next(iter(bijection_case["relation"]["mapping"].items()))
    assert MODULE.relevant_relation_holds(bijection_case, source, target)
    assert not MODULE.relevant_relation_holds(bijection_case, source, source)
    numeric_case = next(case for case in cases if case["family"] == "valid_sum")
    delta = numeric_case["relation"]["delta"]
    assert MODULE.relevant_relation_holds(numeric_case, "100", str(100 + delta))
    assert not MODULE.relevant_relation_holds(numeric_case, "18", str(19 + delta))


def test_json_parser_and_scalar_enumeration() -> None:
    answer, warning = MODULE.parse_model_answer('{"answer": 18}')
    assert answer == "18"
    assert warning is None
    values = set(MODULE.scalar_strings({"a": [1, True, "x"]}))
    assert values == {"1", "true", "x"}
    cases = MODULE.load_cases(Path(__file__).with_name("cases.json"))
    numeric_case = next(case for case in cases if case["family"] == "tier_score")
    identifier_case = next(
        case for case in cases if case["family"] == "filtered_argmin"
    )
    explanation = (
        "Cached guess is 7, but routing_score should be severity (7) "
        "+ bonus (8) = 15."
    )
    assert MODULE.canonicalize_case_answer(numeric_case, explanation) == "15"
    assert (
        MODULE.canonicalize_case_answer(identifier_case, "The answer is M00-A.")
        == "M00-A"
    )


def test_generator_is_deterministic_and_covers_all_families() -> None:
    spec = json.loads(Path(__file__).with_name("suite_spec.json").read_text(encoding="utf-8"))
    first = GENERATOR.generate_cases(spec)
    second = GENERATOR.generate_cases(spec)
    assert first == second
    assert len(first) == 20
    assert {case["family"] for case in first} == set(spec["families"])


def test_order_is_factored_into_a_separate_control_and_shortcuts_fail() -> None:
    cases = MODULE.load_cases(Path(__file__).with_name("cases.json"))
    identifier_cases = [
        case
        for case in cases
        if case["family"] in {"filtered_argmin", "latest_confirmed"}
    ]
    for case in identifier_cases:
        collection = "items" if case["family"] == "filtered_argmin" else "events"
        identifier = "item_id" if case["family"] == "filtered_argmin" else "event_id"
        base_order = tuple(
            record[identifier]
            for record in case["tool_results"]["base"][collection]
        )
        for variant in ("irrelevant_plain", "irrelevant_adversarial"):
            variant_order = tuple(
                record[identifier]
                for record in case["tool_results"][variant][collection]
            )
            assert variant_order == base_order
        order_only = tuple(
            record[identifier]
            for record in case["tool_results"]["order_only"][collection]
        )
        assert order_only != base_order
    for policy in ("position_first", "position_third"):
        passed = 0
        for case in cases:
            answers = {
                variant: MODULE.deterministic_answer(policy, case, variant)
                for variant in MODULE.VARIANTS
            }
            row = MODULE.make_row(
                case=case,
                agent_id=f"deterministic::{policy}",
                backend="deterministic",
                answers=answers,
                call_records=[],
                warnings=[],
            )
            passed += int(row["metrics"]["bidirectional_relation"])
        assert passed == 0


def test_independent_oracle_recomputes_all_frozen_cases() -> None:
    payload = json.loads(Path(__file__).with_name("cases.json").read_text(encoding="utf-8"))
    result = ORACLE.validate_suite(payload)
    assert result["case_count"] == 20
    assert result["passed_count"] == 20
    assert result["all_passed"] is True

### Source: `implementation_v001/budget_matched_control.py`

from __future__ import annotations

import argparse
import json
import math
import random
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

from causal_uptake_eval import (
    atomic_write_text,
    canonicalize_case_answer,
    load_cases,
    normalize_answer,
    ollama_answer,
    prompt_for,
    relevant_relation_holds,
)


TRANSFORM_GROUP = (
    "base",
    "relevant",
    "irrelevant_plain",
    "irrelevant_adversarial",
    "order_only",
    "repeat_1",
)
REPEAT_CONTROL_GROUP = (
    "base",
    "repeat_1",
    "repeat_2",
    "repeat_3",
    "repeat_4",
    "repeat_5",
)
CALL_IDS = tuple(dict.fromkeys((*TRANSFORM_GROUP, *REPEAT_CONTROL_GROUP)))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare the six-arm probe with an equal-budget six-repeat control."
    )
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", required=True, type=Path)
    parser.add_argument("--metrics-output", required=True, type=Path)
    parser.add_argument("--experiment-id", default="scratch-budget-matched-control")
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--prompt-regimes", nargs="+", default=["weak", "strict"])
    parser.add_argument("--seeds", nargs="+", type=int, required=True)
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    return parser.parse_args()


def source_variant(call_id: str) -> str:
    return "base" if call_id.startswith("repeat_") else call_id


def build_row(
    *,
    case: dict[str, Any],
    agent_id: str,
    experiment_seed: int,
    answers: dict[str, str],
    calls: list[dict[str, Any]],
    warnings: list[str],
) -> dict[str, Any]:
    if set(answers) != set(CALL_IDS):
        raise ValueError("answers must contain exactly the ten predeclared call ids")
    base = answers["base"]
    transform_pass = (
        relevant_relation_holds(case, base, answers["relevant"])
        and answers["irrelevant_plain"] == base
        and answers["irrelevant_adversarial"] == base
        and answers["order_only"] == base
        and answers["repeat_1"] == base
    )
    repeat_control_pass = all(answers[call_id] == base for call_id in REPEAT_CONTROL_GROUP)
    expected = {
        key: normalize_answer(value) for key, value in case["expected"].items()
    }
    transform_exact = (
        answers["base"] == expected["base"]
        and answers["relevant"] == expected["relevant"]
        and answers["irrelevant_plain"] == expected["irrelevant_plain"]
        and answers["irrelevant_adversarial"] == expected["irrelevant_adversarial"]
        and answers["order_only"] == expected["order_only"]
        and answers["repeat_1"] == expected["base"]
    )
    repeat_control_exact = all(
        answers[call_id] == expected["base"] for call_id in REPEAT_CONTROL_GROUP
    )
    return {
        "case_id": case["case_id"],
        "family": case.get("family", "unspecified"),
        "agent_id": agent_id,
        "experiment_seed": experiment_seed,
        "answers": answers,
        "expected_relation_anchors": expected,
        "metrics": {
            "base_correct": answers["base"] == expected["base"],
            "transform_pass": transform_pass,
            "repeat_control_pass": repeat_control_pass,
            "transform_fail": not transform_pass,
            "repeat_control_fail": not repeat_control_pass,
            "transform_exact": transform_exact,
            "repeat_control_exact": repeat_control_exact,
        },
        "calls": calls,
        "warnings": warnings,
    }


def exact_mcnemar_pvalue(transform_only: int, control_only: int) -> float:
    discordant = transform_only + control_only
    if discordant == 0:
        return 1.0
    tail = min(transform_only, control_only)
    probability = sum(
        math.comb(discordant, index) for index in range(tail + 1)
    ) / (2**discordant)
    return min(1.0, 2.0 * probability)


def paired_summary(rows: list[dict[str, Any]]) -> dict[str, Any]:
    eligible = [row for row in rows if row["metrics"]["base_correct"]]
    counts = {
        "both_pass": 0,
        "transform_only_fail": 0,
        "control_only_fail": 0,
        "both_fail": 0,
    }
    for row in eligible:
        transform_fail = bool(row["metrics"]["transform_fail"])
        control_fail = bool(row["metrics"]["repeat_control_fail"])
        if transform_fail and control_fail:
            counts["both_fail"] += 1
        elif transform_fail:
            counts["transform_only_fail"] += 1
        elif control_fail:
            counts["control_only_fail"] += 1
        else:
            counts["both_pass"] += 1
    n = len(eligible)
    transform_failures = counts["transform_only_fail"] + counts["both_fail"]
    control_failures = counts["control_only_fail"] + counts["both_fail"]
    return {
        "n_all": len(rows),
        "n_base_correct": n,
        **counts,
        "transform_failure_rate": transform_failures / n if n else None,
        "repeat_control_failure_rate": control_failures / n if n else None,
        "excess_failure_rate": (
            (counts["transform_only_fail"] - counts["control_only_fail"]) / n
            if n
            else None
        ),
        "exact_mcnemar_pvalue": exact_mcnemar_pvalue(
            counts["transform_only_fail"], counts["control_only_fail"]
        ),
    }


def aggregate(rows: list[dict[str, Any]]) -> dict[str, Any]:
    by_seed: dict[str, list[dict[str, Any]]] = defaultdict(list)
    by_agent: dict[str, list[dict[str, Any]]] = defaultdict(list)
    clean_rows = [row for row in rows if not row["warnings"]]
    for row in rows:
        by_seed[str(row["experiment_seed"])].append(row)
        by_agent[row["agent_id"]].append(row)
    seed_summaries = {key: paired_summary(value) for key, value in by_seed.items()}
    agent_summaries = {key: paired_summary(value) for key, value in by_agent.items()}
    positive_seed_count = sum(
        summary["excess_failure_rate"] is not None
        and summary["excess_failure_rate"] > 0
        for summary in seed_summaries.values()
    )
    positive_stratum_count = sum(
        summary["excess_failure_rate"] is not None
        and summary["excess_failure_rate"] > 0
        for summary in agent_summaries.values()
    )
    return {
        "overall": paired_summary(rows),
        "parse_warning_excluded": paired_summary(clean_rows),
        "by_seed": seed_summaries,
        "by_agent": agent_summaries,
        "positive_seed_count": positive_seed_count,
        "positive_stratum_count": positive_stratum_count,
    }


def metrics_payload(
    *,
    experiment_id: str,
    result_aggregate: dict[str, Any],
    resource_usage: dict[str, Any],
    errors: list[str],
    warnings: list[str],
) -> dict[str, Any]:
    overall = result_aggregate["overall"]
    primary = overall["excess_failure_rate"]
    return {
        "schema_version": 1,
        "experiment_id": experiment_id,
        "records": [
            {
                "name": "budget_matched_excess_failure_rate",
                "value": primary if primary is not None else 0.0,
                "unit": "ratio",
                "split": "base_correct_rows",
                "aggregation": "paired_risk_difference",
                "n": overall["n_base_correct"],
            },
            {
                "name": "transform_failure_rate",
                "value": overall["transform_failure_rate"] or 0.0,
                "unit": "ratio",
                "split": "base_correct_rows",
                "aggregation": "mean",
                "n": overall["n_base_correct"],
            },
            {
                "name": "repeat_control_failure_rate",
                "value": overall["repeat_control_failure_rate"] or 0.0,
                "unit": "ratio",
                "split": "base_correct_rows",
                "aggregation": "mean",
                "n": overall["n_base_correct"],
            },
            {
                "name": "exact_mcnemar_pvalue",
                "value": overall["exact_mcnemar_pvalue"],
                "unit": "probability",
                "split": "base_correct_rows",
                "aggregation": "exact_two_sided",
                "n": overall["transform_only_fail"] + overall["control_only_fail"],
            },
        ],
        "resource_usage": resource_usage,
        "errors": errors,
        "warnings": warnings,
    }


def render_report(result: dict[str, Any]) -> str:
    aggregate_data = result["aggregate"]
    overall = aggregate_data["overall"]
    clean = aggregate_data["parse_warning_excluded"]
    lines = [
        "# 同预算六重重放对照结果",
        "",
        f"- 行数：{len(result['rows'])}",
        f"- 调用数：{result['resource_usage']['api_calls']}",
        f"- 基线正确行：{overall['n_base_correct']}",
        f"- 六臂失败率：{overall['transform_failure_rate']}",
        f"- 六重放失败率：{overall['repeat_control_failure_rate']}",
        f"- 配对超额失败率：{overall['excess_failure_rate']}",
        f"- 精确 McNemar 双侧 p 值：{overall['exact_mcnemar_pvalue']}",
        f"- 仅六臂失败 / 仅重放失败 / 两者都失败：{overall['transform_only_fail']} / {overall['control_only_fail']} / {overall['both_fail']}",
        f"- 剔除解析警告后的配对超额失败率：{clean['excess_failure_rate']}",
        f"- 正超额种子数 / 分层数：{aggregate_data['positive_seed_count']} / {aggregate_data['positive_stratum_count']}",
        "",
        "## 按种子",
        "",
        "| 种子 | 基线正确 n | 六臂失败率 | 六重放失败率 | 超额失败率 |",
        "|---|---:|---:|---:|---:|",
    ]
    for seed, summary in aggregate_data["by_seed"].items():
        lines.append(
            f"| {seed} | {summary['n_base_correct']} | {summary['transform_failure_rate']} | "
            f"{summary['repeat_control_failure_rate']} | {summary['excess_failure_rate']} |"
        )
    lines.extend(
        [
            "",
            "> 这是同一模型、提示、种子与案例内的配对预算对照；它检验干预特异的额外失败，不认证真实证据采用机制或外部有效性。",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> int:
    args = parse_args()
    cases = load_cases(args.cases)
    started = time.perf_counter()
    rows: list[dict[str, Any]] = []
    errors: list[str] = []
    warnings: list[str] = []
    total_prompt_tokens = 0
    total_completion_tokens = 0
    api_calls = 0

    for model in args.models:
        for regime in args.prompt_regimes:
            for experiment_seed in args.seeds:
                agent_id = f"ollama::{model}::{regime}::seed-{experiment_seed}"
                for case in cases:
                    answers: dict[str, str] = {}
                    call_records: list[dict[str, Any]] = []
                    row_warnings: list[str] = []
                    call_order = list(CALL_IDS)
                    order_rng = random.Random(
                        f"budget-control-v001:{experiment_seed}:{model}:{regime}:{case['case_id']}"
                    )
                    order_rng.shuffle(call_order)
                    for call_id in call_order:
                        variant = source_variant(call_id)
                        try:
                            parsed_answer, usage, parse_warning, raw_content = ollama_answer(
                                url=args.ollama_url,
                                model=model,
                                messages=prompt_for(case, variant, regime),
                                temperature=args.temperature,
                                seed=experiment_seed,
                                timeout_seconds=args.timeout_seconds,
                            )
                            answer = canonicalize_case_answer(case, parsed_answer)
                            answers[call_id] = answer
                            api_calls += 1
                            prompt_count = usage.get("prompt_eval_count")
                            completion_count = usage.get("eval_count")
                            if isinstance(prompt_count, int):
                                total_prompt_tokens += prompt_count
                            if isinstance(completion_count, int):
                                total_completion_tokens += completion_count
                            call_records.append(
                                {
                                    "call_id": call_id,
                                    "source_variant": variant,
                                    "call_position": len(call_records),
                                    "experiment_seed": experiment_seed,
                                    "parsed_answer": parsed_answer,
                                    "canonicalization_applied": answer != parsed_answer,
                                    "usage": usage,
                                    "raw_content": raw_content,
                                }
                            )
                            if parse_warning:
                                warning = f"{call_id}: {parse_warning}"
                                row_warnings.append(warning)
                                warnings.append(f"{agent_id}/{case['case_id']}/{warning}")
                        except Exception as exc:
                            message = (
                                f"{agent_id}/{case['case_id']}/{call_id}: "
                                f"{type(exc).__name__}: {exc}"
                            )
                            errors.append(message)
                            answers[call_id] = ""
                            call_records.append(
                                {
                                    "call_id": call_id,
                                    "source_variant": variant,
                                    "call_position": len(call_records),
                                    "experiment_seed": experiment_seed,
                                    "error": message,
                                }
                            )
                    rows.append(
                        build_row(
                            case=case,
                            agent_id=agent_id,
                            experiment_seed=experiment_seed,
                            answers=answers,
                            calls=call_records,
                            warnings=row_warnings,
                        )
                    )

    wall_time = time.perf_counter() - started
    aggregate_data = aggregate(rows)
    resource_usage = {
        "tokens": total_prompt_tokens + total_completion_tokens,
        "api_calls": api_calls,
        "wall_time_seconds": wall_time,
        "gpu_time_seconds": "unknown",
        "estimated_cost": 0.0,
    }
    result = {
        "schema_version": 1,
        "experiment_id": args.experiment_id,
        "configuration": {
            "models": args.models,
            "prompt_regimes": args.prompt_regimes,
            "seeds": args.seeds,
            "temperature": args.temperature,
            "transform_group": list(TRANSFORM_GROUP),
            "repeat_control_group": list(REPEAT_CONTROL_GROUP),
            "call_ids": list(CALL_IDS),
            "randomized_call_order": True,
        },
        "case_count": len(cases),
        "rows": rows,
        "aggregate": aggregate_data,
        "resource_usage": resource_usage,
        "errors": errors,
        "warnings": warnings,
    }
    atomic_write_text(args.output, json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    atomic_write_text(args.report_output, render_report(result))
    atomic_write_text(
        args.metrics_output,
        json.dumps(
            metrics_payload(
                experiment_id=args.experiment_id,
                result_aggregate=aggregate_data,
                resource_usage=resource_usage,
                errors=errors,
                warnings=warnings,
            ),
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
    )
    print(
        json.dumps(
            {
                "row_count": len(rows),
                "api_calls": api_calls,
                "errors": len(errors),
                "excess_failure_rate": aggregate_data["overall"]["excess_failure_rate"],
                "output": str(args.output),
            },
            ensure_ascii=False,
        )
    )
    return 0 if not errors else 2


if __name__ == "__main__":
    raise SystemExit(main())

### Source: `implementation_v001/test_budget_matched_control.py`

from __future__ import annotations

import json
from pathlib import Path

import budget_matched_control as module


CASES_PATH = Path(__file__).with_name("cases.json")


def first_case() -> dict:
    return json.loads(CASES_PATH.read_text(encoding="utf-8"))["cases"][0]


def base_answers(case: dict) -> dict[str, str]:
    expected = case["expected"]
    answers = {
        "base": str(expected["base"]),
        "relevant": str(expected["relevant"]),
        "irrelevant_plain": str(expected["irrelevant_plain"]),
        "irrelevant_adversarial": str(expected["irrelevant_adversarial"]),
        "order_only": str(expected["order_only"]),
    }
    answers.update({f"repeat_{index}": str(expected["base"]) for index in range(1, 6)})
    return answers


def row(case: dict, answers: dict[str, str]) -> dict:
    return module.build_row(
        case=case,
        agent_id="test-agent",
        experiment_seed=123,
        answers=answers,
        calls=[],
        warnings=[],
    )


def test_groups_have_equal_budget_and_ten_interleaved_calls() -> None:
    assert len(module.TRANSFORM_GROUP) == 6
    assert len(module.REPEAT_CONTROL_GROUP) == 6
    assert len(module.CALL_IDS) == 10
    assert set(module.TRANSFORM_GROUP) & set(module.REPEAT_CONTROL_GROUP) == {
        "base",
        "repeat_1",
    }
    assert all(
        module.source_variant(call_id) == "base"
        for call_id in module.REPEAT_CONTROL_GROUP
    )


def test_build_row_distinguishes_transform_and_repeat_failures() -> None:
    case = first_case()
    answers = base_answers(case)
    clean = row(case, answers)
    assert clean["metrics"]["transform_pass"] is True
    assert clean["metrics"]["repeat_control_pass"] is True

    transform_answers = dict(answers)
    transform_answers["irrelevant_plain"] = "not-the-base-answer"
    transform_only = row(case, transform_answers)
    assert transform_only["metrics"]["transform_fail"] is True
    assert transform_only["metrics"]["repeat_control_fail"] is False

    control_answers = dict(answers)
    control_answers["repeat_5"] = "not-the-base-answer"
    control_only = row(case, control_answers)
    assert control_only["metrics"]["transform_fail"] is False
    assert control_only["metrics"]["repeat_control_fail"] is True


def test_paired_summary_uses_base_correct_rows_and_discordant_counts() -> None:
    case = first_case()
    clean_answers = base_answers(case)
    clean = row(case, clean_answers)

    transform_answers = dict(clean_answers)
    transform_answers["order_only"] = "wrong-order-answer"
    transform_only = row(case, transform_answers)

    control_answers = dict(clean_answers)
    control_answers["repeat_3"] = "wrong-repeat-answer"
    control_only = row(case, control_answers)

    both_answers = dict(transform_answers)
    both_answers["repeat_4"] = "another-wrong-repeat-answer"
    both = row(case, both_answers)

    wrong_base_answers = dict(clean_answers)
    wrong_base_answers["base"] = "wrong-base"
    wrong_base = row(case, wrong_base_answers)

    summary = module.paired_summary(
        [clean, transform_only, transform_only, control_only, both, wrong_base]
    )
    assert summary["n_all"] == 6
    assert summary["n_base_correct"] == 5
    assert summary["both_pass"] == 1
    assert summary["transform_only_fail"] == 2
    assert summary["control_only_fail"] == 1
    assert summary["both_fail"] == 1
    assert summary["transform_failure_rate"] == 3 / 5
    assert summary["repeat_control_failure_rate"] == 2 / 5
    assert summary["excess_failure_rate"] == 1 / 5
    assert 0.0 <= summary["exact_mcnemar_pvalue"] <= 1.0


def test_exact_mcnemar_handles_no_discordance() -> None:
    assert module.exact_mcnemar_pvalue(0, 0) == 1.0
    assert module.exact_mcnemar_pvalue(10, 0) < 0.01

### Source: `implementation_v001/run_verified_budget_control.py`

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run the independent oracle before the budget-matched control."
    )
    parser.add_argument("--cases", required=True, type=Path)
    parser.add_argument("--oracle-output", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--report-output", required=True, type=Path)
    parser.add_argument("--metrics-output", required=True, type=Path)
    parser.add_argument("--experiment-id", required=True)
    parser.add_argument("--models", nargs="+", required=True)
    parser.add_argument("--prompt-regimes", nargs="+", required=True)
    parser.add_argument("--seeds", nargs="+", type=int, required=True)
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--temperature", type=float, default=0.2)
    parser.add_argument("--timeout-seconds", type=float, default=120.0)
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parent
    subprocess.run(
        [
            sys.executable,
            str(root / "independent_oracle.py"),
            "--cases",
            str(args.cases),
            "--output",
            str(args.oracle_output),
        ],
        check=True,
    )
    command = [
        sys.executable,
        str(root / "budget_matched_control.py"),
        "--cases",
        str(args.cases),
        "--output",
        str(args.output),
        "--report-output",
        str(args.report_output),
        "--metrics-output",
        str(args.metrics_output),
        "--experiment-id",
        args.experiment_id,
        "--models",
        *args.models,
        "--prompt-regimes",
        *args.prompt_regimes,
        "--seeds",
        *(str(seed) for seed in args.seeds),
        "--ollama-url",
        args.ollama_url,
        "--temperature",
        str(args.temperature),
        "--timeout-seconds",
        str(args.timeout_seconds),
    ]
    return subprocess.run(command, check=False).returncode


if __name__ == "__main__":
    raise SystemExit(main())

## 7. Known Limitations

### Source: `candidate_v001.md`

# 候选 v001：同预算工具结果变形脆弱性

## 核心对象

本候选不再把有限变形关系解释为真实证据采用。它测量一个更窄的现象：基线答对后，结构化工具字段与记录顺序的六臂变形是否比相同六调用预算下的完全重放更容易导致关系失败。

每行执行十次随机交织调用。六臂组为基线、任务相关等变、普通无关不变、答案形状诱饵不变、纯顺序不变和一次重放；六重放组为六次完全相同输入。两个组共享基线和第一次重放，各含六次调用。主要统计量是基线正确行上的配对风险差和精确 McNemar 不一致行检验。

## 当前经验状态

Formal `attempt-budget-control-008` 完成 360 行、3600 次调用、827968 个令牌，零调用错误，独立求解器 20/20，执行、指标和输出契约全部通过。188 个基线正确行中：

- 六臂失败 86，六重放失败 10；
- 仅六臂失败 76，仅重放失败 0，两者都失败 10；
- 配对超额失败率 0.40425531914893614，精确 McNemar 双侧 p 值 2.6469779601696886e-23；
- 剔除解析警告行后超额 0.40860215053763443；
- 三个种子和十八个模型—提示—种子分层全部为正。

结果不是全家族一致：`tier_score` 的六臂和六重放均失败 6/18，超额为 0。当前样本内六臂关系通过与六臂完整精确正确都为 102/188，未显示相对完整反事实标签的无真值增量。

## 旧主张的处理

`attempt-mutation-007` 的九策略 1.0 平衡准确率只保留为评估器内部校准；两个正类读取 `expected`，不能认证真实采用。`attempt-qwen-007` 的 86/187 是旧单次对六次描述事实，但存在预算暴露混杂。两条旧 Claim 均已降为 `scope_reduced`，新同预算 Claim 是唯一核心支持。

## 最近先行边界

LLMORPH 已把 36 个关系扩展到四个自然语言处理基准和超过 56 万次测试，METAL 已占据大模型黑盒变形测试的基本方法骨架；ReliabilityBench、CAIR、CVT-RL 和 PriVE-Tools 又覆盖智能体变形、反事实影响、工具输出扰动或证据提供问题。因此当前候选属于 `ANALOGICAL_REDUCTION`；可辩护增量只限于工具返回析因六臂、同预算六重放配对基线和当前冻结套件中的超额脆弱性现象。

## 扩大价值

下一步应在真实多步工具任务、跨供应商模型和独立关系标注上复现；加入未见、非共线变形与留出代理策略，并检验该信号能否在控制完整反事实正确性后预测独立终态、复核失败或修复收益。当前候选是一颗现象/评价种子，不是已完成的方法论文。

### Source: `audit_v001/seed_support_seed-audit-010.md`

# Seed 支撑事实审计 v001

> ADVISORY_ONLY：仅陈列可核查的机械或显式事实；不判断新颖性、科学充分性或交付结论。

- Run：`20260815_1818_run11`
- 截止时间：`2026-08-15T14:20:59.380877Z`
- Seed：`seed_v001.md`；SHA-256：`64fa745d2afc28dec5d848ec79a271935ff70715bb44ddc4776fd6e8abb722f5`
- Portfolio：`hypotheses_v001/portfolio.json`；SHA-256：`44cbca69d01bdbe9e0bec01cad1b1533d51aa6874e8bca5836ca70823026e9c3`
- Supporting attempts：`attempt-budget-control-008`

## 审计记录

| 类别 | 代码 | 事实 | 来源 |
|---|---|---|---|
| `finding` | `seed_snapshot` | 已读取当前 Seed 的精确字节身份。 | `seed_v001.md` |
| `finding` | `portfolio_snapshot` | 已读取 1 个 hypothesis 的当前 portfolio 身份。 | `hypotheses_v001/portfolio.json` |
| `finding` | `seed_hypothesis_reference_resolved` | Seed hypothesis 引用可解析：H001。 | `seed_v001.md`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `seed_claim_reference_resolved` | Seed Claim 引用可解析：claim-budget-matched-excess。 | `seed_v001.md`<br>`hypotheses_v001/falsification/plan-h001-v001.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-001 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-001` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-001 记录了来源降级。 | `hypotheses_v001/priors/prior-001/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-001 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-001/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-002 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-002` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-002 记录了来源降级。 | `hypotheses_v001/priors/prior-002/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-002 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-002/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-003 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-003` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-003 记录了来源降级。 | `hypotheses_v001/priors/prior-003/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-003 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-003/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-004 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-004` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-004 记录了来源降级。 | `hypotheses_v001/priors/prior-004/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-004 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-004/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-005 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-005` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-005 记录了来源降级。 | `hypotheses_v001/priors/prior-005/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-005 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-005/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-006 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-006` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-006 记录了来源降级。 | `hypotheses_v001/priors/prior-006/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-006 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-006/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-007 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-007` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-007 记录了来源降级。 | `hypotheses_v001/priors/prior-007/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-007 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-007/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-008 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-008` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-008 记录了来源降级。 | `hypotheses_v001/priors/prior-008/request.json` |
| `warning` | `prior_hypothesis_snapshot_stale` | 最近先行审计 prior-008 的 hypothesis/portfolio 身份不是当前字节。 | `hypotheses_v001/priors/prior-008/request.json`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `prior_audit_material_present` | 最近先行审计 prior-009 含时间、查询和候选材料。 | `hypotheses_v001/priors/prior-009` |
| `warning` | `prior_audit_degraded` | 最近先行审计 prior-009 记录了来源降级。 | `hypotheses_v001/priors/prior-009/request.json` |
| `warning` | `attempt_spec_parity_different` | supporting attempt attempt-budget-control-008 的 Spec parity 维度 model_provider_revision 显式为 different。 | `experiment_v001/attempts/attempt-budget-control-008/spec.json#/parity_dimensions/model_provider_revision` |
| `finding` | `supporting_attempt_bound` | supporting attempt attempt-budget-control-008 绑定了可核验的 Spec、Claim 列表与 metrics 快照。 | `experiment_v001/attempts/attempt-budget-control-008/execution.json`<br>`experiment_v001/attempts/attempt-budget-control-008/spec.json`<br>`experiment_v001/attempts/attempt-budget-control-008/metrics.json` |
| `finding` | `independent_claim_validation_present` | 存在显式绑定为 independent_claim_validation 的有效 supporting attempt。 | `experiment_v001/attempts/attempt-budget-control-008/spec.json` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 0 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-budget-control-008/metrics.json#/records/1/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 1 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-budget-control-008/metrics.json#/records/2/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 2 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-budget-control-008/metrics.json#/records/0/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 3 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-budget-control-008/metrics.json#/records/3/value` |
| `warning` | `seed_numeric_literals_unmapped` | Seed 正文含未被成功显式映射的可见数字。 | `seed_v001.md` |

## 可追踪事实

```json
{
  "comparisons": [],
  "declared_claim_ids": [
    "claim-budget-matched-excess"
  ],
  "declared_hypothesis_ids": [
    "H001"
  ],
  "independent_claim_validation_attempt_ids": [
    "attempt-budget-control-008"
  ],
  "prior_audits": [
    {
      "age_days": 0.16488861015046297,
      "audit_id": "prior-001",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T10:23:33.004960Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-001",
      "queries": [
        "counterfactual tool output perturbation LLM agent tool result utilization causal sensitivity metamorphic testing"
      ]
    },
    {
      "age_days": 0.1424753929050926,
      "audit_id": "prior-002",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T10:55:49.506930Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-002",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    },
    {
      "age_days": 0.10802428868055557,
      "audit_id": "prior-003",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T11:45:26.082335Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-003",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    },
    {
      "age_days": 0.08333402262731482,
      "audit_id": "prior-004",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T12:20:59.321322Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-004",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    },
    {
      "age_days": 0.05761551530092592,
      "audit_id": "prior-005",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T12:58:01.400355Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-005",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    },
    {
      "age_days": 0.05382060505787036,
      "audit_id": "prior-006",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T13:03:29.280600Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-006",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    },
    {
      "age_days": 0.0037263453125,
      "audit_id": "prior-007",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T14:15:37.424642Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-007",
      "queries": [
        "large language model metamorphic testing equal budget repeated calls tool output field perturbation paired reliability"
      ]
    },
    {
      "age_days": 0.0023601254166666667,
      "audit_id": "prior-008",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T14:17:35.466041Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-008",
      "queries": [
        "large language model metamorphic testing equal budget repeated calls tool output field perturbation paired reliability"
      ]
    },
    {
      "age_days": 0.0017469053009259259,
      "audit_id": "prior-009",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T14:18:28.448259Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-009",
      "queries": [
        "large language model metamorphic testing equal budget repeated calls tool output field perturbation paired reliability"
      ]
    }
  ],
  "supporting_attempts": [
    {
      "attempt_id": "attempt-budget-control-008",
      "claim_ids": [
        "claim-budget-matched-excess"
      ],
      "execution_sha256": "8d5310053883d750427eb129d19907e5c09d7a7093b2ffc98b393c75feb967df",
      "hypothesis_id": "H001",
      "metric_record_count": 4,
      "metrics_sha256": "957374383425a86e3f1e9b91b84af4de6aad1fa06fe1cb23c44016c5262e3a2b",
      "purpose": "independent_claim_validation",
      "schema_version": 8,
      "sources": [
        "experiment_v001/attempts/attempt-budget-control-008/execution.json",
        "experiment_v001/attempts/attempt-budget-control-008/spec.json",
        "experiment_v001/attempts/attempt-budget-control-008/metrics.json"
      ],
      "spec_sha256": "82b9110e4c2f144c3eddc40866663dec7ae0367d23a5d43861d687bd2c11c485"
    }
  ]
}
```

## 机械权限边界

本材料不改变 Claim 或 hypothesis 状态，不改变三位 Reviewer、同字节哈希链或主研究者裁决权。

## Final Core Evidence Closure (machine generated, bounded)

This appendix exposes selected Formal Spec, Claim and metric facts; it does not judge scientific sufficiency.
Closure SHA-256: `87539af330bee561224aa71607c39ce9381151ba5444828db605611949147e23`

```json
{
  "artifact_kind": "final_core_evidence_closure",
  "attempts": [
    {
      "attempt_id": "attempt-budget-control-008",
      "execution_schema_version": 8,
      "execution_sha256": "8d5310053883d750427eb129d19907e5c09d7a7093b2ffc98b393c75feb967df",
      "metrics": {
        "errors": {
          "items": [],
          "omitted_count": 0,
          "total_count": 0
        },
        "experiment_id": "exp-budget-control-v008",
        "included_record_count": 4,
        "omitted_record_count": 0,
        "primary_metric_selection_priority": "budget_matched_excess_failure_rate",
        "record_count": 4,
        "records": [
          {
            "aggregation": "paired_risk_difference",
            "n": 188,
            "name": "budget_matched_excess_failure_rate",
            "source_index": 0,
            "split": "base_correct_rows",
            "unit": "ratio",
            "value": 0.40425531914893614
          },
          {
            "aggregation": "mean",
            "n": 188,
            "name": "transform_failure_rate",
            "source_index": 1,
            "split": "base_correct_rows",
            "unit": "ratio",
            "value": 0.4574468085106383
          },
          {
            "aggregation": "mean",
            "n": 188,
            "name": "repeat_control_failure_rate",
            "source_index": 2,
            "split": "base_correct_rows",
            "unit": "ratio",
            "value": 0.05319148936170213
          },
          {
            "aggregation": "exact_two_sided",
            "n": 76,
            "name": "exact_mcnemar_pvalue",
            "source_index": 3,
            "split": "base_correct_rows",
            "unit": "probability",
            "value": 2.6469779601696886e-23
          }
        ],
        "resource_usage": {
          "api_calls": 3600,
          "estimated_cost": 0.0,
          "gpu_time_seconds": "unknown",
          "tokens": 827968,
          "wall_time_seconds": 1595.3243782999998
        },
        "warnings": {
          "items": [
            "ollama::qwen2.5:7b::weak::seed-456/tier_score_01/order_only: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::weak::seed-456/tier_score_01/repeat_3: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::weak::seed-456/tier_score_01/repeat_5: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::weak::seed-456/tier_score_02/base: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::weak::seed-456/tier_score_02/repeat_4: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_00/repeat_4: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_00/repeat_5: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_00/repeat_2: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_00/base: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_00/repeat_1: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_00/order_only: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_00/irrelevant_plain: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_00/repeat_3: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_01/repeat_2: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_01/order_only: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_01/repeat_5: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_01/repeat_1: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_01/repeat_3: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_01/repeat_4: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_01/base: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_01/irrelevant_adversarial: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_01/irrelevant_plain: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_02/irrelevant_plain: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_02/repeat_3: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_02/repeat_5: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_02/repeat_4: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_02/repeat_2: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/tier_score_02/base: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_00/repeat_2: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_00/repeat_5: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_00/repeat_1: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_00/repeat_4: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_00/order_only: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_00/irrelevant_plain: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_00/repeat_3: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_00/base: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_01/repeat_2: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_01/irrelevant_plain: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_01/repeat_4: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_01/repeat_1: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_01/repeat_5: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_01/order_only: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_01/repeat_3: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_02/relevant: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-456/tier_score_02/irrelevant_plain: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-789/tier_score_00/repeat_5: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-123/tier_score_02/irrelevant_plain: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-456/tier_score_02/order_only: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-456/tier_score_02/base: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-456/tier_score_02/repeat_3: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-456/tier_score_02/repeat_1: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-456/tier_score_02/repeat_5: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-456/tier_score_02/irrelevant_plain: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-456/tier_score_02/repeat_2: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-456/tier_score_02/repeat_4: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-789/tier_score_02/repeat_2: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-789/tier_score_02/repeat_3: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-789/tier_score_02/order_only: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-789/tier_score_02/repeat_1: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-789/tier_score_02/repeat_4: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-789/tier_score_02/repeat_5: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-789/tier_score_02/base: response was not a JSON object with an answer key"
          ],
          "omitted_count": 0,
          "total_count": 62
        }
      },
      "metrics_path": "experiment_v001/attempts/attempt-budget-control-008/metrics.json",
      "metrics_sha256": "957374383425a86e3f1e9b91b84af4de6aad1fa06fe1cb23c44016c5262e3a2b",
      "spec": {
        "claim_ids": {
          "items": [
            "claim-budget-matched-excess"
          ],
          "omitted_count": 0,
          "total_count": 1
        },
        "dataset": "五个确定性结构化工具任务族、每族四例、共二十例；四个字段臂共享记录排列，纯顺序臂使用字段相同的无固定点循环排列。",
        "experiment_id": "exp-budget-control-v008",
        "falsification_rule": "任一预声明签名不满足，则‘干预特异的额外关系失败’主张不支持；不得用原 86/187 单次对六次结果绕过同预算对照，也不得据正结果声称真实采用机制或部署外推。",
        "hypothesis_id": "H001",
        "independent_ground_truth": {
          "description": "独立家族求解器从原始工具字段重算基线及五个源变体的精确答案和关系语义，不导入本对照程序；正式运行前必须 20/20 通过。两组共享同一基线和一次重放，组内六调用预算严格相等。",
          "external_card_ids": {
            "items": [],
            "omitted_count": 0,
            "total_count": 0
          },
          "external_evidence_ids": {
            "items": [],
            "omitted_count": 0,
            "total_count": 0
          },
          "external_literature_refs": {
            "items": [
              "P039",
              "P040",
              "P097"
            ],
            "omitted_count": 0,
            "total_count": 3
          },
          "run_local_fact_refs": {
            "items": [
              "implementation_v001/independent_oracle.py",
              "implementation_v001/cases.json",
              "review_v001/evaluations/eval-0005/EMP/report.json"
            ],
            "omitted_count": 0,
            "total_count": 3
          }
        },
        "model": "qwen2.5:7b、qwen3:4b、qwen3:8b；严格与弱两种提示制度。",
        "primary_metric": "budget_matched_excess_failure_rate",
        "provider": "本机 Ollama 服务；模型与服务身份由正式执行记录和本机清单绑定。",
        "purpose": "independent_claim_validation",
        "research_question": "在相同六调用预算下，六臂字段/顺序变形是否比六次完全相同重放产生显著且分层稳定的额外失败？",
        "revision": "reviewer-killer-1 equal-budget paired ten-call protocol, full-manifest binding",
        "sampling_unit": "模型 × 提示制度 × 种子 × 冻结案例，共 360 行；每行十次随机交织调用，同时形成共享基线和 repeat_1 的两个六调用组。",
        "secondary_metrics": {
          "items": [
            "transform_failure_rate",
            "repeat_control_failure_rate",
            "exact_mcnemar_pvalue",
            "transform_only_fail",
            "control_only_fail",
            "parse_warning_excluded_excess_failure_rate",
            "positive_seed_count",
            "positive_stratum_count"
          ],
          "omitted_count": 0,
          "total_count": 8
        }
      },
      "spec_path": "experiment_v001/attempts/attempt-budget-control-008/spec.json",
      "spec_sha256": "82b9110e4c2f144c3eddc40866663dec7ae0367d23a5d43861d687bd2c11c485"
    }
  ],
  "bounds": {
    "finding_records": 64,
    "list_items_per_field": 64,
    "metric_records_per_attempt": 64,
    "raw_code_stdout_stderr_included": false,
    "text_characters_per_field": 1024
  },
  "mechanical_effects": {
    "checks_explicit_mapping_truth": true,
    "makes_scientific_sufficiency_judgment": false,
    "requires_all_seed_numbers_mapped": false
  },
  "related_comparisons": [],
  "run_id": "20260815_1818_run11",
  "schema_version": 1,
  "seed": {
    "path": "seed_v001.md",
    "sha256": "64fa745d2afc28dec5d848ec79a271935ff70715bb44ddc4776fd6e8abb722f5"
  },
  "seed_evidence": {
    "explicit_metric_mapping_count": 4,
    "finding_count": 5,
    "findings": [
      {
        "code": "seed_metric_mapping_resolved",
        "details": {
          "json_pointer": "/records/1/value",
          "mapping_index": 0,
          "seed_value": 0.4574468085106383,
          "source_path": "experiment_v001/attempts/attempt-budget-control-008/metrics.json",
          "source_value": 0.4574468085106383
        },
        "kind": "finding",
        "message": "数字映射 0 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-budget-control-008/metrics.json#/records/1/value"
          ],
          "omitted_count": 0,
          "total_count": 2
        }
      },
      {
        "code": "seed_metric_mapping_resolved",
        "details": {
          "json_pointer": "/records/2/value",
          "mapping_index": 1,
          "seed_value": 0.05319148936170213,
          "source_path": "experiment_v001/attempts/attempt-budget-control-008/metrics.json",
          "source_value": 0.05319148936170213
        },
        "kind": "finding",
        "message": "数字映射 1 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-budget-control-008/metrics.json#/records/2/value"
          ],
          "omitted_count": 0,
          "total_count": 2
        }
      },
      {
        "code": "seed_metric_mapping_resolved",
        "details": {
          "json_pointer": "/records/0/value",
          "mapping_index": 2,
          "seed_value": 0.40425531914893614,
          "source_path": "experiment_v001/attempts/attempt-budget-control-008/metrics.json",
          "source_value": 0.40425531914893614
        },
        "kind": "finding",
        "message": "数字映射 2 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-budget-control-008/metrics.json#/records/0/value"
          ],
          "omitted_count": 0,
          "total_count": 2
        }
      },
      {
        "code": "seed_metric_mapping_resolved",
        "details": {
          "json_pointer": "/records/3/value",
          "mapping_index": 3,
          "seed_value": 2.6469779601696886e-23,
          "source_path": "experiment_v001/attempts/attempt-budget-control-008/metrics.json",
          "source_value": 2.6469779601696886e-23
        },
        "kind": "finding",
        "message": "数字映射 3 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-budget-control-008/metrics.json#/records/3/value"
          ],
          "omitted_count": 0,
          "total_count": 2
        }
      },
      {
        "code": "seed_numeric_literals_unmapped",
        "details": {
          "numeric_literal_count": 27,
          "numeric_literals": [
            "40.43",
            "0.10",
            "0.05",
            "360",
            "3600",
            "188",
            "76",
            "0",
            "10",
            "186",
            "84",
            "8",
            "0.40860215053763443",
            "0.4127",
            "0.4032",
            "0.3968",
            "1.0",
            "0.8571",
            "0.7607",
            "36",
            "56",
            "40.43",
            "0.4043",
            "0",
            "0",
            "12",
            "62"
          ],
          "omitted_numeric_literal_count": 0
        },
        "kind": "warning",
        "message": "Seed 正文含未被成功显式映射的可见数字。",
        "sources": {
          "items": [
            "seed_v001.md"
          ],
          "omitted_count": 0,
          "total_count": 1
        }
      }
    ],
    "mapping_integrity_error_count": 0,
    "mapping_integrity_valid": true,
    "omitted_finding_count": 0
  },
  "selected_supporting_attempt_ids": [
    "attempt-budget-control-008"
  ],
  "version": "v001"
}
```

## Evidence Inventory (machine generated)

```json
{
  "comparison_count": 0,
  "comparisons": [],
  "formal_attempt_count": 13,
  "formal_attempts": [
    {
      "association": "MATCH",
      "attempt_id": "attempt-budget-control-008",
      "path": "experiment_v001/attempts/attempt-budget-control-008/execution.json",
      "read_error": null,
      "record_sha256": "8d5310053883d750427eb129d19907e5c09d7a7093b2ffc98b393c75feb967df",
      "schema_version": 8,
      "selected_in_core": true,
      "status": "SUCCESS",
      "valid_review_support": true
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-mutation-002",
      "path": "experiment_v001/attempts/attempt-mutation-002/execution.json",
      "read_error": null,
      "record_sha256": "06ee4d2bc685535a07d197a22cab1698f8819f3f286500fc7db73485a7f9941b",
      "schema_version": 8,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": false
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-mutation-003",
      "path": "experiment_v001/attempts/attempt-mutation-003/execution.json",
      "read_error": null,
      "record_sha256": "ec6df59e59fb367f4493492c8ab5281416588b9d571e2b2ec259a937706e13f8",
      "schema_version": 8,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": false
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-mutation-004",
      "path": "experiment_v001/attempts/attempt-mutation-004/execution.json",
      "read_error": null,
      "record_sha256": "9385d64776f9433a0e5a1a566b5b6ec83c9c736647eb7637e2b7261641553d51",
      "schema_version": 8,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": false
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-mutation-005",
      "path": "experiment_v001/attempts/attempt-mutation-005/execution.json",
      "read_error": null,
      "record_sha256": "1a051684c839f010ab95ae2e6e6339a03c8ac33e490779ed3bf280f88f951100",
      "schema_version": 8,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": false
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-mutation-006",
      "path": "experiment_v001/attempts/attempt-mutation-006/execution.json",
      "read_error": null,
      "record_sha256": "8eeb16569a1e493efba78b53955dc9584037ca903cee0baf2ab0616fc9b77de4",
      "schema_version": 8,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": false
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-mutation-007",
      "path": "experiment_v001/attempts/attempt-mutation-007/execution.json",
      "read_error": null,
      "record_sha256": "83d22699d11ec657567a24703a9e2b9685b355dac9d98e948ebf9a35e0b352b9",
      "schema_version": 8,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": true
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-qwen-002",
      "path": "experiment_v001/attempts/attempt-qwen-002/execution.json",
      "read_error": null,
      "record_sha256": "ce02aafd2a8a864cf51e2951d81d63e2e5c77457a7aa1ba979d307b7bc9d9e1e",
      "schema_version": 8,
      "selected_in_core": false,
      "status": "FAILED",
      "valid_review_support": false
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-qwen-003",
      "path": "experiment_v001/attempts/attempt-qwen-003/execution.json",
      "read_error": null,
      "record_sha256": "00adfb51e8333e3c81abc3a2e994d323ef446be0dba58b07253374d2981cf2cc",
      "schema_version": 8,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": false
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-qwen-004",
      "path": "experiment_v001/attempts/attempt-qwen-004/execution.json",
      "read_error": null,
      "record_sha256": "2d0d12838154fdf9d636fd133ba6d0e2d6805c2ff1eaf9b9ccead65daf101579",
      "schema_version": 8,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": false
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-qwen-005",
      "path": "experiment_v001/attempts/attempt-qwen-005/execution.json",
      "read_error": null,
      "record_sha256": "699c57ef7da657ad599edf52ea07c69689832f082934d2d9a6b3205b2e3eba61",
      "schema_version": 8,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": false
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-qwen-006",
      "path": "experiment_v001/attempts/attempt-qwen-006/execution.json",
      "read_error": null,
      "record_sha256": "dfcf55c8d527ce53f2cc858002f7a87f0ae8c9ea0257fbc4399deaa9a077f180",
      "schema_version": 8,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": false
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-qwen-007",
      "path": "experiment_v001/attempts/attempt-qwen-007/execution.json",
      "read_error": null,
      "record_sha256": "509edd3221b5f92df179648fd8ade17a63fb98d2df212389631dec8831de754f",
      "schema_version": 8,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": true
    }
  ],
  "implementation_key": "8d4b260c29a16166f69a628cc457cd675d2815b6782a376f82dcd2f27f2fe60b",
  "machine_judgment": "NONE_FACTS_ONLY",
  "recorded_attempt_count": 0,
  "recorded_attempts": [],
  "schema_version": 1,
  "version": "v001"
}
```
