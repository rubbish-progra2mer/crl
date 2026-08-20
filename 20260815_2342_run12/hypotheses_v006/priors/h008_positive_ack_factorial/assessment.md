# 最近先行科研解释

> 本文件属于主研究者解释，可在阅读候选、PDF、Evidence 和实验后继续修订；它不进入机器事实快照哈希。

- 审计标识：`h008_positive_ack_factorial`
- 碰撞类型：`DIRECT_EXACT`（一般现象）+ `DIRECT_PARTIAL`（配对评价）+ `CONSTRUCTIVE_COMPOSITE`（响应×效果正交干预，经实验后不足以存活）

## 真正的 nearest prior

- *Failing Tools: Benchmarking LLM Agent Recovery Under Runtime Tool Failures*（OpenReview `j7YsSnA64D`，2026-05）：搜索索引可核验的正文把 FM1 明确定义为“success-response trust”，即把成功字段当作状态转移证明而不读回；其 218 个有状态情景也直接包含 silent no-op、partial write、确认调用和禁止的危险后续动作。这是 h-008 一般现象与轨迹指标的最强直接碰撞。
- *Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures*（arXiv:2608.02645v1；精确审计候选见 `../h008_verified_calls/candidates.json`）：论文形式化区分 response channel 与 effect channel；但 Algorithm 1 在 `response == SUCCESS` 时直接返回，只在 `AMBIGUOUS` 分支调用外部 verifier。实验把 timeout、delayed visibility、partial success、conflict 按故障等级联合采样，没有报告 SUCCESS/AMBIGUOUS × applied/no-op 四格策略效应。
- *AgentCheck*（arXiv:2607.11098v3；精确审计候选见 `../h008_agentcheck/candidates.json`）：记录干净轨迹并只改变一个缓存工具响应，覆盖 12 种故障；其错误、陈旧、矛盾、错误答案、silent empty 等注入没有把“回执标签”与“真实状态效果”作为两个独立随机因子。
- *AgentAbstain*（arXiv:2607.10059v1；精确审计候选见 `../h008_agentabstain/candidates.json`）：用 263 个 should-act/should-abstain 配对任务、42 个可执行沙箱和 commit check 测量运行时发现后是否停止。S6 把必要工具从正常行为改为持续显式报错；论文图中的 2×2 是“是否提交×是否口头拒绝”的结果分类，不是 response×effect 的实验因子。
- *From Confident Closing to Silent Failure*（arXiv:2606.09863v1；精确审计候选见 `../h008_false_success/candidates.json`）与 ToolGate（KB P074）：分别占据 false-success 的大规模观察刻画和契约后置条件门方法。

## 实质组件重合

- 问题重合：工具响应不能证明外部状态，silent no-op 会被当作完成。
- 行为重合：缺少 readback、成功回执信任、危险或未证实的下游动作、提前完成声明。
- 方法重合：独立状态读取、任务后置条件、提交门、verify-before-retry；h-008 不得把这些包装为新算法。
- 评价重合：受控故障注入、配对任务、可执行沙箱、逐轨迹必需/禁止调用、隐藏状态和提交检查。

## 仍存贡献增量

- 仅剩一个评价与因果辨认差分：四格独立操纵 `response∈{SUCCESS, AMBIGUOUS}` 与 `effect∈{applied, no-op}`，在 effect 固定时估计回执标签对主动读回和危险提交的政策效应，并在 response 固定时估计真实效果本身是否可被代理辨认。
- 该差分不等于发现 success-response trust；它回答现有联合故障条件无法回答的机制问题：模型是因为真实故障线索而谨慎，还是因为肯定标签本身停止取证。
- 若差分存活，贡献优先定位为小而严谨的因果诊断套件与跨模型经验规律；“对显式成功做 effect witness”只作为中介验证或系统含义，不与 ToolGate/Verified Tool Calls 竞争一般方法新颖性。

## 最危险替代解释

- `AMBIGUOUS` 自带不确定语义，观察到差异可能只是普通指令理解；必须用至少两套等长模板和状态中性控制检验措辞依赖。
- 本地小模型可能放大策略差异；若 qwen3:8b 不复现或跨域不稳，不能外推到通用代理。
- 任务提示若明确说“先验证再提交”，会把目标行为泄漏成指令遵循；主条件必须只陈述业务依赖关系与工具能力。
- 只做四格并不能自动成为论文贡献；若效应近乎确定、无异质性、无预测或设计含义，则可被视为 Failing Tools 的平凡消融。
- AgentAbstain 的配对因果框架与 commit check 很强；h-008 必须证明双因子设计能分解其单一 trigger 无法分解的机制，而不是换名复刻。

## 最小区分实验

- 先用 3 个写入域×4 个任务模板×4 格×2 个本地模型的确定性杀手试验；主指标为首次下游动作前的 read_state 比例、no-op 时的危险提交率和 effect×response 交互。
- 同一任务四格必须共享任务、系统提示、工具定义、写参数、最大轮数与采样配置；环境评分器直接读隐藏状态，不用语言模型裁判。
- 若 qwen3:4b 与 qwen3:8b 均没有 SUCCESS/AMBIGUOUS 对比，立即 falsify；若只有一条措辞有差异，增加等长同义模板后仍不稳也 falsify。
- 若出现强差异，再加成功格的机械 effect-witness 与等预算非绑定读回对照，检验危险提交下降是否由读回中介；不先做大实验。

## 方法死亡后仍存现象

- 即便全量后置条件验证的方法新颖性已死亡，响应标签作为代理信息获取策略的因果输入仍可能是独立经验现象。
- 若这个标签效应也被本地实验否证，则 silent no-op、false success、postcondition verification 和 abstention 都完全退回最近先行，本候选无剩余。

## 背景与身份未解决项

- OpenReview 对当前匿名网络请求返回 403，未能把 *Failing Tools* PDF 保存到 Run；这里对其方法边界只使用搜索索引可核验的正文段落，不能声称已读完整附录。若本地实验强阳性，进入 Formal 前必须从公开仓库、作者页或可访问会话补齐全文并核查场景生成代码。
- 通用 `audit_prior` 因外部源降级没有返回全部已知强邻居；精确标题审计已分别冻结 Verified Tool Calls、AgentCheck、False Success、AgentAbstain 的候选身份，原论文 HTML 用于组件级核对。

## 试验后结论

- 有效杀手试验见 `../../../workbench_v006/h008_pilot_assessment.md`。qwen3:4b 与 qwen3:8b 在 `SUCCESS` 后分别 12/12 直接提交；在 `AMBIGUOUS` 后分别 11/12 与 12/12 盲重试；所有四格的独立读回均为 0/12。
- 因果标签效应存在，但不支持“模糊回执触发核验”的强机制，且提交/重试分叉被 Verified Tool Calls 的问题设定与算法直接预示。响应×效果四格只是 Failing Tools、AgentCheck、AgentAbstain 评价部件的低成本组合，无法单独支撑 CCF-B 研究种子。
- 先前记录的 `SURVIVING_EVALUATION_DELTA` 因此关闭；h-008 应按 `prior_collision` 结束，而非进入 Formal。
