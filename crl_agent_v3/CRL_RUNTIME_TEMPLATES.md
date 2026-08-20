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

只有真实外部施加或已经客观达到的执行边界使本次 Goal、会话或平台执行窗口无法继续，而研究 frontier 仍存且主研究者没有形成科学终局时，Run 才以 `ACTIVE` 留下 handoff。主研究者也可在真实 backtracking、正交 re-expansion 与必要高信息量检查后形成 No-Delivery，表示本次 Run 继续投入的预期科研价值已不足。合法 handoff 可在现有 `memory_vNNN.md`、`selection_context_vNNN.md`、`failure_attribution_vNNN.md`、实验结果或其他适合的 Run-local 研究材料中留下耐久 continuation；只有用户明确暂停时才使用 `PAUSED_BY_USER`。

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

当最近工作碰撞成为候选淘汰、Reviewer 致命风险、Delivery 或 Run-level No-Go 的主要依据时，优先复用现有 Prior Audit，而不是再造 novelty 工具：

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

AUTONOMOUS Run 准备最终 Seed 前，应按 `CRL.md` 判断方向发现阶段是否已经充分去风险。若已经明确一个当前资源内可执行、信息增益高、失败会使论文级 surviving contribution delta 大幅塌缩或退化为一般已知现象/最近先行实例的实验，应先继续研究，不能只把 Claim 缩窄到一个局部真实事实后启动 final-delivery Review。若剩余工作主要是外部有效性、扩大数据/模型/任务、论文规模增强，或依赖当前资源之外的新条件，则可以交付边界清楚的受限 Seed。若真实回溯、正交再扩张和必要高信息量检查后，主研究者判断本次 Run 的继续投入预期科研价值已不足，则可形成 No-Delivery；脚本不评分该判断。

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

默认宽 AUTONOMOUS Run 在局部盆地耗尽或当前没有活动候选时，默认进入 frontier discovery：backtrack，并寻找结构不同的问题、失败现象、机制/干预家族、评价/基准、系统约束或贡献形态；若科学坐标实质改变，再复用 `advance-version --transition-file <JSON>` 进入下一搜索时期。转换 JSON 只要求 `CHANGED_COORDINATE`、`SURVIVING_FRONTIER`、`NEXT_HIGH_INFORMATION_ACTION`，可选 `RESOURCE_NEEDED`；工具原子创建下一版本 `selection_context_vNNN.md`。文献扫描、查询改写、候选重命名、候选/版本/检索数量或查询指纹互不重复不能代替 re-expansion。

`DIRECTED` 与宽 AUTONOMOUS Run 都可写 `NO_DELIVERY.md` 或显式恢复后的版本化后继，自由说明真实停止理由、正交探索、高信息量检查与剩余科研价值判断；不要求 Seed、实验或 Review。宽自主 No-Delivery 只关闭本次 Run，不表示领域穷尽。版本数、时长、Token、候选数、检索数和单个负结果不能单独支持终局，写入入口只核验机械一致性。

当实际平台/模型额度耗尽、服务当前不可用、权限缺失、明确算力/进程/执行限制已经触发，或下一步必须等待当前不可获得的资源，而 frontier 尚存且没有科学终局时，结束本次 Goal/会话并留下第 1 节所述 continuation；Run 仍为 `ACTIVE`，也不因 handoff 自动推进 `vNNN`。不得由主研究者自行设定软预算来触发 handoff。`TERMINATED_BY_USER.md` 只在用户明确永久终止时生成，形成后不可恢复。

常用机械入口还包括：

```text
tools/manage_run.py start|advance-version|pause|terminate
tools/inspect_run.py
tools/query_knowledge.py cards|passages|hybrid|evidence|paper
```

没有调用某个可选工具本身不能成为科研不合格理由。
