# P012 三读 reconciliation

## 1. 来源与全部尝试绑定

- PDF：`knowledge_base/staging/papers/P012_reflexion.pdf`；SHA-256：`efba04cd48b779131fc4c3c58ae49e8523ded534f9225a7c57c7bdad0823803d`
- 主 Codex 首读：`knowledge_base/pilot/reads/P012/read_1.md`；SHA-256：`4d7ce1273d9d7fbd64dafeecafa756d0b17658e087cf503d5eb0605d70d92e91`
- 二读 `r2-20260719-p012-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P012/read_2_attempts/r2-20260719-p012-a1/invocation.md`；SHA-256：`eb944e88c0c9fa281408cd22bd69f5c1e4bdad75bf77c8850e95efcd4c324677`。Report：`knowledge_base/pilot/reads/P012/read_2_attempts/r2-20260719-p012-a1/report.md`；SHA-256：`bfb7de966f1d64824f38625fec5ba33a4408cb7db2d099c883ef2a808163a97c`。
- 第三读 `r3-20260719-p012-a1`：`ACCEPTED`；触发原因是 Reflexion 是 reflection/verbal learning 的唯一直接祖先/强 baseline。Invocation：`knowledge_base/pilot/reads/P012/read_3_attempts/r3-20260719-p012-a1/invocation.md`；SHA-256：`97bde726a8668a59ccc7246ab2cb3aab8206e9d03cd22956a945039804866f7d`。Report：`knowledge_base/pilot/reads/P012/read_3_attempts/r3-20260719-p012-a1/report.md`；SHA-256：`eae5c61300a8f6fcec936a5ec0e73e4e6f572d656113582651877b779d184fd3`。
- 其他 attempts：无。独立读者均为 `procedural_blinding`，声明未读前读/Cards/其他报告/blind query。第三读未进行像素级渲染，首读和二读的视觉核查用于补足该边界。

## 2. 七类逐项裁决

### Changed computation — `AGREE`

三读一致：Reflexion 不更新权重，而在 trial 后将 evaluator 的稀疏 reward/反馈与轨迹送入 Self-Reflection model，生成语言经验并追加到容量受限 episodic memory；下一 trial Actor 以短期轨迹+长期反思为上下文重新行动。最小链是 failure detection→verbal reflection→persistent context→retry。核点：PDF pp.3–5 §3/Figure 2/Algorithm 1。

### Baseline — `AGREE`

ALFWorld 直接 baseline 是相同 ReAct仅 reset/retry；Hotpot有仅保留最近轨迹 EPM 消融；编程有“无内部 tests但反思”和“有 tests无 reflection”双消融。WebShop 是明确负结果。CoT(GT) 获得数据集 ground-truth context，是 oracle 条件，不能与普通反思混同。核点：PDF pp.5–8、12–14。

### 公平性与预算 — `AGREE`

完整方法允许多 trial、额外 reflection calls、tool/test execution 和更长 context，未与等 token/call随机重采样/搜索对齐。Hotpot各路径 shots不同，编程内部自生成 tests并执行；“pass@1”是多轮生成/内部筛测后一次 hidden-test submission，不等于单次 LM sample。核点：PDF pp.6–8、14–19。

### 主要结果 — `AGREE`

ALFWorld heuristic Reflexion最终 130/134，作者称较强 baseline +22 points；Hotpot反思相对 EPM +8 points；Rust hardest完整 .68 vs base .60，但无 tests反思 .52、tests无反思 .60。WebShop四 trials无改善；starchat .26=.26；MBPP Python 77.1低于base/SOTA 80.1。核点：PDF pp.5–8、12–14。

### Limitation — `AGREE`

收益依赖 evaluator grounding与强 backbone；内部 tests有 false positive，错误 feedback会诱导 harmful edit；探索型任务的反思可 generic/local-minimum。无完整 token/cost/seed/CI、长期 memory污染、跨任务迁移或对抗反馈实验。Algorithm 1 trial index有排版疑问，prompt是正文/附录有限呈现。核点：PDF pp.4–8、12–16。

### Operator — `AGREE`

Pilot 抽取 `Evaluator-Grounded Verbal Reflection Memory`：将环境/测试反馈与失败轨迹压缩为语言化、可持久重用的下一 trial 条件。明确 evaluator provenance 是机制输入，不把任意自我批评等同 Reflexion。

### Failure — `AGREE`

Pilot 抽取 `Ungrounded Reflection Causes Harmful Retry`：无可信 tests/evaluator时，强制反思会把 .60 降到 .52；WebShop反思也可不具帮助性。它说明 reflection 质量受反馈可判别性和探索空间约束，不写成普遍无效。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：无阻断项。
- Open limits：等预算 attribution、完整模型/超参、Hotpot/EPM token对齐、长期反思累积稳定性和开放工具安全未解决。
- CORE disposition：`ACCEPT`。三读确认祖先机制、grounding条件与真实负结果。
- Task 5 计划：1 个 Operator Card、1 个 Failure Card、1 个 Paper Card；先建立 Evidence。
