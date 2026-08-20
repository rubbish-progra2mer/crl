# P070 独立二读报告

## 0. 身份、冻结输入与读取边界

- paper_id：`P070`
- attempt_id：`r2-20260720-p070-a1`
- 论文：*ProMCP: Profiling Token Flows and Latency Costs in Model Context Protocol–Based LLM Agents*（Findings of ACL 2026；ACL Anthology `2026.findings-acl.1967`）
- 冻结 PDF：`knowledge_base/staging/plan05_sat_a1/P070_promcp.pdf`
- PDF SHA-256：`d67090fae5dd6eef7edb633ad9e3b7f4b3873b48fea8276aecb5d5877377f777`
- invocation SHA-256：`aedfedae785bbd1ccfdb953ec5147465002024c42618a268f2a4204d09b2c259`
- 统一 prompt SHA-256：`ffb7c12e663f44318d8eda1c270cbc26ad66665fd803247a2ab66a8f23fa333a`
- 完成时间：`2026-07-20T02:45:05+08:00`
- 执行身份：`/root/plan03_blind_evaluator_v1`；具体模型产品名/版本不可验证，记为 `unknown`。
- read boundary：`procedural_blinding`，不是技术文件隔离。
- provenance：`reused independent reader thread due platform thread cap`

[AUTHOR_FACT] 本报告逐页读取并核验指定 PDF 的全部 12 个物理页。文本层使用 PyMuPDF 分批读取，视觉层使用 pdfjs-dist/Canvas 在内存中逐页渲染，并对表 1–2 另行放大检查；未生成中间文件。

[READER_INTERPRETATION] 本线程此前存在与 P070 无关的独立盲读上下文，因此不是全新空线程；本次是线程首次接触 P070，未读取或利用 P070 的 read_1、Cards、其他报告、其他论文读稿、Corpus/saturation/retrieval 材料，也未联网或枚举工作区。

[AUTHOR_FACT] 可观察访问轨迹仅包括本 attempt 的 `invocation.md`、统一 `second_read_prompt.md`、指定 `P070_promcp.pdf`，以及对目标 `report.md` 是否存在的精确检查。

[READER_INTERPRETATION] 本报告只进行独立核源，不生成 Card、Evidence 或 manifest，不作 Candidate 评价，也不与首读自动调和。

## 1. 方法究竟改变哪一步计算

[AUTHOR_FACT] ProMCP 是观察性 profiling/instrumentation framework，不改变 agent 的 prompt、tool output 或决策。它在 MCP Host–Client–Server 边界记录消息、时间戳、payload、model/tool/transport metadata，并把一次 tool-augmented interaction 分成六个通信阶段。（物理页 2–5、11，§3.1–3.3、附录 A.2，图 1）

[AUTHOR_FACT] 六阶段为：S1 User→LLM prompting；S2 LLM→Client planning；S3 Client→Server tool call；S4 Server→Client tool response；S5 Client→LLM context update；S6 LLM→User answer synthesis。多工具/多轮任务重复这些事件，最终按任务聚合。（物理页 3–4，§3.1，定位：`Six-stage decomposition`）

[AUTHOR_FACT] 框架对每个阶段记录 token footprint 与 latency，并另聚合为 tool-plan（S1–S2）、tool-execution（S3–S4）、answer-synthesis（S5–S6）三个面向用户的段。它还把 session initialize、metadata exchange、`tools/list` schema discovery 与 readiness 作为六阶段之前的 first-class hidden cost 单独记录。（物理页 4–5，§3.1–3.3，图 1）

[AUTHOR_FACT] token 计算区分两类量：provider/local tokenizer 给出的 LLM usage tokens，以及 schema、JSON tool call、tool result 等 MCP artifact 在相同 tokenizer 下的 protocol token footprint。后者在被注入 LLM context 时才成为推理成本。（物理页 4，§3.2，定位：`Token footprint vs. LLM usage tokens`）

[READER_INTERPRETATION] 真正新增的计算是跨组件 event correlation 与阶段归因，而非一个改善任务效果的新 agent 算法。论文后续关于优化 schema 或结果压缩的建议来自 profiling 观察，并未作为受控 intervention 实施。

## 2. 输入、输出、可用信息与干预时点

[AUTHOR_FACT] 每条 log 包含 run/task/stage/semantic phase/direction 标识，高精度发送与接收时间戳，模型、server、tool、transport，LLM token usage、MCP artifact token footprint，以及截断 payload preview；敏感字段可在发布日志中 redact/hash。（物理页 4，§3.2，定位：`Unified event log`）

[AUTHOR_FACT] custom client 的 L-Cust/C-Cust 在执行时直接 hook LLM 与 server 消息；local tokens 用本地模型 tokenizer，cloud tokens 对齐 provider usage 与 client trace。C-OTS 无协议级 trace，只能从导出的 `conversations.json` 识别 tool-use messages、映射 S1–S6、用对应 tokenizer 计数并从 timestamp delta 重建 latency。（物理页 6，§3.5）

[AUTHOR_FACT] latency 在 instrumented component 的单调时钟边界测量：LLM 阶段从 dispatch 到 completion/最后 streamed chunk；S3–S4 从 JSON-RPC request emission 到相应 response receipt。初始化、schema discovery 与正式任务阶段分开报告。（物理页 4–5，§3.2–3.3）

[READER_INTERPRETATION] 对 custom client，干预点是运行时观测 hook；对 C-OTS，只有用户可见导出日志后的 post-hoc reconstruction。两者的可用信息强度不同，统一 CSV/JSON schema 只是输出格式一致，不代表底层可观察性一致。

[OPEN_QUESTION] 报告表把六个方向阶段压缩成 `context/llm_plan/tool_call/tool_result/final_ans` 五个 data phases，未无歧义说明 S5 context update、schema injection、重复注入的 LLM input tokens 分别落在哪一列，也未说明 protocol footprint 与 usage token 在总量中如何避免重复计数。（物理页 4、8，§3.1–3.2，表 1）

## 3. 六阶段成本归因与 hidden initialization

[AUTHOR_FACT] 初始化先执行 handshake、metadata exchange、`tools/list` 与 readiness；schema discovery 的 token footprint 在不同 server 间差异明显。作者将它与任务执行成本分开，以避免被静默摊销或忽略。（物理页 4–5、6–7，§3.3、§4.3.1，图 1–3）

[AUTHOR_FACT] Figure 2/3 中 tools discovery 主导初始化 token；HTTP/SSE 初始化 latency 低于 STDIO。作者将差异归因于 STDIO 每次连接启动新 subprocess 的 cold start，而 HTTP server 通常 warm/persistent；连接建立后，双方 discovery latency 都很小。（物理页 6–7，§4.3.1，图 2–3）

[READER_INTERPRETATION] 这不是 HTTP/SSE transport 本身普遍快于 STDIO 的纯协议对照，而是 warm persistent server 与 cold subprocess lifecycle 的组合差异。若 STDIO server 复用或 HTTP cold start，结论可能变化。

[OPEN_QUESTION] initialization 没有并入表 1–2 的 per-task Total，也未按 session 内任务数给 amortized cost；短 session、频繁重连与长期复用会得到完全不同的用户均摊开销。（物理页 5、7–8，§3.3、§4.3.1–4.3.3）

[READER_INTERPRETATION] 作者由“连接后 discovery latency 很小”进一步称 schema transmission bandwidth-bound rather than compute-bound，但没有改变 schema payload、带宽或 CPU 作受控实验；这是合理假设而非充分识别的瓶颈因果。

## 4. 不同拓扑的瓶颈及其边界

[AUTHOR_FACT] 三个拓扑是：L-Cust（local LLM + custom FastMCP client + STDIO）、C-Cust（Claude Sonnet 4.5 API + custom FastMCP client）、C-OTS（Claude Sonnet 4.5 + Claude Desktop，内部 orchestration 不可见）。（物理页 5–6，§3.4、§4.2）

[AUTHOR_FACT] MCP-Bench 含 30 个结构化 single-server tasks，评估 15 servers/151 tools；MCP-Universe 含 125 个更开放、多步、较大 tool response 的 tasks，覆盖 8 servers。两套合计为 20 servers/169 tools。（物理页 6，§4.1）

[AUTHOR_FACT] MCP-Bench 上 custom clients 的 `llm_plan` token 占比为 52.0%–63.2%；C-OTS planning 仅 2.1%，而 `tool_result/final_ans` 为 48.6%/43.0%。作者称 C-OTS 使用 deferred loading 降低 tool-list search tokens。（物理页 7–8，§4.3.2，表 1）

[AUTHOR_FACT] MCP-Universe 上 C-Cust 和 L-Cust(Mistral) 的 `tool_result` 分别占 77.5% 和 81.8%；L-Cust(LLaMA) 只有 20.0%。C-OTS 总量报告为 1,282,317 tokens，其中 `tool_result` 1,063,220（82.9%），远高于 custom setups。（物理页 7–8，§4.3.2，表 1）

[AUTHOR_FACT] 作者把 C-OTS 极高 tool-result token 主要归因于 WebSearch 全量多文档结果跨轮保留并重复消费；Desktop 将 raw JSON、metadata、headers、auxiliary fields 直接注入 context，而 custom clients 只抽取 task-relevant data。作者明确说这是 client orchestration policy，不是 MCP protocol requirement。（物理页 8，表 1 后段）

[READER_INTERPRETATION] “OTS output/tool-result bottleneck”不能外推为所有 OTS clients 的固有性质；它高度依赖此版本 Desktop 的 deferred loading、raw-result retention、WebSearch 使用和生成策略。相反，custom schema bottleneck 也依赖一次给模型暴露大量 schemas 的 client policy。

[AUTHOR_FACT] latency 上，MCP-Bench 的 L-Cust(Mistral/LLaMA)、C-Cust、C-OTS Total 分别为 1.28/3.90/22.76/94.86 秒；MCP-Universe 分别为 73.53/41.43/46.61/382.05 秒。C-OTS 的 `final_answer` 在两套任务分别占表中 86.4% 和 75.0%。（物理页 8–9，§4.3.3，表 2）

[AUTHOR_FACT] L-Cust Mistral 在 MCP-Universe 的 planning 为 46.84±113.38 秒，作者描述为在重 context 下可能“hanging”或低效；LLaMA 从 3.90 增至 41.43 秒但方差较低。C-Cust 的 simple-task planning 已为 14.60 秒，作者归因于 cloud prefill/system+tool definitions 的 latency floor。（物理页 8–9，§4.3.3，表 2）

[READER_INTERPRETATION] Bench→Universe 不是只改变“任务复杂度”：任务数、server 集、tool response 大小、交互深度和执行路径同时变化。因此模型 scaling/bottleneck shift 是 workload-level 观察，不能唯一归因于 context complexity。

## 5. Tool runtime 结论的适用范围

[AUTHOR_FACT] 表 2 在当前任务上报告 custom setups 的 `tool_call` 和 `tool_result` latency 通常远小于 planning/final answer；论文据此称实际 tool execution 在所有配置中占比很小。（物理页 8–9，表 2、Conclusion）

[AUTHOR_FACT] 作者在 Limitations 明确限定，这些 benchmark 使用 lightweight-to-moderate tools；生产环境中的重 I/O、数据库、远程服务或长计算可能进入完全不同 regime。ProMCP 可以通过 S3–S4 揭示这种 regime shift，但论文没有实测。（物理页 9，Limitations，定位：`lightweight-to-moderate tools`）

[READER_INTERPRETATION] 因此可支持的结论是“在这 20 个 server/两套 workload/当前运行路径中，orchestration latency 主导”，不能写成“MCP tool runtime 一般可忽略”或“优化工具执行永远无收益”。

[OPEN_QUESTION] S3–S4 从 client request emission 到 response receipt，天然混合 request serialization、transport、server queue、tool compute 和 response transfer；论文没有 server-internal span，因此即使工具变重，也未必能把纯 tool compute 与网络/排队完全分离。（物理页 3–4，§3.1–3.2）

## 6. Post-hoc reconstruction 的限制

[AUTHOR_FACT] C-OTS 只从 `conversations.json` 中的 user-visible tool-use messages 与 timestamps 重建阶段；作者承认它看不到导出数据之外的 intermediate states、内部 retries、精确毫秒级 jitter。（物理页 6、9，§3.5、Limitations）

[AUTHOR_FACT] C-OTS 由 provider 管理 streaming/buffering，max plan/synthesis tokens 为 unconstrained，temperature/top-p 为 provider defaults，retry policy 不暴露；L-Cust/C-Cust 则关闭 streaming，分别使用 T=0.8/1.0，plan/synthesis 上限 12K/10K，最多 10 rounds、3 retries、sequential tools、caching off。（物理页 11，附录 A.1，表 3）

[READER_INTERPRETATION] C-OTS 的 `final_answer` timestamp delta 可能吸收不可见 planning、buffering、retry 或 transport time。因而 75%–86.4% 的“answer synthesis”是按可见消息边界的归属，不等同于 provider 内部纯 decoder compute。

[READER_INTERPRETATION] C-Cust vs C-OTS 虽使用同一 Claude family，是最近的 client-implementation 对照，但 streaming、token limits、prompt orchestration、result filtering、retry、buffering 全部同时变化。瓶颈“反转”是整套 deployment policy 的结果，不是单一 OTS/custom 开关的因果效应。

[OPEN_QUESTION] 若没有 provider-side spans 或同步 instrumentation，C-OTS 无法验证 deferred loading 的内部耗时、隐藏 schema search、重试和 first-token latency；post-hoc trace 可用于用户可见 end-to-end accounting，但不适合精确内部阶段因果归因。

## 7. 最强与最近基线

[AUTHOR_FACT] ProMCP 没有与另一个 profiler 或非-MCP direct-tool stack 做对照；实证基线就是 L-Cust、C-Cust、C-OTS 三个 deployment configurations，以及 MCP-Bench/MCP-Universe 两类 workload。（物理页 2–3、5–9，§2–4）

[READER_INTERPRETATION] 因为缺少“同模型、同 prompt、同 tool path、同 transport 的非-MCP”对照，论文测得的是实际 MCP stack 的阶段成本，而不是 MCP 相对传统工具集成的**增量 protocol overhead**。标题和贡献中的 protocol overhead 应理解为内部归因，不是 causal overhead delta。

[READER_INTERPRETATION] 最近组合基线是 C-Cust vs C-OTS：两者都标为 Claude Sonnet 4.5，可比较 custom 与 commercial stack；但前述配置/可观测性差异阻止纯 client programmability 归因。L-Cust Mistral vs LLaMA 更适合展示模型对相同本地拓扑的敏感性，而不是拓扑效应。

[AUTHOR_FACT] 100-task quality audit 报告 L-Cust(Mistral/LLaMA)、C-Cust、C-OTS 的 tool accuracy 为 85/91/92/100%，execution success 为 81/87/89/100%，human quality 为 4.06/4.52/4.64/4.91。（物理页 9、11，§4.3.3、附录 A.2，表 4）

[READER_INTERPRETATION] 各配置并非同等成功/质量：更高成本的 C-OTS 同时有更高 accuracy/quality，custom clients 的 tool failure 还可能 fallback 到内部知识并改变 final-answer 成本。不能只凭“均为高质量”排除 cost–quality trade-off，也不能把不同执行路径视为完全 matched workload。

## 8. 模型、token、tool-call、prompt 与 oracle 混杂

[AUTHOR_FACT] L-Cust 使用不同本地模型，C-Cust/C-OTS 才共享 Claude family；各拓扑的 temperature、streaming、token limits、retry 可见性和 result retention 不同。（物理页 6、11，§4.2、表 3）

[READER_INTERPRETATION] 所谓 topology effect 同时混合模型算力/架构、API 网络、client policy、prompt、streaming 和 tool path。论文的 stage breakdown 能描述这些差异在哪里显现，但不能仅凭观察决定哪个单因导致差异。

[AUTHOR_FACT] 作者承认模型 tokenizer 的绝对 token 不可直接比较，并仅在 MCP-Bench 的 S1 user prompts 上测得 Mistral/LLaMA/Claude token counts 与 LLaMA 的 Pearson `r≥0.99`。（物理页 11–12，附录 A.3，表 5）

[READER_INTERPRETATION] S1 短 user prompts 的近线性不能证明大型 JSON schemas、嵌套 tool results、代码和多轮重复 context 也保持同一比例；“relative rankings invariant regardless of tokenizer”超过了该项验证的直接范围。

[AUTHOR_FACT] L-Cust/C-Cust 限制 10 rounds、3 retries、sequential tools 并关闭 cache，C-OTS retry/并行不可见。MCP-Bench 中 tool failure 后有时 fallback 到 LLM internal knowledge。（物理页 7、11，§4.3.2、附录 A.1）

[READER_INTERPRETATION] tool-call 数、retry、成功路径和 fallback 不同会直接改变每阶段 tokens/latency。论文没有报告按成功任务、调用次数或相同 trace length 配平的结果。

## 9. 作者限制、负结果与未测试边界

[AUTHOR_FACT] 作者明示三项限制：C-OTS 依赖 post-hoc reconstruction；仅一台 Windows 11/RTX 4090/i9-13900K/64GB 硬件，OS scheduling/STDIO buffer 的跨平台差异未测；tool-runtime 结论只覆盖轻至中等工具。（物理页 6、9，§4.2、Limitations）

[AUTHOR_FACT] 主要负结果包括：Mistral local 在复杂 workload 的 planning latency 与方差激增；C-OTS 在 MCP-Universe 发生超过 1.2M token 的结果膨胀及约 382 秒总 latency；custom clients 因全量 schema 暴露形成固定 planning overhead；STDIO cold start 拉高初始化。（物理页 6–9，图 2–3、表 1–2）

[AUTHOR_FACT] custom clients 并非总能成功调用工具，失败后可能使用模型内部知识回答；quality audit 的最低 execution success 为 81%。（物理页 7、11，§4.3.2、表 4）

[READER_INTERPRETATION] 尚未测试的关键边界包括：Linux/macOS、不同网络 RTT/带宽、warm STDIO、更多 OTS clients/providers、重数据库/远程 API/GPU jobs、parallel tools、cache、不同 schema 压缩/检索策略、长 session 初始化摊销、provider-side spans，以及在等质量/等成功/等 tool trace 下的 topology ablation。

## 10. Operator 候选（仅供主 Codex 后续裁决）

1. [READER_INTERPRETATION] **O1：六阶段跨边界 event correlation。** 用 run/task/stage/timestamp 把 Host–Client–Server 消息统一到 S1–S6。（物理页 3–5，§3.1–3.2，图 1）
2. [READER_INTERPRETATION] **O2：usage tokens 与 protocol footprint 分账。** 将 LLM 推理/生成用量和 schema/JSON/result 表征成本分开。（物理页 4，§3.2）
3. [READER_INTERPRETATION] **O3：初始化与 tools discovery first-class accounting。** 不把 pre-query schema 成本静默忽略。（物理页 4–7，§3.3、§4.3.1）
4. [READER_INTERPRETATION] **O4：stage-aligned topology normalization。** 把 local/API/OTS traces 转为平行 CSV/JSON 以做阶段统计，但需携带 observability level。（物理页 5–6，§3.5）
5. [READER_INTERPRETATION] **O5：结果保留/压缩策略 profiling。** 追踪 raw tool results 的跨轮重复注入，定位 context inflation。（物理页 7–8，§4.3.2）
6. [READER_INTERPRETATION] **O6：plan/tool/synthesis 三段用户视角账本。** 将 S1–S6 聚合成可解释的 end-to-end latency segments。（物理页 4，§3.1）

## 11. Failure 候选（仅供主 Codex 后续裁决）

1. [READER_INTERPRETATION] **F1：全量 schema 注入造成固定 planning/prefill 开销。** 在 custom clients 的简单任务上尤其突出。（物理页 7–9，表 1–2）
2. [READER_INTERPRETATION] **F2：raw tool result 跨轮保留与重复消费。** C-OTS/WebSearch 产生百万级 context inflation。（物理页 7–8，表 1 后段）
3. [READER_INTERPRETATION] **F3：本地模型在重 context 下 planning collapse/high variance。** Mistral Universe 结果最明显。（物理页 8–9，表 2）
4. [READER_INTERPRETATION] **F4：STDIO cold subprocess 启动罚时。** 会被误当 transport 固有延迟。（物理页 6–7，图 3）
5. [READER_INTERPRETATION] **F5：tool failure 后 fallback 改变成本归因。** 成本下降/转移不代表工具路径成功。（物理页 7、11）
6. [READER_INTERPRETATION] **F6：post-hoc OTS 阶段错归。** 不可见 retry/buffering/planning 可能被计入 final answer。（物理页 6、9、11）
7. [READER_INTERPRETATION] **F7：轻工具外推错误。** 当前 S3–S4 很小不能代表重 I/O/长计算。（物理页 9，Limitations）
8. [READER_INTERPRETATION] **F8：topology/model/config 混杂。** 观察到瓶颈反转却无法识别单一因果开关。（物理页 5–6、11，§3.4、表 3）
9. [READER_INTERPRETATION] **F9：表格聚合/算术口径不透明。** 若 total、phase mean 与百分比不能闭合，会削弱精确成本基线的可复核性。（物理页 8，表 1–2）

## 12. 解析文本、视觉 PDF 与表内一致性

[AUTHOR_FACT] 文本层与视觉层均覆盖物理页 1–12。视觉核对确认：六阶段定义在页 3–4，架构图与 hidden initialization 在页 5，topology normalization/workloads 在页 6，初始化图和 token 解释在页 7，表 1–2 在页 8，结论与限制在页 9，evaluation card/quality/tokenizer 在页 11–12。

[READER_INTERPRETATION] 未发现文本解析与视觉 PDF 的版式冲突；放大页 8 后，关键数值与文本提取一致。但论文表格本身存在无法由取整解释的内部不闭合，属于 source-level discrepancy。

[OPEN_QUESTION] 表 1 的 MCP-Bench L-Cust(LLaMA) 五阶段均值相加为 `405+3026+63+1477+1851=6822`，而 Total 印为 5822；列百分比相加为 117.2%。表 2 也有多列百分比超过 100%（如 Bench C-Cust 为 103.5%，Universe Mistral/LLaMA/C-Cust 分别约 102.2%/103.3%/102.8%），部分阶段均值之和与 Total 不同。正文未说明这是每任务比例平均、缺失阶段条件统计、排版错误或其他 denominator，需作者澄清。（物理页 8，表 1–2）

## 13. 独立性声明

[READER_INTERPRETATION] 本报告仅记录冻结输入下的作者事实、独立解释、开放问题以及 Operator/Failure 候选，并提供物理页/章节/图表/短定位；未接收首读结论，未生成正式 Card/Evidence，未执行 Candidate、novelty/prior-work 或科研裁决。
