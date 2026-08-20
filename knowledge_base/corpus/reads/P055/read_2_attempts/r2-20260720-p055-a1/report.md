# P055 独立二读报告

## 1. Provenance 与读取边界

- 本报告对应 invocation：`r2-20260720-p055-a1/invocation.md`；冻结 prompt SHA-256 为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`。
- 原始 PDF：`P055_planner_formalizer_constraints.pdf`，实核 SHA-256 为 `0d21a03ded6ae892d0818ec8e0f453b3ca0fc1c4cb3e30ae2c3b182c40868207`，与 invocation 一致；共 33 个物理页（ACL 印刷页 13724–13756）。
- 读取采用 procedural blinding：科研输入仅为 invocation、统一 prompt 与该 PDF；未读取首读、Card、其他读者报告、Corpus Report、blind 材料，也未联网。此边界不等于文件级技术隔离。
- 我逐物理页读取全文并检查渲染版面，覆盖正文、Figures 1–7、Tables 1–13、Listings 1–27、附录定义与 prompts。

## 2. 方法改变的计算步骤

- [AUTHOR_FACT] CoPE 在已有规划域/问题上增加一句自然语言 constraint；LLM-as-Planner 直接输出 plan，LLM-as-Formalizer 输出 PDDL、PDDL3、SMT/Z3 或 LTL 表示，再由对应求解器生成 plan。定位：物理页 1–2，Abstract、Figure 1；物理页 5–6，§5。
- [AUTHOR_FACT] Formalizer 又分 Generation、Editing、Revision：Generation 从输入直接写受约束代码；Editing 先写无约束代码，再根据 constraint 修改；Revision 根据执行错误最多重生成三次。定位：物理页 5，§5；物理页 24–29，Listings 16–27。
- [READER_INTERPRETATION] 论文的核心干预有两层：先改变任务语义（加入约束），再比较多种“自然语言→形式表示→专用求解器”的计算分解。Editing 把约束处理隔离为第二次模型调用，是最明确的 changed-computation operator。

## 3. 输入、输出、可用信息与干预时点

- [AUTHOR_FACT] 基础输入为 `(Dd, Dp, DF′G)`：DD、PD，以及 ground-truth PDDL DF 的 header；后者给出动作名称与参数，用于固定 ontology 和公平评测。加入约束后输入为 `(Dd, Dp, DF′, C)`。定位：物理页 3，§3；物理页 5，§5。
- [AUTHOR_FACT] Planner 输出 grounded action sequence；Formalizer 先输出 DF/PF 或其他形式程序，再由 solver 搜计划，最终都相对于加约束后的 ground-truth PDDL 验证。定位：物理页 3、5，§3、§5。
- [AUTHOR_FACT] Editing 的干预发生在模型已生成无约束 formalization 之后；Revision 发生在 compiler/solver/runtime 返回 error message 之后。定位：物理页 5，§5；物理页 25–27，Listings 18–19、23、26。
- [READER_INTERPRETATION] 所有方法都不是从未知 action ontology 开始；DF′ 暴露动作接口。不同 formalism 还获得不同强度的 prompt 规则、示例和工具反馈，因此“formal language 的选择”与“提示/工具接口”不可完全分离。

## 4. constraint taxonomy

- [AUTHOR_FACT] 约束被定义为补充且非破坏性的信息，它收缩可接受行为；作者先定义 primitive action/state，再将约束分为 Initial、Goal、Action、State 四类。定位：物理页 3–4，§3、Definitions 1–6；Table 1。
- [AUTHOR_FACT] Initial constraint 改变 primitive initial state；Goal constraint 改变 primitive goal-state set；Action constraint 收缩 primitive action-sequence set；State constraint 收缩 primitive state-trace set且不属于前三类。定位：物理页 4，Definitions 3–6。
- [AUTHOR_FACT] State 类作为兜底而被作者称为使分类 complete；约束仅引入新 predicates、不移除既有 predicates，且本文不讨论多个 predicates/constraints 的 conjunction。定位：物理页 4，§3；物理页 10，§8。
- [AUTHOR_FACT] 约束平均 15.885 words。每个域人工标注 100 条约束；BlocksWorld action 类含 10 families、state 类 5 families、initial 与 goal 各 4 families。三名受训作者分别写不重叠约束，再过滤。定位：物理页 5，§4；物理页 14，Appendix C。
- [READER_INTERPRETATION] taxonomy 描述的是约束对 primitive 轨迹/动作集合的影响，不只是表面语言类型。它适合比较不同 formalism 的表达成本，但 family 数量不均，category 平均性能不应自动解释为纯类别难度。
- [OPEN_QUESTION] Appendix F 的 theorem 将 `D={State, Initial, Goal}` 称为 complete，而正文又把 Action 作为第四类，并让 State 排除其他类型；Action 与 State 在证明中的关系及四类是否严格互斥，需要作者进一步澄清。定位：物理页 14–15，Appendix F。

## 5. 数据规模与“性能下降”统计口径

- [AUTHOR_FACT] 完整 CoPE 把每条 constraint 与每个 problem 配对，可形成 10,000 个 constrained problems；主实验为控制分析规模，每条 constraint 只人工配一个 representative problem，故每个域评测 100 题。定位：物理页 5，§4。
- [AUTHOR_FACT] Correctness 是成功通过 ground-truth PDDL 验证的 plan 百分比；不是与单一 ground-truth plan 比较。PDDL/PDDL3 的 plan 用 VAL 检查动作可执行性与最终 goal。定位：物理页 5，§5；物理页 14，§E.1。
- [AUTHOR_FACT] 摘要称“一句约束 consistently halves performance”；正文更谨慎地说通常减半。Tables 3–13 提供每个模型/方法的 100 题百分比，但没有置信区间、重复 seed 或显著性检验。定位：物理页 1、7；物理页 30–33。
- [AUTHOR_FACT] 大量强模型单元确有大幅下降：BlocksWorld Planner 中 Gemini-3-Flash 98→59、DeepSeek-R1 91→54；CoinCollector Planner 中 Gemini 93→57、Qwen3-32B 96→52。定位：物理页 30–31，Tables 3、7。
- [AUTHOR_FACT] 但“每个单元都下降”并不成立：BlocksWorld PDDL Generate 的 Qwen2.5-32B 为 4→6；BlocksWorld SMT Edit+Revision 的 DeepSeek-R1 为 1→22；CoinCollector SMT Edit+Revision 的 DeepSeek-R1 为 43→47。定位：物理页 30–32，Tables 4、6、10。
- [READER_INTERPRETATION] “halves”是描述性总体趋势，不是报告过的统计 estimand。样本由 constraint family 和人工 representative pairing 构成，且若干低基线单元有反向波动；不宜把该短语理解为跨所有模型、方法、类别都显著减半。
- [OPEN_QUESTION] PDF 未说明 representative problem 的选择准则、是否在选择时盲于方法结果，也未给出 family/category 分层的样本数和不确定性区间。

## 6. PDDL、PDDL3、SMT、LTL 的可比性与结果

- [AUTHOR_FACT] PDDL 使用 `dual-bfws-ffparser`；PDDL3 先经 TCORE 编译为 PDDL，再用相同 planner/VAL；SMT 由 LLM 写调用 Z3 的 Python，prompt 固定最多 100 steps；LTL 用 Spot 搜索 conjunction 的 lasso-shaped accepting run，再从状态变化推断 PDDL actions。定位：物理页 5–7，§5；物理页 26–29，Listings 24–27。
- [AUTHOR_FACT] LTL 只在 CoinCollector 上测试 goal/action/state constraints，不测试 initial constraints；约束公式由额外模型调用生成，环境 adjacency 也由模型生成。作者明确说 LTL 主要适合简单导航 action dynamics，泛化性不如其他语言。定位：物理页 6–7，§5；Figure 3。
- [AUTHOR_FACT] PDDL 通常优于 SMT；PDDL3 常因 compiler/syntax error 弱于 PDDL。作者也指出 PDDL3 constraint syntax 不能直接覆盖 action constraints 或需要新 predicates 的 state constraints。定位：物理页 4、7，§3、§6。
- [AUTHOR_FACT] 在 BlocksWorld，最强受约束结果并非 Planner：Gemini PDDL Edit+Revision 为 76%，PDDL3 Edit+Revision 为 74%，Planner 为 59%。在 CoinCollector，Gemini PDDL3 Generate+Revision 为 62%，Planner/PDDL Edit 均为 57%。定位：物理页 30–32，Tables 3–10。
- [AUTHOR_FACT] SMT 在 BlocksWorld 明显较弱（Gemini constrained 最高 31%），在 CoinCollector 更有竞争力（Gemini Generate+Revision 48%）；LTL 的 unconstrained 强但 constrained 明显下降（Gemini 97→36、DeepSeek-R1 100→44）。定位：物理页 31–32，Tables 6、10–11。
- [READER_INTERPRETATION] 这些差异同时混合 formalism expressivity、训练语料频率、编译器/求解器、固定 horizon、动作反推、prompt 长度与工具错误表面；不能仅归因于“语言本身更适合约束”。

## 7. syntax revision 预算与 oracle 差异

- [AUTHOR_FACT] Planner 只有一次生成 plan 的机会；Formalizer 最多获得三次把代码改到 syntactically correct 的机会。作者认为 syntax check 几乎免费，且强调不是重新规划。定位：物理页 5，§5。
- [AUTHOR_FACT] 实际 prompts 不只暴露 parser syntax：PDDL revision 获得通用执行 error；PDDL3 revision 分为 compiler error 与 solver error，并把 original/compiled DF/PF 和 solver error 返回；SMT revision 获得 Python/Z3 error。定位：物理页 25–27，Listings 19、23、26。
- [READER_INTERPRETATION] “只修 syntax”与可观察接口并不完全一致：solver/runtime error 可能携带超出语法的结构或语义线索。Revision 还增加最多三次 LLM 调用，因此与单次 Planner、单次 Generate 不是等 tool-call/token 预算。
- [OPEN_QUESTION] 未报告每题实际 revision 次数、错误类型分布、总 token、wall time、solver time 或费用；也未给 Planner 一个对应的 validation-feedback budget，公平性只能接受作者的任务设计论证，不能从等预算实验得到验证。

## 8. 最强基线与 closest combination baseline

- [AUTHOR_FACT] 直接 LLM-as-Planner 是主要强基线，且主文称其在总体上常优于 Formalizer；但全表显示最佳方法随 domain/model 改变，并非统一 Planner 胜出。定位：物理页 7，§6；物理页 30–33，Tables 3–13。
- [READER_INTERPRETATION] 对“约束形式化是否有效”的 closest combination baseline 是同一 model/formalism 下：Generate vs Edit，以及各自 without/with Revision；这能局部隔离“先生成再编辑”，但 Edit 天然多一次模型调用，Revision 再增加调用。
- [AUTHOR_FACT] 论文还用 BlocksWorld-XL–100（50 blocks）与 MysteryBlocksWorld-100 检查复杂度和 lexical shift；无约束时 PDDL Formalizer 对 lexical shift 较稳，但加入约束后优势大幅消失。定位：物理页 8–9，Figure 6；物理页 33，Tables 12–13。
- [OPEN_QUESTION] 未提供同等 token/tool-call 的 planner+validator、self-refine planner 或共享外部反馈 baseline；因此无法判断多阶段 Formalizer 的提升有多少来自 formalization、多少来自额外调用和 solver oracle。

## 9. model、prompt 与版本混杂

- [AUTHOR_FACT] 使用 Gemini-3-Flash、DeepSeek-R1、DeepSeek-V3、DeepSeek-V3.2 Thinking/Non-Thinking、Qwen3-32B、Qwen2.5-32B；DeepSeek 经 API，Qwen 在单 H100 上通过 KANI 默认 temperature。定位：物理页 7，§5。
- [AUTHOR_FACT] 作者在脚注承认 DeepSeek API endpoint 于 2025-12-01 改变；Planner/PDDL/SMT/LTL 被认为使用相同模型，但 PDDL3 实验“may have used different models”。定位：物理页 7，脚注 2。
- [READER_INTERPRETATION] 因此 PDDL3 与其他 formalism 的跨方法差异存在模型版本污染，不能作为纯 formalism comparison。
- [AUTHOR_FACT] prompts 的信息量差异很大：Planner 是简短 one-shot 示例；PDDL/PDDL3 有 generate/edit/revision 模板；SMT 明示 Z3、输出格式和 100 steps；LTL prompt 详细列出 dynamics、公式范式和多个例子。定位：物理页 24–29，Listings 15–27。
- [OPEN_QUESTION] 未报告各 prompt 的 token 长度、各模型实际 reasoning token、温度的数值、max tokens、重试/解析策略或 API 费用。

## 10. faithfulness false positive

- [AUTHOR_FACT] 正确率只验证最终 plan；生成代码可能错误描述环境或未真正编码 constraint，但计划碰巧通过，从而产生 faithfulness false positive。作者明确承认该风险。定位：物理页 10，§8。
- [AUTHOR_FACT] 作者从“all datasets and methods”抽查 20 个样本，观察到 0 个 false positive，随后称 false-positive rate negligible。定位：物理页 10，§8；短定位文本：“20 samples ... there were no false positives”。
- [READER_INTERPRETATION] 0/20 只能说明这 20 个抽样中未观察到，不能支持跨所有 datasets/methods 的“negligible”强结论；PDF 未给抽样框、分层方式、判定 rubric 或一致性检查。
- [OPEN_QUESTION] 尤其当形式表示可能非唯一时，怎样人工判断“代码没有实际满足 constraint”没有操作化说明；该 faithfulness 结论应保留不确定性。

## 11. 作者明示限制、负向结果与未测试边界

- [AUTHOR_FACT] 作者未覆盖自然语言中所有 constraints/requests；conjunction、negation、ambiguity 留待未来。定位：物理页 10，§8。
- [AUTHOR_FACT] CoPE 仍只覆盖 BlocksWorld 与 CoinCollector 两类 oversimplified proof-of-concept 域；真实世界安全性未验证。定位：物理页 10，§8。
- [AUTHOR_FACT] 引入 constraint 后 syntax error 增多，尤其 PDDL3；revision 后剩余问题主要为 semantic errors，包括 PDDL3 constraint section 错误和 PDDL 缺失/错误 predicates。定位：物理页 7，§6；物理页 8，Figure 4；物理页 17，Figure 7。
- [AUTHOR_FACT] 随 50-block complexity 和 lexical perturbation 增强，无约束 Formalizer 的部分鲁棒性会在约束加入后消失，强模型也可下降超过一半或三分之二。定位：物理页 8–9，Figure 6。

## 12. 可抽取的 Operator 与真实 Failure（仅二读建议，不生成 Card）

- [READER_INTERPRETATION] 可抽取 Operator：先生成无约束形式程序，再以自然语言 constraint 作局部 code edit；必要时利用 parser/compiler/runtime error 迭代修复。
- [READER_INTERPRETATION] 可抽取 Operator：把 constraint 按其收缩 initial state、goal set、action sequence 或 state trace 的位置分类，再选择 PDDL/PDDL3/SMT/LTL 编码接口。
- [AUTHOR_FACT] 可记录 Failure：一句短约束会使多模型、多方法 correctness 大幅下降；complexity 与 lexical shift 会进一步放大下降。定位：物理页 6–9，Figures 2、3、6；物理页 30–33。
- [AUTHOR_FACT] 可记录 Failure：PDDL3 的低资源 syntax/compiler errors；PDDL 对 constraint predicates 的缺失/误用；SMT 的函数/index/step 编码错误；Planner 违反约束、动作前置条件或 hallucinate 不存在的计划。定位：物理页 7–8，Figure 4、§6。
- [READER_INTERPRETATION] 不应抽取为无条件结论：“constraint 一定让每个设置减半”“PDDL 一定胜过 Planner”或“0/20 证明无 faithfulness 问题”；原表存在反例且预算不同。

## 13. 解析文本与可视 PDF 一致性

- [AUTHOR_FACT] PDF 为文本型双栏文档；33 页均可读取。物理页 16 只有附录过渡文字并大面积留白，物理页 17 单独放置 Figure 7，这与渲染一致，不是解析缺页。
- [READER_INTERPRETATION] 未发现改变结论的文本—渲染冲突。需要注意：物理页 3–4 的公式、物理页 6–9 的多面板图，以及物理页 30–33 的长表在纯文本抽取中会错序或挤压；本报告按渲染页的标题、表头和分组复核。Figure 2/5/6 的精确柱高不从抽取文本估读，关键数值以 Tables 3–13 为准。

## 14. 独立结论

- [READER_INTERPRETATION] 论文可靠展示了一个重要边界：给标准规划任务加入短而语义真实的约束，会显著削弱现有 Planner 和多种 Formalizer；Editing 与 solver feedback 能缓解但不能消除问题。
- [READER_INTERPRETATION] 跨 formalism 的排名不能脱离工具链、prompt、horizon、revision 次数和模型版本解释。最可信的是同表、同模型、同方法 before/after constraint 的描述性下降；最弱的是把所有设置概括为统一“减半”或把 0/20 faithfulness 抽查外推为 negligible。
- [OPEN_QUESTION] 若要形成更强机制结论，需要等预算的 planner+validator 基线、固定模型版本、逐题配对统计、revision trace/cost，以及直接验证形式程序是否忠实编码 constraint。
