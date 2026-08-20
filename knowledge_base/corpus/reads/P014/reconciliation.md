# P014 三读 reconciliation

## 1. 来源与全部尝试绑定

- PDF：`knowledge_base/staging/papers/P014_instruct_of_reflection.pdf`；SHA-256：`57a01e87496308e3345839c48f085516dd2824ec5aaacf51b71f127c12f42bb7`。
- 主 Codex 首读：`knowledge_base/pilot/reads/P014/read_1.md`；SHA-256：`73e4d9a72d96d89c2509251348d352d7f51fdec9137036c36b5b3ab67f6cca9c`。
- 二读 `r2-20260719-p014-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P014/read_2_attempts/r2-20260719-p014-a1/invocation.md`，SHA-256：`7f1a825a6b6d8d5ee6176fcb2e8011a9ecc2d5fd27e57d3bf9710f31b17ce700`；Report：`knowledge_base/pilot/reads/P014/read_2_attempts/r2-20260719-p014-a1/report.md`，SHA-256：`eef6a91123b44a3228a6d9045eef2e8cdcb604eece4372704417013de970f789`。
- 第三读 `r3-20260719-p014-a1`：`ACCEPTED`；触发原因是该论文同时影响 reflection control、外部 verifier 归因与负向边界。Invocation：`knowledge_base/pilot/reads/P014/read_3_attempts/r3-20260719-p014-a1/invocation.md`，SHA-256：`2ffe9ea1ac5c1ec3da68f73de187847eede67a9083e6c19e055a3a3f332b1e57`；Report：`knowledge_base/pilot/reads/P014/read_3_attempts/r3-20260719-p014-a1/report.md`，SHA-256：`9a29b37eb3b8e10f0934a27b4604907dcf4facca18760cb0fd8678fa722ad8af`。
- 其他 attempts：无。两名独立读者均为 `procedural_blinding`；运行时强制读取的通用技能说明不含 Pilot 科研结论，已如实披露。

## 2. 逐项裁决

### Changed computation — `AGREE`

三读一致：IoRT 在 basic/reflected response 产生后增加动态控制器。答案不一致时由独立 GPT-3.5 instructor 在 meta-thought 辅助下 select；答案一致时决定 stop 或 refresh；meta-thinker 还从任务级 meta-memory 检索并追加 `(question, meta-thought)`。核心是候选生成后的动态 `stop/select/refresh` gate，而不是模型参数更新或 equality classifier 本身。核点：PDF pp.5–6，§4.1–4.3、Figure 4、式 (1)–(7)。

### Baseline — `AGREE WITH SOURCE CONFLICT`

流程上最接近 Self-Reflection、CRITIC、Self-Contrast；计算量较接近 PoT/CoT-SC(8)、Multi-Agent 与 Self-Contrast；HSP 组合是 meta guidance 的较近控制。IoRT 并非所有 cell 都优于最强 baseline。论文正文声称 Llama2-7B/GSM8K 上 Self-Contrast 胜 IoRT，但 Table 1 为 20.5 对 24.0，方向相反；Pilot 采用表格数值并保留源文冲突，不替作者消解。核点：PDF p.7，Tables 1–2、§5.2。

### 公平性与预算 — `AGREE`

所有 backbone 的 meta-thinker 与 instructor 均固定为 GPT-3.5-Turbo-0613；因此 Llama 行不能解释为 base model intrinsic self-correction。IoRT 使用更多调用、任务特定 few-shot/meta assets 与数学代码执行，论文未给完整等 token/等模型/等 prompt 的单因素比较。数学平均 calls 7.3，StrategyQA 3877 tokens，但跨表结果含外部来源。核点：PDF pp.6–8，§5、Tables 1–3、Figure 5。

### 结果与边界 — `AGREE`

IoRT 相对 plain PoT/CoT 多数为正，但主要收益混合了 selector、meta guidance、额外计算和更强外部模型。无 select 的 IoRT* 平均约低 4.4%，无 meta-thought 约低 2.1%；去 equality gate 的精度只小幅降低却需要跑满迭代。正确答案仍会 drift；selector 也会误判。Meta-memory 是否跨问题/运行重置未说明。附录部分案例的响应、代码与标记相互冲突，不作为 Evidence。核点：PDF pp.7–9、12、21–23，Table 3、Figure 5、Tables 13–14。

### Operator — `AGREE`

Pilot 抽取 `Dynamic Stop–Select–Refresh Reflection Control`：在每轮反思后显式比较候选状态，再根据一致性与独立 criterion 选择、停止或重启。Operator 必须公开 instructor 的模型、信息来源、额外调用与 meta-memory 生命周期，不能写成“模型自己会反思”。

### Failure — `AGREE`

Pilot 记录两类窄 Failure：`Static Reflection Redundant–Drift–Stubborn Trilemma`，以及 `Strong External Instructor Masquerades as Base-Model Self-Improvement`。前者是作者直接分类的反思边界；后者是基于明确实验配置的归因限制，不声称 IoRT 无效。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：Meta-memory 是否跨 test item/run 累积；人工 meta/refresh/reflect examples 的精确来源；缺少“相同 GPT instructor、无 reflection”的完整 selector-only 消融；开放 Agent trajectory 的 consistency/stop 定义。
- 上述问题限制 Claim 宽度，但不阻断作为近期 reflection-control/归因边界材料。
- CORE disposition：`ACCEPT`。该论文是 Pilot 中关键冲突/多 Operator 来源，因此进行了第三读；不据此要求其他普通论文第三读。

