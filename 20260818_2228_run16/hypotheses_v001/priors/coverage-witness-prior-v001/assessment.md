# 最近先行科研解释

> 本文件属于主研究者解释，可在阅读候选、PDF、Evidence 和实验后继续修订；它不进入机器事实快照哈希。

- 审计标识：`coverage-witness-prior-v001`
- 碰撞类型：`PROBLEM_AND_EVALUATION_OCCUPIED_RUNTIME_METHOD_UNRESOLVED`

## 重大科研决策（仅在本先行实际参与关闭、方法核/论文方向杀伤或重大升级时填写）

- KILLED：把“完整性敏感负向推理”作为新问题、形式化、评价协议或自然文档现象；把一般模型外工具合约门控作为新计算。
- SURVIVES：尚待真实 API 杀手实验判定的窄系统差分——从工具原生分页/作用域/快照元数据无 oracle 地生成查询相对覆盖见证，并在负命题提交前执行非对称准入与定向补查。
- WHY：CROWN-QA 已给出几乎相同的查询相对覆盖语义、Certified-Negative/Unknown 标签、合成配对、真实文档对照、结构化 certificate 与固定映射；ToolGate 已以 Hoare 风格合约决定工具结果是否提交。现有两项 Formal 只证明本地系统行为差分，不能恢复已被占据的新颖性。

<!-- 普通检索无需填写本区；重大决策的权威结构化记录仍写入 Hypothesis decision history。 -->

## 真正的 nearest prior

1. CROWN-QA / When Absence Is Evidence（arXiv:2608.04591v1）：定义完整性敏感负向推理；只有证据完整且覆盖查询作用域时才允许 Certified-Negative，否则为 Unknown。含 5,000 个合成样本、1,599 个真实文档对照样本、三模型、七种提示，以及结构化 query scope / evidence scope / coverage certificate 加固定映射。它直接占据当前问题、形式化、评价和现象。
2. ToolGate（arXiv:2601.04688v1）：Hoare 风格工具前/后置条件、可信符号状态与运行时提交门，直接占据一般合约式结果准入；但未检索到对负命题查询覆盖的专门实例。
3. NabaOS / Tool Receipts（arXiv:2603.10060v1）：运行时回执、claim-level 认识论分类和错误不存在检测。其协议对 absence 的机械条件是 cited tool call `result_count = 0`；其“false absence”注入是工具已有非空结果而模型声称为空，因此不处理“工具为空但覆盖不完整”。
4. Verified Tool Calls（arXiv:2608.02645v1）：对非原子写操作做只读后置条件核验、verify-before-retry 和幂等键；已明确三值 verifier、完整 postcondition 与陈旧可见性。它的实验是两个写操作工作流，且把更丰富的语义完整性验证列为未来工作。
5. SGR-Bench（arXiv:2605.22219v1）：测得检索作用域漂移占所审计失败的 37.2%，主张评价应验证结果是否锚定正确 source slice；没有提出工具覆盖见证或否定性命题运行时准入。
6. Failing Tools / AgentCheck / ReliabilityBench：覆盖陈旧、部分、静默无操作与故障恢复，是必须纳入扩大实验的强评价与基线家族。

## 实质组件重合

- 与 CROWN-QA 重合：查询相对覆盖语义、完整/部分/作用域错配控制、负向结论与未知的非对称许可、结构化 certificate 和固定决策映射。
- 与 ToolGate 重合：模型外合约、运行时结果提交门和可信状态更新。
- 与 NabaOS 重合：运行时检查 claim 与工具证据、避免只依赖模型自我标注、检测错误不存在结论。
- 与 Verified Tool Calls 重合：模型外 wrapper、三值不确定性、只读核验、一次额外查询、陈旧/部分状态。
- 与 SGR-Bench 重合：作用域漂移和结果集合完整性是主要失败源。
- 不重合的当前计算：见证绑定的是“查询是否覆盖待否定命题”，而不是“调用是否真实”或“写操作后置条件是否成立”；门控对象是负命题提交，不是所有动作重试。

## 仍存贡献增量

- Problem / Phenomenon：无；CROWN-QA 已占据。
- Computation：仅剩“从真实工具原生元数据生成覆盖见证 + 负命题准入 + 定向补查”的系统组合是否未被 ToolGate/CROWN 直接实现；尚未通过真实 API 证明。
- Evaluation：无独立新颖性；现有指标可作为系统实验测量，但不能主张新评价。
- Empirical Finding：两项本地 Screening 显示 gate 在 Qwen3-8B 合成任务上把强提示错误否定率 0.6875 降至 0；在 Qwen2.5-7B、公开 SGR-Bench answer sets 的 11 个可解析任务上把一般 postcondition 的 0.4545 降至 0.0909。第二项仍为模拟分页且有 11/12 偏差。

## 最危险替代解释

当前结果可能只是适配器把 oracle 完整性转写为显式元数据、再自动全量补查；在真实 API、复杂查询谓词或无法一键扩大作用域时，见证生成可能等价于手写完整后置条件。即使系统有效，也可能只是 CROWN-QA certificate/固定映射嵌入 ToolGate 合约的直接组合。

## 最小区分实验

冻结至少两个真实分页 API 的原始响应，只用 API 原生 `totalResults`、分页游标、作用域回显或快照字段生成见证，不允许读取 oracle answer set。比较：CROWN-style 模型 certificate + 固定规则、ToolGate-style 任务特定后置条件、coverage gate；三者信息和补查预算匹配。组合基线追平、原生元数据不足或必须手写答案时，当前方法核心死亡。

## 方法死亡后仍存现象

无可退守的新评价现象：CROWN-QA 已直接占据。如果运行时方法被组合强基线吸收，当前论文方向应关闭，而不是缩窄 Claim 制造 Delivery。

## 背景与身份未解决项

本次机器先行检索快照 degraded，候选排序未召回上述最危险工作；上述判断来自主研究者对实时 arXiv 主页面/全文的阅读。扩大前应把这些论文 PDF 或可定位正文保存为 Run-local 审计材料，并检查其引用邻域。
