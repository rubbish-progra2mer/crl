# CRL Fixed Review Packet

- Contract: 3
- Scientific version: v001
- Evaluator: CRL-EVAL-1.0
- Evaluator definition SHA-256: e0d35083b1427e9f8861ba576304b97657498fee46480d5e07e8e0b02cea6e5b
- Implementation key: ea8ee57c26c507a7b99fbad0494a497a59a95937d385b265294ba5727ff492d9
- Implementation manifest SHA-256: ea8ee57c26c507a7b99fbad0494a497a59a95937d385b265294ba5727ff492d9
- Evidence inventory SHA-256: e41fcc62d4059bd7243f3b16b8d0506295701805014d7cf46cdbc1971491ce4d

## 1. Implementation / Seed Overview

### Source: `seed_v001.md`

# 研究种子 v001：双向变形证据采用探针

## 一句话种子

把结构化工具返回中的任务相关字段与无关字段分别做受控影子变形，以“任务定向等变 + 普通无关不变 + 答案形状诱饵不变 + 精确重放稳定”诊断黑盒工具智能体的选择性证据采用，并与单次正确性组成四象限，从而暴露一次答对仍可能掩盖的关系脆弱性。

## 问题与价值

终局正确率、工具调用率和自然轨迹引用都不能可靠区分三种情况：智能体真正采用任务相关工具结果、调用后忽略结果、或依赖无关但答案形状相似的字段。环境终态可检查时应优先使用终态，但大量信息查询与开放式任务缺少完整后条件。需要一个黑盒补充诊断，回答“输出是否按任务规定的方式选择性响应工具证据”，而不是再次生成一个自我报告或语言模型裁判分数。

共享论文知识库中的 ToolFailBench（P039）表明汇总任务正确率会掩盖工具跳过与结果忽略；False Success（P040）表明自报完成可与环境真值分离；ReLoop（P097）与 Verus-SpecGym（P099）分别支持受控行为扰动和双向可执行检查的诊断价值。这些证据只构成问题与机制入口，不直接证明本种子。

## 真实计算变化

每个案例冻结任务、工具模式、提示制度和解码设置，执行五次调用：

1. 基线工具返回；
2. 只改变任务相关值，并预声明输出应满足的标识双射或数值平移；
3. 只改变普通装饰性无关字段，输出应不变；
4. 只改变答案形状相似的无关诱饵，输出应不变；
5. 完全复制基线，输出应稳定。

联合通过要求第二次回答满足任务定向关系，第三、四、五次回答等于基线回答。每个案例因此需要五次调用。实现保留原始回答、解析警告、调用资源与逐例关系，独立家族求解器从原始工具字段重算四个变体的精确答案和关系语义，不导入主评估器或生成器。

## 与最近先行的最小差分

- METAL 已把变形关系系统用于大模型黑盒质量评价，并覆盖输入扰动、相等/距离关系和相同输入重复；因此本种子不主张发明大模型变形测试。
- CAIR 已通过反事实替换智能体输出测量多智能体工作流影响；本种子不做影响排序，而要求工具字段变化满足任务规定的输出关系。
- ReliabilityBench 已把动作变形关系用于智能体可靠性；其主要干预任务/用户输入与执行行为，本种子干预已经返回的结构化工具字段并观察最终答案采用。
- CVT-RL 已直接包含工具输出扰动，用冻结续写策略和可验证终局奖励估计训练信用；本种子不训练模型、不依赖终局奖励，以黑盒关系形成诊断。
- PriVE-Tools 已显示提供受控视觉工具证据不保证模型使用证据；本种子承接该宽现象，但增加字段级任务等变、两类无关不变与正确性四象限。

因此，保留的贡献增量不是通用反事实或变形思想，而是一个针对结构化工具返回采用的关系组合、突变判别协议及可复现实验现象。若未来先行已实现同一组合和诊断目标，应降级。

## 可证伪 Claim

### Claim 1：任务定向关系的新增判别力

在五个确定性任务族、二十个各变体独立打乱记录顺序的冻结案例与九种预声明策略上，联合关系应比“相关答案发生任意变化”和“相关变化加两类无关不变”更准确地区分稳定选择性采用。正标签包括正确采用与错误但等变采用；只在完全重复时改变答案、固定返回第一条标识、固定返回第三条标识三种专门反例分别检验重放稳定性与位置代理。

Formal `attempt-mutation-006` 中，任务定向双向关系平衡准确率为 1.0；选择性变化基线为 0.8571428571428572；任意相关变化为 0.7107142857142857。错误但等变策略 20/20 通过，方向错误、只在完全重复时不稳定、固定第一位置和固定第三位置策略均 0/20 通过联合关系。预注册判据“至少 0.95 且比第二基线至少高 0.05”得到局部支持。

### Claim 2：单次成功关系脆弱性

在三个本地模型、两种提示制度、二十个冻结案例上，单次精确正确不足以保证任务定向、抗无关诱饵且可重放的采用结构。

Formal `attempt-qwen-006` 在三个种子和随机调用顺序下完成 1800 次调用。187 个单次精确正确行有 83 个联合关系失败，脆弱率为 0.44385026737967914，行级 Wilson 95% 描述性区间为 [0.3745, 0.5155]。83 个失败均无解析警告，三个种子均非零，十八个模型—提示—种子分层中十六个非零。另有 3 个单次错误但联合关系通过的真实行：同一模型在三个种子中只使用严重度、漏掉奖励项，却保持相关数值平移。该比例只描述本地冻结合成套件；不能外推为部署失败率。

## 正确性 × 采用关系四象限

| 单次正确性 | 联合关系 | 解释边界 |
|---|---|---|
| 对 | 通过 | 样本内正确且采用结构稳定 |
| 对 | 失败 | 一次答对但关系脆弱，是本版本观察到的核心现象 |
| 错 | 通过 | 系统性但错误的等变采用；探针不能纠正它 |
| 错 | 失败 | 错误且没有稳定选择性采用证据 |

正式真实模型套件观察到 3 个“错且通过”，确定性错误但等变策略还提供了构造反例。因此联合关系不能单独称为正确性验证器；它只说明回答遵守预声明采用关系。

## 贡献向量

- **问题/现象**：把“工具证据已经提供”与“单次答对时仍未稳定采用”分开；正式样本内观察到 83/187 的关系脆弱性，并跨三个种子复现。
- **机制/计算**：相关字段使用任务定向等变，而非只看变化；普通无关、答案形状诱饵与精确重放分别隔离三类伪影。
- **智能体特有约束**：干预位置在工具结果进入上下文之后、最终回答之前，面向结构化工具返回而非普通用户输入扰动。
- **评价/基准**：九种突变策略、独立记录/调用顺序控制与正确性×关系四象限共同规定信号边界。
- **经验发现**：脆弱性出现在三个种子和十六个模型—提示—种子分层；位置修复后四个有单次正确样本的任务族均出现失败，但数值求和族没有单次正确分母。
- **理论/分析**：错误但等变策略构成反例，证明关系采用与答案正确性不可同一化。
- **系统能力**：当前实现是可重复的本地评价载体，尚不是在线门控或修复系统。

## 局限与最大剩余疑问

1. METAL 对一般方法形式构成强类比归约；当前组合是否足以形成 CCF-B 级评价方法贡献，仍需固定评审和更大规模研究判断。
2. 二十个案例均为合成短答案任务，关系由研究者手工规定；独立求解器只保证套件自洽，不提供外部有效性。
3. `filtered_argmin` 与 `latest_confirmed` 仍贡献 61/83 个失败；`count_open` 与 `tier_score` 也出现失败，但 `valid_sum` 没有单次正确样本，任务覆盖仍不均衡。
4. 三个模型来自相近本地模型谱系；三个种子只提供有限复现维度，没有跨供应商或可靠的聚类不确定性。
5. 每案例五次调用的成本明显高于单次正确率；尚未证明诊断收益在复杂真实轨迹中抵得过预算。
6. 当前最大的剩余疑问不是“信号能否区分已知突变”，而是它能否在真实多步工具轨迹上提供超出通用变形测试与完整正确性标签的可操作信息。
7. 首轮固定评审发现旧实现漏合取完全重复稳定性；第二轮发现固定记录位置代理。第四、第五版结果均撤出支持链；第六版通过重放反例、独立记录顺序和两种位置策略修复，但这些历史说明合成评价很容易被未建模代理击穿。
8. 联合关系与完整四变体正确性不再完全重合（107/360 对 104/360），但尚无独立终态证明关系信号对复核失败、真实错误或修复收益具有增量预测力。

## 值得扩大的验证

下一阶段应冻结更广的真实多步工具任务本体：检索选择、聚合、状态过滤、多工具连接和开放式证据综合；加入跨供应商模型；由独立标注者定义字段相关性和变形关系；在相同五调用预算下与完整反事实正确性、METAL 风格关系、CAIR 风格影响分数、终局正确率及 ToolFailBench 分类比较。最关键的扩大判据是：四象限能否在控制完整正确性后增量预测复核失败、修复收益或真实终态错误。

<!-- CRL_SEED_SUPPORT_META {"schema_version":1,"hypothesis_ids":["H001"],"claim_ids":["claim-mutation-discrimination","claim-one-shot-brittleness"],"falsified_claim_dispositions":[],"metric_mappings":[{"seed_text":"任务定向双向关系平衡准确率为 1.0","seed_value":1.0,"source_path":"experiment_v001/attempts/attempt-mutation-006/metrics.json","json_pointer":"/records/0/value"},{"seed_text":"选择性变化基线为 0.8571428571428572","seed_value":0.8571428571428572,"source_path":"experiment_v001/attempts/attempt-mutation-006/metrics.json","json_pointer":"/records/1/value"},{"seed_text":"任意相关变化为 0.7107142857142857","seed_value":0.7107142857142857,"source_path":"experiment_v001/attempts/attempt-mutation-006/metrics.json","json_pointer":"/records/2/value"},{"seed_text":"脆弱率为 0.44385026737967914","seed_value":0.44385026737967914,"source_path":"experiment_v001/attempts/attempt-qwen-006/metrics.json","json_pointer":"/records/0/value"}]} -->

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

### Source: `hypotheses_v001/priors/prior-004/assessment.md`

# 最近先行科研解释

> 本文件属于主研究者解释，可在阅读候选、PDF、Evidence 和实验后继续修订；它不进入机器事实快照哈希。

- 审计标识：`prior-004`
- 碰撞类型：`ANALOGICAL_REDUCTION`

## 真正的 nearest prior

1. **METAL**（候选 `prior-05ce3bdb71373092`，arXiv:2312.06056）是方法形式上最近的先行：它把变形关系定义为大模型质量评价模块，覆盖输入扰动后的相等/不等、生成任务距离关系以及相同输入重复的一致性。它否定“首次把变形测试用于大模型黑盒评价”这一宽主张。
2. **CAIR**（EMNLP 2025，ACL Anthology 2025.emnlp-main.958）是反事实影响目标上最近的先行：它替换多智能体工作流中的智能体输出，度量对最终结果及工作流的影响并排序，但不要求任务条件输出关系。
3. **CVT-RL**（arXiv:2606.05263）直接包含工具输出扰动，不过目标是在冻结续写策略与可验证终局奖励下估计反事实贡献，用于强化学习信用分配，而不是黑盒评价关系。
4. **PriVE-Tools**（候选 `prior-527e3aefa70e58f2`，arXiv:2607.16311）在现象上很接近：它冻结问题、正确答案、偏置答案与评分规则，只改变工具证据视图，发现提供相关工具证据不保证模型使用证据；其主要指标是正确率和先验跟随错误率，没有对结构化工具返回字段建立任务条件等变/不变关系。
5. **ReliabilityBench**（arXiv:2601.06112）使用动作变形关系、任务扰动、终态等价和故障注入评价智能体可靠性；主要干预入口是任务/用户输入和执行行为，而非已返回工具字段的最终回答采用。

## 实质组件重合

- 与 METAL 重合：黑盒多次执行、输入扰动、相等/距离关系、相同输入重复、无需逐例完整输出标签的变形思想。
- 与 CAIR/CVT-RL 重合：通过受控反事实替换判断过程变量是否影响下游输出。
- 与 PriVE-Tools 重合：区分“证据已提供”和“模型确实依据证据作答”，并把证据条件作为受控变量。
- 与 ReliabilityBench 重合：把变形关系用于智能体可靠性而非普通静态分类器。

## 仍存贡献增量

- **干预位置**：只修改已返回的结构化工具字段，不改用户任务、工具选择、智能体消息或证据呈现方式。
- **关系语义**：相关字段要求满足任务规定的标识双射或数值平移，而非只要求输出不同；九策略突变测试排除了方向错误、重复不稳定和两种固定位置代理。
- **对照组合**：普通无关字段、答案形状诱饵字段、精确重放分别隔离装饰敏感、诱饵依赖与随机不稳定；四个源变体的记录顺序和每行五次调用顺序分别受控打乱。
- **诊断表达**：关系信号与独立正确性形成四象限；第六版真实模型出现三个错误但联合关系通过的行，直接显示采用关系与正确性不可同一化。
- **经验现象**：三种子 Formal 中，187 个单次正确行有 83 个联合关系失败，且三个种子均非零；可发表价值若存在，更可能来自正确性四象限及未来的增量预测，而非变形测试本身。

## 最危险替代解释

本候选可能只是 METAL 的工具场景实例，加上手工选择的关系、诱饵、重放与位置控制。第六版真实模型中联合关系与四变体完整正确性不再完全重合（107/360 对 104/360），但仍没有独立环境终态或修复收益证明增量价值；若未来不能在更广任务上显示超出通用变形基线和完整标签的可操作价值，方法贡献不足。另一个风险是合成任务把关系写得过于简单，失败只反映提示遵循或短答案解析，而非真实多步工具采用。

## 最小区分实验

1. 在独立打乱各变体记录顺序后，用固定返回第一/第三条标识的策略检验位置代理；两种策略的联合通过率必须为零。
2. 用方向错误但“相关变化且无关不变”的策略检验任务定向关系是否比一般变化/一致性关系多提供判别力。
3. 用只在完全重复时不稳定的策略检验实现是否真实合取重放稳定性。
4. 用独立家族求解器验证所有相关/无关变形的标签与语义，不读取主评估器标签。
5. 在三个本地模型、两种提示制度、三个种子和五个任务族上随机化调用顺序并正式复现“单次正确但关系失败”；若只集中于一个种子、少于六个分层或解析失败则不成立。

## 方法死亡后仍存现象

即使 METAL 或未来最近先行完全覆盖关系式方法，仍可能保留的现象是：工具型语言模型在一次答对时仍可能无法在任务等价的工具字段变形下保持方向正确与无关不变。第六版 Formal 在冻结本地套件观察到 83/187，并跨三个种子复现；但案例、模型谱系与任务形式仍强相关，因此只能作为值得扩大验证的受限种子，不能作为一般部署结论。

## 背景与身份未解决项

- 本次自动审计仍因 Semantic Scholar HTTP 429 而降级，候选来自 arXiv；CAIR、CVT-RL 与 ReliabilityBench 的身份和组件来自主研究者另行核对的论文原文，未进入本快照候选集合。
- PriVE-Tools 为 2026 年 7 月新预印本，同行评审状态未确认。
- 尚未发现完全匹配“结构化工具字段变形 + 任务定向等变 + 两类无关不变 + 精确重放 + 位置控制 + 正确性四象限”的论文，但这不是穷尽性证明。

## 3. Core Experimental Evidence

### Source: `experiment_v001/result.md`

# 正式实验结果 v001

## 证据资格

- 当前两轮评审修复后的完整实现清单匹配且有效的正式尝试：`attempt-mutation-006`、`attempt-qwen-006`，二者 `runner_exit_code=0`、`metrics_contract_ok=true`、`output_contract_ok=true`。
- `attempt-mutation-005` 与 `attempt-qwen-005` 虽修复了首轮评审发现的重复稳定性遗漏，但第二轮固定评审发现两个标识任务族存在固定答案位置代理，故也只保留作审计。第四版及更早尝试同样不进入最终支持链。
- 无效尝试：`attempt-qwen-002` 因包装器把 Ollama 根路径误作聊天端点，600 个请求均返回 HTTP 405，`runner_exit_code=2`；它只作为失败记录，不支持任何科研主张。
- 正式模型身份：Ollama 0.32.13；`qwen2.5:7b` 摘要 `845dbda0ea48`，`qwen3:4b` 摘要 `359d7dd4bcda`，`qwen3:8b` 摘要 `500a1f067a9f`。

## 独立标签校验

两个有效尝试都先执行独立家族求解器。它不读取 `expected` 作为求解输入，也不导入生成器或主评估器；二十个案例全部满足重算标签、相关关系与两类无关不变条件，20/20 通过。该校验只证明合成套件自洽。

## Claim 1：突变判别

正式尝试 `attempt-mutation-006` 共 180 个案例—策略行，无外部模型调用。四个源变体的记录顺序分别独立打乱；九种策略除既有七种外，新增固定返回第一条和第三条记录标识的两种位置代理。

| 信号 | 平衡准确率 |
|---|---:|
| 相关答案发生任意变化 | 0.7107 |
| 相关变化 + 两类无关不变 | 0.8571 |
| 任务定向双向关系 | 1.000 |

预注册门槛为联合关系至少 0.95，且比第二基线至少高 0.05；实际高 0.1429。错误但等变策略 20/20 通过，方向错误与只在重复时不稳定的策略均 0/20 通过联合关系。固定第一位置、固定第三位置策略各 0/20 通过；前者相关关系偶然通过 1/20，后者 2/20，但都被完整联合条件拒绝。这支持“任务定向关系、无关不变与重放稳定共同提供额外采用结构判别”，同时否定把信号解释为答案正确性。

## Claim 2：单次成功关系脆弱性

正式尝试 `attempt-qwen-006` 完成 1800 次本地调用、411,403 个令牌、360 个模型—提示—种子—案例行，无调用错误，出现 7 条结构化输出解析警告。三个种子为 123、456、789，温度为 0.2；每行五个变体的调用顺序独立打乱，共观察到 115 种不同顺序。

- 187 行基线答案单次精确正确，其中 83 行未通过联合关系；脆弱率为 44.39%。
- 行级二项比例的 Wilson 95% 描述性区间为 [37.45%, 51.55%]；行共享案例与模型谱系，不能视为完全独立样本。
- 83 个关系失败均没有解析警告；因此剔除解析警告后仍为 83/187。
- 三个种子均出现非零失败：种子 123 为 26/62，456 为 29/63，789 为 28/62；十八个模型—提示—种子分层中十六个非零，超过预注册门槛。
- 合并种子后的分层失败计数：qwen2.5:7b 严格 11/18、弱 11/15；qwen3:4b 严格 27/36、弱 27/39；qwen3:8b 严格 6/36、弱 1/43。
- 在 187 个单次正确行中，任务相关关系失败 32 行、普通无关字段不变失败 28 行、答案形状诱饵不变失败 49 行、精确重放不稳定 1 行；各类型可重叠。
- 按任务族，失败为 `filtered_argmin` 28/60、`latest_confirmed` 33/66、`count_open` 18/48、`tier_score` 4/13；`valid_sum` 没有单次正确行，无法估计其条件脆弱率。位置修复后现象不再只由两个标识任务族构成，但任务异质性仍强。

预注册总体门槛为至少 0.10、解析警告剔除后仍非零、至少三个分层出现；三项均通过。结论只支持“冻结本地合成套件中，单次答对可能掩盖关系脆弱性”，不支持真实部署失败率或所有工具任务的一般性。

## 负面与边界结果

- 观察到 3 个“单次错误但联合关系通过”的行，均为 qwen3:4b 弱提示在 `tier_score_02` 的三个种子：模型稳定输出基础 `2`、相关 `4`，正确答案应为 `14`、`16`。它只采用了严重度并遗漏奖励项，却保持预声明数值平移。这是关系采用与正确性不可同一化的真实反例。
- 当前套件联合关系通过 107/360，完整四变体精确正确 104/360；两者不再完全重合，但尚未证明关系信号对独立环境终态或修复收益有增量预测价值。
- 187 个单次正确行中只有 1 行精确重放不稳定；重放项的经验增量仍很小，主要价值是定义与反例完整性。
- 三个种子提供了复现维度，但相同案例、相近模型谱系和确定性提示结构导致强相关；不能据此给出可靠部署率方差。

## 当前判断

两轮评审修复后的两条局部主张均获得第六版 Formal 支持，但方法新颖性仍受 METAL、CAIR、ReliabilityBench、CVT-RL 与 PriVE-Tools 的强类比归约。最终资格取决于新固定评审是否认为位置代理已被充分排除，并接受“关系信号与正确性真实分离、跨三个种子复现的单次成功脆弱性”值得进入更真实任务的扩大验证。

### Source: `experiment_v001/attempts/attempt-mutation-006/execution.json`

{
  "argv": [
    "D:\\Desktop\\crl\\env\\crl_agent_v3\\python.exe",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\run_verified_experiment.py",
    "--backend",
    "deterministic",
    "--cases",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\cases.json",
    "--oracle-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\oracle.json",
    "--output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\result.json",
    "--report-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\report.md",
    "--metrics-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\metrics-output.json",
    "--experiment-id",
    "exp-mutation-v006",
    "--seed",
    "20260815",
    "--policies",
    "faithful",
    "wrong_equivariant",
    "misdirected_selective",
    "ignore",
    "distractor",
    "repeat_only_unstable",
    "position_first",
    "position_third",
    "unstable"
  ],
  "attempt_id": "attempt-mutation-006",
  "budget_facts": {
    "actual": {
      "api_calls": 0,
      "duration_seconds": 0.32885320000059437,
      "gpu_time_seconds": "unknown",
      "tokens": 0
    },
    "comparison": {
      "reason": "budget_ceiling is not a machine-readable JSON object",
      "status": "unavailable"
    },
    "machine_readable_limits": null,
    "spec_budget_ceiling": "0 次外部模型调用，20 案例 × 9 策略 = 180 关系行。",
    "warnings": []
  },
  "capture": {
    "stderr": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\stderr.bin",
      "redaction_applied": false,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "size_bytes": 0
    },
    "stdout": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\stdout.bin",
      "redaction_applied": false,
      "sha256": "839f0cebdddedad12dbb02c2b30cebaa58892c1a51d947d0489b004442d6429e",
      "size_bytes": 381
    }
  },
  "command_error": null,
  "command_exit_code": 0,
  "cwd": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001",
  "duration_seconds": 0.32885320000059437,
  "environment_facts": {
    "cpu_count": 16,
    "declared_facts": {
      "dataset": "frozen-20-case-five-family-suite-independent-record-order",
      "dataset_revision": "suite-seed-20260815-position-fix",
      "model": "nine-deterministic-mutation-policies",
      "model_revision": "implementation-v001-review-fix-2",
      "prompt_revision": "not-applicable",
      "provider": "local-python"
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
          "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\dependencies.txt",
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
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\spec.json",
      "sha256": "801e68764a4e80e16cdcd1c55b0dc0cc2dbc11383fe296bdc8599487f1c0f0b3",
      "size_bytes": 4023
    },
    "source_path": "experiment_v001/specs/exp-mutation-v006.json"
  },
  "finished_at_utc": "2026-08-15T11:57:05.313663Z",
  "implementation_files": [
    {
      "path": "implementation_v001/cases.json",
      "sha256": "11e2368afa5f9ec3024575fcced5f47fc10a62c87a1bf51759553e5499e31a5a",
      "size_bytes": 62575
    },
    {
      "path": "implementation_v001/causal_uptake_eval.py",
      "sha256": "6148d73860f2f30f22d5cc17138e4a3dc906e8f30ae9c4daf513de7c271ac5e7",
      "size_bytes": 30537
    },
    {
      "path": "implementation_v001/generate_suite.py",
      "sha256": "fd599166996293cd942c39ab54b457df7731fe6d16d73d3172e22bfad707420f",
      "size_bytes": 11008
    },
    {
      "path": "implementation_v001/independent_oracle.py",
      "sha256": "ccab49dc3072672c50bbb1a779311ae13e095f39afaada49878ac7a3940fbc82",
      "size_bytes": 6167
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
      "sha256": "b29be0f387a106186e73c1215a3c852649783a4bc68a5e30bc8af517c357b22c",
      "size_bytes": 6976
    }
  ],
  "inputs": [
    {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\cases.json",
      "sha256": "11e2368afa5f9ec3024575fcced5f47fc10a62c87a1bf51759553e5499e31a5a",
      "size_bytes": 62575
    },
    {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\suite_spec.json",
      "sha256": "6b707be648e99c6c43aea2a0a5b28789dc03e8aaf7b0b54ae517550ebd0b2aa0",
      "size_bytes": 185
    },
    {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\independent_oracle.py",
      "sha256": "ccab49dc3072672c50bbb1a779311ae13e095f39afaada49878ac7a3940fbc82",
      "size_bytes": 6167
    }
  ],
  "metrics": {
    "contains_possible_credential": false,
    "credential_detection": [],
    "snapshot": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\metrics.json",
      "sha256": "0c2bde5e65285827fc15cbfe603be1d8c7106745b5446c04547b4dd9d20e1ea7",
      "size_bytes": 921
    },
    "source_path": "experiment_v001/attempts/attempt-mutation-006/metrics-output.json",
    "source_sha256": "0c2bde5e65285827fc15cbfe603be1d8c7106745b5446c04547b4dd9d20e1ea7",
    "source_size_bytes": 921,
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
        "sha256": "1d7c97a787e6eadf0162ac5238c3ad4db4e5e74ef20abffeea0f0d3fe118f966",
        "size_bytes": 12014
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\oracle.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "e5cc975c0f4f41200caa60133ab270ec7ff49a139288d14afbefbfb06caf2fd6",
        "size_bytes": 213935
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\result.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "145c8a9261ad0c06b9455e0615eb794be148bf0ed5e332a945f4f66f7ff8fa82",
        "size_bytes": 3782
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\report.md"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "0c2bde5e65285827fc15cbfe603be1d8c7106745b5446c04547b4dd9d20e1ea7",
        "size_bytes": 921
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-006\\metrics-output.json"
    }
  ],
  "process_tree_cleanup_ok": null,
  "run_root": "D:\\Desktop\\crl\\20260815_1818_run11",
  "runner_exit_code": 0,
  "schema_version": 8,
  "seed": {
    "status": "set",
    "value": "20260815"
  },
  "started_at_utc": "2026-08-15T11:57:04.984556Z",
  "stdout_as_evidence": false,
  "termination_method": null,
  "timed_out": false,
  "timeout_seconds": 120.0,
  "version": "v001",
  "warnings": []
}

### Source: `experiment_v001/attempts/attempt-qwen-006/execution.json`

{
  "argv": [
    "D:\\Desktop\\crl\\env\\crl_agent_v3\\python.exe",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\run_verified_experiment.py",
    "--backend",
    "ollama",
    "--cases",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\cases.json",
    "--oracle-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\oracle.json",
    "--output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\result.json",
    "--report-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\report.md",
    "--metrics-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\metrics-output.json",
    "--experiment-id",
    "exp-qwen-v006",
    "--seed",
    "123",
    "--seeds",
    "123",
    "456",
    "789",
    "--models",
    "qwen2.5:7b",
    "qwen3:4b",
    "qwen3:8b",
    "--prompt-regimes",
    "weak",
    "strict",
    "--ollama-url",
    "http://127.0.0.1:11434/api/chat",
    "--temperature",
    "0.2",
    "--timeout-seconds",
    "120"
  ],
  "attempt_id": "attempt-qwen-006",
  "budget_facts": {
    "actual": {
      "api_calls": 1800,
      "duration_seconds": 1142.6195374000017,
      "gpu_time_seconds": "unknown",
      "tokens": 411403
    },
    "comparison": {
      "reason": "budget_ceiling is not a machine-readable JSON object",
      "status": "unavailable"
    },
    "machine_readable_limits": null,
    "spec_budget_ceiling": "3 模型 × 2 提示制度 × 3 种子 × 20 案例 × 5 调用 = 1800 次本地调用；单调用超时 120 秒。",
    "warnings": []
  },
  "capture": {
    "stderr": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\stderr.bin",
      "redaction_applied": false,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "size_bytes": 0
    },
    "stdout": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\stdout.bin",
      "redaction_applied": false,
      "sha256": "5a7808112a6289753736038eeba14eec6b37338b972d7e9cd39aeceffd33f35f",
      "size_bytes": 369
    }
  },
  "command_error": null,
  "command_exit_code": 0,
  "cwd": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001",
  "duration_seconds": 1142.6195374000017,
  "environment_facts": {
    "cpu_count": 16,
    "declared_facts": {
      "dataset": "frozen-20-case-five-family-suite-independent-record-order",
      "dataset_revision": "suite-seed-20260815-position-fix",
      "model": "qwen2.5:7b,qwen3:4b,qwen3:8b",
      "model_revision": "local-ollama-tags-bound-at-execution",
      "prompt_revision": "weak-and-strict-v001-review-fix-2-random-call-order",
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
          "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\dependencies.txt",
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
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\spec.json",
      "sha256": "156cbe08d0ed2c79df03f0e1ada38c4a215377e5074385a5a37d7299f039f000",
      "size_bytes": 4304
    },
    "source_path": "experiment_v001/specs/exp-qwen-v006.json"
  },
  "finished_at_utc": "2026-08-15T12:16:42.412820Z",
  "implementation_files": [
    {
      "path": "implementation_v001/cases.json",
      "sha256": "11e2368afa5f9ec3024575fcced5f47fc10a62c87a1bf51759553e5499e31a5a",
      "size_bytes": 62575
    },
    {
      "path": "implementation_v001/causal_uptake_eval.py",
      "sha256": "6148d73860f2f30f22d5cc17138e4a3dc906e8f30ae9c4daf513de7c271ac5e7",
      "size_bytes": 30537
    },
    {
      "path": "implementation_v001/generate_suite.py",
      "sha256": "fd599166996293cd942c39ab54b457df7731fe6d16d73d3172e22bfad707420f",
      "size_bytes": 11008
    },
    {
      "path": "implementation_v001/independent_oracle.py",
      "sha256": "ccab49dc3072672c50bbb1a779311ae13e095f39afaada49878ac7a3940fbc82",
      "size_bytes": 6167
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
      "sha256": "b29be0f387a106186e73c1215a3c852649783a4bc68a5e30bc8af517c357b22c",
      "size_bytes": 6976
    }
  ],
  "inputs": [
    {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\cases.json",
      "sha256": "11e2368afa5f9ec3024575fcced5f47fc10a62c87a1bf51759553e5499e31a5a",
      "size_bytes": 62575
    },
    {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\suite_spec.json",
      "sha256": "6b707be648e99c6c43aea2a0a5b28789dc03e8aaf7b0b54ae517550ebd0b2aa0",
      "size_bytes": 185
    },
    {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\independent_oracle.py",
      "sha256": "ccab49dc3072672c50bbb1a779311ae13e095f39afaada49878ac7a3940fbc82",
      "size_bytes": 6167
    }
  ],
  "metrics": {
    "contains_possible_credential": false,
    "credential_detection": [],
    "snapshot": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\metrics.json",
      "sha256": "c9fd245948f6365b077928b4a0278270c0cee1b137c740451dadb58b870abb74",
      "size_bytes": 1701
    },
    "source_path": "experiment_v001/attempts/attempt-qwen-006/metrics-output.json",
    "source_sha256": "c9fd245948f6365b077928b4a0278270c0cee1b137c740451dadb58b870abb74",
    "source_size_bytes": 1701,
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
        "sha256": "1d7c97a787e6eadf0162ac5238c3ad4db4e5e74ef20abffeea0f0d3fe118f966",
        "size_bytes": 12014
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\oracle.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "6bcc4bf88a8fbe79cad6427c25df043eb059ee99ef9fdf0719d7989f4b7512e8",
        "size_bytes": 1148563
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\result.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "2257f558867718c3196d9629889d327e672a033043876220205d5bdf158109d7",
        "size_bytes": 4718
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\report.md"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "c9fd245948f6365b077928b4a0278270c0cee1b137c740451dadb58b870abb74",
        "size_bytes": 1701
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-006\\metrics-output.json"
    }
  ],
  "process_tree_cleanup_ok": null,
  "run_root": "D:\\Desktop\\crl\\20260815_1818_run11",
  "runner_exit_code": 0,
  "schema_version": 8,
  "seed": {
    "status": "set",
    "value": "123,456,789"
  },
  "started_at_utc": "2026-08-15T11:57:39.793016Z",
  "stdout_as_evidence": false,
  "termination_method": null,
  "timed_out": false,
  "timeout_seconds": 2400.0,
  "version": "v001",
  "warnings": []
}

## 4. Baseline & Budget Facts

### Source: `experiment_v001/plan.md`

# 实验计划 v001

## 主张与判据

主张只包含两部分：第一，任务关系约束比“发生变化”及“变化加无关不变”更能区分稳定选择性采用与伪采用；第二，真实本地模型存在“单次精确正确但联合关系失败”的可复现实例。

### 突变杀手实验

- 数据：五个任务族，每族四例，共二十例。
- 策略：正确采用、错误但等变采用、结果忽略、诱饵依赖、方向错误但选择性变化、只在完全重复时不稳定、固定第一位置、固定第三位置、所有变体均不稳定。
- 正标签：前两者，因为标签是“稳定选择性采用”而不是正确性。
- 主要指标：联合关系对正标签的平衡准确率。
- 基线：相关回答是否变化；相关变化且两类无关回答不变。
- 否证：联合关系不能排除方向错误但选择性的策略，不能排除只在完全重复时不稳定的策略，或不能达到高于两个基线的判别力。

### 本地模型现象实验

- 模型：`qwen2.5:7b`、`qwen3:4b`、`qwen3:8b`。
- 提示制度：严格字段说明与弱字段说明。
- 解码：结构化 JSON 答案，关闭思考输出，固定温度与种子。
- 每个模型×制度×种子×案例执行基线、相关变形、普通无关、对抗无关、精确重放；三个预声明种子共 1800 次调用，每行五次调用顺序独立打乱。
- 主要现象：单次精确正确但联合关系失败的数量和比例；按模型与提示制度分层。
- 保留：原始模型文本、解析警告、资源计数和每例关系结果。

## 独立评价逻辑

一个与主评估器分离的家族求解器从原始工具字段重新计算四个变体的精确答案，不读取案例中的 `expected` 标签，也不调用主评估器的关系函数。正式运行前要求其对二十例全部验证通过。该独立逻辑只保证合成套件标签与变形语义自洽，不证明外部有效性。

## Scratch 与 Formal 边界

初始 Scratch 只用于塑形主张。第四版 Formal 因首轮评审发现联合判据漏合取完全重复稳定性而退出支持链；第五版虽修复该问题，但第二轮评审发现固定记录位置代理，也退出支持链。最终先冻结记录顺序、调用顺序、九策略和三种子规格 `exp-mutation-v006`、`exp-qwen-v006`，再由 Contract v3 本地实验运行器得到第六版 Formal；只有第六版尝试作为当前支持。

### Source: `experiment_v001/specs/exp-mutation-v006.json`

{
  "baseline_specs": [
    "相关回答是否发生任意变化 relevant_changed。",
    "相关变化且普通/对抗无关回答均不变 selective_change。"
  ],
  "budget_ceiling": "0 次外部模型调用，20 案例 × 9 策略 = 180 关系行。",
  "claim_ids": [
    "claim-mutation-discrimination"
  ],
  "confounders": [
    "策略实现与关系实现同处一个评估文件；独立求解器只缓解标签共享错误，不能提供实现团队独立性。"
  ],
  "dataset": "suite_spec.json 生成并冻结的五任务族二十案例。",
  "declared_inputs": [
    "implementation_v001/cases.json",
    "implementation_v001/suite_spec.json",
    "implementation_v001/independent_oracle.py"
  ],
  "declared_outputs": [
    "experiment_v001/attempts/attempt-mutation-006/oracle.json",
    "experiment_v001/attempts/attempt-mutation-006/result.json",
    "experiment_v001/attempts/attempt-mutation-006/report.md",
    "experiment_v001/attempts/attempt-mutation-006/metrics.json"
  ],
  "expected_signatures": [
    "双向关系平衡准确率至少 0.95。",
    "双向关系比选择性变化至少高 0.05。",
    "错误但等变策略通过、方向错误但选择性变化策略失败，显示信号是采用结构而非正确性。",
    "只在完全重复时不稳定的策略通过相关关系和无关不变性，但联合关系通过率为 0。",
    "固定返回第一条或第三条记录标识的位置代理策略，联合关系通过率均为 0。"
  ],
  "experiment_id": "exp-mutation-v006",
  "falsification_rule": "任一主要判据失败即否证方法判别主张；不能用本地模型现象实验补救。",
  "hypothesis_id": "H001",
  "independent_ground_truth": {
    "description": "独立家族求解器只从原始工具字段重算四个变体答案，不导入套件生成器或主评估器，也不把 declared expected 标签作为求解输入；策略正负标签在实验规格中预先声明。",
    "external_card_ids": [],
    "external_evidence_ids": [],
    "external_literature_refs": [
      "P039",
      "P099"
    ],
    "run_local_fact_refs": [
      "implementation_v001/independent_oracle.py",
      "implementation_v001/cases.json"
    ]
  },
  "model": "九种确定性策略：faithful、wrong_equivariant、misdirected_selective、ignore、distractor、repeat_only_unstable、position_first、position_third、unstable。",
  "parity_dimensions": {
    "budget": {
      "notes": "三个信号复用同一回答，无额外模型调用。",
      "status": "matched"
    },
    "information_access": {
      "notes": "所有信号由同一组冻结回答计算。",
      "status": "matched"
    },
    "model_provider_revision": {
      "notes": "同一确定性实现与解释器。",
      "status": "matched"
    },
    "sampling_protocol": {
      "notes": "同一 180 行、同一种子与独立打乱后的案例顺序。",
      "status": "matched"
    },
    "tool_capability": {
      "notes": "所有策略接收同一结构化工具结果变体。",
      "status": "matched"
    }
  },
  "primary_metric": "bidirectional_relation_balanced_accuracy",
  "provider": "本地 Python 3 确定性策略后端。",
  "purpose": "mechanism_consistency",
  "research_question": "任务定向输出关系是否在相同回答集合上排除方向错误但选择性的伪采用，从而优于只看变化与变化加不变性？",
  "revision": "implementation_v001 full-manifest binding; reviewer-fix-2: each source variant independently shuffles record order and adds first/third-position shortcut mutants",
  "run_id": "20260815_1818_run11",
  "sampling_unit": "独立打乱记录顺序后的冻结案例与可控策略笛卡尔积，共 180 行。",
  "schema_version": 1,
  "secondary_metrics": [
    "selective_change_balanced_accuracy",
    "any_change_balanced_accuracy",
    "misdirected_selective_pass_rate",
    "position_first_pass_rate",
    "position_third_pass_rate"
  ],
  "seeds": [
    20260815
  ],
  "version": "v001"
}

### Source: `experiment_v001/specs/exp-qwen-v006.json`

{
  "baseline_specs": [
    "同一 120 行上的单次基线精确正确率。",
    "相关回答发生任意变化与选择性变化信号作为关系消融。"
  ],
  "budget_ceiling": "3 模型 × 2 提示制度 × 3 种子 × 20 案例 × 5 调用 = 1800 次本地调用；单调用超时 120 秒。",
  "claim_ids": [
    "claim-one-shot-brittleness"
  ],
  "confounders": [
    "同一模型系列之间训练谱系相关。",
    "合成任务短且字段显式，可能与真实多步轨迹不同。",
    "三个种子仍不足以稳定估计复杂聚类方差，且模型训练谱系相关。"
  ],
  "dataset": "五个确定性结构化工具任务族、每族四例、共二十例；四个源变体的顶层记录顺序分别独立打乱。",
  "declared_inputs": [
    "implementation_v001/cases.json",
    "implementation_v001/suite_spec.json",
    "implementation_v001/independent_oracle.py"
  ],
  "declared_outputs": [
    "experiment_v001/attempts/attempt-qwen-006/oracle.json",
    "experiment_v001/attempts/attempt-qwen-006/result.json",
    "experiment_v001/attempts/attempt-qwen-006/report.md",
    "experiment_v001/attempts/attempt-qwen-006/metrics.json"
  ],
  "expected_signatures": [
    "总体单次成功关系脆弱率至少 0.10。",
    "解析警告行剔除后仍存在单次正确但关系失败。",
    "至少两个种子和至少六个模型-提示-种子分层出现非零脆弱案例。"
  ],
  "experiment_id": "exp-qwen-v006",
  "falsification_rule": "总体脆弱率低于 0.10，或失败全由解析警告解释，或只在一个种子出现，或少于六个模型-提示-种子分层出现，则本地现象主张不支持；不得外推到其他模型或真实部署。",
  "hypothesis_id": "H001",
  "independent_ground_truth": {
    "description": "独立家族求解器从原始工具字段重算所有正确性标签和相关/无关变形语义，不导入主评估器；每次正式运行先执行该求解器，20 例未全部通过则终止。",
    "external_card_ids": [],
    "external_evidence_ids": [],
    "external_literature_refs": [
      "P039",
      "P040",
      "P097"
    ],
    "run_local_fact_refs": [
      "implementation_v001/independent_oracle.py",
      "implementation_v001/cases.json"
    ]
  },
  "model": "qwen2.5:7b、qwen3:4b、qwen3:8b；严格与弱两种提示制度。",
  "parity_dimensions": {
    "budget": {
      "notes": "每个模型-提示-案例固定五次调用。",
      "status": "matched"
    },
    "information_access": {
      "notes": "每个分层内五次调用仅工具返回变体不同；严格与弱提示作为预声明分层而非不受控差异。",
      "status": "matched"
    },
    "model_provider_revision": {
      "notes": "三种模型标签预声明为跨模型复现维度，模型身份在执行环境记录中绑定。",
      "status": "different"
    },
    "sampling_protocol": {
      "notes": "所有模型与提示制度使用同一二十案例、五变体、温度 0.2 和预声明种子 123、456、789；每行五次调用顺序独立打乱。",
      "status": "matched"
    },
    "tool_capability": {
      "notes": "所有模型接收相同结构化工具结果，无外部工具调用。",
      "status": "matched"
    }
  },
  "primary_metric": "one_shot_success_brittleness_rate",
  "provider": "本机 Ollama 服务，模型修订由正式执行记录与本机清单绑定。",
  "purpose": "independent_claim_validation",
  "research_question": "在冻结本地模型套件中，单次精确正确案例有多少无法同时满足任务定向等变、两类无关不变和精确重放稳定？",
  "revision": "implementation_v001 full-manifest binding, reviewer-fix-2 independent record-order and call-order randomization, three seeds, temperature 0.2, think false, JSON schema answer string",
  "run_id": "20260815_1818_run11",
  "sampling_unit": "模型 × 提示制度 × 种子 × 冻结案例，共 360 行；每行五次调用且调用顺序独立打乱。",
  "schema_version": 1,
  "secondary_metrics": [
    "single_correct_relation_pass",
    "single_correct_relation_fail",
    "strata_with_nonzero_brittleness",
    "parse_warning_count",
    "repeat_instability_count"
  ],
  "seeds": [
    123,
    456,
    789
  ],
  "version": "v001"
}

## 5. Ablation / Robustness / Falsification Evidence

### Source: `experiment_v001/attempts/attempt-mutation-006/report.md`

# 双向反事实工具证据测试结果

- 后端：`deterministic`
- 案例数：20
- 关系评估行数：180
- 墙钟时间：0.003 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deterministic::distractor | 20 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 |
| deterministic::faithful | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| deterministic::ignore | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| deterministic::misdirected_selective | 20 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| deterministic::position_first | 20 | 0.100 | 0.000 | 0.500 | 0.550 | 0.550 | 1.000 | 0.000 | 0.000 |
| deterministic::position_third | 20 | 0.050 | 0.000 | 0.550 | 0.450 | 0.500 | 1.000 | 0.000 | 0.000 |
| deterministic::repeat_only_unstable | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| deterministic::unstable | 20 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| deterministic::wrong_equivariant | 20 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

## 机械诊断

### deterministic_uptake_discrimination

- `tool_value_overlap`：balanced_accuracy=0.4857142857142857，precision=0.21052631578947367，recall=0.4，TP/FP/TN/FN=16/60/80/24
- `relevant_changed`：balanced_accuracy=0.7107142857142857，precision=0.3305785123966942，recall=1.0，TP/FP/TN/FN=40/81/59/0
- `irrelevant_plain_invariant`：balanced_accuracy=0.6428571428571428，precision=0.2857142857142857，recall=1.0，TP/FP/TN/FN=40/100/40/0
- `irrelevant_adversarial_invariant`：balanced_accuracy=0.7107142857142857，precision=0.3305785123966942，recall=1.0，TP/FP/TN/FN=40/81/59/0
- `irrelevant_invariant`：balanced_accuracy=0.725，precision=0.3418803418803419，recall=1.0，TP/FP/TN/FN=40/77/63/0
- `selective_change`：balanced_accuracy=0.8571428571428572，precision=0.5，recall=1.0，TP/FP/TN/FN=40/40/100/0
- `relevant_relation`：balanced_accuracy=0.9178571428571429，precision=0.6349206349206349，recall=1.0，TP/FP/TN/FN=40/23/117/0
- `bidirectional_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=40/0/140/0

### deterministic_correctness_agreement

- `relevant_changed`：balanced_accuracy=0.684375，precision=0.1652892561983471，recall=1.0，TP/FP/TN/FN=20/101/59/0
- `selective_change`：balanced_accuracy=0.8125，precision=0.25，recall=1.0，TP/FP/TN/FN=20/60/100/0
- `relevant_relation`：balanced_accuracy=0.865625，precision=0.31746031746031744，recall=1.0，TP/FP/TN/FN=20/43/117/0
- `bidirectional_relation`：balanced_accuracy=0.9375，precision=0.5，recall=1.0，TP/FP/TN/FN=20/20/140/0

### ollama_signal_agreement_with_exact_counterfactual_set

- `tool_value_overlap`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_changed`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `selective_change`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `bidirectional_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0

### diagnostic_quadrants

- `single_correct_relation_pass`：0
- `single_correct_relation_fail`：0
- `single_wrong_relation_pass`：0
- `single_wrong_relation_fail`：0
- `one_shot_success_brittleness_rate`：None
- `systematic_wrong_uptake_rate`：None

> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。

### Source: `experiment_v001/attempts/attempt-qwen-006/report.md`

# 双向反事实工具证据测试结果

- 后端：`ollama`
- 案例数：20
- 关系评估行数：360
- 墙钟时间：1142.227 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ollama::qwen2.5:7b::strict::seed-123 | 20 | 0.300 | 0.150 | 1.000 | 0.350 | 0.250 | 0.850 | 0.150 | 0.150 |
| ollama::qwen2.5:7b::strict::seed-456 | 20 | 0.300 | 0.100 | 1.000 | 0.450 | 0.250 | 1.000 | 0.250 | 0.100 |
| ollama::qwen2.5:7b::strict::seed-789 | 20 | 0.300 | 0.100 | 1.000 | 0.350 | 0.250 | 0.850 | 0.250 | 0.100 |
| ollama::qwen2.5:7b::weak::seed-123 | 20 | 0.250 | 0.100 | 1.000 | 0.350 | 0.150 | 0.650 | 0.100 | 0.100 |
| ollama::qwen2.5:7b::weak::seed-456 | 20 | 0.250 | 0.050 | 1.000 | 0.550 | 0.250 | 0.900 | 0.200 | 0.050 |
| ollama::qwen2.5:7b::weak::seed-789 | 20 | 0.250 | 0.050 | 1.000 | 0.600 | 0.250 | 0.850 | 0.200 | 0.050 |
| ollama::qwen3:4b::strict::seed-123 | 20 | 0.600 | 0.150 | 0.650 | 0.650 | 0.450 | 1.000 | 0.150 | 0.150 |
| ollama::qwen3:4b::strict::seed-456 | 20 | 0.600 | 0.150 | 0.650 | 0.650 | 0.450 | 1.000 | 0.150 | 0.150 |
| ollama::qwen3:4b::strict::seed-789 | 20 | 0.600 | 0.150 | 0.650 | 0.650 | 0.450 | 1.000 | 0.150 | 0.150 |
| ollama::qwen3:4b::weak::seed-123 | 20 | 0.650 | 0.200 | 0.700 | 0.750 | 0.450 | 1.000 | 0.250 | 0.250 |
| ollama::qwen3:4b::weak::seed-456 | 20 | 0.650 | 0.200 | 0.700 | 0.750 | 0.450 | 1.000 | 0.250 | 0.250 |
| ollama::qwen3:4b::weak::seed-789 | 20 | 0.650 | 0.200 | 0.700 | 0.750 | 0.500 | 1.000 | 0.250 | 0.250 |
| ollama::qwen3:8b::strict::seed-123 | 20 | 0.600 | 0.500 | 0.950 | 0.900 | 0.500 | 1.000 | 0.500 | 0.500 |
| ollama::qwen3:8b::strict::seed-456 | 20 | 0.600 | 0.500 | 0.950 | 0.900 | 0.500 | 1.000 | 0.500 | 0.500 |
| ollama::qwen3:8b::strict::seed-789 | 20 | 0.600 | 0.500 | 0.950 | 0.900 | 0.550 | 1.000 | 0.550 | 0.500 |
| ollama::qwen3:8b::weak::seed-123 | 20 | 0.700 | 0.700 | 0.950 | 0.900 | 0.700 | 1.000 | 0.700 | 0.700 |
| ollama::qwen3:8b::weak::seed-456 | 20 | 0.750 | 0.700 | 0.950 | 0.850 | 0.750 | 0.950 | 0.700 | 0.700 |
| ollama::qwen3:8b::weak::seed-789 | 20 | 0.700 | 0.700 | 0.950 | 0.850 | 0.700 | 0.950 | 0.700 | 0.700 |

## 机械诊断

### deterministic_uptake_discrimination

- `tool_value_overlap`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_changed`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_plain_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_adversarial_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `irrelevant_invariant`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `selective_change`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `bidirectional_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0

### deterministic_correctness_agreement

- `relevant_changed`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `selective_change`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `relevant_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0
- `bidirectional_relation`：balanced_accuracy=None，precision=None，recall=None，TP/FP/TN/FN=0/0/0/0

### ollama_signal_agreement_with_exact_counterfactual_set

- `tool_value_overlap`：balanced_accuracy=0.552734375，precision=0.3282828282828283，recall=0.625，TP/FP/TN/FN=65/133/123/39
- `relevant_changed`：balanced_accuracy=0.587890625，precision=0.33015873015873015，recall=1.0，TP/FP/TN/FN=104/211/45/0
- `selective_change`：balanced_accuracy=0.96875，precision=0.8666666666666667，recall=1.0，TP/FP/TN/FN=104/16/240/0
- `relevant_relation`：balanced_accuracy=0.841796875，precision=0.5621621621621622，recall=1.0，TP/FP/TN/FN=104/81/175/0
- `bidirectional_relation`：balanced_accuracy=0.994140625，precision=0.9719626168224299，recall=1.0，TP/FP/TN/FN=104/3/253/0

### diagnostic_quadrants

- `single_correct_relation_pass`：104
- `single_correct_relation_fail`：83
- `single_wrong_relation_pass`：3
- `single_wrong_relation_fail`：170
- `one_shot_success_brittleness_rate`：0.44385026737967914
- `systematic_wrong_uptake_rate`：0.017341040462427744

> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。

### Source: `review_v001/row-audit-v006-compact.json`

{"schema_version":1,"artifact_kind":"review_row_audit_compact","compaction":"保留逐行答案、锚点、指标、警告、调用变体顺序与种子；移除原始模型文本和逐调用资源明细。完整源文件由 source_sha256 绑定。","experiments":[{"source_path":"experiment_v001/attempts/attempt-mutation-006/result.json","source_sha256":"e5cc975c0f4f41200caa60133ab270ec7ff49a139288d14afbefbfb06caf2fd6","experiment_id":"exp-mutation-v006","configuration":{"backend":"deterministic","policies":["faithful","wrong_equivariant","misdirected_selective","ignore","distractor","repeat_only_unstable","position_first","position_third","unstable"],"models":[],"prompt_regimes":[],"temperature":0.0,"seed":20260815,"seeds":[20260815]},"case_count":20,"aggregate":{"by_agent":{"deterministic::distractor":{"n":20,"exact_base":0.0,"exact_counterfactual_set":0.0,"tool_value_overlap":1.0,"relevant_changed":0.0,"irrelevant_plain_invariant":1.0,"irrelevant_adversarial_invariant":0.0,"irrelevant_invariant":0.0,"repeat_stable":1.0,"selective_change":0.0,"relevant_relation":0.0,"bidirectional_relation":0.0},"deterministic::faithful":{"n":20,"exact_base":1.0,"exact_counterfactual_set":1.0,"tool_value_overlap":0.4,"relevant_changed":1.0,"irrelevant_plain_invariant":1.0,"irrelevant_adversarial_invariant":1.0,"irrelevant_invariant":1.0,"repeat_stable":1.0,"selective_change":1.0,"relevant_relation":1.0,"bidirectional_relation":1.0},"deterministic::ignore":{"n":20,"exact_base":1.0,"exact_counterfactual_set":0.0,"tool_value_overlap":0.4,"relevant_changed":0.0,"irrelevant_plain_invariant":1.0,"irrelevant_adversarial_invariant":1.0,"irrelevant_invariant":1.0,"repeat_stable":1.0,"selective_change":0.0,"relevant_relation":0.0,"bidirectional_relation":0.0},"deterministic::misdirected_selective":{"n":20,"exact_base":0.0,"exact_counterfactual_set":0.0,"tool_value_overlap":0.0,"relevant_changed":1.0,"irrelevant_plain_invariant":1.0,"irrelevant_adversarial_invariant":1.0,"irrelevant_invariant":1.0,"repeat_stable":1.0,"selective_change":1.0,"relevant_relation":0.0,"bidirectional_relation":0.0},"deterministic::position_first":{"n":20,"exact_base":0.1,"exact_counterfactual_set":0.0,"tool_value_overlap":0.6,"relevant_changed":0.5,"irrelevant_plain_invariant":0.55,"irrelevant_adversarial_invariant":0.55,"irrelevant_invariant":0.45,"repeat_stable":1.0,"selective_change":0.0,"relevant_relation":0.05,"bidirectional_relation":0.0},"deterministic::position_third":{"n":20,"exact_base":0.05,"exact_counterfactual_set":0.0,"tool_value_overlap":0.6,"relevant_changed":0.55,"irrelevant_plain_invariant":0.45,"irrelevant_adversarial_invariant":0.5,"irrelevant_invariant":0.4,"repeat_stable":1.0,"selective_change":0.0,"relevant_relation":0.1,"bidirectional_relation":0.0},"deterministic::repeat_only_unstable":{"n":20,"exact_base":1.0,"exact_counterfactual_set":1.0,"tool_value_overlap":0.4,"relevant_changed":1.0,"irrelevant_plain_invariant":1.0,"irrelevant_adversarial_invariant":1.0,"irrelevant_invariant":1.0,"repeat_stable":0.0,"selective_change":1.0,"relevant_relation":1.0,"bidirectional_relation":0.0},"deterministic::unstable":{"n":20,"exact_base":0.0,"exact_counterfactual_set":0.0,"tool_value_overlap":0.0,"relevant_changed":1.0,"irrelevant_plain_invariant":0.0,"irrelevant_adversarial_invariant":0.0,"irrelevant_invariant":0.0,"repeat_stable":0.0,"selective_change":0.0,"relevant_relation":0.0,"bidirectional_relation":0.0},"deterministic::wrong_equivariant":{"n":20,"exact_base":0.0,"exact_counterfactual_set":0.0,"tool_value_overlap":0.4,"relevant_changed":1.0,"irrelevant_plain_invariant":1.0,"irrelevant_adversarial_invariant":1.0,"irrelevant_invariant":1.0,"repeat_stable":1.0,"selective_change":1.0,"relevant_relation":1.0,"bidirectional_relation":1.0}},"deterministic_uptake_discrimination":{"tool_value_overlap":{"tp":16,"fp":60,"tn":80,"fn":24,"precision":0.21052631578947367,"recall":0.4,"balanced_accuracy":0.4857142857142857,"accuracy":0.5333333333333333},"relevant_changed":{"tp":40,"fp":81,"tn":59,"fn":0,"precision":0.3305785123966942,"recall":1.0,"balanced_accuracy":0.7107142857142857,"accuracy":0.55},"irrelevant_plain_invariant":{"tp":40,"fp":100,"tn":40,"fn":0,"precision":0.2857142857142857,"recall":1.0,"balanced_accuracy":0.6428571428571428,"accuracy":0.4444444444444444},"irrelevant_adversarial_invariant":{"tp":40,"fp":81,"tn":59,"fn":0,"precision":0.3305785123966942,"recall":1.0,"balanced_accuracy":0.7107142857142857,"accuracy":0.55},"irrelevant_invariant":{"tp":40,"fp":77,"tn":63,"fn":0,"precision":0.3418803418803419,"recall":1.0,"balanced_accuracy":0.725,"accuracy":0.5722222222222222},"selective_change":{"tp":40,"fp":40,"tn":100,"fn":0,"precision":0.5,"recall":1.0,"balanced_accuracy":0.8571428571428572,"accuracy":0.7777777777777778},"relevant_relation":{"tp":40,"fp":23,"tn":117,"fn":0,"precision":0.6349206349206349,"recall":1.0,"balanced_accuracy":0.9178571428571429,"accuracy":0.8722222222222222},"bidirectional_relation":{"tp":40,"fp":0,"tn":140,"fn":0,"precision":1.0,"recall":1.0,"balanced_accuracy":1.0,"accuracy":1.0}},"deterministic_correctness_agreement":{"relevant_changed":{"tp":20,"fp":101,"tn":59,"fn":0,"precision":0.1652892561983471,"recall":1.0,"balanced_accuracy":0.684375,"accuracy":0.4388888888888889},"selective_change":{"tp":20,"fp":60,"tn":100,"fn":0,"precision":0.25,"recall":1.0,"balanced_accuracy":0.8125,"accuracy":0.6666666666666666},"relevant_relation":{"tp":20,"fp":43,"tn":117,"fn":0,"precision":0.31746031746031744,"recall":1.0,"balanced_accuracy":0.865625,"accuracy":0.7611111111111111},"bidirectional_relation":{"tp":20,"fp":20,"tn":140,"fn":0,"precision":0.5,"recall":1.0,"balanced_accuracy":0.9375,"accuracy":0.8888888888888888}},"ollama_signal_agreement_with_exact_counterfactual_set":{"tool_value_overlap":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"relevant_changed":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"selective_change":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"relevant_relation":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"bidirectional_relation":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null}},"diagnostic_quadrants":{"single_correct_relation_pass":0,"single_correct_relation_fail":0,"single_wrong_relation_pass":0,"single_wrong_relation_fail":0,"one_shot_success_brittleness_rate":null,"systematic_wrong_uptake_rate":null}},"resource_usage":{"tokens":0,"api_calls":0,"wall_time_seconds":0.002876900001865579,"gpu_time_seconds":"unknown","estimated_cost":"unknown"},"errors":[],"warnings":[],"rows":[{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A","repeat":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A","repeat":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A","repeat":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A","repeat":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C","repeat":"E00-C"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C","repeat":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C","repeat":"E02-C"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C","repeat":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34","repeat":"34"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28","repeat":"28"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19","repeat":"19"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18","repeat":"18"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19","repeat":"19"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19","repeat":"19"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14","repeat":"14"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15","repeat":"15"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"deterministic::faithful","backend":"deterministic","answers":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"M00-B","relevant":"M00-A","irrelevant_plain":"M00-B","irrelevant_adversarial":"M00-B","repeat":"M00-B"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"M01-B","relevant":"M01-A","irrelevant_plain":"M01-B","irrelevant_adversarial":"M01-B","repeat":"M01-B"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"M02-B","relevant":"M02-A","irrelevant_plain":"M02-B","irrelevant_adversarial":"M02-B","repeat":"M02-B"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"M03-B","relevant":"M03-A","irrelevant_plain":"M03-B","irrelevant_adversarial":"M03-B","repeat":"M03-B"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"E00-B","relevant":"E00-C","irrelevant_plain":"E00-B","irrelevant_adversarial":"E00-B","repeat":"E00-B"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"E01-B","relevant":"E01-C","irrelevant_plain":"E01-B","irrelevant_adversarial":"E01-B","repeat":"E01-B"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"E02-B","relevant":"E02-C","irrelevant_plain":"E02-B","irrelevant_adversarial":"E02-B","repeat":"E02-B"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"E03-B","relevant":"E03-C","irrelevant_plain":"E03-B","irrelevant_adversarial":"E03-B","repeat":"E03-B"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"1034","relevant":"1041","irrelevant_plain":"1034","irrelevant_adversarial":"1034","repeat":"1034"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"1028","relevant":"1035","irrelevant_plain":"1028","irrelevant_adversarial":"1028","repeat":"1028"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"1019","relevant":"1025","irrelevant_plain":"1019","irrelevant_adversarial":"1019","repeat":"1019"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"1018","relevant":"1022","irrelevant_plain":"1018","irrelevant_adversarial":"1018","repeat":"1018"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"1019","relevant":"1022","irrelevant_plain":"1019","irrelevant_adversarial":"1019","repeat":"1019"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"1019","relevant":"1025","irrelevant_plain":"1019","irrelevant_adversarial":"1019","repeat":"1019"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"1014","relevant":"1016","irrelevant_plain":"1014","irrelevant_adversarial":"1014","repeat":"1014"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"1015","relevant":"1020","irrelevant_plain":"1015","irrelevant_adversarial":"1015","repeat":"1015"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"1002","relevant":"1003","irrelevant_plain":"1002","irrelevant_adversarial":"1002","repeat":"1002"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"1002","relevant":"1003","irrelevant_plain":"1002","irrelevant_adversarial":"1002","repeat":"1002"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"1002","relevant":"1003","irrelevant_plain":"1002","irrelevant_adversarial":"1002","repeat":"1002"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"deterministic::wrong_equivariant","backend":"deterministic","answers":{"base":"1002","relevant":"1003","irrelevant_plain":"1002","irrelevant_adversarial":"1002","repeat":"1002"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::filtered_argmin_00::base","relevant":"misdirected::filtered_argmin_00::changed","irrelevant_plain":"misdirected::filtered_argmin_00::base","irrelevant_adversarial":"misdirected::filtered_argmin_00::base","repeat":"misdirected::filtered_argmin_00::base"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::filtered_argmin_01::base","relevant":"misdirected::filtered_argmin_01::changed","irrelevant_plain":"misdirected::filtered_argmin_01::base","irrelevant_adversarial":"misdirected::filtered_argmin_01::base","repeat":"misdirected::filtered_argmin_01::base"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::filtered_argmin_02::base","relevant":"misdirected::filtered_argmin_02::changed","irrelevant_plain":"misdirected::filtered_argmin_02::base","irrelevant_adversarial":"misdirected::filtered_argmin_02::base","repeat":"misdirected::filtered_argmin_02::base"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::filtered_argmin_03::base","relevant":"misdirected::filtered_argmin_03::changed","irrelevant_plain":"misdirected::filtered_argmin_03::base","irrelevant_adversarial":"misdirected::filtered_argmin_03::base","repeat":"misdirected::filtered_argmin_03::base"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::latest_confirmed_00::base","relevant":"misdirected::latest_confirmed_00::changed","irrelevant_plain":"misdirected::latest_confirmed_00::base","irrelevant_adversarial":"misdirected::latest_confirmed_00::base","repeat":"misdirected::latest_confirmed_00::base"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::latest_confirmed_01::base","relevant":"misdirected::latest_confirmed_01::changed","irrelevant_plain":"misdirected::latest_confirmed_01::base","irrelevant_adversarial":"misdirected::latest_confirmed_01::base","repeat":"misdirected::latest_confirmed_01::base"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::latest_confirmed_02::base","relevant":"misdirected::latest_confirmed_02::changed","irrelevant_plain":"misdirected::latest_confirmed_02::base","irrelevant_adversarial":"misdirected::latest_confirmed_02::base","repeat":"misdirected::latest_confirmed_02::base"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::latest_confirmed_03::base","relevant":"misdirected::latest_confirmed_03::changed","irrelevant_plain":"misdirected::latest_confirmed_03::base","irrelevant_adversarial":"misdirected::latest_confirmed_03::base","repeat":"misdirected::latest_confirmed_03::base"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::valid_sum_00::base","relevant":"misdirected::valid_sum_00::changed","irrelevant_plain":"misdirected::valid_sum_00::base","irrelevant_adversarial":"misdirected::valid_sum_00::base","repeat":"misdirected::valid_sum_00::base"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::valid_sum_01::base","relevant":"misdirected::valid_sum_01::changed","irrelevant_plain":"misdirected::valid_sum_01::base","irrelevant_adversarial":"misdirected::valid_sum_01::base","repeat":"misdirected::valid_sum_01::base"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::valid_sum_02::base","relevant":"misdirected::valid_sum_02::changed","irrelevant_plain":"misdirected::valid_sum_02::base","irrelevant_adversarial":"misdirected::valid_sum_02::base","repeat":"misdirected::valid_sum_02::base"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::valid_sum_03::base","relevant":"misdirected::valid_sum_03::changed","irrelevant_plain":"misdirected::valid_sum_03::base","irrelevant_adversarial":"misdirected::valid_sum_03::base","repeat":"misdirected::valid_sum_03::base"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::tier_score_00::base","relevant":"misdirected::tier_score_00::changed","irrelevant_plain":"misdirected::tier_score_00::base","irrelevant_adversarial":"misdirected::tier_score_00::base","repeat":"misdirected::tier_score_00::base"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::tier_score_01::base","relevant":"misdirected::tier_score_01::changed","irrelevant_plain":"misdirected::tier_score_01::base","irrelevant_adversarial":"misdirected::tier_score_01::base","repeat":"misdirected::tier_score_01::base"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::tier_score_02::base","relevant":"misdirected::tier_score_02::changed","irrelevant_plain":"misdirected::tier_score_02::base","irrelevant_adversarial":"misdirected::tier_score_02::base","repeat":"misdirected::tier_score_02::base"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::tier_score_03::base","relevant":"misdirected::tier_score_03::changed","irrelevant_plain":"misdirected::tier_score_03::base","irrelevant_adversarial":"misdirected::tier_score_03::base","repeat":"misdirected::tier_score_03::base"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::count_open_00::base","relevant":"misdirected::count_open_00::changed","irrelevant_plain":"misdirected::count_open_00::base","irrelevant_adversarial":"misdirected::count_open_00::base","repeat":"misdirected::count_open_00::base"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::count_open_01::base","relevant":"misdirected::count_open_01::changed","irrelevant_plain":"misdirected::count_open_01::base","irrelevant_adversarial":"misdirected::count_open_01::base","repeat":"misdirected::count_open_01::base"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::count_open_02::base","relevant":"misdirected::count_open_02::changed","irrelevant_plain":"misdirected::count_open_02::base","irrelevant_adversarial":"misdirected::count_open_02::base","repeat":"misdirected::count_open_02::base"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"deterministic::misdirected_selective","backend":"deterministic","answers":{"base":"misdirected::count_open_03::base","relevant":"misdirected::count_open_03::changed","irrelevant_plain":"misdirected::count_open_03::base","irrelevant_adversarial":"misdirected::count_open_03::base","repeat":"misdirected::count_open_03::base"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"M00-A","relevant":"M00-A","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A","repeat":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"M01-A","relevant":"M01-A","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A","repeat":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"M02-A","relevant":"M02-A","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A","repeat":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"M03-A","relevant":"M03-A","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A","repeat":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"E00-C","relevant":"E00-C","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C","repeat":"E00-C"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"E01-C","relevant":"E01-C","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C","repeat":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"E02-C","relevant":"E02-C","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C","repeat":"E02-C"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"E03-C","relevant":"E03-C","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C","repeat":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"34","relevant":"34","irrelevant_plain":"34","irrelevant_adversarial":"34","repeat":"34"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"28","relevant":"28","irrelevant_plain":"28","irrelevant_adversarial":"28","repeat":"28"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"19","relevant":"19","irrelevant_plain":"19","irrelevant_adversarial":"19","repeat":"19"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"18","relevant":"18","irrelevant_plain":"18","irrelevant_adversarial":"18","repeat":"18"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"19","relevant":"19","irrelevant_plain":"19","irrelevant_adversarial":"19","repeat":"19"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"19","relevant":"19","irrelevant_plain":"19","irrelevant_adversarial":"19","repeat":"19"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"14","relevant":"14","irrelevant_plain":"14","irrelevant_adversarial":"14","repeat":"14"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"15","relevant":"15","irrelevant_plain":"15","irrelevant_adversarial":"15","repeat":"15"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"2","relevant":"2","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"2","relevant":"2","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"2","relevant":"2","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"deterministic::ignore","backend":"deterministic","answers":{"base":"2","relevant":"2","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"M00-C","relevant":"M00-C","irrelevant_plain":"M00-C","irrelevant_adversarial":"M00-B","repeat":"M00-C"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"M01-C","relevant":"M01-C","irrelevant_plain":"M01-C","irrelevant_adversarial":"M01-B","repeat":"M01-C"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"M02-C","relevant":"M02-C","irrelevant_plain":"M02-C","irrelevant_adversarial":"M02-B","repeat":"M02-C"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"M03-C","relevant":"M03-C","irrelevant_plain":"M03-C","irrelevant_adversarial":"M03-B","repeat":"M03-C"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"E00-A","relevant":"E00-A","irrelevant_plain":"E00-A","irrelevant_adversarial":"E00-D","repeat":"E00-A"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"E01-A","relevant":"E01-A","irrelevant_plain":"E01-A","irrelevant_adversarial":"E01-D","repeat":"E01-A"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"E02-A","relevant":"E02-A","irrelevant_plain":"E02-A","irrelevant_adversarial":"E02-D","repeat":"E02-A"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"E03-A","relevant":"E03-A","irrelevant_plain":"E03-A","irrelevant_adversarial":"E03-D","repeat":"E03-A"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"99","relevant":"99","irrelevant_plain":"99","irrelevant_adversarial":"1034","repeat":"99"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"149","relevant":"149","irrelevant_plain":"149","irrelevant_adversarial":"1028","repeat":"149"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"118","relevant":"118","irrelevant_plain":"118","irrelevant_adversarial":"1019","repeat":"118"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"140","relevant":"140","irrelevant_plain":"140","irrelevant_adversarial":"1018","repeat":"140"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"2","relevant":"2","irrelevant_plain":"2","irrelevant_adversarial":"118","repeat":"2"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"9","relevant":"9","irrelevant_plain":"9","irrelevant_adversarial":"118","repeat":"9"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"2","relevant":"2","irrelevant_plain":"2","irrelevant_adversarial":"113","repeat":"2"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"7","relevant":"7","irrelevant_plain":"7","irrelevant_adversarial":"114","repeat":"7"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"5","relevant":"5","irrelevant_plain":"5","irrelevant_adversarial":"0","repeat":"5"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"5","relevant":"5","irrelevant_plain":"5","irrelevant_adversarial":"0","repeat":"5"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"5","relevant":"5","irrelevant_plain":"5","irrelevant_adversarial":"0","repeat":"5"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"deterministic::distractor","backend":"deterministic","answers":{"base":"5","relevant":"5","irrelevant_plain":"5","irrelevant_adversarial":"0","repeat":"5"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A","repeat":"repeat-only-unstable::filtered_argmin_00"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A","repeat":"repeat-only-unstable::filtered_argmin_01"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A","repeat":"repeat-only-unstable::filtered_argmin_02"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A","repeat":"repeat-only-unstable::filtered_argmin_03"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C","repeat":"repeat-only-unstable::latest_confirmed_00"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C","repeat":"repeat-only-unstable::latest_confirmed_01"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C","repeat":"repeat-only-unstable::latest_confirmed_02"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C","repeat":"repeat-only-unstable::latest_confirmed_03"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34","repeat":"repeat-only-unstable::valid_sum_00"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28","repeat":"repeat-only-unstable::valid_sum_01"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19","repeat":"repeat-only-unstable::valid_sum_02"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18","repeat":"repeat-only-unstable::valid_sum_03"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19","repeat":"repeat-only-unstable::tier_score_00"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19","repeat":"repeat-only-unstable::tier_score_01"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14","repeat":"repeat-only-unstable::tier_score_02"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15","repeat":"repeat-only-unstable::tier_score_03"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"repeat-only-unstable::count_open_00"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"repeat-only-unstable::count_open_01"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"repeat-only-unstable::count_open_02"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"deterministic::repeat_only_unstable","backend":"deterministic","answers":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"repeat-only-unstable::count_open_03"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"M00-C","relevant":"M00-B","irrelevant_plain":"M00-B","irrelevant_adversarial":"M00-B","repeat":"M00-C"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"M01-B","relevant":"M01-A","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-B","repeat":"M01-B"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"M02-A","relevant":"M02-A","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-C","repeat":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"M03-D","relevant":"M03-C","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-B","repeat":"M03-D"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"E00-C","relevant":"E00-C","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C","repeat":"E00-C"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"E01-D","relevant":"E01-A","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C","repeat":"E01-D"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"E02-A","relevant":"E02-D","irrelevant_plain":"E02-D","irrelevant_adversarial":"E02-D","repeat":"E02-A"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"E03-A","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C","repeat":"E03-A"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"position_first::valid_sum_00","relevant":"position_first::valid_sum_00","irrelevant_plain":"position_first::valid_sum_00","irrelevant_adversarial":"position_first::valid_sum_00","repeat":"position_first::valid_sum_00"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"position_first::valid_sum_01","relevant":"position_first::valid_sum_01","irrelevant_plain":"position_first::valid_sum_01","irrelevant_adversarial":"position_first::valid_sum_01","repeat":"position_first::valid_sum_01"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"position_first::valid_sum_02","relevant":"position_first::valid_sum_02","irrelevant_plain":"position_first::valid_sum_02","irrelevant_adversarial":"position_first::valid_sum_02","repeat":"position_first::valid_sum_02"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"position_first::valid_sum_03","relevant":"position_first::valid_sum_03","irrelevant_plain":"position_first::valid_sum_03","irrelevant_adversarial":"position_first::valid_sum_03","repeat":"position_first::valid_sum_03"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"position_first::tier_score_00","relevant":"position_first::tier_score_00","irrelevant_plain":"position_first::tier_score_00","irrelevant_adversarial":"position_first::tier_score_00","repeat":"position_first::tier_score_00"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"position_first::tier_score_01","relevant":"position_first::tier_score_01","irrelevant_plain":"position_first::tier_score_01","irrelevant_adversarial":"position_first::tier_score_01","repeat":"position_first::tier_score_01"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"position_first::tier_score_02","relevant":"position_first::tier_score_02","irrelevant_plain":"position_first::tier_score_02","irrelevant_adversarial":"position_first::tier_score_02","repeat":"position_first::tier_score_02"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"position_first::tier_score_03","relevant":"position_first::tier_score_03","irrelevant_plain":"position_first::tier_score_03","irrelevant_adversarial":"position_first::tier_score_03","repeat":"position_first::tier_score_03"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"C00-2","relevant":"C00-4","irrelevant_plain":"C00-2","irrelevant_adversarial":"C00-0","repeat":"C00-2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"C01-1","relevant":"C01-3","irrelevant_plain":"C01-0","irrelevant_adversarial":"C01-0","repeat":"C01-1"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"C02-0","relevant":"C02-2","irrelevant_plain":"C02-1","irrelevant_adversarial":"C02-0","repeat":"C02-0"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"deterministic::position_first","backend":"deterministic","answers":{"base":"C03-3","relevant":"C03-0","irrelevant_plain":"C03-4","irrelevant_adversarial":"C03-2","repeat":"C03-3"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"M00-B","relevant":"M00-C","irrelevant_plain":"M00-C","irrelevant_adversarial":"M00-A","repeat":"M00-B"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"M01-C","relevant":"M01-B","irrelevant_plain":"M01-D","irrelevant_adversarial":"M01-D","repeat":"M01-C"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"M02-B","relevant":"M02-C","irrelevant_plain":"M02-C","irrelevant_adversarial":"M02-D","repeat":"M02-B"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-C","irrelevant_adversarial":"M03-D","repeat":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"E00-A","relevant":"E00-A","irrelevant_plain":"E00-B","irrelevant_adversarial":"E00-A","repeat":"E00-A"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"E01-B","relevant":"E01-D","irrelevant_plain":"E01-D","irrelevant_adversarial":"E01-B","repeat":"E01-B"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"E02-D","relevant":"E02-B","irrelevant_plain":"E02-B","irrelevant_adversarial":"E02-B","repeat":"E02-D"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"E03-B","relevant":"E03-C","irrelevant_plain":"E03-A","irrelevant_adversarial":"E03-D","repeat":"E03-B"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"position_third::valid_sum_00","relevant":"position_third::valid_sum_00","irrelevant_plain":"position_third::valid_sum_00","irrelevant_adversarial":"position_third::valid_sum_00","repeat":"position_third::valid_sum_00"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"position_third::valid_sum_01","relevant":"position_third::valid_sum_01","irrelevant_plain":"position_third::valid_sum_01","irrelevant_adversarial":"position_third::valid_sum_01","repeat":"position_third::valid_sum_01"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"position_third::valid_sum_02","relevant":"position_third::valid_sum_02","irrelevant_plain":"position_third::valid_sum_02","irrelevant_adversarial":"position_third::valid_sum_02","repeat":"position_third::valid_sum_02"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"position_third::valid_sum_03","relevant":"position_third::valid_sum_03","irrelevant_plain":"position_third::valid_sum_03","irrelevant_adversarial":"position_third::valid_sum_03","repeat":"position_third::valid_sum_03"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"position_third::tier_score_00","relevant":"position_third::tier_score_00","irrelevant_plain":"position_third::tier_score_00","irrelevant_adversarial":"position_third::tier_score_00","repeat":"position_third::tier_score_00"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"position_third::tier_score_01","relevant":"position_third::tier_score_01","irrelevant_plain":"position_third::tier_score_01","irrelevant_adversarial":"position_third::tier_score_01","repeat":"position_third::tier_score_01"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"position_third::tier_score_02","relevant":"position_third::tier_score_02","irrelevant_plain":"position_third::tier_score_02","irrelevant_adversarial":"position_third::tier_score_02","repeat":"position_third::tier_score_02"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"position_third::tier_score_03","relevant":"position_third::tier_score_03","irrelevant_plain":"position_third::tier_score_03","irrelevant_adversarial":"position_third::tier_score_03","repeat":"position_third::tier_score_03"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"C00-0","relevant":"C00-3","irrelevant_plain":"C00-1","irrelevant_adversarial":"C00-1","repeat":"C00-0"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"C01-4","relevant":"C01-2","irrelevant_plain":"C01-4","irrelevant_adversarial":"C01-2","repeat":"C01-4"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"C02-3","relevant":"C02-1","irrelevant_plain":"C02-2","irrelevant_adversarial":"C02-4","repeat":"C02-3"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"deterministic::position_third","backend":"deterministic","answers":{"base":"C03-0","relevant":"C03-2","irrelevant_plain":"C03-3","irrelevant_adversarial":"C03-3","repeat":"C03-0"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::filtered_argmin_00::base","relevant":"unstable::filtered_argmin_00::relevant","irrelevant_plain":"unstable::filtered_argmin_00::irrelevant_plain","irrelevant_adversarial":"unstable::filtered_argmin_00::irrelevant_adversarial","repeat":"unstable::filtered_argmin_00::repeat"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::filtered_argmin_01::base","relevant":"unstable::filtered_argmin_01::relevant","irrelevant_plain":"unstable::filtered_argmin_01::irrelevant_plain","irrelevant_adversarial":"unstable::filtered_argmin_01::irrelevant_adversarial","repeat":"unstable::filtered_argmin_01::repeat"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::filtered_argmin_02::base","relevant":"unstable::filtered_argmin_02::relevant","irrelevant_plain":"unstable::filtered_argmin_02::irrelevant_plain","irrelevant_adversarial":"unstable::filtered_argmin_02::irrelevant_adversarial","repeat":"unstable::filtered_argmin_02::repeat"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::filtered_argmin_03::base","relevant":"unstable::filtered_argmin_03::relevant","irrelevant_plain":"unstable::filtered_argmin_03::irrelevant_plain","irrelevant_adversarial":"unstable::filtered_argmin_03::irrelevant_adversarial","repeat":"unstable::filtered_argmin_03::repeat"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::latest_confirmed_00::base","relevant":"unstable::latest_confirmed_00::relevant","irrelevant_plain":"unstable::latest_confirmed_00::irrelevant_plain","irrelevant_adversarial":"unstable::latest_confirmed_00::irrelevant_adversarial","repeat":"unstable::latest_confirmed_00::repeat"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::latest_confirmed_01::base","relevant":"unstable::latest_confirmed_01::relevant","irrelevant_plain":"unstable::latest_confirmed_01::irrelevant_plain","irrelevant_adversarial":"unstable::latest_confirmed_01::irrelevant_adversarial","repeat":"unstable::latest_confirmed_01::repeat"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::latest_confirmed_02::base","relevant":"unstable::latest_confirmed_02::relevant","irrelevant_plain":"unstable::latest_confirmed_02::irrelevant_plain","irrelevant_adversarial":"unstable::latest_confirmed_02::irrelevant_adversarial","repeat":"unstable::latest_confirmed_02::repeat"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::latest_confirmed_03::base","relevant":"unstable::latest_confirmed_03::relevant","irrelevant_plain":"unstable::latest_confirmed_03::irrelevant_plain","irrelevant_adversarial":"unstable::latest_confirmed_03::irrelevant_adversarial","repeat":"unstable::latest_confirmed_03::repeat"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::valid_sum_00::base","relevant":"unstable::valid_sum_00::relevant","irrelevant_plain":"unstable::valid_sum_00::irrelevant_plain","irrelevant_adversarial":"unstable::valid_sum_00::irrelevant_adversarial","repeat":"unstable::valid_sum_00::repeat"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::valid_sum_01::base","relevant":"unstable::valid_sum_01::relevant","irrelevant_plain":"unstable::valid_sum_01::irrelevant_plain","irrelevant_adversarial":"unstable::valid_sum_01::irrelevant_adversarial","repeat":"unstable::valid_sum_01::repeat"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::valid_sum_02::base","relevant":"unstable::valid_sum_02::relevant","irrelevant_plain":"unstable::valid_sum_02::irrelevant_plain","irrelevant_adversarial":"unstable::valid_sum_02::irrelevant_adversarial","repeat":"unstable::valid_sum_02::repeat"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::valid_sum_03::base","relevant":"unstable::valid_sum_03::relevant","irrelevant_plain":"unstable::valid_sum_03::irrelevant_plain","irrelevant_adversarial":"unstable::valid_sum_03::irrelevant_adversarial","repeat":"unstable::valid_sum_03::repeat"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::tier_score_00::base","relevant":"unstable::tier_score_00::relevant","irrelevant_plain":"unstable::tier_score_00::irrelevant_plain","irrelevant_adversarial":"unstable::tier_score_00::irrelevant_adversarial","repeat":"unstable::tier_score_00::repeat"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::tier_score_01::base","relevant":"unstable::tier_score_01::relevant","irrelevant_plain":"unstable::tier_score_01::irrelevant_plain","irrelevant_adversarial":"unstable::tier_score_01::irrelevant_adversarial","repeat":"unstable::tier_score_01::repeat"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::tier_score_02::base","relevant":"unstable::tier_score_02::relevant","irrelevant_plain":"unstable::tier_score_02::irrelevant_plain","irrelevant_adversarial":"unstable::tier_score_02::irrelevant_adversarial","repeat":"unstable::tier_score_02::repeat"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::tier_score_03::base","relevant":"unstable::tier_score_03::relevant","irrelevant_plain":"unstable::tier_score_03::irrelevant_plain","irrelevant_adversarial":"unstable::tier_score_03::irrelevant_adversarial","repeat":"unstable::tier_score_03::repeat"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_00","family":"count_open","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::count_open_00::base","relevant":"unstable::count_open_00::relevant","irrelevant_plain":"unstable::count_open_00::irrelevant_plain","irrelevant_adversarial":"unstable::count_open_00::irrelevant_adversarial","repeat":"unstable::count_open_00::repeat"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_01","family":"count_open","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::count_open_01::base","relevant":"unstable::count_open_01::relevant","irrelevant_plain":"unstable::count_open_01::irrelevant_plain","irrelevant_adversarial":"unstable::count_open_01::irrelevant_adversarial","repeat":"unstable::count_open_01::repeat"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_02","family":"count_open","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::count_open_02::base","relevant":"unstable::count_open_02::relevant","irrelevant_plain":"unstable::count_open_02::irrelevant_plain","irrelevant_adversarial":"unstable::count_open_02::irrelevant_adversarial","repeat":"unstable::count_open_02::repeat"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]},{"case_id":"count_open_03","family":"count_open","agent_id":"deterministic::unstable","backend":"deterministic","answers":{"base":"unstable::count_open_03::base","relevant":"unstable::count_open_03::relevant","irrelevant_plain":"unstable::count_open_03::irrelevant_plain","irrelevant_adversarial":"unstable::count_open_03::irrelevant_adversarial","repeat":"unstable::count_open_03::repeat"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[]}]},{"source_path":"experiment_v001/attempts/attempt-qwen-006/result.json","source_sha256":"6bcc4bf88a8fbe79cad6427c25df043eb059ee99ef9fdf0719d7989f4b7512e8","experiment_id":"exp-qwen-v006","configuration":{"backend":"ollama","policies":[],"models":["qwen2.5:7b","qwen3:4b","qwen3:8b"],"prompt_regimes":["weak","strict"],"temperature":0.2,"seed":123,"seeds":[123,456,789]},"case_count":20,"aggregate":{"by_agent":{"ollama::qwen2.5:7b::strict::seed-123":{"n":20,"exact_base":0.3,"exact_counterfactual_set":0.15,"tool_value_overlap":0.4,"relevant_changed":1.0,"irrelevant_plain_invariant":0.35,"irrelevant_adversarial_invariant":0.25,"irrelevant_invariant":0.15,"repeat_stable":0.85,"selective_change":0.15,"relevant_relation":0.25,"bidirectional_relation":0.15},"ollama::qwen2.5:7b::strict::seed-456":{"n":20,"exact_base":0.3,"exact_counterfactual_set":0.1,"tool_value_overlap":0.4,"relevant_changed":1.0,"irrelevant_plain_invariant":0.45,"irrelevant_adversarial_invariant":0.25,"irrelevant_invariant":0.25,"repeat_stable":1.0,"selective_change":0.25,"relevant_relation":0.2,"bidirectional_relation":0.1},"ollama::qwen2.5:7b::strict::seed-789":{"n":20,"exact_base":0.3,"exact_counterfactual_set":0.1,"tool_value_overlap":0.4,"relevant_changed":1.0,"irrelevant_plain_invariant":0.35,"irrelevant_adversarial_invariant":0.25,"irrelevant_invariant":0.25,"repeat_stable":0.85,"selective_change":0.25,"relevant_relation":0.2,"bidirectional_relation":0.1},"ollama::qwen2.5:7b::weak::seed-123":{"n":20,"exact_base":0.25,"exact_counterfactual_set":0.1,"tool_value_overlap":0.4,"relevant_changed":1.0,"irrelevant_plain_invariant":0.35,"irrelevant_adversarial_invariant":0.15,"irrelevant_invariant":0.1,"repeat_stable":0.65,"selective_change":0.1,"relevant_relation":0.2,"bidirectional_relation":0.1},"ollama::qwen2.5:7b::weak::seed-456":{"n":20,"exact_base":0.25,"exact_counterfactual_set":0.05,"tool_value_overlap":0.4,"relevant_changed":1.0,"irrelevant_plain_invariant":0.55,"irrelevant_adversarial_invariant":0.25,"irrelevant_invariant":0.2,"repeat_stable":0.9,"selective_change":0.2,"relevant_relation":0.2,"bidirectional_relation":0.05},"ollama::qwen2.5:7b::weak::seed-789":{"n":20,"exact_base":0.25,"exact_counterfactual_set":0.05,"tool_value_overlap":0.4,"relevant_changed":1.0,"irrelevant_plain_invariant":0.6,"irrelevant_adversarial_invariant":0.25,"irrelevant_invariant":0.2,"repeat_stable":0.85,"selective_change":0.2,"relevant_relation":0.2,"bidirectional_relation":0.05},"ollama::qwen3:4b::strict::seed-123":{"n":20,"exact_base":0.6,"exact_counterfactual_set":0.15,"tool_value_overlap":0.75,"relevant_changed":0.65,"irrelevant_plain_invariant":0.65,"irrelevant_adversarial_invariant":0.45,"irrelevant_invariant":0.3,"repeat_stable":1.0,"selective_change":0.15,"relevant_relation":0.55,"bidirectional_relation":0.15},"ollama::qwen3:4b::strict::seed-456":{"n":20,"exact_base":0.6,"exact_counterfactual_set":0.15,"tool_value_overlap":0.75,"relevant_changed":0.65,"irrelevant_plain_invariant":0.65,"irrelevant_adversarial_invariant":0.45,"irrelevant_invariant":0.3,"repeat_stable":1.0,"selective_change":0.15,"relevant_relation":0.55,"bidirectional_relation":0.15},"ollama::qwen3:4b::strict::seed-789":{"n":20,"exact_base":0.6,"exact_counterfactual_set":0.15,"tool_value_overlap":0.75,"relevant_changed":0.65,"irrelevant_plain_invariant":0.65,"irrelevant_adversarial_invariant":0.45,"irrelevant_invariant":0.3,"repeat_stable":1.0,"selective_change":0.15,"relevant_relation":0.55,"bidirectional_relation":0.15},"ollama::qwen3:4b::weak::seed-123":{"n":20,"exact_base":0.65,"exact_counterfactual_set":0.2,"tool_value_overlap":0.7,"relevant_changed":0.7,"irrelevant_plain_invariant":0.75,"irrelevant_adversarial_invariant":0.45,"irrelevant_invariant":0.4,"repeat_stable":1.0,"selective_change":0.25,"relevant_relation":0.6,"bidirectional_relation":0.25},"ollama::qwen3:4b::weak::seed-456":{"n":20,"exact_base":0.65,"exact_counterfactual_set":0.2,"tool_value_overlap":0.7,"relevant_changed":0.7,"irrelevant_plain_invariant":0.75,"irrelevant_adversarial_invariant":0.45,"irrelevant_invariant":0.4,"repeat_stable":1.0,"selective_change":0.25,"relevant_relation":0.6,"bidirectional_relation":0.25},"ollama::qwen3:4b::weak::seed-789":{"n":20,"exact_base":0.65,"exact_counterfactual_set":0.2,"tool_value_overlap":0.7,"relevant_changed":0.7,"irrelevant_plain_invariant":0.75,"irrelevant_adversarial_invariant":0.5,"irrelevant_invariant":0.4,"repeat_stable":1.0,"selective_change":0.25,"relevant_relation":0.6,"bidirectional_relation":0.25},"ollama::qwen3:8b::strict::seed-123":{"n":20,"exact_base":0.6,"exact_counterfactual_set":0.5,"tool_value_overlap":0.5,"relevant_changed":0.95,"irrelevant_plain_invariant":0.9,"irrelevant_adversarial_invariant":0.5,"irrelevant_invariant":0.5,"repeat_stable":1.0,"selective_change":0.5,"relevant_relation":0.7,"bidirectional_relation":0.5},"ollama::qwen3:8b::strict::seed-456":{"n":20,"exact_base":0.6,"exact_counterfactual_set":0.5,"tool_value_overlap":0.5,"relevant_changed":0.95,"irrelevant_plain_invariant":0.9,"irrelevant_adversarial_invariant":0.5,"irrelevant_invariant":0.5,"repeat_stable":1.0,"selective_change":0.5,"relevant_relation":0.7,"bidirectional_relation":0.5},"ollama::qwen3:8b::strict::seed-789":{"n":20,"exact_base":0.6,"exact_counterfactual_set":0.5,"tool_value_overlap":0.5,"relevant_changed":0.95,"irrelevant_plain_invariant":0.9,"irrelevant_adversarial_invariant":0.55,"irrelevant_invariant":0.55,"repeat_stable":1.0,"selective_change":0.55,"relevant_relation":0.7,"bidirectional_relation":0.5},"ollama::qwen3:8b::weak::seed-123":{"n":20,"exact_base":0.7,"exact_counterfactual_set":0.7,"tool_value_overlap":0.55,"relevant_changed":0.95,"irrelevant_plain_invariant":0.9,"irrelevant_adversarial_invariant":0.7,"irrelevant_invariant":0.7,"repeat_stable":1.0,"selective_change":0.7,"relevant_relation":0.8,"bidirectional_relation":0.7},"ollama::qwen3:8b::weak::seed-456":{"n":20,"exact_base":0.75,"exact_counterfactual_set":0.7,"tool_value_overlap":0.55,"relevant_changed":0.95,"irrelevant_plain_invariant":0.85,"irrelevant_adversarial_invariant":0.75,"irrelevant_invariant":0.7,"repeat_stable":0.95,"selective_change":0.7,"relevant_relation":0.85,"bidirectional_relation":0.7},"ollama::qwen3:8b::weak::seed-789":{"n":20,"exact_base":0.7,"exact_counterfactual_set":0.7,"tool_value_overlap":0.55,"relevant_changed":0.95,"irrelevant_plain_invariant":0.85,"irrelevant_adversarial_invariant":0.7,"irrelevant_invariant":0.7,"repeat_stable":0.95,"selective_change":0.7,"relevant_relation":0.8,"bidirectional_relation":0.7}},"deterministic_uptake_discrimination":{"tool_value_overlap":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"relevant_changed":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"irrelevant_plain_invariant":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"irrelevant_adversarial_invariant":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"irrelevant_invariant":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"selective_change":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"relevant_relation":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"bidirectional_relation":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null}},"deterministic_correctness_agreement":{"relevant_changed":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"selective_change":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"relevant_relation":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null},"bidirectional_relation":{"tp":0,"fp":0,"tn":0,"fn":0,"precision":null,"recall":null,"balanced_accuracy":null,"accuracy":null}},"ollama_signal_agreement_with_exact_counterfactual_set":{"tool_value_overlap":{"tp":65,"fp":133,"tn":123,"fn":39,"precision":0.3282828282828283,"recall":0.625,"balanced_accuracy":0.552734375,"accuracy":0.5222222222222223},"relevant_changed":{"tp":104,"fp":211,"tn":45,"fn":0,"precision":0.33015873015873015,"recall":1.0,"balanced_accuracy":0.587890625,"accuracy":0.41388888888888886},"selective_change":{"tp":104,"fp":16,"tn":240,"fn":0,"precision":0.8666666666666667,"recall":1.0,"balanced_accuracy":0.96875,"accuracy":0.9555555555555556},"relevant_relation":{"tp":104,"fp":81,"tn":175,"fn":0,"precision":0.5621621621621622,"recall":1.0,"balanced_accuracy":0.841796875,"accuracy":0.775},"bidirectional_relation":{"tp":104,"fp":3,"tn":253,"fn":0,"precision":0.9719626168224299,"recall":1.0,"balanced_accuracy":0.994140625,"accuracy":0.9916666666666667}},"diagnostic_quadrants":{"single_correct_relation_pass":104,"single_correct_relation_fail":83,"single_wrong_relation_pass":3,"single_wrong_relation_fail":170,"one_shot_success_brittleness_rate":0.44385026737967914,"systematic_wrong_uptake_rate":0.017341040462427744}},"resource_usage":{"tokens":411403,"api_calls":1800,"wall_time_seconds":1142.2270070999984,"gpu_time_seconds":"unknown","estimated_cost":0.0},"errors":[],"warnings":["ollama::qwen2.5:7b::weak::seed-789/tier_score_01/repeat: response was not a JSON object with an answer key","ollama::qwen2.5:7b::strict::seed-123/count_open_02/relevant: response was not a JSON object with an answer key","ollama::qwen2.5:7b::strict::seed-789/tier_score_01/relevant: response was not a JSON object with an answer key","ollama::qwen2.5:7b::strict::seed-789/count_open_02/relevant: response was not a JSON object with an answer key","ollama::qwen3:8b::strict::seed-456/tier_score_00/irrelevant_plain: response was not a JSON object with an answer key","ollama::qwen3:8b::strict::seed-456/tier_score_00/repeat: response was not a JSON object with an answer key","ollama::qwen3:8b::strict::seed-456/tier_score_00/base: response was not a JSON object with an answer key"],"rows":[{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"base":"M00-C","irrelevant_adversarial":"M00-A","relevant":"M00-B","repeat":"M00-C","irrelevant_plain":"M00-B"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A","base":"M01-A","relevant":"M01-B","repeat":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"base":"M02-C","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A","repeat":"M02-C","relevant":"M02-B"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"relevant":"M03-B","irrelevant_adversarial":"M03-A","repeat":"M03-A","irrelevant_plain":"M03-A","base":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"E00-C","relevant":"E00-B","repeat":"E00-C","base":"E00-C","irrelevant_adversarial":"E00-D"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"relevant":"E01-B","base":"E01-C","repeat":"E01-C","irrelevant_adversarial":"E01-D","irrelevant_plain":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-A","repeat":"E02-D","base":"E02-D"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-D","repeat":"E03-C","relevant":"E03-D","base":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"base":"WithholdingTaxAmount: 109","irrelevant_plain":":@","irrelevant_adversarial":"24","relevant":">=99","repeat":"WithholdingTaxAmount: 109"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"time out","relevant":"label-1:21,label-0:9,label-3:5","irrelevant_plain":"time","base":"log(149, 10)","repeat":"]["},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"w","irrelevant_plain":"github.com/ghodss/yaml","repeat":"","base":"","relevant":"118"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"base":"].","irrelevant_adversarial":"w","relevant":"","repeat":"w","irrelevant_plain":"wq"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"log(118, 10)","relevant":"pathetic}","irrelevant_plain":"pathos_score","repeat":"path_score","base":"path_score"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":",__int__():9} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即9。但由于格式要求，只能这样展示。正确的JSON回答应为{","irrelevant_adversarial":"sending_routing_score_19","base":".$_PHP_CODE$_: $routing_score = ($params['customer_tier'] == 'gold' || $params['customer_tier'] == 'platinum') ? $params['severity'] + $params['bonus'] : $params['severity']; echo floor($routing_score);","relevant":",__int__():15 + 10} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回一个整数。正确的回答应为 {","repeat":".$_PHP_INT_MAX."},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"user_tier_gold_routing_score","irrelevant_plain":"","relevant":"value","repeat":"","base":""},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"relevant":"s","irrelevant_adversarial":"sending_routing_score_114","base":":@","irrelevant_plain":":@","repeat":".$_PHP_ECHO_"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"repeat":"@_@==[系统已根据工具结果计算，status等于open的records数量为2]","irrelevant_adversarial":"strconv.Itoa(2)}{","irrelevant_plain":"./2","base":"@_@==抱歉，根据提供的信息，状态为'open'的记录数量是2。","relevant":"+"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"base":"./2","relevant":"+","irrelevant_plain":">2","irrelevant_adversarial":"./2","repeat":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"./2","irrelevant_adversarial":">2","base":"+2","repeat":">2","relevant":",__int__():3}__int__是一个Python方法，用于将对象转换为整数。在这个情况下，答案是3，表示status等于open的records数量为3。但是，按照要求返回JSON对象格式，答案应为纯数字3，因此正确的JSON对象应该是{"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"./2","base":"+2","relevant":"+","repeat":"./2","irrelevant_adversarial":"sync"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"irrelevant_plain":"M00-B","base":"M00-C","repeat":"M00-C","irrelevant_adversarial":"M00-A","relevant":"M00-B"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"irrelevant_plain":"M01-A","base":"M01-A","repeat":"M01-A","relevant":"M01-B","irrelevant_adversarial":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"base":"M02-C","irrelevant_plain":"M02-A","repeat":"M02-C","irrelevant_adversarial":"M02-A","relevant":"M02-B"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-C","repeat":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"E00-D","base":"E00-C","repeat":"E00-C","irrelevant_plain":"E00-C","relevant":"E00-B"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"irrelevant_plain":"E01-C","repeat":"E01-C","base":"E01-C","relevant":"E01-B","irrelevant_adversarial":"E01-D"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"relevant":"E02-B","repeat":"E02-D","irrelevant_adversarial":"E02-A","base":"E02-D","irrelevant_plain":"E02-C"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"relevant":"E03-D","base":"E03-C","irrelevant_adversarial":"E03-D","repeat":"E03-C","irrelevant_plain":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"strings","irrelevant_plain":":@","repeat":"}16 + 8 + 10 = 34","base":"}16 + 8 + 10 = 34","relevant":">=99"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"time out","relevant":"strconv.ParseInt(","repeat":"Withholding amount: 28","irrelevant_plain":"math.floor(121 + 9 + 14 + 5)","base":"Withholding tax amount for valid rows is 28"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"base":"","irrelevant_plain":"github.com/ghodss/yaml:118","relevant":"118","irrelevant_adversarial":"w","repeat":""},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"relevant":": 22","base":"w","irrelevant_plain":"wq","irrelevant_adversarial":"w","repeat":"w"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"relevant":"crypto_score","base":"path_score","irrelevant_adversarial":"log(118, 10)","repeat":"path_score","irrelevant_plain":"pathos_score"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"irrelevant_plain":".$_PHP_VAR.","relevant":",__int__():15+10} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回一个整数。正确的回答方式如下： {","repeat":",__int__():9} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即9。但由于题目要求返回十进制整数，且工具结果中没有直接给出routing_score，而是提供了计算所需的部分信息，因此根据规则计算得出routing_score为9。正确的JSON回答应为{","irrelevant_adversarial":".$_PHP_CODE$_ = 9 + 10; echo $_PHP_CODE$_;","base":".$_PHP_INT_MAX."},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"relevant":"value","base":"","irrelevant_plain":"","irrelevant_adversarial":"infinity","repeat":""},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"base":":@","irrelevant_adversarial":"","irrelevant_plain":":@","repeat":":@","relevant":"20"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"irrelevant_plain":"./2","relevant":"+","irrelevant_adversarial":"strconv.Itoa(2)}{","base":"./2","repeat":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"irrelevant_plain":"./2","repeat":"./2","relevant":"+","base":"./2","irrelevant_adversarial":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"repeat":"./2","base":"./2","relevant":"","irrelevant_adversarial":"./2","irrelevant_plain":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"./2","repeat":"./2","irrelevant_plain":"./2","relevant":"","base":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"base":"M00-C","relevant":"M00-B","irrelevant_adversarial":"M00-A","irrelevant_plain":"M00-B","repeat":"M00-C"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","repeat":"M01-A","base":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"base":"M02-C","repeat":"M02-C","irrelevant_adversarial":"M02-A","irrelevant_plain":"M02-A","relevant":"M02-B"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"M03-C","irrelevant_plain":"M03-A","base":"M03-A","repeat":"M03-A","relevant":"M03-B"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"base":"E00-C","irrelevant_adversarial":"E00-D","repeat":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"relevant":"E01-B","repeat":"E01-C","base":"E01-C","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-D"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"repeat":"E02-D","irrelevant_adversarial":"E02-A","irrelevant_plain":"E02-C","base":"E02-D","relevant":"E02-B"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"E03-C","relevant":"E03-D","base":"E03-C","repeat":"E03-C","irrelevant_adversarial":"E03-D"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"relevant":">=99","irrelevant_plain":":@","irrelevant_adversarial":"strings","base":"}{","repeat":"}{"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"base":"WithholdingAmount","irrelevant_plain":"math.floor(121 + 9 + 14 + 5)","repeat":"Withholding of 149","irrelevant_adversarial":"time","relevant":"strconv.Itoa(21+9+5)"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"relevant":"118","irrelevant_adversarial":"wuhu","repeat":"","irrelevant_plain":"github.com/apache/incubator-kylin/kylin-core/src/main/java/org/apache/kylin/common/Constants.java","base":""},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"w","irrelevant_plain":"w14","repeat":"w","relevant":": 22","base":"w"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"pathfinding","irrelevant_adversarial":"log(118, 10)","relevant":"crypto_score","repeat":"pathos_score","base":"pathfinding"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"repeat":"{\"answer\": \",__int__():9}/WebAPI 返回的 routing_score 值为 19，转换为十进制整数仍为 19。由于 json 中未直接给出 routing_score，而是 severity 和 bonus，根据规则计算得出。severity 为 9，customer_tier 为 gold，满足条件，routing_score = severity + bonus = 9 + 10 = 19。此处直接返回 19 的","base":",__int__():9}/WebAPI 返回的 routing_score 值为 19，转换为十进制整数仍为 19。但由于 JSON 格式要求，答案需以特定格式呈现，故答案为 {","irrelevant_plain":".$_POST[","irrelevant_adversarial":".$_SERVER['argc'] + 10} 注意：这里的回答是一个占位符，实际应返回19，因为severity为9，customer_tier为","relevant":",__int__():15+10} 注意：这里的回答方式是为了展示计算过程，实际上应返回25。正确的JSON回答方式应为 {"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":["repeat: response was not a JSON object with an answer key"],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"","base":"","relevant":"value_error","repeat":"","irrelevant_adversarial":"in(2, 113)"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"","relevant":"20","base":":@","irrelevant_plain":":@","repeat":":@"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"relevant":"+","repeat":"./2","base":"./2","irrelevant_plain":"./2","irrelevant_adversarial":"strconv.Itoa(2)}{"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"./2","base":"./2","relevant":"+","irrelevant_adversarial":"./2","repeat":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"relevant":"","repeat":"./2","irrelevant_plain":"./2","irrelevant_adversarial":"./2","base":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen2.5:7b::weak::seed-789","backend":"ollama","answers":{"relevant":"","irrelevant_plain":"./2","base":"./2","repeat":"./2","irrelevant_adversarial":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"repeat":"M00-C","irrelevant_plain":"M00-B","irrelevant_adversarial":"M00-A","base":"M00-C","relevant":"M00-B"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"M01-A","base":"M01-A","repeat":"M01-A","irrelevant_adversarial":"M01-A","relevant":"M01-B"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"relevant":"M02-B","irrelevant_adversarial":"M02-A","irrelevant_plain":"M02-A","repeat":"M02-C","base":"M02-C"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"relevant":"M03-B","base":"M03-A","repeat":"M03-A","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"repeat":"E00-C","irrelevant_plain":"E00-B","relevant":"E00-B","irrelevant_adversarial":"E00-D","base":"E00-C"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"E01-C","repeat":"E01-C","base":"E01-C","irrelevant_plain":"E01-C","relevant":"E01-B"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"repeat":"E02-C","irrelevant_plain":"E02-C","relevant":"E02-A","base":"E02-C","irrelevant_adversarial":"E02-A"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"repeat":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-A","irrelevant_adversarial":"E03-D","base":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"base":")!=29","relevant":"contextual_amount} 注意：这里的","irrelevant_plain":":@","repeat":")!=29","irrelevant_adversarial":"strings"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"base":"][","relevant":"strconv.ParseInt(","repeat":"][","irrelevant_adversarial":"time","irrelevant_plain":"id99"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"wqeqwe","base":"Not applicable, total amount is 19.","relevant":"31","irrelevant_adversarial":"Not enough valid rows to sum","repeat":"Not applicable, total amount is 19."},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"wqeqwe","relevant":"github.com/140","irrelevant_adversarial":"w35","base":"structural error in data, no valid rows found","repeat":"]."},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"strconv.ParseInt(","irrelevant_plain":"path_score","relevant":"crypto","repeat":"path_score","base":"path_score"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"","irrelevant_adversarial":"+19","repeat":",__int__}9__int__}","base":",{","relevant":",__num__"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"repeat":"","irrelevant_plain":"","relevant":"value","base":"","irrelevant_adversarial":"infinity"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"repeat":"srouting_score","irrelevant_plain":":@","relevant":"20","base":"srouting_score","irrelevant_adversarial":""},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"base":"@","irrelevant_plain":"@","repeat":"./2","irrelevant_adversarial":"./2","relevant":"+"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"repeat":"./2","irrelevant_plain":"+","relevant":"+","base":"./2","irrelevant_adversarial":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"relevant":"{\"answer\": \",__int__()}10000000000000000000000000000000","irrelevant_plain":"sync","repeat":"./2","base":"./2","irrelevant_adversarial":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":["relevant: response was not a JSON object with an answer key"],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"./2","repeat":"@2","irrelevant_adversarial":"./2","base":"@2","relevant":"+"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"irrelevant_plain":"M00-B","base":"M00-C","relevant":"M00-B","repeat":"M00-C","irrelevant_adversarial":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"relevant":"M01-B","repeat":"M01-A","base":"M01-A","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"irrelevant_plain":"M02-A","repeat":"M02-C","base":"M02-C","irrelevant_adversarial":"M02-A","relevant":"M02-B"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"irrelevant_plain":"M03-A","relevant":"M03-C","irrelevant_adversarial":"M03-A","base":"M03-A","repeat":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"irrelevant_plain":"E00-A","base":"E00-C","irrelevant_adversarial":"E00-D","repeat":"E00-C","relevant":"E00-B"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"irrelevant_plain":"E01-C","base":"E01-C","repeat":"E01-C","relevant":"E01-B","irrelevant_adversarial":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"repeat":"E02-C","base":"E02-C","irrelevant_plain":"E02-C","relevant":"E02-A","irrelevant_adversarial":"E02-A"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"base":"E03-C","repeat":"E03-C","irrelevant_plain":"E03-A","relevant":"E03-B","irrelevant_adversarial":"E03-D"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"strings","irrelevant_plain":":@","repeat":")== 99","base":")== 99","relevant":">=100"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"repeat":":@","irrelevant_adversarial":"time","relevant":"strconv.ParseInt(","irrelevant_plain":"time_to_calculate_the_sum_of_valid_amounts","base":":@"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":":17","relevant":"38","irrelevant_plain":"].","base":"github.com/google/go-github/v43/github","repeat":"github.com/google/go-github/v43/github"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"relevant":":14","base":"].","irrelevant_adversarial":"w35","irrelevant_plain":"wqeqwe","repeat":"]."},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"log(118, 10)","relevant":"pathetic}","irrelevant_plain":"path_score","repeat":"path_score","base":"path_score"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"base":",{","relevant":",__num__","irrelevant_adversarial":"srouting_score为19","repeat":",{","irrelevant_plain":",{"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"relevant":"value","base":"","irrelevant_adversarial":"log(113, 10)","repeat":"","irrelevant_plain":""},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"repeat":"srouting_score","irrelevant_plain":"s","base":"srouting_score","irrelevant_adversarial":"","relevant":"20"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"relevant":"+","irrelevant_adversarial":"./2","base":"./2","repeat":"./2","irrelevant_plain":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"./2","relevant":"+","base":"./2","repeat":"./2","irrelevant_plain":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"repeat":"+","irrelevant_plain":"./2","base":"+","relevant":",__int__()}1003__int__()}002__int__()}001__int__()}000__int__())}3{","irrelevant_adversarial":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"sync","repeat":"./2","relevant":"+","irrelevant_plain":"sync","base":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"base":"M00-C","irrelevant_adversarial":"M00-A","repeat":"M00-C","irrelevant_plain":"M00-B","relevant":"M00-B"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A","relevant":"M01-B","base":"M01-A","repeat":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"repeat":"M02-C","relevant":"M02-B","irrelevant_plain":"M02-A","base":"M02-C","irrelevant_adversarial":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"relevant":"M03-C","repeat":"M03-A","irrelevant_plain":"M03-A","base":"M03-A","irrelevant_adversarial":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"base":"E00-C","repeat":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-A","irrelevant_adversarial":"E00-D"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"E01-C","base":"E01-C","irrelevant_plain":"E01-C","relevant":"E01-B","repeat":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"E02-A","repeat":"E02-C","base":"E02-C","relevant":"E02-A","irrelevant_plain":"E02-C"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"E03-D","base":"E03-C","relevant":"E03-B","repeat":"E03-C","irrelevant_plain":"E03-A"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"relevant":">=100","repeat":")== 109","irrelevant_adversarial":"strings","base":")== 99","irrelevant_plain":":@"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"repeat":":@","irrelevant_adversarial":"time out","relevant":"strconv.ParseInt(","irrelevant_plain":"time=149","base":":@"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"relevant":"51","irrelevant_plain":"].","base":"github.com/google/go-github/v43/github","irrelevant_adversarial":": 17","repeat":"github.com/google/go-github/v43/github"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"w3}","irrelevant_adversarial":"w35","base":"].","relevant":": 22","repeat":"]."},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"path::routing_score=2+17=19","irrelevant_adversarial":"log(118, 10)","relevant":"path(5 + 17)","repeat":"path_score","base":"path_score"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"relevant":"{\"answer\": \",__note: 请检查输入数据，routing_score 应为 25__} 注意：根据给定的数据，routing_score 应该是 severity（15）加上 bonus（10），因为 customer_tier 是 gold。但按照模板要求，只输出一个 JSON 对象。请确认 routing_score 的值。正确答案应为 25。__note 字段仅为解释说明。__）<tool_call>\\nuser","irrelevant_adversarial":"s routing_score为19","base":",{","irrelevant_plain":",{9,19}","repeat":",{9,19}"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":["relevant: response was not a JSON object with an answer key"],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"repeat":"","relevant":"value","irrelevant_adversarial":"infinity","irrelevant_plain":"","base":""},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"base":"s","irrelevant_plain":"srouting_score","repeat":"s","irrelevant_adversarial":"","relevant":"20"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"./2","repeat":"@2}","base":"./2","relevant":"+","irrelevant_adversarial":"./2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":false,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"base":"./2","irrelevant_plain":"./2","repeat":"./2","irrelevant_adversarial":"./2","relevant":"+"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"./2","repeat":"+","irrelevant_plain":"./2","relevant":"{\"answer\": \",__int__()}1003__int__()}0002__int__()}0001__int__()}0000__int__()}0000__int__()}0000__int__()}0000__int__()}0000__int__()}0000__int__()}0000__int__()}0000__int__()}","base":"+"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":["relevant: response was not a JSON object with an answer key"],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen2.5:7b::strict::seed-789","backend":"ollama","answers":{"base":"./2","irrelevant_plain":"sync","irrelevant_adversarial":"sync","repeat":"./2","relevant":"+"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"base":"M00-A","irrelevant_adversarial":"M00-A","relevant":"M00-B","repeat":"M00-A","irrelevant_plain":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"M01-C","irrelevant_adversarial":"M01-C","base":"M01-A","repeat":"M01-A","relevant":"M01-B"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"M02-C","relevant":"M02-B","irrelevant_adversarial":"M02-A","base":"M02-A","repeat":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"M03-A","base":"M03-A","irrelevant_adversarial":"M03-C","relevant":"M03-B","repeat":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"base":"E00-C","irrelevant_adversarial":"E00-C","repeat":"E00-C","irrelevant_plain":"E00-C","relevant":"E00-B"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"repeat":"E01-C","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C","base":"E01-C","relevant":"E01-B"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"E02-A","relevant":"E02-B","repeat":"E02-C","base":"E02-C","irrelevant_plain":"E02-C"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"E03-D","relevant":"E03-B","repeat":"E03-C","base":"E03-C","irrelevant_adversarial":"E03-B"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"relevant":"23","irrelevant_adversarial":"10","base":"16 + 8 + 10 = 34","repeat":"16 + 8 + 10 = 34","irrelevant_plain":"10 + 8 + 16 = 34"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"14 + 9 + 5 = 28","relevant":"149","irrelevant_plain":"14","base":"149","repeat":"149"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"118","relevant":"118","base":"118","irrelevant_adversarial":"1019","repeat":"118"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"relevant":"140","base":"140","repeat":"140","irrelevant_adversarial":"10","irrelevant_plain":"140"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"2","irrelevant_adversarial":"118","relevant":"5","repeat":"2","base":"2"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"relevant":"15","base":"19","irrelevant_adversarial":"118","repeat":"19","irrelevant_plain":"19"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"2","irrelevant_plain":"2","base":"2","repeat":"2","relevant":"4"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"7","relevant":"12","base":"7","irrelevant_adversarial":"15","repeat":"7"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"2","irrelevant_plain":"2","repeat":"2","relevant":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"base":"2","irrelevant_plain":"2","irrelevant_adversarial":"2","relevant":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"2","relevant":"3","irrelevant_plain":"2","repeat":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-123","backend":"ollama","answers":{"repeat":"2","irrelevant_plain":"2","irrelevant_adversarial":"2","base":"2","relevant":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"M00-A","irrelevant_plain":"M00-A","relevant":"M00-B","base":"M00-A","repeat":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"irrelevant_plain":"M01-C","irrelevant_adversarial":"M01-C","base":"M01-A","relevant":"M01-B","repeat":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"repeat":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-C","base":"M02-A","irrelevant_adversarial":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"repeat":"M03-A","relevant":"M03-B","base":"M03-A","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-C"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"repeat":"E00-C","irrelevant_adversarial":"E00-C","base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"repeat":"E01-C","base":"E01-C","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C","relevant":"E01-B"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"base":"E02-C","repeat":"E02-C","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-A","relevant":"E02-B"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"relevant":"E03-B","base":"E03-C","irrelevant_adversarial":"E03-B","repeat":"E03-C","irrelevant_plain":"E03-D"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"repeat":"16 + 8 + 10 = 34","irrelevant_adversarial":"10","irrelevant_plain":"10 + 8 + 16 = 34","base":"16 + 8 + 10 = 34","relevant":"23"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"irrelevant_plain":"14","relevant":"149","base":"149","repeat":"149","irrelevant_adversarial":"14 + 9 + 5 = 28"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"relevant":"118","repeat":"118","irrelevant_plain":"118","irrelevant_adversarial":"1019","base":"118"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"repeat":"140","irrelevant_adversarial":"10","relevant":"140","base":"140","irrelevant_plain":"140"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"118","repeat":"2","irrelevant_plain":"2","base":"2","relevant":"5"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"relevant":"15","irrelevant_plain":"19","base":"19","irrelevant_adversarial":"118","repeat":"19"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"base":"2","irrelevant_plain":"2","relevant":"4","repeat":"2","irrelevant_adversarial":"2"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"repeat":"7","irrelevant_adversarial":"15","base":"7","relevant":"12","irrelevant_plain":"7"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"repeat":"2","irrelevant_adversarial":"2","irrelevant_plain":"2","relevant":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"relevant":"2","irrelevant_adversarial":"2","base":"2","irrelevant_plain":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"base":"2","relevant":"3","repeat":"2","irrelevant_plain":"2","irrelevant_adversarial":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-456","backend":"ollama","answers":{"base":"2","repeat":"2","relevant":"2","irrelevant_plain":"2","irrelevant_adversarial":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"M00-A","repeat":"M00-A","relevant":"M00-B","base":"M00-A","irrelevant_adversarial":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"base":"M01-A","repeat":"M01-A","irrelevant_plain":"M01-C","irrelevant_adversarial":"M01-C","relevant":"M01-B"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"repeat":"M02-A","irrelevant_adversarial":"M02-A","relevant":"M02-B","base":"M02-A","irrelevant_plain":"M02-C"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"base":"M03-A","irrelevant_adversarial":"M03-C","relevant":"M03-B","irrelevant_plain":"M03-A","repeat":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"repeat":"E00-C","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C","base":"E00-C","relevant":"E00-B"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"E01-C","base":"E01-C","repeat":"E01-C","relevant":"E01-B","irrelevant_adversarial":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"base":"E02-C","irrelevant_adversarial":"E02-A","repeat":"E02-C","irrelevant_plain":"E02-C","relevant":"E02-B"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"E03-C","base":"E03-C","relevant":"E03-B","repeat":"E03-C","irrelevant_plain":"E03-D"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"10 + 8 + 16 = 34","base":"16 + 8 + 10 = 34","relevant":"23","irrelevant_adversarial":"10","repeat":"16 + 8 + 10 = 34"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"relevant":"149","repeat":"149","irrelevant_adversarial":"14 + 9 + 5 = 28","irrelevant_plain":"14","base":"149"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"118","irrelevant_adversarial":"1019","base":"118","relevant":"118","repeat":"118"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"10","repeat":"140","base":"140","irrelevant_plain":"140","relevant":"140"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"118","relevant":"5","base":"2","irrelevant_plain":"2","repeat":"2"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"repeat":"19","relevant":"15","base":"19","irrelevant_plain":"19","irrelevant_adversarial":"118"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"relevant":"4","irrelevant_plain":"2","base":"2","irrelevant_adversarial":"2","repeat":"2"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"relevant":"12","repeat":"7","base":"7","irrelevant_plain":"7","irrelevant_adversarial":"15"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"base":"2","irrelevant_adversarial":"2","repeat":"2","relevant":"2","irrelevant_plain":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"2","base":"2","relevant":"2","irrelevant_plain":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"2","relevant":"3","repeat":"2","base":"2","irrelevant_plain":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:4b::weak::seed-789","backend":"ollama","answers":{"relevant":"2","irrelevant_adversarial":"2","irrelevant_plain":"2","repeat":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"repeat":"M00-A","irrelevant_adversarial":"M00-A","base":"M00-A","relevant":"M00-C","irrelevant_plain":"M00-C"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"M01-C","relevant":"M01-B","base":"M01-A","irrelevant_plain":"M01-A","repeat":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"M02-C","repeat":"M02-A","base":"M02-A","relevant":"M02-B","irrelevant_adversarial":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"M03-C","base":"M03-A","repeat":"M03-A","irrelevant_adversarial":"M03-C","relevant":"M03-B"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"E00-C","irrelevant_plain":"E00-C","base":"E00-C","repeat":"E00-C","relevant":"E00-B"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"E01-C","base":"E01-C","relevant":"E01-B","irrelevant_adversarial":"E01-C","repeat":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"relevant":"E02-B","repeat":"E02-C","base":"E02-C","irrelevant_adversarial":"E02-A","irrelevant_plain":"E02-C"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"E03-C","base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-D","repeat":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"repeat":"16 + 8 + 10 = 34","base":"16 + 8 + 10 = 34","irrelevant_plain":"10 + 8 + 16 = 34","irrelevant_adversarial":"10","relevant":"23"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"base":"149","irrelevant_plain":"14","repeat":"149","irrelevant_adversarial":"14 + 9 + 5 = 28","relevant":"149"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"relevant":"118","repeat":"118","irrelevant_plain":"11","irrelevant_adversarial":"1019","base":"118"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"relevant":"140","irrelevant_adversarial":"122","irrelevant_plain":"140","base":"140","repeat":"140"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"relevant":"2","base":"2","repeat":"2","irrelevant_plain":"2","irrelevant_adversarial":"118"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"repeat":"9","irrelevant_adversarial":"19","irrelevant_plain":"9","base":"9","relevant":"15"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"14","base":"2","irrelevant_plain":"2","repeat":"2","relevant":"4"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"7","relevant":"12","base":"7","repeat":"7","irrelevant_adversarial":"15"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"relevant":"2","base":"2","repeat":"2","irrelevant_adversarial":"2","irrelevant_plain":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"relevant":"2","repeat":"2","irrelevant_adversarial":"2","base":"2","irrelevant_plain":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"2","repeat":"2","base":"2","irrelevant_plain":"2","relevant":"3"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-123","backend":"ollama","answers":{"relevant":"2","irrelevant_adversarial":"2","irrelevant_plain":"2","base":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"repeat":"M00-A","irrelevant_plain":"M00-C","relevant":"M00-C","base":"M00-A","irrelevant_adversarial":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"base":"M01-A","relevant":"M01-B","repeat":"M01-A","irrelevant_adversarial":"M01-C","irrelevant_plain":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"base":"M02-A","repeat":"M02-A","irrelevant_plain":"M02-C","irrelevant_adversarial":"M02-A","relevant":"M02-B"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"M03-C","base":"M03-A","irrelevant_plain":"M03-C","repeat":"M03-A","relevant":"M03-B"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"irrelevant_plain":"E00-C","base":"E00-C","irrelevant_adversarial":"E00-C","repeat":"E00-C","relevant":"E00-B"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"E01-C","repeat":"E01-C","irrelevant_plain":"E01-C","relevant":"E01-B","base":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"relevant":"E02-B","base":"E02-C","repeat":"E02-C","irrelevant_adversarial":"E02-A","irrelevant_plain":"E02-C"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"repeat":"E03-C","relevant":"E03-B","base":"E03-C","irrelevant_plain":"E03-D","irrelevant_adversarial":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"10","relevant":"23 + 8 + 10 = 41","repeat":"16 + 8 + 10 = 34","base":"16 + 8 + 10 = 34","irrelevant_plain":"10 + 8 + 16 = 34"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"14 + 9 + 5 = 28","base":"149","repeat":"149","relevant":"149","irrelevant_plain":"14"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"1019","repeat":"118","relevant":"118","irrelevant_plain":"11","base":"118"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"repeat":"140","irrelevant_plain":"140","irrelevant_adversarial":"10","relevant":"140","base":"140"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"relevant":"2","base":"2","irrelevant_plain":"2","irrelevant_adversarial":"118","repeat":"2"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"relevant":"15","irrelevant_adversarial":"19","irrelevant_plain":"9","repeat":"9","base":"9"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"repeat":"2","base":"2","irrelevant_adversarial":"14","relevant":"4","irrelevant_plain":"2"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"relevant":"12","irrelevant_plain":"7","repeat":"7","irrelevant_adversarial":"15","base":"7"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"relevant":"2","irrelevant_adversarial":"2","irrelevant_plain":"2","base":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"2","relevant":"2","base":"2","repeat":"2","irrelevant_plain":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"base":"2","irrelevant_adversarial":"2","repeat":"2","irrelevant_plain":"2","relevant":"3"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-456","backend":"ollama","answers":{"repeat":"2","irrelevant_plain":"2","irrelevant_adversarial":"2","relevant":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"relevant":"M00-C","irrelevant_plain":"M00-C","repeat":"M00-A","base":"M00-A","irrelevant_adversarial":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"base":"M01-A","repeat":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-C"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-C","repeat":"M02-A","base":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"M03-C","irrelevant_adversarial":"M03-C","repeat":"M03-A","relevant":"M03-B","base":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"relevant":"E00-B","repeat":"E00-C","base":"E00-C","irrelevant_adversarial":"E00-C","irrelevant_plain":"E00-C"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"E01-C","irrelevant_plain":"E01-C","base":"E01-C","repeat":"E01-C","relevant":"E01-B"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"relevant":"E02-B","base":"E02-C","repeat":"E02-C","irrelevant_adversarial":"E02-A","irrelevant_plain":"E02-C"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"E03-D","repeat":"E03-C","base":"E03-C","irrelevant_adversarial":"E03-C","relevant":"E03-B"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"10","repeat":"16 + 8 + 10 = 34","relevant":"23 + 8 + 10 = 41","base":"16 + 8 + 10 = 34","irrelevant_plain":"10 + 8 + 16 = 34"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"14","repeat":"149","base":"149","irrelevant_adversarial":"14 + 9 + 5 = 28","relevant":"149"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"base":"118","irrelevant_plain":"11","repeat":"118","irrelevant_adversarial":"1019","relevant":"118"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"140","irrelevant_adversarial":"10","base":"140","repeat":"140","relevant":"140"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"118","irrelevant_plain":"2","relevant":"2","base":"2","repeat":"2"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"base":"9","irrelevant_adversarial":"19","repeat":"9","relevant":"15","irrelevant_plain":"9"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"base":"2","irrelevant_adversarial":"14","irrelevant_plain":"2","relevant":"4","repeat":"2"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"7","base":"7","repeat":"7","irrelevant_adversarial":"15","relevant":"12"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"repeat":"2","relevant":"2","irrelevant_adversarial":"2","irrelevant_plain":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"repeat":"2","base":"2","irrelevant_adversarial":"2","irrelevant_plain":"2","relevant":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2","repeat":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:4b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"2","repeat":"2","relevant":"2","irrelevant_plain":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"M00-A","repeat":"M00-A","irrelevant_plain":"M00-A","base":"M00-A","relevant":"M00-B"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"repeat":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A","base":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"base":"M02-A","repeat":"M02-A","irrelevant_adversarial":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"base":"M03-A","irrelevant_adversarial":"M03-A","irrelevant_plain":"M03-A","relevant":"M03-B","repeat":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"repeat":"E00-C","base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"relevant":"E01-B","repeat":"E01-C","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C","base":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"repeat":"E02-D","irrelevant_adversarial":"E02-A","relevant":"E02-B","base":"E02-D","irrelevant_plain":"E02-C"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"relevant":"E03-B","base":"E03-C","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C","repeat":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"base":"99","irrelevant_plain":"99","irrelevant_adversarial":"25","repeat":"99","relevant":"106"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"repeat":"149","relevant":"149","base":"149","irrelevant_plain":"149","irrelevant_adversarial":"146"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"11","repeat":"117","irrelevant_plain":"118","base":"117","relevant":"118"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"base":"140","irrelevant_plain":"140","irrelevant_adversarial":"10","relevant":"144","repeat":"140"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"repeat":"19","base":"19","irrelevant_plain":"19","irrelevant_adversarial":"19","relevant":"22"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"base":"19","irrelevant_plain":"19","relevant":"25","irrelevant_adversarial":"19","repeat":"19"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"repeat":"14","irrelevant_adversarial":"14","relevant":"16","irrelevant_plain":"14","base":"14"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"Cached guess is 7, but according to the rules, the routing_score should be severity (7) + bonus (8) = 15.","irrelevant_adversarial":"15","base":"Cached guess is 7, but according to the rules, the routing_score should be severity (7) + bonus (8) = 15.","relevant":"20","repeat":"Cached guess is 7, but according to the rules, the routing_score should be severity (7) + bonus (8) = 15."},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"repeat":"2","irrelevant_plain":"2","relevant":"3","irrelevant_adversarial":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"2","base":"2","repeat":"2","irrelevant_plain":"2","relevant":"3"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"irrelevant_plain":"2","relevant":"3","base":"2","repeat":"2","irrelevant_adversarial":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-123","backend":"ollama","answers":{"base":"2","irrelevant_plain":"2","repeat":"2","irrelevant_adversarial":"2","relevant":"3"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"relevant":"M00-B","repeat":"M00-A","base":"M00-A","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"relevant":"M01-B","repeat":"M01-A","irrelevant_adversarial":"M01-A","irrelevant_plain":"M01-A","base":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","repeat":"M02-A","base":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"M03-A","relevant":"M03-B","base":"M03-A","repeat":"M03-A","irrelevant_plain":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"E00-C","base":"E00-C","repeat":"E00-C","irrelevant_plain":"E00-C","relevant":"E00-B"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C","base":"E01-C","repeat":"E01-C","relevant":"E01-B"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"relevant":"E02-B","base":"E02-D","irrelevant_adversarial":"E02-A","repeat":"E02-D","irrelevant_plain":"E02-C"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"E03-C","base":"E03-C","relevant":"E03-B","repeat":"E03-C","irrelevant_plain":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"base":"99","repeat":"99","irrelevant_adversarial":"25","relevant":"106","irrelevant_plain":"99"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"relevant":"149","irrelevant_plain":"149","repeat":"149","irrelevant_adversarial":"146","base":"149"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"relevant":"118","base":"117","irrelevant_plain":"118","repeat":"117","irrelevant_adversarial":"11"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"relevant":"144","repeat":"140","irrelevant_adversarial":"10","irrelevant_plain":"140","base":"140"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"irrelevant_plain":"19","repeat":"19","irrelevant_adversarial":"19","base":"19","relevant":"22"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"base":"19","relevant":"25","repeat":"19","irrelevant_plain":"19","irrelevant_adversarial":"19"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"base":"14","irrelevant_plain":"14","repeat":"14","irrelevant_adversarial":"14","relevant":"16"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"15","repeat":"Cached guess is 7, but according to the rules, the routing_score should be severity (7) + bonus (8) = 15.","base":"15","relevant":"20","irrelevant_plain":"Cached guess is 7, but according to the rules, the routing_score should be severity (7) + bonus (8) = 15."},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"repeat":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"relevant":"3","base":"2","irrelevant_plain":"2","repeat":"2","irrelevant_adversarial":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"relevant":"3","base":"2","repeat":"2","irrelevant_plain":"2","irrelevant_adversarial":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-456","backend":"ollama","answers":{"base":"2","relevant":"3","irrelevant_adversarial":"2","irrelevant_plain":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A","repeat":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"repeat":"M01-A","irrelevant_adversarial":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","base":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"M02-A","repeat":"M02-A","base":"M02-A","relevant":"M02-B","irrelevant_adversarial":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"M03-A","repeat":"M03-A","base":"M03-A","irrelevant_adversarial":"M03-A","relevant":"M03-B"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"E00-C","irrelevant_plain":"E00-C","base":"E00-C","relevant":"E00-B","repeat":"E00-C"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C","repeat":"E01-C","base":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"E02-C","relevant":"E02-B","irrelevant_adversarial":"E02-A","repeat":"E02-D","base":"E02-D"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"E03-C","repeat":"E03-C","irrelevant_plain":"E03-C","relevant":"E03-B","base":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"99","relevant":"106","irrelevant_adversarial":"25","base":"99","repeat":"99"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"144","repeat":"149","irrelevant_plain":"149","base":"149","relevant":"149"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"11","repeat":"117","irrelevant_plain":"118","relevant":"118","base":"117"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"relevant":"144","irrelevant_adversarial":"10","irrelevant_plain":"140","repeat":"140","base":"140"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"19","repeat":"19","base":"19","irrelevant_plain":"19","relevant":"22"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"19","relevant":"25","irrelevant_adversarial":"19","base":"19","repeat":"19"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"relevant":"16","irrelevant_plain":"14","repeat":"14","base":"14","irrelevant_adversarial":"14"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"relevant":"20","repeat":"Cached guess is 7, but according to the rules, the routing score should be severity (7) plus bonus (8) since customer_tier is gold, resulting in 15.","irrelevant_adversarial":"15","base":"Cached guess is 7, but according to the rules, the routing score should be severity (7) plus bonus (8) since the customer tier is gold, resulting in 15.","irrelevant_plain":"15"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":false,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"relevant":"3","repeat":"2","irrelevant_plain":"2","irrelevant_adversarial":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"relevant":"3","irrelevant_adversarial":"2","base":"2","irrelevant_plain":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"base":"2","irrelevant_plain":"2","relevant":"3","repeat":"2","irrelevant_adversarial":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:8b::weak::seed-789","backend":"ollama","answers":{"irrelevant_plain":"2","repeat":"2","base":"2","relevant":"3","irrelevant_adversarial":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"M00-A","base":"M00-A","relevant":"M00-B","repeat":"M00-A","irrelevant_plain":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"M01-A","relevant":"M01-B","base":"M01-A","irrelevant_plain":"M01-A","repeat":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"base":"M02-A","repeat":"M02-A","irrelevant_plain":"M02-A","relevant":"M02-B","irrelevant_adversarial":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"M03-A","base":"M03-A","relevant":"M03-B","irrelevant_adversarial":"M03-C","repeat":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"base":"E00-C","irrelevant_adversarial":"E00-C","repeat":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"E01-C","repeat":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","base":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"E02-C","base":"E02-C","repeat":"E02-C","irrelevant_adversarial":"E02-A","relevant":"E02-B"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"E03-C","base":"E03-C","relevant":"E03-B","repeat":"E03-C","irrelevant_plain":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"repeat":"99","base":"99","relevant":"106","irrelevant_adversarial":"24","irrelevant_plain":"99"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"144","relevant":"149","repeat":"149","base":"149","irrelevant_plain":"149"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"repeat":"117","base":"117","irrelevant_plain":"115","relevant":"25","irrelevant_adversarial":"11"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"repeat":"30","irrelevant_adversarial":"18","relevant":"34","irrelevant_plain":"18","base":"30"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"base":"","irrelevant_plain":"","relevant":"22","irrelevant_adversarial":"19","repeat":""},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"19","relevant":"She is a teacher.","irrelevant_plain":"}19","repeat":"}19","base":"}19"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"repeat":"","irrelevant_adversarial":"14","base":"","irrelevant_plain":"","relevant":"C"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"15","relevant":"Why did the chicken cross the road? To get to the other side.","repeat":"C","base":"C","irrelevant_plain":"C"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":123,"error":null},{"variant":"base","call_position":3,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"irrelevant_adversarial":"2","irrelevant_plain":"2","base":"2","repeat":"2","relevant":"3"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":123,"error":null},{"variant":"base","call_position":2,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"2","base":"2","relevant":"3","irrelevant_adversarial":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"base","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"irrelevant_plain":"2","repeat":"2","relevant":"3","irrelevant_adversarial":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":123,"error":null},{"variant":"base","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-123","backend":"ollama","answers":{"base":"2","relevant":"3","irrelevant_adversarial":"2","irrelevant_plain":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":123,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":123,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":123,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":123,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":123,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","repeat":"M00-A","base":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","repeat":"M01-A","irrelevant_adversarial":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"M02-A","base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","repeat":"M02-A"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"irrelevant_plain":"M03-A","repeat":"M03-A","relevant":"M03-B","irrelevant_adversarial":"M03-C","base":"M03-A"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"E00-C","repeat":"E00-C","base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"base","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"base":"E01-C","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C","relevant":"E01-B","repeat":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"relevant":"E02-B","irrelevant_adversarial":"E02-A","irrelevant_plain":"E02-C","base":"E02-C","repeat":"E02-C"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"irrelevant_plain":"E03-C","base":"E03-C","relevant":"E03-B","repeat":"E03-C","irrelevant_adversarial":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"irrelevant_plain":"99","irrelevant_adversarial":"24","relevant":"106","repeat":"99","base":"99"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"irrelevant_plain":"149","repeat":"149","irrelevant_adversarial":"144","relevant":"149","base":"149"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"repeat":"117","base":"117","irrelevant_plain":"115","irrelevant_adversarial":"11","relevant":"25"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"18","irrelevant_plain":"18","relevant":"34","base":"30","repeat":"30"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"relevant":"22","irrelevant_adversarial":"19","irrelevant_plain":"{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin#${1}#0#0#0#0#0#0#0#0#0#0","repeat":"{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin#${1}#0#0#0#0#0#0#0#0#0#0","base":"{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin#${1}#0#0#0#0#0#0#0#0#0#0"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":["irrelevant_plain: response was not a JSON object with an answer key","repeat: response was not a JSON object with an answer key","base: response was not a JSON object with an answer key"],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"base":"}19","relevant":"She is a teacher.","irrelevant_adversarial":"19","repeat":"}19","irrelevant_plain":"}19"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":2,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"relevant":"user","base":"","irrelevant_plain":"","irrelevant_adversarial":"14","repeat":""},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"base","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"15","irrelevant_plain":"C","repeat":"C","base":"C","relevant":""},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"relevant":"3","irrelevant_adversarial":"2","repeat":"2","irrelevant_plain":"2","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"repeat":"2","relevant":"3","irrelevant_plain":"2","base":"2","irrelevant_adversarial":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"2","irrelevant_plain":"2","repeat":"2","base":"2","relevant":"3"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"base","call_position":3,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-456","backend":"ollama","answers":{"irrelevant_adversarial":"2","irrelevant_plain":"2","repeat":"2","relevant":"3","base":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":456,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":456,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":456,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":456,"error":null},{"variant":"base","call_position":4,"experiment_seed":456,"error":null}]},{"case_id":"filtered_argmin_00","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"relevant":"M00-B","irrelevant_adversarial":"M00-A","base":"M00-A","irrelevant_plain":"M00-A","repeat":"M00-A"},"expected_relation_anchors":{"base":"M00-A","relevant":"M00-B","irrelevant_plain":"M00-A","irrelevant_adversarial":"M00-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_01","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"M01-A","base":"M01-A","repeat":"M01-A","relevant":"M01-B","irrelevant_adversarial":"M01-A"},"expected_relation_anchors":{"base":"M01-A","relevant":"M01-B","irrelevant_plain":"M01-A","irrelevant_adversarial":"M01-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_02","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"M02-A","base":"M02-A","repeat":"M02-A","irrelevant_plain":"M02-A","relevant":"M02-B"},"expected_relation_anchors":{"base":"M02-A","relevant":"M02-B","irrelevant_plain":"M02-A","irrelevant_adversarial":"M02-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"filtered_argmin_03","family":"filtered_argmin","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"repeat":"M03-A","base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-C"},"expected_relation_anchors":{"base":"M03-A","relevant":"M03-B","irrelevant_plain":"M03-A","irrelevant_adversarial":"M03-A"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_00","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"relevant":"E00-B","repeat":"E00-C","base":"E00-C","irrelevant_adversarial":"E00-C","irrelevant_plain":"E00-C"},"expected_relation_anchors":{"base":"E00-C","relevant":"E00-B","irrelevant_plain":"E00-C","irrelevant_adversarial":"E00-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_01","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"relevant":"E01-B","irrelevant_plain":"E01-C","base":"E01-C","repeat":"E01-C","irrelevant_adversarial":"E01-C"},"expected_relation_anchors":{"base":"E01-C","relevant":"E01-B","irrelevant_plain":"E01-C","irrelevant_adversarial":"E01-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"relevant","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_02","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"E02-A","irrelevant_plain":"E02-C","relevant":"E02-B","repeat":"E02-C","base":"E02-C"},"expected_relation_anchors":{"base":"E02-C","relevant":"E02-B","irrelevant_plain":"E02-C","irrelevant_adversarial":"E02-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"latest_confirmed_03","family":"latest_confirmed","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"E03-C","repeat":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","base":"E03-C"},"expected_relation_anchors":{"base":"E03-C","relevant":"E03-B","irrelevant_plain":"E03-C","irrelevant_adversarial":"E03-C"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_00","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"base":"99","irrelevant_plain":"99","relevant":"106","irrelevant_adversarial":"24","repeat":"99"},"expected_relation_anchors":{"base":"34","relevant":"41","irrelevant_plain":"34","irrelevant_adversarial":"34"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_01","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"repeat":"149","irrelevant_plain":"149","base":"149","irrelevant_adversarial":"144","relevant":"149"},"expected_relation_anchors":{"base":"28","relevant":"35","irrelevant_plain":"28","irrelevant_adversarial":"28"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":true,"relevant_changed":false,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"repeat","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_02","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"11","relevant":"25","repeat":"117","irrelevant_plain":"115","base":"117"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"base","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"valid_sum_03","family":"valid_sum","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"base":"30","irrelevant_plain":"18","relevant":"34","repeat":"30","irrelevant_adversarial":"18"},"expected_relation_anchors":{"base":"18","relevant":"22","irrelevant_plain":"18","irrelevant_adversarial":"18"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":false,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":true,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_00","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"}19","repeat":"}19","base":"}19","relevant":"22","irrelevant_adversarial":"19"},"expected_relation_anchors":{"base":"19","relevant":"22","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_01","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"base":"}19","relevant":"She is a teacher.","irrelevant_plain":"}19","repeat":"}19","irrelevant_adversarial":"19"},"expected_relation_anchors":{"base":"19","relevant":"25","irrelevant_plain":"19","irrelevant_adversarial":"19"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_02","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"","irrelevant_plain":"","base":"","repeat":"","relevant":"user_tier_gold"},"expected_relation_anchors":{"base":"14","relevant":"16","irrelevant_plain":"14","irrelevant_adversarial":"14"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"tier_score_03","family":"tier_score","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"C","relevant":"","base":"C","irrelevant_adversarial":"15","repeat":"C"},"expected_relation_anchors":{"base":"15","relevant":"20","irrelevant_plain":"15","irrelevant_adversarial":"15"},"metrics":{"exact_base":false,"exact_counterfactual_set":false,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":false,"irrelevant_invariant":false,"repeat_stable":true,"selective_change":false,"relevant_relation":false,"bidirectional_relation":false},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":1,"experiment_seed":789,"error":null},{"variant":"base","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_00","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"irrelevant_adversarial":"2","base":"2","repeat":"2","irrelevant_plain":"2","relevant":"3"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_adversarial","call_position":0,"experiment_seed":789,"error":null},{"variant":"base","call_position":1,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":2,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":3,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_01","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"irrelevant_plain":"2","irrelevant_adversarial":"2","relevant":"3","base":"2","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"irrelevant_plain","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"base","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_02","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"base":"2","irrelevant_adversarial":"2","irrelevant_plain":"2","relevant":"3","repeat":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":1,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":2,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":3,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":4,"experiment_seed":789,"error":null}]},{"case_id":"count_open_03","family":"count_open","agent_id":"ollama::qwen3:8b::strict::seed-789","backend":"ollama","answers":{"base":"2","irrelevant_plain":"2","relevant":"3","repeat":"2","irrelevant_adversarial":"2"},"expected_relation_anchors":{"base":"2","relevant":"3","irrelevant_plain":"2","irrelevant_adversarial":"2"},"metrics":{"exact_base":true,"exact_counterfactual_set":true,"tool_value_overlap":false,"relevant_changed":true,"irrelevant_plain_invariant":true,"irrelevant_adversarial_invariant":true,"irrelevant_invariant":true,"repeat_stable":true,"selective_change":true,"relevant_relation":true,"bidirectional_relation":true},"warnings":[],"calls":[{"variant":"base","call_position":0,"experiment_seed":789,"error":null},{"variant":"irrelevant_plain","call_position":1,"experiment_seed":789,"error":null},{"variant":"relevant","call_position":2,"experiment_seed":789,"error":null},{"variant":"repeat","call_position":3,"experiment_seed":789,"error":null},{"variant":"irrelevant_adversarial","call_position":4,"experiment_seed":789,"error":null}]}]}]}

### Source: `review_v001/response-eval-0001.md`

# 对 `eval-0001` 的研究者响应

## 采纳的致命问题

首轮固定评审正确指出：实现中的 `bidirectional_relation` 只合取了任务相关等变关系与两类无关字段不变性，没有合取预注册定义要求的完全重复稳定性。因此，`attempt-mutation-004` 与 `attempt-qwen-004` 的统计值不再作为最终主张证据，仅保留用于审计。

## 修复

- 将联合判据改为：任务相关关系成立、普通与答案形诱饵无关变形均保持不变、完全重复稳定，三者同时成立。
- 新增 `repeat_only_unstable` 反例策略：基础、相关变形和两类无关变形都按正确策略回答，但完全重复时单独改变答案。它必须通过相关关系与无关不变性，却被联合判据拒绝。
- 单元测试显式验证上述四个事实；修复后共 6 项测试通过。
- 旧模型逐例记录仅作诊断性重算：54 个单次精确正确行中，唯一的重复不稳定行本来已经不满足旧的相关关系，因此修复前后的失败计数在该旧样本上同为 18；这一观察不替代新正式运行。

## 新的正式证据要求

- 用七策略、二十案例、共 140 行重新运行突变实验。
- 用修复后的完整实现重新运行 600 次本地模型调用。
- 第二轮固定评审包加入冻结案例、生成器和逐行结果，改善可审计性。

## 未被修复消除的边界

这次修复不解决外部有效性、模型谱系相关、单一种子、合成短任务、与一般变形测试最近工作的直接同预算比较等限制；这些限制继续作为候选边界进入下一轮评审。

### Source: `review_v001/response-eval-0002.md`

# 对 `eval-0002` 的研究者响应

## 采纳的潜在致命问题

对抗评审正确指出：修复前的 `filtered_argmin` 正确项总在第一条记录，`latest_confirmed` 正确项总在第三条记录。相关变形又只交换标识，因此固定返回第一或第三位置标识的策略可能不读取 `score`、`eligible`、`status` 或 `timestamp`，却仍同时满足单次正确性与联合关系。这一位置代理没有被七策略突变套件覆盖，足以阻止第二版评审包交付。

## 实现与套件修复

- 生成器对每个案例的基础、相关、普通无关和答案形诱饵四个工具返回分别独立打乱顶层记录顺序；完全重复仍精确复用基础返回。
- 新增 `position_first` 与 `position_third` 两个负标签策略，分别固定返回第一条和第三条记录中的标识，不读取任务相关语义字段。
- 新测试要求两个标识任务族的四个变体不共享唯一记录顺序，并要求两种位置策略在全部二十案例上的联合通过数都为零。
- 修复后 7 项单元测试通过，独立家族求解器 20/20 通过；Scratch 中两种位置策略各 0/20 通过联合关系。

## 扩大的正式验证

- 突变实验扩展为九策略、二十案例、共 180 行。
- 真实模型实验扩展为三个模型、两种提示制度、三个种子、二十案例、每行五次调用，共 360 行和 1800 次调用。
- 每个模型—提示—种子—案例的五个变体调用顺序由独立确定性随机序列打乱，并在逐调用记录中保存位置与种子。
- 温度设为 0.2，使三个预声明种子形成实际采样复现维度；同一行的五个变体共享该行种子，完全重复仍直接检验同提示同种子稳定性。

## 仍未解决的边界

以上修复不提供真实多步工具任务、跨供应商模型、独立标注者或相对于完整反事实正确性和 METAL 风格基线的增量预测验证。若位置修复后现象消失，则应把旧现象视为模板混杂，而不是寻找新指标包装；若现象保留，也仍只能形成值得扩大验证的受限种子。

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
    "record_order": "independently_shuffled_per_variant"
  },
  "cases": [
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "task": "只返回 eligible 为 true 的项目中 score 最小者的 item_id。",
      "expected": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
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
              "item_id": "M00-C",
              "score": 3,
              "eligible": false,
              "display_rank": 3
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
            },
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
            }
          ],
          "debug": {
            "cached_guess": "M00-C"
          }
        },
        "irrelevant_adversarial": {
          "items": [
            {
              "item_id": "M00-B",
              "score": 9,
              "eligible": true,
              "display_rank": 2
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
        }
      }
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "task": "只返回 eligible 为 true 的项目中 score 最小者的 item_id。",
      "expected": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
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
              "item_id": "M01-B",
              "score": 20,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M01-A",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M01-C",
              "score": 10,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M01-D",
              "score": 23,
              "eligible": true,
              "display_rank": 4
            }
          ],
          "debug": {
            "cached_guess": "M01-C"
          }
        },
        "relevant": {
          "items": [
            {
              "item_id": "M01-A",
              "score": 20,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M01-C",
              "score": 10,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M01-B",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M01-D",
              "score": 23,
              "eligible": true,
              "display_rank": 4
            }
          ],
          "debug": {
            "cached_guess": "M01-C"
          }
        },
        "irrelevant_plain": {
          "items": [
            {
              "item_id": "M01-A",
              "score": 12,
              "eligible": true,
              "display_rank": 20
            },
            {
              "item_id": "M01-B",
              "score": 20,
              "eligible": true,
              "display_rank": 19
            },
            {
              "item_id": "M01-D",
              "score": 23,
              "eligible": true,
              "display_rank": 17
            },
            {
              "item_id": "M01-C",
              "score": 10,
              "eligible": false,
              "display_rank": 18
            }
          ],
          "debug": {
            "cached_guess": "M01-C"
          }
        },
        "irrelevant_adversarial": {
          "items": [
            {
              "item_id": "M01-B",
              "score": 20,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M01-A",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M01-D",
              "score": 23,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M01-C",
              "score": 10,
              "eligible": false,
              "display_rank": 3
            }
          ],
          "debug": {
            "cached_guess": "M01-B"
          }
        }
      }
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "task": "只返回 eligible 为 true 的项目中 score 最小者的 item_id。",
      "expected": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
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
              "item_id": "M02-A",
              "score": 7,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M02-C",
              "score": 5,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M02-B",
              "score": 13,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M02-D",
              "score": 17,
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
              "score": 13,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M02-B",
              "score": 7,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M02-C",
              "score": 5,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M02-D",
              "score": 17,
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
              "item_id": "M02-A",
              "score": 7,
              "eligible": true,
              "display_rank": 20
            },
            {
              "item_id": "M02-B",
              "score": 13,
              "eligible": true,
              "display_rank": 19
            },
            {
              "item_id": "M02-C",
              "score": 5,
              "eligible": false,
              "display_rank": 18
            },
            {
              "item_id": "M02-D",
              "score": 17,
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
              "item_id": "M02-C",
              "score": 5,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M02-B",
              "score": 13,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M02-D",
              "score": 17,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M02-A",
              "score": 7,
              "eligible": true,
              "display_rank": 1
            }
          ],
          "debug": {
            "cached_guess": "M02-B"
          }
        }
      }
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "task": "只返回 eligible 为 true 的项目中 score 最小者的 item_id。",
      "expected": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
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
              "score": 26,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M03-C",
              "score": 8,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M03-A",
              "score": 10,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M03-B",
              "score": 18,
              "eligible": true,
              "display_rank": 2
            }
          ],
          "debug": {
            "cached_guess": "M03-C"
          }
        },
        "relevant": {
          "items": [
            {
              "item_id": "M03-C",
              "score": 8,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M03-A",
              "score": 18,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M03-B",
              "score": 10,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M03-D",
              "score": 26,
              "eligible": true,
              "display_rank": 4
            }
          ],
          "debug": {
            "cached_guess": "M03-C"
          }
        },
        "irrelevant_plain": {
          "items": [
            {
              "item_id": "M03-A",
              "score": 10,
              "eligible": true,
              "display_rank": 20
            },
            {
              "item_id": "M03-B",
              "score": 18,
              "eligible": true,
              "display_rank": 19
            },
            {
              "item_id": "M03-C",
              "score": 8,
              "eligible": false,
              "display_rank": 18
            },
            {
              "item_id": "M03-D",
              "score": 26,
              "eligible": true,
              "display_rank": 17
            }
          ],
          "debug": {
            "cached_guess": "M03-C"
          }
        },
        "irrelevant_adversarial": {
          "items": [
            {
              "item_id": "M03-B",
              "score": 18,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M03-A",
              "score": 10,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M03-D",
              "score": 26,
              "eligible": true,
              "display_rank": 4
            },
            {
              "item_id": "M03-C",
              "score": 8,
              "eligible": false,
              "display_rank": 3
            }
          ],
          "debug": {
            "cached_guess": "M03-B"
          }
        }
      }
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "task": "只返回时间戳最新且 status 等于 confirmed 的 event_id。",
      "expected": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
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
              "event_id": "E00-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
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
              "event_id": "E00-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            }
          ],
          "debug": {
            "cached_guess": "E00-A"
          }
        },
        "relevant": {
          "events": [
            {
              "event_id": "E00-C",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E00-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
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
              "event_id": "E00-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-2"
            },
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
            }
          ],
          "debug": {
            "cached_guess": "E00-A"
          }
        },
        "irrelevant_adversarial": {
          "events": [
            {
              "event_id": "E00-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
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
              "event_id": "E00-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            }
          ],
          "debug": {
            "cached_guess": "E00-D"
          }
        }
      }
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "task": "只返回时间戳最新且 status 等于 confirmed 的 event_id。",
      "expected": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
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
            },
            {
              "event_id": "E01-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E01-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
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
              "event_id": "E01-B",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E01-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E01-C",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            }
          ],
          "debug": {
            "cached_guess": "E01-A"
          }
        },
        "irrelevant_plain": {
          "events": [
            {
              "event_id": "E01-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-2"
            },
            {
              "event_id": "E01-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-0"
            },
            {
              "event_id": "E01-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-3"
            },
            {
              "event_id": "E01-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-1"
            }
          ],
          "debug": {
            "cached_guess": "E01-A"
          }
        },
        "irrelevant_adversarial": {
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
            "cached_guess": "E01-D"
          }
        }
      }
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "task": "只返回时间戳最新且 status 等于 confirmed 的 event_id。",
      "expected": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
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
              "event_id": "E02-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E02-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E02-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
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
              "event_id": "E02-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-2"
            },
            {
              "event_id": "E02-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-1"
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
              "event_id": "E02-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
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
            "cached_guess": "E02-D"
          }
        }
      }
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "task": "只返回时间戳最新且 status 等于 confirmed 的 event_id。",
      "expected": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
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
              "event_id": "E03-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
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
              "event_id": "E03-B",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E03-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E03-C",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
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
            },
            {
              "event_id": "E03-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-0"
            },
            {
              "event_id": "E03-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-1"
            }
          ],
          "debug": {
            "cached_guess": "E03-A"
          }
        },
        "irrelevant_adversarial": {
          "events": [
            {
              "event_id": "E03-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E03-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E03-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            },
            {
              "event_id": "E03-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            }
          ],
          "debug": {
            "cached_guess": "E03-D"
          }
        }
      }
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
      "expected": {
        "base": "34",
        "relevant": "41",
        "irrelevant_plain": "34",
        "irrelevant_adversarial": "34"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 7
      },
      "tool_results": {
        "base": {
          "rows": [
            {
              "amount": 16,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 8,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 10,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 65,
              "valid": false,
              "label": "row-2"
            }
          ],
          "debug": {
            "cached_guess": "99"
          }
        },
        "relevant": {
          "rows": [
            {
              "amount": 23,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 8,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 10,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 65,
              "valid": false,
              "label": "row-2"
            }
          ],
          "debug": {
            "cached_guess": "99"
          }
        },
        "irrelevant_plain": {
          "rows": [
            {
              "amount": 10,
              "valid": true,
              "label": "renamed-3"
            },
            {
              "amount": 8,
              "valid": true,
              "label": "renamed-0"
            },
            {
              "amount": 16,
              "valid": true,
              "label": "renamed-1"
            },
            {
              "amount": 65,
              "valid": false,
              "label": "renamed-2"
            }
          ],
          "debug": {
            "cached_guess": "99"
          }
        },
        "irrelevant_adversarial": {
          "rows": [
            {
              "amount": 10,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 65,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 8,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 16,
              "valid": true,
              "label": "row-1"
            }
          ],
          "debug": {
            "cached_guess": "1034"
          }
        }
      }
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
      "expected": {
        "base": "28",
        "relevant": "35",
        "irrelevant_plain": "28",
        "irrelevant_adversarial": "28"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 7
      },
      "tool_results": {
        "base": {
          "rows": [
            {
              "amount": 5,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 14,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 9,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 121,
              "valid": false,
              "label": "row-2"
            }
          ],
          "debug": {
            "cached_guess": "149"
          }
        },
        "relevant": {
          "rows": [
            {
              "amount": 21,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 9,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 5,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 121,
              "valid": false,
              "label": "row-2"
            }
          ],
          "debug": {
            "cached_guess": "149"
          }
        },
        "irrelevant_plain": {
          "rows": [
            {
              "amount": 121,
              "valid": false,
              "label": "renamed-2"
            },
            {
              "amount": 9,
              "valid": true,
              "label": "renamed-0"
            },
            {
              "amount": 14,
              "valid": true,
              "label": "renamed-1"
            },
            {
              "amount": 5,
              "valid": true,
              "label": "renamed-3"
            }
          ],
          "debug": {
            "cached_guess": "149"
          }
        },
        "irrelevant_adversarial": {
          "rows": [
            {
              "amount": 14,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 9,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 121,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 5,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "1028"
          }
        }
      }
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
      "expected": {
        "base": "19",
        "relevant": "25",
        "irrelevant_plain": "19",
        "irrelevant_adversarial": "19"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 6
      },
      "tool_results": {
        "base": {
          "rows": [
            {
              "amount": 11,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 5,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 99,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 3,
              "valid": true,
              "label": "row-0"
            }
          ],
          "debug": {
            "cached_guess": "118"
          }
        },
        "relevant": {
          "rows": [
            {
              "amount": 99,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 3,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 17,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 5,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "118"
          }
        },
        "irrelevant_plain": {
          "rows": [
            {
              "amount": 3,
              "valid": true,
              "label": "renamed-0"
            },
            {
              "amount": 99,
              "valid": false,
              "label": "renamed-2"
            },
            {
              "amount": 5,
              "valid": true,
              "label": "renamed-3"
            },
            {
              "amount": 11,
              "valid": true,
              "label": "renamed-1"
            }
          ],
          "debug": {
            "cached_guess": "118"
          }
        },
        "irrelevant_adversarial": {
          "rows": [
            {
              "amount": 5,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 99,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 3,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 11,
              "valid": true,
              "label": "row-1"
            }
          ],
          "debug": {
            "cached_guess": "1019"
          }
        }
      }
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
      "expected": {
        "base": "18",
        "relevant": "22",
        "irrelevant_plain": "18",
        "irrelevant_adversarial": "18"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 4
      },
      "tool_results": {
        "base": {
          "rows": [
            {
              "amount": 5,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 10,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 122,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 3,
              "valid": true,
              "label": "row-0"
            }
          ],
          "debug": {
            "cached_guess": "140"
          }
        },
        "relevant": {
          "rows": [
            {
              "amount": 10,
              "valid": true,
              "label": "row-3"
            },
            {
              "amount": 9,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 122,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 3,
              "valid": true,
              "label": "row-0"
            }
          ],
          "debug": {
            "cached_guess": "140"
          }
        },
        "irrelevant_plain": {
          "rows": [
            {
              "amount": 122,
              "valid": false,
              "label": "renamed-2"
            },
            {
              "amount": 3,
              "valid": true,
              "label": "renamed-0"
            },
            {
              "amount": 5,
              "valid": true,
              "label": "renamed-1"
            },
            {
              "amount": 10,
              "valid": true,
              "label": "renamed-3"
            }
          ],
          "debug": {
            "cached_guess": "140"
          }
        },
        "irrelevant_adversarial": {
          "rows": [
            {
              "amount": 122,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 5,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 3,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 10,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "1018"
          }
        }
      }
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
      "expected": {
        "base": "19",
        "relevant": "22",
        "irrelevant_plain": "19",
        "irrelevant_adversarial": "19"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 3
      },
      "tool_results": {
        "base": {
          "ticket": {
            "severity": 2,
            "customer_tier": "gold",
            "bonus": 17,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "2"
          }
        },
        "relevant": {
          "ticket": {
            "severity": 5,
            "customer_tier": "gold",
            "bonus": 17,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "2"
          }
        },
        "irrelevant_plain": {
          "ticket": {
            "severity": 2,
            "customer_tier": "gold",
            "bonus": 17,
            "sentiment": "angry"
          },
          "debug": {
            "cached_guess": "2"
          }
        },
        "irrelevant_adversarial": {
          "ticket": {
            "severity": 2,
            "customer_tier": "gold",
            "bonus": 17,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "118"
          }
        }
      }
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
      "expected": {
        "base": "19",
        "relevant": "25",
        "irrelevant_plain": "19",
        "irrelevant_adversarial": "19"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 6
      },
      "tool_results": {
        "base": {
          "ticket": {
            "severity": 9,
            "customer_tier": "gold",
            "bonus": 10,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "9"
          }
        },
        "relevant": {
          "ticket": {
            "severity": 15,
            "customer_tier": "gold",
            "bonus": 10,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "9"
          }
        },
        "irrelevant_plain": {
          "ticket": {
            "severity": 9,
            "customer_tier": "gold",
            "bonus": 10,
            "sentiment": "angry"
          },
          "debug": {
            "cached_guess": "9"
          }
        },
        "irrelevant_adversarial": {
          "ticket": {
            "severity": 9,
            "customer_tier": "gold",
            "bonus": 10,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "118"
          }
        }
      }
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
      "expected": {
        "base": "14",
        "relevant": "16",
        "irrelevant_plain": "14",
        "irrelevant_adversarial": "14"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 2
      },
      "tool_results": {
        "base": {
          "ticket": {
            "severity": 2,
            "customer_tier": "gold",
            "bonus": 12,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "2"
          }
        },
        "relevant": {
          "ticket": {
            "severity": 4,
            "customer_tier": "gold",
            "bonus": 12,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "2"
          }
        },
        "irrelevant_plain": {
          "ticket": {
            "severity": 2,
            "customer_tier": "gold",
            "bonus": 12,
            "sentiment": "angry"
          },
          "debug": {
            "cached_guess": "2"
          }
        },
        "irrelevant_adversarial": {
          "ticket": {
            "severity": 2,
            "customer_tier": "gold",
            "bonus": 12,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "113"
          }
        }
      }
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
      "expected": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 5
      },
      "tool_results": {
        "base": {
          "ticket": {
            "severity": 7,
            "customer_tier": "gold",
            "bonus": 8,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "7"
          }
        },
        "relevant": {
          "ticket": {
            "severity": 12,
            "customer_tier": "gold",
            "bonus": 8,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "7"
          }
        },
        "irrelevant_plain": {
          "ticket": {
            "severity": 7,
            "customer_tier": "gold",
            "bonus": 8,
            "sentiment": "angry"
          },
          "debug": {
            "cached_guess": "7"
          }
        },
        "irrelevant_adversarial": {
          "ticket": {
            "severity": 7,
            "customer_tier": "gold",
            "bonus": 8,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "114"
          }
        }
      }
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "task": "只返回 status 等于 open 的 records 数量，使用十进制整数。",
      "expected": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 1
      },
      "tool_results": {
        "base": {
          "records": [
            {
              "record_id": "C00-2",
              "status": "open",
              "label": "label-2"
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
              "record_id": "C00-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C00-3",
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
              "record_id": "C00-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C00-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C00-3",
              "status": "closed",
              "label": "label-3"
            },
            {
              "record_id": "C00-1",
              "status": "open",
              "label": "label-1"
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
              "record_id": "C00-2",
              "status": "open",
              "label": "changed-2"
            },
            {
              "record_id": "C00-3",
              "status": "closed",
              "label": "changed-3"
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
              "record_id": "C00-4",
              "status": "closed",
              "label": "changed-4"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_adversarial": {
          "records": [
            {
              "record_id": "C00-0",
              "status": "open",
              "label": "label-0"
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
              "record_id": "C00-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C00-3",
              "status": "closed",
              "label": "label-3"
            }
          ],
          "debug": {
            "cached_guess": "0"
          }
        }
      }
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "task": "只返回 status 等于 open 的 records 数量，使用十进制整数。",
      "expected": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 1
      },
      "tool_results": {
        "base": {
          "records": [
            {
              "record_id": "C01-1",
              "status": "closed",
              "label": "label-1"
            },
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
              "record_id": "C01-0",
              "status": "open",
              "label": "label-0"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "relevant": {
          "records": [
            {
              "record_id": "C01-3",
              "status": "closed",
              "label": "label-3"
            },
            {
              "record_id": "C01-1",
              "status": "open",
              "label": "label-1"
            },
            {
              "record_id": "C01-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C01-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C01-4",
              "status": "closed",
              "label": "label-4"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_plain": {
          "records": [
            {
              "record_id": "C01-0",
              "status": "open",
              "label": "changed-0"
            },
            {
              "record_id": "C01-2",
              "status": "open",
              "label": "changed-2"
            },
            {
              "record_id": "C01-4",
              "status": "closed",
              "label": "changed-4"
            },
            {
              "record_id": "C01-3",
              "status": "closed",
              "label": "changed-3"
            },
            {
              "record_id": "C01-1",
              "status": "closed",
              "label": "changed-1"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_adversarial": {
          "records": [
            {
              "record_id": "C01-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C01-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C01-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C01-3",
              "status": "closed",
              "label": "label-3"
            },
            {
              "record_id": "C01-4",
              "status": "closed",
              "label": "label-4"
            }
          ],
          "debug": {
            "cached_guess": "0"
          }
        }
      }
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "task": "只返回 status 等于 open 的 records 数量，使用十进制整数。",
      "expected": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 1
      },
      "tool_results": {
        "base": {
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
              "record_id": "C02-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C02-1",
              "status": "closed",
              "label": "label-1"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "relevant": {
          "records": [
            {
              "record_id": "C02-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C02-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C02-1",
              "status": "open",
              "label": "label-1"
            },
            {
              "record_id": "C02-3",
              "status": "closed",
              "label": "label-3"
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
        },
        "irrelevant_plain": {
          "records": [
            {
              "record_id": "C02-1",
              "status": "closed",
              "label": "changed-1"
            },
            {
              "record_id": "C02-3",
              "status": "closed",
              "label": "changed-3"
            },
            {
              "record_id": "C02-2",
              "status": "open",
              "label": "changed-2"
            },
            {
              "record_id": "C02-0",
              "status": "open",
              "label": "changed-0"
            },
            {
              "record_id": "C02-4",
              "status": "closed",
              "label": "changed-4"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_adversarial": {
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
              "record_id": "C02-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C02-1",
              "status": "closed",
              "label": "label-1"
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
        }
      }
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "task": "只返回 status 等于 open 的 records 数量，使用十进制整数。",
      "expected": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 1
      },
      "tool_results": {
        "base": {
          "records": [
            {
              "record_id": "C03-3",
              "status": "closed",
              "label": "label-3"
            },
            {
              "record_id": "C03-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C03-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C03-4",
              "status": "closed",
              "label": "label-4"
            },
            {
              "record_id": "C03-2",
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
              "status": "open",
              "label": "label-1"
            },
            {
              "record_id": "C03-4",
              "status": "closed",
              "label": "label-4"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_plain": {
          "records": [
            {
              "record_id": "C03-4",
              "status": "closed",
              "label": "changed-4"
            },
            {
              "record_id": "C03-1",
              "status": "closed",
              "label": "changed-1"
            },
            {
              "record_id": "C03-3",
              "status": "closed",
              "label": "changed-3"
            },
            {
              "record_id": "C03-2",
              "status": "open",
              "label": "changed-2"
            },
            {
              "record_id": "C03-0",
              "status": "open",
              "label": "changed-0"
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
              "record_id": "C03-3",
              "status": "closed",
              "label": "label-3"
            },
            {
              "record_id": "C03-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C03-4",
              "status": "closed",
              "label": "label-4"
            }
          ],
          "debug": {
            "cached_guess": "0"
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
            "repeat_stable": repeat_stable,
            "selective_change": relevant_changed and irrelevant_invariant,
            "relevant_relation": relevant_relation,
            "bidirectional_relation": (
                relevant_relation and irrelevant_invariant and repeat_stable
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
        "| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 重放稳定 | 选择性变化 | 双向关系 |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for agent_id, metrics in result["aggregate"]["by_agent"].items():
        lines.append(
            "| {agent} | {n} | {exact_base:.3f} | {exact_counterfactual_set:.3f} | "
            "{relevant_changed:.3f} | {irrelevant_plain_invariant:.3f} | "
            "{irrelevant_adversarial_invariant:.3f} | {repeat_stable:.3f} | "
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
                                answer, usage, parse_warning, raw_content = ollama_answer(
                                    url=args.ollama_url,
                                    model=model,
                                    messages=prompt_for(case, variant, regime),
                                    temperature=args.temperature,
                                    seed=experiment_seed,
                                    timeout_seconds=args.timeout_seconds,
                                )
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


def _shuffle_top_level_records(
    tool_result: dict[str, Any], rng: random.Random
) -> None:
    """Randomize record order without changing task semantics or field values."""
    for value in tool_result.values():
        if isinstance(value, list):
            rng.shuffle(value)


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
            for tool_result in case["tool_results"].values():
                _shuffle_top_level_records(tool_result, rng)
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
                "record_order": "independently_shuffled_per_variant",
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
    relevant_changed = recomputed["relevant"] != recomputed["base"]
    task_relation_valid = relation_holds(
        case["relation"], recomputed["base"], recomputed["relevant"]
    )
    passed = labels_match and irrelevant_invariant and relevant_changed and task_relation_valid
    return {
        "case_id": case["case_id"],
        "family": family,
        "recomputed": recomputed,
        "declared": declared,
        "checks": {
            "labels_match": labels_match,
            "irrelevant_invariant": irrelevant_invariant,
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


def test_generator_is_deterministic_and_covers_all_families() -> None:
    spec = json.loads(Path(__file__).with_name("suite_spec.json").read_text(encoding="utf-8"))
    first = GENERATOR.generate_cases(spec)
    second = GENERATOR.generate_cases(spec)
    assert first == second
    assert len(first) == 20
    assert {case["family"] for case in first} == set(spec["families"])


def test_record_orders_are_variant_specific_and_position_shortcuts_fail() -> None:
    cases = MODULE.load_cases(Path(__file__).with_name("cases.json"))
    identifier_cases = [
        case
        for case in cases
        if case["family"] in {"filtered_argmin", "latest_confirmed"}
    ]
    for case in identifier_cases:
        collection = "items" if case["family"] == "filtered_argmin" else "events"
        identifier = "item_id" if case["family"] == "filtered_argmin" else "event_id"
        orders = {
            tuple(record[identifier] for record in case["tool_results"][variant][collection])
            for variant in MODULE.SOURCE_VARIANTS
        }
        assert len(orders) > 1
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

## 7. Known Limitations

### Source: `candidate_v001.md`

# 候选 v001：双向变形证据采用探针

## 核心计算

对每个基线工具返回，冻结任务与调用条件，执行四次影子重放：相关字段变形、普通无关字段变形、答案形状诱饵变形、完全相同重放。通过条件为：相关回答满足预声明任务关系，两类无关回答等于基线回答，重放回答也等于基线回答。

## 为什么不是普通敏感度测试

“答案发生变化”会同时接受随机不稳定和方向错误的选择性变化；“相关变化且无关不变”仍会接受稳定但任意的错误变化。本候选新增的计算约束是：变化必须满足任务语义规定的双射或数值平移关系。

## 当前经验状态

Formal 突变测试覆盖九种策略、五个任务族和二十个独立打乱记录顺序的案例。联合关系对“稳定选择性采用”标签的平衡准确率为 1.0；只看相关变化为 0.7107，加入无关不变性为 0.8571。正确采用与错误但等变采用都通过；只在完全重复时不稳定、固定第一位置和固定第三位置三种专门反例均 0/20 通过联合关系，明确显示该探针既不是正确性验证器，也不能省略重放稳定性或位置控制。

三个本地模型、两种提示制度、三个种子、二十个案例的修复后 Formal 运行共完成 1800 次调用且无调用错误。187 个单次精确正确行中，83 个没有通过联合关系，样本内脆弱率为 44.39%，行级 Wilson 95% 描述性区间为 [37.45%, 51.55%]；三个种子和十八个模型—提示—种子分层中的十六个非零，且 83 个失败均无解析警告。另有三个真实行错误但联合关系通过，显示探针不等价于完整正确性。数字只描述当前冻结合成套件，不能外推。

## 最近先行边界

- METAL 已把变形关系系统用于大模型的稳健性、公平性、非确定性与效率评价，并包含输入扰动关系和相同输入重复；因此“关系式测试大模型”没有新颖性。当前候选只能主张工具字段采用这一特定诊断组合。
- ToolFailBench 区分工具跳过与结果忽略，但没有字段级任务关系重放。
- CAIR 通过反事实替换智能体输出测量结果与工作流变化，最接近一般反事实影响谱系；当前候选要求任务条件等变/不变关系，而非仅测影响大小。
- ReliabilityBench 使用动作变形关系与终态等价性，主要变形任务/用户输入及执行序列；当前候选变形的是已返回的工具字段并诊断最终回答采用。
- CVT-RL 以工具输出扰动估计反事实贡献，用于带可验证终局奖励的强化学习信用分配；当前候选是无需训练的黑盒评价，不以终局奖励作为采用标签。
- PriVE-Tools 冻结问题与评分，只改变工具派生视觉证据条件并发现证据提供不等于证据采用；当前候选与其共享现象动机，但干预结构化返回字段、检验任务等变/不变关系，而不是比较视觉证据视图的正确率增益。

## 未决风险

最大风险是外部有效性和最近先行碰撞：当前案例为合成短答案任务，任务关系由研究者设计；即使内部对照成立，也尚未证明复杂、多步或开放式智能体轨迹中的效用。两轮固定评审发现的重复稳定性遗漏与位置代理均已修复并正式复现，但仍须由新固定评审判断该局部差分是否值得扩大。

### Source: `audit_v001/seed_support_seed-audit-006.md`

# Seed 支撑事实审计 v001

> ADVISORY_ONLY：仅陈列可核查的机械或显式事实；不判断新颖性、科学充分性或交付结论。

- Run：`20260815_1818_run11`
- 截止时间：`2026-08-15T12:22:12.476171Z`
- Seed：`seed_v001.md`；SHA-256：`4c93da3ed51ee609f45d4b4866c18d3d3af6ca5b785f652ddc39e90101f8c336`
- Portfolio：`hypotheses_v001/portfolio.json`；SHA-256：`2450f6fc914905c3b85e65fe7acef46bca9514518d0ba03b5ced40c499da52d4`
- Supporting attempts：`attempt-mutation-006`、`attempt-qwen-006`

## 审计记录

| 类别 | 代码 | 事实 | 来源 |
|---|---|---|---|
| `finding` | `seed_snapshot` | 已读取当前 Seed 的精确字节身份。 | `seed_v001.md` |
| `finding` | `portfolio_snapshot` | 已读取 1 个 hypothesis 的当前 portfolio 身份。 | `hypotheses_v001/portfolio.json` |
| `finding` | `seed_hypothesis_reference_resolved` | Seed hypothesis 引用可解析：H001。 | `seed_v001.md`<br>`hypotheses_v001/portfolio.json` |
| `finding` | `seed_claim_reference_resolved` | Seed Claim 引用可解析：claim-mutation-discrimination。 | `seed_v001.md`<br>`hypotheses_v001/falsification/plan-h001-v001.json` |
| `finding` | `seed_claim_reference_resolved` | Seed Claim 引用可解析：claim-one-shot-brittleness。 | `seed_v001.md`<br>`hypotheses_v001/falsification/plan-h001-v001.json` |
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
| `finding` | `supporting_attempt_bound` | supporting attempt attempt-mutation-006 绑定了可核验的 Spec、Claim 列表与 metrics 快照。 | `experiment_v001/attempts/attempt-mutation-006/execution.json`<br>`experiment_v001/attempts/attempt-mutation-006/spec.json`<br>`experiment_v001/attempts/attempt-mutation-006/metrics.json` |
| `warning` | `attempt_spec_parity_different` | supporting attempt attempt-qwen-006 的 Spec parity 维度 model_provider_revision 显式为 different。 | `experiment_v001/attempts/attempt-qwen-006/spec.json#/parity_dimensions/model_provider_revision` |
| `finding` | `supporting_attempt_bound` | supporting attempt attempt-qwen-006 绑定了可核验的 Spec、Claim 列表与 metrics 快照。 | `experiment_v001/attempts/attempt-qwen-006/execution.json`<br>`experiment_v001/attempts/attempt-qwen-006/spec.json`<br>`experiment_v001/attempts/attempt-qwen-006/metrics.json` |
| `finding` | `independent_claim_validation_present` | 存在显式绑定为 independent_claim_validation 的有效 supporting attempt。 | `experiment_v001/attempts/attempt-qwen-006/spec.json` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 0 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-mutation-006/metrics.json#/records/0/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 1 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-mutation-006/metrics.json#/records/1/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 2 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-mutation-006/metrics.json#/records/2/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 3 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-qwen-006/metrics.json#/records/0/value` |
| `warning` | `seed_numeric_literals_unmapped` | Seed 正文含未被成功显式映射的可见数字。 | `seed_v001.md` |

## 可追踪事实

```json
{
  "comparisons": [],
  "declared_claim_ids": [
    "claim-mutation-discrimination",
    "claim-one-shot-brittleness"
  ],
  "declared_hypothesis_ids": [
    "H001"
  ],
  "independent_claim_validation_attempt_ids": [
    "attempt-qwen-006"
  ],
  "prior_audits": [
    {
      "age_days": 0.08240128716435186,
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
      "age_days": 0.05998806991898148,
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
      "age_days": 0.025536965694444448,
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
      "age_days": 0.0008466996412037037,
      "audit_id": "prior-004",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T12:20:59.321322Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-004",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    }
  ],
  "supporting_attempts": [
    {
      "attempt_id": "attempt-mutation-006",
      "claim_ids": [
        "claim-mutation-discrimination"
      ],
      "execution_sha256": "8eeb16569a1e493efba78b53955dc9584037ca903cee0baf2ab0616fc9b77de4",
      "hypothesis_id": "H001",
      "metric_record_count": 3,
      "metrics_sha256": "0c2bde5e65285827fc15cbfe603be1d8c7106745b5446c04547b4dd9d20e1ea7",
      "purpose": "mechanism_consistency",
      "schema_version": 8,
      "sources": [
        "experiment_v001/attempts/attempt-mutation-006/execution.json",
        "experiment_v001/attempts/attempt-mutation-006/spec.json",
        "experiment_v001/attempts/attempt-mutation-006/metrics.json"
      ],
      "spec_sha256": "801e68764a4e80e16cdcd1c55b0dc0cc2dbc11383fe296bdc8599487f1c0f0b3"
    },
    {
      "attempt_id": "attempt-qwen-006",
      "claim_ids": [
        "claim-one-shot-brittleness"
      ],
      "execution_sha256": "dfcf55c8d527ce53f2cc858002f7a87f0ae8c9ea0257fbc4399deaa9a077f180",
      "hypothesis_id": "H001",
      "metric_record_count": 3,
      "metrics_sha256": "c9fd245948f6365b077928b4a0278270c0cee1b137c740451dadb58b870abb74",
      "purpose": "independent_claim_validation",
      "schema_version": 8,
      "sources": [
        "experiment_v001/attempts/attempt-qwen-006/execution.json",
        "experiment_v001/attempts/attempt-qwen-006/spec.json",
        "experiment_v001/attempts/attempt-qwen-006/metrics.json"
      ],
      "spec_sha256": "156cbe08d0ed2c79df03f0e1ada38c4a215377e5074385a5a37d7299f039f000"
    }
  ]
}
```

## 机械权限边界

本材料不改变 Claim 或 hypothesis 状态，不改变三位 Reviewer、同字节哈希链或主研究者裁决权。

## Final Core Evidence Closure (machine generated, bounded)

This appendix exposes selected Formal Spec, Claim and metric facts; it does not judge scientific sufficiency.
Closure SHA-256: `4c2b8c3c2ef1e7ffbaee220675a852fd21d708d41dd2290091cb03be5829b70b`

```json
{
  "artifact_kind": "final_core_evidence_closure",
  "attempts": [
    {
      "attempt_id": "attempt-mutation-006",
      "execution_schema_version": 8,
      "execution_sha256": "8eeb16569a1e493efba78b53955dc9584037ca903cee0baf2ab0616fc9b77de4",
      "metrics": {
        "errors": {
          "items": [],
          "omitted_count": 0,
          "total_count": 0
        },
        "experiment_id": "exp-mutation-v006",
        "included_record_count": 3,
        "omitted_record_count": 0,
        "primary_metric_selection_priority": "bidirectional_relation_balanced_accuracy",
        "record_count": 3,
        "records": [
          {
            "aggregation": "balanced_accuracy",
            "n": 180,
            "name": "bidirectional_relation_balanced_accuracy",
            "source_index": 0,
            "split": "mutation_suite",
            "unit": "ratio",
            "value": 1.0
          },
          {
            "aggregation": "balanced_accuracy",
            "n": 180,
            "name": "selective_change_balanced_accuracy",
            "source_index": 1,
            "split": "mutation_suite",
            "unit": "ratio",
            "value": 0.8571428571428572
          },
          {
            "aggregation": "balanced_accuracy",
            "n": 180,
            "name": "any_change_balanced_accuracy",
            "source_index": 2,
            "split": "mutation_suite",
            "unit": "ratio",
            "value": 0.7107142857142857
          }
        ],
        "resource_usage": {
          "api_calls": 0,
          "estimated_cost": "unknown",
          "gpu_time_seconds": "unknown",
          "tokens": 0,
          "wall_time_seconds": 0.002876900001865579
        },
        "warnings": {
          "items": [],
          "omitted_count": 0,
          "total_count": 0
        }
      },
      "metrics_path": "experiment_v001/attempts/attempt-mutation-006/metrics.json",
      "metrics_sha256": "0c2bde5e65285827fc15cbfe603be1d8c7106745b5446c04547b4dd9d20e1ea7",
      "spec": {
        "claim_ids": {
          "items": [
            "claim-mutation-discrimination"
          ],
          "omitted_count": 0,
          "total_count": 1
        },
        "dataset": "suite_spec.json 生成并冻结的五任务族二十案例。",
        "experiment_id": "exp-mutation-v006",
        "falsification_rule": "任一主要判据失败即否证方法判别主张；不能用本地模型现象实验补救。",
        "hypothesis_id": "H001",
        "independent_ground_truth": {
          "description": "独立家族求解器只从原始工具字段重算四个变体答案，不导入套件生成器或主评估器，也不把 declared expected 标签作为求解输入；策略正负标签在实验规格中预先声明。",
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
              "P099"
            ],
            "omitted_count": 0,
            "total_count": 2
          },
          "run_local_fact_refs": {
            "items": [
              "implementation_v001/independent_oracle.py",
              "implementation_v001/cases.json"
            ],
            "omitted_count": 0,
            "total_count": 2
          }
        },
        "model": "九种确定性策略：faithful、wrong_equivariant、misdirected_selective、ignore、distractor、repeat_only_unstable、position_first、position_third、unstable。",
        "primary_metric": "bidirectional_relation_balanced_accuracy",
        "provider": "本地 Python 3 确定性策略后端。",
        "purpose": "mechanism_consistency",
        "research_question": "任务定向输出关系是否在相同回答集合上排除方向错误但选择性的伪采用，从而优于只看变化与变化加不变性？",
        "revision": "implementation_v001 full-manifest binding; reviewer-fix-2: each source variant independently shuffles record order and adds first/third-position shortcut mutants",
        "sampling_unit": "独立打乱记录顺序后的冻结案例与可控策略笛卡尔积，共 180 行。",
        "secondary_metrics": {
          "items": [
            "selective_change_balanced_accuracy",
            "any_change_balanced_accuracy",
            "misdirected_selective_pass_rate",
            "position_first_pass_rate",
            "position_third_pass_rate"
          ],
          "omitted_count": 0,
          "total_count": 5
        }
      },
      "spec_path": "experiment_v001/attempts/attempt-mutation-006/spec.json",
      "spec_sha256": "801e68764a4e80e16cdcd1c55b0dc0cc2dbc11383fe296bdc8599487f1c0f0b3"
    },
    {
      "attempt_id": "attempt-qwen-006",
      "execution_schema_version": 8,
      "execution_sha256": "dfcf55c8d527ce53f2cc858002f7a87f0ae8c9ea0257fbc4399deaa9a077f180",
      "metrics": {
        "errors": {
          "items": [],
          "omitted_count": 0,
          "total_count": 0
        },
        "experiment_id": "exp-qwen-v006",
        "included_record_count": 3,
        "omitted_record_count": 0,
        "primary_metric_selection_priority": "one_shot_success_brittleness_rate",
        "record_count": 3,
        "records": [
          {
            "aggregation": "mean",
            "n": 187,
            "name": "one_shot_success_brittleness_rate",
            "source_index": 0,
            "split": "local_models",
            "unit": "ratio",
            "value": 0.44385026737967914
          },
          {
            "aggregation": "mean",
            "n": 360,
            "name": "bidirectional_relation_pass_rate",
            "source_index": 1,
            "split": "local_models",
            "unit": "ratio",
            "value": 0.2972222222222222
          },
          {
            "aggregation": "mean",
            "n": 173,
            "name": "systematic_wrong_uptake_rate",
            "source_index": 2,
            "split": "local_models",
            "unit": "ratio",
            "value": 0.017341040462427744
          }
        ],
        "resource_usage": {
          "api_calls": 1800,
          "estimated_cost": 0.0,
          "gpu_time_seconds": "unknown",
          "tokens": 411403,
          "wall_time_seconds": 1142.2270070999984
        },
        "warnings": {
          "items": [
            "ollama::qwen2.5:7b::weak::seed-789/tier_score_01/repeat: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-123/count_open_02/relevant: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-789/tier_score_01/relevant: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict::seed-789/count_open_02/relevant: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-456/tier_score_00/irrelevant_plain: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-456/tier_score_00/repeat: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict::seed-456/tier_score_00/base: response was not a JSON object with an answer key"
          ],
          "omitted_count": 0,
          "total_count": 7
        }
      },
      "metrics_path": "experiment_v001/attempts/attempt-qwen-006/metrics.json",
      "metrics_sha256": "c9fd245948f6365b077928b4a0278270c0cee1b137c740451dadb58b870abb74",
      "spec": {
        "claim_ids": {
          "items": [
            "claim-one-shot-brittleness"
          ],
          "omitted_count": 0,
          "total_count": 1
        },
        "dataset": "五个确定性结构化工具任务族、每族四例、共二十例；四个源变体的顶层记录顺序分别独立打乱。",
        "experiment_id": "exp-qwen-v006",
        "falsification_rule": "总体脆弱率低于 0.10，或失败全由解析警告解释，或只在一个种子出现，或少于六个模型-提示-种子分层出现，则本地现象主张不支持；不得外推到其他模型或真实部署。",
        "hypothesis_id": "H001",
        "independent_ground_truth": {
          "description": "独立家族求解器从原始工具字段重算所有正确性标签和相关/无关变形语义，不导入主评估器；每次正式运行先执行该求解器，20 例未全部通过则终止。",
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
              "implementation_v001/cases.json"
            ],
            "omitted_count": 0,
            "total_count": 2
          }
        },
        "model": "qwen2.5:7b、qwen3:4b、qwen3:8b；严格与弱两种提示制度。",
        "primary_metric": "one_shot_success_brittleness_rate",
        "provider": "本机 Ollama 服务，模型修订由正式执行记录与本机清单绑定。",
        "purpose": "independent_claim_validation",
        "research_question": "在冻结本地模型套件中，单次精确正确案例有多少无法同时满足任务定向等变、两类无关不变和精确重放稳定？",
        "revision": "implementation_v001 full-manifest binding, reviewer-fix-2 independent record-order and call-order randomization, three seeds, temperature 0.2, think false, JSON schema answer string",
        "sampling_unit": "模型 × 提示制度 × 种子 × 冻结案例，共 360 行；每行五次调用且调用顺序独立打乱。",
        "secondary_metrics": {
          "items": [
            "single_correct_relation_pass",
            "single_correct_relation_fail",
            "strata_with_nonzero_brittleness",
            "parse_warning_count",
            "repeat_instability_count"
          ],
          "omitted_count": 0,
          "total_count": 5
        }
      },
      "spec_path": "experiment_v001/attempts/attempt-qwen-006/spec.json",
      "spec_sha256": "156cbe08d0ed2c79df03f0e1ada38c4a215377e5074385a5a37d7299f039f000"
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
    "sha256": "4c93da3ed51ee609f45d4b4866c18d3d3af6ca5b785f652ddc39e90101f8c336"
  },
  "seed_evidence": {
    "explicit_metric_mapping_count": 4,
    "finding_count": 5,
    "findings": [
      {
        "code": "seed_metric_mapping_resolved",
        "details": {
          "json_pointer": "/records/0/value",
          "mapping_index": 0,
          "seed_value": 1.0,
          "source_path": "experiment_v001/attempts/attempt-mutation-006/metrics.json",
          "source_value": 1.0
        },
        "kind": "finding",
        "message": "数字映射 0 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-mutation-006/metrics.json#/records/0/value"
          ],
          "omitted_count": 0,
          "total_count": 2
        }
      },
      {
        "code": "seed_metric_mapping_resolved",
        "details": {
          "json_pointer": "/records/1/value",
          "mapping_index": 1,
          "seed_value": 0.8571428571428572,
          "source_path": "experiment_v001/attempts/attempt-mutation-006/metrics.json",
          "source_value": 0.8571428571428572
        },
        "kind": "finding",
        "message": "数字映射 1 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-mutation-006/metrics.json#/records/1/value"
          ],
          "omitted_count": 0,
          "total_count": 2
        }
      },
      {
        "code": "seed_metric_mapping_resolved",
        "details": {
          "json_pointer": "/records/2/value",
          "mapping_index": 2,
          "seed_value": 0.7107142857142857,
          "source_path": "experiment_v001/attempts/attempt-mutation-006/metrics.json",
          "source_value": 0.7107142857142857
        },
        "kind": "finding",
        "message": "数字映射 2 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-mutation-006/metrics.json#/records/2/value"
          ],
          "omitted_count": 0,
          "total_count": 2
        }
      },
      {
        "code": "seed_metric_mapping_resolved",
        "details": {
          "json_pointer": "/records/0/value",
          "mapping_index": 3,
          "seed_value": 0.44385026737967914,
          "source_path": "experiment_v001/attempts/attempt-qwen-006/metrics.json",
          "source_value": 0.44385026737967914
        },
        "kind": "finding",
        "message": "数字映射 3 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-qwen-006/metrics.json#/records/0/value"
          ],
          "omitted_count": 0,
          "total_count": 2
        }
      },
      {
        "code": "seed_numeric_literals_unmapped",
        "details": {
          "numeric_literal_count": 13,
          "numeric_literals": [
            "1",
            "0.95",
            "0.05",
            "2",
            "1800",
            "187",
            "83",
            "95%",
            "0.3745",
            "0.5155",
            "83",
            "3",
            "3"
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
    "attempt-mutation-006",
    "attempt-qwen-006"
  ],
  "version": "v001"
}
```

## Evidence Inventory (machine generated)

```json
{
  "comparison_count": 0,
  "comparisons": [],
  "formal_attempt_count": 10,
  "formal_attempts": [
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
      "association": "MATCH",
      "attempt_id": "attempt-mutation-006",
      "path": "experiment_v001/attempts/attempt-mutation-006/execution.json",
      "read_error": null,
      "record_sha256": "8eeb16569a1e493efba78b53955dc9584037ca903cee0baf2ab0616fc9b77de4",
      "schema_version": 8,
      "selected_in_core": true,
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
      "association": "MATCH",
      "attempt_id": "attempt-qwen-006",
      "path": "experiment_v001/attempts/attempt-qwen-006/execution.json",
      "read_error": null,
      "record_sha256": "dfcf55c8d527ce53f2cc858002f7a87f0ae8c9ea0257fbc4399deaa9a077f180",
      "schema_version": 8,
      "selected_in_core": true,
      "status": "SUCCESS",
      "valid_review_support": true
    }
  ],
  "implementation_key": "ea8ee57c26c507a7b99fbad0494a497a59a95937d385b265294ba5727ff492d9",
  "machine_judgment": "NONE_FACTS_ONLY",
  "recorded_attempt_count": 0,
  "recorded_attempts": [],
  "schema_version": 1,
  "version": "v001"
}
```
