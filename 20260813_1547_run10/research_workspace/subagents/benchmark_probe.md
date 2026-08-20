# v001 基准与高信息量实验路径勘探（Research Subagent 非权威草案）

- Run：`20260813_1547_run10`
- Version：`v001`
- 子任务：寻找可注入“语法成功但语义错误”工具观测、且由方法外部终局判定成功的现有基准/环境
- 调研截止：2026-08-13
- 权威边界：本文只是原生 Research Subagent 的事实材料与实验建议；最终取舍、Candidate、Seed 和 Decision 均由主 AI 研究者裁决
- 隔离声明：只读取了本 Run、`crl_agent_v3` 机器文档、冻结共享知识库和论文/官方仓库一级网络来源；未读取其他 Run
- 执行声明：本子任务没有运行正式实验、Recorded 实验或机器健康检查，也没有安装或下载基准

## 1. 中心结论

截至本次核查，没有发现一个已经公开可运行、且原生同时满足下列三项的基准：

1. 在多步文本/结构化工具轨迹中可控注入**结构合法、无异常码、但语义错误**的观测；
2. 主指标由不属于候选方法的环境终态、数据库状态或隐藏单元测试判定，而不是由“是否重试/是否走参考路径”等方法同形规则判定；
3. 候选与强基线能在相同工具权限、模型和可比预算下直接运行。

最稳妥的 v001 路径是：

- **正式核心载体首选 AppWorld**：复用其数据库状态单元测试与“无附带损害”判定，只在函数调用/MCP 工具边界加一个薄故障适配器。方法只看到正常工具接口和被扰动的返回，终局测试不暴露给方法。
- **τ³-bench 作为第二域/复现实验载体**：其数据库哈希终局很合适，但当前官方仓库仍有 2026-07 报告的空评价条件和 no-op 任务假阳性问题；正式使用前必须固定提交并逐任务审计，排除已知问题任务。其大语言模型用户模拟器还会引入额外随机性。
- **ToolMaze 仅作 Scratch/Recorded 诊断载体，不承担核心终局主张**：它原生提供 P3/P4 隐式语义扰动和恢复成本，但官方 `judge.py` 主要检查工具名覆盖、调用次数、重试/切换/停止，不检查参数、执行顺序或数据库终态；“调用了预期工具”不能替代任务完成。
- **BFCL、ToolBench/StableToolBench 不适合作为 v001 核心终局**：它们分别更适合函数调用构造/状态处理和大规模工具访问；当前协议没有同时提供原生隐式语义故障与独立终局。
- 2026 年最贴题的 Failing Tools、AgentNoiseBench 目前官方仓库仍未放出实现，现阶段只能做碰撞监控和故障类型参考。

这不是 v001 的 No-Go：AppWorld/τ³-bench 的薄适配器路径足以做真实、外部终局、同权限实验；但应把“新方法优于 ToolMaze 官方通过率”从候选主张中删除。

## 2. 基准适配表

| 基准/后继 | 多步文本/工具环境 | 原生“结构合法但语义错误”注入 | 方法外部终局 | 当前公开可运行性 | v001 结论 |
|---|---|---|---|---|---|
| AppWorld | 是；9 个日常应用、457 个应用程序接口，支持函数调用/MCP/编码智能体 | 否；需要在工具服务器响应层加薄适配器 | **强**：数据库状态单元测试检查任务目标及附带损害；测试集只公开评价程序，不公开设置/解法 | 官方包与数据公开；Python 3.11+；当前本机共享 Python 3.11.15 版本匹配，但依赖仍应放 Run-local 隔离环境 | **首选 Formal 载体**。只用函数调用/MCP 模式，禁止候选获得通用文件/数据库访问 |
| τ³-bench（τ²-bench 官方仓库现行版） | 是；airline/retail/telecom 等客户服务工具任务 | 否；可包装工具分发器注入 silent no-op / stale read | **中强**：DB 哈希、环境断言、通信条件；部分自然语言断言用大语言模型 | 官方代码公开；现行版要求 Python `>=3.12,<3.14`，与共享 3.11 不兼容，需要 Run-local 3.12；2026-07 仍有评价空条件假阳性 issue | **第二正式域/稳健性域**。固定提交，排除或修复已知问题任务；控制用户模拟器方差 |
| 原始 τ-bench | 是 | 否 | DB 终态 + 必要输出，但任务版本已过时 | 官方 README 明确要求使用 τ³-bench | 只作历史文献定位，不再作为实现基线 |
| ToolMaze（2026） | 是；400 个任务，C1–C4 有向无环图，P0–P4 | **是**：P3/P4 为隐式瞬时/永久语义扰动；固定响应，first-touch 激活 | **弱/不充分**：官方判定侧重预期工具集合、次数和恢复行为；缺少参数、顺序及真实终态核验 | 代码、数据和最小依赖公开；原 README 建议 Python 3.10，未在本机验证 | **仅 Scratch/Recorded 行为诊断**；报告命中、重试、替代路径和调用成本，不把官方 pass 当独立任务成功 |
| Failing Tools（2026） | 是；218 个有状态服务情景 | **是**：stale、corrupt、partial、silent no-op、success-shaped 等 | 中：required/forbidden calls、确认检查点和行为 rubric；终局是否完全程序化仍需代码核查 | 论文称将公开；当前官方入口未找到可运行仓库 | **监控**。代码放出后优先复核，但当前不能作为实施依赖 |
| AgentNoiseBench（2026） | 是；对 τ²-bench/VitaBench 等注入用户/工具噪声 | 是：错误事实、不完整响应、误导信号等 | 中：轨迹感知评价 + 原基准终局；噪声由生成器/参考智能体约束可解性 | 官方 GitHub 当前只有 “Code Coming Soon” | **监控**。当前不可复查，不进入正式实验 |
| BFCL v3/v4 | 多轮状态工具评价存在；v4 还覆盖网络搜索、记忆和格式敏感性 | **否**：主要测模型调用选择、参数、状态与返回匹配；环境默认不是欺骗性语义故障 | 中：抽象语法树、执行、状态、响应等分解；不是为恢复后的多路径任务终局设计 | 官方 `bfcl-eval` 可运行，建议 Python 3.10；公开版本/榜单需严格固定 | **非核心**。可作函数调用格式、参数与额外调用副作用的回归检查，不用于证明语义故障恢复 |
| ToolBench | 多工具、真实应用程序接口、DFSDT 回溯 | 否；原生不稳定应用程序接口常产生显式/时变失败 | 弱：ToolEval/Pass/Win 依赖大语言模型评价，且常用 oracle API 集；预算未严格配平 | 公开但真实应用程序接口不稳定 | **排除核心**。DFSDT 保留为强控制流基线 |
| StableToolBench | 是；MirrorAPI 模拟 ToolBench 工具 | 主要解决可复现性；论文故障消融返回显式 “no useful information” | 弱至中：StableToolEval/FAC 仍不等价于隐藏环境终态 | 公开代码、模型/镜像；本机未验证 | **补充域而非核心**。不满足隐式语义错误 + 独立终局组合 |
| ToolSandbox | 是；可变世界状态、Milestone/Minefield 有向无环图 | 否；需自定义响应适配器 | 中：支持多路径和禁区，但人工里程碑带过程先验，用户模拟器有误差 | 公开 | 可作 AppWorld 之外的补充诊断，不优先于 AppWorld |
| Tools Fail（EMNLP 2024） | 受控计算器是单步；自然错误部分是具身/视觉 | **是**：计算器给语法合法错误数值 | 算术真值独立，但不满足 v001 多步文本工具边界；另一部分越出非视觉边界 | 论文公开 | 只作故障定义和单步校准，不作 v001 主载体 |

## 3. 对三个指定家族的审计

### 3.1 τ-bench → τ²-bench → τ³-bench

优点：

- 原始 τ-bench 的关键价值是 episode 结束后比较数据库终态与目标状态，而不是信任智能体的完成声明；冻结知识库 `ev-p007-terminal-state-evaluation` 已固定这一点。
- 当前 τ³-bench 官方评价文档明确：默认通过重放参考动作得到目标 DB，并按 DB 哈希比较预测终态；其他等价动作路径可通过，避免强绑唯一轨迹。
- 因此可以在工具返回层注入假成功，而不改变终局评价代码；这是认识论分离最清楚的设计之一。

障碍：

- 原始 τ-bench 任务已经被官方标为过时，不能再以旧仓库任务作为正式主结果。
- τ³-bench 官方仓库的 issue #384 指出多类空 `communicate_info`、未进入 `reward_basis` 的断言和 no-write 任务会自动给分。对于 v001，至少应排除 issue 中列出的 airline/retail P0/P1 问题任务，并在固定提交上对所有纳入任务检查：目标 DB 是否真的变化、每个启用评价维度是否非空。
- 用户由大语言模型模拟；候选和基线即使同配置，也可能经历不同对话。若无法固定用户轨迹/随机种子，应把 τ³ 作为第二域，并报告重复试验与方差，不能把单次差值归因于恢复机制。
- 当前实现要求 Python 3.12，而 CRL 共享环境是 3.11.15；不得升级共享环境，应建立 Run-local 3.12 隔离环境并固定 `uv.lock`/提交。

建议注入点：工具分发器返回结果之后、消息写入智能体上下文之前。对第一次本应成功的 write 调用，运行器不提交真实状态，但返回与成功路径相同结构的确认体；随后正常 read API 可暴露真实未变化状态，第二次 write 可成功。最终 DB 哈希仍由原 evaluator 独立判断。

### 3.2 BFCL v3/v4

BFCL 的优势是可执行函数调用、多轮状态、缺参数/缺函数/长上下文等分解，且可报告抽象语法树、执行、状态和响应误差。它适合作为“候选是否破坏基础函数调用能力”的回归集。

它不原生测 v001 的核心干预：默认工具结果不是“语法成功但语义错误”，多轮评分又针对预定义调用/状态目标。若强行注入额外错误，候选为了验证而增加的调用可能改变 BFCL 的既有聚合语义，难以区分“正确恢复”与“偏离参考调用”。因此：

- 不用 BFCL 作为主要终局；
- 可抽取少量 multi-turn base/missing-parameter 条目做 clean regression；
- 若做故障扩展，只把参数正确率、状态匹配和额外调用数分开报告，不把官方总分直接解释为故障恢复率。

### 3.3 ToolBench → StableToolBench

原 ToolBench 的最近控制流基线 DFSDT 确实提供显式 give-up、回退到分叉状态和兄弟动作重采样；冻结知识库 P005 的核查也指出最公平对照应是同成本 ReAct@N。但其核心测量存在三项不适配：

- 真实 RapidAPI 时变，故障既不固定也常为显式异常；
- 主结果混合检索、oracle API 集、模型、搜索预算与 ToolEval；
- ToolEval/Pass/Win 不是隐藏环境终态，拒绝/尝试有时也会被评价为 pass。

StableToolBench 用 MirrorAPI 改善了可复现性，但已展示的 failure ablation 是返回显式无用信息，并非欺骗性语义成功；其终局仍不如 AppWorld 的状态单元测试独立。因此 ToolBench 家族可提供 DFSDT 和等成本 ReAct@N 基线，不应承担核心正向证据。

## 4. 推荐的独立评价依据

### 4.1 首选：AppWorld 隐藏状态测试

运行方式：

- 使用 AppWorld 的函数调用或 MCP 智能体接口，不使用开放的 `world.execute` 编码 shell，防止候选读取任务文件、评价程序或底层数据库。
- 候选只获得任务文本、公开工具规范、动作历史和工具返回。
- 故障适配器运行在工具服务端；它可访问本次注入清单，但不向候选暴露注入标志、真实值或评价结果。
- episode 结束后调用原生 `world.evaluate()`/CLI evaluator；主指标用 Task Goal Completion、Scenario Goal Completion、单元测试通过和附带损害，不用候选自评。

核心独立性：方法构造只决定何时验证/回滚/重规划；最终正确状态由 AppWorld 原有测试定义。故障模板由固定、预注册的适配器生成，不用候选本身生成的规则判定成功。

### 4.2 次选：经审计的 τ³ DB 终态

只纳入满足以下条件的任务：

- 参考动作产生非初始 DB 哈希，或有非空、真正进入 reward basis 的环境/通信条件；
- 不在当前 issue #384 的已知 P0/P1 问题集合，除非固定提交已修复且重新审计；
- 注入后存在至少一条在同权限、同总调用预算内可完成的恢复路径；
- 用户模拟器、模型版本、温度、最大轮数在所有方法中一致。

主指标用最终 DB/环境断言成功；自然语言 judge 只作次要指标。

### 4.3 ToolMaze 只保留过程指标

可用指标：实际命中扰动、首次验证位置、重试/替代路径、重复调用、恢复后继续错误的比例、工具调用数和 token。官方 TSR/PRR/RC 可以原样保存，但不能单独支撑“真实任务完成”，原因是当前 `judge.py` 的 subset matching 只要求工具名集合和次数覆盖，并明确不检查顺序；部分路径还直接以“是否重试/是否停止”定义通过，评价规则与候选恢复行为同形。

## 5. 可控故障注入方式

建议先只实现两种，避免把 v001 变成故障大杂烩。

### F1：瞬时 silent no-op write（首要）

1. 运行器在影子状态中确认候选提出的 write 调用语法、权限和前置条件本来可成功。
2. 第一次命中时，不向真实 episode 状态提交副作用，但返回与正常成功响应相同的 JSON schema、状态字段和类型。
3. 不加入 `stale`、`corrupt`、`warning` 等显式词，不改变工具名和可见权限。
4. 正常 read-back 会显示状态未改变；同一 write 第二次调用正常提交。

它直接测试：智能体是否把“返回 success”当作已提交状态，还是在后续依赖动作前验证 postcondition。AppWorld/τ³ 的最终 DB 判定可独立抓住未恢复的 no-op。

### F2：瞬时 stale read（第二故障族）

1. 对第一次命中的状态读取，返回同一任务初始快照或此前合法快照；字段齐全、类型正确、实体标识合法。
2. 第二次读取返回当前真实状态；若存在公开的等价读取工具，也允许交叉验证。
3. 只改变一个对后续动作有因果影响的字段；不改无关装饰字段，不通过异常长度/额外日志泄漏故障。

只有当一个不访问隐藏真值的 oracle 恢复策略能在预算内通过最终测试时，样例才准入。若 stale 值无法从任何可见信息反证，它测的是猜测而不是恢复能力，应删除或改为“校准弃权”任务。

### 不建议首轮使用

- 永久语义污染且无替代工具：任务不可解，会把恢复能力与拒绝/弃权混在一起。
- 随机改任意数字：容易产生明显越界值，方法只学表面异常。
- 返回显式错误文本：退化成普通 retry 基准，越出 target problem。
- 用候选自身的置信度决定注入位置或错误值：使方法和测量同源。

## 6. 公平比较与预算契约

所有方法固定：同一 backbone/请求模型版本、同一用户模拟器（若有）、同一工具 schema、权限、可见历史、上下文上限、温度、停止规则、任务顺序和故障清单。每个 task × seed × fault payload 在运行前写入只供运行器读取的哈希清单，所有方法复用。

预算至少同时记录并约束：

- 总工具调用、额外验证调用、write 调用、read 调用；
- 大语言模型调用次数、输入/输出 token；
- 最大轮数和超时；
- 可取得的延迟与费用。

推荐比较：

1. Vanilla：原始智能体，无恢复控制器。
2. Blind Retry-1：每个成功 write 固定重试一次；检验“多一次调用”是否足够。
3. Random-B：在同样的额外验证预算 `B` 下随机选择状态转移验证；检验选择性本身。
4. Verify-Every-Write：每次 write 后 read-back；作为高成本强基线，报告成功—成本前沿；若调用数超过 `B`，另给预算裁剪版本。
5. Generic Reflection / Self-Consistency：获得与候选相同的大语言模型调用/token 预算，但不获得额外工具或错误提示。
6. DFSDT/ReAct@N：同总工具调用/模型调用成本的回溯搜索基线；ToolBench 文献中它是最接近的控制流对照。
7. Schema-only Postcondition Gate：只检查公开 schema/类型，不加入任务特定真值；预期抓不住 F1/F2，但能证明收益不是结构校验。
8. Candidate：只能使用与上述方法相同的任务、工具和返回；不得读取注入器、评价测试或影子状态。

主报告必须给成功—成本曲线，而不是只在候选多调用时比较 success。若 Verify-Every-Write 在相同或更低成本下吸收候选，候选没有独立方法价值。

## 7. 最小高信息量 Scratch / Recorded 方案

### Scratch A：注入器与终局分离（不调模型）

- AppWorld dev 选 4 个至少两步、包含状态写入的任务。
- 对每项回放：clean、F1、F2；检查故障返回 JSON schema 与 clean 一致、隐藏状态确实分叉、原生 evaluator 能抓住未恢复终局。
- 用一个手写、仅依赖公开 read-back 的 oracle 验证—重试策略确认每个 injected task 在 `B<=2` 额外工具调用内可解。
- 任一任务若 evaluator 不抓错、oracle 需隐藏状态、或返回带表面故障标志，立即剔除。

### Scratch B：ToolMaze 行为签名

- 固定 12 个 C2/C3 任务，各取 P0/P3/P4；运行 Vanilla、Blind Retry-1、Verify-Every-Write、Candidate。
- 只把 hit、retry、switch、abort、重复调用和 token/call cost 作为可信输出；官方 pass/PRR/RC 原样保存但标记为过程评价。
- 高信息量问题：Candidate 是否在 P3/P4 更早触发验证，且不是在 P0 全面增加验证；能否减少盲重试循环。

### Recorded Pilot：AppWorld dev 的真实终局

- Batch A：预注册 12 个符合准入条件的 dev 任务，clean/F1 成对；四个方法为 Vanilla、Random-B、Verify-Every-Write、Candidate，共 96 个 episode（每条件先 1 次）。
- 只有当 Candidate 至少产生两个 Vanilla 未恢复而它恢复的**终局成功**，且 clean 不出现系统性回退，才扩展 Batch B。
- Batch B：再加入 24 个未用于方法构造的 dev 任务；先跑 F1，再在机制仍成立时加入 F2。对结论敏感或不一致的 task × method 对重复 3 次，而不是一开始全量重复。
- 结构化保存：task/fault/seed manifest 哈希、实现 manifest、原始轨迹、工具返回前后值（仅 evaluator 侧）、最终测试、token/call/cost、超时和 provider 模型身份。

建议主指标：

- `Injected terminal success` 与 paired `Δsuccess(Fault-Clean)`；
- `Recovery given hit`，但 recovery 必须以最终测试成功定义；
- clean retention；
- 额外工具调用/token；
- verification precision（验证是否集中在真正注入点）；
- collateral-damage test failure；
- success—cost Pareto dominance。

Pilot 的作用是杀机制或确认值得实现，不支持论文级主张。

## 8. Formal / Review-support 前置

1. 冻结 AppWorld（首选）或 τ³ 的代码提交、包版本、数据版本和 SHA-256；建立 Run-local 隔离环境，不修改共享 Python。
2. 冻结候选、所有强基线、提示、工具 schema、最大轮数、预算和 fault manifest；测试集运行后不再调阈值。
3. 将 AppWorld 函数调用/MCP 服务置于候选不可读取数据库、ground truth、评价代码和故障清单的进程边界；禁用通用 shell/文件工具。
4. 对每个正式任务先做 evaluator-side oracle solvability 检查；oracle 不能成为候选可见工具或提示。
5. 做“无侧信道”检验：clean/F1/F2 的键、类型、错误码、显式状态、日志前缀和超时策略一致；若延迟不可完全一致，记录并做 latency-blind 重放。
6. 所有方法面对同一预注册 task × seed × payload；若 first-touch 导致方法命中不同工具，必须报告 hit-conditioned 指标和意向处理指标，不能只保留被候选命中的样例。
7. 正式集使用未参与实现和阈值选择的 AppWorld `test_normal`/`test_challenge`；只使用允许的总体评价，不看单任务隐藏报告调方法。
8. 至少 50 个实际命中且 oracle 可恢复的任务对，并做配对置信区间/置换或 bootstrap；随机 API 模型至少多 trial。样本数最终应由 Pilot 的配对方差再估计，不能把“50”当机械充分性。
9. τ³ 如进入 Formal：先审计固定提交的每个 reward basis，排除已知空条件任务；保存用户模拟器全部原始消息和重复方差。
10. 交付核心证据至少包含一项 AppWorld/τ³ 的原生外部终局；ToolMaze、LLM judge、人工轨迹标签都只能补充。

## 9. 泄漏与混杂风险

- **任务/测试泄漏**：AppWorld 的测试评价程序在本地可用，编码 shell 可能读取。必须用受限函数调用/MCP 服务，且 evaluator 在独立进程运行。
- **公开基准污染**：AppWorld、τ、BFCL、ToolBench 已公开较久。新生成且预注册的 fault timing/payload 可降低“记住 clean 解法”对恢复主张的解释力；仍需报告可能的任务污染。
- **注入器—方法同源**：若 Candidate 的规则直接来自同一批 fault template，收益可能是模板识别。dev 构造、hidden test fault template 和评价必须分离；至少留一个未见扰动家族。
- **表面侧信道**：字段缺失、异常 token、固定延迟、额外 metadata 会把语义检测变成格式检测。
- **方法相关命中**：first-touch 注入会因不同策略选择不同 victim；不能只比较被 Candidate 命中的轨迹。固定 tool-class rule，并同时报告 ITT 与 hit-conditioned。
- **预算不公平**：候选验证更多次、更多 token 或多一个模型时，必须给 Random-B/Retry/Reflection/Verify-All 等成本匹配基线。
- **用户模拟器方差**：τ³ 中不同对话可能掩盖故障效应；AppWorld 无在线大语言模型用户时更干净。
- **clean 能力混杂**：方法可能先改善一般规划，再看似改善故障恢复。必须有 clean pair 和 `Fault-Clean` 差分。
- **基础调用失败混杂**：如果模型在注入前就选错工具，无法归因到语义恢复。报告 perturbation hit rate，并在 oracle/预注册层保证目标调用可达。
- **评价同形**：ToolMaze/Failing Tools 的 required recovery action 与 Candidate 机制可能重合；外部终局主指标不得使用“是否执行了 Candidate 设计动作”。
- **合成外部效度**：silent no-op/stale read 是受控代理，不证明真实生产频率；主张限定为相同故障模型下的恢复能力。

## 10. 会导致 v001 直接 reframe/kill 的测量障碍

以下均是“杀当前测量/候选或重构问题”的条件，不是 Run-level No-Delivery：

1. **不可观测且不可恢复**：在不访问隐藏状态时，oracle 也无法在预算内区分 clean 与 semantic-fault；这时应把问题改为 calibrated abstention，或换成存在公开冗余/读回路径的任务。
2. **外部 evaluator 不抓错**：未恢复的 silent no-op 仍被判成功；应杀该 task/benchmark 载体，不能靠过程 rubric 补成终局。
3. **侧信道可完全解释收益**：移除异常格式/metadata 后 Candidate 优势消失；杀当前注入器与主张。
4. **强基线吸收**：Verify-Every-Write、Random-B 或 Blind Retry-1 在相同预算下达到相同/更高终局成功且 clean 不更差；杀 Candidate 的选择性机制或收缩为成本工程。
5. **只靠额外预算**：success 与总调用数单调一致，控制调用/token 后效果消失；不成立为独立方法贡献。
6. **方法在 clean 上系统性破坏正确轨迹**：恢复收益来自过度怀疑并造成大量无谓回滚/附带损害；除非能形成清楚的成功—成本 Pareto 改进，否则 reframe。
7. **真实命中率过低**：在预注册多步任务中，大多数运行在注入前失败或不触及 victim，无法测量目标机制；应换 backbone/task slice，而不是从命中样例中事后挑好结果。
8. **τ³ 用户模拟器噪声大于处理效应**：若重复方差吞没 paired fault effect，τ³ 降为补充域，正式核心转到 AppWorld。
9. **Formal 只能依赖 ToolMaze/LLM judge**：若 AppWorld/τ³ 适配器无法在当前资源下实现，v001 不应交付 Seed；应 reframe 到有确定性外部终局的相邻问题。
10. **最近工作完全覆盖**：若 Failing Tools/AgentNoiseBench 后续公开实现已包含同样的 selective verify/rollback 计算和独立终局，v001 必须做组件级 Prior Audit；无法形成 changed-computation 差异时杀当前方法谱系。

## 11. 建议给主研究者的下一步

优先在 AppWorld dev 上实现一个最薄的函数调用/MCP response adapter，只做 F1 silent no-op write，并先完成 Scratch A 的四项 evaluator/oracle 校验。该步骤能最快回答最大的测量不确定性：“方法是否能在没有外部真值时，通过普通读回动作恢复，并被独立终局确认”。在此之前，不值得实现复杂候选，也不应启动固定 Reviewer。

若 AppWorld 的受限函数调用接口无法安全隔离评价文件，再转 τ³ 的经审计 DB-write 子集；不要先转 ToolMaze，因为它的当前官方 pass 不是足够独立的终局。

## 12. 证据与一级来源

冻结知识库定位：

- `knowledge_base/cards/paper/paper-tau-bench.md`；`ev-p007-terminal-state-evaluation`、`ev-p007-repeat-reliability-collapse`
- `knowledge_base/corpus/reads/P007/reconciliation.md`
- `knowledge_base/cards/paper/paper-p047.md`（τ² 双控制与环境断言）
- `knowledge_base/cards/paper/paper-p066.md`；`knowledge_base/corpus/reads/P066/reconciliation.md`（BFCL）
- `knowledge_base/cards/paper/paper-p005.md`；`knowledge_base/corpus/reads/P005/reconciliation.md`（ToolBench/DFSDT）
- `knowledge_base/cards/paper/paper-p037.md`（ToolSandbox）
- `knowledge_base/cards/paper/paper-p040.md`（环境真值揭示 false success）
- `knowledge_base/cards/paper/paper-p074.md`（结构 contract 无法保证丰富语义真值）

在线一级来源（访问于 2026-08-13）：

- AppWorld 论文与官方仓库：<https://arxiv.org/abs/2407.18901>；<https://github.com/StonyBrookNLP/appworld>
- τ³-bench 官方仓库、评价说明和当前评价缺口：<https://github.com/sierra-research/tau2-bench>；<https://github.com/sierra-research/tau2-bench/blob/main/docs/evaluation.md>；<https://github.com/sierra-research/tau2-bench/issues/384>
- ToolMaze 论文、官方仓库和判定代码：<https://arxiv.org/abs/2606.05806>；<https://github.com/Zhudongsheng75/ToolMaze>；<https://github.com/Zhudongsheng75/ToolMaze/blob/main/evaluation/core/judge.py>
- BFCL 论文/官方实现/当前榜单：<https://proceedings.mlr.press/v267/patil25a.html>；<https://github.com/ShishirPatil/gorilla/tree/main/berkeley-function-call-leaderboard>；<https://gorilla.cs.berkeley.edu/leaderboard.html>
- ToolBench 与 StableToolBench 官方仓库：<https://github.com/OpenBMB/ToolBench>；<https://github.com/THUNLP-MT/StableToolBench>
- Failing Tools（OpenReview 论文入口）：<https://openreview.net/pdf?id=j7YsSnA64D>
- AgentNoiseBench 论文与当前官方仓库状态：<https://arxiv.org/abs/2602.11348>；<https://github.com/keven-cyber/agentnoisebench>
- Tools Fail：<https://aclanthology.org/2024.emnlp-main.790/>；<https://arxiv.org/abs/2406.19228>

