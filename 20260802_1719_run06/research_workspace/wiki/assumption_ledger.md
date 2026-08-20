# 假设账本

本账本只属于 Run `20260802_1719_run06`，不进入共享论文知识库。事实、实验结果与尚未证实的前提分开记录。

## A001：范围胶囊对运行时可见

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A001`
- assumption: 工具运行时能够取得分页、时间窗、归档、权限和截断等范围元数据，即使这些字段不直接暴露给语言模型。
- source: 工具系统设计推断；本轮模拟器构造。
- used_by: `candidate_v001.md` 的主张条件化覆盖门；`scope_closure_probe.py`。
- risk: 若运行时也不知道返回覆盖范围，方法不能证明否定主张，只能一律降级为未知。
- how_to_verify: 在 ToolBench、τ2-bench 或真实开放应用程序接口样本中统计可恢复的范围字段比例，并注入缺失字段消融。
- status: `unverified`
- related evidence: ToolGate P074 说明固定后置条件依赖接口模式；其缺少模式时采用恒真后置条件，不能证明本假设普遍成立。
- last_updated: `2026-08-02`

## A002：范围胶囊真实且未被工具载荷污染

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A002`
- assumption: 范围元数据由可信运行时或连接器生成，能够真实描述本次观察范围，而不是由不可信工具正文任意声明。
- source: 方法安全前提。
- used_by: 否定覆盖包含检查。
- risk: 伪造的“分页完成”或“组织范围”会让覆盖门错误许可全局否定。
- how_to_verify: 将范围胶囊绑定到调用参数、响应头和连接器身份；对正文伪造同名字段做对抗测试。
- status: `unverified`
- related evidence: ContractBench（arXiv:2605.17281）说明中间观察工件的时效与字节完整性会失效，但处理对象不同。
- last_updated: `2026-08-02`

## A003：覆盖闭包期间存在一致快照

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A003`
- assumption: 多页或多范围查询要么读取同一快照，要么其版本变化可以被检测并触发重试。
- source: 数据库分页与动态工具语义推断。
- used_by: 完整否定覆盖证书。
- risk: 闭包期间新增目标记录会使“未发现”证书过时。
- how_to_verify: 在连接器中记录快照或版本标识；注入分页间并发写入并测试证书失效。
- status: `unverified`
- related evidence: ToolGate P074 明确把动态数据状态列为限制；STALE P030 说明识别更新不保证下游应用。
- last_updated: `2026-08-02`

## A004：主张范围与极性可正确编译

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A004`
- assumption: 系统能把候选自然语言主张解析为存在性/否定/全称极性、目标谓词和实体/时间/权限范围，错误率足以支持运行时使用。
- source: 方法内尚未实现的自然语言编译环节；当前实验直接使用任务生成器中的结构化范围。
- used_by: 从 `Q_tool` 到 `Q_claim` 的关键方法变化。
- risk: 当前结果可能只证明结构化元数据上的确定性规则，不能证明自然语言智能体端到端有效。
- how_to_verify: 构建独立人工标注的主张范围集，报告解析精确率，并对解析错误做端到端消融。
- status: `unverified`
- related evidence: 当前两个 22 任务实验没有验证自然语言范围编译。
- last_updated: `2026-08-02`

## A005：合成失效具有现实代表性

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A005`
- assumption: 默认时间窗、隐藏归档、分页后页和权限子集是现实工具代理中足以频繁影响全局否定结论的失效来源。
- source: 公开接口常见设计、ToolGate 限制与本轮研究推断；尚无真实轨迹频率证据。
- used_by: CCF-B 方法潜力判断与扩大价值。
- risk: 若真实基准很少要求全局否定或范围元数据始终显式，当前高增益会是合成构造特例。
- how_to_verify: 在 AppWorld、ToolSandbox、τ2-bench 和真实深度研究轨迹中标注无范围否定频率及错误贡献。
- status: `unverified`
- related evidence: P040 证明虚假成功普遍，但没有把原因定位为无范围否定；P074 证明合法空返回可能通过后置条件，但没有报告下游否定错误。
- last_updated: `2026-08-02`

## A006：独立终局判定不与方法同源

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A006`
- assumption: 实验标签来自隐藏数据库中是否真实存在目标记录，而不是由覆盖门的许可规则生成。
- source: `scope_closure_probe.py` 的数据生成器与评价器。
- used_by: 核心主张独立验证资格。
- risk: 若标签由覆盖规则直接定义，100% 结果只是构造闭环。
- how_to_verify: 检查输出中的隐藏记录、标签计算和模式实现；对标签独立重算。
- status: `supported`
- related evidence: `closure_qwen3_8b_22.json`、`closure_qwen2_5_7b_22.json` 中保存了全部隐藏记录与逐任务标签。
- last_updated: `2026-08-02`

## A007：文字提醒是充分的提示基线

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A007`
- assumption: 当前一句“合法返回仍可能是局部范围”的系统提醒代表了合理的无工具文字自检基线。
- source: 本轮实验设计判断。
- used_by: “确定性门优于提示”对比。
- risk: 更强的分步提示、示例或独立裁判可能取得更好结果，使当前对比偏弱。
- how_to_verify: 增加等词元分步核对、少样本示例和独立语言模型裁判，同时保持工具预算一致。
- status: `unverified`
- related evidence: Qwen3-8B 提醒无改善；Qwen2.5-7B 提醒把 18/22 个任务退为未知，说明提示效应具有模型依赖性。
- last_updated: `2026-08-02`

## A008：确定性闭包规则在模拟器内正确

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A008`
- assumption: 对本轮结构化任务，正面见证、连续全范围分页和权限不足三类证书与隐藏数据库语义一致。
- source: 实现与逐任务输出。
- used_by: 实验结果解释。
- risk: 实现错误会制造虚假满分。
- how_to_verify: 对每类条件手工重算；增加属性测试，随机改变记录数、页大小、时间和权限。
- status: `supported`
- related evidence: 两个模型各 22 个任务上，可访问任务均为 100% 正确，权限不足均返回未知；仍需更广属性测试。
- last_updated: `2026-08-02`

## A009：成本对比支持工具效率优势

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A009`
- assumption: 主张条件化覆盖门在平衡测试分布下比始终全量扫描使用更少的工具调用。
- source: 候选早期直觉。
- used_by: 早期效率叙事。
- risk: 错误声称效率优势会夸大方法价值。
- how_to_verify: 直接比较逐条件和总体工具调用。
- status: `contradicted`
- related evidence: 两个 22 任务实验中覆盖门平均 3.00 次工具调用，全量扫描为 2.82 次；覆盖门仅在首页已有见证时调用更少，但模型输入词元约少 46%。
- last_updated: `2026-08-02`

## A010：没有同构最近工作

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A010`
- assumption: 截至 2026-08-02，尚无工作把工具调用范围胶囊与下游主张范围做确定性包含检查，并采用正面见证/否定覆盖的不对称许可规则。
- source: 共享知识库检索与开放网络关键词检索。
- used_by: 新颖性判断。
- risk: 漏检同构工作会使方法新意失效。
- how_to_verify: 继续沿 ToolGate、ContractBench、证据充分性、证明携带动作和数据库查询完备性引用链做最近先行检索。
- status: `unverified`
- related evidence: 已核对 ToolGate、ContractBench、Near-Miss、过程感知评估、CaRT、Eval-RAR、证明携带动作；目前均只部分相邻。
- last_updated: `2026-08-02`

## A011：固定模式契约不会改变本轮载荷

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A011`
- assumption: 本轮所有初始工具载荷结构合法且状态为成功，因此只检查字段和类型的固定后置条件会全部接受，行为等同原始条件。
- source: 模拟器构造与 ToolGate P074 的模式语义。
- used_by: 与固定工具契约的差异说明。
- risk: 若真实 ToolGate 会动态生成更强语义约束，则当前“等同原始”对照偏弱。
- how_to_verify: 实现官方 ToolGate 合同生成/验证逻辑或取得其代码，在同一载荷上复跑。
- status: `supported`
- related evidence: 初始载荷均为非空或空的合法 `status/items` 对象；P074 说明模式允许空列表时不强制非空。
- last_updated: `2026-08-02`

## A012：真实工具能执行覆盖闭包

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A012`
- assumption: 对足够多的目标工具，系统可以通过继续分页、扩大时间窗、包含归档或切换授权范围完成主张所需覆盖。
- source: 本轮模拟器能力；现实接口推断。
- used_by: 从诚实未知提升到任务成功的价值主张。
- risk: 若大多数工具无法扩大覆盖，方法主要成为保守拒绝器而非修复器。
- how_to_verify: 在多种真实接口上统计每种缺口的可修复比例，并把不可修复任务单独报告。
- status: `unverified`
- related evidence: 合成可访问任务全部可闭包；权限任务不可闭包并按预期返回未知。
- last_updated: `2026-08-02`

## A013：多维边际覆盖足以构成联合覆盖

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A013`
- assumption: 分别证明实体、时间、归档、权限和分页等每个维度的边际范围被覆盖，就足以证明多维主张集合已被观察联合覆盖。
- source: `seed_v001.md` 中“各维观察范围的并集覆盖”的非形式化表述可能隐含这一假设。
- used_by: 一般否定或全称主张的覆盖证书声音性。
- risk: 不同观察的维度相关性会产生未观察空洞；每个边际都完整时，联合笛卡尔空间仍可能不完整，从而错误许可否定。
- how_to_verify: 把每次观察表示为多维联合集合，证明 `S_claim` 包含于兼容观察联合范围之并集；加入“部门甲×近期、部门乙×早期”等边际完整但联合有洞的反例测试。
- status: `contradicted`
- related evidence: Reviewer 2 与 Reviewer 3 独立提出同一反例；当前单一组织范围模拟器没有覆盖这种多维交叉组合。
- last_updated: `2026-08-02`

## A014：当前实验直接隔离了主张条件化的独立优势

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A014`
- assumption: 当前 22 个任务足以证明 `Q_claim` 随不同候选主张范围变化所带来的优势，且该优势不能由任务专用固定规则实现。
- source: 方法新意的早期实验解释。
- used_by: 相对固定动态契约和查询规划器的独立方法价值判断。
- risk: 所有正式任务的主张范围基本恒定，当前门可以退化为“首页有见证则通过，否则全扫”，因此没有直接隔离主张条件化变化。
- how_to_verify: 保持完全相同的观察载荷，成对改变局部/时间段/全历史/归档/权限/组织范围和量词，再与任务条件化动态契约及同预算规划器比较。
- status: `contradicted`
- related evidence: Reviewer 3 指出当前任务范围恒定；安全全扫取得相同正确性且平均调用更少。
- last_updated: `2026-08-02`

## A015：十八次无证书否定都是独立事实错误

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A015`
- assumption: 原始条件中的 18 次无证书错误否定均可由隐藏数据库真值独立判定为事实错误。
- source: 聚合安全指标可能引出的过强解释。
- used_by: 独立核心证据成熟度判断。
- risk: 把方法规范违规全部当作事实错误会使评价规则与方法规则重新同源并夸大独立证据。
- how_to_verify: 分开报告事实错误否定、事实正确但未认证否定、错误许可、未知与认证正确否定。
- status: `contradicted`
- related evidence: 正式结果只有 14 次事实性假阴性，却有 18 次无证书错误否定；三位 Reviewer 均要求区分事实真值指标与证书规范指标。
- last_updated: `2026-08-02`

## A016：连接器级查询签名足以绑定具体联合单元

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A016`
- assumption: 连接器、操作名、认证主体和范围模式相同，就足以证明一张空页面来自声明的具体实体×时间×归档单元。
- source: v003 来源身份设计隐含的实现假设。
- used_by: `seed_v003.md` 的来源绑定页链声音性。
- risk: 实际请求单元 A 的空响应可被标注为 B；因为没有记录级单元可交叉检查，B 可能被错误判为完整。
- how_to_verify: 构造“实际请求 A、观察标注 B”的空页面，并要求生产求值器与证书验证器均失败关闭。
- status: `contradicted`
- related evidence: v004 正式尝试 `request-bound-counterexamples-v004` 中 `empty_page_requested_for_a_but_labelled_b` 返回 `UNKNOWN`；该反例直接说明 v003 的连接器级签名不足。
- last_updated: `2026-08-02`

## A017：适配器如实记录实际出站请求

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A017`
- assumption: 观察中的规范请求载荷由可信适配器根据实际出站请求生成，且不会把请求 A 与响应 A 同时伪装成请求 B 与响应 B。
- source: v004 方法的信任边界；系统设计推断。
- used_by: `seed_v004.md` 的每单元请求绑定、错误单元标注检测与覆盖证书。
- risk: 若适配器可同时伪造请求记录和响应元数据，内核只能验证内部一致性，不能恢复外部事实。
- how_to_verify: 在真实连接器层从传输拦截或可信调用日志独立采集请求字节，与适配器规范载荷逐次比对；对适配器伪造做故障注入。
- status: `unverified`
- related evidence: v004 的 26 项反例证明不一致请求绑定会被拒绝，但实验使用受控适配器，未独立观测真实网络请求。
- last_updated: `2026-08-02`

## A018：规范请求序列化覆盖全部语义参数

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A018`
- assumption: `connector_id`、操作、认证主体、实体、时间桶、归档状态、游标、快照、适配器版本、范围模式版本和序列化版本包含了当前接口中会改变响应语义的全部参数。
- source: v004 请求规范设计。
- used_by: 请求载荷摘要相等即视为同一页请求的判断。
- risk: 若遗漏排序、区域、租户、隐式默认过滤器或服务器特性开关，不同语义请求仍可能拥有相同摘要。
- how_to_verify: 为每个真实连接器建立参数完备表，从实际传输请求生成规范载荷；逐个改变参数并检查摘要与证书是否失效。
- status: `unverified`
- related evidence: 当前三个本地夹具只使用已列出的联合单元、游标与快照参数。
- last_updated: `2026-08-02`

## A019：第二条证书验证路径等价于外部独立核验

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A019`
- assumption: 不调用生产求值器和生产追踪器的第二条实现路径，可以被称为对原始连接器事实的独立外部验证。
- source: v003 文案可能引出的过强解释。
- used_by: 证书有效率与实现独立性叙事。
- risk: 两条路径仍共享数据类型、观察摘要和同一规范；称为外部独立会夸大证据强度。
- how_to_verify: 使用独立采集的原始请求/响应日志、单独实现的解析器和盲化证书语料复核。
- status: `contradicted`
- related evidence: v004 测试证明第二路径不调用生产 `evaluate_claim()`，但没有独立采集原始连接器传输事实；因此文案收紧为“第二实现路径的归一化观察级复核”。
- last_updated: `2026-08-02`

## A020：v004 在干净夹具上保持 v003 的任务语义与成本

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A020`
- assumption: 给定请求载荷与标注单元一致的干净适配器输入，新增请求绑定只收紧证据合法性，不改变 v003 的决定、调用成本、正确性或错误提交。
- source: v004 回归目标。
- used_by: v004 相对 v003 的兼容性判断。
- risk: 若改造意外改变调度或证书许可，主实验指标不可直接继承。
- how_to_verify: 对 26,460 行逐行比较主张、预算、方法、决定、调用数、正确性与错误提交。
- status: `supported`
- related evidence: 正式尝试 `request-bound-joint-coverage-756x5-v004` 与 v003 对应正式尝试的 26,460 行在七个字段上零差异。
- last_updated: `2026-08-02`

## A021：本地反例与半真实夹具足以估计真实连接器收益

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A021`
- assumption: 26 项人工反例和三个本地半真实夹具的安全性、回答率与调用成本可以直接外推到真实工具型大语言模型智能体。
- source: 潜在的实验外推。
- used_by: CCF-B 扩大价值判断。
- risk: 真实适配器、隐式参数、授权变化、网络重试与自然语言范围编译可能显著改变效果。
- how_to_verify: 在至少两个真实连接器和一个公开工具智能体基准上，使用独立标注的自然语言主张与传输级请求日志复现。
- status: `unverified`
- related evidence: v004 提供实现声音性反例和 756 任务模拟回归，没有真实连接器或端到端自然语言实验。
- last_updated: `2026-08-02`

## A022：先按外层标签过滤不会隐藏载荷冲突

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A022`
- assumption: 先按观察外层来源、单元或快照把页面分桶，再检查桶内规范请求载荷，不会把实际指向当前期望请求的冲突页面路由到桶外。
- source: v004 生产追踪器与第二验证路径的筛选顺序。
- used_by: `seed_v004.md` 中“任何已知绑定冲突优先于见证并失败关闭”的核心主张。
- risk: 外层来源被重标、载荷仍指向当前请求的见证页可被忽略；合法空页随后错误认证存在假或全称真。
- how_to_verify: 在冻结 v004 原实现中构造合法空页与“外层来源 T、载荷来源 S”的同请求同游标见证页，并检查生产决定与证书验证。
- status: `contradicted`
- related evidence: 三名 v004 Reviewer 独立提出同一最小反例；工作台 `v004-outer-label-bypass-reproduction.json` 复现 `FALSE`、联合范围覆盖、证书有效且错误认证提交为真，文件 SHA-256 `f1b3878937e474996b890090638234f9e84b580c65b402ebff5133dd0c47752b`。
- last_updated: `2026-08-02`

## A023：响应页面与所记录请求正确关联

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A023`
- assumption: 每个观察中的响应页面确实由同一观察记录的出站请求产生，包括并发请求、重试、缓存命中和响应乱序情形。
- source: v004 Reviewer 3 对适配器信任边界的细分。
- used_by: 请求绑定摘要能够支撑页面范围结论的条件声音性。
- risk: 即使请求载荷记录完全真实，若响应 B 被错误附到请求 A，内核仍可能为 A 认证错误否定。
- how_to_verify: 在可信传输层绑定交换标识、请求原始字节摘要和响应原始字节摘要；注入并发乱序、重试复用与缓存错配。
- status: `unverified`
- related evidence: 当前本地连接器同步生成观察，没有覆盖请求—响应错配；该前提不能由 v004 的请求载荷相等测试推出。
- last_updated: `2026-08-02`

## A024：完整键相关并集足以关闭跨表示重标绕过

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A024`
- assumption: 在任何路由与见证之前，只要取“外层完整键相关、载荷完整键相关或单侧来源/快照下记录相关”的并集，就可以阻止所有跨表示冲突页面移出当前请求桶。
- source: v005 方法内核与正式攻击矩阵。
- used_by: `seed_v005.md` 的适配器声明观察级失败关闭主张。
- risk: 不同表示可以在不同坐标分别偏离，使任何单个完整键都不相关；记录页随之在一致性检查前被漏掉并产生错误认证。
- how_to_verify: 令外层键提供期望来源但错误快照，载荷键提供期望快照但错误来源，两侧请求单元均在范围外、记录单元在范围内；检查存在假旧证书是否仍有效。
- status: `contradicted`
- related evidence: 三名 v005 Reviewer 均指出组合闭包不足；冻结 v005 复现 `v005-cross-coordinate-split-reproduction.json` 返回 `FALSE`、证书有效、冲突页不在审计承诺中，结果 SHA-256 `83f66e727cd4aca79d94b3649792d718a44bdbadc638665145d25954236f94cd`。
- last_updated: `2026-08-03`

## A025：求值器收到的相关观察集合是完整的

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A025`
- assumption: 证书生成与验证接收到可信采集层提供的完整相关观察多重集，调用者不会在进入内核之前删除冲突页面。
- source: v005 `audit_observation_digests` 的能力边界。
- used_by: 证书不能通过省略或重标已知冲突页面保持有效的主张。
- risk: 若攻击者能先删页再让求值器生成新证书，多重集摘要只能承诺删减后的输入，无法证明历史完整性。
- how_to_verify: 将证书输入根绑定到只追加透明日志或可信传输捕获的批次根；验证器独立取得批次根，而不是接收调用者任选的观察列表。
- status: `unverified`
- related evidence: v005 测试证明旧干净证书在加入重标冲突页后失效，但没有可信外部日志证明输入集合全局完整。
- last_updated: `2026-08-02`

## A026：严格跨表示复核的宿主计算成本可以忽略

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A026`
- assumption: 即使使用有界载荷解析缓存，严格预检和重算相关观察多重集也不会显著增加当前原型的宿主运行时间。
- source: 只报告工具调用成本可能隐含的实现假设。
- used_by: v005 效率解释。
- risk: 只展示工具调用数会掩盖实际系统开销，并使效率主张不完整。
- how_to_verify: 在相同 26,460 回合正式运行上比较 v004 与 v005 的执行时长，并在缓存解析结果后重新测量。
- status: `contradicted`
- related evidence: v004 正式主尝试约 167.26 秒；v005 r2 正式主尝试约 270.85 秒，缓存后的当前原型约慢 1.62 倍。未缓存 v005 尝试约 639.97 秒。该差异不是工具调用成本。
- last_updated: `2026-08-02`

## A027：逐坐标可能相关包络关闭跨坐标分裂

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A027`
- assumption: 对每个来源身份坐标分别在外层键与载荷键间取析取，对快照在两表示间取析取，对范围在外层单元、载荷单元与记录单元间取析取，再将三个坐标组取合取，可以在保留自洽异源页可忽略性的同时捕获跨坐标分裂。
- source: v006 逐坐标可能相关包络。
- used_by: `seed_v006.md` 的本地条件声音性主张。
- risk: 若实现仍要求任一完整表示先匹配，来源、快照和范围可分散在两侧并绕过一致性检查。
- how_to_verify: 对七个来源身份坐标分别构造两种镜像分裂，交叉存在/全称、两种输入顺序、范围外请求与范围内记录，并检查独立构造真值、生产决定、第二路径证书和审计摘要。
- status: `contradicted`
- related evidence: v006 的 150 项面板仅覆盖“每个坐标至少有一侧等于声明值”的构造，未覆盖两侧表示版本均不同但语义来源相同的页面。三名 v006 Reviewer 指出版本字段可成为相关性硬门；冻结 v006 复现 `workbench_v006/v006-normalization-version-gate-bypass.json` 在声明 v2/B、干净 v2/B、隐藏外层 v1/B、载荷 v1/A、记录 B 时返回 `FALSE`、证书有效、隐藏页不在审计摘要中，而独立世界真值为 `TRUE`，结果 SHA-256 `005b0208135ba93a370807efbc6e087802b40724476338606d2ccf08c4b76d61`。
- last_updated: `2026-08-03`

## A028：连接器语义等价请求具有唯一规范键

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A028`
- assumption: 在给定 `semantic_normalization_version` 下，所有会得到同一响应语义的连接器请求都映射为唯一的来源身份、范围单元、游标和快照键；大小写、统一码、端点、默认参数与版本别名不会产生多个自洽键。
- source: v005 Reviewer 2、3 指出的规范 JSON 字节唯一性与连接器语义唯一性差异。
- used_by: 自洽异源页可安全忽略、两键相等代表同一请求语义的条件声音性。
- risk: 若语义等价请求可映射为不同键，实际属于当前主张的冲突页可能被当作真正异源页忽略。
- how_to_verify: 为每个真实连接器建立语义规范化表，枚举大小写、统一码、别名、缺省参数和版本等价类；要求等价请求键相同、非等价请求键不同，并由传输级请求响应对复核。
- status: `unverified`
- related evidence: v006 已把 `semantic_normalization_version` 纳入来源身份、规范载荷和证书绑定，并测试版本变异会使证书失效；本地夹具只声明 `fixture-semantic-normalization-v1`，没有验证真实连接器映射的单射性。
- last_updated: `2026-08-03`

## A029：非规范载荷全局失败关闭优先于无关页可用性

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A029`
- assumption: 在没有独立可信路由包络时，把任何已保留、已认证但不能规范解析的载荷视为当前批次中所有主张的冲突，可以避免解析失败掩盖相关记录；代价是确实异源的非规范页也会污染无关主张。
- source: v006 对 Reviewer 3 非规范载荷组合分支的修复。
- used_by: 无有效载荷键时不产生错误认证的规则。
- risk: 若选择忽略无法解析且外层看似无关的页，载荷真实语义和范围内记录可能被隐藏；若全局污染，真实系统可用性可能显著下降。
- how_to_verify: 同时构造“范围外请求＋范围内记录＋非规范载荷”和“真正异源、范围外、非规范载荷”两类页面，检查前者失败关闭且后者明确记录可用性损失。
- status: `supported`
- related evidence: `coordinate-closed-counterexamples-r3-v006` 同时覆盖存在/全称、两种顺序、旧证书隐藏和真正异源非规范对照；所有相关用例返回 `UNKNOWN`，对照项显式记录可用性成本。
- last_updated: `2026-08-03`

## A030：缓存不可变派生结果不改变干净行为

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A030`
- assumption: 对冻结观察的来源键、规范载荷解析、摘要及同次求值预检结果做缓存和复用，只消除重复计算，不改变决定、调用成本、正确性、证书有效性、证明类型或理由。
- source: v006 两次正式大规模超时后的性能修复。
- used_by: v006 最终实现的性能与回归解释。
- risk: 错误的缓存键或跨主张复用会让相关性结果串扰，形成行为变化或错误证书。
- how_to_verify: 用与 v005 完全相同的种子、世界、预算和方法，对 26,460 行逐行比较配置与 13 个行为字段；另重新执行攻击面板和单元测试。
- status: `supported`
- related evidence: 正式尝试 `v005-v006-clean-regression-v006` 报告 26,460 行行为差异 0、配置差异 0；最终实现的 `coordinate-closed-counterexamples-r3-v006` 为 150/150，`kernel-tests-41-r3-v006` 为 41/41。同配置 Harness 时长由 v005 的 270.85 秒降至 v006 的 39.13 秒。
- last_updated: `2026-08-03`

## A031：响应内容、记录解码与页面元数据忠实反映连接器事实

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A031`
- assumption: 对每个已经和出站请求正确关联的响应，适配器对记录内容、记录所属联合单元、快照、游标、终止、权限和截断状态的解码忠实反映实际连接器响应；不会生成内部自洽但事实错误的阳性记录或错误完整页面。
- source: v006 三名 Reviewer 对响应忠实前提缺口的共同意见；A017 与 A023 尚未覆盖响应内容和解码语义。
- used_by: v007 从自洽页面的记录见证或完整空页链推出外部主张真假的条件声音性。
- risk: 若适配器可把错误租户记录解码为当前单元的阳性记录，或把未终止页面标为终止，v007 的全局内部一致性防火墙仍可能接受该自洽输入并认证错误外部结论。
- how_to_verify: 在可信传输层保存脱敏原始响应摘要与交换标识，由独立解码器逐项复核记录归属、记录谓词、快照、游标、终止、权限和截断元数据；注入跨租户响应、缓存错配、乱序、错误终止和错误权限故障。
- status: `unverified`
- related evidence: v008 正式尝试 `real-connector-response-attestation-v008` 保存了 GitLab 与 Crossref 各一次原始 HTTP 响应；同一进程内两个独立投影函数对每个响应各解码 5 条同序记录，承诺重算均一致，删除、注入、改变终止和改变权限的 8/8 个变异均被检测。但它不是独立传输捕获、密码学透明日志或提供方事实真实性证明，也未穷举真实分页、快照、权限与截断行为，所以本假设仍为未验证。
- last_updated: `2026-08-03`

## A032：全局内部一致性检查先于语义路由可关闭已表示的重标绕过

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A032`
- assumption: 对所有保留且带证明的观察，先检查规范载荷可解析、外层键等于载荷键、每条记录单元等于载荷请求单元，再进行任何语义相关性筛选，可使已表示出的跨来源、快照、单元和版本重标冲突无法被路由到审计集合外。
- source: v007 全局内部一致性防火墙。
- used_by: v007 的观察级失败关闭主张。
- risk: 全局检查会让真正异源但内部损坏的页污染无关主张，并增加摘要和验证成本；它仍不能识别 A031 所述的内部自洽外部错误。
- how_to_verify: 复跑 v006 版本门绕过、共同错误鉴权主体、七来源坐标分裂、范围外请求与范围内记录、非规范载荷、两种量词、两种顺序和旧证书重放；同时保留自洽真正异源对照。
- status: `supported`
- related evidence: 正式尝试 `global-coherence-counterexamples-v007` 的 166/166 个原始案例通过，错误认证提交 0；`kernel-tests-47-v007` 为 47/47。v006 原始版本门构造对存在与全称、两种顺序均返回 `UNKNOWN`，对应旧证书均被拒绝。
- last_updated: `2026-08-03`

## A033：语义来源与表示元数据分离能阻止版本字段充当相关性硬门

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A033`
- assumption: 先用连接器、查询语义和鉴权主体判断语义来源，再对语义相关页检查范围模式、适配器、语义规范化和请求序列化四类表示元数据，可以让表示错配产生 `UNKNOWN` 而不是被静默忽略。
- source: v007 语义投影与表示兼容性规则。
- used_by: v007 对规范化版本硬门绕过的修复。
- risk: 连接器、查询签名或鉴权主体若本身不是稳定的规范语义标识，仍可能把真实相关页归为异源；该残余风险由 A018、A028 和 A031 约束。
- how_to_verify: 对四类表示字段逐项构造自洽、同语义来源、同快照、同声明单元的错配页；要求生产求值与独立验证均失败关闭，并检查干净输入逐行不回归。
- status: `contradicted`
- related evidence: v007 Reviewer 构造了范围模式 v1 的原始单元 B1 与 v2 的 B2 映射到同一语义单元 B 的自洽反例。v007 在检查表示错配前先用原始单元做相关性路由，因 B1 不等于声明的 B2 而静默忽略隐藏阳性页，错误认证 `FALSE`。v008 的 180 项正式攻击面板把该构造扩展到存在/全称、两种顺序和旧证书重放并验证旧规则不安全、新全局表示门返回 `UNKNOWN`；因此 v007 的这条机制假设本身已被反驳。
- last_updated: `2026-08-03`

## A034：全局审计摘要完整承诺传入的保留观察多重集

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A034`
- assumption: v007 的“保留且带证明”过滤足以支持“证书完整承诺求值器实际收到的观察多重集”的对外表述，因此加入任何新收到的观察后旧证书都会失效。
- source: v007 证书模式 7 的全局审计规则。
- used_by: 旧证书不能隐藏后加入页面的输入完整性主张。
- risk: 未带证明的观察若在摘要前被跳过，调用者可用一个布尔状态把新冲突移出承诺；调用前删页或采集层漏页仍另属于 A025 的未验证风险。
- how_to_verify: 对自洽异源页、内部冲突页和非规范页分别执行加入前后证书重放，检查旧证书拒绝且新证书的审计摘要包含全部保留观察。
- status: `contradicted`
- related evidence: v007 只遍历 `attested=true` 的观察；加入 `attested=false` 的冲突观察不会进入全局摘要，也不会使旧证书失效。v008 正式 180 项攻击面板和 55 项测试均包含该反例、证明状态切换与旧证书重放，确认 v007 的完整性表述不成立。A025 仍保持 `unverified`。
- last_updated: `2026-08-03`

## A035：全局表示同质门先于全部语义坐标路由

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A035`
- assumption: 在当前可信批次模型下，对每个实际收到的观察先要求范围模式、适配器、语义规范化版本和请求序列化版本全部等于主张版本，再进行查询、鉴权、快照或原始单元路由，可以关闭版本化单元编码及其他表示字段造成的相关性硬门绕过。
- source: v007 Reviewer 的 B1/B2 同语义单元反例与 v008 的保守修复。
- used_by: v008 对已收到批次中表示错配页面的失败关闭主张。
- risk: 任一真正无关但版本不同的页面也会污染当前主张，形成明显可用性和拒绝服务成本；该规则不证明跨版本语义等价关系，只拒绝混合表示。
- how_to_verify: 构造不同表示版本、不同原始单元但同语义单元的存在/全称反例，并让表示错配页同时在查询、鉴权、快照和单元上异源；要求所有路径在这些字段路由前返回 `UNKNOWN`，同时逐行比较干净投影输入与行为。
- status: `supported`
- related evidence: 正式 `homogeneous-attested-counterexamples-v008` 为 180/180、错误认证提交 0，`kernel-tests-55-v008` 为 55/55；`v007-v008-projected-clean-regression-v008` 对 26,460 行报告投影输入摘要差异 0、配置差异 0、行为差异 0。
- last_updated: `2026-08-03`

## A036：所有实际收到的观察必须进入审计，未带证明即失败关闭

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A036`
- assumption: 对求值器实际收到的每个观察先纳入有序多重集摘要并检查证明状态；`attested=false` 不可被忽略，而必须使当前主张 `UNKNOWN`，证明状态变化也必须改变观察摘要并使旧证书失效。
- source: v007 Reviewer 对收到、保留、带证明集合混淆的反例。
- used_by: v008 的批次内输入承诺与旧证书重放规则。
- risk: 它仍只覆盖调用者实际传入内核的集合；传入前省略与采集层漏页继续由 A025 约束。单独的布尔值也不是密码学证明，必须由外部可信边界验证。
- how_to_verify: 对未带证明冲突、证明状态翻转、观察加入前后旧证书重放逐项测试，并核对全局审计摘要和完整观察摘要是否变化。
- status: `supported`
- related evidence: 正式 180 项攻击面板与 55 项测试覆盖未带证明观察、状态切换和旧证书，均失败关闭且错误认证提交 0；v008 证书模式 8 对全部传入观察摘要排序后承诺。
- last_updated: `2026-08-03`

## A037：响应承诺可检测本地解码内容和关键分页语义的篡改

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A037`
- assumption: 若可信边界为规范请求、完整有序记录、下一游标、状态、权限完整性和静默截断标志提供正确响应承诺，则生产观察中删除或注入记录、改变终止/权限语义或缺失承诺都会在求值前被检测并失败关闭。
- source: v007 Reviewer 对 A031 过于笼统、记录省略可形成假空终止页的反例。
- used_by: v008 的响应级一致性防线；不用于宣称提供方事实真实性。
- risk: 生产解码器与承诺生成器若共享同一错误，或攻击者同时控制观察和承诺，哈希自洽不能证明外部事实；快照、权限、截断的服务端语义仍需真实连接器专项验证。
- how_to_verify: 从保存的原始响应由独立边界生成承诺；分别删记录、注记录、改游标/终止、权限和截断字段，并让验证器独立重算。进一步应使用独立进程或透明日志取得承诺根。
- status: `supported`
- related evidence: 正式 180 项攻击面板与 55 项测试覆盖省略阳性记录、注入记录、终止/权限变异和承诺缺失；正式真实连接器尝试保存 GitLab 与 Crossref 原始字节，两套投影序列均相等、承诺均可重算，8/8 个变异均不匹配原承诺。支持范围严格限于给定正确承诺后的本地一致性检测。
- last_updated: `2026-08-03`

## A038：固定信任锚下生产路径不能重签签名清单

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A038`
- assumption: 若主张从独立固定公钥信任锚取得验证密钥，签名私钥只存在于独立签名者进程，生产消费者不能仅通过修改解码结果并重算普通响应承诺，生成可通过验签的新页面。
- source: v008 Reviewer 2、3 对“错误解码后普通哈希可重签”的共同阻断意见。
- used_by: v009 对漏记录后重算和伪终止后重算的失败关闭主张。
- risk: 若消费者可同时替换固定公钥，或私钥实际泄露给生产路径，非对称签名退化为另一种自报承诺。
- how_to_verify: 让独立签名进程用一次性私钥从原始字节签发；消费者只接收单独固定的公钥身份；分别执行普通重算、另一有效密钥自签、签名篡改和私钥产物扫描。
- status: `supported`
- related evidence: 正式 `two-process-signed-trust-bridge-13-v009` 中合法三页会话通过；漏记录后重算与伪终止后重算均为 `UNKNOWN`；第二个独立攻击签名者生成的内部自洽、密码学有效清单因不匹配固定信任锚而为 `UNKNOWN`。签名者与消费者进程标识不同，输出中私钥文件为 0，公钥 2048 位。该支持只覆盖受控带外信任锚和本地进程边界。
- last_updated: `2026-08-03`

## A039：签名会话链可检测已提交会话内的删页、拼接和重放

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A039`
- assumption: 每页签名同时绑定会话标识、连续页序、前页签名摘要、当前/下一游标和终止元数据；从声明起始游标按协议后继闭合，可使删除中间页、保留孤立终止页、跨会话拼接和完全页重放无法形成完整负证据链。
- source: v008 Reviewer 2 的 P0→c1、删除 P1、拼接 E(c2) 构造及 v009 会话清单设计。
- used_by: v009 的会话内分页完整性主张。
- risk: 若整个会话从未提交给验证器，或攻击者可让验证器选择任意会话根，本地链不能证明全局采集历史完整；该风险仍由 A025 和外部只追加根约束。
- how_to_verify: 对三页签名会话分别删除中间页、删除终止页、只保留非初始终止页、拼接同密钥另一会话页、重复完全相同页面、制造循环和分支。
- status: `supported`
- related evidence: 正式 194 项攻击和 65 项测试均包含上述构造并全部通过；正式双进程信任桥中的删中间页、跨会话拼接和完全页重放均返回 `UNKNOWN`。结论严格限于给定已提交签名会话的内部连续性。
- last_updated: `2026-08-03`

## A040：签名语义单元可安全承接同版本原始别名

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A040`
- assumption: 若签名者在规范请求和每条记录中绑定稳定 `semantic_cell_id`，生产页链按该语义标识路由，并拒绝声明中重复的语义标识，则同一表示版本的 B1/B2 原始别名不会被静默当作异源页，也不会把同一语义单元重复计数。
- source: v008 Reviewer 2 的同版本 B1/B2 别名意见。
- used_by: v009 的语义单元路由与声明唯一性规则。
- risk: 真实连接器的 `semantic_cell_id` 生成器若错误地合并不等价单元或拆分等价单元，签名只能不可抵赖地绑定错误映射；A028 在真实连接器上仍未验证。
- how_to_verify: 在相同表示版本下让声明使用 B1、签名页使用 B2但共享语义标识，分别构造存在见证、全称反例和完整空页；另尝试在一个声明中同时加入 B1/B2。
- status: `supported`
- related evidence: 正式攻击和测试中的存在/全称别名路由正确，重复语义声明构造被拒绝；正式双进程信任桥的签名 B2 页对 B1 声明返回 `TRUE`。该证据来自受控语义映射，不验证真实连接器的映射正确性。
- last_updated: `2026-08-03`

## A041：固定公钥信任锚的注册、轮换与撤销安全

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A041`
- assumption: 验证器所持公钥通过独立可信渠道注册，攻击者不能在注册时替换公钥；后续轮换、撤销和身份绑定不会让旧密钥或攻击者密钥被误接受。
- source: v009 从普通哈希承诺推进到非对称签名后新增的根信任前提。
- used_by: 将签名成功解释为“来自预期签名者”而非“由任意密钥自签”。
- risk: 若注册通道与清单由同一攻击者控制，攻击者可以生成自己的密钥和完全有效的恶意清单；密码学正确不等于身份授权正确。
- how_to_verify: 接入硬件保护或独立证书/透明日志注册，执行密钥替换、过期、撤销、回滚和多验证器不一致视图测试。
- status: `unverified`
- related evidence: v009 正式端到端实验使用单独文件模拟受控带外公钥固定，并成功拒绝第二个有效密钥的自签清单；没有实现硬件根、证书颁发机构、透明日志、轮换或撤销，因此不能把受控注册步骤外推为生产安全。
- last_updated: `2026-08-03`

## A042：非对称签名强化在当前模拟原型中的宿主开销很小

- run_id: `20260802_1719_run06`
- run_ref_type: `explicit_run_id`
- assumption_id: `A042`
- assumption: 对签名与公钥验签结果做有界缓存后，v009 相对 v008 的 26,460 回合宿主执行时长只会小幅增加。
- source: v009 性能设计中的缓存预期。
- used_by: 安全强化成本解释。
- risk: 即使任务决定和工具调用完全不变，密码学载荷构造、签名和独立验签仍可能显著增加本地计算成本。
- how_to_verify: 在相同种子、世界、预算和方法下用 Harness 比较 v008/v009 完整主回归时长，并同时核对输入投影与行为零差异。
- status: `contradicted`
- related evidence: v008 Harness 时长 62.355 秒，v009 为 121.804 秒，比值 1.953；配置、26,460 行 v008 输入投影和 13 个行为字段差异均为 0。该结果表明当前原型约慢 95.3%，不能宣称开销很小。
- last_updated: `2026-08-03`
