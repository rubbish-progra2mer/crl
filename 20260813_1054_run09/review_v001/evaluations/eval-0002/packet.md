# CRL Fixed Review Packet

- Contract: 3
- Scientific version: v001
- Evaluator: CRL-EVAL-1.0
- Evaluator definition SHA-256: e0d35083b1427e9f8861ba576304b97657498fee46480d5e07e8e0b02cea6e5b
- Implementation key: e76decbab2541209f12f559ba63461caa055149a167607543c04f2515f0c58bf
- Implementation manifest SHA-256: e76decbab2541209f12f559ba63461caa055149a167607543c04f2515f0c58bf
- Evidence inventory SHA-256: 0e8ed52c89cac526814682d086f8b0cf9ae361694bc930438eb261551bc2bc61

## 1. Implementation / Seed Overview

### Source: `seed_v001.md`

# 计划派生证据义务：面向开放世界工具故障的提交前最小读回

## 研究种子

工具智能体执行写操作后，成功回执可能对应空操作、部分写入、错误对象或重复作用。固定写工具契约能保守验证状态，却会检查当前计划并不需要的字段；基于已知故障分支的信息增益方法更便宜，但其确信依赖封闭分支模型。

本种子提出 Plan-Derived Evidence Obligations（计划派生证据义务，PDEO）：不先猜故障类型，而从下一项外部副作用或成功声明所需的状态前提开始，沿类型计划反向传播证据义务，删除可信确定性步骤已经建立的谓词，再在只读探针覆盖和成本上求最小集合。只有每个剩余义务都由真实环境读回满足，受保护承诺才可执行。

## 计算核

设受保护承诺需要原子谓词集合 (G)，其前面存在一段类型化计划动作。对动作从后向前处理：可信确定性效果若建立了 (G) 中的谓词则消解它，并加入该动作自身前提；外部不确定写入及其回执不能消解义务。得到写后检查点的义务闭包 (O) 后，在探针集合 (R) 上求：

\[
\arg\min_{S \subseteq R} \sum_{r\in S} c(r)
\quad \text{s.t.} \quad
\bigcup_{r\in S}\operatorname{cover}(r) \supseteq O.
\]

运行时只读取 (S)，并对 (O) 做闭集判断。任何缺失、不匹配或读取失败都停止提交；恢复是独立策略，不属于当前方法核。

与 DQBP 的实质差异是：PDEO 没有后状态分支、故障先验或决策风险目标。与固定工具契约的差异是：义务由当前计划的下游承诺产生，而非永久绑定到写工具。与全量读回的差异是：计划无关状态不进入覆盖目标。

## 最近工作定位

[ToolGate](https://aclanthology.org/2026.findings-acl.470/) 用预先给定的霍尔式前置/后置条件控制调用和状态提交；PDEO 的候选增量是从当前计划反向生成写后证据集合并按探针成本最小化。[VERIMAP](https://arxiv.org/abs/2510.17109) 在规划时为子任务生成自然语言或 Python 验证函数；PDEO 限于类型状态谓词上的确定传播和环境读回。[Verified Tool Calls](https://arxiv.org/abs/2608.02645) 已覆盖写后验证和重试前验证，因此“验证写操作”本身不是本种子的新颖点。

[Failing Tools](https://openreview.net/forum?id=j7YsSnA64D) 把必需动作表述为证据义务和轨迹状态安全不变量，但其基准约束由人工给定。[ETAS](https://arxiv.org/abs/2607.17780) 更系统地提供类型/效果语义、轨迹监控和动态资源残余义务；PDEO 若要形成独立论文贡献，必须证明运行时状态证据编译与最小探针选择不是 ETAS 的直接实例。[AgentCheck](https://arxiv.org/abs/2607.11098) 支持系统故障注入评价，但不是计划派生义务方法。

因此，当前只能主张一个有碰撞风险的窄方法增量，不能声称已经完成新颖性证明。

## 反证历史

首个候选 DQBP 在三个域、每域 10,000 个同分布 Scratch 样本上与状态信息增益都达到 1.000 成功率和 0 危险错误，但平均探针成本为 1.7703，对方为约 1.707；预设成功率优势为 0。该结果杀死了“决策取商自然优于状态信息增益”的方法核，也促使本种子放弃封闭故障分支。

## 第一阶段正式证据

最终实现匹配的有效 Formal attempt `attempt-pdeo-formal-002` 在预约、访问控制和库存三个合成域上执行 171 个确定性案例：24 个原始分支、48 个系统性单义务替换、63 个安全无关字段替换和 36 个义务—无关字段配对替换。评价器以独立声明的安全规则生成标签，不调用 PDEO 编译器；执行 Schema 7、退出码 0、指标与输出契约均通过。较早的 001 运行数值完全一致，但实现文件身份清单未覆盖测试和辅助源码，因而保留为与最终实现不匹配的历史。

核心结果：

- 48 个单义务故障：PDEO 危险提交率 0；DQBP 为 0.5833，状态信息增益为 0.7500；
- 63 个安全无关变异：PDEO 提交召回率 1.000；DQBP 为 0.7460，状态信息增益为 0.9524；
- 同一义务故障分割平均探针成本：PDEO 3，写工具本地完整契约 5，全量读回 6；
- 人工最小义务同样是危险提交率 0、召回率 1、成本 3，说明编译器达到当前人工上界，但没有超越它。

指标文件哈希为 `c0bf6a60ead529de4eeb80e6881d378a44783e8d918597cfa0e61873cc962158`，执行记录哈希为 `65d6721da32c82b39c624c3cf7a752f7472f588f485494b25b2d3ed0e5aafad4`。这套实验只变化状态、不变化计划，因而首次固定三审拒绝把它视为计划条件化机制的充分识别。

## 三审驱动的计划变化证据

有效的首次固定三审 `eval-0001` 没有联网、工具或越界事件；三角色都将关键风险评为潜在致命。主研究者没有按聚合分数 61.1250 交付，而是接受实证 Reviewer 的核心异议并做一次有界修订：四个域各冻结四个计划变体，加入静态域契约、直接提交消融、人工逐计划最小上界和独立规则输入。

最终实现匹配的 `attempt-pdeo-plan-formal-002` 运行 178 个计划—状态案例：16 个规范安全、48 个单义务故障、60 个安全无关字段变异、22 个双义务故障和 32 个义务加无关字段故障。另运行 16 个规格遗漏敏感性案例。执行 Schema 7、退出码 0，指标、证据与输出契约均通过。

核心结果：

- 16 个计划的义务集合和探针集合精确匹配率均为 1.000；
- PDEO 逐计划平均探针成本为 2.000，静态域契约为 3.250；
- 48 个单义务故障中 PDEO 危险提交率为 0；
- 60 个安全无关变异中 PDEO 召回率为 1.000，静态域契约为 0.5333；
- 16 个故意遗漏真实安全原子的案例全部危险提交，直接证明规格不完整会摧毁保证；
- 四个域各自都保持 PDEO 故障危险提交率 0 和安全无关变异召回率 1，同时成本低于静态域契约。

计划变化排除了“每域固定三探针契约”的解释；人工逐计划最小上界与 PDEO 完全相同，说明方法只是把给定形式知识自动执行到同一上界，没有产生额外安全知识。执行记录散列为 `77b5b5ebba1161f070526bab564d7f6b09614fb7dd1e61eede362aa1e2e339a5`，指标散列为 `c32ebf96005ff9df20ddeaf3a50e49d46a717eb92d5f77c4bc603fb7afe7d24c`。

## 最小可证伪主张

在类型计划、工具效果、承诺安全原子和只读探针覆盖正确且完整，状态谓词离散、读回无噪声的四个受控域内，PDEO 能随计划变化编译出与人工最小义务一致的探针集合，在系统性义务故障上保持零危险提交，对安全的计划无关变异保持完整提交召回，并以严格低于静态域契约的平均探针成本实现这一性质。

“开放世界”只表示故障状态值不必来自候选的有限分支模型，并不表示安全谓词、对象类型或承诺语义是开放的。该主张不扩展到未知谓词、自然语言计划生成、真实应用程序接口、并发、陈旧读、权限失败、带噪探针、恢复质量或端到端任务成功率。

## 替代解释与失败边界

最强替代解释是：正确类型计划已经包含了关键安全知识，PDEO 只是经典最弱前置条件与加权集合覆盖的直接组合。计划变化实验确认该组合确实按计划重新编译，但仍无法排除“直接形式方法移植”的判断。

规格遗漏敏感性不是附带限制：遗漏一个真实安全原子时 16/16 案例危险提交。因此 PDEO 没有独立发现缺失规格的能力；同一 Run 作者产生的类型计划、冻结规则和探针目录仍可能形成同源偏差。

其次，信息增益和 DQBP 的高危险提交率来自其封闭分支模型无法表示系统性变异。这是目标失败模式的一部分，但不是对所有自适应验证方法的普遍优势；允许开放集异常检测或把义务谓词加入其状态模型后，差距可能缩小。

写工具完整契约验证的是“工具是否完整履约”，PDEO 验证的是“当前承诺是否已有足够证据”。两者目标不同；工具审计、合规或未来未知计划仍可能需要完整契约。

## 扩大价值

若第二次固定三审认为这颗窄种子仍具有方法潜力，下一步最有价值的扩大不是增加更多同构合成域，而是：

1. 在真实模型上下文协议或应用程序接口任务中，由独立标注者给出承诺前提并注入非原子故障；
2. 加入陈旧、权限受限和带噪读回，研究义务在证据来源不可靠时的组合规则；
3. 与 ToolGate 完整契约、开放集故障检测及 ETAS 式残余义务做组件级实现比较；
4. 单独评价自然语言计划到类型义务的转换，避免把规格错误藏在控制器之外。

这颗种子的价值在于把“验证写工具”收窄成可计算、可反证的计划条件化证据闭包，并以计划变化而非只靠状态变化识别其机制；是否达到 CCF-B 方法潜力，仍取决于最近工作碰撞和第二次固定 Reviewer 对“直接形式方法移植”异议的判断。

### Source: `candidate_v001.md`

# 候选方法：计划派生证据义务

暂名：Plan-Derived Evidence Obligations（计划派生证据义务，PDEO）。

## 问题边界

工具智能体执行状态写入后，结构合法的成功回执并不等于真实环境已经满足后续动作的安全前提。完整读回所有状态虽然稳健，却把与当前计划无关的字段也纳入验证；基于已知故障分支的自适应探针又可能在开放世界故障下过早确信。

PDEO 只处理带类型的工具计划：计划节点显式给出状态前提、确定性效果、依赖边和外部承诺标记。它不声称从任意自然语言自动得到正确形式规格；自然语言到类型计划的生成质量是后续扩展问题。

## 真实计算变化

1. **承诺锚定**：从会产生外部副作用或面向用户成功声明的计划节点开始，提取其必须有环境证据支持的原子谓词。
2. **向后义务传播**：沿计划依赖图反向传播这些谓词。可信确定性节点可以用已声明效果消解或改写谓词；刚执行的外部写操作及其回执不能自行消解义务。
3. **证据最小化**：合并重复谓词，并删除已由可信、未过期观测蕴含的谓词，得到当前写入之后的最小证据义务集。
4. **探针编译**：在只读探针的谓词覆盖集合与调用成本上求最小成本覆盖，而不是枚举故障分支或最大化状态熵。
5. **闭集提交**：只有每个义务都被真实读回且取值满足时，才允许执行被保护的承诺；不满足、缺失或读取失败一律停止提交并交给独立恢复策略。

PDEO 改变的是运行时验证条件的来源：验证集合由当前计划的下游承诺反向计算，而不是由写工具的固定后置条件、通用读回清单或已知故障分布给出。

## 与首个失败候选的关系

决策取商分支探针（DQBP）依赖有限分支模型和先验，在 Scratch 中被共享分支模型的状态信息增益基线完全追平且成本更高。PDEO 不再预测故障分支或恢复动作，只为“现在能否安全提交下游承诺”生成最坏情况证据义务。两者的输入、目标函数和失败边界不同，PDEO 不把 DQBP 的负结果改名复活。

## 公平基线

- 无验证与静态回执契约：不读取环境；
- 固定目标读回：只读取写入目标的表面状态；
- 写工具本地完整契约：验证该写工具声明的全部效果，包括当前计划无关字段；
- 全量读回：调用所有可用只读探针；
- 状态信息增益与 DQBP：共享同一已知分支模型、探针目录和预算；
- 人工最小义务：人工给出真实下游前提，作为义务编译质量上界，不作为可部署方法。

所有方法共享同一类型计划、工具规格、只读探针和真实返回。隐藏模拟器只负责生成状态及评价提交是否安全，不向 PDEO 暴露当前样本标签或故障类型。

## 固定三审后的机制识别修订

首次固定三审指出，原 Formal 只变化环境状态而没有变化计划，因此 PDEO 在三个域中总是选择固定的三探针集合，尚不能识别“计划派生”是否真正发生。修订版冻结四个域、16 个计划变体与独立评价规则；同一域内的承诺前提随计划变化，静态域契约取该域全部可能义务的并集，直接提交消融只保留最终动作的直接前提。PDEO 必须逐计划重编译义务与探针集合，而不是读取评价器的隐藏状态标签。

修订版还加入规格遗漏敏感性：从每个计划的真实安全规则中故意删去一个原子谓词，只破坏该谓词并观察危险提交。该实验不是为方法加分，而是把“类型规格完整性是致命外部前提”变成可量化的反证边界。

## 杀手实验

在预约、访问控制和库存三个状态型工具域中加入两类条件：

- 已知分支：来自控制器可见的正常、空操作、部分写入、错误目标和重复写入模型；
- 未见故障：在已知分支模型之外，伪造表面成功或审计事件，但破坏一个下游承诺所需谓词。

主指标是危险提交率、合法状态提交召回率和平均探针成本。若 PDEO 不能在未见故障上比 DQBP/状态信息增益显著降低危险提交，或其成本不优于写工具本地完整契约，则该方法核淘汰。若优势仅来自人工暴露隐藏故障标签或把评价真值写入义务，也直接淘汰。

## 2. Closest Prior Evidence

### Source: `nearest_prior_v001.md`

# 最近工作边界：计划派生证据义务

本文件记录当前检索能支持的边界，不宣称已经证明新颖性。

## 直接近邻

1. **ToolGate（Findings of ACL 2026）**：维护显式符号状态，用预先给定的霍尔式前置/后置条件决定工具能否调用及结果能否提交。PDEO 的差异候选是后置验证集合由当前计划的下游承诺反向生成，并按探针成本最小化；若 ToolGate 正文已经包含等价的计划条件化契约合成，则差异消失。
2. **VERIMAP / Verification-Aware Planning for Multi-Agent Systems（ICLR 2026 投稿）**：规划器在分解子任务时同时生成验证函数，并在失败后重规划。PDEO 不生成任意自然语言或 Python 验证函数，而在类型状态谓词上做确定的反向传播与最小证据覆盖；两者都属于验证感知规划，方法级重叠很强。
3. **Failing Tools（2026）**：把必需动作解释为证据义务、禁止动作解释为轨迹状态安全不变量，并要求写后读回。其约束由基准人工给定；PDEO 试图从类型计划计算当前承诺所需义务。术语和目标高度接近，必须避免把人工基准约束误报成方法空白。
4. **Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures（2026）**：写后验证、重试前验证和幂等键的轻量包装器。PDEO 的剩余差异只可能是验证谓词的计划条件化生成与最小化，而不是“写后验证”本身。
5. **ETAS: An Effect-Typed Language for Agent Systems（2026）**：以类型/效果语义表示智能体、工具、策略和轨迹，对动态资源发出残余义务。它比 PDEO 更靠近编程语言与静态保证；PDEO 若不能证明自己在运行时探针选择上的独立计算与实证价值，就会被视为较弱实例。
6. **AgentCheck（2026）**：对模型上下文协议工具注入超时、陈旧数据等故障，并评价缓解策略。它强化了未见运行时故障的评价必要性，但不是计划条件化证据编译方法。

## 方法成立所需的最小差异

PDEO 必须同时满足：

- 义务来自下游承诺，而非人工为当前样本写入故障标签；
- 对计划无关的工具状态不做完整验证，成本低于完整工具契约；
- 不依赖封闭故障枚举，在未见故障上比 DQBP/信息增益更少危险提交；
- 类型计划错误、工具效果错误和探针覆盖缺失被明确列为保证边界。

缺少任一项时，当前候选将分别退化为固定后置条件、全量读回、已有分支探针或无法验证的形式化包装。

## 修订后的组件级边界

首次固定三审后，方法增量进一步收窄为三个必须同时存在的组件：从当前承诺做反向义务传播、把未被可信确定性动作消解的义务编译为最小成本读回、在证据不全时闭集拒绝。去掉第一项会退化成工具级静态契约；去掉反向传播只看最终动作直接前提，会漏掉上游依赖；去掉第三项则只剩一般探针选择。

修订 Formal 能区分 PDEO 与静态域契约和直接提交消融，但不能消除 ETAS 残余义务、VERIMAP 计划生成验证函数以及经典最弱前置条件/集合覆盖的概念碰撞。因而最近工作边界仍是 Reviewer 和主研究者的最终裁决重点，不能从合成实验结果推导新颖性。

## 3. Core Experimental Evidence

### Source: `experiment_v001/plan_variation_result.md`

# PDEO 计划变化验证结果

## 有效执行

最终支撑记录为 `attempt-pdeo-plan-formal-002`。执行 Schema 7，退出码 0，指标、证据与输出契约均通过；预算上限为 30 秒、0 令牌、0 外部接口调用、0 图形处理器秒，实际墙钟 0.160 秒且没有外部接口调用。执行记录绑定当前实现文件清单和冻结规则输入。

## 主结果

- 16 个计划的编译义务精确匹配率：1.000；
- 16 个计划的编译探针集合精确匹配率：1.000；
- PDEO 逐计划平均探针成本：2.000；静态域契约：3.250；
- 48 个单义务故障中 PDEO 危险提交率：0；
- 60 个安全无关变异中 PDEO 提交召回率：1.000；静态域契约：0.5333；
- 16 个规格遗漏敏感性案例中危险提交率：1.000，表明不完整规格会直接破坏保证。

## 分域结果

- 预约：PDEO/静态成本 1.75/3.00，20 个故障中 PDEO 危险提交率 0，15 个安全无关变异召回率 1.000/0.5333；
- 访问控制：2.00/3.00，24 个故障中 PDEO 危险提交率 0，13 个安全无关变异召回率 1.000/0.6154；
- 库存：2.00/3.00，24 个故障中 PDEO 危险提交率 0，13 个安全无关变异召回率 1.000/0.6154；
- 文档发布：2.25/4.00，34 个故障中 PDEO 危险提交率 0，19 个安全无关变异召回率 1.000/0.4211。

## 解释

计划变体使 PDEO 的义务和探针选择实际变化，排除了“每域固定三探针契约”这一解释；其输出与人工逐计划最小上界一致，但没有超越人工规格。静态域契约在故障上同样安全，却因验证当前计划无关的合法字段而成本更高、召回更低。直接提交消融说明不做反向传播无法覆盖上游依赖。

这些结果只支持正确、完整的类型规格和确定性无噪读回条件下的窄机制主张。它们没有消除 ETAS、VERIMAP、ToolGate 或经典最弱前置条件与集合覆盖的最近工作碰撞，也没有提供外部团队制定的规格。

## 固定身份

- 执行记录散列：`77b5b5ebba1161f070526bab564d7f6b09614fb7dd1e61eede362aa1e2e339a5`；
- 指标散列：`c32ebf96005ff9df20ddeaf3a50e49d46a717eb92d5f77c4bc603fb7afe7d24c`；
- 详细输出散列：`0a199ce1a8435157e1bb0e4a18148d318b575abb1e7178077fa2a0bfb530664c`；
- 冻结规则散列：`b025c5ce3d1e5947164374be5f0c4d2397584ba74e330b9967bbf46fe72f081f`；
- 实验规格散列：`225c967ced092414cef78d0e8b0b5f48654ddfc66ce442c4ca47c5fdee97066a`。

### Source: `experiment_v001/attempts/attempt-pdeo-plan-formal-002/execution.json`

{
  "argv": [
    "D:\\Desktop\\crl\\env\\crl_agent_v3\\python.exe",
    "formal_plan_variation_experiment.py",
    "--rules-input",
    "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\specs\\pdeo-plan-heldout-rules-v2.json",
    "--metrics-output",
    "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-plan-formal-002\\metrics-output.json",
    "--details-output",
    "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-plan-formal-002\\plan-variation-details.json"
  ],
  "attempt_id": "attempt-pdeo-plan-formal-002",
  "budget_facts": {
    "actual": {
      "api_calls": 0,
      "duration_seconds": 0.15995549999934155,
      "gpu_time_seconds": 0,
      "tokens": 0
    },
    "comparison": {
      "status": "compared"
    },
    "machine_readable_limits": {
      "api_calls": 0,
      "duration_seconds": 30,
      "gpu_time_seconds": 0,
      "tokens": 0
    },
    "spec_budget_ceiling": "{\"duration_seconds\": 30, \"tokens\": 0, \"api_calls\": 0, \"gpu_time_seconds\": 0}",
    "warnings": []
  },
  "capture": {
    "stderr": {
      "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-plan-formal-002\\stderr.bin",
      "redaction_applied": false,
      "sha256": "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855",
      "size_bytes": 0
    },
    "stdout": {
      "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-plan-formal-002\\stdout.bin",
      "redaction_applied": false,
      "sha256": "b333004219c3d06ec7cd1ae0d300fb3eeaa2ed1ed48d50ac78e2fab7180e1fab",
      "size_bytes": 2254
    }
  },
  "command_error": null,
  "command_exit_code": 0,
  "cwd": "D:\\Desktop\\crl\\20260813_1054_run09\\implementation_v001",
  "duration_seconds": 0.15995549999934155,
  "environment_facts": {
    "cpu_count": 16,
    "declared_facts": {
      "dataset": "pdeo-plan-variation-178",
      "dataset_revision": "v2-heldout-plan-rules-domain-metrics",
      "model": "deterministic-typed-plan-controller",
      "provider": "local-python-3.11"
    },
    "dependencies": {
      "snapshot": {
        "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-plan-formal-002\\dependencies.txt",
        "sha256": "480ab3b94b0b3b95bb6ff16eb9c4e138b942a818e488d43f71f810c5fe2e143a",
        "size_bytes": 769
      },
      "source_path": "D:\\Desktop\\crl\\crl_agent_v3\\CRL_ENVIRONMENT_LOCK.txt",
      "source_type": "lock_file"
    },
    "executable": "D:\\Desktop\\crl\\env\\crl_agent_v3\\python.exe",
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
    "python": "3.11.15 | packaged by Anaconda, Inc. | (main, Jun 11 2026, 15:12:53) [MSC v.1942 64 bit (AMD64)]",
    "runner_and_modules": [
      {
        "path": "tools/run_local_experiment.py",
        "sha256": "2a6007ec765584afc80e56f90efb168d2383962a49ee5e8ab5a84ccaa3509190",
        "size_bytes": 32062
      },
      {
        "path": "crl_v3/experiment.py",
        "sha256": "d92817fcfd085ad100aa34f97a95e653956d22ea63ee8527f4b657d6b16a39da",
        "size_bytes": 37547
      },
      {
        "path": "crl_v3/falsification.py",
        "sha256": "5a852d0df4101c5b240363559d0cc05a2f64c725574d999b999e92deba97b9b8",
        "size_bytes": 40435
      },
      {
        "path": "crl_v3/workspace.py",
        "sha256": "74b7b3837e62404cbe68a1bc3f12ce4764a13e042b96131a1bd3bfa00ef57be9",
        "size_bytes": 27543
      },
      {
        "path": "crl_v3/decision.py",
        "sha256": "dff699c46b6e5bde36d589ff19e6f66ef3a2ea2ae0b7ceb42247030203f6d9c9",
        "size_bytes": 37790
      }
    ]
  },
  "evidence_contract_ok": true,
  "experiment_spec": {
    "snapshot": {
      "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-plan-formal-002\\spec.json",
      "sha256": "225c967ced092414cef78d0e8b0b5f48654ddfc66ce442c4ca47c5fdee97066a",
      "size_bytes": 4356
    },
    "source_path": "experiment_v001/specs/pdeo-plan-variation-suite-v2.json"
  },
  "finished_at_utc": "2026-08-13T03:50:09.497311Z",
  "implementation_files": [
    {
      "path": "implementation_v001/dqbp_core.py",
      "sha256": "4f9fc83512bfa8f0a660d90563793ddd7ed9462715b23a00c05ddf45d0b1039e",
      "size_bytes": 8752
    },
    {
      "path": "implementation_v001/formal_pdeo_experiment.py",
      "sha256": "7dea13632b6c6236fa678590f485491f09f04521713cd4a6b65d2b71e732f4fb",
      "size_bytes": 11368
    },
    {
      "path": "implementation_v001/formal_plan_variation_experiment.py",
      "sha256": "f0a08ef5c1a3e9289848cec282967c857831259dd187926390c037fd3ae87d04",
      "size_bytes": 23051
    },
    {
      "path": "implementation_v001/obligation_bench.py",
      "sha256": "5f66bb8d64012283bb19d21fa655736350e52bf2cecdfb7f0fa5af619360f164",
      "size_bytes": 6027
    },
    {
      "path": "implementation_v001/obligation_core.py",
      "sha256": "80833fd3de04257e1063e03b8e87847fae7951b256b1dbb903906d84e6066d75",
      "size_bytes": 5360
    },
    {
      "path": "implementation_v001/plan_variation_bench.py",
      "sha256": "7efb0081cb7aa6006612bde26f67abc8dac07ca90c7ab0325dfdb296ea894411",
      "size_bytes": 6834
    },
    {
      "path": "implementation_v001/run_experiment.py",
      "sha256": "2cd7c1c016a91a032866a39fa3f6671db61fb275fd9e529d8282aa6f6eb12261",
      "size_bytes": 8843
    },
    {
      "path": "implementation_v001/run_obligation_experiment.py",
      "sha256": "7584b680a715c4d13a0ecd7fd32988ca09915466e26395ffe7ff60676cebaeb0",
      "size_bytes": 9673
    },
    {
      "path": "implementation_v001/statefault_bench.py",
      "sha256": "74e6a975376ad01cb74e281a1f9f44737585435e9f3377afbb65e22903d9006a",
      "size_bytes": 13722
    },
    {
      "path": "implementation_v001/test_dqbp.py",
      "sha256": "d6cfb3d528285747243d9a1aa031da731c9fd2c1401e8108f744190667659a17",
      "size_bytes": 1287
    },
    {
      "path": "implementation_v001/test_formal_pdeo.py",
      "sha256": "554ed699ecc8fb4c40c7e0b947a524fab97e7201aeabe9f066ef52184cfc6b03",
      "size_bytes": 1013
    },
    {
      "path": "implementation_v001/test_obligation.py",
      "sha256": "a00eb364959899c22cd640dd2c41c3bc539866206cfc108b2e75167bb75dc6d5",
      "size_bytes": 2062
    },
    {
      "path": "implementation_v001/test_plan_variation.py",
      "sha256": "8102d0d6ecbc44c530b2a26c98b443d7debc59758297e640df8fe8ec129f24b2",
      "size_bytes": 2199
    }
  ],
  "inputs": [
    {
      "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\specs\\pdeo-plan-heldout-rules-v2.json",
      "sha256": "b025c5ce3d1e5947164374be5f0c4d2397584ba74e330b9967bbf46fe72f081f",
      "size_bytes": 3805
    }
  ],
  "metrics": {
    "contains_possible_credential": false,
    "credential_detection": [],
    "snapshot": {
      "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-plan-formal-002\\metrics.json",
      "sha256": "c32ebf96005ff9df20ddeaf3a50e49d46a717eb92d5f77c4bc603fb7afe7d24c",
      "size_bytes": 32355
    },
    "source_path": "experiment_v001/attempts/attempt-pdeo-plan-formal-002/metrics-output.json",
    "source_sha256": "c32ebf96005ff9df20ddeaf3a50e49d46a717eb92d5f77c4bc603fb7afe7d24c",
    "source_size_bytes": 32355,
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
        "sha256": "0a199ce1a8435157e1bb0e4a18148d318b575abb1e7178077fa2a0bfb530664c",
        "size_bytes": 697502
      },
      "before": {
        "exists": false
      },
      "path": "D:\\Desktop\\crl\\20260813_1054_run09\\experiment_v001\\attempts\\attempt-pdeo-plan-formal-002\\plan-variation-details.json"
    }
  ],
  "process_tree_cleanup_ok": null,
  "run_root": "D:\\Desktop\\crl\\20260813_1054_run09",
  "runner_exit_code": 0,
  "schema_version": 7,
  "seed": {
    "status": "not_set"
  },
  "started_at_utc": "2026-08-13T03:50:09.337000Z",
  "stdout_as_evidence": true,
  "termination_method": null,
  "timed_out": false,
  "timeout_seconds": 600.0,
  "version": "v001",
  "warnings": []
}

### Source: `experiment_v001/attempts/attempt-pdeo-plan-formal-002/metrics.json`

{
  "schema_version": 1,
  "experiment_id": "pdeo-plan-variation-suite-v2",
  "records": [
    {
      "name": "pdeo_compiled_obligation_exact_match_rate",
      "value": 1.0,
      "unit": "proportion",
      "split": "heldout_plan_variants",
      "aggregation": "plan_mean",
      "n": 16
    },
    {
      "name": "pdeo_compiled_probe_set_exact_match_rate",
      "value": 1.0,
      "unit": "proportion",
      "split": "heldout_plan_variants",
      "aggregation": "plan_mean",
      "n": 16
    },
    {
      "name": "pdeo_mean_plan_probe_cost",
      "value": 2.0,
      "unit": "cost_units",
      "split": "heldout_plan_variants",
      "aggregation": "plan_mean",
      "n": 16
    },
    {
      "name": "static_domain_contract_mean_plan_probe_cost",
      "value": 3.25,
      "unit": "cost_units",
      "split": "heldout_plan_variants",
      "aggregation": "plan_mean",
      "n": 16
    },
    {
      "name": "pdeo_spec_omission_unsafe_commit_rate",
      "value": 1.0,
      "unit": "proportion",
      "split": "specification_omission_sensitivity",
      "aggregation": "plan_mean",
      "n": 16
    },
    {
      "name": "no_verification_unsafe_commit_rate_canonical_safe",
      "value": 0.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "no_verification_gate_accuracy_canonical_safe",
      "value": 1.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "no_verification_average_probe_cost_canonical_safe",
      "value": 0.0,
      "unit": "cost_units",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "no_verification_valid_commit_recall_canonical_safe",
      "value": 1.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "fixed_target_readback_unsafe_commit_rate_canonical_safe",
      "value": 0.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "fixed_target_readback_gate_accuracy_canonical_safe",
      "value": 1.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "fixed_target_readback_average_probe_cost_canonical_safe",
      "value": 1.0,
      "unit": "cost_units",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "fixed_target_readback_valid_commit_recall_canonical_safe",
      "value": 1.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "static_domain_contract_unsafe_commit_rate_canonical_safe",
      "value": 0.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "static_domain_contract_gate_accuracy_canonical_safe",
      "value": 1.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "static_domain_contract_average_probe_cost_canonical_safe",
      "value": 3.25,
      "unit": "cost_units",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "static_domain_contract_valid_commit_recall_canonical_safe",
      "value": 1.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "pdeo_direct_commit_only_unsafe_commit_rate_canonical_safe",
      "value": 0.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "pdeo_direct_commit_only_gate_accuracy_canonical_safe",
      "value": 0.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "pdeo_direct_commit_only_average_probe_cost_canonical_safe",
      "value": 0.0,
      "unit": "cost_units",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "pdeo_direct_commit_only_valid_commit_recall_canonical_safe",
      "value": 0.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "pdeo_unsafe_commit_rate_canonical_safe",
      "value": 0.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "pdeo_gate_accuracy_canonical_safe",
      "value": 1.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "pdeo_average_probe_cost_canonical_safe",
      "value": 2.0,
      "unit": "cost_units",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "pdeo_valid_commit_recall_canonical_safe",
      "value": 1.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "human_per_plan_minimal_unsafe_commit_rate_canonical_safe",
      "value": 0.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "human_per_plan_minimal_gate_accuracy_canonical_safe",
      "value": 1.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "human_per_plan_minimal_average_probe_cost_canonical_safe",
      "value": 2.0,
      "unit": "cost_units",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "human_per_plan_minimal_valid_commit_recall_canonical_safe",
      "value": 1.0,
      "unit": "proportion",
      "split": "canonical_safe",
      "aggregation": "case_mean",
      "n": 16
    },
    {
      "name": "no_verification_unsafe_commit_rate_obligation_plus_nuisance_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "no_verification_gate_accuracy_obligation_plus_nuisance_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "no_verification_average_probe_cost_obligation_plus_nuisance_faults",
      "value": 0.0,
      "unit": "cost_units",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "fixed_target_readback_unsafe_commit_rate_obligation_plus_nuisance_faults",
      "value": 0.625,
      "unit": "proportion",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "fixed_target_readback_gate_accuracy_obligation_plus_nuisance_faults",
      "value": 0.375,
      "unit": "proportion",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "fixed_target_readback_average_probe_cost_obligation_plus_nuisance_faults",
      "value": 1.0,
      "unit": "cost_units",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "static_domain_contract_unsafe_commit_rate_obligation_plus_nuisance_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "static_domain_contract_gate_accuracy_obligation_plus_nuisance_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "static_domain_contract_average_probe_cost_obligation_plus_nuisance_faults",
      "value": 3.28125,
      "unit": "cost_units",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "pdeo_direct_commit_only_unsafe_commit_rate_obligation_plus_nuisance_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "pdeo_direct_commit_only_gate_accuracy_obligation_plus_nuisance_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "pdeo_direct_commit_only_average_probe_cost_obligation_plus_nuisance_faults",
      "value": 0.0,
      "unit": "cost_units",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "pdeo_unsafe_commit_rate_obligation_plus_nuisance_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "pdeo_gate_accuracy_obligation_plus_nuisance_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "pdeo_average_probe_cost_obligation_plus_nuisance_faults",
      "value": 2.375,
      "unit": "cost_units",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "human_per_plan_minimal_unsafe_commit_rate_obligation_plus_nuisance_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "human_per_plan_minimal_gate_accuracy_obligation_plus_nuisance_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "human_per_plan_minimal_average_probe_cost_obligation_plus_nuisance_faults",
      "value": 2.375,
      "unit": "cost_units",
      "split": "obligation_plus_nuisance_faults",
      "aggregation": "case_mean",
      "n": 32
    },
    {
      "name": "no_verification_unsafe_commit_rate_paired_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "no_verification_gate_accuracy_paired_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "no_verification_average_probe_cost_paired_obligation_faults",
      "value": 0.0,
      "unit": "cost_units",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "fixed_target_readback_unsafe_commit_rate_paired_obligation_faults",
      "value": 0.4090909090909091,
      "unit": "proportion",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "fixed_target_readback_gate_accuracy_paired_obligation_faults",
      "value": 0.5909090909090909,
      "unit": "proportion",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "fixed_target_readback_average_probe_cost_paired_obligation_faults",
      "value": 1.0,
      "unit": "cost_units",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "static_domain_contract_unsafe_commit_rate_paired_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "static_domain_contract_gate_accuracy_paired_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "static_domain_contract_average_probe_cost_paired_obligation_faults",
      "value": 3.3636363636363638,
      "unit": "cost_units",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "pdeo_direct_commit_only_unsafe_commit_rate_paired_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "pdeo_direct_commit_only_gate_accuracy_paired_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "pdeo_direct_commit_only_average_probe_cost_paired_obligation_faults",
      "value": 0.0,
      "unit": "cost_units",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "pdeo_unsafe_commit_rate_paired_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "pdeo_gate_accuracy_paired_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "pdeo_average_probe_cost_paired_obligation_faults",
      "value": 2.9545454545454546,
      "unit": "cost_units",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "human_per_plan_minimal_unsafe_commit_rate_paired_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "human_per_plan_minimal_gate_accuracy_paired_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "human_per_plan_minimal_average_probe_cost_paired_obligation_faults",
      "value": 2.9545454545454546,
      "unit": "cost_units",
      "split": "paired_obligation_faults",
      "aggregation": "case_mean",
      "n": 22
    },
    {
      "name": "no_verification_unsafe_commit_rate_safe_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "no_verification_gate_accuracy_safe_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "no_verification_average_probe_cost_safe_nuisance_variants",
      "value": 0.0,
      "unit": "cost_units",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "no_verification_valid_commit_recall_safe_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "fixed_target_readback_unsafe_commit_rate_safe_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "fixed_target_readback_gate_accuracy_safe_nuisance_variants",
      "value": 0.9,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "fixed_target_readback_average_probe_cost_safe_nuisance_variants",
      "value": 1.0,
      "unit": "cost_units",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "fixed_target_readback_valid_commit_recall_safe_nuisance_variants",
      "value": 0.9,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "static_domain_contract_unsafe_commit_rate_safe_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "static_domain_contract_gate_accuracy_safe_nuisance_variants",
      "value": 0.5333333333333333,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "static_domain_contract_average_probe_cost_safe_nuisance_variants",
      "value": 3.316666666666667,
      "unit": "cost_units",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "static_domain_contract_valid_commit_recall_safe_nuisance_variants",
      "value": 0.5333333333333333,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "pdeo_direct_commit_only_unsafe_commit_rate_safe_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "pdeo_direct_commit_only_gate_accuracy_safe_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "pdeo_direct_commit_only_average_probe_cost_safe_nuisance_variants",
      "value": 0.0,
      "unit": "cost_units",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "pdeo_direct_commit_only_valid_commit_recall_safe_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "pdeo_unsafe_commit_rate_safe_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "pdeo_gate_accuracy_safe_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "pdeo_average_probe_cost_safe_nuisance_variants",
      "value": 1.75,
      "unit": "cost_units",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "pdeo_valid_commit_recall_safe_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "human_per_plan_minimal_unsafe_commit_rate_safe_nuisance_variants",
      "value": 0.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "human_per_plan_minimal_gate_accuracy_safe_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "human_per_plan_minimal_average_probe_cost_safe_nuisance_variants",
      "value": 1.75,
      "unit": "cost_units",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "human_per_plan_minimal_valid_commit_recall_safe_nuisance_variants",
      "value": 1.0,
      "unit": "proportion",
      "split": "safe_nuisance_variants",
      "aggregation": "case_mean",
      "n": 60
    },
    {
      "name": "no_verification_unsafe_commit_rate_single_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "no_verification_gate_accuracy_single_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "no_verification_average_probe_cost_single_obligation_faults",
      "value": 0.0,
      "unit": "cost_units",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "fixed_target_readback_unsafe_commit_rate_single_obligation_faults",
      "value": 0.625,
      "unit": "proportion",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "fixed_target_readback_gate_accuracy_single_obligation_faults",
      "value": 0.375,
      "unit": "proportion",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "fixed_target_readback_average_probe_cost_single_obligation_faults",
      "value": 1.0,
      "unit": "cost_units",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "static_domain_contract_unsafe_commit_rate_single_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "static_domain_contract_gate_accuracy_single_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "static_domain_contract_average_probe_cost_single_obligation_faults",
      "value": 3.3541666666666665,
      "unit": "cost_units",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "pdeo_direct_commit_only_unsafe_commit_rate_single_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "pdeo_direct_commit_only_gate_accuracy_single_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "pdeo_direct_commit_only_average_probe_cost_single_obligation_faults",
      "value": 0.0,
      "unit": "cost_units",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "pdeo_unsafe_commit_rate_single_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "pdeo_gate_accuracy_single_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "pdeo_average_probe_cost_single_obligation_faults",
      "value": 2.375,
      "unit": "cost_units",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "human_per_plan_minimal_unsafe_commit_rate_single_obligation_faults",
      "value": 0.0,
      "unit": "proportion",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "human_per_plan_minimal_gate_accuracy_single_obligation_faults",
      "value": 1.0,
      "unit": "proportion",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "human_per_plan_minimal_average_probe_cost_single_obligation_faults",
      "value": 2.375,
      "unit": "cost_units",
      "split": "single_obligation_faults",
      "aggregation": "case_mean",
      "n": 48
    },
    {
      "name": "pdeo_mean_plan_probe_cost_access_control",
      "value": 2.0,
      "unit": "cost_units",
      "split": "domain:access_control",
      "aggregation": "plan_mean",
      "n": 4
    },
    {
      "name": "static_domain_contract_mean_plan_probe_cost_access_control",
      "value": 3.0,
      "unit": "cost_units",
      "split": "domain:access_control",
      "aggregation": "plan_mean",
      "n": 4
    },
    {
      "name": "static_domain_contract_unsafe_commit_rate_all_faults_access_control",
      "value": 0.0,
      "unit": "proportion",
      "split": "domain:access_control",
      "aggregation": "fault_case_mean",
      "n": 24
    },
    {
      "name": "static_domain_contract_valid_commit_recall_safe_nuisance_access_control",
      "value": 0.6153846153846154,
      "unit": "proportion",
      "split": "domain:access_control",
      "aggregation": "safe_case_mean",
      "n": 13
    },
    {
      "name": "pdeo_unsafe_commit_rate_all_faults_access_control",
      "value": 0.0,
      "unit": "proportion",
      "split": "domain:access_control",
      "aggregation": "fault_case_mean",
      "n": 24
    },
    {
      "name": "pdeo_valid_commit_recall_safe_nuisance_access_control",
      "value": 1.0,
      "unit": "proportion",
      "split": "domain:access_control",
      "aggregation": "safe_case_mean",
      "n": 13
    },
    {
      "name": "human_per_plan_minimal_unsafe_commit_rate_all_faults_access_control",
      "value": 0.0,
      "unit": "proportion",
      "split": "domain:access_control",
      "aggregation": "fault_case_mean",
      "n": 24
    },
    {
      "name": "human_per_plan_minimal_valid_commit_recall_safe_nuisance_access_control",
      "value": 1.0,
      "unit": "proportion",
      "split": "domain:access_control",
      "aggregation": "safe_case_mean",
      "n": 13
    },
    {
      "name": "pdeo_mean_plan_probe_cost_document_release",
      "value": 2.25,
      "unit": "cost_units",
      "split": "domain:document_release",
      "aggregation": "plan_mean",
      "n": 4
    },
    {
      "name": "static_domain_contract_mean_plan_probe_cost_document_release",
      "value": 4.0,
      "unit": "cost_units",
      "split": "domain:document_release",
      "aggregation": "plan_mean",
      "n": 4
    },
    {
      "name": "static_domain_contract_unsafe_commit_rate_all_faults_document_release",
      "value": 0.0,
      "unit": "proportion",
      "split": "domain:document_release",
      "aggregation": "fault_case_mean",
      "n": 34
    },
    {
      "name": "static_domain_contract_valid_commit_recall_safe_nuisance_document_release",
      "value": 0.42105263157894735,
      "unit": "proportion",
      "split": "domain:document_release",
      "aggregation": "safe_case_mean",
      "n": 19
    },
    {
      "name": "pdeo_unsafe_commit_rate_all_faults_document_release",
      "value": 0.0,
      "unit": "proportion",
      "split": "domain:document_release",
      "aggregation": "fault_case_mean",
      "n": 34
    },
    {
      "name": "pdeo_valid_commit_recall_safe_nuisance_document_release",
      "value": 1.0,
      "unit": "proportion",
      "split": "domain:document_release",
      "aggregation": "safe_case_mean",
      "n": 19
    },
    {
      "name": "human_per_plan_minimal_unsafe_commit_rate_all_faults_document_release",
      "value": 0.0,
      "unit": "proportion",
      "split": "domain:document_release",
      "aggregation": "fault_case_mean",
      "n": 34
    },
    {
      "name": "human_per_plan_minimal_valid_commit_recall_safe_nuisance_document_release",
      "value": 1.0,
      "unit": "proportion",
      "split": "domain:document_release",
      "aggregation": "safe_case_mean",
      "n": 19
    },
    {
      "name": "pdeo_mean_plan_probe_cost_inventory",
      "value": 2.0,
      "unit": "cost_units",
      "split": "domain:inventory",
      "aggregation": "plan_mean",
      "n": 4
    },
    {
      "name": "static_domain_contract_mean_plan_probe_cost_inventory",
      "value": 3.0,
      "unit": "cost_units",
      "split": "domain:inventory",
      "aggregation": "plan_mean",
      "n": 4
    },
    {
      "name": "static_domain_contract_unsafe_commit_rate_all_faults_inventory",
      "value": 0.0,
      "unit": "proportion",
      "split": "domain:inventory",
      "aggregation": "fault_case_mean",
      "n": 24
    },
    {
      "name": "static_domain_contract_valid_commit_recall_safe_nuisance_inventory",
      "value": 0.6153846153846154,
      "unit": "proportion",
      "split": "domain:inventory",
      "aggregation": "safe_case_mean",
      "n": 13
    },
    {
      "name": "pdeo_unsafe_commit_rate_all_faults_inventory",
      "value": 0.0,
      "unit": "proportion",
      "split": "domain:inventory",
      "aggregation": "fault_case_mean",
      "n": 24
    },
    {
      "name": "pdeo_valid_commit_recall_safe_nuisance_inventory",
      "value": 1.0,
      "unit": "proportion",
      "split": "domain:inventory",
      "aggregation": "safe_case_mean",
      "n": 13
    },
    {
      "name": "human_per_plan_minimal_unsafe_commit_rate_all_faults_inventory",
      "value": 0.0,
      "unit": "proportion",
      "split": "domain:inventory",
      "aggregation": "fault_case_mean",
      "n": 24
    },
    {
      "name": "human_per_plan_minimal_valid_commit_recall_safe_nuisance_inventory",
      "value": 1.0,
      "unit": "proportion",
      "split": "domain:inventory",
      "aggregation": "safe_case_mean",
      "n": 13
    },
    {
      "name": "pdeo_mean_plan_probe_cost_reservation",
      "value": 1.75,
      "unit": "cost_units",
      "split": "domain:reservation",
      "aggregation": "plan_mean",
      "n": 4
    },
    {
      "name": "static_domain_contract_mean_plan_probe_cost_reservation",
      "value": 3.0,
      "unit": "cost_units",
      "split": "domain:reservation",
      "aggregation": "plan_mean",
      "n": 4
    },
    {
      "name": "static_domain_contract_unsafe_commit_rate_all_faults_reservation",
      "value": 0.0,
      "unit": "proportion",
      "split": "domain:reservation",
      "aggregation": "fault_case_mean",
      "n": 20
    },
    {
      "name": "static_domain_contract_valid_commit_recall_safe_nuisance_reservation",
      "value": 0.5333333333333333,
      "unit": "proportion",
      "split": "domain:reservation",
      "aggregation": "safe_case_mean",
      "n": 15
    },
    {
      "name": "pdeo_unsafe_commit_rate_all_faults_reservation",
      "value": 0.0,
      "unit": "proportion",
      "split": "domain:reservation",
      "aggregation": "fault_case_mean",
      "n": 20
    },
    {
      "name": "pdeo_valid_commit_recall_safe_nuisance_reservation",
      "value": 1.0,
      "unit": "proportion",
      "split": "domain:reservation",
      "aggregation": "safe_case_mean",
      "n": 15
    },
    {
      "name": "human_per_plan_minimal_unsafe_commit_rate_all_faults_reservation",
      "value": 0.0,
      "unit": "proportion",
      "split": "domain:reservation",
      "aggregation": "fault_case_mean",
      "n": 20
    },
    {
      "name": "human_per_plan_minimal_valid_commit_recall_safe_nuisance_reservation",
      "value": 1.0,
      "unit": "proportion",
      "split": "domain:reservation",
      "aggregation": "safe_case_mean",
      "n": 15
    }
  ],
  "resource_usage": {
    "tokens": 0,
    "api_calls": 0,
    "wall_time_seconds": 0.029532699999435863,
    "gpu_time_seconds": 0,
    "estimated_cost": 0
  },
  "errors": [],
  "warnings": [
    "Heldout rules are byte-frozen in a separate declared input, but were authored within the same Run rather than by an external team.",
    "All domains remain synthetic and all read probes are deterministic and noise-free.",
    "Specification omission sensitivity is an expected failure test outside the correct-specification claim scope."
  ]
}

## 4. Baseline & Budget Facts

### Source: `experiment_v001/plan_variation_plan.md`

# PDEO 计划变化验证计划

## 目的

回应首次固定三审的机制识别异议：原 Formal 只改变环境状态，PDEO 在每个域内始终选择固定的三探针集合，无法证明验证集合来自当前计划。修订实验要求同一域内的受保护承诺前提发生变化，并检验 PDEO 是否逐计划重编译义务与探针。

## 冻结设计

- 四个合成域：预约、访问控制、库存、文档发布；
- 每域四个计划变体，共 16 个；
- 178 个计划—状态案例：16 个规范安全案例、48 个单义务故障、60 个安全无关字段变异、22 个双义务故障、32 个义务加无关字段故障；
- 另设 16 个规格遗漏敏感性案例，每个计划故意遗漏一个真实安全原子并只破坏该原子；
- 真实安全原子、规范状态和值域保存在独立冻结输入 `pdeo-plan-heldout-rules-v2.json`，候选计划与编译器不读取该文件。

## 公平比较

- 无验证；
- 固定目标读回；
- 静态域契约：验证该域所有可能计划义务的并集；
- 仅直接承诺检查消融：不做反向传播；
- 人工逐计划最小义务上界；
- PDEO。

所有方法共享相同类型计划、探针目录、探针成本、状态和返回；冻结规则只供评价器与人工上界使用。

## 预注册反证条件

以下任一项成立即反证计划条件化主张：16 个计划的义务或探针集合精确匹配率低于 1；单义务故障危险提交率高于 0；安全无关变异提交召回率低于 1；或 PDEO 的逐计划平均探针成本不低于静态域契约。规格遗漏应产生危险提交；若没有，则必须审计是否偷偷进行了全量读回。

## 保证边界

独立规则文件仍由同一主研究者在同一 Run 内设计；人工上界与 PDEO 预期相同；全部域为合成、读回确定且无噪。因此该实验识别计算机制，不证明外部规格正确、真实生态有效或方法新颖。

### Source: `experiment_v001/specs/pdeo-plan-variation-suite-v2.json`

{
  "baseline_specs": [
    "无验证",
    "固定目标读回",
    "静态每域完整承诺契约",
    "不做反向传播的直接承诺检查消融",
    "人工逐计划最小义务上界"
  ],
  "budget_ceiling": "{\"duration_seconds\": 30, \"tokens\": 0, \"api_calls\": 0, \"gpu_time_seconds\": 0}",
  "claim_ids": [
    "pdeo-plan-conditioned-compilation"
  ],
  "confounders": [
    "独立规则文件仍由同一主研究者在同一 Run 内设计。",
    "人工逐计划上界与 PDEO 应相同，因此实验不证明超越人工契约。",
    "域与状态仍为合成，读回确定且无噪。",
    "静态每域契约验证所有潜在承诺原子，可能比单一当前承诺更保守。"
  ],
  "dataset": "四个合成域、16 个计划变体、178 个系统计划—状态案例和 16 个规格遗漏敏感性案例",
  "declared_inputs": [
    "experiment_v001/specs/pdeo-plan-heldout-rules-v2.json"
  ],
  "declared_outputs": [],
  "expected_signatures": [
    "16 个计划的义务和探针集合精确匹配率均为 1。",
    "单义务故障危险提交率为 0，安全无关变异召回率为 1。",
    "PDEO 按计划平均探针成本低于静态每域契约。",
    "故意遗漏一个真实规格义务时，PDEO 会出现危险提交，确认保证依赖规格完整性。"
  ],
  "experiment_id": "pdeo-plan-variation-suite-v2",
  "falsification_rule": "任一主精确率或召回率低于 1、危险提交率高于 0、或 PDEO 平均成本不低于静态每域契约，即反证计划条件化主张。规格遗漏测试应暴露失败；若不失败，需审计是否存在隐藏全量读取。",
  "hypothesis_id": "h4-pdeo",
  "independent_ground_truth": {
    "description": "16 个计划的安全原子、规范状态和值域保存在独立 UTF-8 JSON 输入 pdeo-plan-heldout-rules-v2.json 中并由 Formal runner 冻结；实验程序从该文件生成标签和人工逐计划上界，候选实现不导入该文件。",
    "external_card_ids": [],
    "external_evidence_ids": [],
    "external_literature_refs": [
      "ToolGate: Findings of ACL 2026",
      "ETAS: arXiv:2607.17780",
      "Verification-Aware Planning for Multi-Agent Systems: arXiv:2510.17109"
    ],
    "run_local_fact_refs": [
      "experiment_v001/specs/pdeo-plan-heldout-rules-v2.json",
      "implementation_v001/formal_plan_variation_experiment.py"
    ]
  },
  "model": "无语言模型；确定性类型计划控制器",
  "parity_dimensions": {
    "budget": {
      "notes": "按相同探针单位成本计费；方法可选择不同数量，报告实际成本与安全/召回帕累托。",
      "status": "matched"
    },
    "information_access": {
      "notes": "所有可部署方法共享候选类型计划、状态和探针返回；冻结规则仅供评价器和人工上界使用。",
      "status": "matched"
    },
    "model_provider_revision": {
      "notes": "全部方法为同一 Python 运行时中的确定性代码，不调用语言模型。",
      "status": "matched"
    },
    "sampling_protocol": {
      "notes": "每种方法运行相同的 178 个计划—状态案例；规格遗漏单独作为边界敏感性测试。",
      "status": "matched"
    },
    "tool_capability": {
      "notes": "所有方法共享同一域内探针目录和成本；静态契约按固定域原子求最小覆盖。",
      "status": "matched"
    }
  },
  "primary_metric": "pdeo_compiled_obligation_exact_match_rate",
  "provider": "本地 Python 3.11",
  "purpose": "independent_claim_validation",
  "research_question": "PDEO 的义务与探针是否真正随下游计划变化，并在静态每域契约保持安全的前提下获得更低成本和更高的计划条件化接受率？",
  "revision": "pdeo-plan-variation-r2",
  "run_id": "20260813_1054_run09",
  "sampling_unit": "一个类型计划变体与一个完整环境状态的组合",
  "schema_version": 1,
  "secondary_metrics": [
    "pdeo_compiled_probe_set_exact_match_rate",
    "pdeo_unsafe_commit_rate_single_obligation_faults",
    "pdeo_valid_commit_recall_safe_nuisance_variants",
    "pdeo_mean_plan_probe_cost",
    "static_domain_contract_mean_plan_probe_cost",
    "static_domain_contract_valid_commit_recall_safe_nuisance_variants",
    "pdeo_spec_omission_unsafe_commit_rate"
  ],
  "seeds": [],
  "version": "v001"
}

### Source: `experiment_v001/specs/pdeo-plan-heldout-rules-v2.json`

{
  "schema_version": 1,
  "ruleset_id": "pdeo-plan-heldout-rules-v2",
  "domains": {
    "reservation": {
      "canonical_state": {
        "target_status": "CONFIRMED",
        "payment_state": "CAPTURED",
        "other_booking": "UNCHANGED",
        "audit_event": "TARGET_CONFIRMED"
      },
      "field_values": {
        "target_status": ["CONFIRMED", "PENDING"],
        "payment_state": ["CAPTURED", "PENDING", "DOUBLE_CAPTURED"],
        "other_booking": ["UNCHANGED", "CONFIRMED"],
        "audit_event": ["TARGET_CONFIRMED", "NO_MUTATION", "OTHER_CONFIRMED"]
      },
      "variants": {
        "full_confirmation": [["target_status", "CONFIRMED"], ["payment_state", "CAPTURED"], ["other_booking", "UNCHANGED"]],
        "status_notice": [["target_status", "CONFIRMED"]],
        "payment_receipt": [["payment_state", "CAPTURED"]],
        "exclusive_itinerary": [["target_status", "CONFIRMED"], ["other_booking", "UNCHANGED"]]
      }
    },
    "access_control": {
      "canonical_state": {
        "target_role": "EDITOR",
        "scope_state": "PROJECT_ONLY",
        "other_principal": "UNCHANGED",
        "audit_event": "TARGET_GRANTED"
      },
      "field_values": {
        "target_role": ["EDITOR", "VIEWER"],
        "scope_state": ["PROJECT_ONLY", "ORGANIZATION_WIDE", "DUPLICATE_BINDING"],
        "other_principal": ["UNCHANGED", "EDITOR"],
        "audit_event": ["TARGET_GRANTED", "NO_MUTATION", "OTHER_GRANTED"]
      },
      "variants": {
        "editor_operation": [["target_role", "EDITOR"], ["scope_state", "PROJECT_ONLY"], ["other_principal", "UNCHANGED"]],
        "role_notice": [["target_role", "EDITOR"]],
        "scoped_editor": [["target_role", "EDITOR"], ["scope_state", "PROJECT_ONLY"]],
        "isolation_attestation": [["scope_state", "PROJECT_ONLY"], ["other_principal", "UNCHANGED"]]
      }
    },
    "inventory": {
      "canonical_state": {
        "target_quantity": "PLUS_5",
        "warehouse_balance": "BALANCED",
        "other_sku": "UNCHANGED",
        "audit_event": "TARGET_INCREMENTED"
      },
      "field_values": {
        "target_quantity": ["PLUS_5", "UNCHANGED", "PLUS_10"],
        "warehouse_balance": ["BALANCED", "UNBALANCED"],
        "other_sku": ["UNCHANGED", "PLUS_5"],
        "audit_event": ["TARGET_INCREMENTED", "NO_MUTATION", "OTHER_INCREMENTED"]
      },
      "variants": {
        "publish_restock": [["target_quantity", "PLUS_5"], ["warehouse_balance", "BALANCED"], ["other_sku", "UNCHANGED"]],
        "quantity_notice": [["target_quantity", "PLUS_5"]],
        "balanced_restock": [["target_quantity", "PLUS_5"], ["warehouse_balance", "BALANCED"]],
        "isolation_attestation": [["warehouse_balance", "BALANCED"], ["other_sku", "UNCHANGED"]]
      }
    },
    "document_release": {
      "canonical_state": {
        "document_signature": "SIGNED",
        "audience_state": "PUBLIC",
        "sibling_document": "UNCHANGED",
        "checksum_state": "MATCH",
        "audit_event": "DOCUMENT_READY"
      },
      "field_values": {
        "document_signature": ["SIGNED", "UNSIGNED", "REVOKED"],
        "audience_state": ["PUBLIC", "PRIVATE", "WRONG_GROUP"],
        "sibling_document": ["UNCHANGED", "PUBLISHED"],
        "checksum_state": ["MATCH", "MISMATCH", "MISSING"],
        "audit_event": ["DOCUMENT_READY", "NO_MUTATION", "WRONG_DOCUMENT"]
      },
      "variants": {
        "public_release": [["document_signature", "SIGNED"], ["audience_state", "PUBLIC"], ["sibling_document", "UNCHANGED"], ["checksum_state", "MATCH"]],
        "internal_archive": [["document_signature", "SIGNED"], ["checksum_state", "MATCH"]],
        "public_preview": [["audience_state", "PUBLIC"], ["checksum_state", "MATCH"]],
        "signature_notice": [["document_signature", "SIGNED"]]
      }
    }
  }
}

## 5. Ablation / Robustness / Falsification Evidence

### Source: `review_response_v001.md`

# 首次固定三审回应

## 三审事实

`review_v001/evaluations/eval-0001` 是有效的固定三审：科学性、实证性和对抗性三个角色均未联网、未调用工具、未读取 packet 外信息，且没有无效理由。三者都把关键风险评为 `potentially_fatal`。聚合分数 61.1250 只是诊断信息，不构成交付门槛。

## 主研究者接受的异议

1. 原实验只改变状态而不改变计划，PDEO 在每个域内固定选择三探针，不能识别计划条件化机制；
2. 缺少静态每域完整承诺契约这一强基线；
3. 类型规格、评价规则和探针覆盖由同一研究者给出，遗漏可能致命；
4. packet 给出源码散列与路径，但没有向 Reviewer 展示关键源码正文；
5. 最弱前置条件、集合覆盖、ETAS 残余义务和 VERIMAP 验证函数仍构成严重最近工作碰撞。

## 有界修订

- 冻结四域 16 个计划变体，使同域内承诺前提和最小探针随计划变化；
- 加入静态域契约、直接提交消融与人工逐计划最小上界；
- 把真实安全规则保存为独立声明输入，候选实现不读取；
- 加入 16 个规格遗漏敏感性案例，结果 16/16 危险提交，明确该前提是致命边界；
- 在第二次固定 packet 中直接纳入核心实现、基准构造和 Formal 评价源码正文。

## 未解决且不粉饰的风险

修订只回答机制是否随计划变化，并没有取得外部团队规格、真实应用程序接口数据或最近工作作者级比较。人工逐计划上界与 PDEO 完全相同，说明当前优势是自动执行给定形式知识，而非产生新知识。方法是否足以构成 CCF-B 级独立贡献，仍须由第二次固定三审和主研究者结合最近工作边界裁决。

### Source: `review_v001/evaluations/eval-0001/aggregate.json`

{
  "canonical_evaluation_id": "eval-0001",
  "evaluation_id": "eval-0001",
  "evaluator_version": "CRL-EVAL-1.0",
  "implementation_key": "0424092c3d015458de5a2033cb9db7ac8bceeede66122a7ccba6bbf5b1062cff",
  "invalid_reasons": [],
  "measurement_key": "f8e1a5550893f05b076a3190b4559ef120da816ff6b9e2fc588900e66bf98d73",
  "measurement_kind": "CANONICAL_IMPLEMENTATION_SCORE",
  "overall_score_numerator": 611250,
  "overall_score_percent": "61.1250",
  "packet_key": "e156c03321e8cb3574486fec8703b00e026c48d4f6e40c57a505903121143518",
  "role_results": {
    "ADV": {
      "output": {
        "confidence": "high",
        "critical_risk": "potentially_fatal",
        "diagnostics": {
          "best_stress_test": "由独立团队预先冻结外部安全规则和未见长计划域，包含交互效果与多字段复合故障；在候选实现冻结后生成类型规格和探针目录，逐项比较 PDEO 编译义务与穷举真值，并追加单个遗漏或错误 cover 的敏感性测试。",
          "boundary_warning": "零危险提交与成本 3 只能外推到当前三个同构、离散、确定、无噪、短计划合成域；尤其不能外推为真实工具生态中的开放世界安全保证或端到端代理可靠性。",
          "hidden_assumption": "受保护承诺的安全条件能够被人工类型规格完整、正确地分解为已知原子谓词，并且每个 cover 声明对应一个真实、即时、无噪且无权限障碍的环境读回。",
          "most_fatal_failure_mode": "类型计划或工具效果遗漏一个真实安全谓词时，PDEO 不会生成或读取该义务，仍可能在内部闭集判断通过后危险提交；同源评价规则可能同时遗漏它，使实验无法暴露该失败。",
          "reproduction_breakpoint": "复现者最可能在重建并运行 formal_pdeo_experiment.py 时中断：packet 只有源码哈希和机器本地路径，没有源码内容、完整状态输入、案例生成逻辑及探针成本定义。"
        },
        "evaluator_version": "CRL-EVAL-1.0",
        "free_review": "packet 对一次确定性运行的身份和输出保存较好，但方法核仍未经过真正独立的对抗复现。评价器、编译器、案例生成和人工类型知识同处一个程序与词表；“未见故障”只是封闭分支基线未建模，并非超出规格谓词或探针覆盖的未知状态。PDEO 与人工最小义务在全部域完全相同，成本恒为 3，说明当前实验主要确认手写安全知识被正确搬运，而未证明计划派生在复杂计划中仍可靠。最危险的反例不是再换一个词表值，而是独立安全规则包含一个类型计划遗漏的前提：PDEO 将无从生成证据并可能危险提交。源码、真实状态及成本定义未随 packet 内容提供，也使独立团队无法判断零错误是否含实现捷径。当前证据支持窄构造正确性，不足以支持开放世界方法核。",
        "model_identity": "gpt-5.6-sol",
        "reasoning_effort": "xhigh",
        "reasons": {
          "adversarial_survivability": "48 个单义务故障、36 个义务—无关字段配对故障和 63 个安全变异提供了真实的系统性压力，PDEO 在这些冻结案例上达到零危险提交和完整召回。但攻击均围绕已知原子谓词及准确覆盖探针构造，没有独立域、长计划、交互效果、未知谓词、多义务耦合或规格扰动。当前结果更像验证“检查全部正确义务即可安全”的构造性质，尚未排除一个遗漏义务就直接危险提交的核心脆弱性。",
          "boundary_generalization": "证据仅覆盖三个结构同源的合成域、固定小探针目录、离散无噪状态和确定性控制器，且各域 PDEO 都固定选择成本为 3 的三个探针。没有真实 API、自然语言计划、长 horizon、并发、陈旧读、权限失败、噪声或大规模集合覆盖证据。作者虽明确收窄主张，但现有结果几乎不支持越出该窄边界的泛化。",
          "confound_leakage_control": "标签函数据称不调用 PDEO 编译器，且零模型、零接口调用降低了模型记忆和外部缓存风险。然而评价规则、编译器、案例生成与基线位于同一实验程序，并共享人工类型规格和预先存在的状态词表；没有独立作者、盲测或外部真实规则。所谓开放世界故障仍是该词表内系统枚举，可能使候选义务与评价谓词在设计时同源；源码级捷径审计为 packet insufficient。完整工具契约还评价更强目标且预算不同，其低召回不能作为同目标优势。",
          "evidence_auditability": "关键汇总值、逐例方法决策、探针列表、成本字段以及 artifact 哈希均被提供，主要指标原则上可从 rows 重新聚合。可是安全标签所依据的完整真实状态、SAFETY_RULES、编译器源码和探针权重定义没有内容级展示，因此无法独立核验 expected、cover 与 probe_cost 是否正确。stdout 也只有哈希，Evidence Inventory 的 comparison_count 为 0，故哈希身份链强于语义审计链。",
          "reproducibility_traceability": "packet 提供了执行命令、Python 与依赖版本、实现文件及输出哈希、退出码和逐例结果，运行身份追踪较完整。但实现源码、完整案例状态、探针成本目录和案例生成输入未实际给出，只有本地路径与哈希，独立团队无法仅凭 packet 重建 171 个案例并执行同一程序。Git 状态不可用、seed 未设置且预算上限不可机器比较，也削弱了复现闭环。"
        },
        "review_protocol": "CRL-IR-1.0",
        "reviewer_role": "ADV",
        "scores": {
          "adversarial_survivability": 2,
          "boundary_generalization": 1,
          "confound_leakage_control": 2,
          "evidence_auditability": 2,
          "reproducibility_traceability": 2
        }
      },
      "report_sha256": "5f37dd042c90fd4f043f475fb3075f812e5ae3146d6d3861174a3474e57f4441",
      "role_score_basis_points": 4625
    },
    "EMP": {
      "output": {
        "confidence": "high",
        "critical_risk": "potentially_fatal",
        "diagnostics": {
          "baseline_confound": "缺少静态的每域三探针最小契约基线；同时 PDEO 使用成本3的承诺对齐读回，而DQBP和信息增益平均仅约1.67且受封闭分支模型限制，当前优势可能由更多且目标对齐的信息访问解释。",
          "biggest_empirical_threat": "计划和下游承诺几乎未变化，PDEO 在每个域始终选择固定三个探针；因此实验无法排除它只是静态域内最小契约的等价实现，而非真正由当前计划动态派生证据。",
          "killer_experiment": "冻结实现后，在每个域生成多种具有不同下游承诺、动作顺序和确定效果的类型计划，独立给出安全标签并注入未见义务故障；以相同探针成本将 PDEO 与静态每工具/每域最小契约、开放集检测和义务增强基线比较。若 PDEO 的探针集合不随计划正确变化或不优于静态三探针基线，计划派生机制主张即被推翻。",
          "missing_validation": "最需要补充由独立人员设计的留出计划与非同构域验证，明确检验同一工具在不同下游承诺下是否产生不同且最小的证据义务。",
          "strongest_empirical_evidence": "在独立声明的 SAFETY_RULES 标签下，PDEO 同时实现48/48义务故障不提交、63/63安全无关变异提交，并以成本3达到与人工最小义务相同的门控结果。"
        },
        "evaluator_version": "CRL-EVAL-1.0",
        "free_review": "该实验是一项记录完整的确定性合成一致性测试，能够可信证明冻结套件内的窄结果：给定正确规格和无噪读回，三个承诺相关探针足以安全门控，并比完整读回便宜。核心不足是实验只广泛变异状态，没有广泛变异计划；因此最重要的“计划派生”属性与静态域内最小契约不可辨识。评价规则虽不调用编译器，却与候选共享人工规格并处于同一程序，独立性仍有限。DQBP和信息增益的失败主要暴露封闭分支模型边界，不能代表强开放集验证方法。若不加入计划变化和静态三探针控制，当前证据更像实现符合预设规则，而非独立验证方法机制。",
        "model_identity": "gpt-5.6-sol",
        "reasoning_effort": "xhigh",
        "reasons": {
          "baseline_fairness": "各方法共享案例、类型计划、工具规格、探针返回和成本，DQBP 与信息增益也共享预算 3。问题在于 PDEO 实际读取成本为 3，而两个主要失败基线平均只读约 1.67，且其封闭分支模型按构造不能表示目标变异；未加入开放集方法或允许其利用计划义务的版本。完整工具契约还优化更强的工具履约目标，最关键的静态“每域固定三个承诺相关探针”基线则缺失。",
          "experimental_validity": "171 个确定性案例直接测量了危险提交、无关变异召回和探针成本，标签函数也不调用 PDEO 编译器。可是实验主要改变状态值，未系统改变类型计划、动作序列或下游承诺；每个域中 PDEO 始终读取同一组三个探针。因此结果能验证固定门控集合在该套件上正确，却不足以独立识别“计划派生”机制相对于静态域内最小契约的作用。",
          "measurement_reliability": "指标定义、分割、聚合、样本数和逐案例记录均明确，正式运行与最终实现清单匹配且无执行错误。确定性穷举不依赖随机种子，001 与 002 数值一致也提供了一定复现迹象。局限是评价规则与候选仍位于同一实验程序并共享人工类型规格，缺少外部标注者或独立评价实现，且未报告按域分解以揭示结构相关性。",
          "result_strength": "PDEO 在48个义务故障上为0危险提交、在63个安全变异上召回率为1，成本3也明确低于完整契约5和全量读回6，数值信号很强。但它与人工最小义务完全持平，且案例来自三个共享结构的合成域，许多案例是同一少数计划模板的系统变异而非独立统计单元。结果足以支持该冻结套件上的窄一致性结论，尚不足以支持一般经验优势或计划派生机制的强结论。",
          "robustness_falsification": "套件包含已知分支、48 个单义务替换、63 个无关变异和36 个义务—无关配对，具备有价值的正负控制。它还保留了 DQBP 的负结果，没有隐藏先前失败。可是没有计划条件变化、编译组件消融、非同构域、多个义务同时失效、探针覆盖扰动或读回失效实验，因而主要机制和边界仍未受到足够强的反证。"
        },
        "review_protocol": "CRL-IR-1.0",
        "reviewer_role": "EMP",
        "scores": {
          "baseline_fairness": 2,
          "experimental_validity": 2,
          "measurement_reliability": 3,
          "result_strength": 2,
          "robustness_falsification": 2
        }
      },
      "report_sha256": "209f6ba4fba734961b1dee82feab82a2f16c55e9cb8f24c0ed7cfd8b85a12d90",
      "role_score_basis_points": 5500
    },
    "SCI": {
      "output": {
        "confidence": "high",
        "critical_risk": "potentially_fatal",
        "diagnostics": {
          "biggest_scientific_risk": "核心可能只是经典最弱前置条件传播与加权集合覆盖的直接工程组合；当前实验主要证明该组合在由同一人工类型规格支撑的合成闭集语义中按设计工作，尚未证明独立于既有残余义务机制的科学增量。",
          "mechanism_falsifier": "在类型计划、工具效果、探针覆盖和无噪读回均正确的条件下，出现一个所有已编译义务 O 都被真实读回满足、但独立安全规则仍判定受保护承诺不安全的案例；这将直接否定反向义务闭包对提交安全的充分性。",
          "most_dangerous_prior_collision": "ETAS：其类型/效果语义、动态资源残余义务和轨迹监控最可能把 PDEO 的反向义务传播解释为较弱的运行时实例，而 packet 没有提供组件级等价性排除。",
          "strongest_scientific_contribution": "把写后验证从固定工具后置条件收窄为由当前下游承诺反向编译的证据闭包，并在受控实验中同时保持安全义务故障零危险提交、无关状态完整接受以及低于完整契约的读回成本。"
        },
        "evaluator_version": "CRL-EVAL-1.0",
        "free_review": "PDEO 的机制与窄主张都很清楚，正式实验也比单纯展示高准确率更有信息量：它分别测量危险提交、无关变异召回和探针成本，并用独立声明的安全规则生成标签。当前最关键的问题不是实现是否按设计运行，而是科学增量是否超出“最弱前置条件＋集合覆盖”。PDEO 与人工最小义务完全相同，且故障直接围绕人工安全谓词系统生成，使结果尚不足以证明计划派生机制在复杂计划中带来独立价值。最有判别力的后续证据应让同一写工具服务于不同下游承诺，验证义务与探针集合随计划改变，并与 ETAS、ToolGate 做组件级等价比较；否则 prior collision 可能致命。",
        "model_identity": "gpt-5.6-sol",
        "reasoning_effort": "xhigh",
        "reasons": {
          "claim_calibration": "最小主张严格限制在类型计划、效果与覆盖正确、离散状态和无噪读回的三个受控域，并逐项排除真实接口、并发、陈旧读、权限失败、恢复和端到端成功率。正式指标直接支持该范围内的零危险提交、无关变异召回 1.0，以及相对完整契约的成本 3 对 5。packet 也没有声称优于人工最小义务、替代完整审计或普遍胜过所有自适应验证；“开放世界”只能继续按相对封闭分支模型的未建模变异来窄解。",
          "mechanism_clarity": "计算链条明确：从承诺谓词 G 反向传播，可信确定效果可消解义务，外部不确定写入及回执不可消解，随后对剩余闭包 O 求加权探针覆盖并进行闭集提交判断。方法的输入假设、停止条件和不保证范围均被具体列出，且可以由危险提交、错误接受或成本不最小直接反驳。171 个案例中 PDEO 与人工最小义务一致，并呈现零危险提交、完整无关变异召回和成本 3，和所述机制相符。",
          "prior_separation": "packet 给出的实质差异是：义务由当前计划的下游承诺反向产生，再按探针成本最小覆盖，而非使用固定工具契约、人工样本约束或封闭故障分支。该差异在计算输入和验证目标上真实存在，但 ETAS 的残余义务、VERIMAP 的计划内验证生成以及 ToolGate 的契约机制均可能吸收它。尤其当前没有正文级等价性排除或组件级实现比较，且作者明确无法排除“最弱前置条件加加权集合覆盖的直接组合”，故只能评为 Mixed。",
          "problem_value": "研究针对成功回执与真实写入状态不一致时的危险外部提交，涉及安全性与验证成本的实质权衡，而非单纯 benchmark 调参。把“工具是否完整履约”与“当前下游承诺是否已有充分证据”分开，也形成了有价值的研究问题。缺口是三个同构合成域尚不能证明该问题在真实接口中的频率、代价和代表性，因此未达到强证据水平。",
          "scientific_specificity": "packet 明确给出三个域、四类分割、样本数、基线、探针成本、独立安全规则以及逐项指标，实验对象和评价口径高度具体。结果也清楚限定为 48 个单义务故障、63 个无关变异及小型探针目录，而没有用总体准确率掩盖安全与召回差异。不过三个域结构同源，探针成本恒定为 3，尚未展示不同下游承诺确实生成不同义务、复杂覆盖结构或规模增长，因此对关键“计划派生”计算的经验归因仍有限。"
        },
        "review_protocol": "CRL-IR-1.0",
        "reviewer_role": "SCI",
        "scores": {
          "claim_calibration": 4,
          "mechanism_clarity": 4,
          "prior_separation": 2,
          "problem_value": 3,
          "scientific_specificity": 3
        }
      },
      "report_sha256": "f6fc189aa8d55589c511596a48a448389efa3c5e2741355cc527adc3f0185cf2",
      "role_score_basis_points": 7875
    }
  },
  "schema_version": 1,
  "score_is_gate": false,
  "stability": {
    "max_numerator": 611250,
    "mean_numerator": "611250",
    "min_numerator": 611250,
    "overall_score_numerators": [
      611250
    ],
    "population_variance_numerator_squared": "0",
    "range_numerator": 0,
    "valid_measurement_count": 1
  },
  "valid": true
}

### Source: `failure_attribution_v001.md`

# 失败归因：DQBP Scratch 反证

## 证据级别

本记录只依据 `workbench_v001/scratch_metrics.json` 与 `workbench_v001/scratch_details.json`。这是控制器隔离的 Scratch 仿真，不是 Formal / Review-support 实验，未调用语言模型，也不能支持交付。

## 观察结果

三个域、每域 10,000 个同分布样本、预算 2、随机种子 20260813：

- DQBP：成功率 1.000，危险错误率 0，平均探针成本 1.7703；
- 状态信息增益：成功率 1.000，危险错误率 0，平均探针成本约 1.707；
- 固定目标读回：成功率 0.651；
- DQBP 相对预算匹配最佳基线的预设成功率优势：0.000。

在失败加重与成功加重的先验变体中，DQBP 与状态信息增益仍都达到 1.000 成功率，且 DQBP 平均成本分别为 1.805 和 1.728，均高于状态信息增益的 1.710 和 1.705。

## 主研究者解释

失败发生在方法核而非单一代码实现：DQBP 与状态信息增益共享有限分支模型，当前探针足以让状态熵目标顺便分离全部决策类。DQBP 在访问控制域选择成本为 2 的审计事件，在预约与库存域也没有形成更短的决策证据路径，因此“先按下游决策取商”没有转化为成本或成功率收益。

更根本地，DQBP 的目标是标准贝叶斯决策风险下的探针价值；在没有新的结构约束时，它容易被一般价值信息或强信息增益基线吸收。继续调节分支先验或添加专门让状态熵追逐噪声的样本，会把结果变成对基线不利的数据设计，不能作为挽救依据。

## 杀伤范围

- 杀死：当前 DQBP 方法核及其“优于状态信息增益”的主张；
- 未杀死：写后环境验证这一问题；
- 未支持：Run 级无交付，因为在终局前仍需完成一次正交路线复核；
- 不得复用：不能把相同分支模型换名后作为新候选。

## 后续约束

新的 H4 不使用已知故障分支来选择探针，而从计划承诺产生必须验证的证据闭包；它必须在未见故障上接受反证，并与完整工具契约、全量读回、DQBP 和状态信息增益共同比较。

## 6. Reproducibility Facts

### Source: `implementation_v001/obligation_core.py`

from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Mapping, Sequence


PROCEED = "PROCEED"
ABSTAIN = "ABSTAIN"


@dataclass(frozen=True, order=True, slots=True)
class Atom:
    field: str
    expected: str


@dataclass(frozen=True, slots=True)
class PlanAction:
    name: str
    preconditions: tuple[Atom, ...]
    effects: Mapping[str, str]
    trusted_deterministic: bool = True


@dataclass(frozen=True, slots=True)
class EvidenceProbe:
    name: str
    cost: int
    covers: frozenset[str]


@dataclass(frozen=True, slots=True)
class CompiledObligations:
    atoms: tuple[Atom, ...]
    probes: tuple[EvidenceProbe, ...]
    total_cost: int


@dataclass(frozen=True, slots=True)
class GateResult:
    method: str
    selected: str
    expected: str
    probe_names: tuple[str, ...]
    probe_cost: int

    @property
    def correct(self) -> bool:
        return self.selected == self.expected

    @property
    def unsafe_commit(self) -> bool:
        return self.selected == PROCEED and self.expected != PROCEED


def backward_obligations(
    prefix_actions: Sequence[PlanAction],
    protected_commit: PlanAction,
) -> tuple[Atom, ...]:
    """Compute evidence required at the post-write checkpoint.

    The protected commit is not executed by this function. Trusted deterministic
    prefix actions may establish future atoms; untrusted external actions cannot
    discharge evidence obligations merely through their declared effects.
    """

    required = set(protected_commit.preconditions)
    for action in reversed(prefix_actions):
        transformed: set[Atom] = set()
        for atom in required:
            if atom.field not in action.effects or not action.trusted_deterministic:
                transformed.add(atom)
                continue
            produced = action.effects[atom.field]
            if produced != atom.expected:
                raise ValueError(
                    f"plan action {action.name} establishes {atom.field}={produced}, "
                    f"but downstream requires {atom.expected}"
                )
        transformed.update(action.preconditions)
        required = transformed
    return tuple(sorted(required))


def minimum_cost_probe_cover(
    atoms: Sequence[Atom], probes: Sequence[EvidenceProbe]
) -> tuple[EvidenceProbe, ...]:
    required_fields = {atom.field for atom in atoms}
    if not required_fields:
        return ()

    candidates: list[tuple[tuple[int, int, tuple[str, ...]], tuple[EvidenceProbe, ...]]] = []
    for size in range(1, len(probes) + 1):
        for subset in combinations(probes, size):
            covered: set[str] = set()
            for probe in subset:
                covered.update(probe.covers)
            if required_fields.issubset(covered):
                key = (
                    sum(probe.cost for probe in subset),
                    len(subset),
                    tuple(sorted(probe.name for probe in subset)),
                )
                candidates.append((key, tuple(sorted(subset, key=lambda item: item.name))))
    if not candidates:
        missing = required_fields - set().union(*(probe.covers for probe in probes))
        raise ValueError(f"no probe cover for required fields: {sorted(missing)}")
    return min(candidates, key=lambda item: item[0])[1]


def compile_obligations(
    prefix_actions: Sequence[PlanAction],
    protected_commit: PlanAction,
    probes: Sequence[EvidenceProbe],
) -> CompiledObligations:
    atoms = backward_obligations(prefix_actions, protected_commit)
    selected = minimum_cost_probe_cover(atoms, probes)
    return CompiledObligations(
        atoms=atoms,
        probes=selected,
        total_cost=sum(probe.cost for probe in selected),
    )


def evaluate_atoms(atoms: Sequence[Atom], state: Mapping[str, str]) -> bool:
    return all(state.get(atom.field) == atom.expected for atom in atoms)


def run_compiled_gate(
    compiled: CompiledObligations,
    state: Mapping[str, str],
    *,
    expected: str,
    method: str = "pdeo",
) -> GateResult:
    visible_fields: set[str] = set()
    for probe in compiled.probes:
        visible_fields.update(probe.covers)
    observed = {field: state[field] for field in visible_fields if field in state}
    selected = PROCEED if evaluate_atoms(compiled.atoms, observed) else ABSTAIN
    return GateResult(
        method=method,
        selected=selected,
        expected=expected,
        probe_names=tuple(probe.name for probe in compiled.probes),
        probe_cost=compiled.total_cost,
    )


def run_atom_gate(
    method: str,
    atoms: Sequence[Atom],
    probes: Sequence[EvidenceProbe],
    state: Mapping[str, str],
    *,
    expected: str,
) -> GateResult:
    selected_probes = minimum_cost_probe_cover(atoms, probes) if atoms else ()
    visible_fields: set[str] = set()
    for probe in selected_probes:
        visible_fields.update(probe.covers)
    observed = {field: state[field] for field in visible_fields if field in state}
    selected = PROCEED if evaluate_atoms(atoms, observed) else ABSTAIN
    return GateResult(
        method=method,
        selected=selected,
        expected=expected,
        probe_names=tuple(probe.name for probe in selected_probes),
        probe_cost=sum(probe.cost for probe in selected_probes),
    )

### Source: `implementation_v001/plan_variation_bench.py`

from __future__ import annotations

from dataclasses import dataclass

from obligation_core import Atom, EvidenceProbe, PlanAction


@dataclass(frozen=True, slots=True)
class PlanVariant:
    name: str
    prefix_actions: tuple[PlanAction, ...]
    protected_commit: PlanAction


@dataclass(frozen=True, slots=True)
class PlanVariationDomain:
    name: str
    variants: tuple[PlanVariant, ...]
    probes: tuple[EvidenceProbe, ...]
    static_domain_atoms: tuple[Atom, ...]
    fixed_target_atom: Atom


def _derived_variant(
    name: str,
    required_environment_atoms: tuple[Atom, ...],
    derived_field: str,
) -> PlanVariant:
    prefix = PlanAction(
        name=f"prepare_{name}",
        preconditions=required_environment_atoms,
        effects={derived_field: "READY"},
        trusted_deterministic=True,
    )
    commit = PlanAction(
        name=f"commit_{name}",
        preconditions=(Atom(derived_field, "READY"),),
        effects={},
        trusted_deterministic=True,
    )
    return PlanVariant(name, (prefix,), commit)


def _single_field_probes(
    fields: tuple[str, ...], *, audit_field: str = "audit_event"
) -> tuple[EvidenceProbe, ...]:
    probes = [EvidenceProbe(f"read_{field}", 1, frozenset({field})) for field in fields]
    probes.append(EvidenceProbe("read_audit_event", 2, frozenset({audit_field})))
    return tuple(probes)


def build_plan_variation_domains() -> tuple[PlanVariationDomain, ...]:
    reservation_atoms = (
        Atom("target_status", "CONFIRMED"),
        Atom("payment_state", "CAPTURED"),
        Atom("other_booking", "UNCHANGED"),
    )
    reservation = PlanVariationDomain(
        name="reservation",
        variants=(
            _derived_variant(
                "full_confirmation", reservation_atoms, "confirmation_ready"
            ),
            _derived_variant(
                "status_notice", (reservation_atoms[0],), "status_notice_ready"
            ),
            _derived_variant(
                "payment_receipt", (reservation_atoms[1],), "receipt_ready"
            ),
            _derived_variant(
                "exclusive_itinerary",
                (reservation_atoms[0], reservation_atoms[2]),
                "itinerary_ready",
            ),
        ),
        probes=_single_field_probes(tuple(atom.field for atom in reservation_atoms)),
        static_domain_atoms=reservation_atoms,
        fixed_target_atom=reservation_atoms[0],
    )

    access_atoms = (
        Atom("target_role", "EDITOR"),
        Atom("scope_state", "PROJECT_ONLY"),
        Atom("other_principal", "UNCHANGED"),
    )
    access = PlanVariationDomain(
        name="access_control",
        variants=(
            _derived_variant("editor_operation", access_atoms, "editor_ready"),
            _derived_variant("role_notice", (access_atoms[0],), "role_notice_ready"),
            _derived_variant(
                "scoped_editor",
                (access_atoms[0], access_atoms[1]),
                "scoped_editor_ready",
            ),
            _derived_variant(
                "isolation_attestation",
                (access_atoms[1], access_atoms[2]),
                "isolation_ready",
            ),
        ),
        probes=_single_field_probes(tuple(atom.field for atom in access_atoms)),
        static_domain_atoms=access_atoms,
        fixed_target_atom=access_atoms[0],
    )

    inventory_atoms = (
        Atom("target_quantity", "PLUS_5"),
        Atom("warehouse_balance", "BALANCED"),
        Atom("other_sku", "UNCHANGED"),
    )
    inventory = PlanVariationDomain(
        name="inventory",
        variants=(
            _derived_variant("publish_restock", inventory_atoms, "restock_ready"),
            _derived_variant(
                "quantity_notice", (inventory_atoms[0],), "quantity_notice_ready"
            ),
            _derived_variant(
                "balanced_restock",
                (inventory_atoms[0], inventory_atoms[1]),
                "balanced_restock_ready",
            ),
            _derived_variant(
                "isolation_attestation",
                (inventory_atoms[1], inventory_atoms[2]),
                "inventory_isolation_ready",
            ),
        ),
        probes=_single_field_probes(tuple(atom.field for atom in inventory_atoms)),
        static_domain_atoms=inventory_atoms,
        fixed_target_atom=inventory_atoms[0],
    )

    document_atoms = (
        Atom("document_signature", "SIGNED"),
        Atom("audience_state", "PUBLIC"),
        Atom("sibling_document", "UNCHANGED"),
        Atom("checksum_state", "MATCH"),
    )
    document = PlanVariationDomain(
        name="document_release",
        variants=(
            _derived_variant("public_release", document_atoms, "public_release_ready"),
            _derived_variant(
                "internal_archive",
                (document_atoms[0], document_atoms[3]),
                "archive_ready",
            ),
            _derived_variant(
                "public_preview",
                (document_atoms[1], document_atoms[3]),
                "preview_ready",
            ),
            _derived_variant(
                "signature_notice", (document_atoms[0],), "signature_notice_ready"
            ),
        ),
        probes=(
            EvidenceProbe(
                "read_document_snapshot",
                2,
                frozenset({"document_signature", "checksum_state"}),
            ),
            EvidenceProbe("read_audience_state", 1, frozenset({"audience_state"})),
            EvidenceProbe(
                "read_sibling_document", 1, frozenset({"sibling_document"})
            ),
            EvidenceProbe(
                "read_document_signature", 1, frozenset({"document_signature"})
            ),
            EvidenceProbe("read_checksum_state", 1, frozenset({"checksum_state"})),
            EvidenceProbe("read_audit_event", 2, frozenset({"audit_event"})),
        ),
        static_domain_atoms=document_atoms,
        fixed_target_atom=document_atoms[0],
    )
    return reservation, access, inventory, document


def validate_plan_variation_domains(
    domains: tuple[PlanVariationDomain, ...],
) -> None:
    for domain in domains:
        variant_names = [variant.name for variant in domain.variants]
        if len(variant_names) != len(set(variant_names)):
            raise ValueError(f"duplicate plan variant: {domain.name}")
        covered = set().union(*(probe.covers for probe in domain.probes))
        static_fields = {atom.field for atom in domain.static_domain_atoms}
        if not static_fields.issubset(covered):
            raise ValueError(f"static contract lacks probe cover: {domain.name}")
        if domain.fixed_target_atom not in domain.static_domain_atoms:
            raise ValueError(f"fixed target is outside static atoms: {domain.name}")

### Source: `implementation_v001/formal_plan_variation_experiment.py`

from __future__ import annotations

import argparse
import json
import time
from dataclasses import dataclass
from itertools import combinations
from pathlib import Path
from typing import Mapping, Sequence

from obligation_core import (
    ABSTAIN,
    PROCEED,
    Atom,
    CompiledObligations,
    GateResult,
    PlanAction,
    compile_obligations,
    minimum_cost_probe_cover,
    run_atom_gate,
    run_compiled_gate,
)
from plan_variation_bench import (
    PlanVariant,
    PlanVariationDomain,
    build_plan_variation_domains,
    validate_plan_variation_domains,
)


EXPERIMENT_ID = "pdeo-plan-variation-suite-v2"
METHODS = (
    "no_verification",
    "fixed_target_readback",
    "static_domain_contract",
    "pdeo_direct_commit_only",
    "pdeo",
    "human_per_plan_minimal",
)


@dataclass(frozen=True, slots=True)
class HeldoutRule:
    atoms: tuple[Atom, ...]


@dataclass(frozen=True, slots=True)
class HeldoutDomain:
    canonical_state: Mapping[str, str]
    field_values: Mapping[str, tuple[str, ...]]
    variants: Mapping[str, HeldoutRule]


@dataclass(frozen=True, slots=True)
class VariationCase:
    case_id: str
    domain: str
    variant: str
    split: str
    state: Mapping[str, str]
    expected: str


def load_heldout_rules(path: Path) -> dict[str, HeldoutDomain]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if value.get("schema_version") != 1:
        raise ValueError("heldout rules schema_version must be 1")
    domains: dict[str, HeldoutDomain] = {}
    for domain_name, raw_domain in value["domains"].items():
        variants = {
            name: HeldoutRule(tuple(Atom(field, expected) for field, expected in rows))
            for name, rows in raw_domain["variants"].items()
        }
        domains[domain_name] = HeldoutDomain(
            canonical_state=dict(raw_domain["canonical_state"]),
            field_values={
                field: tuple(values)
                for field, values in raw_domain["field_values"].items()
            },
            variants=variants,
        )
    return domains


def validate_candidate_against_rules(
    candidates: Sequence[PlanVariationDomain],
    rules: Mapping[str, HeldoutDomain],
) -> None:
    candidate_domains = {domain.name: domain for domain in candidates}
    if set(candidate_domains) != set(rules):
        raise ValueError("candidate and heldout domain names differ")
    for domain_name, heldout in rules.items():
        candidate_names = {variant.name for variant in candidate_domains[domain_name].variants}
        if candidate_names != set(heldout.variants):
            raise ValueError(f"candidate and heldout variants differ: {domain_name}")
        if set(heldout.canonical_state) != set(heldout.field_values):
            raise ValueError(f"heldout state vocabulary differs: {domain_name}")
        for field, current in heldout.canonical_state.items():
            if current not in heldout.field_values[field]:
                raise ValueError(f"canonical value missing from vocabulary: {domain_name}/{field}")


def _is_safe(rule: HeldoutRule, state: Mapping[str, str]) -> bool:
    return all(state.get(atom.field) == atom.expected for atom in rule.atoms)


def _first_bad_value(
    heldout: HeldoutDomain, atom: Atom
) -> str:
    return next(value for value in heldout.field_values[atom.field] if value != atom.expected)


def build_cases(rules: Mapping[str, HeldoutDomain]) -> tuple[VariationCase, ...]:
    cases: list[VariationCase] = []
    seen: set[tuple[str, str, str, tuple[tuple[str, str], ...]]] = set()

    def add(
        domain_name: str,
        variant_name: str,
        split: str,
        state: Mapping[str, str],
        label: str,
    ) -> None:
        key = (domain_name, variant_name, split, tuple(sorted(state.items())))
        if key in seen:
            return
        seen.add(key)
        rule = rules[domain_name].variants[variant_name]
        expected = PROCEED if _is_safe(rule, state) else ABSTAIN
        cases.append(
            VariationCase(
                case_id=f"{domain_name}-{variant_name}-{label}-{len(cases):04d}",
                domain=domain_name,
                variant=variant_name,
                split=split,
                state=dict(state),
                expected=expected,
            )
        )

    for domain_name, heldout in rules.items():
        all_fields = set(heldout.canonical_state)
        for variant_name, rule in heldout.variants.items():
            base = dict(heldout.canonical_state)
            add(domain_name, variant_name, "canonical_safe", base, "canonical")

            for atom in rule.atoms:
                for alternative in heldout.field_values[atom.field]:
                    if alternative == atom.expected:
                        continue
                    mutated = dict(base)
                    mutated[atom.field] = alternative
                    add(
                        domain_name,
                        variant_name,
                        "single_obligation_faults",
                        mutated,
                        f"{atom.field}-{alternative}",
                    )

            required_fields = {atom.field for atom in rule.atoms}
            nuisance_fields = sorted(all_fields - required_fields)
            for field in nuisance_fields:
                for alternative in heldout.field_values[field]:
                    if alternative == base[field]:
                        continue
                    mutated = dict(base)
                    mutated[field] = alternative
                    add(
                        domain_name,
                        variant_name,
                        "safe_nuisance_variants",
                        mutated,
                        f"{field}-{alternative}",
                    )

            for left, right in combinations(rule.atoms, 2):
                mutated = dict(base)
                mutated[left.field] = _first_bad_value(heldout, left)
                mutated[right.field] = _first_bad_value(heldout, right)
                add(
                    domain_name,
                    variant_name,
                    "paired_obligation_faults",
                    mutated,
                    f"{left.field}-{right.field}",
                )

            if nuisance_fields:
                nuisance = nuisance_fields[0]
                nuisance_bad = next(
                    value
                    for value in heldout.field_values[nuisance]
                    if value != base[nuisance]
                )
                for atom in rule.atoms:
                    mutated = dict(base)
                    mutated[atom.field] = _first_bad_value(heldout, atom)
                    mutated[nuisance] = nuisance_bad
                    add(
                        domain_name,
                        variant_name,
                        "obligation_plus_nuisance_faults",
                        mutated,
                        f"{atom.field}-plus-{nuisance}",
                    )
    return tuple(cases)


def _find_variant(domain: PlanVariationDomain, name: str) -> PlanVariant:
    return next(variant for variant in domain.variants if variant.name == name)


def _run_method(
    method: str,
    domain: PlanVariationDomain,
    variant: PlanVariant,
    rule: HeldoutRule,
    state: Mapping[str, str],
    expected: str,
    compiled: CompiledObligations,
) -> GateResult:
    if method == "no_verification":
        return GateResult(method, PROCEED, expected, (), 0)
    if method == "fixed_target_readback":
        return run_atom_gate(
            method,
            (domain.fixed_target_atom,),
            domain.probes,
            state,
            expected=expected,
        )
    if method == "static_domain_contract":
        return run_atom_gate(
            method,
            domain.static_domain_atoms,
            domain.probes,
            state,
            expected=expected,
        )
    if method == "pdeo_direct_commit_only":
        return GateResult(method, ABSTAIN, expected, (), 0)
    if method == "pdeo":
        return run_compiled_gate(compiled, state, expected=expected, method=method)
    if method == "human_per_plan_minimal":
        return run_atom_gate(
            method,
            rule.atoms,
            domain.probes,
            state,
            expected=expected,
        )
    raise ValueError(f"unsupported method: {method}")


def _mean(values: Sequence[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _metric(
    name: str,
    value: float,
    *,
    unit: str,
    split: str,
    aggregation: str,
    n: int,
) -> dict[str, object]:
    return {
        "name": name,
        "value": value,
        "unit": unit,
        "split": split,
        "aggregation": aggregation,
        "n": n,
    }


def _corrupt_variant(variant: PlanVariant, omitted: Atom) -> PlanVariant:
    if len(variant.prefix_actions) != 1:
        raise ValueError("spec omission test expects one prefix action")
    current = variant.prefix_actions[0]
    reduced = tuple(atom for atom in current.preconditions if atom != omitted)
    corrupted = PlanAction(
        name=current.name + "_omitted",
        preconditions=reduced,
        effects=current.effects,
        trusted_deterministic=current.trusted_deterministic,
    )
    return PlanVariant(variant.name + "_omitted", (corrupted,), variant.protected_commit)


def run_formal(rules_path: Path) -> tuple[dict, dict]:
    started = time.perf_counter()
    domains = build_plan_variation_domains()
    validate_plan_variation_domains(domains)
    rules = load_heldout_rules(rules_path)
    validate_candidate_against_rules(domains, rules)
    domain_by_name = {domain.name: domain for domain in domains}

    compiled: dict[tuple[str, str], CompiledObligations] = {}
    exact_atom_matches: list[float] = []
    exact_probe_matches: list[float] = []
    plan_cost_rows: list[dict[str, object]] = []
    for domain in domains:
        heldout = rules[domain.name]
        static_probes = minimum_cost_probe_cover(domain.static_domain_atoms, domain.probes)
        static_cost = sum(probe.cost for probe in static_probes)
        for variant in domain.variants:
            key = (domain.name, variant.name)
            item = compile_obligations(
                variant.prefix_actions, variant.protected_commit, domain.probes
            )
            compiled[key] = item
            rule = heldout.variants[variant.name]
            oracle_probes = minimum_cost_probe_cover(rule.atoms, domain.probes)
            exact_atom_matches.append(float(set(item.atoms) == set(rule.atoms)))
            exact_probe_matches.append(
                float(
                    {probe.name for probe in item.probes}
                    == {probe.name for probe in oracle_probes}
                )
            )
            plan_cost_rows.append(
                {
                    "domain": domain.name,
                    "variant": variant.name,
                    "pdeo_cost": item.total_cost,
                    "static_domain_cost": static_cost,
                    "compiled_atoms": [
                        [atom.field, atom.expected] for atom in item.atoms
                    ],
                    "heldout_atoms": [
                        [atom.field, atom.expected] for atom in rule.atoms
                    ],
                    "compiled_probes": [probe.name for probe in item.probes],
                    "oracle_probes": [probe.name for probe in oracle_probes],
                }
            )

    cases = build_cases(rules)
    rows: list[dict[str, object]] = []
    for case in cases:
        domain = domain_by_name[case.domain]
        variant = _find_variant(domain, case.variant)
        rule = rules[case.domain].variants[case.variant]
        for method in METHODS:
            result = _run_method(
                method,
                domain,
                variant,
                rule,
                case.state,
                case.expected,
                compiled[(case.domain, case.variant)],
            )
            rows.append(
                {
                    "case_id": case.case_id,
                    "domain": case.domain,
                    "variant": case.variant,
                    "split": case.split,
                    "state": dict(case.state),
                    "method": method,
                    "selected": result.selected,
                    "expected": case.expected,
                    "correct": result.correct,
                    "unsafe_commit": result.unsafe_commit,
                    "probe_cost": result.probe_cost,
                    "probes": list(result.probe_names),
                }
            )

    omission_rows: list[dict[str, object]] = []
    for domain in domains:
        heldout = rules[domain.name]
        for variant in domain.variants:
            rule = heldout.variants[variant.name]
            omitted = rule.atoms[0]
            corrupted = _corrupt_variant(variant, omitted)
            corrupted_compiled = compile_obligations(
                corrupted.prefix_actions, corrupted.protected_commit, domain.probes
            )
            state = dict(heldout.canonical_state)
            state[omitted.field] = _first_bad_value(heldout, omitted)
            result = run_compiled_gate(
                corrupted_compiled, state, expected=ABSTAIN, method="pdeo_spec_omission"
            )
            omission_rows.append(
                {
                    "domain": domain.name,
                    "variant": variant.name,
                    "omitted_atom": [omitted.field, omitted.expected],
                    "state": state,
                    "compiled_atoms": [
                        [atom.field, atom.expected] for atom in corrupted_compiled.atoms
                    ],
                    "selected": result.selected,
                    "unsafe_commit": result.unsafe_commit,
                }
            )

    records: list[dict[str, object]] = [
        _metric(
            "pdeo_compiled_obligation_exact_match_rate",
            _mean(exact_atom_matches),
            unit="proportion",
            split="heldout_plan_variants",
            aggregation="plan_mean",
            n=len(exact_atom_matches),
        ),
        _metric(
            "pdeo_compiled_probe_set_exact_match_rate",
            _mean(exact_probe_matches),
            unit="proportion",
            split="heldout_plan_variants",
            aggregation="plan_mean",
            n=len(exact_probe_matches),
        ),
        _metric(
            "pdeo_mean_plan_probe_cost",
            _mean([float(row["pdeo_cost"]) for row in plan_cost_rows]),
            unit="cost_units",
            split="heldout_plan_variants",
            aggregation="plan_mean",
            n=len(plan_cost_rows),
        ),
        _metric(
            "static_domain_contract_mean_plan_probe_cost",
            _mean([float(row["static_domain_cost"]) for row in plan_cost_rows]),
            unit="cost_units",
            split="heldout_plan_variants",
            aggregation="plan_mean",
            n=len(plan_cost_rows),
        ),
        _metric(
            "pdeo_spec_omission_unsafe_commit_rate",
            _mean([float(row["unsafe_commit"]) for row in omission_rows]),
            unit="proportion",
            split="specification_omission_sensitivity",
            aggregation="plan_mean",
            n=len(omission_rows),
        ),
    ]

    splits = sorted({case.split for case in cases})
    for split in splits:
        for method in METHODS:
            subset = [
                row
                for row in rows
                if row["split"] == split and row["method"] == method
            ]
            safe = [row for row in subset if row["expected"] == PROCEED]
            records.extend(
                [
                    _metric(
                        f"{method}_unsafe_commit_rate_{split}",
                        _mean([float(row["unsafe_commit"]) for row in subset]),
                        unit="proportion",
                        split=split,
                        aggregation="case_mean",
                        n=len(subset),
                    ),
                    _metric(
                        f"{method}_gate_accuracy_{split}",
                        _mean([float(row["correct"]) for row in subset]),
                        unit="proportion",
                        split=split,
                        aggregation="case_mean",
                        n=len(subset),
                    ),
                    _metric(
                        f"{method}_average_probe_cost_{split}",
                        _mean([float(row["probe_cost"]) for row in subset]),
                        unit="cost_units",
                        split=split,
                        aggregation="case_mean",
                        n=len(subset),
                    ),
                ]
            )
            if safe:
                records.append(
                    _metric(
                        f"{method}_valid_commit_recall_{split}",
                        _mean(
                            [float(row["selected"] == PROCEED) for row in safe]
                        ),
                        unit="proportion",
                        split=split,
                        aggregation="case_mean",
                        n=len(safe),
                    )
                )

    for domain_name in sorted(rules):
        plan_rows = [row for row in plan_cost_rows if row["domain"] == domain_name]
        records.extend(
            [
                _metric(
                    f"pdeo_mean_plan_probe_cost_{domain_name}",
                    _mean([float(row["pdeo_cost"]) for row in plan_rows]),
                    unit="cost_units",
                    split=f"domain:{domain_name}",
                    aggregation="plan_mean",
                    n=len(plan_rows),
                ),
                _metric(
                    f"static_domain_contract_mean_plan_probe_cost_{domain_name}",
                    _mean([float(row["static_domain_cost"]) for row in plan_rows]),
                    unit="cost_units",
                    split=f"domain:{domain_name}",
                    aggregation="plan_mean",
                    n=len(plan_rows),
                ),
            ]
        )
        for method in ("static_domain_contract", "pdeo", "human_per_plan_minimal"):
            faults = [
                row
                for row in rows
                if row["domain"] == domain_name
                and row["method"] == method
                and row["split"]
                in {
                    "single_obligation_faults",
                    "paired_obligation_faults",
                    "obligation_plus_nuisance_faults",
                }
            ]
            safe_nuisance = [
                row
                for row in rows
                if row["domain"] == domain_name
                and row["method"] == method
                and row["split"] == "safe_nuisance_variants"
            ]
            records.extend(
                [
                    _metric(
                        f"{method}_unsafe_commit_rate_all_faults_{domain_name}",
                        _mean([float(row["unsafe_commit"]) for row in faults]),
                        unit="proportion",
                        split=f"domain:{domain_name}",
                        aggregation="fault_case_mean",
                        n=len(faults),
                    ),
                    _metric(
                        f"{method}_valid_commit_recall_safe_nuisance_{domain_name}",
                        _mean(
                            [
                                float(row["selected"] == PROCEED)
                                for row in safe_nuisance
                            ]
                        ),
                        unit="proportion",
                        split=f"domain:{domain_name}",
                        aggregation="safe_case_mean",
                        n=len(safe_nuisance),
                    ),
                ]
            )

    metrics = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "records": records,
        "resource_usage": {
            "tokens": 0,
            "api_calls": 0,
            "wall_time_seconds": time.perf_counter() - started,
            "gpu_time_seconds": 0,
            "estimated_cost": 0,
        },
        "errors": [],
        "warnings": [
            "Heldout rules are byte-frozen in a separate declared input, but were authored within the same Run rather than by an external team.",
            "All domains remain synthetic and all read probes are deterministic and noise-free.",
            "Specification omission sensitivity is an expected failure test outside the correct-specification claim scope."
        ],
    }
    details = {
        "schema_version": 1,
        "experiment_id": EXPERIMENT_ID,
        "rules_path": str(rules_path),
        "case_count": len(cases),
        "cases_by_split": {
            split: sum(case.split == split for case in cases) for split in splits
        },
        "plan_cost_and_exactness": plan_cost_rows,
        "specification_omission_rows": omission_rows,
        "rows": rows,
    }
    return metrics, details


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rules-input", type=Path, required=True)
    parser.add_argument("--metrics-output", type=Path, required=True)
    parser.add_argument("--details-output", type=Path, required=True)
    args = parser.parse_args()
    metrics, details = run_formal(args.rules_input)
    args.metrics_output.write_text(
        json.dumps(metrics, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    args.details_output.write_text(
        json.dumps(details, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
        newline="\n",
    )
    wanted = {
        "pdeo_compiled_obligation_exact_match_rate",
        "pdeo_compiled_probe_set_exact_match_rate",
        "pdeo_mean_plan_probe_cost",
        "static_domain_contract_mean_plan_probe_cost",
        "pdeo_spec_omission_unsafe_commit_rate",
        "pdeo_unsafe_commit_rate_single_obligation_faults",
        "pdeo_valid_commit_recall_safe_nuisance_variants",
        "static_domain_contract_valid_commit_recall_safe_nuisance_variants",
    }
    print(
        json.dumps(
            {
                "experiment_id": EXPERIMENT_ID,
                "case_count": details["case_count"],
                "key_records": [
                    record for record in metrics["records"] if record["name"] in wanted
                ],
                "warnings": metrics["warnings"],
            },
            ensure_ascii=False,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()

### Source: `implementation_v001/test_plan_variation.py`

from __future__ import annotations

from pathlib import Path

from formal_plan_variation_experiment import (
    build_cases,
    load_heldout_rules,
    run_formal,
)
from obligation_core import compile_obligations
from plan_variation_bench import (
    build_plan_variation_domains,
    validate_plan_variation_domains,
)


RULES = (
    Path(__file__).resolve().parents[1]
    / "experiment_v001"
    / "specs"
    / "pdeo-plan-heldout-rules-v2.json"
)


def test_compiled_obligations_change_with_plan() -> None:
    domains = build_plan_variation_domains()
    validate_plan_variation_domains(domains)
    for domain in domains:
        atom_sets = {
            frozenset(
                compile_obligations(
                    variant.prefix_actions, variant.protected_commit, domain.probes
                ).atoms
            )
            for variant in domain.variants
        }
        assert len(atom_sets) == len(domain.variants)


def test_heldout_suite_has_plan_and_state_variation() -> None:
    rules = load_heldout_rules(RULES)
    cases = build_cases(rules)
    assert len(rules) == 4
    assert sum(len(domain.variants) for domain in rules.values()) == 16
    assert len(cases) >= 150
    assert {case.split for case in cases} == {
        "canonical_safe",
        "obligation_plus_nuisance_faults",
        "paired_obligation_faults",
        "safe_nuisance_variants",
        "single_obligation_faults",
    }


def test_plan_variation_killer_conditions() -> None:
    metrics, _ = run_formal(RULES)
    by_name = {record["name"]: record for record in metrics["records"]}
    assert by_name["pdeo_compiled_obligation_exact_match_rate"]["value"] == 1.0
    assert by_name["pdeo_compiled_probe_set_exact_match_rate"]["value"] == 1.0
    assert (
        by_name["pdeo_unsafe_commit_rate_single_obligation_faults"]["value"]
        == 0.0
    )
    assert (
        by_name["pdeo_valid_commit_recall_safe_nuisance_variants"]["value"]
        == 1.0
    )
    assert (
        by_name["pdeo_mean_plan_probe_cost"]["value"]
        < by_name["static_domain_contract_mean_plan_probe_cost"]["value"]
    )
    assert by_name["pdeo_spec_omission_unsafe_commit_rate"]["value"] == 1.0

## 7. Known Limitations

### Source: `selection_context_v001.md`

# 当前选择与淘汰上下文

## 选择

当前唯一进入正式实验的候选是 H4：计划派生证据义务（PDEO）。它从受保护下游承诺反向传播状态谓词，并按只读探针成本求最小覆盖；与 H1 的有限分支决策风险目标不同。

选择依据不是“结果更好看”，而是 H4 在方法输入和失败模型上与 H1 正交：H1 需要已知故障分支与先验，H4 需要正确的类型计划与工具效果。正式系统性变异实验已支持其窄主张，但没有解除类型规格和真实生态有效性风险。

## 已淘汰或不投入

- **H1 DQBP**：状态信息增益以更低成本达到相同已知分支成功率，主优势为 0；方法核被公平基线吸收。
- **H2 自动补全后置条件**：与 ToolGate 的缺失契约边界及自动形式化验证/修复最近工作过近，且当前无法低成本获得独立真实契约。
- **H3 新鲜度账本**：STALE/CUPMEM 和 Agent-BRACE 已覆盖写侧裁决、受权读出与不确定信念状态。
- **大规模工具检索正交路线**：ToolRet、Meta-Tool、ToolDreamer、NaviAgent、非负近邻检索和自适应候选数已形成密集强近邻。
- **形式规格验证正交路线**：Verus-SpecGym、往返验证修复、变异测试和主动判别输入已覆盖主要机制空间。

## 仍可能杀死 H4 的因素

1. Reviewer 判断其只是经典最弱前置条件和集合覆盖的直接工程移植，没有足够独立方法贡献；
2. ETAS 的残余义务或 VERIMAP 的计划生成验证函数在正文中已包含等价运行时证据编译；
3. 合成实验与人工类型计划使最大剩余疑问仍是端到端目标对应性；
4. 工具完整契约的额外拒绝反映更强正确性目标，而非不必要成本。

因此，当前状态只足以准备固定三审，不足以由主研究者直接宣布交付。

## 首次固定三审与处置

`review_v001/evaluations/eval-0001` 是有效的首次固定三审：三角色均无联网、工具或越界事件，但都把关键风险评为 `potentially_fatal`。主研究者没有据总分 61.1250 宣布交付，而是接受其中可反证的实证异议：原实验没有计划变化，无法区分计划条件化编译与每域固定三探针契约。

有界修订增加四域 16 个计划变体、静态域契约、直接提交消融、逐计划人工最小上界和规格遗漏敏感性。最终支撑 attempt 改为 `attempt-pdeo-plan-formal-002`；旧实验和首次三审完整保留为历史，不再作为最终实现的唯一机制证据。

### Source: `evidence_packet_v001.md`

# 证据清单

## 文献与边界证据

- ToolGate，Findings of ACL 2026：固定霍尔式前置/后置契约与验证提交。https://aclanthology.org/2026.findings-acl.470/
- VERIMAP，2026：规划时为子任务生成验证函数。https://arxiv.org/abs/2510.17109
- Failing Tools，2026：把轨迹约束解释为证据义务和安全不变量。https://openreview.net/forum?id=j7YsSnA64D
- Verified Tool Calls，2026：固定写后验证、重试前验证与幂等键。https://arxiv.org/abs/2608.02645
- ETAS，2026：类型/效果语义、轨迹监控与动态资源残余义务。https://arxiv.org/abs/2607.17780
- AgentCheck，2026：模型上下文协议工具的系统故障注入工作台。https://arxiv.org/abs/2607.11098

以上来源只支持最近边界和问题存在性；它们不自动证明 PDEO 新颖。

## Run 内检索快照

- `hypotheses_v001/searches/initial-scope-001/`
- `hypotheses_v001/searches/orthogonal-tool-retrieval-001/`

## 负结果

- `workbench_v001/scratch_metrics.json`
- `workbench_v001/scratch_details.json`
- `failure_attribution_v001.md`

这些材料只支持 H1 淘汰，不支持 H4 交付。

## H4 Scratch

- `workbench_v001/pdeo_scratch_metrics.json`
- `workbench_v001/pdeo_scratch_details.json`

这些材料用于预检和实现修正，不是交付支撑。

## H4 Formal / Review-support

- `experiment_v001/specs/pdeo-plan-heldout-rules-v2.json`
- `experiment_v001/specs/pdeo-plan-variation-suite-v2.json`
- `experiment_v001/attempts/attempt-pdeo-plan-formal-002/execution.json`
- `experiment_v001/attempts/attempt-pdeo-plan-formal-002/metrics.json`
- `experiment_v001/attempts/attempt-pdeo-plan-formal-002/plan-variation-details.json`
- `experiment_v001/plan_variation_plan.md`
- `experiment_v001/plan_variation_result.md`

最终支撑是 `attempt-pdeo-plan-formal-002`。它在四个域、16 个计划变体和 178 个计划—状态案例上评价逐计划义务与探针编译，并以独立冻结输入提供评价规则。候选实现不读取该规则文件；但规则、计划与实现仍由同一主研究者在同一 Run 内设计，不能等价为外部独立基准。

关键源码随最终 Reviewer packet 直接提供正文：

- `implementation_v001/obligation_core.py`
- `implementation_v001/plan_variation_bench.py`
- `implementation_v001/formal_plan_variation_experiment.py`
- `implementation_v001/test_plan_variation.py`

## 较早 H4 证据与三审历史

- `experiment_v001/specs/pdeo-systematic-fault-suite-v1.json`
- `experiment_v001/attempts/attempt-pdeo-formal-002/execution.json`
- `experiment_v001/attempts/attempt-pdeo-formal-002/metrics.json`
- `experiment_v001/attempts/attempt-pdeo-formal-002/formal-details.json`
- `experiment_v001/plan.md`
- `experiment_v001/result.md`
- `review_v001/evaluations/eval-0001/aggregate.json`
- `review_response_v001.md`

第一套系统性状态变异实验用于证明闭集提交性质，但计划没有变化。评价规则与 PDEO 编译器在同一实验程序中以独立常量和函数实现；标签函数不调用编译器。首次固定三审有效，却指出它不能识别“计划派生”而非“每域固定契约”。因此它保留为较早支持，不替代最终的计划变化 Formal。

`attempt-pdeo-formal-001` 是同规格的早期有效运行，但其实现文件身份清单不完整，与最终实现 manifest 不匹配；它保留在 Run 中，不作为交付支撑。001 与 002 的数值指标除墙钟时间外完全相同。

### Source: `hypothesis_portfolio_v001.md`

# 假设组合与当前选择

## H1：决策取商的写后分支探针

状态：已淘汰。

Scratch 仿真中，DQBP 与共享同一分支模型和探针集合的状态信息增益基线都达到 1.000 成功率、0 危险错误；DQBP 平均探针成本为 1.7703，状态信息增益为 1.707。预设的主要成功率优势为 0.000。该方法的决策风险目标没有产生不可被公平基线吸收的收益。

## H2：从工具文档自动补全缺失后置条件

状态：不投入。

它与 ToolGate 的缺失契约边界直接相邻，且正确性评价依赖大规模人工契约或可执行规格。Verus-SpecGym、基于往返验证与修复的自动形式化、变异测试规格评价等最近工作已把“生成规格后再用独立执行反证”推进得很近；当前没有足够清晰的独立计算变化。

## H3：带权限标记的状态新鲜度账本

状态：已淘汰为主候选。

STALE/CUPMEM 已覆盖写侧裁决和受权读出，Agent-BRACE 又覆盖显式不确定信念状态；剩余差异不足以支撑独立方法核。

## H4：计划派生证据义务

状态：唯一存活候选；已完成三审驱动的有界修订，等待第二次固定三审。

从下游外部承诺的前提沿类型计划反向传播，得到当前写入之后必须由真实环境读回支持的原子谓词，再求最小成本探针覆盖。它不依赖有限故障分支或先验，目标是在开放世界故障下保持闭集提交，同时避免验证计划无关的完整工具状态。

独立风险：方法可能只是经典最弱前置条件与集合覆盖在工具智能体上的直接移植；类型计划和工具效果若错误，安全保证会失效；若完整工具契约本来就很小，成本优势消失。

首次固定三审没有接受为交付依据：三位 Reviewer 都把最近工作碰撞和同源规格风险列为潜在致命问题，实证 Reviewer 进一步指出原实验只变化状态、不变化计划。主研究者接受这一机制识别异议，冻结了 16 个计划变体、四域静态强契约、直接提交消融、人工作为上界的逐计划最小探针，以及独立保存的评价规则。修订 Formal 中 PDEO 的逐计划义务与探针集合和人工上界完全一致，平均成本 2.0，静态域契约为 3.25；规格遗漏则在 16/16 个案例中产生危险提交，确认该前提不能被隐藏。

## 正交路线复核

除状态验证外，本版本复核了大规模工具检索与自动形式规格两条正交路线。工具检索已有 ToolRet、Meta-Tool、ToolDreamer、NaviAgent、非负近邻检索和自适应候选数等强近邻；规格路线已有 Verus-SpecGym、往返验证修复、变异测试与主动判别输入。未找到足以在当前资源下形成更清晰方法核的缺口。

H4 的最近边界包括 ToolGate 的固定霍尔契约、VERIMAP 的计划同时生成验证函数、Failing Tools 的人工轨迹证据约束、Verified Tool Calls 的固定写后验证包装，以及 ETAS 的类型/效果与残余义务。H4 只有在“反向计划条件化 + 最小证据覆盖 + 未见故障闭集提交”这一组合产生可复查优势时才继续。

## Evidence Inventory (machine generated)

```json
{
  "comparison_count": 0,
  "comparisons": [],
  "formal_attempt_count": 4,
  "formal_attempts": [
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-pdeo-formal-001",
      "path": "experiment_v001/attempts/attempt-pdeo-formal-001/execution.json",
      "read_error": null,
      "record_sha256": "879c6b9a87c853db7f5c747ab8e404d71894d68c3c59276960be0a36eb217a2e",
      "schema_version": 7,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": true
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-pdeo-formal-002",
      "path": "experiment_v001/attempts/attempt-pdeo-formal-002/execution.json",
      "read_error": null,
      "record_sha256": "65d6721da32c82b39c624c3cf7a752f7472f588f485494b25b2d3ed0e5aafad4",
      "schema_version": 7,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": true
    },
    {
      "association": "MISMATCH",
      "attempt_id": "attempt-pdeo-plan-formal-001",
      "path": "experiment_v001/attempts/attempt-pdeo-plan-formal-001/execution.json",
      "read_error": null,
      "record_sha256": "77b5b5ebba1161f070526bab564d7f6b09614fb7dd1e61eede362aa1e2e339a5",
      "schema_version": 7,
      "selected_in_core": false,
      "status": "SUCCESS",
      "valid_review_support": false
    },
    {
      "association": "MATCH",
      "attempt_id": "attempt-pdeo-plan-formal-002",
      "path": "experiment_v001/attempts/attempt-pdeo-plan-formal-002/execution.json",
      "read_error": null,
      "record_sha256": "9c88816647766073aca733785f24c68d292ca90ba556714e97f811a5d3a06d48",
      "schema_version": 7,
      "selected_in_core": true,
      "status": "SUCCESS",
      "valid_review_support": true
    }
  ],
  "implementation_key": "e76decbab2541209f12f559ba63461caa055149a167607543c04f2515f0c58bf",
  "machine_judgment": "NONE_FACTS_ONLY",
  "recorded_attempt_count": 0,
  "recorded_attempts": [],
  "schema_version": 1,
  "version": "v001"
}
```
