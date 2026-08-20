# v002 状态转移验证：最近先行与组件级碰撞审计（非权威草案）

## 0. 边界与结论先行

本草案只服务于当前 Run `20260813_1547_run10` 的 v002 先行碰撞判断；它不是 Candidate、Seed、Decision，也不替代主研究者裁决。材料来自本 Run 的本地检索结果、共享只读知识库以及下列论文一级来源；未读取其他 Run。

**碰撞结论（仅属先行审计）：按当前表述，通用核心“从接口描述与请求/响应值自动构造写前—写后读取序列，用外部可见状态差分验证 create/delete/update”已经被占据，不能作为新的方法主张。** 最直接的占据来自 Karlsson 等人的黑盒 REST 行为探索：它仅以 OpenAPI 描述为输入，构造操作序列，复用先前响应值，并执行 `GET–POST/PUT/DELETE–GET` 的状态差分；ARMeta 又自动生成了带资源标识锚定的 `GET–更新–GET` 元变测试。MASTOR、RESTler 则分别占据了响应句柄传播、多操作生命周期和删除后读回等组件。

本轮尚未在所核对一级来源中找到**完全同时满足**以下约束的同一方法：拦截在线大语言模型智能体即将执行/刚执行的真实写调用；无服务源码、无历史轨迹、无训练、无人工后置条件；严格沿用智能体同一凭据；自动覆盖 membership、move、cursor；并把分页不完备、可见性不足和读取错误保守地归为 `UNKNOWN`。但这组剩余差异目前更像：

1. 把已有离线黑盒 REST 行为测试迁移到在线智能体；
2. 扩充状态转移模板；
3. 叠加 Verified Tool Calls 已有的 `TRUE/FALSE/UNKNOWN` 运行时包装。

因此，“所有约束尚未在同一论文共同出现”不足以证明 CCF-B 方法新颖性。若 v002 继续，必须显示出一种不能被现有 `B=<C(O),Q>` 行为生成器、元变关系模板和三值后置验证器简单组合吸收的**新增计算**，尤其是可观测性、读取计划充分性或句柄—状态转移绑定方面的非平凡机制。

## 1. 检索与证据范围

### 1.1 Run-local 检索

使用本 Run 的 `query_research.py`，版本固定为 `v002`，执行了三条检索：

- `prior black-box REST automatic pre/post state differential read-after-write effect oracle OAS CRUD`
- `operator request/response handle create/delete/update/membership/move/cursor visibility pagination UNKNOWN runtime verification`
- `prior metamorphic REST testing dynamic invariant state transition RESTler etc`

结果位于 `hypotheses_v002/searches/v002-transition-collision/`，请求指纹为 `3cd7a8078ac78c3765e1e71ea621c9d9e4b538acf70c2a36f747a5a1f3abcf55`。共享知识库对 ToolGate 有直接命中，但对近年的 REST 行为测试覆盖不足，因此它只能作为入口，不能充当新颖性 Gate；缺口由一级网络来源正文补足。

### 1.2 审计轴

逐篇区分：

- 是否需要服务实现源码；
- 是否需要历史请求/响应轨迹；
- 是否需要专门训练或微调；
- 是否依赖人工编写/确认规则、后置条件或元变关系；
- 是否要求多凭据/跨用户视图；
- 离线 API 测试，还是在线智能体调用时验证；
- 只断言响应，还是用额外读调用核对外部状态转移。

## 2. 依赖与碰撞矩阵

| 工作 | 源码 | 历史轨迹 | 训练 | 人工规则/后置条件 | 多凭据 | 场景 | 核心观测 | 对 v002 的碰撞 |
|---|---|---|---|---|---|---|---|---|
| Karlsson et al., *Exploring behaviours of RESTful APIs in an industrial setting* (SQJ 2024) | 否；仅 OpenAPI | 否 | 否 | **是**；B1–B4 是预定义通用行为谓词 | 否 | 离线黑盒属性探索 | **写前/写后 GET 的外部可见状态差分** | **致命核心碰撞**：自动序列、响应值复用、create/update/delete 差分已存在 |
| Khan et al., *ARMeta* (arXiv:2605.28321, 2026) | 否 | 否 | 未报告任务微调；调用通用 LLM | 自动推断元变关系，但仍受 OpenAPI 和生成假设约束；失败需人工分类 | 未报告 | 离线 REST 元变测试 | **种子/跟随执行间的状态与响应关系** | **强碰撞**：正文示例就是标识锚定的 `GET–更新–GET` |
| Deng et al., *MASTOR* (arXiv:2606.10465, 2026) | **是；完整实现及传递导入闭包** | 否 | 否 | 生成器内置分析/断言机制 | 否 | 离线变异测试与测试生成 | 多操作响应字段捕获、后续绑定、状态回读 | 组件强碰撞；因源码依赖不直接占据 v002 无源码约束 |
| Alonso et al., *SATORI* (ASE 2025) | 否 | 否 | 通用 LLM，无专门训练 | LLM 生成后可由人确认 | 否 | 离线断言生成；生成时无需执行 API | **单响应字段不变量** | 邻近但非外部状态转移；主要占据自动响应断言 |
| Alonso et al., *AGORA* (ISSTA 2023) / *AGORA+* (TOSEM 2025) | 否 | **是；请求—响应对** | 否；Daikon 动态不变量挖掘 | 可能不变量需开发者确认 | 否 | 离线断言挖掘 | 操作级前/后置响应不变量 | 不直接碰撞状态序列；AGORA+ 明示 create-update-delete 序列不变量仍是未来工作 |
| Khan et al., *RESTOR* (arXiv:2607.23963, 2026) | 推理时否 | 推理时仅单个样本；**训练时使用生产流量/执行反馈** | **是；GRPO 微调** | 训练数据构造含领域专家选关键字段/逻辑；产物仍需 QA 审核 | 未报告 | 离线/持续集成断言生成 | **当前响应体断言** | 非状态转移；占据“一样本自动响应预言机”，但违反无训练约束 |
| Atlidakis et al., *RESTler* (ICSE 2019) | 否；OpenAPI/Swagger | 否 | 否 | 依赖内置/手写 active checkers；规格不全时可需用户依赖注解 | “用户命名空间”检查器**需要另一用户视图** | 离线有状态模糊测试 | 响应句柄生产者—消费者；删除后访问、泄漏、层级等主动探测 | 句柄图、生命周期和 delete 后读回均碰撞；不是通用自动效果预言机 |
| *Checking Security Properties of Cloud Services REST APIs* (ICST 2020) | 否；RESTler 基础 | 否 | 否 | **手写安全属性检查器** | 部分检查器是 | 离线安全测试 | use-after-free、resource leak、hierarchy、namespace | 直接占据删除后不可访问，但仅预设安全规则 |
| Arcuri, *EvoMaster* (2019；后续工具报告) | 白盒模式**是**；黑盒模式否 | 否 | 否 | 搜索启发式与故障预言机内置 | 否 | 离线测试生成/模糊测试 | 主要是覆盖、状态码/500 与序列可达性 | 状态序列基础设施碰撞；文献明确没有解决一般 oracle 问题 |
| Segura et al., *Metamorphic Testing of RESTful Web APIs* (TSE 2018) | 否 | 否 | 否 | **六类关系人工识别/实例化** | 否 | 离线元变测试 | 查询输出的相等、包含、排序、分页等关系 | membership/cursor 的关系模板先行；非自动写效果验证 |
| Troya et al., *Automated Generation of Metamorphic Relations for Query-Based Systems* (MET 2022) | 否；需轻量参数规格 | 否 | 否 | 关系模式预定义 | 否 | 离线查询测试 | 过滤、排序、分页等读查询关系 | 自动 cursor/pagination 读取关系的邻近先行；不覆盖写状态转移 |
| *Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures* (arXiv:2608.02645) | 否 | 否 | 否 | **是；手工领域后置条件** | 否 | **在线工具智能体运行时** | 只读后置验证，`TRUE/FALSE/UNKNOWN`，验证后再重试 | **强组合碰撞**：在线包装和三值语义已存在；唯一明显缺口是自动编译后置读取计划 |
| Hou et al., *ToolGate* (Findings ACL 2026) | 否 | 否 | 否 | 依赖工具契约/响应模式；缺模式时可退化为 `Q=True` | 否 | 在线智能体边界 | **响应模式/契约断言后再提交可信状态** | 只占据响应验证，不核对外部效果 |
| Wu et al., *Cordon* (arXiv:2606.17573, 2026) | 否 | 否 | 否 | 策略、授权与约束需要显式表示 | 可能有授权主体但非必需多凭据探测 | 在线语义事务 | 暂存效果、验证 lineage/authority/constraint 后提交或中止 | 事务化控制邻近；不证明已由外部服务确认的实际状态转移 |

“未报告”表示正文中没有找到明确要求或保证，不能推断为“不需要”或“满足同权限”。

## 3. 最邻近工作的实际计算

### 3.1 最直接占据：黑盒 REST 行为探索（Karlsson et al., 2024）

一级来源：[Springer 正文](https://link.springer.com/article/10.1007/s11219-024-09686-0)。

论文把一个待探索行为写为 `B=<C(O),Q>`：`Q` 根据 OpenAPI 描述 `O` 生成操作序列，`C` 检查实际响应。其正文 §3.2 定义四个行为：

- B3：对潜在改变状态的 POST/PUT/DELETE，在其前后执行相同 GET，并要求响应改变；典型序列是 `GET–POST–GET`。
- B4：执行 `GET–POST–DELETE–GET` 一类序列，并要求首尾 GET 相等；中间还可插入 GET 来确认创建资源可见。
- §3.3 的类型图把操作输入、输出和模式字段连接起来；先前操作产生的值可以复用于后续请求，从而把请求作用在同一实体上。
- 正文删除示例先确认创建资源存在，再确认删除后消失。

证据位置：正文 §3.2 “Definition of Behaviours” 中 B3/B4；§3.3 “Test Generation” 的 operation graph、value reuse 与 sequence generation；§3.1 明确其黑盒输入只有 OAS，不需访问实现；§5 讨论无状态重置会使 shrink 受状态漂移影响。

它已经吸收：

- 公共接口描述驱动的读计划/写计划组合；
- create/delete/update 的写前—写后外部可见差分；
- 从响应到后续请求的资源值复用；
- 无源码、无训练、无历史轨迹。

剩余差异并不等于自动新颖性：该工作是离线属性探索，B1–B4 是人为预定义的通用谓词；它发现“行为”，但没有仅凭响应判断行为是否符合业务需求，论文评估也明确需要结合需求解释发现。它没有在线拦截智能体真实调用，没有三值可观测性语义，也没有明确覆盖 membership/move/cursor 或同凭据保证。**然而，若 v002 仅新增一组状态转移模板并把运行位置改成 agent middleware，核心计算仍落入其 `Q,C` 框架。**

### 3.2 精确 update 碰撞：ARMeta（2026）

一级来源：[arXiv 正文](https://arxiv.org/html/2605.28321)。

ARMeta 以 OpenAPI 描述为主要输入，由多个 LLM 智能体自动推断元变关系并生成可执行 Behave 测试。正文 §II 的示例不是抽象响应断言，而是：创建 pet，先 GET，POST 更新其 status，再按同一 id GET，并断言标识不变且 status 发生预期变化。§III 将这种计算表述为种子执行与跟随执行之间的输出关系；其关系类型包括字段/资源修改、create/delete/filter 以及 equality/inclusion/exclusion/difference。

证据位置：正文 §II “Motivating Example”的完整 `GET–POST update–GET` 场景；§III-A/III-C 的 MR 与工作流；§IV 的 1000-request、30-minute 实验预算；§V 对误报的人工检查；§VI 对 OAS 不准确的限制。

它已经吸收：

- 从描述自动生成前后读回；
- 用资源 id 锚定更新对象；
- inclusion/exclusion/difference 等集合关系；
- 无服务实现源码的跨调用效果检查。

其边界是离线测试生成而非在线智能体保护；依赖 OAS 的准确性；实验中的失败还需人工区分真实缺陷和错误假设，UserManagement 上报告的真阳性率只有 56.9%。它没有把分页、权限可见性或读错误形式化为 `UNKNOWN`。但这再次说明“自动生成 pre/post 状态差分”本身不能作为 v002 新方法。

### 3.3 源码型多操作碰撞：MASTOR（2026）

一级来源：[arXiv 正文](https://arxiv.org/html/2606.10465)。

MASTOR 读取完整服务实现及传递导入闭包，从源码恢复 API 语义并生成变异杀伤预言机。其 multi-operation pattern 识别资源生命周期 CRUD、标识传播、字段数据流和嵌套依赖；生成阶段按有序操作序列运行，捕获响应字段并绑定到后续输入。正文示例为 POST user 后提取 id，再以该 id GET，并对各步状态码/字段断言。论文还讨论 response-only 无法验证不可见外部副作用，需要实际外部服务比较或后续 retrieval。

证据位置：正文 §3.1/§3.2 的 source closure 与静态分析输入；multi-operation pattern 段；§4 的响应捕获和后续参数绑定；§5 消融中 multi-operation 对 mutation score 的贡献；§3 的 external side effect 限制。

因此，MASTOR 不满足 v002 的“无实现源码”，但已经占据“句柄捕获—跨操作绑定—生命周期回读”这一方法组件。不能把这些组件的黑盒化本身表述成从零出现的新机制。

### 3.4 在线三值碰撞：Verified Tool Calls（2026）

一级来源：[arXiv 正文](https://arxiv.org/html/2608.02645)。

该工作正面处理非原子工具失败：真实调用返回不确定结果后，以只读后置条件验证外部状态，输出 `true/false/unknown`，据此决定接受、修复或重试。它明确要求后置条件完整、带领域知识，且不能仅从 API 自动推出；论文实验使用手工设计工作流。其局限/未来工作包含陈旧状态和自动语义验证器。

证据位置：正文 §4.2–§4.4 的 verifier、三值结果与 verify-before-retry；§7 的限制和自动语义验证方向。

这项工作没有占据自动读取计划编译，却占据了 v002 的在线包装、只读验证和 `UNKNOWN` 语义。把 Karlsson/ARMeta 的自动序列生成器接到 Verified Tool Calls 的三值控制流，是明显的**组件拼接基线**；v002 必须超过这个基线，而不能把拼接本身当作核心贡献。

## 4. 其他指定方法的吸收范围

### 4.1 SATORI、AGORA/AGORA+、RESTOR：都是响应预言机，不是外部效果证明

- **SATORI**：[arXiv 正文](https://arxiv.org/html/2508.16318)。以静态 OAS 为输入，LLM 推断预定义类别的 response-field oracle，并输出 Postman assertions；生成阶段无需执行 API。正文 limitation 指出现有实现主要处理单响应字段、不处理多变量关系。它占据自动响应断言，不占据写后外部状态转移。
- **AGORA**：[作者论文 PDF](https://personales.us.es/sergiosegura/files/papers/alonso23-issta.pdf)，ISSTA 2023，DOI `10.1145/3597926.3598114`。从既有请求—响应对产生 Daikon 跟踪，挖掘 105 类 likely invariants，再转成测试 oracle。依赖历史执行样本且不验证跨操作效果。
- **AGORA+**：[作者论文页](https://homes.cs.washington.edu/~mernst/pubs/rest-oracle-tosem2025-abstract.html) / [作者 PDF](https://www.javalenzuela.com/publication/2025_tosem_agoraplus/2025_tosem_agoraPlus.pdf)。输入 OAS、请求和对应响应，构造 Daikon 声明/数据跟踪，生成操作级前置/后置不变量并由开发者确认；正文 discussion 明确把 create-update-delete 一类 sequence invariants 留作未来工作。
- **RESTOR**：[arXiv 正文](https://arxiv.org/html/2607.23963)。推理时可只看一个请求—响应样本，不需源码、数据库模式、OAS 或历史，但模型本身通过生产流量和执行反馈进行 GRPO 训练；训练数据构造含专家选择的关键字段/逻辑，最终 assertion 仍由生产 QA 审核。输出只断言当前响应体，不发后续读取来证明状态转移。

结论：dynamic invariant mining 与 response assertion 邻近，但不能直接吸收 v002 的 external-effect differential；反过来，v002 也不能以“无需轨迹”去声称压过 RESTOR，因为 RESTOR 把依赖搬到了训练阶段而非消除。

### 4.2 RESTler 与 EvoMaster：有状态序列和主动探测，但预言机受限

- **RESTler**：[ICSE 2019 论文 PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2021/03/RESTler.pdf)。静态分析 Swagger/OpenAPI 里的 producer-consumer dependencies；例如一个请求生成 resource id，后续请求消费它。运行时用动态响应反馈修剪无效序列。这与 v002 的 request/response handle graph 高度重合。
- **RESTler 主动属性检查器**：[ICST 2020 论文 PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/02/paper2.pdf)。use-after-free 检查删除资源后仍能否访问；resource-leak 检查失败创建是否留下状态；hierarchy 检查子资源能否从错误父路径访问；user-namespace 检查另一用户是否可访问。这些是手写安全模板，其中 namespace 明确需要跨用户视图，不能作为 v002 的同权限证据。
- **EvoMaster**：[原始论文正文](https://arxiv.org/html/1901.01538) / [工具报告](https://pmc.ncbi.nlm.nih.gov/articles/PMC11607064/)。白盒模式依赖被测服务驱动、插桩和源码/字节码；后续也有仅需 schema 和运行中 API 的黑盒模式，但能力较弱，主要 fault oracle 是 HTTP 500 等。其 resource-dependency 工作明确未解决一般 oracle problem。

这些工作占据“状态序列搜索＋句柄依赖＋主动附加请求”的基础构件；v002 的剩余位置只能是如何在无源码、无手工规则且在线的条件下，构造**可信而不过度断言**的外部效果判据。

### 4.3 元变 REST 测试：membership 和 cursor 也不是空白词汇

- **Segura et al.**，*Metamorphic Testing of RESTful Web APIs*，IEEE TSE 2018，DOI [`10.1109/TSE.2017.2764464`](https://doi.org/10.1109/TSE.2017.2764464)：提出六类抽象元变输出关系，覆盖 equality、inclusion、排序、过滤、分页等查询语义；关系识别/实例化依赖人工。
- **Troya et al.**，*Automated Generation of Metamorphic Relations for Query-Based Systems*，MET@ICSE 2022：[作者 PDF](https://javiertroyauma.github.io/publications/MET22_at_ICSE22.pdf)。从轻量查询参数规格自动生成过滤、排序和分页关系，但对象是读查询系统而非写效果。

因此，membership/inclusion/exclusion 与 cursor/pagination 的关系本身有明确先行。所核对来源中尚未找到“真实写调用改变 cursor 所代表集合，并在分页不完备时强制 UNKNOWN”的同构方法，但仅把已有查询元变关系移入写后读取仍可能是模板扩张。

### 4.4 ToolGate 与 Cordon：在线边界相邻，观测对象不同

- **ToolGate**：[ACL Anthology 正文](https://aclanthology.org/2026.findings-acl.470/)。用 Hoare 风格 `P/Q` 契约检查工具结果，再允许其进入可信智能体状态；依赖 response schema/tool contract，正文报告约四分之一 ToolBench 工具缺结构化 schema，此时后置条件可能退化为 `Q=True`。它检查返回响应而非再次读取外部世界。
- **Cordon**：[arXiv 正文](https://arxiv.org/html/2606.17573)。把工具任务建模为语义事务，暂存本地状态/外部效果并验证 lineage、authority 和约束，再 commit/abort。它依赖效果可暂存或受事务控制，不解决第三方服务已经确认写入后的同凭据读回证明。

两者说明“在线智能体工具边界＋提交前验证”也已拥挤；v002 不能仅以在线部署场景区别于离线 REST 测试。

## 5. 按拟议状态转移逐项碰撞

| v002 转移 | 已有最邻近计算 | 剩余但未证明新颖的差异 |
|---|---|---|
| create | Karlsson B3 的 `GET–POST–GET`；ARMeta create+GET；MASTOR POST 后 id 捕获与 GET | 在线围绕 agent 的既有写调用；三值可观测性 |
| delete | Karlsson B4 的 create/delete 回归；RESTler use-after-free；MASTOR 生命周期序列 | 同权限、无手写安全规则、分页不完备时 UNKNOWN |
| update | **ARMeta 正文完整 `GET–POST update–GET` 且同 id 断言**；Karlsson B3 包含 PUT | 几乎只剩在线化和保守 UNKNOWN；碰撞最重 |
| membership | ARMeta inclusion/exclusion；REST 元变测试的集合包含关系 | 如何自动选择集合查询、证明枚举充分，不把不可见误判为不存在 |
| move | RESTler hierarchy 有父子资源路径探测；MASTOR 有嵌套依赖 | “源消失且目标出现”的同一动作双侧合取在所核对论文中未找到完全同构实例 |
| cursor/pagination | TSE 2018 与 MET 2022 已覆盖分页/查询元变关系 | 把不完备游标视为 UNKNOWN、并与写动作绑定的在线语义未找到完全同构先行 |
| 读错误/可见性不足 | Verified Tool Calls 已有 `UNKNOWN` | 自动识别何种观测不足以及何时可从 UNKNOWN 升级，尚无直接命中 |
| 响应句柄锚定 | RESTler producer-consumer graph；MASTOR capture/bind；Karlsson type graph value reuse；ARMeta id reuse | 不是独立新颖组件 |

## 6. 致命碰撞与当前唯一可能保留的研究问题

### 6.1 致命碰撞

1. **泛化 create/update/delete 的 pre/post external read differential：已被 Karlsson 2024 占据。**
2. **自动生成、id 锚定的 update 前后读回：已被 ARMeta 2026 精确占据。**
3. **响应句柄传播和有状态生命周期序列：已被 RESTler 与 MASTOR 占据。**
4. **在线智能体、只读后置核对和三值 `UNKNOWN`：已被 Verified Tool Calls 占据，但其后置条件手写。**
5. **membership/cursor 所需的集合和分页关系：元变 REST/查询测试已有成熟模板。**

将 1/2 的自动序列、3 的句柄依赖、4 的在线三值控制流和 5 的关系模板组合起来，是审稿人最容易提出的“已知模块拼接”反证。

### 6.2 所核对文献尚未吸收的联合点

当前只保留一个窄而高风险的问题：**能否从一次真实工具写调用及其可访问的公开接口语义中，自动推导出一个带“观测覆盖证明/不充分证据”的最小读计划，使 `FALSE` 只在足以排除分页遗漏、权限不可见、延迟一致性、歧义句柄和读副作用后才成立；否则机械地落到 `UNKNOWN`。**

这里真正可能新增的不是“再读一次”或“比较前后”，而是“什么条件下这组读取足以支持否定一个状态转移”的计算。如果没有新的覆盖/可观测性语义、计划最小化/充分性判据或不可区分性处理，v002 会被现有黑盒行为测试＋Verified Tool Calls 完整吸收。此处只是新颖性生存条件，不是候选建议或最终裁决。

## 7. 检索失败与证据限制

- 本 Run 本地知识库没有充分覆盖 2024–2026 REST oracle/元变测试，Run-local 检索不能单独给出“未发现”结论。
- 未找到 MASTOR、ARMeta、RESTler、ToolGate、Cordon 对“所有验证读都严格复用原 agent 凭据”的明确保证；无明文不能视为满足。
- 未找到对 `move = source disappearance AND destination appearance` 且结合在线智能体调用、同权限和三值未知的完全同构一级论文；RESTler hierarchy 只是最邻近路径/父子资源探测。
- 未找到对 pagination/cursor 不完备自动推断“不可判定”的 REST agent 工作；既有分页元变测试主要验证查询关系。
- Karlsson 2024 的行为谓词是预定义的，且行为发现不等于业务正确性；它虽是核心计算碰撞，却不证明 v002 的所有安全语义都已经解决。
- ARMeta 是 2026 年预印本；正文与实验可核对，但截至本审计未以正式会议版本替代其 arXiv 身份。
- RESTOR 的公开论文称专有训练数据和模型不可用，无法复现实证，只能按正文核对其计算依赖。

## 8. 一级来源清单

1. Karlsson et al. *Exploring behaviours of RESTful APIs in an industrial setting*. Software Quality Journal, 2024. [Publisher full text](https://link.springer.com/article/10.1007/s11219-024-09686-0).
2. Khan et al. *Multi-Agent LLM-based Metamorphic Testing for REST APIs (ARMeta)*. arXiv:2605.28321, 2026. [Full text](https://arxiv.org/html/2605.28321).
3. Deng et al. *MASTOR*. arXiv:2606.10465, 2026. [Full text](https://arxiv.org/html/2606.10465).
4. Alonso et al. *SATORI*. ASE 2025 / arXiv:2508.16318. [Full text](https://arxiv.org/html/2508.16318).
5. Alonso et al. *AGORA*. ISSTA 2023. [Author PDF](https://personales.us.es/sergiosegura/files/papers/alonso23-issta.pdf).
6. Valenzuela et al. *AGORA+*. ACM TOSEM, 2025. [Author page](https://homes.cs.washington.edu/~mernst/pubs/rest-oracle-tosem2025-abstract.html), [author PDF](https://www.javalenzuela.com/publication/2025_tosem_agoraplus/2025_tosem_agoraPlus.pdf).
7. Khan et al. *RESTOR*. arXiv:2607.23963, 2026. [Full text](https://arxiv.org/html/2607.23963).
8. Atlidakis et al. *RESTler: Stateful REST API Fuzzing*. ICSE 2019. [Microsoft Research PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2021/03/RESTler.pdf).
9. Atlidakis et al. *Checking Security Properties of Cloud Services REST APIs*. ICST 2020. [Microsoft Research PDF](https://www.microsoft.com/en-us/research/wp-content/uploads/2019/02/paper2.pdf).
10. Arcuri. *RESTful API Automated Test Case Generation with EvoMaster*. arXiv:1901.01538, 2019. [Full text](https://arxiv.org/html/1901.01538).
11. Segura et al. *Metamorphic Testing of RESTful Web APIs*. IEEE TSE, 2018. [DOI](https://doi.org/10.1109/TSE.2017.2764464).
12. Troya et al. *Automated Generation of Metamorphic Relations for Query-Based Systems*. MET@ICSE 2022. [Author PDF](https://javiertroyauma.github.io/publications/MET22_at_ICSE22.pdf).
13. *Verified Tool Calls Improve LLM Agent Reliability Under Non-Atomic Failures*. arXiv:2608.02645, 2026. [Full text](https://arxiv.org/html/2608.02645).
14. Hou et al. *ToolGate*. Findings of ACL 2026. [ACL Anthology](https://aclanthology.org/2026.findings-acl.470/).
15. Wu et al. *Cordon*. arXiv:2606.17573, 2026. [Full text](https://arxiv.org/html/2606.17573).
