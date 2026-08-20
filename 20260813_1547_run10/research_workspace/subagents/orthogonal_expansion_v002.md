# v002 后备正交研究空间扩张（非权威草案）

## 0. 文档边界与结论先行

本草案只服务于当前 Run `20260813_1547_run10` 的 v002 后备空间扩张；不生成 Candidate、Seed、Decision 或最终科研裁决。材料只来自当前 Run、只读共享知识库与一级网络来源，未读取其他 Run。

本轮显式排除或降权以下已死亡/被占据计算：自动 API 测试预言机或写后读回验证、ToolGate/Cordon 式事务门、依赖图局部回滚、Sherlock 式验证预算放置、提示式自审和模块堆叠。保留下来的四条正交路线分别作用于：

1. **读观测的否定语义**：什么时候“没看到”才允许推出“不存在”；
2. **工具结果到后续动作的因果使用**：结果发生任务相关变化时，行为是否随之正确变化；
3. **时间流逝下的工具调用决定**：相同历史在不同 elapsed-time 下是否应重新调用工具；
4. **工具菜单呈现扰动下的选择稳定性**：功能不变而名称、描述、顺序或相关干扰项变化时，工具选择是否漂移。

按“当前资源可做真实实验 + CCF-B 方法潜力 + 最近先行风险”综合排序：

| 顺位 | 路线 | 失败证据 | 最近先行风险 | 当前科研姿态 |
|---|---|---|---|---|
| 1 | R2 工具结果相关变换等变性 | A：两组直接干预证据 | 高 | **KEEP-CONDITIONAL**；不能退化为 AgentCheck 式测试工作台 |
| 2 | R1 观察覆盖证明 | A（失败存在）；算子证据仍不足 | 极高 | **REFRAME-CONDITIONAL**；单纯三值标签只是符号化实现 |
| 3 | R3 时间盲性与时态化工具调用 | A | 极高 | **BACKUP-ONLY**；简单时间戳、TTL 或工具调用门已接近被占据 |
| 4 | R4 工具菜单呈现干扰 | A | 致命/近致命 | **FAILURE-ONLY**；适合压力测试，不宜优先开方法盆地 |

这里的 `A/B` 一方面指 CRL evidence level，另一方面每条路线都列出实际配对、消融或干预式 A/B 证据。失败事实可以是 A 级，而拟议修复仍可能只有 C 级；两者没有混写。

## 1. 检索记录与降级

### 1.1 Run-local purpose-aware retrieval

已存在的主检索包：

- `hypotheses_v002/searches/orthogonal_expansion_v002_01/`
- 用途覆盖 `failure / problem / measurement / operator`，查询包括工具菜单扰动、结果忽略、长输出压缩、记忆负迁移、澄清、工具输出反事实扰动与 choice-set stability。
- 结果：720 条原始观测、98 篇去重论文、201 个 Cards、216 个 Evidence、146 个 Passages；各路由 `degraded=false`，有 2 个机械噪声标记。

为补充“观察覆盖证明”，另执行：

- `hypotheses_v002/searches/observation_coverage_proof_v002/`
- `failure=agent tool observation incomplete pagination permissions stale freshness successful read absence unknown`
- `problem=tool using LLM agent absence from partial observation not evidence of nonexistence belief state`
- `measurement=coverage pagination exhaustion permission scope freshness read success unknown open world tool benchmark`
- `operator=coverage certificate observation completeness proof obligations belief state tool agent`
- `prior=Agent-BRACE BeliefMem NeSyFS belief state uncertainty tool agent`
- 结果：320 条原始观测、72 篇去重论文、117 个 Cards、153 个 Evidence、64 个 Passages；所有检索路由 `degraded=false`，有 3 个机械噪声标记。查询词中的具体 2026 论文名没有在冻结库形成直接命中，因此最近先行判断不能由本地排序替代，已核对一级网络正文。

### 1.2 一级来源检索

核对日期为 2026-08-13。主要定向查询包括：

- `Agent-BRACE 2605.11436`、`BeliefMem 2605.05583`、`NeSyFS 2607.28942`；
- `tool result ignore counterfactual observation action sensitivity`、`AgentCheck 2607.11098`、`AttriGuard 2603.10749`、`Causal Agent Replay 2606.08275`；
- `tool selection order description bias`、`BiasBusters`、`ToolTweak`、`ToolScope`、`canary tools`；
- `tool temporal blindness elapsed time freshness`；
- 数据库/知识库的 `query completeness / open-world negation / partial closed-world`。

网络检索只用于最近先行和公开 benchmark 路径；任何“未找到同构工作”均只视为暂时未命中，不视为新颖性证明。

## 2. R1：观察覆盖证明——从“不在返回中”到“可证明不存在”

### 2.1 可反证失败模式

- `failure_mode_id`: FM-v002-OCP
- `failure_statement`: 文本与工具型智能体会把局部、未穷尽、越权不可见、已经陈旧或调用失败的读结果当成完整世界快照，从“未见目标实体/关系”错误推出“目标不存在”，进而采取错误的后续动作。
- `affected_setting`: 返回集合或列表的工具；分页/游标；主体权限隔离；最终一致或带时间戳的数据；认证、网络或模式错误可能表现为空集合的接口。
- `evidence_level`: **A-for-failure**；方法修复仍是 C。
- `linked_route_status`: 自动写后读回验证已被本 Run 杀死且被最近工作占据；本路线只有在它适用于普通读观测的否定推理、而非验证某次写是否成功时才具正交性。

### 2.2 直接 A/B 证据

1. **当前 Run 的 AppWorld 配对 Scratch（直接、单域）**：`workbench_v001/scratch_appworld_silent_noop/paired_noop_discriminativity.json` 与 `scratch_report.md` 比较真实写世界和 success-shaped silent-no-op 世界。七个已编译 post-only entity witnesses 中只有一个同时通过洁净世界并拒绝空操作；四个在两世界都为真，两个在两世界都为假。`venmo.remind_payment_request` 的真实副作用是接收者通知，而相同调用者是发送者；调用者可见的请求集合在真实写和空操作下都不变。这个 A/B 直接反证“同权限读不到 ⇒ 副作用不存在”，但只覆盖一个权限不可见实例，不能自动外推到所有分页/新鲜度情形。
2. **AgentCheck（直接、公开干预）**：其 clean/faulted replay 固定其他工具结果、只改变一个响应；Category B 的 stale、contradiction、wrong answer、silent empty 是五个 Agent 最弱故障带。B4 明确要求把 silent empty 当作“缺少观测”而非任务事实的否定；弱 Agent 上 schema-aware handling 只从 1/10 到 4/10，完整 mitigation stack 到 7/10。论文也显示简单重试几乎不改善 stale/contradiction/wrong-answer。一级来源：[AgentCheck](https://arxiv.org/html/2607.11098)，§3–§5。
3. **相邻直接证据**：Agent-BRACE 的 TextWorld 定性例把未访问出口、未读 cookbook 等保持为 `possible/unknown`，而不是从未见推出不存在；七级不确定性压成二元 certain/unknown 时，Qwen3-4B 平均准确率从 79.3% 降到 65.3%。这证明显式不确定性对局部可观测决策有用，但没有测试 API 分页、权限、调用成功或时间新鲜的覆盖证书。[Agent-BRACE](https://arxiv.org/html/2605.11436)，§2.3、§4、Appendix K。

### 2.3 干预算子的最小计算边界

可审计的覆盖条件可写成一个**否定事实的导出规则**，而不是“再读一次”：

```text
NEGATIVE(predicate, observation) 可成立，当且仅当：
  read_success
  AND enumeration_exhausted
  AND permission_scope_covers(predicate.subject_scope)
  AND observed_at >= predicate.required_freshness
否则：UNKNOWN
```

四个条件分别对应：

- `read_success`：调用确实成功，且空结果不是认证、网络、模式或反序列化失败的降级表示；
- `enumeration_exhausted`：游标结束、短页/终止条件可证明，且没有截断、重复页或安全上限提前停止；
- `permission_scope_covers`：当前凭据的可见主体/资源类别足以覆盖被否定命题；不能借用其他用户凭据补洞；
- `required_freshness`：返回的观察时点满足任务所需时间窗口；陈旧快照只能支持历史命题。

**正交生存条件**：该规则只约束智能体如何解释已经发生的读观测以及何时允许生成否定事实；不得围绕每次写调用自动生成读回计划、不得把它放进 ToolGate/Cordon 式 commit gate，也不得用它做验证预算调度。

### 2.4 与指定最近工作的组件级区分

| 工作 | 已有计算 | 与覆盖证明的差异 | 碰撞判断 |
|---|---|---|---|
| [Agent-BRACE](https://arxiv.org/html/2605.11436) | belief model 把原子自然语言 claim 标为 `confirmed ... unknown`，policy 直接以 belief 作上下文；两模块用 PPO 联合训练，state correctness/tracking reward 依赖训练期世界状态或 LLM judge | 不确定性是学习到的 claim confidence；没有“只有分页、权限、新鲜度、调用成功齐备才允许导出否定”的证明义务 | **强相邻，不同构**；若覆盖证明只把 `unknown` 改成符号字段，则被其吸收 |
| [BeliefMem](https://arxiv.org/html/2605.05583) | 对每个 attribute 保存多个候选结论及独立概率，以 Noisy-OR 合并支持证据；只存已被观察支持的候选 | 作者明示不是完整归一化 posterior、没有理论收敛保证；其概率回答“候选多可信”，不回答“枚举/权限覆盖是否足以推出不存在” | **强相邻，不同构**；若本路线只是多候选概率记忆，则被其吸收 |
| [NeSyFS](https://arxiv.org/html/2607.28942) | 从 observation/action 更新 KG，加入新 triplet、删除旧 triplet；KG 支持 fast reaction、反思和 TSMC 式 slow planning | 没有 `unknown`/coverage certificate；缺少某 triplet 不构成可审计的否定推理 | **结构相邻**；若只是在 KG edge 上加标签，则只是实现扩展 |
| 一般 POMDP / belief-state 方法 | 维护 latent state 的 posterior 或其近似，基于历史选择动作 | 覆盖证明是 observation semantics：判定一个具体负命题是否是所有与观测兼容世界中的 certain answer | **概念先行充分**；不能声称“首次考虑部分可观测” |
| 数据库 completeness / partial closed-world | 已有 completeness statements、query completeness、open-world negation 与 certain answers | 正好提供“何时缺失可当作否定”的逻辑祖先 | **潜在致命祖先**；仅把数据库完备性规则搬到 Agent 中不足以成为新方法 |

相关数据库一级入口：[Completeness, Recall, and Negation in Open-World Knowledge Bases](https://arxiv.org/abs/2305.05403)、[Complete Approximations of Incomplete Queries](https://arxiv.org/abs/2407.20932)。

### 2.5 这是新计算还是符号化实现？

**当前判断：单独的四位 coverage flag + `FALSE/UNKNOWN` 规则更接近“经典开放世界/查询完备性语义在工具 Agent 中的符号化实现”，尚不足以证明 CCF-B 方法贡献。** 它只有在以下至少一项成立时才可能升级为真正的新计算：

- 从自然语言工具规范和真实响应中自动合成可复查的覆盖证明义务，而不是人工写四个布尔字段；
- 在不新增权限、不依赖隐藏状态的条件下，联合求解最小必要观测与不可区分世界，证明何时永远只能 `UNKNOWN`；
- 把 coverage certificate 编译为 action semantics，使不同工具/分页/主体/时态在同一推理系统中组合，并在真实长程任务上产生超出简单规则的可测收益。

如果实现只是 `if status==200 and has_more==false then absent`，或只把 Agent-BRACE 的 `unknown` 标签换成 JSON，该楔子应立即淘汰。

### 2.6 强基线、最小高信息量检查与 benchmark 路径

**强基线**：闭世界 `empty⇒absent`；always-UNKNOWN；手工四条件硬规则；Agent-BRACE 式自然语言 belief；Verified Tool Calls 的手工三值后置条件（只作为邻近上界，不重新打开写后验证）；分页穷尽但不检查权限/时间的消融。

**最小检查**：在当前 Run 的 AppWorld dev 环境中选择 12–24 个只读/列表决策点，逐一构造四个单因素配对：完整页 vs 截断页、同凭据覆盖 vs 同凭据不可见、fresh vs stale、成功空集合 vs 错误降级空集合。任务要求根据“是否存在对象”选择下一动作，不包含前置写调用。比较闭世界、手工规则与自动覆盖推导：

- negative-entailment precision/recall；
- `UNKNOWN` 覆盖率及错误弃答成本；
- 后续动作正确率和任务终局；
- 额外工具调用与 token 成本；
- 各 coverage bit 的独立消融。

**公开路径**：AppWorld dev；ToolSandbox 的状态化多轮工具任务；AgentCheck 的 B1–B4 scenarios。AppWorld 当前已在 Run-local 环境可执行；ToolSandbox/AgentCheck 需另行核对依赖，但公开代码/场景可作为第二域。

**最可能杀死本路线的事实**：手工四条件规则已经达到全部增益；自动合成只是在复现 OpenAPI/REST query completeness；或大部分真实 API 根本不暴露足够权限/分页/时间元数据，使方法几乎全部输出 `UNKNOWN`。

## 3. R2：工具结果相关变换等变性——调用了工具却没有让结果支配行为

### 3.1 可反证失败模式

- `failure_mode_id`: FM-v002-ROE
- `failure_statement`: 智能体完成了正确工具调用，甚至收到了正确结果，但最终回答或下一动作仍由参数化先验、既有计划或无关上下文支配；当工具结果发生任务相关变化时，行为不发生应有变化，或当无关字段变化时反而漂移。
- `affected_setting`: 单轮函数调用后的回答；多步轨迹中中间结果决定下一工具参数/分支；工具结果与模型先验冲突的任务。
- `evidence_level`: **A**。
- `orthogonality`: 它不验证工具是否真的改变外部状态，不做回滚/事务门，也不问“哪一步值得验证”；它只审计并可能约束 `observation → action` 的功能依赖。

### 3.2 直接 A/B 证据

1. **ToolFailBench**：1,000 个单轮任务中，tool-required parametric traps 让 mock result 反驳模型可能记忆的先验；paired no-tool controls 则挂载同类工具但应直接回答。论文单独标注 `Tool-Skip / Result-Ignore / Output-Fabrication / Unnecessary-Tool-Use`，最佳模型 Clean Tool-Use Rate 也只有 86.33%。这是“调用后忽略结果”与“未调用”可分的直接配对证据。共享库定位：P039，`ev-p039-failure-core`、`ev-p039-aggregate-score-masking`，PDF `knowledge_base/papers/P039_toolfailbench.pdf`；一级来源：[arXiv:2607.04686](https://arxiv.org/abs/2607.04686)，公开 traces：[Hugging Face](https://huggingface.co/datasets/SoHarshh/toolfailbench-traces)。
2. **Tool-use Tax 的 OracleCalc 干预**：Agent-OracleCalc 让工具直接返回 gold answer，消除计算/格式错误，但模型仍需消费结果。计算错误被修正后，Type D“工具结果正确但最终预测错误”成为 66–74% 的主要残余瓶颈。该干预直接说明“正确工具输出”不等于“被正确整合”。一级来源：[Are Tools All We Need?](https://arxiv.org/html/2605.00136)，§2.2、§3.4、Appendix B。

### 3.3 可研究的干预算子与正交生存条件

最小非提示式干预不是让模型“再检查一次”，而是定义**相关变换等变性 / 无关变换不变性**：

- 对固定任务、工具调用和历史，把一个任务决定性字段替换为另一个类型合法值；正确的下游 answer/action 应按已知映射变化；
- 只替换时间戳格式、无关 metadata、字段顺序等不影响任务语义的内容；正确行为应保持不变；
- 将两类配对约束用于训练一个 observation-use policy、选择候选动作，或形成可执行的行为约束；不能只生成诊断报告。

这条路线的可能方法空间是“相关变量变化时应如何改变动作”的结构化等变约束，而不是“工具结果是否看起来可信”。它允许研究结果整合而不需要外部真值进入部署输入。

### 3.4 最近先行风险

| 工作 | 最邻近计算 | 风险 |
|---|---|---|
| [AgentCheck](https://arxiv.org/html/2607.11098) | 缓存真实工具响应，只改一个响应并 replay；比较 clean/faulted/mitigated 三条轨迹 | **最直接测试碰撞**。如果本路线只做 tool-output perturbation + rerun + 报告差异，已被完整吸收 |
| [AttriGuard](https://arxiv.org/html/2603.10749) | teacher-forced shadow replay；削弱外部 observation 的控制成分；用 action survival 做 causal attribution | **方法形状强碰撞**。虽目标是提示注入，已占据“并行反事实 observation + 动作级因果归因” |
| [Causal Agent Replay](https://arxiv.org/abs/2606.08275) | 对 Agent step 做 do-intervention 并向前重执行，以 outcome distribution 估计因果效应 | **一般因果 replay 祖先**；只换成工具结果字段不足以新颖 |
| ToolFailBench / Tool-use Tax | parametric traps、gold-output oracle、Result-Ignore / Type-D measurement | 已占据 failure measurement，不提供普适修复 |

因此，只有“任务相关字段—动作关系的可组合等变约束”真正改变 inference/training computation、且超过 AgentCheck/AttriGuard/CAR 的直接适配时，才有方法潜力。若只做反事实 replay 测试，路线应淘汰。

### 3.5 强基线、最小高信息量检查与 benchmark 路径

**强基线**：原始 ReAct/native function calling；明确“严格使用工具结果”的提示基线；等 token 的独立重采样/多数票；字段抽取后直接回答的 deterministic upper bound；AgentCheck replay detector；AttriGuard 的 observation-attenuation 适配；训练时不加等变损失的相同模型。

**最小检查**：从 ToolFailBench 的 Result-Ignore 子集抽取 80–120 条，生成三联组：原始返回、任务相关字段的类型合法替换、无关字段替换。固定 task、tool schema、tool call 和 pre-result history，对同一 Agent 运行：

- `relevant_sensitivity`：答案/下一动作是否按预注册映射正确变化；
- `irrelevant_invariance`：无关变化下是否保持；
- `prior_override_rate`：返回与参数先验冲突时回退先验的比例；
- `overreaction_rate`：无关字段导致动作漂移；
- 成本与 abstention。

若单轮信号成立，再在 AppWorld dev 的纯读→后续分支任务上做 12–24 个 replay fixtures；使用官方 evaluator 只评终局，不向方法暴露 hidden state。

**公开路径**：ToolFailBench 代码与 633MB traces 已公开；AgentCheck 120 scenarios 与 MCP proxy 公开；AppWorld 当前 Run-local 可执行。

**最可能杀死本路线的事实**：AgentCheck + AttriGuard 的简单组合已经达到同样效果；配对约束只提升单轮答案复制、不能迁移到多步 action；或等变训练使模型盲从错误/恶意结果，安全—忠实权衡导致总体任务成功下降。

## 4. R3：时间盲性——相同历史在不同 elapsed-time 下仍作出同一工具调用决定

### 4.1 可反证失败模式

- `failure_mode_id`: FM-v002-TEMP
- `failure_statement`: 智能体默认上下文静止，对消息之间真实经过的时间不敏感，因而对已经陈旧的工具结果继续直接回答，或在几乎不可能变化的短间隔内重复调用工具。
- `affected_setting`: 动态事实、价格/状态/库存/日程等；多轮对话中上下文包含过去工具结果；任务对“最新/当前”有显式或隐式需求。
- `evidence_level`: **A**。
- `orthogonality`: 不判断某次写是否成功，也不做验证预算放置；研究的是 time-indexed observation 的有效域和正常工具调用 policy。

### 4.2 直接 A/B 证据

1. **TicToc controlled elapsed-time pairs**：76 个动态场景改变消息之间 elapsed time，收集人类在“调用工具/直接回答”间的偏好；即使提供时间戳，没有模型的 normalized alignment rate 超过 65%，naive prompt-based alignment 对多数模型效果有限。一级来源：[Your LLM Agents are Temporally Blind](https://aclanthology.org/2026.findings-acl.1848/)。
2. **AgentCheck stale pair**：同任务 clean response 为 2024 当前人口、faulted response 换成明确带 2011 年份的陈旧值；五个 Agent 中三个仍把 2011 数字称为当前，两个识别陈旧。固定其余响应的 A/B 支持“时间字段在场也可能不支配行为”。[AgentCheck](https://arxiv.org/html/2607.11098)，§5.2 Figure 4。
3. **相邻 A/B**：P095 在显式 serial 全序标记下，LLM 仍发生 prior-override 和 serial-comparison drift；matched pipeline 从 67.2 提升到 78.0（+10.8pp），漂移随长上下文从 75% 降到 61%。这直接支撑“显式时间/序号在上下文中不等于模型会应用”，但载体是 memory QA，不是工具调用决策。共享库：P095，`ev-p095-prior-override-drift`、`ev-p095-matched-comparison`。

### 4.3 可能干预点与最近先行风险

只有把工具观测视为带**时间有效域**的 typed value，而不是在 prompt 里提醒“注意时间”，才算计算变化：每个结果携带 `observed_at` 与可解释的 validity interval；后续任务的 reference time 与 validity interval 做确定性关系计算，决定该值能否用于当前命题。若 validity 未知，输出时态 `UNKNOWN`，而不是模型猜测“可能过期”。

但最近先行已非常拥挤：

- TicToc 本身给出专门 post-training alignment 作为可行修复；
- P095 已占据显式版本标记下的 deterministic extract-then-max；
- P041 WHEN2TOOL 用 hidden-state probe 做 tool necessity gate；
- [SMART](https://aclanthology.org/2025.findings-acl.239/) 通过监督训练缓解 tool overuse；
- [Tool-use Tax](https://arxiv.org/html/2605.00136) 的 G-STEP 又占据 inference-time continue/commit gate。

因此，简单 timestamp prompt、TTL、always-refresh、hidden-state necessity probe 或二元 call gate 都不能作为新方法主张。只有“不同工具/属性的 time-validity semantics 可自动获得、组合并跨域迁移”才可能保留。

### 4.4 强基线、最小检查与 benchmark 路径

**强基线**：always-call；never-call；timestamp prompt；固定 TTL；P041 hidden-state probe；SMART；P095 deterministic latest；同成本 supervised classifier。

**最小检查**：直接复用 TicToc 的 paired elapsed-time split，在同一模型上比较 timestamp prompt、固定 TTL、typed validity interval 三种计算。预注册：human-alignment、真实 answer accuracy（若有）、不必要调用率、漏调用率、成本；必须分高/中/低 volatility，不能只报总平均。若公开数据不足以评终局，再在 AppWorld 选择可程序化设置不同更新时间的只读任务作第二域。

**公开路径**：TicToc 论文/数据；AppWorld dev；P095 FactConsolidation 类时序记忆载体只能作相邻稳健性域。

**最可能杀死本路线的事实**：固定 TTL 已等于或优于复杂算子；人类 tool-call preference 与实际任务正确性不一致；工具规范没有可靠 volatility/validity 元数据，自动估计又退化成有标签分类器；或该方向被视为 P095/TicToc/WHEN2TOOL 的直接组合。

## 5. R4：工具菜单呈现干扰——功能集合不变，选择因描述/顺序/相关干扰项漂移

### 5.1 可反证失败模式

- `failure_mode_id`: FM-v002-MENU
- `failure_statement`: 工具的功能适配度没有变化，但描述措辞、排列位置、供应商 metadata 或加入语义相关工具会显著改变工具选择，并连带产生 wrong function、wrong count、wrong parameter 与参数幻觉。
- `affected_setting`: MCP/函数调用；多工具市场；语义重叠工具；BFCL 类 AST 评价及真实 end-to-end 调用。
- `evidence_level`: **A**。
- `orthogonality`: 位于 action selection 之前，不处理工具结果、状态验证、回滚或预算调度。

### 5.2 直接 A/B 证据

1. **P069**：只编辑 tool description 可使 GPT-4.1 和 Qwen2.5-7B 的工具使用差异超过 10 倍；功能相同、描述/参数相同的工具仍表现出先出现偏置。共享库：`ev-p069-description-induced-preference`、`ev-p069-identical-tool-order-bias`；一级来源：[EMNLP 2025](https://aclanthology.org/2025.emnlp-main.1060/)。
2. **P084**：固定 200 个 BFCL request，把平均可见工具从 2.7 扩到 5.6、加入语义相关但预期功能不同的函数；表 2 的九个模型 AST 分数全部下降，错误含 wrong function、wrong function count、wrong parameter assignment 和 parameter hallucination。共享库：`ev-p084-expanded-toolkit-controlled-setting`、`ev-p084-expanded-toolkit-table`、`ev-p084-related-toolkit-error-types`；一级来源：[TrustNLP 2025](https://aclanthology.org/2025.trustnlp-main.20/)。
3. **近期重复证据**：[ToolTweak](https://arxiv.org/abs/2510.02554) 通过优化名称/描述把目标工具选择率从约 20% 推到最高 81%；[BiasBusters](https://arxiv.org/abs/2510.00307) 直接控制 metadata、顺序和预训练暴露并报告 selection bias。

### 5.3 可想到的干预算子及为何降权

一个纯测量算子是 `choice-set nuisance intervention`：对同一功能集合随机化顺序、等价改写描述、匿名化 provider、注入相关 decoys，测量 tool-selection distribution 的稳定性。它可以作为所有工具选择方法的强压力测试。

但把多次随机化结果做多数票、把工具描述统一改写、top-k filtering、tool merge 或“先过滤再均匀采样”作为方法，均已经高度占据或只是自洽采样：

- [BiasBusters](https://arxiv.org/abs/2510.00307) 已提出 relevant-subset filtering + uniform sampling；
- [ToolScope](https://aclanthology.org/2026.acl-long.1573/) 已做 tool merging、auto-correction 与 context-aware top-k retrieval，在三个 benchmark 上报告 8.38%–38.6% selection accuracy 增益；
- ToolTweak 已测 paraphrasing/perplexity filtering 防御；
- [Canary Tools](https://arxiv.org/abs/2608.04719) 已将 semantic decoy、parameter trap、capability mirage、prerequisite blindness、temporal decoy、granularity trap 做成 8,640-run 诊断框架。

所以本路线当前最多保留为 measurement/interference suite；没有找到不落入 filtering、merging、metadata normalization、随机采样或提示式自审的新算子。

### 5.4 强基线、最小检查与 benchmark 路径

**强基线**：原始全菜单；BM25/embedding top-k；ToolScope；BiasBusters；description paraphrase；order counterbalancing；等 token 的随机/多数票；oracle correct-tool-present 上界。

**最小检查**：复用 P069 公开代码与 P084 的 200 BFCL subset，构造 4× 配对：原顺序、反序、匿名工具名、等长描述改写；再加不同 decoy density。至少三 seeds，报告 AST、correct-tool recall、selection、argument correctness、端到端执行、prompt tokens 与 position-specific confusion。若任何拟议方法只在未 counterbalance 的单一顺序获益，立即判伪。

**公开路径**：P069 GitHub；BFCL；P084 subset；BiasBusters benchmark；Canary Tools；需要真实执行时可把少量 AppWorld API 工具规格映射成等价/近等价菜单。

**最可能杀死本路线的事实**：ToolScope/BiasBusters 已在同 benchmark 与公平 token budget 下达到同等或更好结果；扰动只暴露评测 confound，不能形成方法；或匿名化/统一描述本身损害工具语义，使“稳定”以更低正确率为代价。

## 6. 证据分级、缺口与人工抽查

### 6.1 Evidence admission table

| 路线 | 直接性与级别 | historical/source status | admission decision |
|---|---|---|---|
| R1 覆盖证明 | 当前 Run AppWorld real/no-op pair + AgentCheck controlled replay；A-for-failure | 自动读回/三值后置验证为 historical-route-conflict；数据库 completeness 是强祖先 | 失败模式可保留；算子只能进高风险 hypothesis backlog，不能当 gap 事实 |
| R2 结果等变性 | ToolFailBench parametric traps/control + Tool-use Tax OracleCalc；A | AgentCheck/AttriGuard/CAR 强碰撞但目标不完全相同 | 可保留作优先最小实验；方法主张需 component-level differentiation |
| R3 时间盲性 | TicToc elapsed-time A/B + AgentCheck stale A/B；A | TicToc/P095/P041/SMART/G-STEP source crowded | 只作后备；简单门/TTL 不准进入方法假设 |
| R4 菜单干扰 | P069 description/order + P084 expanded toolkit；A | BiasBusters/ToolScope/ToolTweak/Canary source occupied | failure/measurement keep；method route kill unless出现结构新算子 |

### 6.2 明确证据缺口

- R1 没有一篇直接论文同时测分页穷尽、同权限可见性、时间新鲜、读取成功四类覆盖，并证明该 coverage calculus 改善文本/工具 Agent 终局；当前只可拆分支撑。
- R1 尚未证明自动合成 coverage obligations 能超过四条硬编码规则，也未证明真实工具接口暴露足够 metadata。
- R2 的直接强证据主要为单轮或 calculator/search；长程 stateful action 的迁移需要 AppWorld/ToolSandbox 再证。
- R2 的 counterfactual output generation 可能引入人工模板伪影；需要 irrelevant control、type-valid replacement 和跨生成器测试。
- R3 的人类 tool-call preference 未必等于程序化任务成功；需要独立终局或真实时态事实核对。
- R4 的 AST 退化可能同时受 prompt 长度、工具顺序和生成 decoy 质量影响；方法实验必须配平 token 与 order。

### 6.3 被拒绝/仅相邻的空间

- **通用 observation/context compression**：P079 只有相邻原因证据；更近期 ACON 与 AGORA 已直接占据 AppWorld/OfficeBench 的 action-conditioned compression 和 agent-aware structural floor，降权。
- **experience replay portability / memory negative transfer**：P064 的 error propagation/misaligned replay 失败事实直接，但 2026 的 SAMem、MemHarness、Trajectory-Informed Memory Generation、continual memory reuse 已正面占据 state-aware retrieval、experience reconstruction 与 AppWorld memory guidance；不再列为优先正交方向。
- **普通 tool necessity / overuse gate**：P041、SMART、Tool-use Tax G-STEP 以及 ToolFailBench controls 已过度拥挤；简单 call/no-call classifier 不是新方法。
- **argument handle / provenance graph**：DORA 显示 gold tool order 只带来 1.08–4.40% 提升且 argument grounding 仍是瓶颈，但 opaque handle、producer-consumer graph、typed variable binding 已由 LLMCompiler、RESTler、MASTOR 等占据；容易退化成工程实现或依赖图变体。

### 6.4 人工抽查

- A 级抽查：R2 的 Tool-use Tax `Agent-OracleCalc` 不是从“论文没做结果整合”反推失败；论文明确让工具返回 gold answer，并直接报告正确计算后 Type D integration failure 升为 66–74% 残余瓶颈。
- 拒绝项抽查：R4 的 failure evidence 很强，但方法空间被 BiasBusters/ToolScope/ToolTweak/Canary 正面占据，因此不能把“失败仍存在”偷换成“存在新方法空白”。
- 关键 assumption：R1 自动 coverage synthesis、R2 等变约束的长程迁移、R3 validity semantics 的可得性均不是现有 evidence，必须由后续 Scratch/Recorded 实验处理，不能在本草案中写成事实。

## 7. 给主研究者的非裁决性实验顺序建议

若 v002 需要最少成本获得最大信息量，可先做两个互不依赖的 Scratch：

1. **R2 ToolFailBench 三联组**：不接真实写 API、不读回状态，80–120 个 task 即可估计 result-relevant sensitivity、irrelevant invariance 和 prior override；若简单 baseline 已饱和或 AgentCheck/AttriGuard 适配完全吸收，则迅速杀死。
2. **R1 只读覆盖四因素微基准**：不用写后验证，只测试“空返回是否允许导出否定”；先以手工四条件规则作为强基线。若自动方法不能超过硬规则或 `UNKNOWN` 覆盖率过低/过高，则该楔子只是符号化实现。

R3 和 R4 可作为上述两条失败后的独立 backtrack 空间，但在启动 implementation 前应先做更窄的最近先行/代码可用性核查。这里没有选出 Candidate，也不建议启动固定 Reviewer。

## 8. 主要一级来源

1. Agent-BRACE, arXiv:2605.11436. <https://arxiv.org/html/2605.11436>
2. BeliefMem, arXiv:2605.05583. <https://arxiv.org/html/2605.05583>
3. NeSyFS, arXiv:2607.28942. <https://arxiv.org/html/2607.28942>
4. AgentCheck, arXiv:2607.11098. <https://arxiv.org/html/2607.11098>
5. ToolFailBench, arXiv:2607.04686. <https://arxiv.org/abs/2607.04686>
6. Are Tools All We Need?, arXiv:2605.00136. <https://arxiv.org/html/2605.00136>
7. AttriGuard, arXiv:2603.10749. <https://arxiv.org/html/2603.10749>
8. Causal Agent Replay, arXiv:2606.08275. <https://arxiv.org/abs/2606.08275>
9. Your LLM Agents are Temporally Blind, Findings ACL 2026. <https://aclanthology.org/2026.findings-acl.1848/>
10. Tool Preferences in Agentic LLMs are Unreliable, EMNLP 2025. <https://aclanthology.org/2025.emnlp-main.1060/>
11. On the Robustness of Agentic Function Calling, TrustNLP 2025. <https://aclanthology.org/2025.trustnlp-main.20/>
12. BiasBusters, ICLR 2026. <https://arxiv.org/abs/2510.00307>
13. ToolTweak, arXiv:2510.02554. <https://arxiv.org/abs/2510.02554>
14. ToolScope, ACL 2026. <https://aclanthology.org/2026.acl-long.1573/>
15. Diagnosing Tool-Selection Reasoning with Canary Tools, arXiv:2608.04719. <https://arxiv.org/abs/2608.04719>
16. Completeness, Recall, and Negation in Open-World Knowledge Bases. <https://arxiv.org/abs/2305.05403>
17. Complete Approximations of Incomplete Queries. <https://arxiv.org/abs/2407.20932>
