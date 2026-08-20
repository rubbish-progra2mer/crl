<!-- crl-v3-evidence-ids
["ev-p051-omitted-constraint-failure","ev-p051-solver-guarantee-boundary","ev-p051-formalization-pipeline","ev-p052-implicit-constraint-failure","ev-p052-self-diagnosis-nontermination","ev-p052-direct-code-smt-baselines","ev-p052-decomposed-formalization","ev-p054-natural-language-implicit-predicate-failure","ev-p055-plan-correctness-false-positive-boundary","ev-p055-constraint-performance-drop","ev-p004-failure-core","ev-p004-macro-constraint-failure","ev-p050-operator-core","ev-p046-operator-core"]
-->
# Research Map

## Observed Failure and boundary

- [AUTHOR_FACT] P051 的 LLM 生成代码在 block picking 任务遗漏 all-different 约束，计划重复选择同一 block。[[evidence:ev-p051-omitted-constraint-failure]]
- [AUTHOR_FACT] P051 明确把 solver 保证限定为"对已编码且可满足的约束系统求解"。[[evidence:ev-p051-solver-guarantee-boundary]]
- [AUTHOR_FACT] P052 的 Definer 会遗漏隐式守恒约束（roastery 加工量不得超过收货量等），使 solver 在错误模型上给出更优目标值。[[evidence:ev-p052-implicit-constraint-failure]]
- [AUTHOR_FACT] P052 的同模型自评修复会误诊失败原因并引入不终止循环。[[evidence:ev-p052-self-diagnosis-nontermination]]
- [AUTHOR_FACT] P054 报告更自然的描述令 formalizer 遗漏 `clear` 等隐式 predicate，产生 unsolvable PDDL 或错误计划。[[evidence:ev-p054-natural-language-implicit-predicate-failure]]
- [AUTHOR_FACT] P055 报告一行式约束普遍显著削弱 planning 与 formalization 表现。[[evidence:ev-p055-constraint-performance-drop]]
- [AUTHOR_FACT] P055 在 Limitations 原文承认 plan correctness 指标可产生假阳性（"the plan may happen to be correct, but the generated code does not actually correctly describe the environment that satisfies the constraint"），声称"to the best of our knowledge there is no feasible alternative"，并只在跨数据集合并抽样的 20 个样本上检查、未发现假阳性、据此称假阳性率可忽略。[[evidence:ev-p055-plan-correctness-false-positive-boundary]]
- [AUTHOR_FACT] P004 报告 agent 常满足部分约束却在 macro 层面整体失败，微观分数高不等于宏观合规。[[evidence:ev-p004-failure-core]] [[evidence:ev-p004-macro-constraint-failure]]
- [CODEX_SYNTHESIS] 以上事实共同界定一个认证不对称：形式化管线的验收信号（solver SAT/OPTIMAL + 返回解通过检查）作用在**解**上，而故障发生在**模型**上。模型漏掉约束 c 时解仍可能碰巧满足 c，此时解级认证输出 PASS 且不产生任何错误信号——静默漏约束（silent under-constraint masked by solution-level success）。
- [CODEX_HYPOTHESIS] H1（发生率）：在多约束、自由形式的形式化任务上，静默漏约束的自然发生率显著大于零，且随 scaffold 强度上升而下降。P055 的"20 样本零假阳性"与其简化域（BlocksWorld/CoinCollector 一行式约束）和小样本有关，不外推到多约束现实载体。
- [CODEX_HYPOTHESIS] H2（机制）：掩盖概率由约束的 binding 频率（slack）决定——可行集内碰巧合规的解占比越高，漏编码越难被解级检查暴露；收紧实例参数应使同一故障由掩盖转为暴露。
- [CODEX_HYPOTHESIS] H3（互补）：错误触发修复信号（UNSAT core、返回解检查失败、运行时异常）按构造对被掩盖故障覆盖率≈0。

## Intervention stage

失败发生在形式化管线的**认证/验收计算**：solver 求解之后、结果被接受/报告/交付之前。该步当前读取的信息是返回解 s 与（评测场景下的）解级参考检查器输出；它不读取生成模型 M 的可行集结构。干预后的认证计算额外读取 M 本身（可执行、可搜索）与逐约束参考条件，输出逐约束 enforcement 判定与实例级掩盖质量。

## Use Thesis, Value Bridge and Mechanism Demand

绑定 problem_v001.md（SHA cae9ef65de842f69c839365a58c8ef88ec78ac6dd5d509de0a919e7ba9c9400d）已固定的消费者（solver-backed 形式化系统的建设者与 benchmark 维护者）、决策接口（认证/验收环节的逐约束 enforcement 判定）、proxy 边界与 Mechanism Demand（含 carrier-independent statement 与另外两类 carrier 预测）。本版 Research Map 在任何 Promotion carrier outcome 暴露前形成：截至本文写入，本 Run 未下载、未读取任何实验数据集实例或 outcome。

## Operator shortlist and source recheck

查询由 Problem 的 Mechanism Demand 生成（认证计算、反例搜索、覆盖审计），不含任何 Candidate 自创名称。三次正式查询与内部车道查询已于 2026-07-26 执行（failure/operator/paper 各 20 条上限；内部车道 0 命中，属正常）。

1. **P050 Active Counterexample-Seeking Verifier**（test-time search & verification 簇）[[evidence:ev-p050-operator-core]]
   - Baseline → Changed Computation：固定/随机测试弱区分候选程序 → 主动搜索最大化行为分歧的判别性输入。
   - 结构映射：候选程序集合 ↦ 生成的约束模型 M 与参考条件集合；行为分歧 ↦ "M 接受但参考条件拒绝"的解；判别性输入搜索 ↦ 在 F(M) 内对每个参考条件做定向对抗搜索（如对成本类条件求极值解）。
   - 信息时点：生成后、接受前——与本簇失败的干预时点完全一致。
   - 迁移前提与失败边界（原 Evidence 回核）：P050 卡明示"divergence proves non-equivalence but not correctness"。迁移后同构限制：探针找到违反解 ⇒ 该条件未被 enforce（由参考检查器认证，soundness 成立）；探针未找到 ≠ 已证明 enforce（incompleteness 如实保留为指标定义的一部分）。
2. **P051/P052 Decomposed Solver-Backed Formal Planning**（planning 簇，被审计的对象范式）[[evidence:ev-p051-formalization-pipeline]] [[evidence:ev-p052-decomposed-formalization]] [[evidence:ev-p052-direct-code-smt-baselines]]
   - 该 Operator 定义了被试计算（NL→SMT 编码→solver）与其基线族（Direct / Code）；其五轮自评边界与自诊断失败 [[evidence:ev-p052-self-diagnosis-nontermination]] 说明"同模型自查"不是可靠的 enforcement 信号，构成 K1 的 comparator 臂之一。
3. **P046 SMT Pre-Execution Policy Guard**（tool 簇）[[evidence:ev-p046-operator-core]]
   - 需求侧证据：其卡片自述"guarantees stop at the reviewed encoding; automatic formalization can be incomplete or underconstrained"——形式 guard 的部署者正是 enforcement 审计的潜在消费者。不借用其计算。
4. **P068 Evidence Audit Before Benchmark Scoring**（evaluation 簇）
   - 借用其排序结构（先审计证据、后计分），不借用其具体计算；支持"审计置于报告之前"的接口设计。

**谱系链定位**：本 Mechanism Demand 落在 CORPUS_REPORT §5 的 Planning & reasoning 链（ReAct P001 → ToT/LATS 搜索 → TravelPlanner P004 约束载体 → LLMCompiler/NaviAgent 分解 → P051/P052 solver-backed formalization → P054/P055 formalizer 极限/约束压力 → P053 generator 表示）。链上每步改变的计算依次是：推理-行动交织 → 候选状态搜索 → 约束化评测 → 任务分解 → 形式化+solver 求解 → 形式化的压力测试 → 中间表示压缩。**沿链下一步最自然的 changed computation**：链在生成侧（更好的 formalizer/表示）和修复侧（错误触发环）持续推进，但**认证侧计算自 P004 的解级检查器以来从未改变**；自然下一步是把认证从"检查返回解"升级为"探查模型可行集"。**它为什么还没被做**：P055 明文认为不存在可行替代（认知空白，非 Failure Card 排除）；2026 年 OR 载体的探针工作刚出现、未触及 agent 规划基准；修复侧工作全部以错误信号为触发，静默情形对它们不可见。检查全部 51 张 Failure Card，无任何卡排除该方向。

**跨机制簇探针**：本簇 Failure（解级认证无法区分 enforce 与碰巧合规）与 verification 簇 P050 Operator（把执行预算花在分歧可能藏身处的主动反例搜索）共享中间计算性质——**验收决策所依赖的证据由被动检查交付物改为主动搜索反例**。该共享性质经原始来源复核成立（P050 Abstract 原文与 P051 §3.3.3 原文），P050 的 changed computation 构成本簇 Failure 的候选干预。命中已按 §4 规约用于 kernel 生成（K1 的通道之一）。

## Competing method kernels

### K1（主 kernel）：逐约束 enforcement 探针与掩盖率分解

- **目标 Failure**：failure-solver-guarantee-stops-at-formalization + failure-constraint-shift-breaks-formalization（解级成功掩盖静默漏约束）。
- **Intervention point**：认证/验收计算（solver 之后、接受/报告之前）。
- **Changed computation**：对每个参考条件 c_i，在生成模型 M 的可行集内做定向对抗搜索（solver 调用，无 LLM）：找到被 M 接受但违反 c_i 的解 ⇒ c_i 未被 enforce。输出逐约束 enforcement 判定，与解级 PASS 交叉得到掩盖质量分解：enforced / masked（未 enforce ∧ 解级 PASS）/ caught（未 enforce ∧ 解级 FAIL 或错误信号）。
- **借用 Operator**：P050 主动反例搜索（认证侧计算）；P051/P052 定义被试范式与 comparator（Direct self-check、返回解检查）；P068 审计先于计分的接口顺序。
- **使用接口/Value Bridge**：benchmark 评测协议与 CI 验收门的逐约束 enforcement 报告；见 problem_v001。
- **Closest fair composition**：(a) 解级参考检查器本身（现行认证，被审计对象）；(b) P052 式同模型 self-assess（"你是否编码了全部约束？"）在同实例上的判定；(c) 错误信号集合（UNSAT/异常/解级 FAIL）作为故障检测器。三者与探针在同一批冻结形式化产物上比较检测覆盖，无需额外 LLM 预算差异（探针零 LLM 调用）。
- **主要未经验证的科学跃迁**：仅一条——在多约束 agent 规划载体上，自然发生的 enforcement 故障中存在非零质量被解级成功掩盖，且掩盖结构由 slack 主导（H1+H2 合为对"掩盖现象及其机制结构"的单一断言；H3 是按构造的对照测量，不含新跃迁）。
- **Predicted signature**：problem_v001 的 S1–S4。
- **最便宜直接否证条件**：对 15–20 个自由形式形式化产物做探针，若解级 PASS 实例中 enforcement 故障率≈0（掩盖质量为空），kernel 死亡；若故障全部同时触发错误信号（无静默质量），kernel 同样死亡。
- **Fresh Promotion carrier**：存在——多约束规划基准验证集按确定性哈希规则预承诺分桶（W/D/C 物理分离），Workbench 只触碰 W 桶；D 桶对 Candidate 形成保持 fresh。
- **Carrier-independent statement**：在任何"NL 约束规格→可执行约束模型→solver→解级认证"的管线中，逐条件 enforcement 可由模型可行集内的定向对抗搜索度量；静默漏约束质量 = 未 enforce 且解级通过的条件质量。不含任何 benchmark/dataset/协议名称。
- **生成通道**：占用者局限分析（P055 Limitations 原文 p.10："no feasible alternative" + 20 样本边界；OR 载体探针工作未触及 agent 规划基准）+ 跨簇探针（P050 → 认证侧迁移）+ facet 级重组（P050 的 Before/after computation 应用于 P051/P055 的认证环节 Intervention target）。属通道 4/5 混合；通道 5 成分（占用者原文论断的直接反驳）降低碰撞基础率。
- **廉价新颖性探针结论**：中性检索式与执行日（2026-07-26）——"testing LLM generated formal specifications unit tests counterexample validation omitted constraints"（命中：Alloy 载体 2510.23350、Verus-SpecGym 2605.26457）；"LLM optimization modeling formalization validation solver probe enforcement missing constraint silent failure audit"（命中：ReLoop 2602.15983、Constraint Injection 2606.04816、OptArgus 2605.11738——全部 OR/程序验证载体）；"TravelPlanner SMT formalization audit constraint enforcement verification faithfulness solver success masks omission"（未命中任何 enforcement 审计工作）。中性结论：探针式规格验证计算在相邻载体存在，agent 规划载体上的掩盖率量化、slack 机制结构与修复盲区分解未检得先行。"暂未找到"不等于已证明新颖，完整最近先行检索在冻结前另行执行。

### K2（替代 kernel）：探针触发的静默修复环

- **目标 Failure**：同上；**Intervention point**：修复触发计算（不同于 K1 的认证计算）；**决策变量**：修复动作（把探针发现的未 enforce 条件作为合成错误信号送入重形式化环）vs K1 的接受/报告。
- **Changed computation**：错误触发修复环的触发集从{UNSAT, 异常, 解级 FAIL}扩为{…, 探针违例}。
- **借用 Operator**：K1 探针 + P051/P052 修复环结构。
- **主要科学跃迁**：探针信号引导的定向重形式化在匹配预算下优于非定向重试——这是独立于 K1 跃迁的第二条未验证跃迁，且以 K1 成立为前提。
- **最便宜否证**：若 K1 掩盖质量为零，K2 无对象。
- **Carrier-independent statement**：在同类管线中，把"未 enforce 条件"作为合成错误信号可使错误触发修复环覆盖静默故障。
- **生成通道**：多来源组合（K1 探针贡献 intervention target 与信号，P051/P052 贡献修复环 scaffold；未经验证跃迁为修复有效性一条）。
- **廉价新颖性探针结论**：修复环节点已被占用（P051 unsat-core、2606.29700 planner-in-the-loop、2606.00981），差异仅在触发信号来源；碰撞基础率高。

## Natural-language disposition

- **K1：keep**。理由：因果杠杆直接作用于链上从未改变的认证计算；迁移前提经 P050 原 Evidence 回核成立且迁移后 soundness 有参考检查器背书；使用价值绑定已固定的消费者决策（报告协议与验收门）；fresh Promotion 可行（预承诺分桶）；可证伪性极强（15–20 实例探针即可杀死）；证据基础横跨四篇独立论文的作者事实。
- **K1 Workbench 决定性探针实际结果**（workbench_v001/falsifier_report.md，2026-07-26，W 桶 22 实例，探针只杀伤或授权、不作晋级证据）：否证条件未触发——16 个形式化成功实例中 14 个解级 PASS，其中 4 个（≈29%）存在证书背书的未 enforce 类别（cuisine×3、room_type×1，witness 均经参考检查器复核）；另见 caught 案例（house_rule）与 5 例 default-UNSAT 过约束（错误信号可见）。掩盖质量显著非零，K1 获授权进入全量冻结实现。典型案例：idx064 把"enjoy American and Indian cuisines"编码为逐餐厅成员归属而非菜系覆盖，模型允许 American 零覆盖，默认解碰巧双覆盖。
- **K2：kill（本版本）**。理由：(a) 依赖 K1 尚未验证的跃迁，若与 K1 同版本推进将同时押注两条独立新机制，违反单跃迁约束；(b) 修复环节点被 2026 年多篇工作密集占用，差异仅剩触发信号，碰撞基础率高；(c) K1 成立后 K2 是接收方扩大路线图上的自然下一步，作为 scale-up 步骤交付比作为本版本主张更诚实。排除依据：CRL 单跃迁纪律 + 新颖性探针命中（修复环占用）。
- 未制造陪跑路线。K1 之外的其他方向排除理由：生成侧改进（更强 formalizer/表示）被 P053/P054/P055 谱系与 2606 系列占用；case 生成式验证被 2510.23350（Alloy）占用且重新引入 LLM 生成测试的保真风险；训练/微调方向被 Problem 硬排除；执行恢复方向被 CORPUS_SCOPE 排除。
- 选择理由与载体便利无关的说明：K1 的选择先于任何数据下载（本文写入时无任何实例被读取）；载体（带逐约束参考检查器的多约束规划基准）由 Mechanism Demand 的"审计场景下参考条件可得"约束推出，而非因数据现成。

## Family Viability

首版本，无既往失败需归因。核心机制签名（掩盖质量非零且 slack 结构化）尚未在任何数据上观察——这正是 Workbench 决定性探针与 Promotion Development 的对象。当前判断：family 可行，进入 K1 的 Workbench 探针；若探针显示掩盖质量≈0，按 K1 否证条件关闭本 Problem（Problem 级 kill 是正常产出），不得换指标续命。

## Candidate Promotion Audit

### Promotion Development 前（2026-07-26，D 桶未打开时写入）

- **Use Thesis、Decision Interface 与 Value Bridge**：见 problem_v001（SHA cae9ef65…）与 candidate_v001（SHA 42e017c7…）——消费者为 solver-backed 形式化系统建设者与 benchmark 维护者；接口为验收/报告环节的逐约束 enforcement 判定；价值桥为认证输出对约束忠实度的校准。
- **Target Failure 直接表现在哪个结果变量上**：解级认证输出（PASS/FAIL）与真实 enforcement 状态的错配——具体为"PASS 且 ≥1 适用约束未被编码"的掩盖格质量。
- **Candidate 实际改变哪个决策变量**：形式化产物的接受/报告决策（从解级 PASS 即接受，变为逐约束 enforcement 剖面后接受/标记）。
- **为什么该变化可能影响 Target Failure 而不只是改善 validity/execution/格式**：探针直接测量 Target Failure 的构成量（掩盖质量），其 witness 由参考检查器复核为语义违规——不经过任何 validity/格式代理。
- **主要未经验证的科学跃迁及决定性前置反证**：掩盖现象及其 slack 结构在 fresh 数据上稳定出现；Workbench 反证已执行（W 桶 22 实例，4/14 掩盖，反证未杀死 kernel）。
- **Promotion 数据为何相对 Candidate 形成保持 fresh**：W/D/C 在读取任何内容前由确定性哈希规则物理分桶（manifest SHA dfeaf9fe…）；候选形成只消费了 W 桶 outcome 与 D 桶机械元数据计数；D 桶文件在实验启动前未被任何主流程代码打开。
- **最接近的已有方法或组件组合**：外部无可运行竞争分解（nearest_prior_v001 检索结论）；内部臂矩阵 A1–A4 分别代理现行认证、错误触发修复家族、P052 自评家族与 ReLoop 行为测试家族。

### Promotion Development 完成后、冻结 Review Packet 前（2026-07-26，dev_001 之后）

- **Development baseline 是否真实出现 Target Failure、条件**：出现。F1 自由形式条件下 3 例证书背书 enforcement 故障（cuisine 量词结构误译 ×1、house_rule 未编码 ×2），其中 1 例被解级认证掩盖（idx120，λ=1.0）。条件边界：只在自由形式 scaffold 下出现；F2 一行清单 scaffold 本批 0 故障；出现的故障形态与 Workbench（W 桶）观察同型（成员归属 vs 覆盖的量词翻转）。
- **隔离单位与可支持 Claim**：instance-disjoint（承诺哈希分桶）。支持：同分布 fresh 实例上的掩盖现象与 luck 机制 Claim。不支持：跨模型、跨载体、跨 scaffold 泛化；掩盖率数值外推。
- **合理聚类单位**：实例（同实例多类别相关）；主指标 M2 在实例级。
- **是否改善最终结果变量而非代理**：本 Candidate 是测量 harness——它的"结果变量"就是认证输出与真实 enforcement 的错配（掩盖质量），由证书直接测得，无代理链。
- **相对公平 comparator，结果来自唯一 delta 还是 bundle**：探针 delta 的归因由设计保证（同批冻结 F1 产物全臂共享）。臂间事实：A3 同模型自查 0/3 全漏（0/91 虚警）；A4 行为测试 3/3 覆盖（0/68 虚警）——A4 在本批与探针证书一致，探针的差异化在证书性（SAT witness + 检查器复核的可证明性）与已预先声明的 A4 结构性弱点（参数硬编码不可测、可行性纠缠），后者在 n=3 上未被激发；此限定如实进入 Claim 边界。F2/A3 结论保持 bundle 级。
- **为什么值得/不值得作为种子交付并移交 Confirmation**：值得——现象在 fresh 数据以证书级证据出现且机制变量（λ）方向正确；harness 全链路可复现（单段 capture、raw 可重算）；同型故障跨桶复现提示稳定故障形态；self-check 的证书级失败是独立有用的负向结果。不利面如实交付：n_masked=1、掩盖率 CI 宽 [0.85%, 22.7%]、W→D 衰减（29%→4.8%）表明质量对实例构成敏感；预注册 C-GATE-1 按 D 点估计计算的通过概率约 8%（严酷测试，预期难过）。

## Seed Readiness Audit

- **changed computation 能否不提 benchmark/dataset/协议名称完整陈述**：能——candidate_v001 的 Carrier-independent statement（可行集内逐条件对抗探针 + 三格掩盖分解），另两类 carrier 预测（NL→数据库查询、NL→调度/资源配置模型）已在 problem_v001 写明。
- **预注册机制签名是否真实出现、条件**：SIG-1 出现（Wilson CI 下界 0.85% > 0）；SIG-2 primary 出现（masked λ 中位数 = 1.0 > 0.5；n_masked=1 如实声明）；SIG-2 secondary luck 排序出现（1.0 > 0.0）；密度排序与预注册方向相反——域级密度是坏代理，可行集 luck 才是机制变量（如实报告，不改指标）。未出现条件：F2 清单 scaffold 下故障率为 0（现象被最便宜的 scaffold 关闭——这既是边界也是可交付的实践结论）。
- **closest-composition comparator 是否真实运行、delta 归因**：内部臂矩阵（A1/A2/A3/A4）在同批冻结 F1 产物上真实运行；探针 delta 由设计归因；外部无可运行竞争分解（absence-of-evidence，2026-07-26 检索）。
- **最强组件级/组合级/完整 pipeline 近邻与剩余差异**：组件级 = solver 反例查询（标准）与 vacuity/coverage 经典线；组合级 = Zhong-Yu-Klein 2020（SQL 测试套件）、ReLoop（OR 扰动验证）、Constraint Injection（VRP 训练探针）、2510.23350（Alloy LLM 测试）；完整 pipeline = P051/P052/planner-in-the-loop。剩余真实差异：认证时点的逐约束证书级 enforcement 剖面 + 掩盖三格分解 + 可行集 luck 机制测量 + agent 规划载体，且两个最近邻自证该空缺（ReLoop 定性承认、Constraint Injection 列为 open problem）。
- **保留 Confirmation 载体、未触碰证明**：C 桶（33 行）全部 SC3 实例；承诺清单（manifest SHA dfeaf9fe…）+ 物理分桶 + 主流程代码只引用 W/D 路径（冻结 config 与两个 capture 的 inputs 哈希可机械核验）+ C 文件自承诺起无任何读取（含元数据）。接收方可重跑 commit_split.py 独立重算全部 180 行分配。
- **接收方扩大最可能在哪一步碎掉、最便宜验证顺序**：(1) 更强模型故障率趋零 → 掩盖质量空置（最大风险；最便宜验证 = 换 model 参数重跑 dev 管线，<1 USD）；(2) C 桶功效不足（C-GATE-1 通过概率按 D 点估计约 8%，严酷）；(3) 扩大到多城/全槽位外的 schema 时 harness 检查器需重写（工程量数天）；(4) A4 行为测试在更大样本上可能与探针等效（则种子价值收窄为证书化与量化协议本身）。最便宜顺序：先 (1) 再 C 桶 (2) 再全验证集 180 实例复算 (3)。
- **综合：为什么值得作为种子交付**：一条被证书证明存在、机制变量方向正确、全链路可复现、被两个最近邻自证为空缺的测量分解，附带两个立即可用的实践结论（一行清单 scaffold 关闭静默通道；同模型自查在证书对照下完全不可靠）。交付判据是"值得投入扩大"而非"已经成立"；不利证据（薄 n、衰减、严酷 C 门）全部如实随附。

## Unique narrow Gap

在带逐约束参考检查器的多约束 agent 规划载体上，量化"解级成功掩盖的静默漏约束"：其自然发生率（按 scaffold 强度分层）、slack 机制结构、以及错误触发修复信号对其的覆盖盲区。仍缺的 computation 是认证侧的逐约束可行集对抗探针及其掩盖质量分解——生成侧与修复侧的既有工作都不计算它。
