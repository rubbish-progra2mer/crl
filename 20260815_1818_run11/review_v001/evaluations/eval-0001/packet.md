# CRL Fixed Review Packet

- Contract: 3
- Scientific version: v001
- Evaluator: CRL-EVAL-1.0
- Evaluator definition SHA-256: e0d35083b1427e9f8861ba576304b97657498fee46480d5e07e8e0b02cea6e5b
- Implementation key: cfd9cb4f4decadc4ec3587ec8b1df391c76771a0c0c6f8819e91d6b1abfa22b8
- Implementation manifest SHA-256: cfd9cb4f4decadc4ec3587ec8b1df391c76771a0c0c6f8819e91d6b1abfa22b8
- Evidence inventory SHA-256: 01e184299f30f69e9aec088f0b49c9dd33e53ff52c3e8d71875c27a0b09d128c

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

在五个确定性任务族、二十个冻结案例与六种预声明策略上，联合关系应比“相关答案发生任意变化”和“相关变化加两类无关不变”更准确地区分稳定选择性采用。正标签包括正确采用与错误但等变采用，后者用于阻止把探针偷换成正确性。

Formal `attempt-mutation-004` 中，任务定向双向关系平衡准确率为 1.0；选择性变化基线为 0.875；任意相关变化为 0.75。错误但等变策略 20/20 通过，方向错误但选择性变化策略 0/20 通过。预注册判据“至少 0.95 且比第二基线至少高 0.05”得到局部支持。

### Claim 2：单次成功关系脆弱性

在三个本地模型、两种提示制度、二十个冻结案例上，单次精确正确不足以保证任务定向、抗无关诱饵且可重放的采用结构。

Formal `attempt-qwen-004` 中，54 个单次精确正确行有 18 个联合关系失败，脆弱率为 0.3333333333333333，Wilson 95% 区间为 [0.2224, 0.4664]。18 个失败均无解析警告，六个模型—提示分层中五个出现非零失败。该比例只描述本地冻结合成套件；不能外推为部署失败率。

## 正确性 × 采用关系四象限

| 单次正确性 | 联合关系 | 解释边界 |
|---|---|---|
| 对 | 通过 | 样本内正确且采用结构稳定 |
| 对 | 失败 | 一次答对但关系脆弱，是本版本观察到的核心现象 |
| 错 | 通过 | 系统性但错误的等变采用；探针不能纠正它 |
| 错 | 失败 | 错误且没有稳定选择性采用证据 |

正式真实模型套件没有观察到“错且通过”，但确定性突变策略已证明它在逻辑上可以发生。因此联合关系永远不能单独称为正确性验证器。

## 贡献向量

- **问题/现象**：把“工具证据已经提供”与“单次答对时仍未稳定采用”分开；正式样本内观察到 18/54 的关系脆弱性。
- **机制/计算**：相关字段使用任务定向等变，而非只看变化；普通无关、答案形状诱饵与精确重放分别隔离三类伪影。
- **智能体特有约束**：干预位置在工具结果进入上下文之后、最终回答之前，面向结构化工具返回而非普通用户输入扰动。
- **评价/基准**：六种突变策略与正确性×关系四象限共同规定信号边界。
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

## 值得扩大的验证

下一阶段应冻结更广的工具任务本体：检索选择、聚合、状态过滤、多工具连接和开放式证据综合；加入跨供应商模型与至少三个种子；由独立标注者定义字段相关性和变形关系；与 METAL 风格相等/距离关系、CAIR 风格影响分数、终局正确率及 ToolFailBench 分类做同预算比较。最关键的扩大判据是：四象限能否预测后续复核失败、修复收益或真实终态错误，而不仅是在合成套件上重述完整反事实正确性。

<!-- CRL_SEED_SUPPORT_META {"schema_version":1,"hypothesis_ids":["H001"],"claim_ids":["claim-mutation-discrimination","claim-one-shot-brittleness"],"falsified_claim_dispositions":[],"metric_mappings":[{"seed_text":"任务定向双向关系平衡准确率为 1.0","seed_value":1.0,"source_path":"experiment_v001/attempts/attempt-mutation-004/metrics.json","json_pointer":"/records/0/value"},{"seed_text":"选择性变化基线为 0.875","seed_value":0.875,"source_path":"experiment_v001/attempts/attempt-mutation-004/metrics.json","json_pointer":"/records/1/value"},{"seed_text":"任意相关变化为 0.75","seed_value":0.75,"source_path":"experiment_v001/attempts/attempt-mutation-004/metrics.json","json_pointer":"/records/2/value"},{"seed_text":"脆弱率为 0.3333333333333333","seed_value":0.3333333333333333,"source_path":"experiment_v001/attempts/attempt-qwen-004/metrics.json","json_pointer":"/records/0/value"}]} -->

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

### Source: `hypotheses_v001/priors/prior-002/assessment.md`

# 最近先行科研解释

> 本文件属于主研究者解释，可在阅读候选、PDF、Evidence 和实验后继续修订；它不进入机器事实快照哈希。

- 审计标识：`prior-002`
- 碰撞类型：`ANALOGICAL_REDUCTION`

## 真正的 nearest prior

1. **METAL**（候选 `prior-05ce3bdb71373092`，arXiv:2312.06056）是方法形式上最近的先行：它把变形关系定义为大模型质量评价模块，覆盖输入扰动后的相等/不等、生成任务距离关系以及相同输入重复的一致性。它足以否定“首次把变形测试用于大模型黑盒评价”这一宽主张。
2. **CAIR**（EMNLP 2025，ACL Anthology 2025.emnlp-main.958）是反事实影响目标上最近的先行：它替换多智能体工作流中的智能体输出，度量对最终结果及工作流的影响并排序，但不要求任务条件输出关系。
3. **CVT-RL**（arXiv:2606.05263）直接包含工具输出扰动，不过其目标是在冻结续写策略与可验证终局奖励下估计反事实贡献，用于强化学习信用分配，而不是黑盒评价关系。
4. **PriVE-Tools**（候选 `prior-527e3aefa70e58f2`，arXiv:2607.16311）在现象上很接近：它冻结问题、正确答案、偏置答案与评分规则，只改变裁剪、缩放、框选等工具证据视图，发现提供相关工具证据不保证模型使用该证据；但其干预改变证据呈现条件，主要以正确率和先验跟随错误率评价，没有对结构化工具返回字段建立等变/不变关系。
5. **ReliabilityBench**（arXiv:2601.06112）使用动作变形关系、任务扰动、终态等价和故障注入评价智能体可靠性；其主要干预入口是任务/用户输入和执行行为，而非已返回工具字段的最终回答采用。

## 实质组件重合

- 与 METAL 重合：黑盒多次执行、输入扰动、相等/距离关系、相同输入重复、无需逐例完整输出标签的变形思想。
- 与 CAIR/CVT-RL 重合：通过受控反事实替换判断某个过程变量是否影响下游输出。
- 与 PriVE-Tools 重合：区分“证据已提供”和“模型确实依据证据作答”，并把证据条件作为受控变量。
- 与 ReliabilityBench 重合：把变形关系用于智能体可靠性而非普通静态分类器。

## 仍存贡献增量

- **干预位置**：只修改已返回的结构化工具字段，而不改用户任务、工具选择、智能体消息或证据呈现方式。
- **关系语义**：相关字段不是只要求输出“不同”，而是要求满足由任务规定的标识双射或数值平移；突变测试表明这可排除稳定但方向错误的选择性变化。
- **对照组合**：普通无关字段、答案形状诱饵字段、精确重放分别隔离装饰敏感、诱饵依赖与随机不稳定。
- **诊断表达**：关系信号与独立正确性形成四象限；明确允许“错误但等变”通过，避免把采用结构误称为正确性。
- **经验现象**：候选的可发表价值更可能来自“单次成功中的工具采用脆弱性”及其分层，而不是变形测试本身。

## 最危险替代解释

本候选可能只是 METAL 的一个工具场景实例，加上手工选择的几个关系和诱饵；若没有跨任务、跨模型的稳定现象、明确优于通用变形基线的新增判别力，方法贡献不足。另一个风险是合成任务把关系写得过于简单，真实模型失败只反映提示遵循或短答案解析，而非智能体工具采用。

## 最小区分实验

1. 用方向错误但“相关变化且无关不变”的可控策略检验任务定向关系是否比 METAL 风格的变化/一致性关系多提供判别力。
2. 用独立家族求解器验证所有相关/无关变形的标签与语义，不读取主评估器标签。
3. 在至少三个本地模型、两种提示制度和五个任务族上正式复现“单次正确但关系失败”，并按模型、提示和任务族分层；若只集中于一个模型或解析失败则不成立。

## 方法死亡后仍存现象

即使 METAL 或未来最近先行完全覆盖关系式方法，仍可保留的候选现象是：工具型语言模型在一次答对时仍可能无法在任务等价的工具字段变形下保持方向正确、无关不变和重复稳定。该现象必须由正式复现与扩展评审支持，当前 Scratch 不足以交付。

## 背景与身份未解决项

- 本次自动审计因 Semantic Scholar HTTP 429 而降级，候选只来自 arXiv；CAIR、CVT-RL 与 ReliabilityBench 的身份和组件来自主研究者另行核对的论文原文，未进入本快照候选集合。
- PriVE-Tools 为 2026 年 7 月新预印本，同行评审状态未确认。
- 尚未发现完全匹配“结构化工具字段变形 + 任务定向等变 + 两类无关不变 + 正确性四象限”的论文，但这不是穷尽性证明。

## 3. Core Experimental Evidence

### Source: `experiment_v001/result.md`

# 正式实验结果 v001

## 证据资格

- 当前完整实现清单匹配且有效的正式尝试：`attempt-mutation-004`、`attempt-qwen-004`，二者 `runner_exit_code=0`、`metrics_contract_ok=true`、`output_contract_ok=true`。
- 历史有效但完整实现清单不匹配：`attempt-mutation-002/003` 与 `attempt-qwen-003` 只绑定了三个运行文件；数值与 v004 重跑一致，但不作为最终交付支持。
- 无效尝试：`attempt-qwen-002` 因包装器把 Ollama 根路径误作聊天端点，600 个请求均返回 HTTP 405，`runner_exit_code=2`；它只作为失败记录，不支持任何科研主张。
- 正式模型身份：Ollama 0.32.13；`qwen2.5:7b` 摘要 `845dbda0ea48`，`qwen3:4b` 摘要 `359d7dd4bcda`，`qwen3:8b` 摘要 `500a1f067a9f`。

## 独立标签校验

两个有效尝试都先执行独立家族求解器。它不读取 `expected` 作为求解输入，也不导入生成器或主评估器；二十个案例全部满足重算标签、相关关系与两类无关不变条件，20/20 通过。该校验只证明合成套件自洽。

## Claim 1：突变判别

正式尝试 `attempt-mutation-004` 共 120 个案例—策略行，无外部模型调用。

| 信号 | 平衡准确率 |
|---|---:|
| 相关答案发生任意变化 | 0.750 |
| 相关变化 + 两类无关不变 | 0.875 |
| 任务定向双向关系 | 1.000 |

预注册门槛为双向关系至少 0.95，且比第二基线至少高 0.05；实际高 0.125。错误但等变策略 20/20 通过，方向错误但选择性变化策略 0/20 通过。这支持“任务定向关系提供额外采用结构判别”，同时否定把信号解释为答案正确性。

## Claim 2：单次成功关系脆弱性

正式尝试 `attempt-qwen-004` 完成 600 次本地调用、137,323 个令牌、120 个模型—提示—案例行，无调用错误，出现 4 条结构化输出解析警告。

- 54 行基线答案单次精确正确，其中 18 行未通过联合关系；脆弱率为 33.33%。
- 二项比例的 Wilson 95% 区间为 [22.24%, 46.64%]，仅描述冻结套件内的行级比例。
- 18 个关系失败均没有解析警告；因此剔除解析警告后仍为 18/54。
- 六个模型—提示分层中五个出现非零脆弱案例，超过预注册的至少三个分层门槛。
- 分层脆弱率：qwen2.5:7b 严格 0/8，弱 4/5；qwen3:4b 严格 4/8，弱 7/12；qwen3:8b 严格 1/9，弱 2/12。
- 在 54 个单次正确行中，任务相关关系失败 9 行、普通无关字段不变失败 15 行、答案形状诱饵不变失败 3 行、精确重放不稳定 1 行；各类型可重叠。
- 按任务族，关系失败集中于 `filtered_argmin` 8/20 与 `latest_confirmed` 8/12；`count_open` 为 0/16，`tier_score` 为 1/5，`valid_sum` 为 1/1。该异质性限制宽泛外推。

预注册总体门槛为至少 0.10、解析警告剔除后仍非零、至少三个分层出现；三项均通过。结论只支持“冻结本地合成套件中，单次答对可能掩盖关系脆弱性”，不支持真实部署失败率或所有工具任务的一般性。

## 负面与边界结果

- 正式真实模型中没有观察到错误但联合关系通过的行；这不改变突变套件已证明的逻辑可能性，也不能把关系信号升级为正确性验证器。
- 在当前真实模型套件上，联合关系通过与完整四变体精确正确恰好重合（36/120）；这是样本内现象，且两者共享冻结任务语义，不能解释为普遍等价。
- 结果高度依赖两个标识选择任务族；数值任务中基线答对样本少，需未来扩大任务结构与模型谱系。
- 固定单一种子保证复现路径，但未估计跨种子方差。

## 当前判断

两条局部主张均获得正式支持，但方法新颖性仍受 METAL、CAIR、ReliabilityBench、CVT-RL 与 PriVE-Tools 的强类比归约。候选能否成为研究种子，取决于固定评审是否接受“工具字段任务关系 + 双重无关诱饵 + 正确性四象限”及观察到的单次成功脆弱性具有足够论文潜力。

### Source: `experiment_v001/attempts/attempt-mutation-004/execution.json`

{
  "argv": [
    "python",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\run_verified_experiment.py",
    "--backend",
    "deterministic",
    "--cases",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\cases.json",
    "--oracle-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-004\\oracle.json",
    "--output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-004\\result.json",
    "--report-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-004\\report.md",
    "--metrics-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-004\\metrics-output.json",
    "--experiment-id",
    "exp-mutation-v004",
    "--seed",
    "20260815",
    "--policies",
    "faithful",
    "wrong_equivariant",
    "misdirected_selective",
    "ignore",
    "distractor",
    "unstable"
  ],
  "attempt_id": "attempt-mutation-004",
  "budget_facts": {
    "actual": {
      "api_calls": 0,
      "duration_seconds": 0.2248641999976826,
      "gpu_time_seconds": "unknown",
      "tokens": 0
    },
    "comparison": {
      "reason": "budget_ceiling is not a machine-readable JSON object",
      "status": "unavailable"
    },
    "machine_readable_limits": null,
    "spec_budget_ceiling": "0 次外部模型调用，20 案例 × 6 策略 = 120 关系行。",
    "warnings": []
  },
  "capture": {
    "stderr": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-004\\stderr.bin",
      "redaction_applied": false,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "size_bytes": 0
    },
    "stdout": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-004\\stdout.bin",
      "redaction_applied": false,
      "sha256": "55336cb21fd7a6252fcbaad64e62d28602373b8c43c36a10ea3dee1c5582ddf7",
      "size_bytes": 381
    }
  },
  "command_error": null,
  "command_exit_code": 0,
  "cwd": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001",
  "duration_seconds": 0.2248641999976826,
  "environment_facts": {
    "cpu_count": 16,
    "declared_facts": {
      "dataset": "frozen-20-case-five-family-suite",
      "dataset_revision": "suite-seed-20260815",
      "model": "six-deterministic-mutation-policies",
      "model_revision": "implementation-v001-full-manifest",
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
    "platform": "Windows-11-10.0.26100-SP0",
    "runner": {
      "dependencies": {
        "scope": "formal_runner_machine_environment",
        "snapshot": {
          "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-004\\dependencies.txt",
          "sha256": "480ab3b94b0b3b95bb6ff16eb9c4e138b942a818e488d43f71f810c5fe2e143a",
          "size_bytes": 769
        },
        "source_path": "D:\\Desktop\\crl\\crl_agent_v3\\CRL_ENVIRONMENT_LOCK.txt",
        "source_type": "lock_file",
        "subject_relationship": "unbound"
      },
      "executable": {
        "path": "D:\\Apps\\Miniconda\\python.exe",
        "sha256": "388fe2cffda8a134e7d7dc4e978f7c478857ece6b69694daecbed25e51ec633a",
        "size_bytes": 104264,
        "status": "bound"
      },
      "python": "3.13.5 | packaged by Anaconda, Inc. | (main, Jun 12 2025, 16:37:03) [MSC v.1929 64 bit (AMD64)]",
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
      "argv0": "python",
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
        "path": "D:\\Apps\\Miniconda\\python.exe",
        "resolution": "path_search",
        "sha256": "388fe2cffda8a134e7d7dc4e978f7c478857ece6b69694daecbed25e51ec633a",
        "size_bytes": 104264,
        "status": "bound"
      },
      "runner_relationship": "same_executable",
      "runtime": {
        "python": "3.13.5 | packaged by Anaconda, Inc. | (main, Jun 12 2025, 16:37:03) [MSC v.1929 64 bit (AMD64)]",
        "status": "bound_to_runner_python"
      }
    }
  },
  "evidence_contract_ok": true,
  "experiment_spec": {
    "snapshot": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-004\\spec.json",
      "sha256": "1cc3b8cbd88a803fa508518ac12ea9ff29fd7a03ffd303095177453ac150b51a",
      "size_bytes": 3542
    },
    "source_path": "experiment_v001/specs/exp-mutation-v004.json"
  },
  "finished_at_utc": "2026-08-15T11:18:27.403552Z",
  "implementation_files": [
    {
      "path": "implementation_v001/cases.json",
      "sha256": "16405ec1aaf9b54c385a855371b2894f3716cd5c54929d780e1103ef10fca577",
      "size_bytes": 62543
    },
    {
      "path": "implementation_v001/causal_uptake_eval.py",
      "sha256": "b7aa5cb24002bd08631d24018e2b31a729f1b64f8ae8614871f358defb1a7e25",
      "size_bytes": 28074
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
      "sha256": "e155e4d981324ec35b88df15cb47cc98e90c45e70cd4ae09df0d843dc99077cd",
      "size_bytes": 4940
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
    }
  ],
  "metrics": {
    "contains_possible_credential": false,
    "credential_detection": [],
    "snapshot": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-004\\metrics.json",
      "sha256": "b60265bcd2c3030c8f4021a6c38fed6d265060bfeea161c0f05530c592102644",
      "size_bytes": 894
    },
    "source_path": "experiment_v001/attempts/attempt-mutation-004/metrics-output.json",
    "source_sha256": "b60265bcd2c3030c8f4021a6c38fed6d265060bfeea161c0f05530c592102644",
    "source_size_bytes": 894,
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
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-004\\oracle.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "44bd91de176bae3757845c51ade11396da9c299d2b7c37541bb77a2914f66abe",
        "size_bytes": 144166
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-004\\result.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "f968f5dcc94b8bd10db8c71c9c79685d94e62f350ff77e8bb2b9c2393707f7ac",
        "size_bytes": 3283
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-mutation-004\\report.md"
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
  "started_at_utc": "2026-08-15T11:18:27.178655Z",
  "stdout_as_evidence": false,
  "termination_method": null,
  "timed_out": false,
  "timeout_seconds": 120.0,
  "version": "v001",
  "warnings": []
}

### Source: `experiment_v001/attempts/attempt-qwen-004/execution.json`

{
  "argv": [
    "python",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\run_verified_experiment.py",
    "--backend",
    "ollama",
    "--cases",
    "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001\\cases.json",
    "--oracle-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-004\\oracle.json",
    "--output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-004\\result.json",
    "--report-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-004\\report.md",
    "--metrics-output",
    "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-004\\metrics-output.json",
    "--experiment-id",
    "exp-qwen-v004",
    "--seed",
    "123",
    "--models",
    "qwen2.5:7b",
    "qwen3:4b",
    "qwen3:8b",
    "--prompt-regimes",
    "strict",
    "weak",
    "--temperature",
    "0",
    "--timeout-seconds",
    "120"
  ],
  "attempt_id": "attempt-qwen-004",
  "budget_facts": {
    "actual": {
      "api_calls": 600,
      "duration_seconds": 348.7255425999974,
      "gpu_time_seconds": "unknown",
      "tokens": 137323
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
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-004\\stderr.bin",
      "redaction_applied": false,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "size_bytes": 0
    },
    "stdout": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-004\\stdout.bin",
      "redaction_applied": false,
      "sha256": "acdb65ab598b17c3ef9a58ada1f0b29037cd451f01d663998d79f3792196de51",
      "size_bytes": 368
    }
  },
  "command_error": null,
  "command_exit_code": 0,
  "cwd": "D:\\Desktop\\crl\\20260815_1818_run11\\implementation_v001",
  "duration_seconds": 348.7255425999974,
  "environment_facts": {
    "cpu_count": 16,
    "declared_facts": {
      "dataset": "frozen-20-case-five-family-suite",
      "dataset_revision": "suite-seed-20260815",
      "model": "qwen2.5-7b,qwen3-4b,qwen3-8b",
      "model_revision": "845dbda0ea48,359d7dd4bcda,500a1f067a9f",
      "prompt_revision": "strict-and-weak-v001",
      "provider": "ollama-0.32.13-local"
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
    "platform": "Windows-11-10.0.26100-SP0",
    "runner": {
      "dependencies": {
        "scope": "formal_runner_machine_environment",
        "snapshot": {
          "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-004\\dependencies.txt",
          "sha256": "480ab3b94b0b3b95bb6ff16eb9c4e138b942a818e488d43f71f810c5fe2e143a",
          "size_bytes": 769
        },
        "source_path": "D:\\Desktop\\crl\\crl_agent_v3\\CRL_ENVIRONMENT_LOCK.txt",
        "source_type": "lock_file",
        "subject_relationship": "unbound"
      },
      "executable": {
        "path": "D:\\Apps\\Miniconda\\python.exe",
        "sha256": "388fe2cffda8a134e7d7dc4e978f7c478857ece6b69694daecbed25e51ec633a",
        "size_bytes": 104264,
        "status": "bound"
      },
      "python": "3.13.5 | packaged by Anaconda, Inc. | (main, Jun 12 2025, 16:37:03) [MSC v.1929 64 bit (AMD64)]",
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
      "argv0": "python",
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
        "path": "D:\\Apps\\Miniconda\\python.exe",
        "resolution": "path_search",
        "sha256": "388fe2cffda8a134e7d7dc4e978f7c478857ece6b69694daecbed25e51ec633a",
        "size_bytes": 104264,
        "status": "bound"
      },
      "runner_relationship": "same_executable",
      "runtime": {
        "python": "3.13.5 | packaged by Anaconda, Inc. | (main, Jun 12 2025, 16:37:03) [MSC v.1929 64 bit (AMD64)]",
        "status": "bound_to_runner_python"
      }
    }
  },
  "evidence_contract_ok": true,
  "experiment_spec": {
    "snapshot": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-004\\spec.json",
      "sha256": "97ece5b833a0a491ed549b2fedf478ef228b8237fcc1e98ff22c643b8ae2139e",
      "size_bytes": 3926
    },
    "source_path": "experiment_v001/specs/exp-qwen-v004.json"
  },
  "finished_at_utc": "2026-08-15T11:24:32.670175Z",
  "implementation_files": [
    {
      "path": "implementation_v001/cases.json",
      "sha256": "16405ec1aaf9b54c385a855371b2894f3716cd5c54929d780e1103ef10fca577",
      "size_bytes": 62543
    },
    {
      "path": "implementation_v001/causal_uptake_eval.py",
      "sha256": "b7aa5cb24002bd08631d24018e2b31a729f1b64f8ae8614871f358defb1a7e25",
      "size_bytes": 28074
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
      "sha256": "e155e4d981324ec35b88df15cb47cc98e90c45e70cd4ae09df0d843dc99077cd",
      "size_bytes": 4940
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
    }
  ],
  "metrics": {
    "contains_possible_credential": false,
    "credential_detection": [],
    "snapshot": {
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-004\\metrics.json",
      "sha256": "10cd9ca9f2fe5d3a74b7d8c3d34082727abd70e824c8ef6d18abbf45fa1f051c",
      "size_bytes": 1282
    },
    "source_path": "experiment_v001/attempts/attempt-qwen-004/metrics-output.json",
    "source_sha256": "10cd9ca9f2fe5d3a74b7d8c3d34082727abd70e824c8ef6d18abbf45fa1f051c",
    "source_size_bytes": 1282,
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
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-004\\oracle.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "0392bc7d511d3e8a1a246bf141709e56f261143c17798aedbc85a386f9b0d73a",
        "size_bytes": 347631
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-004\\result.json"
    },
    {
      "after": {
        "artifact_retained": true,
        "contains_possible_credential": false,
        "credential_detection": [],
        "exists": true,
        "sha256": "491fd3de5d12fe60b1117acd2013c77d6ca79b6b741b0641ac703ae44f8e00d3",
        "size_bytes": 3357
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260815_1818_run11\\experiment_v001\\attempts\\attempt-qwen-004\\report.md"
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
  "started_at_utc": "2026-08-15T11:18:43.944605Z",
  "stdout_as_evidence": false,
  "termination_method": null,
  "timed_out": false,
  "timeout_seconds": 1200.0,
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
- 策略：正确采用、错误但等变采用、结果忽略、诱饵依赖、方向错误但选择性变化、随机不稳定。
- 正标签：前两者，因为标签是“稳定选择性采用”而不是正确性。
- 主要指标：联合关系对正标签的平衡准确率。
- 基线：相关回答是否变化；相关变化且两类无关回答不变。
- 否证：联合关系不能排除方向错误但选择性的策略，或不能达到高于两个基线的判别力。

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

现有突变及 600 次本地调用均为 Scratch，用于塑形主张和锁定实现。正式证据将冻结代码、案例、实验规格、种子、模型标识和输出路径后，通过 Contract v3 本地实验运行器重新执行；Scratch 数字不会直接作为交付资格证据。

## 5. Ablation / Robustness / Falsification Evidence

### Source: `experiment_v001/attempts/attempt-mutation-004/report.md`

# 双向反事实工具证据测试结果

- 后端：`deterministic`
- 案例数：20
- 关系评估行数：120
- 墙钟时间：0.001 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| deterministic::distractor | 20 | 0.000 | 0.000 | 0.000 | 1.000 | 0.000 | 1.000 | 0.000 | 0.000 |
| deterministic::faithful | 20 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |
| deterministic::ignore | 20 | 1.000 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 0.000 | 0.000 |
| deterministic::misdirected_selective | 20 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 0.000 |
| deterministic::unstable | 20 | 0.000 | 0.000 | 1.000 | 0.000 | 0.000 | 0.000 | 0.000 | 0.000 |
| deterministic::wrong_equivariant | 20 | 0.000 | 0.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 | 1.000 |

## 机械诊断

### deterministic_uptake_discrimination

- `tool_value_overlap`：balanced_accuracy=0.525，precision=0.36363636363636365，recall=0.4，TP/FP/TN/FN=16/28/52/24
- `relevant_changed`：balanced_accuracy=0.75，precision=0.5，recall=1.0，TP/FP/TN/FN=40/40/40/0
- `irrelevant_plain_invariant`：balanced_accuracy=0.625，precision=0.4，recall=1.0，TP/FP/TN/FN=40/60/20/0
- `irrelevant_adversarial_invariant`：balanced_accuracy=0.75，precision=0.5，recall=1.0，TP/FP/TN/FN=40/40/40/0
- `irrelevant_invariant`：balanced_accuracy=0.75，precision=0.5，recall=1.0，TP/FP/TN/FN=40/40/40/0
- `selective_change`：balanced_accuracy=0.875，precision=0.6666666666666666，recall=1.0，TP/FP/TN/FN=40/20/60/0
- `relevant_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=40/0/80/0
- `bidirectional_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=40/0/80/0

### deterministic_correctness_agreement

- `relevant_changed`：balanced_accuracy=0.7，precision=0.25，recall=1.0，TP/FP/TN/FN=20/60/40/0
- `selective_change`：balanced_accuracy=0.8，precision=0.3333333333333333，recall=1.0，TP/FP/TN/FN=20/40/60/0
- `relevant_relation`：balanced_accuracy=0.9，precision=0.5，recall=1.0，TP/FP/TN/FN=20/20/80/0
- `bidirectional_relation`：balanced_accuracy=0.9，precision=0.5，recall=1.0，TP/FP/TN/FN=20/20/80/0

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

### Source: `experiment_v001/attempts/attempt-qwen-004/report.md`

# 双向反事实工具证据测试结果

- 后端：`ollama`
- 案例数：20
- 关系评估行数：120
- 墙钟时间：348.453 秒

## 按智能体汇总

| 智能体 | n | 单次精确 | 反事实集精确 | 相关应变 | 普通无关不变 | 诱饵无关不变 | 重放稳定 | 选择性变化 | 双向关系 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| ollama::qwen2.5:7b::strict | 20 | 0.400 | 0.400 | 1.000 | 0.800 | 0.700 | 0.900 | 0.700 | 0.400 |
| ollama::qwen2.5:7b::weak | 20 | 0.250 | 0.050 | 0.900 | 0.600 | 0.700 | 0.900 | 0.400 | 0.050 |
| ollama::qwen3:4b::strict | 20 | 0.400 | 0.200 | 0.600 | 0.750 | 0.650 | 0.950 | 0.250 | 0.200 |
| ollama::qwen3:4b::weak | 20 | 0.600 | 0.250 | 0.800 | 0.600 | 0.650 | 0.900 | 0.350 | 0.250 |
| ollama::qwen3:8b::strict | 20 | 0.450 | 0.400 | 0.750 | 0.900 | 0.600 | 0.900 | 0.500 | 0.400 |
| ollama::qwen3:8b::weak | 20 | 0.600 | 0.500 | 0.650 | 1.000 | 0.700 | 1.000 | 0.600 | 0.500 |

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

- `tool_value_overlap`：balanced_accuracy=0.4484126984126984，precision=0.25806451612903225，recall=0.4444444444444444，TP/FP/TN/FN=16/46/38/20
- `relevant_changed`：balanced_accuracy=0.6547619047619048，precision=0.3829787234042553，recall=1.0，TP/FP/TN/FN=36/58/26/0
- `selective_change`：balanced_accuracy=0.8809523809523809，precision=0.6428571428571429，recall=1.0，TP/FP/TN/FN=36/20/64/0
- `relevant_relation`：balanced_accuracy=0.9107142857142857，precision=0.7058823529411765，recall=1.0，TP/FP/TN/FN=36/15/69/0
- `bidirectional_relation`：balanced_accuracy=1.0，precision=1.0，recall=1.0，TP/FP/TN/FN=36/0/84/0

### diagnostic_quadrants

- `single_correct_relation_pass`：36
- `single_correct_relation_fail`：18
- `single_wrong_relation_pass`：0
- `single_wrong_relation_fail`：66
- `one_shot_success_brittleness_rate`：0.3333333333333333
- `systematic_wrong_uptake_rate`：0.0

> 以上是机械结果，不自动证明科学新颖性、外部有效性或交付资格。

## 6. Reproducibility Facts

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
            "bidirectional_relation": relevant_relation and irrelevant_invariant,
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
    for policy in ("ignore", "distractor", "unstable"):
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

## 7. Known Limitations

### Source: `candidate_v001.md`

# 候选 v001：双向变形证据采用探针

## 核心计算

对每个基线工具返回，冻结任务与调用条件，执行四次影子重放：相关字段变形、普通无关字段变形、答案形状诱饵变形、完全相同重放。通过条件为：相关回答满足预声明任务关系，两类无关回答等于基线回答，重放回答也等于基线回答。

## 为什么不是普通敏感度测试

“答案发生变化”会同时接受随机不稳定和方向错误的选择性变化；“相关变化且无关不变”仍会接受稳定但任意的错误变化。本候选新增的计算约束是：变化必须满足任务语义规定的双射或数值平移关系。

## 当前经验状态

Formal 突变测试覆盖六种策略、五个任务族和二十个案例。联合关系对“稳定选择性采用”标签的平衡准确率为 1.0；只看相关变化为 0.75，加入无关不变性为 0.875。正确采用与错误但等变采用都通过，明确显示该探针不是正确性验证器。

三个本地模型、两种提示制度、二十个案例的 Formal 运行共完成 600 次调用且无调用错误。54 个单次精确正确行中，18 个没有通过联合关系，样本内脆弱率为 33.33%，Wilson 95% 区间为 [22.24%, 46.64%]；六个模型—提示分层中五个非零，且 18 个失败均无解析警告。该数字只描述当前冻结合成套件，不能外推。

## 最近先行边界

- METAL 已把变形关系系统用于大模型的稳健性、公平性、非确定性与效率评价，并包含输入扰动关系和相同输入重复；因此“关系式测试大模型”没有新颖性。当前候选只能主张工具字段采用这一特定诊断组合。
- ToolFailBench 区分工具跳过与结果忽略，但没有字段级任务关系重放。
- CAIR 通过反事实替换智能体输出测量结果与工作流变化，最接近一般反事实影响谱系；当前候选要求任务条件等变/不变关系，而非仅测影响大小。
- ReliabilityBench 使用动作变形关系与终态等价性，主要变形任务/用户输入及执行序列；当前候选变形的是已返回的工具字段并诊断最终回答采用。
- CVT-RL 以工具输出扰动估计反事实贡献，用于带可验证终局奖励的强化学习信用分配；当前候选是无需训练的黑盒评价，不以终局奖励作为采用标签。
- PriVE-Tools 冻结问题与评分，只改变工具派生视觉证据条件并发现证据提供不等于证据采用；当前候选与其共享现象动机，但干预结构化返回字段、检验任务等变/不变关系，而不是比较视觉证据视图的正确率增益。

## 未决风险

最大风险是外部有效性和最近先行碰撞：当前案例为合成短答案任务，任务关系由研究者设计；即使内部对照成立，也尚未证明复杂、多步或开放式智能体轨迹中的效用。进入种子前必须完成独立求解器校验、正式复现、最近先行审计与固定评审。

## Final Core Evidence Closure (machine generated, bounded)

This appendix exposes selected Formal Spec, Claim and metric facts; it does not judge scientific sufficiency.
Closure SHA-256: `ca4c7ff9b845d0d719d415633caf9e4d3200f3f74de29c470e3c28c645233432`

```json
{
  "artifact_kind": "final_core_evidence_closure",
  "attempts": [
    {
      "attempt_id": "attempt-mutation-004",
      "execution_schema_version": 8,
      "execution_sha256": "9385d64776f9433a0e5a1a566b5b6ec83c9c736647eb7637e2b7261641553d51",
      "metrics": {
        "errors": {
          "items": [],
          "omitted_count": 0,
          "total_count": 0
        },
        "experiment_id": "exp-mutation-v004",
        "included_record_count": 3,
        "omitted_record_count": 0,
        "primary_metric_selection_priority": "bidirectional_relation_balanced_accuracy",
        "record_count": 3,
        "records": [
          {
            "aggregation": "balanced_accuracy",
            "n": 120,
            "name": "bidirectional_relation_balanced_accuracy",
            "source_index": 0,
            "split": "mutation_suite",
            "unit": "ratio",
            "value": 1.0
          },
          {
            "aggregation": "balanced_accuracy",
            "n": 120,
            "name": "selective_change_balanced_accuracy",
            "source_index": 1,
            "split": "mutation_suite",
            "unit": "ratio",
            "value": 0.875
          },
          {
            "aggregation": "balanced_accuracy",
            "n": 120,
            "name": "any_change_balanced_accuracy",
            "source_index": 2,
            "split": "mutation_suite",
            "unit": "ratio",
            "value": 0.75
          }
        ],
        "resource_usage": {
          "api_calls": 0,
          "estimated_cost": "unknown",
          "gpu_time_seconds": "unknown",
          "tokens": 0,
          "wall_time_seconds": 0.001351399998384295
        },
        "warnings": {
          "items": [],
          "omitted_count": 0,
          "total_count": 0
        }
      },
      "metrics_path": "experiment_v001/attempts/attempt-mutation-004/metrics.json",
      "metrics_sha256": "b60265bcd2c3030c8f4021a6c38fed6d265060bfeea161c0f05530c592102644",
      "spec": {
        "claim_ids": {
          "items": [
            "claim-mutation-discrimination"
          ],
          "omitted_count": 0,
          "total_count": 1
        },
        "dataset": "suite_spec.json 生成并冻结的五任务族二十案例。",
        "experiment_id": "exp-mutation-v004",
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
        "model": "六种确定性策略：faithful、wrong_equivariant、misdirected_selective、ignore、distractor、unstable。",
        "primary_metric": "bidirectional_relation_balanced_accuracy",
        "provider": "本地 Python 3 确定性策略后端。",
        "purpose": "mechanism_consistency",
        "research_question": "任务定向输出关系是否在相同回答集合上排除方向错误但选择性的伪采用，从而优于只看变化与变化加不变性？",
        "revision": "implementation_v001 full-manifest binding; mutation computation unchanged",
        "sampling_unit": "冻结案例与可控策略的笛卡尔积，共 120 行。",
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
      "spec_path": "experiment_v001/attempts/attempt-mutation-004/spec.json",
      "spec_sha256": "1cc3b8cbd88a803fa508518ac12ea9ff29fd7a03ffd303095177453ac150b51a"
    },
    {
      "attempt_id": "attempt-qwen-004",
      "execution_schema_version": 8,
      "execution_sha256": "2d0d12838154fdf9d636fd133ba6d0e2d6805c2ff1eaf9b9ccead65daf101579",
      "metrics": {
        "errors": {
          "items": [],
          "omitted_count": 0,
          "total_count": 0
        },
        "experiment_id": "exp-qwen-v004",
        "included_record_count": 3,
        "omitted_record_count": 0,
        "primary_metric_selection_priority": "one_shot_success_brittleness_rate",
        "record_count": 3,
        "records": [
          {
            "aggregation": "mean",
            "n": 54,
            "name": "one_shot_success_brittleness_rate",
            "source_index": 0,
            "split": "local_models",
            "unit": "ratio",
            "value": 0.3333333333333333
          },
          {
            "aggregation": "mean",
            "n": 120,
            "name": "bidirectional_relation_pass_rate",
            "source_index": 1,
            "split": "local_models",
            "unit": "ratio",
            "value": 0.3
          },
          {
            "aggregation": "mean",
            "n": 66,
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
          "tokens": 137323,
          "wall_time_seconds": 348.4525797999995
        },
        "warnings": {
          "items": [
            "ollama::qwen2.5:7b::strict/tier_score_03/repeat: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict/count_open_01/relevant: response was not a JSON object with an answer key",
            "ollama::qwen2.5:7b::strict/count_open_02/relevant: response was not a JSON object with an answer key",
            "ollama::qwen3:8b::strict/tier_score_02/irrelevant_plain: response was not a JSON object with an answer key"
          ],
          "omitted_count": 0,
          "total_count": 4
        }
      },
      "metrics_path": "experiment_v001/attempts/attempt-qwen-004/metrics.json",
      "metrics_sha256": "10cd9ca9f2fe5d3a74b7d8c3d34082727abd70e824c8ef6d18abbf45fa1f051c",
      "spec": {
        "claim_ids": {
          "items": [
            "claim-one-shot-brittleness"
          ],
          "omitted_count": 0,
          "total_count": 1
        },
        "dataset": "五个确定性结构化工具任务族、每族四例、共二十例。",
        "experiment_id": "exp-qwen-v004",
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
        "revision": "implementation_v001 full-manifest binding, endpoint-fix, temperature 0, think false, JSON schema answer string",
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
      "spec_path": "experiment_v001/attempts/attempt-qwen-004/spec.json",
      "spec_sha256": "97ece5b833a0a491ed549b2fedf478ef228b8237fcc1e98ff22c643b8ae2139e"
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
    "sha256": "7ce687f90953285c768e765de9e72ebb8c49e5d743fd88a84f31960232c0cd8a"
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
          "source_path": "experiment_v001/attempts/attempt-mutation-004/metrics.json",
          "source_value": 1.0
        },
        "kind": "finding",
        "message": "数字映射 0 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-mutation-004/metrics.json#/records/0/value"
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
          "seed_value": 0.875,
          "source_path": "experiment_v001/attempts/attempt-mutation-004/metrics.json",
          "source_value": 0.875
        },
        "kind": "finding",
        "message": "数字映射 1 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-mutation-004/metrics.json#/records/1/value"
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
          "seed_value": 0.75,
          "source_path": "experiment_v001/attempts/attempt-mutation-004/metrics.json",
          "source_value": 0.75
        },
        "kind": "finding",
        "message": "数字映射 2 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-mutation-004/metrics.json#/records/2/value"
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
          "seed_value": 0.3333333333333333,
          "source_path": "experiment_v001/attempts/attempt-qwen-004/metrics.json",
          "source_value": 0.3333333333333333
        },
        "kind": "finding",
        "message": "数字映射 3 可追踪到精确实验事实。",
        "sources": {
          "items": [
            "seed_v001.md",
            "experiment_v001/attempts/attempt-qwen-004/metrics.json#/records/0/value"
          ],
          "omitted_count": 0,
          "total_count": 2
        }
      },
      {
        "code": "seed_numeric_literals_unmapped",
        "details": {
          "numeric_literal_count": 10,
          "numeric_literals": [
            "1",
            "0.95",
            "0.05",
            "2",
            "54",
            "18",
            "95%",
            "0.2224",
            "0.4664",
            "18"
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
    "attempt-mutation-004",
    "attempt-qwen-004"
  ],
  "version": "v001"
}
```

## Evidence Inventory (machine generated)

```json
{
  "comparison_count": 0,
  "comparisons": [],
  "formal_attempt_count": 6,
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
      "valid_review_support": true
    },
    {
      "association": "MATCH",
      "attempt_id": "attempt-mutation-004",
      "path": "experiment_v001/attempts/attempt-mutation-004/execution.json",
      "read_error": null,
      "record_sha256": "9385d64776f9433a0e5a1a566b5b6ec83c9c736647eb7637e2b7261641553d51",
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
      "valid_review_support": true
    },
    {
      "association": "MATCH",
      "attempt_id": "attempt-qwen-004",
      "path": "experiment_v001/attempts/attempt-qwen-004/execution.json",
      "read_error": null,
      "record_sha256": "2d0d12838154fdf9d636fd133ba6d0e2d6805c2ff1eaf9b9ccead65daf101579",
      "schema_version": 8,
      "selected_in_core": true,
      "status": "SUCCESS",
      "valid_review_support": true
    }
  ],
  "implementation_key": "cfd9cb4f4decadc4ec3587ec8b1df391c76771a0c0c6f8819e91d6b1abfa22b8",
  "machine_judgment": "NONE_FACTS_ONLY",
  "recorded_attempt_count": 0,
  "recorded_attempts": [],
  "schema_version": 1,
  "version": "v001"
}
```
