# P016 三读 reconciliation

## 1. 来源与全部尝试绑定

- PDF：`knowledge_base/staging/papers/P016_mast_failures.pdf`；SHA-256：`6aff168d6e201217d3f79611f6ad024590a599a03b97ac2aeb0b0b128bac374c`。
- 主 Codex 首读：`knowledge_base/pilot/reads/P016/read_1.md`；SHA-256：`ecde721eb81872dc76f226ade0f67995fcd814cefbfe1f507e903f99f93a0944`。
- 二读 `r2-20260719-p016-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P016/read_2_attempts/r2-20260719-p016-a1/invocation.md`，SHA-256：`832bf55413b76c81b9c91011be266eba0582fb845a88e99d18134d0857fd486b`；Report：`knowledge_base/pilot/reads/P016/read_2_attempts/r2-20260719-p016-a1/report.md`，SHA-256：`6b2f09aac164c5ab9e1a698b2d13488b4e68a16e3957de897c3563c03e8d48f1`。
- 第三读 `r3-20260719-p016-a1`：`ACCEPTED`；触发原因是该论文是多代理 Failure taxonomy 的高复用来源，且 intervention 表与 failure occurrence 图存在表面冲突。Invocation：`knowledge_base/pilot/reads/P016/read_3_attempts/r3-20260719-p016-a1/invocation.md`，SHA-256：`5352c052f420c02fb760bcc37b668bcccb43491f948a78b01e57b12996da6093`；Report：`knowledge_base/pilot/reads/P016/read_3_attempts/r3-20260719-p016-a1/report.md`，SHA-256：`c53e0daa7293992b57308f8803e249c9b24e279afea0cde8c6a54c59558feded`。
- 其他 attempts：无。独立读者均为 `procedural_blinding`；运行时强制工具说明的额外读取已披露，不含 Pilot 科研结论。

## 2. 逐项裁决

### Changed computation — `AGREE`

MAST 的主要贡献不是新的 agent policy，而是对 1,600+ 条多代理 execution traces 作人工/模型辅助的 trace-level failure diagnosis，形成 system design、inter-agent misalignment、task verification 三大类及子类。论文随后以 topology 与 prompt interventions 检验部分 failure diagnosis 是否能指导修改。核点：PDF methodology/taxonomy sections、Figures 1–4、Tables 1–2。

### Baseline 与测量口径 — `AGREE WITH SOURCE CONFLICT`

比较对象是七个现有 multi-agent systems，并非在统一 architecture 上只改变一个变量。Failure occurrence 是一条 trace 可含多个标签的计数，不等于 task failure rate，不能与 accuracy 直接互换。AG2 prompt intervention 的 Table 5 显示 accuracy 上升，但 Figure 10 的总 failure occurrences 从 1622 增至 1818；其中 topology-related occurrences 降至 462。附录 H.3 把二者都描述为下降，和图中总数冲突。Pilot 分别保留两个口径，不把它们强行合并。

### 公平性与边界 — `AGREE`

系统、任务、模型、工具、拓扑和 prompt 同时变化，taxonomy prevalence 不是因果效应。标注依赖 taxonomy 定义与 trace 可观测性；同一 trace 多标签、任务准确率与 failure occurrence 的分母不同。Checklist 还声称 Tables 2/5 含置信区间，但 Table 2 无区间且 Table 5 的 ChatDev 列缺区间；Figure 11 内部标题与 caption 的系统名也冲突。这些源文异常限制精确量化，但不推翻 taxonomy 的描述性用途。

### Operator — `AGREE`

Pilot 抽取 `Trace-Level Multi-Agent Failure Taxonomy Audit`：先把多代理执行轨迹分解到 system design、coordination/alignment 与 verification failure，再据此选择局部 architecture/prompt intervention。它是诊断 Operator，不自动判定科研优劣，也不把标签频率当因果机制。

### Failure — `AGREE`

Pilot 抽取 `Accuracy Gain Can Coexist with More Failure-Mode Occurrences`：在不同分母与多标签口径下，intervention 可提高 end-task accuracy，同时增加被标记的 failure occurrences；因此“准确率提高”不能自动解释为内部协作更可靠。另保留三类具体 failure family，但不把 taxonomy 当 exhaustive truth。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：AG2 Figure 10 总 occurrence 与附录叙述冲突；Figure 11 系统名；部分 CI 声明与表格不符；标注者一致性与跨系统可迁移的完整细节。
- 这些异常要求 Card 采用窄表述并区分 accuracy、task failure 与 occurrence，不阻断作为 multi-agent failure taxonomy 来源。
- CORE disposition：`ACCEPT`。它影响多个 Failure/Operator 且存在真实源冲突，因此第三读必要；不据此要求普通论文第三读。

