# P068 独立二读报告

## 0. 读取身份、边界与完整性

- `[AUTHOR_FACT]` 论文：Yukun Huang、Leonardo F. R. Ribeiro、Momchil Hardalov、Bhuwan Dhingra、Markus Dreyer、Venkatesh Saligrama，*DeepFact: Co-Evolving Benchmarks and Agents for Deep Research Factuality*，ACL 2026 Long Papers，ACL Anthology `2026.acl-long.1586`（PDF p.1，标题页）。
- `[AUTHOR_FACT]` 本次唯一论文源为 `knowledge_base/staging/plan05_sat_a1/P068_deepfact.pdf`；实测 SHA-256 为 `a26aeaefd0f1c763a40c1383c3a18ac723629519f6089abcdfe85ad74057f079`，与 invocation 冻结值一致；PDF 共 31 页。
- `[READER_INTERPRETATION]` Provenance: reused independent reader thread due platform thread cap
- `[READER_INTERPRETATION]` 本报告只读取本 attempt 的 `invocation.md`、其中内嵌冻结统一 prompt、指定 PDF 与已在同一复用线程中完成复核的必要规则；未读取 read_1、Cards、其他报告、其他论文读稿、Corpus/saturation/retrieval 文件，未联网。
- `[READER_INTERPRETATION]` 已按 PDF p.1–31 顺序提取每页文本并逐页执行内存视觉渲染；每页文本均非空，流程图、结果表、算法、附录表及案例未见 parsed text 与视觉 PDF 的实质冲突。

## 1. 一句话技术结论

- `[AUTHOR_FACT]` Audit-then-Score（AtS）把 benchmark 从固定 `(claim,context,label)` 改成版本化 `(claim,context,label,rationale)`：Challenger 先独立给 verdict/rationale，只有与当前 label 不同的项目进入 audit；Auditor 接受的 evidence-backed proposal 先改写 benchmark，再用改写后的版本给该 Challenger 计分（PDF p.2、5，Figure 1，§5.1；PDF p.22，Algorithm 1）。
- `[READER_INTERPRETATION]` AtS 的核心价值是让强 verifier 能暴露并纠正静态 gold 错误；其核心审计盲区也来自同一 gate：benchmark 与 Challenger **同错同标签**、或同标签但 rationale/证据错误时，不会进入 audit，故 AtS 不能自动发现 consensus mismatch（PDF p.22，Algorithm 1 lines 8–10）。
- `[AUTHOR_FACT]` DeepFact-Eval 输入单个 sentence-level claim 和完整 DRR context，通过 query planning、外部检索、全文摘要、定向问答与反思迭代输出三类 verdict 和 evidence-backed rationale；主结果最终把 Contradictory 与 Inconclusive 合并成 Unsupported，报告二分类性能（PDF p.3、5–6，§3.1、§6.2，Figure 2；PDF p.8，§8.2）。
- `[READER_INTERPRETATION]` DeepFact-Bench v4 与 DeepFact-Eval 并非完全独立：v4 的 Round 2/3 直接使用 DeepFact-Eval GPT-4.1/GPT-5 作为 Challenger 修订 label/rationale，之后同一方法家族再在 v4 上报告 83.4%/87.2%；这不等于标签被模型单方面决定，但形成 benchmark–verifier 共演化依赖，应与“冻结快照上的独立泛化”区分（PDF p.6，§6.3；PDF p.8，Table 2）。

## 2. 冻结问题逐项回答

### Q1. 方法究竟改变哪一步计算？

- `[AUTHOR_FACT]` 静态评测以 one-shot human label `y_i^h` 为固定 gold，按 verifier prediction 与其 exact match 计分（PDF p.3–4，§3.2）。
- `[AUTHOR_FACT]` AtS 把 benchmark state 写为 `B_t={(c_i,d_i,y_i^(t),ρ_i^(t))}`，其中 verdict 与 rationale 都有版本；Challenger `M_t` 对 `(c_i,d_i)` 产生 `(ŷ_i,ρ̂_i)`（PDF p.4–5，§5.1）。
- `[AUTHOR_FACT]` 当且仅当 `ŷ_i≠y_i^(t)` 时形成 proposal；Auditor 比较新旧 rationale，接受后以新 verdict/rationale 替换旧状态，生成 `B_(t+1)`；最后用 `B_(t+1)` 给发起挑战的模型评分（PDF p.5，§5.1；PDF p.22，Algorithm 1）。
- `[READER_INTERPRETATION]` 改变发生在 benchmark supervision 与评分顺序，不是 verifier loss：传统是“固定 gold→score”，AtS 是“预测→分歧审计→更新 gold→score”。
- `[READER_INTERPRETATION]` 每个被接受的 challenge 在更新后必然与 Challenger prediction 一致，因此该项目会从旧版“错”变成新版“对”；Auditor 是阻止自证循环的唯一外部门槛，score 的可信度取决于 audit 独立性与证据质量。

### Q2. 输入、输出、可用信息与干预时点

- `[AUTHOR_FACT]` benchmark item 的 verifier 输入是 verbatim sentence `c_i` 与完整 DRR `d_i`；报告上下文用于消歧。输出是 `Supported/Inconclusive/Contradictory` verdict 和 rationale（PDF p.3，§3.1；PDF p.5，§6.1–6.2）。
- `[AUTHOR_FACT]` DeepFact-Eval 读取周边报告，生成 breadth-oriented queries，检索并摘要候选文档，再对摘要做 targeted Q&A 以恢复关键细节；若证据不足则继续 retrieve–interrogate–reason loop（PDF p.5–6，Figure 2，§6.2）。
- `[AUTHOR_FACT]` 实现上 verifier 为 GPT-4.1、全文摘要用 GPT-4.1 mini；最多 2 个 iteration、每步 5 queries、保留最多 40 sources、每次请求最多 8192 completion tokens（PDF p.17，§C.2–C.3）。
- `[AUTHOR_FACT]` DeepFact-Eval-lite 将语义相关、共享证据和 report context 的 claims 分组联合验证，Table 2 报告 group=5 与 group=10（PDF p.6，§6.2；PDF p.8，Table 2）。
- `[OPEN_QUESTION]` 论文未给出 lite 分组的 embedding/model、相似度阈值、组内 prompt、冲突拆分规则，因而无法判断共享上下文是否会造成跨 claim 污染或标签互相锚定。
- `[AUTHOR_FACT]` AtS audit 时 human expert 只审查 Challenger 与当前 benchmark 的 label disagreement，并看到 agent verdict/rationale；Round 1 不要求专家新写 rationale，Round 2 起更新时也写自己的 rationale（PDF p.16–17，§B.5）。
- `[OPEN_QUESTION]` Algorithm 1 的 Auditor 函数形式只比较 `ρ̂_i` 与 `ρ_i^(t)`，未显式传入 claim、context 或原始 evidence；正文/UI 暗示 auditor 可查看上下文，但实现级可用信息未形式化（PDF p.5、22）。

### Q3. 最强基线与最接近组合基线

- `[AUTHOR_FACT]` 同 GPT-4.1 backbone 的传统 baselines 为 FactCheck-GPT、SAFE、VeriScore、FIRE；deep-research baselines 为 GPT-Researcher Deep/Deep+ 与 SmolAgents（PDF p.8，§8.1，Table 2）。
- `[AUTHOR_FACT]` 主表最强传统 baseline 是 FIRE 58.5%，最强 deep-research baseline 是 GPT-Researcher Deep 69.1%；DeepFact-Eval GPT-4.1 为 83.4%，分别高 24.9 与 14.3 points（PDF p.8，Table 2）。
- `[AUTHOR_FACT]` 最接近的 compute-matched 组合对照是 DeepFact-Eval Group=10 与 GPT-Researcher Deep：成本约 `$0.21` 对 `$0.18`，accuracy 76.3 对 69.1；Group=5 为 `$0.30`、77.9（PDF p.8–9，Table 2，§8.2）。
- `[READER_INTERPRETATION]` Full DeepFact-Eval 与 GPT-Researcher 不等配：前者 516.9K input/18.6K output/$1.16，后者 52.3K/9.0K/$0.18；因此 full 83.4% 的一部分可能来自近 10 倍 input token 与 6.4 倍 API cost。Group=10 的 +7.2-point 结果更接近隔离 workflow 效果。
- `[AUTHOR_FACT]` 更强 backbone 的 DeepFact-Eval GPT-5 为 87.2%，Gemini-2.5-Pro 为 81.5%，Qwen3-32B 为 72.5%；它们是 model ablation，不能与 GPT-4.1 baselines 作同模型归因（PDF p.8，Table 2）。
- `[READER_INTERPRETATION]` 传统方法先用 GPT-4.1 拆成 atomic claims，再按“任一 contradictory→整句 contradictory；否则任一 inconclusive→整句 inconclusive”聚合；DeepFact-Eval直接判 sentence。该适配保证输出空间可比，但 decomposition error 与保守聚合可能额外压低传统 baseline（PDF p.17，§C.1）。

### Q4. 模型、token、tool、prompt、oracle 与成本差异

- `[AUTHOR_FACT]` Table 2 的 GPT-4.1 主比较使用相同 backbone 名称，但 verifier scaffold、可读信息范围、检索深度与 token budget显著不同；DeepFact-Eval 另用 GPT-4.1 mini 做全文摘要（PDF p.8，Table 2；PDF p.17，§C.2）。
- `[AUTHOR_FACT]` Full DeepFact-Eval 每 claim 平均 516.9K input tokens、18.6K output、估算 `$1.16`；Group=5 为 131.4K/4.9K/$0.30，Group=10 为 93.5K/3.5K/$0.21（PDF p.8，Table 2）。
- `[AUTHOR_FACT]` GPT-Researcher Deep/Deep+ 分别为 52.3K/9.0K/$0.18 与 83.3K/13.9K/$0.28；提高 Deep+ search budget 后 accuracy 反从 69.1 降至 68.3（PDF p.8–9，Table 2，§8.2）。
- `[AUTHOR_FACT]` 成本只按 2025-12-23 OpenAI token 价格估算；GPT-4.1 mini 用价格比折算为 GPT-4.1 equivalent cost。传统 snippet pipelines 的 token/cost 留空，理由是“negligible”（PDF p.8，§8.2；PDF p.17，§C.2）。
- `[READER_INTERPRETATION]` 该成本不含搜索服务、网页获取、embedding、文档存储/解析、并发基础设施与失败重试；“每 claim cost”也未说明 group variant 的组构造成本。因此它是 API token estimate，不是端到端运维成本。
- `[AUTHOR_FACT]` 主 benchmark 的隐藏 oracle 是 micro-gold known answers；120/143 test micro-golds 为人工构造 adversarial claims。unsupported micro-golds 由作者注入并手工确认错误，supported micro-golds先经 LLM entailment check 再 human review（PDF p.4，§4.1；PDF p.5，§6.1）。
- `[READER_INTERPRETATION]` micro-gold 既用于报告每轮 benchmark accuracy，又用于 post-release Challenger gate；反复用同一 hidden set 选择是否触发 evolution 会逐渐把它从“未触碰测试”变成 maintenance validation set，长期存在 selection/overfitting 风险（PDF p.8，§7.4；PDF p.24，§H）。
- `[OPEN_QUESTION]` 论文未说明 micro-gold 标识/标签是否随 v4 公开。若公开，后续 Challenger gate 可被直接针对；若完全隐藏，第三方无法复核 60.8→90.9 与触发规则。

### Q5. 作者限制、负向结果和未测试边界

- `[AUTHOR_FACT]` 作者承认 verifier 只能依据现有文献，不能通过新实验或模拟验证；当文献沉默或冲突时存在 epistemic limit（PDF p.10，Limitations）。
- `[AUTHOR_FACT]` 长上下文与迭代检索使 deep verification 昂贵，限制实时使用；lite variant 仍以 accuracy 损失换效率（PDF p.10，Limitations；PDF p.8，Table 2）。
- `[AUTHOR_FACT]` Group=5 相比 full accuracy 从 83.4 降至 77.9（-5.5 points），Group=10 降至 76.3（-7.1 points）；作者称其为 minor loss（PDF p.8–9，Table 2，§8.2）。
- `[AUTHOR_FACT]` GPT-Researcher 增加 search depth 后成本从 `$0.18` 升到 `$0.28`，accuracy 从 69.1 降至 68.3，构成明确负向 compute-scaling 结果（PDF p.8–9，Table 2）。
- `[AUTHOR_FACT]` Human audit 仍会被错误 agent 误导：micro-gold flow `H:1→A:0→H':0` 为 2.8%；另有 5.6% 在 agent 正确时仍保持错误，11.2% human/agent 同错且未改善（PDF p.6，Table 1）。
- `[AUTHOR_FACT]` 更严格的 human+agent 双同意 gate 在 Round 2 提高 86.0→88.0，却在 Round 3 降低 90.9→90.2，显示 conservativeness 会冻结可避免错误（PDF p.7，§7.3）。
- `[AUTHOR_FACT]` DeepFact-Eval 的案例错误包括：找到表面匹配 citation 却没有追查底层被引工作，以及忽略长句中的 niche taxonomy sub-claim（PDF p.28–30，§L.3）。
- `[READER_INTERPRETATION]` 未测试边界包括真正开放的实时事实、非公开/付费文献、非英语资料、source manipulation、retrieval poisoning、同一方法家族以外的强 Challenger、长期多版本 reviewer drift，以及 post-release agent-only maintenance 的真实误修订率。

### Q6. 可抽取的 Operator 与真实 Failure

- `[READER_INTERPRETATION]` **Operator O1：disagreement-gated Audit-then-Score。** 先由 Challenger 独立预测，只把 label disagreement 连同证据送审，accepted update 先改变版本化 gold 再评分（PDF p.2、5、22，Figure 1，Algorithm 1）。
- `[READER_INTERPRETATION]` **Operator O2：hidden micro-gold calibration。** 在高认知负荷、无完整 gold 的 benchmark 中嵌入 known-answer probes，持续估计 label/auditor 质量，并作为维护/停止信号（PDF p.4，§4.1；PDF p.24，§H）。
- `[READER_INTERPRETATION]` **Operator O3：breadth-to-depth verification。** 先广搜并摘要多个 sources，再对摘要做 claim-critical Q&A，反思证据是否充分；grouped variant 复用语义相关 claims 的 evidence（PDF p.5–6，Figure 2，§6.2）。
- `[AUTHOR_FACT]` **真实 Failure F1：one-shot expert gold 脆弱。** 在 hidden known-answer micro-golds 上，专家 seed accuracy 为 60.8%；同一 claims 经三轮 evidence-backed audit 后 benchmark micro-gold accuracy 为 90.9%（PDF p.1–2，Abstract/§1；PDF p.6，Figure 3）。
- `[READER_INTERPRETATION]` 这一结果证明“有限时 one-shot label 在所构造 probes 上错误率高”，但不能直接推出全部自然 benchmark items 也只有 60.8%：micro-golds 有 1:4 supported/unsupported 配比、25% hidden-test 注入、且多数为 adversarial modification（PDF p.4，§4.1）。
- `[OPEN_QUESTION]` 论文未报告 micro-gold class-wise confusion 或 majority baseline。按 1:4 配比，若 micro-gold accuracy 是普通二分类/两类 exact accuracy，恒猜 unsupported 可达 80%；这不否认专家有 39.2% 错误，却说明 raw accuracy 的解释需要类别分解。
- `[READER_INTERPRETATION]` **真实 Failure F2：同错不审计。** Algorithm 1 仅以 `ŷ≠y` 触发 proposal；benchmark 与 Challenger 共用错误 label，或 label 相同但依据错误，均无法修订 rationale。这是协议结构上的实际审计盲点（PDF p.22，lines 8–10）。
- `[READER_INTERPRETATION]` **真实 Failure F3：method-family benchmark dependence。** DeepFact-Eval GPT-4.1/GPT-5 参与 v4 的 Round 2/3 演化，随后同方法在 v4 上评测；accepted proposal 会直接成为新 rationale/label。Human audit 限制了单方面改写，但 head-to-head 仍不是 verifier-naive benchmark（PDF p.6，§6.3；PDF p.8，Table 2）。
- `[AUTHOR_FACT]` **真实 Failure F4：retrieval/nuance 漏检。** 作者案例明确展示 DeepFact-Eval 因未检查底层 citation 和忽略 NQ 是 single-hop 的 niche detail 而误判 Supported（PDF p.29–30，§L.3）。
- `[READER_INTERPRETATION]` **潜在 Failure P1：accepted-update scoring circularity。** Challenger 对被接受 proposal 的 label 由错变对；若 auditor 被说服能力、rationale 风格或同模型家族偏差影响，score 会吸收该偏差。版本化能追踪变化，但不能自行提供外部真值。
- `[READER_INTERPRETATION]` **潜在 Failure P2：adversarial micro-gold context leakage。** Task 定义要求 `c_i` 是 `d_i` 的 verbatim sentence，但 unsupported micro-gold 由修改 authentic sentence 产生；附录同时展示 original 与 adversarial sentence。论文未说明 `d_i` 是否同步替换。若保留原报告原句，context 会直接暴露篡改差异；若同步替换，则不再保留原 DRR（PDF p.3–4，§3.1、§4.1；PDF p.26–27，§L.1）。
- `[READER_INTERPRETATION]` **潜在 Failure P3：consensus/credibility 未操作化。** Supported 定义要求不存在 equally/more credible contradiction，但 DeepFact-Eval 没有公开 source credibility、study quality 或 scientific consensus 的形式评分；其“broader literature”能力主要由端到端结果和案例间接支持（PDF p.14，Table 3；PDF p.5–6，§6.2）。

### Q7. 核心证据定位表

| 主题 | 标签与证据 | 精确定位 |
|---|---|---|
| AtS 流程 | `[AUTHOR_FACT]` disagreement→proposal→audit→update→score。 | PDF p.2、5，Figure 1，§5.1；PDF p.22，Algorithm 1 |
| versioned state | `[AUTHOR_FACT]` item 保存 claim、DRR、current verdict、rationale。 | PDF p.4–5，§5.1–6.1 |
| expert one-shot | `[AUTHOR_FACT]` hidden micro-gold accuracy 60.8%。 | PDF p.4，§4.3 |
| audit 后质量 | `[AUTHOR_FACT]` 三轮后 micro-gold accuracy 90.9%。 | PDF p.6，Figure 3，§7.1 |
| micro-gold 构造 | `[AUTHOR_FACT]` 1:4 supported/unsupported；注入项作者验证，supported 经 LLM+human。 | PDF p.4，§4.1 |
| DeepFact-Eval 输入 | `[AUTHOR_FACT]` claim sentence+完整 DRR context。 | PDF p.3、5，§3.1、§6.2 |
| 检索配置 | `[AUTHOR_FACT]` 2 iterations、5 queries/step、40 sources、8192 completion tokens。 | PDF p.17，§C.3 |
| verifier 成本 | `[AUTHOR_FACT]` full 516.9K/18.6K/$1.16；group10 93.5K/3.5K/$0.21。 | PDF p.8，Table 2 |
| 强 baseline | `[AUTHOR_FACT]` FIRE 58.5，GPT-Researcher 69.1，DeepFact 83.4。 | PDF p.8，Table 2 |
| 共演化依赖 | `[AUTHOR_FACT]` Round2/3 Challenger 为 DeepFact-Eval GPT-4.1/GPT-5。 | PDF p.6，§6.3 |
| audit blind spot | `[AUTHOR_FACT]` 只有 `ŷ_i≠y_i` 才加入 proposal。 | PDF p.22，Algorithm 1 lines 8–10 |
| 真实模型失败 | `[AUTHOR_FACT]` citation nuance 与 niche sub-claim 两类误判。 | PDF p.28–30，§L.3 |

### Q8. parsed text 与 visual PDF 是否冲突？

- `[READER_INTERPRETATION]` 31/31 页完成顺序 parsed-text 核验与逐页视觉渲染；正文、Figure 1–7、Table 1–8、Algorithm 1、成本列和案例均未发现解析错位造成的事实冲突。
- `[READER_INTERPRETATION]` PDF p.2 的 AtS 箭头顺序、p.6–7 的嵌套 bar/flow table、p.8 的性能/成本大表、p.9 的外部数据集饼图、p.18–21 的争议案例表、p.22 的算法和 p.31 的 taxonomy 已单独视觉核对，数值/字段与 parsed text 一致。
- `[READER_INTERPRETATION]` 发现的是论文内部方法张力而非解析冲突：宣称 labels/rationales 可修订，但 Algorithm 1 不允许“同 label、改 rationale”的 proposal；宣称 frozen v4 上公平比较，但 v4 已由 DeepFact-Eval 方法家族参与演化；micro-gold 的 verbatim/context 处理未说明。

## 3. 逐页覆盖账本

| PDF 页 | 覆盖内容与核验结果 |
|---:|---|
| 1 | `[AUTHOR_FACT]` 标题、摘要、引言与专家 60.8% 发现；文本/视觉一致。 |
| 2 | `[AUTHOR_FACT]` Figure 1、AtS 流程、v4 与主要贡献；文本/视觉一致。 |
| 3 | `[AUTHOR_FACT]` 相关工作、三类 sentence-level task、静态 gold 问题；文本/视觉一致。 |
| 4 | `[AUTHOR_FACT]` micro-gold 构造、expert study、AtS state 起始；文本/视觉一致。 |
| 5 | `[AUTHOR_FACT]` Figure 2、AtS 公式、治理、Bench/Eval 定义；文本/视觉一致。 |
| 6 | `[AUTHOR_FACT]` Figure 3、四轮 rollout、human audit flow；文本/视觉一致。 |
| 7 | `[AUTHOR_FACT]` Figure 4、agent auditors、频率/strictness/cost；文本/视觉一致。 |
| 8 | `[AUTHOR_FACT]` Table 2、维护 gate、baseline 与主结果；文本/视觉一致。 |
| 9 | `[AUTHOR_FACT]` Figure 5、group cost trade-off、外部 benchmark 审计、结论；文本/视觉一致。 |
| 10 | `[AUTHOR_FACT]` Limitations、Ethics、参考文献起始；文本/视觉一致。 |
| 11 | `[AUTHOR_FACT]` 参考文献；文本/视觉一致。 |
| 12 | `[AUTHOR_FACT]` 参考文献；文本/视觉一致。 |
| 13 | `[AUTHOR_FACT]` 参考文献结束、Appendix A/B pilot 起始；文本/视觉一致。 |
| 14 | `[AUTHOR_FACT]` Table 3 label 定义与 pilot design implications；文本/视觉一致。 |
| 15 | `[AUTHOR_FACT]` Figure 6、expert recruitment、DRR 生成起始；文本/视觉一致。 |
| 16 | `[AUTHOR_FACT]` Figure 7、prompt/report generation、audit rounds 起始；文本/视觉一致。 |
| 17 | `[AUTHOR_FACT]` audit rounds、post-hoc check、baseline mapping、成本/超参；文本/视觉一致。 |
| 18 | `[AUTHOR_FACT]` Table 4 SciFact disagreements 与外部数据 setup；文本/视觉一致。 |
| 19 | `[AUTHOR_FACT]` ExpertQA/Factcheck setup、blind re-annotation 与估算结果；文本/视觉一致。 |
| 20 | `[AUTHOR_FACT]` disagreement taxonomy、risk-stratified sampling、bootstrap 起始；文本/视觉一致。 |
| 21 | `[AUTHOR_FACT]` Table 5 外部 benchmark 争议案例；文本/视觉一致。 |
| 22 | `[AUTHOR_FACT]` Algorithm 1 完整 AtS 流程；文本/视觉一致。 |
| 23 | `[AUTHOR_FACT]` Table 6–7、report-level bootstrap 与 CI；文本/视觉一致。 |
| 24 | `[AUTHOR_FACT]` benchmark governance、hidden monitoring、版本报告与相关工作；文本/视觉一致。 |
| 25 | `[AUTHOR_FACT]` 多 agent 区别、AI use、release/intended use；文本/视觉一致。 |
| 26 | `[AUTHOR_FACT]` adversarial collection/analysis error examples；文本/视觉一致。 |
| 27 | `[AUTHOR_FACT]` adversarial generalization 与 DRR analysis error；文本/视觉一致。 |
| 28 | `[AUTHOR_FACT]` collection/overclaim errors 与 Eval failure 起始；文本/视觉一致。 |
| 29 | `[AUTHOR_FACT]` Eval success 与 citation nuance failure；文本/视觉一致。 |
| 30 | `[AUTHOR_FACT]` niche detail failure；文本/视觉一致。 |
| 31 | `[AUTHOR_FACT]` Table 8 DRR factuality error taxonomy；文本/视觉一致。 |

## 4. 关键未决问题

1. `[OPEN_QUESTION]` 一条自然 claim 通常由几位独立 expert 审核？正文强调多 expert 不现实，但没有逐 item 冗余度与 auditor escalation 规则。
2. `[OPEN_QUESTION]` 60.8→90.9 有多少来自 audit role，有多少来自同一 claim 的重复暴露、更多时间、逐轮更强模型和直接提供 evidence？当前设计不能分离这些因素。
3. `[OPEN_QUESTION]` micro-gold 的 class-wise accuracy、混淆矩阵、majority baseline 与自然 claim 难度匹配如何？
4. `[OPEN_QUESTION]` adversarial `c_i` 是否同步写回完整 `d_i`；若不同步，claim 不再 verbatim 且上下文可能泄露原句。
5. `[OPEN_QUESTION]` Challenger 是否看到 incumbent label/rationale？Algorithm 1 调用 `M(c_i,d_i)` 表示不看，但 §6.3 “conditioned on previous consensus”措辞可能指 benchmark round state，需实现确认。
6. `[OPEN_QUESTION]` 同 label 但 rationale 错误/过时的项目如何更新；现有 proposal gate 不允许这种维护。
7. `[OPEN_QUESTION]` DeepFact-Eval 参与 v4 后，是否存在由从未参与构建的 verifier family 做独立审计/测试的 held-out benchmark 版本？
8. `[OPEN_QUESTION]` hidden micro-gold 如何在公开 release、可复现性与 post-release gate 防泄漏之间平衡？
9. `[OPEN_QUESTION]` source credibility、retraction/currency、conflicting literature 与 consensus 的操作化规则是什么；是否有 uncited/cited、single-source/multi-source 分层指标？
10. `[OPEN_QUESTION]` `$1.16/claim` 是否包含搜索、embedding、网页访问与失败重试；一个数百 claim DRR 的端到端 wall-clock/总成本未报告。
11. `[OPEN_QUESTION]` agent-only audit 只在 micro-gold 上验证；对无 known answer 的自然 claims，是否会形成同模型家族的共识漂移？
12. `[OPEN_QUESTION]` 外部 benchmark 的“估算准确率”多由 disagreement-only、子样本 extrapolation 或作者 inspection 得出，完整独立重标后结果是否仍成立？

## 5. 独立阅读结语

- `[READER_INTERPRETATION]` AtS 最可复用的机制是把 benchmark 的 label、evidence rationale、版本和变更 provenance 纳入正式评测协议，并用 hidden probes 监控人机审计质量。
- `[READER_INTERPRETATION]` one-shot expert 60.8% 是有力的脆弱性信号，但其结论边界是 adversarial、类别不平衡且重复审计的 micro-gold；非 micro-gold 自然 claims 没有独立 truth，可依赖的是版本化证据审计而非“已知 90.9% 总体准确”。
- `[READER_INTERPRETATION]` DeepFact-Eval 的核心增益既来自 breadth-to-depth workflow，也来自显著更大的信息与 token budget；Group=10 的近成本对照仍保留 +7.2 points，是比 full-vs-baseline 更干净的证据。
- `[READER_INTERPRETATION]` hidden-gold、disagreement-only gate 与 benchmark–verifier 共演化是该框架必须长期治理的三条边界；版本化提升可审计性，但不会自动消除共享盲点、选择偏差或 evaluator-family leakage。
