# P018 双读 reconciliation

## 1. 来源与全部尝试绑定

- PDF：`knowledge_base/staging/papers/P018_expel.pdf`；SHA-256：`01e533d81fb4a5f91797c073a9b1929acbaa64da45a592b26563ca7d135024f3`。
- 主 Codex 首读：`knowledge_base/pilot/reads/P018/read_1.md`；SHA-256：`e129a26592a96327c210cf5b86cd015dc859b6c886a9a28f5b638c9b506ca0c8`。
- 二读 `r2-20260719-p018-a1`：`ACCEPTED`。Invocation：`knowledge_base/pilot/reads/P018/read_2_attempts/r2-20260719-p018-a1/invocation.md`，SHA-256：`8ce8015566e26e8c03cd6ed3354e49f8cb6efe7b0d35d2c9d3850e50b3ea720a`；Report：`knowledge_base/pilot/reads/P018/read_2_attempts/r2-20260719-p018-a1/report.md`，SHA-256：`2301e8f46f31a232b0e279b7dc13d91386549028191787e093246f5856fc0441`。
- 其他 attempts：无。二读采用 `procedural_blinding` 并声明未读首读、Cards、其他报告或 blind query。
- 第三读：未启动。P018 不属于发现阻断冲突或影响多个关键 Operator 的论文；两读结论足以支持 Pilot 的窄主张。按本轮尺度约束，不为普通论文增加第三读。

## 2. 逐项裁决

### Changed computation — `AGREE`

ExpeL 把训练任务中的成功/失败轨迹压缩为跨任务自然语言 insights，并保存成功轨迹。测试时，不做权重更新，而把全部 insights 与按任务相似度检索的 top-k 成功轨迹加入单次 ReAct agent 的 prompt。机制是“离线经验抽取 + 规则记忆 + 示例轨迹检索”的双层经验注入。核点：PDF §3、Figures 1–2、Algorithms 1–2。

### Baseline — `AGREE`

最接近消融分别是 `insights only`、`retrieve only`、raw reflections + insights，以及使用随机/推理相似度替代 task similarity。ReAct 是主体基线，但 ExpeL 同时获得更长 context、检索示例和离线 GPT-4 抽取，因此不是等计算单变量比较。

### 公平性与预算 — `AGREE`

测试 agent 使用 GPT-3.5；经验抽取由 GPT-4 离线完成。ExpeL 的测试 token 明显高于 ReAct：Hotpot 约 4310 对 1320，ALFWorld 2857 对 2051，WebShop 3291 对 2575；离线 GPT-4 成本未计入测试预算。Gain 不能仅归因于“学习了更好规则”。核点：PDF experiments/cost tables。

### 结果与边界 — `AGREE`

作者报告 HotpotQA 39、ALFWorld 59、WebShop 41，高于对应 ReAct 28/50/35；但未做严格等 token/等模型/等示例预算控制。把 raw reflections 直接加入 insights 时 Hotpot 约 29，接近 ReAct 28 且明显低于完整 ExpeL 39，说明未筛选反思会污染长期规则。ALFWorld 上 task similarity 59，高于 random 42.5 与 reasoning similarity 48.5，表明检索键设计是机制的一部分。

### Operator — `AGREE`

Pilot 抽取 `Dual-Level Experiential Memory Injection`：将跨任务稳定规则与任务相似的成功轨迹分别存储，并在新任务开始前共同注入。Operator 必须公开离线教师模型、检索键、token 增量与经验来源，不能写成无代价的 self-improvement。

### Failure — `AGREE`

Pilot 抽取 `Unfiltered Reflection Contaminates Long-Term Insights`：把局部、带噪 reflection 不加筛选地混入长期规则，在 HotpotQA 消融中几乎抹去完整方法收益。该 Failure 限定于本文设置，不外推为“reflection 无效”。

## 3. 未解决项与准入裁决

- `UNRESOLVED`：离线 GPT-4 总成本与重现方差；严格等 token/等 retrieved demonstrations 的归因；经验库跨数据集迁移；论文对 half-swap/four-fold 叙述的口径细节。
- CORE disposition：`ACCEPT`。它提供 agent learning/experience memory 的直接机制与一个有实验支持的负向边界；双读已足够，不启动第三读。

