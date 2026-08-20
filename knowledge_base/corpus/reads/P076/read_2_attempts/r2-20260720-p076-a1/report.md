# P076 独立二读报告

## Provenance 与读取边界

- Attempt：`r2-20260720-p076-a1`
- 引用的冻结 invocation：`knowledge_base/corpus/reads/P076/read_2_attempts/r2-20260720-p076-a1/invocation.md`
- 实际读取路径：`knowledge_base/staging/plan05_sat_a2/P076_mas_malicious_code.pdf`
- 实际 PDF SHA-256：`5fb79d30a11ef7b2e28d5eadc53af9b7ecb41d8ee60c8e04c2ec3c59e8b1fb11`，与 invocation 冻结值一致。
- PDF 共 33 个物理页；逐页解析覆盖 33/33。物理页 1–10、18–21 的主图、主表、形式化定义和实验设置做了视觉核对；References 与含完整攻击模板/对话的附录以解析和结构核对为主，未在本报告复现或截图传播可操作内容。
- 未读取 read_1、Cards、其他 read_2、saturation、retrieval、blind 或其他论文；未联网。
- 技术隔离状态：`procedural_blinding`，不是文件级技术 allowlist。
- Actual model/version：`unknown`（runtime 未暴露精确 serving version）。可见 task path：`/root/plan05_card_source_audit_e`；产品 thread ID 不可见。
- 可观察工具轨迹：读取冻结 invocation；计算指定 PDF SHA-256；以本地 PDF 解析器逐页提取并对潜在 payload 行做防扩散屏蔽；以内存渲染核对安全的主文/表格页；仅写本报告。
- 安全处理：仅核验攻击机制、实验设计、结果和边界；不复述 Appendix G–I 的完整 orchestrator instructions、attack templates、input queries，也不复述 Appendix J–M 中可直接复用的代码、命令或 payload。

## 一、结论摘要

[AUTHOR_FACT] 论文提出 multi-agent system control-flow hijacking：不可信网页、文件、图像或音频内容被前线 Agent 处理后，影响其返回给 orchestrator 的 status/error metadata；orchestrator 再基于这些 metadata 改变后续 Agent 调用，可能把原本无害任务重定向到高权限 code-execution 或 data-access capability。（物理页 1–5；Figures 1–2）

[READER_INTERPRETATION] changed computation 不在单个模型输出层，而在 **跨 Agent metadata → orchestration decision → capability invocation** 链路。攻击利用 confused-deputy 结构，把来自不可信输入的要求重新包装成系统内部、看似可信的 Agent 状态，从而改变 action-trace suffix。

[AUTHOR_FACT] 作者在 AutoGen、CrewAI、MetaGPT 上测试五种 orchestrator 配置和四个 LLM；Web Redirect 主表中 MAS hijacking ASR 为 2%–100%，而所用既有 IPI templates 近乎全部失败。GPT-4o 的 Web Redirect ASR 随 orchestrator 为 58%–90%；某些 GPT-4o-mini/AutoGen 配置达到 100%。（物理页 6–7 §5–§6.1，Table 2）

[READER_INTERPRETATION] 证据支持“系统级 metadata/control-flow 攻击在这些默认或近默认 MAS 配置中显著有效”，但不支持以下无条件外推：所有 MAS 均可被攻破、攻击完全独立于 prompt interpretation、攻击可逃逸任意 sandbox、所有恶意代码类别已实测、或现有 IPI defense 对此攻击无效。

## 二、物理页逐页覆盖

| 物理页 | 核验内容 | 解析/视觉状态 |
|---:|---|---|
| 1 | Abstract、问题与贡献、Web-based ASR 概述 | 文本+视觉一致。 |
| 2 | Figure 1；MAS hijacking 与 IPI/jailbreak 区分；框架范围 | 文本+视觉一致；图仅为高层控制流，不在报告复现 payload。 |
| 3 | Table 1；Figure 2；refusal 后系统仍执行的案例概述 | 文本+视觉一致。 |
| 4 | §2 Agent/MAS、data/metadata、三类 topology；§3 threat model 起始 | 文本+视觉一致。 |
| 5 | adversary goals；§4 attack mechanism；laundering conjecture | 文本+视觉一致。 |
| 6 | §5 frameworks/models/trials/detection/baselines；§6 Web Redirect | 文本+视觉一致。 |
| 7 | Tables 2–4：Web Redirect、Local、Web Single、Web Image | 文本+视觉一致；表头/百分比未发现解析反转。 |
| 8 | Table 5 exfiltration；incidental contact、paraphrase、direct hijack；失控案例 | 文本+视觉一致；发现 `80% (28/40)` 算术冲突。 |
| 9 | audio/video 观察；Related Work；defense 分类 | 文本+视觉一致。 |
| 10 | Discussion：metadata laundering、refusal insufficiency、trust model | 文本+视觉一致。 |
| 11 | Ethics Statement 与 References 起始 | 解析覆盖；受控实验和披露事实已核对。 |
| 12 | References | 解析覆盖。 |
| 13 | References | 解析覆盖。 |
| 14 | References | 解析覆盖。 |
| 15 | References | 解析覆盖。 |
| 16 | Appendix A.1：agent security/IPI 扩展综述 | 解析覆盖；未保留攻击字符串。 |
| 17 | Appendix A.2–A.3：MAS attacks 与 defense taxonomy | 解析覆盖。 |
| 18 | Appendix B Figures 3–4：local/multimodal attack flow | 文本+视觉一致；只核对高层步骤。 |
| 19 | Appendix C formal definition；Appendix D Table 6 benign success | 文本+视觉一致。 |
| 20 | Table 7 direct-ask refusal/ASR；Appendix E setup | 文本+视觉一致。 |
| 21 | Appendix E detection/log labeling；Appendix F Figure 5 topology | 文本+视觉一致。 |
| 22 | topology 第三类；Appendix G orchestrator instructions | 解析覆盖；完整 instructions 有意不复述。 |
| 23 | Appendix H attack templates | 结构核对；模板正文有意不复述。 |
| 24 | Appendix I input queries | 结构核对；原始 query wordings 有意不复述。 |
| 25 | Appendix J CrewAI refusal→execution transcript 起始 | 角色/安全状态/执行事件核对；代码与命令屏蔽。 |
| 26 | Appendix J 续 | 同上。 |
| 27 | Appendix K AutoGen refusal→execution transcript 起始 | 角色/拒绝/警告/执行事件核对；payload 屏蔽。 |
| 28 | Appendix K 续 | 同上。 |
| 29 | Appendix L benign task→malicious execution | 文件探索、错误 metadata 与执行结果核对；细节屏蔽。 |
| 30 | Appendix M LLM autolabel misclassification 起始 | 自动标注误判事实与 transcript 结构核对。 |
| 31 | Appendix M 续 | 同上。 |
| 32 | Appendix M 续 | 同上。 |
| 33 | Appendix M 续与结束 | 同上。 |

## 三、Threat model 与 changed computation

### 3.1 攻击者能力和目标

[AUTHOR_FACT] 攻击者不控制 Agent，也不能直接 prompt 用户的 MAS；攻击者控制 MAS 可能访问的外部内容，例如网页或用户设备上已有文件。在更强 threat model 中，攻击文件已位于用户环境；网页攻击还测试文本、截图图像，视频音频只做探索性案例。（物理页 4–5 §3.1）

[AUTHOR_FACT] 实验目标是两类高危 capability：在 code-execution environment 中触发攻击者指定代码，以及从 CrewAI 可访问的 auxiliary knowledge/data source 构造并外传测试用户资料。（物理页 5 §3.2；物理页 7–8 §6.2–§6.3）

[READER_INTERPRETATION] 前提包括：MAS 能访问不可信内容；至少一条跨 Agent 通信链可把内容转成 control metadata；orchestrator 会根据 metadata 自适应重规划；系统中存在具有足够文件、网络或执行权限的高危 capability。缺少 code executor、网络 egress、敏感数据挂载或跨 Agent trust 时，攻击后果会显著不同。

### 3.2 控制流改变

[AUTHOR_FACT] 攻击内容伪装成合理 error/status message，并包含针对后续 Agent 角色的行为要求。前线 file/web agent 把它返回为 output/metadata；orchestrator 不直接接触原始不可信内容，却信任该输出并修改调用计划。（物理页 5 §4）

[AUTHOR_FACT] Appendix C 把 MAS 定义成 agents `A` 与通信 edges `C` 的有向图；攻击输入 `d'` 的目标是修改系统处理该输入后的 action-trace suffix，使其包含攻击者指定的一组自然语言或形式化 actions，且重定向持续到 trace 结束。（物理页 19 Appendix C）

[READER_INTERPRETATION] 形式化定义刻画了“action suffix 被重定向”，但未建模 trust label、权限、sandbox、概率、并发、消息完整性或因果干预。因此它是攻击目标定义，不是安全保证或对 root cause 的形式证明。

### 3.3 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 输入：恶意 local/web/multimodal content、框架自己的 tool output 与 inter-agent metadata；用户初始请求本身可为无害内容访问任务。
- [AUTHOR_FACT] 干预时点：前线 Agent 读取外部内容后、orchestrator 基于返回的 status/error 更新下一步 agent selection 之前。
- [AUTHOR_FACT] 输出：被修改的 task/action trace，最终可能调用 code executor、file/data agent 或网络能力。
- [READER_INTERPRETATION] 攻击者不需要读取 orchestrator hidden state，但实验模板针对不同 orchestrator 略作指令调整，因此并非完全 topology-agnostic black-box universal string。

## 四、Framework、模型、预算与检测

[AUTHOR_FACT] 框架/拓扑为：AutoGen Magentic-One、Selector、Round-Robin；CrewAI default orchestrator；MetaGPT Data Interpreter。模型为 GPT-4o、GPT-4o-mini、Gemini 1.5 Pro、Gemini 1.5 Flash；CrewAI 因已知 tool-use bug 只测 OpenAI 模型。（物理页 6 §5；物理页 7 Table 2；物理页 20 Appendix E）

[AUTHOR_FACT] 作者称尽量保持 framework default，仅做在实验环境运行所需的最小修改；模型经 API 调用并使用 framework-library defaults，实验在 CPU 与外部模型 API 上进行。（物理页 20 Appendix E）

[OPEN_QUESTION] PDF 未冻结精确 API model snapshot、temperature、sampling parameters、framework commit、tool timeout、最大轮数、token budget、成本或平均 action/tool-call 数。云模型和开源框架均会变化，复现风险高。

[AUTHOR_FACT] 主实验交叉多种 input type、三种 fake-error style、两种 user-query wording；每个 `(framework, orchestrator, model, input, error, query)` tuple 跑 10 trials。每个 orchestrator 的 exact instructions 略有变化。（物理页 6 §5；物理页 21 Appendix E）

[READER_INTERPRETATION] 单 tuple 只有 10 次，未报告置信区间；表中百分比常聚合多个 error/query/model cell。小差异不能解释为稳定的模型或 topology 排名。

[AUTHOR_FACT] ASR 的主检测是在 code executor 即将执行测试 payload 时退出并写入唯一标记；另设受控服务器监听相关网络连接作为 backup。完整 logs 再由 regex 与人工检查识别未注册执行、unsafe-code detection 与 refusal。GPT-4o-mini 自动标注产生过多 false negatives，故未采用。（物理页 6 §5；物理页 21 Appendix E；物理页 30–33 Appendix M）

[READER_INTERPRETATION] 主要 ASR 更直接测量“执行路径到达并触发指定 payload”而非攻击者取得长期、交互式远程控制的完整后果；backup connection 提供额外佐证，但论文未报告每个 ASR cell 有多少由主标记或 backup 判定。

## 五、Baseline 与对照完整性

[AUTHOR_FACT] 三类基线是：

1. 与攻击访问命令措辞/格式相同、但内容 benign 的 local/web task；
2. 用户直接要求系统执行恶意动作的 Direct Ask；
3. 来自既有 AgentDojo/Debenedetti repository 的三种 IPI templates。（物理页 6 §5；物理页 19–21 Tables 6–7 / Appendix E）

[AUTHOR_FACT] Benign task success 按模型聚合为 Local 96%–100%、Web 86%–100%；某些攻击配置接近 benign success，Magentic-One+Gemini 1.5 Pro 的特定攻击成功率甚至高于其 benign web retrieval success。（物理页 19 Table 6 及正文）

[AUTHOR_FACT] Direct Ask 按模型聚合时，GPT-4o refusal 72%、ASR 0%；GPT-4o-mini refusal 86%、ASR 6%；Gemini 1.5 Pro/Flash refusal 0%、ASR 分别 37%/41%。（物理页 20 Table 7）

[READER_INTERPRETATION] 这些对照支持“内部 metadata presentation 比普通恶意 ask 或所测 IPI templates 更能触发系统级执行”。但 Table 2 的 IPI/DA 列并非所有行都具有相同模型组合：Crew baseline 明确只用 GPT-4o，其他行会受模型分布影响；不能把列差异完全归因于 attack-string mechanism。

[OPEN_QUESTION] 最接近但缺失的组合基线包括：相同 fake-error 格式但删除跨 Agent role instructions、相同 metadata 由可信系统组件产生、只允许低权限 agent、禁网络 egress、禁 code executor、固定 orchestration、不传递 error text、以及随机/benign error-message control。缺少这些对照，无法精确分解“格式、错误恢复、角色指令、权限和 topology”各自贡献。

## 六、主要结果

### 6.1 Web Redirect 与 IPI/DA

[AUTHOR_FACT] Table 2 的 Web Redirect ASR：

- AutoGen Magentic-One：GPT-4o 58%、GPT-4o-mini 88%、Gemini Pro 88%、Gemini Flash 33%；
- AutoGen Selector：65%、98%、78%、38%；
- AutoGen Round-Robin：73%、100%、73%、60%；
- CrewAI default：GPT-4o 62%、GPT-4o-mini 43%；
- MetaGPT Data Interpreter：90%、88%、14%、2%。

同表的 IPI 列为 0%–1%，Direct Ask 列为 0%–50%。（物理页 7 Table 2）

[READER_INTERPRETATION] 攻击并非所有模型/框架都稳定成功：MetaGPT+Gemini Flash 仅 2%，MetaGPT+Gemini Pro 14%，而 AutoGen 多数配置很高。framework/input/capability wiring 与模型同样重要。

### 6.2 输入类型

[AUTHOR_FACT] Local File、Web Redirect、Web Single、Web Image 的 ASR 分布差异很大。例：Magentic-One+GPT-4o Local 97% 而 Web Single 27%、Web Image 25%；Magentic-One+Gemini Pro Local 97%、Web Redirect 88%、Web Image 60%。Web Image 只在 AutoGen 上测试。（物理页 7 Tables 3–4）

[AUTHOR_FACT] 音频/视频实验仅报告“occasionally”成功且结果不一致，没有表格化 ASR 或完整配置矩阵。（物理页 9 §6.5）

[READER_INTERPRETATION] 多模态可作为入口得到初步支持，但不能概括为稳定、跨框架的 multimodal attack。

### 6.3 数据外传

[AUTHOR_FACT] Exfiltration 只在 CrewAI 上测试，因为作者称它是评价框架中唯一支持 auxiliary data sources 的系统。四种 orchestrator/sub-agent model 组合下，Local Exfil ASR 为 23%–65%，Web Exfil 为 3%–27%，通常低于对应远程控制类 payload；作者把差异归因于多步任务更复杂。（物理页 8 Table 5 / §6.3）

[READER_INTERPRETATION] 该实验支持“CrewAI 测试环境中的辅助资料可被多步链路外传”，不能直接外推到所有框架、真实用户秘密、任意 RAG/API，或容器外数据。

### 6.4 现实性与 presentation

[AUTHOR_FACT] Incidental-contact setting 中，目录同时含一个 benign file 与一个 attack file，35/40 trials 成功，ASR 87.5%。10 个 user-query paraphrases 均至少有成功 trial，各自 ASR 40%–85%，合计 200 trials 平均 59.5%。（物理页 8 §6.4）

[AUTHOR_FACT] Direct-hijack 段落报告 `ASR is 80% (28 out of 40 trials)`、refusal 0%。（物理页 8 §6.4）

[READER_INTERPRETATION] `28/40 = 70%`，与同句 `80%` 明确冲突。PDF 无法判断正确值是 28、32 还是百分比排版错误；后续引用必须保留为 `[OPEN_QUESTION]`，不得任选一个数。

## 七、“独立于 prompt injection”应如何理解

[AUTHOR_FACT] 作者明确承认 adversarial inputs “are a form of indirect prompt injection”，但把 MAS hijacking 与传统 IPI 区分为：前者操纵 shared metadata/inter-agent communication 和 system-level control flow，后者主要针对单 Agent reasoning/output。（物理页 2–3，Table 1）

[AUTHOR_FACT] 所测既有 IPI templates 在 Table 2 中几乎全为 0%–1%，而 MAS hijacking 很高；若把 adversarial metadata 直接作为 orchestrator user prompt，作者报告高 ASR/零 refusal，与普通 Direct Ask 的高 refusal/低 ASR 形成反差。（物理页 7–8 §6.1/§6.4）

[READER_INTERPRETATION] 这支持“攻击不等同于已知 IPI templates，且单 Agent refusal 不能保证系统安全”。它不支持“完全不依赖 prompt injection 或模型对自然语言指令的服从”，因为攻击仍需要模型解释伪造 error/status 和后续 role instructions。论文给出的 laundering/safety-alignment explanation 是由对照支持的 conjecture，不是机制隔离实验的唯一结论。

[OPEN_QUESTION] 未测试强 adaptive IPI、与 MAS hijacking 等 token/格式/角色信息的 IPI、模型级 instruction-hierarchy defense，或把同一内部 metadata 直接注入但不经前线 Agent 改写的严格 matched controls。

## 八、code-execution 与 exfiltration claim 边界

[AUTHOR_FACT] 实验 payload 主要是一种非混淆 Python 远程控制类脚本；CrewAI 另测一种资料外传脚本。Appendix G–I 提供 framework-specific instructions/templates/queries，Appendix J–L 给出具体 transcripts。（物理页 6/21 §5/Appendix E；物理页 22–29）

[READER_INTERPRETATION] “arbitrary malicious code”在系统能力层面有合理依据：一旦攻击者控制的文件被通用 code executor 执行，后果原则上受 executor 权限而非 payload 类别限制。但直接实证只覆盖上述两类 payload，未系统测试文件破坏、权限提升、持久化、横向移动或其他代码类别。

[AUTHOR_FACT] 论文分别描述用户设备上的 code execution 与 containerized environment 内数据风险；实验均在受控实验室环境，未攻击生产服务。（物理页 1–3；物理页 11 Ethics Statement；物理页 20 Appendix E）

[READER_INTERPRETATION] 论文没有证明 container escape、host privilege escalation 或超出 code-executor sandbox 权限的访问。“用户设备任意代码执行”只适用于 executor 直接运行于该设备且权限允许的部署；容器化部署的实证边界是容器内执行/数据与允许的网络 egress。

## 九、Defense、安全边界与披露

[AUTHOR_FACT] 作者只综述 prompt-tuning、agent-level tool validation/tagging、model-level alignment/structured queries/information-flow 等 defense，并明确说其对 MAS hijacking 的有效性和 utility collateral damage 留待 future evaluation。（物理页 9 §7.2；物理页 17 Appendix A.3）

[READER_INTERPRETATION] 本论文没有 defense baseline、没有 patched framework、没有 sandbox/egress ablation、没有 utility-vs-security 曲线。不能从本文声称任何已有 defense 有效或无效。

[AUTHOR_FACT] 所有实验在 controlled lab 进行，无生产 live agents 被攻击；作者通过指定渠道联系 Microsoft、Crew 和 MetaGPT。MetaGPT 确认在处理 executor sandbox，Microsoft 确认复现并调查。（物理页 11 Ethics Statement）

[OPEN_QUESTION] PDF 没有披露供应商修复版本、复现日期、CVE/安全公告、默认配置后续变化或 remediation 结果。

## 十、负向结果与真实 Failure 线索

[AUTHOR_FACT] ASR 强烈依赖框架、orchestrator、模型与输入：同一 Web Redirect 在 MetaGPT 上从 90%（GPT-4o）降到 2%（Gemini Flash）；Local 在 MetaGPT 上为 0%–8%，而 AutoGen 多个配置达 70%–97%。（物理页 7 Tables 2–3）

[AUTHOR_FACT] Web Single 通常弱于 Web Redirect；audio/video 不稳定；exfiltration 多步攻击通常弱于单一执行类 payload。（物理页 7–9 §6.2–§6.5）

[AUTHOR_FACT] 个别 sub-agent 明确认出危险、拒绝或发出警告，但其他 Agent 或 orchestrator 仍生成、转交或执行相关代码；另有 benign task 完成后系统主动探索同目录并触发恶意文件的案例。（物理页 8–9 §6.5；物理页 25–29 Appendices J–L）

[AUTHOR_FACT] GPT-4o-mini 对完整 logs 的自动安全标注产生过多 false negatives，作者转用 regex 与 manual verification。（物理页 21 Appendix E；物理页 30–33 Appendix M）

可记录的 Failure：

- [READER_INTERPRETATION] **Per-agent refusal does not compose into system safety**：一个 Agent 的 refusal/warning 可被后续 Agent 的 capability invocation 绕过。
- [READER_INTERPRETATION] **Untyped metadata becomes control authority**：error/status 未携带 trust/provenance，却能影响 orchestrator 与高权限工具。
- [READER_INTERPRETATION] **Adaptive recovery can amplify malicious state**：为 benign robustness 设计的重试、替代路径和探索会继续寻找完成攻击的路径。
- [READER_INTERPRETATION] **LLM log autolabeling can miss system-level harm**：单一自动分类器不足以替代 execution instrumentation 与人工核验。
- [READER_INTERPRETATION] **Attack claims are capability-bound**：没有 code execution、network egress 或 sensitive-data access 时，论文的严重后果不成立。

## 十一、可抽取 Operator 与不可越界内容

### 可抽取 Operator

1. **Untrusted-metadata control-flow redirection**
   - 输入：不可信 external content 及前线 Agent 产生的 status/error metadata。
   - changed computation：orchestrator 的 next-agent/capability selection 被 metadata 改写。
   - 输出：包含攻击者指定 capability actions 的 action-trace suffix。
   - 时点：tool/content ingestion 之后、高权限 Agent invocation 之前。

2. **Capability-laundering through a confused deputy**
   - 前线 Agent 把外部内容重新表述成内部可信消息；orchestrator 将其视为系统进度/恢复要求。
   - 该 Operator 是攻击机制抽象，不应携带本文完整模板、命令或 payload。

3. **Execution-instrumented ASR measurement**
   - 用 executor-side unique marker、受控网络观测、regex 与人工核验确认危险路径是否真正到达执行，而非只测模型生成文本。
   - 边界：instrumentation 会修改 executor；需报告“would execute”和真实副作用的区别。

### 不应抽成强结论

- 不应写成“所有 MAS 均可执行任意恶意代码”。
- 不应写成“攻击与 prompt injection 无关”；准确说法是它针对系统级 metadata/control flow，且显著强于所测传统 IPI templates。
- 不应声称已经证明 sandbox escape 或 host compromise。
- 不应把一种远程控制类 payload 和一种 exfil payload 当作所有恶意行为的全面实测。
- 不应声称任何 defense 已被验证。
- 不应传播 Appendix G–I 的完整攻击材料或 Appendix J–M 的可执行片段。

## 十二、Reconciliation 前必须保留的 Open Questions

1. Direct-hijack 的正确结果是 80%、28/40，还是 32/40？
2. 每个表格 cell 的确切 trial 数、聚合维度和置信区间是什么？
3. 精确 API model snapshots、framework commits、temperature、token/step limits 与 tool timeout 是什么？
4. 在完全 matched 的 error-format/role-instruction/metadata controls 下，各组成因素贡献多少？
5. 禁用 code executor、阻断 egress、最小权限、typed provenance metadata 或固定 orchestration 各自能降低多少 ASR，utility 损失多少？
6. 主检测 unique marker 与 backup connection 分别贡献了多少成功判定？
7. 攻击成功是否需要 payload 内容进入 orchestrator context，还是只需前线 Agent 的抽象 status？
8. 一个固定攻击模板能否跨 framework/orchestrator 迁移，还是必须按拓扑定制？
9. 真实 container boundary、host permissions 与挂载数据范围是什么？
10. 结果对更强 adaptive IPI、现代 instruction hierarchy 和 agent-level tool validators 是否仍成立？

## 十三、最终二读判断

[READER_INTERPRETATION] P076 的核心证据是系统性的：它用多框架、多 orchestrator、多模型、多输入形式和 executor-side instrumentation 说明，不可信内容可通过 Agent 间 metadata 信任改变系统 control flow，且单 Agent refusal 与传统 IPI 失败不能保证 MAS 整体安全。最可复用的研究对象是“untrusted metadata 获得 orchestration authority”这一 failure，而不是具体攻击字符串。

[READER_INTERPRETATION] 证据边界同样明确：默认配置与云模型版本未完全冻结、每 tuple 样本小、攻击模板按框架调整、defense 未测试、严重后果依赖 code/data/network capability、容器逃逸未证明，且 direct-hijack 百分比存在算术冲突。后续 reconciliation 必须保留这些限制，并继续避免扩散可执行攻击材料。
