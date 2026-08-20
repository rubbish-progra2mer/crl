# P071 独立二读报告

## 0. 身份、冻结输入与路径澄清

- paper_id：`P071`
- attempt_id：`r2-20260720-p071-a1`
- 论文：*Agentic Plan Caching: Test-Time Memory for Fast and Cost-Efficient LLM Agents*（NeurIPS 2025；arXiv:2506.14852）
- 最终授权 canonical PDF：`knowledge_base/papers/P071_agentic_plan_caching.pdf`
- PDF SHA-256：`af2ec5f2b4431048ef71d4e090a43a6e9ed9104bcba6dd6d0826c8e26cbc3c8a`
- invocation SHA-256：`663b99950f753bc44f5eb153a9ca355359737ae78d9de71180938a39eb0b07cc`
- prompt：直接使用 `invocation.md` 中的 `Frozen prompt bytes`；冻结 prompt SHA-256 记录为 `ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`
- 完成时间：`2026-07-20T02:55:30+08:00`
- 执行身份：`/root/plan03_blind_evaluator_v1`；具体模型产品名/版本不可验证，记为 `unknown`。
- read boundary：`procedural_blinding`，不是技术文件隔离。
- provenance：`reused independent reader thread due platform thread cap`

[AUTHOR_FACT] 本报告逐页读取并核验最终授权 PDF 的全部 27 个物理页。文本层使用 PyMuPDF 分批读取，视觉层使用 pdfjs-dist/Canvas 在内存中逐页检查；未生成中间文件。

[READER_INTERPRETATION] 本线程此前存在与 P071 无关的独立盲读上下文，故不是全新空线程；本次是线程首次接触 P071，未读取或利用 P071 的 read_1、Cards、其他 read_2、Corpus/saturation/retrieval 材料，也未联网或枚举工作区。

[AUTHOR_FACT] 可观察访问轨迹如下：最初指定的 `knowledge_base/papers/2025-neurips-agentic-plan-caching.pdf` 与 attempt 内 `prompt.md` 均不存在，只发生精确路径检查；随后主任务授权使用 invocation 内嵌 prompt，并最终更正 canonical PDF 为 `knowledge_base/papers/P071_agentic_plan_caching.pdf`。该文件 SHA 与 invocation 记录一致。未读取 invocation 所列 staging PDF、统一 template 或任何其他论文材料。

[READER_INTERPRETATION] 本次只写此 `report.md`，不修改 invocation，不生成 Card、Evidence 或 manifest，不作 Candidate 评价，也不与首读自动调和。

## 1. 方法究竟改变哪一步计算

[AUTHOR_FACT] APC 面向交替执行 Plan/Act 的 agent。传统无缓存路径在每轮由 expensive large planner 依据 query 与累计 actor responses 生成下一 plan 或 final output；APC 把已完成执行中的规划结构提取为 `(keyword, plan template)`，在后续相似任务中复用。（物理页 1–5、22，§1–3.1，图 1–2，算法 1–3）

[AUTHOR_FACT] 每次新 query 先由 lightweight LM 抽取高层 intent keyword，并以 exact keyword lookup 查询 cache。hit 时 small planner LM 根据 query、template 与当前累计 responses 反复适配下一 plan；actor LM 仍访问 task-specific external context 并执行。miss 时 large planner 完整运行，结束后从 execution log 生成 template 并写入 cache。（物理页 4–5、22，§3.1，图 2，算法 1–3）

[AUTHOR_FACT] template generation 是两步过滤：rule-based filter 从 planner/actor log 抽取关键 plan、response、output 并移除冗长 reasoning；lightweight LLM 再删除 entity、number 等 context-specific 内容，保留计划顺序、预期 response 类型与终止结构。（物理页 4–5、24、26–27，§3.1、附录 B.4/D，图 2(c)）

[READER_INTERPRETATION] 核心 operator 不是缓存最终答案，而是缓存“如何索取/处理 context”的控制模板，并把 cache hit 的 planner 从大模型替换成小模型。成本收益同时来自结构复用、prompt 变短、模型价格下降与可能减少 Plan–Act iterations，不能只归因于“计划记忆”一个因素。

## 2. 输入、输出、可用信息与干预时点

[AUTHOR_FACT] 输入为 query `q`、动态 context `ctx` 和当前 cache `C`；输出为最终答案 `o` 与可能更新后的 cache。actor 可访问 external document/table/web environment，planner 在 Minion 数据任务中不直接访问该 context，只通过 actor responses 迭代。（物理页 3–5、22–24，图 1–2、算法 1–3、附录 B.3–B.4）

[AUTHOR_FACT] cache-hit small planner 接收 query、retrieved template 和 past actor responses，生成下一 message 或 final answer；cache-miss large planner 接收 query 与 responses。实验把最大 Plan–Act iterations 设为 10。（物理页 5–6、22，§3.1、§4.1，算法 2–3）

[AUTHOR_FACT] 正文称只有 agent “successfully completes execution with correct outputs”才生成 cache entry；keyword/cache-generation/adaptation prompts 分别要求去除问题特定细节、保持 workflow 顺序和针对当前上下文改写。（物理页 5、24，§3.1、附录 B.4）

[OPEN_QUESTION] “correct output”在真实在线部署中如何被判定没有定义。若使用 benchmark reference/GPT-4o judge 决定是否写入，就是运行期 oracle；若不校验，错误 plan 会进入 cache。附录算法 3 在任何 `o` 产生后都无条件 `GenerateTemplate`，并没有正文所述 success/correctness gate。（物理页 5、22，§3.1 与算法 3）

[READER_INTERPRETATION] intervention 发生在两处：任务到达时决定是否用 small planner 替换 large planner；cache miss 完成后把这次轨迹压缩写回。它是跨测试请求持续演化的 test-time memory，而非冻结模型上的独立 i.i.d. 推理。

## 3. Plan template extraction、matching 与 adaptation 证据

[AUTHOR_FACT] keyword-based exact matching 在 Figure 3 中比 query embedding similarity（threshold 0.7/0.8/0.9）呈现更低 false-positive 与 false-negative；作者认为 query embedding 会过度关注 entity 等 context-specific details。（物理页 5，§3.2，图 3）

[READER_INTERPRETATION] 图 3 没有在正文说明 cache-hit ground truth 如何标注、样本量、置信区间或 keyword extraction 重复稳定性。exact match 的优势依赖 lightweight LM 对同一 intent 始终输出规范化同一字符串；同义 keyword 会变成 false miss，碰撞则 false hit。

[AUTHOR_FACT] 作者主动避免 fuzzy match，因为它重新引入 threshold 与成本问题。FinanceBench 上 exact match hit rate 46%、cost $1.86、accuracy 85.50%；fuzzy threshold >80% 为 54%/$1.15/83.00%，>60% 为 64%/$0.93/77.00%。（物理页 9–10，§4.4，表 6）

[AUTHOR_FACT] lookup microbenchmark 到 `10^6` entries 时 exact hit/miss 为 56/37 µs，SentenceTransformer fuzzy 为约 148 ms；每点平均 100 trials 且每次清 CPU cache。（物理页 9–10，§4.4，表 5）

[READER_INTERPRETATION] fuzzy 相对 exact 确为数量级更慢，但 148 ms 相对于多秒级 LLM round 未必主导 end-to-end latency；论文没有把 fuzzy embedding 预计算、索引结构或 ANN baseline 纳入，因而不能外推为所有 fuzzy retrieval 都不可扩展。

[AUTHOR_FACT] full-history caching 使用同一 keyword-level hit 判定，把完整过去 agent log 当作 small planner ICL；FinanceBench 上它为 $1.99/72.00%，APC 为 $1.86/85.50%。作者归因于小模型难处理长而未过滤的 history。（物理页 6–7、25，§3.2、§4.1–4.2，表 9）

[READER_INTERPRETATION] 这是最近的组合基线，但同时改变了信息结构和上下文长度。APC 获得更短、由 LLM 清洗、显式含 expected response/termination 的 prompt；缺少 length-matched summary、随机模板、只压缩不复用等对照，无法把收益唯一归因于 plan abstraction 而非长上下文减负或额外 prompt engineering。

## 4. 成功轨迹、数据顺序与 test-time 依赖

[AUTHOR_FACT] cache 初始为空；FinanceBench 100-query latency sample 的 hit rate 为 46%，cache miss 生成 entry，后续 query 才能命中。cold-start 表显示随着累计 query 增加，entries 从 15 到 46，hit rate 从 14.29% 到 48.00%。（物理页 8、10，§4.3–4.5，表 3、7）

[READER_INTERPRETATION] 结果依赖 test query 顺序、同一 split 内 intent 的重复频率和先前轨迹质量。论文在 test split 上让较早样本的执行影响较晚样本，属于 transductive online evaluation；若随机顺序或用户分布改变，hit rate、cost、accuracy 都会改变。

[OPEN_QUESTION] 正文未报告任务顺序的多个随机种子、hit-rate 置信区间、cache pollution/recovery、同 keyword 多模板选择或错误 entry 的 invalidation。单一 dictionary key 也无法表达同一 intent 在不同 context 下需要多种互斥 plan 的情况。

[AUTHOR_FACT] 作者称 Table 7 展示“marginal cost and latency”随 warm-up 降低，但表中 cost/latency 是累计值及其占最终总量百分比，随 percentile 单调上升；只有 hit rate 上升是直接显示的。（物理页 10，§4.5，表 7）

[READER_INTERPRETATION] 表 7 本身不能直接支持边际单查询成本/延迟下降，需用相邻区间差分或每 query 平均值重新计算。预热 cache 可缓解 cold start，但必须用与评测/未来请求隔离的 offline samples，否则会引入数据泄漏。

## 5. 主结果与最近基线

[AUTHOR_FACT] Baselines 包括：large planner 始终使用的 Accuracy-Optimal、small planner 始终使用的 Cost-Optimal、query-level Semantic Caching（0.80/0.85/0.90）、以及 keyword-matched Full-History Caching。（物理页 6–7，§4.1）

[READER_INTERPRETATION] Accuracy/Cost-Optimal 给出性能—价格两端，Semantic Caching 检验“缓存答案”，Full-History 检验“复用整段经验”。缺少最关键的路由对照：在相同 hit positions 直接让 small planner 从 query/responses 规划但不给 template，因而无法量化 template 本身相对“预测到可用小模型的任务”贡献多少。

[AUTHOR_FACT] 表 1 中 Accuracy-Optimal→APC 的 cost/accuracy 为：QASPER `$2.14/58.00% → $0.78/57.00%`；AIME 2024 `$1.14/64.52% → $0.85/61.29%`；AIME 2025 `$1.34/61.29% → $0.81/58.06%`；GAIA `$69.02/37.58% → $16.27/36.97%`。（物理页 7–8，§4.2，表 1）

[AUTHOR_FACT] FinanceBench/TabMWP 在主模型组合下 Accuracy-Optimal 为 `$4.03/91.00%`、`$3.35/83.00%`，APC 为 `$1.86/85.50%`、`$2.03/82.00%`。作者总括平均 cost reduction 50.31%、保留 96.61% optimal performance。（物理页 2、6–8、25，§4、图 4、表 9）

[AUTHOR_FACT] GAIA 使用 Open Deep Research architecture，large/small planner 分别 GPT-4o/GPT-4o-mini；APC 成本下降 76.42%，accuracy 只降 0.61 个百分点。作者同时承认 GAIA task space 异质，exact keyword 的 initial planning cache hit 较少。（物理页 7–8，§4.2）

[READER_INTERPRETATION] GAIA 说明 APC 可接入第二种 architecture，但不能证明对多 agent、parallel planner 或任意 Plan–Act 框架普适。低 initial hit 与大成本下降的具体来源（后续哪些 phase 命中、减少多少 large-model calls）未被逐阶段报告。

[OPEN_QUESTION] “50.31% average”和“96.61%”的 macro/weighted averaging unit 没有明确说明：正文称 five workloads，却展示 FinanceBench、QASPER、TabMWP、AIME 2024、AIME 2025、GAIA 六个 benchmark columns；无法判断两个 AIME 年份是否先合并、GAIA 是否同权，以及分母是否按 query、dataset 或 dollar 总额加权。（物理页 2、6–8，§4、表 1）

## 6. 成本、延迟和更长上下文混杂

[AUTHOR_FACT] 主模型为 GPT-4o large planner、Llama-3.1-8B small planner/actor、GPT-4o-mini keyword/template filter。成本按 OpenAI/Together/Anthropic 当时的 input/output token API prices 计算，不是统一 token、FLOP 或 energy。（物理页 6、23，§4.1、附录 B.2，表 8）

[READER_INTERPRETATION] 50.31% 是价格加权 dollar saving，机械地受 GPT-4o 与 Llama/GPT-4o-mini 价差影响；它不等于 token reduction 或 compute reduction，API 调价会改变结论。应同时报告 total input/output tokens、large/small call counts 与 Plan–Act rounds。

[AUTHOR_FACT] 所有 inference 实际经第三方 APIs；temperature 0、max_tokens 4096。作者承认本地 inference 可减少远程服务引入的 latency/throughput variability。（物理页 23，附录 B.2）

[READER_INTERPRETATION] 正文把 Minion actor 描述为“locally hosted”，但附录说全部模型 inference 均经第三方 API；这是部署描述不一致。延迟同时含 provider/network variance，且没有重复运行或误差区间。

[AUTHOR_FACT] FinanceBench 100-query microbenchmark 的累计 Total latency 为 Accuracy-Optimal 1959.24s、Cost-Optimal 1004.79s、APC 1424.82s，APC 相对前者下降 27.28%；APC cache generation 累计 215.80s，54 个 miss 对应约 3.99s/entry。（物理页 8–9，§4.3，表 3）

[READER_INTERPRETATION] 27.28% 只来自 FinanceBench 的一次 100-query、46% hit-rate microbenchmark，不是五/六个 workload 的 latency 平均；摘要/结论把它与跨 workload cost/accuracy 并列为“on average”容易被误读为广泛延迟证据。

[OPEN_QUESTION] 表 3 各组件之和与 Total 不闭合：Accuracy-Optimal `1813.41+94.39=1907.80`，低于 1959.24；Cost-Optimal `856.75+93.31=950.06`，低于 1004.79；APC 已列组件约 1401.35s（lookup <1s），低于 1424.82。剩余系统/网络/调度延迟未命名。（物理页 9，表 3）

[AUTHOR_FACT] Table 2 的 cache overhead 平均 1.04%、zero-hit worst case 1.31%，但只展示 FinanceBench/TabMWP；large planner 仍占 APC 主要 cost（Finance 94.17%，Tab 97.76%）。（物理页 8–9，§4.3，表 2）

[READER_INTERPRETATION] “cache overhead minimal”只计 keyword extraction/template generation 的 dollar cost，未包含 cache storage、privacy/security、embedding/fuzzy index、并发一致性或生产 eviction；且 GAIA 等复杂 workload 未给相同 breakdown。

## 7. Cache size、accuracy 负结果与失败边界

[AUTHOR_FACT] FinanceBench cache size 从 1→100 时 hit rate 2%→46%，cost $3.97→$1.86，total latency 2232.76s→1424.82s；accuracy 却从 92.00% 降至 85.50%，中间为 88/85/86%。增大 cache 并非单调保持准确率。（物理页 9，§4.4，表 4）

[READER_INTERPRETATION] 更高 hit rate 会让更多请求使用 small planner/可能不完全匹配的 template，所以效率提升伴随可见 accuracy tax。作者强调 cost/latency diminishing returns，但没有分析 cache size 导致的 error propagation 或 per-key failure。

[AUTHOR_FACT] Semantic Caching 在较低 similarity threshold 下因 false-positive hit 明显掉准确率；Full-History hit accuracy 也比 miss 低 21%–32%；APC 的 Figure 5 呈现 hit/miss accuracy 较稳定。（物理页 7–8，§4.2，图 5）

[READER_INTERPRETATION] APC hit/miss stability 图没有样本数、误差条和不同 cache-order 重复；hit/miss subsets 的任务难度可能不同，不能视为 matched causal comparison。

[AUTHOR_FACT] sensitivity results 显示模型更小不一定更便宜：Llama-3.2-3B actor 因 response quality 不足触发更多 Plan–Act iterations，常比 Llama-3.1-8B cost 更高且 accuracy 更低。不同 large/small/actor 选择会显著改变结果。（物理页 25，附录 C，表 9–11）

[READER_INTERPRETATION] 这是重要系统失败模式：单次调用便宜不代表 workflow 便宜；缓存适配失败会通过额外 rounds 放大。主结果没有把 rounds/retries 分布报告出来。

[AUTHOR_FACT] 作者明示限制为：主要研究 two-stage Plan–Act；multi-agent cache consistency 未解决；高度动态、任务变化频繁时历史 plan 适用性下降；cache 可能含敏感/专有信息；production-scale integration、advanced lookup/adaptation 仍属未来工作。（物理页 27，附录 E）

[AUTHOR_FACT] 限制段还称 evaluation “primarily emphasizes cost reduction”，future work 可考虑 latency、throughput、computational overhead；这与正文已经报告单一 Finance latency microbenchmark 并不矛盾于“有测 latency”，但表明作者也未把现有 27.28% 视为广泛系统评估。（物理页 27，附录 E）

[READER_INTERPRETATION] 其他未测试边界包括：context/distribution shift、同 keyword 多种 plan、错误 plan invalidation、并发更新、一致性、cache poisoning、跨用户隐私、长期 stale templates、非英语 keyword 稳定性、真实 web/GUI dynamics、不同 query order 和跨 session sharing。

## 8. 评估器、prompt 与 oracle 混杂

[AUTHOR_FACT] application performance 主要用 GPT-4o LLM-as-a-judge；Finance/Tab prompt 接收 question、reference answer 与 model response，允许单位换算、小 rounding/numeric error，输出 1/0。GPT-4o 同时是主 large planner。（物理页 6、23–24，§4.1、附录 B.4）

[READER_INTERPRETATION] planner 与 judge 同模型家族可能带来自偏好/风格相关，且只有 Finance/Tab judge prompt 被完整披露；QASPER/AIME/GAIA 的 evaluator、ground truth 与 scoring path 未在附录同等详细说明。

[AUTHOR_FACT] cache generation prompt 明确要求去掉 entity/numbers、保持 message→loop(output→message/answer) 序列；adaptation prompt 同时提供 cached task、next cached item、current task、past messages/responses。（物理页 24，附录 B.4）

[READER_INTERPRETATION] APC 与 baselines 并非只有 cache representation 不同：它拥有专门设计的 generation/adaptation prompts、额外 GPT-4o-mini filter 以及结构化 expected response。prompt engineering 和额外模型信息可能贡献 accuracy。

[OPEN_QUESTION] Figure 3 的 false-positive/negative 与 Figure 5 的 hit/miss accuracy 是否使用同一 judge/ground-truth、是否在调 threshold 的开发集或最终 test 上计算未说明；若用 test ground truth选择或过滤 cache，存在 oracle/selection leakage。

## 9. 内部冲突与可复核性

[AUTHOR_FACT] 附录算法 3 的 `Require` 包含 `Plan Template template`，但 cache-miss 路径理论上没有 template，且该变量未被使用；同算法也无正文所述 correct-output check。（物理页 22，算法 3）

[READER_INTERPRETATION] 这是算法规格层内部不一致，影响复现者理解何时写 cache、失败轨迹是否被过滤。

[AUTHOR_FACT] 附录 B.3 把 `TabMWP` 写成 `TabMVP`，正文/表格均用 TabMWP；属于命名排版错误。（物理页 23，附录 B.3）

[AUTHOR_FACT] NeurIPS checklist 自称主实验有适当 error bars/statistical significance，但正文主要 cost/accuracy/latency tables 是单点结果，未说明多次运行、标准差或置信区间；Figure 3/5 也无误差条。（物理页 7–10、17–18，§4、checklist item 7）

[READER_INTERPRETATION] checklist 是作者声明，不能替代实际统计报告。API latency、query ordering、keyword generation 和 judge 都有随机/系统变异，主结论需要重复运行或 bootstrap over queries。

## 10. Operator 候选（仅供主 Codex 后续裁决）

1. [READER_INTERPRETATION] **O1：高层 keyword exact-match routing。** 用小模型把 query 规范化成 intent key，O(1) 查找 plan template。（物理页 4–5、22，图 2、算法 1）
2. [READER_INTERPRETATION] **O2：成功轨迹的 rule+LM plan abstraction。** 从完整 execution log 提取顺序、预期 response 和 termination，去除 context specifics。（物理页 5、24、26–27）
3. [READER_INTERPRETATION] **O3：cache-hit small-planner adaptation。** 以 template 和实时 actor responses 迭代改写，而非复用最终答案。（物理页 5、22、24，算法 2）
4. [READER_INTERPRETATION] **O4：large-miss/small-hit model routing。** 只在 miss 用 expensive planner，hit 用 cheap planner。（物理页 4–6，图 2）
5. [READER_INTERPRETATION] **O5：test-time cache warm-up + LRU capacity control。** 随请求流写入，按 cache size/hit rate 调整成本。（物理页 9–10，表 4、7）
6. [READER_INTERPRETATION] **O6：低 hit-rate 自动停用。** zero-hit 监控后关闭 cache，以避免持续生成无用 entry；论文只描述策略，未给动态 controller 实验。（物理页 8–9，§4.3）

## 11. Failure 候选（仅供主 Codex 后续裁决）

1. [READER_INTERPRETATION] **F1：keyword collision/同义漂移。** exact key 可 false hit 或 false miss，缺少多模板消歧。（物理页 5、10，§3.2、表 6）
2. [READER_INTERPRETATION] **F2：错误/不适用 plan cache pollution。** correctness gate 未规格化，也无 invalidation/feedback repair。（物理页 5、22）
3. [READER_INTERPRETATION] **F3：full-history long-context overload。** 小 planner 无法从冗长日志稳定抽取可复用结构。（物理页 6–8，图 5）
4. [READER_INTERPRETATION] **F4：更高 hit rate 带来 accuracy tax。** cache size 1→100 时 accuracy 92%→85.5%。（物理页 9，表 4）
5. [READER_INTERPRETATION] **F5：cold start 与低重复分布。** dynamic/heterogeneous workload 让 miss 和 template generation 主导。（物理页 7–10、27，GAIA、表 7、Limitations）
6. [READER_INTERPRETATION] **F6：cheap model 触发更多 rounds。** 单次便宜但 workflow 成本/延迟更高且准确率更低。（物理页 25，表 11）
7. [READER_INTERPRETATION] **F7：query-order/transductive dependence。** 较早 test execution 决定较晚结果，单次排序不可泛化。（物理页 10，表 7）
8. [READER_INTERPRETATION] **F8：template 丢失关键 context 或保留敏感信息。** abstraction 与 privacy/security 均无自动保证。（物理页 24、27）
9. [READER_INTERPRETATION] **F9：价格/模型替换混杂。** dollar saving 随 API 价差变化，未等价证明 token/compute saving。（物理页 23，表 8）

## 12. 解析文本与视觉 PDF 核对

[AUTHOR_FACT] 文本层与视觉层均覆盖物理页 1–27。视觉核对确认：方法图与 keyword evidence 在页 3–5，主 setup/results 在页 6–10，算法在页 22，平台/数据/prompt 在页 23–24，model sensitivity 在页 25，workflow/template 示例在页 26–27，正式 limitations 在页 27。

[READER_INTERPRETATION] 未发现影响本报告结论的解析文本—视觉 PDF 冲突；本报告引用的表 1–11、图 1–5 与算法 1–3 的页序、表头和关键数值与视觉页一致。所列算法/命名/latency sum 问题是论文源内容内部不一致，而非解析错误。

## 13. 独立性声明

[READER_INTERPRETATION] 本报告仅记录冻结输入下的作者事实、独立解释、开放问题以及 Operator/Failure 候选，并提供物理页/章节/图表/短定位；未接收首读结论，未生成正式 Card/Evidence，未执行 Candidate、novelty/prior-work 或科研裁决。
