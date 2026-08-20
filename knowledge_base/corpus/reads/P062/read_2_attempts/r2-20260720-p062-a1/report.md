# P062 独立二读报告

## 0. 读取身份、边界与完整性

- `[AUTHOR_FACT]` 论文：Yi Yu 等，*Agentic Memory: Learning Unified Long-Term and Short-Term Memory Management for Large Language Model Agents*，ACL 2026 Long Papers，ACL Anthology 标识 `2026.acl-long.981`（PDF p.1，标题页）。
- `[AUTHOR_FACT]` 本次唯一论文源为 `knowledge_base/staging/plan05_sat_a1/P062_agentic_memory_unified.pdf`；实测 SHA256 为 `ba41464f84dbd8e0d0aeb1e6e0d7fd83b4086b2922579b88f7947448a8e1958f`，与 invocation 冻结值一致；PDF 共 27 页。
- `[READER_INTERPRETATION]` Provenance: reused independent reader thread due platform thread cap
- `[READER_INTERPRETATION]` 本报告只读取了本 attempt 的 `invocation.md`、其中内嵌冻结 prompt、指定 PDF 与已经在同一复用线程中完成复核的必要规则；未读取 read_1、Cards、其他报告、saturation 或 retrieval 材料。
- `[READER_INTERPRETATION]` 已按 PDF p.1–27 顺序提取并核验每页文本，且逐页执行内存视觉渲染复核；每页均有非空文本，未发现解析文本与视觉版面之间的实质冲突。

## 1. 一句话技术结论

- `[AUTHOR_FACT]` AgeMem 把语言生成与六种记忆操作放入同一 LLM policy 的混合动作空间：LTM 为 ADD、UPDATE、DELETE，STM 为 RETRIEVE、SUMMARY、FILTER；训练采用三阶段轨迹和把终局 group-normalized advantage 广播到全轨迹每一步的 step-wise GRPO（PDF p.4–6，§3.1–3.4；Table 1；Eq. 5–6）。
- `[READER_INTERPRETATION]` 其“统一”首先成立在**动作接口与参数共享**层面，而非细粒度因果 credit assignment：同一终局 advantage 被无差别广播给成功轨迹中的所有记忆与推理动作，因此不能单独辨认某个 UPDATE、DELETE、FILTER 或 SUMMARY 是否真正有益（PDF p.6，§3.4；PDF p.18，Appendix A.3）。
- `[READER_INTERPRETATION]` 训练信号高度依赖 query、expected answer 和 LLM judge：任务正确性、Stage-1 存储质量、检索相关性及关键信息保留均直接或间接使用 `q`/`Aq`；这使当前实现更接近“带答案 oracle 的记忆策略训练”，其对无标准答案、持续变化环境的适用性尚未由实验建立（PDF p.4，§3.1；PDF p.6，§3.5；PDF p.17，Eq. 21–25）。

## 2. 冻结问题逐项回答

### Q1. 改变了什么 computation？

- `[AUTHOR_FACT]` 每一步状态写为 `s_t=(C_t,M_t,T)`，其中 `C_t` 是当前上下文，`M_t` 是持久记忆，`T` 包含 query `q`、上下文信息 `I_q`，并在训练时包含 expected answer `A_q`；policy `πθ(a_t|s_t)` 同时产生语言 token 或结构化记忆工具调用（PDF p.4，§3.1）。
- `[AUTHOR_FACT]` LTM 的三种状态变换是新增、按 `memory_id` 更新和删除；STM 的三种状态变换是把 top-k LTM 检索项写回上下文、把指定消息跨度压缩成摘要、以及按语义相似度阈值移除上下文消息（PDF p.4–5，§3.2；PDF p.12–16，Appendix A.1，Eq. 8–15，Figure 6–7）。
- `[AUTHOR_FACT]` 完整训练轨迹串联 Stage 1 LTM 构建、Stage 2 干扰下的 STM 控制、Stage 3 检索与任务执行；Stage 1→2 时清空 `C` 但保留 `M`，Stage 2→3 时保留 Stage-2 上下文并加入 query（PDF p.4–5，§3.1–3.3；PDF p.19–20，Algorithms 1、3–5）。
- `[READER_INTERPRETATION]` 相对“独立 LTM 管理器 + 静态 STM”或“触发式 LTM + 静态 STM”，关键计算改变是让同一生成 policy 在推理循环内选择异质记忆动作，并让同一终局任务结果反向影响早期存储与后期上下文操作；它没有引入新的可学习记忆编码器或显式 value model（PDF p.2，Figure 1；PDF p.3，§2；PDF p.6，Eq. 6）。

### Q2. 输入、输出、信息可见性与时序

- `[AUTHOR_FACT]` Stage 1 输入为 `I_q` 的逐轮采样消息，算法还会在每一步先对现有 LTM 做检索；输出是语言响应、可选 LTM 操作和累积后的 `M`（PDF p.18，Appendix A.3；PDF p.20，Algorithm 3）。
- `[AUTHOR_FACT]` Stage 2 输入是由 `DISTRACTORGEN(q)` 生成的干扰消息，`C` 被重置而 `M` 保留；输出是经过 FILTER/SUMMARY 等操作后的上下文与经验轨迹（PDF p.5，§3.3；PDF p.19–20，Algorithms 1、4；PDF p.27，§D.4）。
- `[AUTHOR_FACT]` Stage 3 接收正式 query `q`，沿用 Stage-2 上下文并访问 `M`，最终输出 `A_pred`；只有轨迹终点获得复合 reward，中间 `r_t` 通常为 0（PDF p.4，§3.1；PDF p.18、20，Appendix A.3，Algorithm 5）。
- `[AUTHOR_FACT]` 终局 reward 由任务、上下文、LTM 三项各占 `1/3` 再加违规罚分；K=8 个同题 rollout 的终局分数组内标准化后，被广播到该轨迹全部时间步（PDF p.6，§3.4–3.5；PDF p.17，Appendix A.2；PDF p.25，§C.4）。
- `[OPEN_QUESTION]` 正文明确把训练时 `A_q` 纳入 task specification 和 policy state，但没有说明 policy 是否被 mask 掉 `A_q`；若未屏蔽，expected answer 不只是 reward oracle，而可能成为动作生成的直接输入（PDF p.4，§3.1）。
- `[OPEN_QUESTION]` Algorithm 3/4 把 `q` 写入 `s_t=(C,M,q)`，而附录文字又称 Stage 1 “task query has not yet been revealed”；Stage 2 的干扰生成也以 `q` 为条件。论文没有给出实现级可见性屏蔽规则，因而无法排除 query leakage（PDF p.18，Appendix A.3；PDF p.19–20，Algorithms 1、3、4）。

### Q3. 最强/最近的组合基线

- `[AUTHOR_FACT]` 主表的 LTM 基线为 LangMem、A-Mem、Mem0、Mem0g，另有 No-Memory 和同工具但不做 RL 的 AgeMem-noRL；Qwen2.5-7B 上最强主表平均基线是 Mem0（37.14），AgeMem 为 41.96；Qwen3-4B 上最强主表平均基线是 A-Mem（45.74），AgeMem 为 54.31（PDF p.7–8，§4.1–4.2，Table 2）。
- `[AUTHOR_FACT]` 更接近“同样加入 STM 与 RL”的组合对照出现在 Appendix D.3：Qwen2.5-7B、三个任务平均值中 A-Mem+ST/RL 为 41.70，LangMem+ST/RL 为 41.56，Mem0+ST/RL 为 40.67，AgeMem 为 43.69；逐任务看，LangMem+ST/RL 在 ALFWorld 为 41.32，略高于 AgeMem 的 41.07（PDF p.26–27，§D.3，Table 7）。
- `[READER_INTERPRETATION]` 因此最近且总体最强的组合基线是 **A-Mem+ST/RL**；若按单任务，ALFWorld 的最强组合基线是 **LangMem+ST/RL**。这比只拿 AgeMem 对 LTM-only 主表基线更能隔离“统一 policy”本身的贡献。
- `[OPEN_QUESTION]` 组合基线只报告 Qwen2.5-7B 的三个任务，没有覆盖 Qwen3-4B、PDDL 和 BabyAI；统一设计在全部模型/任务上的净贡献仍未被等配对照完整验证（PDF p.26–27，§D.3，Table 7）。

### Q4. 模型、token、tool、prompt 与 oracle 差异

- `[AUTHOR_FACT]` 主实验 backbone 为 Qwen2.5-7B-Instruct 与 Qwen3-4B-Instruct；最大 context 8192 token、最大 response 2048 token，训练使用 8 张 48GB RTX 4090，K=8，KL 系数 0.1（PDF p.7，§4.1；PDF p.25，§C.4）。
- `[AUTHOR_FACT]` 作者称各 LTM 基线遵循官方代码和默认/推荐超参数；AgeMem-noRL 使用同一工具接口；RAG 变体用逐步余弦检索追加上下文替换 STM 工具（PDF p.25，§C.3）。
- `[AUTHOR_FACT]` AgeMem 的系统 prompt 强制 `<think>` 后二选一输出 `<tool_call>` 或 `<answer>`，并允许单步多个工具调用；论文给出了 AgeMem 的工具 schema，但没有给出所有基线的完整 prompt（PDF p.14–16，Appendix A.1，Figure 6–7）。
- `[AUTHOR_FACT]` HotpotQA 的 task judge 和 MQ evaluator 都是 Qwen-Max；MQ 将存储事实与 ground-truth supporting facts 比较，task judge 将 agent answer 与 ground-truth answer 比较（PDF p.24–25，§C.2）。
- `[AUTHOR_FACT]` 训练 reward 还使用 LLM 判断 Stage-1 存储是否为高质量、用 LLM 评估检索项与 query 的相关性，并用 expected answer `A_q` 计算任务正确性（PDF p.6，§3.5；PDF p.17，Eq. 17、23、25）。
- `[AUTHOR_FACT]` `DISTRACTORGEN` 是另一个 external LLM 模块，按 target query 条件化生成无共享实体/关键概念的自然对话式干扰；论文未在该段指定模型（PDF p.27，§D.4）。
- `[READER_INTERPRETATION]` 公平性仍无法完全审计：论文没有统一披露各基线的 system prompt、每轮工具调用上限、embedding encoder、外部 LLM 调用次数/成本、实际 context/token budget 是否严格相同，也没有给出全部基线的 token 与 tool-call 表；因此“同 backbone”不等于完整的推理预算等配（PDF p.7，§4.1；PDF p.25，§C.3–C.4）。

### Q5. 作者承认的限制、负结果与未测试范围

- `[AUTHOR_FACT]` 作者明确承认：工具集合固定；五个 benchmark 相对真实开放部署仍受控；未测试持续长期对话或真实用户互动；训练轨迹只来自 HotpotQA，未来需扩展到更丰富交互数据（PDF p.10，Limitations）。
- `[AUTHOR_FACT]` Qwen3-4B 的 `+LT` 在 SciWorld 从 47.89 降至 43.50（-4.4），说明单加 LTM 并非稳定增益（PDF p.26，Figure 9）。
- `[AUTHOR_FACT]` Qwen2.5 主表中 AgeMem 在 PDDL 为 17.31，低于 A-Mem 的 18.39；Qwen3 主表中 AgeMem-noRL 的部分任务也低于 No-Memory（PDF p.8，Table 2）。
- `[AUTHOR_FACT]` 完整 reward 虽提高任务与记忆质量，却增加 token 与工具调用：Qwen2.5 上 2078→2117 token、3.93→4.92 calls；Qwen3 上 2164→2191 token、7.21→8.67 calls（PDF p.9，Table 4；PDF p.26，Table 6）。
- `[AUTHOR_FACT]` 干扰数量从 3 增至 7 时 HotpotQA judge 分数由 0.549 降至 0.537；FILTER 阈值过低或过高也会损伤信息保留/选择质量（PDF p.9，Table 5；PDF p.27，Table 8）。
- `[READER_INTERPRETATION]` 论文未测试真正跨 session 的长周期记忆漂移、错误记忆修复、恶意或相互矛盾信息、存储规模增长、删除不可逆风险、judge/model 迁移、无 ground truth 任务，以及真实 API 成本/延迟。

### Q6. Operator 与真实 Failure

- `[READER_INTERPRETATION]` **Operator O1：统一异质动作 policy。** 在同一 policy/action loop 内联合选择 LTM 的写/改/删与 STM 的取/压/滤，而不是另设 memory manager；该 operator 的可观察产物是结构化工具调用与 `C/M` 状态变换（PDF p.2，Figure 1；PDF p.4–5，Table 1）。
- `[READER_INTERPRETATION]` **Operator O2：时序分离 curriculum。** 先暴露信息并写 LTM，再清空 STM 注入干扰，最后给 query 取回知识；其作用是强制早期存储决策对延迟任务结果负责（PDF p.4–5，§3.1–3.3）。
- `[READER_INTERPRETATION]` **Operator O3：终局相对 advantage 全轨迹广播。** 同题 K 个 rollout 组内归一化终局 reward，再把同一 advantage 写到每个 step（PDF p.5–6，Eq. 5–6）。
- `[READER_INTERPRETATION]` **Failure F1：oracle-coupled policy/reward。** `q/A_q` 既参与 state 定义又参与多项 judge/reward；若可见性未隔离，模型可能学会适配答案 oracle，而非一般化的长期价值估计（PDF p.4、6、17）。
- `[READER_INTERPRETATION]` **Failure F2：伪细粒度 credit。** 广播式 advantage 解决了“无信号”但没有解决“哪个动作有效”；成功轨迹中的冗余添加、错误删除或不必要摘要会获得同样正 advantage（PDF p.6，§3.4）。
- `[READER_INTERPRETATION]` **Failure F3：维护奖励可投机。** `R_maintenance=1[update or delete performed]` 只检查是否发生，不检查修改/删除是否正确、有用或安全，理论上直接奖励无益维护动作（PDF p.17，Eq. 24）。
- `[READER_INTERPRETATION]` **Failure F4：接口契约不一致。** 工具 schema 要求 DELETE 参数 `confirmation`，案例却调用 `confirmed`；SUMMARY schema 仅列 `all` 或数字，案例却使用 `full`。若实现严格解析，这两处示例会失败（PDF p.15–16，Figure 6–7；PDF p.21–22，§B.1–B.2）。
- `[READER_INTERPRETATION]` **Failure F5：对照混杂。** 主表把统一 STM+LTM+RL 系统与多种 LTM-only 默认实现比较；Appendix D.3 缓解该问题，但覆盖不足，且未报告全套预算/提示词等配（PDF p.7–8，Table 2；PDF p.26–27，Table 7）。

### Q7. 核心证据定位表

| 主题 | 标签与证据 | 精确定位 |
|---|---|---|
| 统一动作空间 | `[AUTHOR_FACT]` 语言生成与六种 LTM/STM 工具共同构成 action space。 | PDF p.4–5，§3.1–3.2，Table 1 |
| 三阶段时序 | `[AUTHOR_FACT]` Stage 1 写 LTM；Stage 2 reset STM 并注入 distractor；Stage 3 给 query 并协调检索/推理。 | PDF p.4–5，§3.1–3.3；PDF p.19–20，Algorithms 1、3–5 |
| step-wise GRPO | `[AUTHOR_FACT]` 终局组归一化 advantage 广播到轨迹所有 step。 | PDF p.5–6，§3.4，Eq. 5–6 |
| expected-answer oracle | `[AUTHOR_FACT]` 训练 task specification 含 `A_q`，task reward 由 judge 比较 `A_pred` 与 `A_q`。 | PDF p.4，§3.1；PDF p.6、14，Eq. 17 |
| 存储 oracle | `[AUTHOR_FACT]` 高质量 memory 由 LLM 基于 `q` 与 `A_q` 判定。 | PDF p.17，Eq. 23 |
| update/delete reward | `[AUTHOR_FACT]` 只要执行 update 或 delete，maintenance 指示奖励即为 1。 | PDF p.17，Eq. 24 |
| judge 模型 | `[AUTHOR_FACT]` HotpotQA answer judge 和 MQ evaluator 使用 Qwen-Max。 | PDF p.24–25，§C.2 |
| 主基线 | `[AUTHOR_FACT]` LangMem、A-Mem、Mem0、Mem0g、No-Memory、AgeMem-noRL。 | PDF p.7–8，§4.1，Table 2 |
| 最近组合基线 | `[AUTHOR_FACT]` LangMem/A-Mem/Mem0 均加入相同 ST/RL 扩展后再比较。 | PDF p.26–27，§D.3，Table 7 |
| 作者限制 | `[AUTHOR_FACT]` 固定工具、受控 benchmark、无真实长期交互、只用 HotpotQA 训练。 | PDF p.10，Limitations |

### Q8. parsed 与 visual PDF 冲突

- `[READER_INTERPRETATION]` 27/27 页均完成顺序文本解析与逐页视觉复核；标题、正文、公式、表格、图注、工具 schema、算法及附录在两种视图中一致，未发现需以视觉版面覆盖 parsed text 的冲突。
- `[READER_INTERPRETATION]` PDF p.2 的 Figure 1、p.8–9 与 p.26–27 的结果表/图、p.15–16 的工具 schema、p.17 的奖励公式、p.19–20 的算法是高风险版面，已单独核对视觉排版；数值和字段与解析文本一致。
- `[OPEN_QUESTION]` DELETE 的 `confirmation`/`confirmed` 与 SUMMARY 的 `all`/`full` 是论文内部跨页不一致，不是解析器造成的差异（PDF p.15–16 对 p.21–22）。

## 3. 逐页覆盖账本

| PDF 页 | 覆盖内容与核验结果 |
|---:|---|
| 1 | `[AUTHOR_FACT]` 标题、摘要、引言与问题动机；文本/视觉一致。 |
| 2 | `[AUTHOR_FACT]` Figure 1、C1–C3、统一框架和贡献；文本/视觉一致。 |
| 3 | `[AUTHOR_FACT]` LTM/STM/RL 相关工作与相对定位；文本/视觉一致。 |
| 4 | `[AUTHOR_FACT]` state/action/reward 形式化、三阶段状态与 Table 1；文本/视觉一致。 |
| 5 | `[AUTHOR_FACT]` 六工具功能、三阶段 curriculum、泛化论述、GRPO 开始；文本/视觉一致。 |
| 6 | `[AUTHOR_FACT]` advantage 广播、GRPO 目标、复合 reward、数据集；文本/视觉一致。 |
| 7 | `[AUTHOR_FACT]` 指标、基线、backbone、主结果、MQ/token 图；文本/视觉一致。 |
| 8 | `[AUTHOR_FACT]` Table 2、Figure 4、Table 3 及工具调用分析；文本/视觉一致。 |
| 9 | `[AUTHOR_FACT]` reward/threshold 消融、Table 4–5、结论；文本/视觉一致。 |
| 10 | `[AUTHOR_FACT]` Limitations 与参考文献起始；文本/视觉一致。 |
| 11 | `[AUTHOR_FACT]` 参考文献；文本/视觉一致。 |
| 12 | `[AUTHOR_FACT]` 参考文献结束与 Appendix A.1 RETRIEVE；文本/视觉一致。 |
| 13 | `[AUTHOR_FACT]` ADD/UPDATE/DELETE/SUMMARY/FILTER 定义；文本/视觉一致。 |
| 14 | `[AUTHOR_FACT]` tool-calling system prompt 与 reward 公式起始；文本/视觉一致。 |
| 15 | `[AUTHOR_FACT]` Figure 6 STM tool schema；文本/视觉一致。 |
| 16 | `[AUTHOR_FACT]` Figure 7 LTM tool schema；文本/视觉一致。 |
| 17 | `[AUTHOR_FACT]` Eq. 18–26 的 context/memory/penalty reward；文本/视觉一致。 |
| 18 | `[AUTHOR_FACT]` 完整训练和三阶段 rollout 的说明；文本/视觉一致。 |
| 19 | `[AUTHOR_FACT]` Algorithms 1–2 与 Case 1 起始；文本/视觉一致。 |
| 20 | `[AUTHOR_FACT]` Algorithms 3–5 与 Case 1；文本/视觉一致。 |
| 21 | `[AUTHOR_FACT]` UPDATE/DELETE/ADD 案例与 Case 2 起始；文本/视觉一致。 |
| 22 | `[AUTHOR_FACT]` FILTER/SUMMARY 案例与 Case 3 起始；文本/视觉一致。 |
| 23 | `[AUTHOR_FACT]` RETRIEVE 综合案例与数据集附录起始；文本/视觉一致。 |
| 24 | `[AUTHOR_FACT]` 数据集细节与 MQ judge prompt；文本/视觉一致。 |
| 25 | `[AUTHOR_FACT]` answer judge prompt、基线配置和训练配置；文本/视觉一致。 |
| 26 | `[AUTHOR_FACT]` Qwen3 消融、reward ablation、组合基线论述；文本/视觉一致。 |
| 27 | `[AUTHOR_FACT]` Table 7–8 与 distractor sensitivity；文本/视觉一致。 |

## 4. 关键未决问题

1. `[OPEN_QUESTION]` policy 实际输入是否屏蔽 `A_q`，Stage 1/2 是否屏蔽 `q`？代码级数据流未在论文中给出。
2. `[OPEN_QUESTION]` 判定 `N_high_quality` 的 LLM 是什么模型、什么 prompt、是否与 Qwen-Max 相同、是否会看到完整 expected answer？
3. `[OPEN_QUESTION]` `R_preservation` 的 key token/phrase 如何抽取，摘要中的同义改写如何被判为“保留”？
4. `[OPEN_QUESTION]` `R_maintenance` 是否在实际代码中另有质量门槛？论文公式只给出动作发生指示量。
5. `[OPEN_QUESTION]` UPDATE/DELETE 在 Stage 1 需要先获得 `memory_id`，而算法称每步自动 retrieval；这些自动检索是否计入 Table 3 工具调用、token 与成本没有说明。
6. `[OPEN_QUESTION]` 不同 baseline 是否使用完全相同的 context 8192、response 2048、轮数上限、检索 k、embedding、system prompt 与外部 judge 调用预算？
7. `[OPEN_QUESTION]` Table 7 的 “+ST/RL” 如何把同一 RL 扩展接到三种结构不同的 LTM 系统，训练步数与超参数是否完全一致？
8. `[OPEN_QUESTION]` 固定工具接口中的参数冲突（`confirmation`/`confirmed`、`all`/`full`）在真实实现中采用哪一套契约？

## 5. 独立阅读结语

- `[READER_INTERPRETATION]` 该工作最清晰、可复用的机制贡献是：把 LTM 与 STM 操作显式化为同一 policy 的工具动作，并用“信息暴露—干扰压力—延迟任务”的阶段结构训练联合控制。
- `[READER_INTERPRETATION]` 最需要谨慎对待的因果主张是“统一策略本身带来增益”：最接近的 ST/RL 增强基线确实仍低于 AgeMem 的三任务平均值，但覆盖范围有限，且 prompt、工具预算与 oracle 使用尚未完全等配公开。
- `[READER_INTERPRETATION]` 最关键的机制风险不是奖励稀疏本身，而是 oracle 可见性、全轨迹同 advantage 和无质量门槛的 update/delete 指示奖励三者叠加，可能把“会触发记忆工具”误当成“学会了正确的长期记忆维护”。
