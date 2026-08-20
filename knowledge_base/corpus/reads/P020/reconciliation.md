# P020 双读 reconciliation

## 1. 来源与尝试绑定

- PDF：`knowledge_base/staging/papers/P020_agenttts.pdf`；SHA-256：`454906b0f931fd092ab25163c1ea3fd69e793eac570320ba257d174bee9b0c7c`
- 主 Codex 首读：`knowledge_base/pilot/reads/P020/read_1.md`；SHA-256：`c4135e11be031432f0daf84fec1a0c4618ed5759938daa3dc039c3f819e4da79`
- 二读 `r2-20260719-p020-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P020/read_2_attempts/r2-20260719-p020-a1/invocation.md`；SHA-256：`eb33ea538154dd64bb996de0f22eab285d595b3de071df3f8db53b5cd76eaf1b`。Report：`knowledge_base/pilot/reads/P020/read_2_attempts/r2-20260719-p020-a1/report.md`；SHA-256：`0b69a1fc2481d63dad8767556dc4e9366245bef97b1e93d2df59180a58e489ee`。
- 其他二读 attempts：无。第三读 attempts：无；本文不是唯一祖先/强 baseline，计划不超过两个 Operator/Failure Cards。两读核心判断一致；来源内部 budget 参数冲突不能靠独立读者消除，按 open source limitation 保留。
- 独立性：`procedural_blinding`；二读者声明未读取项目首读/Cards/其他报告/blind query。系统技能说明不含 P020 科研结论。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

两读一致：AgentTTS 在多阶段任务运行前/轮间搜索每个 subtask 的 model 与 repeated-sample count；GPT-o3-mini 根据三条人工总结的 TTS insights、Archive 和 50-sample training feedback 提出新配置。执行端仍是同模型多样本+同模型 fusion。它是 prior-conditioned black-box configuration search，不是基础模型训练。核点：PDF pp.3–8 §§3–6、Figure 2/Algorithm 1。

### Baseline — `AGREE`

最接近的是共用 GPT-o3-mini 搜索骨架的 AgentHPO/MLCopilot；差异主要是 AgentTTS 获得更具体的三条 priors 与初始化。`Best` 是 prior grid search 的 training optimum 参考线。没有“相同 priors + non-LLM deterministic/evolutionary controller”控制。核点：PDF p.8 Table 1/Figure 3、pp.35–36。

### 公平性与预算 — `RESOLVED_BY_SOURCE`

方法用平均 prompt/decode 长度和近似 FLOPs 归一化，忽略 attention 小项，且公式未明确计 fusion 调用；pilot curves、model-family screening、prior grid 的离线成本未计入 Table 1 search time。Table 4 与 Appendix A.4 对 CWQ/WebQSP/TaskBench 长度写法冲突，直接影响 normalized budget，故不声称具体配置严格等实际计算。核点：PDF pp.3–4、23–27。

### 主要结果 — `AGREE`

六个 test metrics 只有 2Wiki 的 0.72 清楚高于下一表内值 0.70；Hotpot/CWQ/WebQSP/TaskBench/ChatDev 多为并列。主要支持是一次 50-trial trace 更快达到已知 training optimum，不是所有任务 final quality 更高。Checklist 明示无统计显著性，未报告 variance/多 seed。核点：PDF pp.8、16–22 Table 1/checklist。

### Limitation — `AGREE`

三条 insights 和 model family screening 来自相同六类数据/任务，未做 unseen task-type transfer；只支持静态预定义 stages；50-sample objective+temperature 0.9 有噪声；ChatDev metric 是语义 embedding consistency，不是 functional correctness；API-price/temperature 只在 2Wiki 扩展。Checklist LLM usage 标 NA 与核心 GPT-o3-mini 描述存在披露张力。核点：PDF pp.5、8–10、22、27–38。

### Operator — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Insight-Conditioned Multi-Stage Budget Search`：以模型/样本等价预算、stage-specific saturation/cross-stage dependence 和真实小样本反馈驱动配置搜索。等价预算公式是其输入约束，不另拆 Card。

### Failure — `RESOLVED_BY_SOURCE`

Pilot 只抽取 `Prior Advantage Mistaken for LLM Planning Advantage`：方法获得 dataset/task-informed priors，缺少相同规则的非 LLM controller，故不能隔离 LLM planning 的净贡献。Offline pilot cost 与 noisy optimum 作为同一 Paper Card 的公平性边界。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项；budget 长度冲突阻止精确成本归因，但不改变“搜索 model/sample 配置”的方法身份或定性结果。
- Open limits：fusion 是否计费、batch candidates/trial 对应、grid oracle 使用范围、pilot split/成本、unseen task transfer 和多 seed 均未解决。
- CORE disposition：`ACCEPT`。提供 efficiency/planning 交叉 Operator 和高价值 prior-attribution Failure。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先建立 Evidence。
