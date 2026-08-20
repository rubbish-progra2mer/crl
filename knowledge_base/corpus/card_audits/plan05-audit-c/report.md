# PLAN_05 新增 Failure Card 独立核源报告（C 组）

## 审计身份与边界

- task/thread identity：`/root/plan05_card_source_audit_c`
- 角色：未参与本组 Card 写作的独立核源者
- 审计时间：2026-07-19 23:51:40 +08:00
- 审计对象：指定的 9 张 Failure Card
- 结果口径：检查 Card metadata、production Evidence 与 admitted PDF 是否共同支撑 observed failure、条件与范围、替代解释、未否定边界和 repair boundary；特别检查单篇、窄设置负证据是否被外推。
- 非本任务：未修改 Card 或 Evidence，未创建 Candidate，未执行 novelty/prior-work、Commissioning 或科研三审。

## 结论摘要

- `PASS`：6 张。
- `REVISION_REQUIRED`：3 张。
- 三处修订都不是论文结论不存在，而是当前 Evidence 精确片段没有直接支撑 Card 中的 observed failure；对应 PDF 的相邻或前置结果页已有直接证据，最小处理是修正 Evidence span，并仅在一处收窄 Card 措辞。

| Card | 结论 | 当前 Evidence 对 observed failure 的直接性 | 核心理由 |
|---|---|---|---|
| `failure-constrained-plan-surface-validity` | `REVISION_REQUIRED` | C（间接） | Evidence 只定义 benchmark，没有记录 agent 违反约束的结果；PDF 第 6–7 页有直接结果。 |
| `failure-memory-unit-granularity-mismatch` | `PASS` | B（单篇直接） | 摘要和正文直接区分 turn/session/summary 的碎片、噪声与信息损失。 |
| `failure-sparse-topology-suppresses-correct-insight` | `PASS` | B（单篇直接） | cited passage 直接报告稀疏拓扑阻碍正确信息到达最终输出，Card 同时保留稠密传播错误的反向边界。 |
| `failure-lazy-agent-effective-single-agent-collapse` | `PASS` | B（单篇直接） | 原文明确报告 sequential ReMA 中 reasoning agent 影响下降、meta-thinking agent 承担几乎全部推理，并给出归一化偏置与消融边界。 |
| `failure-retrieved-update-lacks-decision-authority` | `REVISION_REQUIRED` | C（当前片段为定义性证据） | Evidence 只定义 SR/IPA，没有包含“识别不等于应用”的实测差距；PDF 第 7 页紧随其后的结果可直接补足。 |
| `failure-iterative-refinement-corrupts-correct-output` | `PASS` | B（P034 单篇直接；P033 仅为 operator 来源） | RefineBench 直接报告 DeepSeek-R1 的 correct→incorrect 转换；Card 已把负结论限制在该无显式反馈、五轮设置，没有否定 guided/external feedback。 |
| `failure-gold-context-does-not-solve-knowledge-use` | `PASS` | B（单篇直接） | Gold 直接给入必要文档后最佳模型仍仅 39.69 pass^1、26.80 pass^4；Card 没有把残余失败单归因于一个内部机制。 |
| `failure-tool-use-metrics-collapse-distinct-errors` | `REVISION_REQUIRED` | C（当前片段只列 taxonomy） | Evidence 只列四类错误；“aggregate score 会遮蔽不同失败”由 PDF 第 1 页直接报告，但未进入当前 Evidence span。 |
| `failure-confident-completion-without-state-success` | `PASS` | B（单篇直接） | 摘要直接报告语言完成声明与独立环境状态不一致，并在 tau2-bench/AppWorld 两类设置中验证。 |

## 逐卡核源

### 1. `failure-constrained-plan-surface-validity.md`

**结论：`REVISION_REQUIRED`**

- Card SHA-256：`7930aa026c409f69e128808453b5bb016d60f2bd853826613e0a66a18afb3a0b`
- metadata：`P004` / `ev-p004-failure-core` / `papers/P004_travelplanner.pdf`
- PDF SHA-256：`a7c7edd67c90e9997e940aaa7b435d46a8b201ed119c125b341b01b215454133`，与 Card 和 Evidence 一致。
- 当前 Evidence 位于物理第 3 页，只说明 TravelPlanner 用于评测 tool-use 与多约束规划；它没有报告“agents can deliver ... plans that violate constraints”。因此当前 `[AUTHOR_FACT]` 与引用片段之间缺少直接结果证据。
- 原 PDF 物理第 6–7 页直接给出所需事实：测试集多种方法 Delivery Rate 很高而 Final Pass Rate 极低；作者还明确报告 agents 常满足部分约束却遗漏其他约束，不能整体处理多约束。Table 3/4 的视觉版面与抽取文本一致。
- 外推检查：Card 的 benchmark/多日规划范围是合理的；但 “plausible” 不是该实验的操作化指标，可能把“成功交付一个 plan”外推成“质量上看似可信”。
- **最小修订**：将 `ev-p004-failure-core` 的 source span 改为或补入物理第 6–7 页的 Main Results / Table 3–4 直接证据；Observed failure 中把 `plausible travel plans` 收窄为 `delivered travel plans`，或明确写成“在 TravelPlanner 中有较高 delivery 但违反一个或多个结构化约束”。其余 alternative explanation 与 matched-budget repair boundary 可保留。

### 2. `failure-memory-unit-granularity-mismatch.md`

**结论：`PASS`**

- Card SHA-256：`1280fea1e5f4b9808d71cb3cf710690f0094c58dcd5d795a3bd8180417098496`
- metadata：`P011` / `ev-p011-failure-core` / `papers/P011_secom.pdf`
- PDF SHA-256：`998ab05ece554a83870b1baf5762f314837165e99f22ef2af8ffd7ba473c5004`，一致。
- 摘要直接报告 turn/session/summary 三种 memory unit 在 retrieval accuracy 与 retrieved semantic quality 上均有局限。正文进一步将 turn-level 归因为碎片化、session-level 归因为无关信息、summary 归因为信息损失。
- Card 没有把 granularity 写成唯一原因；compression、retriever 和 segmentation 被保留为替代解释。repair boundary 仍标为 hypothesis，并要求 equal context，边界足够窄。
- 无需修改。

### 3. `failure-sparse-topology-suppresses-correct-insight.md`

**结论：`PASS`**

- Card SHA-256：`89e6d5ca11239dbea33cc35eb45a83e2e2de0ca63c67057ca3d93b9c6681b88b`
- metadata：`P017` / `ev-p017-failure-core` / `papers/P017_information_propagation_topologies.pdf`
- PDF SHA-256：`f94767d936354030dc25f10db92a2f6f85f49b7d7163ac45b253e047ca67bd8b`，一致。
- cited passage 直接报告 sparse topology 阻碍 accurate/informative signals 影响最终输出，Chain 的 TCTE 最低；同页任务结果说明中等稀疏度最好，过稀与过密都次优。
- Card 没有外推为“全连接总是最好”，而是明确写入 dense graph 的错误传播与通信预算代价，并把 repair 收窄为 selective/evidence-aware routing。
- 无需修改。

### 4. `failure-lazy-agent-effective-single-agent-collapse.md`

**结论：`PASS`**

- Card SHA-256：`4e69f62e5aea3143aeb3660d704954a745397a47d107f4673cdf861e890cc28d`
- metadata：`P025` / `ev-p025-failure-core` / `papers/P025_lazy_agents_deliberation.pdf`
- PDF SHA-256：`5447d5ad949dd4b0061c36b80e395c97c1dc7534960576660096a2420408fc00`，一致。
- 原文在 sequential ReMA、shared terminal reward 与 multi-turn GRPO 条件下，直接报告一个 agent 只做复制/摘要、其因果影响随训练下降，而 meta-thinking agent 承担几乎全部推理。
- 论文把 turn normalization 的结构偏置作为理论与经验解释，但也显示仅去掉 normalization 不能完全消除 lazy behavior。Card 因而没有把 shared reward 写成唯一已证原因，并把 causal/localized credit 的修复与 restart/length-normalization 变化分离，边界准确。
- 无需修改。

### 5. `failure-retrieved-update-lacks-decision-authority.md`

**结论：`REVISION_REQUIRED`**

- Card SHA-256：`e4aae555e5a7e7a3fd37cca1d0920e9f36e0169ad0459a962208e75e8c22498d`
- metadata：`P030` / `ev-p030-failure-core` / `papers/P030_stale_memory.pdf`
- PDF SHA-256：`388f71f1eb952e7d7e7b19c2f25bfc744c47efa8ee00a548093b949432495109`，一致。
- 当前 Evidence 只解释 SR 测“直接问询下识别过时信念”、IPA 测“更新状态是否进入下游行为”。仅凭这段定义不能推出 Card 的 observed failure。
- 原 PDF 物理第 7 页紧随其后直接报告 `Success on one does not transfer to the other`，并给出 Qwen3.5-27B Type I 的 76.0% SR 对 39.0% IPA、Type II 的 42.0% 对 23.0% 等例子；作者明确称其为 recognizing outdated memory 与 applying updated state 的 gap。页面表格视觉核验一致。
- 外推检查：Card 条件已限制 implicit conflict 与 downstream policy；`write-side adjudication` 仍是 hypothesis，没有被冒充成论文已验证结论。
- **最小修订**：扩展或替换 `ev-p030-failure-core` 的 source span，使其包含第 7 页的实测差距、至少一个数值例子及作者的 gap 结论。Observed failure 可保留，或更窄写为“在 STALE 中，部分模型在显式识别过时信念时成功率更高，但在 downstream application 上明显下降”。

### 6. `failure-iterative-refinement-corrupts-correct-output.md`

**结论：`PASS`**

- Card SHA-256：`46e157d9f14e1b59f6d05f336f1954563d9a70db2f19c3aed375bed33f4225d1`
- metadata：`paper_id=null` / `ev-p033-operator-core` + `ev-p034-failure-core` / `P033` + `P034`
- PDF SHA-256：P033 `a07dfc5ada4ff818c77812dd581065a4e3e40f5736f2f36a97787a66da6e7825`；P034 `ee5c4d93ddf6c0741f0d08042b6aca2e0f08c3d3bd70e6cc6c90378bbc2d8c7f`；均一致。
- P033 Evidence 只支撑 Self-Refine 的 operator 定义，不提供负结果。窄负证据来自 P034：在 RefineBench 的 self-refinement（无显式反馈、最多五轮）中，DeepSeek-R1 的 2→3 转换出现 19.1% correct→incorrect，作者同时报告整体/模型/领域差异。
- Card 已明确区分“Self-Refine 定义 iterative feedback/revision”与“RefineBench 在 minimal protocol 中观察 transition failure”，并写明 prompt/domain/model/evaluator dependence 与 targeted external feedback 的未否定边界。因此 `can corrupt` 是存在性主张，不是对所有 reflection/self-refinement 的普遍否定。
- 使用边界：后续检索时，P033 不得被单独当作 failure evidence；它仅提供 operator lineage，负向判断必须回到 P034。
- 无需修改。

### 7. `failure-gold-context-does-not-solve-knowledge-use.md`

**结论：`PASS`**

- Card SHA-256：`e18eac46016649261430a299dc564e857749ff91419a7103f108630bcd9a444e`
- metadata：`P036` / `ev-p036-failure-core` / `papers/P036_tau_knowledge.pdf`
- PDF SHA-256：`f6fbe657daa349b1495bef6fecd7b1a3c845da3bf296d2589eedb45e051613bd`，一致。
- 论文明确把 Gold 设置定义为直接给入完成任务所需且经审查的 gold documents，从评估中移除 retrieval；最佳模型仍仅 39.69 pass^1，并降至 26.80 pass^4。第 7 页 Table 2 的视觉版面与抽取值一致。
- Card 仅得出“正确文档访问不足以保证成功”，没有将剩余失败单独归因于 reasoning；long context、tool interface、simulator 与 model capability 均作为替代解释保留。repair 也要求在 Gold condition 下比较。
- 无需修改。

### 8. `failure-tool-use-metrics-collapse-distinct-errors.md`

**结论：`REVISION_REQUIRED`**

- Card SHA-256：`d4374a67cda9f7969afacfbe64eae7291613e5f63efc53c89f613bac446e0555`
- metadata：`P039` / `ev-p039-failure-core` / `papers/P039_toolfailbench.pdf`
- PDF SHA-256：`6588af66fd477d9764c20c52c2adb7d92fcbf6a788fe09713bc71916862d3009`，一致。
- 当前 Evidence 位于物理第 3 页，只定义 Tool-Skip、Result-Ignore、Output-Fabrication、Unnecessary-Tool-Use 及 Correct；它没有直接记录“这些不同失败会被一个 aggregate score 遮蔽”。
- 原 PDF 物理第 1 页摘要与 Introduction 直接报告 aggregate benchmark scores hide where tool use fails，以及 never-call、call-but-ignore、invent-extra-information 可在 aggregate evaluation 下表现相似；这正是 Card observed failure 的直接依据。
- 外推检查：该论文是 1,000 个 single-turn、controlled function-calling tasks 的诊断 benchmark，不构成通用工具失败 taxonomy 的穷尽性证明。Card 已写明它是 diagnostic carrier、不是 universal taxonomy proof，边界良好。
- **最小修订**：为 `ev-p039-failure-core` 增补第 1 页摘要/Introduction 的 aggregate-score masking 直接片段；保留第 3 页 taxonomy 作为同一 Evidence 的上下文或拆为第二条 Evidence。Card 文字无需扩大，也不应把这四类写成所有 agent/tool 环境的完备分类。

### 9. `failure-confident-completion-without-state-success.md`

**结论：`PASS`**

- Card SHA-256：`1805cf394413276d28186161e2726c7c49300e4536659263e504fa073c35df58`
- metadata：`P040` / `ev-p040-failure-core` / `papers/P040_false_success.pdf`
- PDF SHA-256：`ab1307fdaaf97841bd09296bca225b736e8e9a712002ac123b1fab663f35ba6a`，一致。
- 摘要直接定义并报告 agent 声称任务完成而环境状态显示未完成的 false success；研究覆盖 tau2-bench 与具有 text-independent ground truth 的 AppWorld。
- Card 正确保留 domain、status-claim subset 与 detector transfer 的限制；环境检查被写成可能的检测/修复边界，并明确警告不要引入部署时不可得的 opaque oracle。
- 无需修改。

## 实际读取文件

### 执行与项目约束

- `D:/Desktop/crl_judge/AGENTS.md`
- `D:/Desktop/crl_judge/crl_agent_v3/AGENTS.md`
- `D:/Desktop/crl_judge/crl_agent_v3/CRL.md`
- `D:/Desktop/crl_judge/crl_agent_v3/CRL_ENVIRONMENT.md`
- `C:/Users/g/.codex/skills/evidence-quality-gate/SKILL.md`
- `C:/Users/g/.codex/skills/evidence-quality-gate/references/rules.md`
- `C:/Users/g/.codex/skills/evidence-quality-gate/references/output_schema.md`
- `C:/Users/g/.codex/skills/evidence-quality-gate/references/checklists.md`
- `C:/Users/g/.codex/skills/pdf/SKILL.md`
- `C:/Users/g/.codex/skills/encoding-safe-edit/SKILL.md`

### Production Evidence

- `D:/Desktop/crl_judge/crl_agent_v3/knowledge_base/corpus/evidence.json`
- SHA-256：`14595b5d45f8861752e6ef188505e761ca87f16885becfb46bfbd2e1667ea257`
- 实际读取 evidence IDs：`ev-p004-failure-core`、`ev-p011-failure-core`、`ev-p017-failure-core`、`ev-p025-failure-core`、`ev-p030-failure-core`、`ev-p033-operator-core`、`ev-p034-failure-core`、`ev-p036-failure-core`、`ev-p039-failure-core`、`ev-p040-failure-core`。

### Failure Cards

- `knowledge_base/cards/failure/failure-constrained-plan-surface-validity.md`
- `knowledge_base/cards/failure/failure-memory-unit-granularity-mismatch.md`
- `knowledge_base/cards/failure/failure-sparse-topology-suppresses-correct-insight.md`
- `knowledge_base/cards/failure/failure-lazy-agent-effective-single-agent-collapse.md`
- `knowledge_base/cards/failure/failure-retrieved-update-lacks-decision-authority.md`
- `knowledge_base/cards/failure/failure-iterative-refinement-corrupts-correct-output.md`
- `knowledge_base/cards/failure/failure-gold-context-does-not-solve-knowledge-use.md`
- `knowledge_base/cards/failure/failure-tool-use-metrics-collapse-distinct-errors.md`
- `knowledge_base/cards/failure/failure-confident-completion-without-state-success.md`

### Admitted PDFs

- `knowledge_base/papers/P004_travelplanner.pdf`
- `knowledge_base/papers/P011_secom.pdf`
- `knowledge_base/papers/P017_information_propagation_topologies.pdf`
- `knowledge_base/papers/P025_lazy_agents_deliberation.pdf`
- `knowledge_base/papers/P030_stale_memory.pdf`
- `knowledge_base/papers/P033_self_refine.pdf`
- `knowledge_base/papers/P034_refinebench.pdf`
- `knowledge_base/papers/P036_tau_knowledge.pdf`
- `knowledge_base/papers/P039_toolfailbench.pdf`
- `knowledge_base/papers/P040_false_success.pdf`

所有 PDF 均由原始文件直接打开；检查了 cited physical page，并对条件、结果、替代解释和边界做了全文关键词定位。对依赖表格/图形的关键点，还视觉检查了 P004 第 6–7 页、P030 第 7 页、P034 第 11 页、P036 第 7 页和 P039 第 3 页。

## 明确未读与未执行范围

- 未读取任何 blind query、blind judgment 或 blind evaluator 输出。
- 未读取 A/B 组审计报告，避免审计意见相互污染。
- 未读取与本组 9 张 Card 无关的 Card、Evidence 或 PDF。
- 未联网扩展文献，也未用模型记忆补写论文结论。
- 未逐页通读这 10 篇论文的全部附录；核源范围是 cited page、与当前 Failure Claim 直接相关的方法/结果/限制上下文，以及必要的表格视觉核验。因此本报告是指定 Claim 的 source audit，不是完整论文评审。
- 未修改 Card、Evidence、PDF、manifest、数据库或索引；未创建 Candidate；未启动科研 Reviewer 三审或 Commissioning。

## 最终处置建议

- 主 Codex 可直接接纳 6 个 `PASS`。
- 三个 `REVISION_REQUIRED` 只需做局部 Evidence/措辞修订，不需要新增 retrieval、schema、自动评分或其他 Harness 能力。
- 修订后只需重核对应 Card 与更新后的 Evidence span；没有理由重跑本组其余 6 张 Card 的审计。
