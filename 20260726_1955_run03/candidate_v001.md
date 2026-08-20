<!-- crl-v3-evidence-ids
["ev-p051-omitted-constraint-failure","ev-p051-solver-guarantee-boundary","ev-p051-formalization-pipeline","ev-p052-implicit-constraint-failure","ev-p052-self-diagnosis-nontermination","ev-p052-direct-code-smt-baselines","ev-p052-decomposed-formalization","ev-p054-natural-language-implicit-predicate-failure","ev-p055-plan-correctness-false-positive-boundary","ev-p055-constraint-performance-drop","ev-p004-failure-core","ev-p004-macro-constraint-failure","ev-p050-operator-core","ev-p046-operator-core"]
-->
# Candidate Implement

## One-sentence method kernel

对 LLM 生成的可执行约束模型，在其可行集内对每个参考条件做 solver 级对抗探针，产出逐约束 enforcement 证书，并量化被"解级认证 + 错误信号"联合掩盖的静默漏约束质量及其松紧度（slack）结构。

## Carrier-independent statement

在任何"自然语言约束规格 → LLM 生成可执行约束模型 → solver 求解 → 只检查返回解的认证 → 只由显式错误信号触发修复"的管线中，每个参考条件的 enforcement 可以由模型可行集内的定向对抗搜索度量：找到被模型接受但违反该条件的解即为该条件未被编码的证书。全部故障质量由此分解为三个格子——错误信号可见（UNSAT/异常）、解级检查捕获、以及对上述两类信号都不可见的静默掩盖格；静默格的质量与其随条件松紧度的结构是经验量，其对错误触发修复的不可见性是构造性质。本陈述不含任何 benchmark、dataset、协议或榜单名称。

**生成通道**：占用者局限分析（P055 Limitations 原文 p.10 "no feasible alternative" 与 20 样本边界；Constraint Injection 2606.04816 Limitations 明文将"更细粒度解耦约束违规剖面指标"列为 open problem；ReLoop 2602.15983 定性承认 "solver feedback catches syntax errors, not missing constraints"）+ 跨簇探针（P050 主动反例搜索 → 认证计算迁移）+ facet 级重组（P050 的 Before/after computation 用于 P051/P055 的认证环节 intervention target）。

## Use Thesis, decision interface and Value Bridge

绑定 problem_v001.md（SHA cae9ef65de842f69c839365a58c8ef88ec78ac6dd5d509de0a919e7ba9c9400d）。消费者：solver-backed LLM 形式化规划系统的建设者与受约束规划 benchmark 维护者。决策接口：形式化产物的验收/报告环节新增逐约束 enforcement 判定与掩盖率报告；改变的决策——是否在 pass rate 之外报告 enforcement、是否把探针作为验收门与静默故障修复触发器、如何按 enforcement 取舍 scaffold 强度。Value Bridge 与 proxy 边界见 problem_v001；本版实验只支持带逐约束参考检查器的载体族上的量化结论。

## Failure/Evidence → Operator → Gap lineage

- Failure：P051 all-different 遗漏 [[evidence:ev-p051-omitted-constraint-failure]]、P052 隐式守恒遗漏 [[evidence:ev-p052-implicit-constraint-failure]]、P054 隐式 predicate 遗漏 [[evidence:ev-p054-natural-language-implicit-predicate-failure]]、P055 约束普遍削弱形式化 [[evidence:ev-p055-constraint-performance-drop]] 且认证指标假阳性通道由作者自认、无可行替代、仅 20 样本核查 [[evidence:ev-p055-plan-correctness-false-positive-boundary]]；P004 建立多约束载体与 macro 失败 [[evidence:ev-p004-failure-core]] [[evidence:ev-p004-macro-constraint-failure]]；P051 的 solver 保证边界 [[evidence:ev-p051-solver-guarantee-boundary]]。
- Operator：P050 主动反例搜索（认证侧结构借用）[[evidence:ev-p050-operator-core]]；P051/P052 定义被审计范式与其自评/修复边界 [[evidence:ev-p051-formalization-pipeline]] [[evidence:ev-p052-decomposed-formalization]] [[evidence:ev-p052-self-diagnosis-nontermination]] [[evidence:ev-p052-direct-code-smt-baselines]]；P046 形式 guard 的 under-constrained 自认（需求侧）[[evidence:ev-p046-operator-core]]。
- Gap：认证计算自解级检查器确立以来从未升级；静默 SAT 掩盖格无人量化（详见 research_map_v001 谱系链分析）。

## Baseline computation

被审计基线（现行认证计算）：输入 = 返回解 s 与解级参考检查器；执行时点 = solver 之后、接受/报告之前；输出 = PASS/FAIL + 错误信号（UNSAT core、运行时异常）。信息访问：不读取生成模型 M 的可行集结构。

## Changed computation

认证计算扩展为：对每个适用参考条件 c，构造 harness 侧 z3 断言"c 被违反"（从实例候选表机械生成，无 LLM），与 M 的全部断言合取后 SAT 查询。SAT ⇒ c 未被 enforce（witness 解经独立 stdlib 参考检查器复核为违规，构成证书）；UNSAT ⇒ c 在 M 中被 enforce（以 harness 编码保真为条件）。与默认解的解级判定交叉，得到逐约束三格分解（error-signaled / caught / masked）。borrowed components：z3 SAT 查询（标准）、参考检查器语义（载体既有）、P050 的搜索结构；**唯一 proposed delta**：认证时点上的逐约束可行集对抗探针及其掩盖质量分解（含 slack 结构度量）。

## Closest-composition difference

外部无可运行竞争分解（nearest-prior 检索结论，2026-07-26，absence-of-evidence 级）。三个最近邻及其与本 delta 的差异：Zhong-Yu-Klein 2020（NL→SQL 蒸馏测试套件：需 gold query、无逐约束剖面、无 slack/修复盲区）；ReLoop 2602.15983（OR 载体 feasibility–correctness gap 量化：检测为同 LLM 抽取 + 扰动敏感性启发式，无证书级剖面、无 slack 机制、修复盲区仅定性）；Constraint Injection 2606.04816（训练方法，探针作训练信号，评测仍 Pass@1，细粒度剖面自认 open problem）。Promotion Development 以内部臂矩阵落实可运行 closest composition：A2（错误信号 = 错误触发修复家族触发面）、A3（同模型 self-check = P052 自评家族，给予类别清单的有利变体）、A4（选项消融/参数缩放行为测试 = ReLoop-CPT 的载体内改编）在同一批冻结形式化产物上与 A5（探针）实测比较。信息访问与成本差异：A3 每实例一次额外同模型调用；A2/A4/A5 零 LLM 调用；全部臂读取相同冻结产物。

## Minimal Claim Contract

当前实验能直接否证的窄 Claim：

1. 在 TP-SC3 载体（TravelPlanner 验证集单城 3 日全槽位变体）+ deepseek-chat 自由形式单次形式化条件下，解级认证通过的实例中存在非零比例（Wilson 95% CI 下界 > 0 需成立）携带证书背书的未 enforce 适用约束（掩盖率 M2）。
2. 掩盖呈 slack 结构：被掩盖故障的违规选项密度低于被捕获故障（方向性），且对被掩盖的预算类故障，反事实收紧预算使同一故障由掩盖翻转为暴露。
3. 检测器比较：错误信号臂对掩盖格覆盖率为 0（构造性质，如实标注）；类别清单辅助的同模型 self-check 臂与行为测试臂对证书背书故障的覆盖率与虚警率为经验量，与探针臂并列报告。

**禁止扩张**：不主张跨形式化器/模型/载体的掩盖率数值外推；不主张对官方 TravelPlanner 排行榜数字或 P051 发表结果的直接重估；不主张探针触发修复的有效性（K2，未测试）；不主张无参考检查器场景的可用性；不主张 scaffold 梯度的因果机制（F2 清单臂只是单点对照）；本版全部结论未经 untouched 数据检验。

## Causal chain and one major scientific risk

失败现象（形式化遗漏/误译，多篇作者事实）→ 干预计算（认证时点逐约束可行集探针）→ 预期中间签名（探针产出证书背书的未 enforce 判定，witness 经检查器复核；掩盖格非空且 slack 结构化）→ 系统决策变化（验收/报告决策由解级 PASS 改为逐约束 enforcement 剖面）→ 最终结果变量（认证输出对真实约束忠实度的校准；掩盖质量可见化）→ 使用价值（benchmark 报告协议与验收门升级）。逐箭头证据状态：现象箭头有四篇论文作者事实与 W 桶 Workbench 观察；探针可行性箭头已在 Workbench 全链路验证（含证书复核）；**主要未经验证的科学跃迁（唯一）**：掩盖现象及其 slack 结构在 fresh 数据上以稳定、可预注册的形态出现（而非 W 桶偶然）。其余箭头（决策变化、使用价值）是接口性主张，不依赖新机制。

## Workbench decisive falsifier

已执行（workbench_v001/falsifier_report.md，W 桶 22 实例）：否证条件未触发——14 个认证 PASS 中 4 个（≈29%）证书背书掩盖（cuisine×3、room_type×1）；另有 caught（house_rule）与 5 例 default-UNSAT 过约束。探针仅授权继续，不作晋级证据。

## Implement contract

冻结文件（implementation_v001/，逐文件 SHA 见 Experiment Artifacts）：
- `tp_lib.py`：实例规范化 + 参考检查器（wb_lib.py 的冻结演进版）。
- `tp_prompt.py`：F1 自由形式与 F2 类别清单两个冻结提示模板 + A3 self-check 模板。
- `tp_api.py`：DeepSeek 调用（httpx、温度 0、重试退避、逐行 raw jsonl、异常脱敏）。
- `tp_solve_probe.py`：例外环境载荷——域构建、生成代码执行、默认解、A5 探针、A4 行为测试。
- `run_promotion.py`：D 桶 SC3 编排器（逐实例 F1→F2→A3 交错、逐行 checkpoint、断点续跑、状态汇总）。
- `analysis.py`：从 raw 独立重算全部指标。
- `config.json`：全部路径、臂开关、N、超时、模型名。
核心 argv：capture runner 以绝对路径执行 `run_promotion.py --config <frozen config.json>`（cwd = implementation_v001）；DeepSeek key 仅经进程环境变量。solver 侧解释器：run 根例外环境 `.venv_z3\python.exe`（python 3.11.15 + z3-solver==4.15.4；创建依据与命令记录于 experiment plan）。

## Neutral comparators

- CMP-A1（解级认证）：真实身份 = 参考检查器对默认解的判定（被审计的现行认证信号）。代码 = tp_lib.py 检查器；成本 0 LLM 调用。
- CMP-A2（错误信号集合）：真实身份 = UNSAT / 生成代码执行异常 / 超时（错误触发修复家族的触发面）。代码 = tp_solve_probe.py 状态输出；成本 0。
- CMP-A3（同模型 self-check，类别清单辅助）：真实身份 = P052 自评家族的有利变体；deepseek-chat 对 (query, F1 代码) 输出逐类别 enforced 判定 JSON。每实例 1 次调用。
- CMP-A4（行为测试）：真实身份 = ReLoop-CPT 的载体内改编（合规选项全删重解 + 预算极端缩放）；机械执行，成本 0 LLM 调用。若该改编被认为不忠实于 ReLoop 原法，结论限缩为"该类行为测试的一个实例"。
- CMP-F2（类别清单 scaffold 形式化）：真实身份 = F1 提示 + 一段类别枚举；用于单点对照清单对故障发生率的影响。每实例 1 次调用。
（无 closest/strongest 排名标签；排序与 collision verdict 只在私有 nearest_prior_v001.md。）

## Experiment contract

- 总体：D 桶全部 SC3 实例（预期 28：easy 10 / medium 9 / hard 9，机械元数据计数，无内容读取）。
- 主要指标：M1 逐类别 enforcement 故障率（F1，证书背书）；**M2 掩盖率 = 认证 PASS 实例中含 ≥1 证书背书未 enforce 适用类别的比例（主指标，Wilson 95% CI）**；M4 检测器比较（A2/A3/A4 对证书背书故障的覆盖率与对 enforce 类别的虚警率）；M5 slack 结构（(a) masked vs caught 的违规选项密度比较；(b) 掩盖预算故障的反事实收紧翻转曲线；(c) 探索性：blocking-clause 采样估计掩盖故障的可行集违规质量）。
- mechanism signature（预注册，两者须现）：SIG-1 M2 的 Wilson 95% CI 下界 > 0；SIG-2 slack 方向性——M5(a) masked 中位违规选项密度 < caught，或 M5(b) 全部被掩盖预算故障在收紧至默认解成本以下时翻转为暴露（至少一条成立即计为出现，两条都报告）。
- no-method 对照：A1 本身即"无探针"的现行认证输出。
- delta ablation：探针不叠加任何生成侧改动，F1 产物在全部检测臂间共享——delta 可归因性由设计保证。
- 预算与公平：F1/F2/A3 逐实例交错（模型漂移控制）；温度 0；逐行记录 provider 返回 model 字段；A2/A4/A5 零 LLM 成本。预计 API 用量 ≈ 28×3 次调用 ≈ 12–20 万 tokens 量级（按实际披露）。
- Artifacts：冻结 implement/config/input；capture `experiment_v001/captures/dev_001/`（execution.json、stdout.bin、stderr.bin）；声明输出 = results jsonl（逐实例逐臂）+ raw API jsonl + aggregate JSON。

## Data roles and freshness

- WORKBENCH：W 桶（67 行）——22 个 SC3 实例的 outcome 已用于 kernel 决定性探针与 harness 设计；对本 Candidate 永久 Workbench。
- PROMOTION_DEVELOPMENT：D 桶（80 行）中的 SC3 子集（预期 28）——桶文件自承诺时点起未被任何主流程代码打开；候选形成只读了 W 桶与 D 桶的机械元数据计数（level/days/cities 列直方图）。提示模板、接口合同、探针设计全部在 W 桶上定型，故 D outcome 相对 Candidate 形成保持 fresh。
- CONFIRMATION：C 桶（33 行）——自承诺时点完全未打开（含元数据）；由确定性规则物理分离，接收方可重算验证。

## Model coverage

单模型（deepseek-chat，响应 model 字段逐行记录）。为什么单模型不是当前必要反证条件：本 Claim 的对象是**认证计算的掩盖格**，其存在性只需一个真实形式化器展示；掩盖率数值的跨模型外推已在 Minimal Claim Contract 中禁止。对接收方的含义：跨模型（尤其更强模型）验证是扩大路线图第一优先风险——若强模型故障率趋零，掩盖格空置，种子的实用价值收窄为审计工具而非普遍现象（该风险如实交付）。

## Reserved confirmation isolation and analysis unit

- 保留载体：C 桶全部 SC3 实例（按与 D 相同的确定性规范化定义总体；主 Codex 未打开 C 文件，预期规模 ≈12，实际由接收方执行时确定）。
- 隔离单位：实例级（instance-disjoint）；W/D/C 由承诺哈希规则物理分桶。同一实例内的多类别判定共享生成过程，聚类单位 = 实例；主指标 M2 在实例级计算。
- 该隔离支持：同分布 fresh 实例上的掩盖现象与 slack 结构 Claim；不支持：跨载体/跨模型/跨 scaffold 泛化。

## Cost and bundle attribution

模型：deepseek-chat；调用：≈28×3（F1/F2/A3）+ 重试；Token：预计 12–20 万（实际披露）；工具权限：HTTPS API + 本地 z3 例外环境 + 本地文件；固定工程计算：z3 SAT 查询每实例每类别 O(1) 次 + A4 重解 + 采样（本地 CPU 秒级）；wall time 预计 1–2 小时。归因边界：探针臂 delta 为唯一方法学主张；F2 与 A3 的结论是 bundle 内对照观察，不得归因为独立方法贡献。

## Risks and kill conditions

- D 桶掩盖率 CI 下界不 > 0 → SIG-1 失败，Claim 1 被否证，版本负面关闭（不得换指标）。
- slack 方向性两条均不成立 → SIG-2 失败，机制部分降级为纯现象报告并如实交付判断（可能不足以构成种子）。
- 证书复核（witness 与 stdlib 检查器）出现不一致 → harness 编码缺陷，实验无效，修复后推进新版本。
- harness 探针编码与检查器的随机赋值一致性测试失败 → 同上。
- D 桶 formalization_error/UNSAT 率过高（>60%）使 PASS 样本不足 → 外部有效性受限，如实报告并由主 Codex 判断是否值得交付。
