# CRL Contract v3 Run 文件指南

本文帮助主 AI 研究者使用文件与薄工具；它不是阶段机、表单或交付评分标准。正式流程只见 `CRL.md`。

## 1. 控制文件与兼容

新 Run 由 `tools/manage_run.py start` 创建 UTF-8 无 BOM、LF 的 `RUN_CHARTER.md`、`RUN_STATUS.md`、`RUN_LEDGER.md`。Charter 至少包含：

```text
RUN_ID: YYYYMMDD_HHMM_runNN
CRL_CONTRACT_VERSION: 3
DEFAULT_DOMAIN: TEXT_AND_TOOL_LLM_AGENT
MODE: AUTONOMOUS 或 DIRECTED
CURRENT_VERSION: v001
```

Status 保存客观生命周期和接手信息，不是科研阶段机。Ledger 只追加创建、转向、科学版本推进、暂停/恢复、Delivery、No-Go 和永久终止等耐久事实，不复制研究正文。

只有真实外部施加或已经客观达到的执行边界使本次 Goal、会话或平台执行窗口无法继续，而研究 frontier 仍存且主研究者没有形成科学终局时，Run 才以 `ACTIVE` 留下 handoff。只有用户明确窄方向创建的 `DIRECTED` Run 可在 Charter 边界内形成 No-Delivery。默认宽 AUTONOMOUS Run 暂未找到合格方向、候选耗尽、局部失败、运行较久或多次验证无效都不形成科学终局；授权仍有效且不存在不可越过的真实外部边界时，必须保持 `ACTIVE` 并继续回退、换题、正交扩展和验证。合法 handoff 可在现有 `memory_vNNN.md`、`selection_context_vNNN.md`、`failure_attribution_vNNN.md`、实验结果或其他适合的 Run-local 研究材料中留下耐久 continuation；只有用户明确暂停时才使用 `PAUSED_BY_USER`。

Contract v2 控制文件和终局仍可由检查器读取、审计和解释，但所有 v2 写入与恢复操作都会拒绝。新的科研创建 v3 Run。

## 2. 可选外部记忆

当前版本可按需使用：

- `problem_vNNN.md`：问题、价值、边界和反证条件；
- `research_map_vNNN.md`：论文、机制、Evidence 和未决问题；
- `nearest_prior_vNNN.md`：最近工作与组件级差异；
- `candidate_vNNN.md`：候选方法、changed computation 和风险；
- `evidence_packet_vNNN.md`：真正依赖的论文证据摘要；
- `selection_context_vNNN.md`：选择、放弃、转向及负面证据范围；
- `memory_vNNN.md`：当前假设、支持、反证和下一检查；
- `hypothesis_portfolio_vNNN.md`：多候选及谱系的非权威同轮记忆；
- `failure_attribution_vNNN.md`：失败事实与归因边界；
- `workbench_vNNN/`：自由草图、代码和 Scratch；
- `implementation_vNNN/`：准备绑定 Recorded、Formal 和 Review 的实现；
- `experiment_vNNN/plan.md`、`result.md`：可选实验计划和解释。

以上均可省略、不检查章节、不规定顺序、不参与交付资格。不得为了通过脚本写空洞内容。Research Subagent 仅指 Codex App 原生委派实际创建的独立任务；Reviewer CLI、角色模拟、Python 子进程和 Markdown 文件都不算。其草案只有经主研究者显式采纳后才进入当前科研判断。

### 2.1 Selection Context 候选偏好约定

`selection_context_vNNN.md` 继续使用既有六段自由 Markdown，不新增 Run 文件类型或 JSON 模式。旧六段内容无需迁移并保持可读；新写或修订活动候选时可使用以下声明：

```text
## 当前最佳候选集合

INCUMBENT_SET: <candidate-a, candidate-b | EMPTY | UNKNOWN>
CHALLENGERS: <candidate-c | EMPTY | INSUFFICIENT>

PAIRWISE_COMPARISON:
  PAIR: <candidate-a> | <candidate-c>
  VERDICT: A_PREFERRED | B_PREFERRED | INCOMPARABLE | INSUFFICIENT_EVIDENCE
  DECISIVE_EVIDENCE: <Run-local 路径或明确文献事实>
  A_SURVIVING_ADVANTAGES: <A 的存活优势>
  B_SURVIVING_ADVANTAGES: <B 的存活优势>
  SURVIVING_FATAL_UNCERTAINTIES: <仍存致命不确定性>
  REVERSAL_CONDITION: <会改变当前结论的新证据>
  NEXT_DISCRIMINATING_ACTION: <可能结果及各结果如何改变偏好>

CANDIDATE_ADMISSION: <candidate-id>
  TARGET_CLAIM: <可观察、实验或机械核验的主张>
  CONTRIBUTION_COORDINATE: <问题/现象/机制/干预/信息/评价/贡献形态>
  CHANGED_COMPUTATION: <相对最近强基线新增、删除或重排的计算>
  RESEARCH_ARTIFACT: <本地执行或机械核验载体>
  STRONGEST_CONSTRUCTIVE_BASELINE: <实际可构造的最强组合基线>
  FATAL_UNCERTAINTY: <最可能使论文级差分崩塌的问题>
  REVERSAL_TEST: <退出、降级、修订或超过 Incumbent 的结果条件>

LOCAL_REWARD_CONTRACT: <candidate-id>
  PRIMARY_OBSERVABLE: <主要可观察量>
  STRONG_BASELINE: <匹配信息、工具和预算的强基线>
  METRIC_DIRECTION: <方向>
  MINIMUM_MEANINGFUL_DELTA: <预先声明的最小实质差异>
  REPETITIONS_OR_UNCERTAINTY: <重复或不确定性表达>
  FAILURE_NEGATIVE_INCONCLUSIVE: <机械失败/科学负面/无结论的区分>
  EXECUTION_COST: <资源成本>
  LOW_FIDELITY_SCOPE: <低保真结果的外推边界>
  INDEPENDENT_ADMISSION_CHECK: <未直接参与本次修订设计的检查>
  SCALE_BRIDGE_ASSUMPTION: <从本地到扩大的桥接假设>
  MUTATION_ACCEPTANCE_CONDITION: <候选内部接受实现变异的条件>

EVIDENCE_ROLE: <candidate-id>
  DEVELOPMENT_EVIDENCE: <用于发现、调试或修订的路径>
  ADMISSION_EVIDENCE: <用于 Challenger 准入的独立检查路径>

INDEPENDENT_IMPLEMENTATION: <candidate-id>
  IMPLEMENTATION_ID: <实现标识>
  ARTIFACT_PATH: <Run-local 实现工件>
  FRESH_SESSION_ID: <由主研究者声明的会话标识；只作为 DECLARED_SESSION，不证明独立性>
  FROZEN_CANDIDATE_PATH: <相同冻结 Candidate Card 路径>
  FIDELITY_CHECK_PATH: <不看实验结果的实现忠实度检查>

IMPLEMENTATION_LOTTERY_EXCEPTION: <candidate-id>
  TYPE: MECHANICALLY_UNIQUE | STRUCTURAL_REFUTATION
  REASON: <无需第二实现的理由>
  EVIDENCE_PATH: <可核验证据路径>

## 新增正向证据

<新增实现、实验、强基线、先行差分及路径>

## 已失效或被杀范围

<证据实际杀死的实现、局部主张、方法核心或论文方向>

## 剩余致命不确定性

<当前最可能使论文级贡献崩塌的问题>

## 下一项最高信息量动作

<直接处理一个剩余致命不确定性的动作>

## 策略变化

PREFERENCE_UPDATE:
  ACTION_ID: <已声明高信息量动作标识>
  AFFECTED_PAIR: <candidate-a> | <candidate-c>
  VERDICT_BEFORE: <四值之一>
  VERDICT_AFTER: <四值之一>
  FATAL_UNCERTAINTY_REDUCED: YES | NO
  EVIDENCE_PATHS: <可追溯路径>
  STOP_REPEATING: <停止重复的动作>
  EXPANDED_COORDINATE: <真实改变的科研坐标>
```

`PAIRWISE_COMPARISON`、候选级声明和 `PREFERENCE_UPDATE` 均可重复。Diagnosis 保留同一结构字段的每次出现和次数，不以最后值覆盖；完全相同的重复也发 advisory，互相冲突的字段使对应块成为 `AMBIGUOUS`/`UNKNOWN`。全部成对比较按无序候选对归一化，反向 Pair 的 `A_PREFERRED`/`B_PREFERRED` 按实际候选身份解释；同一无序对出现不同实际 Verdict 时整组为 `AMBIGUOUS`、机械胜者为空且不得进入实现彩票或其他机械推断，相同实际 Verdict 的重复块则保留并发 advisory。`A_PREFERRED`/`B_PREFERRED` 只有在 Pair、Verdict、`DECISIVE_EVIDENCE`、`SURVIVING_FATAL_UNCERTAINTIES`、`REVERSAL_CONDITION`、`NEXT_DISCRIMINATING_ACTION` 均可解析且决定性证据没有未核验的疑似 Run-local 路径时才产生机械可用胜者；否则只保留 declared Verdict，比较为 `UNKNOWN`。重复 `INCUMBENT_SET`/`CHALLENGERS` 内容冲突时不得合并；同次声明将 `EMPTY`、`NONE` 或 `NOT_APPLICABLE` 与实际候选标识混写时为 `AMBIGUOUS` 且候选列表为空。字段不适用写 `NOT_APPLICABLE`，证据不足写 `INSUFFICIENT`，缺失写 `UNAVAILABLE`，未知写 `UNKNOWN`。`INCOMPARABLE` 保留双方且不是平局或失败；`INSUFFICIENT_EVIDENCE` 不选胜者。局部奖励只用于同一候选内部变异和实验排序，不产生全局 idea 分数，不判断新颖性、Delivery 或终局。相同开发样本的重复运行不能冒充独立准入；相同字节实现工件无论路径或 `FRESH_SESSION_ID` 如何声明都只能计一次。Diagnosis 对 `ARTIFACT_PATH`、`FROZEN_CANDIDATE_PATH`、`FIDELITY_CHECK_PATH` 记录普通文件 SHA-256，并区分 `DECLARED_SESSION` 与 `VERIFIED_ARTIFACT`；后者只证明 Run-local 文件和字节身份，不认证真实会话隔离、过程独立或科学独立性。`DECISIVE_EVIDENCE`、`EVIDENCE_PATHS`、`DEVELOPMENT_EVIDENCE`、`ADMISSION_EVIDENCE` 中疑似 Run-local 路径会核验边界、存在性和普通文件身份，失败显示 `UNVERIFIED` 并发 advisory，普通 DOI、arXiv 和明确文献事实保持 declared text。Diagnosis 不自动选择、淘汰或改状态。

## 3. Recall 与 Active Diagnosis

Run-local 派生索引位于 `.crl/recall/`：

```powershell
# 从当前 Run 或任一 Run 子目录执行时自动发现产品根、Run 和 CURRENT_VERSION
python D:\Desktop\crl\crl_agent_v3\tools\crl.py recall rebuild
python D:\Desktop\crl\crl_agent_v3\tools\crl.py recall rebuild --semantic
python D:\Desktop\crl\crl_agent_v3\tools\crl.py recall search --query "<QUERY>"
python D:\Desktop\crl\crl_agent_v3\tools\crl.py recall resume
```

`--product-root`、`--run-root`、`--version` 仍可在需要时显式覆盖。FTS 是必需底座；`--semantic` 是 best-effort，失败时明确降级。不带 `--semantic` 的 refresh 只重建 FTS；已有向量文件不会被主动删除，但只有新 FTS 身份与其记录一致、且 embedding 模型名和 revision 兼容时才继续使用，否则报告 stale 或 model mismatch 并完整回退 FTS。它不会隐式执行昂贵的 semantic rebuild。`resume` 会结合当前版本最近的关键研究文件与兼容的已有 semantic 索引补充早期思考。Recall 返回来源路径和哈希，排除敏感文本，但仍不是科学事实权威。

大量阅读后、想法趋同、连续失败、候选收敛、准备 Review 或长时间恢复时，可按 `.agents/skills/crl-active-diagnosis/SKILL.md` 判断是否值得收集诊断：

```powershell
python tools\crl.py diagnose --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> collect --diagnosis-id <ID>
python tools\crl.py diagnose --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> show --diagnosis-id <ID>
```

调用 collect 前先执行一次不带 `--semantic` 的 `recall rebuild`。若刷新失败，记录错误后仍可诊断；报告会把 FTS 标为 `READY` 或 `UNAVAILABLE` 并给结构化原因，semantic 降级另行披露。机器只收集事实，主研究者解释。无需按固定节奏调用。

Diagnosis 会在既有六段内容中机械读取候选集合、四值成对比较、决定性证据、反转条件、区分动作、候选准入、本地奖励、开发/准入证据、实现工件与自报会话标识、显式实现彩票例外和 Preference Update。旧格式、歧义或字段缺失显示 `UNAVAILABLE`/`UNKNOWN`，不会补猜；有实现或实验活动却缺少局部奖励合同、相同字节工件被重复声明或单一工件支撑想法级判断时只给 advisory。停滞窗口按每个 `ACTION_ID` 的最后出现位置选择最近三个不同动作，同一动作的多组成对更新仍只计一个动作；同一 `ACTION_ID` 与归一化 `AFFECTED_PAIR` 的冲突重复更新整组为 `AMBIGUOUS`，含 `UNVERIFIED EVIDENCE_PATHS` 的更新为 `UNKNOWN` 且不可评估。它们不能凭自报 Verdict 变化解除停滞，位于最近窗口时使判断为 `UNKNOWN`。三个可解释动作同时未改变四值 Verdict 且未减少致命不确定性时才报告 `PREFERENCE_STAGNATION_WARNING`，要求主研究者更新 selection context、写 `STOP_REPEATING`、扩大科研坐标并选择新辨别动作；工具不改 Status、Ledger、Hypothesis、Candidate、版本或终局。

当最近工作碰撞成为候选淘汰、Reviewer 致命风险、Delivery 或 `DIRECTED` Run-level No-Go 的主要依据时，优先复用现有 Prior Audit，而不是再造 novelty 工具：

```powershell
python tools\audit_prior.py --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> --hypothesis-id <HYPOTHESIS_ID> --audit-id <AUDIT_ID> --query "<QUERY>"
```

它是按需、非权威、Run-local 的可复查来源记录，不是所有候选的强制 Gate。

## 4. Scratch、Recorded 与 Tool Forge

Scratch 直接留在 Workbench。低摩擦、需要留痕的探索可用 Recorded：

```powershell
python tools\crl.py recorded --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> run --record-id <ID> --cwd <RUN_RELATIVE_DIR> --input <RUN_RELATIVE_INPUT> --output <RUN_RELATIVE_OUTPUT> -- <COMMAND...>
```

记录位于 `experiment_vNNN/recorded/<ID>/`，保存实现身份、命令、脱敏 stdout/stderr、输入输出和状态。它可进入 Evidence Inventory，但不能支撑 Delivery。

Recorded 超时会被记录为 `TIMEOUT`，但当前不承诺清理被测命令自行派生的整个进程树；需要可靠进程树终止时使用已有 Formal runner，避免为可选 Recorded 路径重构成熟执行器。

需要 Run-local 分析 helper 时：

```powershell
python tools\crl.py tool --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> create --name <TOOL_NAME>
```

生成模板通过 `RunToolContext` 约束原子 JSON/Markdown/CSV 输出路径。它减少脚手架摩擦，不是任意代码的操作系统沙箱。

## 5. Formal / Review-support attempt

正式 attempt 位于：

```text
experiment_vNNN/attempts/attempt-id/
├── execution.json
├── spec.json
├── metrics.json
├── dependencies.txt
├── stdout.bin
├── stderr.bin
└── 声明输入与输出快照
```

运行器要求当前版本 `--experiment-spec`、实验程序生成的 `--metrics-output`、至少一个 `--implementation-file`，以及 `--output` 或 `--stdout-as-evidence` 中至少一个证据通道。随机种子必须给出值或 `--seed-not-set`。可用重复的 `--declared-fact KEY=VALUE` 记录模型、数据和 provider 身份。

当前写入器生成 execution schema 8，读取器兼容 schema 5、6、7、8；schema 7、8 支持 Spec、Claim、metrics 与完整性绑定。正式规则以“等价 Review-support 真实性语义”为准，不永久绑定某个 schema 名称。

命令中的 `--implementation-file` 与最终 implementation manifest 用来绑定本次测量所依赖的可执行或可机械核验研究 artifact，不表示它必须是新算法。artifact 可以是方法/系统实现、基准或评价 harness、现象复现实验与测量程序，或理论/分析的机械核验程序；所选文件应真实承载 Seed 的核心贡献，而不是无关的占位脚本。

```powershell
& D:\Desktop\crl\env\crl_agent_v3\python.exe `
  D:\Desktop\crl\crl_agent_v3\tools\run_local_experiment.py `
  --product-root D:\Desktop\crl `
  --run-root D:\Desktop\crl\YYYYMMDD_HHMM_runNN `
  --version v001 `
  --attempt-id attempt-001 `
  --cwd D:\Desktop\crl\YYYYMMDD_HHMM_runNN\implementation_v001 `
  --experiment-spec D:\Desktop\crl\YYYYMMDD_HHMM_runNN\experiment_v001\specs\experiment-001.json `
  --metrics-output D:\Desktop\crl\YYYYMMDD_HHMM_runNN\experiment_v001\attempts\attempt-001\metrics-output.json `
  --implementation-file D:\Desktop\crl\YYYYMMDD_HHMM_runNN\implementation_v001\method.py `
  --stdout-as-evidence `
  --timeout-seconds 600 `
  --seed-not-set `
  -- D:\Desktop\crl\env\crl_agent_v3\python.exe method.py `
     --metrics-output D:\Desktop\crl\YYYYMMDD_HHMM_runNN\experiment_v001\attempts\attempt-001\metrics-output.json
```

指标 schema 1 包含 `experiment_id`、非空 `records`、`resource_usage`、`errors`、`warnings`。Runner 核验身份、有限数值、主指标、预算事实、输出和哈希，不判断效果。超时记录仍保留但不能支撑 Delivery。

## 6. 最终 Seed

准备交付的当前版本创建唯一：

```text
seed_vNNN.md
```

Seed 建议自足覆盖研究问题、最近工作、changed computation、最小可证伪 Claim、Formal 支撑、公平基线、替代解释、失败边界和扩大价值。它还应诚实区分机制一致性、评价依据独立的核心验证和扩大验证。这是科学表达建议，不是脚本章节检查。

AUTONOMOUS Run 准备最终 Seed 前，应按 `CRL.md` 判断方向发现阶段是否已经充分去风险。若已经明确一个当前资源内可执行、信息增益高、失败会使论文级 surviving contribution delta 大幅塌缩或退化为一般已知现象/最近先行实例的实验，应先继续研究，不能只把 Claim 缩窄到一个局部真实事实后启动 final-delivery Review。若剩余工作主要是外部有效性、扩大数据/模型/任务、论文规模增强，或依赖当前资源之外的新条件，则可以交付边界清楚的受限 Seed。若尚不能 Delivery，即使真实回溯、正交再扩张和必要高信息量检查后主研究者判断继续投入预期科研价值较低，也不得形成 No-Delivery；授权仍有效且不存在不可越过的真实外部边界时，Run 保持 `ACTIVE` 并继续研究。

方法、稳定经验现象、基准/评价、系统能力和理论/分析都可作为探索中的贡献形态。按当前 `CRL-EVAL-1.0` 正式交付时，Seed 的核心贡献必须有上述 artifact、真实 Formal / Review-support 测量和固定 Reviewer packet 可共同覆盖：现象需要可重复的观察/干预载体，基准或评价需要可执行协议与测量载体，系统需要可执行能力，理论/分析需要机械核验载体。尚只有概念论证而没有当前仪器可核验载体的理论或分析可以继续保留为高价值方向，但暂不具备正式 Delivery 条件。

反证 Spec 模式版本 2 显式保存 `evidence_fidelity`、模型/任务/数据/种子/环境 `subject_scope` 与独立实现数。Hypothesis 从 `draft/active` 转入 `falsified`、`prior_collision` 或 `escalated` 时使用 `manage_hypotheses.py transition --decision-json <JSON>` 追加不可变决策事件；普通 active 修订无需决策 JSON。机器只提示 Screening 或单实现越权杀伤、Representative 范围为空、prior collision 未复查 surviving contribution、结构性反证缺理由等字段组合，不替代科研判断。

## 7. 固定 Review

先把七个区域所需材料保存在 Run 内，再创建不可变 packet。`--section` 使用 `区域编号=Run相对路径`，可重复：

```powershell
python tools\crl.py review create --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> --section 1=seed_vNNN.md --section 2=nearest_prior_vNNN.md --section 3=experiment_vNNN/result.md --section 3=experiment_vNNN/attempts/<ATTEMPT_ID>/metrics.json --final-delivery
python tools\crl.py review run --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> --evaluation-id <eval-NNNN>
python tools\crl.py review status --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> --implementation-key <KEY>
```

final-delivery packet 必须包含 Seed 和有效 Formal attempt 的材料路径。机器会自动附加全部 Formal/comparison/Recorded 身份清单，并为所选 Formal 生成限长 Core Evidence Closure，直接呈现关键 Spec/Claim 和真实指标值。Seed 中已经显式声明的 metric mapping 必须与来源事实一致；未声明 mapping 或仍有未映射数字只作为 Reviewer 可见 advisory，不自动阻止 final Review。每个 measurement 的首次有效三审是 canonical，后续同键只是稳定性测量。

主研究者把 Decision 正文先写到 Run 内临时文件，再绑定 canonical：

```powershell
python tools\crl.py review decide --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> --body-file <RUN_LOCAL_DECISION_BODY>
python tools\crl.py review deliver --product-root D:\Desktop\crl --run-root <RUN> --version <vNNN> --supporting-attempt <ATTEMPT_ID>
```

完整隔离、键和校准规则见 `CRL_REVIEWER_PROTOCOL.md`。

## 8. 无交付与永久结束

默认宽 AUTONOMOUS Run 在局部盆地耗尽或当前没有活动候选时，默认进入 frontier discovery：backtrack，并寻找结构不同的问题、失败现象、机制/干预家族、评价/基准、系统约束或贡献形态；若科学坐标实质改变，再复用 `advance-version --transition-file <JSON>` 进入下一搜索时期。转换 JSON 只要求 `CHANGED_COORDINATE`、`SURVIVING_FRONTIER`、`NEXT_HIGH_INFORMATION_ACTION`，可选 `RESOURCE_NEEDED`；工具原子创建包含既有六段标题的下一版本 `selection_context_vNNN.md`，并把未知的 `INCUMBENT_SET`/`CHALLENGERS` 显式写作 `INSUFFICIENT`，不据版本推进编造候选或偏好。文献扫描、查询改写、候选重命名、候选/版本/检索数量或查询指纹互不重复不能代替 re-expansion。

只有 `DIRECTED` Run 可新写 `NO_DELIVERY.md`，或在用户显式恢复后写版本化后继；正文自由说明窄 Charter 内的真实停止理由、正交探索、高信息量检查与剩余科研价值判断，不要求 Seed、实验或 Review。已有历史 No-Delivery（包括 AUTONOMOUS）保持只读解析、审计和用户显式恢复兼容，不迁移、不重写；恢复后的 AUTONOMOUS 版本不得再次写入 No-Delivery。版本数、时长、Token、候选数、检索数和单个负结果不能单独支持 `DIRECTED` 终局，写入入口核验机械一致性并强制 Charter/Status 的 `MODE` 均为 `DIRECTED`。

当实际平台/模型额度耗尽、服务当前不可用、权限缺失、明确算力/进程/执行限制已经触发，或下一步必须等待当前不可获得的资源，而 frontier 尚存且没有科学终局时，结束本次 Goal/会话并留下第 1 节所述 continuation；Run 仍为 `ACTIVE`，也不因 handoff 自动推进 `vNNN`。不得由主研究者自行设定软预算来触发 handoff。`TERMINATED_BY_USER.md` 只在用户明确永久终止时生成，形成后不可恢复。

常用机械入口还包括：

```text
tools/manage_run.py start|advance-version|pause|terminate
tools/inspect_run.py
tools/query_knowledge.py cards|passages|hybrid|evidence|paper
```

没有调用某个可选工具本身不能成为科研不合格理由。
