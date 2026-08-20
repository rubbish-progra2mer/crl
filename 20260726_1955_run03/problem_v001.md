# Research Problem

## User intent

用户于 2026-07-26 发起本机器 Ready 后的第一个正式研究 Run（run03），未指定研究子方向，明确要求主 Codex 基于共享论文知识库自主选题、自主检索与判断、不中途停下，目标是产出一份合格的 `DELIVERY.md`（一颗值得扩大的研究种子）。用户同时预授权 DeepSeek API（无额度上限，按实验披露用量）。

## Use Thesis and real consumer

**真实研究消费者**：构建与评测 solver-backed LLM 形式化规划系统的研究者与工程团队（P051/P052 范式的建设者），以及受约束规划类 agent benchmark 的维护者。

**其当前决策与可观察限制**：这些消费者当前用两类信号认证一个 LLM 形式化管线：(a) 解级成功——solver 报 SAT/OPTIMAL 且返回的解通过基准的参考检查器；(b) 错误触发修复——UNSAT core（P051）、planner/验证器报错（planner-in-the-loop 反馈）、运行时异常。他们观察不到的量是：**返回解通过检查，是因为约束真的被编码进了形式模型，还是因为解在过大的可行集里碰巧满足了未被编码的约束**。P055 的作者已在原文承认 plan correctness 可能把未忠实表达约束的代码判为成功，但只在跨数据集合并抽样的 20 个样本上检查过这一假阳性通道（KB Failure Card `failure-constraint-shift-breaks-formalization`，Evidence `ev-p055-plan-correctness-false-positive-boundary`）。

**错误后果**：已发表的形式化成功率系统性高估语义忠实度；下游使用者部署静默漏约束的形式化器；当实例分布收紧（约束更常 binding）时，故障在生产中无预警暴露；以错误信号为触发的修复环对这类静默故障结构性失明。

## Decision interface

**Implement 的输入**：一条自然语言约束规格、由 LLM 生成的可执行约束模型 M（SMT 程序或等价可搜索表示）、solver、以及审计场景下可得的逐约束参考检查器。

**输出**：逐约束的 enforcement 判定（enforced / not-enforced-but-masked / not-enforced-and-caught）、实例级 masking 质量，以及可选的"静默故障错误信号"（供修复环消费）。

**接入位置**：形式化管线的认证/验收环节（benchmark 评测代码、CI 验收门、以及研究论文的指标报告协议）。

**会改变的真实决策**：(1) benchmark 维护者是否在 pass rate 之外增加 enforcement-level 报告；(2) 系统建设者是否把解空间探针作为验收门与静默故障的修复触发器；(3) 研究者如何在不同 scaffold 强度的形式化器设计之间取舍（按 enforcement 而非 pass rate 排序）。

## Value Bridge and proxy limit

实验 proxy 是：在一个带逐约束参考检查器的受约束规划基准族上，量化 (i) 自然发生的 enforcement 故障率，(ii) 其中被解级成功掩盖的比例（masking rate），(iii) 掩盖质量随约束松紧度（slack）的结构，(iv) 错误触发修复信号对被掩盖故障的覆盖率（预期≈0，即互补性）。

**明确不能证明**：不能证明所有形式化范式/载体上的掩盖率量级；不能证明真实部署中的伤害率；除非实际运行修复臂，不能证明探针触发修复能提升端任务成功；不能证明在没有参考检查器的纯部署场景下探针审计同样可靠（那需要独立编码探针谓词，会重新引入形式化风险——这是诚实边界）。

## Occupancy scan before problem commitment

扫描日期：2026-07-26（Asia/Shanghai），开放网络（WebSearch），共 11 轮定向查询。逐节点结果：

1. **工具菜单干扰/近邻消歧**（P084 失败空间）：已被占——DiaFORGE（arXiv 2507.03336，消歧微调+相似度谱）、"A Single Rewrite Suffices"（2606.30775，生产 skill 描述改写修 collision）、"Looking Is Not Picking"（2606.16364，attention-segment 机理+readout 干预）、"How Many Tools Should an LLM Agent See?"（2605.24660，chance-corrected 菜单规模）。节点关闭。
2. **工具描述/顺序偏置的归因与缓解**（P069 失败空间）：已被占——ToolTweak（2510.02554，攻击+paraphrase/perplexity 防御）、BiasBusters（2510.00307，偏置发现+缓解）、分布鲁棒性量化（2510.03992）。节点关闭。
3. **描述偏置的动态锁定/反馈下切换**：强邻占——"Don't Blindly Trust It"（2606.21409，不可靠反馈下的行为）、ToolMaze/"When Tools Fail"（2606.05806，等价替代工具与恢复基准）、"Where LLM Agents Fail"（2509.25370，失败归因+反馈学习）；且抽象 bandit 载体的探索失败与 ledger 修复已被 2403.15371 占用。节点关闭；执行恢复方向另被 CORPUS_SCOPE 排除。
4. **记忆写入污染/来源防御**：已被占——StateGuard（写回边界审计）、Memory Contagion（2606.23195）、State Contamination（2605.16746）、长期记忆安全综述（2604.16548）。节点关闭。
5. **语义 plan cache 假阳性验证**：已被占——Asynchronous Verified Semantic Caching（2602.13165）、Temporal Semantic Caching 评测（2605.20630）、SemanticALLI（2601.16286）。节点关闭。
6. **NL→形式规格的 case 级忠实性验证**：已被占——Validating Formal Specifications with LLM-generated Test Cases（2510.23350，Alloy）、Verus-SpecGym（2605.26457，可执行规格 accept/reject 信号）。节点关闭。
7. **形式化修复环**：已被占——P051 unsat-core 交互修复（2404.11891）、Planner-in-the-Loop PDDL 反馈（2606.29700）、Robust Asynchronous Planning via Auto-Formalization（2606.00981）。节点关闭——但全部依赖显式错误信号（UNSAT/验证器报错），对"SAT 且返回解通过检查"的静默漏约束无信号可用。
8. **OR 建模载体的静默漏约束探测**：已被占——ReLoop（2602.15983，solver 扰动行为验证）、Beyond Objective Equivalence: Constraint Injection（2606.04816，VRP 上可行探针+单约束违反探针）、OptArgus（2605.11738）、ConstraintBench（2602.22465）。该占用证明现象与探针计算真实存在，但其载体是 OR 应用题（NL4Opt/VRP 族），未在旗舰 agent 规划基准上量化"已发表成功率中的掩盖质量"，未给出松紧度机制结构，也未量化与错误触发修复环的互补性。
9. **工具参数值来源接地/幻觉**：已被占——AgentLTL（2607.02599，实体接地 trace 约束）、AgentHallu（2601.06818）、The Reasoning Trap（2510.22977）。节点关闭。
10. **TravelPlanner 形式化的 enforcement 审计**（本 Problem 指向的具体开放节点）：未检得任何先行——P051（NAACL 2025，93.3% val pass）及其文献综述、跟进工作均以解级 pass rate 为最终指标；无工作量化其成功中的 enforcement-lucky 比例。
11. **执行恢复/环境反馈学习**：CORPUS_SCOPE §3 明确排除该独立研究方向；多张 KB Failure Card 亦标注不扩展至此。主动排除。

**扫描后仍开放的节点**：对"NL→可执行约束模型→solver→解级认证"管线的**逐约束 enforcement 审计与掩盖率量化**，其载体为带逐约束参考检查器的 agent 规划基准族；机制维度（掩盖质量随 slack 的结构）与互补维度（错误触发修复信号对被掩盖故障的零覆盖）在任何已扫描载体上都未被运行过。近祖先（SQL distilled test suites 2020、Alloy test cases 2510.23350、OR constraint injection 2606.04816）将在 nearest-prior 检索中完整披露并逐项写明剩余差异。

## Mechanism Demand before carrier selection

**因果环节**：NL 约束集 {c_i} → LLM 生成可执行约束模型 M → solver 在 M 的可行集 F(M) 上返回解 s → 认证计算只检查 s（解级检查 + 错误信号）。故障模式：c_i 未被编码（omission）或被错误编码（mistranslation），使 F(M) ⊃ F(true)；当 s 碰巧落在 F(true) 内时，认证计算输出 PASS，故障静默。

**使用时点可得信息**：NL 规格；M 本身（白盒、可执行、可搜索）；solver；审计场景下的逐约束参考检查器。不可得：部署时的黄金形式模型。

**要改变的决策变量**：形式化结果的接受/报告决策——从"解级 PASS 即接受"变为"逐约束 enforcement 判定后接受/标记/触发修复"。

**改变的计算**：认证计算从"检查返回解 s"扩展为"对每个 c_i，在 F(M) 内对抗性搜索违反 c_i 的解 s_i'"——若找到 s_i'（M 接受但参考检查器拒绝的解），则 c_i 未被 enforce；该搜索只用 solver 调用，不用 LLM，不看黄金模型。

**预测机制签名**：(S1) 自由形式形式化下自然 enforcement 故障率显著大于零，且随 scaffold 强度上升而下降；(S2) 被掩盖故障集中于低 binding 频率（高 slack）的约束——slack 越大，返回解碰巧合规的概率越高；对同一故障，收紧实例参数会使掩盖单调转为暴露；(S3) 错误触发修复信号（UNSAT core、解级检查失败）按构造对被掩盖故障覆盖率≈0；(S4) 探针审计对照参考检查器具有高精确率（探针发现的未 enforce 判定能被黄金检查器复核）。

**成本/权限/接口约束**：探针成本为每约束 O(1) 次额外 solver 调用（本地、无 LLM 费用）；审计接入只需读 M 与调用 solver，不改动形式化器本身。

**决定性反例**：若在自由形式（非 P051 级强 scaffold）形式化下，解级 PASS 的实例中 enforcement 故障率以紧置信区间趋近于零，则掩盖现象在该载体族上不构成值得交付的测量对象——本 Problem 及其 kernel 应被杀死或收窄，不得靠改换指标续命。

**Carrier-independent statement**：在任何"把自然语言约束规格翻译为可执行约束模型、以返回解的检查作为成功认证、以显式错误信号作为修复触发"的管线中，逐条件 enforcement 可以通过在模型自身可行集内对抗性搜索违反各参考条件的解来度量；"解级成功掩盖的静默漏约束质量"由此可与"被错误信号捕获的故障质量"分解开来。该陈述不含任何 benchmark、dataset、协议或榜单名称。

**另外两类 carrier 的预测**：若机制成立——(a) 在 NL→数据库查询载体上应表现为"单实例执行正确掩盖语义错误查询"（该载体的祖先证据已存在：distilled test suites，作为机制普适性的支持而非本 Run 贡献）；(b) 在 NL→调度/资源配置模型载体（会议排程、课程表、云资源配额等 NL 规格到 CP/ILP 模型）上应出现同构的 slack-luck 结构：松弛实例下漏约束调度表大量通过人工检查，紧实例下同一故障立即暴露。预测签名同 S2。

## Text/tool LLM Agent scope

研究对象是文本/工具型 LLM Agent 的 solver-backed 规划形式化计算（planning_reasoning 机制簇的 P051/P052→P054/P055 谱系步）。实验被试为通过 API 调用的 LLM 形式化器 + 本地 solver + 本地检查器，全部文本接口。

## Soft constraints

- 优先使用共享主环境已有依赖；solver 若需 Z3，以官方发布的独立可执行文件形式引入（不改动 pip 环境、记录 SHA-256），或在证据显示不可行时按 CRL_ENVIRONMENT 建立例外环境。
- 实验成本目标：单版本 Promotion Development 的 API 费用控制在个位数美元量级，按实验披露实际用量。

## Hard exclusions

- 不研究执行恢复/环境反馈学习方向（CORPUS_SCOPE 排除）。
- 不做模型训练/微调。
- 不使用 LLM judge 作为主要指标（本载体全部指标可由参考检查器与 solver 机械判定）。
- 不把"暂未找到碰撞"写成已证明新颖。

## Cost authorization

本 Run 预授权 provider 白名单：deepseek（RUN_CHARTER，2026-07-26，无上限、按实验披露用量；用途边界为实验被试 rollouts、数据生成与本 Run 内评分）。key 只经进程级临时环境变量传入，绝不进入任何冻结产物。本 Problem 的实验预计只用 deepseek-chat 作为形式化被试；本地 solver 与检查器零 API 成本。
