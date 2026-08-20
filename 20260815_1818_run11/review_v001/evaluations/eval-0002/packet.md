# CRL Fixed Review Packet

- Contract: 3
- Scientific version: v001
- Evaluator: CRL-EVAL-1.0
- Evaluator definition SHA-256: e0d35083b1427e9f8861ba576304b97657498fee46480d5e07e8e0b02cea6e5b
- Implementation key: 5135bed01d0bef962cb6f8262375bb063c1561c8ad6e8be3dc346aa521bcc7b1
- Implementation manifest SHA-256: 5135bed01d0bef962cb6f8262375bb063c1561c8ad6e8be3dc346aa521bcc7b1
- Evidence inventory SHA-256: 50caef6e38cf27372acb416d2de737f84a956744d2001c71ed67cb28dce39c6a

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

在五个确定性任务族、二十个冻结案例与七种预声明策略上，联合关系应比“相关答案发生任意变化”和“相关变化加两类无关不变”更准确地区分稳定选择性采用。正标签包括正确采用与错误但等变采用，后者用于阻止把探针偷换成正确性；只在完全重复时改变答案的专门反例用于检验联合定义确实包含重放稳定性。

Formal `attempt-mutation-005` 中，任务定向双向关系平衡准确率为 1.0；选择性变化基线为 0.8；任意相关变化为 0.7。错误但等变策略 20/20 通过，方向错误但选择性变化策略 0/20 通过；只在完全重复时不稳定的策略对相关关系与无关不变性均为 20/20、对联合关系为 0/20。预注册判据“至少 0.95 且比第二基线至少高 0.05”得到局部支持。

### Claim 2：单次成功关系脆弱性

在三个本地模型、两种提示制度、二十个冻结案例上，单次精确正确不足以保证任务定向、抗无关诱饵且可重放的采用结构。

Formal `attempt-qwen-005` 中，53 个单次精确正确行有 18 个联合关系失败，脆弱率为 0.33962264150943394，Wilson 95% 区间为 [0.2269, 0.4741]。18 个失败均无解析警告，六个模型—提示分层中五个出现非零失败。当前 53 个单次正确行没有完全重复不稳定，且 16/18 的联合失败集中在两个标识选择任务族。该比例只描述本地冻结合成套件；不能外推为部署失败率。

## 正确性 × 采用关系四象限

| 单次正确性 | 联合关系 | 解释边界 |
|---|---|---|
| 对 | 通过 | 样本内正确且采用结构稳定 |
| 对 | 失败 | 一次答对但关系脆弱，是本版本观察到的核心现象 |
| 错 | 通过 | 系统性但错误的等变采用；探针不能纠正它 |
| 错 | 失败 | 错误且没有稳定选择性采用证据 |

正式真实模型套件没有观察到“错且通过”，但确定性突变策略已证明它在逻辑上可以发生。因此联合关系永远不能单独称为正确性验证器。

## 贡献向量

- **问题/现象**：把“工具证据已经提供”与“单次答对时仍未稳定采用”分开；正式样本内观察到 18/53 的关系脆弱性。
- **机制/计算**：相关字段使用任务定向等变，而非只看变化；普通无关、答案形状诱饵与精确重放分别隔离三类伪影。
- **智能体特有约束**：干预位置在工具结果进入上下文之后、最终回答之前，面向结构化工具返回而非普通用户输入扰动。
- **评价/基准**：七种突变策略与正确性×关系四象限共同规定信号边界。
- **经验发现**：脆弱性出现在五个模型—提示分层，但高度集中于两个标识选择任务族。
- **理论/分析**：错误但等变策略构成反例，证明关系采用与答案正确性不可同一化。
- **系统能力**：当前实现是可重复的本地评价载体，尚不是在线门控或修复系统。

## 局限与最大剩余疑问

1. METAL 对一般方法形式构成强类比归约；当前组合是否足以形成 CCF-B 级评价方法贡献，仍需固定评审和更大规模研究判断。
2. 二十个案例均为合成短答案任务，关系由研究者手工规定；独立求解器只保证套件自洽，不提供外部有效性。
3. 正式现象集中于 `filtered_argmin` 与 `latest_confirmed`；数值任务的单次正确样本少，可能说明现象依赖标识选择结构。
4. 三个模型来自相近本地模型谱系，只使用一个固定种子；没有跨供应商、跨规模或跨种子不确定性。
5. 每案例五次调用的成本明显高于单次正确率；尚未证明诊断收益在复杂真实轨迹中抵得过预算。
6. 当前最大的剩余疑问不是“信号能否区分已知突变”，而是它能否在真实多步工具轨迹上提供超出通用变形测试与完整正确性标签的可操作信息。
7. 首轮固定评审发现旧实现漏合取完全重复稳定性；旧第四版结果已撤出支持链。第五版修复与专门反例恢复了实现—主张一致性，但也显示真实模型样本里重放项没有经验增量。

## 值得扩大的验证

下一阶段应冻结更广的工具任务本体：检索选择、聚合、状态过滤、多工具连接和开放式证据综合；加入跨供应商模型与至少三个种子；由独立标注者定义字段相关性和变形关系；与 METAL 风格相等/距离关系、CAIR 风格影响分数、终局正确率及 ToolFailBench 分类做同预算比较。最关键的扩大判据是：四象限能否预测后续复核失败、修复收益或真实终态错误，而不仅是在合成套件上重述完整反事实正确性。

<!-- CRL_SEED_SUPPORT_META {"schema_version":1,"hypothesis_ids":["H001"],"claim_ids":["claim-mutation-discrimination","claim-one-shot-brittleness"],"falsified_claim_dispositions":[],"metric_mappings":[{"seed_text":"任务定向双向关系平衡准确率为 1.0","seed_value":1.0,"source_path":"experiment_v001/attempts/attempt-mutation-005/metrics.json","json_pointer":"/records/0/value"},{"seed_text":"选择性变化基线为 0.8","seed_value":0.8,"source_path":"experiment_v001/attempts/attempt-mutation-005/metrics.json","json_pointer":"/records/1/value"},{"seed_text":"任意相关变化为 0.7","seed_value":0.7,"source_path":"experiment_v001/attempts/attempt-mutation-005/metrics.json","json_pointer":"/records/2/value"},{"seed_text":"脆弱率为 0.33962264150943394","seed_value":0.33962264150943394,"source_path":"experiment_v001/attempts/attempt-qwen-005/metrics.json","json_pointer":"/records/0/value"}]} -->

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

### Source: `hypotheses_v001/priors/prior-003/assessment.md`

# 最近先行科研解释

> 本文件属于主研究者解释，可在阅读候选、PDF、Evidence 和实验后继续修订；它不进入机器事实快照哈希。

- 审计标识：`prior-003`
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
- **关系语义**：相关字段要求满足任务规定的标识双射或数值平移，而非只要求输出不同；七策略突变测试排除了稳定但方向错误的选择性变化。
- **对照组合**：普通无关字段、答案形状诱饵字段、精确重放分别隔离装饰敏感、诱饵依赖与随机不稳定；第五版专门加入只在重复时不稳定的反例，修复了首轮评审发现的实现缺口。
- **诊断表达**：关系信号与独立正确性形成四象限；明确允许错误但等变策略通过，避免把采用结构误称为正确性。
- **经验现象**：53 个单次正确行中 18 个联合关系失败，但 16 个集中在两个标识选择任务族；可发表价值若存在，更可能来自这一受限现象及未来的可操作分层，而非变形测试本身。

## 最危险替代解释

本候选可能只是 METAL 的工具场景实例，加上手工选择的关系、诱饵与重放项。当前真实模型中联合关系与四变体完整正确性恰好同为 35/120，且完全重复项在 53 个单次正确行里没有经验增量；若未来不能在更广任务上显示超出通用变形基线和完整标签的可操作价值，方法贡献不足。另一个风险是合成任务把关系写得过于简单，失败只反映提示遵循或短答案解析，而非真实多步工具采用。

## 最小区分实验

1. 用方向错误但“相关变化且无关不变”的可控策略检验任务定向关系是否比一般变化/一致性关系多提供判别力。
2. 用只在完全重复时不稳定的可控策略检验实现是否真实合取重放稳定性，而非只在文字定义中声称。
3. 用独立家族求解器验证所有相关/无关变形的标签与语义，不读取主评估器标签。
4. 在至少三个本地模型、两种提示制度和五个任务族上正式复现“单次正确但关系失败”，并按模型、提示和任务族分层；若只集中于一个分层或解析失败则不成立。

## 方法死亡后仍存现象

即使 METAL 或未来最近先行完全覆盖关系式方法，仍可能保留的现象是：工具型语言模型在一次答对时仍可能无法在任务等价的工具字段变形下保持方向正确与无关不变。第五版 Formal 在冻结本地套件观察到 18/53，但任务族集中性很强，因此只能作为值得扩大验证的受限种子，不能作为一般部署结论。

## 背景与身份未解决项

- 本次自动审计仍因 Semantic Scholar HTTP 429 而降级，候选来自 arXiv；CAIR、CVT-RL 与 ReliabilityBench 的身份和组件来自主研究者另行核对的论文原文，未进入本快照候选集合。
- PriVE-Tools 为 2026 年 7 月新预印本，同行评审状态未确认。
- 尚未发现完全匹配“结构化工具字段变形 + 任务定向等变 + 两类无关不变 + 精确重放 + 正确性四象限”的论文，但这不是穷尽性证明。

## 3. Core Experimental Evidence

### Source: `experiment_v001/result.md`

# 正式实验结果 v001

## 证据资格

- 当前修复实现清单匹配且有效的正式尝试：`attempt-mutation-005`、`attempt-qwen-005`，二者 `runner_exit_code=0`、`metrics_contract_ok=true`、`output_contract_ok=true`。
- `attempt-mutation-004` 与 `attempt-qwen-004` 虽执行契约有效，但首轮固定评审发现其联合判据漏合取完全重复稳定性，故只保留作审计，不再支持最终主张。更早的 `attempt-mutation-002/003` 与 `attempt-qwen-003` 还只绑定了三个运行文件。
- 无效尝试：`attempt-qwen-002` 因包装器把 Ollama 根路径误作聊天端点，600 个请求均返回 HTTP 405，`runner_exit_code=2`；它只作为失败记录，不支持任何科研主张。
- 正式模型身份：Ollama 0.32.13；`qwen2.5:7b` 摘要 `845dbda0ea48`，`qwen3:4b` 摘要 `359d7dd4bcda`，`qwen3:8b` 摘要 `500a1f067a9f`。

## 独立标签校验

两个有效尝试都先执行独立家族求解器。它不读取 `expected` 作为求解输入，也不导入生成器或主评估器；二十个案例全部满足重算标签、相关关系与两类无关不变条件，20/20 通过。该校验只证明合成套件自洽。

## Claim 1：突变判别

正式尝试 `attempt-mutation-005` 共 140 个案例—策略行，无外部模型调用。新增的第七种 `repeat_only_unstable` 策略在基础、相关与两类无关变形上按正确策略作答，只在完全重复时改变答案。

| 信号 | 平衡准确率 |
|---|---:|
| 相关答案发生任意变化 | 0.700 |
| 相关变化 + 两类无关不变 | 0.800 |
| 任务定向双向关系 | 1.000 |

预注册门槛为双向关系至少 0.95，且比第二基线至少高 0.05；实际高 0.200。错误但等变策略 20/20 通过，方向错误但选择性变化策略 0/20 通过。`repeat_only_unstable` 对相关关系与两类无关不变均为 20/20，却对包含完全重复稳定性的联合关系为 0/20。这支持“任务定向关系与重放稳定性共同提供额外采用结构判别”，同时否定把信号解释为答案正确性。

## Claim 2：单次成功关系脆弱性

正式尝试 `attempt-qwen-005` 完成 600 次本地调用、137,969 个令牌、120 个模型—提示—案例行，无调用错误，出现 3 条结构化输出解析警告。

- 53 行基线答案单次精确正确，其中 18 行未通过联合关系；脆弱率为 33.96%。
- 二项比例的 Wilson 95% 区间为 [22.69%, 47.41%]，仅描述冻结套件内的行级比例。
- 18 个关系失败均没有解析警告；因此剔除解析警告后仍为 18/53。
- 六个模型—提示分层中五个出现非零脆弱案例，超过预注册的至少三个分层门槛。
- 分层脆弱率：qwen2.5:7b 严格 0/8，弱 4/5；qwen3:4b 严格 5/9，弱 6/11；qwen3:8b 严格 1/9，弱 2/11。
- 在 53 个单次正确行中，任务相关关系失败 9 行、普通无关字段不变失败 16 行、答案形状诱饵不变失败 4 行、精确重放不稳定 0 行；各类型可重叠。
- 按任务族，关系失败集中于 `filtered_argmin` 8/20 与 `latest_confirmed` 8/12；`count_open` 为 0/16，`tier_score` 为 1/4，`valid_sum` 为 1/1。该异质性限制宽泛外推。

预注册总体门槛为至少 0.10、解析警告剔除后仍非零、至少三个分层出现；三项均通过。结论只支持“冻结本地合成套件中，单次答对可能掩盖关系脆弱性”，不支持真实部署失败率或所有工具任务的一般性。

## 负面与边界结果

- 正式真实模型中没有观察到错误但联合关系通过的行；这不改变突变套件已证明的逻辑可能性，也不能把关系信号升级为正确性验证器。
- 在当前真实模型套件上，联合关系通过与完整四变体精确正确恰好重合（35/120）；这是样本内现象，且两者共享冻结任务语义，不能解释为普遍等价或增量预测价值。
- 当前真实模型的 53 个单次正确行中没有精确重放不稳定；完全重复稳定性在本样本的经验增量为零，但专门反例证明它是联合定义不可省略的逻辑组成。
- 结果高度依赖两个标识选择任务族；数值任务中基线答对样本少，需未来扩大任务结构与模型谱系。
- 固定单一种子保证复现路径，但未估计跨种子方差。

## 当前判断

修复后的两条局部主张均获得正式支持，但方法新颖性仍受 METAL、CAIR、ReliabilityBench、CVT-RL 与 PriVE-Tools 的强类比归约。首轮固定评审指出并促成了联合判据修复；候选能否成为研究种子，取决于第二轮固定评审是否认为“工具字段任务关系 + 双重无关诱饵 + 完全重放 + 正确性四象限”及观察到的单次成功脆弱性值得扩大验证。

### Source: `experiment_v001/attempts/attempt-mutation-005/execution.json`

{
  "argv": [
    "D:\\Desktop\\crl\\env\\crl_agent_v3\\python.exe",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\run_verified_experiment.py",
    "--backend",
    "deterministic",
    "--cases",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\cases.json",
    "--oracle-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\oracle.json",
    "--output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\result.json",
    "--report-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\report.md",
    "--metrics-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\metrics-output.json",
    "--experiment-id",
    "exp-mutation-v005",
    "--seed",
    "20260815",
    "--policies",
    "faithful",
    "wrong_equivariant",
    "misdirected_selective",
    "ignore",
    "distractor",
    "repeat_only_unstable",
    "unstable"
  ],
  "attempt_id": "attempt-mutation-005",
  "budget_facts": {
    "actual": {
      "api_calls": 0,
      "duration_seconds": 0.3936527000005299,
      "gpu_time_seconds": "unknown",
      "tokens": 0
    },
    "comparison": {
      "reason": "budget_ceiling is not a machine-readable JSON object",
      "status": "unavailable"
    },
    "machine_readable_limits": null,
    "spec_budget_ceiling": "0 次外部模型调用，20 案例 × 7 策略 = 140 关系行。",
    "warnings": []
  },
  "capture": {
    "stderr": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\stderr.bin",
      "redaction_applied": false,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "size_bytes": 0
    },
    "stdout": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\stdout.bin",
      "redaction_applied": false,
      "sha256": "83811e9a104df1cbd677b6f2f4b973cc2b2a15495fc2afc9a2ad35de2cbff81b",
      "size_bytes": 381
    }
  },
  "command_error": null,
  "command_exit_code": 0,
  "cwd": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001",
  "duration_seconds": 0.3936527000005299,
  "environment_facts": {
    "cpu_count": 16,
    "declared_facts": {
      "dataset": "frozen-20-case-five-family-suite",
      "dataset_revision": "suite-seed-20260815",
      "model": "seven-deterministic-mutation-policies",
      "model_revision": "implementation-v001-review-fix",
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
          "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\dependencies.txt",
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
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\spec.json",
      "sha256": "e6eac6f2527c68ba944520c6d4be449f798e46dc5a886b4078b0190cdc6d327d",
      "size_bytes": 3751
    },
    "source_path": "experiment_v001/specs/exp-mutation-v005.json"
  },
  "finished_at_utc": "2026-08-15T11:34:17.219452Z",
  "implementation_files": [
    {
      "path": "implementation_v001/cases.json",
      "sha256": "16405ec1aaf9b54c385a855371b2894f3716cd5c54929d780e1103ef10fca577",
      "size_bytes": 62543
    },
    {
      "path": "implementation_v001/causal_uptake_eval.py",
      "sha256": "cdfb7b631cbc413781d7f5286989baf0bc83f66e9dff51f55d519ec6b14f4b28",
      "size_bytes": 28361
    },
    {
      "path": "implementation_v001/generate_suite.py",
      "sha256": "ec912dd620c69677a2ffd5a09a86d78f23c9cee337266c3d70c1f49d44be5d92",
      "size_bytes": 10506
    },
    {
      "path": "implementation_v001/independent_oracle.py",
      "sha256": "ccab49dc3072672c50bbb1a779311ae13e095f39afaada49878ac7a3940fbc82",
      "size_bytes": 6167
    },
    {
      "path": "implementation_v001/run_verified_experiment.py",
      "sha256": "28368d839bccb637e760815860644e6dee1879bbafdc6144450f2854cec6a562",
      "size_bytes": 2540
    },
    {
      "path": "implementation_v001/suite_spec.json",
      "sha256": "6b707be648e99c6c43aea2a0a5b28789dc03e8aaf7b0b54ae517550ebd0b2aa0",
      "size_bytes": 185
    },
    {
      "path": "implementation_v001/test_causal_uptake_eval.py",
      "sha256": "7dd44672688d0c59fe09bbb0672a9c6d9c57f7cd05fc9589d18db0906807c77b",
      "size_bytes": 5653
    }
  ],
  "inputs": [
    {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\cases.json",
      "sha256": "16405ec1aaf9b54c385a855371b2894f3716cd5c54929d780e1103ef10fca577",
      "size_bytes": 62543
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
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\metrics.json",
      "sha256": "3cba49d89c54c244bb7022b10c0eba1f1526dc93efd4f091d9868eb438c1ee03",
      "size_bytes": 892
    },
    "source_path": "experiment_v001/attempts/attempt-mutation-005/metrics-output.json",
    "source_sha256": "3cba49d89c54c244bb7022b10c0eba1f1526dc93efd4f091d9868eb438c1ee03",
    "source_size_bytes": 892,
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
        "sha256": "a7c852693cf16b83fa4e00c17960555164934ae7c61171cbdc1592f1976c5c2a",
        "size_bytes": 12014
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\oracle.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "99d5cee9b6fa3e8e02aef1ea495d2a1d48297e5b994804cc88e9f1822501eed6",
        "size_bytes": 167164
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\result.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "3b7ac917c39e7d38d913a36382b63e2d2c0249696950466c035c655e211b127a",
        "size_bytes": 3447
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\report.md"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "3cba49d89c54c244bb7022b10c0eba1f1526dc93efd4f091d9868eb438c1ee03",
        "size_bytes": 892
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-005\\metrics-output.json"
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
  "started_at_utc": "2026-08-15T11:34:16.826025Z",
  "stdout_as_evidence": false,
  "termination_method": null,
  "timed_out": false,
  "timeout_seconds": 120.0,
  "version": "v001",
  "warnings": []
}

### Source: `experiment_v001/attempts/attempt-qwen-005/execution.json`

{
  "argv": [
    "D:\\Desktop\\crl\\env\\crl_agent_v3\\python.exe",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\run_verified_experiment.py",
    "--backend",
    "ollama",
    "--cases",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\cases.json",
    "--oracle-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\oracle.json",
    "--output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\result.json",
    "--report-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\report.md",
    "--metrics-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\metrics-output.json",
    "--experiment-id",
    "exp-qwen-v005",
    "--seed",
    "123",
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
    "0",
    "--timeout-seconds",
    "120"
  ],
  "attempt_id": "attempt-qwen-005",
  "budget_facts": {
    "actual": {
      "api_calls": 600,
      "duration_seconds": 416.6946885999969,
      "gpu_time_seconds": "unknown",
      "tokens": 137969
    },
    "comparison": {
      "reason": "budget_ceiling is not a machine-readable JSON object",
      "status": "unavailable"
    },
    "machine_readable_limits": null,
    "spec_budget_ceiling": "3 模型 × 2 提示制度 × 20 案例 × 5 调用 = 600 次本地调用；单调用超时 120 秒。",
    "warnings": []
  },
  "capture": {
    "stderr": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\stderr.bin",
      "redaction_applied": false,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "size_bytes": 0
    },
    "stdout": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\stdout.bin",
      "redaction_applied": false,
      "sha256": "5a8df1e556e1f53d2426a2627eef62919f2d92c2f121324801a2a0f91d9bda6c",
      "size_bytes": 368
    }
  },
  "command_error": null,
  "command_exit_code": 0,
  "cwd": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001",
  "duration_seconds": 416.6946885999969,
  "environment_facts": {
    "cpu_count": 16,
    "declared_facts": {
      "dataset": "frozen-20-case-five-family-suite",
      "dataset_revision": "suite-seed-20260815",
      "model": "qwen2.5:7b,qwen3:4b,qwen3:8b",
      "model_revision": "local-ollama-tags-bound-at-execution",
      "prompt_revision": "weak-and-strict-v001-review-fix",
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
          "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\dependencies.txt",
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
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\spec.json",
      "sha256": "139fec8cdd10fa709915b4131a7c9d1d57db0080d7ba997d29f87c8d0be316d1",
      "size_bytes": 3987
    },
    "source_path": "experiment_v001/specs/exp-qwen-v005.json"
  },
  "finished_at_utc": "2026-08-15T11:41:37.198264Z",
  "implementation_files": [
    {
      "path": "implementation_v001/cases.json",
      "sha256": "16405ec1aaf9b54c385a855371b2894f3716cd5c54929d780e1103ef10fca577",
      "size_bytes": 62543
    },
    {
      "path": "implementation_v001/causal_uptake_eval.py",
      "sha256": "cdfb7b631cbc413781d7f5286989baf0bc83f66e9dff51f55d519ec6b14f4b28",
      "size_bytes": 28361
    },
    {
      "path": "implementation_v001/generate_suite.py",
      "sha256": "ec912dd620c69677a2ffd5a09a86d78f23c9cee337266c3d70c1f49d44be5d92",
      "size_bytes": 10506
    },
    {
      "path": "implementation_v001/independent_oracle.py",
      "sha256": "ccab49dc3072672c50bbb1a779311ae13e095f39afaada49878ac7a3940fbc82",
      "size_bytes": 6167
    },
    {
      "path": "implementation_v001/run_verified_experiment.py",
      "sha256": "28368d839bccb637e760815860644e6dee1879bbafdc6144450f2854cec6a562",
      "size_bytes": 2540
    },
    {
      "path": "implementation_v001/suite_spec.json",
      "sha256": "6b707be648e99c6c43aea2a0a5b28789dc03e8aaf7b0b54ae517550ebd0b2aa0",
      "size_bytes": 185
    },
    {
      "path": "implementation_v001/test_causal_uptake_eval.py",
      "sha256": "7dd44672688d0c59fe09bbb0672a9c6d9c57f7cd05fc9589d18db0906807c77b",
      "size_bytes": 5653
    }
  ],
  "inputs": [
    {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\cases.json",
      "sha256": "16405ec1aaf9b54c385a855371b2894f3716cd5c54929d780e1103ef10fca577",
      "size_bytes": 62543
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
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\metrics.json",
      "sha256": "b969042513211ab31306162e1726bc24868370fee028ee621761ea1c245e45af",
      "size_bytes": 1192
    },
    "source_path": "experiment_v001/attempts/attempt-qwen-005/metrics-output.json",
    "source_sha256": "b969042513211ab31306162e1726bc24868370fee028ee621761ea1c245e45af",
    "source_size_bytes": 1192,
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
        "sha256": "a7c852693cf16b83fa4e00c17960555164934ae7c61171cbdc1592f1976c5c2a",
        "size_bytes": 12014
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\oracle.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "359ef9ca9db372317aedf56d38a7a339a230dee316aaea8309c1b5083ea8c041",
        "size_bytes": 349042
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\result.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "65035c834893da96f9bb6261318ebba891da51bae778e1a48a2a856d04e448f6",
        "size_bytes": 3345
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\report.md"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "b969042513211ab31306162e1726bc24868370fee028ee621761ea1c245e45af",
        "size_bytes": 1192
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-005\\metrics-output.json"
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
  "started_at_utc": "2026-08-15T11:34:40.503397Z",
  "stdout_as_evidence": false,
  "termination_method": null,
  "timed_out": false,
  "timeout_seconds": 900.0,
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
- 策略：正确采用、错误但等变采用、结果忽略、诱饵依赖、方向错误但选择性变化、只在完全重复时不稳定、所有变体均不稳定。
- 正标签：前两者，因为标签是“稳定选择性采用”而不是正确性。
- 主要指标：联合关系对正标签的平衡准确率。
- 基线：相关回答是否变化；相关变化且两类无关回答不变。
- 否证：联合关系不能排除方向错误但选择性的策略，不能排除只在完全重复时不稳定的策略，或不能达到高于两个基线的判别力。

### 本地模型现象实验

- 模型：`qwen2.5:7b`、`qwen3:4b`、`qwen3:8b`。
- 提示制度：严格字段说明与弱字段说明。
- 解码：结构化 JSON 答案，关闭思考输出，固定温度与种子。
- 每个模型×制度×案例执行基线、相关变形、普通无关、对抗无关、精确重放，共 600 次调用。
- 主要现象：单次精确正确但联合关系失败的数量和比例；按模型与提示制度分层。
- 保留：原始模型文本、解析警告、资源计数和每例关系结果。

## 独立评价逻辑

一个与主评估器分离的家族求解器从原始工具字段重新计算四个变体的精确答案，不读取案例中的 `expected` 标签，也不调用主评估器的关系函数。正式运行前要求其对二十例全部验证通过。该独立逻辑只保证合成套件标签与变形语义自洽，不证明外部有效性。

## Scratch 与 Formal 边界

初始突变及 600 次本地调用均为 Scratch，只用于塑形主张和锁定实现。随后完成的 `attempt-mutation-004` 与 `attempt-qwen-004` 因首轮固定评审发现联合判据漏合取完全重复稳定性，已退出最终支持链。修复后先冻结 `exp-mutation-v005` 与 `exp-qwen-v005`，再通过 Contract v3 本地实验运行器得到 `attempt-mutation-005` 与 `attempt-qwen-005`；只有第五版尝试作为当前 Formal 支持。

### Source: `experiment_v001/specs/exp-mutation-v005.json`

{
  "baseline_specs": [
    "相关回答是否发生任意变化 relevant_changed。",
    "相关变化且普通/对抗无关回答均不变 selective_change。"
  ],
  "budget_ceiling": "0 次外部模型调用，20 案例 × 7 策略 = 140 关系行。",
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
    "experiment_v001/attempts/attempt-mutation-005/oracle.json",
    "experiment_v001/attempts/attempt-mutation-005/result.json",
    "experiment_v001/attempts/attempt-mutation-005/report.md",
    "experiment_v001/attempts/attempt-mutation-005/metrics.json"
  ],
  "expected_signatures": [
    "双向关系平衡准确率至少 0.95。",
    "双向关系比选择性变化至少高 0.05。",
    "错误但等变策略通过、方向错误但选择性变化策略失败，显示信号是采用结构而非正确性。",
    "只在完全重复时不稳定的策略通过相关关系和无关不变性，但联合关系通过率为 0。"
  ],
  "experiment_id": "exp-mutation-v005",
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
  "model": "七种确定性策略：faithful、wrong_equivariant、misdirected_selective、ignore、distractor、repeat_only_unstable、unstable。",
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
      "notes": "同一 140 行、同一种子与案例顺序。",
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
  "revision": "implementation_v001 full-manifest binding; reviewer-fix: joint relation now includes exact-repeat stability and a repeat-only-unstable mutant",
  "run_id": "20260815_1818_run11",
  "sampling_unit": "冻结案例与可控策略的笛卡尔积，共 140 行。",
  "schema_version": 1,
  "secondary_metrics": [
    "selective_change_balanced_accuracy",
    "any_change_balanced_accuracy",
    "misdirected_selective_pass_rate"
  ],
  "seeds": [
    20260815
  ],
  "version": "v001"
}

### Source: `experiment_v001/specs/exp-qwen-v005.json`

{
  "baseline_specs": [
    "同一 120 行上的单次基线精确正确率。",
    "相关回答发生任意变化与选择性变化信号作为关系消融。"
  ],
  "budget_ceiling": "3 模型 × 2 提示制度 × 20 案例 × 5 调用 = 600 次本地调用；单调用超时 120 秒。",
  "claim_ids": [
    "claim-one-shot-brittleness"
  ],
  "confounders": [
    "同一模型系列之间训练谱系相关。",
    "合成任务短且字段显式，可能与真实多步轨迹不同。",
    "固定单一种子不估计跨种子方差。"
  ],
  "dataset": "五个确定性结构化工具任务族、每族四例、共二十例。",
  "declared_inputs": [
    "implementation_v001/cases.json",
    "implementation_v001/suite_spec.json",
    "implementation_v001/independent_oracle.py"
  ],
  "declared_outputs": [
    "experiment_v001/attempts/attempt-qwen-005/oracle.json",
    "experiment_v001/attempts/attempt-qwen-005/result.json",
    "experiment_v001/attempts/attempt-qwen-005/report.md",
    "experiment_v001/attempts/attempt-qwen-005/metrics.json"
  ],
  "expected_signatures": [
    "总体单次成功关系脆弱率至少 0.10。",
    "解析警告行剔除后仍存在单次正确但关系失败。",
    "至少三个模型-提示分层出现非零脆弱案例。"
  ],
  "experiment_id": "exp-qwen-v005",
  "falsification_rule": "总体脆弱率低于 0.10，或失败全由解析警告解释，或只在一个分层出现，则本地现象主张不支持；不得外推到其他模型或真实部署。",
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
      "notes": "所有模型与提示制度使用同一二十案例、五变体、温度 0 和种子 123。",
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
  "revision": "implementation_v001 full-manifest binding, reviewer-fix joint relation includes exact-repeat stability, endpoint-fix, temperature 0, think false, JSON schema answer string",
  "run_id": "20260815_1818_run11",
  "sampling_unit": "模型 × 提示制度 × 冻结案例，共 120 行；每行五次调用。",
  "schema_version": 1,
  "secondary_metrics": [
    "single_correct_relation_pass",
    "single_correct_relation_fail",
    "strata_with_nonzero_brittleness",
    "parse_warning_count",
    "repeat_instability_count"
  ],
  "seeds": [
    123
  ],
  "version": "v001"
}

## 5. Ablation / Robustness / Falsification Evidence

### Source: `experiment_v001/attempts/attempt-mutation-005/report.md`

# 双向反事实工具证据测试结果

- 后端：`deterministic`
- 案例数：20
- 关系评估行数：140
- 墙钟时间：0.002 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deterministic::distractor | 20 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 |
| deterministic::faithful | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| deterministic::ignore | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| deterministic::misdirected_selective | 20 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| deterministic::repeat_only_unstable | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 | 1.000 | 0.000 |
| deterministic::unstable | 20 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| deterministic::wrong_equivariant | 20 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

## 机械诊断

### deterministic_uptake_discrimination

- `tool_value_overlap`：balanced_accuracy=0.52，precision=0.3076923076923077，recall=0.4，TP/FP/TN/FN=16/36/64/24
- `relevant_changed`：balanced_accuracy=0.7，precision=0.4，recall=1.0，TP/FP/TN/FN=40/60/40/0
- `irrelevant_plain_invariant`：balanced_accuracy=0.6，precision=0.3333333333333333，recall=1.0，TP/FP/TN/FN=40/80/20/0
- `irrelevant_adversarial_invariant`：balanced_accuracy=0.7，precision=0.4，recall=1.0，TP/FP/TN/FN=40/60/40/0
- `irrelevant_invariant`：balanced_accuracy=0.7，precision=0.4，recall=1.0，TP/FP/TN/FN=40/60/40/0
- `selective_change`：balanced_accuracy=0.8，precision=0.5，recall=1.0，TP/FP/TN/FN=40/40/60/0
- `relevant_relation`：balanced_accuracy=0.9，precision=0.6666666666666666，recall=1.0，TP/FP/TN/FN=40/20/80/0
- `bidirectional_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=40/0/100/0

### deterministic_correctness_agreement

- `relevant_changed`：balanced_accuracy=0.6666666666666666，precision=0.2，recall=1.0，TP/FP/TN/FN=20/80/40/0
- `selective_change`：balanced_accuracy=0.75，precision=0.25，recall=1.0，TP/FP/TN/FN=20/60/60/0
- `relevant_relation`：balanced_accuracy=0.8333333333333333，precision=0.3333333333333333，recall=1.0，TP/FP/TN/FN=20/40/80/0
- `bidirectional_relation`：balanced_accuracy=0.9166666666666667，precision=0.5，recall=1.0，TP/FP/TN/FN=20/20/100/0

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

### Source: `experiment_v001/attempts/attempt-qwen-005/report.md`

# 双向反事实工具证据测试结果

- 后端：`ollama`
- 案例数：20
- 关系评估行数：120
- 墙钟时间：416.359 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ollama::qwen2.5:7b::strict | 20 | 0.400 | 0.400 | 1.000 | 0.800 | 0.800 | 0.950 | 0.700 | 0.400 |
| ollama::qwen2.5:7b::weak | 20 | 0.250 | 0.050 | 0.900 | 0.600 | 0.700 | 0.900 | 0.400 | 0.050 |
| ollama::qwen3:4b::strict | 20 | 0.450 | 0.200 | 0.600 | 0.750 | 0.600 | 1.000 | 0.250 | 0.200 |
| ollama::qwen3:4b::weak | 20 | 0.550 | 0.250 | 0.750 | 0.650 | 0.650 | 0.950 | 0.350 | 0.250 |
| ollama::qwen3:8b::strict | 20 | 0.450 | 0.400 | 0.700 | 0.900 | 0.700 | 1.000 | 0.500 | 0.400 |
| ollama::qwen3:8b::weak | 20 | 0.550 | 0.450 | 0.650 | 0.900 | 0.700 | 0.900 | 0.550 | 0.450 |

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

- `tool_value_overlap`：balanced_accuracy=0.45210084033613446，precision=0.25396825396825395，recall=0.45714285714285713，TP/FP/TN/FN=16/47/38/19
- `relevant_changed`：balanced_accuracy=0.6647058823529411，precision=0.3804347826086957，recall=1.0，TP/FP/TN/FN=35/57/28/0
- `selective_change`：balanced_accuracy=0.8823529411764706，precision=0.6363636363636364，recall=1.0，TP/FP/TN/FN=35/20/65/0
- `relevant_relation`：balanced_accuracy=0.9117647058823529，precision=0.7，recall=1.0，TP/FP/TN/FN=35/15/70/0
- `bidirectional_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=35/0/85/0

### diagnostic_quadrants

- `single_correct_relation_pass`：35
- `single_correct_relation_fail`：18
- `single_wrong_relation_pass`：0
- `single_wrong_relation_fail`：67
- `one_shot_success_brittleness_rate`：0.33962264150943394
- `systematic_wrong_uptake_rate`：0.0

> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。

### Source: `experiment_v001/attempts/attempt-mutation-005/result.json`

{
  "schema_version": 1,
  "experiment_id": "exp-mutation-v005",
  "configuration": {
    "backend": "deterministic",
    "policies": [
      "faithful",
      "wrong_equivariant",
      "misdirected_selective",
      "ignore",
      "distractor",
      "repeat_only_unstable",
      "unstable"
    ],
    "models": [],
    "prompt_regimes": [],
    "temperature": 0.0,
    "seed": 20260815
  },
  "case_count": 20,
  "rows": [
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A",
        "repeat": "M00-A"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A",
        "repeat": "M01-A"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A",
        "repeat": "M02-A"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A",
        "repeat": "M03-A"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C",
        "repeat": "E00-C"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C",
        "repeat": "E01-C"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C",
        "repeat": "E02-C"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C",
        "repeat": "E03-C"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30",
        "repeat": "30"
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55",
        "repeat": "55"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33",
        "repeat": "33"
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37",
        "repeat": "37"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15",
        "repeat": "15"
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29",
        "repeat": "29"
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27",
        "repeat": "27"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31",
        "repeat": "31"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "deterministic::faithful",
      "backend": "deterministic",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": true
    },
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "M00-B",
        "relevant": "M00-A",
        "irrelevant_plain": "M00-B",
        "irrelevant_adversarial": "M00-B",
        "repeat": "M00-B"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "M01-B",
        "relevant": "M01-A",
        "irrelevant_plain": "M01-B",
        "irrelevant_adversarial": "M01-B",
        "repeat": "M01-B"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "M02-B",
        "relevant": "M02-A",
        "irrelevant_plain": "M02-B",
        "irrelevant_adversarial": "M02-B",
        "repeat": "M02-B"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "M03-B",
        "relevant": "M03-A",
        "irrelevant_plain": "M03-B",
        "irrelevant_adversarial": "M03-B",
        "repeat": "M03-B"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "E00-B",
        "relevant": "E00-C",
        "irrelevant_plain": "E00-B",
        "irrelevant_adversarial": "E00-B",
        "repeat": "E00-B"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "E01-B",
        "relevant": "E01-C",
        "irrelevant_plain": "E01-B",
        "irrelevant_adversarial": "E01-B",
        "repeat": "E01-B"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "E02-B",
        "relevant": "E02-C",
        "irrelevant_plain": "E02-B",
        "irrelevant_adversarial": "E02-B",
        "repeat": "E02-B"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "E03-B",
        "relevant": "E03-C",
        "irrelevant_plain": "E03-B",
        "irrelevant_adversarial": "E03-B",
        "repeat": "E03-B"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "1030",
        "relevant": "1034",
        "irrelevant_plain": "1030",
        "irrelevant_adversarial": "1030",
        "repeat": "1030"
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "1055",
        "relevant": "1059",
        "irrelevant_plain": "1055",
        "irrelevant_adversarial": "1055",
        "repeat": "1055"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "1033",
        "relevant": "1039",
        "irrelevant_plain": "1033",
        "irrelevant_adversarial": "1033",
        "repeat": "1033"
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "1037",
        "relevant": "1042",
        "irrelevant_plain": "1037",
        "irrelevant_adversarial": "1037",
        "repeat": "1037"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "1015",
        "relevant": "1020",
        "irrelevant_plain": "1015",
        "irrelevant_adversarial": "1015",
        "repeat": "1015"
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "1029",
        "relevant": "1033",
        "irrelevant_plain": "1029",
        "irrelevant_adversarial": "1029",
        "repeat": "1029"
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "1027",
        "relevant": "1029",
        "irrelevant_plain": "1027",
        "irrelevant_adversarial": "1027",
        "repeat": "1027"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "1031",
        "relevant": "1036",
        "irrelevant_plain": "1031",
        "irrelevant_adversarial": "1031",
        "repeat": "1031"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "1002",
        "relevant": "1003",
        "irrelevant_plain": "1002",
        "irrelevant_adversarial": "1002",
        "repeat": "1002"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "1002",
        "relevant": "1003",
        "irrelevant_plain": "1002",
        "irrelevant_adversarial": "1002",
        "repeat": "1002"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "1002",
        "relevant": "1003",
        "irrelevant_plain": "1002",
        "irrelevant_adversarial": "1002",
        "repeat": "1002"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "deterministic::wrong_equivariant",
      "backend": "deterministic",
      "answers": {
        "base": "1002",
        "relevant": "1003",
        "irrelevant_plain": "1002",
        "irrelevant_adversarial": "1002",
        "repeat": "1002"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": true,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::filtered_argmin_00::base",
        "relevant": "misdirected::filtered_argmin_00::changed",
        "irrelevant_plain": "misdirected::filtered_argmin_00::base",
        "irrelevant_adversarial": "misdirected::filtered_argmin_00::base",
        "repeat": "misdirected::filtered_argmin_00::base"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::filtered_argmin_01::base",
        "relevant": "misdirected::filtered_argmin_01::changed",
        "irrelevant_plain": "misdirected::filtered_argmin_01::base",
        "irrelevant_adversarial": "misdirected::filtered_argmin_01::base",
        "repeat": "misdirected::filtered_argmin_01::base"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::filtered_argmin_02::base",
        "relevant": "misdirected::filtered_argmin_02::changed",
        "irrelevant_plain": "misdirected::filtered_argmin_02::base",
        "irrelevant_adversarial": "misdirected::filtered_argmin_02::base",
        "repeat": "misdirected::filtered_argmin_02::base"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::filtered_argmin_03::base",
        "relevant": "misdirected::filtered_argmin_03::changed",
        "irrelevant_plain": "misdirected::filtered_argmin_03::base",
        "irrelevant_adversarial": "misdirected::filtered_argmin_03::base",
        "repeat": "misdirected::filtered_argmin_03::base"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::latest_confirmed_00::base",
        "relevant": "misdirected::latest_confirmed_00::changed",
        "irrelevant_plain": "misdirected::latest_confirmed_00::base",
        "irrelevant_adversarial": "misdirected::latest_confirmed_00::base",
        "repeat": "misdirected::latest_confirmed_00::base"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::latest_confirmed_01::base",
        "relevant": "misdirected::latest_confirmed_01::changed",
        "irrelevant_plain": "misdirected::latest_confirmed_01::base",
        "irrelevant_adversarial": "misdirected::latest_confirmed_01::base",
        "repeat": "misdirected::latest_confirmed_01::base"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::latest_confirmed_02::base",
        "relevant": "misdirected::latest_confirmed_02::changed",
        "irrelevant_plain": "misdirected::latest_confirmed_02::base",
        "irrelevant_adversarial": "misdirected::latest_confirmed_02::base",
        "repeat": "misdirected::latest_confirmed_02::base"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::latest_confirmed_03::base",
        "relevant": "misdirected::latest_confirmed_03::changed",
        "irrelevant_plain": "misdirected::latest_confirmed_03::base",
        "irrelevant_adversarial": "misdirected::latest_confirmed_03::base",
        "repeat": "misdirected::latest_confirmed_03::base"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::valid_sum_00::base",
        "relevant": "misdirected::valid_sum_00::changed",
        "irrelevant_plain": "misdirected::valid_sum_00::base",
        "irrelevant_adversarial": "misdirected::valid_sum_00::base",
        "repeat": "misdirected::valid_sum_00::base"
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::valid_sum_01::base",
        "relevant": "misdirected::valid_sum_01::changed",
        "irrelevant_plain": "misdirected::valid_sum_01::base",
        "irrelevant_adversarial": "misdirected::valid_sum_01::base",
        "repeat": "misdirected::valid_sum_01::base"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::valid_sum_02::base",
        "relevant": "misdirected::valid_sum_02::changed",
        "irrelevant_plain": "misdirected::valid_sum_02::base",
        "irrelevant_adversarial": "misdirected::valid_sum_02::base",
        "repeat": "misdirected::valid_sum_02::base"
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::valid_sum_03::base",
        "relevant": "misdirected::valid_sum_03::changed",
        "irrelevant_plain": "misdirected::valid_sum_03::base",
        "irrelevant_adversarial": "misdirected::valid_sum_03::base",
        "repeat": "misdirected::valid_sum_03::base"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::tier_score_00::base",
        "relevant": "misdirected::tier_score_00::changed",
        "irrelevant_plain": "misdirected::tier_score_00::base",
        "irrelevant_adversarial": "misdirected::tier_score_00::base",
        "repeat": "misdirected::tier_score_00::base"
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::tier_score_01::base",
        "relevant": "misdirected::tier_score_01::changed",
        "irrelevant_plain": "misdirected::tier_score_01::base",
        "irrelevant_adversarial": "misdirected::tier_score_01::base",
        "repeat": "misdirected::tier_score_01::base"
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::tier_score_02::base",
        "relevant": "misdirected::tier_score_02::changed",
        "irrelevant_plain": "misdirected::tier_score_02::base",
        "irrelevant_adversarial": "misdirected::tier_score_02::base",
        "repeat": "misdirected::tier_score_02::base"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::tier_score_03::base",
        "relevant": "misdirected::tier_score_03::changed",
        "irrelevant_plain": "misdirected::tier_score_03::base",
        "irrelevant_adversarial": "misdirected::tier_score_03::base",
        "repeat": "misdirected::tier_score_03::base"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::count_open_00::base",
        "relevant": "misdirected::count_open_00::changed",
        "irrelevant_plain": "misdirected::count_open_00::base",
        "irrelevant_adversarial": "misdirected::count_open_00::base",
        "repeat": "misdirected::count_open_00::base"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::count_open_01::base",
        "relevant": "misdirected::count_open_01::changed",
        "irrelevant_plain": "misdirected::count_open_01::base",
        "irrelevant_adversarial": "misdirected::count_open_01::base",
        "repeat": "misdirected::count_open_01::base"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::count_open_02::base",
        "relevant": "misdirected::count_open_02::changed",
        "irrelevant_plain": "misdirected::count_open_02::base",
        "irrelevant_adversarial": "misdirected::count_open_02::base",
        "repeat": "misdirected::count_open_02::base"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "deterministic::misdirected_selective",
      "backend": "deterministic",
      "answers": {
        "base": "misdirected::count_open_03::base",
        "relevant": "misdirected::count_open_03::changed",
        "irrelevant_plain": "misdirected::count_open_03::base",
        "irrelevant_adversarial": "misdirected::count_open_03::base",
        "repeat": "misdirected::count_open_03::base"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "M00-A",
        "relevant": "M00-A",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A",
        "repeat": "M00-A"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "M01-A",
        "relevant": "M01-A",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A",
        "repeat": "M01-A"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "M02-A",
        "relevant": "M02-A",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A",
        "repeat": "M02-A"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "M03-A",
        "relevant": "M03-A",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A",
        "repeat": "M03-A"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "E00-C",
        "relevant": "E00-C",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C",
        "repeat": "E00-C"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "E01-C",
        "relevant": "E01-C",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C",
        "repeat": "E01-C"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "E02-C",
        "relevant": "E02-C",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C",
        "repeat": "E02-C"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "E03-C",
        "relevant": "E03-C",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C",
        "repeat": "E03-C"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "30",
        "relevant": "30",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30",
        "repeat": "30"
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "55",
        "relevant": "55",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55",
        "repeat": "55"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "33",
        "relevant": "33",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33",
        "repeat": "33"
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "37",
        "relevant": "37",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37",
        "repeat": "37"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "15",
        "relevant": "15",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15",
        "repeat": "15"
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "29",
        "relevant": "29",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29",
        "repeat": "29"
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "27",
        "relevant": "27",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27",
        "repeat": "27"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "31",
        "relevant": "31",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31",
        "repeat": "31"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "2",
        "relevant": "2",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "2",
        "relevant": "2",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "2",
        "relevant": "2",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "deterministic::ignore",
      "backend": "deterministic",
      "answers": {
        "base": "2",
        "relevant": "2",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "M00-C",
        "relevant": "M00-C",
        "irrelevant_plain": "M00-C",
        "irrelevant_adversarial": "M00-B",
        "repeat": "M00-C"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "M01-C",
        "relevant": "M01-C",
        "irrelevant_plain": "M01-C",
        "irrelevant_adversarial": "M01-B",
        "repeat": "M01-C"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "M02-C",
        "relevant": "M02-C",
        "irrelevant_plain": "M02-C",
        "irrelevant_adversarial": "M02-B",
        "repeat": "M02-C"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "M03-C",
        "relevant": "M03-C",
        "irrelevant_plain": "M03-C",
        "irrelevant_adversarial": "M03-B",
        "repeat": "M03-C"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "E00-A",
        "relevant": "E00-A",
        "irrelevant_plain": "E00-A",
        "irrelevant_adversarial": "E00-D",
        "repeat": "E00-A"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "E01-A",
        "relevant": "E01-A",
        "irrelevant_plain": "E01-A",
        "irrelevant_adversarial": "E01-D",
        "repeat": "E01-A"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "E02-A",
        "relevant": "E02-A",
        "irrelevant_plain": "E02-A",
        "irrelevant_adversarial": "E02-D",
        "repeat": "E02-A"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "E03-A",
        "relevant": "E03-A",
        "irrelevant_plain": "E03-A",
        "irrelevant_adversarial": "E03-D",
        "repeat": "E03-A"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "143",
        "relevant": "143",
        "irrelevant_plain": "143",
        "irrelevant_adversarial": "1030",
        "repeat": "143"
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "128",
        "relevant": "128",
        "irrelevant_plain": "128",
        "irrelevant_adversarial": "1055",
        "repeat": "128"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "98",
        "relevant": "98",
        "irrelevant_plain": "98",
        "irrelevant_adversarial": "1033",
        "repeat": "98"
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "173",
        "relevant": "173",
        "irrelevant_plain": "173",
        "irrelevant_adversarial": "1037",
        "repeat": "173"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "7",
        "relevant": "7",
        "irrelevant_plain": "7",
        "irrelevant_adversarial": "114",
        "repeat": "7"
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "9",
        "relevant": "9",
        "irrelevant_plain": "9",
        "irrelevant_adversarial": "128",
        "repeat": "9"
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "9",
        "relevant": "9",
        "irrelevant_plain": "9",
        "irrelevant_adversarial": "126",
        "repeat": "9"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "11",
        "relevant": "11",
        "irrelevant_plain": "11",
        "irrelevant_adversarial": "130",
        "repeat": "11"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "5",
        "relevant": "5",
        "irrelevant_plain": "5",
        "irrelevant_adversarial": "0",
        "repeat": "5"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "5",
        "relevant": "5",
        "irrelevant_plain": "5",
        "irrelevant_adversarial": "0",
        "repeat": "5"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "5",
        "relevant": "5",
        "irrelevant_plain": "5",
        "irrelevant_adversarial": "0",
        "repeat": "5"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "deterministic::distractor",
      "backend": "deterministic",
      "answers": {
        "base": "5",
        "relevant": "5",
        "irrelevant_plain": "5",
        "irrelevant_adversarial": "0",
        "repeat": "5"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A",
        "repeat": "repeat-only-unstable::filtered_argmin_00"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A",
        "repeat": "repeat-only-unstable::filtered_argmin_01"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A",
        "repeat": "repeat-only-unstable::filtered_argmin_02"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A",
        "repeat": "repeat-only-unstable::filtered_argmin_03"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C",
        "repeat": "repeat-only-unstable::latest_confirmed_00"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C",
        "repeat": "repeat-only-unstable::latest_confirmed_01"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C",
        "repeat": "repeat-only-unstable::latest_confirmed_02"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C",
        "repeat": "repeat-only-unstable::latest_confirmed_03"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30",
        "repeat": "repeat-only-unstable::valid_sum_00"
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55",
        "repeat": "repeat-only-unstable::valid_sum_01"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33",
        "repeat": "repeat-only-unstable::valid_sum_02"
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37",
        "repeat": "repeat-only-unstable::valid_sum_03"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15",
        "repeat": "repeat-only-unstable::tier_score_00"
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29",
        "repeat": "repeat-only-unstable::tier_score_01"
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27",
        "repeat": "repeat-only-unstable::tier_score_02"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31",
        "repeat": "repeat-only-unstable::tier_score_03"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "repeat-only-unstable::count_open_00"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "repeat-only-unstable::count_open_01"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "repeat-only-unstable::count_open_02"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "deterministic::repeat_only_unstable",
      "backend": "deterministic",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "repeat-only-unstable::count_open_03"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::filtered_argmin_00::base",
        "relevant": "unstable::filtered_argmin_00::relevant",
        "irrelevant_plain": "unstable::filtered_argmin_00::irrelevant_plain",
        "irrelevant_adversarial": "unstable::filtered_argmin_00::irrelevant_adversarial",
        "repeat": "unstable::filtered_argmin_00::repeat"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::filtered_argmin_01::base",
        "relevant": "unstable::filtered_argmin_01::relevant",
        "irrelevant_plain": "unstable::filtered_argmin_01::irrelevant_plain",
        "irrelevant_adversarial": "unstable::filtered_argmin_01::irrelevant_adversarial",
        "repeat": "unstable::filtered_argmin_01::repeat"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::filtered_argmin_02::base",
        "relevant": "unstable::filtered_argmin_02::relevant",
        "irrelevant_plain": "unstable::filtered_argmin_02::irrelevant_plain",
        "irrelevant_adversarial": "unstable::filtered_argmin_02::irrelevant_adversarial",
        "repeat": "unstable::filtered_argmin_02::repeat"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::filtered_argmin_03::base",
        "relevant": "unstable::filtered_argmin_03::relevant",
        "irrelevant_plain": "unstable::filtered_argmin_03::irrelevant_plain",
        "irrelevant_adversarial": "unstable::filtered_argmin_03::irrelevant_adversarial",
        "repeat": "unstable::filtered_argmin_03::repeat"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::latest_confirmed_00::base",
        "relevant": "unstable::latest_confirmed_00::relevant",
        "irrelevant_plain": "unstable::latest_confirmed_00::irrelevant_plain",
        "irrelevant_adversarial": "unstable::latest_confirmed_00::irrelevant_adversarial",
        "repeat": "unstable::latest_confirmed_00::repeat"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::latest_confirmed_01::base",
        "relevant": "unstable::latest_confirmed_01::relevant",
        "irrelevant_plain": "unstable::latest_confirmed_01::irrelevant_plain",
        "irrelevant_adversarial": "unstable::latest_confirmed_01::irrelevant_adversarial",
        "repeat": "unstable::latest_confirmed_01::repeat"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::latest_confirmed_02::base",
        "relevant": "unstable::latest_confirmed_02::relevant",
        "irrelevant_plain": "unstable::latest_confirmed_02::irrelevant_plain",
        "irrelevant_adversarial": "unstable::latest_confirmed_02::irrelevant_adversarial",
        "repeat": "unstable::latest_confirmed_02::repeat"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::latest_confirmed_03::base",
        "relevant": "unstable::latest_confirmed_03::relevant",
        "irrelevant_plain": "unstable::latest_confirmed_03::irrelevant_plain",
        "irrelevant_adversarial": "unstable::latest_confirmed_03::irrelevant_adversarial",
        "repeat": "unstable::latest_confirmed_03::repeat"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::valid_sum_00::base",
        "relevant": "unstable::valid_sum_00::relevant",
        "irrelevant_plain": "unstable::valid_sum_00::irrelevant_plain",
        "irrelevant_adversarial": "unstable::valid_sum_00::irrelevant_adversarial",
        "repeat": "unstable::valid_sum_00::repeat"
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::valid_sum_01::base",
        "relevant": "unstable::valid_sum_01::relevant",
        "irrelevant_plain": "unstable::valid_sum_01::irrelevant_plain",
        "irrelevant_adversarial": "unstable::valid_sum_01::irrelevant_adversarial",
        "repeat": "unstable::valid_sum_01::repeat"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::valid_sum_02::base",
        "relevant": "unstable::valid_sum_02::relevant",
        "irrelevant_plain": "unstable::valid_sum_02::irrelevant_plain",
        "irrelevant_adversarial": "unstable::valid_sum_02::irrelevant_adversarial",
        "repeat": "unstable::valid_sum_02::repeat"
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::valid_sum_03::base",
        "relevant": "unstable::valid_sum_03::relevant",
        "irrelevant_plain": "unstable::valid_sum_03::irrelevant_plain",
        "irrelevant_adversarial": "unstable::valid_sum_03::irrelevant_adversarial",
        "repeat": "unstable::valid_sum_03::repeat"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::tier_score_00::base",
        "relevant": "unstable::tier_score_00::relevant",
        "irrelevant_plain": "unstable::tier_score_00::irrelevant_plain",
        "irrelevant_adversarial": "unstable::tier_score_00::irrelevant_adversarial",
        "repeat": "unstable::tier_score_00::repeat"
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::tier_score_01::base",
        "relevant": "unstable::tier_score_01::relevant",
        "irrelevant_plain": "unstable::tier_score_01::irrelevant_plain",
        "irrelevant_adversarial": "unstable::tier_score_01::irrelevant_adversarial",
        "repeat": "unstable::tier_score_01::repeat"
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::tier_score_02::base",
        "relevant": "unstable::tier_score_02::relevant",
        "irrelevant_plain": "unstable::tier_score_02::irrelevant_plain",
        "irrelevant_adversarial": "unstable::tier_score_02::irrelevant_adversarial",
        "repeat": "unstable::tier_score_02::repeat"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::tier_score_03::base",
        "relevant": "unstable::tier_score_03::relevant",
        "irrelevant_plain": "unstable::tier_score_03::irrelevant_plain",
        "irrelevant_adversarial": "unstable::tier_score_03::irrelevant_adversarial",
        "repeat": "unstable::tier_score_03::repeat"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::count_open_00::base",
        "relevant": "unstable::count_open_00::relevant",
        "irrelevant_plain": "unstable::count_open_00::irrelevant_plain",
        "irrelevant_adversarial": "unstable::count_open_00::irrelevant_adversarial",
        "repeat": "unstable::count_open_00::repeat"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::count_open_01::base",
        "relevant": "unstable::count_open_01::relevant",
        "irrelevant_plain": "unstable::count_open_01::irrelevant_plain",
        "irrelevant_adversarial": "unstable::count_open_01::irrelevant_adversarial",
        "repeat": "unstable::count_open_01::repeat"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::count_open_02::base",
        "relevant": "unstable::count_open_02::relevant",
        "irrelevant_plain": "unstable::count_open_02::irrelevant_plain",
        "irrelevant_adversarial": "unstable::count_open_02::irrelevant_adversarial",
        "repeat": "unstable::count_open_02::repeat"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "deterministic::unstable",
      "backend": "deterministic",
      "answers": {
        "base": "unstable::count_open_03::base",
        "relevant": "unstable::count_open_03::relevant",
        "irrelevant_plain": "unstable::count_open_03::irrelevant_plain",
        "irrelevant_adversarial": "unstable::count_open_03::irrelevant_adversarial",
        "repeat": "unstable::count_open_03::repeat"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [],
      "warnings": [],
      "known_selective_uptake_policy": false,
      "known_correct_policy": false
    }
  ],
  "aggregate": {
    "by_agent": {
      "deterministic::distractor": {
        "n": 20,
        "exact_base": 0.0,
        "exact_counterfactual_set": 0.0,
        "tool_value_overlap": 1.0,
        "relevant_changed": 0.0,
        "irrelevant_plain_invariant": 1.0,
        "irrelevant_adversarial_invariant": 0.0,
        "irrelevant_invariant": 0.0,
        "repeat_stable": 1.0,
        "selective_change": 0.0,
        "relevant_relation": 0.0,
        "bidirectional_relation": 0.0
      },
      "deterministic::faithful": {
        "n": 20,
        "exact_base": 1.0,
        "exact_counterfactual_set": 1.0,
        "tool_value_overlap": 0.4,
        "relevant_changed": 1.0,
        "irrelevant_plain_invariant": 1.0,
        "irrelevant_adversarial_invariant": 1.0,
        "irrelevant_invariant": 1.0,
        "repeat_stable": 1.0,
        "selective_change": 1.0,
        "relevant_relation": 1.0,
        "bidirectional_relation": 1.0
      },
      "deterministic::ignore": {
        "n": 20,
        "exact_base": 1.0,
        "exact_counterfactual_set": 0.0,
        "tool_value_overlap": 0.4,
        "relevant_changed": 0.0,
        "irrelevant_plain_invariant": 1.0,
        "irrelevant_adversarial_invariant": 1.0,
        "irrelevant_invariant": 1.0,
        "repeat_stable": 1.0,
        "selective_change": 0.0,
        "relevant_relation": 0.0,
        "bidirectional_relation": 0.0
      },
      "deterministic::misdirected_selective": {
        "n": 20,
        "exact_base": 0.0,
        "exact_counterfactual_set": 0.0,
        "tool_value_overlap": 0.0,
        "relevant_changed": 1.0,
        "irrelevant_plain_invariant": 1.0,
        "irrelevant_adversarial_invariant": 1.0,
        "irrelevant_invariant": 1.0,
        "repeat_stable": 1.0,
        "selective_change": 1.0,
        "relevant_relation": 0.0,
        "bidirectional_relation": 0.0
      },
      "deterministic::repeat_only_unstable": {
        "n": 20,
        "exact_base": 1.0,
        "exact_counterfactual_set": 1.0,
        "tool_value_overlap": 0.4,
        "relevant_changed": 1.0,
        "irrelevant_plain_invariant": 1.0,
        "irrelevant_adversarial_invariant": 1.0,
        "irrelevant_invariant": 1.0,
        "repeat_stable": 0.0,
        "selective_change": 1.0,
        "relevant_relation": 1.0,
        "bidirectional_relation": 0.0
      },
      "deterministic::unstable": {
        "n": 20,
        "exact_base": 0.0,
        "exact_counterfactual_set": 0.0,
        "tool_value_overlap": 0.0,
        "relevant_changed": 1.0,
        "irrelevant_plain_invariant": 0.0,
        "irrelevant_adversarial_invariant": 0.0,
        "irrelevant_invariant": 0.0,
        "repeat_stable": 0.0,
        "selective_change": 0.0,
        "relevant_relation": 0.0,
        "bidirectional_relation": 0.0
      },
      "deterministic::wrong_equivariant": {
        "n": 20,
        "exact_base": 0.0,
        "exact_counterfactual_set": 0.0,
        "tool_value_overlap": 0.4,
        "relevant_changed": 1.0,
        "irrelevant_plain_invariant": 1.0,
        "irrelevant_adversarial_invariant": 1.0,
        "irrelevant_invariant": 1.0,
        "repeat_stable": 1.0,
        "selective_change": 1.0,
        "relevant_relation": 1.0,
        "bidirectional_relation": 1.0
      }
    },
    "deterministic_uptake_discrimination": {
      "tool_value_overlap": {
        "tp": 16,
        "fp": 36,
        "tn": 64,
        "fn": 24,
        "precision": 0.3076923076923077,
        "recall": 0.4,
        "balanced_accuracy": 0.52,
        "accuracy": 0.5714285714285714
      },
      "relevant_changed": {
        "tp": 40,
        "fp": 60,
        "tn": 40,
        "fn": 0,
        "precision": 0.4,
        "recall": 1.0,
        "balanced_accuracy": 0.7,
        "accuracy": 0.5714285714285714
      },
      "irrelevant_plain_invariant": {
        "tp": 40,
        "fp": 80,
        "tn": 20,
        "fn": 0,
        "precision": 0.3333333333333333,
        "recall": 1.0,
        "balanced_accuracy": 0.6,
        "accuracy": 0.42857142857142855
      },
      "irrelevant_adversarial_invariant": {
        "tp": 40,
        "fp": 60,
        "tn": 40,
        "fn": 0,
        "precision": 0.4,
        "recall": 1.0,
        "balanced_accuracy": 0.7,
        "accuracy": 0.5714285714285714
      },
      "irrelevant_invariant": {
        "tp": 40,
        "fp": 60,
        "tn": 40,
        "fn": 0,
        "precision": 0.4,
        "recall": 1.0,
        "balanced_accuracy": 0.7,
        "accuracy": 0.5714285714285714
      },
      "selective_change": {
        "tp": 40,
        "fp": 40,
        "tn": 60,
        "fn": 0,
        "precision": 0.5,
        "recall": 1.0,
        "balanced_accuracy": 0.8,
        "accuracy": 0.7142857142857143
      },
      "relevant_relation": {
        "tp": 40,
        "fp": 20,
        "tn": 80,
        "fn": 0,
        "precision": 0.6666666666666666,
        "recall": 1.0,
        "balanced_accuracy": 0.9,
        "accuracy": 0.8571428571428571
      },
      "bidirectional_relation": {
        "tp": 40,
        "fp": 0,
        "tn": 100,
        "fn": 0,
        "precision": 1.0,
        "recall": 1.0,
        "balanced_accuracy": 1.0,
        "accuracy": 1.0
      }
    },
    "deterministic_correctness_agreement": {
      "relevant_changed": {
        "tp": 20,
        "fp": 80,
        "tn": 40,
        "fn": 0,
        "precision": 0.2,
        "recall": 1.0,
        "balanced_accuracy": 0.6666666666666666,
        "accuracy": 0.42857142857142855
      },
      "selective_change": {
        "tp": 20,
        "fp": 60,
        "tn": 60,
        "fn": 0,
        "precision": 0.25,
        "recall": 1.0,
        "balanced_accuracy": 0.75,
        "accuracy": 0.5714285714285714
      },
      "relevant_relation": {
        "tp": 20,
        "fp": 40,
        "tn": 80,
        "fn": 0,
        "precision": 0.3333333333333333,
        "recall": 1.0,
        "balanced_accuracy": 0.8333333333333333,
        "accuracy": 0.7142857142857143
      },
      "bidirectional_relation": {
        "tp": 20,
        "fp": 20,
        "tn": 100,
        "fn": 0,
        "precision": 0.5,
        "recall": 1.0,
        "balanced_accuracy": 0.9166666666666667,
        "accuracy": 0.8571428571428571
      }
    },
    "ollama_signal_agreement_with_exact_counterfactual_set": {
      "tool_value_overlap": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "relevant_changed": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "selective_change": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "relevant_relation": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "bidirectional_relation": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      }
    },
    "diagnostic_quadrants": {
      "single_correct_relation_pass": 0,
      "single_correct_relation_fail": 0,
      "single_wrong_relation_pass": 0,
      "single_wrong_relation_fail": 0,
      "one_shot_success_brittleness_rate": null,
      "systematic_wrong_uptake_rate": null
    }
  },
  "resource_usage": {
    "tokens": 0,
    "api_calls": 0,
    "wall_time_seconds": 0.0021987000000081025,
    "gpu_time_seconds": "unknown",
    "estimated_cost": "unknown"
  },
  "errors": [],
  "warnings": []
}

### Source: `experiment_v001/attempts/attempt-qwen-005/result.json`

{
  "schema_version": 1,
  "experiment_id": "exp-qwen-v005",
  "configuration": {
    "backend": "ollama",
    "policies": [],
    "models": [
      "qwen2.5:7b",
      "qwen3:4b",
      "qwen3:8b"
    ],
    "prompt_regimes": [
      "weak",
      "strict"
    ],
    "temperature": 0.0,
    "seed": 123
  },
  "case_count": 20,
  "rows": [
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-D",
        "irrelevant_adversarial": "M00-A",
        "repeat": "M00-A"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 8.263592299997981,
            "prompt_eval_count": 195,
            "eval_count": 10,
            "total_duration_ns": 8249154600,
            "load_duration_ns": 7903105400
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6248379999997269,
            "prompt_eval_count": 195,
            "eval_count": 10,
            "total_duration_ns": 621497300,
            "load_duration_ns": 376402800
          },
          "raw_content": "{\"answer\": \"M00-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6209793000016361,
            "prompt_eval_count": 199,
            "eval_count": 10,
            "total_duration_ns": 610318200,
            "load_duration_ns": 370945400
          },
          "raw_content": "{\"answer\": \"M00-D\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.684965699998429,
            "prompt_eval_count": 195,
            "eval_count": 10,
            "total_duration_ns": 683160700,
            "load_duration_ns": 447300200
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5257908999992651,
            "prompt_eval_count": 195,
            "eval_count": 10,
            "total_duration_ns": 523788800,
            "load_duration_ns": 318081500
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-C",
        "irrelevant_adversarial": "M01-A",
        "repeat": "M01-A"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7195238999993308,
            "prompt_eval_count": 198,
            "eval_count": 10,
            "total_duration_ns": 717607700,
            "load_duration_ns": 485724900
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5850298000004841,
            "prompt_eval_count": 198,
            "eval_count": 10,
            "total_duration_ns": 580690000,
            "load_duration_ns": 346675000
          },
          "raw_content": "{\"answer\": \"M01-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6216419999982463,
            "prompt_eval_count": 202,
            "eval_count": 10,
            "total_duration_ns": 620018900,
            "load_duration_ns": 369006100
          },
          "raw_content": "{\"answer\": \"M01-C\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5504418000018632,
            "prompt_eval_count": 198,
            "eval_count": 10,
            "total_duration_ns": 549378300,
            "load_duration_ns": 317367800
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6104499000030046,
            "prompt_eval_count": 198,
            "eval_count": 10,
            "total_duration_ns": 587529800,
            "load_duration_ns": 376312600
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A",
        "repeat": "M02-A"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5519474000029732,
            "prompt_eval_count": 196,
            "eval_count": 10,
            "total_duration_ns": 550205200,
            "load_duration_ns": 318651100
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6285515000017767,
            "prompt_eval_count": 196,
            "eval_count": 10,
            "total_duration_ns": 622356000,
            "load_duration_ns": 379306600
          },
          "raw_content": "{\"answer\": \"M02-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.631622699998843,
            "prompt_eval_count": 200,
            "eval_count": 10,
            "total_duration_ns": 613683600,
            "load_duration_ns": 373017800
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5721516999983578,
            "prompt_eval_count": 196,
            "eval_count": 10,
            "total_duration_ns": 569968200,
            "load_duration_ns": 333356400
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6091825000003155,
            "prompt_eval_count": 196,
            "eval_count": 10,
            "total_duration_ns": 595781400,
            "load_duration_ns": 380808900
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-C",
        "irrelevant_adversarial": "M03-A",
        "repeat": "M03-A"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6217676000014762,
            "prompt_eval_count": 198,
            "eval_count": 10,
            "total_duration_ns": 619090000,
            "load_duration_ns": 376681200
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6292332000011811,
            "prompt_eval_count": 198,
            "eval_count": 10,
            "total_duration_ns": 627795900,
            "load_duration_ns": 380811900
          },
          "raw_content": "{\"answer\": \"M03-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.576869300002727,
            "prompt_eval_count": 202,
            "eval_count": 10,
            "total_duration_ns": 575733100,
            "load_duration_ns": 331043500
          },
          "raw_content": "{\"answer\": \"M03-C\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6645803000028536,
            "prompt_eval_count": 198,
            "eval_count": 10,
            "total_duration_ns": 662377800,
            "load_duration_ns": 420596400
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5846232000003511,
            "prompt_eval_count": 198,
            "eval_count": 10,
            "total_duration_ns": 572600900,
            "load_duration_ns": 358721200
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "E00-D",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-D",
        "repeat": "E00-D"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5965732999975444,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 594627400,
            "load_duration_ns": 305200400
          },
          "raw_content": "{\"answer\": \"E00-D\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6720529000012903,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 668774000,
            "load_duration_ns": 429949600
          },
          "raw_content": "{\"answer\": \"E00-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6321021999974619,
            "prompt_eval_count": 283,
            "eval_count": 10,
            "total_duration_ns": 629522100,
            "load_duration_ns": 356627100
          },
          "raw_content": "{\"answer\": \"E00-C\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6430221000009624,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 640913900,
            "load_duration_ns": 393553900
          },
          "raw_content": "{\"answer\": \"E00-D\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5295750999976008,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 527263200,
            "load_duration_ns": 315040500
          },
          "raw_content": "{\"answer\": \"E00-D\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "E01-D",
        "relevant": "E01-D",
        "irrelevant_plain": "E01-D",
        "irrelevant_adversarial": "E01-D",
        "repeat": "E01-D"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6262353999991319,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 610349200,
            "load_duration_ns": 331870900
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6294078999999329,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 627497700,
            "load_duration_ns": 364794200
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5921270999970147,
            "prompt_eval_count": 283,
            "eval_count": 10,
            "total_duration_ns": 572375500,
            "load_duration_ns": 307294900
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6210627000000386,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 599698800,
            "load_duration_ns": 366454600
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5780200000008335,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 572990600,
            "load_duration_ns": 355880400
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "E02-D",
        "relevant": "E02-D",
        "irrelevant_plain": "E02-D",
        "irrelevant_adversarial": "E02-D",
        "repeat": "E02-D"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.8102828000010049,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 806412200,
            "load_duration_ns": 512351800
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5780095000009169,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 574903800,
            "load_duration_ns": 308953000
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6564744999996037,
            "prompt_eval_count": 283,
            "eval_count": 10,
            "total_duration_ns": 655103200,
            "load_duration_ns": 375461900
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6044078999984777,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 602301300,
            "load_duration_ns": 361111800
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5387249999985215,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 536475900,
            "load_duration_ns": 314985600
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "E03-D",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-D",
        "irrelevant_adversarial": "E03-D",
        "repeat": "E03-D"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6394434000030742,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 633517600,
            "load_duration_ns": 357622300
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5837080999990576,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 579811300,
            "load_duration_ns": 303858400
          },
          "raw_content": "{\"answer\": \"E03-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6466418000018166,
            "prompt_eval_count": 283,
            "eval_count": 10,
            "total_duration_ns": 644899200,
            "load_duration_ns": 367279700
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6479423000018869,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 646927200,
            "load_duration_ns": 411700700
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.7862486000012723,
            "prompt_eval_count": 271,
            "eval_count": 10,
            "total_duration_ns": 777329500,
            "load_duration_ns": 570828200
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "strconv.ParseInt(",
        "relevant": "pathetic 143",
        "irrelevant_plain": "strconv.ParseInt(\"20+7+3\", 10, nil).Int64()}",
        "irrelevant_adversarial": "strconv.Itoa(20+7+3)}",
        "repeat": "strconv.ParseInt(\"143\", 10, nil)}"
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6805984999991779,
            "prompt_eval_count": 166,
            "eval_count": 11,
            "total_duration_ns": 678805700,
            "load_duration_ns": 327762400
          },
          "raw_content": "{\"answer\": \"strconv.ParseInt(\" }"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6340199000005668,
            "prompt_eval_count": 167,
            "eval_count": 12,
            "total_duration_ns": 613206400,
            "load_duration_ns": 332964700
          },
          "raw_content": "{\"answer\": \"pathetic 143\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.8681397000000288,
            "prompt_eval_count": 170,
            "eval_count": 27,
            "total_duration_ns": 866019900,
            "load_duration_ns": 328096200
          },
          "raw_content": "{\"answer\": \"strconv.ParseInt(\\\"20+7+3\\\", 10, nil).Int64()}\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.727861400002439,
            "prompt_eval_count": 167,
            "eval_count": 17,
            "total_duration_ns": 710021700,
            "load_duration_ns": 316959500
          },
          "raw_content": "{\"answer\": \"strconv.Itoa(20+7+3)}\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.8193678000025102,
            "prompt_eval_count": 166,
            "eval_count": 21,
            "total_duration_ns": 817927400,
            "load_duration_ns": 305965900
          },
          "raw_content": "{\"answer\": \"strconv.ParseInt(\\\"143\\\", 10, nil)}\" }"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": ":[19, 22, 14]}",
        "relevant": ":[19, 26, 14]}",
        "irrelevant_plain": ":[19, 22, 14]}",
        "irrelevant_adversarial": ":[19, 22, 14]}",
        "repeat": ":[19, 22, 14]}"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.8339852999997674,
            "prompt_eval_count": 167,
            "eval_count": 18,
            "total_duration_ns": 808657000,
            "load_duration_ns": 401715400
          },
          "raw_content": "{\"answer\": \":[19, 22, 14]}\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.8009984999989683,
            "prompt_eval_count": 167,
            "eval_count": 18,
            "total_duration_ns": 798175300,
            "load_duration_ns": 394015200
          },
          "raw_content": "{\"answer\": \":[19, 26, 14]}\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7787167000024056,
            "prompt_eval_count": 171,
            "eval_count": 18,
            "total_duration_ns": 776776900,
            "load_duration_ns": 380832100
          },
          "raw_content": "{\"answer\": \":[19, 22, 14]}\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7246827999988454,
            "prompt_eval_count": 168,
            "eval_count": 18,
            "total_duration_ns": 718167200,
            "load_duration_ns": 328149800
          },
          "raw_content": "{\"answer\": \":[19, 22, 14]}\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.7350994999978866,
            "prompt_eval_count": 167,
            "eval_count": 18,
            "total_duration_ns": 733350300,
            "load_duration_ns": 315260400
          },
          "raw_content": "{\"answer\": \":[19, 22, 14]}\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "33",
        "relevant": "]=39",
        "irrelevant_plain": "}{",
        "irrelevant_adversarial": "time",
        "repeat": "33"
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5549118000017188,
            "prompt_eval_count": 165,
            "eval_count": 9,
            "total_duration_ns": 553620500,
            "load_duration_ns": 333304600
          },
          "raw_content": "{\"answer\": \"33\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5382071999993059,
            "prompt_eval_count": 166,
            "eval_count": 9,
            "total_duration_ns": 535656200,
            "load_duration_ns": 319623600
          },
          "raw_content": "{\"answer\": \"]=39\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6612112000002526,
            "prompt_eval_count": 169,
            "eval_count": 8,
            "total_duration_ns": 650527900,
            "load_duration_ns": 385865400
          },
          "raw_content": "{\"answer\": \"}{\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6469195999998192,
            "prompt_eval_count": 167,
            "eval_count": 7,
            "total_duration_ns": 642397900,
            "load_duration_ns": 428597600
          },
          "raw_content": "{\"answer\": \"time\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5687665000004927,
            "prompt_eval_count": 165,
            "eval_count": 9,
            "total_duration_ns": 566153100,
            "load_duration_ns": 346477800
          },
          "raw_content": "{\"answer\": \"33\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "oset(11, 24, 2, 0)}",
        "relevant": "strconv.ParseInt(\"173\", 10, nil)}",
        "irrelevant_plain": "",
        "irrelevant_adversarial": "",
        "repeat": "oset(11, 24, 2, 0)}"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.9313909000011336,
            "prompt_eval_count": 167,
            "eval_count": 23,
            "total_duration_ns": 929350300,
            "load_duration_ns": 403780200
          },
          "raw_content": "{\"answer\": \"oset(11, 24, 2, 0)}\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.9604732999978296,
            "prompt_eval_count": 167,
            "eval_count": 21,
            "total_duration_ns": 956342800,
            "load_duration_ns": 422273500
          },
          "raw_content": "{\"answer\": \"strconv.ParseInt(\\\"173\\\", 10, nil)}\" }"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5212485000010929,
            "prompt_eval_count": 171,
            "eval_count": 7,
            "total_duration_ns": 519042200,
            "load_duration_ns": 320450600
          },
          "raw_content": "{\"answer\": \"\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5288400999997975,
            "prompt_eval_count": 168,
            "eval_count": 7,
            "total_duration_ns": 523411500,
            "load_duration_ns": 341468200
          },
          "raw_content": "{\"answer\": \"\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.8409546000002592,
            "prompt_eval_count": 167,
            "eval_count": 23,
            "total_duration_ns": 838781100,
            "load_duration_ns": 329156300
          },
          "raw_content": "{\"answer\": \"oset(11, 24, 2, 0)}\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": ".$_PHP_ECHO_",
        "relevant": "20",
        "irrelevant_plain": ":@",
        "irrelevant_adversarial": "",
        "repeat": ":@"
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6944914999985485,
            "prompt_eval_count": 128,
            "eval_count": 11,
            "total_duration_ns": 693381200,
            "load_duration_ns": 382953200
          },
          "raw_content": "{\"answer\": \".$_PHP_ECHO_\" }"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5675356000028842,
            "prompt_eval_count": 129,
            "eval_count": 9,
            "total_duration_ns": 566113600,
            "load_duration_ns": 360706700
          },
          "raw_content": "{\"answer\": \"20\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5271747999977379,
            "prompt_eval_count": 128,
            "eval_count": 7,
            "total_duration_ns": 524893400,
            "load_duration_ns": 325219600
          },
          "raw_content": "{\"answer\": \":@\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6156652000026952,
            "prompt_eval_count": 130,
            "eval_count": 7,
            "total_duration_ns": 612533300,
            "load_duration_ns": 433804500
          },
          "raw_content": "{\"answer\": \"\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5386758999993617,
            "prompt_eval_count": 128,
            "eval_count": 7,
            "total_duration_ns": 535302400,
            "load_duration_ns": 346047800
          },
          "raw_content": "{\"answer\": \":@\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "sync",
        "relevant": ",__int__():13+20} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回一个整数。正确的回答应该是 {",
        "irrelevant_plain": "sync",
        "irrelevant_adversarial": "log(128, 2)}",
        "repeat": "sync"
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.534849600000598,
            "prompt_eval_count": 129,
            "eval_count": 7,
            "total_duration_ns": 532793500,
            "load_duration_ns": 363012400
          },
          "raw_content": "{\"answer\": \"sync\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 1.1260111999981746,
            "prompt_eval_count": 130,
            "eval_count": 37,
            "total_duration_ns": 1123012000,
            "load_duration_ns": 310208800
          },
          "raw_content": "{\"answer\": \",__int__():13+20} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回一个整数。正确的回答应该是 {\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5642881000021589,
            "prompt_eval_count": 129,
            "eval_count": 7,
            "total_duration_ns": 561411700,
            "load_duration_ns": 384947700
          },
          "raw_content": "{\"answer\": \"sync\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7870605999996769,
            "prompt_eval_count": 131,
            "eval_count": 16,
            "total_duration_ns": 761191900,
            "load_duration_ns": 397708500
          },
          "raw_content": "{\"answer\": \"log(128, 2)}\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.48379080000086105,
            "prompt_eval_count": 129,
            "eval_count": 7,
            "total_duration_ns": 481813400,
            "load_duration_ns": 304886600
          },
          "raw_content": "{\"answer\": \"sync\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "sync",
        "relevant": "crypto_score",
        "irrelevant_plain": "sync",
        "irrelevant_adversarial": "sync",
        "repeat": "sync"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.519997899998998,
            "prompt_eval_count": 129,
            "eval_count": 7,
            "total_duration_ns": 517900500,
            "load_duration_ns": 345128200
          },
          "raw_content": "{\"answer\": \"sync\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5977120999996259,
            "prompt_eval_count": 130,
            "eval_count": 8,
            "total_duration_ns": 595001300,
            "load_duration_ns": 400331100
          },
          "raw_content": "{\"answer\": \"crypto_score\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6278401000017766,
            "prompt_eval_count": 129,
            "eval_count": 7,
            "total_duration_ns": 623999300,
            "load_duration_ns": 461998000
          },
          "raw_content": "{\"answer\": \"sync\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5761528999973962,
            "prompt_eval_count": 131,
            "eval_count": 7,
            "total_duration_ns": 574663600,
            "load_duration_ns": 395500000
          },
          "raw_content": "{\"answer\": \"sync\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5261594000003242,
            "prompt_eval_count": 129,
            "eval_count": 7,
            "total_duration_ns": 524909000,
            "load_duration_ns": 341493000
          },
          "raw_content": "{\"answer\": \"sync\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": ",__int__():11} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即11。但由于格式要求，只能这样展示。正确的JSON回答应该是{",
        "relevant": "os",
        "irrelevant_plain": ",__int__():11} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即11。但由于格式要求，只能这样展示。正确的JSON回答应该是{",
        "irrelevant_adversarial": "crypto_score",
        "repeat": ",__int__():11} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即11。但由于格式要求，只能这样展示。正确的JSON回答应该是{"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 1.534490400001232,
            "prompt_eval_count": 131,
            "eval_count": 48,
            "total_duration_ns": 1513910300,
            "load_duration_ns": 391525300
          },
          "raw_content": "{\"answer\": \",__int__():11} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即11。但由于格式要求，只能这样展示。正确的JSON回答应该是{\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.523815000000468,
            "prompt_eval_count": 131,
            "eval_count": 7,
            "total_duration_ns": 521761000,
            "load_duration_ns": 331333500
          },
          "raw_content": "{\"answer\": \"os\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 1.439307499997085,
            "prompt_eval_count": 131,
            "eval_count": 48,
            "total_duration_ns": 1437522500,
            "load_duration_ns": 320693600
          },
          "raw_content": "{\"answer\": \",__int__():11} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即11。但由于格式要求，只能这样展示。正确的JSON回答应该是{\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.73287049999999,
            "prompt_eval_count": 132,
            "eval_count": 8,
            "total_duration_ns": 730838300,
            "load_duration_ns": 518129000
          },
          "raw_content": "{\"answer\": \"crypto_score\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 1.5203607999974338,
            "prompt_eval_count": 131,
            "eval_count": 48,
            "total_duration_ns": 1517669000,
            "load_duration_ns": 431917100
          },
          "raw_content": "{\"answer\": \",__int__():11} 注意：这里的回答格式不符合要求，正确的回答应该是直接返回routing_score的值，即11。但由于格式要求，只能这样展示。正确的JSON回答应该是{\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "./2",
        "relevant": "+",
        "irrelevant_plain": "./2",
        "irrelevant_adversarial": "./2",
        "repeat": "./2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6014872999985528,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 598753200,
            "load_duration_ns": 339591700
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5795832000003429,
            "prompt_eval_count": 209,
            "eval_count": 7,
            "total_duration_ns": 577715500,
            "load_duration_ns": 378645700
          },
          "raw_content": "{\"answer\": \"+\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5742156999986037,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 572895800,
            "load_duration_ns": 344282800
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5930903000007675,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 570271200,
            "load_duration_ns": 335318100
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5394756000023335,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 536739600,
            "load_duration_ns": 329620300
          },
          "raw_content": "{\"answer\": \"./2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "./2",
        "relevant": "+",
        "irrelevant_plain": "./2",
        "irrelevant_adversarial": "./2",
        "repeat": "./2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5892595000004803,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 586329500,
            "load_duration_ns": 346117400
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6449534999992466,
            "prompt_eval_count": 209,
            "eval_count": 7,
            "total_duration_ns": 617841400,
            "load_duration_ns": 407164000
          },
          "raw_content": "{\"answer\": \"+\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6501152999990154,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 647783900,
            "load_duration_ns": 403823400
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6117048999985855,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 610459000,
            "load_duration_ns": 378682100
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5587440999988758,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 552864100,
            "load_duration_ns": 354908700
          },
          "raw_content": "{\"answer\": \"./2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "./2",
        "relevant": "+",
        "irrelevant_plain": "./2",
        "irrelevant_adversarial": "./2",
        "repeat": "./2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6407809000011184,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 639050800,
            "load_duration_ns": 386809600
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5044510999978229,
            "prompt_eval_count": 209,
            "eval_count": 7,
            "total_duration_ns": 501511900,
            "load_duration_ns": 304231400
          },
          "raw_content": "{\"answer\": \"+\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6408222999998543,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 638785400,
            "load_duration_ns": 387019300
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7362595999984478,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 714871100,
            "load_duration_ns": 489915500
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5589973000023747,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 558209200,
            "load_duration_ns": 358681500
          },
          "raw_content": "{\"answer\": \"./2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "ollama::qwen2.5:7b::weak",
      "backend": "ollama",
      "answers": {
        "base": "./2",
        "relevant": ",__int__():3}__int__是一个Python内置方法，用于将对象转换为整数。在这个场景中，答案是3，表示status等于open的records数量。为了符合要求，返回一个包含答案的JSON对象，并使用Python的内置方法__int__来表示整数3。注意，这里的表示方法是为了适应特定格式要求，实际答案应为3。正确的JSON对象应为{",
        "irrelevant_plain": "./2",
        "irrelevant_adversarial": "./2",
        "repeat": "./2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5458882000020822,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 544197300,
            "load_duration_ns": 298723300
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 2.782490699999471,
            "prompt_eval_count": 209,
            "eval_count": 93,
            "total_duration_ns": 2779449600,
            "load_duration_ns": 636377400
          },
          "raw_content": "{\"answer\": \",__int__():3}__int__是一个Python内置方法，用于将对象转换为整数。在这个场景中，答案是3，表示status等于open的records数量。为了符合要求，返回一个包含答案的JSON对象，并使用Python的内置方法__int__来表示整数3。注意，这里的表示方法是为了适应特定格式要求，实际答案应为3。正确的JSON对象应为{\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5678613999989466,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 563200800,
            "load_duration_ns": 325682500
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5586565000012342,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 554985900,
            "load_duration_ns": 323009100
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5064698999995016,
            "prompt_eval_count": 209,
            "eval_count": 8,
            "total_duration_ns": 503767600,
            "load_duration_ns": 311956400
          },
          "raw_content": "{\"answer\": \"./2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A",
        "repeat": "M00-A"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5950661000024411,
            "prompt_eval_count": 234,
            "eval_count": 10,
            "total_duration_ns": 593813000,
            "load_duration_ns": 310494100
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6612118999983068,
            "prompt_eval_count": 234,
            "eval_count": 10,
            "total_duration_ns": 639936900,
            "load_duration_ns": 380361900
          },
          "raw_content": "{\"answer\": \"M00-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6875502999973833,
            "prompt_eval_count": 238,
            "eval_count": 10,
            "total_duration_ns": 685250000,
            "load_duration_ns": 430953300
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5932058000034885,
            "prompt_eval_count": 234,
            "eval_count": 10,
            "total_duration_ns": 591527500,
            "load_duration_ns": 366013300
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5454131000005873,
            "prompt_eval_count": 234,
            "eval_count": 10,
            "total_duration_ns": 543927500,
            "load_duration_ns": 329602700
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A",
        "repeat": "M01-A"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6053064999978233,
            "prompt_eval_count": 237,
            "eval_count": 10,
            "total_duration_ns": 602902100,
            "load_duration_ns": 339154100
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5718034000019543,
            "prompt_eval_count": 237,
            "eval_count": 10,
            "total_duration_ns": 570234200,
            "load_duration_ns": 323640600
          },
          "raw_content": "{\"answer\": \"M01-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6915585999995528,
            "prompt_eval_count": 241,
            "eval_count": 10,
            "total_duration_ns": 690255600,
            "load_duration_ns": 441206300
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5794726999993145,
            "prompt_eval_count": 237,
            "eval_count": 10,
            "total_duration_ns": 578348000,
            "load_duration_ns": 348157000
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6287518999997701,
            "prompt_eval_count": 237,
            "eval_count": 10,
            "total_duration_ns": 606424600,
            "load_duration_ns": 397751100
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A",
        "repeat": "M02-A"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5526282999999239,
            "prompt_eval_count": 235,
            "eval_count": 10,
            "total_duration_ns": 549669800,
            "load_duration_ns": 305654800
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6395988000003854,
            "prompt_eval_count": 235,
            "eval_count": 10,
            "total_duration_ns": 637912500,
            "load_duration_ns": 396159400
          },
          "raw_content": "{\"answer\": \"M02-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6107402999987244,
            "prompt_eval_count": 239,
            "eval_count": 10,
            "total_duration_ns": 608677600,
            "load_duration_ns": 357533900
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5650396999990335,
            "prompt_eval_count": 235,
            "eval_count": 10,
            "total_duration_ns": 563045400,
            "load_duration_ns": 333377300
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5755433999984234,
            "prompt_eval_count": 235,
            "eval_count": 10,
            "total_duration_ns": 574252600,
            "load_duration_ns": 366089100
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A",
        "repeat": "M03-A"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5545445999996446,
            "prompt_eval_count": 237,
            "eval_count": 10,
            "total_duration_ns": 553468000,
            "load_duration_ns": 324860100
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6313829000027908,
            "prompt_eval_count": 237,
            "eval_count": 10,
            "total_duration_ns": 629787200,
            "load_duration_ns": 409836900
          },
          "raw_content": "{\"answer\": \"M03-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5801318000012543,
            "prompt_eval_count": 241,
            "eval_count": 10,
            "total_duration_ns": 578497300,
            "load_duration_ns": 339677900
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6423098999985086,
            "prompt_eval_count": 237,
            "eval_count": 10,
            "total_duration_ns": 629670800,
            "load_duration_ns": 397734300
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.572566499999084,
            "prompt_eval_count": 237,
            "eval_count": 10,
            "total_duration_ns": 570675100,
            "load_duration_ns": 363391000
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C",
        "repeat": "E00-C"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.9005022999990615,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 898624200,
            "load_duration_ns": 609332000
          },
          "raw_content": "{\"answer\": \"E00-C\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6017881000007037,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 598884100,
            "load_duration_ns": 342823000
          },
          "raw_content": "{\"answer\": \"E00-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6160406000017247,
            "prompt_eval_count": 322,
            "eval_count": 10,
            "total_duration_ns": 614388100,
            "load_duration_ns": 356906900
          },
          "raw_content": "{\"answer\": \"E00-C\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5784146999976656,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 576408600,
            "load_duration_ns": 352850100
          },
          "raw_content": "{\"answer\": \"E00-C\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5858044999986305,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 583934600,
            "load_duration_ns": 385515300
          },
          "raw_content": "{\"answer\": \"E00-C\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C",
        "repeat": "E01-C"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5992393000014999,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 596585200,
            "load_duration_ns": 333185800
          },
          "raw_content": "{\"answer\": \"E01-C\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5876556999974127,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 586046000,
            "load_duration_ns": 339063100
          },
          "raw_content": "{\"answer\": \"E01-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.580031900000904,
            "prompt_eval_count": 322,
            "eval_count": 10,
            "total_duration_ns": 574855400,
            "load_duration_ns": 315147600
          },
          "raw_content": "{\"answer\": \"E01-C\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5592648000019835,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 555166500,
            "load_duration_ns": 342901800
          },
          "raw_content": "{\"answer\": \"E01-C\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5261819999977888,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 524282800,
            "load_duration_ns": 316384500
          },
          "raw_content": "{\"answer\": \"E01-C\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C",
        "repeat": "E02-C"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7633209000014176,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 761331400,
            "load_duration_ns": 488511700
          },
          "raw_content": "{\"answer\": \"E02-C\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5872930000004999,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 583250500,
            "load_duration_ns": 330058300
          },
          "raw_content": "{\"answer\": \"E02-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6380896999980905,
            "prompt_eval_count": 322,
            "eval_count": 10,
            "total_duration_ns": 629336500,
            "load_duration_ns": 359813300
          },
          "raw_content": "{\"answer\": \"E02-C\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5855725999972492,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 583724800,
            "load_duration_ns": 354336100
          },
          "raw_content": "{\"answer\": \"E02-C\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5879429999986314,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 564727800,
            "load_duration_ns": 361583900
          },
          "raw_content": "{\"answer\": \"E02-C\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C",
        "repeat": "E03-C"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6093037999999069,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 581715400,
            "load_duration_ns": 313463000
          },
          "raw_content": "{\"answer\": \"E03-C\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5595288000004075,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 557217100,
            "load_duration_ns": 306638000
          },
          "raw_content": "{\"answer\": \"E03-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6476044000010006,
            "prompt_eval_count": 322,
            "eval_count": 10,
            "total_duration_ns": 629817200,
            "load_duration_ns": 366469100
          },
          "raw_content": "{\"answer\": \"E03-C\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5384639000003517,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 536884200,
            "load_duration_ns": 309848100
          },
          "raw_content": "{\"answer\": \"E03-C\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6732225000014296,
            "prompt_eval_count": 310,
            "eval_count": 10,
            "total_duration_ns": 670664100,
            "load_duration_ns": 461051600
          },
          "raw_content": "{\"answer\": \"E03-C\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "strconv.ParseInt(",
        "relevant": "].",
        "irrelevant_plain": "strconv.ParseInt(",
        "irrelevant_adversarial": "strconv.ParseInt(",
        "repeat": "strconv.ParseInt("
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.674784599999839,
            "prompt_eval_count": 205,
            "eval_count": 11,
            "total_duration_ns": 672423800,
            "load_duration_ns": 326747700
          },
          "raw_content": "{\"answer\": \"strconv.ParseInt(\" }"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5291204000022844,
            "prompt_eval_count": 206,
            "eval_count": 7,
            "total_duration_ns": 527766800,
            "load_duration_ns": 323975700
          },
          "raw_content": "{\"answer\": \"].\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6922678999981144,
            "prompt_eval_count": 209,
            "eval_count": 11,
            "total_duration_ns": 689519600,
            "load_duration_ns": 367488300
          },
          "raw_content": "{\"answer\": \"strconv.ParseInt(\" }"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6640240000015183,
            "prompt_eval_count": 206,
            "eval_count": 11,
            "total_duration_ns": 661727700,
            "load_duration_ns": 341714100
          },
          "raw_content": "{\"answer\": \"strconv.ParseInt(\" }"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6393901000010374,
            "prompt_eval_count": 205,
            "eval_count": 11,
            "total_duration_ns": 637810700,
            "load_duration_ns": 343027400
          },
          "raw_content": "{\"answer\": \"strconv.ParseInt(\" }"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": ":[19, 22, 14].sum()} {",
        "relevant": ":[19, 26, 14].sum()} {",
        "irrelevant_plain": ":[19, 22, 14]}",
        "irrelevant_adversarial": ":[19, 22, 14].sum()} {",
        "repeat": ":[19, 22, 14].sum()} {"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.908341799997288,
            "prompt_eval_count": 206,
            "eval_count": 21,
            "total_duration_ns": 906704700,
            "load_duration_ns": 377861700
          },
          "raw_content": "{\"answer\": \":[19, 22, 14].sum()} {\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.9867864000007103,
            "prompt_eval_count": 206,
            "eval_count": 21,
            "total_duration_ns": 983562400,
            "load_duration_ns": 431024700
          },
          "raw_content": "{\"answer\": \":[19, 26, 14].sum()} {\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.8282715999994252,
            "prompt_eval_count": 210,
            "eval_count": 18,
            "total_duration_ns": 825912700,
            "load_duration_ns": 433417500
          },
          "raw_content": "{\"answer\": \":[19, 22, 14]}\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.8760992999996233,
            "prompt_eval_count": 207,
            "eval_count": 21,
            "total_duration_ns": 874298700,
            "load_duration_ns": 325378000
          },
          "raw_content": "{\"answer\": \":[19, 22, 14].sum()} {\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.8673285999975633,
            "prompt_eval_count": 206,
            "eval_count": 21,
            "total_duration_ns": 866005500,
            "load_duration_ns": 348398200
          },
          "raw_content": "{\"answer\": \":[19, 22, 14].sum()} {\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "time",
        "relevant": "]=39",
        "irrelevant_plain": "]=33",
        "irrelevant_adversarial": "time",
        "repeat": "It is not possible to calculate the sum of 'amount' for valid rows as the provided data does not contain any valid rows."
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5109666000025754,
            "prompt_eval_count": 204,
            "eval_count": 7,
            "total_duration_ns": 509580400,
            "load_duration_ns": 335320800
          },
          "raw_content": "{\"answer\": \"time\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6130554000010306,
            "prompt_eval_count": 205,
            "eval_count": 9,
            "total_duration_ns": 611473300,
            "load_duration_ns": 399178000
          },
          "raw_content": "{\"answer\": \"]=39\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5872294000000693,
            "prompt_eval_count": 208,
            "eval_count": 9,
            "total_duration_ns": 561759900,
            "load_duration_ns": 350836800
          },
          "raw_content": "{\"answer\": \"]=33\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.4862013999991177,
            "prompt_eval_count": 206,
            "eval_count": 7,
            "total_duration_ns": 484340100,
            "load_duration_ns": 307508800
          },
          "raw_content": "{\"answer\": \"time\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 1.0067677999977604,
            "prompt_eval_count": 204,
            "eval_count": 32,
            "total_duration_ns": 1002760700,
            "load_duration_ns": 415463400
          },
          "raw_content": "{\"answer\": \"It is not possible to calculate the sum of 'amount' for valid rows as the provided data does not contain any valid rows.\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "osetka: 37",
        "relevant": "strconv.ParseInt(",
        "irrelevant_plain": "oset(11, 24, 2, 173).",
        "irrelevant_adversarial": "strconv.ParseInt(",
        "repeat": "osetka: 37"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6493046999967191,
            "prompt_eval_count": 206,
            "eval_count": 13,
            "total_duration_ns": 647765000,
            "load_duration_ns": 359309500
          },
          "raw_content": "{\"answer\": \"osetka: 37\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6527358000021195,
            "prompt_eval_count": 206,
            "eval_count": 11,
            "total_duration_ns": 651627000,
            "load_duration_ns": 349658500
          },
          "raw_content": "{\"answer\": \"strconv.ParseInt(\" }"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.8472983999999997,
            "prompt_eval_count": 210,
            "eval_count": 24,
            "total_duration_ns": 843776100,
            "load_duration_ns": 375948000
          },
          "raw_content": "{\"answer\": \"oset(11, 24, 2, 173).\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6889999000013631,
            "prompt_eval_count": 207,
            "eval_count": 11,
            "total_duration_ns": 686222300,
            "load_duration_ns": 380032700
          },
          "raw_content": "{\"answer\": \"strconv.ParseInt(\" }"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6611950000005891,
            "prompt_eval_count": 206,
            "eval_count": 13,
            "total_duration_ns": 639174800,
            "load_duration_ns": 376280500
          },
          "raw_content": "{\"answer\": \"osetka: 37\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "srouting_score",
        "relevant": "20",
        "irrelevant_plain": "s",
        "irrelevant_adversarial": "",
        "repeat": "srouting_score"
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6847798000017065,
            "prompt_eval_count": 167,
            "eval_count": 9,
            "total_duration_ns": 683523800,
            "load_duration_ns": 408321000
          },
          "raw_content": "{\"answer\": \"srouting_score\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5536132999986876,
            "prompt_eval_count": 168,
            "eval_count": 9,
            "total_duration_ns": 528827400,
            "load_duration_ns": 321443600
          },
          "raw_content": "{\"answer\": \"20\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6102920999983326,
            "prompt_eval_count": 167,
            "eval_count": 7,
            "total_duration_ns": 603766600,
            "load_duration_ns": 429776000
          },
          "raw_content": "{\"answer\": \"s\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5640500999979849,
            "prompt_eval_count": 169,
            "eval_count": 7,
            "total_duration_ns": 562225600,
            "load_duration_ns": 368793500
          },
          "raw_content": "{\"answer\": \"\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.7252434000001813,
            "prompt_eval_count": 167,
            "eval_count": 9,
            "total_duration_ns": 706906900,
            "load_duration_ns": 437407200
          },
          "raw_content": "{\"answer\": \"srouting_score\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "sync",
        "relevant": "github.com/google/go-github/v43/github",
        "irrelevant_plain": "sync",
        "irrelevant_adversarial": "log(128, 10)}",
        "repeat": "sync"
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5208940000011353,
            "prompt_eval_count": 168,
            "eval_count": 7,
            "total_duration_ns": 519381700,
            "load_duration_ns": 354946500
          },
          "raw_content": "{\"answer\": \"sync\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6649904000005336,
            "prompt_eval_count": 169,
            "eval_count": 16,
            "total_duration_ns": 661829900,
            "load_duration_ns": 338358400
          },
          "raw_content": "{\"answer\": \"github.com/google/go-github/v43/github\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6002889000010327,
            "prompt_eval_count": 168,
            "eval_count": 7,
            "total_duration_ns": 598349800,
            "load_duration_ns": 420985100
          },
          "raw_content": "{\"answer\": \"sync\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7549755000000005,
            "prompt_eval_count": 170,
            "eval_count": 17,
            "total_duration_ns": 753044000,
            "load_duration_ns": 322088400
          },
          "raw_content": "{\"answer\": \"log(128, 10)}\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.47833039999750326,
            "prompt_eval_count": 168,
            "eval_count": 7,
            "total_duration_ns": 476510500,
            "load_duration_ns": 308838900
          },
          "raw_content": "{\"answer\": \"sync\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "sync",
        "relevant": "crypto",
        "irrelevant_plain": "sync",
        "irrelevant_adversarial": "sync",
        "repeat": "sync"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.4835392999993928,
            "prompt_eval_count": 168,
            "eval_count": 7,
            "total_duration_ns": 481964500,
            "load_duration_ns": 314445200
          },
          "raw_content": "{\"answer\": \"sync\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6345164000013028,
            "prompt_eval_count": 169,
            "eval_count": 7,
            "total_duration_ns": 632513500,
            "load_duration_ns": 459017800
          },
          "raw_content": "{\"answer\": \"crypto\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6266432999982499,
            "prompt_eval_count": 168,
            "eval_count": 7,
            "total_duration_ns": 621064900,
            "load_duration_ns": 449313000
          },
          "raw_content": "{\"answer\": \"sync\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.4871922000020277,
            "prompt_eval_count": 170,
            "eval_count": 7,
            "total_duration_ns": 481104900,
            "load_duration_ns": 315828300
          },
          "raw_content": "{\"answer\": \"sync\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.49985600000218255,
            "prompt_eval_count": 168,
            "eval_count": 7,
            "total_duration_ns": 498448600,
            "load_duration_ns": 317998700
          },
          "raw_content": "{\"answer\": \"sync\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": ",__int__}21__",
        "relevant": "strconv.ParseInt(",
        "irrelevant_plain": ",__int__}21__",
        "irrelevant_adversarial": "github.com/google/go-github/v43/github",
        "repeat": ",__int__}21__"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7362489000006462,
            "prompt_eval_count": 170,
            "eval_count": 13,
            "total_duration_ns": 719829000,
            "load_duration_ns": 386308900
          },
          "raw_content": "{\"answer\": \",__int__}21__\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7304967999989458,
            "prompt_eval_count": 170,
            "eval_count": 11,
            "total_duration_ns": 728366600,
            "load_duration_ns": 377225900
          },
          "raw_content": "{\"answer\": \"strconv.ParseInt(\" }"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7551057999990007,
            "prompt_eval_count": 170,
            "eval_count": 13,
            "total_duration_ns": 753294700,
            "load_duration_ns": 388371800
          },
          "raw_content": "{\"answer\": \",__int__}21__\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.824510200000077,
            "prompt_eval_count": 171,
            "eval_count": 16,
            "total_duration_ns": 822028500,
            "load_duration_ns": 462285100
          },
          "raw_content": "{\"answer\": \"github.com/google/go-github/v43/github\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.673815400001331,
            "prompt_eval_count": 170,
            "eval_count": 13,
            "total_duration_ns": 672075000,
            "load_duration_ns": 309114400
          },
          "raw_content": "{\"answer\": \",__int__}21__\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "./2",
        "relevant": "{\"answer\": \",__int__()}1003__int__()}002__int__()}001__int__()}000__int__()}002__int__()}002__int__()}002__int__()}002__int__()}002__int__()}002__int__()}002__int__()}002__int__()}002",
        "irrelevant_plain": "./2",
        "irrelevant_adversarial": "./2",
        "repeat": "./2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.623380900000484,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 594617600,
            "load_duration_ns": 352437700
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 2.7631160999990243,
            "prompt_eval_count": 248,
            "eval_count": 96,
            "total_duration_ns": 2760801500,
            "load_duration_ns": 385683700
          },
          "raw_content": "{\"answer\": \",__int__()}1003__int__()}002__int__()}001__int__()}000__int__()}002__int__()}002__int__()}002__int__()}002__int__()}002__int__()}002__int__()}002__int__()}002__int__()}002"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5476899999994203,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 546077900,
            "load_duration_ns": 317988100
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7460643999984313,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 743523100,
            "load_duration_ns": 526394400
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5198991999968712,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 518528800,
            "load_duration_ns": 327007200
          },
          "raw_content": "{\"answer\": \"./2\"}"
        }
      ],
      "warnings": [
        "relevant: response was not a JSON object with an answer key"
      ],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "./2",
        "relevant": "+",
        "irrelevant_plain": "./2",
        "irrelevant_adversarial": "./2",
        "repeat": "./2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7417607999996108,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 740273500,
            "load_duration_ns": 496484800
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.589755699998932,
            "prompt_eval_count": 248,
            "eval_count": 7,
            "total_duration_ns": 586856600,
            "load_duration_ns": 383141000
          },
          "raw_content": "{\"answer\": \"+\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5862005000017234,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 585071100,
            "load_duration_ns": 365914400
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.520196900000883,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 517285900,
            "load_duration_ns": 296112000
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6152368999973987,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 613089900,
            "load_duration_ns": 411719800
          },
          "raw_content": "{\"answer\": \"./2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "./2",
        "relevant": "{\"answer\": \",__int__()}1003__int__()}002__int__()}001__int__()}000__int__()}002__int__()}000__int__()}000__int__()}000__int__()}000__int__()}000__int__()}000__int__()}000__int__()}000",
        "irrelevant_plain": "./2",
        "irrelevant_adversarial": "./2",
        "repeat": "./2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5767517999993288,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 574360300,
            "load_duration_ns": 325247500
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 2.8167166000021098,
            "prompt_eval_count": 248,
            "eval_count": 96,
            "total_duration_ns": 2814276100,
            "load_duration_ns": 425478900
          },
          "raw_content": "{\"answer\": \",__int__()}1003__int__()}002__int__()}001__int__()}000__int__()}002__int__()}000__int__()}000__int__()}000__int__()}000__int__()}000__int__()}000__int__()}000__int__()}000"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5755002999976568,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 573751800,
            "load_duration_ns": 351484700
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5219191000032879,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 518778900,
            "load_duration_ns": 311398900
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.584162600000127,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 582714000,
            "load_duration_ns": 387439800
          },
          "raw_content": "{\"answer\": \"./2\"}"
        }
      ],
      "warnings": [
        "relevant: response was not a JSON object with an answer key"
      ],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "ollama::qwen2.5:7b::strict",
      "backend": "ollama",
      "answers": {
        "base": "./2",
        "relevant": ",__int__()}1003__int__()}1002__int__()}1001__int__()}1000__int__()}1000}{",
        "irrelevant_plain": "./2",
        "irrelevant_adversarial": "./2",
        "repeat": "./2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5407448000005388,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 539197800,
            "load_duration_ns": 303854100
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 1.6830097000020032,
            "prompt_eval_count": 248,
            "eval_count": 48,
            "total_duration_ns": 1680431000,
            "load_duration_ns": 380131000
          },
          "raw_content": "{\"answer\": \",__int__()}1003__int__()}1002__int__()}1001__int__()}1000__int__()}1000}{\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5287452000011399,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 527167100,
            "load_duration_ns": 305003000
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5696567999984836,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 568066200,
            "load_duration_ns": 352177400
          },
          "raw_content": "{\"answer\": \"./2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6437867999993614,
            "prompt_eval_count": 248,
            "eval_count": 8,
            "total_duration_ns": 641749700,
            "load_duration_ns": 421522800
          },
          "raw_content": "{\"answer\": \"./2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-C",
        "irrelevant_adversarial": "M00-A",
        "repeat": "M00-A"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 5.754181599997537,
            "prompt_eval_count": 197,
            "eval_count": 13,
            "total_duration_ns": 5752491600,
            "load_duration_ns": 5357588700
          },
          "raw_content": "{\n  \"answer\": \"M00-A\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6422850999988441,
            "prompt_eval_count": 197,
            "eval_count": 13,
            "total_duration_ns": 640446400,
            "load_duration_ns": 344490000
          },
          "raw_content": "{\n  \"answer\": \"M00-B\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7566394999994372,
            "prompt_eval_count": 201,
            "eval_count": 13,
            "total_duration_ns": 755351900,
            "load_duration_ns": 454408000
          },
          "raw_content": "{\n  \"answer\": \"M00-C\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6747374999977183,
            "prompt_eval_count": 197,
            "eval_count": 13,
            "total_duration_ns": 672961500,
            "load_duration_ns": 392050900
          },
          "raw_content": "{\n  \"answer\": \"M00-A\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6790609999989101,
            "prompt_eval_count": 197,
            "eval_count": 13,
            "total_duration_ns": 676795800,
            "load_duration_ns": 422160900
          },
          "raw_content": "{\n  \"answer\": \"M00-A\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "M01-C",
        "relevant": "M01-C",
        "irrelevant_plain": "M01-C",
        "irrelevant_adversarial": "M01-C",
        "repeat": "M01-C"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6378175999998348,
            "prompt_eval_count": 200,
            "eval_count": 13,
            "total_duration_ns": 624006100,
            "load_duration_ns": 320948600
          },
          "raw_content": "{\n  \"answer\": \"M01-C\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6170769999989716,
            "prompt_eval_count": 200,
            "eval_count": 13,
            "total_duration_ns": 614830000,
            "load_duration_ns": 329422300
          },
          "raw_content": "{\n  \"answer\": \"M01-C\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.620759099998395,
            "prompt_eval_count": 204,
            "eval_count": 13,
            "total_duration_ns": 619040000,
            "load_duration_ns": 307668400
          },
          "raw_content": "{\n  \"answer\": \"M01-C\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7067922999995062,
            "prompt_eval_count": 200,
            "eval_count": 13,
            "total_duration_ns": 704149300,
            "load_duration_ns": 414999600
          },
          "raw_content": "{\n  \"answer\": \"M01-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6429124000023876,
            "prompt_eval_count": 200,
            "eval_count": 13,
            "total_duration_ns": 639771800,
            "load_duration_ns": 401740000
          },
          "raw_content": "{\n  \"answer\": \"M01-C\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-C",
        "irrelevant_adversarial": "M02-C",
        "repeat": "M02-A"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6828573999991931,
            "prompt_eval_count": 198,
            "eval_count": 13,
            "total_duration_ns": 680209300,
            "load_duration_ns": 405187600
          },
          "raw_content": "{\n  \"answer\": \"M02-A\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6111319999981788,
            "prompt_eval_count": 198,
            "eval_count": 13,
            "total_duration_ns": 609338700,
            "load_duration_ns": 319173900
          },
          "raw_content": "{\n  \"answer\": \"M02-B\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6656589999984135,
            "prompt_eval_count": 202,
            "eval_count": 13,
            "total_duration_ns": 664117200,
            "load_duration_ns": 365457900
          },
          "raw_content": "{\n  \"answer\": \"M02-C\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6925606999975571,
            "prompt_eval_count": 198,
            "eval_count": 13,
            "total_duration_ns": 689428800,
            "load_duration_ns": 406526100
          },
          "raw_content": "{\n  \"answer\": \"M02-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6736091999991913,
            "prompt_eval_count": 198,
            "eval_count": 13,
            "total_duration_ns": 645928900,
            "load_duration_ns": 395454700
          },
          "raw_content": "{\n  \"answer\": \"M02-A\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A",
        "repeat": "M03-A"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5892824000002292,
            "prompt_eval_count": 200,
            "eval_count": 13,
            "total_duration_ns": 587142700,
            "load_duration_ns": 304632600
          },
          "raw_content": "{\n  \"answer\": \"M03-A\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7268430000003718,
            "prompt_eval_count": 200,
            "eval_count": 13,
            "total_duration_ns": 724509600,
            "load_duration_ns": 435888400
          },
          "raw_content": "{\n  \"answer\": \"M03-B\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6807297999985167,
            "prompt_eval_count": 204,
            "eval_count": 13,
            "total_duration_ns": 677662700,
            "load_duration_ns": 395836100
          },
          "raw_content": "{\n  \"answer\": \"M03-A\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6173643000001903,
            "prompt_eval_count": 200,
            "eval_count": 13,
            "total_duration_ns": 616081300,
            "load_duration_ns": 352454900
          },
          "raw_content": "{\n  \"answer\": \"M03-A\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5658489999987069,
            "prompt_eval_count": 200,
            "eval_count": 13,
            "total_duration_ns": 563138500,
            "load_duration_ns": 316504600
          },
          "raw_content": "{\n  \"answer\": \"M03-A\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-B",
        "irrelevant_adversarial": "E00-C",
        "repeat": "E00-C"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6350040999968769,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 633951600,
            "load_duration_ns": 321602400
          },
          "raw_content": "{\n  \"answer\": \"E00-C\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6739627999995719,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 672234400,
            "load_duration_ns": 377728600
          },
          "raw_content": "{\n  \"answer\": \"E00-B\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6220885000002454,
            "prompt_eval_count": 285,
            "eval_count": 13,
            "total_duration_ns": 619544500,
            "load_duration_ns": 315616800
          },
          "raw_content": "{\n  \"answer\": \"E00-B\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5945524999988265,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 593699500,
            "load_duration_ns": 307391000
          },
          "raw_content": "{\n  \"answer\": \"E00-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5701836000007461,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 568962700,
            "load_duration_ns": 308165700
          },
          "raw_content": "{\n  \"answer\": \"E00-C\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "E01-C",
        "relevant": "E01-C",
        "irrelevant_plain": "E01-B",
        "irrelevant_adversarial": "E01-C",
        "repeat": "E01-C"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.772307200000796,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 770105300,
            "load_duration_ns": 435113600
          },
          "raw_content": "{\n  \"answer\": \"E01-C\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6715522000013152,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 667644500,
            "load_duration_ns": 373245000
          },
          "raw_content": "{\n  \"answer\": \"E01-C\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6567174000010709,
            "prompt_eval_count": 285,
            "eval_count": 13,
            "total_duration_ns": 654813100,
            "load_duration_ns": 359360600
          },
          "raw_content": "{\n  \"answer\": \"E01-B\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6012758999968355,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 598264000,
            "load_duration_ns": 319777800
          },
          "raw_content": "{\n  \"answer\": \"E01-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6245208000000275,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 615466300,
            "load_duration_ns": 369653800
          },
          "raw_content": "{\n  \"answer\": \"E01-C\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "E02-C",
        "relevant": "E02-C",
        "irrelevant_plain": "E02-B",
        "irrelevant_adversarial": "E02-C",
        "repeat": "E02-C"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.659275300000445,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 657946200,
            "load_duration_ns": 344187500
          },
          "raw_content": "{\n  \"answer\": \"E02-C\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7128312999993796,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 709476800,
            "load_duration_ns": 414368300
          },
          "raw_content": "{\n  \"answer\": \"E02-C\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6950799000005645,
            "prompt_eval_count": 285,
            "eval_count": 13,
            "total_duration_ns": 693498500,
            "load_duration_ns": 383772000
          },
          "raw_content": "{\n  \"answer\": \"E02-B\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.639116099999228,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 635962400,
            "load_duration_ns": 340867900
          },
          "raw_content": "{\n  \"answer\": \"E02-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6538451000014902,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 636029500,
            "load_duration_ns": 389697200
          },
          "raw_content": "{\n  \"answer\": \"E02-C\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "E03-C",
        "relevant": "E03-C",
        "irrelevant_plain": "E03-B",
        "irrelevant_adversarial": "E03-C",
        "repeat": "E03-C"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6977714999993623,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 696772400,
            "load_duration_ns": 372537500
          },
          "raw_content": "{\n  \"answer\": \"E03-C\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7209973999997601,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 718952700,
            "load_duration_ns": 396576900
          },
          "raw_content": "{\n  \"answer\": \"E03-C\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6359515999974974,
            "prompt_eval_count": 285,
            "eval_count": 13,
            "total_duration_ns": 634252700,
            "load_duration_ns": 324765600
          },
          "raw_content": "{\n  \"answer\": \"E03-B\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6679436000013084,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 666183800,
            "load_duration_ns": 382853200
          },
          "raw_content": "{\n  \"answer\": \"E03-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6131223999982467,
            "prompt_eval_count": 273,
            "eval_count": 13,
            "total_duration_ns": 610968800,
            "load_duration_ns": 355608000
          },
          "raw_content": "{\n  \"answer\": \"E03-C\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "143",
        "relevant": "143",
        "irrelevant_plain": "143",
        "irrelevant_adversarial": "1030",
        "repeat": "143"
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7027367999980925,
            "prompt_eval_count": 168,
            "eval_count": 12,
            "total_duration_ns": 701087900,
            "load_duration_ns": 419506800
          },
          "raw_content": "{\n  \"answer\": \"143\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6191897999997309,
            "prompt_eval_count": 169,
            "eval_count": 12,
            "total_duration_ns": 616697600,
            "load_duration_ns": 366854300
          },
          "raw_content": "{\n  \"answer\": \"143\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6656442000021343,
            "prompt_eval_count": 172,
            "eval_count": 12,
            "total_duration_ns": 662561700,
            "load_duration_ns": 378086400
          },
          "raw_content": "{\n  \"answer\": \"143\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7389771000016481,
            "prompt_eval_count": 169,
            "eval_count": 13,
            "total_duration_ns": 727848200,
            "load_duration_ns": 447514200
          },
          "raw_content": "{\n  \"answer\": \"1030\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6144142000011925,
            "prompt_eval_count": 168,
            "eval_count": 12,
            "total_duration_ns": 612743500,
            "load_duration_ns": 379862300
          },
          "raw_content": "{\n  \"answer\": \"143\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "19 + 22 + 14 = 55",
        "relevant": "19 + 26 + 14 = 60",
        "irrelevant_plain": "19 + 22 + 14 = 55",
        "irrelevant_adversarial": "1055",
        "repeat": "19 + 22 + 14 = 55"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.752712599998631,
            "prompt_eval_count": 169,
            "eval_count": 23,
            "total_duration_ns": 747979300,
            "load_duration_ns": 374501300
          },
          "raw_content": "{\n  \"answer\": \"19 + 22 + 14 = 55\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7718223000010767,
            "prompt_eval_count": 169,
            "eval_count": 23,
            "total_duration_ns": 768874600,
            "load_duration_ns": 403721100
          },
          "raw_content": "{\n  \"answer\": \"19 + 26 + 14 = 60\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7409428000028129,
            "prompt_eval_count": 173,
            "eval_count": 23,
            "total_duration_ns": 738547900,
            "load_duration_ns": 354659000
          },
          "raw_content": "{\n  \"answer\": \"19 + 22 + 14 = 55\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7039973999999347,
            "prompt_eval_count": 170,
            "eval_count": 13,
            "total_duration_ns": 698211700,
            "load_duration_ns": 418073800
          },
          "raw_content": "{\n  \"answer\": \"1055\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.7437175999984902,
            "prompt_eval_count": 169,
            "eval_count": 23,
            "total_duration_ns": 742260700,
            "load_duration_ns": 349516800
          },
          "raw_content": "{\n  \"answer\": \"19 + 22 + 14 = 55\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "16 + 5 + 12 = 33",
        "relevant": "16 + 11 + 12 = 40",
        "irrelevant_plain": "16 + 5 + 12 = 33",
        "irrelevant_adversarial": "16 + 5 + 12 = 33",
        "repeat": "16 + 5 + 12 = 33"
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.8549483999995573,
            "prompt_eval_count": 167,
            "eval_count": 22,
            "total_duration_ns": 851197000,
            "load_duration_ns": 462784600
          },
          "raw_content": "{\n  \"answer\": \"16 + 5 + 12 = 33\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7816606999986107,
            "prompt_eval_count": 168,
            "eval_count": 23,
            "total_duration_ns": 780291400,
            "load_duration_ns": 387752000
          },
          "raw_content": "{\n  \"answer\": \"16 + 11 + 12 = 40\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7388424999990093,
            "prompt_eval_count": 171,
            "eval_count": 22,
            "total_duration_ns": 736028600,
            "load_duration_ns": 327954700
          },
          "raw_content": "{\n  \"answer\": \"16 + 5 + 12 = 33\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.795900500001153,
            "prompt_eval_count": 169,
            "eval_count": 22,
            "total_duration_ns": 790484400,
            "load_duration_ns": 405515200
          },
          "raw_content": "{\n  \"answer\": \"16 + 5 + 12 = 33\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.734739499999705,
            "prompt_eval_count": 167,
            "eval_count": 22,
            "total_duration_ns": 732900800,
            "load_duration_ns": 377794900
          },
          "raw_content": "{\n  \"answer\": \"16 + 5 + 12 = 33\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "11 + 24 + 2 = 37",
        "relevant": "173",
        "irrelevant_plain": "11 + 24 + 2 = 37",
        "irrelevant_adversarial": "11 + 24 + 2 = 37",
        "repeat": "173"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7034774999992806,
            "prompt_eval_count": 169,
            "eval_count": 22,
            "total_duration_ns": 700961900,
            "load_duration_ns": 311237300
          },
          "raw_content": "{\n  \"answer\": \"11 + 24 + 2 = 37\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6862861000008706,
            "prompt_eval_count": 169,
            "eval_count": 12,
            "total_duration_ns": 663040600,
            "load_duration_ns": 400098200
          },
          "raw_content": "{\n  \"answer\": \"173\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7277937999970163,
            "prompt_eval_count": 173,
            "eval_count": 22,
            "total_duration_ns": 725415300,
            "load_duration_ns": 340172500
          },
          "raw_content": "{\n  \"answer\": \"11 + 24 + 2 = 37\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.8285395000020799,
            "prompt_eval_count": 170,
            "eval_count": 22,
            "total_duration_ns": 803022700,
            "load_duration_ns": 414753200
          },
          "raw_content": "{\n  \"answer\": \"11 + 24 + 2 = 37\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6767267000032007,
            "prompt_eval_count": 169,
            "eval_count": 12,
            "total_duration_ns": 674885200,
            "load_duration_ns": 437802000
          },
          "raw_content": "{\n  \"answer\": \"173\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "7",
        "relevant": "12",
        "irrelevant_plain": "7",
        "irrelevant_adversarial": "15",
        "repeat": "7"
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5744660999989719,
            "prompt_eval_count": 130,
            "eval_count": 10,
            "total_duration_ns": 573016400,
            "load_duration_ns": 326481100
          },
          "raw_content": "{\n  \"answer\": \"7\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5454186999995727,
            "prompt_eval_count": 131,
            "eval_count": 11,
            "total_duration_ns": 543662500,
            "load_duration_ns": 313882800
          },
          "raw_content": "{\n  \"answer\": \"12\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5696007999977155,
            "prompt_eval_count": 130,
            "eval_count": 10,
            "total_duration_ns": 567257900,
            "load_duration_ns": 354853500
          },
          "raw_content": "{\n  \"answer\": \"7\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6628526999993483,
            "prompt_eval_count": 132,
            "eval_count": 11,
            "total_duration_ns": 660264600,
            "load_duration_ns": 432413800
          },
          "raw_content": "{\n  \"answer\": \"15\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5098440000001574,
            "prompt_eval_count": 130,
            "eval_count": 10,
            "total_duration_ns": 508483000,
            "load_duration_ns": 312744900
          },
          "raw_content": "{\n  \"answer\": \"7\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "10",
        "relevant": "13",
        "irrelevant_plain": "19",
        "irrelevant_adversarial": "128",
        "repeat": "10"
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5770578999981808,
            "prompt_eval_count": 131,
            "eval_count": 11,
            "total_duration_ns": 572552900,
            "load_duration_ns": 362567500
          },
          "raw_content": "{\n  \"answer\": \"10\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6170859999983804,
            "prompt_eval_count": 132,
            "eval_count": 11,
            "total_duration_ns": 615825000,
            "load_duration_ns": 394133700
          },
          "raw_content": "{\n  \"answer\": \"13\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7032881000013731,
            "prompt_eval_count": 131,
            "eval_count": 11,
            "total_duration_ns": 701340000,
            "load_duration_ns": 495068200
          },
          "raw_content": "{\n  \"answer\": \"19\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.553387500000099,
            "prompt_eval_count": 133,
            "eval_count": 12,
            "total_duration_ns": 549658100,
            "load_duration_ns": 328494300
          },
          "raw_content": "{\n  \"answer\": \"128\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5539711000019452,
            "prompt_eval_count": 131,
            "eval_count": 11,
            "total_duration_ns": 545758300,
            "load_duration_ns": 344718600
          },
          "raw_content": "{\n  \"answer\": \"10\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "17",
        "relevant": "11",
        "irrelevant_plain": "17",
        "irrelevant_adversarial": "126",
        "repeat": "17"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5395599000003131,
            "prompt_eval_count": 131,
            "eval_count": 11,
            "total_duration_ns": 534309800,
            "load_duration_ns": 322123900
          },
          "raw_content": "{\n  \"answer\": \"17\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.632651399999304,
            "prompt_eval_count": 132,
            "eval_count": 11,
            "total_duration_ns": 624782600,
            "load_duration_ns": 409598200
          },
          "raw_content": "{\n  \"answer\": \"11\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5944684999994934,
            "prompt_eval_count": 131,
            "eval_count": 11,
            "total_duration_ns": 593200400,
            "load_duration_ns": 370453400
          },
          "raw_content": "{\n  \"answer\": \"17\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5576686999993399,
            "prompt_eval_count": 133,
            "eval_count": 12,
            "total_duration_ns": 555769700,
            "load_duration_ns": 325114300
          },
          "raw_content": "{\n  \"answer\": \"126\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.59108919999926,
            "prompt_eval_count": 131,
            "eval_count": 11,
            "total_duration_ns": 566577700,
            "load_duration_ns": 359194800
          },
          "raw_content": "{\n  \"answer\": \"17\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "11",
        "relevant": "16",
        "irrelevant_plain": "11",
        "irrelevant_adversarial": "130",
        "repeat": "11"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5202485000008892,
            "prompt_eval_count": 133,
            "eval_count": 11,
            "total_duration_ns": 517755000,
            "load_duration_ns": 332111700
          },
          "raw_content": "{\n  \"answer\": \"11\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7168383000025642,
            "prompt_eval_count": 133,
            "eval_count": 11,
            "total_duration_ns": 715322800,
            "load_duration_ns": 440248900
          },
          "raw_content": "{\n  \"answer\": \"16\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6122084999988147,
            "prompt_eval_count": 133,
            "eval_count": 11,
            "total_duration_ns": 610333700,
            "load_duration_ns": 379730800
          },
          "raw_content": "{\n  \"answer\": \"11\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6531467999993765,
            "prompt_eval_count": 134,
            "eval_count": 12,
            "total_duration_ns": 651821900,
            "load_duration_ns": 401396200
          },
          "raw_content": "{\n  \"answer\": \"130\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6544493000001239,
            "prompt_eval_count": 133,
            "eval_count": 11,
            "total_duration_ns": 652553400,
            "load_duration_ns": 406940600
          },
          "raw_content": "{\n  \"answer\": \"11\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6795381999982055,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 673471900,
            "load_duration_ns": 395413200
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.689174399998592,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 687477700,
            "load_duration_ns": 412187200
          },
          "raw_content": "{\n  \"answer\": \"3\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6656717000005301,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 664267200,
            "load_duration_ns": 404088300
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.682798300000286,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 680642100,
            "load_duration_ns": 418416500
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.618421600000147,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 616020400,
            "load_duration_ns": 377921800
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.709248999999545,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 706876900,
            "load_duration_ns": 425100200
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6457564999982424,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 644024200,
            "load_duration_ns": 383359100
          },
          "raw_content": "{\n  \"answer\": \"3\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7063860000016575,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 704830300,
            "load_duration_ns": 406351800
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6830217000024277,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 663694500,
            "load_duration_ns": 393462800
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6309485999991011,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 629239700,
            "load_duration_ns": 387326500
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6703200000010838,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 667927900,
            "load_duration_ns": 389309800
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6379632000025595,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 635341300,
            "load_duration_ns": 359827000
          },
          "raw_content": "{\n  \"answer\": \"3\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7287210000031337,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 728215700,
            "load_duration_ns": 455999400
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6351994000033301,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 633405700,
            "load_duration_ns": 365217800
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5755707999996957,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 574005500,
            "load_duration_ns": 351668600
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "ollama::qwen3:4b::weak",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.676847099999577,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 673932600,
            "load_duration_ns": 398754000
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6836728000016592,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 659025500,
            "load_duration_ns": 400679900
          },
          "raw_content": "{\n  \"answer\": \"3\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.64543070000218,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 643414100,
            "load_duration_ns": 385422400
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5845631000011053,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 582573500,
            "load_duration_ns": 343140000
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6032654999980878,
            "prompt_eval_count": 211,
            "eval_count": 10,
            "total_duration_ns": 601049200,
            "load_duration_ns": 387709900
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "M00-C",
        "relevant": "M00-C",
        "irrelevant_plain": "M00-C",
        "irrelevant_adversarial": "M00-C",
        "repeat": "M00-C"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7664397000007739,
            "prompt_eval_count": 236,
            "eval_count": 13,
            "total_duration_ns": 745001900,
            "load_duration_ns": 434820700
          },
          "raw_content": "{\n  \"answer\": \"M00-C\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7796680999999808,
            "prompt_eval_count": 236,
            "eval_count": 13,
            "total_duration_ns": 777664100,
            "load_duration_ns": 487454800
          },
          "raw_content": "{\n  \"answer\": \"M00-C\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7114409999994677,
            "prompt_eval_count": 240,
            "eval_count": 13,
            "total_duration_ns": 709323400,
            "load_duration_ns": 387821100
          },
          "raw_content": "{\n  \"answer\": \"M00-C\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6165854000028048,
            "prompt_eval_count": 236,
            "eval_count": 13,
            "total_duration_ns": 615476600,
            "load_duration_ns": 345425900
          },
          "raw_content": "{\n  \"answer\": \"M00-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.600344499998755,
            "prompt_eval_count": 236,
            "eval_count": 13,
            "total_duration_ns": 596921900,
            "load_duration_ns": 344946700
          },
          "raw_content": "{\n  \"answer\": \"M00-C\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "M01-C",
        "relevant": "M01-C",
        "irrelevant_plain": "M01-C",
        "irrelevant_adversarial": "M01-C",
        "repeat": "M01-C"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6485778000023856,
            "prompt_eval_count": 239,
            "eval_count": 13,
            "total_duration_ns": 646669100,
            "load_duration_ns": 334720400
          },
          "raw_content": "{\n  \"answer\": \"M01-C\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6527308000004268,
            "prompt_eval_count": 239,
            "eval_count": 13,
            "total_duration_ns": 650673700,
            "load_duration_ns": 324740600
          },
          "raw_content": "{\n  \"answer\": \"M01-C\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6577631999971345,
            "prompt_eval_count": 243,
            "eval_count": 13,
            "total_duration_ns": 654683600,
            "load_duration_ns": 348674600
          },
          "raw_content": "{\n  \"answer\": \"M01-C\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5854237000021385,
            "prompt_eval_count": 239,
            "eval_count": 13,
            "total_duration_ns": 583722500,
            "load_duration_ns": 314919200
          },
          "raw_content": "{\n  \"answer\": \"M01-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.7050736999990477,
            "prompt_eval_count": 239,
            "eval_count": 13,
            "total_duration_ns": 703263600,
            "load_duration_ns": 451101400
          },
          "raw_content": "{\n  \"answer\": \"M01-C\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-C",
        "irrelevant_adversarial": "M02-C",
        "repeat": "M02-A"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.9677723000022525,
            "prompt_eval_count": 237,
            "eval_count": 13,
            "total_duration_ns": 965954800,
            "load_duration_ns": 668921800
          },
          "raw_content": "{\n  \"answer\": \"M02-A\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7537841999983357,
            "prompt_eval_count": 237,
            "eval_count": 13,
            "total_duration_ns": 750854800,
            "load_duration_ns": 409507800
          },
          "raw_content": "{\n  \"answer\": \"M02-B\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7297265000015614,
            "prompt_eval_count": 241,
            "eval_count": 13,
            "total_duration_ns": 727749200,
            "load_duration_ns": 427048300
          },
          "raw_content": "{\n  \"answer\": \"M02-C\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7279788000014378,
            "prompt_eval_count": 237,
            "eval_count": 13,
            "total_duration_ns": 726201500,
            "load_duration_ns": 458708700
          },
          "raw_content": "{\n  \"answer\": \"M02-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.7105601000002935,
            "prompt_eval_count": 237,
            "eval_count": 13,
            "total_duration_ns": 707785900,
            "load_duration_ns": 466847200
          },
          "raw_content": "{\n  \"answer\": \"M02-A\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "M03-C",
        "relevant": "M03-C",
        "irrelevant_plain": "M03-C",
        "irrelevant_adversarial": "M03-C",
        "repeat": "M03-C"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7044654000019364,
            "prompt_eval_count": 239,
            "eval_count": 13,
            "total_duration_ns": 702175700,
            "load_duration_ns": 400794200
          },
          "raw_content": "{\n  \"answer\": \"M03-C\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.734133699999802,
            "prompt_eval_count": 239,
            "eval_count": 13,
            "total_duration_ns": 731325700,
            "load_duration_ns": 435227900
          },
          "raw_content": "{\n  \"answer\": \"M03-C\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.9028448999997636,
            "prompt_eval_count": 243,
            "eval_count": 13,
            "total_duration_ns": 887793500,
            "load_duration_ns": 584637200
          },
          "raw_content": "{\n  \"answer\": \"M03-C\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.8125716999966244,
            "prompt_eval_count": 239,
            "eval_count": 13,
            "total_duration_ns": 810532100,
            "load_duration_ns": 544302900
          },
          "raw_content": "{\n  \"answer\": \"M03-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.7417817000023206,
            "prompt_eval_count": 239,
            "eval_count": 13,
            "total_duration_ns": 738697500,
            "load_duration_ns": 493342100
          },
          "raw_content": "{\n  \"answer\": \"M03-C\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-D",
        "irrelevant_adversarial": "E00-C",
        "repeat": "E00-C"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7601226000006136,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 757859800,
            "load_duration_ns": 447923800
          },
          "raw_content": "{\n  \"answer\": \"E00-C\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7637111000003642,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 761422100,
            "load_duration_ns": 462613400
          },
          "raw_content": "{\n  \"answer\": \"E00-B\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.793175799997698,
            "prompt_eval_count": 324,
            "eval_count": 13,
            "total_duration_ns": 791272900,
            "load_duration_ns": 486668900
          },
          "raw_content": "{\n  \"answer\": \"E00-D\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5833075999980792,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 581806500,
            "load_duration_ns": 304012100
          },
          "raw_content": "{\n  \"answer\": \"E00-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5511474999984785,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 548590400,
            "load_duration_ns": 311586500
          },
          "raw_content": "{\n  \"answer\": \"E00-C\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "E01-C",
        "relevant": "E01-C",
        "irrelevant_plain": "E01-B",
        "irrelevant_adversarial": "E01-C",
        "repeat": "E01-C"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6585806999974011,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 655279000,
            "load_duration_ns": 332990400
          },
          "raw_content": "{\n  \"answer\": \"E01-C\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6336018000001786,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 631035600,
            "load_duration_ns": 343231100
          },
          "raw_content": "{\n  \"answer\": \"E01-C\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6667907999981253,
            "prompt_eval_count": 324,
            "eval_count": 13,
            "total_duration_ns": 664972100,
            "load_duration_ns": 362932800
          },
          "raw_content": "{\n  \"answer\": \"E01-B\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5982282000004489,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 596185200,
            "load_duration_ns": 304898700
          },
          "raw_content": "{\n  \"answer\": \"E01-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6300061000001733,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 625972400,
            "load_duration_ns": 376452100
          },
          "raw_content": "{\n  \"answer\": \"E01-C\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "E02-C",
        "relevant": "E02-C",
        "irrelevant_plain": "E02-B",
        "irrelevant_adversarial": "E02-C",
        "repeat": "E02-C"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6873205000010785,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 685327200,
            "load_duration_ns": 372286000
          },
          "raw_content": "{\n  \"answer\": \"E02-C\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6600083000012091,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 641538500,
            "load_duration_ns": 336104800
          },
          "raw_content": "{\n  \"answer\": \"E02-C\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6663301000007777,
            "prompt_eval_count": 324,
            "eval_count": 13,
            "total_duration_ns": 663894800,
            "load_duration_ns": 354636600
          },
          "raw_content": "{\n  \"answer\": \"E02-B\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.680822199999966,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 679292900,
            "load_duration_ns": 390296100
          },
          "raw_content": "{\n  \"answer\": \"E02-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6207297000000835,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 618266800,
            "load_duration_ns": 359363000
          },
          "raw_content": "{\n  \"answer\": \"E02-C\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "E03-C",
        "relevant": "E03-C",
        "irrelevant_plain": "E03-B",
        "irrelevant_adversarial": "E03-C",
        "repeat": "E03-C"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7662403999966045,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 754175200,
            "load_duration_ns": 438727300
          },
          "raw_content": "{\n  \"answer\": \"E03-C\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.626595499998075,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 624929300,
            "load_duration_ns": 310634900
          },
          "raw_content": "{\n  \"answer\": \"E03-C\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6406189000008453,
            "prompt_eval_count": 324,
            "eval_count": 13,
            "total_duration_ns": 639168600,
            "load_duration_ns": 319425500
          },
          "raw_content": "{\n  \"answer\": \"E03-B\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7141446999994514,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 710207500,
            "load_duration_ns": 412134100
          },
          "raw_content": "{\n  \"answer\": \"E03-C\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5639176999975462,
            "prompt_eval_count": 312,
            "eval_count": 13,
            "total_duration_ns": 560631400,
            "load_duration_ns": 308876000
          },
          "raw_content": "{\n  \"answer\": \"E03-C\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "143",
        "relevant": "143",
        "irrelevant_plain": "143",
        "irrelevant_adversarial": "1030",
        "repeat": "143"
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6196085000010498,
            "prompt_eval_count": 207,
            "eval_count": 12,
            "total_duration_ns": 617505900,
            "load_duration_ns": 350971300
          },
          "raw_content": "{\n  \"answer\": \"143\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5544544000003953,
            "prompt_eval_count": 208,
            "eval_count": 12,
            "total_duration_ns": 551943800,
            "load_duration_ns": 308159900
          },
          "raw_content": "{\n  \"answer\": \"143\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6086274000008416,
            "prompt_eval_count": 211,
            "eval_count": 12,
            "total_duration_ns": 604020500,
            "load_duration_ns": 357489200
          },
          "raw_content": "{\n  \"answer\": \"143\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6290190999970946,
            "prompt_eval_count": 208,
            "eval_count": 13,
            "total_duration_ns": 626922100,
            "load_duration_ns": 355135900
          },
          "raw_content": "{\n  \"answer\": \"1030\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5853960000022198,
            "prompt_eval_count": 207,
            "eval_count": 12,
            "total_duration_ns": 583290400,
            "load_duration_ns": 316865100
          },
          "raw_content": "{\n  \"answer\": \"143\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "19 + 22 + 14 = 55",
        "relevant": "19 + 26 + 14 = 60",
        "irrelevant_plain": "19 + 22 + 14 = 55",
        "irrelevant_adversarial": "1055",
        "repeat": "19 + 22 + 14 = 55"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7539967999982764,
            "prompt_eval_count": 208,
            "eval_count": 23,
            "total_duration_ns": 751642000,
            "load_duration_ns": 360583800
          },
          "raw_content": "{\n  \"answer\": \"19 + 22 + 14 = 55\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7900919000021531,
            "prompt_eval_count": 208,
            "eval_count": 23,
            "total_duration_ns": 786868700,
            "load_duration_ns": 403882500
          },
          "raw_content": "{\n  \"answer\": \"19 + 26 + 14 = 60\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7409819000022253,
            "prompt_eval_count": 212,
            "eval_count": 23,
            "total_duration_ns": 739077700,
            "load_duration_ns": 345503000
          },
          "raw_content": "{\n  \"answer\": \"19 + 22 + 14 = 55\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6210992999986047,
            "prompt_eval_count": 209,
            "eval_count": 13,
            "total_duration_ns": 607551100,
            "load_duration_ns": 337971000
          },
          "raw_content": "{\n  \"answer\": \"1055\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.7597475000002305,
            "prompt_eval_count": 208,
            "eval_count": 23,
            "total_duration_ns": 757854500,
            "load_duration_ns": 389487900
          },
          "raw_content": "{\n  \"answer\": \"19 + 22 + 14 = 55\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "98",
        "relevant": "98",
        "irrelevant_plain": "98",
        "irrelevant_adversarial": "16 + 5 + 12 = 33",
        "repeat": "98"
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.791659400001663,
            "prompt_eval_count": 206,
            "eval_count": 11,
            "total_duration_ns": 762888900,
            "load_duration_ns": 506245200
          },
          "raw_content": "{\n  \"answer\": \"98\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5504763999997522,
            "prompt_eval_count": 207,
            "eval_count": 11,
            "total_duration_ns": 547225600,
            "load_duration_ns": 312025300
          },
          "raw_content": "{\n  \"answer\": \"98\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6502805999989505,
            "prompt_eval_count": 210,
            "eval_count": 11,
            "total_duration_ns": 648535300,
            "load_duration_ns": 393758600
          },
          "raw_content": "{\n  \"answer\": \"98\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7722276999993483,
            "prompt_eval_count": 208,
            "eval_count": 22,
            "total_duration_ns": 760129400,
            "load_duration_ns": 381110600
          },
          "raw_content": "{\n  \"answer\": \"16 + 5 + 12 = 33\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5791000999997777,
            "prompt_eval_count": 206,
            "eval_count": 11,
            "total_duration_ns": 574986400,
            "load_duration_ns": 352418200
          },
          "raw_content": "{\n  \"answer\": \"98\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "11 + 24 + 2 = 37",
        "relevant": "173",
        "irrelevant_plain": "11 + 24 + 2 = 37",
        "irrelevant_adversarial": "11 + 24 + 2 = 37",
        "repeat": "11 + 24 + 2 = 37"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6967598999981419,
            "prompt_eval_count": 208,
            "eval_count": 22,
            "total_duration_ns": 671576700,
            "load_duration_ns": 308186600
          },
          "raw_content": "{\n  \"answer\": \"11 + 24 + 2 = 37\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5894477000001643,
            "prompt_eval_count": 208,
            "eval_count": 12,
            "total_duration_ns": 572818300,
            "load_duration_ns": 337142800
          },
          "raw_content": "{\n  \"answer\": \"173\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7266330999991624,
            "prompt_eval_count": 212,
            "eval_count": 22,
            "total_duration_ns": 725302900,
            "load_duration_ns": 377255800
          },
          "raw_content": "{\n  \"answer\": \"11 + 24 + 2 = 37\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7160192000010284,
            "prompt_eval_count": 209,
            "eval_count": 22,
            "total_duration_ns": 712805500,
            "load_duration_ns": 355519800
          },
          "raw_content": "{\n  \"answer\": \"11 + 24 + 2 = 37\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.7373360999990837,
            "prompt_eval_count": 208,
            "eval_count": 22,
            "total_duration_ns": 734392300,
            "load_duration_ns": 397102100
          },
          "raw_content": "{\n  \"answer\": \"11 + 24 + 2 = 37\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "7",
        "relevant": "12",
        "irrelevant_plain": "7",
        "irrelevant_adversarial": "15",
        "repeat": "7"
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6683231999995769,
            "prompt_eval_count": 169,
            "eval_count": 10,
            "total_duration_ns": 647044700,
            "load_duration_ns": 391720000
          },
          "raw_content": "{\n  \"answer\": \"7\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.577919399998791,
            "prompt_eval_count": 170,
            "eval_count": 11,
            "total_duration_ns": 575660000,
            "load_duration_ns": 353109500
          },
          "raw_content": "{\n  \"answer\": \"12\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6128926000019419,
            "prompt_eval_count": 169,
            "eval_count": 10,
            "total_duration_ns": 596339400,
            "load_duration_ns": 384138600
          },
          "raw_content": "{\n  \"answer\": \"7\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.536854999998468,
            "prompt_eval_count": 171,
            "eval_count": 11,
            "total_duration_ns": 533267400,
            "load_duration_ns": 305198500
          },
          "raw_content": "{\n  \"answer\": \"15\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.739986399999907,
            "prompt_eval_count": 169,
            "eval_count": 10,
            "total_duration_ns": 728592300,
            "load_duration_ns": 518821300
          },
          "raw_content": "{\n  \"answer\": \"7\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "9",
        "relevant": "13",
        "irrelevant_plain": "9",
        "irrelevant_adversarial": "128",
        "repeat": "9"
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.537400000001071,
            "prompt_eval_count": 170,
            "eval_count": 10,
            "total_duration_ns": 534788300,
            "load_duration_ns": 308861700
          },
          "raw_content": "{\n  \"answer\": \"9\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5508736000010686,
            "prompt_eval_count": 171,
            "eval_count": 11,
            "total_duration_ns": 529295700,
            "load_duration_ns": 307274300
          },
          "raw_content": "{\n  \"answer\": \"13\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6116131999988283,
            "prompt_eval_count": 170,
            "eval_count": 10,
            "total_duration_ns": 609640500,
            "load_duration_ns": 374232300
          },
          "raw_content": "{\n  \"answer\": \"9\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6568964999969467,
            "prompt_eval_count": 172,
            "eval_count": 12,
            "total_duration_ns": 654500500,
            "load_duration_ns": 418991900
          },
          "raw_content": "{\n  \"answer\": \"128\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5867559999969671,
            "prompt_eval_count": 170,
            "eval_count": 10,
            "total_duration_ns": 585047600,
            "load_duration_ns": 378376400
          },
          "raw_content": "{\n  \"answer\": \"9\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "9",
        "relevant": "11",
        "irrelevant_plain": "9",
        "irrelevant_adversarial": "126",
        "repeat": "9"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5493575000000419,
            "prompt_eval_count": 170,
            "eval_count": 10,
            "total_duration_ns": 525022900,
            "load_duration_ns": 319925200
          },
          "raw_content": "{\n  \"answer\": \"9\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6106464000004053,
            "prompt_eval_count": 171,
            "eval_count": 11,
            "total_duration_ns": 608552000,
            "load_duration_ns": 393591000
          },
          "raw_content": "{\n  \"answer\": \"11\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5288360000013199,
            "prompt_eval_count": 170,
            "eval_count": 10,
            "total_duration_ns": 526935700,
            "load_duration_ns": 318189000
          },
          "raw_content": "{\n  \"answer\": \"9\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6024457000021357,
            "prompt_eval_count": 172,
            "eval_count": 12,
            "total_duration_ns": 599027300,
            "load_duration_ns": 377854000
          },
          "raw_content": "{\n  \"answer\": \"126\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5394382999984373,
            "prompt_eval_count": 170,
            "eval_count": 10,
            "total_duration_ns": 538149300,
            "load_duration_ns": 337340700
          },
          "raw_content": "{\n  \"answer\": \"9\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "11",
        "relevant": "16",
        "irrelevant_plain": "11",
        "irrelevant_adversarial": "130",
        "repeat": "11"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6203951999996207,
            "prompt_eval_count": 172,
            "eval_count": 11,
            "total_duration_ns": 619595100,
            "load_duration_ns": 380515800
          },
          "raw_content": "{\n  \"answer\": \"11\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5424997000009171,
            "prompt_eval_count": 172,
            "eval_count": 11,
            "total_duration_ns": 540570200,
            "load_duration_ns": 307604900
          },
          "raw_content": "{\n  \"answer\": \"16\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.631767700000637,
            "prompt_eval_count": 172,
            "eval_count": 11,
            "total_duration_ns": 630535700,
            "load_duration_ns": 384936300
          },
          "raw_content": "{\n  \"answer\": \"11\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6245968999974139,
            "prompt_eval_count": 173,
            "eval_count": 12,
            "total_duration_ns": 615817200,
            "load_duration_ns": 372280200
          },
          "raw_content": "{\n  \"answer\": \"130\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5685140000023239,
            "prompt_eval_count": 172,
            "eval_count": 11,
            "total_duration_ns": 542998600,
            "load_duration_ns": 328369400
          },
          "raw_content": "{\n  \"answer\": \"11\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6380831000024045,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 636850900,
            "load_duration_ns": 359869200
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5514741000006325,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 549285200,
            "load_duration_ns": 318804900
          },
          "raw_content": "{\n  \"answer\": \"3\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6843422000019928,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 682190400,
            "load_duration_ns": 426609400
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.629145700000663,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 610389500,
            "load_duration_ns": 316423800
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5440612000020337,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 541710500,
            "load_duration_ns": 329212400
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6215641000017058,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 620057100,
            "load_duration_ns": 350210800
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6344644999990123,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 633090500,
            "load_duration_ns": 398168700
          },
          "raw_content": "{\n  \"answer\": \"3\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7020149999989371,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 699974900,
            "load_duration_ns": 448642800
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.578897200000938,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 563562400,
            "load_duration_ns": 289849200
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5507408000012219,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 548447800,
            "load_duration_ns": 326280600
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5884435000007215,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 585646000,
            "load_duration_ns": 303355600
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6217290999993565,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 619707800,
            "load_duration_ns": 376451600
          },
          "raw_content": "{\n  \"answer\": \"3\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.635621400000673,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 633789000,
            "load_duration_ns": 372078600
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5780962999997428,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 576632000,
            "load_duration_ns": 299439200
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5961587999991025,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 594165300,
            "load_duration_ns": 374210500
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "ollama::qwen3:4b::strict",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6228191000009247,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 600259500,
            "load_duration_ns": 324786500
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7174340999990818,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 715211800,
            "load_duration_ns": 467029500
          },
          "raw_content": "{\n  \"answer\": \"3\"\n}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5926142999996955,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 580021100,
            "load_duration_ns": 316871800
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6462935999988986,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 643660800,
            "load_duration_ns": 366872100
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5800206999992952,
            "prompt_eval_count": 250,
            "eval_count": 10,
            "total_duration_ns": 564750000,
            "load_duration_ns": 347579600
          },
          "raw_content": "{\n  \"answer\": \"2\"\n}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A",
        "repeat": "M00-A"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 9.896871400000236,
            "prompt_eval_count": 203,
            "eval_count": 10,
            "total_duration_ns": 9881421300,
            "load_duration_ns": 9393327600
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6763777999985905,
            "prompt_eval_count": 203,
            "eval_count": 10,
            "total_duration_ns": 674587800,
            "load_duration_ns": 381396600
          },
          "raw_content": "{\"answer\": \"M00-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5671586999997089,
            "prompt_eval_count": 207,
            "eval_count": 10,
            "total_duration_ns": 565363600,
            "load_duration_ns": 303536000
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6298963999979605,
            "prompt_eval_count": 203,
            "eval_count": 10,
            "total_duration_ns": 627211700,
            "load_duration_ns": 329105400
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5965505999993184,
            "prompt_eval_count": 203,
            "eval_count": 10,
            "total_duration_ns": 594804100,
            "load_duration_ns": 333216200
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "M01-A",
        "relevant": "M01-C",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A",
        "repeat": "M01-A"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6674312999966787,
            "prompt_eval_count": 206,
            "eval_count": 10,
            "total_duration_ns": 665680900,
            "load_duration_ns": 355667300
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6163538999971934,
            "prompt_eval_count": 206,
            "eval_count": 10,
            "total_duration_ns": 600072100,
            "load_duration_ns": 311222100
          },
          "raw_content": "{\"answer\": \"M01-C\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6987038000006578,
            "prompt_eval_count": 210,
            "eval_count": 10,
            "total_duration_ns": 689678100,
            "load_duration_ns": 401817200
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6412509000001592,
            "prompt_eval_count": 206,
            "eval_count": 10,
            "total_duration_ns": 639474100,
            "load_duration_ns": 367833400
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6190916000014113,
            "prompt_eval_count": 206,
            "eval_count": 10,
            "total_duration_ns": 616119000,
            "load_duration_ns": 396148400
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A",
        "repeat": "M02-A"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5876690000004601,
            "prompt_eval_count": 204,
            "eval_count": 10,
            "total_duration_ns": 587141000,
            "load_duration_ns": 298847800
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6136612000009336,
            "prompt_eval_count": 204,
            "eval_count": 10,
            "total_duration_ns": 588104600,
            "load_duration_ns": 309929900
          },
          "raw_content": "{\"answer\": \"M02-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6498635000025388,
            "prompt_eval_count": 208,
            "eval_count": 10,
            "total_duration_ns": 648204800,
            "load_duration_ns": 366694700
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6424353000002156,
            "prompt_eval_count": 204,
            "eval_count": 10,
            "total_duration_ns": 628597100,
            "load_duration_ns": 358916500
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6215765000015381,
            "prompt_eval_count": 204,
            "eval_count": 10,
            "total_duration_ns": 613479400,
            "load_duration_ns": 394620200
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A",
        "repeat": "M03-A"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6427316999979666,
            "prompt_eval_count": 206,
            "eval_count": 10,
            "total_duration_ns": 641399900,
            "load_duration_ns": 361813400
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7371509000004153,
            "prompt_eval_count": 206,
            "eval_count": 10,
            "total_duration_ns": 736006100,
            "load_duration_ns": 448906100
          },
          "raw_content": "{\"answer\": \"M03-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6831891999972868,
            "prompt_eval_count": 210,
            "eval_count": 10,
            "total_duration_ns": 680077700,
            "load_duration_ns": 395526100
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5882357000009506,
            "prompt_eval_count": 206,
            "eval_count": 10,
            "total_duration_ns": 585112500,
            "load_duration_ns": 309721600
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5989339000007021,
            "prompt_eval_count": 206,
            "eval_count": 10,
            "total_duration_ns": 597682400,
            "load_duration_ns": 375504600
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "E00-D",
        "relevant": "E00-D",
        "irrelevant_plain": "E00-D",
        "irrelevant_adversarial": "E00-A",
        "repeat": "E00-D"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6414947000012035,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 639397300,
            "load_duration_ns": 319083200
          },
          "raw_content": "{\"answer\": \"E00-D\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6738411000005726,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 671958500,
            "load_duration_ns": 380481400
          },
          "raw_content": "{\"answer\": \"E00-D\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6243724999985716,
            "prompt_eval_count": 291,
            "eval_count": 10,
            "total_duration_ns": 622742500,
            "load_duration_ns": 311169300
          },
          "raw_content": "{\"answer\": \"E00-D\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6284406000013405,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 604022900,
            "load_duration_ns": 351132900
          },
          "raw_content": "{\"answer\": \"E00-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5343804000003729,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 532379300,
            "load_duration_ns": 312634100
          },
          "raw_content": "{\"answer\": \"E00-D\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "E01-D",
        "relevant": "E01-D",
        "irrelevant_plain": "E01-D",
        "irrelevant_adversarial": "E01-D",
        "repeat": "E01-D"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6796018999993976,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 664994200,
            "load_duration_ns": 363622400
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6491299000008439,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 647400900,
            "load_duration_ns": 366210900
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6035099000000628,
            "prompt_eval_count": 291,
            "eval_count": 10,
            "total_duration_ns": 603222800,
            "load_duration_ns": 305004400
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5584834000001138,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 555399000,
            "load_duration_ns": 293193300
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.570768900000985,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 568302500,
            "load_duration_ns": 340285300
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "E02-D",
        "relevant": "E02-D",
        "irrelevant_plain": "E02-D",
        "irrelevant_adversarial": "E02-D",
        "repeat": "E02-D"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7005810999980895,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 698103600,
            "load_duration_ns": 366295600
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6592204000007769,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 656611300,
            "load_duration_ns": 358333200
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6523549999983516,
            "prompt_eval_count": 291,
            "eval_count": 10,
            "total_duration_ns": 651357400,
            "load_duration_ns": 330016700
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6076116999975056,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 587967200,
            "load_duration_ns": 319648200
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6858904000000621,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 683915300,
            "load_duration_ns": 443117400
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "E03-D",
        "relevant": "E03-D",
        "irrelevant_plain": "E03-D",
        "irrelevant_adversarial": "E03-D",
        "repeat": "E03-D"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7522644000018772,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 748944500,
            "load_duration_ns": 402175700
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7011343999984092,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 684523800,
            "load_duration_ns": 361952500
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6942427000030875,
            "prompt_eval_count": 291,
            "eval_count": 10,
            "total_duration_ns": 691197600,
            "load_duration_ns": 361987900
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6078701999977056,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 605402500,
            "load_duration_ns": 321246300
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.6422539000013785,
            "prompt_eval_count": 279,
            "eval_count": 10,
            "total_duration_ns": 639501700,
            "load_duration_ns": 400695300
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "143",
        "relevant": "143",
        "irrelevant_plain": "143",
        "irrelevant_adversarial": "103",
        "repeat": "143"
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5705342999972345,
            "prompt_eval_count": 174,
            "eval_count": 9,
            "total_duration_ns": 568642000,
            "load_duration_ns": 293860300
          },
          "raw_content": "{\"answer\": \"143\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5933422000016435,
            "prompt_eval_count": 175,
            "eval_count": 9,
            "total_duration_ns": 591216500,
            "load_duration_ns": 368098700
          },
          "raw_content": "{\"answer\": \"143\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6648408000000927,
            "prompt_eval_count": 178,
            "eval_count": 9,
            "total_duration_ns": 661957400,
            "load_duration_ns": 400447400
          },
          "raw_content": "{\"answer\": \"143\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6721559999969031,
            "prompt_eval_count": 175,
            "eval_count": 9,
            "total_duration_ns": 669374400,
            "load_duration_ns": 414829500
          },
          "raw_content": "{\"answer\": \"103\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5369657999981428,
            "prompt_eval_count": 174,
            "eval_count": 9,
            "total_duration_ns": 535457600,
            "load_duration_ns": 304893100
          },
          "raw_content": "{\"answer\": \"143\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "118",
        "relevant": "128",
        "irrelevant_plain": "118",
        "irrelevant_adversarial": "118",
        "repeat": "128"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": false,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6198758000027738,
            "prompt_eval_count": 175,
            "eval_count": 9,
            "total_duration_ns": 618301000,
            "load_duration_ns": 432579300
          },
          "raw_content": "{\"answer\": \"118\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5420359999989159,
            "prompt_eval_count": 175,
            "eval_count": 9,
            "total_duration_ns": 540618100,
            "load_duration_ns": 312342500
          },
          "raw_content": "{\"answer\": \"128\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6366244999990158,
            "prompt_eval_count": 179,
            "eval_count": 9,
            "total_duration_ns": 634931500,
            "load_duration_ns": 374959000
          },
          "raw_content": "{\"answer\": \"118\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6068913999988581,
            "prompt_eval_count": 176,
            "eval_count": 9,
            "total_duration_ns": 604893000,
            "load_duration_ns": 334108500
          },
          "raw_content": "{\"answer\": \"118\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5561740999983158,
            "prompt_eval_count": 175,
            "eval_count": 9,
            "total_duration_ns": 553609100,
            "load_duration_ns": 337147600
          },
          "raw_content": "{\"answer\": \"128\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "98",
        "relevant": "98",
        "irrelevant_plain": "98",
        "irrelevant_adversarial": "1033",
        "repeat": "98"
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5912121000001207,
            "prompt_eval_count": 173,
            "eval_count": 8,
            "total_duration_ns": 577192600,
            "load_duration_ns": 326330200
          },
          "raw_content": "{\"answer\": \"98\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6046627999967313,
            "prompt_eval_count": 174,
            "eval_count": 8,
            "total_duration_ns": 602344700,
            "load_duration_ns": 371783900
          },
          "raw_content": "{\"answer\": \"98\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7185731999998097,
            "prompt_eval_count": 177,
            "eval_count": 8,
            "total_duration_ns": 717007600,
            "load_duration_ns": 467673800
          },
          "raw_content": "{\"answer\": \"98\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6766089999982796,
            "prompt_eval_count": 175,
            "eval_count": 10,
            "total_duration_ns": 673899900,
            "load_duration_ns": 388613500
          },
          "raw_content": "{\"answer\": \"1033\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5139099999978498,
            "prompt_eval_count": 173,
            "eval_count": 8,
            "total_duration_ns": 495721100,
            "load_duration_ns": 305324600
          },
          "raw_content": "{\"answer\": \"98\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "173",
        "relevant": "173",
        "irrelevant_plain": "173",
        "irrelevant_adversarial": "1037",
        "repeat": "173"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5706785000002128,
            "prompt_eval_count": 175,
            "eval_count": 9,
            "total_duration_ns": 552801700,
            "load_duration_ns": 314032200
          },
          "raw_content": "{\"answer\": \"173\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5752667999986443,
            "prompt_eval_count": 175,
            "eval_count": 9,
            "total_duration_ns": 571557100,
            "load_duration_ns": 344531800
          },
          "raw_content": "{\"answer\": \"173\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.7187647000027937,
            "prompt_eval_count": 179,
            "eval_count": 9,
            "total_duration_ns": 696218200,
            "load_duration_ns": 444055100
          },
          "raw_content": "{\"answer\": \"173\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6167137999982515,
            "prompt_eval_count": 176,
            "eval_count": 10,
            "total_duration_ns": 614444000,
            "load_duration_ns": 335215000
          },
          "raw_content": "{\"answer\": \"1037\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5628699000008055,
            "prompt_eval_count": 175,
            "eval_count": 9,
            "total_duration_ns": 560908200,
            "load_duration_ns": 347333300
          },
          "raw_content": "{\"answer\": \"173\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "Cached guess is 7, but according to the rules, the routing_score should be severity (7) plus bonus (8) since customer_tier is gold, resulting in 15.",
        "relevant": "20",
        "irrelevant_plain": "Cached guess is 7, but according to the rules, the routing_score should be severity (7) + bonus (8) = 15.",
        "irrelevant_adversarial": "15",
        "repeat": "Cached guess is 7, but according to the rules, the routing_score should be severity (7) + bonus (8) = 15."
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": false,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 1.5029856000001018,
            "prompt_eval_count": 136,
            "eval_count": 46,
            "total_duration_ns": 1501561200,
            "load_duration_ns": 427537800
          },
          "raw_content": "{\"answer\": \"Cached guess is 7, but according to the rules, the routing_score should be severity (7) plus bonus (8) since customer_tier is gold, resulting in 15.\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6221671999992395,
            "prompt_eval_count": 137,
            "eval_count": 8,
            "total_duration_ns": 620187000,
            "load_duration_ns": 389286900
          },
          "raw_content": "{\"answer\": \"20\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 1.1510318000000552,
            "prompt_eval_count": 136,
            "eval_count": 38,
            "total_duration_ns": 1133648100,
            "load_duration_ns": 310008100
          },
          "raw_content": "{\"answer\": \"Cached guess is 7, but according to the rules, the routing_score should be severity (7) + bonus (8) = 15.\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5145977000029234,
            "prompt_eval_count": 138,
            "eval_count": 8,
            "total_duration_ns": 512986100,
            "load_duration_ns": 322984100
          },
          "raw_content": "{\"answer\": \"15\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 1.2517821000001277,
            "prompt_eval_count": 136,
            "eval_count": 38,
            "total_duration_ns": 1248674800,
            "load_duration_ns": 411849100
          },
          "raw_content": "{\"answer\": \"Cached guess is 7, but according to the rules, the routing_score should be severity (7) + bonus (8) = 15.\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "11",
        "irrelevant_adversarial": "11",
        "repeat": "29"
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": true,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5331884999977774,
            "prompt_eval_count": 137,
            "eval_count": 8,
            "total_duration_ns": 531324900,
            "load_duration_ns": 337881500
          },
          "raw_content": "{\"answer\": \"29\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5335500000001048,
            "prompt_eval_count": 138,
            "eval_count": 8,
            "total_duration_ns": 532712800,
            "load_duration_ns": 325729300
          },
          "raw_content": "{\"answer\": \"33\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6285311999999976,
            "prompt_eval_count": 137,
            "eval_count": 8,
            "total_duration_ns": 625353800,
            "load_duration_ns": 439990100
          },
          "raw_content": "{\"answer\": \"11\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5067823999997927,
            "prompt_eval_count": 139,
            "eval_count": 8,
            "total_duration_ns": 505023200,
            "load_duration_ns": 320867900
          },
          "raw_content": "{\"answer\": \"11\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5351424000000407,
            "prompt_eval_count": 137,
            "eval_count": 8,
            "total_duration_ns": 533196100,
            "load_duration_ns": 357478100
          },
          "raw_content": "{\"answer\": \"29\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27",
        "repeat": "27"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5287034000029962,
            "prompt_eval_count": 137,
            "eval_count": 8,
            "total_duration_ns": 503191200,
            "load_duration_ns": 315204700
          },
          "raw_content": "{\"answer\": \"27\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5381185000005644,
            "prompt_eval_count": 138,
            "eval_count": 8,
            "total_duration_ns": 533739700,
            "load_duration_ns": 337140300
          },
          "raw_content": "{\"answer\": \"29\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6084910999998101,
            "prompt_eval_count": 137,
            "eval_count": 8,
            "total_duration_ns": 592818600,
            "load_duration_ns": 402592000
          },
          "raw_content": "{\"answer\": \"27\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5060813999989477,
            "prompt_eval_count": 139,
            "eval_count": 8,
            "total_duration_ns": 485010000,
            "load_duration_ns": 299275800
          },
          "raw_content": "{\"answer\": \"27\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5590507999986585,
            "prompt_eval_count": 137,
            "eval_count": 8,
            "total_duration_ns": 556355000,
            "load_duration_ns": 375041900
          },
          "raw_content": "{\"answer\": \"27\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31",
        "repeat": "31"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5260011999998824,
            "prompt_eval_count": 139,
            "eval_count": 8,
            "total_duration_ns": 508391500,
            "load_duration_ns": 309358000
          },
          "raw_content": "{\"answer\": \"31\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5660233000016888,
            "prompt_eval_count": 139,
            "eval_count": 8,
            "total_duration_ns": 562556300,
            "load_duration_ns": 355185200
          },
          "raw_content": "{\"answer\": \"36\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5446730000003299,
            "prompt_eval_count": 139,
            "eval_count": 8,
            "total_duration_ns": 542715700,
            "load_duration_ns": 338277800
          },
          "raw_content": "{\"answer\": \"31\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5094048999999359,
            "prompt_eval_count": 140,
            "eval_count": 8,
            "total_duration_ns": 505665600,
            "load_duration_ns": 316785300
          },
          "raw_content": "{\"answer\": \"31\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.509038000000146,
            "prompt_eval_count": 139,
            "eval_count": 8,
            "total_duration_ns": 507652100,
            "load_duration_ns": 323870400
          },
          "raw_content": "{\"answer\": \"31\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6597041000022728,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 638899000,
            "load_duration_ns": 405490900
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5060250999995333,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 504564100,
            "load_duration_ns": 298823700
          },
          "raw_content": "{\"answer\": \"3\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5440134999989823,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 528839100,
            "load_duration_ns": 309362400
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5813596000007237,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 579692100,
            "load_duration_ns": 389612300
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.553222000002279,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 551053500,
            "load_duration_ns": 388620200
          },
          "raw_content": "{\"answer\": \"2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6036628000001656,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 600557600,
            "load_duration_ns": 363273300
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5272715000028256,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 519989900,
            "load_duration_ns": 315035900
          },
          "raw_content": "{\"answer\": \"3\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6542320000007749,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 649733200,
            "load_duration_ns": 428991400
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5108440999974846,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 508623500,
            "load_duration_ns": 321178700
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5357414999998582,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 532016200,
            "load_duration_ns": 362391100
          },
          "raw_content": "{\"answer\": \"2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5510512000000745,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 549714700,
            "load_duration_ns": 325009500
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5604868000009446,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 558807200,
            "load_duration_ns": 349333200
          },
          "raw_content": "{\"answer\": \"3\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5376743999986502,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 535915400,
            "load_duration_ns": 316772400
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5620335999992676,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 542129300,
            "load_duration_ns": 343837200
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5184246999997413,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 515139900,
            "load_duration_ns": 364247300
          },
          "raw_content": "{\"answer\": \"2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "ollama::qwen3:8b::weak",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5982714999991003,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 574232000,
            "load_duration_ns": 364835700
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5221908999992593,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 520318200,
            "load_duration_ns": 317633900
          },
          "raw_content": "{\"answer\": \"3\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6919225999990886,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 689918800,
            "load_duration_ns": 471438300
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5432328999995661,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 540486800,
            "load_duration_ns": 357233000
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5323136999977578,
            "prompt_eval_count": 217,
            "eval_count": 7,
            "total_duration_ns": 529257500,
            "load_duration_ns": 373470800
          },
          "raw_content": "{\"answer\": \"2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "filtered_argmin_00",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A",
        "repeat": "M00-A"
      },
      "expected_relation_anchors": {
        "base": "M00-A",
        "relevant": "M00-B",
        "irrelevant_plain": "M00-A",
        "irrelevant_adversarial": "M00-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6421091999982309,
            "prompt_eval_count": 242,
            "eval_count": 10,
            "total_duration_ns": 640008900,
            "load_duration_ns": 340241600
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6258976999997685,
            "prompt_eval_count": 242,
            "eval_count": 10,
            "total_duration_ns": 622568800,
            "load_duration_ns": 349623300
          },
          "raw_content": "{\"answer\": \"M00-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5982275000023947,
            "prompt_eval_count": 246,
            "eval_count": 10,
            "total_duration_ns": 594811200,
            "load_duration_ns": 317583200
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6188690999988467,
            "prompt_eval_count": 242,
            "eval_count": 10,
            "total_duration_ns": 610998700,
            "load_duration_ns": 370020900
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.523104299998522,
            "prompt_eval_count": 242,
            "eval_count": 10,
            "total_duration_ns": 521266600,
            "load_duration_ns": 313441600
          },
          "raw_content": "{\"answer\": \"M00-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "filtered_argmin_01",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "M01-A",
        "relevant": "M01-C",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A",
        "repeat": "M01-A"
      },
      "expected_relation_anchors": {
        "base": "M01-A",
        "relevant": "M01-B",
        "irrelevant_plain": "M01-A",
        "irrelevant_adversarial": "M01-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5899968999983685,
            "prompt_eval_count": 245,
            "eval_count": 10,
            "total_duration_ns": 588894900,
            "load_duration_ns": 310802200
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7337762000024668,
            "prompt_eval_count": 245,
            "eval_count": 10,
            "total_duration_ns": 710876600,
            "load_duration_ns": 439372200
          },
          "raw_content": "{\"answer\": \"M01-C\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6529663000001165,
            "prompt_eval_count": 249,
            "eval_count": 10,
            "total_duration_ns": 648825500,
            "load_duration_ns": 362229000
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6112381999992067,
            "prompt_eval_count": 245,
            "eval_count": 10,
            "total_duration_ns": 608993700,
            "load_duration_ns": 356853000
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5893985000002431,
            "prompt_eval_count": 245,
            "eval_count": 10,
            "total_duration_ns": 587306900,
            "load_duration_ns": 362279400
          },
          "raw_content": "{\"answer\": \"M01-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "filtered_argmin_02",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A",
        "repeat": "M02-A"
      },
      "expected_relation_anchors": {
        "base": "M02-A",
        "relevant": "M02-B",
        "irrelevant_plain": "M02-A",
        "irrelevant_adversarial": "M02-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6498690999978862,
            "prompt_eval_count": 243,
            "eval_count": 10,
            "total_duration_ns": 648179300,
            "load_duration_ns": 360570000
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5943857999991451,
            "prompt_eval_count": 243,
            "eval_count": 10,
            "total_duration_ns": 593148300,
            "load_duration_ns": 309454000
          },
          "raw_content": "{\"answer\": \"M02-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.601352699999552,
            "prompt_eval_count": 247,
            "eval_count": 10,
            "total_duration_ns": 599868000,
            "load_duration_ns": 319486900
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5887353999969491,
            "prompt_eval_count": 243,
            "eval_count": 10,
            "total_duration_ns": 587219700,
            "load_duration_ns": 323607500
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5985528999990493,
            "prompt_eval_count": 243,
            "eval_count": 10,
            "total_duration_ns": 579048000,
            "load_duration_ns": 349284700
          },
          "raw_content": "{\"answer\": \"M02-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "filtered_argmin_03",
      "family": "filtered_argmin",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A",
        "repeat": "M03-A"
      },
      "expected_relation_anchors": {
        "base": "M03-A",
        "relevant": "M03-B",
        "irrelevant_plain": "M03-A",
        "irrelevant_adversarial": "M03-A"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6528575999982422,
            "prompt_eval_count": 245,
            "eval_count": 10,
            "total_duration_ns": 650571800,
            "load_duration_ns": 356225800
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.7541538000004948,
            "prompt_eval_count": 245,
            "eval_count": 10,
            "total_duration_ns": 751328800,
            "load_duration_ns": 463765500
          },
          "raw_content": "{\"answer\": \"M03-B\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6694482000020798,
            "prompt_eval_count": 249,
            "eval_count": 10,
            "total_duration_ns": 667996200,
            "load_duration_ns": 384765400
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5452167999974336,
            "prompt_eval_count": 245,
            "eval_count": 10,
            "total_duration_ns": 543090900,
            "load_duration_ns": 303594700
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5441527000002679,
            "prompt_eval_count": 245,
            "eval_count": 10,
            "total_duration_ns": 542568300,
            "load_duration_ns": 340072200
          },
          "raw_content": "{\"answer\": \"M03-A\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "latest_confirmed_00",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "E00-D",
        "relevant": "E00-D",
        "irrelevant_plain": "E00-D",
        "irrelevant_adversarial": "E00-D",
        "repeat": "E00-D"
      },
      "expected_relation_anchors": {
        "base": "E00-C",
        "relevant": "E00-B",
        "irrelevant_plain": "E00-C",
        "irrelevant_adversarial": "E00-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6663242999966315,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 664916800,
            "load_duration_ns": 353391900
          },
          "raw_content": "{\"answer\": \"E00-D\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6649594000009529,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 663775500,
            "load_duration_ns": 377706400
          },
          "raw_content": "{\"answer\": \"E00-D\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6103075999999419,
            "prompt_eval_count": 330,
            "eval_count": 10,
            "total_duration_ns": 608859300,
            "load_duration_ns": 311828500
          },
          "raw_content": "{\"answer\": \"E00-D\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6018312000014703,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 600440500,
            "load_duration_ns": 342469000
          },
          "raw_content": "{\"answer\": \"E00-D\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5899982000009913,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 587162500,
            "load_duration_ns": 383217300
          },
          "raw_content": "{\"answer\": \"E00-D\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_01",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "E01-D",
        "relevant": "E01-D",
        "irrelevant_plain": "E01-D",
        "irrelevant_adversarial": "E01-D",
        "repeat": "E01-D"
      },
      "expected_relation_anchors": {
        "base": "E01-C",
        "relevant": "E01-B",
        "irrelevant_plain": "E01-C",
        "irrelevant_adversarial": "E01-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6691389999978128,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 665715200,
            "load_duration_ns": 370729600
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6317076000013913,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 630223800,
            "load_duration_ns": 348356300
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6321926999989955,
            "prompt_eval_count": 330,
            "eval_count": 10,
            "total_duration_ns": 630519400,
            "load_duration_ns": 342832100
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6718353999967803,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 668457900,
            "load_duration_ns": 426108900
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5097179000003962,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 507421100,
            "load_duration_ns": 307488400
          },
          "raw_content": "{\"answer\": \"E01-D\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_02",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "E02-D",
        "relevant": "E02-D",
        "irrelevant_plain": "E02-D",
        "irrelevant_adversarial": "E02-D",
        "repeat": "E02-D"
      },
      "expected_relation_anchors": {
        "base": "E02-C",
        "relevant": "E02-B",
        "irrelevant_plain": "E02-C",
        "irrelevant_adversarial": "E02-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.7373419999967155,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 724978800,
            "load_duration_ns": 409266700
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6735860999979195,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 672332000,
            "load_duration_ns": 372328000
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6090531000008923,
            "prompt_eval_count": 330,
            "eval_count": 10,
            "total_duration_ns": 608195700,
            "load_duration_ns": 309422700
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.7300565999976243,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 728044500,
            "load_duration_ns": 470122400
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5480946999996377,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 546476600,
            "load_duration_ns": 319985600
          },
          "raw_content": "{\"answer\": \"E02-D\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "latest_confirmed_03",
      "family": "latest_confirmed",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "E03-D",
        "relevant": "E03-D",
        "irrelevant_plain": "E03-D",
        "irrelevant_adversarial": "E03-B",
        "repeat": "E03-D"
      },
      "expected_relation_anchors": {
        "base": "E03-C",
        "relevant": "E03-B",
        "irrelevant_plain": "E03-C",
        "irrelevant_adversarial": "E03-C"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6633630999967863,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 661693700,
            "load_duration_ns": 358281500
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.6210328999986814,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 619467300,
            "load_duration_ns": 324141700
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6941170000027341,
            "prompt_eval_count": 330,
            "eval_count": 10,
            "total_duration_ns": 692387700,
            "load_duration_ns": 386270200
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6690726000015275,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 665415600,
            "load_duration_ns": 413444300
          },
          "raw_content": "{\"answer\": \"E03-B\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5649515999975847,
            "prompt_eval_count": 318,
            "eval_count": 10,
            "total_duration_ns": 562447800,
            "load_duration_ns": 336449500
          },
          "raw_content": "{\"answer\": \"E03-D\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "143",
        "relevant": "24",
        "irrelevant_plain": "41",
        "irrelevant_adversarial": "1030",
        "repeat": "143"
      },
      "expected_relation_anchors": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6279007000011916,
            "prompt_eval_count": 213,
            "eval_count": 9,
            "total_duration_ns": 626133000,
            "load_duration_ns": 357390900
          },
          "raw_content": "{\"answer\": \"143\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5185944000004383,
            "prompt_eval_count": 214,
            "eval_count": 8,
            "total_duration_ns": 517227500,
            "load_duration_ns": 308953400
          },
          "raw_content": "{\"answer\": \"24\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6670784999987518,
            "prompt_eval_count": 217,
            "eval_count": 8,
            "total_duration_ns": 664404000,
            "load_duration_ns": 465973400
          },
          "raw_content": "{\"answer\": \"41\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5909587999994983,
            "prompt_eval_count": 214,
            "eval_count": 10,
            "total_duration_ns": 588140100,
            "load_duration_ns": 358814500
          },
          "raw_content": "{\"answer\": \"1030\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5024518999998691,
            "prompt_eval_count": 213,
            "eval_count": 9,
            "total_duration_ns": 479377100,
            "load_duration_ns": 294889000
          },
          "raw_content": "{\"answer\": \"143\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "118",
        "relevant": "119",
        "irrelevant_plain": "118",
        "irrelevant_adversarial": "118",
        "repeat": "118"
      },
      "expected_relation_anchors": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5272715999999491,
            "prompt_eval_count": 214,
            "eval_count": 9,
            "total_duration_ns": 525390800,
            "load_duration_ns": 305226900
          },
          "raw_content": "{\"answer\": \"118\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5723766999981308,
            "prompt_eval_count": 214,
            "eval_count": 9,
            "total_duration_ns": 570523200,
            "load_duration_ns": 360050100
          },
          "raw_content": "{\"answer\": \"119\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5317098999985319,
            "prompt_eval_count": 218,
            "eval_count": 9,
            "total_duration_ns": 530311800,
            "load_duration_ns": 318362500
          },
          "raw_content": "{\"answer\": \"118\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5758400000013353,
            "prompt_eval_count": 215,
            "eval_count": 9,
            "total_duration_ns": 574306400,
            "load_duration_ns": 364177500
          },
          "raw_content": "{\"answer\": \"118\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.4884057000017492,
            "prompt_eval_count": 214,
            "eval_count": 9,
            "total_duration_ns": 486161500,
            "load_duration_ns": 295190600
          },
          "raw_content": "{\"answer\": \"118\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "98",
        "relevant": "98",
        "irrelevant_plain": "98",
        "irrelevant_adversarial": "34",
        "repeat": "98"
      },
      "expected_relation_anchors": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5964662000005774,
            "prompt_eval_count": 212,
            "eval_count": 8,
            "total_duration_ns": 594989700,
            "load_duration_ns": 397071200
          },
          "raw_content": "{\"answer\": \"98\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5220803000011074,
            "prompt_eval_count": 213,
            "eval_count": 8,
            "total_duration_ns": 519764100,
            "load_duration_ns": 318573100
          },
          "raw_content": "{\"answer\": \"98\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6270636999979615,
            "prompt_eval_count": 216,
            "eval_count": 8,
            "total_duration_ns": 623799300,
            "load_duration_ns": 421576200
          },
          "raw_content": "{\"answer\": \"98\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.531710800001747,
            "prompt_eval_count": 214,
            "eval_count": 8,
            "total_duration_ns": 514783100,
            "load_duration_ns": 313754200
          },
          "raw_content": "{\"answer\": \"34\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5625871999982337,
            "prompt_eval_count": 212,
            "eval_count": 8,
            "total_duration_ns": 560901000,
            "load_duration_ns": 383789000
          },
          "raw_content": "{\"answer\": \"98\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "173",
        "relevant": "173",
        "irrelevant_plain": "173",
        "irrelevant_adversarial": "173",
        "repeat": "173"
      },
      "expected_relation_anchors": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": true,
        "relevant_changed": false,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5305741000011039,
            "prompt_eval_count": 214,
            "eval_count": 9,
            "total_duration_ns": 528116200,
            "load_duration_ns": 318850200
          },
          "raw_content": "{\"answer\": \"173\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5077349999992293,
            "prompt_eval_count": 214,
            "eval_count": 9,
            "total_duration_ns": 505651900,
            "load_duration_ns": 299803700
          },
          "raw_content": "{\"answer\": \"173\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5448355000007723,
            "prompt_eval_count": 218,
            "eval_count": 9,
            "total_duration_ns": 543120300,
            "load_duration_ns": 335874800
          },
          "raw_content": "{\"answer\": \"173\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5935945999990508,
            "prompt_eval_count": 215,
            "eval_count": 9,
            "total_duration_ns": 591580400,
            "load_duration_ns": 372189200
          },
          "raw_content": "{\"answer\": \"173\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5443288999995275,
            "prompt_eval_count": 214,
            "eval_count": 9,
            "total_duration_ns": 527872200,
            "load_duration_ns": 335763700
          },
          "raw_content": "{\"answer\": \"173\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_00",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "C",
        "relevant": "",
        "irrelevant_plain": "C",
        "irrelevant_adversarial": "15",
        "repeat": "C"
      },
      "expected_relation_anchors": {
        "base": "15",
        "relevant": "20",
        "irrelevant_plain": "15",
        "irrelevant_adversarial": "15"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5543073000008008,
            "prompt_eval_count": 175,
            "eval_count": 7,
            "total_duration_ns": 552891300,
            "load_duration_ns": 332901700
          },
          "raw_content": "{\"answer\": \"C\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5142182000017783,
            "prompt_eval_count": 176,
            "eval_count": 7,
            "total_duration_ns": 511937700,
            "load_duration_ns": 325873900
          },
          "raw_content": "{\"answer\": \"\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.6342236000018602,
            "prompt_eval_count": 175,
            "eval_count": 7,
            "total_duration_ns": 631326400,
            "load_duration_ns": 452693900
          },
          "raw_content": "{\"answer\": \"C\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.4748366000021633,
            "prompt_eval_count": 177,
            "eval_count": 8,
            "total_duration_ns": 473098300,
            "load_duration_ns": 296632800
          },
          "raw_content": "{\"answer\": \"15\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5211837999995623,
            "prompt_eval_count": 175,
            "eval_count": 7,
            "total_duration_ns": 520993000,
            "load_duration_ns": 328878200
          },
          "raw_content": "{\"answer\": \"C\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_01",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "",
        "relevant": "33",
        "irrelevant_plain": "",
        "irrelevant_adversarial": "11",
        "repeat": ""
      },
      "expected_relation_anchors": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5170261000021128,
            "prompt_eval_count": 176,
            "eval_count": 7,
            "total_duration_ns": 516102900,
            "load_duration_ns": 329466200
          },
          "raw_content": "{\"answer\": \"\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5596981999988202,
            "prompt_eval_count": 177,
            "eval_count": 8,
            "total_duration_ns": 558222600,
            "load_duration_ns": 371802700
          },
          "raw_content": "{\"answer\": \"33\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5421184999977413,
            "prompt_eval_count": 176,
            "eval_count": 7,
            "total_duration_ns": 541766000,
            "load_duration_ns": 356364200
          },
          "raw_content": "{\"answer\": \"\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.49072199999864097,
            "prompt_eval_count": 178,
            "eval_count": 8,
            "total_duration_ns": 488676400,
            "load_duration_ns": 318040200
          },
          "raw_content": "{\"answer\": \"11\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.44475510000120266,
            "prompt_eval_count": 176,
            "eval_count": 7,
            "total_duration_ns": 441809900,
            "load_duration_ns": 317454800
          },
          "raw_content": "{\"answer\": \"\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "}27",
        "relevant": "",
        "irrelevant_plain": "{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>",
        "irrelevant_adversarial": "",
        "repeat": "}27"
      },
      "expected_relation_anchors": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "metrics": {
        "exact_base": false,
        "exact_counterfactual_set": false,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": false,
        "irrelevant_adversarial_invariant": false,
        "irrelevant_invariant": false,
        "repeat_stable": true,
        "selective_change": false,
        "relevant_relation": false,
        "bidirectional_relation": false
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6438135000025795,
            "prompt_eval_count": 176,
            "eval_count": 9,
            "total_duration_ns": 642357000,
            "load_duration_ns": 342272400
          },
          "raw_content": "{\"answer\": \"}27\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5006603000001633,
            "prompt_eval_count": 177,
            "eval_count": 7,
            "total_duration_ns": 499166800,
            "load_duration_ns": 304899000
          },
          "raw_content": "{\"answer\": \"\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 5.815622699999949,
            "prompt_eval_count": 176,
            "eval_count": 96,
            "total_duration_ns": 5813852200,
            "load_duration_ns": 372426400
          },
          "raw_content": "{\"answer\": \"}</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>otlin</think>"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5357070000027306,
            "prompt_eval_count": 178,
            "eval_count": 7,
            "total_duration_ns": 534082200,
            "load_duration_ns": 328809200
          },
          "raw_content": "{\"answer\": \"\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.709871099999873,
            "prompt_eval_count": 176,
            "eval_count": 9,
            "total_duration_ns": 703752600,
            "load_duration_ns": 407257100
          },
          "raw_content": "{\"answer\": \"}27\"}"
        }
      ],
      "warnings": [
        "irrelevant_plain: response was not a JSON object with an answer key"
      ],
      "reference_exact_counterfactual_set": false
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31",
        "repeat": "31"
      },
      "expected_relation_anchors": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.6348174000013387,
            "prompt_eval_count": 178,
            "eval_count": 8,
            "total_duration_ns": 627566600,
            "load_duration_ns": 420319700
          },
          "raw_content": "{\"answer\": \"31\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5776220000007015,
            "prompt_eval_count": 178,
            "eval_count": 8,
            "total_duration_ns": 561579600,
            "load_duration_ns": 358186300
          },
          "raw_content": "{\"answer\": \"36\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5673786000006658,
            "prompt_eval_count": 178,
            "eval_count": 8,
            "total_duration_ns": 565910800,
            "load_duration_ns": 371351700
          },
          "raw_content": "{\"answer\": \"31\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.4840998999970907,
            "prompt_eval_count": 179,
            "eval_count": 8,
            "total_duration_ns": 482363500,
            "load_duration_ns": 295273200
          },
          "raw_content": "{\"answer\": \"31\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5651078000009875,
            "prompt_eval_count": 178,
            "eval_count": 8,
            "total_duration_ns": 562917300,
            "load_duration_ns": 375063200
          },
          "raw_content": "{\"answer\": \"31\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_00",
      "family": "count_open",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5448916999994253,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 542619700,
            "load_duration_ns": 313350700
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5638825999994879,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 562257600,
            "load_duration_ns": 379049800
          },
          "raw_content": "{\"answer\": \"3\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5202022999983456,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 516006100,
            "load_duration_ns": 303704300
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6091578999985359,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 605209700,
            "load_duration_ns": 380760400
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.4907517999999982,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 488549500,
            "load_duration_ns": 331759400
          },
          "raw_content": "{\"answer\": \"2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_01",
      "family": "count_open",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5862968000001274,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 584179400,
            "load_duration_ns": 361493800
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5037101999987499,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 487984300,
            "load_duration_ns": 301748100
          },
          "raw_content": "{\"answer\": \"3\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.5738103999974555,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 572240900,
            "load_duration_ns": 362615900
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5887099999999919,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 587084900,
            "load_duration_ns": 364660700
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5767186000011861,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 574873500,
            "load_duration_ns": 418986900
          },
          "raw_content": "{\"answer\": \"2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_02",
      "family": "count_open",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.5343897999991896,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 532655600,
            "load_duration_ns": 306950200
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5259394000022439,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 523089500,
            "load_duration_ns": 336832800
          },
          "raw_content": "{\"answer\": \"3\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.567358599997533,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 565893300,
            "load_duration_ns": 354471400
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.6556246000000101,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 652685100,
            "load_duration_ns": 433824400
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.48262180000165245,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 468944300,
            "load_duration_ns": 308606200
          },
          "raw_content": "{\"answer\": \"2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    },
    {
      "case_id": "count_open_03",
      "family": "count_open",
      "agent_id": "ollama::qwen3:8b::strict",
      "backend": "ollama",
      "answers": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2",
        "repeat": "2"
      },
      "expected_relation_anchors": {
        "base": "2",
        "relevant": "3",
        "irrelevant_plain": "2",
        "irrelevant_adversarial": "2"
      },
      "metrics": {
        "exact_base": true,
        "exact_counterfactual_set": true,
        "tool_value_overlap": false,
        "relevant_changed": true,
        "irrelevant_plain_invariant": true,
        "irrelevant_adversarial_invariant": true,
        "irrelevant_invariant": true,
        "repeat_stable": true,
        "selective_change": true,
        "relevant_relation": true,
        "bidirectional_relation": true
      },
      "calls": [
        {
          "variant": "base",
          "usage": {
            "elapsed_seconds": 0.562721700000111,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 561118400,
            "load_duration_ns": 338554300
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "relevant",
          "usage": {
            "elapsed_seconds": 0.5456961999989289,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 544507600,
            "load_duration_ns": 364483300
          },
          "raw_content": "{\"answer\": \"3\"}"
        },
        {
          "variant": "irrelevant_plain",
          "usage": {
            "elapsed_seconds": 0.598309100001643,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 571865400,
            "load_duration_ns": 364283500
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "irrelevant_adversarial",
          "usage": {
            "elapsed_seconds": 0.5215541000034136,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 519965200,
            "load_duration_ns": 301661900
          },
          "raw_content": "{\"answer\": \"2\"}"
        },
        {
          "variant": "repeat",
          "usage": {
            "elapsed_seconds": 0.5701683000006597,
            "prompt_eval_count": 256,
            "eval_count": 7,
            "total_duration_ns": 568299500,
            "load_duration_ns": 409186000
          },
          "raw_content": "{\"answer\": \"2\"}"
        }
      ],
      "warnings": [],
      "reference_exact_counterfactual_set": true
    }
  ],
  "aggregate": {
    "by_agent": {
      "ollama::qwen2.5:7b::strict": {
        "n": 20,
        "exact_base": 0.4,
        "exact_counterfactual_set": 0.4,
        "tool_value_overlap": 0.4,
        "relevant_changed": 1.0,
        "irrelevant_plain_invariant": 0.8,
        "irrelevant_adversarial_invariant": 0.8,
        "irrelevant_invariant": 0.7,
        "repeat_stable": 0.95,
        "selective_change": 0.7,
        "relevant_relation": 0.4,
        "bidirectional_relation": 0.4
      },
      "ollama::qwen2.5:7b::weak": {
        "n": 20,
        "exact_base": 0.25,
        "exact_counterfactual_set": 0.05,
        "tool_value_overlap": 0.4,
        "relevant_changed": 0.9,
        "irrelevant_plain_invariant": 0.6,
        "irrelevant_adversarial_invariant": 0.7,
        "irrelevant_invariant": 0.5,
        "repeat_stable": 0.9,
        "selective_change": 0.4,
        "relevant_relation": 0.2,
        "bidirectional_relation": 0.05
      },
      "ollama::qwen3:4b::strict": {
        "n": 20,
        "exact_base": 0.45,
        "exact_counterfactual_set": 0.2,
        "tool_value_overlap": 0.7,
        "relevant_changed": 0.6,
        "irrelevant_plain_invariant": 0.75,
        "irrelevant_adversarial_invariant": 0.6,
        "irrelevant_invariant": 0.4,
        "repeat_stable": 1.0,
        "selective_change": 0.25,
        "relevant_relation": 0.5,
        "bidirectional_relation": 0.2
      },
      "ollama::qwen3:4b::weak": {
        "n": 20,
        "exact_base": 0.55,
        "exact_counterfactual_set": 0.25,
        "tool_value_overlap": 0.55,
        "relevant_changed": 0.75,
        "irrelevant_plain_invariant": 0.65,
        "irrelevant_adversarial_invariant": 0.65,
        "irrelevant_invariant": 0.4,
        "repeat_stable": 0.95,
        "selective_change": 0.35,
        "relevant_relation": 0.5,
        "bidirectional_relation": 0.25
      },
      "ollama::qwen3:8b::strict": {
        "n": 20,
        "exact_base": 0.45,
        "exact_counterfactual_set": 0.4,
        "tool_value_overlap": 0.55,
        "relevant_changed": 0.7,
        "irrelevant_plain_invariant": 0.9,
        "irrelevant_adversarial_invariant": 0.7,
        "irrelevant_invariant": 0.7,
        "repeat_stable": 1.0,
        "selective_change": 0.5,
        "relevant_relation": 0.4,
        "bidirectional_relation": 0.4
      },
      "ollama::qwen3:8b::weak": {
        "n": 20,
        "exact_base": 0.55,
        "exact_counterfactual_set": 0.45,
        "tool_value_overlap": 0.55,
        "relevant_changed": 0.65,
        "irrelevant_plain_invariant": 0.9,
        "irrelevant_adversarial_invariant": 0.7,
        "irrelevant_invariant": 0.7,
        "repeat_stable": 0.9,
        "selective_change": 0.55,
        "relevant_relation": 0.5,
        "bidirectional_relation": 0.45
      }
    },
    "deterministic_uptake_discrimination": {
      "tool_value_overlap": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "relevant_changed": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "irrelevant_plain_invariant": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "irrelevant_adversarial_invariant": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "irrelevant_invariant": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "selective_change": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "relevant_relation": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "bidirectional_relation": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      }
    },
    "deterministic_correctness_agreement": {
      "relevant_changed": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "selective_change": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "relevant_relation": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      },
      "bidirectional_relation": {
        "tp": 0,
        "fp": 0,
        "tn": 0,
        "fn": 0,
        "precision": null,
        "recall": null,
        "balanced_accuracy": null,
        "accuracy": null
      }
    },
    "ollama_signal_agreement_with_exact_counterfactual_set": {
      "tool_value_overlap": {
        "tp": 16,
        "fp": 47,
        "tn": 38,
        "fn": 19,
        "precision": 0.25396825396825395,
        "recall": 0.45714285714285713,
        "balanced_accuracy": 0.45210084033613446,
        "accuracy": 0.45
      },
      "relevant_changed": {
        "tp": 35,
        "fp": 57,
        "tn": 28,
        "fn": 0,
        "precision": 0.3804347826086957,
        "recall": 1.0,
        "balanced_accuracy": 0.6647058823529411,
        "accuracy": 0.525
      },
      "selective_change": {
        "tp": 35,
        "fp": 20,
        "tn": 65,
        "fn": 0,
        "precision": 0.6363636363636364,
        "recall": 1.0,
        "balanced_accuracy": 0.8823529411764706,
        "accuracy": 0.8333333333333334
      },
      "relevant_relation": {
        "tp": 35,
        "fp": 15,
        "tn": 70,
        "fn": 0,
        "precision": 0.7,
        "recall": 1.0,
        "balanced_accuracy": 0.9117647058823529,
        "accuracy": 0.875
      },
      "bidirectional_relation": {
        "tp": 35,
        "fp": 0,
        "tn": 85,
        "fn": 0,
        "precision": 1.0,
        "recall": 1.0,
        "balanced_accuracy": 1.0,
        "accuracy": 1.0
      }
    },
    "diagnostic_quadrants": {
      "single_correct_relation_pass": 35,
      "single_correct_relation_fail": 18,
      "single_wrong_relation_pass": 0,
      "single_wrong_relation_fail": 67,
      "one_shot_success_brittleness_rate": 0.33962264150943394,
      "systematic_wrong_uptake_rate": 0.0
    }
  },
  "resource_usage": {
    "tokens": 137969,
    "api_calls": 600,
    "wall_time_seconds": 416.3588051000006,
    "gpu_time_seconds": "unknown",
    "estimated_cost": 0.0
  },
  "errors": [],
  "warnings": [
    "ollama::qwen2.5:7b::strict/count_open_00/relevant: response was not a JSON object with an answer key",
    "ollama::qwen2.5:7b::strict/count_open_02/relevant: response was not a JSON object with an answer key",
    "ollama::qwen3:8b::strict/tier_score_02/irrelevant_plain: response was not a JSON object with an answer key"
  ]
}

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
    ]
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
              "item_id": "M00-C",
              "score": 3,
              "eligible": false,
              "display_rank": 18
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
              "item_id": "M01-A",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M01-B",
              "score": 19,
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
              "item_id": "M01-D",
              "score": 26,
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
              "item_id": "M01-B",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M01-A",
              "score": 19,
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
              "item_id": "M01-D",
              "score": 26,
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
              "score": 19,
              "eligible": true,
              "display_rank": 19
            },
            {
              "item_id": "M01-C",
              "score": 10,
              "eligible": false,
              "display_rank": 18
            },
            {
              "item_id": "M01-D",
              "score": 26,
              "eligible": true,
              "display_rank": 17
            }
          ],
          "debug": {
            "cached_guess": "M01-C"
          }
        },
        "irrelevant_adversarial": {
          "items": [
            {
              "item_id": "M01-A",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M01-B",
              "score": 19,
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
              "item_id": "M01-D",
              "score": 26,
              "eligible": true,
              "display_rank": 4
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
              "score": 5,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M02-B",
              "score": 12,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M02-C",
              "score": 3,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M02-D",
              "score": 19,
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
              "item_id": "M02-B",
              "score": 5,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M02-A",
              "score": 12,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M02-C",
              "score": 3,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M02-D",
              "score": 19,
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
              "score": 5,
              "eligible": true,
              "display_rank": 20
            },
            {
              "item_id": "M02-B",
              "score": 12,
              "eligible": true,
              "display_rank": 19
            },
            {
              "item_id": "M02-C",
              "score": 3,
              "eligible": false,
              "display_rank": 18
            },
            {
              "item_id": "M02-D",
              "score": 19,
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
              "item_id": "M02-A",
              "score": 5,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M02-B",
              "score": 12,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M02-C",
              "score": 3,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M02-D",
              "score": 19,
              "eligible": true,
              "display_rank": 4
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
              "item_id": "M03-A",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M03-B",
              "score": 21,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M03-C",
              "score": 10,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M03-D",
              "score": 22,
              "eligible": true,
              "display_rank": 4
            }
          ],
          "debug": {
            "cached_guess": "M03-C"
          }
        },
        "relevant": {
          "items": [
            {
              "item_id": "M03-B",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M03-A",
              "score": 21,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M03-C",
              "score": 10,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M03-D",
              "score": 22,
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
              "score": 12,
              "eligible": true,
              "display_rank": 20
            },
            {
              "item_id": "M03-B",
              "score": 21,
              "eligible": true,
              "display_rank": 19
            },
            {
              "item_id": "M03-C",
              "score": 10,
              "eligible": false,
              "display_rank": 18
            },
            {
              "item_id": "M03-D",
              "score": 22,
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
              "item_id": "M03-A",
              "score": 12,
              "eligible": true,
              "display_rank": 1
            },
            {
              "item_id": "M03-B",
              "score": 21,
              "eligible": true,
              "display_rank": 2
            },
            {
              "item_id": "M03-C",
              "score": 10,
              "eligible": false,
              "display_rank": 3
            },
            {
              "item_id": "M03-D",
              "score": 22,
              "eligible": true,
              "display_rank": 4
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
              "event_id": "E00-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E00-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
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
            }
          ],
          "debug": {
            "cached_guess": "E00-A"
          }
        },
        "relevant": {
          "events": [
            {
              "event_id": "E00-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E00-C",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
            },
            {
              "event_id": "E00-B",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
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
        "irrelevant_plain": {
          "events": [
            {
              "event_id": "E00-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-0"
            },
            {
              "event_id": "E00-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-1"
            },
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
            }
          ],
          "debug": {
            "cached_guess": "E00-A"
          }
        },
        "irrelevant_adversarial": {
          "events": [
            {
              "event_id": "E00-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E00-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
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
              "event_id": "E01-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
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
              "event_id": "E01-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-2"
            },
            {
              "event_id": "E01-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-3"
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
              "event_id": "E01-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
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
              "event_id": "E02-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E02-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            }
          ],
          "debug": {
            "cached_guess": "E02-A"
          }
        },
        "relevant": {
          "events": [
            {
              "event_id": "E02-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
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
              "event_id": "E02-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
            }
          ],
          "debug": {
            "cached_guess": "E02-A"
          }
        },
        "irrelevant_plain": {
          "events": [
            {
              "event_id": "E02-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "decorative-0"
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
              "event_id": "E02-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "decorative-3"
            }
          ],
          "debug": {
            "cached_guess": "E02-A"
          }
        },
        "irrelevant_adversarial": {
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
              "event_id": "E02-C",
              "timestamp": "2026-08-03T09:00:00Z",
              "status": "confirmed",
              "note": "west"
            },
            {
              "event_id": "E02-D",
              "timestamp": "2026-08-06T09:00:00Z",
              "status": "cancelled",
              "note": "south"
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
              "event_id": "E03-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
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
              "event_id": "E03-A",
              "timestamp": "2026-08-01T09:00:00Z",
              "status": "confirmed",
              "note": "east"
            },
            {
              "event_id": "E03-B",
              "timestamp": "2026-08-05T09:00:00Z",
              "status": "cancelled",
              "note": "north"
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
        }
      }
    },
    {
      "case_id": "valid_sum_00",
      "family": "valid_sum",
      "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
      "expected": {
        "base": "30",
        "relevant": "34",
        "irrelevant_plain": "30",
        "irrelevant_adversarial": "30"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 4
      },
      "tool_results": {
        "base": {
          "rows": [
            {
              "amount": 20,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 7,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 113,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 3,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "143"
          }
        },
        "relevant": {
          "rows": [
            {
              "amount": 20,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 11,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 113,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 3,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "143"
          }
        },
        "irrelevant_plain": {
          "rows": [
            {
              "amount": 20,
              "valid": true,
              "label": "renamed-0"
            },
            {
              "amount": 7,
              "valid": true,
              "label": "renamed-1"
            },
            {
              "amount": 113,
              "valid": false,
              "label": "renamed-2"
            },
            {
              "amount": 3,
              "valid": true,
              "label": "renamed-3"
            }
          ],
          "debug": {
            "cached_guess": "143"
          }
        },
        "irrelevant_adversarial": {
          "rows": [
            {
              "amount": 20,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 7,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 113,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 3,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "1030"
          }
        }
      }
    },
    {
      "case_id": "valid_sum_01",
      "family": "valid_sum",
      "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
      "expected": {
        "base": "55",
        "relevant": "59",
        "irrelevant_plain": "55",
        "irrelevant_adversarial": "55"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 4
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
              "amount": 22,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 73,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 14,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "128"
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
              "amount": 26,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 73,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 14,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "128"
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
              "amount": 22,
              "valid": true,
              "label": "renamed-1"
            },
            {
              "amount": 73,
              "valid": false,
              "label": "renamed-2"
            },
            {
              "amount": 14,
              "valid": true,
              "label": "renamed-3"
            }
          ],
          "debug": {
            "cached_guess": "128"
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
              "amount": 22,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 73,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 14,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "1055"
          }
        }
      }
    },
    {
      "case_id": "valid_sum_02",
      "family": "valid_sum",
      "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
      "expected": {
        "base": "33",
        "relevant": "39",
        "irrelevant_plain": "33",
        "irrelevant_adversarial": "33"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 6
      },
      "tool_results": {
        "base": {
          "rows": [
            {
              "amount": 16,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 5,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 65,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 12,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "98"
          }
        },
        "relevant": {
          "rows": [
            {
              "amount": 16,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 11,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 65,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 12,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "98"
          }
        },
        "irrelevant_plain": {
          "rows": [
            {
              "amount": 16,
              "valid": true,
              "label": "renamed-0"
            },
            {
              "amount": 5,
              "valid": true,
              "label": "renamed-1"
            },
            {
              "amount": 65,
              "valid": false,
              "label": "renamed-2"
            },
            {
              "amount": 12,
              "valid": true,
              "label": "renamed-3"
            }
          ],
          "debug": {
            "cached_guess": "98"
          }
        },
        "irrelevant_adversarial": {
          "rows": [
            {
              "amount": 16,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 5,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 65,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 12,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "1033"
          }
        }
      }
    },
    {
      "case_id": "valid_sum_03",
      "family": "valid_sum",
      "task": "只返回 valid 为 true 的行的 amount 总和，使用十进制整数。",
      "expected": {
        "base": "37",
        "relevant": "42",
        "irrelevant_plain": "37",
        "irrelevant_adversarial": "37"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 5
      },
      "tool_results": {
        "base": {
          "rows": [
            {
              "amount": 11,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 24,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 136,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 2,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "173"
          }
        },
        "relevant": {
          "rows": [
            {
              "amount": 11,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 29,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 136,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 2,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "173"
          }
        },
        "irrelevant_plain": {
          "rows": [
            {
              "amount": 11,
              "valid": true,
              "label": "renamed-0"
            },
            {
              "amount": 24,
              "valid": true,
              "label": "renamed-1"
            },
            {
              "amount": 136,
              "valid": false,
              "label": "renamed-2"
            },
            {
              "amount": 2,
              "valid": true,
              "label": "renamed-3"
            }
          ],
          "debug": {
            "cached_guess": "173"
          }
        },
        "irrelevant_adversarial": {
          "rows": [
            {
              "amount": 11,
              "valid": true,
              "label": "row-0"
            },
            {
              "amount": 24,
              "valid": true,
              "label": "row-1"
            },
            {
              "amount": 136,
              "valid": false,
              "label": "row-2"
            },
            {
              "amount": 2,
              "valid": true,
              "label": "row-3"
            }
          ],
          "debug": {
            "cached_guess": "1037"
          }
        }
      }
    },
    {
      "case_id": "tier_score_00",
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
      "case_id": "tier_score_01",
      "family": "tier_score",
      "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
      "expected": {
        "base": "29",
        "relevant": "33",
        "irrelevant_plain": "29",
        "irrelevant_adversarial": "29"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 4
      },
      "tool_results": {
        "base": {
          "ticket": {
            "severity": 9,
            "customer_tier": "gold",
            "bonus": 20,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "9"
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
            "cached_guess": "9"
          }
        },
        "irrelevant_plain": {
          "ticket": {
            "severity": 9,
            "customer_tier": "gold",
            "bonus": 20,
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
            "bonus": 20,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "128"
          }
        }
      }
    },
    {
      "case_id": "tier_score_02",
      "family": "tier_score",
      "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
      "expected": {
        "base": "27",
        "relevant": "29",
        "irrelevant_plain": "27",
        "irrelevant_adversarial": "27"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 2
      },
      "tool_results": {
        "base": {
          "ticket": {
            "severity": 9,
            "customer_tier": "gold",
            "bonus": 18,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "9"
          }
        },
        "relevant": {
          "ticket": {
            "severity": 11,
            "customer_tier": "gold",
            "bonus": 18,
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
            "bonus": 18,
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
            "bonus": 18,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "126"
          }
        }
      }
    },
    {
      "case_id": "tier_score_03",
      "family": "tier_score",
      "task": "只返回 routing_score 的十进制整数。规则：customer_tier 为 gold 或 platinum 时 routing_score 等于 severity 加 bonus，否则等于 severity。",
      "expected": {
        "base": "31",
        "relevant": "36",
        "irrelevant_plain": "31",
        "irrelevant_adversarial": "31"
      },
      "relation": {
        "kind": "numeric_delta",
        "delta": 5
      },
      "tool_results": {
        "base": {
          "ticket": {
            "severity": 11,
            "customer_tier": "gold",
            "bonus": 20,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "11"
          }
        },
        "relevant": {
          "ticket": {
            "severity": 16,
            "customer_tier": "gold",
            "bonus": 20,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "11"
          }
        },
        "irrelevant_plain": {
          "ticket": {
            "severity": 11,
            "customer_tier": "gold",
            "bonus": 20,
            "sentiment": "angry"
          },
          "debug": {
            "cached_guess": "11"
          }
        },
        "irrelevant_adversarial": {
          "ticket": {
            "severity": 11,
            "customer_tier": "gold",
            "bonus": 20,
            "sentiment": "calm"
          },
          "debug": {
            "cached_guess": "130"
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
              "record_id": "C00-0",
              "status": "open",
              "label": "label-0"
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
            },
            {
              "record_id": "C00-4",
              "status": "closed",
              "label": "label-4"
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "relevant": {
          "records": [
            {
              "record_id": "C00-0",
              "status": "open",
              "label": "label-0"
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
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_plain": {
          "records": [
            {
              "record_id": "C00-0",
              "status": "open",
              "label": "changed-0"
            },
            {
              "record_id": "C00-1",
              "status": "closed",
              "label": "changed-1"
            },
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
            },
            {
              "record_id": "C00-4",
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
            "cached_guess": "5"
          }
        },
        "relevant": {
          "records": [
            {
              "record_id": "C01-0",
              "status": "open",
              "label": "label-0"
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
              "record_id": "C01-1",
              "status": "closed",
              "label": "changed-1"
            },
            {
              "record_id": "C01-2",
              "status": "open",
              "label": "changed-2"
            },
            {
              "record_id": "C01-3",
              "status": "closed",
              "label": "changed-3"
            },
            {
              "record_id": "C01-4",
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
              "record_id": "C02-1",
              "status": "closed",
              "label": "label-1"
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
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "relevant": {
          "records": [
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
            }
          ],
          "debug": {
            "cached_guess": "5"
          }
        },
        "irrelevant_plain": {
          "records": [
            {
              "record_id": "C02-0",
              "status": "open",
              "label": "changed-0"
            },
            {
              "record_id": "C02-1",
              "status": "closed",
              "label": "changed-1"
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
              "record_id": "C02-1",
              "status": "closed",
              "label": "label-1"
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
              "record_id": "C03-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C03-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C03-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C03-3",
              "status": "closed",
              "label": "label-3"
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
        "relevant": {
          "records": [
            {
              "record_id": "C03-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C03-1",
              "status": "open",
              "label": "label-1"
            },
            {
              "record_id": "C03-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C03-3",
              "status": "closed",
              "label": "label-3"
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
              "record_id": "C03-0",
              "status": "open",
              "label": "changed-0"
            },
            {
              "record_id": "C03-1",
              "status": "closed",
              "label": "changed-1"
            },
            {
              "record_id": "C03-2",
              "status": "open",
              "label": "changed-2"
            },
            {
              "record_id": "C03-3",
              "status": "closed",
              "label": "changed-3"
            },
            {
              "record_id": "C03-4",
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
              "record_id": "C03-0",
              "status": "open",
              "label": "label-0"
            },
            {
              "record_id": "C03-1",
              "status": "closed",
              "label": "label-1"
            },
            {
              "record_id": "C03-2",
              "status": "open",
              "label": "label-2"
            },
            {
              "record_id": "C03-3",
              "status": "closed",
              "label": "label-3"
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
            "unstable",
        ],
    )
    parser.add_argument("--models", nargs="+", default=[])
    parser.add_argument("--prompt-regimes", nargs="+", default=["weak", "strict"])
    parser.add_argument("--ollama-url", default="http://127.0.0.1:11434/api/chat")
    parser.add_argument("--temperature", type=float, default=0.0)
    parser.add_argument("--seed", type=int, default=123)
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
        for model in args.models:
            for regime in args.prompt_regimes:
                agent_id = f"ollama::{model}::{regime}"
                for case in cases:
                    answers: dict[str, str] = {}
                    call_records: list[dict[str, Any]] = []
                    row_warnings: list[str] = []
                    for variant in VARIANTS:
                        try:
                            answer, usage, parse_warning, raw_content = ollama_answer(
                                url=args.ollama_url,
                                model=model,
                                messages=prompt_for(case, variant, regime),
                                temperature=args.temperature,
                                seed=args.seed,
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
                            call_records.append({"variant": variant, "error": message})
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
            cases.append(BUILDERS[family](index, rng))
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

Formal 突变测试覆盖七种策略、五个任务族和二十个案例。联合关系对“稳定选择性采用”标签的平衡准确率为 1.0；只看相关变化为 0.70，加入无关不变性为 0.80。正确采用与错误但等变采用都通过；只在完全重复时不稳定的专门反例通过相关关系与无关不变性，却被联合关系拒绝，明确显示该探针既不是正确性验证器，也不能省略重放稳定性。

三个本地模型、两种提示制度、二十个案例的修复后 Formal 运行共完成 600 次调用且无调用错误。53 个单次精确正确行中，18 个没有通过联合关系，样本内脆弱率为 33.96%，Wilson 95% 区间为 [22.69%, 47.41%]；六个模型—提示分层中五个非零，且 18 个失败均无解析警告。该数字只描述当前冻结合成套件，不能外推。

## 最近先行边界

- METAL 已把变形关系系统用于大模型的稳健性、公平性、非确定性与效率评价，并包含输入扰动关系和相同输入重复；因此“关系式测试大模型”没有新颖性。当前候选只能主张工具字段采用这一特定诊断组合。
- ToolFailBench 区分工具跳过与结果忽略，但没有字段级任务关系重放。
- CAIR 通过反事实替换智能体输出测量结果与工作流变化，最接近一般反事实影响谱系；当前候选要求任务条件等变/不变关系，而非仅测影响大小。
- ReliabilityBench 使用动作变形关系与终态等价性，主要变形任务/用户输入及执行序列；当前候选变形的是已返回的工具字段并诊断最终回答采用。
- CVT-RL 以工具输出扰动估计反事实贡献，用于带可验证终局奖励的强化学习信用分配；当前候选是无需训练的黑盒评价，不以终局奖励作为采用标签。
- PriVE-Tools 冻结问题与评分，只改变工具派生视觉证据条件并发现证据提供不等于证据采用；当前候选与其共享现象动机，但干预结构化返回字段、检验任务等变/不变关系，而不是比较视觉证据视图的正确率增益。

## 未决风险

最大风险是外部有效性和最近先行碰撞：当前案例为合成短答案任务，任务关系由研究者设计；即使内部对照成立，也尚未证明复杂、多步或开放式智能体轨迹中的效用。首轮固定评审发现的实现缺陷已修复并完成正式复现，但仍须由第二轮固定评审判断该局部差分是否值得扩大。

### Source: `audit_v001/seed_support_seed-audit-005.md`

# Seed 支撑事实审计 v001

> ADVISORY_ONLY：仅陈列可核查的机械或显式事实；不判断新颖性、科学充分性或交付结论。

- Run：`20260815_1818_run11`
- 截止时间：`2026-08-15T11:46:20.479992Z`
- Seed：`seed_v001.md`；SHA-256：`7ed95e4a074dc009e19985d49f03b700332781d55cd412e5b77354b4359d36dd`
- Portfolio：`hypotheses_v001/portfolio.json`；SHA-256：`f477e3a215ec57dd60370cc4ab8429e9e2ce65e0642ad128a71e19879a0fb90d`
- Supporting attempts：`attempt-mutation-005`、`attempt-qwen-005`

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
| `finding` | `supporting_attempt_bound` | supporting attempt attempt-mutation-005 绑定了可核验的 Spec、Claim 列表与 metrics 快照。 | `experiment_v001/attempts/attempt-mutation-005/execution.json`<br>`experiment_v001/attempts/attempt-mutation-005/spec.json`<br>`experiment_v001/attempts/attempt-mutation-005/metrics.json` |
| `warning` | `attempt_spec_parity_different` | supporting attempt attempt-qwen-005 的 Spec parity 维度 model_provider_revision 显式为 different。 | `experiment_v001/attempts/attempt-qwen-005/spec.json#/parity_dimensions/model_provider_revision` |
| `finding` | `supporting_attempt_bound` | supporting attempt attempt-qwen-005 绑定了可核验的 Spec、Claim 列表与 metrics 快照。 | `experiment_v001/attempts/attempt-qwen-005/execution.json`<br>`experiment_v001/attempts/attempt-qwen-005/spec.json`<br>`experiment_v001/attempts/attempt-qwen-005/metrics.json` |
| `finding` | `independent_claim_validation_present` | 存在显式绑定为 independent_claim_validation 的有效 supporting attempt。 | `experiment_v001/attempts/attempt-qwen-005/spec.json` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 0 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-mutation-005/metrics.json#/records/0/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 1 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-mutation-005/metrics.json#/records/1/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 2 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-mutation-005/metrics.json#/records/2/value` |
| `finding` | `seed_metric_mapping_resolved` | 数字映射 3 可追踪到精确实验事实。 | `seed_v001.md`<br>`experiment_v001/attempts/attempt-qwen-005/metrics.json#/records/0/value` |
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
    "attempt-qwen-005"
  ],
  "prior_audits": [
    {
      "age_days": 0.05749392398148148,
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
      "age_days": 0.03508070673611111,
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
      "age_days": 0.0006296025115740741,
      "audit_id": "prior-003",
      "candidate_count": 15,
      "created_at_utc": "2026-08-15T11:45:26.082335Z",
      "degraded": true,
      "hypothesis_id": "H001",
      "path": "hypotheses_v001/priors/prior-003",
      "queries": [
        "tool output perturbation metamorphic relation tool-using language model agent evaluation evidence uptake counterfactual"
      ]
    }
  ],
  "supporting_attempts": [
    {
      "attempt_id": "attempt-mutation-005",
      "claim_ids": [
        "claim-mutation-discrimination"
      ],
      "execution_sha256": "1a051684c839f010ab95ae2e6e6339a03c8ac33e490779ed3bf280f88f951100",
      "hypothesis_id": "H001",
      "metric_record_count": 3,
      "metrics_sha256": "3cba49d89c54c244bb7022b10c0eba1f1526dc93efd4f091d9868eb438c1ee03",
      "purpose": "mechanism_consistency",
      "schema_version": 8,
      "sources": [
        "experiment_v001/attempts/attempt-mutation-005/execution.json",
        "experiment_v001/attempts/attempt-mutation-005/spec.json",
        "experiment_v001/attempts/attempt-mutation-005/metrics.json"
      ],
      "spec_sha256": "e6eac6f2527c68ba944520c6d4be449f798e46dc5a886b4078b0190cdc6d327d"
    },
    {
      "attempt_id": "attempt-qwen-005",
      "claim_ids": [
        "claim-one-shot-brittleness"
      ],
      "execution_sha256": "699c57ef7da657ad599edf52ea07c69689832f082934d2d9a6b3205b2e3eba61",
      "hypothesis_id": "H001",
      "metric_record_count": 3,
      "metrics_sha256": "b969042513211ab31306162e1726bc24868370fee028ee621761ea1c245e45af",
      "purpose": "independent_claim_validation",
      "schema_version": 8,
      "sources": [
        "experiment_v001/attempts/attempt-qwen-005/execution.json",
        "experiment_v001/attempts/attempt-qwen-005/spec.json",
        "experiment_v001/attempts/attempt-qwen-005/metrics.json"
      ],
      "spec_sha256": "139fec8cdd10fa709915b4131a7c9d1d57db0080d7ba997d29f87c8d0be316d1"
    }
  ]
}
```

## 机械权限边界

本材料不改变 Claim 或 hypothesis 状态，不改变三位 Reviewer、同字节哈希链或主研究者裁决权。

## Final Core Evidence Closure (machine generated, bounded)

This appendix exposes selected Formal Spec, Claim and metric facts; it does not judge scientific sufficiency.
Closure SHA-256: `627a93ea3b0a27a78eceb3132cadbf2517a839309ec79a166b2b600e8e4be913`

```json
{
  "artifact_kind": "final_core_evidence_closure",
  "attempts": [
    {
      "attempt_id": "attempt-mutation-005",
      "execution_schema_version": 8,
      "execution_sha256": "1a051684c839f010ab95ae2e6e6339a03c8ac33e490779ed3bf280f88f951100",
      "metrics": {
        "errors": {
          "items": [],
          "omitted_count": 0,
          "total_count": 0
        },
        "experiment_id": "exp-mutation-v005",
        "included_record_count": 3,
        "omitted_record_count": 0,
        "primary_metric_selection_priority": "bidirectional_relation_balanced_accuracy",
        "record_count": 3,
        "records": [
          {
            "aggregation": "balanced_accuracy",
            "n": 140,
            "name": "bidirectional_relation_balanced_accuracy",
            "source_index": 0,
            "split": "mutation_suite",
            "unit": "ratio",
            "value": 1.0
          },
          {
            "aggregation": "balanced_accuracy",
            "n": 140,
            "name": "selective_change_balanced_accuracy",
            "source_index": 1,
            "split": "mutation_suite",
            "unit": "ratio",
            "value": 0.8
          },
          {
            "aggregation": "balanced_accuracy",
            "n": 140,
            "name": "any_change_balanced_accuracy",
            "source_index": 2,
            "split": "mutation_suite",
            "unit": "ratio",
            "value": 0.7
          }
        ],
        "resource_usage": {
          "api_calls": 0,
          "estimated_cost": "unknown",
          "gpu_time_seconds": "unknown",
          "tokens": 0,
          "wall_time_seconds": 0.0021987000000081025
        },
        "warnings": {
          "items": [],
          "omitted_count": 0,
          "total_count": 0
        }
      },
      "metrics_path": "experiment_v001/attempts/attempt-mutation-005/metrics.json",
      "metrics_sha256": "3cba49d89c54c244bb7022b10c0eba1f1526dc93efd4f091d9868eb438c1ee03",
      "spec": {
        "claim_ids": {
          "items": [
            "claim-mutation-discrimination"
          ],
          "omitted_count": 0,
          "total_count": 1
        },
        "dataset": "suite_spec.json 生成并冻结的五任务族二十案例。",
        "experiment_id": "exp-mutation-v005",
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
        "model": "七种确定性策略：faithful、wrong_equivariant、misdirected_selective、ignore、distractor、repeat_only_unstable、unstable。",
        "primary_metric": "bidirectional_relation_balanced_accuracy",
        "provider": "本地 Python 3 确定性策略后端。",
        "purpose": "mechanism_consistency",
        "research_question": "任务定向输出关系是否在相同回答集合上排除方向错误但选择性的伪采用，从而优于只看变化与变化加不变性？",
        "revision": "implementation_v001 full-manifest binding; reviewer-fix: joint relation now includes exact-repeat stability and a repeat-only-unstable mutant",
        "sampling_unit": "冻结案例与可控策略的笛卡尔积，共 140 行。",
        "secondary_metrics": {
          "items": [
            "selective_change_balanced_accuracy",
            "any_change_balanced_accuracy",
            "misdirected_selective_pass_rate"
          ],
          "omitted_count": 0,
          "total_count": 3
        }
      },
      "spec_path": "experiment_v001/attempts/attempt-mutation-005/spec.json",
      "spec_sha256": "e6eac6f2527c68ba944520c6d4be449f798e46dc5a886b4078b0190cdc6d327d"
    },
    {
      "attempt_id": "attempt-qwen-005",
      "execution_schema_version": 8,
      "execution_sha256": "699c57ef7da657ad599edf52ea07c69689832f082934d2d9a6b3205b2e3eba61",
      "metrics": {
        "errors": {
          "items": [],
          "omitted_count": 0,
          "total_count": 0
        },
        "experiment_id": "exp-qwen-v005",
        "included_record_count": 3,
        "omitted_record_count": 0,
        "primary_metric_selection_priority": "one_shot_success_brittleness_rate",
        "record_count": 3,
        "records": [
          {
            "aggregation": "mean",
            "n": 53,
            "name": "one_shot_success_brittleness_rate",
            "source_index": 0,
            "split": "local_models",
            "unit": "ratio",
            "value": 0.33962264150943394
          },
          {
            "aggregation": "mean",
            "n": 120,
            "name": "bidirectional_relation_pass_rate",
            "source_index": 1,
            "split": "local_models",
            "unit": "ratio",
            "value": 0.2916666666666667
          },
          {
            "aggregation": "mean",
            "n": 67,
            "name": "systematic_wrong_uptake_rate",
            "source_index": 2,
            "split": "local_models",
            "unit": "ratio",
            "value": 0.0
          }
        ],
        "resource_usage": {
          "api_calls": 600,
          "estimated_cost": 0.0,
          "gpu_time_seconds": "unknown",
          "tokens": 137969,
          "wall_time_seconds": 416.3588051000006
        },
        "warnings": {
          "items": [
            "ollama::qwen2.5:7b::strict/count_open_00/relevant: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict/count_open_02/relevant: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict/tier_score_02/irrelevant_plain: response was not a JSON object with an answer key"
          ],
          "omitted_count": 0,
          "total_count": 3
        }
      },
      "metrics_path": "experiment_v001/attempts/attempt-qwen-005/metrics.json",
      "metrics_sha256": "b969042513211ab31306162e1726bc24868370fee028ee621761ea1c245e45af",
      "spec": {
        "claim_ids": {
          "items": [
            "claim-one-shot-brittleness"
          ],
          "omitted_count": 0,
          "total_count": 1
        },
        "dataset": "五个确定性结构化工具任务族、每族四例、共二十例。",
        "experiment_id": "exp-qwen-v005",
        "falsification_rule": "总体脆弱率低于 0.10，或失败全由解析警告解释，或只在一个分层出现，则本地现象主张不支持；不得外推到其他模型或真实部署。",
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
        "revision": "implementation_v001 full-manifest binding, reviewer-fix joint relation includes exact-repeat stability, endpoint-fix, temperature 0, think false, JSON schema answer string",
        "sampling_unit": "模型 × 提示制度 × 冻结案例，共 120 行；每行五次调用。",
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
      "spec_path": "experiment_v001/attempts/attempt-qwen-005/spec.json",
      "spec_sha256": "139fec8cdd10fa709915b4131a7c9d1d57db0080d7ba997d29f87c8d0be316d1"
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
    "sha256": "7ed95e4a074dc009e19985d49f03b700332781d55cd412e5b77354b4359d36dd"
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
          "source_path": "experiment_v001/attempts/attempt-mutation-005/metrics.json",
          "source_value": 1.0
        },
        "kind": "finding",
        "message": "数字映射 0 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-mutation-005/metrics.json#/records/0/value"
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
          "seed_value": 0.8,
          "source_path": "experiment_v001/attempts/attempt-mutation-005/metrics.json",
          "source_value": 0.8
        },
        "kind": "finding",
        "message": "数字映射 1 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-mutation-005/metrics.json#/records/1/value"
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
          "seed_value": 0.7,
          "source_path": "experiment_v001/attempts/attempt-mutation-005/metrics.json",
          "source_value": 0.7
        },
        "kind": "finding",
        "message": "数字映射 2 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-mutation-005/metrics.json#/records/2/value"
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
          "seed_value": 0.33962264150943394,
          "source_path": "experiment_v001/attempts/attempt-qwen-005/metrics.json",
          "source_value": 0.33962264150943394
        },
        "kind": "finding",
        "message": "数字映射 3 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-qwen-005/metrics.json#/records/0/value"
          ],
          "omitted_count": 0,
          "total_count": 2
        }
      },
      {
        "code": "seed_numeric_literals_unmapped",
        "details": {
          "numeric_literal_count": 11,
          "numeric_literals": [
            "1",
            "0.95",
            "0.05",
            "2",
            "53",
            "18",
            "95%",
            "0.2269",
            "0.4741",
            "18",
            "53"
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
    "attempt-mutation-005",
    "attempt-qwen-005"
  ],
  "version": "v001"
}
```

## Evidence Inventory (machine generated)

```json
{
  "comparison_count": 0,
  "comparisons": [],
  "formal_attempt_count": 8,
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
      "association": "MATCH",
      "attempt_id": "attempt-mutation-005",
      "path": "experiment_v001/attempts/attempt-mutation-005/execution.json",
      "read_error": null,
      "record_sha256": "1a051684c839f010ab95ae2e6e6339a03c8ac33e490779ed3bf280f88f951100",
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
      "association": "MATCH",
      "attempt_id": "attempt-qwen-005",
      "path": "experiment_v001/attempts/attempt-qwen-005/execution.json",
      "read_error": null,
      "record_sha256": "699c57ef7da657ad599edf52ea07c69689832f082934d2d9a6b3205b2e3eba61",
      "schema_version": 8,
      "selected_in_core": true,
      "status": "SUCCESS",
      "valid_review_support": true
    }
  ],
  "implementation_key": "5135bed01d0bef962cb6f8262375bb063c1561c8ad6e8be3dc346aa521bcc7b1",
  "machine_judgment": "NONE_FACTS_ONLY",
  "recorded_attempt_count": 0,
  "recorded_attempts": [],
  "schema_version": 1,
  "version": "v001"
}
```
